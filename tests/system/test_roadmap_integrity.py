"""
System tests for ROADMAP.md integrity.

Option B: ROADMAP "Текущий статус" contains ONLY future work.
Released versions must NOT appear in the status table.
"""

import subprocess
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestRoadmapIntegrity:
    """Ensure ROADMAP.md accurately reflects project status."""

    @pytest.fixture(scope="class")
    def released_versions(self):
        """Get all released versions from git tags."""
        result = subprocess.run(
            ["git", "tag", "--list", "v*"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        tags = result.stdout.strip().splitlines()
        # Return set of version strings without 'v' prefix
        return {tag.lstrip("v") for tag in tags}

    def _extract_status_table(self):
        """Extract the 'Текущий статус' table lines from ROADMAP.md."""
        roadmap = PROJECT_ROOT / "ROADMAP.md"
        content = roadmap.read_text(encoding="utf-8")
        lines = content.splitlines()

        in_status_section = False
        table_lines = []
        for line in lines:
            if line.strip().startswith("## Текущий статус"):
                in_status_section = True
                continue
            if in_status_section:
                # Stop at next heading or horizontal rule
                if line.strip().startswith("## ") or line.strip() == "---":
                    break
                table_lines.append(line)
        return table_lines

    def test_no_released_versions_in_status_table(self, released_versions):
        """Released versions must not appear in the 'Текущий статус' table."""
        table_lines = self._extract_status_table()
        table_text = "\n".join(table_lines)

        stale = []
        for version in released_versions:
            # Look for | vX.Y.Z | in the status table (exact table row, not substring)
            if f"| v{version} |" in table_text:
                stale.append(version)

        if stale:
            pytest.fail(
                f"ROADMAP.md 'Текущий статус' table contains released versions: {stale}\n"
                f"Released versions: {sorted(released_versions)}\n"
                f"Fix: remove released versions from status table. "
                f"Release history belongs in CHANGELOG.md."
            )
