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
