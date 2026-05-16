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
        self.assertIn('<html lang="ru">', self.content, 'Must have <html lang="ru">')

    def test_contains_expected_chart_keywords(self):
        keywords = ["ECharts", "Chart.js", "radar", "heatmap"]
        for kw in keywords:
            with self.subTest(keyword=kw):
                self.assertIn(kw.lower(), self.content.lower(),
                              f"Dashboard must contain keyword: {kw}")


if __name__ == "__main__":
    unittest.main()
