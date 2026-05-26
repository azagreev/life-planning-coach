"""v0.19.0: Persona module rename to `mode_<short>` convention.

Mapping:
    adhd_mode.md               → mode_adhd.md
    time_structure_unemployed.md → mode_unemployed.md
    elder_homebound_mode.md    → mode_elder.md
    planning_friction_audit.md → mode_planning_friction.md

Tests verify:
- Old files don't exist anymore
- New files present
- No old-path refs in runtime files (master, modules, platforms, tests)
- Naming convention unified (all start with `mode_`)
- New files still under per-module budget
"""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCES = REPO_ROOT / "references"
PLATFORMS = REPO_ROOT / "platforms"
TESTS = REPO_ROOT / "tests"

OLD_NAMES = [
    "adhd_mode.md",
    "time_structure_unemployed.md",
    "elder_homebound_mode.md",
    "planning_friction_audit.md",
]

NEW_NAMES = [
    "mode_adhd.md",
    "mode_unemployed.md",
    "mode_elder.md",
    "mode_planning_friction.md",
]

# Runtime files that must not contain old persona paths
RUNTIME_CHECK_PATHS = [
    REPO_ROOT / "SKILL.master.md",
    REPO_ROOT / "SKILL.md",
    REFERENCES / "module_phase1_diagnostic.md",
    REFERENCES / "module_phase2_goal_architecture.md",
    REFERENCES / "module_phase3_weekly_review.md",
    REFERENCES / "module_phase4_dashboard.md",
    REFERENCES / "module_phase5_execution.md",
    REFERENCES / "module_phase1_5_goal_filter.md",
    PLATFORMS / "claude" / "SKILL.md",
    PLATFORMS / "grok" / "SKILL.md",
    PLATFORMS / "kimi" / "SKILL.md",
    PLATFORMS / "kimi-cli" / "SKILL.md",
    TESTS / "system" / "test_v140_features.py",
]

PER_MODULE_BUDGET_TOKENS = 2500


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _approx_tokens(text: str) -> int:
    return len(text) // 3


class TestPersonaRenameFiles(unittest.TestCase):
    """File-level rename: old files removed, new files present."""

    def test_old_persona_files_removed(self):
        for old in OLD_NAMES:
            self.assertFalse(
                (REFERENCES / old).exists(),
                f"Old persona file {old} must be removed (renamed to mode_*.md)",
            )

    def test_new_persona_files_present(self):
        for new in NEW_NAMES:
            self.assertTrue(
                (REFERENCES / new).exists(),
                f"New persona file {new} must exist after rename",
            )

    def test_persona_naming_convention_unified(self):
        """All 4 persona files start with `mode_` prefix."""
        for new in NEW_NAMES:
            self.assertTrue(
                new.startswith("mode_"),
                f"Persona file {new} must follow mode_<short> convention",
            )


class TestNoOldRefsInRuntimeFiles(unittest.TestCase):
    """Cross-reference cleanup: no old persona paths in runtime files."""

    def test_no_old_refs_in_runtime(self):
        violations = []
        for path in RUNTIME_CHECK_PATHS:
            if not path.exists():
                continue  # skip if file doesn't exist (e.g. lazy-build artifacts)
            body = _read(path)
            for old in OLD_NAMES:
                if old in body:
                    violations.append((path.relative_to(REPO_ROOT).as_posix(), old))
        self.assertFalse(
            violations,
            f"Old persona refs found in runtime files: {violations}. "
            "Run: python scripts/rename_persona_modules.py --apply",
        )

    def test_no_old_refs_in_phase_modules(self):
        """Specific check for module_phase*.md — they should all use new names."""
        for module in REFERENCES.glob("module_phase*.md"):
            body = _read(module)
            for old in OLD_NAMES:
                self.assertNotIn(
                    old,
                    body,
                    f"{module.name} must not reference old persona path '{old}'",
                )

    def test_master_routes_to_new_persona_paths(self):
        """Master Routing/Persona Detection must use new mode_* paths."""
        body = _read(REPO_ROOT / "SKILL.master.md")
        for new in NEW_NAMES:
            self.assertIn(
                new,
                body,
                f"SKILL.master.md must reference new persona path 'references/{new}'",
            )


class TestRenamedModulesBudget(unittest.TestCase):
    """Renamed modules must stay within per-module budget."""

    def test_renamed_modules_under_budget(self):
        oversize = []
        for new in NEW_NAMES:
            path = REFERENCES / new
            if not path.exists():
                continue
            tokens = _approx_tokens(_read(path))
            if tokens > PER_MODULE_BUDGET_TOKENS:
                oversize.append((new, tokens))
        self.assertFalse(
            oversize,
            f"Renamed persona modules over budget: {oversize}",
        )


if __name__ == "__main__":
    unittest.main()
