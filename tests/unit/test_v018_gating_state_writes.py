"""v0.18.0 acceptance tests: gating triggers + state writes per phase + Core Values Compass.

Closes 7 ⚠ gaps from state_v2_schema.md §9 Field availability matrix:
- persona.active_mode, emotion_regulation_log, wins_log, reward_audit_results,
  calendar_events_log, recovery_sessions_log, core_values_alignment.

Also verifies:
- Schema bump 2.0 → 2.0.1 + session.gating_mode field.
- SKILL.master.md has compact gating trigger algorithm + bootstrap/backfill triggers
  while staying under the 4 000-token cold-load budget.
- Phase 1.5 has inline Compass Mode (FR-04 from prd_core_values_discovery.md).
- templates/AI_Instructions.md has the 4 mode names + bootstrap + backfill protocols.

These tests don't simulate writes — they check that each phase module
*declares* the write-rule (so the skill, when executing, knows what to persist).
"""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MASTER = REPO_ROOT / "SKILL.master.md"
REFERENCES = REPO_ROOT / "references"
SCHEMA = REFERENCES / "state_v2_schema.md"
AI_INSTRUCTIONS = REFERENCES / "templates" / "AI_Instructions.md"

PHASE1 = REFERENCES / "module_phase1_diagnostic.md"
PHASE1_5 = REFERENCES / "module_phase1_5_goal_filter.md"
PHASE2 = REFERENCES / "module_phase2_goal_architecture.md"
PHASE3 = REFERENCES / "module_phase3_weekly_review.md"
PHASE4 = REFERENCES / "module_phase4_dashboard.md"
PHASE5 = REFERENCES / "module_phase5_execution.md"

ALL_PHASE_MODULES = [PHASE1, PHASE1_5, PHASE2, PHASE3, PHASE4, PHASE5]

GATING_MODES = [
    "full_persistence",
    "wiki_no_execution",
    "execution_no_wiki",
    "lean_conversation",
]

TIER1_BUDGET_TOKENS = 4100  # bumped 4000→4100 в v1.2.0 (Tier 3 refs для COM-B, env_design, Premortem)
PER_MODULE_BUDGET_TOKENS = 2500


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _approx_tokens(text: str) -> int:
    return len(text) // 3


# =========================================================================
# E1: Schema bump 2.0 → 2.0.1 + session.gating_mode
# =========================================================================


class TestSchemaVersion(unittest.TestCase):
    """State v2 schema must declare version 2.0.1 with gating_mode field."""

    def test_schema_version_2_0_1(self):
        """v0.18.0 introduced 2.0.1; later versions (2.1, 2.2) preserve gating_mode."""
        import re
        body = _read(SCHEMA)
        # Accept any 2.0.1+ semver (2.0.1, 2.1, 2.2, etc.) — gating_mode field is preserved
        match = re.search(r'"schema_version":\s*"(2\.(?:0\.[1-9]\d*|[1-9]\d*(?:\.\d+)?))"', body)
        self.assertIsNotNone(
            match,
            "state_v2_schema.md must declare schema_version 2.0.1 or later in JSON",
        )

    def test_session_gating_mode_field_declared(self):
        body = _read(SCHEMA)
        self.assertIn(
            "gating_mode",
            body,
            "state_v2_schema.md must declare session.gating_mode tracker (v0.18.0)",
        )
        # All 4 modes must appear in the schema doc itself.
        for mode in GATING_MODES:
            self.assertIn(
                mode,
                body,
                f"state_v2_schema.md must mention mode '{mode}' (4 gating modes)",
            )

    def test_schema_changelog_entry(self):
        body = _read(SCHEMA)
        self.assertIn(
            "2.0.1",
            body,
            "state_v2_schema.md must have explicit changelog entry for 2.0.1",
        )
        self.assertIn(
            "Changelog",
            body,
            "state_v2_schema.md must have a Changelog section after 2.0.1 bump",
        )


# =========================================================================
# E4: SKILL.master.md gating + bootstrap + backfill triggers
# =========================================================================


class TestMasterGatingTriggers(unittest.TestCase):
    """SKILL.master.md must contain compact gating trigger algorithm + bootstrap/backfill."""

    def test_master_has_session_start_algorithm(self):
        body = _read(MASTER)
        self.assertIn(
            "on session_start",
            body,
            "SKILL.master.md §3 Persistence Mode must declare 'on session_start' trigger",
        )

    def test_master_mentions_all_4_modes(self):
        body = _read(MASTER)
        for mode in GATING_MODES:
            self.assertIn(
                mode,
                body,
                f"SKILL.master.md must mention gating mode '{mode}' for trigger algorithm",
            )

    def test_master_has_gating_mode_write(self):
        body = _read(MASTER)
        self.assertIn(
            "session.gating_mode",
            body,
            "SKILL.master.md must write session.gating_mode after detection",
        )

    def test_master_has_bootstrap_trigger(self):
        body = _read(MASTER)
        self.assertIn(
            "wiki_bootstrapped",
            body,
            "SKILL.master.md must reference wiki_bootstrapped flag for bootstrap trigger",
        )
        self.assertIn(
            "bootstrap",
            body.lower(),
            "SKILL.master.md must describe bootstrap protocol trigger condition",
        )

    def test_master_has_backfill_trigger(self):
        body = _read(MASTER)
        self.assertIn(
            "backfill_offered",
            body,
            "SKILL.master.md must reference backfill_offered single-fire flag",
        )

    def test_master_under_tier1_budget(self):
        body = _read(MASTER)
        tokens = _approx_tokens(body)
        self.assertLessEqual(
            tokens,
            TIER1_BUDGET_TOKENS,
            f"SKILL.master.md ≈ {tokens} tokens — must stay ≤ {TIER1_BUDGET_TOKENS} "
            f"after v0.18.0 gating trigger addition",
        )


# =========================================================================
# E2: Per-phase state writes (close 7 gaps)
# =========================================================================


class TestPhase1StateWrites(unittest.TestCase):
    """Phase 1 must write persona.active_mode and emotion_regulation_log."""

    def test_phase1_writes_persona_active_mode(self):
        body = _read(PHASE1)
        self.assertIn(
            "persona.active_mode",
            body,
            "module_phase1_diagnostic.md must declare write for persona.active_mode (gap closed v0.18.0)",
        )

    def test_phase1_writes_emotion_regulation_log(self):
        body = _read(PHASE1)
        self.assertIn(
            "emotion_regulation_log",
            body,
            "module_phase1_diagnostic.md must declare write for emotion_regulation_log "
            "(Phase 0.5 ER protocol — gap closed v0.18.0)",
        )

    def test_phase1_writes_core_diagnosis_fields(self):
        body = _read(PHASE1)
        for field in ["wheel_of_life", "values_schwartz", "readiness_gates"]:
            self.assertIn(
                field,
                body,
                f"module_phase1_diagnostic.md must declare write for diagnosis.{field}",
            )


class TestPhase1_5StateWrites(unittest.TestCase):
    """Phase 1.5 must write core_values (full), core_values_alignment, Compass Mode artifacts."""

    def test_phase1_5_writes_core_values_alignment(self):
        body = _read(PHASE1_5)
        self.assertIn(
            "core_values_alignment",
            body,
            "module_phase1_5_goal_filter.md must declare core_values_alignment link "
            "при добавлении цели (gap closed v0.18.0)",
        )

    def test_phase1_5_writes_core_values_with_derived_from(self):
        body = _read(PHASE1_5)
        self.assertIn(
            "derived_from",
            body,
            "module_phase1_5_goal_filter.md must write core_values[].derived_from "
            "(domain/experience/energizing_activity provenance)",
        )

    def test_phase1_5_writes_compass_question(self):
        body = _read(PHASE1_5)
        self.assertIn(
            "compass_question",
            body,
            "module_phase1_5_goal_filter.md must write core_values[].compass_question "
            "(Compass Mode FR-04)",
        )


class TestPhase1_5CompassMode(unittest.TestCase):
    """Phase 1.5 must have inline Compass Mode section (FR-04 from PRD)."""

    def test_compass_mode_section_present(self):
        body = _read(PHASE1_5)
        self.assertIn(
            "Compass Mode",
            body,
            "module_phase1_5_goal_filter.md must have Compass Mode section "
            "(FR-04 from docs/research/prd_core_values_discovery.md)",
        )

    def test_compass_mode_has_daily_decision_protocol(self):
        body = _read(PHASE1_5)
        # Daily Decision Protocol must mention Pause + Compass question + Decision
        for term in ["Pause", "Compass", "Decision"]:
            self.assertIn(
                term,
                body,
                f"Compass Mode Daily Decision Protocol must include '{term}' step",
            )

    def test_compass_mode_references_template(self):
        body = _read(PHASE1_5)
        self.assertIn(
            "Core_Values_Compass.md",
            body,
            "Compass Mode must reference templates/Core_Values_Compass.md for full alignment audit",
        )


class TestPhase2StateWrites(unittest.TestCase):
    """Phase 2 must write full habit loop (cue/routine/reward/anchor/tiny_version)."""

    def test_phase2_writes_full_habit_loop(self):
        body = _read(PHASE2)
        for habit_field in ["cue", "routine", "reward", "anchor", "tiny_version"]:
            self.assertIn(
                habit_field,
                body,
                f"module_phase2_goal_architecture.md must write habits[].{habit_field} "
                f"(full Habit Loop — gap closed v0.18.0)",
            )


class TestPhase3StateWrites(unittest.TestCase):
    """Phase 3 must write wins_log and reward_audit_results."""

    def test_phase3_writes_wins_log(self):
        body = _read(PHASE3)
        self.assertIn(
            "wins_log",
            body,
            "module_phase3_weekly_review.md must write wins_log first-class "
            "(Step 5 Celebration — gap closed v0.18.0)",
        )

    def test_phase3_writes_reward_audit_results(self):
        body = _read(PHASE3)
        self.assertIn(
            "reward_audit_results",
            body,
            "module_phase3_weekly_review.md must write reward_audit_results "
            "(optional Step 7 — gap closed v0.18.0)",
        )


class TestPhase5StateWrites(unittest.TestCase):
    """Phase 5 must write calendar_events_log and recovery_sessions_log."""

    def test_phase5_writes_calendar_events_log(self):
        body = _read(PHASE5)
        self.assertIn(
            "calendar_events_log",
            body,
            "module_phase5_execution.md must write calendar_events_log "
            "(post create_event — gap closed v0.18.0)",
        )

    def test_phase5_writes_recovery_sessions_log(self):
        body = _read(PHASE5)
        self.assertIn(
            "recovery_sessions_log",
            body,
            "module_phase5_execution.md must write recovery_sessions_log "
            "(post recovery_protocol — gap closed v0.18.0)",
        )


# =========================================================================
# E5: templates/AI_Instructions.md — operational layer
# =========================================================================


class TestAIInstructions(unittest.TestCase):
    """AI_Instructions.md must contain full gating/bootstrap/backfill operational protocols."""

    def test_ai_instructions_has_all_4_modes(self):
        body = _read(AI_INSTRUCTIONS)
        for mode in GATING_MODES:
            self.assertIn(
                mode,
                body,
                f"templates/AI_Instructions.md §Gating must mention mode '{mode}'",
            )

    def test_ai_instructions_has_bootstrap_protocol(self):
        body = _read(AI_INSTRUCTIONS)
        self.assertIn(
            "wiki_bootstrapped",
            body,
            "templates/AI_Instructions.md must contain Bootstrap protocol with wiki_bootstrapped check",
        )
        self.assertIn(
            "Bootstrap",
            body,
            "templates/AI_Instructions.md must have Bootstrap section header",
        )

    def test_ai_instructions_has_backfill_protocol(self):
        body = _read(AI_INSTRUCTIONS)
        self.assertIn(
            "backfill_offered",
            body,
            "templates/AI_Instructions.md must contain Backfill protocol with single-fire flag",
        )

    def test_ai_instructions_writes_gating_mode(self):
        body = _read(AI_INSTRUCTIONS)
        self.assertIn(
            "session.gating_mode",
            body,
            "templates/AI_Instructions.md must instruct writing session.gating_mode (v2.0.1+)",
        )

    def test_ai_instructions_schema_v2_0_1(self):
        body = _read(AI_INSTRUCTIONS)
        self.assertIn(
            "2.0.1",
            body,
            "templates/AI_Instructions.md must declare schema_version 2.0.1 (frontmatter)",
        )

    def test_ai_instructions_write_rules_table_complete(self):
        body = _read(AI_INSTRUCTIONS)
        # 7 fields that were ⚠ gaps in v0.17.0 must appear in the write-rules table
        for field in [
            "persona.active_mode",
            "emotion_regulation_log",
            "wins_log",
            "reward_audit_results",
            "calendar_events_log",
            "recovery_sessions_log",
            "core_values_alignment",
        ]:
            self.assertIn(
                field,
                body,
                f"templates/AI_Instructions.md write-rules table must include '{field}' "
                f"(was ⚠ gap in v0.17.0)",
            )


# =========================================================================
# Field availability matrix — all 7 gaps closed
# =========================================================================


class TestStateV2GapMatrixResolved(unittest.TestCase):
    """state_v2_schema.md §9 must show ✅ for all 7 previously ⚠ fields."""

    def test_no_warning_status_for_resolved_fields(self):
        body = _read(SCHEMA)
        # Locate §9 (Field availability matrix)
        idx_start = body.find("## 9. Field availability matrix")
        idx_end = body.find("## 10.")
        if idx_end == -1:
            idx_end = len(body)
        self.assertGreater(
            idx_start, -1, "state_v2_schema.md must have §9 Field availability matrix"
        )
        matrix = body[idx_start:idx_end]
        # Fields that were ⚠ in v0.17.0 — must NOT carry ⚠ status anymore
        resolved_fields = [
            "persona.active_mode",
            "emotion_regulation_log",
            "wins_log",
            "reward_audit_results",
            "calendar_events_log",
            "recovery_sessions_log",
            "core_values_alignment",
        ]
        for field in resolved_fields:
            # field name appears in a row → that row must have ✅ (not ⚠)
            for line in matrix.splitlines():
                if field in line:
                    self.assertIn(
                        "✅",
                        line,
                        f"§9 row for '{field}' must show ✅ after v0.18.0 (was ⚠ in v0.17.0). "
                        f"Row: {line!r}",
                    )
                    self.assertNotIn(
                        "⚠️",
                        line,
                        f"§9 row for '{field}' must not carry ⚠️ status after v0.18.0",
                    )


# =========================================================================
# Per-module budget preserved
# =========================================================================


class TestModuleBudgetsPreserved(unittest.TestCase):
    """All phase modules must stay ≤ 2 500 tokens after v0.18.0 additions."""

    def test_each_module_under_budget(self):
        oversize = []
        for path in ALL_PHASE_MODULES:
            tokens = _approx_tokens(_read(path))
            if tokens > PER_MODULE_BUDGET_TOKENS:
                oversize.append((path.name, tokens))
        self.assertFalse(
            oversize,
            f"Phase modules over {PER_MODULE_BUDGET_TOKENS}-token budget after v0.18.0: {oversize}",
        )


if __name__ == "__main__":
    unittest.main()
