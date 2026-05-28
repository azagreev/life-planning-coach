"""System tests for v1.4.0 — WoL Health Assessment Methodology (Sub-feature A).

Covers (per PRD `docs/research/prd_health_assessment_wol_subsegments.md` v1.0):

- Sub-feature A: WoL Health Sub-segments + Health Index calculation
  - New Tier 3 ref `references/wol_health_subsegments.md`
  - 6 canonical sub-segment IDs (English keys, like sphere IDs in §1 schema)
  - Health Index formula (avg of filled sub-segments)
  - 4 categories with action mapping
  - Weakest sub-segment surface
  - 4 persona adaptations (ADHD / Transitional / Elder / Planning Friction)
  - State schema bump 2.2.5 → 2.2.6 (additive)
  - Phase 1 module loads ref opt-in (single-score ≤ 6 OR explicit interest)
  - State writes: `diagnosis.wheel_of_life.current.health_subsegments`

Sub-feature B (`health_snapshot.md`) and C (Phase 3 opt-in) are NOT in this
test file — they ship in subsequent PRs and get their own test scope.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
REFERENCES = PROJECT_ROOT / "references"
SCHEMA = REFERENCES / "state_v2_schema.md"
WOL_HEALTH = REFERENCES / "wol_health_subsegments.md"
PHASE1 = REFERENCES / "module_phase1_diagnostic.md"

CANONICAL_SUBSEGMENTS = [
    "energy",
    "recovery",
    "physical_wellbeing",
    "stress_resilience",
    "nutrition",
    "reserve",
]


@pytest.fixture(scope="module")
def schema_text() -> str:
    return SCHEMA.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def wol_health_text() -> str:
    assert WOL_HEALTH.exists(), (
        f"Missing {WOL_HEALTH} — v1.4.0 Sub-feature A introduces this Tier 3 ref."
    )
    return WOL_HEALTH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def phase1_text() -> str:
    return PHASE1.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Schema bump 2.2.5 → 2.2.6
# ---------------------------------------------------------------------------


class TestSchemaBump:
    def test_schema_frontmatter_version_2_2_6(self, schema_text: str) -> None:
        assert re.search(
            r"\*\*Версия схемы:\*\*\s*`2\.2\.6`",
            schema_text,
        ), (
            "state_v2_schema.md frontmatter must declare `2.2.6` — Sub-feature A "
            "adds optional `health_subsegments` block (additive)."
        )

    def test_schema_json_example_version_2_2_6(self, schema_text: str) -> None:
        assert '"schema_version": "2.2.6"' in schema_text, (
            "JSON example must show `schema_version: 2.2.6` so consumer code "
            "produces matching state docs."
        )

    def test_changelog_2_2_6_entry_present(self, schema_text: str) -> None:
        assert "**2.2.6**" in schema_text, (
            "§12 Changelog must have a `**2.2.6**` entry explaining the additive "
            "bump (health_subsegments object)."
        )

    def test_schema_history_preserves_prior_versions(self, schema_text: str) -> None:
        """Prior schema entries must remain visible — no rewriting history."""
        for prior in ("**2.2.5**", "**2.2.4**", "**2.2.3**", "**2.2.2**", "**2.2**", "**2.1**", "**2.0.1**", "**2.0**"):
            assert prior in schema_text, (
                f"Prior schema entry {prior} missing from §12. Bumping a version "
                "doesn't erase history — append, don't overwrite."
            )


# ---------------------------------------------------------------------------
# health_subsegments field shape (state schema)
# ---------------------------------------------------------------------------


class TestHealthSubsegmentsFieldSpec:
    def test_section_3_4_5_exists(self, schema_text: str) -> None:
        assert "### 3.4.5 diagnosis.wheel_of_life.current.health_subsegments" in schema_text, (
            "state_v2_schema.md must have §3.4.5 dedicated to health_subsegments — "
            "every additive bump gets its own spec section."
        )

    def test_health_subsegments_in_current_block(self, schema_text: str) -> None:
        """JSON example must show `health_subsegments` inside `current`."""
        # Find `"current": {` block then check health_subsegments follows
        match = re.search(
            r'"current":\s*\{(.*?)\n\s*\},',
            schema_text,
            re.DOTALL,
        )
        assert match, "JSON example `current` block missing"
        current_block = match.group(1)
        assert "health_subsegments" in current_block, (
            "JSON example `current` block must include `health_subsegments` "
            "alongside the 11 spheres so its location is canonical."
        )

    @pytest.mark.parametrize("subseg", CANONICAL_SUBSEGMENTS)
    def test_schema_lists_each_canonical_subsegment(
        self, schema_text: str, subseg: str
    ) -> None:
        """§3.4.5 must enumerate each of the 6 canonical sub-segment keys."""
        # Find §3.4.5 body
        match = re.search(
            r"### 3\.4\.5 diagnosis\.wheel_of_life\.current\.health_subsegments(.*?)(?=^###?\s|\Z)",
            schema_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match, "§3.4.5 body not found"
        body = match.group(1)
        assert f"`health_subsegments.{subseg}`" in body, (
            f"§3.4.5 must list `health_subsegments.{subseg}` (1-10) field — "
            "canonical 6-segment contract from PRD §2."
        )

    def test_write_rule_table_includes_health_subsegments(self, schema_text: str) -> None:
        """§9 write-rules table must add a row for health_subsegments."""
        assert "current.health_subsegments" in schema_text, (
            "§9 write-rules table must include `current.health_subsegments` "
            "write trigger (Phase 1 WoL detailed mode)."
        )


# ---------------------------------------------------------------------------
# wol_health_subsegments.md Tier 3 ref
# ---------------------------------------------------------------------------


class TestWolHealthRefContent:
    def test_ref_declares_tier_3(self, wol_health_text: str) -> None:
        assert "**Tier:** 3" in wol_health_text, (
            "wol_health_subsegments.md must declare Tier 3 (lazy-load) — "
            "не часть Tier 1 cold-load."
        )

    def test_ref_declares_schema_version(self, wol_health_text: str) -> None:
        assert "v2.2.6" in wol_health_text, (
            "Header must reference schema version v2.2.6+ so consumers know the "
            "minimum supporting state schema."
        )

    def test_ref_cites_prd(self, wol_health_text: str) -> None:
        assert "prd_health_assessment_wol_subsegments.md" in wol_health_text, (
            "Ref must cross-link to the source PRD so future readers can "
            "validate decisions against intent."
        )

    def test_ref_explicitly_avoids_track_metabolism_duplication(
        self, wol_health_text: str
    ) -> None:
        """PRD §9 explicit non-goal: «Не дублируем track_health_metabolism.md»."""
        assert "track_health_metabolism.md" in wol_health_text, (
            "Ref must explicitly reference `track_health_metabolism.md` so "
            "the «middle ground» positioning is clear."
        )
        assert re.search(
            r"(не\s+дубл|NOT\s+duplicat)",
            wol_health_text,
            re.IGNORECASE,
        ), (
            "Ref must explicitly say it does NOT duplicate the deep health track."
        )

    @pytest.mark.parametrize("subseg", CANONICAL_SUBSEGMENTS)
    def test_ref_lists_each_subsegment(self, wol_health_text: str, subseg: str) -> None:
        assert f"`{subseg}`" in wol_health_text, (
            f"Ref must list canonical id `{subseg}` (English key) — alignment "
            "with state schema §3.4.5."
        )

    def test_ref_has_health_index_formula(self, wol_health_text: str) -> None:
        assert re.search(
            r"Health Index\s*=\s*avg",
            wol_health_text,
            re.IGNORECASE,
        ), (
            "Ref must show explicit `Health Index = avg(...)` formula. PRD §3 "
            "defines this — без формулы Sub-feature A не воспроизводима."
        )

    @pytest.mark.parametrize(
        ("threshold", "category"),
        [
            (8.0, "Отличный"),
            (6.5, "Хороший"),
            (5.0, "Средний"),
            (5.0, "Низкий"),  # appears in "≤ 5.0" condition
        ],
    )
    def test_ref_has_four_categories(
        self, wol_health_text: str, threshold: float, category: str
    ) -> None:
        """All 4 PRD §3 categories must be enumerated with their action."""
        assert category in wol_health_text, (
            f"Category «{category}» (threshold {threshold}) missing from ref. "
            "PRD §3 defines exactly 4 categories — each maps to a different action."
        )

    def test_ref_has_weakest_subsegment_surface(self, wol_health_text: str) -> None:
        assert re.search(
            r"(weakest|самый\s+слабый|min\()",
            wol_health_text,
            re.IGNORECASE,
        ), (
            "Ref must describe weakest-sub-segment identification. PRD §3 says: "
            "«Дополнительно определяется самый слабый суб-сегмент»."
        )

    @pytest.mark.parametrize(
        "persona_module",
        ["mode_adhd.md", "mode_unemployed.md", "mode_elder.md", "mode_planning_friction.md"],
    )
    def test_ref_covers_all_four_personas(
        self, wol_health_text: str, persona_module: str
    ) -> None:
        assert persona_module in wol_health_text, (
            f"Ref must reference `{persona_module}` — PRD §5 defines persona "
            "adaptations for all 4 modes; missing one orphans that persona's flow."
        )

    def test_ref_routes_to_health_snapshot_for_low_score(
        self, wol_health_text: str
    ) -> None:
        """Low/Middle Health Index routes to `health_snapshot.md` (Sub-feature B)."""
        assert "health_snapshot.md" in wol_health_text, (
            "Ref must reference `health_snapshot.md` (Sub-feature B, v1.4.x) for "
            "Low/Middle routing. Even though B not yet shipped, A's routing logic "
            "names the target."
        )

    def test_ref_documents_opt_in_default(self, wol_health_text: str) -> None:
        """Default WoL flow stays single-score — sub-segments are opt-in."""
        assert re.search(
            r"(default|по\s+умолчанию|opt-in)",
            wol_health_text,
            re.IGNORECASE,
        ), (
            "Ref must document that single-score is default; sub-segments are "
            "opt-in. PRD doesn't replace existing WoL — extends it."
        )


# ---------------------------------------------------------------------------
# Phase 1 module integration
# ---------------------------------------------------------------------------


class TestPhase1Integration:
    def test_phase1_references_wol_health_ref(self, phase1_text: str) -> None:
        assert "wol_health_subsegments.md" in phase1_text, (
            "module_phase1_diagnostic.md must reference `wol_health_subsegments.md` "
            "(either in spheres section or state-writes block) so loading point "
            "is discoverable from the Phase 1 module."
        )

    def test_phase1_mentions_schema_version_2_2_6(self, phase1_text: str) -> None:
        assert "v2.2.6" in phase1_text, (
            "Phase 1 module must mention `v2.2.6` near the sub-segments reference "
            "so the minimum schema version is visible at the loading point."
        )

    def test_phase1_state_write_includes_health_subsegments(
        self, phase1_text: str
    ) -> None:
        assert "health_subsegments" in phase1_text, (
            "Phase 1 State writes block must include `health_subsegments` so "
            "the write trigger is explicit per AGENTS §3.6."
        )


# ---------------------------------------------------------------------------
# Budget guards (Phase 1 must stay under 2500)
# ---------------------------------------------------------------------------


class TestPhase1BudgetUnchanged:
    """Sub-feature A must not blow per-module budget. Existing
    `test_tier_token_budgets.test_each_module_under_budget` covers this
    generically; this dedicated test gives a Sub-feature-A-specific error
    message so a regression points to the right cause."""

    def test_phase1_within_budget(self, phase1_text: str) -> None:
        tokens = len(phase1_text) // 3
        assert tokens <= 2500, (
            f"Phase 1 module = {tokens} tokens (budget 2500). Sub-feature A's "
            "additions blew the budget. Tighten the inline notes — full detail "
            "lives in `wol_health_subsegments.md`, the module only needs to "
            "name the loading trigger."
        )
