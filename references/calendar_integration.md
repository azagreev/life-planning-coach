# Google Calendar Integration Reference (MCP)

> **Runtime**: Claude.ai web/desktop + Kimi Code CLI (requires Google Calendar MCP server)
> **Not supported**: Grok (uses native connectors), Kimi OK Computer (web, no MCP)
> **Setup**: Claude — Settings → Customize → Connectors → Google Calendar → Connect (Max plan); Kimi CLI — manual JSON config
> **Version**: 0.3.0
> **PoC verified**: 2026-05-26 on Claude Max — see [docs/research/mcp_poc_log.md](../docs/research/mcp_poc_log.md). 14/14 ops functional. Schema deviations documented below.

---

## MCP Tools (8 confirmed)

Internal names shown in expanded tool call cards as `Google Calendar:<name>`. All connector params use connector-specific shapes (NOT raw Google API).

| Tool | Description | Key Parameters (connector-specific) |
|------|-------------|--------------------------------------|
| `list_calendars` | Discover user's calendars | — |
| `list_events` | Read events for date range. Always expanded (`singleEvents=true`). No pagination tokens visible. | `calendarId`, `timeMin`, `timeMax`, `pageSize` |
| `get_event` | Read single event | `calendarId`, `eventId` |
| `create_event` | Create event (supports recurrence) | `calendarId`, `summary`, `description`, `startTime`, `endTime`, `timeZone`, `colorId`, `overrideReminders`, `recurrenceData` |
| `update_event` | Modify event. Scope via id type: master id → all; instance id → single. NO "this and following" scope param. | `calendarId`, `eventId`, `notificationLevel` + fields to update |
| `delete_event` | Remove event. May double-fire ("Already deleted" on retry) — net effect OK. | `calendarId`, `eventId` |
| `respond_to_event` | RSVP to invitee event | `calendarId`, `eventId`, response value |
| `suggest_time` | Find free time windows. Coarse granularity (broad gaps, not carved slots). Response in UTC. | `attendeeEmails` (calendar IDs accepted), `startTime`, `endTime`, `durationMinutes`, `preferences:{startHour,endHour,pageSize}`, `excludeWeekends` |

---

## Schema Quirks (must follow exactly)

**These deviations from canonical Google Calendar API discovered during PoC 2026-05-26:**

1. **`recurrenceData` (input) ≠ `recurrence` (output)** — connector uses asymmetric field naming. Pass as array of RFC 5545 strings: `["RRULE:FREQ=WEEKLY;BYDAY=SU"]`.
2. **`overrideReminders` flat (NOT `reminders.overrides`)** — pass as array directly: `[{"method":"popup","minutes":15}]`. No `useDefault` flag exposed.
3. **`attendeeEmails` for `suggest_time` calendar specifier** — Calendar IDs (`...@group.calendar.google.com`) accepted as email-shaped strings.
4. **`startTime`/`endTime` flat (NOT `start.dateTime`/`end.dateTime`)** — pass as ISO 8601 without TZ offset; separate `timeZone` field.
5. **UNTIL in RRULE MUST be UTC with trailing Z** — local format `20260610T235959` rejected with `UNPARSABLE_NUMBER`. Required: `20260610T205959Z`. UNTIL is endpoint-inclusive per RFC 5545.
6. **`suggest_time` response in UTC** — regardless of requested `timeZone` (which only controls working-hours interpretation). Convert to user TZ for display.
7. **`update_event` scope** — determined by id type, no scope param. Master id updates all instances; instance id (`{master}_{UTC_timestamp}`) updates one.
8. **No pagination tokens** in `list_events` response. Untested behavior with > pageSize events.
9. **Lazy tool discovery** — not all 8 tools load upfront in a chat session; first use of a tool triggers `Searched available tools` precall (+5s overhead).
10. **Write permission auto-extends session-wide** — first manual approval covers subsequent write/delete ops in same browser session, across distinct chats. User may not expect this.
11. **Preflight `get_event` before `delete_event`** — Claude emergent behavior wraps deletes in `get_event` first (safety pattern). Doubles latency. Skill batch-cleanup prompts should explicitly say "skip preflight" if cleanup intent is clear.
12. **Empty calendar response has no `events` field** — `list_events` for empty calendar returns object WITHOUT `events` array entirely (not `[]`). Defensive code: `const events = response.events ?? [];`

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

### REMINDER_PRESETS (pass as `overrideReminders`)
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

### RRULE_PRESETS (pass as `recurrenceData`)
```json
{
  "weekly_sunday": ["RRULE:FREQ=WEEKLY;BYDAY=SU"],
  "daily":         ["RRULE:FREQ=DAILY"],
  "weekdays":      ["RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"]
}
```

When adding `UNTIL`: format as UTC with Z, e.g. `["RRULE:FREQ=DAILY;UNTIL=20260610T205959Z"]`. UNTIL is endpoint-inclusive.

---

## Latency Expectations (from PoC 2026-05-26)

End-to-end wall-clock (prompt → response), Claude Max plan:

| Category | p50 estimate | p95 estimate |
|----------|---------------|---------------|
| Read-only ops (`list_*`, `get_*`, `suggest_time`) | ~20s | ~25s |
| Write/delete ops (first in session — incl. permission UX) | ~50s | ~110s |
| Write/delete ops (subsequent, auto-extended permission) | ~25s | ~35s |

Note: latency dominated by LLM reasoning + permission UX, not MCP transport. This is normal Claude chat UX.

---

## Prompt Patterns

Use **connector-specific field names** (NOT Google API shape).

> Каждое recurring event = WHEN-type Implementation Intention ("когда X — то Y"). См. [`implementation_intentions.md`](implementation_intentions.md) для framing.

### Weekly Review
```
create_event(
  calendarId={user_calendar_id},
  summary="Weekly Review",
  description="🎉 Что получилось на этой неделе? Что принесло радость или гордость?\n🌱 Что хочется попробовать по-другому?\n💡 Какой инсайт пришёл?\n🎯 Что важно на следующей неделе?",
  startTime="{next_sunday}T19:00:00",
  endTime="{next_sunday}T19:30:00",
  timeZone="{user_tz}",
  colorId="5",
  overrideReminders=[{"method":"popup","minutes":60},{"method":"popup","minutes":15}],
  recurrenceData=["RRULE:FREQ=WEEKLY;BYDAY=SU"]
)
```

### WOOP Session
```
create_event(
  calendarId={user_calendar_id},
  summary="WOOP Сессия",
  description="✨ Желание — Чего хочется?\n🌟 Лучший результат — Как будет, если получится?\n🪨 Препятствие — Что может помешать?\n📝 План — Какой первый шаг?",
  startTime="{tomorrow}T07:00:00",
  endTime="{tomorrow}T07:15:00",
  timeZone="{user_tz}",
  colorId="7",
  overrideReminders=[{"method":"popup","minutes":5}],
  recurrenceData=["RRULE:FREQ=DAILY"]
)
```

### Time Block
```
create_event(
  calendarId={user_calendar_id},
  summary={title},
  startTime={date_time},
  endTime={date_time + duration},
  timeZone={user_tz},
  colorId=COLOR_MAP[activity_type],
  overrideReminders=REMINDER_PRESETS[activity_type] || REMINDER_PRESETS["default"]
)
```

---

## Free Slot Algorithm

**Primary path** — use `suggest_time`:
```
suggest_time(
  attendeeEmails=[user_calendar_id],
  startTime={range_start},
  endTime={range_end},
  durationMinutes={requested_minutes},
  timeZone={user_tz},  // affects working-hours interp, NOT response format
  preferences={"startHour": 9, "endHour": 19, "pageSize": 3},
  excludeWeekends=true  // optional
)
→ returns broad free windows in UTC
→ converted back to user TZ for display
```

⚠️ **Coarse granularity:** `suggest_time` returns aggregate free gaps, not carved-out slots of requested duration. Small busy blocks (e.g. 15-min) may NOT be visible in response.

**Precise path** — supplement with `list_events`:
```
1. list_events(timeMin=range_start, timeMax=range_end)
2. Extract busy[] from response (already expanded into discrete instances)
3. Merge overlapping busy intervals
4. Find gaps >= requested_duration within work_hours
5. Return top 3 gaps as "HH:MM–HH:MM (N минут)" in user TZ
```

**Recommendation**: use `suggest_time` for "give me roughly when I'm free" queries; use `list_events`-based algorithm when precise slot boundaries matter.

---

## Retry Persistence Protocol

Когда Google Calendar недоступен в текущей сессии, запланированные события можно сохранить в очередь:

1. **Сохранить в очередь**: Все pending events добавляются в `conversation_state.persistence_retry.calendar.pending_events`
2. **Отметить статус**: `available_last_session = false`, `failed_consecutive_sessions += 1`
3. **Сообщить пользователю**: «Без календаря цели остаются намерениями без временных якорей. Временные слоты помогают памяти — мозгу легче удерживать то, что привязано к конкретному моменту. Предлагаю подключить календарь — один клик, и я автоматически создам напоминания для всех целей.»
4. **В следующей сессии**: Проверить доступность Calendar MCP
   - Если доступен И `pending_events_count > 0` → предложить создать накопленные события
   - Если пользователь согласен → batch-create, очистить очередь
   - Если отказался → `user_declined_count += 1`
   - Если `user_declined_count >= 2` → `backoff_until_session = current_session + 3` (не предлагать 3 сессии)
5. **После успешной синхронизации**: Сбросить все retry-счётчики

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| MCP tools not visible | Connector not authorized | Settings → Customize → Connectors → Google Calendar → Connect |
| `UNPARSABLE_NUMBER` on recurring create | UNTIL in local time | Format as UTC with trailing Z (e.g. `20260610T205959Z`) |
| Write op shows "Already deleted" on delete | Connector double-fires delete on retry; first call succeeded | Treat as success — verify via `list_events` if needed |
| First op in chat slower than expected | Lazy tool discovery (+5s `Searched available tools`) | Expected behavior; subsequent calls fast |
| Write op didn't ask for approval | Session-scope auto-extend after first "Allow once" | Expected behavior; surface to user if surprising |
| Recurring "this and following" not respected | Scope param doesn't exist | Manually split: update master to `UNTIL=before_split`, create new master from `split_date` |
| `suggest_time` missed a small busy block | Coarse granularity | Supplement with `list_events`-based algorithm above |
| `suggest_time` returned UTC times | Response always in UTC | Convert to user TZ in display layer |
| Events not appearing | Wrong calendarId | Use `list_calendars` to find correct ID |
| Rate limit (429) | Too many requests | Wait 60s; use text-only mode |

---

## Daily Top-3 (Text-Only — Tasks NOT in MCP)

**PoC 2026-05-26 finding:** Google Tasks API is **not in Anthropic MCP Connector directory** (as of Max plan, 2026-05). Tasks MCP unavailable.

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

**Alternative**: if/when Todoist or Things MCP appear, integrate via separate connector. Until then, conversational task management (Claude as proxy) or external TMS app (manual sync).
