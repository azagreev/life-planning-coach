"""v1.0.0: smoke tests for scripts/build-skill.py CLI.

Tests focus on:
- Argument parsing
- Version sync function (replace_in_file)
- Stale version scanner
- ZIP creation helper

End-to-end build/release flows are integration-tested via release.sh
exit codes (out of scope for unit tests — they require git/gh).
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from unittest.mock import patch

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))


def test_module_imports():
    """The module loads without syntax errors."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_skill", PROJECT_ROOT / "scripts" / "build-skill.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "main")
    assert hasattr(mod, "cmd_build")
    assert hasattr(mod, "cmd_version")
    assert hasattr(mod, "cmd_verify")
    assert hasattr(mod, "cmd_release")


def _load_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_skill", PROJECT_ROOT / "scripts" / "build-skill.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_read_skill_version_returns_semver():
    mod = _load_module()
    version = mod._read_skill_version()
    import re
    assert re.match(r"^\d+\.\d+\.\d+", version), f"Expected semver, got: {version}"


def test_replace_in_file_idempotent(tmp_path):
    mod = _load_module()
    f = tmp_path / "test.txt"
    f.write_text("version: 1.2.3", encoding="utf-8")
    count1 = mod._replace_in_file(f, r"version:\s*\S+", "version: 2.0.0")
    count2 = mod._replace_in_file(f, r"version:\s*\S+", "version: 2.0.0")
    assert count1 == 1
    assert count2 == 1  # still matches new pattern
    assert f.read_text(encoding="utf-8") == "version: 2.0.0"


def test_replace_in_file_no_match_returns_zero(tmp_path):
    mod = _load_module()
    f = tmp_path / "test.txt"
    f.write_text("content without version", encoding="utf-8")
    count = mod._replace_in_file(f, r"version:\s*\S+", "version: 2.0.0")
    assert count == 0


def test_cmd_version_rejects_bad_format(capsys):
    mod = _load_module()
    import argparse
    args = argparse.Namespace(version="not-semver")
    rc = mod.cmd_version(args)
    assert rc == 1
    err = capsys.readouterr().err
    assert "bad version format" in err.lower()


def test_cmd_version_accepts_semver():
    mod = _load_module()
    import argparse
    # Run version sync to current version (no-op) to validate flow
    current = mod._read_skill_version()
    args = argparse.Namespace(version=current)
    rc = mod.cmd_version(args)
    assert rc == 0


def test_copy_references_excludes_dev_only(tmp_path):
    mod = _load_module()
    src = tmp_path / "refs"
    src.mkdir()
    (src / "keep.md").write_text("keep")
    (src / "research_old.md").write_text("dev-only")
    (src / "acceptance_criteria_v1.md").write_text("dev-only")
    research = src / "research"
    research.mkdir()
    (research / "deep.md").write_text("dev-only")

    dst = tmp_path / "out"
    mod._copy_references(src, dst)

    assert (dst / "keep.md").exists()
    assert not (dst / "research_old.md").exists()
    assert not (dst / "acceptance_criteria_v1.md").exists()
    assert not (dst / "research").exists()


def test_make_zip_creates_dir_entry(tmp_path):
    mod = _load_module()
    src = tmp_path / "skill"
    src.mkdir()
    (src / "SKILL.md").write_text("test", encoding="utf-8")

    zip_path = tmp_path / "out.zip"
    mod._make_zip(zip_path, src, "myskill")

    import zipfile
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        assert "myskill/" in names, f"Missing root dir entry. Got: {names}"
        assert "myskill/SKILL.md" in names


def test_make_zip_normalizes_lf(tmp_path):
    mod = _load_module()
    src = tmp_path / "skill"
    src.mkdir()
    (src / "test.md").write_bytes(b"line1\r\nline2\r\n")

    zip_path = tmp_path / "out.zip"
    mod._make_zip(zip_path, src, "skill")

    import zipfile
    with zipfile.ZipFile(zip_path) as zf:
        content = zf.read("skill/test.md")
        assert b"\r\n" not in content
        assert content == b"line1\nline2\n"


def test_argparse_help_no_crash():
    mod = _load_module()
    with pytest.raises(SystemExit) as exc:
        mod.main(["--help"])
    assert exc.value.code == 0


def test_argparse_no_args_fails():
    mod = _load_module()
    with pytest.raises(SystemExit) as exc:
        mod.main([])
    assert exc.value.code != 0


def test_argparse_invalid_subcommand_fails():
    mod = _load_module()
    with pytest.raises(SystemExit) as exc:
        mod.main(["nonexistent"])
    assert exc.value.code != 0


def test_clean_prev_artifacts_keeps_current_removes_previous(tmp_path):
    """--clean-prev must delete prior-version artifacts but keep the current build."""
    mod = _load_module()
    dist = tmp_path / "dist"
    dist.mkdir()

    # Current version (must be kept)
    (dist / "life-planning-coach-v1.4.0.zip").write_text("cur", encoding="utf-8")
    (dist / "life-planning-coach-v1.4.0.skill").write_text("cur", encoding="utf-8")
    (dist / "life-planning-coach-v1.4.0-grok.md").write_text("cur", encoding="utf-8")
    cur_dir = dist / "life-planning-coach-v1.4.0"
    cur_dir.mkdir()
    (cur_dir / "SKILL.md").write_text("cur", encoding="utf-8")

    # Previous version (must be removed)
    (dist / "life-planning-coach-v1.3.1.zip").write_text("old", encoding="utf-8")
    (dist / "life-planning-coach-v1.3.1-kimi.md").write_text("old", encoding="utf-8")
    prev_dir = dist / "life-planning-coach-v1.3.1"
    prev_dir.mkdir()
    (prev_dir / "SKILL.md").write_text("old", encoding="utf-8")

    # Unrelated file (does not match glob — must be untouched)
    (dist / "README.txt").write_text("keep", encoding="utf-8")

    removed = mod._clean_prev_artifacts(dist, "1.4.0")

    assert {p.name for p in removed} == {
        "life-planning-coach-v1.3.1",
        "life-planning-coach-v1.3.1-kimi.md",
        "life-planning-coach-v1.3.1.zip",
    }
    # Current build kept
    assert (dist / "life-planning-coach-v1.4.0.zip").exists()
    assert (dist / "life-planning-coach-v1.4.0.skill").exists()
    assert (dist / "life-planning-coach-v1.4.0-grok.md").exists()
    assert cur_dir.exists()
    # Previous build removed (this is the bug the no-op silently skipped)
    assert not (dist / "life-planning-coach-v1.3.1.zip").exists()
    assert not (dist / "life-planning-coach-v1.3.1-kimi.md").exists()
    assert not prev_dir.exists()
    # Unrelated file untouched
    assert (dist / "README.txt").exists()


def test_clean_prev_artifacts_missing_dir_returns_empty(tmp_path):
    """No dist dir → no-op, returns empty list (not a crash)."""
    mod = _load_module()
    assert mod._clean_prev_artifacts(tmp_path / "nonexistent", "1.4.0") == []
