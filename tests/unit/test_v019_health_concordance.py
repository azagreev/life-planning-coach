"""v0.19.0 acceptance tests: Health Track + Goal Concordance.

Verifies:
- Schema bump 2.0.1 → 2.2 (additive: diagnosis.health_metabolism + partner_coordination)
- New Tier 3 ref references/track_health_metabolism.md exists and has 7 levers
- Phase 1 has opt-in Health Track entry
- Phase 3 has optional Health Review step
- Phase 1.5 has Partner Coordination Check (step 7)
- Phase 2 has Partner Discussion Checkpoint
- emotion_regulation.md has Conflict Reappraisal (Finkel 2013) + repair attempts
- Coaching ≠ therapy disclaimers present
- Per-module budgets preserved
- No eating-disorder diagnosis language in Health Track (safety)
"""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCES = REPO_ROOT / "references"
SCHEMA = REFERENCES / "state_v2_schema.md"
HEALTH_TRACK = REFERENCES / "track_health_metabolism.md"
EMOTION_REG = REFERENCES / "emotion_regulation.md"

PHASE1 = REFERENCES / "module_phase1_diagnostic.md"
PHASE1_5 = REFERENCES / "module_phase1_5_goal_filter.md"
PHASE2 = REFERENCES / "module_phase2_goal_architecture.md"
PHASE3 = REFERENCES / "module_phase3_weekly_review.md"

PER_MODULE_BUDGET_TOKENS = 2500
TRACK_HEALTH_BUDGET_TOKENS = 2500


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _approx_tokens(text: str) -> int:
    return len(text) // 3


# =====================================================
# Schema 2.2 + new blocks
# =====================================================


class TestSchemaV2_2(unittest.TestCase):
    """Schema must declare v2.2 with health_metabolism + partner_coordination."""

    def test_schema_v2_2_declared(self):
        body = _read(SCHEMA)
        # Accept 2.2 or any 2.2.x patch bump (additive fields only)
        self.assertRegex(
            body,
            r'"schema_version":\s*"2\.2(?:\.\d+)?"',
            "state_v2_schema.md must declare schema_version 2.2 or 2.2.x in JSON",
        )
        self.assertRegex(
            body, r"`2\.2(?:\.\d+)?`", "state_v2_schema.md header must declare 2.2 or 2.2.x"
        )

    def test_wiki_cleanup_mode_field_documented(self):
        """v2.2.1 — Layered cleanup defaults (Path A fallback strategy)."""
        body = _read(SCHEMA)
        self.assertIn(
            "wiki_cleanup_mode",
            body,
            "state_v2_schema.md must declare persistence_retry.drive.wiki_cleanup_mode",
        )
        # All 4 modes must be enumerated
        for mode in ("apps_script", "batch_weekly", "reminder", "ignore"):
            self.assertIn(
                mode,
                body,
                f"state_v2_schema.md must document wiki_cleanup_mode value '{mode}'",
            )

    def test_health_metabolism_block_present(self):
        body = _read(SCHEMA)
        self.assertIn(
            "health_metabolism",
            body,
            "state_v2_schema.md must declare diagnosis.health_metabolism block (v2.1)",
        )

    def test_health_metabolism_has_7_levers(self):
        body = _read(SCHEMA)
        # 7 fields covering 7 evidence-based levers
        for lever in [
            "sleep_quality",
            "sleep_hours",
            "stress_level",
            "protein_target_met",
            "fiber_target_met",
            "chewing_awareness",
            "caffeine_cutoff_hour",
        ]:
            self.assertIn(
                lever,
                body,
                f"state_v2_schema.md health_metabolism must declare '{lever}' field",
            )

    def test_partner_coordination_block_present(self):
        body = _read(SCHEMA)
        self.assertIn(
            "partner_coordination",
            body,
            "state_v2_schema.md must declare goal_filter.active_goals[].partner_coordination (v2.2)",
        )
        # All 3 Goal Concordance dimensions
        for dim in ["communication", "cooperation", "compatibility"]:
            self.assertIn(
                dim,
                body,
                f"partner_coordination must include '{dim}' dimension",
            )

    def test_schema_changelog_includes_2_1_and_2_2(self):
        body = _read(SCHEMA)
        idx = body.find("## 12. Changelog")
        self.assertGreater(idx, -1)
        changelog = body[idx:]
        self.assertIn("2.1", changelog, "§12 must have changelog entry for 2.1")
        self.assertIn("2.2", changelog, "§12 must have changelog entry for 2.2")


# =====================================================
# Health Track Tier 3 ref
# =====================================================


class TestHealthTrackRef(unittest.TestCase):
    """references/track_health_metabolism.md must exist and meet structural requirements."""

    def test_track_health_metabolism_file_exists(self):
        self.assertTrue(
            HEALTH_TRACK.exists(),
            "references/track_health_metabolism.md must exist (Tier 3 ref for v0.19.0)",
        )

    def test_track_health_under_budget(self):
        body = _read(HEALTH_TRACK)
        tokens = _approx_tokens(body)
        self.assertLessEqual(
            tokens,
            TRACK_HEALTH_BUDGET_TOKENS,
            f"track_health_metabolism.md ≈ {tokens} tokens > {TRACK_HEALTH_BUDGET_TOKENS}",
        )

    def test_track_health_has_7_levers(self):
        body = _read(HEALTH_TRACK).lower()
        for lever in ["сон", "стресс", "белок", "клетчатк", "жевани", "кофеин", "хлороген"]:
            self.assertIn(
                lever,
                body,
                f"track_health_metabolism.md must cover lever '{lever}' (one of 7 from PRD)",
            )

    def test_track_health_has_safety_disclaimer(self):
        body = _read(HEALTH_TRACK)
        # Safety: not for eating disorders
        self.assertIn(
            "РПП",
            body,
            "track_health_metabolism.md must declare safety boundary for eating disorders",
        )

    def test_track_health_evidence_based(self):
        body = _read(HEALTH_TRACK)
        # Key authors referenced
        for author in ["Spiegel", "Epel", "Leidy", "Wanders"]:
            self.assertIn(
                author,
                body,
                f"track_health_metabolism.md must cite '{author}' (high-priority lever evidence)",
            )

    def test_no_eating_disorder_diagnosis_words(self):
        """Skill must not diagnose; safety check for clinical language."""
        body = _read(HEALTH_TRACK).lower()
        forbidden = ["диагноз анорексии", "диагностируй булимию", "diagnose anorexia"]
        for word in forbidden:
            self.assertNotIn(
                word,
                body,
                f"track_health_metabolism.md must not contain diagnostic phrase '{word}'",
            )


# =====================================================
# Phase 1 — Health Track opt-in entry
# =====================================================


class TestPhase1HealthTrack(unittest.TestCase):
    def test_phase1_has_health_track_optin(self):
        body = _read(PHASE1)
        self.assertIn(
            "Health Track",
            body,
            "module_phase1_diagnostic.md must have Health Track entry (opt-in)",
        )
        self.assertIn(
            "track_health_metabolism.md",
            body,
            "module_phase1_diagnostic.md must reference Tier 3 ref",
        )

    def test_phase1_health_track_is_optin(self):
        body = _read(PHASE1)
        # opt-in язык, не блокирующий core flow
        self.assertIn(
            "opt-in",
            body.lower(),
            "Health Track entry в Phase 1 должен быть opt-in",
        )

    def test_module_phase1_under_budget_after_health(self):
        body = _read(PHASE1)
        tokens = _approx_tokens(body)
        self.assertLessEqual(
            tokens,
            PER_MODULE_BUDGET_TOKENS,
            f"module_phase1_diagnostic.md ≈ {tokens} tokens (budget {PER_MODULE_BUDGET_TOKENS})",
        )


# =====================================================
# Phase 3 — Health Track review (optional step)
# =====================================================


class TestPhase3HealthReview(unittest.TestCase):
    def test_phase3_has_health_review_step(self):
        body = _read(PHASE3)
        self.assertIn(
            "Health Track Review",
            body,
            "module_phase3_weekly_review.md must have optional Health Track Review step",
        )

    def test_phase3_under_budget_after_health(self):
        tokens = _approx_tokens(_read(PHASE3))
        self.assertLessEqual(tokens, PER_MODULE_BUDGET_TOKENS)


# =====================================================
# Phase 1.5 — Partner Coordination Check
# =====================================================


class TestPhase1_5PartnerCoordination(unittest.TestCase):
    def test_phase1_5_has_partner_coordination(self):
        body = _read(PHASE1_5)
        self.assertIn(
            "Partner Coordination",
            body,
            "module_phase1_5_goal_filter.md must have Partner Coordination Check (step 7)",
        )
        # Goal Concordance methodology terms
        for term in ["communication", "cooperation", "compatibility"]:
            self.assertIn(
                term.lower(),
                body.lower(),
                f"Partner Coordination must measure '{term}'",
            )

    def test_phase1_5_writes_partner_coordination(self):
        body = _read(PHASE1_5)
        self.assertIn(
            "partner_coordination",
            body,
            "module_phase1_5_goal_filter.md must write goal_filter.active_goals[].partner_coordination",
        )

    def test_coaching_not_therapy_disclaimer_present(self):
        body = _read(PHASE1_5)
        self.assertIn(
            "coaching, не therapy",
            body,
            "Partner Coordination must declare coaching ≠ therapy disclaimer",
        )

    def test_phase1_5_under_budget_after_concordance(self):
        tokens = _approx_tokens(_read(PHASE1_5))
        self.assertLessEqual(tokens, PER_MODULE_BUDGET_TOKENS)


# =====================================================
# Phase 2 — Partner Discussion Checkpoint
# =====================================================


class TestPhase2PartnerCheckpoint(unittest.TestCase):
    def test_phase2_has_partner_discussion_checkpoint(self):
        body = _read(PHASE2)
        self.assertIn(
            "Partner Discussion Checkpoint",
            body,
            "module_phase2_goal_architecture.md must have Partner Discussion Checkpoint (v2.2+)",
        )

    def test_phase2_under_budget(self):
        tokens = _approx_tokens(_read(PHASE2))
        self.assertLessEqual(tokens, PER_MODULE_BUDGET_TOKENS)


# =====================================================
# Emotion Regulation — Conflict Reappraisal + Repair Attempts
# =====================================================


class TestEmotionRegulationV019(unittest.TestCase):
    def test_emotion_regulation_has_conflict_reappraisal(self):
        body = _read(EMOTION_REG)
        self.assertIn(
            "Conflict Reappraisal",
            body,
            "emotion_regulation.md must have Conflict Reappraisal technique (Finkel 2013)",
        )

    def test_emotion_regulation_cites_finkel(self):
        body = _read(EMOTION_REG)
        self.assertIn(
            "Finkel",
            body,
            "emotion_regulation.md must cite Finkel et al. (2013) for conflict reappraisal",
        )

    def test_emotion_regulation_has_repair_attempts(self):
        body = _read(EMOTION_REG)
        self.assertIn(
            "Gottman",
            body,
            "emotion_regulation.md must cite Gottman for repair attempts",
        )


# =====================================================
# State v2 §9 matrix — new fields tracked
# =====================================================


class TestSchemaMatrixV019(unittest.TestCase):
    def test_v9_matrix_includes_health_metabolism(self):
        body = _read(SCHEMA)
        idx_start = body.find("## 9. Field availability matrix")
        idx_end = body.find("## 10.")
        matrix = body[idx_start:idx_end] if idx_end > -1 else body[idx_start:]
        self.assertIn(
            "health_metabolism",
            matrix,
            "§9 matrix must include diagnosis.health_metabolism row",
        )

    def test_v9_matrix_includes_partner_coordination(self):
        body = _read(SCHEMA)
        idx_start = body.find("## 9. Field availability matrix")
        idx_end = body.find("## 10.")
        matrix = body[idx_start:idx_end] if idx_end > -1 else body[idx_start:]
        self.assertIn(
            "partner_coordination",
            matrix,
            "§9 matrix must include partner_coordination row",
        )


if __name__ == "__main__":
    unittest.main()
