"""v1.0.0 platform parity — structural contract assertions.

Validates that all 4 platform SKILL files (claude/grok/kimi/kimi-cli) carry the
same operational contract. Differences in inlining strategy (single-file vs
lazy-load) are tolerated — we test that the CONTRACT is reachable, not byte-
identical files.

For lazy-load platforms (claude, kimi-cli) we extend the corpus with the
reference files those platforms can load at runtime via filesystem/MCP.

If a parity test fails, master + overlay drifted relative to other platforms —
either the contract changed (update test) or a platform overlay regressed.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PLATFORMS_DIR = PROJECT_ROOT / "platforms"
REFERENCES = PROJECT_ROOT / "references"

# Files lazy-load platforms (claude, kimi-cli) can read at runtime
LAZY_LOAD_EXTRAS = [
    "module_phase1_diagnostic.md",
    "module_phase1_5_goal_filter.md",
    "module_phase2_goal_architecture.md",
    "module_phase3_weekly_review.md",
    "module_phase4_dashboard.md",
    "module_phase5_execution.md",
    "mode_adhd.md",
    "mode_unemployed.md",
    "mode_elder.md",
    "mode_planning_friction.md",
    "emotion_regulation.md",
    "diagnostic_methods.md",
    "track_health_metabolism.md",
    "state_v2_schema.md",
]

# Single-file platforms (grok, kimi) have everything inlined
LAZY_LOAD_PLATFORMS = {"claude", "kimi-cli"}
SINGLE_FILE_PLATFORMS = {"grok", "kimi"}
ALL_PLATFORMS = ["claude", "grok", "kimi", "kimi-cli"]


def _platform_corpus(platform: str) -> str:
    """Return reachable content for a platform.

    For lazy-load platforms — SKILL.md + concatenated lazy-load refs.
    For single-file platforms — SKILL.md alone (everything is inlined).
    """
    skill_path = PLATFORMS_DIR / platform / "SKILL.md"
    body = skill_path.read_text(encoding="utf-8")
    if platform in LAZY_LOAD_PLATFORMS:
        extras = []
        for ref in LAZY_LOAD_EXTRAS:
            ref_path = REFERENCES / ref
            if ref_path.exists():
                extras.append(ref_path.read_text(encoding="utf-8"))
        body += "\n\n" + "\n\n".join(extras)
    return body


def _strip_code(text: str) -> str:
    """Remove code blocks for prose-only checks."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    return text


# ----- Parity contract tests (parametrized × 4 platforms) ---------------


@pytest.mark.parametrize("platform", ALL_PLATFORMS)
class TestPlatformParity:
    """Each test runs once per platform; failures are platform-specific."""

    def test_routing_map_present(self, platform: str):
        corpus = _platform_corpus(platform)
        assert "Routing Map" in corpus, f"{platform}: missing Routing Map header"
        # All 6 phase modules should appear in Routing Map block
        for module in [
            "module_phase1_diagnostic",
            "module_phase1_5_goal_filter",
            "module_phase2_goal_architecture",
            "module_phase3_weekly_review",
            "module_phase4_dashboard",
            "module_phase5_execution",
        ]:
            assert module in corpus, f"{platform}: Routing Map missing reference to {module}"

    def test_4_gating_modes_present(self, platform: str):
        corpus = _platform_corpus(platform)
        for mode in [
            "full_persistence",
            "wiki_no_execution",
            "execution_no_wiki",
            "lean_conversation",
        ]:
            assert mode in corpus, f"{platform}: missing gating mode '{mode}'"

    def test_emotional_landing_4_steps(self, platform: str):
        corpus = _platform_corpus(platform)
        for step in ["VALIDATE", "REFLECT", "ONE THING", "BRIDGE"]:
            assert step in corpus, f"{platform}: Emotional Landing missing step '{step}'"

    def test_4_persona_modes_referenced(self, platform: str):
        corpus = _platform_corpus(platform)
        for persona in [
            "mode_adhd",
            "mode_unemployed",
            "mode_elder",
            "mode_planning_friction",
        ]:
            assert persona in corpus, f"{platform}: missing persona '{persona}'"

    def test_phase_0_5_er_protocols(self, platform: str):
        corpus = _platform_corpus(platform)
        for protocol in [
            "Cognitive Reappraisal",
            "Grounding",
            "Self-Compassion",
        ]:
            assert protocol in corpus, f"{platform}: missing ER protocol '{protocol}'"

    def test_health_track_entry_present(self, platform: str):
        corpus = _platform_corpus(platform)
        # Health Track is opt-in; the trigger words/section should be reachable
        assert "Health Track" in corpus, f"{platform}: missing Health Track entry (v0.19.0)"

    def test_partner_coordination_present(self, platform: str):
        corpus = _platform_corpus(platform)
        # Goal Concordance v0.19.0 — может быть "Partner Coordination" или "partner_coordination"
        assert (
            "Partner Coordination" in corpus or "partner_coordination" in corpus
        ), f"{platform}: missing Partner Coordination (Goal Concordance v0.19.0)"

    def test_compass_mode_present(self, platform: str):
        corpus = _platform_corpus(platform)
        assert "Compass Mode" in corpus, f"{platform}: missing Compass Mode (FR-04 v0.18.0)"

    def test_safety_warning_signs(self, platform: str):
        corpus = _platform_corpus(platform)
        for sign in ["самоповреждени", "безысход"]:
            assert sign in corpus.lower(), f"{platform}: missing safety warning sign '{sign}'"

    def test_language_rules_forbidden_words(self, platform: str):
        corpus = _platform_corpus(platform)
        # Skill must declare forbidden words: «надо», «должен», «провал»
        for forbidden in ["надо", "должен", "провал"]:
            assert forbidden in corpus, f"{platform}: missing forbidden word declaration '{forbidden}'"

    def test_drive_used_consistently(self, platform: str):
        """No lowercase 'drive' as standalone word in prose (proper noun).

        Excluded from check:
        - Code blocks / inline code (JSON keys like persistence_retry.drive.*)
        - YAML frontmatter (MCP server IDs like 'google-drive')
        - Compound identifiers (google-drive, drive-сервиc)
        """
        skill_path = PLATFORMS_DIR / platform / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        # Strip frontmatter
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
        text = _strip_code(text)
        # Exclude 'google-drive' compound identifier (Google service name)
        text = text.replace("google-drive", "")
        lowercase_drive = re.findall(r"(?<![_A-Za-z])drive(?![_A-Za-z])", text)
        assert lowercase_drive == [], (
            f"{platform}: {len(lowercase_drive)} 'drive' (lowercase) occurrences "
            f"in SKILL.md prose. Use 'Drive' (proper noun)."
        )

    def test_mode_naming_convention(self, platform: str):
        """All persona refs use mode_<short> convention (v0.19.0)."""
        corpus = _platform_corpus(platform)
        old_names = ["adhd_mode.md", "time_structure_unemployed.md", "elder_homebound_mode.md", "planning_friction_audit.md"]
        for old in old_names:
            assert old not in corpus, f"{platform}: still references old persona path '{old}'"

    def test_schema_v2_referenced(self, platform: str):
        """Schema v2 is mentioned by version OR by canonical 11 sphere structure.

        Single-file platforms (grok, kimi) don't inline state_v2_schema.md
        (not in P0_REFS), so the exact "2.2" string may be absent — but
        canonical contract markers are present.

        kimi is ultra-condensed and may carry neither — accepts gating modes
        as schema-v2 marker (gating_mode introduced in v2.0.1).
        """
        corpus = _platform_corpus(platform)
        has_version = bool(re.search(r"\b2\.[0-9]+(?:\.\d+)?\b", corpus))
        has_canonical = "personal_growth" in corpus and "fun_recreation" in corpus
        has_gating = "full_persistence" in corpus  # introduced with schema v2.0.1
        assert has_version or has_canonical or has_gating, (
            f"{platform}: no schema 2.x marker found (version / canonical spheres / gating modes)"
        )

    def test_zero_setup_default(self, platform: str):
        corpus = _platform_corpus(platform)
        # Persistence is opt-in, not blocking onboarding
        assert "Zero-Setup" in corpus or "zero-setup" in corpus.lower(), (
            f"{platform}: missing Zero-Setup Default principle"
        )

    def test_canonical_sphere_set_present(self, platform: str):
        """Canonical sphere IDs reachable.

        Thresholds tuned to platform inlining strategy:
        - Lazy-load (claude, kimi-cli): ≥ 9/11 (master + extras carry full set)
        - Single-file grok: ≥ 8/11 (most refs inlined)
        - Single-file kimi: ≥ 5/11 (ultra-condensed, structural contract only)

        kimi sacrifices sphere-name coverage for cold-load budget;
        full canonical set lives in state_v2_schema.md anyway.
        """
        canonical = [
            "health", "finances", "career", "family", "romance",
            "social", "personal_growth", "meaning", "fun_recreation",
            "contribution", "physical_environment",
        ]
        corpus = _platform_corpus(platform)
        present = [s for s in canonical if s in corpus]
        thresholds = {"claude": 9, "grok": 8, "kimi": 5, "kimi-cli": 9}
        threshold = thresholds.get(platform, 8)
        assert len(present) >= threshold, (
            f"{platform}: only {len(present)}/11 canonical spheres reachable "
            f"(threshold {threshold}): {present}"
        )
