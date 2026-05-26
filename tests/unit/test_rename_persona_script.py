"""v1.0.0: smoke tests for scripts/rename_persona_modules.py.

This script ran as a one-shot migration in v0.19.0 but is preserved as a
template. Tests verify it loads, has correct mapping, and the replace helper
is safe to re-run (idempotent: nothing to replace after rename).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "rename_persona", PROJECT_ROOT / "scripts" / "rename_persona_modules.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_module_imports():
    mod = _load_module()
    assert hasattr(mod, "main")
    assert hasattr(mod, "RENAMES")
    assert hasattr(mod, "REPLACEMENTS")


def test_renames_mapping_complete():
    mod = _load_module()
    assert mod.RENAMES == {
        "adhd_mode.md": "mode_adhd.md",
        "time_structure_unemployed.md": "mode_unemployed.md",
        "elder_homebound_mode.md": "mode_elder.md",
        "planning_friction_audit.md": "mode_planning_friction.md",
    }


def test_replacements_include_both_path_forms():
    """Each rename should generate both `references/X` and `X` (bare) replacements."""
    mod = _load_module()
    pairs = {(old, new) for old, new in mod.REPLACEMENTS}
    for old, new in mod.RENAMES.items():
        assert (f"references/{old}", f"references/{new}") in pairs
        assert (old, new) in pairs


def test_replace_in_file_idempotent(tmp_path):
    mod = _load_module()
    # Create a file that has only NEW names (post-rename state)
    f = tmp_path / "test.md"
    f.write_text("see references/mode_adhd.md for ADHD support", encoding="utf-8")
    count = mod.replace_in_file(f, dry_run=True)
    assert count == 0, "Re-running rename on already-migrated file should be no-op"


def test_replace_in_file_replaces_old_paths(tmp_path):
    mod = _load_module()
    f = tmp_path / "test.md"
    f.write_text("see references/adhd_mode.md and references/time_structure_unemployed.md", encoding="utf-8")
    count = mod.replace_in_file(f, dry_run=False)
    assert count >= 2
    new_content = f.read_text(encoding="utf-8")
    assert "adhd_mode.md" not in new_content
    assert "mode_adhd.md" in new_content
    assert "time_structure_unemployed.md" not in new_content
    assert "mode_unemployed.md" in new_content


def test_skip_dirs_excludes_archive():
    mod = _load_module()
    assert "archive" in mod.SKIP_DIRS
    assert ".git" in mod.SKIP_DIRS
    assert "dist" in mod.SKIP_DIRS


def test_skip_files_excludes_self():
    mod = _load_module()
    assert "rename_persona_modules.py" in mod.SKIP_FILES


def test_find_files_excludes_skip_dirs(tmp_path, monkeypatch):
    """find_files should not enter SKIP_DIRS."""
    mod = _load_module()
    # Temporarily redirect REPO_ROOT
    monkeypatch.setattr(mod, "REPO_ROOT", tmp_path)

    (tmp_path / "keep.md").write_text("text")
    archive = tmp_path / "archive"
    archive.mkdir()
    (archive / "skip.md").write_text("text")

    files = mod.find_files()
    files_str = [str(f) for f in files]
    assert any("keep.md" in f for f in files_str)
    assert not any("archive" in f for f in files_str)
