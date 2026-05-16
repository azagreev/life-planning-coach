"""Unit tests for calendar_integration/state.py Pydantic models."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import importlib.util

_project_root = Path(__file__).resolve().parents[2]
_state_path = _project_root / "calendar_integration" / "state.py"
_spec = importlib.util.spec_from_file_location("calendar_integration.state_standalone", _state_path)
_state = importlib.util.module_from_spec(_spec)
sys.modules["calendar_integration.state_standalone"] = _state
_spec.loader.exec_module(_state)

ConversationState = _state.ConversationState
LifeWheel = _state.LifeWheel
Values = _state.Values
Goals = _state.Goals
WOOP = _state.WOOP
WeeklyReview = _state.WeeklyReview
OKRTheme = _state.OKRTheme
TwelveWeek = _state.TwelveWeek

from pydantic import ValidationError


class TestConversationStateValidCreation(unittest.TestCase):
    """Tests for valid ConversationState creation."""

    def test_default_creation(self) -> None:
        state = ConversationState()
        self.assertEqual(state.user_id, "")
        self.assertEqual(state.stage, 1)
        self.assertEqual(state.phase, "")
        self.assertEqual(state.completed_phases, [])
        self.assertEqual(state.current_question, 0)
        self.assertIsInstance(state.life_wheel, LifeWheel)
        self.assertIsInstance(state.values, Values)
        self.assertIsInstance(state.goals, Goals)
        self.assertEqual(state.weekly_reviews, [])

    def test_full_creation(self) -> None:
        state = ConversationState(
            user_id="user-123",
            stage=2,
            phase="values",
            completed_phases=["wheel_of_life"],
            current_question=3,
            life_wheel=LifeWheel(
                health=7,
                career=4,
                finances=6,
                relationships=8,
                personal_growth=5,
                fun_recreation=3,
                physical_environment=6,
                family_friends=7,
            ),
            values=Values(
                self_direction=0.85,
                achievement=0.72,
                benevolence=0.91,
            ),
            goals=Goals(
                bhag="Change the world",
                themes=[OKRTheme(objective="Health", key_results=["Run 5k"])],
                twelve_week=TwelveWeek(
                    objectives=["Launch product"],
                    key_results=["100 users"],
                ),
                weekly=["Plan week"],
                daily_woop=[WOOP(wish="Wake up early", outcome="Productive day", obstacle="Alarm", plan="Place phone across room")],
            ),
            weekly_reviews=[
                WeeklyReview(
                    date="2026-05-16",
                    format="gtd_scrum",
                    worked=["Deep work"],
                    didnt_work=["Social media"],
                    changes=["Block apps"],
                    lead_measures={"hours": 10},
                    lag_measures={"tasks": 5},
                    adjustments=["Earlier bedtime"],
                )
            ],
        )
        self.assertEqual(state.user_id, "user-123")
        self.assertEqual(state.stage, 2)
        self.assertEqual(state.life_wheel.health, 7)
        self.assertEqual(state.values.benevolence, 0.91)
        self.assertEqual(state.goals.bhag, "Change the world")
        self.assertEqual(len(state.weekly_reviews), 1)


class TestLifeWheelValidation(unittest.TestCase):
    """Tests for LifeWheel value range validation."""

    def test_life_wheel_below_min_raises(self) -> None:
        with self.assertRaises(ValidationError):
            ConversationState(
                life_wheel=LifeWheel(health=0)
            )

    def test_life_wheel_above_max_raises(self) -> None:
        with self.assertRaises(ValidationError):
            ConversationState(
                life_wheel=LifeWheel(career=11)
            )

    def test_life_wheel_at_boundary_ok(self) -> None:
        state = ConversationState(
            life_wheel=LifeWheel(health=1, career=10)
        )
        self.assertEqual(state.life_wheel.health, 1)
        self.assertEqual(state.life_wheel.career, 10)


class TestStageValidation(unittest.TestCase):
    """Tests for stage value validation."""

    def test_stage_zero_raises(self) -> None:
        with self.assertRaises(ValidationError):
            ConversationState(stage=0)

    def test_stage_four_raises(self) -> None:
        with self.assertRaises(ValidationError):
            ConversationState(stage=4)

    def test_stage_negative_raises(self) -> None:
        with self.assertRaises(ValidationError):
            ConversationState(stage=-1)

    def test_stage_one_ok(self) -> None:
        state = ConversationState(stage=1)
        self.assertEqual(state.stage, 1)

    def test_stage_two_ok(self) -> None:
        state = ConversationState(stage=2)
        self.assertEqual(state.stage, 2)

    def test_stage_three_ok(self) -> None:
        state = ConversationState(stage=3)
        self.assertEqual(state.stage, 3)


class TestJsonRoundtrip(unittest.TestCase):
    """Tests for JSON serialization/deserialization roundtrip."""

    def test_roundtrip_preserves_data(self) -> None:
        original = ConversationState(
            user_id="uuid-abc",
            stage=2,
            phase="ikigai",
            completed_phases=["wheel_of_life", "values"],
            current_question=5,
            life_wheel=LifeWheel(health=8, career=6),
            values=Values(achievement=0.9),
            goals=Goals(bhag="Test BHAG"),
            weekly_reviews=[WeeklyReview(date="2026-01-01")],
        )
        json_str = original.to_json()
        restored = ConversationState.from_json(json_str)

        self.assertEqual(restored.user_id, original.user_id)
        self.assertEqual(restored.stage, original.stage)
        self.assertEqual(restored.phase, original.phase)
        self.assertEqual(restored.completed_phases, original.completed_phases)
        self.assertEqual(restored.current_question, original.current_question)
        self.assertEqual(restored.life_wheel.health, original.life_wheel.health)
        self.assertEqual(restored.life_wheel.career, original.life_wheel.career)
        self.assertEqual(restored.values.achievement, original.values.achievement)
        self.assertEqual(restored.goals.bhag, original.goals.bhag)
        self.assertEqual(len(restored.weekly_reviews), 1)
        self.assertEqual(restored.weekly_reviews[0].date, "2026-01-01")

    def test_to_json_is_valid_json(self) -> None:
        state = ConversationState(user_id="u1", stage=1)
        raw = state.to_json()
        parsed = json.loads(raw)
        self.assertEqual(parsed["user_id"], "u1")
        self.assertEqual(parsed["stage"], 1)


class TestMarkdownExport(unittest.TestCase):
    """Tests for Markdown export."""

    def test_contains_header(self) -> None:
        state = ConversationState()
        md = state.export_markdown()
        self.assertIn("# Life Planning Coach — Session Report", md)

    def test_contains_wheel_of_life_section(self) -> None:
        state = ConversationState(life_wheel=LifeWheel(health=7))
        md = state.export_markdown()
        self.assertIn("## Wheel of Life", md)
        self.assertIn("Health", md)
        self.assertIn("7/10", md)

    def test_contains_values_section(self) -> None:
        state = ConversationState(values=Values(achievement=0.75))
        md = state.export_markdown()
        self.assertIn("## Values (Schwartz PVQ)", md)
        self.assertIn("Achievement", md)
        self.assertIn("0.75", md)

    def test_contains_goals_section(self) -> None:
        state = ConversationState(goals=Goals(bhag="Be awesome"))
        md = state.export_markdown()
        self.assertIn("## Goals", md)
        self.assertIn("### BHAG", md)
        self.assertIn("Be awesome", md)

    def test_contains_weekly_reviews_section(self) -> None:
        state = ConversationState(
            weekly_reviews=[WeeklyReview(date="2026-05-16", format="gtd_scrum")]
        )
        md = state.export_markdown()
        self.assertIn("## Weekly Reviews", md)
        self.assertIn("2026-05-16", md)
        self.assertIn("gtd_scrum", md)

    def test_contains_user_info(self) -> None:
        state = ConversationState(
            user_id="user-42",
            stage=2,
            phase="designing_life",
            completed_phases=["wheel_of_life"],
        )
        md = state.export_markdown()
        self.assertIn("user-42", md)
        self.assertIn("2", md)
        self.assertIn("designing_life", md)
        self.assertIn("wheel_of_life", md)


if __name__ == "__main__":
    unittest.main()
