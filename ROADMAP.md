# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.
> **Как обновлять:** `release.sh` управляет статусом автоматически. Ручное редактирование таблицы запрещено.

---

## Текущий статус

> Факты о выпущенных версиях — в [CHANGELOG.md](CHANGELOG.md). Эта таблица содержит только будущее.

| Версия | Статус | Ожидаемая дата | Ключевая фича |
|--------|--------|----------------|---------------|

---

## История релизов

Полный список выпущенных версий — в [CHANGELOG.md](CHANGELOG.md).

<details>
<summary><strong>v0.7.0 — v0.9.1 (выпущено, кликни для деталей)</strong></summary>

### v0.9.1 — Apple-style Dashboard Redesign
- Activity Rings (SVG), Liquid Glass карточки, Dark/Light mode
- Размер: 1,403 KB → ~61 KB (23× уменьшение)
- Удалены внешние зависимости (ECharts, Chart.js, Font Awesome)

### v0.9.0 — Мобильная адаптация + Habit Tracker
- Habit streaks в дашборде, mobile responsive
- 5-Minute Micro-Sessions, Quick Decision Protocol
- Reward Audit (Dopamine Budget)

### v0.8.0 — Habit Loop Framework + Execution Layer v2
- Habit Loop (Cue-Routine-Reward, Tiny Habits, Habit Stacking)
- Task Breakdown with Checkpoints, Markdown Tables as UI
- Weak Goal Taxonomy + Sanity-Check

### v0.7.1 — Execution Layer Patch
- Win Alert Protocol, Recovery Protocol MVP, Energy-Based Scheduling

### v0.7.0 — Эмоциональная регуляция
- Emotion Regulation Protocol (cognitive reappraisal, grounding, self-compassion)
- Dashboard 8→11 доменов (BUG-001 fix)
</details>

---

## v0.10.0 — Polish & Infrastructure

**Цель:** Закрыть техдолг, упростить релизный процесс, отполировать существующие фичи.

**Scope:**
- [x] **Multi-Platform Skill Adaptation** — Claude.ai, Grok (xAI), Kimi OK Computer. `SKILL.master.md` + overlays + `build-platform-skill.py`. 42+ consistency tests.
- [x] **Kimi Code CLI support** — directory-based skill с `references/` + MCP (v0.10.2)
- [x] **README rewrite + USER_GUIDEs** — 4 platform guides + cross-platform comparison (v0.10.2)
- [x] **E2E behavioral testing** — golden dataset + evaluation rubric (v0.10.2)
- [ ] **CI/CD через GitHub Actions** — автоматический запуск тестов при push/PR
- [ ] **Ревизия текстов событий календаря** — tone check, нет «надо/должен»
- [ ] **Единые Release Notes из CHANGELOG** — генерация из CHANGELOG.md
- [ ] **PDF экспорт дашборда** — кнопка печати/PDF
- [ ] **Архивация старых планов** — перенос plan_v*.md в references/archive/

---

## v0.10.2 — README Rewrite & Kimi CLI (Released)

**Цель:** Исправить катастрофу README.md, добавить Kimi Code CLI как 4-ю платформу, создать полноценную документацию по платформам.

**Выполнено:**
- Полный rewrite README.md — value prop + quick-start + platform table
- Kimi Code CLI: `platforms/kimi-cli/SKILL.md` (323 lines), overlay, MCP support
- 4 USER_GUIDE: Claude, Grok, Kimi OK Computer, Kimi Code CLI
- `CROSS_PLATFORM_COMPARISON.md` — feature matrix + decision tree
- E2E framework: `golden_dataset.json` (20 cases), `evaluation_rubric.md`, `MANUAL_TEST_RUN.md`
- Исправлены BUG-002..BUG-007 (inline refs, heading demotion, dashboard condense)
- Удалён `RETRO_v091_v092.md` из публичного репозитория

---

## Advanced Patterns — Research Debt

Следующие паттерны сохранены как research direction в `references/communication_style.md`:

| Паттерн | Почему вынесено | Когда вернуть |
|---------|-----------------|---------------|
| Attachment Style Awareness (4 стиля) | Невозможно протестировать без реальных пользователей; требует психометрии | v0.11+ при расширении Emotional Regulation |
| Dynamic Adaptation Triggers (5+ triggers) | Мета-уровень, покрывается 4 квадранта; сложно измерить | v0.11+ при полноценном Habit Loop |
| Goal Ownership Language Rules | Дублирует Communication Style; лучше как style guide | Встроить в AC-6 как подпункт |

---

## v0.11.0 — Calendar Intelligence + Chronotype Layer (Audit + Research)

> **Источник 1:** [Audit Report `references/audit/AUDIT_CALENDAR_INTEGRATION.md`](references/audit/AUDIT_CALENDAR_INTEGRATION.md) — 15 gaps, 4 критических.
> **Источник 2:** [Research `references/research/planning_research_2026-05-20.md`](references/research/planning_research_2026-05-20.md) — Идея #1, P0.
> **Цель:** Перевести календарную интеграцию в функциональность + персонализировать время планирования под хронотип.

### P0 (Блокирует релиз)
- [x] **`references/calendar_intelligence.md`** — Pre-flight protocol: `list_events` → density check → conflict detection → smart proposal → `create_event`
- [x] **`references/chronotype_native_planning.md`** — 3 профиля (Жаворонок/Промежуточный/Сова), Peak-Trough-Rebound heuristics, bedtime to-do list
- [x] **Обновить 4 `platforms/*/SKILL.md`** — Phase 5: проверка календаря перед созданием события; Phase 0/1: хронотип-определение
- [x] **Исправить `platforms/kimi/SKILL.md`** — удалить несостоятельный retry protocol, заменить на честный text-only flow (Paper Coach Mode)
- [x] **Исправить dangling references** — `calendar_constants.md` добавлен в `P0_REFS`, platform-neutral wording

### P1 (Обязательно в релиз)
- [ ] **Функциональные тесты календаря** — Free Slot Algorithm, event patterns, conflict detection, JSON validation для COLOR_MAP/REMINDER_PRESETS/RRULE_PRESETS
- [x] **Обновить `references/energy_scheduling.md`** — хронотип-специфичные peak hours
- [x] **Обновить `references/diagnostic_methods.md`** — 2–3 вопроса для определения хронотипа в Phase 0/1
- [ ] **Обновить `build-skill.yml`** — гонить ВСЕ тесты (`pytest tests/`), не только `tests/release`
- [ ] **Провести PoC MCP** — Gate 0–2: OAuth + CRUD + `suggest_time` (заполнить `references/research/mcp_poc_log.md`)

### P2 (Желательно)
- [ ] **Интегрировать `energy_scheduling.md`** с calendar reading (energy peak → free slot search)
- [ ] **User preference для work hours** — вместо hardcoded 9:00–18:00
- [ ] **Kimi-CLI в multi-platform tests** — добавить `"kimi-cli"` в `PLATFORMS`
- [ ] **Timezone intelligence** — определение timezone пользователя, DST handling

---

## v0.12.0 — Behavioral Science Layer

> **Источник:** [Research `references/research/planning_research_2026-05-20.md`](references/research/planning_research_2026-05-20.md) — Идеи #2, #3, #4.
> **Цель:** Сделать планирование привычкой (Habit Stack Builder) и завершить день осознанно (Shutdown Ritual).

### P0
- [x] **`references/habit_stack_builder.md`** — progressive ritual escalation (2→5→10→15 мин), Two-Day Rule, habit anchoring
- [x] **`references/shutdown_ritual.md`** — 5 шагов (Capture→Review→Plan→Celebrate→Close), Zeigarnik elimination, psychological detachment
- [x] **Обновить `references/habit_loop.md`** — ссылка на habit_stack_builder.md

### P1
- [x] **`references/fresh_start_engine.md`** — temporal landmarks (Monday, 1st, New Year, birthday), Fresh Week/Month/Year triggers, dark side protection

---

## v0.13.0 — Smart Scheduling Layer

> **Источник:** [Research `references/research/planning_research_2026-05-20.md`](references/research/planning_research_2026-05-20.md) — Идеи #5, #6, #7.
> **Цель:** Защитить пользователя от перегрузки и оптимизировать расписание через данные.

### P0
- [ ] **`references/workload_warning.md`** — суммирование запланированного времени, threshold (default 6ч), warning message
- [ ] **Обновить `references/energy_scheduling.md`** — self-reported 1–10 scale, pattern learning, smart suggestions

### P1
- [ ] **`references/calendar_pattern_analyzer.md`** — meeting load %, chronotype alignment, boundary violations, recovery deficit, trends (MCP read-only)

---

## v0.14.0 — Inclusive Coaching Layer

> **Источник:** [Research `references/research/planning_research_2026-05-20.md`](references/research/planning_research_2026-05-20.md) — Идеи #8, #9, #10.
> **Цель:** Адаптировать коучинг под недообслуживаемые аудитории.

### P0
- [ ] **`references/adhd_mode.md`** — micro-tasking, body doubling prompts, visual timer, time blindness protection, external scaffolding (opt-in)
- [ ] **`references/time_structure_unemployed.md`** — daily structure template, purpose exploration, social activities, small wins

### P1
- [ ] **`references/planning_friction_audit.md`** — smart defaults, template library (Deep Work/Meeting/Recovery day)

---

## R&D — Future Lab

> **Источник:** [Research `references/research/planning_research_2026-05-20.md`](references/research/planning_research_2026-05-20.md) — Идеи #11, #12.
> **Статус:** Не в ROADMAP до срабатывания триггера.

| Идея | Триггер |
|------|---------|
| Body Doubling via AI | Retention проблема становится критичной |
| Wearable Energy Integration | Wearable MCP servers становятся stable |

---

## Идеи без привязки к версии (см. BACKLOG.md)

| Идея | Триггер | Источник |
|------|---------|----------|
| Интеграция с Google Tasks MCP | Когда Tasks API станет доступен через MCP | Техническое ограничение |
| Голосовые напоминания | Когда Claude.ai добавит голос | Технологический тренд |
| Групповые сессии (парный коучинг) | Когда 5+ пользователей запросят | Пользовательский запрос |
| Интеграция Fitness API (Apple Health, Google Fit) | При расширении сферы «Здоровье» | Расширение Wheel of Life |
| Мультиязычность (EN/RU toggle) | 10+ запросов от англоязычных пользователей | Потенциал open source |

---

## Как предложить фичу

1. Проверьте `BACKLOG.md` — возможно, идея уже записана
2. Создайте GitHub Issue с тегом `enhancement`
3. Или напишите в Telegram: [@zagreev](https://t.me/zagreev)

---

## Баг-трекер

Активные баги и известные проблемы — в [BUGS.md](BUGS.md).
