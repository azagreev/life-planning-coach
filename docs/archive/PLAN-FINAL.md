> **Архив:** Это исторический план миграции на MCP версии 0.2.0. Выполнен и заменён актуальной реализацией. Сохранён для контекста.

# FINAL PLAN: Migrate to Official Google Calendar MCP

> **Status**: Completed (archived)  
> **Branch**: `feature/mcp-experiment` → eventual merge to `main`  
> **Approach**: Official Calendar MCP (zero-setup) + domain logic as prompt constants

---

## 1. Final Project Structure (after migration)

```
life-planning-coach/
├── .git/
├── references/
│   ├── diagnostic_methods.md      # unchanged
│   ├── dashboard_guide.md          # unchanged
│   ├── goal_architecture.md        # unchanged
│   ├── science_backing.md          # unchanged
│   ├── weekly_review.md            # unchanged
│   └── calendar_integration.md     # REWRITE: MCP reference + prompt patterns
├── .gitattributes
├── README.md                       # REWRITE: remove Python setup instructions
├── SKILL.md                        # REWRITE: Stage 5 → MCP + prompt constants
├── life-planning-dashboard.html    # unchanged
├── setup.py                        # REWRITE: remove all dependencies
├── PLAN.md                         # keep (investigation history)
├── PLAN-MIGRATION.md               # keep (migration plan)
└── PLAN-FINAL.md                   # this file

# DELETED:
# ├── calendar_integration/          # entire package removed
# │   ├── __init__.py
# │   ├── auth.py
# │   ├── calendar_manager.py
# │   ├── config.py
# │   ├── example_usage.py
# │   ├── exceptions.py
# │   ├── models.py
# │   ├── requirements.txt
# │   ├── state.py
# │   └── tasks_manager.py
```

---

## 2. What Changes in SKILL.md

### 2.1 Frontmatter change

```yaml
---
name: life-planning-coach
version: 0.2.0          # bump: breaking change
runtime: "claude.ai"
requires_mcp: "google-calendar"    # NEW: specifies required MCP connector
---
```

### 2.2 Stage 5 — Full New Text (replacement for lines 255-285)

```markdown
## Stage 5: Google Calendar Integration (via MCP)

### Prerequisites
- **Zero setup**: Official Google Calendar MCP is built into claude.ai.
- User connects via Settings → MCP → Google Calendar → Authorize (one click).
- No credentials.json, no encryption key, no Python environment needed.
- If MCP is unavailable or user declines: gracefully degrade to text-only planning.

### MCP Tools Available
| Tool | Purpose |
|------|---------|
| `list_calendars` | Discover user's calendars |
| `list_events` | Read events for a date range |
| `get_event` | Read single event details |
| `create_event` | Create new event (supports recurrence) |
| `update_event` | Modify existing event |
| `delete_event` | Remove event |
| `respond_to_event` | RSVP to invitations |
| `suggest_time` | Find available meeting slots |

### Calendar Constants (use in all MCP calls)

**COLOR_MAP** — Life Planning color scheme for Google Calendar:
```json
{
  "deep_work": "2",      // Sage green — focus work
  "woop": "7",           // Peacock blue — WOOP sessions
  "weekly_review": "5",  // Banana yellow — Weekly Review
  "family": "1",         // Lavender purple — family time
  "exercise": "6",       // Tangerine orange — sport/health
  "reading": "4",        // Flamingo pink — learning
  "urgent": "11",        // Tomato red — deadlines
  "personal": "3",       // Grape — personal tasks
  "meeting": "9",        // Blueberry — meetings
  "planning": "10",      // Basil — planning sessions
  "default": "8"         // Graphite — fallback
}
```

**REMINDER_PRESETS** — Pre-configured reminder sets:
```json
{
  "default":        [{"method": "popup", "minutes": 15}],
  "weekly_review":  [{"method": "popup", "minutes": 60}, {"method": "popup", "minutes": 15}],
  "woop":           [{"method": "popup", "minutes": 5}],
  "milestone":      [{"method": "popup", "minutes": 1440}, {"method": "popup", "minutes": 60}],
  "deep_work":      [{"method": "popup", "minutes": 5}],
  "exercise":       [{"method": "popup", "minutes": 30}],
  "urgent":         [{"method": "popup", "minutes": 60}, {"method": "popup", "minutes": 15}, {"method": "popup", "minutes": 0}]
}
```

**RRULE_PRESETS** — Recurrence patterns:
```json
{
  "weekly_sunday": ["RRULE:FREQ=WEEKLY;BYDAY=SU"],
  "daily":         ["RRULE:FREQ=DAILY"],
  "weekdays":      ["RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"]
}
```

### Preset: Weekly Review Reminder
When user requests a Weekly Review reminder:
1. Ask for preferred day/time (default: Sunday 19:00, user's timezone).
2. Call `create_event` with:
   - `summary`: "Weekly Review"
   - `description`: "Weekly Review — ретроспектива недели:\n1. Что прошло хорошо?\n2. Что можно улучшить?\n3. Какие уроки извлечены?\n4. Приоритеты на следующую неделю"
   - `start` / `end`: next Sunday at chosen time, 30 min duration
   - `colorId`: `COLOR_MAP["weekly_review"]` → "5"
   - `reminders`: `REMINDER_PRESETS["weekly_review"]`
   - `recurrence`: `RRULE_PRESETS["weekly_sunday"]`
3. Confirm to user: recurring event created, next occurrence date.

### Preset: WOOP Reminder
When user requests a WOOP session reminder:
1. Ask for preferred time (default: 07:00, user's timezone).
2. Call `create_event` with:
   - `summary`: "WOOP Сессия"
   - `description`: "WOOP-сессия (Wish, Outcome, Obstacle, Plan):\n1. Wish — Какое желание хочешь реализовать сегодня?\n2. Outcome — Какой лучший результат представляешь?\n3. Obstacle — Какое главное препятствие?\n4. Plan — Если X, то Y"
   - `start` / `end`: tomorrow at chosen time, 15 min duration
   - `colorId`: `COLOR_MAP["woop"]` → "7"
   - `reminders`: `REMINDER_PRESETS["woop"]`
   - `recurrence`: `RRULE_PRESETS["daily"]`
3. Confirm to user: recurring event created.

### Preset: Milestone Event
When user wants to mark a milestone (e.g., 12-Week Year goal):
1. Ask: title, target date/time, advance reminder (default: 7 days).
2. Call `create_event` with:
   - `summary`: `Milestone: {title}`
   - `start` / `end`: target date/time, 30 min duration
   - `colorId`: `COLOR_MAP["urgent"]` → "11"
   - `reminders`: `REMINDER_PRESETS["milestone"]`
3. Confirm: event created with advance reminder.

### Preset: Time Block
When user requests a time block for deep work or other activity:
1. Ask: title, date, start time, duration (minutes), activity type.
2. Determine `colorId` from `COLOR_MAP` (default: "deep_work" → "2").
3. Determine `reminders` from `REMINDER_PRESETS` by activity type (fallback: "default").
4. Call `create_event` with:
   - `summary`: `{title}`
   - `start` / `end`: computed from date + time + duration
   - `colorId`: from step 2
   - `reminders`: from step 3
5. Confirm: time block created.

### Free Slots Analysis
When user asks "when am I free?" or "find a slot":
1. Ask: target date, minimum duration, preferred work hours (default 9-18).
2. Call `list_events` for target date from 00:00 to 23:59.
3. Apply algorithm:
   - Define work window: `work_start` to `work_end`.
   - Extract busy intervals from returned events.
   - Sort busy intervals by start time.
   - Merge overlapping busy intervals.
   - Find gaps between busy intervals where `gap_duration >= requested_duration`.
   - Also check gap from `work_start` to first busy, and from last busy to `work_end`.
4. Present top 3 free slots to user with format: "Свободно: HH:MM–HH:MM (N минут)".
5. Alternative: use `suggest_time` if available from MCP.

### Daily Top-3 (Conversation State, No Sync)
Since Google Tasks API is not available via official MCP:
1. When user defines 3 daily priorities: store in conversation state.
2. Present as formatted text list with checkboxes (☐ / ☑).
3. On next session: ask completion status, archive to `weekly_reviews`.
4. No synchronization to Google Tasks — purely conversational feature.

### Event Data Schema (for parsing MCP responses)
```json
{
  "id": "string",
  "summary": "string (title)",
  "description": "string",
  "start": {"dateTime": "ISO-8601", "timeZone": "string"},
  "end": {"dateTime": "ISO-8601", "timeZone": "string"},
  "colorId": "string (1-11)",
  "reminders": {
    "useDefault": false,
    "overrides": [{"method": "popup|email", "minutes": int}]
  },
  "recurrence": ["RRULE:..."],
  "attendees": [{"email": "string"}],
  "htmlLink": "string (URL)",
  "status": "confirmed|tentative|cancelled"
}
```

### Failure Modes
| Scenario | Response |
|----------|----------|
| MCP not connected | "Для работы с календарём нужно подключить Google Calendar в настройках Claude. Продолжим без синхронизации?" |
| User declines OAuth | "Понял, будем работать без календаря. Все планы останутся в нашем разговоре." |
| Rate limit (429) | "Google Calendar временно недоступен из-за лимита запросов. Попробуем через минуту или продолжим без календаря?" |
| Permission denied (403) | "Недостаточно прав для изменения календаря. Проверьте доступ в настройках Google Calendar MCP." |
| Recurrence not supported | "Создам отдельные события на ближайшие 4 недели вместо повторяющегося." |
```

### 2.3 What stays unchanged in SKILL.md
- Stages 1-4 (Diagnostic, Goal Architecture, Weekly Review, Dashboard)
- Emotional Intelligence Backbone
- Conversation State JSON schema
- Progressive Disclosure Rules
- Safety & Ethics
- Data Export
- All references except `calendar_integration.md`

---

## 3. What Changes in Other Files

### 3.1 `setup.py` — New minimal version
```python
"""
Setup script for life-planning-coach skill.
"""
from setuptools import setup

setup(
    name="life-planning-coach",
    version="0.2.0",
    description="Evidence-based life planning coach for Claude",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/azagreev/life-planning-coach",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
)
```

### 3.2 `references/calendar_integration.md` — New reference
Replace the 2265-line architecture doc with a 200-line MCP reference:
- MCP tool descriptions
- JSON schemas for tool arguments
- COLOR_MAP, REMINDER_PRESETS, RRULE tables
- Prompt pattern examples
- Troubleshooting guide

### 3.3 `README.md` — Remove Python setup
Remove sections about:
- `credentials.json`
- `CALENDAR_ENCRYPTION_KEY`
- `pip install -r requirements.txt`
- Python API examples

Keep:
- Skill description
- Methodology overview
- Dashboard usage
- License

---

## 4. Acceptance Criteria (Definition of Done)

### 4.1 Structure
- [ ] `calendar_integration/` directory does not exist
- [ ] No `.py` files related to Calendar/Tasks API in repo
- [ ] `setup.py` has zero dependencies
- [ ] `SKILL.md` frontmatter includes `requires_mcp: "google-calendar"`

### 4.2 SKILL.md content
- [ ] Stage 5 describes MCP tools, not Python API
- [ ] COLOR_MAP, REMINDER_PRESETS, RRULE are embedded as JSON/code blocks
- [ ] All 4 presets (Weekly Review, WOOP, Milestone, Time Block) have step-by-step prompt instructions
- [ ] Free slot algorithm is described as reasoning steps
- [ ] Daily Top-3 is described as conversation-state text list (no Tasks sync)
- [ ] Failure modes table covers: not connected, declined, rate limit, permission denied, recurrence unsupported
- [ ] Event data schema is documented for parsing MCP responses

### 4.3 References
- [ ] `references/calendar_integration.md` is under 300 lines
- [ ] `references/calendar_integration.md` contains only MCP reference (no Python architecture)

### 4.4 Git
- [ ] All changes committed on `feature/mcp-experiment`
- [ ] Commit message explains the migration
- [ ] `main` branch is untouched until explicit merge request

### 4.5 No regression
- [ ] Stages 1-4 in SKILL.md are unchanged
- [ ] Dashboard section is unchanged
- [ ] Emotional Intelligence protocol is unchanged
- [ ] Safety & Ethics section is unchanged

---

## 5. Risk Assessment & Fallback

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Official MCP doesn't support write scopes | Medium | High | SKILL.md includes read-only fallback; user can still use `list_events` |
| Recurrence (RRULE) rejected by MCP | Medium | Medium | Fallback: create individual events for 4 weeks |
| MCP latency > 2s | Low | Low | Retry once; if persists, switch to text-only mode |
| User wants Tasks API back | Low | Low | `tasks_manager.py` exists in `main` branch history; can restore |
| Skill size still too large | Low | Medium | After migration, skill is ~70% smaller; if still large, further trim references |

**Fallback plan**: If MCP migration fails in practice, create `revert-mcp` branch from `main` and restore Python module.

---

## 6. Execution Checklist (post-approval)

- [ ] Delete `calendar_integration/` (git rm -rf)
- [ ] Rewrite `SKILL.md` Stage 5 + frontmatter
- [ ] Rewrite `setup.py` (minimal)
- [ ] Rewrite `references/calendar_integration.md`
- [ ] Update `README.md` (remove Python setup)
- [ ] Commit all changes
- [ ] Present diff for final review
- [ ] Merge to `main` (upon user approval)

---

## 7. Approval Required

**Do you approve this final plan?**

Please confirm:
1. ✅ The new Stage 5 structure looks correct
2. ✅ Acceptance criteria are sufficient
3. ✅ You're ready to execute (or want changes)

Reply with **"Approve — execute"** or list requested changes.
