# Module: Phase 4 — Interactive Dashboard

> **Tier:** 2 (lazy-load module)
> **Загружается:** при запросе «покажи дашборд», «визуализируй прогресс», «нарисуй колесо».
> **Предусловие:** есть данные хотя бы из Phase 1 (Wheel of Life) ИЛИ Phase 2 (Goals).
> **Связанные refs:** `dashboard_guide.md`, `state_v2_schema.md`, `templates/Progress_Dashboard.md`

---

## Entry triggers

- «Покажи дашборд / дашборд / dashboard»
- «Визуализируй прогресс»
- «Нарисуй колесо жизни»
- «Хочу увидеть всё в одной картинке»
- «HTML», «график», «диаграмма», «график прогресса»

---

## Two delivery modes

### Mode A: HTML Dashboard (default, если доступна генерация файлов)
1. Считай state v2 (из памяти, wiki или текущей сессии).
2. Сформируй `window.lpData` — JSON по контракту из `references/dashboard_guide.md`.
3. Скопируй `life-planning-dashboard.html`, инжектни `lpData` в `<script>` блок перед `</head>`.
4. Выдай файл пользователю с инструкцией: «Открой в браузере — работает offline».

### Mode B: Text Dashboard (fallback)
Если файл-генерация недоступна (Grok / Kimi Web / no code execution):
1. Используй шаблон из `references/templates/Progress_Dashboard.md`.
2. Сгенерируй markdown-таблицу: 11 сфер × score + индикатор изменения.
3. Добавь блок «Top-3 goals + статус».
4. Заверши блоком «Что менять — одна формулировка».

---

## JSON Data Contract (`window.lpData`)

Минимальный набор полей (полная схема — в `references/dashboard_guide.md`):

```json
{
  "schema_version": "2.0",
  "user_id": "anonymous",
  "generated_at": "2026-05-26T14:30:00Z",
  "wheel_of_life": {
    "health": 6, "finances": 4, "career": 7, "family": 8,
    "romance": 5, "social": 6, "personal_growth": 7,
    "meaning": 5, "fun_recreation": 3, "contribution": 6,
    "physical_environment": 7
  },
  "core_values": ["autonomy", "contribution", "family"],
  "goals": [
    { "id": "g1", "layer": "quarter", "title": "...", "owner_value": "autonomy", "progress": 0.65 }
  ],
  "wins_log": [ { "ts": "...", "text": "..." } ],
  "habits": [ { "id": "h1", "name": "...", "streak": 12, "status": "green" } ]
}
```

**Schema version contract:** dashboard принимает major=2. При несовпадении показывает fallback message + sample data вместо краша.

---

## Three tabs (canonical structure)

1. **Overview** — Wheel of Life (radar), core values (chips), wins-strip за последние 4 недели.
2. **Retrospective** — Velocity chart (Lead vs Lag по KR), habits streaks, weekly review markers.
3. **Goals** — Goal Architecture tree (BHAG → Themes → Quarter KR → Weekly), AGF radar per goal, progress bars.

См. `references/dashboard_guide.md` для display rules каждого таба.

---

## Coaching display rules

- **Не показывай** числа без интерпретации. После таблицы — одна фраза «что это значит».
- **Не интерпретируй** низкое значение как «плохо». «Низкое = эта сфера сейчас тебя зовёт».
- **Не сравнивай** с «нормами» — нет нормы.
- **Подсвечивай** изменения с прошлой недели (если есть `wheel_of_life_history`): зелёный +, красный −, серый =.
- **Closing**: всегда заверши вопросом «Что ты видишь? На что хочется обратить внимание?» — это передаёт agency пользователю.

---

## Persona adaptations

- **ADHD** (`references/adhd_mode.md`): минимизируй цифры. Один большой визуал (radar) + 3 ключевых wins. Никаких сводных таблиц на 30 строк.
- **Elder homebound** (`references/elder_homebound_mode.md`): не показывай KR / Velocity. Только wheel (без Career/Romance/Finance) + меморный блок («что было важного на этой неделе»).
- **Planning Friction** (`references/planning_friction_audit.md`): один таб (Overview). Не подавай 3 таба сразу.

---

## State writes

Phase 4 в норме **не пишет** в state — только читает. Исключение:
- `dashboard_generated_at`: ISO timestamp последней генерации (для UX «открой свой свежий дашборд»).
- `dashboard_mode_used`: "html" | "text" — для debug telemetry (без PII).

См. `references/state_v2_schema.md`.

---

## Common exit transitions

- **Phase 3 (Weekly Review)** — пользователь увидел просадку и хочет понять → `references/module_phase3_weekly_review.md`
- **Phase 1.5 (Re-filter)** — увидел, что goal больше не светится → `references/module_phase1_5_goal_filter.md`
- **Phase 5 (Execution)** — хочет сразу занести action в календарь → `references/module_phase5_execution.md`

---

## Gotchas

- **НЕ генерируй** HTML до того, как у пользователя есть данные Phase 1 минимум. Иначе дашборд будет пустой и обескураживающий.
- **НЕ хардкодь** `WHEEL_SPHERES` / `EXECUTION_SCORES` в HTML. Контракт — data-driven через `window.lpData`.
- **НЕ переименовывай** канонические sphere id (`health`, `finances`, ...). Это контракт со state v2.
- **НЕ показывай** «динамику» если нет истории. Покажи snapshot и пометь «первый замер».
- **НЕ обещай** persistence дашборда. HTML — это снимок текущего state, не living document.
- **ВСЕГДА** заверши генерацию вопросом — без него дашборд становится приговором, а не зеркалом.
