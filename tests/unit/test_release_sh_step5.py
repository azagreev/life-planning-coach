"""Regression tests for release.sh step 5 fixes — BUG-008 + BUG-010.

История:
- BUG-008 (v1.3.0, PR #14): step 5 крашился на Windows cp1251 с
  `Python write /dev/stdout: The pipe is being closed.`. Root cause —
  inline Python `print(content.decode('utf-8'))` пытался записать UTF-8
  README (emoji 🧭, кириллица) в cp1251 stdout → UnicodeEncodeError →
  pipe break. Fix: `sys.stdout.buffer.write(bytes)` — binary write
  bypass'ит text encoding entirely.

- BUG-010 (v1.3.1 release, fixed in v1.3.2+ prep): рецидив того же
  «pipe is being closed» error. После BUG-008 fix encoding больше не
  проблема, но `grep -oP` находит match рано и закрывает upstream pipe,
  пока Python всё ещё writing decoded bytes (~3-5 KB README). Python
  raises BrokenPipeError → exits non-zero → empty result → check fails
  даже если GitHub README correct. Fix: decode → temp-file, потом grep
  на файл (sequential, no concurrent pipe → no early-exit issue).

Эти тесты ловят регрессии обоих багов: если кто-то откатит fix BUG-008
(вернёт `print(decode)` pattern) или BUG-010 (вернёт pipe-to-grep вместо
temp-file) — fail с указанием bug ID.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASE_SH = PROJECT_ROOT / "scripts" / "release.sh"


def test_release_sh_exists():
    assert RELEASE_SH.exists(), f"Missing {RELEASE_SH}"


def test_step5_uses_binary_stdout_write():
    """Step 5 line с inline python -c — должен использовать sys.stdout.buffer.write,
    не print(content.decode('utf-8'))."""
    source = RELEASE_SH.read_text(encoding="utf-8")

    assert "sys.stdout.buffer.write" in source, (
        "scripts/release.sh step 5 должен использовать sys.stdout.buffer.write(bytes) "
        "вместо print(content.decode('utf-8')) для Windows cp1251 compat (BUG-008). "
        "См. BUGS.md → BUG-008 для контекста."
    )


def test_step5_does_not_use_problematic_print_pattern():
    """Anti-pattern check: print(base64.b64decode(...).decode('utf-8')) was the original bug."""
    source = RELEASE_SH.read_text(encoding="utf-8")

    # Конкретный pattern BUG-008 — не должен повторяться
    assert "print(base64.b64decode" not in source, (
        "BUG-008 anti-pattern detected: print(base64.b64decode(...).decode(...)) "
        "крашит Windows cp1251 stdout. Используй sys.stdout.buffer.write(bytes) вместо."
    )


def test_step5_chain_intact():
    """Sanity check: step 5 still uses gh api + python decode + grep."""
    source = RELEASE_SH.read_text(encoding="utf-8")

    step5_idx = source.find("[5/7] Проверка на GitHub")
    assert step5_idx != -1, "Step 5 header missing"

    # Step 5 body extends ~1200 chars now (temp-file approach takes more lines)
    step5_block = source[step5_idx:step5_idx + 1500]
    assert "gh api" in step5_block, "gh api call missing в step 5"
    assert "base64.b64decode" in step5_block, "base64 decode missing в step 5"
    assert "grep" in step5_block, "grep call missing в step 5"


def test_step5_uses_temp_file_not_pipe_to_grep():
    """BUG-010 fix: decoded README must go to a temp file, not piped to grep.

    Anti-pattern: `python -c ...decode... | grep -oP ...` — grep early-exit
    closes upstream pipe → Python BrokenPipeError → empty result. Fix:
    write decoded bytes to a temp file, then grep on the file (sequential,
    no concurrent pipe lifecycle).
    """
    source = RELEASE_SH.read_text(encoding="utf-8")

    step5_idx = source.find("[5/7] Проверка на GitHub")
    assert step5_idx != -1, "Step 5 header missing"
    step5_block = source[step5_idx:step5_idx + 1500]

    # mktemp pattern signals temp-file approach
    assert "mktemp" in step5_block, (
        "BUG-010 fix expects `mktemp` + redirect-to-file pattern in step 5. "
        "Piping `python -c ...decode...` directly to grep risks BrokenPipeError "
        "when grep matches early. See BUGS.md → BUG-010 для контекста."
    )

    # grep should read from the temp file path, not from a pipe
    # (look for `grep ... "$TMP_README"` or similar variable-path pattern)
    assert "TMP_README" in step5_block, (
        "BUG-010 fix expects `TMP_README` variable holding decoded README "
        "path so grep reads from disk, not from a closing pipe."
    )

    # trap EXIT cleanup ensures temp-file deletion even on failure mid-step
    assert "trap" in step5_block and "EXIT" in step5_block, (
        "BUG-010 fix expects `trap '... EXIT'` to guarantee temp-file cleanup "
        "even if a later command (e.g. grep) fails."
    )


def test_step5_does_not_use_pipe_python_to_grep_directly():
    """Anti-pattern check: `python -c '...sys.stdout.buffer.write...' | grep`
    is the BUG-010 reproducer. Must not appear in release.sh."""
    source = RELEASE_SH.read_text(encoding="utf-8")

    step5_idx = source.find("[5/7] Проверка на GitHub")
    step5_block = source[step5_idx:step5_idx + 1500]

    # Direct python -> grep pipe is the BUG-010 anti-pattern.
    # Look for the literal `| grep` immediately after a python -c block.
    # `python -c "..."` followed (possibly with whitespace/backslash continuation)
    # by `| grep` indicates the broken pattern.
    import re
    broken = re.search(
        r"python.*-c\s+\"[^\"]+sys\.stdout\.buffer\.write[^\"]+\"\s*\|\s*grep",
        step5_block,
        re.DOTALL,
    )
    assert not broken, (
        "BUG-010 anti-pattern detected: Python decode piped directly to grep. "
        "grep early-exit closes upstream pipe → BrokenPipeError. Write decoded "
        "bytes to a temp file first, then grep on the file."
    )


def test_step2_6_uses_python_build_not_bash():
    """BUG-011 fix: artifact rebuild must use python build-skill.py (no rsync).

    `bash scripts/build-skill.sh` depends on rsync which is absent on Windows
    MSYS bash. Use `python scripts/build-skill.py build` for cross-platform.
    """
    source = RELEASE_SH.read_text(encoding="utf-8")

    step26_idx = source.find("[2.6/7]")
    assert step26_idx != -1, (
        "Step 2.6 header missing — BUG-011 fix moves rebuild to after version "
        "sync. См. BUGS.md → BUG-011 для контекста."
    )
    step26_block = source[step26_idx:step26_idx + 600]

    assert "build-skill.py build" in step26_block, (
        "Step 2.6 must invoke `python scripts/build-skill.py build` (pure-Python, "
        "no rsync). `bash scripts/build-skill.sh` would fail silently on Windows."
    )

    # Old silent-failure pattern must not return: `>/dev/null 2>&1 || true` swallows
    # build failure and lets release continue with stale artifacts.
    assert ">/dev/null 2>&1 || true" not in step26_block, (
        "Step 2.6 must NOT use `>/dev/null 2>&1 || true` — this hid the BUG-011 "
        "silent failure for several releases. Let exit code propagate so failure "
        "halts the release atomically."
    )


def test_old_step1_5_bash_build_invocation_removed():
    """BUG-011 fix: old `bash scripts/build-skill.sh` *invocation* must be
    removed (not just moved). Placed in step 1.5 (before sync), it produced
    artifacts with the OLD version even when build succeeded — step 7 then
    could not find v${VERSION} files.

    Note: the string may appear in `#` comments explaining the fix — only
    actual invocations (non-comment lines) trigger the regression.
    """
    source = RELEASE_SH.read_text(encoding="utf-8")

    invocation_lines = [
        line for line in source.splitlines()
        if "bash scripts/build-skill.sh" in line
        and not line.lstrip().startswith("#")
    ]
    assert not invocation_lines, (
        "BUG-011 fix expects ALL `bash scripts/build-skill.sh` invocations "
        "removed from release.sh (comments are fine). Use "
        "`python scripts/build-skill.py build` instead — works on Windows "
        f"MSYS bash too. Found invocation lines: {invocation_lines}"
    )
