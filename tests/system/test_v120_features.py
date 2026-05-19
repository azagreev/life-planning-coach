"""Tests for v0.12.0 Behavioral Science Layer features."""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
REFERENCES = PROJECT_ROOT / "references"
PLATFORMS = PROJECT_ROOT / "platforms"


class TestHabitStackBuilder:
    """Validate references/habit_stack_builder.md content and structure."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "habit_stack_builder.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 150, f"File too long: {len(lines)} lines (max 150)"

    def test_habit_anchoring_formula(self, content):
        assert "После [" in content or "после [" in content.lower()
        assert "я буду [" in content or "я буду [" in content.lower()

    def test_progressive_escalation_four_levels(self, content):
        # Week 1-2, Week 3-4, Week 5-8, Week 9+
        assert "1-2" in content or "1–2" in content
        assert "3-4" in content or "3–4" in content
        assert "5-8" in content or "5–8" in content
        assert "9+" in content or "9+" in content

    def test_two_day_rule(self, content):
        assert "не более 1 дня" in content.lower() or "two-day" in content.lower() or "1 дня подряд" in content.lower()

    def test_no_shame_language(self, content):
        shame_words = ["провал", "сорвался", "сдался", "неудачник"]
        for word in shame_words:
            assert word not in content.lower(), f"Shame word '{word}' found"

    def test_no_streak_tracking(self, content):
        streak_words = ["streak", "цепочка", "unbroken", "серия"]
        for word in streak_words:
            assert word not in content.lower(), f"Streak word '{word}' found"

    def test_no_forbidden_words(self, content):
        forbidden = ["надо", "должен", "обязан"]
        for word in forbidden:
            assert word not in content.lower(), f"Forbidden word '{word}' found"

    def test_scientific_backing(self, content):
        assert "fogg" in content.lower() or "b=map" in content.lower()
        assert "clear" in content.lower() or "habit stacking" in content.lower()
        assert "lally" in content.lower() or "66" in content

    def test_onboarding_question(self, content):
        assert "кофе" in content.lower() or "завтракаете" in content.lower() or "душ" in content.lower()

    def test_integration_with_habit_loop(self, content):
        assert "habit_loop.md" in content


class TestShutdownRitual:
    """Validate references/shutdown_ritual.md content and structure."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "shutdown_ritual.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 120, f"File too long: {len(lines)} lines (max 120)"

    def test_five_steps_present(self, content):
        lower = content.lower()
        assert "capture" in lower or "собрать" in lower
        assert "review" in lower or "обзор" in lower or "итог" in lower
        assert "plan" in lower or "план" in lower
        assert "celebrate" in lower or "праздн" in lower or "побед" in lower
        assert "close" in lower or "закрыт" in lower or "закрыть" in lower

    def test_explicit_work_day_closed(self, content):
        assert "рабочий день закрыт" in content.lower() or "work day is closed" in content.lower()

    def test_three_small_wins(self, content):
        assert "3" in content and ("маленьких побед" in content.lower() or "small wins" in content.lower() or "побед" in content.lower())

    def test_top_three_unfinished(self, content):
        assert "3" in content and ("незаверш" in content.lower() or "unfinished" in content.lower() or "top 3" in content.lower())

    def test_zeigarnik_reference(self, content):
        assert "zeigarnik" in content.lower() or "зейгарник" in content.lower() or "masicampo" in content.lower()

    def test_not_mandatory(self, content):
        assert "permission" in content.lower() or "опционально" in content.lower() or "предлож" in content.lower()

    def test_distinct_from_recovery(self, content):
        assert "recovery_protocol.md" in content.lower() or "recovery" in content.lower()
        # Should explain difference between daily shutdown and recovery after skip
        assert "не заменяет" in content.lower() or "≠" in content or "не тот же" in content.lower() or "отличается" in content.lower()

    def test_scientific_backing(self, content):
        assert "sonnentag" in content.lower() or "detachment" in content.lower()
        assert "newport" in content.lower() or "shutdown" in content.lower()

    def test_no_forbidden_words(self, content):
        forbidden = ["надо", "должен", "обязан"]
        for word in forbidden:
            assert word not in content.lower(), f"Forbidden word '{word}' found"


class TestFreshStartEngine:
    """Validate references/fresh_start_engine.md content and structure."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "fresh_start_engine.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 120, f"File too long: {len(lines)} lines (max 120)"

    def test_four_temporal_landmarks(self, content):
        lower = content.lower()
        assert "понедельник" in lower or "monday" in lower or "fresh week" in lower
        assert "1-е" in lower or "1-го" in lower or "month" in lower or "месяц" in lower
        assert "new year" in lower or "новый год" in lower or "год" in lower
        assert "день рождения" in lower or "birthday" in lower or "персональн" in lower or "personal" in lower

    def test_dark_side_protection(self, content):
        lower = content.lower()
        assert "не ждите" in lower or "не откладывайте" in lower or "начните сейчас" in lower or "с малого" in lower

    def test_permission_based(self, content):
        lower = content.lower()
        assert "опционально" in lower or "permission" in lower or "предлож" in lower or "не навязывать" in lower

    def test_not_mandatory(self, content):
        lower = content.lower()
        assert ("не mandatory" in lower or "не обязательно" in lower or "опционально" in lower
                or "не навязывать" in lower or "предлагать" in lower or "уважать отказ" in lower)

    def test_scientific_backing(self, content):
        lower = content.lower()
        assert "dai" in lower or "milkman" in lower
        assert "oscarsson" in lower or "19%" in content

    def test_integration_with_weekly_review(self, content):
        assert "weekly_review.md" in content.lower() or "goal_architecture.md" in content.lower()

    def test_no_forbidden_words(self, content):
        forbidden = ["надо", "должен", "обязан"]
        for word in forbidden:
            assert word not in content.lower(), f"Forbidden word '{word}' found"


class TestPlatformIntegration:
    """Validate all 4 platform SKILL.md files reference the new v0.12 modules."""

    @pytest.fixture(scope="class")
    def platforms(self):
        return {
            "claude": PLATFORMS / "claude" / "SKILL.md",
            "grok": PLATFORMS / "grok" / "SKILL.md",
            "kimi": PLATFORMS / "kimi" / "SKILL.md",
            "kimi-cli": PLATFORMS / "kimi-cli" / "SKILL.md",
        }

    def test_all_platforms_reference_habit_stack_builder(self, platforms):
        for name, path in platforms.items():
            content = path.read_text(encoding="utf-8")
            assert "habit_stack_builder.md" in content, f"{name} missing habit_stack_builder reference"

    def test_all_platforms_reference_shutdown_ritual(self, platforms):
        for name, path in platforms.items():
            content = path.read_text(encoding="utf-8")
            assert "shutdown_ritual.md" in content, f"{name} missing shutdown_ritual reference"

    def test_all_platforms_reference_fresh_start_engine(self, platforms):
        for name, path in platforms.items():
            content = path.read_text(encoding="utf-8")
            assert "fresh_start_engine.md" in content, f"{name} missing fresh_start_engine reference"

    def test_claude_size_still_under_limit(self, platforms):
        content = platforms["claude"].read_text(encoding="utf-8")
        lines = content.splitlines()
        words = len(content.split())
        assert len(lines) <= 500, f"Claude SKILL.md too long: {len(lines)} lines"
        assert words <= 5000, f"Claude SKILL.md too wordy: {words} words"

    def test_kimi_cli_size_still_under_limit(self, platforms):
        content = platforms["kimi-cli"].read_text(encoding="utf-8")
        lines = content.splitlines()
        assert len(lines) <= 500, f"Kimi CLI SKILL.md too long: {len(lines)} lines"

    def test_no_cross_contamination(self, platforms):
        # Claude should not mention Kimi/Grok specific terms
        claude = platforms["claude"].read_text(encoding="utf-8").lower()
        assert "render_file" not in claude
        assert "kimi_ref" not in claude
        assert "memory_space" not in claude

        # Kimi should not mention Claude/Grok specific terms
        kimi = platforms["kimi"].read_text(encoding="utf-8").lower()
        assert "mcp" not in kimi
        assert "claude" not in kimi

        # Grok should not mention Claude/Kimi specific terms
        grok = platforms["grok"].read_text(encoding="utf-8").lower()
        assert "mcp" not in grok
        assert "claude" not in grok
        assert "kimi_ref" not in grok


class TestHabitLoopUpdated:
    """Validate habit_loop.md cross-references habit_stack_builder.md."""

    def test_habit_loop_references_stack_builder(self):
        path = REFERENCES / "habit_loop.md"
        content = path.read_text(encoding="utf-8").lower()
        assert (
            "habit_stack_builder" in content or "habit stack builder" in content
        ), "habit_loop.md missing cross-reference to habit_stack_builder.md"
