"""
System tests for SKILL.master.md integrity.

These checks keep the platform-agnostic source aligned with generated
platform artifacts and referenced progressive-disclosure files.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MASTER_PATH = PROJECT_ROOT / "SKILL.master.md"
ROOT_SKILL = PROJECT_ROOT / "SKILL.md"
CLAUDE_SKILL = PROJECT_ROOT / "platforms" / "claude" / "SKILL.md"
BUILD_SCRIPT = PROJECT_ROOT / "scripts" / "build-platform-skill.py"

REQUIRED_SECTIONS = [
    "## Instructions",
    "## Examples",
    "## Gotchas",
    "## Troubleshooting",
    "## Privacy & Data Handling",
    "## References",
]

FORBIDDEN_PLATFORM_TERMS = [
    "Claude Memory",
    "Claude",
    "Grok",
    "Kimi",
    "MCP",
    "Google Drive",
    "Google Calendar",
    "memory_space",
    "KIMI_REF",
    "render_file",
]


@pytest.fixture(scope="module")
def master_text():
    return MASTER_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def master_frontmatter(master_text):
    match = re.match(r"^---\n(.*?)\n---\n", master_text, re.DOTALL)
    assert match, "SKILL.master.md must start with YAML frontmatter"
    return yaml.safe_load(match.group(1))


def _master_body(text: str) -> str:
    return text.split("\n---\n", 1)[1]


class TestMasterFrontmatter:
    def test_master_frontmatter_required_fields(self, master_frontmatter):
        for field in ("name", "version", "description"):
            assert field in master_frontmatter, f"Missing frontmatter field: {field}"

    def test_master_version_matches_git_tag(self, master_frontmatter):
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        git_version = result.stdout.strip().lstrip("v")
        assert str(master_frontmatter["version"]).lstrip("v") == git_version

    def test_master_description_contains_trigger_phrases(self, master_frontmatter):
        description = master_frontmatter.get("description", "")
        assert "Используй при запросах:" in description
        trigger_tail = description.split("Используй при запросах:", 1)[1]
        triggers = [item.strip() for item in trigger_tail.split(",") if item.strip()]
        assert len(triggers) >= 10


class TestMasterStructure:
    def test_master_has_required_sections(self, master_text):
        for section in REQUIRED_SECTIONS:
            assert section in master_text, f"Missing required section: {section}"

    def test_master_uses_generic_assistant_examples(self, master_text):
        assert "**Assistant**:" in master_text
        assert "**Claude**:" not in master_text
        assert "**Grok**:" not in master_text
        assert "**Kimi**:" not in master_text

    def test_master_reference_links_exist(self, master_text):
        references = sorted(set(re.findall(r"`(references/[^`]+)`", master_text)))
        assert references, "Expected references links in SKILL.master.md"

        missing = []
        for reference in references:
            path = PROJECT_ROOT / reference
            if not path.exists():
                missing.append(reference)

        assert not missing, f"Missing referenced files/directories: {missing}"

    def test_master_body_is_platform_agnostic(self, master_text):
        body = _master_body(master_text)
        violations = []
        for term in FORBIDDEN_PLATFORM_TERMS:
            if term in body:
                violations.append(term)

        assert not violations, (
            "SKILL.master.md body must remain platform-agnostic. "
            f"Found: {violations}"
        )


class TestMasterPlatformSync:
    @pytest.fixture(scope="class", autouse=True)
    def rebuild_platforms(self):
        result = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), "all"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    def test_claude_platform_file_exists_after_build(self):
        assert CLAUDE_SKILL.exists()

    def test_root_skill_matches_claude_platform_skill(self):
        assert ROOT_SKILL.read_text(encoding="utf-8") == CLAUDE_SKILL.read_text(
            encoding="utf-8"
        ), "Root SKILL.md must stay synced with platforms/claude/SKILL.md"
