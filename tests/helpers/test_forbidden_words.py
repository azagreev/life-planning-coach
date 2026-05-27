"""Smoke tests для tests/helpers/forbidden_words.py.

Покрывают:
- Базовое поведение find_forbidden / assert_no_forbidden
- Whitelist Russian quoted speech `«...»`
- Edge cases: nested quotes, multi-line, case sensitivity
"""

from __future__ import annotations

import pytest

from tests.helpers.forbidden_words import (
    assert_no_forbidden,
    find_forbidden,
    strip_quoted_speech,
)


class TestStripQuotedSpeech:
    def test_strips_simple_quote(self):
        assert strip_quoted_speech("До «цитаты» и после.") == "До  и после."

    def test_no_quotes_unchanged(self):
        text = "Просто текст без цитат."
        assert strip_quoted_speech(text) == text

    def test_multiple_quotes(self):
        text = "Первая «one» и вторая «two» цитаты."
        assert strip_quoted_speech(text) == "Первая  и вторая  цитаты."

    def test_nested_quotes_handled_first_closing(self):
        # Non-greedy match: «outer "inner" part» → strips до первой », что для
        # «outer "inner" part» означает strip всю outer цитату (внутри double quotes
        # не closing »). Конкретный edge — но безопасный default.
        text = 'Quote: «outer "inner" part» end.'
        # Non-greedy матчит «...» до первой », inner double quotes игнорируются
        assert "outer" not in strip_quoted_speech(text)
        assert "end." in strip_quoted_speech(text)


class TestFindForbidden:
    def test_clean_content_returns_empty(self):
        assert find_forbidden("Просто чистый текст.", ["надо"]) == []

    def test_forbidden_found_with_line_number(self):
        content = "Первая строка.\nВторая, тут надо что-то.\nТретья."
        violations = find_forbidden(content, ["надо"])
        assert violations == [("надо", 2)]

    def test_quoted_speech_excluded_by_default(self):
        # Forbidden word ВНУТРИ цитаты — игнорируется (default allow_quoted=True)
        content = 'Пример: «знаю что должен сделать», но не делай так.'
        violations = find_forbidden(content, ["должен"])
        assert violations == [], f"Quoted 'должен' must be ignored, got: {violations}"

    def test_unquoted_forbidden_still_caught(self):
        content = "Ты должен это сделать прямо сейчас."
        violations = find_forbidden(content, ["должен"])
        assert violations == [("должен", 1)]

    def test_mixed_quoted_and_unquoted(self):
        content = (
            "Антипаттерн: «ты должен это сделать» — звучит как обвинение.\n"
            "Лучше: ты можешь это сделать.\n"
            "Худо: ты обязан это сделать."
        )
        # «должен» внутри цитаты — игнор; «обязан» вне цитаты — caught
        violations = find_forbidden(content, ["должен", "обязан"])
        assert ("обязан", 3) in violations
        assert ("должен", 1) not in violations, "Quoted 'должен' should be filtered"

    def test_allow_quoted_false_catches_inside_quotes(self):
        content = 'Пример: «ты должен это сделать».'
        violations = find_forbidden(content, ["должен"], allow_quoted=False)
        assert violations == [("должен", 1)]

    def test_case_insensitive_by_default(self):
        content = "Ты ДОЛЖЕН это сделать."
        violations = find_forbidden(content, ["должен"])
        assert violations == [("должен", 1)]

    def test_case_sensitive_when_flag_true(self):
        content = "Ты ДОЛЖЕН это сделать."
        violations = find_forbidden(content, ["должен"], case_sensitive=True)
        assert violations == []


class TestAssertNoForbidden:
    def test_clean_content_no_raise(self):
        assert_no_forbidden("Просто чистый текст.", ["надо"])

    def test_raises_on_forbidden_unquoted(self):
        with pytest.raises(AssertionError, match="line 1:"):
            assert_no_forbidden("Ты должен это сделать.", ["должен"])

    def test_does_not_raise_on_quoted(self):
        # Regression guard для PR-D: quoted speech не должна fail
        content = 'Пример anti-pattern: «ты должен это сделать».'
        assert_no_forbidden(content, ["должен"])

    def test_error_message_includes_context(self):
        with pytest.raises(AssertionError, match="in references/example.md"):
            assert_no_forbidden(
                "должен", ["должен"], context="references/example.md"
            )

    def test_error_message_truncates_after_10(self):
        # Generate 12 forbidden lines — should show first 10 + "and 2 more"
        content = "\n".join(["должен"] * 12)
        with pytest.raises(AssertionError, match="and 2 more"):
            assert_no_forbidden(content, ["должен"])
