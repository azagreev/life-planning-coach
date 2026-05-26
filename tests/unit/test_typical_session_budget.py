"""v1.0.0: typical session token budget.

Validates that a realistic coaching session (master + 2-4 phase modules +
1 persona + optional ER/Health) stays under the 18K-token cold-load budget
declared in ROADMAP v1.0 acceptance criteria.

Cold-load = Tier 1 (master) + Tier 2 (phase modules loaded lazily as user
enters phases) + on-demand Tier 3 (persona, ER, Health Track, etc).

Token estimate: 1 token ≈ 3 chars for Russian-heavy text (conservative).
"""

from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REFERENCES = PROJECT_ROOT / "references"
MASTER = PROJECT_ROOT / "SKILL.master.md"


def _tokens(path: Path) -> int:
    return len(path.read_text(encoding="utf-8")) // 3


def _flow_size(*module_paths: Path) -> int:
    return sum(_tokens(p) for p in module_paths)


class TestTypicalSessionBudgets(unittest.TestCase):
    """Each flow simulates a realistic user journey."""

    QUICK_BUDGET = 14_000
    DEEP_BUDGET = 18_000
    HEALTH_BUDGET = 20_000
    RECOVERY_BUDGET = 14_000

    def test_quick_diagnostic_flow_under_14k(self):
        """Track A: master + Phase 1 + Phase 1.5 + Phase 2."""
        flow = [
            MASTER,
            REFERENCES / "module_phase1_diagnostic.md",
            REFERENCES / "module_phase1_5_goal_filter.md",
            REFERENCES / "module_phase2_goal_architecture.md",
        ]
        size = _flow_size(*flow)
        self.assertLessEqual(
            size, self.QUICK_BUDGET,
            f"Quick diagnostic flow ≈ {size} tokens > {self.QUICK_BUDGET}"
        )

    def test_deep_diagnostic_with_persona_under_18k(self):
        """Track B + dashboard + execution + 1 persona ADHD."""
        flow = [
            MASTER,
            REFERENCES / "module_phase1_diagnostic.md",
            REFERENCES / "module_phase1_5_goal_filter.md",
            REFERENCES / "module_phase2_goal_architecture.md",
            REFERENCES / "module_phase4_dashboard.md",
            REFERENCES / "module_phase5_execution.md",
            REFERENCES / "mode_adhd.md",
        ]
        size = _flow_size(*flow)
        self.assertLessEqual(
            size, self.DEEP_BUDGET,
            f"Deep diagnostic + ADHD persona flow ≈ {size} tokens > {self.DEEP_BUDGET}"
        )

    def test_health_track_activated_under_20k(self):
        """Quick flow + Health Track Tier 3 ref."""
        flow = [
            MASTER,
            REFERENCES / "module_phase1_diagnostic.md",
            REFERENCES / "module_phase1_5_goal_filter.md",
            REFERENCES / "module_phase2_goal_architecture.md",
            REFERENCES / "module_phase3_weekly_review.md",
            REFERENCES / "track_health_metabolism.md",
        ]
        size = _flow_size(*flow)
        self.assertLessEqual(
            size, self.HEALTH_BUDGET,
            f"Health Track flow ≈ {size} tokens > {self.HEALTH_BUDGET}"
        )

    def test_recovery_session_under_14k(self):
        """Recovery: master + Phase 1 + recovery_protocol + emotion_regulation."""
        recovery = REFERENCES / "recovery_protocol.md"
        # recovery_protocol.md may or may not exist as separate file
        if not recovery.exists():
            self.skipTest("recovery_protocol.md not yet implemented")
        flow = [
            MASTER,
            REFERENCES / "module_phase1_diagnostic.md",
            recovery,
            REFERENCES / "emotion_regulation.md",
        ]
        size = _flow_size(*flow)
        self.assertLessEqual(
            size, self.RECOVERY_BUDGET,
            f"Recovery + ER flow ≈ {size} tokens > {self.RECOVERY_BUDGET}"
        )

    def test_master_cold_load_under_4k(self):
        """v0.17+ Tier 1 budget — should never regress."""
        self.assertLessEqual(
            _tokens(MASTER), 4_000,
            f"Master cold-load ≈ {_tokens(MASTER)} tokens > 4000"
        )

    def test_phase_module_typical_under_2_5k(self):
        """Each individual phase module under 2.5K — already enforced
        elsewhere, but include here for v1.0 acceptance traceability."""
        for module in [
            "module_phase1_diagnostic.md",
            "module_phase1_5_goal_filter.md",
            "module_phase2_goal_architecture.md",
            "module_phase3_weekly_review.md",
            "module_phase4_dashboard.md",
            "module_phase5_execution.md",
        ]:
            path = REFERENCES / module
            tokens = _tokens(path)
            self.assertLessEqual(
                tokens, 2_500,
                f"{module}: {tokens} tokens > 2500"
            )


if __name__ == "__main__":
    unittest.main()
