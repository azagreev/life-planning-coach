"""Token-budget tests for the Tier 1/2/3 IA decomposition (v0.17.0).

Covers:
- Tier 1 (SKILL.master.md) cold-load budget ≤ 4000 tokens.
- Tier 2 (references/module_phase*.md) per-phase budget ≤ 2500 tokens.
- Tier 2 total (all phase modules together) ≤ 14000 tokens.
- Tier 2 module set is complete (6 canonical phase modules exist).
- Tier 1 declares Routing Map with pointers to every Tier 2 module.

Token estimation: ~1 token per 3 chars (rough Russian-text heuristic).
This is conservative — tiktoken-based estimates are usually 10–20 % lower.

If you need to bump a budget, do it consciously: tighter Tier 1 = lower
cold-load cost on every session start. The whole point of the decomposition
is to keep Tier 1 small.
"""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MASTER = REPO_ROOT / "SKILL.master.md"
REFERENCES = REPO_ROOT / "references"

CANONICAL_PHASE_MODULES = [
    "module_phase1_diagnostic.md",
    "module_phase1_5_goal_filter.md",
    "module_phase2_goal_architecture.md",
    "module_phase3_weekly_review.md",
    "module_phase4_dashboard.md",
    "module_phase5_execution.md",
]

# Budgets in approx-tokens (1 token ≈ 3 chars for Russian-heavy text).
# Tier 1 budget bumped 4000 → 4100 in v1.2.0 to accommodate Tier 3 references
# for 3 new evidence-based methods (COM-B, Environment Design, Premortem).
# Each new ref adds ~7 tokens (path в Tier 3 listing). Headroom ~2.5%.
TIER1_BUDGET_TOKENS = 4100
PER_MODULE_BUDGET_TOKENS = 2500
ALL_MODULES_BUDGET_TOKENS = 14000


def _approx_tokens(text: str) -> int:
    """Rough Russian-text token estimate: ~1 token per 3 chars."""
    return len(text) // 3


class TestTier1Budget(unittest.TestCase):
    """SKILL.master.md must stay under the cold-load budget."""

    def test_master_exists(self):
        self.assertTrue(MASTER.exists(), "SKILL.master.md must exist at repo root")

    def test_master_under_tier1_budget(self):
        content = MASTER.read_text(encoding="utf-8")
        tokens = _approx_tokens(content)
        self.assertLessEqual(
            tokens,
            TIER1_BUDGET_TOKENS,
            f"SKILL.master.md ≈ {tokens} tokens (limit: {TIER1_BUDGET_TOKENS}). "
            f"Move detail into a Tier 2 module under references/module_phase*.md.",
        )

    def test_master_declares_routing_map(self):
        content = MASTER.read_text(encoding="utf-8")
        # Must contain a Routing Map header AND link to every phase module.
        self.assertIn(
            "Routing Map",
            content,
            "SKILL.master.md must have a 'Routing Map' section to route into Tier 2 modules.",
        )
        for module in CANONICAL_PHASE_MODULES:
            self.assertIn(
                module,
                content,
                f"SKILL.master.md must reference `references/{module}` "
                f"in its Routing Map / References block.",
            )


class TestTier2ModuleSet(unittest.TestCase):
    """All 6 canonical phase modules must exist."""

    def test_all_modules_present(self):
        for module in CANONICAL_PHASE_MODULES:
            path = REFERENCES / module
            self.assertTrue(
                path.exists(),
                f"Tier 2 module missing: references/{module}. "
                f"Phase modules are the contract that SKILL.master.md routes into.",
            )


class TestPerModuleBudget(unittest.TestCase):
    """Each phase module must stay under its individual budget."""

    def test_each_module_under_budget(self):
        oversize = []
        for module in CANONICAL_PHASE_MODULES:
            path = REFERENCES / module
            if not path.exists():
                continue  # covered by TestTier2ModuleSet
            content = path.read_text(encoding="utf-8")
            tokens = _approx_tokens(content)
            if tokens > PER_MODULE_BUDGET_TOKENS:
                oversize.append((module, tokens))
        self.assertFalse(
            oversize,
            "Phase modules over budget (limit "
            f"{PER_MODULE_BUDGET_TOKENS} tokens): {oversize}. "
            "Split protocol detail into a Tier 3 ref under references/*.md.",
        )


class TestTier2TotalBudget(unittest.TestCase):
    """Sum of all phase modules must stay under the aggregate budget."""

    def test_total_modules_under_budget(self):
        total = 0
        for module in CANONICAL_PHASE_MODULES:
            path = REFERENCES / module
            if not path.exists():
                continue
            total += _approx_tokens(path.read_text(encoding="utf-8"))
        self.assertLessEqual(
            total,
            ALL_MODULES_BUDGET_TOKENS,
            f"All phase modules combined ≈ {total} tokens "
            f"(limit: {ALL_MODULES_BUDGET_TOKENS}). "
            "Typical session loads 1–2 modules, so the cap is generous; "
            "if you blew it, modules have drifted into Tier 1 territory.",
        )


if __name__ == "__main__":
    unittest.main()
