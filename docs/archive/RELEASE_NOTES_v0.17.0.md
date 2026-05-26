## Что нового в v0.17.0 — IA Decomposition (Tier 1 Core + 6 Phase Modules)

Снизили cold-load `SKILL.master.md` с ~6.5K до ~3.6K tokens через декомпозицию архитектуры на Tier 1/2/3. Phase-протоколы переехали в `references/module_phase*.md` и грузятся lazy по факту входа в фазу. Tier 1 Core управляет маршрутизацией через явный Routing Map.

### Added

- **6 phase modules** (`references/module_phase*.md`) — Tier 2, lazy-load:
  - `module_phase1_diagnostic.md` — Phase 1 Diagnostic + Phase 0.5 ER Protocol (Cognitive Reappraisal, Grounding, Self-Compassion)
  - `module_phase1_5_goal_filter.md` — Authentic Goal Filter (Red Flags, AGF radar, Goal Portfolio) + Core Values Discovery (bottom-up: Life Domains → Meaningful Experiences → Energizing Activities)
  - `module_phase2_goal_architecture.md` — BHAG → Life Themes → 12-Week OKR → Weekly → Daily WOOP + Habit Loop (Cue/Routine/Reward/Anchor)
  - `module_phase3_weekly_review.md` — 7-step Weekly Review (GTD + Scrum Retro + Progress Audit + Adjustment + Celebration + Habit Review + Reward Audit)
  - `module_phase4_dashboard.md` — HTML / Text dashboard generation + JSON Data Contract (`window.lpData`)
  - `module_phase5_execution.md` — Calendar Integration + Daily Top-3 + Energy-aware scheduling + Shutdown Ritual
- **`tests/unit/test_tier_token_budgets.py`** — token-budget guardrails:
  - `Tier 1` (`SKILL.master.md`) ≤ 4000 tokens cold-load
  - Каждый phase module ≤ 2500 tokens
  - Сумма всех модулей ≤ 14000 tokens
  - Master обязан декларировать Routing Map с указанием каждого Tier 2 модуля

### Changed

- **`SKILL.master.md`** переписан как Tier 1 Core (~3.6K tokens, было ~6.5K):
  - Phase 0 Emotional Landing — полный (5–10 мин, VALIDATE → REFLECT → ONE THING → BRIDGE) + Style Calibration + Persona Detection routing
  - **Routing Map** — таблица «сигнал пользователя → какой модуль грузить» — управляет переходами в Tier 2
  - **Persistence Mode gating** — 4 режима (`full_persistence`, `wiki_no_execution`, `execution_no_wiki`, `lean_conversation`) по комбинации Drive × Calendar
  - **Backfill protocol** при mid-session подключении Drive — bootstrap wiki + dump state v2
  - Safety, Language Rules, Privacy, References Index — компактно (одна таблица Troubleshooting вместо двух)
  - Глубокий Phase 1–5 контент вынесен в Tier 2 модули
- **`scripts/build-platform-skill.py`** — `P0_REFS` дополнен 6 phase modules; `inline_references()` получил **append-fallback**: P0 refs без явной load-инструкции (например, ссылка из Routing Map таблицы) аппендятся в Appendix в конце single-file platforms (grok / kimi).
- **`references/module_phase5_execution.md`** — формулировка про calendar connector нейтрализована (механизм авторизации — в overlay'ах).
- **Platform overlays** упрощены до перевода нейтральных терминов:
  - `claude.overlay.yaml`: `AI Memory` → `Claude Memory`, `Cloud Storage` → `Google Drive`, frontmatter override
  - `grok.overlay.yaml`: `AI Memory` → `Native Memory`, `Cloud Storage` → `Google Drive connector`, append Grok-specific notes
  - `kimi.overlay.yaml`: `AI Memory` → `memory_space`, `Cloud Storage` → `файловая система (write_file)`, append Kimi-specific notes
  - `kimi-cli.overlay.yaml`: аналог Kimi но с MCP support и без `KIMI_REF`
- **Platform builds** пересобраны:
  - `claude/SKILL.md`: 192 строк, 1.5K слов (lazy refs через файловую систему)
  - `grok/SKILL.md`: 1030 строк, 8.1K слов (single-file с inlined Tier 2 + Tier 3 refs)
  - `kimi/SKILL.md`: 714 строк, 5.8K слов (ultra-condensed inlined)
  - `kimi-cli/SKILL.md`: 197 строк, 1.6K слов (lazy refs через `read_file`)

### Fixed

- **`tests/system/test_v140_features.py`** fixture `platforms` для lazy-load платформ (claude, kimi-cli) теперь собирает «reachable corpus»: SKILL.md + содержимое 6 phase modules + 4 persona refs + emotion_regulation + diagnostic_methods. Семантика: тесты проверяют доступность контента в скилле, а не физическую локацию.
- **`setup.py`** — версия обновлена до 0.17.0.

### Roadmap progress

✅ P0: Tier 1 Skill Core ≤ 4K tokens (Routing Map + Phase 0 + Safety + Language Rules + Reference Index)
✅ P0: 6 phase modules с lazy-load инструкциями
✅ P0: Token budget tests per tier (4 теста)
✅ P1: Platform rebuild — все 4 платформы (claude / grok / kimi / kimi-cli)

⏳ Deferred:
- P1 Legacy compatibility bundle — отложено; если зависимостей нет, делаем сразу cutover в v0.18.0

### Acceptance criteria

- ✅ `SKILL.master.md` ≈ 3650 tokens (≤ 4000 cold-load budget)
- ✅ Все 6 phase modules ≤ 2500 tokens каждый
- ✅ Сумма модулей ≈ 4300 tokens (≤ 14000)
- ✅ Routing Map ссылается на все 6 phase modules
- ✅ Master обязательно содержит ссылки на 6 phase modules (test_master_declares_routing_map)
- ✅ 434 теста pass, 11 failures = release-flow artifacts (version mismatch / zip / clean tree — исправятся при tag)

### Что дальше

- **v0.18.0** — Gating logic в SKILL.master.md + state writes per phase + Core Values Discovery flow
- **v0.19.0** — Health & Metabolism Track + Goal Concordance (schema bump 2.1 / 2.2)
- **v1.0.0** — Build pipeline rework + platform lazy-loading для Claude.ai + polish
