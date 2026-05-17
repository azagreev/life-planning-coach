"""
System tests for v0.9.0 reference files:
- references/micro_sessions.md
- references/quick_decision.md
- references/reward_audit.md
- life-planning-dashboard.html (Streaks block)
- SKILL.md integration
"""

import pathlib
import re
import subprocess
import tempfile
import os

import pytest

ROOT = pathlib.Path(__file__).parent.parent.parent


class TestMicroSessions:
    FILE = ROOT / "references" / "micro_sessions.md"

    def test_file_exists(self):
        assert self.FILE.exists(), "micro_sessions.md does not exist"

    def test_line_count_under_100(self):
        lines = self.FILE.read_text(encoding="utf-8").splitlines()
        assert len(lines) < 100, f"Expected <100 lines, got {len(lines)}"

    def test_trigger_phrases_present(self):
        text = self.FILE.read_text(encoding="utf-8").lower()
        assert "5 минут" in text, "Missing trigger '5 минут'"
        assert "быстро" in text, "Missing trigger 'быстро'"
        assert "срочно" in text, "Missing trigger 'срочно'"

    def test_protocol_steps_present(self):
        text = self.FILE.read_text(encoding="utf-8")
        steps = [m for m in re.finditer(r"^### \d+\.", text, re.MULTILINE)]
        assert len(steps) >= 3, f"Expected ≥3 protocol steps, found {len(steps)}"

    def test_no_forbidden_words(self):
        text = self.FILE.read_text(encoding="utf-8")
        forbidden = ["надо", "должен", "провал"]
        for word in forbidden:
            assert word not in text.lower(), f"Forbidden word '{word}' found in micro_sessions.md"


class TestQuickDecision:
    FILE = ROOT / "references" / "quick_decision.md"

    def test_file_exists(self):
        assert self.FILE.exists(), "quick_decision.md does not exist"

    def test_line_count_under_100(self):
        lines = self.FILE.read_text(encoding="utf-8").splitlines()
        assert len(lines) < 100, f"Expected <100 lines, got {len(lines)}"

    def test_question_count(self):
        text = self.FILE.read_text(encoding="utf-8")
        questions = [m for m in re.finditer(r"^### \d+\.", text, re.MULTILINE)]
        assert 2 <= len(questions) <= 3, f"Expected 2-3 questions, found {len(questions)}"

    def test_communication_style_link(self):
        text = self.FILE.read_text(encoding="utf-8").lower()
        assert "big five" in text or "quadrant" in text or "стиль" in text, \
            "Missing communication style reference (Big Five / quadrant)"

    def test_no_forbidden_words(self):
        text = self.FILE.read_text(encoding="utf-8")
        forbidden = ["надо", "должен", "провал"]
        for word in forbidden:
            assert word not in text.lower(), f"Forbidden word '{word}' found in quick_decision.md"


class TestRewardAudit:
    FILE = ROOT / "references" / "reward_audit.md"

    def test_file_exists(self):
        assert self.FILE.exists(), "reward_audit.md does not exist"

    def test_line_count_under_120(self):
        lines = self.FILE.read_text(encoding="utf-8").splitlines()
        assert len(lines) < 120, f"Expected <120 lines, got {len(lines)}"

    def test_grayscale_ios_instruction(self):
        text = self.FILE.read_text(encoding="utf-8").lower()
        assert "color filters" in text or "grayscale" in text, "Missing iOS grayscale instruction"
        assert "accessibility" in text, "Missing Accessibility reference for iOS"

    def test_grayscale_android_instruction(self):
        text = self.FILE.read_text(encoding="utf-8").lower()
        assert "color correction" in text, "Missing Android Color Correction instruction"
        assert "monochrome" in text, "Missing Android Monochrome instruction"

    def test_scientific_citations_present(self):
        text = self.FILE.read_text(encoding="utf-8")
        citations = [m.group(1) for m in re.finditer(r"([A-Z][a-z]+(?:\s+et\s+al\.?)?\s*\(\d{4}\))", text)]
        assert len(citations) >= 3, f"Expected ≥3 citations, found {len(citations)}: {citations}"

    def test_no_dopamine_detox_term(self):
        text = self.FILE.read_text(encoding="utf-8").lower()
        assert "dopamine detox" not in text, "Forbidden term 'dopamine detox' found"

    def test_opt_in_framing(self):
        text = self.FILE.read_text(encoding="utf-8").lower()
        assert "reward management" in text or "осознанность" in text, \
            "Missing opt-in framing ('Reward Management' or 'осознанность')"


class TestDashboardStreaks:
    FILE = ROOT / "life-planning-dashboard.html"

    def test_streak_data_array_exists(self):
        text = self.FILE.read_text(encoding="utf-8")
        assert "const STREAK_DATA" in text, "Missing STREAK_DATA array"

    def test_four_categories_present(self):
        text = self.FILE.read_text(encoding="utf-8")
        categories = ["active_habits", "digital", "sugar", "focus"]
        for cat in categories:
            assert cat in text, f"Missing streak category '{cat}'"

    def test_streak_render_function_exists(self):
        text = self.FILE.read_text(encoding="utf-8")
        assert "function renderStreaks()" in text, "Missing renderStreaks() function"

    def test_no_console_errors_on_load(self):
        """Extract user JS (last <script> block) and syntax-check with node."""
        text = self.FILE.read_text(encoding="utf-8")
        # Find the last <script> block (user code, not embedded libraries)
        scripts = list(re.finditer(r"<script>(.*?)</script>", text, re.DOTALL))
        if not scripts:
            pytest.skip("No <script> blocks found")
        user_js = scripts[-1].group(1)
        # Wrap in a function to allow top-level const/let in node check
        js_to_check = "(() => {\n" + user_js + "\n})();"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            f.write(js_to_check)
            tmp = f.name
        try:
            result = subprocess.run(
                ["node", "--check", tmp],
                capture_output=True,
                text=True,
                timeout=10,
            )
            assert result.returncode == 0, f"JS syntax error: {result.stderr}"
        finally:
            os.unlink(tmp)


class TestSkillMdIntegration:
    FILE = ROOT / "SKILL.md"

    def test_reward_audit_reference_in_skill_md(self):
        text = self.FILE.read_text(encoding="utf-8")
        assert "reward_audit.md" in text, "Missing reward_audit.md reference in SKILL.md"

    def test_micro_sessions_reference_in_skill_md(self):
        text = self.FILE.read_text(encoding="utf-8")
        assert "micro_sessions.md" in text, "Missing micro_sessions.md reference in SKILL.md"

    def test_quick_decision_reference_in_skill_md(self):
        text = self.FILE.read_text(encoding="utf-8")
        assert "quick_decision.md" in text, "Missing quick_decision.md reference in SKILL.md"

    def test_skill_md_line_count_under_500(self):
        lines = self.FILE.read_text(encoding="utf-8").splitlines()
        assert len(lines) <= 500, f"SKILL.md exceeds 500 lines: {len(lines)}"

    def test_skill_md_word_count_under_5000(self):
        words = self.FILE.read_text(encoding="utf-8").split()
        assert len(words) <= 5000, f"SKILL.md exceeds 5000 words: {len(words)}"
