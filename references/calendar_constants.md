# Calendar Constants для Google Calendar

> **Для AI-ассистента:** Используй эти константы во всех вызовах для календаря. Загрузи этот файл перед работой с календарём.

## Calendar Tools Available

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

| Сценарий | Ответ |
|----------|-------|
| Calendar not connected | "Для работы с календарём нужно подключить Google Calendar в настройках. Продолжим без синхронизации?" |
| User declines OAuth | "Понял, будем работать без календаря. Все планы останутся в нашем разговоре." |
| Rate limit (429) | "Google Calendar временно недоступен из-за лимита запросов. Попробуем через минуту или продолжим без календаря?" |
| Permission denied (403) | "Недостаточно прав для изменения календаря. Проверьте доступ в настройках Google Calendar." |
| Recurrence not supported | "Создам отдельные события на ближайшие 4 недели вместо повторяющегося." |

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
