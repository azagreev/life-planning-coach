# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.
> **Как обновлять:** После каждого релиза переносить `In Progress` → `Done`, а `Planned` → `In Progress`.

---

## Текущий статус

| Версия | Статус | Ожидаемая дата | Ключевая фича |
|--------|--------|----------------|---------------|
| v0.6.0 | ✅ Released | 2026-05-16 | Authentic Goals + Portfolio + Adaptive Style |
| v0.7.0 | ✅ Released | 2026-05-17 | Эмоциональная регуляция (minimal) + BUG-001 fix |
| v0.7.1 | ✅ Released | 2026-05-18 | Execution Layer — patch (Win Alert, Recovery, Energy Scheduling) |
| v0.8.0 | ✅ Released | 2026-05-17 | Habit Loop Framework + Execution Layer v2 (6 фич) |
| v0.9.0 | 🔄 In Progress | TBD | Мобильная адаптация + Habit Tracker + краткие сессии |

---

## v0.7.0 — Эмоциональная регуляция (Minimal Scope)

**Цель:** Дать пользователю инструменты для управления эмоциональным состоянием на пути к целям. + Закрыть P1-баг BUG-001.

**Scope:** Minimal — 3 задачи, ~6-7 часов. [Подробный план](references/plan_v0.7.0.md).

**Входит:**
- [x] **BUG-001: Dashboard 8→11 доменов** — P1-баг, дашборд показывает 8 сфер вместо 11
- [x] **Emotion Regulation Protocol** — 3 техники (cognitive reappraisal, grounding, self-compassion)
- [x] **Фикс зависших тестов** — 3 теста устарели после v0.6.1 cleanup

**Не входит (отложено в v0.7.1/v0.8.0):**
- Resilience Assessment (требует психометрии)
- Failure Recovery Protocol
- Energy Management
- Dashboard Self-Contained (большой рефакторинг)
- Calendar Event Copy Review

**Методики:**
- Cognitive Reappraisal (Gross, 1998) — d = 0.45
- Self-Compassion (Neff) — r = 0.47

**Детали планирования:** [`references/plan_v0.7.0.md`](references/plan_v0.7.0.md)

---

## v0.7.1 — Execution Layer Patch (конкурентный анализ 2026-05-17)

**Цель:** Закрыть критичные пробелы в execution layer на основе конкурентного анализа 7 скиллов. 3 фичи прошли 3-цикловой дебат Advocate/Critic и получили вердикт **IMPLEMENT**.

**Scope:** Patch — 3 reference-файла, ~6–8 часов. Не трогает SKILL.md инструкции (≤500 строк).

**Входит:**
- [x] **Win Alert Protocol** (`references/win_alert.md`) — структурированное празднование побед: что достигнуто → домен Wheel of Life → почему важно → ресурсы пользователя → следующий шаг. Адаптируется под Communication Style quadrant. НЕ применяется во время кризиса/Emotional Landing.
- [x] **Recovery Protocol MVP** (`references/recovery_protocol.md`, ≤200 строк) — 3 стратегии + Recovery для 2+ пропусков: Reschedule → Catch-up Mini-Session (15 мин, 3 вопроса) → Skip with Reflection → Recovery Protocol (Emotional Landing → Wheel of Life → 1 приоритет). Паттерн-анализ conversational-only (не декларативный).
- [x] **Energy-Based Scheduling** (`references/energy_scheduling.md`, ≤80 строк) — 3 уровня энергии → маппинг на тип задачи → 1 калибровочный вопрос → защита пиковых часов фокус-блоками. Связь с AC-8 (Energy Check) и Seasonal Planning.

**Не входит (отложено в v0.8.0):**
- Markdown-таблицы как UI (DEFER, conf 8/10 — ждёт dashboard fix + MI review)
- Status Icon System (DEFER, conf 7/10 — ждёт Execution Layer v2)
- Clarifying-Questions-First (DEFER, conf 7/10 — пересекается с Phase 0/Track A)
- Weak Goal Taxonomy (DEFER, conf 7/10 — lightweight pilot возможен в v0.7.1, full в v0.8.0)

**Детали анализа:** [`references/competitive_research_2026.md`](references/competitive_research_2026.md)

---

## v0.8.0 — Habit Loop Framework + Execution Layer v2

**Цель:** Мост между целями и ежедневными действиями через привычки. Закрыть execution layer пробелы, отложенные из v0.7.1.

**Scope:** 6 фич (сокращено с 12 — realistic minor release).

**Входит:**
- [x] **Habit Loop Framework** (`references/habit_loop.md`) — Cue-Routine-Reward + Tiny Habits + Habit Stacking + Timeline (Lally)
- [x] **Task Breakdown with Checkpoints** (`references/action_breakdown_template.md`) — WOOP → шаги с ✓-чекпоинтами
- [x] **Markdown Tables as UI** (`references/markdown_tables.md`) — 4 шаблона, stage-appropriate
- [x] **Weak Goal Taxonomy (full)** (`references/weak_goal_taxonomy.md`) — 5 паттернов + Sanity-Check Framework
- [x] **Status Icon System** (`references/status_icons.md`) — ⬜🔄✅❌⏸️⚠️ + accessibility fallback
- [x] **AGENTS.md overhaul** — актуализация после v0.7.1

**Не входит (отложено в v0.9.0+):**
- Auto-Review Triggers (требует structured session metadata)
- Structured Growth Report (требует re-assessment flow)
- Adaptive Response Length (требует интеграции с Deep Why/Energy Check)
- Calendar Event Copy Review (scope ambiguity)
- Voice-Optimized Output (отложено из v0.9.0, conf 6/10 — ждёт метрики мобильного использования)

**Методики:**
- Tiny Habits (Fogg, 2019)
- Habit Stacking (Clear, 2018)
- Context-Dependent Repetition (Wood & Neal, 2007)
- Habit Timeline (Lally et al., 2010)

---

## v0.9.0 — Мобильная адаптация + Habit Tracker + краткие сессии

**Цель:** Скилл должен работать эффективно на мобильных устройствах, поддерживать отслеживание привычек и давать быстрые инструменты в режиме нехватки времени.

**Scope:** 4 фичи + Dashboard дополнение (streak-логика + mobile responsiveness).

**Приоритеты и порядок работы:**

| Приоритет | Фича | Файл | Зависимости | Описание |
|-----------|------|------|-------------|----------|
| **P0** | **Habit Tracker / Dashboard Streaks** | inline в HTML | — | Визуализация цепочек привычек в дашборде. Streak data model inline в HTML. Связь с `habit_loop.md` (Lally timeline). |
| **P0** | **Mobile Dashboard** | `life-planning-dashboard.html` | Habit Tracker (данные) | Адаптивная вёрстка: 11 сфер Wheel of Life + Habit streaks + mobile responsiveness. BUG-001 (8→11) уже исправлен. |
| **P1** | **5-Minute Micro-Sessions** | `references/micro_sessions.md` | — | Быстрые чек-ины: эмоция → 1 действие. ≤100 строк, opt-in через «у меня 5 минут». Tiny Habits (<30 сек). |
| **P1** | **Quick Decision Protocol** | `references/quick_decision.md` | — | 2–3 вопроса для решения «здесь и сейчас». Интеграция с Communication Style quadrant. |

**Порядок реализации (согласовано):**
1. Habit Tracker / Dashboard Streaks (data model)
2. Mobile Dashboard (CSS поверх готового data model)
3. 5-Minute Micro-Sessions + Quick Decision Protocol (параллельно, независимые reference-файлы)

**Не входит (отложено в v0.9.1+):**
- Voice-Optimized Output (conf 6/10 — ждёт метрики мобильного использования)
- Auto-Review Triggers (требует session metadata persistence)
- Structured Growth Report (требует re-assessment flow)
- Adaptive Response Length (требует интеграции Deep Why + Energy Check)

---

## Advanced Patterns — Research Debt (из AC v0.6, вынесено в v0.7)

Следующие паттерны были удалены из формальных Acceptance Criteria v0.7 как over-engineering для текущей версии, но сохранены как research direction в `references/communication_style.md`:

| Бывший AC | Паттерн | Почему вынесено | Когда вернуть |
|-----------|---------|-----------------|---------------|
| AC-13 | Attachment Style Awareness (4 стиля) | Невозможно протестировать без реальных пользователей; требует психометрии | v0.7+ при расширении Emotional Regulation |
| AC-14 | Dynamic Adaptation Triggers (5+ triggers) | Мета-уровень, покрывается AC-6 (4 квадранта); сложно измерить | v0.8+ при полноценном Habit Loop |
| AC-15 | Goal Ownership Language Rules | Дублирует AC-6/AC-7; лучше как style guide, не AC | Встроить в AC-6 как подпункт при рефакторинге Communication Style |

---

## Идеи без привязки к версии (см. BACKLOG.md)

| Идея | Триггер | Источник |
|------|---------|----------|
| Интеграция с Google Tasks MCP | Когда Tasks API станет доступен через MCP | Пользовательский запрос |
| Голосовые напоминания | Когда Claude.ai добавит голос | Технологический тренд |
| Групповые сессии (парный коучинг) | Когда 5+ пользователей запросят | Пользовательский запрос |
| Интеграция Fitness API (Apple Health, Google Fit) | При расширении сферы «Здоровье» | Расширение Wheel of Life |

---

## Как предложить фичу

1. Проверьте `BACKLOG.md` — возможно, идея уже записана
2. Создайте GitHub Issue с тегом `enhancement`
3. Или напишите в Telegram: [@zagreev](https://t.me/zagreev)

---

## Баг-трекер

Активные баги и известные проблемы — в [BUGS.md](BUGS.md).

## История изменений

Полный список изменений — в [CHANGELOG.md](CHANGELOG.md).
