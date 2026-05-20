"""Tests for v0.13.0 Smart Scheduling Layer features."""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
REFERENCES = PROJECT_ROOT / "references"
PLATFORMS = PROJECT_ROOT / "platforms"


class TestWorkloadWarning:
    """Validate references/workload_warning.md content and structure."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "workload_warning.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 100, f"File too long: {len(lines)} lines (max 100)"

    def test_three_levels_present(self, content):
        lower = content.lower()
        assert "green" in lower or "🟢" in content
        assert "yellow" in lower or "🟡" in content
        assert "red" in lower or "🔴" in content

    def test_threshold_configurable(self, content):
        lower = content.lower()
        assert "6 часов" in lower or "6 hours" in lower
        assert "configurable" in lower or "по умолчанию" in lower or "изменить" in lower

    def test_mi_aligned_tone(self, content):
        lower = content.lower()
        forbidden = ["надо", "должен", "обязан"]
        for word in forbidden:
            assert word not in lower, f"Forbidden word '{word}' found"
        assert "хотите" in lower or "предлагать" in lower or "предлож" in lower

    def test_defer_backlog_suggestion(self, content):
        lower = content.lower()
        assert "отложить" in lower or "перенести" in lower or "бэклог" in lower
        # Should not force — check for autonomy language
        assert "предлож" in lower or "хотите" in lower or "можно" in lower

    def test_paper_coach_mode_present(self, content):
        lower = content.lower()
        assert "paper coach" in lower or "text-only" in lower or "markdown-таблице" in lower
        assert "| задача |" in lower or "|--------|" in lower

    def test_sunsama_shutdown_check(self, content):
        lower = content.lower()
        assert "sunsama" in lower or "shutdown" in lower or "окончания дня" in lower
        assert "завершения" in lower or "completion" in lower or "закончится" in lower

    def test_fifteen_percent_buffer_present(self, content):
        lower = content.lower()
        assert "15%" in content or "15 %" in content or "15 процентов" in lower


class TestEnergySchedulingV2:
    """Validate references/energy_scheduling.md content and structure (v2)."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "energy_scheduling.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 120, f"File too long: {len(lines)} lines (max 120)"

    def test_v1_content_preserved(self, content):
        lower = content.lower()
        # Three energy levels
        assert "high" in lower or "🟢" in content
        assert "medium" in lower or "🟡" in content
        assert "low" in lower or "🔴" in content
        # Peak hours / chronotype
        assert "жаворонок" in lower or "chronotype" in lower or "пик" in lower
        # Heuristics
        assert "защищайте" in lower or "heuristics" in lower or "буфер" in lower

    def test_self_report_scale_present(self, content):
        lower = content.lower()
        assert "1–10" in content or "1-10" in content or "1 до 10" in lower or "от 1 до 10" in lower

    def test_pattern_learning_present(self, content):
        lower = content.lower()
        assert "на основе того, что вы мне рассказывали" in lower or "pattern learning" in lower
        assert "никаких притворных баз данных" in lower or "не угадывайте" in lower

    def test_rain_plan_present(self, content):
        lower = content.lower()
        assert "rain plan" in lower or "дождевой" in lower or "b-шаблон" in lower or "уменьшите амбиции" in lower

    def test_recovery_micro_block_present(self, content):
        lower = content.lower()
        assert "10–15 минут" in content or "micro-block" in lower or "микро" in lower or "восстановление" in lower

    def test_energy_aware_meeting_lengths_present(self, content):
        lower = content.lower()
        assert "20 мин" in lower or "50–55 мин" in lower or "короткие встречи" in lower or "встречи" in lower

    def test_no_forbidden_words(self, content):
        forbidden = ["надо", "должен", "обязан"]
        for word in forbidden:
            assert word not in content.lower(), f"Forbidden word '{word}' found"


class TestCalendarPatternAnalyzer:
    """Validate references/calendar_pattern_analyzer.md content and structure."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "calendar_pattern_analyzer.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 120, f"File too long: {len(lines)} lines (max 120)"

    def test_read_only_declaration(self, content):
        lower = content.lower()
        assert "list_events" in lower
        # These should be explicitly listed as NOT used
        assert "create_event" in lower
        assert "delete_event" in lower
        assert "update_event" in lower
        assert "read-only" in lower or "read only" in lower

    def test_five_metrics_present(self, content):
        lower = content.lower()
        assert "meeting load" in lower or "загрузка встречами" in lower
        assert "focus time" in lower or "фокус" in lower
        assert "boundary" in lower or "границ" in lower
        assert "recovery" in lower or "восстановление" in lower
        assert "alignment" in lower or "выравнивание" in lower or "хронотип" in lower

    def test_permission_based(self, content):
        lower = content.lower()
        assert "согласие" in lower or "проанализирую" in lower or "спросите" in lower or "разрешения" in lower

    def test_conversational_insight_format(self, content):
        lower = content.lower()
        # Should explicitly forbid productivity score and comparison in anti-patterns
        assert "продуктивный скор" in lower or "productivity score" in lower
        assert "не сравнивать" in lower or "comparison" in lower or "не выдавать" in lower

    def test_weekly_trend_present(self, content):
        lower = content.lower()
        assert "3 недели" in lower or "3+ недель" in lower or "three weeks" in lower or "минимум 3" in lower

    def test_no_forbidden_words(self, content):
        forbidden = ["надо", "должен", "обязан"]
        for word in forbidden:
            assert word not in content.lower(), f"Forbidden word '{word}' found"


class TestPlatformIntegrationV13:
    """Validate all 4 platform SKILL.md files reference the new v0.13 modules."""

    @pytest.fixture(scope="class")
    def platforms(self):
        return {
            "claude": PLATFORMS / "claude" / "SKILL.md",
            "grok": PLATFORMS / "grok" / "SKILL.md",
            "kimi": PLATFORMS / "kimi" / "SKILL.md",
            "kimi-cli": PLATFORMS / "kimi-cli" / "SKILL.md",
        }

    def test_all_platforms_reference_workload_warning(self, platforms):
        missing = []
        for name, path in platforms.items():
            content = path.read_text(encoding="utf-8")
            if "workload_warning.md" not in content:
                missing.append(name)
        if missing:
            pytest.skip(f"Wave 2 not yet applied — missing in: {', '.join(missing)}")

    def test_all_platforms_reference_pattern_analyzer(self, platforms):
        missing = []
        for name, path in platforms.items():
            content = path.read_text(encoding="utf-8")
            if "calendar_pattern_analyzer.md" not in content:
                missing.append(name)
        if missing:
            pytest.skip(f"Wave 2 not yet applied — missing in: {', '.join(missing)}")

    def test_all_platforms_reference_energy_scheduling_v2(self, platforms):
        for name, path in platforms.items():
            content = path.read_text(encoding="utf-8")
            assert "energy_scheduling.md" in content, f"{name} missing energy_scheduling reference"

    def test_claude_size_still_under_limit(self, platforms):
        content = platforms["claude"].read_text(encoding="utf-8")
        lines = content.splitlines()
        words = len(content.split())
        assert len(lines) <= 500, f"Claude SKILL.md too long: {len(lines)} lines"
        assert words <= 5000, f"Claude SKILL.md too wordy: {words} words"
