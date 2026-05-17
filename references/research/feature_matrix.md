# Feature Matrix: Python Module vs MCP

**Gate 5: Domain Logic Mapping**  
*Project: life-planning-coach*  
*Scope: `calendar_integration/` Python module vs Google Calendar MCP server*

---

## Methodology

- **Domain Logic** = business rules, life-planning abstractions, algorithms, and presets that encode the *skill's* knowledge. NOT infrastructure (OAuth, HTTP, retry, encryption, raw API mapping).
- **MCP Tool** = hypothetical or actual tool exposed by a Google Calendar MCP server.
- **Status**:
  - `Replaceable` → thin wrapper around API; MCP tool can do it directly.
  - `Partial` → MCP can do the API call, but Python layer adds validation, defaults, or domain-specific mapping that must be preserved.
  - `Lost` → pure domain logic with no MCP equivalent; would need to be re-implemented in prompts or a new middleware layer.

---

## CalendarManager (`calendar_manager.py`, 1051 lines)

| Method | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| `__init__` | 10 | 0 | N/A | Replaceable |
| `_get_service` | 13 | 0 | N/A | Replaceable |
| `_parse_event_response` | 3 | 0 | N/A | Replaceable |
| `_execute_api_call` | 15 | 0 | N/A | Replaceable |
| `get_events` | 71 | 6 | `calendar_list_events` | Partial |
| `get_event` | 32 | 0 | `calendar_get_event` | Replaceable |
| `create_event` | 88 | 13 | `calendar_create_event` | Partial |
| `update_event` | 66 | 8 | `calendar_update_event` | Partial |
| `delete_event` | 32 | 0 | `calendar_delete_event` | Replaceable |
| `get_free_slots` | 94 | 14 | `calendar_query_freebusy` | Partial |
| `_find_free_intervals` | 54 | 54 | N/A | **Lost** |
| `create_weekly_review_reminder` | 60 | 60 | N/A | **Lost** |
| `create_woop_reminder` | 53 | 53 | N/A | **Lost** |
| `create_milestone_event` | 54 | 54 | N/A | **Lost** |
| `create_time_block` | 54 | 54 | N/A | **Lost** |
| `create_recurring_event` | 47 | 1 | `calendar_create_event` | Partial |
| `get_event_instances` | 34 | 0 | `calendar_get_event_instances` | Replaceable |
| `delete_event_series` | 12 | 0 | `calendar_delete_event` | Replaceable |
| `get_available_colors` | 25 | 0 | `calendar_get_colors` | Replaceable |
| `get_calendar_list` | 29 | 0 | `calendar_list_calendars` | Replaceable |
| `search_events` | 19 | 2 | `calendar_search_events` | Partial |
| `_handle_http_error` | 56 | 0 | N/A | Replaceable |

### CalendarManager Summary
- **Total lines:** 1051
- **Domain logic lines:** ~311
- **Replaceable by MCP:** ~740
- **Lost without replacement:** ~275 (pure domain algorithms + presets)

---

## TasksManager (`tasks_manager.py`, 844 lines)

| Method | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| `__init__` | 10 | 0 | N/A | Replaceable |
| `_get_service` | 10 | 0 | N/A | Replaceable |
| `_parse_task_response` | 3 | 0 | N/A | Replaceable |
| `_execute_api_call` | 7 | 0 | N/A | Replaceable |
| `get_tasks` | 63 | 2 | `tasks_list` | Partial |
| `get_task` | 32 | 0 | `tasks_get` | Replaceable |
| `create_task` | 60 | 4 | `tasks_create` | Partial |
| `update_task` | 53 | 8 | `tasks_update` | Partial |
| `complete_task` | 40 | 2 | `tasks_update` | Partial |
| `uncomplete_task` | 17 | 0 | `tasks_update` | Replaceable |
| `delete_task` | 28 | 0 | `tasks_delete` | Replaceable |
| `get_task_lists` | 21 | 0 | `tasks_list_lists` | Replaceable |
| `create_tasklist` | 26 | 0 | `tasks_create_list` | Replaceable |
| `get_or_create_tasklist` | 18 | 18 | N/A | **Lost** |
| `delete_tasklist` | 18 | 0 | `tasks_delete_list` | Replaceable |
| `create_tasks_batch` | 32 | 32 | N/A | **Lost** |
| `create_task_with_subtasks` | 47 | 47 | N/A | **Lost** |
| `clear_completed` | 31 | 31 | N/A | **Lost** |
| `create_daily_top3` | 74 | 74 | N/A | **Lost** |
| `create_weekly_goal_tasks` | 35 | 35 | N/A | **Lost** |
| `create_12week_goal_task` | 49 | 49 | N/A | **Lost** |
| `_format_due_date` | 14 | 0 | N/A | Replaceable |
| `_handle_http_error` | 44 | 0 | N/A | Replaceable |

### TasksManager Summary
- **Total lines:** 844
- **Domain logic lines:** ~302
- **Replaceable by MCP:** ~542
- **Lost without replacement:** ~286 (hierarchical tasks, batch ops, life-planning presets)

---

## Auth Layer (`auth.py`, 675 lines)

| Symbol | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| `SecureTokenStorage` (class + methods) | 144 | 0 | N/A | Replaceable |
| `require_auth` (decorator) | 22 | 0 | N/A | Replaceable |
| `CalendarAuth` (class + methods) | 259 | 0 | N/A | Replaceable |
| `with_retry` (decorator) | 113 | 0 | N/A | Replaceable |
| Module-level imports / whitespace | 137 | 0 | N/A | Replaceable |

### Auth Layer Summary
- **Total lines:** 675
- **Domain logic lines:** 0
- **Replaceable by MCP:** 675 (MCP handles auth internally; Fernet encryption becomes unnecessary)
- **Lost without replacement:** 0

---

## Configuration (`config.py`, 252 lines)

| Symbol | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| `_GOOGLE_EVENT_COLORS` | 13 | 13 | N/A | **Lost** |
| `COLOR_MAP` | 13 | 13 | N/A | **Lost** |
| `COLOR_NAME_BY_ID` | 3 | 3 | N/A | **Lost** |
| `REMINDER_PRESETS` | 29 | 29 | N/A | **Lost** |
| `DEFAULT_*` constants | 8 | 8 | N/A | **Lost** |
| `MAX_RETRIES`, `BASE_RETRY_DELAY`, etc. | 5 | 0 | N/A | Replaceable |
| `DEFAULT_SCOPES` / `MINIMAL_SCOPES` | 9 | 0 | N/A | Replaceable |
| `WOOP_RRULE` | 1 | 1 | N/A | **Lost** |
| `WEEKLY_REVIEW_RRULE` | 1 | 1 | N/A | **Lost** |
| `CalendarConfig` (dataclass + methods) | 106 | 106 | N/A | **Lost** |
| Imports / docstring | 54 | 54 | N/A | **Lost** |

### Config Summary
- **Total lines:** 252
- **Domain logic lines:** ~252
- **Replaceable by MCP:** 0
- **Lost without replacement:** ~252 (all color presets, reminder presets, RRULEs, and config class are pure domain knowledge)

---

## Data Models (`models.py`, 406 lines)

| Symbol | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| `Reminder` | 40 | 40 | N/A | **Lost** |
| `CalendarEvent` | 137 | 137 | N/A | **Lost** |
| `CalendarTask` | 94 | 94 | N/A | **Lost** |
| `TimeSlot` | 68 | 68 | N/A | **Lost** |
| `FreeBusyWindow` | 35 | 35 | N/A | **Lost** |
| Imports / module docstring | 32 | 32 | N/A | **Lost** |

### Models Summary
- **Total lines:** 406
- **Domain logic lines:** ~406
- **Replaceable by MCP:** 0
- **Lost without replacement:** ~406 (MCP returns raw JSON; typed models with validation, duration calculation, slot arithmetic, and API serialization are all domain layer)

---

## Conversation State (`state.py`, 206 lines)

| Symbol | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| `LifeWheel` | 12 | 12 | N/A | **Lost** |
| `Values` | 14 | 14 | N/A | **Lost** |
| `OKRTheme` | 5 | 5 | N/A | **Lost** |
| `TwelveWeek` | 5 | 5 | N/A | **Lost** |
| `WOOP` | 7 | 7 | N/A | **Lost** |
| `Goals` | 8 | 8 | N/A | **Lost** |
| `WeeklyReview` | 10 | 10 | N/A | **Lost** |
| `ConversationState` | 116 | 116 | N/A | **Lost** |
| Imports / docstring | 29 | 29 | N/A | **Lost** |

### State Summary
- **Total lines:** 206
- **Domain logic lines:** ~206
- **Replaceable by MCP:** 0
- **Lost without replacement:** ~206 (pure skill state; unrelated to Calendar API but part of the module)

---

## Exceptions (`exceptions.py`, 239 lines)

| Symbol | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| `CalendarError` hierarchy | 239 | 0 | N/A | Replaceable |

### Exceptions Summary
- **Total lines:** 239
- **Domain logic lines:** 0
- **Replaceable by MCP:** 239 (MCP returns its own error schema)
- **Lost without replacement:** 0

---

## Example Usage (`example_usage.py`, 311 lines)

| Symbol | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| `example_initialization` | 36 | 0 | N/A | Replaceable |
| `example_weekly_review` | 24 | 0 | N/A | Replaceable |
| `example_woop_reminder` | 24 | 0 | N/A | Replaceable |
| `example_read_week_events` | 35 | 0 | N/A | Replaceable |
| `example_daily_top3` | 30 | 0 | N/A | Replaceable |
| `example_find_free_slots` | 35 | 0 | N/A | Replaceable |
| `example_time_block` | 27 | 0 | N/A | Replaceable |
| `main` | 28 | 0 | N/A | Replaceable |
| Imports / boilerplate | 72 | 0 | N/A | Replaceable |

### Example Usage Summary
- **Total lines:** 311
- **Domain logic lines:** 0
- **Replaceable by MCP:** 311
- **Lost without replacement:** 0

---

## Module Exports (`__init__.py`, 86 lines)

| Symbol | Lines | Domain Logic | MCP Tool | Status |
|--------|-------|--------------|----------|--------|
| Imports / `__all__` | 86 | 0 | N/A | Replaceable |

---

## Global Summary

| Metric | Value |
|--------|-------|
| **Total Python lines** | 4070 |
| **Domain logic lines (non-MCP)** | ~1477 |
| **Infrastructure / replaceable by MCP** | ~2593 |
| **Lost without replacement** | ~1477 |

### Breakdown by File

| File | Total | Domain | Replaceable | Lost |
|------|-------|--------|-------------|------|
| `calendar_manager.py` | 1051 | ~311 | ~740 | ~275 |
| `tasks_manager.py` | 844 | ~302 | ~542 | ~286 |
| `auth.py` | 675 | 0 | 675 | 0 |
| `config.py` | 252 | ~252 | 0 | ~252 |
| `models.py` | 406 | ~406 | 0 | ~406 |
| `state.py` | 206 | ~206 | 0 | ~206 |
| `exceptions.py` | 239 | 0 | 239 | 0 |
| `example_usage.py` | 311 | 0 | 311 | 0 |
| `__init__.py` | 86 | 0 | 86 | 0 |
| **TOTAL** | **4070** | **~1477** | **~2593** | **~1477** |

---

## What Cannot Be Replaced by MCP (Detailed)

### 1. Free-Slot Algorithm (`_find_free_intervals`, 54 lines)
- Merges overlapping busy intervals.
- Computes gaps between merged busy slots.
- Filters gaps by minimum duration.
- **Why lost:** MCP can return `freebusy` raw data, but the *algorithm* to turn that into user-facing "free slots" is pure business logic.

### 2. Life-Planning Event Presets (~221 lines across 4 methods)
- **`create_weekly_review_reminder`**: Computes next Sunday, sets 19:00, injects 4-step retrospective template, uses `COLOR_MAP["weekly_review"]` + `REMINDER_PRESETS["weekly_review"]` + `WEEKLY_REVIEW_RRULE`.
- **`create_woop_reminder`**: Computes tomorrow 07:00, injects WOOP (Wish-Outcome-Obstacle-Plan) template, uses `COLOR_MAP["woop"]` + `REMINDER_PRESETS["woop"]` + `WOOP_RRULE`.
- **`create_milestone_event`**: Calculates `advance_reminder_days` into minutes, uses urgent color, formats title as `Milestone: {title}`.
- **`create_time_block`**: Maps semantic color names (`deep_work`, `exercise`) to Google color IDs and reminder presets; converts `duration` → `end` datetime.
- **Why lost:** MCP tools are generic; they do not encode life-coaching semantics, templates, or color psychology.

### 3. Hierarchical Task Operations (~126 lines across 3 methods)
- **`create_task_with_subtasks`**: Parent creation → subtask creation with `parent` linkage.
- **`create_daily_top3`**: Parent task `Top-3 [date]` → numbered emoji subtasks (`1️⃣`, `2️⃣`, `3️⃣`). Validates 1–10 priorities.
- **`create_12week_goal_task`**: Prefixes title with `12W:`, links subtasks under parent.
- **Why lost:** Google Tasks API supports `parent`, but the *orchestration* of parent→child batches with semantic naming is domain logic.

### 4. Batch & Maintenance Operations (~63 lines across 2 methods)
- **`create_tasks_batch`**: Sequential batch with per-item error handling.
- **`clear_completed`**: Fetch all → filter `is_completed()` → delete loop with error tolerance.
- **`get_or_create_tasklist`**: Lookup by title, create-on-miss.
- **Why lost:** MCP may expose single-item tools; batch orchestration and maintenance workflows must be built on top.

### 5. Configuration & Data Models (~864 lines)
- **`COLOR_MAP`**: Semantic life-planning colors (deep_work = Sage green, weekly_review = Banana yellow).
- **`REMINDER_PRESETS`**: Life-contextual reminder timings (WOOP = 5 min popup, milestone = 1 day + 1 hour).
- **`RRULE` presets**: `WOOP_RRULE` (daily), `WEEKLY_REVIEW_RRULE` (weekly on Sunday).
- **`CalendarConfig`**: Centralized domain config with color/reminder resolution.
- **`CalendarEvent` / `CalendarTask` / `TimeSlot`**: Typed models with validation, duration math, timezone handling, and Google-API serialization/deserialization.
- **Why lost:** MCP works over raw API schemas. All typed wrappers, validation, and domain-specific constants must exist somewhere else (prompts or a new layer).

### 6. Conversation State (`state.py`, 206 lines)
- `LifeWheel`, `Values`, `Goals`, `WeeklyReview`, `ConversationState`.
- **Why lost:** Entirely unrelated to Calendar API; pure skill state management. Would need equivalent Pydantic/json-schema layer in any rewrite.

---

## Conclusion

- **~64%** of the Python module (2593 / 4070 lines) is infrastructure that an MCP server could absorb.
- **~36%** (1477 / 4070 lines) is **domain logic that would be lost** in a naive MCP migration.
- The highest-value losses are:
  1. **Free-slot algorithm** (time-planning intelligence)
  2. **Life-planning presets** (WOOP, Weekly Review, Time Blocks with semantic colors)
  3. **Hierarchical task workflows** (Daily Top-3, 12-Week Goals)
  4. **Typed models & config** (type safety, validation, constants)

**Recommendation:** If migrating to MCP, preserve the **Config**, **Models**, **State**, and **Preset Methods** as a lightweight domain layer (e.g., a Pydantic-based SDK or prompt-embedded logic). Only replace the **Auth**, **HTTP transport**, **retry**, and **raw CRUD** layers with MCP tool calls.
