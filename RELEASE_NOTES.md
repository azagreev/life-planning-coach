# Release Notes — life-planning-coach v0.2.0

> **Тип релиза:** Major migration  
> **Дата:** 2026-05-16  
> **Миграция:** Python-пакет `calendar_integration/` → Official Google Calendar MCP (zero-setup)

---

## Что нового

### Google Calendar через MCP (zero-setup)
- Интеграция переписана на официальный Google Calendar MCP-коннектор, встроенный в claude.ai.
- Подключение: Settings → MCP → Google Calendar → Authorize (один клик).
- Не требуется: Python-окружение, `credentials.json`, OAuth-консоль Google, зависимости.

### 4 пресета жизненного планирования
- **Weekly Review** — еженедельная ретроспектива ( recurring, напоминания за 60 и 15 мин ).
- **WOOP** — утренняя сессия Wish-Outcome-Obstacle-Plan ( ежедневно, 15 мин ).
- **Milestone** — веха 12-Week Year ( напоминание за сутки ).
- **Time Block** — блок глубокой работы с цветовой маркировкой.

### Встроенные константы в SKILL.md
- `COLOR_MAP` — цветовая схема событий (11 категорий).
- `REMINDER_PRESETS` — предустановленные наборы напоминаний.
- `RRULE_PRESETS` — паттерны повторения (weekly, daily, weekdays).

### Анализ свободных слотов
- Алгоритм поиска окна: `list_events` → извлечение busy-интервалов → слияние → поиск gap ≥ запрошенной длительности.
- Альтернатива: нативный `suggest_time` MCP, если доступен.

### Таблица отказов (Failure Modes)
- 5 сценариев с ответами на русском: MCP не подключен, отказ от OAuth, rate limit, permission denied, recurrence not supported.

### Документация
- **README.md** полностью переписан: value prop, workflow, пошаговая установка, FAQ, troubleshooting.
- Добавлен **психологический дисклеймер**: скилл — не замена терапии, порекомендует профессионала при кризисе.

### Сборка
- `setup.py` — нулевые зависимости (`install_requires` удалён).

---

## Критические изменения

- **Удалён весь пакет `calendar_integration/`** (~4070 строк): `auth.py`, `calendar_manager.py`, `tasks_manager.py`, `config.py`, `models.py`, `exceptions.py`, `example_usage.py`, `requirements.txt`.
- **Удалена интеграция Google Tasks API.** Daily Top-3 теперь хранится только в контексте разговора (текстовый формат, без синхронизации).
- **Удалены `references/calendar_integration.md`** (старая инструкция по OAuth Python) и `__init__.py`.

---

## Руководство по миграции

| Если раньше вы... | Теперь... |
|---|---|
| Устанавливали Python-зависимости (`pip install -r calendar_integration/requirements.txt`) | Ничего устанавливать не нужно |
| Создавали `credentials.json` в Google Cloud Console | Авторизуйтесь в Settings → MCP → Google Calendar |
| Использовали Google Tasks для Daily Top-3 | Ведите Daily Top-3 в разговоре с Claude (текст + чекбоксы) |
| Полагались на локальное шифрование токенов | OAuth управляется Anthropic (zero-trust, скилл не видит токены) |

**Для пользователей v0.1.x:** удалите старый `calendar_integration/` и `references/calendar_integration.md`, затем загрузите новый `SKILL.md` (или `.skill`) в Claude. Данные Wheel of Life и целей экспортируйте через «Сохрани прогресс в Markdown» до обновления.

---

## Известные ограничения

1. **Google Tasks API недоступен через MCP.** Daily Top-3 — только текст в контексте разговора, без кросс-девайс синхронизации.
2. **MCP требует Claude Pro.** Без подписки календарная интеграция не работает; скилл gracefully降级到 текстовому режиму.
3. **Контекст разговора ограничен.** При длинных диалогах данные могут сжиматься — рекомендуется экспорт после каждой сессии.
4. **Русский язык в Failure Modes.** Ответы на ошибки MCP на русском; технические детали (коды HTTP) скрыты от пользователя.
5. **Recurrence fallback.** Если MCP не поддерживает `RRULE`, скилл создаёт 4 отдельных события вручную.
