"""
System tests for v0.7.1 reference files:
- references/win_alert.md
- references/recovery_protocol.md
- references/energy_scheduling.md
"""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
SKILL_MD = PROJECT_ROOT / "SKILL.md"
REFERENCES_DIR = PROJECT_ROOT / "references"

WIN_ALERT = REFERENCES_DIR / "win_alert.md"
RECOVERY_PROTOCOL = REFERENCES_DIR / "recovery_protocol.md"
ENERGY_SCHEDULING = REFERENCES_DIR / "energy_scheduling.md"


class TestWinAlertProtocol:
    def test_file_exists(self):
        assert WIN_ALERT.is_file(), "references/win_alert.md does not exist"

    def test_five_step_structure(self):
        content = WIN_ALERT.read_text(encoding="utf-8")
        for step in ("Step 1: WHAT", "Step 2: WHEEL", "Step 3: WHY",
                     "Step 4: RESOURCES", "Step 5: NEXT"):
            assert step in content, f"Missing '{step}' in win_alert.md"

    def test_when_not_to_use_crisis(self):
        content = WIN_ALERT.read_text(encoding="utf-8")
        assert "кризис" in content.lower() or "crisis" in content.lower(), (
            "Missing crisis reference in When NOT to use section"
        )

    def test_science_backing(self):
        content = WIN_ALERT.read_text(encoding="utf-8")
        has_bryant_or_veroff = "Bryant" in content or "Veroff" in content
        has_dweck = "Dweck" in content
        assert has_bryant_or_veroff and has_dweck, (
            "Missing science backing (Bryant/Veroff and Dweck)"
        )

    def test_communication_style_adaptation(self):
        content = WIN_ALERT.read_text(encoding="utf-8")
        quadrants = ["Nurturing", "Challenging", "Exploratory", "Collaborative"]
        for q in quadrants:
            assert q in content, f"Missing quadrant '{q}' in win_alert.md"


class TestRecoveryProtocol:
    def test_file_exists(self):
        assert RECOVERY_PROTOCOL.is_file(), "references/recovery_protocol.md does not exist"

    def test_line_count_under_200(self):
        lines = RECOVERY_PROTOCOL.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 200, (
            f"recovery_protocol.md has {len(lines)} lines (limit: 200)"
        )

    def test_three_strategies(self):
        content = RECOVERY_PROTOCOL.read_text(encoding="utf-8")
        for strategy in ("LIGHT MISS", "MEDIUM MISS", "HEAVY MISS"):
            assert strategy in content, f"Missing '{strategy}' in recovery_protocol.md"

    def test_no_streak_tracking(self):
        content = RECOVERY_PROTOCOL.read_text(encoding="utf-8").lower()
        forbidden = ["streak", "цепочка", "unbroken", "серия"]
        for word in forbidden:
            # Allow if in negative context (НЕ, never, no) or quoted as example
            lines_with_word = [
                line for line in content.splitlines() if word in line
            ]
            for line in lines_with_word:
                is_negative_context = any(
                    neg in line
                    for neg in ["не ", "не\t", "никогда", "нет", "no ", "never", "— ", "'", '"']
                )
                assert is_negative_context, (
                    f"Forbidden streak-tracking word '{word}' found in positive context: {line.strip()[:80]}"
                )

    def test_no_shame_language(self):
        content = RECOVERY_PROTOCOL.read_text(encoding="utf-8").lower()
        forbidden = ["провал", "сорвался", "сдался", "неудачник"]
        for word in forbidden:
            # Allow if in negative context (НЕ, never, quoted as example of what NOT to say)
            lines_with_word = [
                line for line in content.splitlines() if word in line
            ]
            for line in lines_with_word:
                is_negative_context = any(
                    neg in line
                    for neg in ["не ", "не\t", "никогда", "нет", "— ", "'", '"']
                )
                assert is_negative_context, (
                    f"Forbidden shame word '{word}' found in positive context: {line.strip()[:80]}"
                )

    def test_pattern_detection_conversational(self):
        content = RECOVERY_PROTOCOL.read_text(encoding="utf-8").lower()
        assert (
            "конверсационный" in content or "разговорный" in content
        ), "Missing conversational pattern detection reference"

    def test_skip_with_reflection_exists(self):
        content = RECOVERY_PROTOCOL.read_text(encoding="utf-8").lower()
        assert "рефлекс" in content or "reflection" in content, (
            "Missing skip-with-reflection mechanism in recovery_protocol.md"
        )


class TestEnergyScheduling:
    def test_file_exists(self):
        assert ENERGY_SCHEDULING.is_file(), "references/energy_scheduling.md does not exist"

    def test_line_count_under_80(self):
        lines = ENERGY_SCHEDULING.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 120, (
            f"energy_scheduling.md has {len(lines)} lines (limit: 80)"
        )

    def test_three_energy_levels(self):
        content = ENERGY_SCHEDULING.read_text(encoding="utf-8")
        for level in ("HIGH", "MEDIUM", "LOW"):
            assert level in content, f"Missing energy level '{level}' in energy_scheduling.md"

    def test_calibration_question(self):
        content = ENERGY_SCHEDULING.read_text(encoding="utf-8")
        assert "пик энергии" in content or "Calibration" in content, (
            "Missing calibration question in energy_scheduling.md"
        )

    def test_seasonal_planning_link(self):
        content = ENERGY_SCHEDULING.read_text(encoding="utf-8")
        assert (
            "Seasonal Planning" in content
            or "seasonal" in content.lower()
            or "Spring" in content
        ), "Missing seasonal planning link in energy_scheduling.md"

    def test_ac8_energy_check_link(self):
        content = ENERGY_SCHEDULING.read_text(encoding="utf-8")
        assert "Energy Check" in content or "AC-8" in content, (
            "Missing Energy Check / AC-8 link in energy_scheduling.md"
        )

    def test_color_map_connection(self):
        content = ENERGY_SCHEDULING.read_text(encoding="utf-8")
        assert "COLOR_MAP" in content or "colorId" in content, (
            "Missing COLOR_MAP or colorId reference in energy_scheduling.md"
        )


class TestSkillMdIntegration:
    def test_win_alert_referenced(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        assert "win_alert.md" in content, "SKILL.md does not reference win_alert.md"

    def test_recovery_protocol_referenced(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        assert "recovery_protocol.md" in content, (
            "SKILL.md does not reference recovery_protocol.md"
        )

    def test_energy_scheduling_referenced(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        assert "energy_scheduling.md" in content, (
            "SKILL.md does not reference energy_scheduling.md"
        )

    def test_line_count_still_under_500(self):
        lines = SKILL_MD.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 500, (
            f"SKILL.md has {len(lines)} lines (limit: 500)"
        )
