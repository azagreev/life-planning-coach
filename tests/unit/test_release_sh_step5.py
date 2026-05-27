"""Regression test для BUG-008 (v1.3.0): release.sh step 5 Windows cp1251 fix.

История:
- v1.2.0 release: step 5 «Проверка на GitHub» крашился на Windows MSYS bash
  с `Python write /dev/stdout: The pipe is being closed.`
- Root cause: inline Python `-c "print(content.decode('utf-8'))"` пытался
  записать UTF-8 README (с emoji 🧭, кириллицей) в stdout, который на Windows
  по default cp1251 — UnicodeEncodeError → pipe break.
- Fix v1.3.0: заменили на `sys.stdout.buffer.write(bytes)` — binary write
  bypass'ит text encoding entirely. Pipe несёт raw UTF-8 bytes, grep их
  обрабатывает без проблем.

Этот тест ловит регрессию: если кто-то откатит fix или добавит другую
`print(content.decode(...))` pattern в release.sh — fail с указанием BUG-008.
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


def test_step5_pipe_chain_intact():
    """Sanity check: step 5 pipe chain still uses gh api + python decode + grep."""
    source = RELEASE_SH.read_text(encoding="utf-8")

    # Step 5 verification block (lines around 130-145 region)
    step5_idx = source.find("[5/7] Проверка на GitHub")
    assert step5_idx != -1, "Step 5 header missing"

    # Next ~500 chars должны содержать pipe chain
    step5_block = source[step5_idx:step5_idx + 800]
    assert "gh api" in step5_block, "gh api call missing в step 5"
    assert "base64.b64decode" in step5_block, "base64 decode missing в step 5"
    assert "grep" in step5_block, "grep call missing в step 5"
