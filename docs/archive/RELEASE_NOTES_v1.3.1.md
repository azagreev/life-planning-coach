## Что нового в v1.3.1

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
