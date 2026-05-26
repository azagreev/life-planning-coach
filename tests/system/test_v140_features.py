"""System tests for v0.14.0 — Inclusive Coaching Layer.

Covers: mode_adhd.md, mode_unemployed.md, mode_elder.md,
mode_planning_friction.md, persona hooks in SKILL.master.md, platform integration.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent


@pytest.fixture(scope="module")
def platforms():
    """Load each platform's reachable skill corpus.

    After the v0.17.0 Tier 1 decomposition, lazy-load platforms (claude,
    kimi-cli) keep persona detail in `references/module_*.md` and other
    refs rather than inlining everything in SKILL.md. The acceptance
    semantic is "the user will reach this content when the skill is
    active", so the fixture concatenates SKILL.md with every file the
    platform can lazy-load (phase modules + persona refs + emotion ref).
    Single-file platforms (grok, kimi) already carry inlined modules, so
    their SKILL.md is enough on its own.
    """
    references_dir = PROJECT_ROOT / "references"
    lazy_load_extras = [
        "module_phase1_diagnostic.md",
        "module_phase1_5_goal_filter.md",
        "module_phase2_goal_architecture.md",
        "module_phase3_weekly_review.md",
        "module_phase4_dashboard.md",
        "module_phase5_execution.md",
        "mode_adhd.md",
        "mode_unemployed.md",
        "mode_elder.md",
        "mode_planning_friction.md",
        "emotion_regulation.md",
        "diagnostic_methods.md",
    ]

    def _read(path: Path) -> str:
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def _lazy_corpus(skill_path: Path) -> str:
        body = _read(skill_path)
        if not body:
            return ""
        extras = [_read(references_dir / ref) for ref in lazy_load_extras]
        return body + "\n\n" + "\n\n".join(e for e in extras if e)

    contents = {}
    claude_skill = PROJECT_ROOT / "platforms" / "claude" / "SKILL.md"
    if claude_skill.exists():
        contents["claude"] = _lazy_corpus(claude_skill)

    kimi_cli_skill = PROJECT_ROOT / "platforms" / "kimi-cli" / "SKILL.md"
    if kimi_cli_skill.exists():
        contents["kimi_cli"] = _lazy_corpus(kimi_cli_skill)

    for single_file in ("grok", "kimi"):
        path = PROJECT_ROOT / "platforms" / single_file / "SKILL.md"
        if path.exists():
            contents[single_file] = _read(path)

    return contents


class TestAdhdMode:
    """Validate references/mode_adhd.md"""

    def test_file_exists_and_size(self):
        path = PROJECT_ROOT / "references" / "mode_adhd.md"
        assert path.exists()
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 120

    def test_opt_in_framing(self):
        content = (PROJECT_ROOT / "references" / "mode_adhd.md").read_text(encoding="utf-8").lower()
        assert "opt-in" in content or "opt in" in content
        assert "никогда не предполагайте" in content or "не предполагайте" in content

    def test_car_method_present(self):
        content = (PROJECT_ROOT / "references" / "mode_adhd.md").read_text(encoding="utf-8").lower()
        assert "c.a.r" in content or "capture" in content
        assert "action" in content
        assert "review" in content

    def test_five_minute_rule(self):
        content = (PROJECT_ROOT / "references" / "mode_adhd.md").read_text(encoding="utf-8").lower()
        assert "5 минут" in content or "5-minute" in content

    def test_visual_timer(self):
        content = (PROJECT_ROOT / "references" / "mode_adhd.md").read_text(encoding="utf-8").lower()
        assert "визуальный" in content or "visual" in content
        assert "таймер" in content or "timer" in content

    def test_time_buffer_2x(self):
        content = (PROJECT_ROOT / "references" / "mode_adhd.md").read_text(encoding="utf-8").lower()
        assert "вдвое" in content or "×2" in content or "2×" in content or "time buffer" in content

    def test_body_doubling(self):
        content = (PROJECT_ROOT / "references" / "mode_adhd.md").read_text(encoding="utf-8").lower()
        assert "body double" in content or "body doubling" in content or "присутствие" in content

    def test_no_medical_advice(self):
        lines = (PROJECT_ROOT / "references" / "mode_adhd.md").read_text(encoding="utf-8").lower().splitlines()
        forbidden = ["лекарств", "медикамент", "диагноз", "психиатр"]
        for i, line in enumerate(lines):
            if "❌" in line or "не " in line or "anti-pattern" in line:
                continue
            for word in forbidden:
                assert word not in line, f"Found forbidden word '{word}' on line {i+1}: {line}"


class TestTimeStructureUnemployed:
    """Validate references/mode_unemployed.md"""

    def test_file_exists_and_size(self):
        path = PROJECT_ROOT / "references" / "mode_unemployed.md"
        assert path.exists()
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 120

    def test_daily_template_present(self):
        content = (PROJECT_ROOT / "references" / "mode_unemployed.md").read_text(encoding="utf-8").lower()
        assert "08:00" in content or "8:00" in content
        assert "17:00" in content or "18:00" in content

    def test_sharp_hours(self):
        content = (PROJECT_ROOT / "references" / "mode_unemployed.md").read_text(encoding="utf-8").lower()
        assert "9:00" in content or "09:00" in content
        assert "13:00" in content

    def test_ten_principles(self):
        content = (PROJECT_ROOT / "references" / "mode_unemployed.md").read_text(encoding="utf-8").lower()
        assert "принцип" in content or "principle" in content
        # At least 10 numbered principles (table format: | 1 | ... |)
        lines = content.splitlines()
        numbered = [
            line
            for line in lines
            if any(f"| {n} |" in line or line.strip().startswith(f"{n}.") for n in range(1, 11))
        ]
        assert len(numbered) >= 10

    def test_no_shame_guilt(self):
        content = (PROJECT_ROOT / "references" / "mode_unemployed.md").read_text(encoding="utf-8").lower()
        assert "вина" not in content or "стыд" not in content

    def test_social_anchors(self):
        content = (PROJECT_ROOT / "references" / "mode_unemployed.md").read_text(encoding="utf-8").lower()
        assert "социальн" in content or "social" in content
        assert "якор" in content or "anchor" in content

    def test_small_wins(self):
        content = (PROJECT_ROOT / "references" / "mode_unemployed.md").read_text(encoding="utf-8").lower()
        assert "small win" in content or "маленьк" in content or "побед" in content

    def test_anti_marathon_pattern(self):
        content = (PROJECT_ROOT / "references" / "mode_unemployed.md").read_text(encoding="utf-8").lower()
        assert "марафон" in content or "8 час" in content or "8-hour" in content


class TestElderHomebound:
    """Validate references/mode_elder.md"""

    def test_file_exists_and_size(self):
        path = PROJECT_ROOT / "references" / "mode_elder.md"
        assert path.exists()
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 120

    def test_solo_aging_normalization(self):
        content = (PROJECT_ROOT / "references" / "mode_elder.md").read_text(encoding="utf-8").lower()
        assert "solo aging" in content or "нет детей" in content
        assert "не провал" in content or "не failure" in content

    def test_micro_anchors(self):
        content = (PROJECT_ROOT / "references" / "mode_elder.md").read_text(encoding="utf-8").lower()
        assert "якор" in content or "anchor" in content
        assert "ритуал" in content or "ritual" in content

    def test_mattering(self):
        content = (PROJECT_ROOT / "references" / "mode_elder.md").read_text(encoding="utf-8").lower()
        assert "mattering" in content or "значим" in content
        assert "микро-вклад" in content or "micro-contribution" in content

    def test_legacy_through_memory(self):
        content = (PROJECT_ROOT / "references" / "mode_elder.md").read_text(encoding="utf-8").lower()
        assert "история" in content or "memory" in content
        assert "наследие" in content or "legacy" in content

    def test_frankl_dignity(self):
        content = (PROJECT_ROOT / "references" / "mode_elder.md").read_text(encoding="utf-8").lower()
        assert "достоинств" in content or "dignity" in content
        assert "франкл" in content or "frankl" in content

    def test_no_productivity_imposition(self):
        lines = (PROJECT_ROOT / "references" / "mode_elder.md").read_text(encoding="utf-8").lower().splitlines()
        forbidden = ["продуктивност", "цели на 5 лет", "надо планировать"]
        for i, line in enumerate(lines):
            if "❌" in line or "не делать" in line or "anti-pattern" in line or "микро-якоря" in line:
                continue
            for word in forbidden:
                assert word not in line, f"Found forbidden word '{word}' on line {i+1}: {line}"

    def test_no_medical_advice(self):
        content = (PROJECT_ROOT / "references" / "mode_elder.md").read_text(encoding="utf-8").lower()
        forbidden = ["лекарств", "диагноз", "врачебн"]
        for word in forbidden:
            assert word not in content, f"Found forbidden word: {word}"


class TestPlanningFrictionAudit:
    """Validate references/mode_planning_friction.md"""

    def test_file_exists_and_size(self):
        path = PROJECT_ROOT / "references" / "mode_planning_friction.md"
        assert path.exists()
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 120

    def test_friction_detection_questions(self):
        content = (PROJECT_ROOT / "references" / "mode_planning_friction.md").read_text(encoding="utf-8").lower()
        assert "трение" in content or "friction" in content
        assert "вопрос" in content or "question" in content

    def test_three_templates(self):
        content = (PROJECT_ROOT / "references" / "mode_planning_friction.md").read_text(encoding="utf-8").lower()
        assert "deep work" in content or "глубокая работа" in content
        assert "meeting" in content or "встреч" in content
        assert "recovery" in content or "восстановлен" in content

    def test_smart_defaults(self):
        content = (PROJECT_ROOT / "references" / "mode_planning_friction.md").read_text(encoding="utf-8").lower()
        assert "25 мин" in content or "25min" in content
        assert "45 мин" in content or "45min" in content
        assert "15 мин" in content or "15min" in content

    def test_ten_percent_rule(self):
        content = (PROJECT_ROOT / "references" / "mode_planning_friction.md").read_text(encoding="utf-8").lower()
        assert "10%" in content or "10 процент" in content

    def test_no_shaming(self):
        lines = (PROJECT_ROOT / "references" / "mode_planning_friction.md").read_text(encoding="utf-8").lower().splitlines()
        for i, line in enumerate(lines):
            if "❌" in line or "anti-pattern" in line:
                continue
            assert "просто планируй" not in line, f"Found shaming phrase on line {i+1}: {line}"

    def test_science_references(self):
        content = (PROJECT_ROOT / "references" / "mode_planning_friction.md").read_text(encoding="utf-8")
        assert "sweller" in content.lower() or "gollwitzer" in content.lower() or "fogg" in content.lower()


class TestPersonaHooks:
    """Verify persona detection and reference loading in SKILL.master.md"""

    def test_adhd_opt_in_trigger_present(self, platforms):
        for name, content in platforms.items():
            assert "микро-шаг" in content.lower() or "adhd" in content.lower()
            assert "хотите" in content.lower()

    def test_adhd_reference_loaded(self, platforms):
        for name, content in platforms.items():
            assert "mode_adhd.md" in content or "references/adhd" in content

    def test_adhd_time_buffer_in_calendar(self, platforms):
        for name, content in platforms.items():
            assert "time buffer" in content.lower() or "вдвое" in content.lower() or "×2" in content

    def test_unemployed_trigger_phrases_present(self, platforms):
        for name, content in platforms.items():
            assert "без работы" in content.lower() or "уволен" in content.lower() or "декрет" in content.lower() or "поиск" in content.lower()

    def test_unemployed_reference_loaded(self, platforms):
        for name, content in platforms.items():
            assert "mode_unemployed.md" in content or "references/time_structure" in content

    def test_unemployed_sharp_hours_in_calendar(self, platforms):
        for name, content in platforms.items():
            assert "sharp hours" in content.lower() or "9:00" in content or "13:00" in content

    def test_elder_homebound_trigger_phrases_present(self, platforms):
        for name, content in platforms.items():
            assert "пенсионер" in content.lower() or "старый" in content.lower() or "не могу" in content.lower()

    def test_elder_homebound_reference_loaded(self, platforms):
        for name, content in platforms.items():
            assert "mode_elder.md" in content or "references/elder_homebound" in content

    def test_elder_adapted_wheel_present(self, platforms):
        for name, content in platforms.items():
            if "elder" in content.lower():
                assert "micro-check-in" in content.lower() or "микро-чек" in content.lower() or "микро-" in content.lower()

    def test_friction_audit_hook_present(self, platforms):
        for name, content in platforms.items():
            assert "planning_friction" in content.lower() or "friction audit" in content.lower()


class TestPlatformIntegrationV14:
    """Verify platform files build correctly and contain v0.14.0 content"""

    def test_master_version_is_at_least_014(self):
        """v0.14 introduced inclusive coaching layer — version must be ≥ 0.14.0."""
        content = (PROJECT_ROOT / "SKILL.master.md").read_text(encoding="utf-8")
        match = re.search(r"^version:\s*([\d.]+)", content, re.MULTILINE)
        assert match, "SKILL.master.md must declare version in frontmatter"
        parts = [int(p) for p in match.group(1).split(".")[:3]]
        while len(parts) < 3:
            parts.append(0)
        assert tuple(parts) >= (0, 14, 0), (
            f"SKILL.master.md version {match.group(1)} < 0.14.0 (v140 features expected)"
        )

    def test_all_four_references_in_master(self):
        content = (PROJECT_ROOT / "SKILL.master.md").read_text(encoding="utf-8")
        assert "mode_adhd.md" in content
        assert "mode_unemployed.md" in content
        assert "mode_elder.md" in content
        assert "mode_planning_friction.md" in content

    def test_claude_platform_exists(self):
        path = PROJECT_ROOT / "platforms" / "claude" / "SKILL.md"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "mode_adhd.md" in content

    def test_kimi_platform_exists(self):
        path = PROJECT_ROOT / "platforms" / "kimi" / "SKILL.md"
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "mode_adhd.md" in content
