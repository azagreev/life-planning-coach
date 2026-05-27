"""System tests for v1.3.0 — WoL Refactor + v1.2 Follow-ups.

Covers (по PR):
- PR-C: COM-B Phase 0 upsell в emotion_regulation.md § 5 + com_b_diagnostic.md table update.
- PR-A: WoL frequency gate, schema 2.2.5 (diagnosis.wheel_of_life.last_assessed_at), Phase 1 module gating.
- PR-B: AAR sighted_count runtime pattern matching в Phase 3 Step 9 (stacked на PR-A).

См. ROADMAP.md «v1.3.0» и CHANGELOG.md `## [1.3.0]` для full scope.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
REFERENCES = PROJECT_ROOT / "references"
PLATFORMS = PROJECT_ROOT / "platforms"

# Russian quoted speech pattern для local forbidden-words check.
# Helper (tests/helpers/forbidden_words.py) — landed в PR-D; here inline для
# orthogonal PR без stacked dependency. После merge PR-D можно migrate.
_QUOTED_SPEECH = re.compile(r"«[^»]*»")


def _strip_quoted(content: str) -> str:
    return _QUOTED_SPEECH.sub("", content)


class TestCOMBUpsell:
    """PR-C: COM-B Phase 0 upsell в emotion_regulation.md § 5."""

    @pytest.fixture(scope="class")
    def er_content(self):
        path = REFERENCES / "emotion_regulation.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def com_b_content(self):
        path = REFERENCES / "com_b_diagnostic.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def master_content(self):
        path = PROJECT_ROOT / "SKILL.master.md"
        return path.read_text(encoding="utf-8")

    def test_er_module_has_com_b_upsell_section(self, er_content):
        """§ 5 with COM-B Upsell heading must exist."""
        assert "## 5. COM-B Upsell" in er_content, (
            "emotion_regulation.md must have '## 5. COM-B Upsell' section "
            "(v1.3.0 PR-C). See ROADMAP «v1.3.0 → COM-B Phase 0 soft upsell»."
        )

    def test_com_b_upsell_is_opt_in(self, er_content):
        """Framing must be soft / opt-in, не directive."""
        lower = er_content.lower()
        # Должно быть «Хочешь» / opt-in framing
        assert "хочешь" in lower or "хотите" in lower or "opt-in" in lower, (
            "COM-B upsell must use opt-in framing ('Хочешь', 'opt-in')"
        )
        # Decline handling must be documented
        assert "decline" in lower or "не сейчас" in lower or "давай позже" in lower, (
            "Must document decline handling pattern"
        )
        # After 2 declines: stop
        assert "второго" in lower or "второй" in lower or "two declines" in lower, (
            "Must specify 2-decline cutoff rule per session"
        )

    def test_com_b_upsell_references_com_b_diagnostic(self, er_content):
        """Routing must link to com_b_diagnostic.md."""
        assert "com_b_diagnostic.md" in er_content, (
            "COM-B upsell must link к references/com_b_diagnostic.md как next step"
        )

    def test_com_b_upsell_cites_michie(self, er_content):
        """Evidence citation Michie 2011 required (как в Tier 3 ref)."""
        lower = er_content.lower()
        assert "michie" in lower, "Missing Michie citation"
        assert "2011" in er_content, "Missing 2011 year"
        assert "implementation science" in lower or "10.1186/1748-5908-6-42" in er_content, (
            "Missing journal name or DOI"
        )

    def test_com_b_upsell_distinguishes_from_phase_1(self, er_content):
        """Must explain why в ER module, не в Phase 1."""
        lower = er_content.lower()
        # Distinction между sphere-level (Phase 1) и single-behavior level (ER upsell)
        assert ("sphere" in lower or "сфер" in lower), (
            "Must mention sphere-level Phase 1 vs single-behavior упomination"
        )
        assert ("single" in lower or "single-behavior" in lower or "одно конкретное" in lower), (
            "Must contrast с Phase 1 sphere-level entry"
        )
        # Lean conversation mode context
        assert "lean_conversation" in lower or "lean conversation" in lower, (
            "Must mention lean_conversation mode rationale"
        )

    def test_com_b_diagnostic_table_points_to_er_module(self, com_b_content):
        """com_b_diagnostic.md table «Где это уже встроено» Phase 0 row must
        reference emotion_regulation.md § 5, не master."""
        # Ищем row для Phase 0/0.5 ER upsell
        assert "emotion_regulation.md" in com_b_content, (
            "com_b_diagnostic.md table must reference emotion_regulation.md для Phase 0 entry"
        )
        # v1.3.0 entry должен быть phrased как ER upsell
        lower = com_b_content.lower()
        assert "v1.3" in lower or "er upsell" in lower or "phase 0.5" in lower, (
            "Phase 0 row должна mention v1.3 ER upsell или Phase 0.5"
        )

    def test_master_does_not_have_phase0_com_b_trigger(self, master_content):
        """Regression guard для v1.2 budget decision:
        SKILL.master.md НЕ должен иметь direct COM-B trigger в Phase 0 (Emotional Landing).
        Discovery работает через Tier 3 listing + ER module upsell."""
        # COM-B всё ещё в Tier 3 listing — это нормально
        assert "com_b_diagnostic.md" in master_content, (
            "Tier 3 listing должен mention com_b_diagnostic.md"
        )
        # НО: не должно быть «Phase 0» + «COM-B» в одной близости (trigger pattern)
        # Простая проверка: в первых 3000 chars (Phase 0 / Routing Map территория)
        # COM-B не должен mentioned как направление из Phase 0
        head = master_content[:3000].lower()
        # Phase 0 section не должна содержать direct COM-B trigger.
        # OK если упоминается в Routing Map для direct user request («как себя заставить»).
        phase0_idx = head.find("phase 0")
        if phase0_idx != -1:
            # Check 500 chars после Phase 0 mention — не должно быть com_b trigger
            phase0_block = head[phase0_idx:phase0_idx + 500]
            assert "com_b" not in phase0_block, (
                "Regression: SKILL.master.md Phase 0 section имеет COM-B trigger. "
                "Это нарушает v1.2.0 architecture decision (см. CHANGELOG ## [1.2.0])."
            )

    def test_com_b_upsell_section_no_forbidden_words(self, er_content):
        """Forbidden directive words check (с whitelist Russian quoted speech)
        — scoped TO § 5 COM-B Upsell section ONLY.

        Pre-existing ER content (§3 Self-Compassion antipattern examples) использует
        английские `"..."` quotes для anti-pattern dialogue — не whitelisted helper'ом
        и не в scope PR-C. Migrating всех existing examples к Russian «...» — separate
        refactor.
        """
        # Slice § 5 COM-B Upsell content
        section_start = er_content.find("## 5. COM-B Upsell")
        assert section_start != -1, "§ 5 COM-B Upsell section должна существовать"
        next_section = er_content.find("\n## ", section_start + 1)
        section = er_content[section_start:next_section] if next_section != -1 else er_content[section_start:]

        forbidden = ["надо", "должен", "обязан"]
        stripped = _strip_quoted(section).lower()
        for word in forbidden:
            assert word not in stripped, (
                f"Forbidden directive word '{word}' found в § 5 COM-B Upsell "
                f"вне Russian quoted speech. Если это user example — оберни в «...»."
            )

    def test_er_module_within_reasonable_size(self, er_content):
        """ER module — Tier 2 routing target, должен оставаться обозримым.

        Currently ~217 lines pre-PR-C. After § 5 — ~260 lines. Hard limit 350.
        (ER module не входит в ALL_MODULES_BUDGET_TOKENS=15000 phase modules constraint —
        lazy-loaded at Phase 0.5 entry, не aggregated.)
        """
        lines = er_content.splitlines()
        assert len(lines) <= 350, f"emotion_regulation.md too long: {len(lines)} lines (max 350)"


class TestWoLFrequencyGate:
    """PR-A: WoL frequency gate в Phase 1 module + schema 2.2.5."""

    @pytest.fixture(scope="class")
    def phase1_content(self):
        path = REFERENCES / "module_phase1_diagnostic.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def schema_content(self):
        path = REFERENCES / "state_v2_schema.md"
        return path.read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def evidence_map_content(self):
        path = REFERENCES / "evidence_map.md"
        return path.read_text(encoding="utf-8")

    def test_phase1_has_wol_frequency_gate_section(self, phase1_content):
        """Phase 1 module должен содержать `## WoL Frequency Gate` heading."""
        assert "## WoL Frequency Gate" in phase1_content, (
            "module_phase1_diagnostic.md must have '## WoL Frequency Gate' section "
            "(v1.3.0 PR-A). PRD v0.15 §5."
        )

    def test_phase1_wol_gate_three_branches(self, phase1_content):
        """Gate должен покрывать все 3 ветки: < 30d, ≥ 30d, null."""
        # Find section
        idx = phase1_content.find("## WoL Frequency Gate")
        assert idx != -1
        next_h = phase1_content.find("\n## ", idx + 1)
        section = phase1_content[idx:next_h] if next_h != -1 else phase1_content[idx:]
        lower = section.lower()

        assert "30 дней" in lower or "30 days" in lower, "Must mention 30-day threshold"
        assert "< 30" in section or "&lt; 30" in section, "Missing < 30 days branch"
        assert "≥ 30" in section or ">= 30" in section, "Missing ≥ 30 days branch"
        assert "null" in lower, "Missing null (never assessed) branch"

    def test_phase1_wol_gate_mentions_last_assessed_at(self, phase1_content):
        """Gate должен reference field `last_assessed_at` для check."""
        assert "last_assessed_at" in phase1_content, (
            "WoL gate must check diagnosis.wheel_of_life.last_assessed_at field"
        )

    def test_phase1_state_write_includes_last_assessed_at(self, phase1_content):
        """State writes секция должна require write `last_assessed_at` after completion."""
        # Find State writes section
        idx = phase1_content.find("## State writes")
        assert idx != -1, "State writes section missing"
        state_section = phase1_content[idx:]

        assert "last_assessed_at" in state_section, (
            "State writes должна include обязательный write `last_assessed_at` после WoL completion"
        )
        assert "обязательно" in state_section.lower(), (
            "Write trigger должна быть marked как обязательная"
        )

    def test_phase1_under_token_budget(self, phase1_content):
        """Regression guard: Phase 1 module ≤ 2500 tokens (chars/3 estimate)."""
        approx_tokens = len(phase1_content) // 3
        assert approx_tokens <= 2500, (
            f"module_phase1_diagnostic.md = {approx_tokens} tokens > 2500 limit. "
            f"Trim verbose sections or move detail к state_v2_schema.md / external refs."
        )

    def test_evidence_map_wol_entry_updated(self, evidence_map_content):
        """evidence_map.md WoL entry должен mention frequency gate implementation, не v1.3 plan."""
        # Find WoL entry
        idx = evidence_map_content.find("### Wheel of Life")
        assert idx != -1, "Wheel of Life entry missing в evidence_map.md"
        entry = evidence_map_content[idx:idx + 500]

        assert "v1.3 plan" not in entry, (
            "WoL entry все еще говорит 'v1.3 plan' — после ship должен говорить о реализации"
        )
        assert "last_assessed_at" in entry, (
            "WoL entry должна mention `last_assessed_at` field (schema 2.2.5)"
        )
        assert "2.2.5" in entry, "Must reference schema 2.2.5"

    def test_phase1_no_forbidden_words_in_wol_gate(self, phase1_content):
        """Forbidden words check scoped к WoL Frequency Gate section."""
        idx = phase1_content.find("## WoL Frequency Gate")
        assert idx != -1
        next_h = phase1_content.find("\n## ", idx + 1)
        section = phase1_content[idx:next_h] if next_h != -1 else phase1_content[idx:]

        forbidden = ["надо", "должен", "обязан"]
        stripped = _strip_quoted(section).lower()
        # «обязательно» в State writes context допустимо как marker для skill —
        # whitelist его (содержит «обязан» substring но другой смысл).
        # Используем substring check excluding «обязательно»:
        for word in forbidden:
            if word == "обязан":
                # Allow «обязательно» (modifier для write trigger)
                lines = [l for l in stripped.splitlines() if word in l and "обязательно" not in l]
                assert not lines, f"Forbidden '{word}' (not 'обязательно') в WoL gate: {lines}"
            else:
                assert word not in stripped, f"Forbidden '{word}' в WoL gate"


class TestSchemaWoLField:
    """PR-A: schema 2.2.4 → 2.2.5 (additive bump, last_assessed_at field)."""

    @pytest.fixture(scope="class")
    def content(self):
        path = REFERENCES / "state_v2_schema.md"
        return path.read_text(encoding="utf-8")

    def test_schema_version_bumped_to_2_2_5(self, content):
        """`schema_version` в JSON literal должен быть 2.2.5."""
        assert '"schema_version": "2.2.5"' in content, (
            "JSON schema literal must say schema_version: 2.2.5"
        )

    def test_header_version_2_2_5(self, content):
        """Header `Версия схемы` должна показывать 2.2.5."""
        assert "**Версия схемы:** `2.2.5`" in content, (
            "Header line должна show Версия схемы: 2.2.5"
        )

    def test_last_assessed_at_field_in_json_schema(self, content):
        """JSON schema должна include last_assessed_at field в wheel_of_life block."""
        # wheel_of_life block должен содержать last_assessed_at
        wol_idx = content.find('"wheel_of_life": {')
        assert wol_idx != -1
        # Next 500 chars должны иметь last_assessed_at
        wol_block = content[wol_idx:wol_idx + 500]
        assert "last_assessed_at" in wol_block, (
            "wheel_of_life block в JSON schema must include last_assessed_at field"
        )

    def test_3_4_4_section_documented(self, content):
        """Должна быть §3.4.4 doc для last_assessed_at field."""
        assert "### 3.4.4 diagnosis.wheel_of_life.last_assessed_at" in content, (
            "Missing §3.4.4 documentation for last_assessed_at field"
        )

    def test_additive_bump_2_2_4_to_2_2_5_documented(self, content):
        """§4.1 Additive bumps должна mention `2.2.4 → 2.2.5` transition."""
        assert "2.2.4 → 2.2.5" in content, (
            "Missing §4.1 entry для 2.2.4 → 2.2.5 bump"
        )

    def test_field_matrix_includes_last_assessed_at(self, content):
        """§9 Field availability matrix должна include row для last_assessed_at."""
        idx = content.find("## 9. Field availability matrix")
        assert idx != -1
        # Slice до next ## header (or end of file)
        next_h = content.find("\n## ", idx + 1)
        matrix_section = content[idx:next_h] if next_h != -1 else content[idx:]
        assert "diagnosis.wheel_of_life.last_assessed_at" in matrix_section, (
            "§9 field matrix должна have row для last_assessed_at"
        )
        assert "2.2.5" in matrix_section, "Matrix row должен mention schema 2.2.5"

    def test_changelog_2_2_5_entry_exists(self, content):
        """§12 Changelog должна have 2.2.5 entry с PRD reference."""
        idx = content.find("## 12. Changelog схемы")
        assert idx != -1
        cl_section = content[idx:]
        assert "**2.2.5**" in cl_section, "Missing 2.2.5 changelog entry"
        # Section должна быть FIRST (newest first ordering)
        first_entry_pos = cl_section.find("**2.")
        first_2_5 = cl_section.find("**2.2.5**")
        assert first_2_5 == first_entry_pos, (
            "2.2.5 entry must be FIRST (newest first ordering)"
        )

    def test_changelog_2_2_4_entry_still_present(self, content):
        """Regression guard: history-preserving bumps."""
        idx = content.find("## 12. Changelog схемы")
        cl_section = content[idx:] if idx != -1 else ""
        assert "**2.2.4**" in cl_section, "v2.2.4 changelog entry должна remain"
        assert "**2.2.3**" in cl_section, "v2.2.3 changelog entry должна remain"
        assert "**2.2.2**" in cl_section, "v2.2.2 changelog entry должна remain"
