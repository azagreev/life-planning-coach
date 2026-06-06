# Calendar Intelligence — Pre-flight Protocol

> **Integration:** Использует `references/calendar_constants.md` (COLOR_MAP, REMINDER_PRESETS).  
> **Runtime:** Claude.ai + Kimi Code CLI (требуется Google Calendar MCP).  
> **Not supported:** Grok (native connectors), Kimi OK Computer (text-only).

---

## Pre-flight Checklist

Перед созданием любого события выполни 5 шагов:

1. **Density Check** — `list_events` на дату  
   Суммарная загрузка >6ч → warning: «У вас уже X часов запланировано. Добавление ещё одного события — риск перегрузки.»  
   >8ч → предложи перенести или делегировать.

2. **Conflict Detection** — проверь overlap с существующими событиями  
   Если conflict → не перезаписывай. Предложи 2–3 альтернативных слота.

3. **Chronotype Alignment** — сравни время с peak/trough профиля  
   См. `references/chronotype_native_planning.md`.  
   Deep Work → peak hours. Админ/рутина → trough.

4. **Smart Proposal** — если conflict или неподходящее время  
   Используй Free Slot Algorithm или `suggest_time` (если доступен).

5. **Create with Validation** — `create_event` → `get_event` для подтверждения  
   Проверь: summary, time, colorId, reminders совпадают с intent.

---

## Free Slot Algorithm

```
list_events(timeMin, timeMax)
  → извлечь busy intervals
  → merge overlapping
  → найти gap ≥ requested_duration
  → вернуть 2–3 варианта с учётом chronotype
```

Fallback: `suggest_time` (MCP native) если доступен.

---

## Workload Warning Thresholds

| Загрузка | Сообщение |
|----------|-----------|
| ≤6ч | Нормальная загрузка |
| 6–8ч | «Риск перегрузки. Рассмотрите перенос несрочных задач.» |
| >8ч | «Высокая загрузка. Рекомендую перенести или делегировать.» |

---

## Work Hours (User-Configurable)

Рабочие часы настраиваются пользователем (по умолчанию 9:00–18:00). Пороги загрузки выше рассчитаны относительно стандартного дня.

### Calibration Question

> «Какое время начала и окончания рабочего дня для вас комфортное?»

Ответ задаёт рамки для Density Check и Boundary Detection.
