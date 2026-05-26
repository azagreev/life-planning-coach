"""Tests for state_v2 templates rebuild (B5).

Covers:
- Canonical 11 sphere IDs across all artefacts (no drift)
- state_v2_schema.md structure completeness
- HTML dashboard is data-driven (no hardcoded sphere arrays)
- Wiki templates carry schema_version frontmatter
- dashboard_guide.md is the thin runtime variant (≤300 lines)
- Index.md refs resolve to existing template files
- Token budgets for wiki templates
"""

import re
import unittest
from pathlib import Path


CANONICAL_SPHERES = [
    "health",
    "finances",
    "career",
    "family",
    "romance",
    "social",
    "personal_growth",
    "meaning",
    "fun_recreation",
    "contribution",
    "physical_environment",
]

LEGACY_SPHERE_IDS = ["growth", "spirituality", "fun", "environment"]

REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCES = REPO_ROOT / "references"
TEMPLATES = REFERENCES / "templates"


def _approx_tokens(text: str) -> int:
    """Rough Russian-text token estimate: ~1 token per 3 chars."""
    return len(text) // 3


class TestCanonicalSpheres(unittest.TestCase):
    """All artefacts must use the same canonical 11 sphere IDs."""

    def test_state_v2_schema_lists_11_canonical_ids(self):
        path = REFERENCES / "state_v2_schema.md"
        self.assertTrue(path.exists(), "state_v2_schema.md must exist")
        content = path.read_text(encoding="utf-8")
        for sphere_id in CANONICAL_SPHERES:
            self.assertIn(
                f"`{sphere_id}`",
                content,
                f"state_v2_schema.md must mention canonical id `{sphere_id}`",
            )

    def test_html_dashboard_uses_canonical_ids(self):
        html = REPO_ROOT / "life-planning-dashboard.html"
        content = html.read_text(encoding="utf-8")
        match = re.search(r"CANONICAL_SPHERE_IDS\s*=\s*Object\.keys\(SPHERE_META\)", content)
        self.assertIsNotNone(
            match,
            "HTML dashboard must derive CANONICAL_SPHERE_IDS from SPHERE_META",
        )
        for sphere_id in CANONICAL_SPHERES:
            self.assertRegex(
                content,
                rf"\b{sphere_id}\b\s*:\s*\{{",
                f"SPHERE_META must define canonical id `{sphere_id}`",
            )

    def test_html_dashboard_has_no_legacy_sphere_ids(self):
        html = REPO_ROOT / "life-planning-dashboard.html"
        content = html.read_text(encoding="utf-8")
        # Allow legacy mentions only inside HTML/JS comments noting deprecation
        for legacy in LEGACY_SPHERE_IDS:
            pattern = rf"(?:id|sphere_id)\s*[:=]\s*['\"]{legacy}['\"]"
            self.assertIsNone(
                re.search(pattern, content),
                f"HTML dashboard must not use legacy sphere id `{legacy}`",
            )

    def test_wheel_of_life_history_template_uses_canonical_ids(self):
        path = TEMPLATES / "Wheel_of_Life_History.md"
        content = path.read_text(encoding="utf-8")
        for sphere_id in CANONICAL_SPHERES:
            self.assertIn(
                f"`{sphere_id}`",
                content,
                f"Wheel_of_Life_History.md must reference canonical id `{sphere_id}`",
            )
        # 11 spheres declared in frontmatter
        self.assertIn("spheres_count: 11", content)


class TestStateV2SchemaCompleteness(unittest.TestCase):
    """state_v2_schema.md contains all required top-level keys."""

    REQUIRED_TOP_KEYS = [
        "schema_version",
        "user_id",
        '"session"',
        '"persona"',
        '"communication_style"',
        '"diagnosis"',
        '"goals"',
        '"goal_filter"',
        '"habits"',
        '"weekly_reviews"',
        '"emotion_regulation_log"',
        '"wins_log"',
        '"reward_audit_results"',
        '"calendar_events_log"',
        '"recovery_sessions_log"',
        '"persistence_retry"',
    ]

    def test_all_top_level_keys_present(self):
        path = REFERENCES / "state_v2_schema.md"
        content = path.read_text(encoding="utf-8")
        for key in self.REQUIRED_TOP_KEYS:
            self.assertIn(key, content, f"state_v2 schema missing key: {key}")

    def test_schema_version_is_2_0(self):
        content = (REFERENCES / "state_v2_schema.md").read_text(encoding="utf-8")
        self.assertIn('"schema_version": "2.0"', content)

    def test_core_values_block_present(self):
        content = (REFERENCES / "state_v2_schema.md").read_text(encoding="utf-8")
        self.assertIn('"core_values"', content)
        self.assertIn("compass_question", content)
        self.assertIn("derived_from", content)
        self.assertIn("priority_rank", content)


class TestHtmlDataDriven(unittest.TestCase):
    """HTML dashboard must read window.lpData, not hardcode user data."""

    @classmethod
    def setUpClass(cls):
        cls.content = (REPO_ROOT / "life-planning-dashboard.html").read_text(encoding="utf-8")

    def test_resolves_window_lp_data(self):
        self.assertIn("window.lpData", self.content)
        self.assertIn("function resolveData()", self.content)

    def test_sample_fallback_isolated(self):
        # SAMPLE_FALLBACK is a single named const, not an ad-hoc data dump.
        self.assertIn("const SAMPLE_FALLBACK", self.content)
        # Old data names removed in favor of LP_DATA-derived consts.
        self.assertNotIn("// DATA STRUCTURES — preserved from v0.9.0", self.content)

    def test_schema_version_compatibility_check(self):
        self.assertIn("SUPPORTED_SCHEMA_MAJOR", self.content)
        self.assertRegex(self.content, r"SUPPORTED_SCHEMA_MAJOR\s*=\s*2")

    def test_core_values_panel_rendered(self):
        self.assertIn("renderCoreValues", self.content)
        self.assertIn('id="core-values-list"', self.content)

    def test_health_and_concordance_placeholders_present(self):
        # Hidden by default, become visible when schema 2.1 / 2.2 data arrives.
        self.assertIn('id="health-track-card"', self.content)
        self.assertIn('id="concordance-card"', self.content)
        self.assertIn("renderHealthTrack", self.content)
        self.assertIn("renderConcordance", self.content)

    def test_version_bumped(self):
        self.assertIn("LIFE PLANNING COACH DASHBOARD v1.0.0", self.content)


class TestWikiTemplatesV2(unittest.TestCase):
    """All wiki templates carry schema_version: 2.0 frontmatter."""

    EXPECTED_TEMPLATES = [
        "AI_Instructions.md",
        "Hot_Cache.md",
        "Index.md",
        "Goals.md",
        "Wheel_of_Life_History.md",
        "Raw_Session.md",
        "Progress_Dashboard.md",
        "USER_PROGRESS_JOURNAL.md",
        "Core_Values_Compass.md",
    ]

    def test_all_templates_exist(self):
        for fname in self.EXPECTED_TEMPLATES:
            self.assertTrue(
                (TEMPLATES / fname).exists(),
                f"Missing template: {fname}",
            )

    def test_all_templates_have_schema_version(self):
        for fname in self.EXPECTED_TEMPLATES:
            content = (TEMPLATES / fname).read_text(encoding="utf-8")
            self.assertIn(
                'schema_version: "2.0"',
                content,
                f"{fname} must declare schema_version: 2.0 in frontmatter",
            )

    def test_index_refs_resolve(self):
        """Index.md must not reference non-existent template files."""
        index = (TEMPLATES / "Index.md").read_text(encoding="utf-8")
        # Index references files relative to wiki root, not template root.
        # We only check that legacy refs to Concepts/ and Frameworks/ are gone.
        self.assertNotIn("Concepts/Wheel_of_Life.md", index)
        self.assertNotIn("Concepts/WOOP.md", index)
        self.assertNotIn("Concepts/OKR.md", index)
        self.assertNotIn("Frameworks/Weekly_Review.md", index)
        self.assertNotIn("Frameworks/Focus_Blocks.md", index)
        # Required new ref
        self.assertIn("Core_Values_Compass.md", index)


class TestWikiTemplateTokenBudgets(unittest.TestCase):
    """Per-template token budgets per AI_Instructions.md §Token-бюджеты."""

    # Budgets sized to v2 richness (AGF radar, Core Values, Habits Loop, etc).
    # Heavy templates (Goals/Wheel) carry the most user data and warrant larger budgets.
    BUDGETS = {
        "Hot_Cache.md": 1000,
        "Index.md": 500,
        "Goals.md": 2500,
        "Wheel_of_Life_History.md": 3000,
        "Core_Values_Compass.md": 2000,
        "Raw_Session.md": 800,
        "USER_PROGRESS_JOURNAL.md": 1500,
        "Progress_Dashboard.md": 2000,
        "AI_Instructions.md": 2000,
    }

    def test_each_template_within_budget(self):
        for fname, budget in self.BUDGETS.items():
            content = (TEMPLATES / fname).read_text(encoding="utf-8")
            tokens = _approx_tokens(content)
            self.assertLessEqual(
                tokens,
                budget,
                f"{fname}: {tokens} tokens > budget {budget}",
            )


class TestDashboardGuideThin(unittest.TestCase):
    """references/dashboard_guide.md must be the thin runtime variant."""

    def test_dashboard_guide_is_thin(self):
        path = REFERENCES / "dashboard_guide.md"
        self.assertTrue(path.exists())
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(
            len(lines),
            300,
            f"dashboard_guide.md must be ≤300 lines (got {len(lines)}). "
            "Heavy architecture content belongs in docs/research/dashboard_architecture_v1.md",
        )

    def test_heavy_architecture_moved_to_docs(self):
        archive = REPO_ROOT / "docs" / "research" / "dashboard_architecture_v1.md"
        self.assertTrue(
            archive.exists(),
            "Heavy dashboard architecture doc must live in docs/research/dashboard_architecture_v1.md",
        )

    def test_dashboard_guide_references_state_v2(self):
        content = (REFERENCES / "dashboard_guide.md").read_text(encoding="utf-8")
        self.assertIn("state_v2_schema", content)
        self.assertIn("window.lpData", content)


class TestSchemaVersioning(unittest.TestCase):
    """Schema bumps must be additive (v2.x stays compatible with v2.0 clients)."""

    def test_html_accepts_2_x_schema(self):
        content = (REPO_ROOT / "life-planning-dashboard.html").read_text(encoding="utf-8")
        self.assertIn("SUPPORTED_SCHEMA_MAJOR", content)
        # Check the compat logic: major mismatch falls back, minor bumps pass through
        self.assertRegex(content, r"major\s*!==\s*SUPPORTED_SCHEMA_MAJOR")


if __name__ == "__main__":
    unittest.main()
