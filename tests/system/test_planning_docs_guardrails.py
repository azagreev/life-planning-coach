"""System tests for planning-docs hygiene guardrails.

Closes BACKLOG tech-debt «Planning docs guardrails» (RICE 64, ~0.5 EAS).

Catches the regressions we manually cleaned up in PR #19:

- ROADMAP `## Текущая версия` not matching the latest git tag.
- ROADMAP scope sections («## vX.Y.Z (planned/TBD/Candidate)») drifting
  into changelog-style content («✅ Shipped», «released», `## [X.Y.Z]`).
- ROADMAP carrying leftover double `---` separators after a section
  removal (left behind in v1.3.0 ship → cleaned in PR #19).
- ROADMAP / BACKLOG containing duplicate H3 headings within the same H2
  section (the «Интеграция с Google Tasks MCP» duplicate fixed in PR #19).
- ROADMAP's claimed «Текущая версия» missing from CHANGELOG.md (would
  mean an undocumented release or an off-by-one mismatch).

These tests cover the «roadmap не превращается в changelog» rule from the
Tech Debt table without requiring manual review of every PR touching
planning docs.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
ROADMAP = PROJECT_ROOT / "ROADMAP.md"
BACKLOG = PROJECT_ROOT / "BACKLOG.md"
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _latest_git_tag() -> str | None:
    """Return latest annotated tag (`vX.Y.Z`), stripped of leading `v`.

    Returns None if git is unavailable or repo is shallow without tags —
    so tests can skip cleanly instead of failing the wrong thing.
    """
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout.strip().lstrip("v")


def _parse_h2_sections(content: str) -> dict[str, str]:
    """Return mapping of H2 heading text → section body (excluding the heading line)."""
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_body: list[str] = []
    for line in content.splitlines():
        if line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_body)
            current_heading = line[3:].strip()
            current_body = []
        else:
            if current_heading is not None:
                current_body.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_body)
    return sections


def _h3_headings_in(section_body: str) -> list[str]:
    return [
        line[4:].strip()
        for line in section_body.splitlines()
        if line.startswith("### ")
    ]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def roadmap_text() -> str:
    assert ROADMAP.exists(), f"Missing {ROADMAP}"
    return ROADMAP.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def backlog_text() -> str:
    assert BACKLOG.exists(), f"Missing {BACKLOG}"
    return BACKLOG.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def changelog_text() -> str:
    assert CHANGELOG.exists(), f"Missing {CHANGELOG}"
    return CHANGELOG.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Current-version coherence
# ---------------------------------------------------------------------------


class TestCurrentVersionCoherence:
    """ROADMAP `Текущая версия` must agree with git tags and CHANGELOG."""

    def test_roadmap_declares_current_version(self, roadmap_text: str) -> None:
        match = re.search(r"\*\*Текущая версия:\*\*\s*`v([\d.]+)`", roadmap_text)
        assert match, (
            "ROADMAP.md must have a single `**Текущая версия:** `vX.Y.Z`` line "
            "in the `Текущий статус` section."
        )

    def test_roadmap_version_matches_latest_git_tag(self, roadmap_text: str) -> None:
        latest_tag = _latest_git_tag()
        if latest_tag is None:
            pytest.skip(
                "git describe unavailable (shallow clone / missing tags) — "
                "tag/ROADMAP mismatch is enforced in environments where tags exist."
            )
        match = re.search(r"\*\*Текущая версия:\*\*\s*`v([\d.]+)`", roadmap_text)
        assert match, "Текущая версия line missing — see test_roadmap_declares_current_version"
        roadmap_version = match.group(1)
        assert roadmap_version == latest_tag, (
            f"ROADMAP.md «Текущая версия» = v{roadmap_version} but latest git "
            f"tag = v{latest_tag}. Run `bash scripts/release.sh X.Y.Z` or update "
            "ROADMAP manually so the two stay in sync."
        )

    def test_roadmap_version_present_in_changelog(
        self, roadmap_text: str, changelog_text: str
    ) -> None:
        match = re.search(r"\*\*Текущая версия:\*\*\s*`v([\d.]+)`", roadmap_text)
        assert match, "Текущая версия line missing"
        version = match.group(1)
        assert f"## [{version}]" in changelog_text, (
            f"ROADMAP claims current version v{version} but CHANGELOG has no "
            f"`## [{version}]` heading. Either CHANGELOG entry is missing or "
            "ROADMAP version is stale."
        )


# ---------------------------------------------------------------------------
# Scope sections must stay forward-looking (no changelog drift)
# ---------------------------------------------------------------------------


# Heading pattern for "future scope" sections in ROADMAP:
#   "## v1.4.0 (TBD)", "## v0.17.x Candidate", "## v1.3.0 (planned)"
# Anything matching `## vX.Y.* (planned|TBD|Candidate)` or a bare candidate
# heading counts as forward scope.
_SCOPE_HEADING_RE = re.compile(
    r"^## v[\d.]+(?:\.x)?\s*(?:[—-]\s*)?(?:\(planned\)|\(TBD\)|Candidate)",
    re.IGNORECASE,
)


def _scope_sections(roadmap_text: str) -> dict[str, str]:
    return {
        heading: body
        for heading, body in _parse_h2_sections(roadmap_text).items()
        if _SCOPE_HEADING_RE.match("## " + heading)
    }


class TestScopeSectionsNoChangelogDrift:
    """`## vX.Y.Z (planned/TBD/Candidate)` sections must stay forward-looking."""

    def test_at_least_one_scope_section_exists(self, roadmap_text: str) -> None:
        """Sanity check — отсутствие scope-секций = degenerate ROADMAP."""
        sections = _scope_sections(roadmap_text)
        assert sections, (
            "ROADMAP must have ≥ 1 forward-scope section (e.g. "
            "`## v1.4.0 (TBD)` or `## v0.17.x Candidate`). Otherwise it's "
            "just an archive — move forward work back in."
        )

    def test_scope_sections_have_no_shipped_emoji(self, roadmap_text: str) -> None:
        """Forward scope must not contain `✅ Shipped` or `✅ Closed` markers."""
        for heading, body in _scope_sections(roadmap_text).items():
            for marker in ("✅ Shipped", "✅ Closed", "✅ Done"):
                assert marker not in body, (
                    f"ROADMAP scope section `## {heading}` contains «{marker}» — "
                    "shipped items belong in CHANGELOG.md, not in forward scope. "
                    "Move the entry out (see PR #19 for an example pass)."
                )

    def test_scope_sections_no_changelog_style_version_headings(
        self, roadmap_text: str
    ) -> None:
        """No `## [X.Y.Z]` (changelog format) inside forward scope."""
        for heading, body in _scope_sections(roadmap_text).items():
            # `## [` would appear in body only if the H2 starts inside scope
            # body, which is malformed. More commonly we'd see `### [X.Y.Z]`.
            assert not re.search(r"^###?\s+\[\d+\.\d+\.\d+\]", body, re.MULTILINE), (
                f"ROADMAP scope section `## {heading}` contains a "
                "`## [X.Y.Z]` or `### [X.Y.Z]` heading — that's CHANGELOG.md "
                "syntax. Forward scope should use `(planned)` / `(TBD)` markers."
            )

    def test_scope_sections_no_released_wording(self, roadmap_text: str) -> None:
        """Forward scope must not say «released» or «выпущено» about its own items."""
        forbidden_phrases = [
            r"\breleased\s+\d{4}-\d{2}-\d{2}",  # "released 2026-05-27"
            r"\bshipped\s+\d{4}-\d{2}-\d{2}",  # "shipped 2026-05-27"
            r"\bвыпущено\b",
        ]
        for heading, body in _scope_sections(roadmap_text).items():
            for pat in forbidden_phrases:
                match = re.search(pat, body, re.IGNORECASE)
                assert not match, (
                    f"ROADMAP scope section `## {heading}` contains «{match.group(0)}»"
                    f" — release dates belong in CHANGELOG.md, not forward scope."
                )


# ---------------------------------------------------------------------------
# Structural hygiene
# ---------------------------------------------------------------------------


class TestStructuralHygiene:
    """Structural patterns that leak through manual edits."""

    def test_roadmap_has_no_consecutive_separators(self, roadmap_text: str) -> None:
        """`---` followed by another `---` (with only blank lines between) = orphaned section."""
        # Match `---\n\n---` (allowing blank lines/whitespace between).
        assert not re.search(r"^---\s*\n(?:\s*\n)+---\s*$", roadmap_text, re.MULTILINE), (
            "ROADMAP.md has consecutive `---` separators (likely leftover "
            "from removing a section). Clean up to single `---` divider."
        )

    def test_backlog_has_no_consecutive_separators(self, backlog_text: str) -> None:
        assert not re.search(r"^---\s*\n(?:\s*\n)+---\s*$", backlog_text, re.MULTILINE), (
            "BACKLOG.md has consecutive `---` separators."
        )

    def test_roadmap_no_duplicate_h3_within_section(self, roadmap_text: str) -> None:
        self._assert_no_duplicate_h3(roadmap_text, doc="ROADMAP.md")

    def test_backlog_no_duplicate_h3_within_section(self, backlog_text: str) -> None:
        self._assert_no_duplicate_h3(backlog_text, doc="BACKLOG.md")

    @staticmethod
    def _assert_no_duplicate_h3(content: str, doc: str) -> None:
        for h2, body in _parse_h2_sections(content).items():
            h3s = _h3_headings_in(body)
            seen: dict[str, int] = {}
            for h3 in h3s:
                seen[h3] = seen.get(h3, 0) + 1
            duplicates = [h3 for h3, count in seen.items() if count > 1]
            assert not duplicates, (
                f"{doc} section `## {h2}` has duplicate H3 headings: "
                f"{duplicates}. Each entry must appear once "
                "(see «Интеграция с Google Tasks MCP» dedup in PR #19)."
            )
