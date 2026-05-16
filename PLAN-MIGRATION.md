# Plan: Migrate to Official Google Calendar MCP (Zero-Setup)

> **Branch**: `feature/mcp-experiment`  
> **Strategy**: Official Calendar MCP (built-in, zero-setup) + preserve domain logic + Tasks → text lists  
> **Decision basis**: Gates 3, 5, 5b completed. User chose: Option 2 + zero-setup + no Tasks.

---

## 1. Philosophy

**What we KEEP** (~1477 lines of domain logic):
- COLOR_MAP, REMINDER_PRESETS, RRULE constants → used in MCP prompts
- Preset logic (Weekly Review, WOOP, Milestone, Time Block) → converted to prompt templates
- Free-slot algorithm → embedded in SKILL.md as reasoning instructions
- Conversation state models (state.py) → unchanged, JSON still valid
- Data models (CalendarEvent, TimeSlot) → reference for MCP output parsing

**What we DELETE** (~2593 lines of infrastructure):
- `auth.py` — OAuth, Fernet, token refresh (all replaced by MCP OAuth)
- `tasks_manager.py` — Google Tasks API (no MCP equivalent)
- `calendar_manager.py` — HTTP calls, retry, API serialization
- `requirements.txt` — google-api-python-client, google-auth, cryptography
- `example_usage.py` — outdated Python examples

**What we REWRITE**:
- `SKILL.md` Stage 5 — Python API → MCP tool calls
- `references/calendar_integration.md` — architecture docs → MCP prompt reference

---

## 2. New Architecture

```
SKILL.md (Claude skill)
├── Stage 1-4: Unchanged
└── Stage 5: Google Calendar via MCP
    ├── MCP Tools (official, zero-setup):
    │   ├── create_event  → for presets, time blocks, milestones
    │   ├── update_event  → modify existing
    │   ├── delete_event  → remove
    │   ├── get_event     → single event lookup
    │   ├── list_events   → read calendar (free slot analysis)
    │   ├── list_calendars→ multi-calendar support
    │   ├── respond_to_event → RSVP
    │   └── suggest_time  → alternative to free-slot algo
    ├── Domain Logic (in prompt):
    │   ├── COLOR_MAP → passed as colorId in create_event
    │   ├── REMINDER_PRESETS → passed as reminders JSON
    │   ├── RRULE → passed as recurrence array
    │   ├── Weekly Review preset → prompt template
    │   ├── WOOP preset → prompt template
    │   ├── Milestone preset → prompt template
    │   └── Time Block preset → prompt template
    └── Daily Top-3 → Conversation state only (text list)
```

---

## 3. File-by-File Changes

### 3.1 DELETE (complete removal)

| File | Lines | Reason |
|------|-------|--------|
| `calendar_integration/auth.py` | 675 | OAuth + Fernet + retry — all handled by MCP |
| `calendar_integration/tasks_manager.py` | 844 | Tasks API not in official MCP; Daily Top-3 → text |
| `calendar_integration/example_usage.py` | ~200 | Python examples no longer relevant |
| `calendar_integration/requirements.txt` | ~10 | google-api deps removed |

### 3.2 KEEP (domain logic preserved)

| File | Lines | What stays | What goes |
|------|-------|------------|-----------|
| `calendar_integration/config.py` | 252 | COLOR_MAP, REMINDER_PRESETS, RRULE, CalendarConfig | Scopes, GOOGLE_TOKEN_URI, retry constants |
| `calendar_integration/models.py` | 406 | CalendarEvent, TimeSlot (as data structures) | to_api_body(), from_api_response() — no API calls |
| `calendar_integration/state.py` | 206 | Conversation state (unchanged) | — |

### 3.3 REWRITE

| File | Action |
|------|--------|
| `SKILL.md` Stage 5 | Replace Python API with MCP tool calls + domain prompt templates |
| `references/calendar_integration.md` | Replace architecture with MCP tool reference + prompt patterns |
| `setup.py` | Remove google-api dependencies, keep package metadata |

---

## 4. SKILL.md Stage 5 — New Specification

### 4.1 MCP Connector Setup (for user)

```markdown
### Stage 5: Google Calendar Integration (via MCP)

**Zero-setup**: Official Google Calendar MCP is pre-installed in claude.ai.
User connects once via Settings → MCP → Google Calendar → Authorize.
No credentials.json, no encryption key, no Python environment needed.

**Available MCP tools**:
- `create_event` — Create calendar events (supports recurrence)
- `update_event` — Modify events
- `delete_event` — Remove events
- `get_event` — Read single event
- `list_events` — Query events by date range
- `list_calendars` — Discover user's calendars
- `respond_to_event` — RSVP to invitations
- `suggest_time` — Find meeting times (alternative to free-slot algo)
```

### 4.2 Domain Prompt Templates

Each preset becomes a structured prompt template in SKILL.md:

**Weekly Review Reminder**:
```
When user asks for Weekly Review reminder:
1. Determine next Sunday at {hour}:{minute} in user's timezone
2. Call create_event with:
   - summary: "Weekly Review"
   - description: "1. Что прошло хорошо?\n2. Что можно улучшить?\n3. Какие уроки?\n4. Приоритеты на неделю"
   - start/end: Sunday {hour}:{minute} for 30 min
   - colorId: 5 (Banana yellow = weekly_review)
   - reminders: [{"method":"popup","minutes":60},{"method":"popup","minutes":15}]
   - recurrence: ["RRULE:FREQ=WEEKLY;BYDAY=SU"]
```

**WOOP Reminder**:
```
When user asks for WOOP reminder:
1. Determine tomorrow at {hour}:{minute} in user's timezone
2. Call create_event with:
   - summary: "WOOP Сессия"
   - description: "Wish — Какое желание?\nOutcome — Лучший результат?\nObstacle — Главное препятствие?\nPlan — Если X, то Y"
   - start/end: Tomorrow {hour}:{minute} for 15 min
   - colorId: 7 (Peacock blue = woop)
   - reminders: [{"method":"popup","minutes":5}]
   - recurrence: ["RRULE:FREQ=DAILY"]
```

**Time Block**:
```
When user asks to block time for deep work:
1. Ask: title, date, start time, duration, type (deep_work/exercise/family/etc.)
2. Determine colorId from COLOR_MAP
3. Call create_event with appropriate reminders from REMINDER_PRESETS
```

**Free Slots Analysis**:
```
When user asks "when am I free?":
1. Call list_events for target date range
2. Apply free-slot algorithm (defined in prompt):
   - Define work hours window (default 9-18)
   - Extract busy intervals from events
   - Merge overlapping busy slots
   - Find gaps >= requested duration
3. Present top 3 options to user
```

### 4.3 Daily Top-3 (Text-Only)

```markdown
### Daily Top-3 (Conversation State)

Since Google Tasks API is not available via official MCP,
Daily Top-3 is stored in conversation state as text list.

**Workflow**:
1. User agrees on 3 priorities for today
2. Store in state: `goals.daily_top3 = ["...", "...", "..."]`
3. Present as formatted list with checkboxes
4. On next session, ask for completion status
5. Archive to `weekly_reviews` for tracking

**No sync to Google Tasks** — purely conversational feature.
```

---

## 5. Reference: COLOR_MAP for MCP

| Type | colorId | Color | Usage |
|------|---------|-------|-------|
| deep_work | 2 | Sage green | Focus work blocks |
| woop | 7 | Peacock blue | WOOP sessions |
| weekly_review | 5 | Banana yellow | Weekly retrospectives |
| family | 1 | Lavender purple | Family/personal time |
| exercise | 6 | Tangerine orange | Sport/health |
| reading | 4 | Flamingo pink | Learning/reading |
| urgent | 11 | Tomato red | Deadlines/milestones |
| personal | 3 | Grape | Personal tasks |
| meeting | 9 | Blueberry | Meetings |
| planning | 10 | Basil | Planning sessions |
| default | 8 | Graphite | Fallback |

---

## 6. Reference: REMINDER_PRESETS for MCP

| Preset | Reminders JSON |
|--------|----------------|
| default | `[{"method":"popup","minutes":15}]` |
| weekly_review | `[{"method":"popup","minutes":60},{"method":"popup","minutes":15}]` |
| woop | `[{"method":"popup","minutes":5}]` |
| milestone | `[{"method":"popup","minutes":1440},{"method":"popup","minutes":60}]` |
| deep_work | `[{"method":"popup","minutes":5}]` |
| exercise | `[{"method":"popup","minutes":30}]` |
| urgent | `[{"method":"popup","minutes":60},{"method":"popup","minutes":15},{"method":"popup","minutes":0}]` |

---

## 7. Reference: RRULE for MCP

| Pattern | RRULE | Usage |
|---------|-------|-------|
| Weekly (Sunday) | `["RRULE:FREQ=WEEKLY;BYDAY=SU"]` | Weekly Review |
| Daily | `["RRULE:FREQ=DAILY"]` | WOOP sessions |
| Weekdays | `["RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"]` | Work blocks |

---

## 8. Execution Steps

### Phase 1: Clean up (delete infrastructure)
1. `git rm calendar_integration/auth.py`
2. `git rm calendar_integration/tasks_manager.py`
3. `git rm calendar_integration/example_usage.py`
4. `git rm calendar_integration/requirements.txt`
5. `git rm calendar_integration/exceptions.py` (or simplify to minimal)
6. Update `setup.py` — remove google-api deps
7. Update `calendar_integration/__init__.py` — remove auth/tasks imports

### Phase 2: Trim domain files
8. `config.py` — remove GOOGLE_TOKEN_URI, scopes, retry constants; keep COLOR_MAP, REMINDER_PRESETS, RRULE
9. `models.py` — remove `to_api_body()` and `from_api_response()` methods; keep dataclass definitions as data structures

### Phase 3: Rewrite SKILL.md
10. Rewrite Stage 5 section (lines 255-285) with MCP tool calls
11. Add `requires_mcp: "google-calendar"` to frontmatter
12. Add MCP setup instructions

### Phase 4: Rewrite reference docs
13. Rewrite `references/calendar_integration.md` — replace Python architecture with MCP prompt patterns

### Phase 5: Commit
14. Commit all changes with message: "migrate: replace Python Calendar API with official MCP"

---

## 9. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Official MCP doesn't support write scopes | Use `list_events` for read-only fallback; document limitation |
| Recurrence (RRULE) not supported by MCP | Fall back to creating individual weekly events via script |
| MCP unavailable (user not connected) | SKILL.md includes graceful degradation: "Calendar недоступен. Продолжим без синхронизации?" |
| User wants Tasks back later | Keep `tasks_manager.py` in git history; can restore from `main` |

---

## 10. Size Impact

| Metric | Before | After | Δ |
|--------|--------|-------|---|
| Python files | 4070 lines | ~900 lines (domain only) | **-78%** |
| Dependencies | google-api, auth, cryptography | None (MCP built-in) | **-100%** |
| Setup complexity | credentials.json + OAuth + env var | One-click in claude.ai | **Minimal** |
| Skill size (.zip) | Larger | Significantly smaller | **~70% reduction** |

---

## 11. Open Questions (for user)

1. **Should we keep `calendar_manager.py` skeleton?** Or delete entirely since MCP handles all CRUD?
   - *Recommendation*: Delete. MCP tools + prompt templates replace it.

2. **Should `models.py` stay as Python dataclasses?** Or convert to JSON schemas in SKILL.md?
   - *Recommendation*: Keep as lightweight dataclasses for potential future use; remove API serialization.

3. **Should we create a `domain/` folder** for preserved logic (COLOR_MAP, RRULE) separate from `calendar_integration/`?
   - *Recommendation*: Yes — `domain/calendar_presets.py` with pure data; delete `calendar_integration/` package entirely.

---

## 12. Go/No-Go Checklist

- [ ] User approves this plan
- [ ] User confirms: no need for Tasks API (text-only Daily Top-3 OK)
- [ ] User confirms: official MCP write scopes acceptable (or read-only fallback OK)
- [ ] Execute Phase 1-5
- [ ] Test: `list_events` via MCP in claude.ai (validate connector works)
- [ ] Test: `create_event` with colorId and recurrence
- [ ] Commit and merge to `main`
