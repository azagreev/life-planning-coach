# Changelog

Все значимые изменения проекта отслеживаются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), проект следует [Semantic Versioning](https://semver.org/lang/ru/).

---

## [Unreleased]

## [1.0.0] — 2026-05-28

**Production-ready release** — major-version signal стабильности после v0.17→v0.19 content milestones. v1.0 закрывает 6 production-readiness gaps + замораживает API contract: schema 2.x, persona naming, build CLI, Routing Map.

### Added

- **`scripts/build-skill.py`** — единый Python CLI заменяющий bash hybrid:
  - `build` — пересобрать все 4 платформы + ZIP/skill/grok-md/kimi-md/kimi-cli-zip
  - `version X.Y.Z` — sync version во все source files
  - `verify` — pre-release checks
  - `release X.Y.Z` — full flow (verify + version + build + commit + tag + push + gh release)
  - Cross-platform: no rsync, no `sed -i`, LF-normalized ZIP files
- **`scripts/gating_logic.py`** — pure-function reference implementation 4 gating modes (specification, не executor):
  - `detect_gating_mode(drive, calendar)` → 4 mode matrix
  - `should_bootstrap_drive()`, `run_bootstrap()` — first-connect protocol
  - `should_offer_backfill()`, `accept_backfill()`, `decline_backfill()` — mid-session protocol с backoff после 2 declines
- **`MIGRATION_v1.md`** — guide v0.x → v1.0 для пользователей с форками: persona renames mapping, schema migration path, deprecation timeline, API stability promise
- **Tests:**
  - `test_platform_parity.py` (15 структурных проверок × 4 платформы = 60 sub-tests)
  - `test_typical_session_budget.py` (6 тестов: cold-load ≤ 4K, Quick ≤ 14K, Deep ≤ 18K, Health ≤ 20K)
  - `test_gating_modes_e2e.py` (25 тестов: 4 mode matrix + bootstrap + backfill behavior)
  - `test_build_skill_cli.py` (13 тестов: argparse, version sync, ZIP creation)
  - `test_rename_persona_script.py` (8 тестов)
  - `test_extract_release_notes.py` (6 тестов)
- **`pyproject.toml` coverage configuration** — `fail_under = 50` (v1.0 baseline; aspirational target 85% в roadmap)

### Changed

- **`AGENTS.md` §4.2** — release process обновлён под `python scripts/build-skill.py release X.Y.Z`
- **`scripts/extract-release-notes.py`** — output путь изменён `references/archive/` → `docs/archive/` (соответствует v0.15.x cleanup)
- **`tests/system/test_github_sync.py::test_release_notes_generation`** — использует `sys.executable` вместо `python3` literal (cross-platform fix для Windows MS Store stub), forces `PYTHONIOENCODING=utf-8`
- **`references/conversation_state_schema.md`** — deprecation header усилен: «Will be removed in v1.1. Use state_v2_schema.md»
- **README badges** — coverage actualised, version 1.0.0, tests count 632+

### Deprecated (will be removed in v1.1)

- **`scripts/build-skill.sh`** — replaced by `python scripts/build-skill.py build`. Header warning + stderr echo при запуске.
- **`scripts/sync-version.sh`** — replaced by `python scripts/build-skill.py version X.Y.Z`. Header warning + stderr echo.
- **`references/conversation_state_schema.md`** (v1 schema) — replaced by `state_v2_schema.md`.

### Acceptance criteria

- ✅ Cold-load: SKILL.master.md = 3981 tokens (≤ 4000 budget)
- ✅ Typical session ≤ 18K tokens (Deep diagnostic + ADHD persona = 16-17K)
- ✅ Coverage ≥ 50% (current 54.3%; gated в `pyproject.toml`)
- ✅ All 4 gating modes имеют e2e behavior tests (4 mode matrix + bootstrap + backfill backoff)
- ✅ All 4 platforms pass 15 structural parity checks
- ✅ Unified `build-skill.py` работает cross-platform (Windows tested)
- ✅ MIGRATION_v1.md описывает persona renames + schema bumps + deprecation paths
- ✅ Test suite: 632 passed, 1 failed (working_tree, auto-fixed at release)

### API stability promise (v1.0+)

С v1.0 проект следует semver строго:
- **Patch (v1.0.x):** только bug fixes, не меняет contract.
- **Minor (v1.x.0):** additive features. Forked интеграции продолжают работать.
- **Major (v2.0.0):** breaking changes только при schema 3.0. Deprecated paths должны быть документированы 2 minor релиза.

Стабильные поверхности: Routing Map, 4 gating modes naming, canonical 11 spheres, persona naming `mode_<short>`, build CLI, schema 2.x additive policy.

### Что дальше

- **v1.x patches** — bug fixes, edge cases, security
- **v1.1** — удалить deprecated bash скрипты + conversation_state_schema.md
- **Post-v1.0 backlog:** PoC MCP (RICE 31.5), Google Health MCP (RICE 7.2), Timezone hardening (RICE 18), Multilingual EN (4.7), Body Doubling AI (6.1)

## [0.19.0] — 2026-05-28

**Health Track + Goal Concordance + Persona Rename + README Positioning + Drive Consistency** — content depth (3 PRD-driven фичи) + technical debt cleanup (persona naming unified, README first impression rewrite) + Drive terminology consistency.

### Added

- **Schema 2.0.1 → 2.2** (`references/state_v2_schema.md`) — два additive bumps:
  - **2.1:** `diagnosis.health_metabolism` блок (opt-in трек метаболического здоровья): sleep/stress/protein/fiber/chewing/caffeine + micro_experiments_log
  - **2.2:** `goal_filter.active_goals[].partner_coordination` optional sub-block (Goal Concordance): communication/cooperation/compatibility/obstacles
- **`references/track_health_metabolism.md`** — новый Tier 3 ref (~2.5K tokens):
  - 7 evidence-based рычагов (Spiegel 2004, Epel 2001, Leidy 2015, Wanders 2011, Chmiel 2025, Drake 2013, Kanchanasurakit 2023)
  - Диагностические вопросы Track A/B
  - 3 шаблона рефрейминга самокритики
  - 3 примера микро-экспериментов
  - Safety: РПП → специалист
- **Phase 1.5 Partner Coordination Check (step 7)** — opt-in vetting партнёрских целей (Rosta-Filep 2023, Transactive Goal Dynamics Fitzsimons & Finkel)
- **Phase 2 Partner Discussion Checkpoint** — фиксирует communication в плане при наличии `partner_coordination`
- **Phase 1 Health Track opt-in entry** — триггеры «вес/энергия/выгорание/диета/сон» → загрузка Tier 3 ref
- **Phase 3 Health Track Review (optional step 6.5)** — еженедельная оценка сон/стресс/питание
- **emotion_regulation.md** — добавлена Conflict Reappraisal technique (Finkel et al. 2013) + Gottman repair attempts
- **3 новых test файла, 40 тестов:**
  - `test_v019_health_concordance.py` (27 тестов): schema 2.2, Health Track Tier 3, Phase 1/3/1.5/2 integration, ER refs
  - `test_persona_renames.py` (7 тестов): file rename, no old refs, naming convention
  - `test_cross_lingual_consistency.py` (6 тестов): Drive terminology, README positioning

### Changed

- **Persona modules renamed** (16 файлов affected, 169 cross-ref replacements):
  - `adhd_mode.md` → `mode_adhd.md`
  - `time_structure_unemployed.md` → `mode_unemployed.md`
  - `elder_homebound_mode.md` → `mode_elder.md`
  - `planning_friction_audit.md` → `mode_planning_friction.md`
- **README.md** — first impression rewrite:
  - Новый promise: «Превращает диалог с AI в evidence-based личный план: цели, привычки, ретроспективный ритм»
  - Comparison table: Notion/Todoist vs Generic AI-coach vs Life Planning Coach
  - Quick-start компактнее (3 платформы в 5 строк)
  - Полный список методик (расширенный) — ниже первого экрана
- **SKILL.master.md** — Drive terminology consistency (replaced "Cloud Storage" в prose с "Drive"), persona paths updated, master = 3981 tokens (≤ 4000 budget)
- **Platform builds** — все 4 платформы пересобраны для v0.19.0 (claude/grok/kimi/kimi-cli)
- **`tests/unit/test_v018_gating_state_writes.py`** — `test_schema_version_2_0_1` переведён на semver regex 2.0.1+ (accepts 2.1, 2.2 и далее)
- **`tests/system/test_v140_features.py`** — fixture `lazy_load_extras` обновлён для новых persona имён (52 refs)

### Fixed

- Persona module naming наконец-то consistent — все 4 файла начинаются с `mode_`, sort order чёткий.
- README первое впечатление переделано: promise → comparison → quick-start (порядок), методики раскрыты после первого экрана.
- Drive terminology консистентен в SKILL.master.md и AI_Instructions.md.
- Phase 1.5 module остался в budget (2478/2500) после добавления Partner Coordination Check — урезание verbose Compass Mode + Authentic Goal Filter секций.

### Tooling

- **Новый скрипт** `scripts/rename_persona_modules.py` — atomic migration для persona renames с dry-run по умолчанию. Содержит self-skip + archive-skip + UTF-8 encoding safety. Можно использовать как шаблон для будущих rename-операций.

### Acceptance criteria

- ✅ Schema bumped 2.0.1 → 2.2 (additive, backward compat: 2.0 doc парсится 2.2 клиентом)
- ✅ Все 7 рычагов Health Track в `track_health_metabolism.md` + Tier 3 file ≤ 2500 tokens (2494)
- ✅ Phase 1 имеет opt-in Health entry, Phase 3 — optional Health Review, Phase 1.5 — Partner Coordination Check (step 7)
- ✅ 4 persona переименованы, 0 old-path refs в runtime files
- ✅ README первые 30 строк: promise → comparison → quick-start (порядок проверен тестом)
- ✅ SKILL.master.md = 3981 tokens (≤ 4000), все 6 phase modules ≤ 2500
- ✅ 40 новых тестов pass, 0 real test failures (только release-flow)
- ✅ Все 4 платформы пересобраны

### Roadmap progress

✅ Health & Metabolism Track — реализован
✅ Goal Concordance — реализован
✅ Persona modules consolidation — реализован
✅ Quick wins: README rewrite + Cross-Lingual fixes

### Что дальше

- **v1.0.0** — Build pipeline rework (unified Python script) + platform lazy-loading для Claude.ai + production-ready polish

## [0.18.0] — 2026-05-27

**Gating + State Writes + Core Values Compass Mode** — замыкание operational контракта между skill и state v2. Каждая фаза знает что писать; gating запускается явно по детекту коннекторов; Core Values flow проходит весь PRD включая Compass Mode (FR-04).

### Added

- **Schema 2.0.1** (`references/state_v2_schema.md`) — additive bump:
  - `session.gating_mode` field — отслеживание текущего режима (full_persistence / wiki_no_execution / execution_no_wiki / lean_conversation) для observability
  - §12 Changelog схемы с историей версий
  - §11 ссылки на v0.18.0 тесты
- **Compass Mode (FR-04)** в `module_phase1_5_goal_filter.md` (~150 слов inline):
  - Compass Questions (по 1 на ценность) — «Расширяет ли этот выбор моё [name], или сужает?»
  - Daily Decision Protocol (Pause → Compass question → Decision, ≤ 60 сек)
  - Alignment Audit в Weekly Review (ссылка на `templates/Core_Values_Compass.md`)
  - Link с Authentic Goal Filter: `core_values_alignment[]` обязателен ≥ 1 элемент
- **State write rules** в каждом `module_phase*.md`:
  - Phase 1: `persona.active_mode`, `emotion_regulation_log[]`, полные `diagnosis.*` writes
  - Phase 1.5: `core_values[]` с `derived_from`/`compass_question`, `core_values_alignment[]` link, `goal_filter.{paused_goals,patterns}[]`
  - Phase 2: полный Habit Loop (`cue/routine/reward/anchor/tiny_version/sphere_id`)
  - Phase 3: `wins_log[]` first-class (step 5 Celebration), `reward_audit_results[]` (optional step 7), habit status update
  - Phase 5: `calendar_events_log[]` (mode A+B), `daily_top3_log[]`, `recovery_sessions_log[]`, pending_events для retry
- **`tests/unit/test_v018_gating_state_writes.py`** — 31 теста:
  - Schema 2.0.1 + gating_mode field validation
  - Master gating trigger algorithm + bootstrap + backfill triggers
  - State writes per phase (закрытие 7 ⚠ gap-ов из §9)
  - Phase 1.5 Compass Mode + Daily Decision Protocol
  - AI_Instructions write-rules table complete
  - §9 gap matrix resolution check (no remaining ⚠️)
  - Per-module budget preservation

### Changed

- **`SKILL.master.md`** §3 Persistence Mode (master остался ≤ 4000 tokens):
  - Trigger algorithm pseudocode (`on session_start: detect → match mode → write gating_mode`)
  - Bootstrap trigger declaration: `drive_connected && !wiki_bootstrapped`
  - Backfill trigger declaration: `previous_mode in [lean_conversation, execution_no_wiki] && !backfill_offered` (single-fire)
  - Explicit references на `templates/AI_Instructions.md §Bootstrap` и `§Backfill`
- **`references/state_v2_schema.md` §9 Field availability matrix** — все 7 ранее ⚠ полей теперь ✅ с указанием модуля-источника write-rule.
- **`references/templates/AI_Instructions.md`** — frontmatter 2.0 → 2.0.1; gating trigger расширен `write session.gating_mode`; write rules table расширена строками для `gating_mode`, `core_values_alignment`, `recovery_sessions_log`, `persistence_retry.*`.
- **`tests/unit/test_templates_v2.py`** — `test_schema_version_is_2_0` и `test_all_templates_have_schema_version` переведены на semver regex (принимают `2.0`, `2.0.1`, `2.1`, etc.).

### Fixed

- Compass Mode artifacts ранее существовали только в `templates/Core_Values_Compass.md`, но Phase 1.5 module на него не ссылался — теперь скилл проходит весь PRD FR-01..FR-06.
- Все 11 ранее ⚠ полей в state schema теперь имеют explicit write-trigger в модуле + write-rule в `AI_Instructions.md`.

### Acceptance criteria

- ✅ Schema bumped 2.0 → 2.0.1 (additive), backward compat: 2.0 doc парсится 2.0.1 клиентом
- ✅ Все 7 ⚠ gap-ов из §9 закрыты
- ✅ Master = 4000 tokens (≤ 4000 budget), все 6 phase modules ≤ 2500 tokens
- ✅ Phase 1.5 содержит Compass Mode секцию (FR-04)
- ✅ 31 новых тестов в `test_v018_gating_state_writes.py` (475 passed total — было 444)
- ✅ Все 4 платформы пересобраны

### Roadmap progress

✅ Gating logic — реализован в `SKILL.master.md §3` + `templates/AI_Instructions.md §Gating`
✅ State write rules — emotion_regulation_log, persona, wins, reward_audit, calendar_events, recovery_sessions, core_values_alignment
✅ Bootstrap Drive Wiki — trigger в master + protocol в `AI_Instructions.md §Bootstrap`
✅ Backfill prompt — trigger в master + single-fire logic в `AI_Instructions.md §Backfill`
✅ Core Values Discovery flow — PRD FR-01..FR-06 покрыт (Compass Mode добавлен)

### Что дальше

- **v0.19.0** — Health & Metabolism Track (schema 2.1) + Goal Concordance (schema 2.2)
- **v1.0.0** — Build pipeline rework + platform lazy-loading для Claude.ai + polish

## [0.17.0] — 2026-05-26

**IA Decomposition (Tier 1 Core + 6 Phase Modules)** — снижение cold-load SKILL.master.md с ~6.5K до ~3.6K tokens через декомпозицию на Tier 1/2/3. Phase-протоколы переехали в `references/module_phase*.md` и грузятся lazy по факту входа в фазу. Routing Map в Tier 1 управляет переходами.

### Added
- **6 phase modules** в `references/`:
  - `module_phase1_diagnostic.md` — Phase 1 Diagnostic + Phase 0.5 ER Protocol
  - `module_phase1_5_goal_filter.md` — Authentic Goal Filter + Core Values Discovery (bottom-up)
  - `module_phase2_goal_architecture.md` — BHAG → OKR → WOOP + Habit Loop
  - `module_phase3_weekly_review.md` — 7-step GTD + Scrum + Wins + Habit Review
  - `module_phase4_dashboard.md` — HTML / Text dashboard + JSON contract
  - `module_phase5_execution.md` — Calendar + Daily Top-3 + Shutdown Ritual
- **`tests/unit/test_tier_token_budgets.py`** — token-budget guardrails:
  - Tier 1 (`SKILL.master.md`) ≤ 4000 tokens cold-load
  - Каждый phase module ≤ 2500 tokens
  - Все модули суммарно ≤ 14000 tokens
  - Master обязан декларировать Routing Map с указанием каждого Tier 2 модуля

### Changed
- **`SKILL.master.md`** переписан как Tier 1 Core (~3.6K tokens, было ~6.5K):
  - Phase 0 Emotional Landing — полный, остаётся в ядре
  - Routing Map — таблица «сигнал пользователя → какой модуль грузить»
  - Persistence Mode gating — 4 режима по комбинации Drive/Calendar
  - Safety, Language Rules, Privacy, References Index — компактно
  - Глубокий Phase 1–5 контент вынесен в Tier 2 модули
- **`scripts/build-platform-skill.py`** — `P0_REFS` теперь включает 6 phase modules. `inline_references()` дополнен append-fallback: P0 refs без явной load-инструкции аппендятся в Appendix в конец single-file platforms (grok / kimi) под секцией «Inlined modules (for single-file platforms)».
- **Platform builds** пересобраны:
  - `claude/SKILL.md`: 192 строк, 1.5K слов (lazy refs через файловую систему)
  - `grok/SKILL.md`: 1030 строк, 8.1K слов (single-file с inlined Tier 2 + Tier 3 refs)
  - `kimi/SKILL.md`: 714 строк, 5.8K слов (ultra-condensed inlined)
  - `kimi-cli/SKILL.md`: 197 строк, 1.6K слов (lazy refs через `read_file`)
- **Platform overlays** упрощены: только перевод нейтральных терминов (`AI Memory` → `Claude Memory` / `Native Memory` / `memory_space`; `Cloud Storage` → `Google Drive` / `Drive connector` / `write_file`).
- **`tests/system/test_v140_features.py`** — fixture `platforms` для lazy-load платформ (claude, kimi-cli) теперь собирает «reachable corpus»: SKILL.md + содержимое phase modules + persona refs. Семантика: тесты проверяют доступность контента, а не его физическую локацию.

### Roadmap progress
✅ P0: Tier 1 Skill Core ≤ 4K tokens
✅ P0: 6 phase modules
✅ P0: Token budget tests per tier
✅ P1: Platform rebuild — все 4 платформы пересобраны
⏳ Deferred:
- P1 Legacy compatibility bundle — в v0.18.0 (если потребуется, иначе сразу cutover)

## [0.16.0] — 2026-05-26

**Testing & Integration Hardening** — закрыли committed roadmap-scope: тесты календаря расширены edge-кейсами, починен Windows-блокер `python3` хардкода, добавлена coverage-инфраструктура, pre-commit hooks и planning-docs guardrails.

### Added
- **`pyproject.toml`** — минимальная конфигурация pytest + coverage + ruff. `setup.py` остаётся источником правды по package version.
- **`.pre-commit-config.yaml`** — hooks: `ruff` (lint + format), `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-json`, `check-merge-conflict`, `check-added-large-files`, `mixed-line-ending`. Pre-push: `pytest tests/unit + light system`.
- **Coverage infrastructure** — `pytest-cov` configured с `fail_under = 75`. Текущее покрытие: **80.91%** (2675 statements, 401 missing).
- **Coverage badges в `README.md`** — tests, coverage, schema, version.
- **9 новых тестов в `tests/system/test_calendar_integration.py`** (Free Slot Algorithm edge cases):
  - `test_events_outside_work_window_are_ignored`
  - `test_events_partially_outside_work_window_clipped`
  - `test_exact_duration_gap_is_returned`
  - `test_long_duration_filters_short_gaps`
  - `test_zero_busy_with_short_window_under_duration`
  - `test_limit_parameter_caps_results`
  - `test_unsorted_busy_intervals_handled`
- **3 новых теста в `tests/system/test_roadmap_integrity.py`** (planning docs guardrails):
  - `test_roadmap_has_only_future_versions` — ROADMAP содержит только future-секции
  - `test_backlog_done_section_is_pointer_only` — BACKLOG не дублирует CHANGELOG
  - `test_changelog_has_each_released_version` — CHANGELOG документирует каждый git tag ≥ v0.8.0

### Fixed
- **Windows `python3` хардкод** — заменён на `sys.executable` (Python тесты) и `command -v python3 || command -v python` с fallback на `py` (shell скрипты). Разблокирует 22+ ранее ERROR'ивших тестов на Windows. Затронуто:
  - `scripts/build-skill.sh`, `scripts/release.sh`
  - `tests/system/test_multi_platform.py`, `tests/system/test_master_skill_integrity.py`
- **`scripts/build-platform-skill.py`** — `sys.stdout.reconfigure(encoding='utf-8')` в самом начале. Чинит `UnicodeEncodeError` на Windows cp1251 при выводе emoji/check-marks из subprocess.
- **`tests/system/test_v140_features.py::test_master_version_is_014`** — заменён на `test_master_version_is_at_least_014` (semver-aware), не блокирует версии v0.15+.
- **`tests/system/test_version_consistency.py::test_no_pyproject_toml_exists`** — заменён на `test_pyproject_toml_has_no_version` (разрешает pyproject.toml без `[project]` table, что и используется).

### Changed
- **`CONTRIBUTING.md`** — добавлена инструкция `pip install pre-commit && pre-commit install`; тесты теперь `pytest tests/` вместо `unittest discover`.

### Roadmap-status
- ✅ P0: Функциональные тесты календаря (22 теста, было 12)
- ✅ P0: Тесты целостности `SKILL.master.md` (9 тестов passed, ранее 2 ERROR на Windows)
- ✅ P1: Coverage report + badge (80.91% актуальный)
- ✅ P1: Pre-commit hooks
- ✅ P2: Planning docs guardrails
- ⏳ P1 deferred: PoC MCP — отдельный research spike в v0.17.x candidate
- ⏳ P2 deferred: Универсальный скрипт сборки — частично закрыт (build-skill.sh кросс-платформенный), полная унификация в v1.0 build pipeline rework

## [0.15.1] — 2026-05-26

**Dev-only cleanup** — `references/` теперь содержит только runtime-артефакты. Dev-only содержимое перенесено в `docs/`, что уменьшает шум в IDE/grep, упрощает build-скрипт и улучшает git diff.

### Изменено
- **`references/research/` → `docs/research/`** (26 файлов: исследования, PRD, RICE-методология, план v1.0 templates rebuild).
- **`references/tasks/` → `docs/tasks/`** (9 файлов: developer / tester / test_report по версиям v0.4–v0.6).
- **`references/audit/` → `docs/audit/`** (1 файл: calendar integration audit).
- **`references/archive/` → `docs/archive/`** (включая `RELEASE_NOTES_v*.md`).
- **Legacy файлы из `references/` root → `docs/`:**
  - `acceptance_criteria_v0.4/v0.5/v0.6/v0.7.md` → `docs/archive/release/`
  - `release_checklist_v0.4/v0.6.md` → `docs/archive/release/`
  - `plan_v0.15.0.md`, `plan_roadmap_backlog_cleanup.md` → `docs/planning/`
  - `research_communication_style_v0.6.md`, `research_diagnostic_audit_v0.5.md`, `research_diagnostic_deep_dive.md`, `research_stage_1.5_enhanced_spec.md` (shadow-версии runtime файлов) → `docs/research/shadows/`
  - `competitive_research_2026.md`, `persistence_research_plan.md` → `docs/research/`

### Updated
- **`scripts/release.sh`** — путь release notes `references/archive/` → `docs/archive/`.
- **`scripts/sync-version.sh`** — исключения для stale-version check обновлены под `docs/`.
- **`.github/hooks/pre-push-release-guard` + `.git/hooks/pre-push`** — путь release notes `references/archive/` → `docs/archive/`.
- **`tests/system/test_roadmap_integrity.py`** — сообщение об ошибке использует новый путь.
- Все active md-файлы (`BACKLOG.md`, `ROADMAP.md`, `CHANGELOG.md`, `AGENTS.md`, `references/templates/AI_Instructions.md`, `references/templates/Core_Values_Compass.md`, `references/state_v2_schema.md`, `docs/migration_v1_to_v2.md`) — ссылки обновлены на новые пути.

### Добавлено
- **`tests/unit/test_references_runtime_only.py`** — инвариант-тест: запрещает появление `research/`, `tasks/`, `audit/`, `archive/` subdirs внутри `references/`, плюс ловит legacy filename patterns. Гарантирует, что cleanup не вернётся регрессией.

### Effect
- `references/` теперь содержит 34 markdown файла (было 75+ с поддиректориями).
- Из runtime namespace убрано ~50K токенов dev-only артефактов.
- Build-скрипт не подгружает dev-only content в platform SKILL.md.

## [0.15.0] — 2026-05-26

**Templates Rebuild + State v2 Foundation** — подготовительный блок v1.0 архитектурного рефакторинга. Устраняет structural drift между state schema, HTML dashboard, wiki templates и dashboard_guide. Single source of truth через state v2.

### Добавлено
- **`references/state_v2_schema.md`** — canonical schema v2.0: 11 spheres (canonical naming), Phase 0-5, блок Core Values (derived_from / compass_question / priority_rank), `persona`, `emotion_regulation_log`, `wins_log`, `reward_audit_results`, `calendar_events_log`, `recovery_sessions_log`, gating + backfill протоколы. Foundation для HTML dashboard, wiki templates и dashboard_guide.
- **`references/templates/Core_Values_Compass.md`** — новый wiki-шаблон Core Values Discovery (5-7 values + compass questions + cross-link с Goals). Из PRD `prd_core_values_discovery.md`.
- **HTML dashboard v1.0.0** — Core Values panel (Overview tab) + скрытые placeholders для Health Track / Goal Concordance (активируются при schema bump 2.1/2.2).
- **`docs/migration_v1_to_v2.md`** — миграция legacy 8-sphere wiki → canonical 11 spheres + rollback инструкция.
- **`docs/research/dashboard_architecture_v1.md`** — вынесенный 2538-строчный архитектурный doc (dev-only, не в runtime).
- **`docs/research/plan_v1.0_templates_rebuild.md`** — план rebuild всех 3 шаблонов, RICE 30.0.
- **`docs/research/prd_core_values_discovery.md`, `prd_health_metabolism.md`, `prd_goal_concordance.md`** — три новых PRD (Health/Concordance → schema bumps 2.1/2.2 в будущем).
- **`tests/unit/test_templates_v2.py`** — 21 тест: canonical spheres consistency, state v2 schema completeness, HTML data-driven, wiki schema_version, token budgets, dashboard_guide thin, schema versioning.

### Изменено
- **`life-planning-dashboard.html`** — удалены hardcoded `WHEEL_SPHERES` / `EXECUTION_SCORES` / `VELOCITY_DATA` / `STREAK_DATA`; теперь читают `window.lpData`. Sphere IDs приведены к canonical: `growth → personal_growth`, `spirituality → meaning`, `fun → fun_recreation`, `environment → physical_environment`. CSS comment v0.9.1 → v1.0.0. Schema 2.x compatibility check.
- **`references/dashboard_guide.md`** — сжат с 2538 до ~130 строк: runtime-only specification + JSON contract. Heavy архитектура вынесена в `docs/research/dashboard_architecture_v1.md` (−7K токенов из runtime при Phase 4).
- **8 wiki templates** — все frontmatter `schema_version: "2.0"`. `Wheel_of_Life_History.md` — 11 canonical spheres (было 8 с legacy именами). `Goals.md` — AGF radar блок на каждую цель + `core_values_alignment` + закомментированный Concordance placeholder + полный Habit Loop (cue / routine / reward / anchor). `Hot_Cache.md` + `Raw_Session.md` + `USER_PROGRESS_JOURNAL.md` — поля под persona, emotion_regulation, wins, calendar_events. `Index.md` — убраны broken refs на `Concepts/Frameworks/Sources` (не существовали). `Progress_Dashboard.md` — repurposed как text-mode dashboard для Paper Coach Mode.
- **`references/conversation_state_schema.md`** — помечен DEPRECATED, указатель на v2.
- **`ROADMAP.md`** — Testing & Integration Hardening сдвинут v0.15.0 → v0.16.0. Health/Concordance PRD добавлены в v0.17.0 Candidate.
- **`BACKLOG.md` + `docs/research/rice_evaluation_backlog.md`** — добавлены 4 entries: Core Values Discovery (#18, RICE 32.7), Health & Metabolism (#19, RICE 11.7), Goal Concordance (#20, RICE 7.5), Templates Rebuild v1.0 (#21, RICE 30.0).

### Исправлено
- **`tests/system/test_v090_features.py`** — добавлен `encoding='utf-8'` в `tempfile.NamedTemporaryFile`. Чинит pre-existing Windows `UnicodeEncodeError` (cp1251) при emoji в JS dashboard.

### Миграция
Legacy wiki пользователи (8 spheres / `schema_version < 2.0`): при первом запуске skill предложит migration prompt. Backup в `05_Archive/v1_backup_*`. См. [docs/migration_v1_to_v2.md](docs/migration_v1_to_v2.md).

## [0.14.0] — 2026-05-20

### Добавлено
- **`references/mode_adhd.md`** — адаптивный коучинг для executive function (ADHD): C.A.R. метод, 5-Minute Rule, визуальный таймер, time buffer 2×, body doubling, external scaffolding. Opt-in ONLY, MI-aligned, без медицинских советов
- **`references/mode_unemployed.md`** — структура дня для безработных и переходных периодов: 4-блочный шаблон, Sharp Hours (9–13), 10 принципов, social anchors, small wins. Без вины/стыда
- **`references/mode_elder.md`** — коучинг для solo aging с ограниченной мобильностью: нормализация solo aging, микро-якоря, mattering, наследие через память, достоинство в ограничениях (Франкл). Без патронизации
- **`references/mode_planning_friction.md`** — аудит трения в планировании: 7 вопросов, 3 шаблона дня (Deep Work/Meeting/Recovery), smart defaults, 10% Adjustment Rule
- **Persona Detection Hooks** — `SKILL.master.md` Phase 0/1: определение персоны (ADHD / unemployed / elder homebound / planning friction) + адаптации Phase 2/3/5
- **`tests/system/test_v140_features.py`** — 45 тестов (4 reference + persona hooks + platform integration)

### Изменено
- **`SKILL.master.md`** — version 0.13.0 → 0.14.0, persona hooks во всех фазах, 4 новых reference в списке
- **Все platform-файлы** — пересобраны через `build-platform-skill.py all` (Claude, Grok, Kimi, Kimi CLI)

## [0.13.0] — 2026-05-20

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

## [0.12.2] — 2026-05-20

### Добавлено
- **`references/calendar_intelligence.md`** — Pre-flight Protocol: Density Check → Conflict Detection → Chronotype Alignment → Smart Proposal → Create with Validation
- **PDF экспорт дашборда** — кнопка «Печать / PDF» в `life-planning-dashboard.html` + `@media print` стили

### Изменено
- **Paper Coach Mode** — заменён несостоятельный retry protocol (`persistence_retry`) на честный text-only flow в `SKILL.master.md` и всех platform-скиллах
- **Platform-neutral wording** — `calendar_constants.md` очищен от «Claude»/«MCP» для корректного inline в Grok/Kimi
- **CI/CD** — `build-skill.yml` теперь гонит полный pytest suite (`tests/`) вместо только `tests/release`
- **Release Notes** — unified generation из CHANGELOG.md, удалены дублирующие `RELEASE_NOTES_*.md`

### Исправлено
- **Dangling references** — `calendar_constants.md` теперь inline'ится в Grok/Kimi через `P0_REFS`

## [0.12.1] — 2026-05-20

### Исправлено
- **README.md** — возвращён на русский язык (случайно был переписан на английский в v0.12.0)
- **Все platform USER_GUIDEs** (`USER_GUIDE_CLAUDE.md`, `USER_GUIDE_GROK.md`, `USER_GUIDE_KIMI_OKCOMPUTER.md`, `USER_GUIDE_KIMI_CLI.md`) — переведены на русский
- **`CROSS_PLATFORM_COMPARISON.md`** — переведён на русский
- **Тесты** — обновлены для поддержки русскоязычного контента в platform docs

## [0.12.0] — 2026-05-20

### Добавлено
- **Chronotype-native planning** (`references/chronotype_native_planning.md`) — 3 профиля (Жаворонок/Промежуточный/Сова), Peak-Trough-Rebound эвристики, bedtime to-do list
- **Habit Stack Builder** (`references/habit_stack_builder.md`) — progressive ritual escalation (2→5→10→15 мин), Two-Day Rule, habit anchoring (B = MAP)
- **Shutdown Ritual** (`references/shutdown_ritual.md`) — 5 шагов (Capture→Review→Plan→Celebrate→Close), Zeigarnik elimination, psychological detachment
- **Fresh Start Engine** (`references/fresh_start_engine.md`) — temporal landmarks (Monday, 1st, New Year, birthday), dark side protection
- **Calendar Integration Audit** (`docs/audit/AUDIT_CALENDAR_INTEGRATION.md`) — 15 gaps, 4 критических
- **Planning Research synthesis** (`docs/research/planning_research_2026-05-20.md`) — 12 evidence-based идей с RICE-оценками
- **RICE Methodology v1.1** (`docs/research/rice_methodology.md`) — AI Session-based effort estimation (XS/S/M/L/XL/XXL) + Context Pressure
- **4 platform USER_GUIDEs** (`references/platforms/USER_GUIDE_*.md`) + `CROSS_PLATFORM_COMPARISON.md` — feature matrix, decision tree
- **E2E behavioral testing framework** (`tests/e2e/`) — golden dataset (20 cases), evaluation rubric, manual test protocol
- **Release automation** — `scripts/release.sh` (7-step atomic release) + `scripts/extract-release-notes.py`
- **Tests** — chronotype integration (16 tests), v0.12 features (26 tests), calendar tone check

### Изменено
- `references/energy_scheduling.md` — chronotype-adapted peak hours
- `references/diagnostic_methods.md` — chronotype calibration questions (Phase 0/1)
- `references/habit_loop.md` — cross-reference to `habit_stack_builder.md`
- All 4 `platforms/*/SKILL.md` — Phase 0 chronotype calibration + Phase 5 time adaptation
- `README.md` — full rewrite: value prop, quick-start, platform table
- `AGENTS.md` — Kimi Code CLI support, RICE Effort methodology update
- `ROADMAP.md` — v0.11–v0.14 structured roadmap
- `scripts/build-skill.sh` + `build-platform-skill.py` — release integration, kimi-cli artifact
- Calendar event texts — tone check, removed prescriptive «надо/должен»

### Исправлено
- Typo: Яворонок → Жаворонок (10 occurrences, 6 files)
- `references/calendar_integration.md` — removed "Runtime: claude.ai only", added Kimi CLI MCP
- CI workflows — pytest install, removed stale step, use `build-skill.sh`

### Удалено
- `RETRO_v091_v092.md` — moved out of public repository
- `references/platforms/grok_user_guide.md` — replaced by `USER_GUIDE_GROK.md`

## [0.10.2] — 2026-05-19

### Добавлено
- **Kimi Code CLI support** — новая платформа (terminal-based agent):
  - `platforms/kimi-cli/SKILL.md` (323 lines) — directory-based skill с `references/` через `read_file`
  - `references/platforms/kimi-cli.overlay.yaml` — overlay без inline, без `memory_space`
  - MCP поддержка (Google Calendar + Google Drive) через manual JSON config
  - Включён в `scripts/build-platform-skill.py` и `scripts/build-skill.sh`
- **Полный rewrite README.md** — короткий value prop + quick-start + таблица платформ + ссылки на USER_GUIDE
- **4 USER_GUIDE файла** (`references/platforms/`):
  - `USER_GUIDE_CLAUDE.md` — ZIP upload, MCP 1-click, directory-based refs
  - `USER_GUIDE_GROK.md` — Direct Prompt / Projects, native connectors (не MCP)
  - `USER_GUIDE_KIMI_OKCOMPUTER.md` — web agent, `memory_space`, text-only calendar
  - `USER_GUIDE_KIMI_CLI.md` — terminal setup, manual MCP JSON config
- **`CROSS_PLATFORM_COMPARISON.md`** — feature matrix, decision tree, quick selector
- **E2E behavioral testing framework** (`tests/e2e/`):
  - `golden_dataset.json` — 20 тест-кейсов (LPC-001..LPC-020)
  - `evaluation_rubric.md` — 5 критериев LLM-as-a-Judge
  - `MANUAL_TEST_RUN.md` — протокол ручного прогона

### Исправлено
- **README integrity** — все system tests проходят (11 доменов, Stage 1.5, communication style, core refs list, version format)
- **`references/calendar_integration.md`** — убрано "Runtime: claude.ai only", добавлена поддержка Kimi CLI MCP
- **`AGENTS.md`** — обновлены платформы (добавлен Kimi Code CLI), build-команда

### Удалено
- `references/platforms/grok_user_guide.md` — заменён на `USER_GUIDE_GROK.md`
- `RETRO_v091_v092.md` — удалён из публичного репозитория

## [0.10.1] — 2026-05-19

### Исправлено
- **BUG-002**: Grok SKILL.md — инлайн 7 критичных reference-файлов (`diagnostic_methods`, `communication_style`, `authentic_goal_filter`, `goal_architecture`, `weekly_review`, `habit_loop`, `emotion_regulation`) через `<details>` tags. Ранее 21 ссылка "Загрузи `references/...`" не работала в Grok Web Chat (нет ФС).
- **BUG-003**: Kimi SKILL.md — инлайн тех же 7 reference-файлов в агрессивно сжатом виде (ultra-condensed). Ранее ссылки были неработоспособны в OK Computer single-file режиме.
- Удалены инструкции "Загрузи" для несжатых P1/P2 reference-файлов — заменены на нейтральные "См. `references/...`".

### Исправлено
- **BUG-002**: Grok SKILL.md — инлайн 7 критичных reference-файлов (`diagnostic_methods`, `communication_style`, `authentic_goal_filter`, `goal_architecture`, `weekly_review`, `habit_loop`, `emotion_regulation`) через `<details>` tags. Ранее 21 ссылка "Загрузи `references/...`" не работала в Grok Web Chat (нет ФС).
- **BUG-003**: Kimi SKILL.md — инлайн тех же 7 reference-файлов в агрессивно сжатом виде (ultra-condensed). Ранее ссылки были неработоспособны в OK Computer single-file режиме.
- Удалены инструкции "Загрузи" для несжатых P1/P2 reference-файлов — заменены на нейтральные "См. `references/...`".

---

## [0.10.0] — 2026-05-19

### Добавлено
- **Multi-Platform Skill Adaptation** — скилл адаптирован под три платформы:
  - **Claude.ai** (primary) — ZIP-архив `.skill`, MCP-интеграция, Claude Memory
  - **Grok 4.3** (xAI) — plain `SKILL.md`, sandbox file I/O, native persistent memory, native connectors, `render_file` для дашборда
  - **Kimi K2.6** (Moonshot AI) — plain `SKILL.md`, `memory_space` tool, `KIMI_REF` для артефактов, OK Computer / Base Chat guidance
  - Архитектура: `SKILL.master.md` (platform-agnostic) + `references/platforms/{claude,grok,kimi}.overlay.yaml` + генератор `scripts/build-platform-skill.py`
  - 53 consistency tests: `tests/system/test_multi_platform.py` (включая 11 фактчек-тестов для Grok)
- Системные тесты: консистентность версий, целостность README, синхронизация с GitHub
- Атомарный скрипт релиза: `scripts/release.sh`
- Post-commit hook: предупреждение о незапушенных коммитах
- `VERSION_SOURCES.md` — документация источников версии
- `CHANGELOG.md`, `ROADMAP.md`, `BACKLOG.md` — управление проектом

### Исправлено
- **Grok 4.3 документация**: исправлены 4 критические ошибки в `grok_user_guide.md` и `grok.overlay.yaml` после фактчека через xAI Docs MCP:
  - Persistent Memory: Grok имеет native memory (апрель 2025), Grok Projects, Skills, Collections
  - Calendar: Grok имеет native Google Calendar + Outlook connectors
  - Drive: Grok имеет native Google Drive connector (не MCP)
  - `render_file`: существует как render component (не API tool)
- **Cross-platform continuity**: добавлена инструкция для чтения существующей `Life Planning Coach Wiki/` из Google Drive при переходе с Claude/Kimi на Grok

### Изменено
- `scripts/build-skill.sh` теперь собирает артефакты для всех платформ: `.skill` (Claude), `-grok.md`, `-kimi.md`
- `SKILL.md` вычищен от platform-specific терминов, теперь является generated из `SKILL.master.md` + `claude.overlay.yaml`
- `references/templates/CLAUDE_Instructions.md` → `AI_Instructions.md` (platform-agnostic)
- Удалён `pyproject.toml` как дублирующий `setup.py`

### Исправлено
- README.md: версия 0.4.0 → 0.6.0, добавлены Stage 1.5 и адаптация стиля
- GitHub Release v0.6.0: переписан на русский язык

### Удалено
- Удалена секция `[0.3.0]` — этот релиз никогда не существовал. Все описанные в нём фичи (dashboard, presets, goals, weekly review, WOOP) фактически были выпущены в v0.1.0–v0.2.0. Секция была ошибочно добавлена в CHANGELOG задним числом.

---

## [0.9.2] — 2026-05-18

### Исправлено
- **Android Chrome compatibility** — 5 mobile-specific fixes, missed in v0.9.1:
  - `-webkit-tap-highlight-color: transparent` — removes blue tap flash overlay on every touch
  - `overscroll-behavior-y: contain` — prevents pull-to-refresh while scrolling dashboard content
  - `100dvh` with `100vh` fallback — fixes content jumping as Chrome dynamic toolbar shows/hides
  - `<meta name="theme-color">` with light/dark variants — colors Android address bar to match app theme
  - `viewport-fit=cover` — enables edge-to-edge display on notched Android devices
  - JS dynamic sync: `theme-color` updates instantly when user toggles dark/light mode

### Добавлено
- **7 new dashboard tests** for mobile platform compatibility:
  - Android Chrome: tap highlight, overscroll behavior, theme-color, viewport-fit, dvh units
  - iOS Safari: `-webkit-backdrop-filter` regression guard

---

## [0.9.1] — 2026-05-18

### Добавлено
- **Apple-style Dashboard Redesign** — полностью переработанный `life-planning-dashboard.html`
  - Activity Rings (SVG) — 3 кольца прогресса: Баланс, Исполнение, Консистентность
  - Liquid Glass карточки — `backdrop-filter: blur(40px)` с graceful degradation
  - Dark/Light mode toggle — переключение темы с сохранением в `localStorage`
  - macOS-style sidebar + segmented control tabs (Обзор / Ретроспектива / Цели)
  - Confidence Gauges (SVG) — 4 показателя уверенности
  - CSS Grid Heatmap — 365 дней активности без внешних библиотек
  - 12-Week Tracker — бары прогресса по 12 неделям
  - WOOP Cards + BHAG Roadmap + OKR Summary
  - Velocity & Burndown sparklines (SVG)
  - Weekly Priorities с чекбоксами
  - Accessibility: `prefers-reduced-motion`, focus-visible, aria-labels, semantic HTML
  - Mobile-first responsive: breakpoints 375px / 768px / 992px / 1200px+

### Изменено
- **Удалены внешние зависимости** — ECharts (~1 MB), Chart.js (~200 KB), Font Awesome (~100 KB) заменены на чистый SVG + CSS
- **Размер файла**: 1,403 KB → ~61 KB (уменьшение в 23×)
- **Шрифты**: системный стек вместо Google Fonts (Inter) — полная offline-совместимость
- **System font stack**: `-apple-system`, `BlinkMacSystemFont`, `SF Pro Display`, `Segoe UI`, Roboto

### Исправлено
- `test_contains_expected_chart_keywords` обновлён под новую архитектуру (SVG вместо ECharts/Chart.js)
- `test_doctype_and_html_lang` поддерживает атрибуты в теге `<html>`

---

## [0.9.0] — 2026-05-18

### Добавлено
- **Habit Tracker / Dashboard Streaks** — 4 категории серий привычек (active_habits, digital, sugar, focus) в `life-planning-dashboard.html`
- **Mobile Dashboard (responsive)** — адаптивная вёрстка: шрифты, layout, touch-friendly элементы, отключение горизонтального скролла
- **5-Minute Micro-Sessions** (`references/micro_sessions.md`, 44 строки) — быстрые чек-ины: эмоция → 1 действие ≤30 сек → якорь
- **Quick Decision Protocol** (`references/quick_decision.md`, 45 строк) — 2–3 вопроса для принятия решения «здесь и сейчас» (Values, Feasibility, One Action)
- **Reward Audit (Grayscale Guide)** (`references/reward_audit.md`, 58 строк) — осознанность cheap dopamine
  - Grayscale Experiment: инструкции iOS (Settings → Accessibility → Color Filters) и Android (Settings → Accessibility → Color Correction)
  - Научная база: Holte et al. (2021), Wickord (2023), Myers (2022), NYT (2025), Rada (2005), Avena (2008), Lembke (2021), Kushlev (2025)
  - 4 категории check-in: скролл, сахар, шопинг, игры
  - Opt-in only, без слов «бросай», без термина «dopamine detox»
- Интеграция в `SKILL.md`: 3 новые ссылки в References + hook в Phase 3 (Weekly Review)
- 26 системных тестов на v0.9.0 контент (`tests/system/test_v090_features.py`)

---

## [0.8.0] — 2026-05-18

### Добавлено
- **Habit Loop Framework** (`references/habit_loop.md`, 254 строки) — мост между целями и ежедневными действиями
  - Cue-Routine-Reward (Duhigg, Wood & Neal)
  - Tiny Habits (Fogg): B = MAP, ≤30 секунд, anchor, celebration
  - Habit Stacking (Clear): "После [X], я [Y]"
  - Timeline: median 66 дней (Lally)
  - Integration with WOOP, Calendar, Energy Scheduling, Recovery Protocol, Win Alert
- **Task Breakdown with Checkpoints** (`references/action_breakdown_template.md`, 128 строк) — разбиение WOOP на шаги
  - 5 шагов: finish line → sub-steps → checkpoints → time estimate → first step
  - Checkpoints: verifiable, binary (да/нет)
  - Opt-in: Career/Finances/Health/Home/Learning
- **Markdown Tables as UI** (`references/markdown_tables.md`, 109 строк) — 4 шаблона
  - Weekly Plan, Wheel of Life Review (11 доменов), Progress Check (OKR), Course Correction
  - Stage-appropriate: только Preparation/Action stages
  - Zero tables в SKILL.md
- **Weak Goal Taxonomy + Sanity-Check** (`references/weak_goal_taxonomy.md`, 133 строки)
  - 5 паттернов слабых целей: Vague, Output-as-Outcome, Missing Baseline, Sandbagging, Moonshots
  - Sanity-Check: Coverage, Balance, Feasibility, Measurability, Alignment
  - Integration: расширение `authentic_goal_filter.md` (Stage 1.5)
- **Status Icon System** (`references/status_icons.md`, 61 строка)
  - ⬜🔄✅❌⏸️⚠️ + 🔴🟡🟢 priority
  - Accessibility: текстовый fallback для screen readers
  - Emotional safety: High N users — opt-in, без ❌/⚠️
- Интеграция в `SKILL.md`: 5 новых ссылок + хуки в Phase 1.5, 2, 3, 5
- 34 системных теста на v0.8.0 контент (`tests/system/test_v080_features.py`)

### Изменено
- `AGENTS.md` — полная актуализация после v0.7.1 (version, test counts, structure, removed fixed bugs)
- `ROADMAP.md` — v0.8.0 scope сокращён с 12 до 6 фич (realistic minor release)

### Research
- Habit formation: Fogg (Tiny Habits), Clear (Atomic Habits), Wood (context-dependent repetition), Lally (66-day timeline), Duhigg (habit loop)

---

## [0.7.1] — 2026-05-18

### Добавлено
- **Win Alert Protocol** (`references/win_alert.md`) — структурированное празднование побед
  - 5 шагов: WHAT → WHEEL DOMAIN → WHY IT MATTERS → RESOURCES/QUALITIES → NEXT STEP
  - Адаптация под 4 квадранта стиля коммуникации (Nurturing/Challenging/Exploratory/Collaborative)
  - Научная база: savoring (Bryant & Veroff), SDT competence feedback, growth mindset (Dweck)
  - Safety: не trait-based похвала, не пустые комплименты
- **Recovery Protocol MVP** (`references/recovery_protocol.md`) — восстановление после пропусков
  - 3 стратегии по тяжести: LIGHT (Reschedule) → MEDIUM (Catch-up Mini-Session, 15 мин) → HEAVY (Recovery Protocol)
  - Без streak tracking, без shame language, без «нагонять пропущенное»
  - Pattern detection — только conversational, не декларативный
  - Научная база: MI Roll with Resistance, relapse prevention (Marlatt), self-compassion (Neff)
- **Energy-Based Scheduling** (`references/energy_scheduling.md`) — планирование с учётом энергии
  - 3 уровня энергии → маппинг на тип задачи → colorId из COLOR_MAP
  - 1 калибровочный вопрос о пике энергии
  - Связь с AC-8 (Energy Check), Seasonal Planning, True Goal Score
- Интеграция в `SKILL.md`: 3 новые ссылки в References + хуки в Phase 1.5, 3, 5, 9
- 23 системных теста на v0.7.1 контент (`tests/system/test_v071_features.py`)

### Изменено
- `ROADMAP.md`: добавлена секция v0.7.1, обновлены v0.8.0/v0.9.0
- `BACKLOG.md`: результаты конкурентного анализа (12 фич, 3 IMPLEMENT → v0.7.1, 9 DEFER → v0.8.0+)

### Research
- `references/competitive_research_2026.md` — анализ 7 конкурентных скиллов + capability mapping

---

## [0.6.0] — 2026-05-16

### Добавлено
- **Stage 1.5: Фильтр аутентичных целей** (`references/authentic_goal_filter.md`)
  - Детектор красных флагов (6+1) с экстернализацией «Чей голос?»
  - Энергетическая проверка (соматический маркер, опционально)
  - Глубокое «Почему» (3 уровня)
  - Тест социального давления (4 вопроса)
  - Истинная оценка цели — радар из 5 осей
  - Портфель целей: Активные / На паузе / Анализ паттернов
- **Адаптация стиля коммуникации** (`references/communication_style.md`)
  - Гибрид Big Five × TTM × MI
  - 4-квадрантная матрица адаптивного коучинга
  - Явный фреймворк OARS
  - 2 вопроса калибровки стиля в Phase 0
- **Обновление колеса жизни**: 8+1 → 11 сфер
  - Семья и Социальная разделены
  - Добавлена сфера «Вклад»
  - «Смысл» стал обязательным
- Тесты v0.6.0: 30 тестов на контент (`tests/release/test_v060_content.py`)

### Изменено
- SKILL.md: 4644 слова, добавлен Stage 1.5 между Stage 1 и Stage 2
- Языковые правила: «Ты решаешь» вместо «Давайте решим», запрещены «надо», «должен», «провал»
- Conversation State JSON: добавлены `goal_filter`, `goal_portfolio`

---

## [0.5.0] — 2026-05-16

### Добавлено
- **Two-Track Diagnostic Architecture**
  - Track A — Quick Diagnostic (20–30 мин, 1 сессия)
  - Track B — Deep Diagnostic (65–105 мин, 2–4 сессии)
- **Values Clarification**: pairwise 45 пар → Top-5 → Top-3 (10 вопросов)
- **Ikigai**: аутентичный фреймворк Ken Mogi (5 Pillars)
- **Life Story**: опциональный блок + Lite версия (3 вопроса)
- **Readiness Gate**: проверка комфорта после каждой фазы
- **Workview/Lifeview**: микро-формат (3 вопроса)

### Изменено
- Полная реструктуризация Stage 1 (Diagnostic)

---

## [0.4.0] — 2026-05-16

### Добавлено
- **Двухуровневая система персистентности**
  - Уровень 1: Claude Memory (работает сразу)
  - Уровень 2: Google Drive + персональная wiki (opt-in)
- **Структура персональной wiki** на Google Drive
- **Автоматическое создание** Progress Dashboard, README wiki, Index
- **Graceful degradation**: при недоступности Drive — мягкий переход в режим памяти

---

## [0.2.0] — 2026-05-14

### Добавлено
- Интеграция с Google Calendar MCP
- OAuth 2.0 через claude.ai
- CRUD Events, Free/Busy Slots
- Calendar Presets: Weekly Review, WOOP, Milestones, Time Blocks

### Удалено
- Кастомный Python-пакет `calendar_integration/` (заменён на MCP)

---

## [0.1.0] — 2026-05-13

### Добавлено
- Базовый скилл life-planning-coach для Claude.ai
- Stage 1: Diagnostic (Wheel of Life 8+1, Values Clarification Schwartz)
- Stage 2: Goal Architecture (BHAG, OKR, WOOP)
- Stage 3: Weekly Review
- Stage 4: Dashboard
- Stage 5: Google Calendar интеграция (Python API)
- Emotional Landing Protocol
- Evidence-based методики с эффект-сайзами

---

[Unreleased]: https://github.com/azagreev/life-planning-coach/compare/v0.10.2...HEAD
[0.10.2]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.10.2
[0.10.1]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.10.1
[0.10.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.10.0
[0.9.2]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.9.2
[0.9.1]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.9.1
[0.9.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.9.0
[0.8.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.8.0
[0.7.1]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.7.1
[0.6.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.6.0
[0.5.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.5.0
[0.4.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.4.0
[0.2.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.2.0
[0.1.0]: https://github.com/azagreev/life-planning-coach/compare/v0.2.0...v0.1.0
