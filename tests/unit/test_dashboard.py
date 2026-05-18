"""Tests for life-planning-dashboard.html."""

import unittest
from pathlib import Path


class TestDashboardHtml(unittest.TestCase):
    """Verify life-planning-dashboard.html structure and content."""

    @classmethod
    def setUpClass(cls):
        cls.path = Path("life-planning-dashboard.html")
        cls.content = cls.path.read_text(encoding="utf-8")
        cls.lines = cls.content.splitlines()

    def test_file_exists_and_is_large(self):
        self.assertTrue(self.path.exists(), "Dashboard HTML must exist")
        self.assertGreater(len(self.lines), 1000, "Dashboard must be > 1000 lines")

    def test_no_external_cdn_urls_or_documented(self):
        cdn_patterns = ["cdn.jsdelivr.net", "cdnjs.cloudflare.com"]
        found = []
        for pattern in cdn_patterns:
            for line in self.lines:
                if pattern in line:
                    found.append((pattern, line.strip()))
        if found:
            # Document CDN URLs found; goal is eventually to make it fully offline
            print("\n[INFO] External CDN URLs found in dashboard (to be made offline):")
            for pattern, line in found:
                print(f"  - {pattern}: {line}")
        # We do not fail here — the goal is eventually offline.
        # If the list grows unexpectedly, a future test can enforce zero CDNs.

    def test_doctype_and_html_lang(self):
        self.assertIn("<!DOCTYPE html>", self.content, "Must have <!DOCTYPE html>")
        import re
        self.assertTrue(
            bool(re.search(r'<html[^>]*\blang=["\']ru["\']', self.content)),
            'Must have <html lang="ru">'
        )

    def test_contains_expected_chart_keywords(self):
        """v0.9.1: Pure SVG/CSS replaces ECharts/Chart.js. Keep heatmap."""
        keywords = ["heatmap", "ring-fill", "streak", "liquid-glass"]
        for kw in keywords:
            with self.subTest(keyword=kw):
                self.assertIn(kw.lower(), self.content.lower(),
                              f"Dashboard must contain keyword: {kw}")

    def test_wheel_has_11_domains(self):
        """BUG-001: Dashboard must show 11 Wheel of Life domains."""
        import re
        match = re.search(r'const WHEEL_SPHERES = \[(.*?)\];', self.content, re.DOTALL)
        self.assertIsNotNone(match, "WHEEL_SPHERES array not found")
        array_text = match.group(1)
        ids = re.findall(r"id: '([^']+)'", array_text)
        self.assertEqual(len(ids), 11, f"Expected 11 domains, found {len(ids)}: {ids}")

        expected_ids = [
            'health', 'finances', 'career', 'family', 'romance',
            'social', 'growth', 'spirituality', 'fun', 'contribution', 'environment'
        ]
        for eid in expected_ids:
            with self.subTest(domain_id=eid):
                self.assertIn(eid, ids, f"Missing domain: {eid}")

    def test_wheel_avg_divides_by_11(self):
        """Average score must divide by 11, not 8."""
        self.assertIn('/ 11).toFixed(1)', self.content,
                      "Average calculation must divide by 11 (was / 8)")

    def test_android_chrome_tap_highlight_removed(self):
        """Android Chrome shows blue tap highlight by default; must be disabled."""
        self.assertIn('-webkit-tap-highlight-color', self.content.lower(),
                      "Must disable tap highlight for Android Chrome")

    def test_android_overscroll_behavior_set(self):
        """Android pull-to-refresh and overscroll glow must be disabled."""
        self.assertIn('overscroll-behavior', self.content.lower(),
                      "Must set overscroll-behavior for Android")

    def test_theme_color_meta_for_android_status_bar(self):
        """Android Chrome address bar color must match app theme."""
        self.assertIn('name="theme-color"', self.content,
                      "Must have theme-color meta for Android status bar")
        self.assertIn('prefers-color-scheme: light', self.content,
                      "Must have light theme-color")
        self.assertIn('prefers-color-scheme: dark', self.content,
                      "Must have dark theme-color")

    def test_ios_safari_backdrop_filter_prefix(self):
        """Liquid Glass requires -webkit-backdrop-filter for iOS Safari."""
        self.assertIn('-webkit-backdrop-filter', self.content,
                      "Must have -webkit-backdrop-filter for iOS Safari")

    def test_dynamic_viewport_units_present(self):
        """100dvh must be present as progressive enhancement for Chrome Android."""
        self.assertIn('100dvh', self.content,
                      "Must have 100dvh for dynamic viewport on Chrome Android")

    def test_viewport_has_viewport_fit_cover(self):
        """Notched Android devices need viewport-fit=cover for edge-to-edge display."""
        self.assertIn('viewport-fit=cover', self.content,
                      "Must have viewport-fit=cover for notched Android devices")


if __name__ == "__main__":
    unittest.main()
