"""
Multi-platform consistency tests for life-planning-coach skill adaptation.

Validates:
- SKILL.master.md is platform-agnostic
- Overlay files are valid YAML with required structure
- Generated platform files have correct frontmatter and no cross-contamination
- Claude skill size remains within limits
"""

import re
import subprocess
import yaml
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
MASTER_PATH = PROJECT_ROOT / "SKILL.master.md"
OVERLAY_DIR = PROJECT_ROOT / "references" / "platforms"
PLATFORMS_DIR = PROJECT_ROOT / "platforms"
BUILD_SCRIPT = PROJECT_ROOT / "scripts" / "build-platform-skill.py"

PLATFORMS = ["claude", "grok", "kimi"]

FORBIDDEN_IN_MASTER = [
    "Claude Memory",
    "Claude",
    "MCP",
    "Google Drive",
    "Google Calendar",
    "memory_space",
    "KIMI_REF",
    "Grok",
    "Kimi",
    "render_file",
]

# Some terms are allowed in specific contexts (e.g., "Google Calendar, Apple Calendar, Outlook" as examples)
ALLOWED_CONTEXTS = [
    # References to templates filenames are checked separately
]


class TestMasterFile:
    """AC-1: Master file is platform-agnostic."""

    def test_master_exists(self):
        assert MASTER_PATH.exists(), f"SKILL.master.md not found at {MASTER_PATH}"

    def test_master_has_frontmatter(self):
        text = MASTER_PATH.read_text(encoding="utf-8")
        assert text.startswith("---\n"), "Master file must start with YAML frontmatter"
        assert "\n---\n" in text, "Master file must have closing frontmatter delimiter"

    def test_master_has_no_platform_refs(self):
        text = MASTER_PATH.read_text(encoding="utf-8")
        body = text.split("\n---\n", 1)[1] if "\n---\n" in text else text
        for term in FORBIDDEN_IN_MASTER:
            if term in ["Claude", "Grok", "Kimi"]:
                # These names might appear in research references — only check main content
                count = body.count(term)
                assert count == 0, f"Platform-specific term '{term}' found {count} time(s) in master body"
            else:
                assert term not in body, f"Platform-specific term '{term}' found in master body"

    def test_master_has_generic_assistant_in_examples(self):
        text = MASTER_PATH.read_text(encoding="utf-8")
        # Examples should use "**Assistant**:" not a platform name
        assert "**Assistant**:" in text, "Master examples should use generic **Assistant** prefix"
        assert "**Claude**:" not in text, "Master should not contain **Claude** in examples"
        assert "**Grok**:" not in text, "Master should not contain **Grok** in examples"
        assert "**Kimi**:" not in text, "Master should not contain **Kimi** in examples"

    def test_master_references_ai_instructions_not_claude(self):
        text = MASTER_PATH.read_text(encoding="utf-8")
        assert "AI_Instructions.md" in text, "Master should reference AI_Instructions.md"
        assert "CLAUDE_Instructions.md" not in text, "Master should not reference CLAUDE_Instructions.md"


class TestOverlayFiles:
    """AC-2: Overlay files are valid and complete."""

    @pytest.mark.parametrize("platform", PLATFORMS)
    def test_overlay_exists(self, platform):
        overlay_path = OVERLAY_DIR / f"{platform}.overlay.yaml"
        assert overlay_path.exists(), f"Overlay not found: {overlay_path}"

    @pytest.mark.parametrize("platform", PLATFORMS)
    def test_overlay_is_valid_yaml(self, platform):
        overlay_path = OVERLAY_DIR / f"{platform}.overlay.yaml"
        content = overlay_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        assert isinstance(data, dict), f"Overlay {platform} must be a YAML dictionary"

    @pytest.mark.parametrize("platform", PLATFORMS)
    def test_overlay_has_replacements(self, platform):
        overlay_path = OVERLAY_DIR / f"{platform}.overlay.yaml"
        data = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
        assert "replacements" in data, f"Overlay {platform} must have 'replacements' key"
        assert isinstance(data["replacements"], list), f"Overlay {platform} replacements must be a list"
        assert len(data["replacements"]) > 0, f"Overlay {platform} must have at least one replacement"

    @pytest.mark.parametrize("platform", PLATFORMS)
    def test_overlay_replacements_have_old_and_new(self, platform):
        overlay_path = OVERLAY_DIR / f"{platform}.overlay.yaml"
        data = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
        for i, rep in enumerate(data.get("replacements", [])):
            assert "old" in rep, f"Overlay {platform} replacement {i} missing 'old'"
            assert "new" in rep, f"Overlay {platform} replacement {i} missing 'new'"
            assert isinstance(rep["old"], str), f"Overlay {platform} replacement {i} 'old' must be string"
            assert isinstance(rep["new"], str), f"Overlay {platform} replacement {i} 'new' must be string"


class TestGeneratedFiles:
    """AC-3, AC-4, AC-5: Generated platform files are correct."""

    @pytest.fixture(scope="class", autouse=True)
    def rebuild_platforms(self):
        """Ensure platform files are up-to-date before testing."""
        result = subprocess.run(
            ["python3", str(BUILD_SCRIPT), "all"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Build failed:\n{result.stderr}"

    @pytest.mark.parametrize("platform", PLATFORMS)
    def test_generated_file_exists(self, platform):
        skill_path = PLATFORMS_DIR / platform / "SKILL.md"
        assert skill_path.exists(), f"Generated skill not found: {skill_path}"

    @pytest.mark.parametrize("platform", PLATFORMS)
    def test_generated_has_frontmatter(self, platform):
        skill_path = PLATFORMS_DIR / platform / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        assert text.startswith("---\n"), f"{platform} skill must start with YAML frontmatter"

    @pytest.mark.parametrize("platform", PLATFORMS)
    def test_generated_has_required_sections(self, platform):
        skill_path = PLATFORMS_DIR / platform / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        required_sections = [
            "## Instructions",
            "## Examples",
            "## Gotchas",
            "## Troubleshooting",
            "## Privacy & Data Handling",
            "## References",
        ]
        for section in required_sections:
            assert section in text, f"{platform} skill missing required section: {section}"

    def test_claude_frontmatter(self):
        skill_path = PLATFORMS_DIR / "claude" / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        frontmatter = text.split("\n---\n", 1)[0]
        assert "min_claude_version:" in frontmatter, "Claude skill must have min_claude_version"
        assert "runtime: claude.ai" in frontmatter, "Claude skill must have runtime: claude.ai"
        assert "requires_mcp:" in frontmatter, "Claude skill must have requires_mcp"
        assert "requires_connector:" not in frontmatter, "Claude skill should not have requires_connector"

    def test_grok_frontmatter(self):
        skill_path = PLATFORMS_DIR / "grok" / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        frontmatter = text.split("\n---\n", 1)[0]
        assert "min_claude_version:" not in frontmatter, "Grok skill must not have min_claude_version"
        assert "requires_mcp:" not in frontmatter, "Grok skill must not have requires_mcp"
        assert "requires_connector:" not in frontmatter, "Grok skill must not have requires_connector"
        assert "runtime:" not in frontmatter, "Grok skill must not have runtime"

    def test_kimi_frontmatter(self):
        skill_path = PLATFORMS_DIR / "kimi" / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        frontmatter = text.split("\n---\n", 1)[0]
        assert "name:" in frontmatter, "Kimi skill must have name"
        assert "description:" in frontmatter, "Kimi skill must have description"
        assert "min_claude_version:" not in frontmatter, "Kimi skill must not have min_claude_version"
        assert "requires_mcp:" not in frontmatter, "Kimi skill must not have requires_mcp"
        assert "requires_connector:" not in frontmatter, "Kimi skill must not have requires_connector"
        assert "runtime:" not in frontmatter, "Kimi skill must not have runtime"
        assert "author:" not in frontmatter, "Kimi skill must not have author"
        assert "last_updated:" not in frontmatter, "Kimi skill must not have last_updated"

    def test_claude_size_limit(self):
        """Claude skill must be ≤500 lines (Anthropic limit)."""
        skill_path = PLATFORMS_DIR / "claude" / "SKILL.md"
        lines = skill_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 500, f"Claude skill has {len(lines)} lines, exceeds 500-line limit"

    def test_claude_word_count(self):
        """Claude skill must be ≤5000 words (Anthropic limit)."""
        skill_path = PLATFORMS_DIR / "claude" / "SKILL.md"
        words = skill_path.read_text(encoding="utf-8").split()
        assert len(words) <= 5000, f"Claude skill has {len(words)} words, exceeds 5000-word limit"


class TestNoCrossContamination:
    """Generated files must not contain wrong platform references."""

    @pytest.fixture(scope="class", autouse=True)
    def rebuild_platforms(self):
        result = subprocess.run(
            ["python3", str(BUILD_SCRIPT), "all"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Build failed:\n{result.stderr}"

    def test_grok_no_claude_refs(self):
        text = (PLATFORMS_DIR / "grok" / "SKILL.md").read_text(encoding="utf-8")
        # "Claude" as a standalone word (case-insensitive)
        matches = re.findall(r'\b[Cc]laude\b', text)
        # Allow "Google Calendar, Apple Calendar, Outlook" context
        allowed_phrases = ["Google Calendar", "Apple Calendar"]
        for phrase in allowed_phrases:
            matches = [m for m in matches if m.lower() not in phrase.lower()]
        assert len(matches) == 0, f"Grok skill contains {len(matches)} Claude reference(s): {matches[:5]}"

    def test_grok_no_mcp_refs(self):
        text = (PLATFORMS_DIR / "grok" / "SKILL.md").read_text(encoding="utf-8")
        assert "MCP" not in text, "Grok skill must not contain 'MCP'"

    def test_grok_no_kimi_refs(self):
        text = (PLATFORMS_DIR / "grok" / "SKILL.md").read_text(encoding="utf-8")
        assert "KIMI_REF" not in text, "Grok skill must not contain 'KIMI_REF'"
        assert "memory_space" not in text, "Grok skill must not contain 'memory_space'"

    def test_kimi_no_claude_refs(self):
        text = (PLATFORMS_DIR / "kimi" / "SKILL.md").read_text(encoding="utf-8")
        matches = re.findall(r'\b[Cc]laude\b', text)
        assert len(matches) == 0, f"Kimi skill contains {len(matches)} Claude reference(s)"

    def test_kimi_no_mcp_refs(self):
        text = (PLATFORMS_DIR / "kimi" / "SKILL.md").read_text(encoding="utf-8")
        assert "MCP" not in text, "Kimi skill must not contain 'MCP'"

    def test_kimi_no_grok_refs(self):
        text = (PLATFORMS_DIR / "kimi" / "SKILL.md").read_text(encoding="utf-8")
        assert "render_file" not in text, "Kimi skill must not contain 'render_file' (Grok-specific)"

    def test_claude_no_grok_refs(self):
        text = (PLATFORMS_DIR / "claude" / "SKILL.md").read_text(encoding="utf-8")
        assert "render_file" not in text, "Claude skill must not contain 'render_file'"

    def test_claude_no_kimi_refs(self):
        text = (PLATFORMS_DIR / "claude" / "SKILL.md").read_text(encoding="utf-8")
        assert "KIMI_REF" not in text, "Claude skill must not contain 'KIMI_REF'"
        assert "memory_space" not in text, "Claude skill must not contain 'memory_space'"


class TestBuildScript:
    """AC-3: Build script produces all platform artifacts."""

    def test_build_script_exists(self):
        assert BUILD_SCRIPT.exists(), f"Build script not found: {BUILD_SCRIPT}"

    def test_build_script_runnable(self):
        result = subprocess.run(
            ["python3", str(BUILD_SCRIPT), "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        # --help now prints usage and exits 0
        assert result.returncode == 0, f"--help failed: {result.stderr}"
        assert "Usage:" in (result.stdout + result.stderr), "Usage text not found in output"

    def test_build_outputs_all_platforms(self):
        result = subprocess.run(
            ["python3", str(BUILD_SCRIPT), "all"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Build failed:\n{result.stderr}"
        for platform in PLATFORMS:
            assert (PLATFORMS_DIR / platform / "SKILL.md").exists(), f"Missing output for {platform}"
