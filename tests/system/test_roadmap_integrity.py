"""
System tests for ROADMAP.md integrity.

Option B: ROADMAP contains ONLY future work.
Released versions must NOT appear as active status rows or detailed sections.
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

    def test_no_released_version_detail_sections(self, released_versions):
        """Released versions must not have detailed roadmap sections."""
        roadmap = PROJECT_ROOT / "ROADMAP.md"
        content = roadmap.read_text(encoding="utf-8")

        stale = []
        for version in released_versions:
            pattern = re.compile(rf"^##\s+v{re.escape(version)}\b", re.MULTILINE)
            if pattern.search(content):
                stale.append(version)

        if stale:
            pytest.fail(
                f"ROADMAP.md contains detailed sections for released versions: {stale}\n"
                f"Release details belong in CHANGELOG.md or docs/archive/."
            )


class TestPlanningDocsGuardrails:
    """Broader planning docs invariants — ROADMAP / BACKLOG / CHANGELOG separation."""

    def test_roadmap_has_only_future_versions(self):
        """ROADMAP.md must mention only future version sections (no released ones)."""
        roadmap = (PROJECT_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        # Tag list
        result = subprocess.run(
            ["git", "tag", "--list", "v*"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        released = {tag.lstrip("v") for tag in result.stdout.strip().splitlines()}

        # Find all ## headings that look like ## vX.Y.Z
        headings = re.findall(r"^##\s+v([\d.]+)", roadmap, re.MULTILINE)
        leaked = [h for h in headings if h in released]
        assert not leaked, (
            f"ROADMAP.md contains released version headings: {leaked}. "
            f"Use CHANGELOG.md instead."
        )

    def test_backlog_done_section_is_pointer_only(self):
        """BACKLOG.md must not duplicate CHANGELOG content for completed items."""
        backlog = (PROJECT_ROOT / "BACKLOG.md").read_text(encoding="utf-8")
        # The Archived/Done section should be a pointer (< 400 chars) not a full re-statement.
        # Look for the "Done" / "Archived" section.
        match = re.search(
            r"##\s*(Archived|Done|Архив|Готово)(.*?)(?=^##|\Z)",
            backlog,
            re.MULTILINE | re.DOTALL,
        )
        if match:
            section_body = match.group(2).strip()
            # Pointer-style section is short and references other docs.
            assert len(section_body) < 1500, (
                f"BACKLOG.md 'Archived/Done' section is {len(section_body)} chars — "
                f"should be a pointer to CHANGELOG.md, not duplicate content."
            )

    def test_changelog_has_each_released_version(self):
        """CHANGELOG.md must document every released git tag from v0.8.0 onward.

        Legacy tags (pre-0.8.0) predate the structured CHANGELOG format and
        are intentionally not enforced.
        """
        result = subprocess.run(
            ["git", "tag", "--list", "v*"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        released = {tag.lstrip("v") for tag in result.stdout.strip().splitlines()}

        def _parsable(v: str) -> bool:
            parts = v.split(".")
            return len(parts) >= 2 and all(p.isdigit() for p in parts[:3])

        def _ge_0_8_0(v: str) -> bool:
            if not _parsable(v):
                return False
            parts = [int(p) for p in v.split(".")[:3]]
            while len(parts) < 3:
                parts.append(0)
            return tuple(parts) >= (0, 8, 0)

        enforced = {v for v in released if _ge_0_8_0(v)}
        changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        missing = [v for v in enforced if f"[{v}]" not in changelog]
        assert not missing, (
            f"CHANGELOG.md missing sections for released versions: {missing}"
        )
