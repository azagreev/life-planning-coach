"""System tests for Drive Wiki Path A skill protocol refactor.

Covers (per BACKLOG «Drive Wiki Path A — full skill protocol refactor», RICE 56):

- `save_state(template, content)` abstraction is formally defined in
  `references/drive_integration.md` with explicit filename pattern.
- `read_state(template)` reads latest snapshot by `modifiedTime`.
- `templates/AI_Instructions.md` references the abstraction and maps templates
  to subfolders with `save_state` call-site wording.
- `references/state_v2_schema.md` §5 cross-references the abstraction.
- Legacy «overwrite полностью» / in-place-edit wording is gone from
  `templates/Hot_Cache.md` and `templates/Progress_Dashboard.md`.
- `templates/Wheel_of_Life_History.md` describes snapshot composition,
  not in-place file editing.

These guards prevent regression of the 2026-05-26 Path A architecture decision
(see `docs/research/mcp_poc_log.md` §Drive PoC for why update_file is absent).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
REFERENCES = PROJECT_ROOT / "references"
TEMPLATES = REFERENCES / "templates"


class TestSaveStateDefinition:
    """`save_state(template, content)` must be formally defined in drive_integration.md."""

    @pytest.fixture(scope="class")
    def drive_integration(self) -> str:
        path = REFERENCES / "drive_integration.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_save_state_section_exists(self, drive_integration: str) -> None:
        """A heading dedicated to save_state must exist."""
        assert re.search(
            r"###\s+`?save_state\(template,\s*content\)`?",
            drive_integration,
        ), (
            "drive_integration.md must define `save_state(template, content)` "
            "as a write abstraction (Path A refactor)."
        )

    def test_read_state_section_exists(self, drive_integration: str) -> None:
        """A heading dedicated to read_state must exist."""
        assert re.search(
            r"###\s+`?read_state\(template\)`?",
            drive_integration,
        ), (
            "drive_integration.md must define `read_state(template)` as the "
            "counterpart abstraction; latest-by-modifiedTime semantics."
        )

    def test_filename_pattern_uses_template_iso(self, drive_integration: str) -> None:
        """Path A files must use `{template}_{ISO}.md` shape."""
        assert "{template}_{iso}.md" in drive_integration.lower() or (
            "{template}_{ISO}.md" in drive_integration
        ), (
            "drive_integration.md must show the canonical filename pattern "
            "`{template}_{ISO}.md` so other docs reference it consistently."
        )

    def test_read_state_picks_latest_by_modified_time(self, drive_integration: str) -> None:
        """read_state must explicitly call out `orderBy=modifiedTime desc`."""
        assert re.search(
            r"orderBy\s*=?\s*[\"']?modifiedTime\s+desc",
            drive_integration,
        ), (
            "drive_integration.md read_state must use `orderBy=modifiedTime desc` "
            "and `pageSize=1` so callers always get the current snapshot."
        )

    def test_forward_compat_note_present(self, drive_integration: str) -> None:
        """save_state section must note Path B / Path F swap point."""
        assert ("Path B" in drive_integration and "Path F" in drive_integration), (
            "save_state must be framed as forward-compat — Path B/F backends swap "
            "at this call site without rewriting phase modules."
        )


class TestAIInstructionsReferences:
    """`templates/AI_Instructions.md` must describe writes via save_state."""

    @pytest.fixture(scope="class")
    def ai_instructions(self) -> str:
        path = TEMPLATES / "AI_Instructions.md"
        assert path.exists(), f"Missing {path}"
        return path.read_text(encoding="utf-8")

    def test_save_state_mentioned_in_write_protocol(self, ai_instructions: str) -> None:
        assert "save_state(template, content)" in ai_instructions, (
            "AI_Instructions.md must reference `save_state(template, content)` "
            "as the canonical write call site."
        )

    def test_template_to_subfolder_table_uses_save_state_calls(self, ai_instructions: str) -> None:
        """The «когда какой template писать» table must use save_state(...) wording."""
        for template_call in [
            'save_state("Hot_Cache"',
            'save_state("Goals"',
            'save_state("Wheel_of_Life_History"',
            'save_state("Progress_Dashboard"',
        ]:
            assert template_call in ai_instructions, (
                f"AI_Instructions.md table must show concrete call `{template_call}` "
                "so phase modules and humans share one mental model."
            )

    def test_forward_compat_explicit(self, ai_instructions: str) -> None:
        """AI_Instructions.md must explain why call sites stay stable across backends."""
        assert re.search(r"forward.?compat", ai_instructions, re.IGNORECASE), (
            "AI_Instructions.md must mention forward-compat: phase modules call "
            "`save_state(...)`; backend (Path A/B/F) swaps without module edits."
        )


class TestStateSchemaCrossRef:
    """`state_v2_schema.md` §5 must cross-ref save_state."""

    @pytest.fixture(scope="class")
    def schema(self) -> str:
        path = REFERENCES / "state_v2_schema.md"
        return path.read_text(encoding="utf-8")

    def test_section_5_mentions_save_state(self, schema: str) -> None:
        """Gating logic section must point to save_state abstraction."""
        section_5_match = re.search(
            r"## 5\. Gating logic.*?(?=^## 6\.)",
            schema,
            re.DOTALL | re.MULTILINE,
        )
        assert section_5_match, "state_v2_schema.md must have §5 Gating logic"
        section_5 = section_5_match.group(0)
        assert "save_state" in section_5, (
            "state_v2_schema.md §5 must cross-reference `save_state` so the "
            "schema doc and Drive integration stay consistent."
        )


class TestLegacyWordingRemoved:
    """Legacy overwrite / in-place edit wording must be gone from templates."""

    def test_hot_cache_no_overwrite_wording(self) -> None:
        path = TEMPLATES / "Hot_Cache.md"
        content = path.read_text(encoding="utf-8")
        assert "overwrite полностью" not in content, (
            "Hot_Cache.md must not say «overwrite полностью» — MCP has no "
            "update_file; writes go through save_state (Path A new-file pattern)."
        )
        # Must point to save_state instead
        assert "save_state" in content, (
            "Hot_Cache.md header must reference save_state so readers know "
            "the actual write mechanism."
        )

    def test_progress_dashboard_no_autoupdate_wording(self) -> None:
        path = TEMPLATES / "Progress_Dashboard.md"
        content = path.read_text(encoding="utf-8")
        # Old line «Автообновляется. Последнее обновление: ...» suggests in-place
        # update; should be replaced with save_state framing.
        assert "Автообновляется. Последнее обновление" not in content, (
            "Progress_Dashboard.md must not say «Автообновляется. Последнее "
            "обновление» — implies in-place update. Reframe as save_state "
            "new-file per save."
        )
        assert "save_state" in content, (
            "Progress_Dashboard.md header must reference save_state."
        )

    def test_wheel_of_life_history_describes_composition_not_in_place_edit(self) -> None:
        path = TEMPLATES / "Wheel_of_Life_History.md"
        content = path.read_text(encoding="utf-8")
        # Old «КАК ОБНОВИТЬ ТАБЛИЦУ ДИНАМИКИ» framed as in-place edit of an
        # existing file. New framing: composition of new snapshot's content.
        assert "КАК СОСТАВИТЬ НОВЫЙ SNAPSHOT" in content, (
            "Wheel_of_Life_History.md must frame its instructions as "
            "«КАК СОСТАВИТЬ НОВЫЙ SNAPSHOT» (composition), not «КАК ОБНОВИТЬ» "
            "(in-place edit). Path A writes a new file per save."
        )
        # Must explicitly mention read_state for picking up the prior snapshot
        assert "read_state" in content, (
            "Wheel_of_Life_History.md instructions must show that the new "
            "snapshot is composed after read_state of the prior latest file."
        )


class TestProtocolConsistency:
    """save_state / read_state references must stay consistent across docs."""

    @pytest.fixture(scope="class")
    def all_refs(self) -> dict[str, str]:
        return {
            "drive": (REFERENCES / "drive_integration.md").read_text(encoding="utf-8"),
            "ai_instructions": (TEMPLATES / "AI_Instructions.md").read_text(encoding="utf-8"),
            "schema": (REFERENCES / "state_v2_schema.md").read_text(encoding="utf-8"),
        }

    def test_iso_format_consistent(self, all_refs: dict[str, str]) -> None:
        """ISO timestamp format must be `YYYY-MM-DDTHH-MM` in both drive_integration and AI_Instructions."""
        for name, content in all_refs.items():
            if name == "schema":
                continue  # schema § only cross-refs, doesn't restate format
            assert "YYYY-MM-DDTHH-MM" in content, (
                f"{name} must spell out the ISO format `YYYY-MM-DDTHH-MM` "
                "(colons replaced with `-`) so call sites pick the right pattern."
            )

    def test_disable_conversion_to_google_type_flag_documented(
        self, all_refs: dict[str, str]
    ) -> None:
        """The MIME-preservation flag must be documented in save_state definition."""
        assert "disableConversionToGoogleType" in all_refs["drive"], (
            "drive_integration.md save_state must include "
            "`disableConversionToGoogleType=true` — without it, text/markdown "
            "is silently converted to Google Doc and Path A breaks (quirk #24)."
        )
