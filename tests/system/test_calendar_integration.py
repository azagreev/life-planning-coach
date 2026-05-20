"""
System tests for Calendar Integration hardening.

The project keeps calendar behavior in markdown references, not in a Python
runtime module. These tests validate the documented contracts directly:
- calendar constants are structurally valid
- event patterns contain the required fields
- free-slot behavior is covered by an executable reference implementation
- user-facing failure modes remain present and supportive
"""

import json
import re
from datetime import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALENDAR_CONSTANTS = PROJECT_ROOT / "references" / "calendar_constants.md"
CALENDAR_INTEGRATION = PROJECT_ROOT / "references" / "calendar_integration.md"


def _strip_json_comments(text: str) -> str:
    """Remove markdown JSON example comments while preserving string content."""
    cleaned_lines = []
    for line in text.splitlines():
        in_string = False
        escaped = False
        output = []
        index = 0
        while index < len(line):
            char = line[index]
            next_char = line[index + 1] if index + 1 < len(line) else ""
            if char == "\\" and not escaped:
                escaped = True
                output.append(char)
                index += 1
                continue
            if char == '"' and not escaped:
                in_string = not in_string
            if not in_string and char == "/" and next_char == "/":
                break
            output.append(char)
            escaped = False
            index += 1
        cleaned_lines.append("".join(output))
    return "\n".join(cleaned_lines)


def _extract_json_block(markdown: str, heading: str) -> dict:
    pattern = re.compile(
        rf"#{{2,3}}\s+{re.escape(heading)}\b.*?```json\n(.*?)\n```",
        re.DOTALL,
    )
    match = pattern.search(markdown)
    assert match, f"Missing json block for {heading}"
    return json.loads(_strip_json_comments(match.group(1)))


def _extract_call_block(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"###\s+{re.escape(heading)}\s*\n```\n(.*?)\n```",
        re.DOTALL,
    )
    match = pattern.search(markdown)
    assert match, f"Missing call block for {heading}"
    return match.group(1)


def _merge_busy_intervals(intervals: list[tuple[time, time]]) -> list[tuple[time, time]]:
    """Reference implementation for the documented Free Slot Algorithm."""
    if not intervals:
        return []

    sorted_intervals = sorted(intervals)
    merged = [sorted_intervals[0]]
    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def _minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def _time_from_minutes(value: int) -> time:
    return time(hour=value // 60, minute=value % 60)


def _find_free_slots(
    busy: list[tuple[time, time]],
    work_window: tuple[time, time],
    duration_minutes: int,
    limit: int = 3,
) -> list[tuple[time, time]]:
    """Find top-N gaps inside work hours using the markdown algorithm."""
    merged = _merge_busy_intervals(busy)
    window_start, window_end = map(_minutes, work_window)
    cursor = window_start
    slots = []

    for start_time, end_time in merged:
        start = max(_minutes(start_time), window_start)
        end = min(_minutes(end_time), window_end)
        if end <= window_start or start >= window_end:
            continue
        if start - cursor >= duration_minutes:
            slots.append((_time_from_minutes(cursor), _time_from_minutes(start)))
        cursor = max(cursor, end)

    if window_end - cursor >= duration_minutes:
        slots.append((_time_from_minutes(cursor), _time_from_minutes(window_end)))

    return slots[:limit]


class TestCalendarConstants:
    @pytest.fixture(scope="class")
    def constant_docs(self):
        return [
            CALENDAR_CONSTANTS.read_text(encoding="utf-8"),
            CALENDAR_INTEGRATION.read_text(encoding="utf-8"),
        ]

    @pytest.mark.parametrize("heading", ["COLOR_MAP", "REMINDER_PRESETS", "RRULE_PRESETS"])
    def test_calendar_json_like_blocks_parse(self, constant_docs, heading):
        for text in constant_docs:
            parsed = _extract_json_block(text, heading)
            assert isinstance(parsed, dict)
            assert parsed, f"{heading} must not be empty"

    def test_color_ids_are_google_calendar_values(self, constant_docs):
        for text in constant_docs:
            color_map = _extract_json_block(text, "COLOR_MAP")
            for activity, color_id in color_map.items():
                assert color_id.isdigit(), f"{activity} colorId must be numeric"
                assert 1 <= int(color_id) <= 11, f"{activity} colorId outside 1..11"

    def test_reminder_presets_have_valid_overrides(self, constant_docs):
        for text in constant_docs:
            presets = _extract_json_block(text, "REMINDER_PRESETS")
            for name, reminders in presets.items():
                assert isinstance(reminders, list), f"{name} reminders must be a list"
                assert reminders, f"{name} reminders must not be empty"
                for reminder in reminders:
                    assert reminder["method"] in {"popup", "email"}
                    assert isinstance(reminder["minutes"], int)
                    assert reminder["minutes"] >= 0

    def test_rrule_presets_have_frequency(self, constant_docs):
        for text in constant_docs:
            presets = _extract_json_block(text, "RRULE_PRESETS")
            for name, rrules in presets.items():
                assert isinstance(rrules, list), f"{name} RRULE preset must be a list"
                assert rrules, f"{name} RRULE preset must not be empty"
                for rrule in rrules:
                    assert rrule.startswith("RRULE:"), f"{name} must start with RRULE:"
                    assert "FREQ=" in rrule, f"{name} must define FREQ"


class TestCalendarEventPatterns:
    @pytest.fixture(scope="class")
    def integration_text(self):
        return CALENDAR_INTEGRATION.read_text(encoding="utf-8")

    @pytest.mark.parametrize(
        ("heading", "required_fields"),
        [
            (
                "Weekly Review",
                ["summary", "description", "start", "end", "colorId", "reminders", "recurrence"],
            ),
            (
                "WOOP Session",
                ["summary", "description", "start", "end", "colorId", "reminders", "recurrence"],
            ),
        ],
    )
    def test_event_patterns_include_required_fields(self, integration_text, heading, required_fields):
        block = _extract_call_block(integration_text, heading)
        for field in required_fields:
            assert re.search(rf"\b{field}\s*=", block), f"{heading} missing {field}"

    def test_failure_modes_cover_core_calendar_errors(self):
        text = CALENDAR_CONSTANTS.read_text(encoding="utf-8")
        required_modes = [
            "Calendar not connected",
            "User declines OAuth",
            "Rate limit (429)",
            "Permission denied (403)",
            "Recurrence not supported",
        ]
        for mode in required_modes:
            assert mode in text, f"Missing failure mode: {mode}"

        supportive_phrases = [
            "Продолжим без синхронизации?",
            "будем работать без календаря",
            "продолжим без календаря?",
            "Создам отдельные события",
        ]
        assert all(phrase in text for phrase in supportive_phrases)


class TestFreeSlotAlgorithm:
    def test_merges_overlapping_busy_intervals(self):
        busy = [
            (time(10, 0), time(11, 0)),
            (time(10, 30), time(12, 0)),
            (time(13, 0), time(14, 0)),
        ]
        assert _merge_busy_intervals(busy) == [
            (time(10, 0), time(12, 0)),
            (time(13, 0), time(14, 0)),
        ]

    def test_merges_back_to_back_events(self):
        busy = [
            (time(9, 0), time(10, 0)),
            (time(10, 0), time(11, 0)),
        ]
        assert _merge_busy_intervals(busy) == [(time(9, 0), time(11, 0))]

    def test_empty_day_returns_work_window(self):
        assert _find_free_slots([], (time(9, 0), time(18, 0)), 30) == [
            (time(9, 0), time(18, 0))
        ]

    def test_fully_busy_day_returns_no_slots(self):
        busy = [(time(9, 0), time(18, 0))]
        assert _find_free_slots(busy, (time(9, 0), time(18, 0)), 30) == []

    def test_ignores_gaps_shorter_than_requested_duration(self):
        busy = [
            (time(9, 0), time(9, 45)),
            (time(10, 0), time(18, 0)),
        ]
        assert _find_free_slots(busy, (time(9, 0), time(18, 0)), 30) == []

    def test_returns_top_three_slots_sorted_by_time(self):
        busy = [
            (time(10, 0), time(11, 0)),
            (time(12, 0), time(13, 0)),
            (time(14, 0), time(15, 0)),
            (time(16, 0), time(17, 0)),
        ]
        assert _find_free_slots(busy, (time(9, 0), time(18, 0)), 30) == [
            (time(9, 0), time(10, 0)),
            (time(11, 0), time(12, 0)),
            (time(13, 0), time(14, 0)),
        ]
