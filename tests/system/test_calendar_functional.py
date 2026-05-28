"""System tests for calendar functional behaviour beyond raw algorithms.

Existing `test_calendar_integration.py` covers:
- Free Slot Algorithm correctness (executable reference impl, 11 tests)
- JSON constants (COLOR_MAP / REMINDER_PRESETS / RRULE_PRESETS)
- Event-pattern field validation (Weekly Review + WOOP Session)
- Calendar failure modes

This file closes the remaining BACKLOG P0 «Calendar functional tests» scope:

- `calendar_intelligence.md` Pre-flight Checklist (5 steps) — required gate
  before any `create_event` call
- Conflict Detection — must not overwrite; must propose alternative slots
- Workload Warning Thresholds — 6h / 8h boundaries documented
- `calendar_pattern_analyzer.md` — read-only contract, consent requirement,
  5 documented metrics with formulas + thresholds, rate-limit guidance

These are skill-instruction tests (the algorithms live as LLM-executed
prose, not as Python). They guard against silent drift in user-protection
content (consent, anti-patterns) and operational gates (preflight steps).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
REFERENCES = PROJECT_ROOT / "references"
CALENDAR_INTELLIGENCE = REFERENCES / "calendar_intelligence.md"
CALENDAR_PATTERN_ANALYZER = REFERENCES / "calendar_pattern_analyzer.md"


@pytest.fixture(scope="module")
def intelligence_text() -> str:
    assert CALENDAR_INTELLIGENCE.exists(), f"Missing {CALENDAR_INTELLIGENCE}"
    return CALENDAR_INTELLIGENCE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def pattern_analyzer_text() -> str:
    assert CALENDAR_PATTERN_ANALYZER.exists(), f"Missing {CALENDAR_PATTERN_ANALYZER}"
    return CALENDAR_PATTERN_ANALYZER.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Pre-flight Checklist (5 required steps before create_event)
# ---------------------------------------------------------------------------


PREFLIGHT_STEPS = [
    "Density Check",        # 1. list_events на дату, суммарная загрузка
    "Conflict Detection",   # 2. проверь overlap → не перезаписывай
    "Chronotype Alignment", # 3. сравни с peak/trough
    "Smart Proposal",       # 4. Free Slot Algorithm / suggest_time
    "Create with Validation",  # 5. create_event → get_event → проверь fields
]


class TestPreflightChecklist:
    """`## Pre-flight Checklist` must enumerate all 5 steps in order."""

    def test_preflight_section_present(self, intelligence_text: str) -> None:
        assert "## Pre-flight Checklist" in intelligence_text, (
            "calendar_intelligence.md must have `## Pre-flight Checklist` "
            "section — the gate before any `create_event` call."
        )

    @pytest.mark.parametrize("step", PREFLIGHT_STEPS)
    def test_each_preflight_step_present(self, intelligence_text: str, step: str) -> None:
        assert step in intelligence_text, (
            f"calendar_intelligence.md Pre-flight Checklist must include `{step}` "
            "step. All 5 steps are load-bearing for safe event creation."
        )

    def test_preflight_steps_in_documented_order(self, intelligence_text: str) -> None:
        positions = [intelligence_text.find(step) for step in PREFLIGHT_STEPS]
        assert all(p >= 0 for p in positions), "Some preflight steps missing"
        assert positions == sorted(positions), (
            f"Preflight steps must appear in canonical order {PREFLIGHT_STEPS}, "
            f"got positions {positions}. Order matters: Density → Conflict → "
            "Chronotype → Smart Proposal → Create with Validation."
        )


# ---------------------------------------------------------------------------
# Conflict Detection — must not overwrite + must propose alternatives
# ---------------------------------------------------------------------------


class TestConflictDetection:
    """Conflict step must explicitly forbid overwrite and require alternatives."""

    def test_conflict_step_forbids_overwrite(self, intelligence_text: str) -> None:
        # Anchored on "Conflict Detection" header for accurate scoping.
        match = re.search(
            r"\*\*Conflict Detection\*\*(.*?)(?=^\d+\.\s+\*\*|\Z)",
            intelligence_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match, "Conflict Detection step not found as `**Conflict Detection**`"
        body = match.group(1)
        assert "не перезапис" in body.lower() or "не перезапис" in body, (
            "Conflict Detection must explicitly say «не перезаписывай» — "
            "without it, the skill could clobber a user's existing event."
        )

    def test_conflict_step_requires_alternative_slots(
        self, intelligence_text: str
    ) -> None:
        match = re.search(
            r"\*\*Conflict Detection\*\*(.*?)(?=^\d+\.\s+\*\*|\Z)",
            intelligence_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match
        body = match.group(1)
        # «Предложи 2–3 альтернативных слота» — exact phrase or close variant
        assert re.search(r"альтернативн", body, re.IGNORECASE), (
            "Conflict Detection must propose alternative slots («альтернативных "
            "слота»). Just blocking the create is not enough — user needs a way "
            "forward."
        )


# ---------------------------------------------------------------------------
# Workload Warning Thresholds (6h / 8h boundaries)
# ---------------------------------------------------------------------------


class TestWorkloadWarnings:
    """Workload thresholds and supportive messaging."""

    def test_workload_section_present(self, intelligence_text: str) -> None:
        assert "Workload Warning Thresholds" in intelligence_text, (
            "calendar_intelligence.md must have `## Workload Warning Thresholds` "
            "section."
        )

    @pytest.mark.parametrize("threshold", ["6", "8"])
    def test_workload_thresholds_documented(
        self, intelligence_text: str, threshold: str
    ) -> None:
        """Both 6h and 8h thresholds must appear in workload section."""
        match = re.search(
            r"## Workload Warning Thresholds(.*?)(?=^## |\Z)",
            intelligence_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match, "Workload section missing"
        body = match.group(1)
        # Threshold appears in patterns like "6ч", "6-8ч", "≤6ч", ">8ч"
        assert re.search(rf"{threshold}\s*ч", body), (
            f"Workload section must reference {threshold}h threshold — "
            "this is the boundary between «normal» / «risk» / «high» load."
        )

    def test_work_hours_configurable(self, intelligence_text: str) -> None:
        """Work hours must be documented as user-configurable, not hardcoded."""
        assert re.search(
            r"настраивают[а-я]+ пользовател", intelligence_text, re.IGNORECASE
        ), (
            "Work Hours must be documented as user-configurable («настраиваются "
            "пользователем»). Hardcoded 9–18 would alienate shift workers, "
            "night owls, parents, students."
        )


# ---------------------------------------------------------------------------
# Calendar Pattern Analyzer — read-only safety contract
# ---------------------------------------------------------------------------


class TestPatternAnalyzerSafety:
    """Pattern Analyzer must be read-only with explicit consent."""

    def test_read_only_protocol_section(self, pattern_analyzer_text: str) -> None:
        assert "## Read-Only Protocol" in pattern_analyzer_text, (
            "calendar_pattern_analyzer.md must declare `## Read-Only Protocol`. "
            "Pattern analysis reads user data and must never write."
        )

    def test_only_list_events_allowed(self, pattern_analyzer_text: str) -> None:
        """Only `list_events` tool may be used — explicitly stated."""
        match = re.search(
            r"## Read-Only Protocol(.*?)(?=^## |\Z)",
            pattern_analyzer_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match
        body = match.group(1)
        assert "list_events" in body, (
            "Read-Only Protocol must explicitly name `list_events` as the "
            "permitted tool."
        )

    def test_write_tools_forbidden(self, pattern_analyzer_text: str) -> None:
        """Write tools must be explicitly forbidden."""
        match = re.search(
            r"## Read-Only Protocol(.*?)(?=^## |\Z)",
            pattern_analyzer_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match
        body = match.group(1)
        for forbidden_tool in ("create_event", "delete_event", "update_event"):
            assert forbidden_tool in body, (
                f"Read-Only Protocol must explicitly list `{forbidden_tool}` "
                "as NOT used. Naming forbidden tools beats vague «no writes»."
            )

    def test_consent_section_present(self, pattern_analyzer_text: str) -> None:
        """Explicit consent flow must be documented."""
        assert "## Security & Permissions" in pattern_analyzer_text, (
            "calendar_pattern_analyzer.md must have `## Security & Permissions` "
            "section describing consent flow."
        )
        # The canonical consent phrase
        assert "Проанализирую ваш календарь" in pattern_analyzer_text, (
            "Consent phrase «Проанализирую ваш календарь...» must be present "
            "verbatim — analyzers don't run without user OK each time."
        )

    def test_no_inter_session_caching(self, pattern_analyzer_text: str) -> None:
        """Event data must not be cached between sessions."""
        assert re.search(
            r"не\s+кэширу", pattern_analyzer_text, re.IGNORECASE
        ), (
            "Pattern analyzer must document that event data is NOT cached "
            "between sessions («данные событий не кэшируются»). Privacy guard."
        )


# ---------------------------------------------------------------------------
# Pattern Analyzer Metrics — 5 documented metrics with formulas + thresholds
# ---------------------------------------------------------------------------


REQUIRED_METRICS = [
    "Meeting Load",
    "Focus Time",
    "Boundary Violation",
    "Recovery Deficit",
    "Chronotype Alignment",
]


class TestPatternAnalyzerMetrics:
    """All 5 metrics must be documented with formula + threshold + insight."""

    def test_metrics_section_present(self, pattern_analyzer_text: str) -> None:
        assert "## Metrics" in pattern_analyzer_text, (
            "calendar_pattern_analyzer.md must have `## Metrics` section."
        )

    @pytest.mark.parametrize("metric", REQUIRED_METRICS)
    def test_each_metric_listed(self, pattern_analyzer_text: str, metric: str) -> None:
        assert metric in pattern_analyzer_text, (
            f"Pattern Analyzer must document `{metric}` metric. "
            "Dropping a metric silently loses observability for that pattern."
        )

    def test_metrics_table_has_all_columns(self, pattern_analyzer_text: str) -> None:
        """Metrics table must include Formula / Threshold / Insight columns."""
        match = re.search(
            r"## Metrics(.*?)(?=^## |\Z)",
            pattern_analyzer_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match, "Metrics section missing"
        body = match.group(1)
        for column_header in ("Formula", "Threshold", "Conversational Insight"):
            assert column_header in body, (
                f"Metrics table must have `{column_header}` column — without "
                "it, a metric is just a name without operational meaning."
            )


# ---------------------------------------------------------------------------
# Pattern Analyzer cadence & data-window constraints
# ---------------------------------------------------------------------------


class TestPatternAnalyzerCadence:
    """Rate limits and data-window minimums guard against noisy advice."""

    def test_default_rate_limit_documented(self, pattern_analyzer_text: str) -> None:
        """Default cadence must be documented as «1 analysis per week»."""
        match = re.search(
            r"## Rate Limits(.*?)(?=^## |\Z)",
            pattern_analyzer_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match, "calendar_pattern_analyzer.md must have `## Rate Limits` section"
        body = match.group(1)
        assert re.search(r"1\s+анализ\s+в\s+неделю", body), (
            "Rate Limits must default to «1 анализ в неделю» — daily analysis "
            "creates anxiety / surveillance feel without signal value."
        )

    def test_minimum_data_window_for_trends(
        self, pattern_analyzer_text: str
    ) -> None:
        """3 weeks minimum for trend talk must be explicit."""
        match = re.search(
            r"## Weekly Trends(.*?)(?=^## |\Z)",
            pattern_analyzer_text,
            re.DOTALL | re.MULTILINE,
        )
        assert match, "calendar_pattern_analyzer.md must have `## Weekly Trends` section"
        body = match.group(1)
        assert re.search(r"3\s+недел", body), (
            "Weekly Trends must require minimum 3 weeks of data before talking "
            "patterns. With < 3 weeks the analyzer must hedge (snapshot / "
            "cautious comparison), not assert trends."
        )


# ---------------------------------------------------------------------------
# Anti-patterns — explicit "what NOT to do" list
# ---------------------------------------------------------------------------


class TestPatternAnalyzerAntiPatterns:
    """`## Anti-Patterns` enumerates UX traps the analyzer must avoid."""

    def test_anti_patterns_section_present(
        self, pattern_analyzer_text: str
    ) -> None:
        assert re.search(
            r"## Anti-Patterns", pattern_analyzer_text
        ), (
            "calendar_pattern_analyzer.md must have `## Anti-Patterns` section "
            "documenting what NOT to do. Most analyzer regressions are «added "
            "a productivity score», not «forgot a metric»."
        )

    def test_no_productivity_score(self, pattern_analyzer_text: str) -> None:
        assert "продуктивный скор" in pattern_analyzer_text or "продуктивный рейтинг" in pattern_analyzer_text, (
            "Anti-Patterns must forbid productivity score/rating wording. "
            "Quantifying user time as a «score» creates anxiety, not insight."
        )

    def test_no_user_comparison(self, pattern_analyzer_text: str) -> None:
        assert re.search(
            r"не\s+сравнивать\s+с\s+другими\s+пользовател",
            pattern_analyzer_text,
            re.IGNORECASE,
        ), (
            "Anti-Patterns must forbid comparison with other users. Social "
            "comparison damages autonomy support (SDT) — opposite of skill goal."
        )

    def test_no_automatic_reschedule(self, pattern_analyzer_text: str) -> None:
        assert re.search(
            r"не\s+переносить\s+встречи\s+автоматически",
            pattern_analyzer_text,
            re.IGNORECASE,
        ), (
            "Anti-Patterns must forbid automatic rescheduling without consent. "
            "Read-only contract + user owns the calendar — analyzer suggests, "
            "user decides."
        )
