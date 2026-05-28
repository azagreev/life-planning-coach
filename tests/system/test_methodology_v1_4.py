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
    """Schema bump tests for v1.4.0 ship state.

    Note: v1.4.0 ships with schema 2.2.7 (Sub-feature A bumped 2.2.5 → 2.2.6;
    Sub-feature B bumped 2.2.6 → 2.2.7). Both sub-features ship together as
    v1.4.0; the intermediate 2.2.6 state is internal implementation detail.
    Tests use history-preservation pattern для 2.2.6 entry.
    """

    def test_schema_frontmatter_version_2_2_7(self, schema_text: str) -> None:
        assert re.search(
            r"\*\*Версия схемы:\*\*\s*`2\.2\.7`",
            schema_text,
        ), (
            "state_v2_schema.md frontmatter must declare `2.2.7` — v1.4.0 ships "
            "with schema 2.2.7 (Sub-feature A added 2.2.6 health_subsegments; "
            "Sub-feature B bumped to 2.2.7 для health_snapshot.last)."
        )

    def test_schema_json_example_version_2_2_7(self, schema_text: str) -> None:
        assert '"schema_version": "2.2.7"' in schema_text, (
            "JSON example must show `schema_version: 2.2.7` so consumer code "
            "produces matching state docs."
        )

    def test_changelog_2_2_7_entry_present(self, schema_text: str) -> None:
        assert "**2.2.7**" in schema_text, (
            "§12 Changelog must have a `**2.2.7**` entry explaining the additive "
            "bump (health_snapshot.last object, Sub-feature B)."
        )

    def test_changelog_2_2_6_entry_persists(self, schema_text: str) -> None:
        """Sub-feature A's bump 2.2.6 (health_subsegments) must remain в §12 — history preservation."""
        assert "**2.2.6**" in schema_text, (
            "§12 Changelog must keep `**2.2.6**` entry (Sub-feature A's "
            "health_subsegments bump) — history preservation pattern."
        )

    def test_schema_history_preserves_prior_versions(self, schema_text: str) -> None:
        """Prior schema entries must remain visible — no rewriting history."""
        for prior in ("**2.2.6**", "**2.2.5**", "**2.2.4**", "**2.2.3**", "**2.2.2**", "**2.2**", "**2.1**", "**2.0.1**", "**2.0**"):
            assert prior in schema_text, (
                f"Prior schema entry {prior} missing from §12. Bumping a version "
                "doesn't erase history — append, don't overwrite."
            )

    def test_changelog_ordering_newest_first(self, schema_text: str) -> None:
        """§12 ordering: 2.2.7 must precede 2.2.6 (newest first)."""
        idx_2_7 = schema_text.find("**2.2.7**")
        idx_2_6 = schema_text.find("**2.2.6**")
        assert idx_2_7 != -1 and idx_2_6 != -1
        assert idx_2_7 < idx_2_6, (
            "§12 must show 2.2.7 entry FIRST (before 2.2.6) — newest-first ordering."
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
    """Sub-features A + B must not blow per-module budget. Existing
    `test_tier_token_budgets.test_each_module_under_budget` covers this
    generically; this dedicated test gives a v1.4-specific error message
    so a regression points to the right cause."""

    def test_phase1_within_budget(self, phase1_text: str) -> None:
        tokens = len(phase1_text) // 3
        assert tokens <= 2500, (
            f"Phase 1 module = {tokens} tokens (budget 2500). Sub-features A + "
            "B additions blew the budget. Tighten the inline notes — full detail "
            "lives in `wol_health_subsegments.md` + `health_snapshot.md`; the "
            "module only needs to name the loading triggers."
        )


# ---------------------------------------------------------------------------
# Sub-feature B — Light Health Snapshot (4-question tool)
# ---------------------------------------------------------------------------


HEALTH_SNAPSHOT = REFERENCES / "health_snapshot.md"

CANONICAL_SNAPSHOT_QUESTIONS = [
    "energy_stability",
    "recovery",
    "stress_management",
    "resilience",
]


@pytest.fixture(scope="module")
def health_snapshot_text() -> str:
    assert HEALTH_SNAPSHOT.exists(), (
        f"Missing {HEALTH_SNAPSHOT} — v1.4.0 Sub-feature B introduces this Tier 3 ref."
    )
    return HEALTH_SNAPSHOT.read_text(encoding="utf-8")


class TestHealthSnapshotFieldSpec:
    """`diagnosis.health_snapshot.last` field shape in state schema."""

    def test_section_3_4_6_exists(self, schema_text: str) -> None:
        assert "### 3.4.6 diagnosis.health_snapshot.last" in schema_text, (
            "state_v2_schema.md must have §3.4.6 для health_snapshot.last spec."
        )

    def test_health_snapshot_block_in_diagnosis(self, schema_text: str) -> None:
        """JSON example must include `health_snapshot` block."""
        assert '"health_snapshot"' in schema_text, (
            "JSON example must include `health_snapshot` block inside `diagnosis`."
        )

    @pytest.mark.parametrize(
        "field",
        ["date", "average_score", "weakest_question", "answered_count", "declined_count"],
    )
    def test_schema_documents_each_snapshot_field(
        self, schema_text: str, field: str
    ) -> None:
        match = re.search(
            r"### 3\.4\.6 diagnosis\.health_snapshot\.last(.*?)(?=^###?\s|\Z)",
            schema_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match, "§3.4.6 body not found"
        body = match.group(1)
        assert f"`health_snapshot.last.{field}`" in body, (
            f"§3.4.6 must document `health_snapshot.last.{field}` field."
        )

    def test_write_rule_table_includes_snapshot(self, schema_text: str) -> None:
        assert "diagnosis.health_snapshot.last" in schema_text, (
            "§9 write-rules table must include `diagnosis.health_snapshot.last` "
            "row (Phase 1 trigger at Health Index ≤ 5.5 OR explicit request)."
        )


class TestHealthSnapshotRefContent:
    """References/health_snapshot.md Tier 3 ref content guards."""

    def test_ref_declares_tier_3(self, health_snapshot_text: str) -> None:
        assert "**Tier:** 3" in health_snapshot_text, (
            "health_snapshot.md must declare Tier 3 (lazy-load)."
        )

    def test_ref_declares_schema_version(self, health_snapshot_text: str) -> None:
        assert "v2.2.7" in health_snapshot_text, (
            "Header must reference schema v2.2.7+ so consumers know the minimum "
            "supporting state schema."
        )

    def test_ref_cites_prd(self, health_snapshot_text: str) -> None:
        assert "prd_health_assessment_wol_subsegments.md" in health_snapshot_text, (
            "Ref must cross-link to source PRD §4."
        )

    def test_ref_explicitly_avoids_track_metabolism_duplication(
        self, health_snapshot_text: str
    ) -> None:
        assert "track_health_metabolism.md" in health_snapshot_text, (
            "Ref must reference `track_health_metabolism.md` so positioning as "
            "decision-gate (vs duplicate) is clear."
        )
        assert re.search(
            r"(не\s+дубл|NOT\s+duplicat)",
            health_snapshot_text,
            re.IGNORECASE,
        ), "Ref must explicitly say it does NOT duplicate the deep health track."

    def test_ref_has_four_questions(self, health_snapshot_text: str) -> None:
        """All 4 PRD §4 questions must be enumerated."""
        # Each question is a numbered item; the table shows them
        # We expect at least the 4 question topics present
        assert re.search(r"уровень\s+энерги", health_snapshot_text, re.IGNORECASE), (
            "Q1 (energy stability) missing"
        )
        assert re.search(r"восстанавлива", health_snapshot_text, re.IGNORECASE), (
            "Q2 (recovery) missing"
        )
        assert re.search(r"стресс", health_snapshot_text, re.IGNORECASE), (
            "Q3 (stress management) missing"
        )
        assert re.search(r"быстро\s+ты\s+приходишь", health_snapshot_text, re.IGNORECASE), (
            "Q4 (resilience / bounce-back) missing"
        )

    @pytest.mark.parametrize("qid", CANONICAL_SNAPSHOT_QUESTIONS)
    def test_ref_has_canonical_question_ids(
        self, health_snapshot_text: str, qid: str
    ) -> None:
        assert f"`{qid}`" in health_snapshot_text, (
            f"Ref must list canonical question ID `{qid}` — alignment с state "
            "schema §3.4.6 weakest_question enum."
        )

    @pytest.mark.parametrize(
        "persona_module",
        ["mode_adhd.md", "mode_unemployed.md", "mode_elder.md", "mode_planning_friction.md"],
    )
    def test_ref_covers_all_four_personas(
        self, health_snapshot_text: str, persona_module: str
    ) -> None:
        assert persona_module in health_snapshot_text, (
            f"Ref must reference `{persona_module}` — PRD §5 defines persona "
            "adaptations for all 4 modes."
        )

    def test_ref_has_snapshot_index_formula(
        self, health_snapshot_text: str
    ) -> None:
        assert re.search(
            r"Snapshot Index\s*=\s*avg",
            health_snapshot_text,
            re.IGNORECASE,
        ), (
            "Ref must show explicit `Snapshot Index = avg(...)` formula. PRD §4 "
            "implies avg over 4 answers."
        )

    @pytest.mark.parametrize(
        "category",
        ["Отличный", "Хороший", "Средний", "Низкий"],
    )
    def test_ref_has_four_categories(
        self, health_snapshot_text: str, category: str
    ) -> None:
        assert category in health_snapshot_text, (
            f"Category «{category}» missing from ref — 4 categories required "
            "for routing decisions."
        )

    def test_ref_documents_2_decline_cutoff(self, health_snapshot_text: str) -> None:
        """2-decline cutoff per session must be documented."""
        assert re.search(
            r"(2-decline|2\s+(раза|times)\s+decline|declined_count)",
            health_snapshot_text,
            re.IGNORECASE,
        ), (
            "Ref must document 2-decline cutoff per session — respects user "
            "autonomy after 2 offers declined."
        )

    def test_ref_has_safety_escalation(self, health_snapshot_text: str) -> None:
        """If all 4 ≤ 3 — escalate per SKILL.master Safety section."""
        assert "Safety" in health_snapshot_text, (
            "Ref must reference Safety section for low-score escalation pattern."
        )
        assert re.search(r"<=\s*3|≤\s*3", health_snapshot_text), (
            "Safety threshold (`≤ 3`) must be explicit in escalation logic."
        )

    def test_ref_documents_routing_to_health_track(
        self, health_snapshot_text: str
    ) -> None:
        """Routing after Snapshot must mention Health Track activation."""
        assert "health_metabolism.active" in health_snapshot_text or "Health Track" in health_snapshot_text, (
            "Ref must document that user-agreed offer activates Health Track "
            "(`track_health_metabolism.md` + `health_metabolism.active = true`)."
        )

    def test_ref_documents_triggers(self, health_snapshot_text: str) -> None:
        """All 3 trigger conditions from PRD §8 must be documented."""
        assert "5.5" in health_snapshot_text, "Trigger «Health Index ≤ 5.5» missing"
        assert re.search(
            r"explicit|по\s+запросу|user\s+request",
            health_snapshot_text,
            re.IGNORECASE,
        ), "Trigger «explicit user request» missing"
        assert re.search(
            r"Phase\s*3|еженедельн|Weekly",
            health_snapshot_text,
            re.IGNORECASE,
        ), "Trigger «Phase 3 opt-in» missing (forward-reference Sub-feature C)"


class TestPhase1IntegrationSnapshot:
    """Phase 1 module must mention health_snapshot loading point."""

    def test_phase1_references_snapshot_ref(self, phase1_text: str) -> None:
        assert "health_snapshot.md" in phase1_text, (
            "module_phase1_diagnostic.md must reference `health_snapshot.md` "
            "so loading point is discoverable from Phase 1."
        )

    def test_phase1_mentions_schema_2_2_7(self, phase1_text: str) -> None:
        assert "v2.2.7" in phase1_text, (
            "Phase 1 module must mention v2.2.7 near snapshot reference."
        )

    def test_phase1_state_write_includes_snapshot_last(
        self, phase1_text: str
    ) -> None:
        assert "health_snapshot.last" in phase1_text, (
            "Phase 1 State writes block must include `health_snapshot.last`."
        )


# ---------------------------------------------------------------------------
# Cross-PR consistency — A and B must coherently route to each other
# ---------------------------------------------------------------------------


class TestSubfeatureAToBRouting:
    """Sub-feature A (wol_health_subsegments.md) must route low-score → Snapshot."""

    @pytest.fixture(scope="class")
    def wol_health_text(self) -> str:
        return (REFERENCES / "wol_health_subsegments.md").read_text(encoding="utf-8")

    def test_subseg_routes_to_health_snapshot(self, wol_health_text: str) -> None:
        """Sub-feature A must explicitly reference Sub-feature B."""
        assert "health_snapshot.md" in wol_health_text, (
            "wol_health_subsegments.md must route Low/Middle categories к "
            "health_snapshot.md (Sub-feature B). Previously B был forward-reference; "
            "now both shipped together, должен быть hard link, не «when shipped»."
        )

    def test_snapshot_back_links_to_subseg(self, health_snapshot_text: str) -> None:
        """Sub-feature B's «Когда запускать» must reference subsegments routing."""
        assert "wol_health_subsegments.md" in health_snapshot_text, (
            "health_snapshot.md must reference wol_health_subsegments.md as the "
            "primary entry-point (low-score auto-offer trigger)."
        )


# ---------------------------------------------------------------------------
# Sub-feature C — Phase 3 Weekly Review opt-in для Health Snapshot
# ---------------------------------------------------------------------------


PHASE3 = REFERENCES / "module_phase3_weekly_review.md"


@pytest.fixture(scope="module")
def phase3_text() -> str:
    return PHASE3.read_text(encoding="utf-8")


class TestSubfeatureCPhase3OptIn:
    """Sub-feature C: Phase 3 §6.5 must offer Snapshot when Health Track NOT active."""

    def test_phase3_references_health_snapshot(self, phase3_text: str) -> None:
        """Phase 3 §6.5 Health Track Review должно reference health_snapshot.md."""
        assert "health_snapshot.md" in phase3_text, (
            "module_phase3_weekly_review.md §6.5 must reference `health_snapshot.md` "
            "as opt-in path for users WITHOUT active Health Track (Sub-feature C, "
            "PRD §8 «опционально — в еженедельном обзоре»)."
        )

    def test_phase3_distinguishes_active_branches(self, phase3_text: str) -> None:
        """§6.5 must have both `active == true` AND `active == false` branches."""
        section_match = re.search(
            r"### 6\.5\.\s*Health Track Review.*?(?=^###?\s|\Z)",
            phase3_text,
            re.DOTALL | re.MULTILINE,
        )
        assert section_match, "§6.5 Health Track Review section missing"
        section = section_match.group(0)
        assert "active == true" in section, (
            "§6.5 must keep existing `active == true` branch (v0.19.0 Health Track "
            "review protocol — sleep/stress/nutrition check-in)."
        )
        assert "active == false" in section, (
            "§6.5 must add `active == false` branch (Sub-feature C) — opt-in "
            "Snapshot для users без active Health Track."
        )

    def test_phase3_mentions_schema_v2_2_7(self, phase3_text: str) -> None:
        """Schema version (2.2.7+) must be visible near Snapshot reference."""
        assert "v2.2.7" in phase3_text, (
            "Phase 3 §6.5 must mention `v2.2.7+` near snapshot reference so "
            "the minimum schema is visible at the loading point."
        )

    def test_phase3_within_budget(self, phase3_text: str) -> None:
        """Sub-feature C must not blow Phase 3 budget (existing 19-token headroom)."""
        tokens = len(phase3_text) // 3
        assert tokens <= 2500, (
            f"Phase 3 module = {tokens} tokens (budget 2500). Sub-feature C blew "
            "the budget. Tighten existing §6.5 wording (the snapshot reference "
            "itself is minimal; the headroom was already tight from v1.2/v1.3)."
        )
