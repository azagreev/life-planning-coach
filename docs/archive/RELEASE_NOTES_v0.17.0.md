## Что нового в v0.17.0

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
