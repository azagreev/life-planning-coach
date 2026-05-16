# План: Заморозка + Исследование Google Calendar MCP

## Статус: ЗАМОРОЖЕНО до результатов исследования

**Дата заморозки:** 2026-05-16
**Причина:** Критические риски, требующие проверки перед принятием решения
**Выбранный вариант:** C. Заморозка + исследование

---

## Контекст

3 цикла дебатов (Адвокат vs Критик) выявили фундаментальные риски:
- MCP-сервер существует, но в Developer Preview
- Работает только в веб-версии `claude.ai`, не в Desktop/Code CLI
- Не поддерживает Google Tasks API
- Личное тестирование не проводилось
- Domain logic (~60-70% кода) — не infrastructure glue

---

## Цель исследования

Проверить гипотезы плана реальными экспериментами и принять обоснованное решение: упрощать или сохранять текущую архитектуру.

---

## Чеклист исследования (Gates)

### Gate 0: Платформенный аудит
- [ ] Проверить, что Official Google Calendar MCP доступен в `claude.ai` web
- [ ] Проверить, что он НЕ доступен в Claude Desktop
- [ ] Проверить, что он НЕ доступен в Claude Code CLI
- [ ] Зафиксировать: какие планы Claude поддерживают MCP (Free/Pro/Max/Team)

### Gate 1: MCP PoC — OAuth & CRUD
- [ ] Подключить Google Calendar MCP в `claude.ai` Settings → Connectors
- [ ] Пройти OAuth flow, зафиксировать запрашиваемые scopes
- [ ] Создать тестовое событие через MCP (`create_event`)
- [ ] Прочитать событие (`get_event` / `list_events`)
- [ ] Обновить событие (`update_event`)
- [ ] Удалить событие (`delete_event`)
- [ ] Зафиксировать latency каждой операции
- [ ] Зафиксировать формат ошибок (token expired, rate limit, permission denied)

### Gate 2: MCP — Advanced Features
- [ ] Создать recurring event с RRULE
- [ ] Получить список календарей (`list_calendars`) — проверить pagination
- [ ] Проверить `suggest_time` — что именно возвращает
- [ ] Проверить `respond_to_event`
- [ ] Проверить multi-calendar support (primary vs others)
- [ ] Проверить, есть ли read-only mode

### Gate 3: Tasks API Investigation
- [ ] Проверить, есть ли Tasks API в Official Calendar MCP
- [ ] Если нет — протестировать community MCP (`taylorwilsdon/google_workspace_mcp` или `zcaceres/gtasks-mcp`)
- [ ] Оценить: стоит ли второй connector для Tasks (Free план = 1 limit)

### Gate 4: UX Research
- [ ] Замерить time-to-setup: Python-модуль vs MCP Connector
- [ ] Оценить onboarding для non-technical пользователя
- [ ] Проверить behavior при отключённом MCP (graceful degradation)
- [ ] Проверить persistence: сохраняется ли авторизация между сессиями

### Gate 5: Domain Logic Mapping
- [ ] Составить таблицу: каждый метод `calendar_manager.py` → MCP tool или fallback
- [ ] Составить таблицу: каждый метод `tasks_manager.py` → MCP tool или fallback
- [ ] Определить, что потеряется безвозвратно
- [ ] Оценить, можно ли перенести domain logic в `domain/` модуль (~850 строк)

### Gate 6: Decision Gate
- [ ] Суммарный отчёт: что работает, что нет, что потеряно
- [ ] Рекомендация: продолжать с упрощением (вариант B) или сохранить текущую архитектуру (вариант A)
- [ ] Если упрощение — обновлённый план с учётом найденных ограничений
- [ ] Если сохранение — план минимальной поддержки текущего кода

---

## Структура ветки

```
main (frozen, текущий код сохранён)
│
└── feature/mcp-experiment (исследовательская ветка)
    ├── research/
    │   ├── mcp_poc_log.md          # Логи тестовых вызовов
    │   ├── scope_analysis.md       # Анализ OAuth scopes
    │   ├── latency_benchmark.md    # Замеры latency
    │   └── feature_matrix.md       # Таблица: Python vs MCP
    ├── domain/                     # Экспериментальный domain core
    │   ├── config.py
    │   ├── models.py
    │   └── algorithms.py
    └── scripts/                    # Fallback generators
        ├── generate_ics.py
        └── generate_daily_top3.py
```

---

## Ресурсы

### Google Calendar MCP
- URL: `https://calendarmcp.googleapis.com/mcp/v1`
- Документация: https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server
- Claude Settings: `claude.ai` → Customize → Connectors → Add custom connector

### Community alternatives
- `taylorwilsdon/google_workspace_mcp` (2.4k stars, includes Tasks)
- `zcaceres/gtasks-mcp` (Tasks only)

### Текущий код (для сравнения)
- `calendar_integration/calendar_manager.py` — 1051 строк
- `calendar_integration/tasks_manager.py` — 844 строк
- `calendar_integration/auth.py` — 675 строк
- `calendar_integration/config.py` — 252 строк
- `calendar_integration/models.py` — 406 строк
- `calendar_integration/state.py` — 206 строк

---

## Критерии разморозки

План размораживается, когда:
1. ✅ Gate 0-5 пройдены, результаты задокументированы
2. ✅ Суммарный отчёт одобрен (адвокат + критик согласны с выводами)
3. ✅ Принято решение: A (сохранить) или B (Domain Core + MCP Bridge)

---

## Заметки

- **Ничего не удалять** из `main` до завершения исследования
- **Тег `v0.1.0`** уже существует — это baseline
- **AGENTS.md** обновлён: исследование GitHub только через API
