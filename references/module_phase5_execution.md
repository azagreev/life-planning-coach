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

### Mode A: Calendar Connected (default — primary path)
- Пользователь подключил Calendar connector (Google / iCloud / Outlook — механизм зависит от платформы).
- Skill создаёт реальные события через connector с подтверждением (схема и quirks — `calendar_integration.md`).
- Использует `references/calendar_constants.md`: COLOR_MAP, presets, failure modes.

### Mode B: Paper Coach Mode (fallback)
- Calendar недоступен (нет Max plan, не подключён connector) или пользователь не хочет подключать.
- Работаем через markdown — Daily Top-3 + Time Blocks таблицей (`references/markdown_tables.md`).
- Фраза для пользователя: «В этом режиме я не создаю события автоматически — вот ваш план в текстовом виде. Скопируйте в свой календарь или заметки. Research показывает: люди, которые записывают планы от руки, запоминают их на 42% лучше.»

---

## Pre-flight: Workload Check

ВСЕГДА перед созданием событий — проверь загрузку через `references/workload_warning.md`:
- 🟢 **Green** (< 60% забронированного времени): создаём всё.
- 🟡 **Yellow** (60–80%): подсветим, что добавляем НА фоне уже плотной недели. Спросим подтверждение.
- 🔴 **Red** (> 80%): СТОП. Сначала разгружаем, потом добавляем. Иначе создаём систему, которая сломается через 3 дня.

---

## What goes into calendar

| Goal layer | Календарь |
|------------|-----------|
| BHAG | Годовая веха (1×/год) |
| Life Themes | Квартальный review (4×/год) |
| 12-Week OKR | Milestone-события (2–3 на KR) |
| Weekly Priorities | Weekly Review (воскресенье, recurring) |
| Daily WOOP | Утреннее напоминание (recurring, ≤ 5 мин) |
| Time Blocks | Deep work (цвета из COLOR_MAP) |
| Habit Loop | Микро-привычки (`references/habit_loop.md`) |

**Цвета через COLOR_MAP** (`references/calendar_constants.md`) — не выдумывай новые.

---

## Energy + Daily Top-3 + Shutdown

**Energy-aware:** загрузи `references/energy_scheduling.md` + `chronotype_native_planning.md` (Lark/Bear/Wolf). Deep Work → пик, Meetings → средний, Recovery → провал.

**Daily Top-3** — 3 задачи, привязанные к KR. Top-1 в пик энергии (1–3ч, утро); Top-2 после обеда; Top-3 легче. Не задачи — **обязательства**. Невыполнение → сигнал для Phase 3 retro.

**Shutdown Ritual** (`references/shutdown_ritual.md`) — 5 шагов, 10–15 мин, permission-based. Психологический detachment.

**End-of-week analysis** (опц.) — `references/calendar_pattern_analyzer.md`: Deep Work vs Meetings, где «протекают» Time Blocks, recovery. Данные без оценки.

**Task Breakdown** для сложных WOOP — `references/action_breakdown_template.md`, шаги ≤ 30 мин или бинарный критерий.

---

## Persona adaptations

- **ADHD** (`references/mode_adhd.md`): **Time Buffer Rule × 2** на все оценки. Visual timer prompts. Body double для страшных задач. Никаких «расписать день поминутно» — даём блоки по 90 мин с большими буферами.
- **Unemployed / transitional** (`references/mode_unemployed.md`): **Sharp Hours 9:00–13:00** — активный поиск / обучение. После 17:00 — строго свободное время. Social activities как якоря дня.
- **Elder homebound** (`references/mode_elder.md`): **Day anchors** — ритуалы, не задачи. «Чай в 10, растения в 15, передача в 20». Никаких KR-милстоунов.
- **Planning Friction** (`references/mode_planning_friction.md`): **Smart defaults** — 25 мин митинг, 45 мин задача, 15 мин буфер. Day templates: Deep Work / Meeting / Recovery. 10%-rule на корректировки.

---

## State writes

В конце Phase 5 запиши в state v2 (`references/state_v2_schema.md`):

**Calendar events (Mode A — connector):**
- `calendar_events_log[]`: append `{event_id (Google Calendar ID), created_at, event_type: "weekly_review"|"woop_morning"|"habit"|"milestone"|"shutdown"|"time_block", title, scheduled_for, recurrence (RRULE или null), color_id (из COLOR_MAP), status: "created"|"updated"|"deleted"}` — каждое реально созданное событие
- В Mode B (Paper Coach) — `calendar_events_log[].created_via: "paper"` без `event_id` (markdown-таблица)

**Daily Top-3 protocol:**
- `daily_top3_log[]`: append `{date, top1: {title, kr_link}, top2: {...}, top3: {...}, completed: [bool, bool, bool], energy_level (1–10 self-report)}`

**Energy self-reports (через день):**
- `energy_self_reports[]`: append `{ts, level (1–10), context: "morning"|"midday"|"evening"|"adhoc"}`

**Shutdown Ritual:**
- `shutdown_ritual_log[]`: append `{ts, completed_steps (1–5), skipped: bool}`

**Recovery sessions (если был запущен `recovery_protocol.md` из-за пропуска > 7 дней или серии трудных недель):**
- `recovery_sessions_log[]`: append `{recovery_id, date, gap_days, strategy_used (из recovery_protocol.md), outcome: "resumed"|"reduced_scope"|"paused"}`
- Также обновить `session.gap_days_since_last_session: 0` (счётчик сбросился)

**Persistence retry (если calendar временно недоступен):**
- `persistence_retry.calendar.pending_events[]`: append событий для retry в следующей сессии

**Session:**
- `session.completed_phases`: append `"5"`
- `session.last_session_at`: ISO timestamp

При записи в Drive — через `references/templates/Raw_Session.md` (calendar_events_log + daily_top3 для сессии) и обновление `references/templates/Hot_Cache.md` (active calendar context + last Daily Top-3).

---

## Common exit transitions

- **Phase 3 (Weekly Review)** — конец недели → `references/module_phase3_weekly_review.md`
- **Phase 0.5 (ER Protocol)** — пользователь застрял на «не могу начать» → см. `module_phase1_diagnostic.md`
- **Recovery** — несколько дней Top-3 не выполнены → `references/recovery_protocol.md`
- **Phase 4 (Dashboard)** — пользователь хочет увидеть execution stats → `references/module_phase4_dashboard.md`

---

## Gotchas

- **НЕ создавай** события без Pre-flight Workload Check. Это правило #1.
- **Recurring events работают** через connector. Fallback на отдельные события только в Mode B.
- **НЕ предлагай** Calendar setup в Phase 0. Это блокирует zero-setup default. Phase 5 — единственное место, где предлагаем connector.
- **НЕ записывай** в Drive во время сессии события одно за одним. Накапливай в памяти, batch-запись в конце (≤ 5 approval'ов).
- **НЕ обещай** автоматическую sync если работаем в Paper Coach Mode. Будь честен про границы.
- **НЕ хардкодь** colorId / цвета. Используй COLOR_MAP из `references/calendar_constants.md`.
- **ВСЕГДА** Pre-flight Workload Check (Green / Yellow / Red) перед записью.
- **ВСЕГДА** связывай каждое событие с конкретным KR (`kr_link`) — иначе календарь превращается в задачник.
