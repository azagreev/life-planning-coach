"""
System tests for calendar event tone compliance.
Ensures calendar integration texts follow coaching guidelines:
- No forbidden words: "надо", "должен", "провал", "обязан"
- No implicit pressure through "нужно"/"важно" in commanding contexts
- Positive framing for event descriptions
"""

import pytest
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALENDAR_MD = PROJECT_ROOT / "references" / "calendar_integration.md"


class TestCalendarTone:
    @pytest.fixture(scope="class")
    def calendar_text(self):
        return CALENDAR_MD.read_text(encoding="utf-8")

    def test_no_explicit_forbidden_words(self, calendar_text):
        forbidden = ["надо", "должен", "провал", "обязан"]
        lines = calendar_text.splitlines()
        for i, line in enumerate(lines, 1):
            for word in forbidden:
                if word in line.lower():
                    pytest.fail(f"Forbidden word '{word}' in calendar_integration.md line {i}: {line}")

    def test_no_scary_statistics_without_context(self, calendar_text):
        """Negative statistics must be framed with context, not used as pressure."""
        scare_patterns = [
            r"\d+% .{0,30}забыва",  # "60% ... forget"
            r"\d+% .{0,30}провал",   # "X% ... fail"
        ]
        for pattern in scare_patterns:
            matches = re.finditer(pattern, calendar_text.lower())
            for m in matches:
                line_num = calendar_text[:m.start()].count("\n") + 1
                pytest.fail(f"Scary statistic without supportive context at line {line_num}: {m.group()}")

    def test_event_descriptions_are_positive(self, calendar_text):
        """Event descriptions should use positive framing."""
        # Extract description="..." values
        desc_pattern = re.compile(r'description="(.*?)(?<!\\)"', re.DOTALL)
        descriptions = desc_pattern.findall(calendar_text)

        assert len(descriptions) >= 2, "Expected at least 2 event descriptions in calendar_integration.md"

        # Combine all descriptions for word-level checks
        all_desc_text = " ".join(descriptions).lower()

        # Verify celebration language in weekly review
        weekly_desc = descriptions[0].lower()
        assert "🎉" in descriptions[0], "Weekly Review should start with celebration"
        assert any(word in weekly_desc for word in ["радость", "гордость", "получилось"]), (
            "Weekly Review should celebrate wins"
        )
        assert "хочется" in weekly_desc, "Weekly Review should use gentle 'хочется' instead of pressure"

        # Verify soft language in WOOP
        woop_desc = descriptions[1].lower()
        assert "✨" in descriptions[1], "WOOP should use inviting emoji"
        assert "хочется" in woop_desc, "WOOP should frame wish as 'хочется'"
        assert "первый шаг" in woop_desc, "WOOP plan should focus on first step, not rigid formula"

        # No commanding pressure words in any description
        pressure_words = ["надо", "должен", "обязан", "следует"]
        for word in pressure_words:
            assert word not in all_desc_text, f"Description contains pressure word '{word}'"
