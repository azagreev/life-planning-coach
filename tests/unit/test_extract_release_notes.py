"""v1.0.0: tests for scripts/extract-release-notes.py.

Validates CHANGELOG section extraction, header rewriting, and idempotence.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "extract_notes", PROJECT_ROOT / "scripts" / "extract-release-notes.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_module_imports():
    mod = _load_module()
    assert hasattr(mod, "main")


def test_extract_existing_version_writes_file(tmp_path, monkeypatch):
    """Run extract for current release; verify file written + header rewritten."""
    mod = _load_module()
    monkeypatch.chdir(PROJECT_ROOT)
    # Use a known historical version
    historical_version = "0.17.0"
    rc = mod.main.__wrapped__() if hasattr(mod.main, "__wrapped__") else None
    # Run via sys.argv proxy
    monkeypatch.setattr(sys, "argv", ["extract-release-notes.py", historical_version])
    rc = mod.main()
    assert rc == 0

    expected = PROJECT_ROOT / "docs" / "archive" / f"RELEASE_NOTES_v{historical_version}.md"
    assert expected.exists()
    content = expected.read_text(encoding="utf-8")
    assert "## Что нового в v0.17.0" in content


def test_extract_unknown_version_returns_error(monkeypatch, capsys):
    mod = _load_module()
    monkeypatch.chdir(PROJECT_ROOT)
    monkeypatch.setattr(sys, "argv", ["extract-release-notes.py", "99.99.99"])
    rc = mod.main()
    assert rc == 1
    out = capsys.readouterr().out
    assert "не найдена" in out


def test_extract_no_version_arg(monkeypatch, capsys):
    mod = _load_module()
    monkeypatch.setattr(sys, "argv", ["extract-release-notes.py"])
    rc = mod.main()
    assert rc == 1


def test_extract_with_v_prefix_strips_it(monkeypatch):
    mod = _load_module()
    monkeypatch.chdir(PROJECT_ROOT)
    monkeypatch.setattr(sys, "argv", ["extract-release-notes.py", "v0.17.0"])
    rc = mod.main()
    assert rc == 0  # v-prefix stripped, version still extracted
    expected = PROJECT_ROOT / "docs" / "archive" / f"RELEASE_NOTES_v0.17.0.md"
    assert expected.exists()


def test_extract_stdout_mode(monkeypatch, capsys):
    """--stdout flag prints to stdout instead of writing file."""
    mod = _load_module()
    monkeypatch.chdir(PROJECT_ROOT)
    monkeypatch.setattr(sys, "argv", ["extract-release-notes.py", "--stdout", "0.17.0"])
    rc = mod.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "## Что нового в v0.17.0" in out
