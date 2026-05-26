"""Pure-function reference implementation of the v0.18.0+ gating protocol.

This module is **a specification, not the executor**. The actual skill is
prompt-based — Claude/Grok/Kimi LLMs interpret SKILL.master.md §3 and write
to state v2 via Drive/Memory. This module mirrors that protocol so tests
can verify the contract behaviorally.

References:
- Schema: references/state_v2_schema.md §5 (gating modes)
- Bootstrap: references/templates/AI_Instructions.md §Bootstrap
- Backfill: references/templates/AI_Instructions.md §Backfill
- Master trigger: SKILL.master.md §3
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


# --- Gating modes -------------------------------------------------------

FULL_PERSISTENCE = "full_persistence"
WIKI_NO_EXECUTION = "wiki_no_execution"
EXECUTION_NO_WIKI = "execution_no_wiki"
LEAN_CONVERSATION = "lean_conversation"

ALL_MODES = {FULL_PERSISTENCE, WIKI_NO_EXECUTION, EXECUTION_NO_WIKI, LEAN_CONVERSATION}

# Modes that can trigger backfill (mid-session Drive connection)
BACKFILL_ELIGIBLE_PREVIOUS_MODES = {LEAN_CONVERSATION, EXECUTION_NO_WIKI}

# After 2 user declines, back off N sessions before re-offering
BACKFILL_BACKOFF_SESSIONS = 3
BACKFILL_DECLINE_THRESHOLD = 2


def detect_gating_mode(drive_connected: bool, calendar_connected: bool) -> str:
    """Return the persistence mode for the current (drive, calendar) combination.

    Mirrors SKILL.master.md §3 trigger algorithm:
        on session_start:
          mode = match (drive, calendar):
            (T,T) → full_persistence
            (T,F) → wiki_no_execution
            (F,T) → execution_no_wiki
            (F,F) → lean_conversation
    """
    match (drive_connected, calendar_connected):
        case (True, True):
            return FULL_PERSISTENCE
        case (True, False):
            return WIKI_NO_EXECUTION
        case (False, True):
            return EXECUTION_NO_WIKI
        case (False, False):
            return LEAN_CONVERSATION


@dataclass
class PersistenceRetry:
    """Mirror of state_v2.persistence_retry.drive subset."""
    wiki_bootstrapped: bool = False
    first_connection_at: str | None = None
    user_declined_count: int = 0
    backoff_until_session: int = 0


@dataclass
class GatingState:
    """Mirror of state_v2 fields needed for gating decisions."""
    session_count: int = 1
    gating_mode: str = LEAN_CONVERSATION
    drive: PersistenceRetry = field(default_factory=PersistenceRetry)
    backfill_offered: bool = False
    backfill_accepted: bool = False


# --- Bootstrap protocol -------------------------------------------------


def should_bootstrap_drive(drive_connected: bool, state: GatingState) -> bool:
    """First connection to Drive in a session → run bootstrap.

    Bootstrap creates Life Planning Coach Wiki/ folder structure + writes
    initial templates from references/templates/. After bootstrap,
    wiki_bootstrapped is set to True (idempotent).
    """
    return drive_connected and not state.drive.wiki_bootstrapped


def run_bootstrap(state: GatingState, now: str | None = None) -> GatingState:
    """Idempotent: marks state as bootstrapped, sets first_connection_at."""
    if state.drive.wiki_bootstrapped:
        return state
    state.drive.wiki_bootstrapped = True
    if state.drive.first_connection_at is None:
        state.drive.first_connection_at = now or datetime.now(timezone.utc).isoformat()
    return state


# --- Backfill protocol --------------------------------------------------


def should_offer_backfill(
    drive_connected: bool,
    previous_mode: str,
    state: GatingState,
) -> bool:
    """Mid-session Drive connection → offer to backfill session data.

    Conditions (all must be true):
    - Drive is now connected
    - Previous mode was lean_conversation or execution_no_wiki (no wiki yet)
    - Backfill not already offered in this session (single-fire)
    - Not in backoff period (user declined ≥ 2 times recently)
    """
    if not drive_connected:
        return False
    if previous_mode not in BACKFILL_ELIGIBLE_PREVIOUS_MODES:
        return False
    if state.backfill_offered:
        return False
    if state.session_count < state.drive.backoff_until_session:
        return False
    return True


def accept_backfill(state: GatingState) -> GatingState:
    """User accepted backfill prompt → mark accepted, run bootstrap, switch mode."""
    state.backfill_offered = True
    state.backfill_accepted = True
    state = run_bootstrap(state)
    state.gating_mode = FULL_PERSISTENCE
    return state


def decline_backfill(state: GatingState) -> GatingState:
    """User declined → mark offered, increment decline counter, set backoff if needed."""
    state.backfill_offered = True
    state.drive.user_declined_count += 1
    if state.drive.user_declined_count >= BACKFILL_DECLINE_THRESHOLD:
        state.drive.backoff_until_session = state.session_count + BACKFILL_BACKOFF_SESSIONS
    return state


# --- Top-level session lifecycle ---------------------------------------


def on_session_start(
    drive_connected: bool,
    calendar_connected: bool,
    state: GatingState | None = None,
) -> GatingState:
    """Apply gating protocol at session start.

    Returns a (possibly new) GatingState with gating_mode set.
    Bootstrap runs if first Drive connection; backfill is a separate
    later trigger (during session) when Drive joins mid-flight.
    """
    state = state or GatingState()
    mode = detect_gating_mode(drive_connected, calendar_connected)
    state.gating_mode = mode

    if should_bootstrap_drive(drive_connected, state):
        state = run_bootstrap(state)

    # Reset session-scoped flags
    state.backfill_offered = False
    state.backfill_accepted = False
    return state


def on_drive_connected_mid_session(
    previous_mode: str,
    state: GatingState,
) -> tuple[GatingState, bool]:
    """Handle Drive connecting after session_start.

    Returns (state, should_prompt_user). If should_prompt_user is True,
    the skill should ask «У тебя накопилось данных за сессию — синхронизировать?»
    and call accept_backfill() or decline_backfill() based on user response.
    """
    will_offer = should_offer_backfill(True, previous_mode, state)
    if not will_offer:
        # Update mode anyway (drive is now connected)
        state.gating_mode = FULL_PERSISTENCE if state.gating_mode == EXECUTION_NO_WIKI else WIKI_NO_EXECUTION
        return state, False
    return state, True
