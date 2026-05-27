"""Forbidden-word checks с whitelist для Russian quoted speech.

Зачем helper:
Существующие forbidden-word checks (`forbidden = ["надо", "должен", "обязан"]`)
ловят directive words в quoted speech (`«знаю, что должен»`), что приводит к
переформулировке user quotes / examples в контенте. Это потеря смысла: цитаты
и примеры anti-patterns специально содержат directive слова — их нельзя убирать.

Helper стрипает Russian quoted blocks `«...»` перед check'ом. Цитаты остаются в
контенте (user видит их), но не блокируют тесты.

Использование:
    from tests.helpers.forbidden_words import assert_no_forbidden

    assert_no_forbidden(
        content,
        ["надо", "должен", "обязан"],
        context="references/com_b_diagnostic.md",
    )

История: добавлен в v1.3.0 (PR-D «trivial cleanup bundle»). Migration старых
forbidden-words checks — by-need (не массовый refactor), чтобы избежать regression
в файлах с custom whitelist logic (test_v071_features.py, test_v060_content.py).
"""

from __future__ import annotations

import re
from typing import Iterable

# Russian quoted speech: «...» — содержимое цитат игнорируется при forbidden-words check.
# Поддерживает nested quotes («внешняя "вложенная" часть») через non-greedy match
# до first closing » (не идеально для deeply nested, но достаточно для типового usage).
QUOTED_SPEECH_PATTERN = re.compile(r"«[^»]*»")


def strip_quoted_speech(content: str) -> str:
    """Remove Russian quoted speech blocks `«...»` для forbidden-word check.

    Examples:
        >>> strip_quoted_speech("Скажи «должен сделать» по-другому.")
        'Скажи  по-другому.'
        >>> strip_quoted_speech("Без цитат — просто текст.")
        'Без цитат — просто текст.'
    """
    return QUOTED_SPEECH_PATTERN.sub("", content)


def find_forbidden(
    content: str,
    forbidden: Iterable[str],
    *,
    allow_quoted: bool = True,
    case_sensitive: bool = False,
) -> list[tuple[str, int]]:
    """Return list of (word, line_number) tuples для forbidden words в content.

    Args:
        content: Text to scan.
        forbidden: Iterable of forbidden words / phrases.
        allow_quoted: Если True (default), Russian `«...»` quoted blocks игнорируются.
        case_sensitive: Если False (default), comparison lowercased.

    Returns:
        Empty list если clean. Otherwise list of (word, line_number) tuples
        (line numbers 1-indexed относительно ORIGINAL content, не stripped версии).
    """
    forbidden_list = list(forbidden)
    if not case_sensitive:
        forbidden_list = [w.lower() for w in forbidden_list]

    # Strip quoted blocks line-by-line чтобы preserve line numbers.
    # Multi-line quotes (редко) могут split — это conservative behavior
    # (форбидден слово в multi-line quote всё равно может trigger, но rare).
    violations: list[tuple[str, int]] = []
    for line_no, line in enumerate(content.splitlines(), 1):
        check_line = strip_quoted_speech(line) if allow_quoted else line
        if not case_sensitive:
            check_line = check_line.lower()
        for word in forbidden_list:
            if word in check_line:
                violations.append((word, line_no))
    return violations


def assert_no_forbidden(
    content: str,
    forbidden: Iterable[str],
    *,
    allow_quoted: bool = True,
    case_sensitive: bool = False,
    context: str = "",
) -> None:
    """Assert content has no forbidden words. Raises AssertionError если found.

    Args:
        content: Text to check.
        forbidden: Iterable of forbidden words / phrases.
        allow_quoted: Если True (default), Russian `«...»` blocks игнорируются.
        case_sensitive: Default False.
        context: Optional context string для error message (e.g. file path).
    """
    violations = find_forbidden(
        content,
        forbidden,
        allow_quoted=allow_quoted,
        case_sensitive=case_sensitive,
    )
    if violations:
        # Limit details for readable output
        shown = violations[:10]
        details = "\n".join(f"  - line {ln}: '{w}'" for w, ln in shown)
        if len(violations) > 10:
            details += f"\n  ... and {len(violations) - 10} more"
        suffix = f" in {context}" if context else ""
        raise AssertionError(
            f"Forbidden words found{suffix}:\n{details}"
        )
