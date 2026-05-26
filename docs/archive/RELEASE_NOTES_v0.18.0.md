## Что нового в v0.18.0 — Gating + State Writes + Compass Mode

Замыкание operational контракта между skill и state v2 после декомпозиции v0.17.0. Каждая фаза знает что писать в state; gating запускается явно по детекту коннекторов на старте сессии; Core Values flow проходит весь PRD включая **Compass Mode (FR-04)** — практическое применение ценностей в daily decisions.

### Added

- **Schema 2.0.1** (`references/state_v2_schema.md`) — additive bump:
  - `session.gating_mode` field — отслеживание текущего режима (`full_persistence` / `wiki_no_execution` / `execution_no_wiki` / `lean_conversation`) для observability и migration check
  - §12 Changelog схемы с историей версий
  - §11 ссылки на v0.18.0 тесты
- **Compass Mode (FR-04)** в `references/module_phase1_5_goal_filter.md` (~150 слов inline):
  - **Compass Questions** (по 1 на ценность) — «Расширяет ли этот выбор моё [name], или сужает?»
  - **Daily Decision Protocol** (Pause → Compass question → Decision, ≤ 60 сек)
  - **Alignment Audit** в Weekly Review (ссылка на `references/templates/Core_Values_Compass.md`)
  - **Link с Authentic Goal Filter**: `core_values_alignment[]` обязателен ≥ 1 элемент при добавлении цели
- **State write rules** в каждом `module_phase*.md` (закрытие 7 ⚠ gap-ов из state_v2_schema.md §9):
  - Phase 1 — `persona.active_mode` (после detection), `emotion_regulation_log[]` (после Phase 0.5 ER), полные `diagnosis.*` writes
  - Phase 1.5 — `core_values[]` с `derived_from`/`compass_question`, `core_values_alignment[]` link, `goal_filter.{paused_goals,patterns}[]`
  - Phase 2 — полный Habit Loop (`cue/routine/reward/anchor/tiny_version/sphere_id`)
  - Phase 3 — `wins_log[]` first-class (step 5 Celebration), `reward_audit_results[]` (optional step 7), habit status update
  - Phase 5 — `calendar_events_log[]` (mode A connector + mode B paper), `daily_top3_log[]`, `recovery_sessions_log[]`, pending_events для retry
- **`tests/unit/test_v018_gating_state_writes.py`** — 31 тест:
  - Schema 2.0.1 + gating_mode field validation
  - Master gating trigger algorithm + bootstrap + backfill triggers
  - State writes per phase (закрытие 7 ⚠ gap-ов)
  - Phase 1.5 Compass Mode + Daily Decision Protocol structure
  - AI_Instructions write-rules table complete
  - §9 gap matrix resolution check (no remaining ⚠️)
  - Per-module budget preservation

### Changed

- **`SKILL.master.md`** §3 Persistence Mode (master = 4000 tokens, на пределе budget):
  - **Trigger algorithm** в pseudocode: `on session_start: detect → match mode → write gating_mode`
  - **Bootstrap trigger**: `drive_connected && !wiki_bootstrapped` → `templates/AI_Instructions.md §Bootstrap`
  - **Backfill trigger** (mid-session): `previous_mode in [lean_conversation, execution_no_wiki] && !backfill_offered` (single-fire) → `templates/AI_Instructions.md §Backfill`
  - Examples переписаны компактнее (2 примера в одну строку каждый), gotchas/troubleshooting сжаты для budget
- **`references/state_v2_schema.md` §9 Field availability matrix** — все 7 ранее ⚠ полей теперь ✅ с указанием модуля-источника write-rule. Добавлен `session.gating_mode` row.
- **`references/templates/AI_Instructions.md`**:
  - Frontmatter 2.0 → 2.0.1
  - §Gating расширен trigger algorithm и явным `write session.gating_mode`
  - Write rules table расширена строками для `gating_mode`, `core_values_alignment`, `recovery_sessions_log`, `persistence_retry.*`
- **`tests/unit/test_templates_v2.py`** — `test_schema_version_is_2_0` и `test_all_templates_have_schema_version` переведены на semver regex (принимают `2.0`, `2.0.1`, `2.1`, etc.)
- **Platform builds** пересобраны для v0.18.0:
  - `platforms/claude/SKILL.md`: 196 строк, 1547 слов
  - `platforms/grok/SKILL.md`: 1060 строк, 8473 слова
  - `platforms/kimi/SKILL.md`: 723 строки, 5954 слова
  - `platforms/kimi-cli/SKILL.md`: 201 строка, 1624 слова

### Fixed

- Compass Mode artifacts ранее существовали только в `templates/Core_Values_Compass.md`, но Phase 1.5 module на него не ссылался — теперь скилл проходит весь PRD FR-01..FR-06.
- Все 7 ранее ⚠ полей в state schema теперь имеют explicit write-trigger в соответствующем module_phase*.md + write-rule в `AI_Instructions.md`.
- Module Phase 1.5 (Compass Mode добавлен) и Phase 5 (recovery_sessions_log добавлен) сначала превысили per-module budget — урезаны до ≤ 2500 tokens без потери семантики.

### Roadmap progress

✅ **Gating logic** — реализован в `SKILL.master.md §3` + `templates/AI_Instructions.md §Gating`
✅ **State write rules** — emotion_regulation_log, persona, wins, reward_audit, calendar_events, recovery_sessions, core_values_alignment
✅ **Bootstrap Drive Wiki** — trigger в master + protocol в `AI_Instructions.md §Bootstrap`
✅ **Backfill prompt** — trigger в master + single-fire logic в `AI_Instructions.md §Backfill`
✅ **Core Values Discovery flow** — PRD FR-01..FR-06 покрыт (Compass Mode добавлен)

### Acceptance criteria

- ✅ Schema bumped 2.0 → 2.0.1 (additive), backward compat: 2.0 doc парсится 2.0.1 клиентом
- ✅ Все 7 ⚠ gap-ов из state_v2_schema.md §9 закрыты
- ✅ Cold-load budget: SKILL.master.md = 4000 tokens (≤ 4000), все 6 phase modules ≤ 2500 tokens
- ✅ Phase 1.5 содержит Compass Mode секцию (FR-04 из `docs/research/prd_core_values_discovery.md`)
- ✅ 31 новых теста в `tests/unit/test_v018_gating_state_writes.py` (все pass)
- ✅ Все 4 платформы пересобраны
- ✅ 475 passed total (444 baseline + 31 new), известные release-flow failures (working tree / version vs tag) разрешатся после tag

### Что дальше

- **v0.19.0** — Health & Metabolism Track (schema bump 2.1) + Goal Concordance (schema bump 2.2)
- **v1.0.0** — Build pipeline rework + platform lazy-loading для Claude.ai + polish
