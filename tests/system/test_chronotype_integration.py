"""Tests for Chronotype-Native Planning integration (v0.11.0 research-driven)."""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
REFERENCES = PROJECT_ROOT / "references"


class TestChronotypeNativePlanning:
    """Validate references/chronotype_native_planning.md content and structure."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "chronotype_native_planning.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 120, f"File too long: {len(lines)} lines (max 120)"

    def test_three_profiles_present(self, content):
        profiles = ["Жаворонок", "Промежуточный", "Сова"]
        for profile in profiles:
            assert profile in content, f"Profile '{profile}' missing"

    def test_bedtime_todo_list_for_owls(self, content):
        assert "bedtime to-do list" in content.lower() or "список дел перед сном" in content.lower()

    def test_no_miracle_morning_for_everyone(self, content):
        # "Магия утра" may appear only in negative context (warning against it)
        lines = content.splitlines()
        for phrase in ["Магия утра", "Miracle Morning", "miracle morning"]:
            for line in lines:
                if phrase in line:
                    assert "не" in line.lower() or "не навязывать" in line.lower() or "warning" in line.lower() or "биолог" in line.lower(), \
                        f"Line contains '{phrase}' without negative context: {line}"

    def test_peak_trough_rebound_mentioned(self, content):
        assert "Peak-Trough-Rebound" in content or "Peak" in content and "Trough" in content and "Rebound" in content

    def test_scientific_backing(self, content):
        assert "Pink (2018)" in content or "Pink" in content
        assert "Scullin" in content or "bedtime" in content.lower()
        assert "Synchrony" in content or "Schmidt" in content

    def test_safety_anti_patterns(self, content):
        assert "Не навязывать" in content or "не навязывать" in content.lower()
        assert "биология" in content.lower() or "биолог" in content.lower()


class TestEnergySchedulingUpdated:
    """Validate energy_scheduling.md contains chronotype-adapted peak hours."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "energy_scheduling.md"
        assert path.exists()
        return path.read_text(encoding="utf-8")

    def test_chronotype_reference(self, content):
        assert "chronotype_native_planning.md" in content

    def test_three_profiles_in_table(self, content):
        assert "Жаворонок" in content
        assert "Промежуточный" in content
        assert "Сова" in content

    def test_peak_hours_per_profile(self, content):
        # At least one specific time range per profile
        assert "8:00–12:00" in content or "8:00-12:00" in content  # Lark peak
        assert "17:00–21:00" in content or "17:00-21:00" in content  # Owl peak

    def test_size_still_reasonable(self, content):
        lines = content.splitlines()
        assert len(lines) <= 120, f"energy_scheduling.md grew too much: {len(lines)} lines"


class TestDiagnosticMethodsUpdated:
    """Validate diagnostic_methods.md contains chronotype questions."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "diagnostic_methods.md"
        assert path.exists()
        return path.read_text(encoding="utf-8")

    def test_chronotype_section_exists(self, content):
        assert "Chronotype Quick Calibration" in content or "хронотип" in content.lower()

    def test_calibration_questions(self, content):
        assert "прилив энергии" in content.lower()
        assert "сосредоточиться" in content.lower() or "концентрироваться" in content.lower()

    def test_no_labels(self, content):
        # Check only chronotype section (after "Chronotype Quick Calibration")
        idx = content.find("Chronotype Quick Calibration")
        if idx == -1:
            idx = content.find("хронотип")
        section = content[idx:] if idx != -1 else content
        assert "ленивый" not in section.lower() or "не используйте" in section.lower()
        assert "дисциплинированный" not in section.lower() or "не используйте" in section.lower()

    def test_scientific_refs_in_diagnostic(self, content):
        assert "Pink" in content or "Peak-Trough-Rebound" in content
        assert "Scullin" in content or "Synchrony" in content


class TestNoRegressions:
    """Ensure existing tests still pass and no forbidden words introduced."""

    def test_no_forbidden_words_in_chronotype_file(self):
        path = REFERENCES / "chronotype_native_planning.md"
        content = path.read_text(encoding="utf-8").lower()
        forbidden = ["надо", "должен", "провал", "обязан"]
        for word in forbidden:
            assert word not in content, f"Forbidden word '{word}' in chronotype file"
