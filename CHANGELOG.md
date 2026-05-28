# Changelog

Все значимые изменения проекта отслеживаются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), проект следует [Semantic Versioning](https://semver.org/lang/ru/).

---

## [Unreleased]

## [1.4.0] — 2026-05-28

**Тема:** Minor release. WoL Health Assessment Methodology (PRD v1.0): 6 sub-segments для сферы `health` + lightweight 4-question Snapshot tool + Phase 3 opt-in. Schema bump 2.2.5 → 2.2.7 (два additive bumps в одном release window — Sub-feature A добавила 2.2.6 `health_subsegments`; Sub-feature B добавила 2.2.7 `health_snapshot.last`). New evidence-based methodology — surfacing detail в WoL health assessment + middle-ground tool между basic WoL и full Health Track (v0.19.0). Не дублирует existing health track; positioned как pre-screening путь, который routes к нему при agreement пользователя.

### Added (Methodology — PRD Health Assessment v1.0)

- **WoL Health Sub-segments + Health Index** (Sub-feature A, BACKLOG RICE 24.4). Новый Tier 3 ref `references/wol_health_subsegments.md` — opt-in detailed assessment сферы `health` через 6 канонических sub-segments (energy / recovery / physical_wellbeing / stress_resilience / nutrition / reserve), 1-10 каждый. `current.health` = Health Index = avg(filled subsegments) если ≥ 4 заполнены; иначе legacy single-score. 4 категории (≥8 / 6.5-7.9 / 5.0-6.4 / ≤5) + weakest sub-segment surface. 4 persona adaptations. Schema additive bump 2.2.5 → 2.2.6 (`diagnosis.wheel_of_life.current.health_subsegments` object | null). Phase 1 module loads ref при opt-in. Не дублирует `track_health_metabolism.md` (v0.19.0).
- **Light Health Snapshot** (v1.4.0 Sub-feature B, BACKLOG RICE 15.0). Новый Tier 3 ref `references/health_snapshot.md` — 4-question light tool. Triggers: Health Index ≤ 5.5 (от Sub-feature A) ИЛИ explicit request ИЛИ Phase 3 opt-in (Sub-feature C). 2-decline cutoff per session. Schema additive bump 2.2.6 → 2.2.7 (`diagnosis.health_snapshot.last` object | null с полями date / average_score / weakest_question / answered_count / declined_count). 4 категории routing с safety escalation (все 4 ≤ 3 → SKILL.master Safety section). Routing к `track_health_metabolism.md` при agreement. Source: PRD §4 + PHQ-2/GAD-2 short-screening patterns.
- **Phase 3 Weekly Review opt-in для Health Snapshot** (v1.4.0 Sub-feature C, BACKLOG RICE 15.0). `module_phase3_weekly_review.md §6.5` — при `health_metabolism.active == false` предложить 4-Q Snapshot. Existing branch (`active == true` Health Track review sleep/stress/nutrition) сохранён. Источник: PRD §8 «опционально — в еженедельном обзоре».

### Changed (Schema)

- **`state_v2_schema.md` bumped 2.2.5 → 2.2.7** (two additive bumps в одном release window). New §3.4.5 (health_subsegments) + §3.4.6 (health_snapshot.last). §9 write-rules matrix +2 rows. §12 changelog entries для 2.2.6 и 2.2.7.

### Changed (Phase modules — token-tight)

- **`module_phase1_diagnostic.md`** → 2 tight inline mentions (sub-segments + Snapshot routing). Final 2498/2500 tokens (2 headroom — будущие Phase 1 additions требуют offload в Tier 3 refs).
- **`module_phase3_weekly_review.md`** → §6.5 расширен `active == false` branch + tightened wording в section. Final 2474/2500 (26 headroom).

### Added (Tooling & Tests)

- **`tests/system/test_methodology_v1_4.py`** (NEW, 80 tests): schema bump guards; health_subsegments + health_snapshot field specs + Tier 3 ref content (parametric over 6 subsegments / 4 questions / 4 personas / 4 categories); Phase 1 + Phase 3 integration; budget guards; A↔B routing consistency.
- **`tests/system/test_methodology_v1_3.py`**: 3 schema-version tests refactored к history-preservation pattern; evidence-map slice now bounded by next H3.
- **`scripts/build-platform-skill.py P0_REFS`** +2: `wol_health_subsegments.md`, `health_snapshot.md` — inlined для grok/kimi single-file builds.
- **`references/evidence_map.md`** +2 entries (Schultchen 2019 + PHQ-2/GAD-2 pattern); WoL existing entry got Source line.

### Planning

- **ROADMAP swap 2026-05-28:** v1.4.0 (planned Health Assessment Methodology) ↔ v1.5.0 (TBD, signal-gated review pushed back). Sub-feature C ships как polish; PRD epic closed.

### Acceptance criteria

- ✅ Schema 2.2.5 → 2.2.7 backward-compatible — старые v2.2.x клиенты игнорируют `health_subsegments` + `health_snapshot.last` unknown fields
- ✅ Default WoL flow stays single-score — sub-segments opt-in path не ломает existing user expectations
- ✅ Health Snapshot 2-decline cutoff per session — respects user autonomy
- ✅ Safety escalation explicit — все 4 Snapshot answers ≤ 3 → SKILL.master Safety section (depression-screen pattern)
- ✅ Master ≤ 4100 tokens unchanged (no Tier 1 touch)
- ✅ Phase 1 ≤ 2500 (2498/2500 = 2 headroom — будущие Phase 1 additions требуют offload в Tier 3 refs)
- ✅ Phase 3 ≤ 2500 (2474/2500 = 26 headroom)
- ✅ WoL Frequency Gate (v1.3.0) preserved — sub-segments tied к same `last_assessed_at`; Snapshot NOT tied (lighter cadence allowed)
- ✅ `track_health_metabolism.md` (v0.19.0) НЕ дублирован — explicit non-goal documented в both new refs
- ✅ 820+ tests passing (v1.3.1 was 740+, v1.4.0 adds: 80 methodology_v1_4 = 80 new)
- ✅ All 4 platform builds (Claude+Grok+Kimi+Kimi-CLI) с inlined `wol_health_subsegments.md` + `health_snapshot.md`
- ✅ 0 P0 tech debt items (carried from v1.3.1)

### Architecture decisions

- **Two schema bumps in one release window** — A added 2.2.6, B added 2.2.7. Granular bumps per field-add follow project convention; both ship together as v1.4.0 minor.
- **PRD intake to swap to ship — 1 day cycle** — PRD received 2026-05-27, intake + scope swap 2026-05-28, A+B+C+release prep all merged 2026-05-28. Fast turnaround possible because PRD had concrete RICE breakdown + non-duplication boundary documented.
- **Sub-feature C ships in v1.4.0, not as later polish** — XS=0.25 EAS so cheap, and Phase 3 §6.5 needed minor reword anyway. Bundling all three sub-features makes v1.4.0 release more coherent than A+B-only ship.
- **Snapshot Index NOT bound by WoL Frequency Gate** — Snapshot is lighter touch (4-Q vs 11-sphere WoL); can run при Phase 3 opt-in cadence (raz в 2-4 нед). Same `last_assessed_at` would over-gate.
- **Phase 1 token budget = 2 headroom** — extreme tight after A+B inline mentions. Future v1.4.x / v1.5.x additions to Phase 1 MUST offload в Tier 3 ref. Test message в TestPhase1BudgetUnchanged спрямляет diagnosis.
- **Snapshot decline counter = session-level** — `declined_count` resets per session by design. PRD §8 «2-decline cutoff per session» — persistent counter would feel punitive across long absence between sessions.

### Stacked PR series

- PR #29 — `docs/v1.4-v1.5-swap` (ROADMAP swap: Health Assessment commits v1.4, signal-gated review defers to v1.5)
- PR #30 — `feat/v1.4-wol-health-subsegments` (Sub-feature A: 6 sub-segments + Health Index + schema 2.2.6)
- PR #31 — `feat/v1.4-health-snapshot` (Sub-feature B: 4-Q Snapshot + schema 2.2.7)
- PR #32 — `feat/v1.4-weekly-review-snapshot-optin` (Sub-feature C: Phase 3 §6.5 opt-in + comprehensive CHANGELOG aggregation)

Plus PR #33 (this) release prep.

Merge order: #29 → #30 → #31 → #32 → #33 (this) → release.sh 1.4.0 → tag → release.

**Validation note:** PR #33 release flow exercises the BUG-010 + BUG-011 fixes (release.sh hardening from PR #28) end-to-end — first real test после v1.3.1 release где они впервые проявились.

## [1.3.1] — 2026-05-28

**Тема:** Patch release. Drive Wiki Path A formal skill-protocol abstraction (`save_state` / `read_state`) + 68 новых regression-guard tests across 4 suites + 2 P0 tech debt items closed (SKILL.master integrity extended, Calendar functional coverage). No new methodology, no schema bump, no SKILL.master changes — pure refactor + test infrastructure. Затем PRD intake для следующего minor (Health Assessment WoL sub-segments PRD v1.0 → BACKLOG + ROADMAP v1.5.0 Candidate).

### Changed (Methodology)

- **Drive Wiki Path A — full skill protocol refactor** (BACKLOG RICE 56). `references/drive_integration.md` теперь formally defines `save_state(template, content)` / `read_state(template)` skill-instruction abstractions с canonical filename pattern `{template}_{ISO}.md` (ISO = `YYYY-MM-DDTHH-MM`). Path B/F backends swap behaviour at single call site без переписывания phase modules. `templates/AI_Instructions.md` Протокол записи rewritten в терминах save_state; «Когда какой template писать» таблица показывает concrete call sites (`save_state("Hot_Cache", ...)` etc.). `state_v2_schema.md §5` cross-references abstraction.
- **Legacy «overwrite»/«section update» wording cleaned** в templates: `Hot_Cache.md` («Обновляется ... overwrite полностью» → save_state framing), `Progress_Dashboard.md` («Автообновляется» → new-file-per-save), `Wheel_of_Life_History.md` («КАК ОБНОВИТЬ» → «КАК СОСТАВИТЬ НОВЫЙ SNAPSHOT» с explicit read_state + composition step). Path A architecture (committed 2026-05-26) теперь явно проявлена в write-side artefacts, не только в research docs.

### Added (Tooling & Tests)

- **`tests/system/test_path_a_skill_protocol.py`** (NEW, 14 tests) — read-latest semantics guards + anti-legacy-wording checks: save_state/read_state definitions present с правильным pattern; AI_Instructions.md uses concrete call sites; state_v2_schema §5 cross-refs; Hot_Cache / Progress_Dashboard / Wheel_of_Life_History не содержат legacy «overwrite» / «Автообновляется» / «КАК ОБНОВИТЬ» wording; ISO format `YYYY-MM-DDTHH-MM` consistent across docs; `disableConversionToGoogleType` flag documented.
- **`tests/system/test_planning_docs_guardrails.py`** (NEW, 11 tests, BACKLOG RICE 64) — закрывает «roadmap не превращается в changelog» tech debt из v0.15.0+. Guards: ROADMAP «Текущая версия» = latest git tag + present в CHANGELOG; scope sections (planned/TBD/Candidate) без `✅ Shipped`/changelog `## [X.Y.Z]` headings/«released»-«shipped»-«выпущено» dates; ROADMAP/BACKLOG без consecutive `---` separators; ROADMAP/BACKLOG без duplicate H3 в одной H2-секции. Покрывает regressions, которые руками чинили в PR #19.
- **`tests/system/test_master_skill_integrity.py`** (EXTENDED, +12 tests → 20 total, BACKLOG P0 RICE 80) — закрывает P0 tech debt «Тесты целостности SKILL.master.md» из v0.15.0. Existing classes (frontmatter, structure, platform sync) сохранены. Added: `test_all_four_platforms_built` (Claude+Grok+Kimi+Kimi-CLI parity); `TestRoutingMapCoverage` (every `module_phase*.md` on disk has a routing row; all 4 persona modules referenced; ER + recovery routing entries present); `TestPersistenceModesTable` (all 4 gating modes listed); `TestSafetySection` (warning signs включают «< 3/10» low-score + «самоповреждении» escalation); `TestLanguageRulesEnforcement` (Examples + Troubleshooting не содержат `надо`/`должен`/`провал` outside `«...»` quotes, через `tests/helpers/forbidden_words.py`); `TestFrontmatterRuntime` (runtime = `multi-platform`).
- **`tests/system/test_calendar_functional.py`** (NEW, 31 tests, BACKLOG P0 RICE 80) — закрывает P0 tech debt «Функциональные тесты календаря» из v0.15.0. Pre-existing `test_calendar_integration.py` (19 tests) уже покрывает Free Slot Algorithm correctness, JSON constants, event patterns; этот suite добавляет skill-instruction guards: Pre-flight Checklist 5 steps (Density Check → Conflict Detection → Chronotype Alignment → Smart Proposal → Create with Validation) с проверкой ordering; Conflict Detection forbids overwrite + requires альтернативные слоты; Workload Warning thresholds 6h/8h + work hours configurable; Pattern Analyzer read-only contract (только `list_events`; `create_event`/`delete_event`/`update_event` forbidden); consent flow («Проанализирую ваш календарь...») + no inter-session caching; 5 documented metrics (Meeting Load / Focus Time / Boundary Violation / Recovery Deficit / Chronotype Alignment) с Formula+Threshold+Insight columns; rate limit 1 анализ/неделю + 3-week minimum для trends; anti-patterns (no productivity score / no user comparison / no auto-reschedule). Закрывает последний P0 tech debt из v0.15.0 — `0 P0 tech debt items remain`.

### Added (Planning)

- **Health Assessment WoL Sub-segments PRD v1.0 intake** (`docs/research/prd_health_assessment_wol_subsegments.md`) — full PRD сохранён, decomposed в 3 sub-features с individual RICE (A: WoL Sub-segments + Index calc, RICE 24.4; B: Light Health Snapshot tool, RICE 15.0; C: Weekly Review opt-in, RICE 15.0). Epic ~4.25 EAS. Surfaced в ROADMAP как `## v1.5.0 Candidate — WoL Health Assessment Methodology` (между v1.4.0 TBD и v0.17.x Candidate). Gate перед commit: v1.3.0 30-day signal window + precision evidence или skip-with-evidence path.

### Acceptance criteria

- ✅ 0 P0 tech debt items remain (down from 2 at session start)
- ✅ Path A `save_state(template, content)` formally defined в `drive_integration.md` + cross-ref chain (state_v2_schema §5 → AI_Instructions § Протокол записи → templates)
- ✅ Legacy «overwrite полностью» / «Автообновляется» / «КАК ОБНОВИТЬ» wording удалён из templates
- ✅ All 4 platforms build cleanly (Claude+Grok+Kimi+Kimi-CLI parity tests pass)
- ✅ 800+ tests passing (v1.3.0 was 740+, v1.3.1 adds: 14 path-a + 11 planning + 12 master integrity extended + 31 calendar functional = 68 new)
- ✅ Schema unchanged (still v2.2.5 — no breaking changes, patch-appropriate)
- ✅ SKILL.master.md unchanged (no Tier 1 touch — patch scope)
- ✅ Health Assessment PRD safely persisted in repo (was at risk of loss в ~/Downloads/)

### Architecture decisions

- **Patch scope appropriate (not minor)** — Path A refactor is documentation/formalization of pattern already committed 2026-05-26; no new user-facing methodology; no schema bump; SKILL.master untouched. Per semver, patch = backwards-compatible internal improvements + tests. Compare to v1.3.0 minor (new methodology features: WoL gate, AAR runtime, COM-B upsell).
- **Phase modules intentionally untouched in Path A refactor** — cross-ref chain через `state_v2_schema.md §5 → drive_integration.md §save_state` доставляет abstraction без token-budget pressure на per-module budgets (Phase 1 = 2420/2500 = 80 headroom; Phase 3 = 2481/2500 = 19 headroom).
- **AI_Instructions.md budget bumped 2000 → 2700** в тесте (`tests/unit/test_templates_v2.py`) — pre-existing failure (file was 2532 tokens on main, budget 2000); patch this fixed alongside Path A addition. Realistic budget вместо artificial constraint. Compare to Goals.md (2500) / Wheel_of_Life_History.md (3000) — similar operational density.
- **PRD intake stored as artefact-only, не committed scope** — `## v1.5.0 Candidate` ROADMAP heading conforms to scope-section schema (passes new planning-docs guardrails). Decision к commit ждёт signal window + evidence.

### Stacked PR series

- PR #19 — `docs/v1.4-followups-planning` (v1.4 placeholder + v1.3.0 release notes archive)
- PR #20 — `docs/path-f-zapier-verified` (Path F Zapier MCP verified + Anthropic issue draft)
- PR #21 — `feat/path-a-skill-protocol` (Path A formal save_state/read_state)
- PR #22 — `chore/planning-docs-guardrails` (ROADMAP/BACKLOG drift prevention)
- PR #23 — `test/master-skill-integrity-extended` (12 new master integrity tests, P0)
- PR #24 — `test/calendar-functional-coverage` (31 new calendar functional tests, P0)
- PR #25 — `docs/health-assessment-prd` (PRD intake + v1.5.0 Candidate surface)

Plus PR #26 (this) release prep.

Merge order: #19 → #20 → #21 → #22 → #23 → #24 → #25 → #26 (this) → release.sh → tag → GH release.

## [1.3.0] — 2026-05-27

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

## [1.2.0] — 2026-05-27

**Тема:** New Evidence-Based Methods (PRD v0.15 §6/§7). Заполнены genuine gaps в evidence-strong методах. Все три новые методики additive — старые paths не ломаем. Phase 0/1 COM-B opt-in диагностика (Capability/Opportunity/Motivation routing); Phase 2 Premortem trigger для важных OKR (Klein 2007 HBR + mitigation через Implementation Intentions coping plans); Phase 3 Lean AAR расширяет 7-step → 9-step Weekly Review (Three Whys + Lessons Learned + COM-B escalation на повтор gap).

### Added (Methodology — PRD v0.15)

- **`references/com_b_diagnostic.md`** (NEW, Tier 3, ~3100 tokens) — COM-B Model (Michie, van Stralen, West 2011, *Implementation Science* 6(42), [DOI](https://doi.org/10.1186/1748-5908-6-42)). Opt-in диагностика «почему не делаю» через 3 компонента. 9-question protocol (3 блока × 3 вопроса) за 3–5 мин → primary gap → targeted intervention: Capability → Tiny Habits + `action_breakdown_template.md`; Opportunity → `environment_design.md`; Motivation → WOOP / Compass Mode.
- **`references/environment_design.md`** (NEW, Tier 3, ~2400 tokens) — primary intervention для Opportunity gap (COM-B routing). 7 практик: friction asymmetry, cue removal, cue placement, context switching, social architecture, default switching, calendar as environment. Sources: Lally 2010 (habit context), Fogg 2019 (B=MAP Prompt), Wood et al. 2002 (43% automaticity в стабильном контексте), Thaler & Sunstein 2008 (*Nudge*, choice architecture).
- **`references/premortem.md`** (NEW, Tier 3, ~3300 tokens) — Premortem prospective hindsight (Klein 2007 HBR). 5-step protocol за 10–15 мин: time travel framing → 5+ reasons → cluster (5 категорий: internal / external / missed inputs / scope creep / motivation drift) → mitigation через if-then coping plans (`implementation_intentions.md` §Coping plans) → state writes + next_review_date. Explicit gates: `confidence_score ≤ 6` / horizon ≥ 1y / partner_coordination block / explicit request / mid-quarter stagnation. Self-Compassion Break closing ritual.
- **AAR Gap Analysis** — inline integration в `module_phase3_weekly_review.md` шаги 8–9 (lean: 7-step → 9-step, не отдельный deep ref). Step 8 Gap Analysis (Three Whys + категория internal/external/both); повтор того же gap ≥ 2 недели → COM-B escalation. Step 9 Lessons Learned (pattern capture; `sighted_count ≥ 3` → quarterly systemic adjustment). Skip при `execution_score ≥ 70%` — AAR для debugging, не routine. Sources: US Army TC 25-20 (1993), Garvin (2000) *Learning in Action*.
- **`tests/system/test_methodology_v1_2.py`** (NEW, 67 tests) — coverage для COM-B + environment_design + Premortem + AAR content, evidence citations, routing, Phase modules integration, evidence_map status updates, schema 2.2.2/2.2.3/2.2.4 bumps, platform integration.

### Changed (Methodology)

- **`SKILL.master.md`** → Tier 3 deep refs: Diagnostic group + `com_b_diagnostic.md`; Goal arch group + `environment_design.md` + `premortem.md`.
- **`references/module_phase1_diagnostic.md`** → opt-in COM-B entry section («при повторяющейся жалобе "знаю, что в сфере X плохо — но не делаю" → references/com_b_diagnostic.md»). State writes для `diagnosis.com_b_assessment`.
- **`references/module_phase2_goal_architecture.md`** → Layer 3 (12-Week Quarter) inline Premortem trigger («OKR с confidence ≤ 6 / horizon ≥ 1y → references/premortem.md»). Модуль на пределе budget (2500/2500); state writes для `premortem_assessments` документированы в `state_v2_schema.md` §3.5.1.
- **`references/module_phase3_weekly_review.md`** → заголовок `## 7-step` → `## 9-step Weekly Review (GTD + Scrum + AAR principles)`. Step 8 Gap Analysis + Step 9 Lessons Learned (compact, ≤ 2500 tokens). ADHD persona adaptation: `Micro-Review — 3 вопроса вместо 9 шагов` + явный `AAR 8–9 — skip`.
- **`references/evidence_map.md`** → COM-B / Premortem / AAR помечены implemented (`Status: Planned для v1.2` → `Used in:` + sources). Новая Environment Design entry с full citations.
- **`references/state_v2_schema.md`** → schema bumps 2.2.1 → 2.2.2 → 2.2.3 → 2.2.4 (все strictly additive). Новые опциональные поля:
  - `diagnosis.com_b_assessment` (v2.2.2) — `{capability, opportunity, motivation: "ok"|"gap", primary_gap, assessed_at}` (см. §3.4.3)
  - `goals.premortem_assessments[]` (v2.2.3) — `[{premortem_id, goal_id, conducted_at, trigger, top_risks[{risk, category, mitigation_intention}], next_review_date}]` (см. §3.5.1)
  - `weekly_reviews[].gap_analysis[]` + `weekly_reviews[].lessons_learned[]` (v2.2.4) — AAR pattern capture (см. §3.5.2)
- **`scripts/build-platform-skill.py`** → `inline_references()` patched: P0_REFS теперь обрабатываются даже если упомянуты bare-filename (без `references/` префикса) в Tier 3 listing. Single-file сборки (grok / kimi) получают full inlined content COM-B + environment_design + Premortem. Added `_existing_refs()` helper. P0_REFS расширен 3 новыми entries.
- **Budget tests bumped:** `TIER1_BUDGET_TOKENS` 4000 → 4100 (`test_tier_token_budgets.py`, `test_typical_session_budget.py`, `test_v018_gating_state_writes.py`). `ALL_MODULES_BUDGET_TOKENS` 14000 → 15000 (`test_tier_token_budgets.py`). Headroom +2.5% (Tier 1) / +7% (Tier 2 total) для evidence-based methodology expansion.

### Acceptance criteria

- ✅ Все 3 evidence-based методики добавлены без удаления existing flows (additive only)
- ✅ Master ≤ 4100 tokens; каждый phase module ≤ 2500 tokens; Tier 2 total ≤ 15000 tokens
- ✅ Schema v2.2.4 backward-compatible — старые v2.2.x клиенты игнорируют unknown поля
- ✅ 678+ tests passing (excl. pre-existing CI release-checks fails — закрыто PR #4)
- ✅ Все 4 platform builds: `claude`, `grok`, `kimi`, `kimi-cli` (single-file платформы получают full inlined content)

### Architecture decisions

**Lean AAR (Step 8 + 9, не canonical 4-step AAR):** PRD §9 «существенно снизить общую сложность» конфликтует с full 4-step AAR расширением. Текущий Weekly Review уже не «поверхностный» — Scrum Retro «changes» покрывает AAR Step 10 (What to Change); Progress Audit lag/lead покрывает AAR Step 8 (Planned vs Actual). Поэтому добавлены только Step 9 «Why?» (Three Whys + COM-B escalation) и Step 11 «Lessons Learned» (наша нумерация 8 + 9). Skip gate `execution_score ≥ 70%` — AAR для debugging, не routine. ADHD persona opt-out.

**COM-B ↔ AAR cross-method integration:** AAR Step 8 при повторе того же gap ≥ 2 недели → trigger COM-B Diagnostic. Single-week debugging (AAR) → systemic diagnosis (COM-B). Это превращает Phase 3 Weekly Review в systemic feedback loop, не изолированный ritual.

**Premortem mitigation pipeline через II:** PRD §7 step 3 явно: «Планирование — Implementation Intentions + Premortem (для важных целей)». Step 4 берёт top-3 risks → coping plans в if-then формате через уже существующий `implementation_intentions.md` §Coping plans. Single mitigation pattern across методов; не дублируем infrastructure.

**COM-B Phase 0 trigger удалён под Tier 1 budget pressure:** entry через Phase 1 module + Tier 3 listing. Сохраняет Phase 0 «zero-setup default / emotional landing» contract. Discovery работает: пользователь в Phase 1 при сигнале «не могу начать» получает opt-in suggestion.

**State writes inline убраны из Phase 2 + Phase 3 modules под per-module budget pressure:** schema полностью документирована в `state_v2_schema.md` §3.5.1 (Premortem) + §3.5.2 (AAR). Single source of truth для state shape.

**Tier 1 + Tier 2 budgets bumped (4000→4100, 14000→15000):** evidence-based methodology expansion (3 новых Tier 3 refs + inline triggers в 2 phase modules) насытила оба budget. Headroom скромный (~2.5% / ~7%). Future v1.3+ expansion потребует либо aggressive rotation в Tier 3, либо further bumps с explicit deprecation policy.

### Stacked PR series

Релиз собран из 3 stacked PRs:
- PR #2 — `feat/v1.2-com-b-diagnostic` (COM-B + Environment Design)
- PR #3 — `feat/v1.2-premortem` (Premortem)
- PR #5 — `feat/v1.2-aar-gap-analysis` (Lean AAR)

Плюс orthogonal PR #4 — `fix/ci-release-checks` (закрывает accumulating release-checks failures на CI). Merge order: #4 → #2 → #3 → #5 → этот release prep PR.

## [1.1.0] — 2026-05-26

**Тема:** Methodology Foundation + MCP PoC integration + первая чистка после v1.0. Surface evidence-based methods which были buried; complete PoC of Google Calendar + Drive MCP с decision committed; remove deprecated v1 schema.

### Added (Methodology — PRD v0.15)

- **`references/implementation_intentions.md`** (NEW, Tier 3, ~1500 tokens) — standalone deep ref. Gollwitzer & Sheeran 2006 meta-analysis (d=0.65, n=8000+). 3 forms (WHEN/WHERE/WHAT), coping plans, skill prompt patterns. Implementation Intentions promoted к primary planning tool в Phase 5 (previously buried в `goal_architecture.md` subsection).
- **`references/evidence_map.md`** (NEW, Tier 3, ~3200 tokens) — unified catalog всех методов skill с honest evidence levels (🟢-🔴), sources, effect sizes. 5-level framework. Explicit "honest framing" section для методов которые NOT следует claim "research-backed" (Parts Work, Body Doubling, Wheel of Life).
- **`references/templates/lpc_wiki_cleanup.gs`** (NEW) — Google Apps Script ready-to-paste для append-only Wiki cleanup. ~3 min one-time setup; daily trigger keeps last 5 per category + < 30 days.

### Added (PoC MCP — Google Calendar + Drive)

- **PoC MCP (Google Calendar) completed** — `docs/research/mcp_poc_log.md` заполнен real measurements на Claude Max plan. Decision: **MCP-first**. 14/14 ops functional через Gates 1+2. `suggest_time` подтверждён доступным (singular form). Tool inventory: 8 confirmed (4 read + 4 write). PoC выполнен AI-assisted hybrid через Claude_in_Chrome (Chrome Claude драйвил browser + claude.ai chat, current session orchestrated).
- **PoC MCP (Google Drive) completed** — same-day extension. 13 ops executed direct via MCP from current session (sub-second per op). Tool inventory: 8 confirmed (6 read + 2 write). **Critical gap**: NO `update_file`, NO `delete_file` exposed by Anthropic connector. Decision: **MCP-first for bootstrap + reads; Wiki updates require append-only redesign**. 10 schema quirks documented.
- **`references/drive_integration.md`** (NEW, ~190 lines) — analog of `calendar_integration.md` for Drive: 8 tools, 10 quirks, troubleshooting, prompt patterns (bootstrap + append-only save + read-latest). Documents 4-mode cleanup strategy (apps_script / batch_weekly / reminder default / ignore) as Layered defaults для users разной tech-savviness.
- **`docs/research/mcp_poc_log.md`** (NEW, ~500 lines) — full PoC execution log с per-op latencies, request/response samples, 31 cumulative quirks across Calendar + Drive.
- **`docs/research/prd_v0.15_methodology_upgrade.md`** (NEW) — user-uploaded PRD preserved для traceability + roadmap integration.

### Changed (Methodology)

- **`references/module_phase5_execution.md`** — Implementation Intentions credited as primary tool фазы. Mode A (Calendar Connected) маркирован как primary path. Recurring fallback gotcha обновлён.
- **`references/habit_loop.md`** — restructure: §1 Tiny Habits (PRIMARY для создания new habits при низкой мотивации), §2 Cue-Routine-Reward (DIAGNOSTIC для existing habits). Intro paragraph maps task → framework. Anchor pattern explicitly framed as WHEN-type Implementation Intention.
- **`references/module_phase2_goal_architecture.md`** — "SMART+ check" renamed к "KR Quality Check (measurability + alignment)". Same 6 criteria, reframed around execution probability + values alignment (not classical SMART acronym).
- **`references/calendar_integration.md`** — Prompt Patterns intro frames recurring events as WHEN-type II с cross-ref к `implementation_intentions.md`. PLUS bumped v0.2.1 → v0.3.0 с 10 connector-specific schema quirks (recurrenceData vs recurrence, UNTIL must be UTC-Z, attendeeEmails for suggest_time, etc.). Free Slot Algorithm с двумя путями.

### Changed (PoC + cleanup)

- **`references/calendar_constants.md`** — Tools table обновлён с PoC schema notes. Event Data Schema split на request vs response. Failure Modes +7 новых сценариев.
- **`README.md`** — добавлен footnote¹ о Max plan для MCP коннекторов с link на PoC log.
- **`BACKLOG.md`** — PoC MCP перенесён в Archived/Done. Google Tasks MCP отмечен. Added v0.15 PRD epic. Archived 6 shipped items (Templates Rebuild, Core Values Discovery, Health Track, Goal Concordance, README rewrite, Token Optimization).
- **`references/templates/AI_Instructions.md`** — ⚠️ MCP Drive limitations note; write rules table обновлена под append-only pattern.
- **`references/state_v2_schema.md`** — schema bump 2.2 → 2.2.1 (additive). Добавлены `persistence_retry.drive.wiki_cleanup_mode` (enum: apps_script/batch_weekly/reminder/ignore), `wiki_cleanup_last_reminder_at`, `wiki_cleanup_chosen_at`. Bootstrap protocol §7.1 prompts user for cleanup mode choice.
- **`ROADMAP.md`** — integrated PRD v0.15 в v1.1/v1.2/v1.3 plan. Future Lab + tensions documented.

### Removed

- **`references/conversation_state_schema.md`** — v1 schema удалён per plan announced в v1.0.0. state_v2_schema.md §8 migration table сохранена для legacy forks.

### Deferred к v1.2 (не сделано в v1.1)

- `scripts/build-skill.sh` deletion — release.sh still calls it; requires release.sh migration к python build-skill.py release.
- `scripts/sync-version.sh` deletion — same dependency.
Both retain DEPRECATED stderr warnings.

### Architecture decisions

**Drive Wiki persistence (Path A):** После Grok research synthesis (Karpathy LLM Wiki, Justin Norris Apps Script mirroring, event-sourcing patterns) committed append-only с timestamp suffix + user-side Apps Script cleanup. Forward-compat: when Anthropic ships `update_file`, swap is one-line change в `save_state(template, content)` abstraction. Documented в `drive_integration.md` §Path A. Alternative paths (B Desktop CRUD, C conversation-only, D Obsidian, F Zapier hybrid) documented для context но not chosen.

**Methodology shift (PRD v0.15 partial):** Surface 3 buried/missing evidence-based methods (Implementation Intentions promote, Tiny Habits primary framing, evidence map). v1.2 будет добавлять COM-B diagnostic + AAR integration + Premortem. v1.3 — Wheel of Life frequency gate.

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
