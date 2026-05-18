"""
System tests for Anthropic Skill Structure Compliance.
Covers AC-16 through AC-21 from acceptance_criteria_v0.7.md.
AC-22 (Version Consistency) is covered by test_version_consistency.py.
"""

import subprocess
import re
import zipfile
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).parent.parent.parent
SKILL_MD = PROJECT_ROOT / "SKILL.md"
REFERENCES_DIR = PROJECT_ROOT / "references"
DIST_DIR = PROJECT_ROOT / "dist"

# Find versioned artifacts in dist/ (e.g., life-planning-coach-v0.6.1.zip)
_zip_files = sorted(DIST_DIR.glob("life-planning-coach-v*.zip"), reverse=True)
ZIP_PATH = _zip_files[0] if _zip_files else PROJECT_ROOT / "life-planning-coach.zip"


class TestYamlFrontmatter:
    """AC-16: YAML Frontmatter validity."""

    @pytest.fixture(scope="class")
    def frontmatter(self):
        """Extract YAML frontmatter from SKILL.md."""
        content = SKILL_MD.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        assert match, "SKILL.md must start with YAML frontmatter between --- and ---"
        return yaml.safe_load(match.group(1))

    def test_frontmatter_has_required_fields(self, frontmatter):
        """AC-16: frontmatter contains name, version, description."""
        for field in ("name", "version", "description"):
            assert field in frontmatter, f"YAML frontmatter missing required field: {field}"

    def test_name_is_kebab_case(self, frontmatter):
        """AC-16: name is kebab-case."""
        name = frontmatter["name"]
        assert re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name), (
            f"name '{name}' is not kebab-case"
        )

    def test_version_matches_git_tag(self, frontmatter):
        """AC-16 + AC-22: version matches latest git tag."""
        tag_result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        git_version = tag_result.stdout.strip().lstrip("v")
        yaml_version = str(frontmatter["version"]).lstrip("v")
        assert yaml_version == git_version, (
            f"SKILL.md version '{yaml_version}' != latest git tag '{git_version}'"
        )

    def test_description_has_trigger_marker(self, frontmatter):
        """AC-16: description contains trigger marker."""
        description = frontmatter.get("description", "")
        markers = ["Используй при:", "Триггеры:", "Когда использовать:", "Trigger phrases:", "Используй при запросах:"]
        assert any(m in description for m in markers), (
            f"description missing trigger marker. Expected one of: {markers}"
        )

    def test_description_has_trigger_phrases(self, frontmatter):
        """AC-16 + AC-20: description contains >=3 trigger phrases after marker."""
        description = frontmatter.get("description", "")
        # Find trigger section and count quoted/comma-separated phrases
        trigger_section_match = re.search(
            r"(?:Используй при:|Триггеры:|Когда использовать:|Trigger phrases:|Используй при запросах:)(.*)",
            description,
            re.DOTALL | re.IGNORECASE,
        )
        if not trigger_section_match:
            pytest.skip("No trigger section found — covered by test_description_has_trigger_marker")

        trigger_section = trigger_section_match.group(1)
        # Count quoted phrases or comma-separated items
        quoted = re.findall(r'["""'']([^"""'']+)["""'']', trigger_section)
        commas = [p.strip() for p in trigger_section.split(",") if len(p.strip()) > 3]
        phrases = quoted if quoted else commas
        assert len(phrases) >= 3, (
            f"Expected >=3 trigger phrases in description, found {len(phrases)}: {phrases[:10]}"
        )

    def test_no_forbidden_words_in_instructions(self):
        """AC-18: no 'claude' or 'anthropic' inside instructions body."""
        content = SKILL_MD.read_text(encoding="utf-8")
        # Extract everything after frontmatter
        body = re.sub(r"^---\s*\n.*?\n---", "", content, flags=re.DOTALL, count=1)
        # Whitelist: code blocks, file paths, frontmatter fields, example role labels
        # Remove code blocks
        body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
        # Remove inline code
        body = re.sub(r"`[^`]+`", "", body)
        # Remove markdown links (keep text)
        body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
        forbidden = ["claude", "anthropic"]
        for word in forbidden:
            # Allow if part of file path or technical term (e.g., AI_Instructions)
            matches = re.findall(rf"\b{word}\b", body, re.IGNORECASE)
            # Filter out: file names with underscores, Memory references, role labels in examples
            cleaned = [m for m in matches if not re.search(
                rf"{word}[\s_](?:Memory|Instructions|Code|Plugin)",
                body[max(0, body.lower().find(m.lower())-20):body.lower().find(m.lower())+len(m)+20],
                re.IGNORECASE
            )]
            if cleaned:
                # One more pass: allow in Examples section as role labels (**Claude**:)
                lines_with_match = [
                    line for line in body.splitlines()
                    if word.lower() in line.lower()
                    and not re.search(rf"^\s*\*\*{word}\s*\*\*:", line, re.IGNORECASE)
                ]
                assert not lines_with_match, (
                    f"Forbidden word '{word}' found in SKILL.md body:\n"
                    + "\n".join(lines_with_match[:3])
                )


class TestSkillMdSize:
    """AC-17: SKILL.md size budget."""

    def test_line_count(self):
        """AC-17: SKILL.md <= 500 lines (hard fail), warning at >400."""
        lines = SKILL_MD.read_text(encoding="utf-8").splitlines()
        line_count = len(lines)
        assert line_count <= 500, (
            f"SKILL.md has {line_count} lines (limit: 500). "
            "Move content to references/ for progressive disclosure."
        )
        if line_count > 400:
            pytest.warns(UserWarning, f"SKILL.md has {line_count} lines (soft limit: 400)")

    def test_word_count(self):
        """AC-17: SKILL.md <= 5000 words."""
        words = SKILL_MD.read_text(encoding="utf-8").split()
        word_count = len(words)
        assert word_count <= 5000, (
            f"SKILL.md has {word_count} words (limit: 5000)"
        )


class TestRequiredSections:
    """AC-18: Required sections present in SKILL.md."""

    @pytest.fixture(scope="class")
    def skill_content(self):
        return SKILL_MD.read_text(encoding="utf-8")

    def test_has_instructions_section(self, skill_content):
        assert "## Instructions" in skill_content, "Missing ## Instructions section"

    def test_has_examples_section(self, skill_content):
        assert "## Examples" in skill_content, "Missing ## Examples section"

    def test_examples_count(self, skill_content):
        """AC-18: minimum 2 Input -> Output examples."""
        examples_match = re.search(
            r"## Examples(.*?)(?=\n## [^#]|\Z)", skill_content, re.DOTALL
        )
        if not examples_match:
            pytest.skip("## Examples section not found")
        examples_section = examples_match.group(1)
        # Count "### Example N:" or "**Example N**" or "Input:" patterns
        example_headers = re.findall(r"(?:### |\*\*)Example \d+[:\*]", examples_section)
        inputs = re.findall(r"(?:Input:|User:|Пользователь:)", examples_section)
        count = max(len(example_headers), len(inputs))
        assert count >= 2, f"Expected >=2 examples in ## Examples, found {count} (headers={example_headers}, inputs={inputs})"


    def test_has_gotchas_or_troubleshooting(self, skill_content):
        has_gotchas = "## Gotchas" in skill_content
        has_troubleshooting = "## Troubleshooting" in skill_content
        assert has_gotchas or has_troubleshooting, (
            "Missing ## Gotchas or ## Troubleshooting section"
        )

    def test_has_privacy_section(self, skill_content):
        assert "## Privacy" in skill_content, "Missing ## Privacy & Data Handling section"

    def test_privacy_has_therapy_disclaimer(self, skill_content):
        """AC-18: Privacy section contains therapy disclaimer."""
        privacy_match = re.search(
            r"## Privacy.*?\n(.*?)(?=## |\Z)", skill_content, re.DOTALL | re.IGNORECASE
        )
        if not privacy_match:
            pytest.skip("Privacy section not found")
        privacy_section = privacy_match.group(1).lower()
        therapy_keywords = ["therapy", "психолог", "therapist", "mental health", "психотерап"]
        assert any(k in privacy_section for k in therapy_keywords), (
            "Privacy section missing therapy/psychologist disclaimer"
        )

    def test_privacy_has_consent_rule(self, skill_content):
        """AC-18: Privacy section contains user consent rule."""
        privacy_match = re.search(
            r"## Privacy.*?\n(.*?)(?=## |\Z)", skill_content, re.DOTALL | re.IGNORECASE
        )
        if not privacy_match:
            pytest.skip("Privacy section not found")
        privacy_section = privacy_match.group(1).lower()
        consent_keywords = ["consent", "согласи", "permission", "разрешен", "explicit"]
        assert any(k in privacy_section for k in consent_keywords), (
            "Privacy section missing user consent rule"
        )

    def test_instructions_are_numbered(self, skill_content):
        """AC-18: Instructions section uses numbered steps (1. or ### 1.)."""
        instructions_match = re.search(
            r"## Instructions.*?\n(.*?)(?=\n## [^#]|\Z)", skill_content, re.DOTALL
        )
        if not instructions_match:
            pytest.skip("## Instructions section not found")
        instructions_section = instructions_match.group(1)
        # Support: "1. text" or "### 1. text" or "### 1 text"
        numbered = re.findall(r"(?:^\s*\d+\.|###\s+\d+\.?)\s+", instructions_section, re.MULTILINE)
        assert len(numbered) >= 2, (
            f"Expected numbered instructions (e.g., 1. or ### 1.), found {len(numbered)}"
        )


class TestProgressiveDisclosure:
    """AC-19: Progressive Disclosure — heavy content in references/."""

    def test_references_dir_exists(self):
        assert REFERENCES_DIR.is_dir(), "references/ directory missing"

    def test_skill_md_links_to_references(self):
        """AC-19: SKILL.md contains explicit links to references/."""
        content = SKILL_MD.read_text(encoding="utf-8")
        links = re.findall(r"references/[\w_/-]+\.md", content)
        assert len(links) >= 3, (
            f"SKILL.md should reference >=3 files in references/, found {len(links)}"
        )

    def test_no_oversized_sections_in_skill_md(self):
        """AC-19: No section in SKILL.md exceeds 300 lines."""
        content = SKILL_MD.read_text(encoding="utf-8")
        sections = re.findall(r"## .*?(?=## |\Z)", content, re.DOTALL)
        for section in sections:
            lines = section.strip().splitlines()
            if len(lines) > 300:
                header = lines[0] if lines else "unknown"
                pytest.fail(
                    f"Section '{header}' has {len(lines)} lines (soft limit: 300). "
                    "Move content to references/ for progressive disclosure."
                )


class TestTriggeringPrecision:
    """AC-20: Description pushiness and concrete triggers."""

    @pytest.fixture(scope="class")
    def frontmatter(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        assert match
        return yaml.safe_load(match.group(1))

    def test_no_abstract_verbs_without_context(self, frontmatter):
        """AC-20: description avoids abstract verbs without context."""
        description = frontmatter.get("description", "")
        abstract_verbs = ["помогает", "улучшает", "оптимизирует", "поддерживает"]
        found = [v for v in abstract_verbs if v in description.lower()]
        if found:
            pytest.warns(
                UserWarning,
                f"Description contains abstract verbs: {found}. Consider making them concrete."
            )

    def test_description_is_pushy(self, frontmatter):
        """AC-20: description contains concrete user-facing triggers."""
        description = frontmatter.get("description", "")
        # Should NOT be a generic sentence; should have specific phrases
        assert len(description) >= 100, (
            "description is too short (<100 chars). Add trigger phrases."
        )
        assert len(description) <= 1024, (
            "description exceeds 1024 chars. Keep it concise and pushy."
        )


class TestZipStructure:
    """AC-21: ZIP packaging structure."""

    def test_zip_has_skill_folder_as_root(self):
        """AC-21: ZIP contains life-planning-coach/ directly at root."""
        zip_path = ZIP_PATH
        if not zip_path.exists():
            pytest.skip("ZIP not found — build with scripts/build-skill.sh")

        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            top_dirs = {name.split("/")[0] for name in names if "/" in name}
            assert "life-planning-coach" in top_dirs, (
                f"ZIP root missing life-planning-coach/. Top entries: {list(top_dirs)[:5]}"
            )
            # Check for nested duplicate
            nested = [n for n in names if n.startswith("life-planning-coach/life-planning-coach/")]
            assert not nested, f"Nested duplicate folder found: {nested[:3]}"

    def test_zip_contains_skill_md(self):
        """AC-21: ZIP contains SKILL.md inside skill folder."""
        zip_path = ZIP_PATH
        if not zip_path.exists():
            pytest.skip("ZIP not found — build with scripts/build-skill.sh")

        with zipfile.ZipFile(zip_path, "r") as zf:
            skill_md_in_zip = "life-planning-coach/SKILL.md" in zf.namelist()
            assert skill_md_in_zip, "ZIP missing life-planning-coach/SKILL.md"
