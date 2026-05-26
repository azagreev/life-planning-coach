# Calendar Constants для Google Calendar

> **Для AI-ассистента:** Используй эти константы во всех вызовах для календаря. Загрузи этот файл перед работой с календарём.
> **Schema verified:** 2026-05-26 — connector schema deviations внизу. Подробнее в `calendar_integration.md`.

## Calendar Tools Available (8 confirmed)

Используют connector-specific схему параметров (НЕ raw Google API).

| Tool | Purpose | Schema notes |
|------|---------|--------------|
| `list_calendars` | Discover user's calendars | — |
| `list_events` | Read events for a date range. Always expanded (singleEvents=true). | Нет pagination tokens; не проверено поведение для > pageSize. |
| `get_event` | Read single event details | — |
| `create_event` | Create new event (supports recurrence) | Используй `recurrenceData` (input) + `overrideReminders` flat. `startTime`/`endTime` без TZ offset + отдельный `timeZone`. |
| `update_event` | Modify existing event | Scope через id type (master = all; instance = single). NO "this and following" scope. |
| `delete_event` | Remove event | Может double-fire ("Already deleted" на retry — net effect OK). |
| `respond_to_event` | RSVP to invitations | — |
| `suggest_time` | Find available meeting slots | `attendeeEmails` (accepts Calendar IDs). Response в UTC независимо от `timeZone`. Coarse granularity. |

## COLOR_MAP

Цветовая схема Life Planning для Google Calendar:

```json
{
  "deep_work": "2",
  "woop": "7",
  "weekly_review": "5",
  "family": "1",
  "exercise": "6",
  "reading": "4",
  "urgent": "11",
  "personal": "3",
  "meeting": "9",
  "planning": "10",
  "default": "8"
}
```

## REMINDER_PRESETS

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

## RRULE_PRESETS

```json
{
  "weekly_sunday": ["RRULE:FREQ=WEEKLY;BYDAY=SU"],
  "daily":         ["RRULE:FREQ=DAILY"],
  "weekdays":      ["RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"]
}
```

## Event Data Schema

### Request shape (connector-specific — что передавать в `create_event` / `update_event`)

```json
{
  "calendarId": "string (...@group.calendar.google.com or 'primary')",
  "summary": "string (title)",
  "description": "string",
  "startTime": "ISO-8601 без TZ offset (e.g. '2026-05-27T19:00:00')",
  "endTime": "ISO-8601 без TZ offset",
  "timeZone": "IANA TZ name (e.g. 'Europe/Moscow')",
  "colorId": "string (1-11)",
  "overrideReminders": [{"method": "popup|email", "minutes": int}],
  "recurrenceData": ["RRULE:...", "EXDATE:...", "RDATE:..."]
}
```

### Response shape (что возвращает Google через connector)

```json
{
  "id": "string",
  "status": "confirmed|tentative|cancelled",
  "summary": "string",
  "description": "string",
  "start": {"dateTime": "ISO-8601+TZ", "timeZone": "string"},
  "end": {"dateTime": "ISO-8601+TZ", "timeZone": "string"},
  "colorId": "string (1-11)",
  "overrideReminders": [{"method": "popup|email", "minutes": int}],
  "recurrence": ["RRULE:..."],
  "recurringEventId": "string (для instances of recurring)",
  "originalStartTime": {"dateTime": "ISO-8601+TZ"},
  "attendees": [{"email": "string"}],
  "htmlLink": "string (URL)",
  "creator": {"email": "string"},
  "organizer": {"email": "string", "displayName": "string", "self": bool}
}
```

⚠️ **Field name asymmetry:** request `recurrenceData` → response `recurrence`. Не путать.

### RRULE UNTIL — критичный формат

UNTIL **обязательно UTC с trailing Z**:
- ✅ `"RRULE:FREQ=DAILY;UNTIL=20260610T205959Z"`
- ❌ `"RRULE:FREQ=DAILY;UNTIL=20260610T235959"` (отклоняется с `UNPARSABLE_NUMBER`)

UNTIL endpoint-**inclusive** (per RFC 5545) — если ожидаешь N instances, проверь что UNTIL покрывает start последнего, иначе будет N+1.

## Presets

### Weekly Review Reminder
- `summary`: "Weekly Review"
- `description`: "Weekly Review — ретроспектива недели:\n1. Что прошло хорошо?\n2. Что можно улучшить?\n3. Какие уроки извлечены?\n4. Приоритеты на следующую неделю"
- `duration`: 30 мин
- `colorId`: 5
- `reminders`: weekly_review preset
- `recurrence`: weekly_sunday

### WOOP Reminder
- `summary`: "WOOP Сессия"
- `description`: "WOOP-сессия (Wish, Outcome, Obstacle, Plan)..."
- `duration`: 15 мин
- `colorId`: 7
- `reminders`: woop preset
- `recurrence`: daily

### Milestone Event
- `summary`: "Milestone: {title}"
- `colorId`: 11
- `reminders`: milestone preset

### Time Block
- `colorId`: определяется из COLOR_MAP по типу активности
- `reminders`: определяется из REMINDER_PRESETS по типу активности

## Failure Modes

| Сценарий | Ответ / Action |
|----------|---------------|
| Calendar not connected | "Для работы с календарём нужно подключить Google Calendar в настройках. Продолжим без синхронизации?" |
| User declines OAuth | "Понял, будем работать без календаря. Все планы останутся в нашем разговоре." |
| Rate limit (429) | "Google Calendar временно недоступен из-за лимита запросов. Попробуем через минуту или продолжим без календаря?" |
| Permission denied (403) | "Недостаточно прав для изменения календаря. Проверьте доступ в настройках Google Calendar." |
| Recurrence not supported | _Не актуально для MCP-режима_ — recurrence работает через `recurrenceData`. В Mode B (Paper Coach, без MCP) — fallback: «Создам отдельные события на ближайшие 4 недели вместо повторяющегося». |
| `UNPARSABLE_NUMBER` на recurring create | Connector требует UNTIL в UTC с Z. **Action**: reformat UNTIL и retry. |
| `delete_event` вернул "Already deleted" | Connector double-fired delete; первый успешен. **Action**: считай success, опционально verify через `list_events`. |
| Write op не запросил approval | Session-scope auto-extend после первого "Allow once". **Action**: ожидаемое поведение; surface to user если важно. |
| `suggest_time` пропустил small busy interval | Coarse granularity. **Action**: supplement через `list_events`-based slot search. |
| `suggest_time` вернул UTC времена | Always UTC регардлесс `timeZone`. **Action**: convert в user TZ для display. |
| "This and following" update не работает | Scope param отсутствует. **Action**: manually split — update master с `UNTIL=before_split`, create new master starting от split_date. |
| Lazy tool load — первая op медленнее | `Searched available tools` precall (+5s). **Action**: ожидаемо, subsequent calls быстрее. |

## Free Slots Analysis

Алгоритм поиска свободных слотов:
1. Определить рабочее окно (по умолчанию 9-18)
2. Извлечь занятые интервалы из событий
3. Отсортировать и слить пересекающиеся интервалы
4. Найти gaps ≥ запрошенной длительности
5. Предложить топ-3 слота: "Свободно: HH:MM–HH:MM (N минут)"

## Daily Top-3

Google Tasks API недоступен напрямую. Daily Top-3 — чисто conversational:
1. Хранить в conversation state
2. Показывать как текстовый список с чекбоксами (☐ / ☑)
3. На следующей сессии — спросить статус выполнения
