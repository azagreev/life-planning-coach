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

    def test_all_four_platforms_built(self):
        """Every platform overlay must produce a SKILL.md after build."""
        missing = []
        for platform in ("claude", "grok", "kimi", "kimi-cli"):
            skill_path = PROJECT_ROOT / "platforms" / platform / "SKILL.md"
            if not skill_path.exists():
                missing.append(platform)
        assert not missing, (
            f"Platform builds missing: {missing}. "
            "Every overlay in references/platforms/*.overlay.yaml must "
            "produce a platforms/<name>/SKILL.md after `build-platform-skill.py all`."
        )

    def test_root_skill_matches_claude_platform_skill(self):
        assert ROOT_SKILL.read_text(encoding="utf-8") == CLAUDE_SKILL.read_text(
            encoding="utf-8"
        ), "Root SKILL.md must stay synced with platforms/claude/SKILL.md"


# ---------------------------------------------------------------------------
# Extended integrity guards (BACKLOG «SKILL.master integrity tests», RICE 80)
# ---------------------------------------------------------------------------


PERSONA_MODULES = [
    "mode_adhd.md",
    "mode_unemployed.md",
    "mode_elder.md",
    "mode_planning_friction.md",
]

ROUTING_SPECIAL_REFS = [
    # Non-phase routing entries that nonetheless must appear in the Routing Map.
    "emotion_regulation.md",  # Phase 0.5 ER Protocol
    "recovery_protocol.md",  # Pause > 7 days / hard week series
]

PERSISTENCE_MODES = [
    "full_persistence",
    "wiki_no_execution",
    "execution_no_wiki",
    "lean_conversation",
]


def _section_body(text: str, heading: str) -> str:
    """Return body of an H2 section by exact heading match, until the next H2.

    H3 subsections within the H2 are included in the body. Returns empty
    string if the heading is not present.
    """
    escaped = re.escape(heading)
    # `^##(?!#)` — exactly two `#` not followed by another `#` (i.e. H2, not H3+)
    pattern = re.compile(
        rf"^{escaped}\s*\n(.*?)(?=^##(?!#)|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


class TestRoutingMapCoverage:
    """Routing Map must reference every phase module and persona mode."""

    @pytest.fixture(scope="class")
    def references_dir(self) -> Path:
        return PROJECT_ROOT / "references"

    def test_routing_map_references_every_phase_module(
        self, master_text: str, references_dir: Path
    ) -> None:
        """Every `module_phase*.md` on disk must have a Routing Map row in master."""
        on_disk = sorted(p.name for p in references_dir.glob("module_phase*.md"))
        assert on_disk, "No module_phase*.md found in references/ — Tier 2 missing"

        unreferenced = [
            module for module in on_disk if module not in master_text
        ]
        assert not unreferenced, (
            f"SKILL.master.md doesn't reference these phase modules: {unreferenced}. "
            "Every phase module must appear in the Routing Map (so the master can "
            "actually route into it) and in the Tier 2 References block."
        )

    def test_master_references_all_four_persona_modes(self, master_text: str) -> None:
        """Persona Detection block must mention each `mode_*.md`."""
        missing = [m for m in PERSONA_MODULES if m not in master_text]
        assert not missing, (
            f"SKILL.master.md must reference all four persona modules. "
            f"Missing: {missing}. Persona Detection block routes into these — "
            "orphaning one means that persona becomes unreachable from Tier 1."
        )

    def test_routing_map_lists_special_phase_refs(self, master_text: str) -> None:
        """Routing Map must include ER (Phase 0.5) and Recovery protocol entries."""
        missing = [m for m in ROUTING_SPECIAL_REFS if m not in master_text]
        assert not missing, (
            f"SKILL.master.md Routing Map missing: {missing}. "
            "ER protocol and Recovery protocol are referenced from Gotchas / "
            "Safety; they must also appear in the routing table so the path is "
            "discoverable, not implicit."
        )


class TestPersistenceModesTable:
    """Persistence Mode table must enumerate all 4 gating modes."""

    def test_master_persistence_table_lists_all_four_modes(
        self, master_text: str
    ) -> None:
        missing = [mode for mode in PERSISTENCE_MODES if mode not in master_text]
        assert not missing, (
            f"SKILL.master.md Persistence Mode table must list all four gating "
            f"modes: {PERSISTENCE_MODES}. Missing: {missing}. "
            "state_v2_schema.md §5 defines these — drift between schema and "
            "master means users on one mode get inconsistent skill behaviour."
        )


class TestSafetySection:
    """Safety & Ethics section must exist with concrete warning signs."""

    def test_safety_ethics_section_present(self, master_text: str) -> None:
        # Either the dedicated heading or the conventional name; both acceptable.
        has_section = bool(
            re.search(
                r"###\s+\d*\.?\s*Safety\s*(?:&|и|and)\s*Ethics\b",
                master_text,
                re.IGNORECASE,
            )
        )
        assert has_section, (
            "SKILL.master.md must have a `### Safety & Ethics` (or numbered "
            "equivalent) subsection. This is load-bearing for crisis routing."
        )

    def test_safety_section_mentions_warning_signs(self, master_text: str) -> None:
        """Warning Signs must reference low scores + self-harm escalation path."""
        # Find the Safety section body — anchored on the heading.
        match = re.search(
            r"###\s+\d*\.?\s*Safety\s*(?:&|и|and)\s*Ethics\b(.*?)(?=^###?\s|\Z)",
            master_text,
            re.DOTALL | re.MULTILINE | re.IGNORECASE,
        )
        assert match, "Safety section missing — see test_safety_ethics_section_present"
        body = match.group(1)
        # Low-score signal — wording varies, but "< 3" or "ниже 3" is the canonical pattern
        assert re.search(r"<\s*3|ниже\s+3", body, re.IGNORECASE), (
            "Safety section must reference low-score signal (e.g. `< 3/10` in "
            "Wheel of Life) — this is the depression-screening trigger."
        )
        # Self-harm escalation — must mention explicit term + escalation
        assert "самоповреждении" in body or "самоповреждения" in body, (
            "Safety section must explicitly mention self-harm escalation "
            "(самоповреждении / самоповреждения) — this is the crisis trigger."
        )


class TestLanguageRulesEnforcement:
    """Forbidden directive words must appear ONLY in Language Rules section.

    The skill bans «надо», «должен», «провал» as coaching language. They appear
    quoted as bad examples inside Language Rules and Gotchas, but must not leak
    into Examples or Troubleshooting prose (where they'd model bad coaching).
    """

    @pytest.fixture(scope="class")
    def examples_body(self, master_text: str) -> str:
        # Section heading is `## Examples` (H2) in master.
        return _section_body(master_text, "## Examples")

    @pytest.fixture(scope="class")
    def troubleshooting_body(self, master_text: str) -> str:
        return _section_body(master_text, "## Troubleshooting")

    def test_examples_section_exists(self, examples_body: str) -> None:
        assert examples_body, "## Examples section must exist with content"

    def test_examples_avoid_forbidden_directive_words(self, examples_body: str) -> None:
        # Import helper lazily (only one test class uses it).
        from tests.helpers.forbidden_words import find_forbidden

        violations = find_forbidden(
            examples_body,
            ["надо", "должен", "провал"],
            allow_quoted=True,  # «...» Russian quotes are whitelisted
            case_sensitive=False,
        )
        assert not violations, (
            "SKILL.master.md `## Examples` section uses banned directive words "
            f"outside quoted speech: {violations}. The examples model good "
            "coaching — they must not use «надо»/«должен»/«провал» themselves "
            "(quoted occurrences inside «...» are fine — that's why we strip "
            "those first)."
        )

    def test_troubleshooting_avoid_forbidden_directive_words(
        self, troubleshooting_body: str
    ) -> None:
        from tests.helpers.forbidden_words import find_forbidden

        violations = find_forbidden(
            troubleshooting_body,
            ["надо", "должен", "провал"],
            allow_quoted=True,
            case_sensitive=False,
        )
        assert not violations, (
            "SKILL.master.md `## Troubleshooting` section uses banned directive "
            f"words outside quoted speech: {violations}."
        )


class TestFrontmatterRuntime:
    """Frontmatter must declare multi-platform runtime."""

    def test_runtime_is_multi_platform(self, master_frontmatter: dict) -> None:
        runtime = master_frontmatter.get("runtime", "")
        assert "multi-platform" in str(runtime).lower(), (
            f"SKILL.master.md frontmatter `runtime` must be «multi-platform», got "
            f"{runtime!r}. Platform-specific runtime values belong in overlay files."
        )
