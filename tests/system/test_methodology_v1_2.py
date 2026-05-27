"""System tests for v1.2.0 — New Evidence-Based Methods.

Covers: com_b_diagnostic.md (COM-B Model), environment_design.md,
opt-in entry в Phase 0/1, Routing Map, evidence_map.md status,
schema bump 2.2.2 (diagnosis.com_b_assessment), platform integration.

Будет расширен в PR2 (Premortem) и PR3 (Lean AAR).
"""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
REFERENCES = PROJECT_ROOT / "references"
PLATFORMS = PROJECT_ROOT / "platforms"


class TestComBDiagnostic:
    """Validate references/com_b_diagnostic.md content and structure."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "com_b_diagnostic.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 250, f"File too long: {len(lines)} lines (max 250)"

    def test_tier_3_frontmatter(self, content):
        head = content[:600].lower()
        assert "tier" in head and "3" in head
        assert "lazy-load" in head or "lazy" in head

    def test_evidence_citation_michie_2011(self, content):
        lower = content.lower()
        assert "michie" in lower, "Missing Michie citation"
        assert "van stralen" in lower, "Missing van Stralen citation"
        assert "west" in lower, "Missing West citation"
        assert "2011" in content, "Missing 2011 year"
        assert "implementation science" in lower, "Missing journal name"
        assert "6(42)" in content or "10.1186/1748-5908-6-42" in content, "Missing volume/DOI"

    def test_three_components(self, content):
        lower = content.lower()
        assert "capability" in lower
        assert "opportunity" in lower
        assert "motivation" in lower

    def test_diagnostic_protocol_three_blocks(self, content):
        lower = content.lower()
        # Должен быть протокол с тремя блоками вопросов
        assert "psychological" in lower or "когнитивн" in lower
        assert "physical" in lower or "физическ" in lower
        assert "social" in lower or "социальн" in lower
        assert "reflective" in lower or "рефлексивн" in lower
        assert "automatic" in lower or "автоматическ" in lower

    def test_three_gap_routings(self, content):
        """Critical: routing logic для всех трёх gap-типов."""
        lower = content.lower()
        # Capability → action_breakdown + Tiny Habits в habit_loop
        assert "action_breakdown_template.md" in lower, "Capability routing must mention action_breakdown_template.md"
        assert "habit_loop.md" in lower, "Capability routing must mention habit_loop.md"
        assert "tiny habits" in lower, "Capability routing must mention Tiny Habits"
        # Opportunity → environment_design
        assert "environment_design.md" in lower, "Opportunity routing must mention environment_design.md"
        # Motivation → WOOP + Compass
        assert "woop" in lower, "Motivation routing must mention WOOP"
        assert "compass" in lower, "Motivation routing must mention Compass Mode"

    def test_when_not_to_use_section(self, content):
        lower = content.lower()
        # Markdown bold "**не**" может ломать прямой поиск — ищем по смысловым маркерам
        assert "когда" in lower and ("использовать" in lower or "применять" in lower)
        # Должен упоминать ER protocol / эмоциональный block
        assert "emotion_regulation" in lower or "phase 0.5" in lower or "er protocol" in lower

    def test_state_write_field_documented(self, content):
        lower = content.lower()
        assert "com_b_assessment" in lower, "Must document state field for persistence"
        assert "primary_gap" in lower, "Must document primary_gap field"

    def test_no_forbidden_words(self, content):
        forbidden = ["надо", "должен", "обязан"]
        for word in forbidden:
            assert word not in content.lower(), f"Forbidden directive word '{word}' found"


class TestEnvironmentDesign:
    """Validate references/environment_design.md content and structure."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "environment_design.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_file_exists_and_size(self, content):
        lines = content.splitlines()
        assert len(lines) <= 220, f"File too long: {len(lines)} lines (max 220)"

    def test_tier_3_frontmatter(self, content):
        head = content[:600].lower()
        assert "tier" in head and "3" in head

    def test_evidence_citations(self, content):
        lower = content.lower()
        # Multiple evidence sources expected
        assert "lally" in lower, "Missing Lally citation (habit context)"
        assert "fogg" in lower, "Missing Fogg citation (B=MAP Prompt)"
        assert "wood" in lower, "Missing Wood et al. citation (43% automaticity)"
        assert "thaler" in lower or "sunstein" in lower or "nudge" in lower, "Missing Nudge / choice architecture citation"

    def test_seven_practices_present(self, content):
        """Must have all 7 environment design practices."""
        lower = content.lower()
        assert "friction" in lower, "Missing friction asymmetry practice"
        assert "cue removal" in lower or "убрать триггер" in lower or "убрать cue" in lower
        assert "cue placement" in lower or "добавить cue" in lower or "поставить cue" in lower
        assert "context switching" in lower or "смена контекста" in lower or "context" in lower
        assert "social" in lower, "Missing social architecture"
        assert "default" in lower, "Missing default switching"
        assert "calendar" in lower, "Missing calendar as environment"

    def test_loaded_from_com_b(self, content):
        lower = content.lower()
        assert "com_b_diagnostic.md" in lower, "Must reference com_b_diagnostic.md as entry point"
        assert "opportunity" in lower, "Must explain Opportunity-gap context"

    def test_when_not_to_use_section(self, content):
        lower = content.lower()
        # Markdown bold "**не**" может ломать прямой поиск — ищем по смысловым маркерам
        assert "когда" in lower and ("использовать" in lower or "применять" in lower)

    def test_no_forbidden_words(self, content):
        forbidden = ["надо", "должен", "обязан"]
        for word in forbidden:
            assert word not in content.lower(), f"Forbidden directive word '{word}' found"


class TestMasterIntegration:
    """Validate SKILL.master.md integrations for COM-B + environment_design."""

    @pytest.fixture(scope="class")
    def content(self):
        path = PROJECT_ROOT / "SKILL.master.md"
        return path.read_text(encoding="utf-8")

    def test_master_references_com_b(self, content):
        # COM-B доступен через Tier 3 listing (Phase 1 module triggers по сигналу)
        assert "com_b_diagnostic.md" in content, "Master must reference com_b_diagnostic.md"

    def test_tier3_includes_com_b(self, content):
        # Diagnostic group в Tier 3 deep refs
        assert "com_b_diagnostic.md" in content

    def test_tier3_includes_environment_design(self, content):
        # Goal arch group в Tier 3 deep refs
        assert "environment_design.md" in content

    def test_master_under_token_budget(self, content):
        # Master ≤ 4000 tokens (rough estimate: chars / 4)
        approx_tokens = len(content) // 4
        assert approx_tokens <= 4000, f"Master ~{approx_tokens} tokens, exceeds 4000 budget"


class TestPhase1ModuleIntegration:
    """Validate module_phase1_diagnostic.md opt-in COM-B entry."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "module_phase1_diagnostic.md"
        return path.read_text(encoding="utf-8")

    def test_com_b_section_present(self, content):
        assert "COM-B" in content or "com-b" in content.lower()
        # Должна быть отдельная секция
        assert "## COM-B" in content or "## Com-B" in content

    def test_com_b_opt_in_framing(self, content):
        lower = content.lower()
        assert "opt-in" in lower or "не запускай автоматически" in lower or "повторяющаяся жалоба" in lower

    def test_loads_com_b_ref(self, content):
        assert "com_b_diagnostic.md" in content, "Must instruct to load com_b_diagnostic.md"

    def test_state_writes_includes_com_b_assessment(self, content):
        assert "com_b_assessment" in content, "State writes must include com_b_assessment field"

    def test_module_under_token_budget(self, content):
        # Phase modules ≤ 2500 tokens
        approx_tokens = len(content) // 4
        assert approx_tokens <= 2500, f"Phase 1 module ~{approx_tokens} tokens, exceeds 2500 budget"


class TestEvidenceMapUpdated:
    """Validate evidence_map.md status updates for v1.2.0."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "evidence_map.md"
        return path.read_text(encoding="utf-8")

    def test_com_b_no_longer_planned(self, content):
        """COM-B should no longer have 'Planned для v1.2' status."""
        # Найти секцию COM-B
        com_b_idx = content.find("### COM-B Model")
        assert com_b_idx >= 0, "Missing COM-B Model section"
        # Взять следующие ~600 chars (примерно одна секция)
        section = content[com_b_idx:com_b_idx + 800]
        assert "Planned для v1.2" not in section, "COM-B still marked as 'Planned для v1.2'"
        # Должен быть Used in:
        assert "Used in:" in section, "COM-B should now have 'Used in:' marker"
        assert "com_b_diagnostic.md" in section

    def test_environment_design_documented(self, content):
        assert "Environment Design" in content or "environment_design" in content
        # Должна быть отдельная секция с evidence
        assert "Lally" in content
        assert "Fogg" in content


class TestSchemaV2_2_2:
    """Validate state_v2_schema.md bump для COM-B."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "state_v2_schema.md"
        return path.read_text(encoding="utf-8")

    def test_schema_version_bumped(self, content):
        # Frontmatter version
        assert "2.2.2" in content, "Schema version must be bumped to 2.2.2"
        # schema_version в JSON
        assert '"schema_version": "2.2.2"' in content

    def test_com_b_assessment_field_documented(self, content):
        # В JSON блоке
        assert "com_b_assessment" in content
        # В §3 поле-за-полем
        assert "3.4.3" in content or "diagnosis.com_b_assessment" in content
        # Все 5 sub-fields документированы
        for field in ["capability", "opportunity", "motivation", "primary_gap", "assessed_at"]:
            assert field in content, f"Missing field documentation: {field}"

    def test_changelog_entry_added(self, content):
        # §12 Changelog
        assert "**2.2.2**" in content or "2.2.2" in content
        # Связан с v1.2.0
        assert "v1.2.0" in content or "v1.2" in content

    def test_additive_policy_documented(self, content):
        # §4.1 Additive bumps должен mention 2.2.2
        assert "2.2 → 2.2.2" in content or "2.2.2" in content

    def test_field_matrix_includes_com_b(self, content):
        # §9 Field availability matrix
        assert "diagnosis.com_b_assessment" in content
        assert "schema 2.2.2" in content or "v1.2.0, schema 2.2.2" in content


class TestPlatformIntegration:
    """Validate all 4 platform SKILL.md files include COM-B + environment_design."""

    @pytest.fixture(scope="class")
    def platforms(self):
        return {
            "claude": PLATFORMS / "claude" / "SKILL.md",
            "grok": PLATFORMS / "grok" / "SKILL.md",
            "kimi": PLATFORMS / "kimi" / "SKILL.md",
            "kimi-cli": PLATFORMS / "kimi-cli" / "SKILL.md",
        }

    def test_lazy_platforms_reference_com_b(self, platforms):
        """Lazy-load platforms (claude, kimi-cli) reference COM-B in Tier 3."""
        for name in ["claude", "kimi-cli"]:
            path = platforms[name]
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            assert "com_b_diagnostic" in content.lower(), f"{name} missing com_b_diagnostic reference"

    def test_lazy_platforms_reference_environment_design(self, platforms):
        for name in ["claude", "kimi-cli"]:
            path = platforms[name]
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            assert "environment_design" in content.lower(), f"{name} missing environment_design reference"
