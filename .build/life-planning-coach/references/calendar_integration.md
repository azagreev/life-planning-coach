# Google Calendar Integration Reference (MCP)

> **Runtime**: claude.ai only (requires official Google Calendar MCP)  
> **Setup**: Zero — MCP is built-in; user authorizes via Settings → MCP → Google Calendar  
> **Version**: 0.2.0

---

## MCP Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `list_calendars` | Discover user's calendars | — |
| `list_events` | Read events for date range | `calendarId`, `timeMin`, `timeMax`, `q` |
| `get_event` | Read single event | `calendarId`, `eventId` |
| `create_event` | Create event (supports recurrence) | `calendarId`, `summary`, `start`, `end`, `colorId`, `reminders`, `recurrence` |
| `update_event` | Modify event | `calendarId`, `eventId`, fields to update |
| `delete_event` | Remove event | `calendarId`, `eventId` |
| `respond_to_event` | RSVP | `calendarId`, `eventId`, `response` |
| `suggest_time` | Find available slots | `calendarId`, `duration`, `timeMin`, `timeMax` |

---

## Life Planning Constants

### COLOR_MAP
```json
{
  "deep_work": "2",      // Sage green
  "woop": "7",           // Peacock blue
  "weekly_review": "5",  // Banana yellow
  "family": "1",         // Lavender purple
  "exercise": "6",       // Tangerine orange
  "reading": "4",        // Flamingo pink
  "urgent": "11",        // Tomato red
  "personal": "3",       // Grape
  "meeting": "9",        // Blueberry
  "planning": "10",      // Basil
  "default": "8"         // Graphite
}
```

### REMINDER_PRESETS
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

### RRULE_PRESETS
```json
{
  "weekly_sunday": ["RRULE:FREQ=WEEKLY;BYDAY=SU"],
  "daily":         ["RRULE:FREQ=DAILY"],
  "weekdays":      ["RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"]
}
```

---

## Prompt Patterns

### Weekly Review
```
create_event(
  summary="Weekly Review",
  description="1. Что прошло хорошо?\n2. Что можно улучшить?\n3. Какие уроки?\n4. Приоритеты на неделю",
  start={next_sunday_19:00},
  end={next_sunday_19:30},
  colorId="5",
  reminders=[{"method":"popup","minutes":60},{"method":"popup","minutes":15}],
  recurrence=["RRULE:FREQ=WEEKLY;BYDAY=SU"]
)
```

### WOOP Session
```
create_event(
  summary="WOOP Сессия",
  description="Wish — Какое желание?\nOutcome — Лучший результат?\nObstacle — Главное препятствие?\nPlan — Если X, то Y",
  start={tomorrow_07:00},
  end={tomorrow_07:15},
  colorId="7",
  reminders=[{"method":"popup","minutes":5}],
  recurrence=["RRULE:FREQ=DAILY"]
)
```

### Time Block
```
create_event(
  summary={title},
  start={date_time},
  end={date_time + duration},
  colorId=COLOR_MAP[activity_type],
  reminders=REMINDER_PRESETS[activity_type] || REMINDER_PRESETS["default"]
)
```

---

## Free Slot Algorithm

```
1. list_events(timeMin=day_start, timeMax=day_end)
2. Extract busy[] from response
3. Merge overlapping busy intervals
4. Find gaps >= requested_duration within work_hours
5. Return top 3 gaps as "HH:MM–HH:MM (N минут)"
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| MCP tools not visible | Connector not authorized | Settings → MCP → Google Calendar → Authorize |
| Write operations fail | Read-only scopes | Check OAuth consent screen; use read-only fallback |
| Recurrence ignored | MCP limitation | Create individual events for 4 weeks |
| Rate limit (429) | Too many requests | Wait 60s; use text-only mode |
| Events not appearing | Wrong calendarId | Use `list_calendars` to find correct ID |

---

## Daily Top-3 (Text-Only)

Google Tasks API is **not available** via official Calendar MCP.
Store Daily Top-3 in conversation state:
```json
{
  "goals": {
    "daily_top3": [
      "☐ Priority 1",
      "☑ Priority 2 (done)",
      "☐ Priority 3"
    ]
  }
}
```
Archive completed top-3 entries to `weekly_reviews` for tracking.
