"""
System tests for v0.8.0 reference files:
- references/habit_loop.md
- references/action_breakdown_template.md
- references/markdown_tables.md
- references/weak_goal_taxonomy.md
- references/status_icons.md
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
SKILL_MD = PROJECT_ROOT / "SKILL.md"
REFERENCES_DIR = PROJECT_ROOT / "references"

HABIT_LOOP = REFERENCES_DIR / "habit_loop.md"
ACTION_BREAKDOWN = REFERENCES_DIR / "action_breakdown_template.md"
MARKDOWN_TABLES = REFERENCES_DIR / "markdown_tables.md"
WEAK_GOAL_TAXONOMY = REFERENCES_DIR / "weak_goal_taxonomy.md"
STATUS_ICONS = REFERENCES_DIR / "status_icons.md"


class TestHabitLoopFramework:
    def test_file_exists(self):
        assert HABIT_LOOP.is_file(), "references/habit_loop.md does not exist"

    def test_line_count_under_260(self):
        lines = HABIT_LOOP.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 260, (
            f"habit_loop.md has {len(lines)} lines (limit: 260)"
        )

    def test_cue_routine_reward_structure(self):
        content = HABIT_LOOP.read_text(encoding="utf-8")
        assert "Cue" in content, "Missing 'Cue' in habit_loop.md"
        assert "Routine" in content, "Missing 'Routine' in habit_loop.md"
        assert "Reward" in content, "Missing 'Reward' in habit_loop.md"

    def test_tiny_habits_present(self):
        content = HABIT_LOOP.read_text(encoding="utf-8")
        assert "Tiny Habits" in content or "B = MAP" in content, (
            "Missing 'Tiny Habits' or 'B = MAP' in habit_loop.md"
        )

    def test_habit_stacking_present(self):
        content = HABIT_LOOP.read_text(encoding="utf-8")
        assert "Habit Stacking" in content or "После [" in content, (
            "Missing 'Habit Stacking' or 'После [' in habit_loop.md"
        )

    def test_lally_timeline_present(self):
        content = HABIT_LOOP.read_text(encoding="utf-8")
        assert "66" in content, "Missing '66' (days) in habit_loop.md"

    def test_integration_with_existing_features(self):
        content = HABIT_LOOP.read_text(encoding="utf-8")
        assert "WOOP" in content, "Missing 'WOOP' in habit_loop.md"
        assert "Calendar" in content, "Missing 'Calendar' in habit_loop.md"
        assert "Recovery" in content, "Missing 'Recovery' in habit_loop.md"


class TestActionBreakdownTemplate:
    def test_file_exists(self):
        assert ACTION_BREAKDOWN.is_file(), (
            "references/action_breakdown_template.md does not exist"
        )

    def test_line_count_under_150(self):
        lines = ACTION_BREAKDOWN.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 150, (
            f"action_breakdown_template.md has {len(lines)} lines (limit: 150)"
        )

    def test_five_step_protocol(self):
        content = ACTION_BREAKDOWN.read_text(encoding="utf-8")
        for step in ("Step 1", "Step 2", "Step 3", "Step 4", "Step 5"):
            assert step in content, f"Missing '{step}' in action_breakdown_template.md"

    def test_checkpoint_format(self):
        content = ACTION_BREAKDOWN.read_text(encoding="utf-8")
        assert "✓" in content or "Checkpoint" in content, (
            "Missing checkpoint marker in action_breakdown_template.md"
        )

    def test_example_present(self):
        content = ACTION_BREAKDOWN.read_text(encoding="utf-8").lower()
        assert "example" in content or "пример" in content, (
            "Missing example in action_breakdown_template.md"
        )

    def test_when_not_to_use(self):
        content = ACTION_BREAKDOWN.read_text(encoding="utf-8")
        assert "When NOT to use" in content or "Не использовать" in content, (
            "Missing 'When NOT to use' or 'Не использовать' in action_breakdown_template.md"
        )


class TestMarkdownTables:
    def test_file_exists(self):
        assert MARKDOWN_TABLES.is_file(), "references/markdown_tables.md does not exist"

    def test_line_count_under_120(self):
        lines = MARKDOWN_TABLES.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 120, (
            f"markdown_tables.md has {len(lines)} lines (limit: 120)"
        )

    def test_four_templates(self):
        content = MARKDOWN_TABLES.read_text(encoding="utf-8")
        assert "Weekly Plan" in content, "Missing 'Weekly Plan' in markdown_tables.md"
        assert "Wheel of Life" in content, (
            "Missing 'Wheel of Life' in markdown_tables.md"
        )
        assert "Progress Check" in content, (
            "Missing 'Progress Check' in markdown_tables.md"
        )
        assert "Course Correction" in content, (
            "Missing 'Course Correction' in markdown_tables.md"
        )

    def test_stage_appropriate_rules(self):
        content = MARKDOWN_TABLES.read_text(encoding="utf-8")
        assert "Precontemplation" in content, (
            "Missing 'Precontemplation' in markdown_tables.md"
        )
        assert "Contemplation" in content, (
            "Missing 'Contemplation' in markdown_tables.md"
        )

    def test_zero_tables_in_skill_md(self):
        content = MARKDOWN_TABLES.read_text(encoding="utf-8").lower()
        assert "zero tables" in content or "таблиц нет" in content or "skill.md" in content, (
            "Missing 'zero tables' or equivalent reference in markdown_tables.md"
        )


class TestWeakGoalTaxonomy:
    def test_file_exists(self):
        assert WEAK_GOAL_TAXONOMY.is_file(), (
            "references/weak_goal_taxonomy.md does not exist"
        )

    def test_line_count_under_200(self):
        lines = WEAK_GOAL_TAXONOMY.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 200, (
            f"weak_goal_taxonomy.md has {len(lines)} lines (limit: 200)"
        )

    def test_five_patterns(self):
        content = WEAK_GOAL_TAXONOMY.read_text(encoding="utf-8")
        assert "Vague" in content, "Missing 'Vague' in weak_goal_taxonomy.md"
        assert "Output-as-Outcome" in content, (
            "Missing 'Output-as-Outcome' in weak_goal_taxonomy.md"
        )
        assert "Missing Baseline" in content, (
            "Missing 'Missing Baseline' in weak_goal_taxonomy.md"
        )
        assert "Sandbagging" in content, (
            "Missing 'Sandbagging' in weak_goal_taxonomy.md"
        )
        assert "Moonshots" in content or "Moonshot" in content, (
            "Missing 'Moonshots' or 'Moonshot' in weak_goal_taxonomy.md"
        )

    def test_sanity_check_framework(self):
        content = WEAK_GOAL_TAXONOMY.read_text(encoding="utf-8")
        for dimension in ("Coverage", "Balance", "Feasibility", "Measurability", "Alignment"):
            assert dimension in content, (
                f"Missing Sanity-Check dimension '{dimension}' in weak_goal_taxonomy.md"
            )

    def test_integration_with_authentic_goal_filter(self):
        content = WEAK_GOAL_TAXONOMY.read_text(encoding="utf-8")
        assert "authentic_goal_filter" in content, (
            "Missing 'authentic_goal_filter' reference in weak_goal_taxonomy.md"
        )


class TestStatusIcons:
    def test_file_exists(self):
        assert STATUS_ICONS.is_file(), "references/status_icons.md does not exist"

    def test_line_count_under_70(self):
        lines = STATUS_ICONS.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 70, (
            f"status_icons.md has {len(lines)} lines (limit: 70)"
        )

    def test_six_core_icons(self):
        content = STATUS_ICONS.read_text(encoding="utf-8")
        for icon in ("⬜", "🔄", "✅", "❌", "⏸️", "⚠️"):
            assert icon in content, f"Missing icon '{icon}' in status_icons.md"

    def test_accessibility_fallback(self):
        content = STATUS_ICONS.read_text(encoding="utf-8").lower()
        assert "screen reader" in content or "текстовый" in content, (
            "Missing screen reader or текстовый fallback in status_icons.md"
        )

    def test_high_n_safety(self):
        content = STATUS_ICONS.read_text(encoding="utf-8").lower()
        assert "high n" in content or "нейротичность" in content, (
            "Missing High N or нейротичность reference in status_icons.md"
        )


class TestSkillMdIntegration:
    def test_habit_loop_referenced(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        assert "habit_loop.md" in content, (
            "SKILL.md does not reference habit_loop.md"
        )

    def test_action_breakdown_referenced(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        assert "action_breakdown_template.md" in content, (
            "SKILL.md does not reference action_breakdown_template.md"
        )

    def test_markdown_tables_referenced(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        assert "markdown_tables.md" in content, (
            "SKILL.md does not reference markdown_tables.md"
        )

    def test_weak_goal_taxonomy_referenced(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        assert "weak_goal_taxonomy.md" in content, (
            "SKILL.md does not reference weak_goal_taxonomy.md"
        )

    def test_status_icons_referenced(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        assert "status_icons.md" in content, (
            "SKILL.md does not reference status_icons.md"
        )

    def test_line_count_still_under_500(self):
        lines = SKILL_MD.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 500, (
            f"SKILL.md has {len(lines)} lines (limit: 500)"
        )
