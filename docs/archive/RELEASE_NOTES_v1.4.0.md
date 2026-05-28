## Что нового в v1.4.0

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
