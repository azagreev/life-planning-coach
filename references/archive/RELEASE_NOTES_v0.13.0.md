## Что нового в v0.13.0

### Добавлено
- **`references/workload_warning.md`** — Pre-flight проверка загрузки: 3 уровня (Green/Yellow/Red), user-configurable threshold (default 6ч/день), estimated completion vs shutdown time, MI-aligned defer/backlog suggestion
- **`references/calendar_pattern_analyzer.md`** — Read-only анализ календаря: 5 метрик (Meeting Load, Focus Time, Boundary Violation, Recovery Deficit, Chronotype Alignment), conversational insights, permission-based
- **Energy Scheduling v2** — self-reported 1–10 scale, pattern learning (честный фрейминг), rain plan, recovery micro-block, energy-aware meeting lengths

### Изменено
- **`references/energy_scheduling.md`** — расширен с 74 до 116 строк (v1 контент сохранён + 6 новых секций)
- **`SKILL.master.md`** — Phase 5 hooks: workload check перед create_event, energy self-report при Daily Planning, optional end-of-week pattern analyzer
- **`references/calendar_intelligence.md`** — user-configurable work hours (default 9:00–18:00) вместо hardcoded
- **`references/calendar_constants.md`** — platform-neutral wording (Claude/MCP убраны)

### Исправлено
- **Тесты** — лимиты строк для `energy_scheduling.md` обновлены с 80→120 в legacy тестах (`test_v071_features.py`, `test_chronotype_integration.py`)
