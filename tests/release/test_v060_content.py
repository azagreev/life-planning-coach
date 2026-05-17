"""Content validation tests for v0.6.0 features.

These tests verify the ACTUAL CONTENT of new features, not just structure.
Run after building the ZIP artifact.
"""

import re
import zipfile
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
ZIP_PATH = PROJECT_ROOT / "life-planning-coach.zip"
REPO_SKILL_MD = PROJECT_ROOT / "SKILL.md"

# Files to check (repo versions, more reliable than ZIP during dev)
AUTHENTIC_GOAL_FILTER = PROJECT_ROOT / "references" / "authentic_goal_filter.md"
COMMUNICATION_STYLE = PROJECT_ROOT / "references" / "communication_style.md"
DIAGNOSTIC_METHODS = PROJECT_ROOT / "references" / "diagnostic_methods.md"


class TestAuthenticGoalFilterContent:
    """Verify authentic_goal_filter.md has all required content."""

    def test_file_exists(self):
        assert AUTHENTIC_GOAL_FILTER.exists(), "authentic_goal_filter.md must exist"

    def test_red_flag_detector_has_6_plus_1(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        # Count red flag markers
        flags = re.findall(r"### [🔴⚪] Red Flag \d", text)
        assert len(flags) >= 7, f"Expected 7 red flags (6+1), found {len(flags)}"

    def test_whose_voice_questions(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        assert "Чей голос" in text or "Чей это голос" in text, (
            "Missing 'Whose voice?' externalization questions"
        )

    def test_energy_check_is_optional(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        assert "опционально" in text or "опциональный" in text, (
            "Energy Check must be marked as optional"
        )
        assert "лёгкость" in text or "тяжесть" in text, (
            "Energy Check must reference somatic markers (lightness/heaviness)"
        )

    def test_deep_why_has_3_levels_not_5(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        # Should have "3 уровня"
        assert "3 уровня" in text, "Deep Why must specify 3 levels"
        # Should NOT have "5 уровней" as the protocol
        assert "5 уровней" not in text or "НЕ 5" in text, (
            "Deep Why must NOT use 5 levels (user fatigue)"
        )

    def test_societal_pressure_test_has_4_questions(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        questions = [
            "никто никогда не узнал",
            "успешного человека",
            "стыдно/страшно",
            "свободу",  # "свободу и рост или статус" — no slash in text
        ]
        found = [q for q in questions if q in text]
        assert len(found) == 4, f"Expected 4 societal pressure questions, found {len(found)}: {found}"

    def test_true_goal_score_is_radar_not_formula(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        assert "Радар" in text or "radar" in text.lower(), (
            "True Goal Score must be a radar chart"
        )
        assert "не формула" in text or "not formula" in text.lower(), (
            "True Goal Score must explicitly state it's NOT a formula"
        )
        # Should NOT have weighted formula pattern
        assert "values_alignment *" not in text, (
            "Must not have weighted formula with multiplication"
        )

    def test_radar_has_5_axes(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        axes = ["Ценности", "Энергия", "Влияние", "Реалистичность", "Аутентичность"]
        found = [a for a in axes if a in text]
        assert len(found) == 5, f"Expected 5 radar axes, found {len(found)}: {found}"

    def test_goal_portfolio_framing(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        assert "On Pause" in text or "на паузе" in text, (
            "Goal Portfolio must use 'On Pause' framing"
        )
        # Must NOT use negative framing
        assert "отсеянные" not in text, (
            "Must NOT use 'отсеянные' (discarded) framing"
        )
        assert "discarded" not in text.lower(), (
            "Must NOT use 'discarded' framing"
        )

    def test_pattern_analysis_present(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        assert "Pattern Analysis" in text or "Паттерн-анализ" in text, (
            "Pattern Analysis must be present"
        )

    def test_hard_goals_real_definition(self):
        text = AUTHENTIC_GOAL_FILTER.read_text(encoding="utf-8")
        # Should have Mark Murphy's definition (at least Heartfelt, since others
        # may be in reference files but not in authentic_goal_filter.md)
        murphy_terms = ["Heartfelt", "Animated", "Required", "Difficult"]
        found = [t for t in murphy_terms if t in text]
        assert len(found) >= 1, f"Expected at least 1 Mark Murphy HARD term, found {found}"
        # Should NOT have fake definition
        assert "High Arousal" not in text, (
            "Must NOT use fake 'High Arousal Reactive Desire' definition"
        )
        assert "Reactive Desire" not in text, (
            "Must NOT use fake 'Reactive Desire' definition"
        )


class TestCommunicationStyleContent:
    """Verify communication_style.md has all required content."""

    def test_file_exists(self):
        assert COMMUNICATION_STYLE.exists(), "communication_style.md must exist"

    def test_four_quadrants_present(self):
        text = COMMUNICATION_STYLE.read_text(encoding="utf-8")
        quadrants = [
            "Nurturing Parent",
            "Challenging Consultant",
            "Exploratory Guide",
            "Collaborative Partner",
        ]
        found = [q for q in quadrants if q in text]
        assert len(found) == 4, f"Expected 4 quadrants, found {len(found)}: {found}"

    def test_ttm_overlay_5_stages(self):
        text = COMMUNICATION_STYLE.read_text(encoding="utf-8")
        stages = ["Precontemplation", "Contemplation", "Preparation", "Action", "Maintenance"]
        found = [s for s in stages if s in text]
        assert len(found) == 5, f"Expected 5 TTM stages, found {len(found)}: {found}"

    def test_oars_framework(self):
        text = COMMUNICATION_STYLE.read_text(encoding="utf-8")
        # OARS components are written with markdown bold: **O**pen-ended, **A**ffirmations, etc.
        oars_patterns = [
            "**O**pen-ended",
            "**A**ffirmations",
            "**R**eflective listening",
            "**S**ummaries",
        ]
        found = [o for o in oars_patterns if o in text]
        assert len(found) >= 3, f"Expected OARS components, found {len(found)}: {found}"

    def test_mi_additional_techniques(self):
        text = COMMUNICATION_STYLE.read_text(encoding="utf-8")
        assert "Roll with Resistance" in text, "Missing 'Roll with Resistance'"
        assert "Develop Discrepancy" in text, "Missing 'Develop Discrepancy'"

    def test_attachment_styles(self):
        text = COMMUNICATION_STYLE.read_text(encoding="utf-8")
        styles = ["Secure", "Anxious", "Avoidant", "Disorganized"]
        found = [s for s in styles if s in text]
        assert len(found) == 4, f"Expected 4 attachment styles, found {len(found)}: {found}"

    def test_dynamic_adaptation_triggers(self):
        text = COMMUNICATION_STYLE.read_text(encoding="utf-8")
        triggers = [
            "Trigger 1",
            "Trigger 2",
            "Trigger 3",
            "Trigger 4",
            "Trigger 5",
        ]
        found = [t for t in triggers if t in text]
        assert len(found) == 5, f"Expected 5 triggers, found {len(found)}: {found}"

    def test_calibration_protocol(self):
        text = COMMUNICATION_STYLE.read_text(encoding="utf-8")
        assert "Calibration" in text, "Missing calibration protocol"
        assert "мягкая поддержка" in text or "прямая правда" in text, (
            "Missing calibration questions"
        )


class TestWheelOfLifeUpdate:
    """Verify Wheel of Life has 11 domains."""

    def test_11_domains(self):
        text = DIAGNOSTIC_METHODS.read_text(encoding="utf-8")
        # Look for the categories section
        assert "Categories (11 domains)" in text or "11 доменов" in text, (
            "Wheel of Life must specify 11 domains"
        )

    def test_family_separate_from_social(self):
        text = DIAGNOSTIC_METHODS.read_text(encoding="utf-8")
        assert "Family" in text, "Missing 'Family' domain"
        assert "Social" in text or "Дружба" in text, "Missing 'Social' domain"
        # Family/Friends should NOT be combined
        assert "Family / Friends" not in text, (
            "Family and Friends must be separate domains"
        )

    def test_contribution_added(self):
        text = DIAGNOSTIC_METHODS.read_text(encoding="utf-8")
        assert "Contribution" in text or "Вклад" in text, (
            "Missing 'Contribution' domain"
        )

    def test_meaning_mandatory(self):
        text = DIAGNOSTIC_METHODS.read_text(encoding="utf-8")
        # Meaning should be present
        assert "Meaning" in text or "Смысл" in text or "meaning" in text.lower(), (
            "Missing 'Meaning' domain"
        )
        # Should NOT be marked as optional
        lines = text.splitlines()
        meaning_lines = [l for l in lines if ("Meaning" in l or "Смысл" in l) and "опционально" in l.lower()]
        assert len(meaning_lines) == 0, (
            "Meaning must NOT be marked as optional"
        )


class TestSkillMdIntegration:
    """Verify SKILL.md integrates v0.6.0 features correctly."""

    def test_stage_1_5_referenced(self):
        text = REPO_SKILL_MD.read_text(encoding="utf-8")
        assert "Stage 1.5" in text, "SKILL.md must reference Stage 1.5"
        assert "Authentic Goal Filter" in text, "SKILL.md must reference Authentic Goal Filter"

    def test_communication_style_referenced(self):
        text = REPO_SKILL_MD.read_text(encoding="utf-8")
        assert "Adaptive Style" in text or "communication_style" in text, (
            "SKILL.md must reference Communication Style"
        )

    def test_version_matches_git_tag(self):
        text = REPO_SKILL_MD.read_text(encoding="utf-8")
        match = re.search(r"^version:\s*(.+)$", text, re.MULTILINE)
        assert match, "SKILL.md must have version in frontmatter"
        version = match.group(1).strip().strip('"').strip("'")
        import subprocess
        git_tag = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip().lstrip("v")
        assert version == git_tag, f"Expected version {git_tag}, got: {version}"

    def test_goal_ownership_language_rules(self):
        text = REPO_SKILL_MD.read_text(encoding="utf-8")
        assert "Goal Ownership" in text, "Missing Goal Ownership Language Rules"
        assert "решаешь" in text, "Missing 'решаешь' autonomy marker"

    def test_token_budget_under_5000(self):
        """Verify repo SKILL.md is under token limit (not just ZIP version)."""
        text = REPO_SKILL_MD.read_text(encoding="utf-8")
        word_count = len(text.split())
        assert word_count < 5000, (
            f"SKILL.md word count {word_count} exceeds 5000 limit"
        )

    def test_no_forbidden_words_in_diagnostic_questions(self):
        """Verify no pressure-inducing words in actual questions/commands.
        Allow them in Language Rules section (where they are explicitly forbidden)."""
        text = REPO_SKILL_MD.read_text(encoding="utf-8")
        forbidden = ["провал", "отстой"]
        lines = text.splitlines()
        found = []
        for i, line in enumerate(lines, 1):
            # Skip Language Rules and Gotchas sections where words are listed as forbidden
            if "Language Rules" in line or "ЗАПРЕЩЕНО" in line or "не используй" in line.lower() or "Gotchas" in line:
                continue
            for word in forbidden:
                if word in line.lower():
                    found.append(f"Line {i}: {line.strip()}")
        assert not found, f"Forbidden words used outside Language Rules: {found[:3]}"

    def test_new_references_included(self):
        """Verify SKILL.md references new v0.6.0 files."""
        text = REPO_SKILL_MD.read_text(encoding="utf-8")
        assert "authentic_goal_filter.md" in text, (
            "SKILL.md must reference authentic_goal_filter.md"
        )
        assert "communication_style.md" in text, (
            "SKILL.md must reference communication_style.md"
        )
