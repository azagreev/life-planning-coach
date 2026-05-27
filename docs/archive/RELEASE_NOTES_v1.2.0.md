## Что нового в v1.2.0

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
