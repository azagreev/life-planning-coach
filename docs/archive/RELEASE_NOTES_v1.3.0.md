## Что нового в v1.3.0

**Тема:** WoL Refactor (PRD v0.15 §5 frequency gate) + v1.2 code review follow-ups + Windows release script bugs closed. Closes 3 follow-up items из v1.2 + addresses PRD's last remaining WoL concern + makes release.sh work end-to-end on Windows. Schema bump 2.2.5 (additive). No new evidence-based methods — focus на operational polish, discovery gaps, и tooling reliability.

### Added (Methodology — PRD v0.15)

- **WoL Frequency Gate** — `diagnosis.wheel_of_life.last_assessed_at` ISO 8601 field (schema 2.2.5). `module_phase1_diagnostic.md` §WoL Frequency Gate gates auto-offer: skip < 30 дней (на explicit request — soft challenge); offer re-assess ≥ 30 дней; null = never assessed → standard Track A/B flow. PRD v0.15 §5 compliance — WoL опциональный инструмент, не routine.
- **AAR sighted_count runtime pattern matching** — `module_phase3_weekly_review.md` Step 9 расширен skill-instruction protocol: load last 4 weekly_reviews → semantic similarity check (same `category` + общая тема) → increment `sighted_count` существующего lesson ИЛИ append new c `sighted_count: 1`. Surface при ≥ 3 → routing к Phase 2 (OKR recalibration) или Phase 1.5 (Compass). Закрывает v1.2 follow-up (RICE 120) — без runtime instruction Step 9 был simple journal, surface threshold никогда не triggered.
- **COM-B Phase 0 upsell** — `references/emotion_regulation.md` §5 COM-B Upsell: opt-in suggestion после ER protocol для repeat «не могу начать». 2-decline cutoff per session. Закрывает discovery gap для lean_conversation users (без full_persistence Phase 1 не trigger'ится автоматически). Phase 0 trigger остаётся удалённым из master (v1.2 architecture decision сохранён) — discovery через Tier 2 routing: master → ER module → com_b_diagnostic.md.

### Added (Tooling & Tests)

- **`tests/helpers/forbidden_words.py`** (NEW shared helper, 120 lines + 17 smoke tests) — whitelist Russian quoted speech `«...»` для forbidden-word checks. API: `assert_no_forbidden(content, ["надо", "должен", "обязан"], context="...")`. Перестаём переформулировать user quotes / anti-pattern examples с directive словами. Migration старых tests by-need (не массовый refactor).
- **`AGENTS.md §3.6 State Writes Policy`** — закрепляет precedent v1.2.0: state writes inline убраны из Phase 2/3 modules под per-module budget pressure (≥ 2400/2500 tokens). Single source of truth = `references/state_v2_schema.md`. §3.7 — guidance для future test authoring через forbidden_words helper.
- **`tests/system/test_methodology_v1_3.py`** (NEW, 33 tests) — coverage для COM-B upsell (9), WoL gate (7), schema 2.2.5 (8), AAR runtime (9). Все scoped к v1.3 additions; inline `_strip_quoted()` для orthogonal PR development (helper landed в PR-D но tests не depend на нём для parallelism).
- **`tests/unit/test_release_sh_step5.py`** (NEW, 4 regression tests) — guard для BUG-008 fix: validates `release.sh` uses `sys.stdout.buffer.write(bytes)` не `print(decoded)`; anti-pattern check; pipe chain sanity.
- **`tests/unit/test_extract_release_notes.py`** + `test_stdout_reconfigure_present_for_windows_safety` — guard для BUG-009 fix.

### Changed (Methodology)

- **`references/module_phase1_diagnostic.md`** → WoL Frequency Gate section добавлена; ER Protocol section trimmed (11 lines → 5 lines, cross-ref к ER module); Health Track trimmed (13 → 5 lines); Persona adaptations trimmed (multi-line → inline); State writes update для `last_assessed_at`. Net: 2487 → 2420 tokens (80 headroom).
- **`references/module_phase3_weekly_review.md`** → Step 9 expanded (2 → 10 lines pattern-matching protocol); State writes trimmed per AGENTS §3.6 (full schemas → cross-refs к state_v2_schema.md, saved ~600 chars). Net: 2492 → 2481 tokens (19 headroom).
- **`references/emotion_regulation.md`** → §5 COM-B Upsell new section (~60 lines между §4 Conflict Reappraisal и Trigger Phrases).
- **`references/com_b_diagnostic.md`** → entry-points table: Phase 0 row updated «(master)» → «(`emotion_regulation.md` §5, v1.3.0+)»; architecture note added про v1.2 budget decision.
- **`references/state_v2_schema.md`** → schema bump 2.2.4 → 2.2.5 (additive). Новое optional поле `diagnosis.wheel_of_life.last_assessed_at` (см. §3.4.4). §3.5.2 sighted_count semantics expanded (semantic match + last 4 reviews window + skill-instruction note).
- **`references/evidence_map.md`** → WoL entry updated к implementation (не «v1.3 plan»); NEW entry «After Action Review — Runtime pattern (v1.3.0)» documenting skill-instruction approach (NOT Python algorithm).

### Changed (Tooling & CI)

- **`.github/workflows/release-checks.yml`** → `git branch -f main origin/main` теперь explicit failure с `::error::` annotation + diagnostic hint (было silent `|| true`, маскировало shallow-clone / race-condition issues).
- **`tests/system/test_methodology_v1_2.py`** → migrated 3 forbidden-words tests к shared helper (example migration pattern); `TestSchemaAARField::test_schema_version_bumped_to_2_2_4` refactored к history preservation pattern после schema 2.2.5 bump.

### Fixed

- **BUG-008** — `scripts/release.sh` step 5 «Проверка на GitHub» крашился на Windows MSYS bash с `Python write /dev/stdout: The pipe is being closed.` после steps 1-4 (push) — tag + GitHub Release не выполнялись автоматически. Root cause: inline `print(content.decode('utf-8'))` на cp1251 default encoding ломался на UTF-8 emoji (`🧭`) + кириллице в README. Fix: `sys.stdout.buffer.write(bytes)` bypass'ит text encoding entirely. Bulletproof на любом OS / encoding. **Project teper has 0 open bugs.**
- **BUG-009** — `scripts/extract-release-notes.py` крашился на финальном `print(✅ ...)` под Windows cp1251 (UnicodeEncodeError, exit code 1 даже если файл создавался). Fix: `sys.stdout/stderr.reconfigure(encoding="utf-8")` guard в начале скрипта.
- **v1.2 release leftovers** — `docs/archive/RELEASE_NOTES_v1.2.0.md` retroactive commit (был заблокирован BUG-009); README badge bump 1.1.0 → 1.2.0 + installation refs (3 places); platforms/*/SKILL.md frontmatter bump (BUG-008 заблокировал release.sh от commit'a этих файлов в v1.2.0 ship).

### Acceptance criteria

- ✅ WoL Frequency Gate работает в Phase 1 module со всеми 3 ветками (< 30d / ≥ 30d / null)
- ✅ AAR sighted_count теперь увеличивается через runtime pattern matching, surface threshold ≥ 3 trigger'ся
- ✅ COM-B discovery работает для lean_conversation users через ER upsell
- ✅ Schema v2.2.5 backward-compatible — старые v2.2.x клиенты игнорируют unknown `last_assessed_at`
- ✅ Master ≤ 4100 tokens; каждый phase module ≤ 2500 tokens (Phase 1: 2420, Phase 3: 2481); Tier 2 total ≤ 15000 (~14522)
- ✅ 740+ tests passing (v1.2 was 678+, v1.3 adds: 33 methodology_v1_3 + 17 forbidden_words + 4 release_sh_step5 + 1 extract_release_notes)
- ✅ release.sh works end-to-end на Windows (BUG-008 fix, validated через PR-F via release.sh execution)
- ✅ 0 open bugs in BUGS.md (BUG-008 + BUG-009 closed)
- ✅ Все 4 platform builds: claude, grok, kimi, kimi-cli

### Architecture decisions

- **WoL gate без Tier 1 touch** — gating logic покоится в Phase 1 module (Tier 2), не в SKILL.master Routing Map. Сохраняет 4100-token master budget из v1.2. Master НЕ trognut.
- **AAR sighted_count = skill-instruction, не code** — pattern matching через LLM semantic judgment, не Python algorithm. Zero runtime cost; risk = LLM consistency, mitigated через explicit criteria («same category + общая тема»). Real-world calibration через user feedback post-ship.
- **COM-B upsell в ER module, не master** — закрепляет v1.2.0 architecture decision «Phase 0 COM-B trigger удалён под Tier 1 budget pressure». Discovery работает через Tier 2 routing path: master → emotion_regulation.md → com_b_diagnostic.md.
- **AGENTS §3.6 State Writes Policy formalized** — per-module budget pressure ≥ 2400/2500 → state writes inline removed in favor of cross-ref к state_v2_schema.md (single source of truth). Applied to Phase 3 module в PR-B (saved ~600 chars).
- **BUG-008 root cause = same class as BUG-009** — оба про Windows cp1251 vs UTF-8 encoding в Python stdout. Fix family: `sys.stdout.reconfigure(encoding="utf-8")` для standalone scripts (BUG-009); `sys.stdout.buffer.write(bytes)` для inline `-c` scripts (BUG-008). Pattern document'ан в both BUGS.md resolutions.

### Stacked PR series

- PR #11 — `fix/v1.3-extract-release-notes-windows-encoding` (BUG-009 fix + v1.2 release leftovers retroactive)
- PR #12 — `chore/v1.3-trivial-cleanup-bundle` (AGENTS §3.6/3.7 + forbidden-words helper + workflow explicit error)
- PR #13 — `feat/v1.3-com-b-phase0-upsell` (COM-B upsell в ER module §5)
- PR #14 — `fix/v1.3-release-sh-step5-encoding` (BUG-008 fix)
- PR #15 — `feat/v1.3-wol-frequency-gate` (core feature + schema 2.2.5)
- PR #17 — `feat/v1.3-aar-sighted-count-runtime` (был #16 → auto-closed after base merge → recreated)

Plus PR #18 (this) release prep + future PR #19 ROADMAP cleanup → v1.4 placeholder.

Merge order: #11 → #12 → #13 → #14 → #15 → #17 → #18 (this) → tag → release → #19.
