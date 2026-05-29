"""v1.0.0: behavioral e2e tests for 4 gating modes.

Tests the pure-function reference implementation in scripts/gating_logic.py,
which mirrors the protocol declared in:
- SKILL.master.md §3 (trigger algorithm)
- references/state_v2_schema.md §5 (mode matrix)
- references/templates/AI_Instructions.md §Bootstrap & §Backfill

This module is the spec-side counterpart to prompt-based execution; tests
here verify the contract rather than the LLM's interpretation of it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

# Imports must come AFTER sys.path insertion
import gating_logic  # noqa: E402
from gating_logic import (  # noqa: E402
    EXECUTION_NO_WIKI,
    FULL_PERSISTENCE,
    LEAN_CONVERSATION,
    WIKI_NO_EXECUTION,
    GatingState,
    PersistenceRetry,
    accept_backfill,
    decline_backfill,
    detect_gating_mode,
    on_drive_connected_mid_session,
    on_session_start,
    run_bootstrap,
    should_bootstrap_drive,
    should_offer_backfill,
)


# ----- Mode detection matrix --------------------------------------------


@pytest.mark.parametrize(
    "drive,calendar,expected_mode",
    [
        (True, True, FULL_PERSISTENCE),
        (True, False, WIKI_NO_EXECUTION),
        (False, True, EXECUTION_NO_WIKI),
        (False, False, LEAN_CONVERSATION),
    ],
)
def test_detect_gating_mode_matrix(drive: bool, calendar: bool, expected_mode: str):
    """Every (drive, calendar) combination maps to one of 4 modes."""
    assert detect_gating_mode(drive, calendar) == expected_mode


def test_all_4_modes_are_valid():
    """No typos in mode constants."""
    assert {FULL_PERSISTENCE, WIKI_NO_EXECUTION, EXECUTION_NO_WIKI, LEAN_CONVERSATION} == gating_logic.ALL_MODES


# ----- on_session_start integration -------------------------------------


@pytest.mark.parametrize(
    "drive,calendar,expected_mode",
    [
        (True, True, FULL_PERSISTENCE),
        (True, False, WIKI_NO_EXECUTION),
        (False, True, EXECUTION_NO_WIKI),
        (False, False, LEAN_CONVERSATION),
    ],
)
def test_session_start_writes_gating_mode(drive, calendar, expected_mode):
    """on_session_start writes session.gating_mode."""
    state = on_session_start(drive, calendar)
    assert state.gating_mode == expected_mode


def test_session_start_resets_session_scoped_flags():
    """backfill_offered/accepted are session-scoped → reset at start."""
    state = GatingState(backfill_offered=True, backfill_accepted=True)
    state = on_session_start(False, False, state)
    assert state.backfill_offered is False
    assert state.backfill_accepted is False


# ----- Bootstrap protocol -----------------------------------------------


def test_bootstrap_triggers_only_on_first_drive_connect():
    state = GatingState()
    assert should_bootstrap_drive(True, state) is True

    # After bootstrap, no longer triggers
    state = run_bootstrap(state)
    assert should_bootstrap_drive(True, state) is False


def test_bootstrap_does_not_trigger_without_drive():
    state = GatingState()
    assert should_bootstrap_drive(False, state) is False


def test_bootstrap_is_idempotent():
    """Running bootstrap twice leaves state unchanged after the first call."""
    state = GatingState()
    state = run_bootstrap(state, now="2026-05-28T10:00:00Z")
    first_at = state.drive.first_connection_at
    state = run_bootstrap(state, now="2026-05-28T11:00:00Z")
    assert state.drive.first_connection_at == first_at  # unchanged
    assert state.drive.wiki_bootstrapped is True


def test_session_start_triggers_bootstrap_when_drive_connected():
    state = on_session_start(True, True)
    assert state.drive.wiki_bootstrapped is True
    assert state.drive.first_connection_at is not None


def test_session_start_does_not_bootstrap_without_drive():
    state = on_session_start(False, True)
    assert state.drive.wiki_bootstrapped is False
    assert state.drive.first_connection_at is None


# ----- Backfill protocol ------------------------------------------------


def test_backfill_offered_only_when_drive_joins_after_lean():
    state = GatingState()
    assert should_offer_backfill(True, LEAN_CONVERSATION, state) is True
    assert should_offer_backfill(True, EXECUTION_NO_WIKI, state) is True
    # Should NOT offer if previously already had wiki
    assert should_offer_backfill(True, WIKI_NO_EXECUTION, state) is False
    assert should_offer_backfill(True, FULL_PERSISTENCE, state) is False


def test_backfill_does_not_offer_without_drive():
    state = GatingState()
    assert should_offer_backfill(False, LEAN_CONVERSATION, state) is False


def test_backfill_offered_only_once_per_session():
    state = GatingState()
    assert should_offer_backfill(True, LEAN_CONVERSATION, state) is True
    state.backfill_offered = True
    assert should_offer_backfill(True, LEAN_CONVERSATION, state) is False


def test_backfill_accepted_runs_bootstrap_and_switches_mode():
    # BUG-018: backfill connects only Drive. From lean_conversation (no calendar)
    # the correct post-accept mode is wiki_no_execution, NOT full_persistence
    # (the §5 matrix reserves full_persistence for drive + calendar).
    state = GatingState(gating_mode=LEAN_CONVERSATION)
    state = accept_backfill(state)
    assert state.backfill_offered is True
    assert state.backfill_accepted is True
    assert state.drive.wiki_bootstrapped is True
    assert state.gating_mode == WIKI_NO_EXECUTION


def test_backfill_accepted_from_execution_no_wiki_switches_to_full():
    # execution_no_wiki = calendar already connected; adding Drive via backfill
    # completes the pair → full_persistence.
    state = GatingState(gating_mode=EXECUTION_NO_WIKI)
    state = accept_backfill(state)
    assert state.backfill_accepted is True
    assert state.drive.wiki_bootstrapped is True
    assert state.gating_mode == FULL_PERSISTENCE


def test_backfill_decline_increments_counter():
    state = GatingState()
    state = decline_backfill(state)
    assert state.backfill_offered is True
    assert state.drive.user_declined_count == 1
    # Single decline — no backoff yet
    assert state.drive.backoff_until_session == 0


def test_backoff_kicks_in_after_2_declines():
    state = GatingState(session_count=5)
    state = decline_backfill(state)
    # First decline — reset offered for next session via on_session_start typically
    state.backfill_offered = False
    state = decline_backfill(state)
    assert state.drive.user_declined_count == 2
    assert state.drive.backoff_until_session == 5 + 3  # session_count + BACKOFF_SESSIONS


def test_backfill_respects_backoff():
    state = GatingState(
        session_count=5,
        drive=PersistenceRetry(backoff_until_session=8),
    )
    # session 5 — still in backoff (backoff_until_session=8 means sessions 5,6,7 blocked)
    assert should_offer_backfill(True, LEAN_CONVERSATION, state) is False

    state.session_count = 8
    assert should_offer_backfill(True, LEAN_CONVERSATION, state) is True


# ----- Mid-session connector change ------------------------------------


def test_mid_session_drive_connect_from_lean_offers_backfill():
    state = GatingState(gating_mode=LEAN_CONVERSATION)
    state, should_prompt = on_drive_connected_mid_session(LEAN_CONVERSATION, state)
    assert should_prompt is True
    # Mode unchanged until user accepts/declines
    assert state.gating_mode == LEAN_CONVERSATION


def test_mid_session_drive_connect_from_execution_no_wiki_offers_backfill():
    state = GatingState(gating_mode=EXECUTION_NO_WIKI)
    state, should_prompt = on_drive_connected_mid_session(EXECUTION_NO_WIKI, state)
    assert should_prompt is True


def test_mid_session_drive_after_backfill_offered_does_not_re_prompt():
    state = GatingState(gating_mode=LEAN_CONVERSATION, backfill_offered=True)
    state, should_prompt = on_drive_connected_mid_session(LEAN_CONVERSATION, state)
    assert should_prompt is False
