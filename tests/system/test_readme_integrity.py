"""
System tests for README.md integrity.

Ensures README stays synchronized with SKILL.md features and references.
"""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestReadmeIntegrity:
    """Ensure README.md reflects current project state."""

    @pytest.fixture(scope="class")
    def readme_content(self):
        return (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def skill_content(self):
        return (PROJECT_ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_readme_mentions_wheel_of_life_11_domains(self, readme_content):
        """README must mention 11 domains, not 8."""
        assert "11 сфер" in readme_content or "11 доменов" in readme_content, (
            "README.md does not mention 11 Wheel of Life domains. "
            "Update from 8 to 11 domains."
        )
        # Ensure old "8 сфер" is not present (unless in historical context)
        lines = readme_content.splitlines()
        for line in lines:
            if "8 сфер" in line and "архив" not in line.lower():
                pytest.fail(
                    f"README.md still mentions '8 сфер' in line: {line}"
                )

    def test_readme_mentions_stage_1_5(self, readme_content):
        """README must mention Stage 1.5 (Authentic Goal Filter)."""
        assert "Stage 1.5" in readme_content or "Фильтр аутентичных целей" in readme_content, (
            "README.md does not mention Stage 1.5. Add Authentic Goal Filter description."
        )

    def test_readme_mentions_communication_style(self, readme_content):
        """README must mention communication style adaptation."""
        assert "стил" in readme_content.lower() and (
            "коммуникац" in readme_content.lower() or "коучинг" in readme_content.lower()
        ), (
            "README.md does not mention communication style adaptation. "
            "Add Big Five / TTM / MI adaptive coaching description."
        )

    def test_readme_lists_core_references(self, readme_content):
        """README must list all core reference files (not archives/research)."""
        core_refs = [
            "diagnostic_methods.md",
            "authentic_goal_filter.md",
            "communication_style.md",
            "goal_architecture.md",
            "weekly_review.md",
            "science_backing.md",
            "dashboard_guide.md",
            "calendar_integration.md",
        ]
        for ref in core_refs:
            assert ref in readme_content, (
                f"README.md does not list core reference file: {ref}. "
                f"Add it to the project structure section."
            )

    def test_readme_links_to_github_releases(self, readme_content):
        """README must link to GitHub Releases for downloads."""
        assert "github.com/azagreev/life-planning-coach/releases" in readme_content, (
            "README.md must link to GitHub Releases page for skill downloads."
        )

    def test_skill_references_match_disk(self, skill_content):
        """SKILL.md must reference files that exist on disk."""
        references_dir = PROJECT_ROOT / "references"

        # Find all markdown file references in SKILL.md
        import re
        ref_links = re.findall(r'\[([^\]]+)\]\(references/([^)]+)\)', skill_content)
        ref_direct = re.findall(r'references/([a-zA-Z0-9_]+\.md)', skill_content)

        all_refs = set([name for _, name in ref_links] + ref_direct)

        for ref in all_refs:
            ref_path = references_dir / ref
            assert ref_path.exists(), (
                f"SKILL.md references {ref} but file does not exist in references/"
            )

    def test_no_forbidden_words_in_readme(self, readme_content):
        """README must not contain forbidden coaching words."""
        forbidden = ["надо", "должен", "провал"]
        lines = readme_content.splitlines()
        for i, line in enumerate(lines, 1):
            for word in forbidden:
                if word in line.lower():
                    # Allow in quotes describing what NOT to do
                    if "не используются" in line or "запрещён" in line or "forbidden" in line.lower():
                        continue
                    # Allow "провалы" in Life Story context (peak moments and failures)
                    if word == "провал" and ("пиковые" in line or "life story" in line.lower() or "моменты" in line):
                        continue
                    # Allow technical instructions ("должен показать статус", etc.)
                    if word == "должен" and ("коннектор" in line or "должен быть" in line or "статус" in line):
                        continue
                    pytest.fail(
                        f"Forbidden word '{word}' in README.md line {i}: {line}"
                    )
