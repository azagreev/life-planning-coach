"""Regression tests for scripts/sync-version.sh.

History:
- v1.3.0 (PR #11) + v1.3.1 (PR #27): manual catchup PRs needed because
  sync-version.sh missed README badge + install refs. PR #27 extended
  sync-version.sh with badge + install-refs sed lines.
- v1.4.0 release (this session): sed delimiter conflict killed step 2
  partway through. The install-refs sed used `|` as delimiter AND as
  regex alternation (between `.zip|-grok.md|...` suffixes), confusing
  sed: «-e expression #1, char 48: unknown option to s'». Fix: switch
  to `#` as delimiter.

These tests guard against re-introducing the same anti-patterns.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SYNC_SH = PROJECT_ROOT / "scripts" / "sync-version.sh"


def test_sync_version_sh_exists() -> None:
    assert SYNC_SH.exists(), f"Missing {SYNC_SH}"


def test_install_refs_sed_uses_non_pipe_delimiter() -> None:
    """The install-refs sed must NOT use `|` as delimiter — the regex needs `|`
    for alternation between suffixes (.zip / -grok.md / -kimi.md / ...). Mixing
    delimiter with alternation killed the v1.4.0 release flow mid-sync."""
    content = SYNC_SH.read_text(encoding="utf-8")

    # Find the install-refs sed line. Sentinel — `life-planning-coach-v[0-9.]`
    # is a unique-enough prefix for that sed.
    install_refs_lines = [
        line for line in content.splitlines()
        if "life-planning-coach-v[0-9.]" in line and not line.lstrip().startswith("#")
    ]
    assert install_refs_lines, (
        "sync-version.sh must contain a sed bumping install refs "
        "(`life-planning-coach-vX.Y.Z.zip|-grok.md|-kimi.md|-kimi-cli.zip|-kimi-cli/`). "
        "If this fails, the install-refs sed got dropped — see PR #27 for why "
        "it must stay."
    )

    for line in install_refs_lines:
        # Anti-pattern: `sed -i -E "s|...|...|g"` где внутри pattern есть `|`
        # для alternation. Sed видит первый inner `|` как delimiter close.
        # Look for the `s|` opener (sed substitute с pipe delimiter).
        assert 's|' not in line.replace('sed -i', '').replace('-E', ''), (
            "sync-version.sh install-refs sed uses `|` as delimiter, but the "
            "regex pattern also uses `|` for alternation between suffixes. "
            "This kills step 2 with «-e expression #1, char N: unknown option «s\'»». "
            "Use `#` (or any other char absent from pattern) as delimiter. "
            f"Offending line: {line}"
        )


def test_install_refs_sed_uses_hash_delimiter() -> None:
    """Stronger positive check: the install-refs sed must explicitly use `#`
    delimiter (the fix applied after v1.4.0 release failure)."""
    content = SYNC_SH.read_text(encoding="utf-8")

    install_refs_lines = [
        line for line in content.splitlines()
        if "life-planning-coach-v[0-9.]" in line and not line.lstrip().startswith("#")
    ]
    assert install_refs_lines, "install-refs sed missing"

    for line in install_refs_lines:
        # Expected pattern: `sed -i -E "s#...#...#g"` with `#` as delimiter
        assert 's#' in line, (
            f"install-refs sed must use `#` delimiter (post-v1.4.0 fix). "
            f"Got line: {line}"
        )


def test_sync_version_sh_bumps_roadmap_current_version() -> None:
    """ROADMAP «Текущая версия» must also be bumped (added in v1.3.1 prep
    to prevent test_planning_docs_guardrails post-release failure)."""
    content = SYNC_SH.read_text(encoding="utf-8")
    assert "ROADMAP.md" in content, (
        "sync-version.sh must touch ROADMAP.md so `test_planning_docs_guardrails`"
        " stays green after release.sh creates the new tag. See PR #26."
    )
    # Must update «Текущая версия» line specifically
    assert "Текущая версия" in content, (
        "sync-version.sh must bump «Текущая версия» line, not just any ROADMAP edit."
    )


def test_sync_version_sh_bumps_readme_install_refs_and_badge() -> None:
    """README has 4 places that need bumping: **Версия:** line, version badge,
    install refs (3 files: .zip / -grok.md / -kimi.md / -kimi-cli.zip / -kimi-cli/)."""
    content = SYNC_SH.read_text(encoding="utf-8")
    assert "**Версия:**" in content, "Missing «**Версия:**» bump в sync-version.sh"
    assert "version-" in content and "-blue" in content, (
        "Missing version badge bump (`version-X.Y.Z-blue`)"
    )
    assert "life-planning-coach-v" in content, "Missing install refs bump"
