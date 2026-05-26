# Module: Phase 5 — Execution Backbone (Calendar Integration)

> **Tier:** 2 (lazy-load module)
> **Загружается:** когда пользователь готов перейти от планирования к исполнению, или при запросе «запланируй», «в календарь», «когда сделать».
> **Предусловие:** есть цели из Phase 2 ИЛИ конкретное намерение, которое стоит зафиксировать во времени.
> **Связанные refs:** `calendar_constants.md`, `calendar_integration.md`, `energy_scheduling.md`, `workload_warning.md`, `chronotype_native_planning.md`, `shutdown_ritual.md`, `markdown_tables.md`

---

## Why calendar matters

> 60% намерений без временного слота забываются через 48 часов (Milkman et al., 2021). Запланированное событие в календаре имеет 80%+ вероятность выполнения vs 30% для списка задач. «Лучше тупой карандаш, чем острый ум» — календарь — это твой карандаш.

---

## Entry triggers

- «Запланируй на завтра / на неделю»
- «В календарь»
- «Когда мне это сделать?»
- «Свободные слоты», «time block», «deep work»
- «Daily Top-3», «план на сегодня»

---

## Two execution modes

### Mode A: Calendar Connected (default if available)
- Пользователь подключил Calendar connector (Google / iCloud / Outlook — конкретный механизм авторизации зависит от платформы, см. overlay).
- Skill создаёт реальные события через connector с подтверждением.
- Использует `references/calendar_constants.md`: COLOR_MAP, presets, failure modes.

### Mode B: Paper Coach Mode (fallback)
- Calendar недоступен или пользователь не хочет подключать.
- Работаем через markdown — Daily Top-3 + Time Blocks таблицей (`references/markdown_tables.md`).
- Фраза для пользователя: «В этом режиме я не создаю события автоматически — вот ваш план в текстовом виде. Скопируйте в свой календарь или заметки. Research показывает: люди, которые записывают планы от руки, запоминают их на 42% лучше.»

---

## Pre-flight: Workload Check

ВСЕГДА перед созданием событий — проверь загрузку через `references/workload_warning.md`:
- 🟢 **Green** (< 60% забронированного времени): создаём всё.
- 🟡 **Yellow** (60–80%): подсветим, что добавляем НА фоне уже плотной недели. Спросим подтверждение.
- 🔴 **Red** (> 80%): СТОП. Сначала разгружаем, потом добавляем. Иначе создаём систему, которая сломается через 3 дня.

---

## What goes into calendar (execution layer)

| Goal layer | Что попадает в календарь |
|------------|-------------------------|
| BHAG | Годовая веха-напоминание (1 раз/год) |
| Life Themes | Квартальная review (4 раза/год) |
| 12-Week OKR | Milestone-события (по 2–3 на KR) |
| Weekly Priorities | Weekly Review (воскресенье вечер, recurring) |
| Daily WOOP | Утреннее напоминание (recurring, ≤ 5 мин) |
| Time Blocks | Блоки глубокой работы (цвета из COLOR_MAP) |
| Habit Loop | Ежедневные микро-привычки (`references/habit_loop.md`) |

**Цвета через COLOR_MAP** (см. `references/calendar_constants.md`): не выдумывай новые, используй каноничные — иначе пользователь теряет визуальный язык.

---

## Energy-aware scheduling

Не все часы одинаковы. Загрузи `references/energy_scheduling.md`:
- Спроси самооценку 1–10 по уровню энергии в разное время дня.
- Маппинг: Deep Work → пик; Меетинги → средний; Recovery → провал.
- Учитывай хронотип через `references/chronotype_native_planning.md` (3 профиля: Lark / Bear / Wolf, Peak-Trough-Rebound).

---

## Daily Top-3 protocol

Каждый рабочий день — 3 ключевые задачи, привязанные к KR:

1. **Top-1** — самая важная. Делается в пик энергии (1–3 часа времени), обычно утром.
2. **Top-2** — следующая по приоритету. Делается во второй пик или после обеда.
3. **Top-3** — третья. Может быть «легче», но всё ещё привязана к KR.

Не задачи из списка, а **обязательства**. Если Top-3 не выполнены — это сигнал для retro (Phase 3), а не «ну ладно».

---

## End-of-day ritual

В конце рабочего дня — предложи Shutdown Ritual (`references/shutdown_ritual.md`):
- 5 шагов, 10–15 минут, permission-based.
- Психологический detachment — без него вечер «остаётся в работе».
- Permission-based: не навязываем, предлагаем «можем сделать ритуал завершения?»

---

## End-of-week analysis (опционально)

Если пользователь готов — предложи read-only анализ паттернов через `references/calendar_pattern_analyzer.md`:
- Сколько часов на Deep Work vs Meetings?
- Где «протекают» Time Blocks?
- Recovery достаточно?

Анализ без оценки — просто данные. Выводы делает пользователь.

---

## Task Breakdown (для сложных WOOP)

Если Daily WOOP сегодня — сложная задача (Career / Finances / Health / Home / Learning):
- Загрузи `references/action_breakdown_template.md`.
- Каждый шаг ≤ 30 минут ИЛИ бинарный критерий.
- Opt-in: пользователь может пропустить разбивку.

---

## Persona adaptations

- **ADHD** (`references/adhd_mode.md`): **Time Buffer Rule × 2** на все оценки. Visual timer prompts. Body double для страшных задач. Никаких «расписать день поминутно» — даём блоки по 90 мин с большими буферами.
- **Unemployed / transitional** (`references/time_structure_unemployed.md`): **Sharp Hours 9:00–13:00** — активный поиск / обучение. После 17:00 — строго свободное время. Social activities как якоря дня.
- **Elder homebound** (`references/elder_homebound_mode.md`): **Day anchors** — ритуалы, не задачи. «Чай в 10, растения в 15, передача в 20». Никаких KR-милстоунов.
- **Planning Friction** (`references/planning_friction_audit.md`): **Smart defaults** — 25 мин митинг, 45 мин задача, 15 мин буфер. Day templates: Deep Work / Meeting / Recovery. 10%-rule на корректировки.

---

## State writes

В конце Phase 5 запиши в state v2:
- `calendar_events_log`: [{ event_id, title, start, end, kr_link, created_via: 'connector'|'paper', color_id }]
- `daily_top3_log`: [{ date, top1, top2, top3, completed: [bool, bool, bool] }]
- `energy_self_reports`: [{ ts, level (1–10), context }]
- `shutdown_ritual_log`: [{ ts, completed_steps: 1–5 }]

См. `references/state_v2_schema.md`. При записи в Drive — через `references/templates/Raw_Session.md` и обновление `Hot_Cache.md` (active calendar context).

---

## Common exit transitions

- **Phase 3 (Weekly Review)** — конец недели → `references/module_phase3_weekly_review.md`
- **Phase 0.5 (ER Protocol)** — пользователь застрял на «не могу начать» → см. `module_phase1_diagnostic.md`
- **Recovery** — несколько дней Top-3 не выполнены → `references/recovery_protocol.md`
- **Phase 4 (Dashboard)** — пользователь хочет увидеть execution stats → `references/module_phase4_dashboard.md`

---

## Gotchas

- **НЕ создавай** события без Pre-flight Workload Check. Это правило #1.
- **НЕ создавай** рекуррентные события если connector не поддерживает — fallback на отдельные события.
- **НЕ предлагай** Calendar setup в Phase 0. Это блокирует zero-setup default. Phase 5 — единственное место, где предлагаем connector.
- **НЕ записывай** в Drive во время сессии события одно за одним. Накапливай в памяти, batch-запись в конце (≤ 5 approval'ов).
- **НЕ обещай** автоматическую sync если работаем в Paper Coach Mode. Будь честен про границы.
- **НЕ хардкодь** colorId / цвета. Используй COLOR_MAP из `references/calendar_constants.md`.
- **ВСЕГДА** Pre-flight Workload Check (Green / Yellow / Red) перед записью.
- **ВСЕГДА** связывай каждое событие с конкретным KR (`kr_link`) — иначе календарь превращается в задачник.
