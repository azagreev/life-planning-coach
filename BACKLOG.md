# Backlog

> **Для кого:** Внутреннее планирование, идеи без committed версии, research debt и техдолг.  
> **Принцип:** Каждая активная идея имеет триггер и RICE score.  
> **Баги:** Активные баги — в [BUGS.md](BUGS.md).  
> **История:** Выпущенные версии — в [CHANGELOG.md](CHANGELOG.md). Старый backlog сохранён в [docs/archive/BACKLOG_before_cleanup_2026-05-21.md](docs/archive/BACKLOG_before_cleanup_2026-05-21.md).

---

## Формат RICE

```
RICE = (Reach × Impact × Confidence) / Effort

Reach: % целевой аудитории (0-100) [GUESS, если нет данных]
Impact: 0.25 minimal → 3.0 massive
Confidence: 0-100%
Effort: Estimated AI Sessions (EAS) + Context Pressure
```

| RICE | Категория | Действие |
|------|-----------|----------|
| > 30 | Quick Win | Немедленно |
| 10-30 | High Priority | Следующий спринт |
| 3-10 | Medium Priority | Backlog |
| < 3 | Moonshot | Исследовать позже |

---

## Active Candidates

### Track 0 Micro-Goal + Tiny Habits unified framework

- **Описание:** Быстрый путь от первого сообщения до одного маленького поведения сегодня. Объединяет Track 0 onboarding (Best Hopes → Scaling → One Small Step → If-Then) с Tiny Habits (BJ Fogg B=MAP). Implementation Intentions как primary "Plan" tool.
- **Триггер:** PRD v0.15 emphasizes Tiny Habits + Implementation Intentions; existing Track 0 research aligned.
- **Статус:** 📋 Track 0 research готов; Tiny Habits/II promote запланирован в v1.1.0 (см. ROADMAP). После v1.1.0 — оценить, нужен ли отдельный Track 0 onboarding flow или integration в Phase 0/0.5 достаточно.
- **RICE (consolidated):** Reach 70 × Impact 2.0 × Confidence 80% / Effort M=2 EAS, Context Pressure Medium = **56.0** (Quick Win).
- **Артефакты:** `docs/research/track0_micro_goal_research.md` (research); v1.1.0 promotes Tiny Habits + II в habit_loop.md + Phase 5; possible new `references/track0_micro_goal.md` после v1.1 если нужен отдельный flow.
- **Риск:** Track 0 как Phase 0 entry vs supplement — TBD после v1.1.0 опыта.

<!-- README rewrite → archived in v0.19.0 (см. CHANGELOG). Originally RICE 120.0. -->

### Реализовать PRD v0.15 Methodology Upgrade

- **Описание:** Surface buried evidence-based methods (Implementation Intentions, Tiny Habits) + add genuine gaps (COM-B, AAR principles, Premortem); refactor Wheel of Life к frequency-gated optional. См. полный PRD: `docs/research/prd_v0.15_methodology_upgrade.md`.
- **Триггер:** PRD получен 2026-05-26, gap analysis done, roadmap drafted.
- **Статус:** 📋 Roadmap committed (v1.1 + v1.2 + v1.3). См. ROADMAP.md.
- **RICE (epic):** Reach 80 × Impact 2.0 × Confidence 75% / Effort L=4 EAS (across 3 minor releases), Context Pressure Medium = **30.0** (Quick Win epic). Subtasks с individual RICE в ROADMAP.
- **Артефакты:** PRD в `docs/research/`; новые refs (implementation_intentions, com_b_diagnostic, premortem); reframed habit_loop, weekly_review; state v2 schema bump для WoL.last_assessed_at.

### WoL Health Sub-segments + Light Health Snapshot (PRD v1.0)

- **Описание:** Усилить оценку сферы `health` в Колесе через 6 суб-сегментов (энергия, восстановление, физ. самочувствие, стрессоустойчивость, питание, общий резерв) → Health Index = avg → routing к лёгкому 4-вопросному Health Snapshot при Low/Middle. Snapshot = «middle ground» между one-shot WoL score и тяжёлым `track_health_metabolism.md` (7-рычаговая система, v0.19.0). См. полный PRD: [`docs/research/prd_health_assessment_wol_subsegments.md`](docs/research/prd_health_assessment_wol_subsegments.md).
- **Триггер:** PRD получен 2026-05-27 (v1.0); intake 2026-05-28; **scope committed к v1.4.0 — 2026-05-28** (swap с pre-existing v1.4 signal-gated review, которая теперь v1.5.0 TBD).
- **Статус:** 🚧 **Committed → v1.4.0 (planned)** в ROADMAP. Implementation в активной разработке. Sub-feature A первой.
- **RICE (epic):** Reach 50 × Impact 1.7 × Confidence 62% / Effort L=4.25 EAS, Context Pressure Medium = **12.4** (High Priority epic). Sub-features ниже.
- **Sub-feature A — WoL Health Sub-segments + Health Index calculation:**
  - 6 sub-segments scoring × WoL health sphere; avg → Health Index; identify weakest sub-segment; 4 категории (≥8 / 6.5-7.9 / 5-6.4 / ≤5).
  - State (additive): `diagnosis.wheel_of_life.current.health_subsegments` (object с 6 fields).
  - Phase 1 module update: per-persona-adapted scoring flow. Token risk: module at 2420/2500 (80 headroom); offload в new Tier 3 ref `references/wol_health_subsegments.md` если inline не помещается.
  - **RICE:** Reach 50 × Impact 1.5 × Confidence 65% / Effort M=2 EAS, CP Medium = **24.4** (High Priority).
- **Sub-feature B — Light Health Snapshot (4-question tool):**
  - New Tier 3 ref `references/health_snapshot.md` (~150 строк) — 4 вопроса + 4 persona adaptations + trigger logic.
  - State (additive): `diagnosis.health_snapshot.last = {date, average_score, weakest_subsegment}`.
  - Triggers: Health Index ≤ 5.5 OR explicit user request OR Phase 3 opt-in (см. Sub-feature C).
  - Routing: Phase 1 после WoL → если Low/Middle → Snapshot; результат → решение про deep-dive в `track_health_metabolism.md` (existing).
  - **RICE:** Reach 25 × Impact 2.0 × Confidence 60% / Effort M=2 EAS, CP Medium = **15.0** (High Priority). **Depends on Sub-feature A** (нужен health_subsegments в state).
- **Sub-feature C — Weekly Review opt-in для Health Snapshot:**
  - Phase 3 (Weekly Review) — optional Snapshot triggered (например, после Step 4 Reflect или как Tiny Habit check-in).
  - **RICE:** Reach 15 × Impact 0.5 × Confidence 50% / Effort XS=0.25 EAS, CP Low = **15.0** (High Priority). **Depends on Sub-feature B**. Bundle с B или ship отдельно как polish.
- **Артефакты:** PRD в `docs/research/`; sub-features A+B = schema bump 2.2.5 → 2.2.6 (additive, two new optional fields); new Tier 3 ref `wol_health_subsegments.md` (если offload нужен) + `health_snapshot.md`; tests в `tests/system/test_methodology_v1_*.py` под соответствующий release.
- **Не делаем (per PRD §9):** дублировать `track_health_metabolism.md`; создавать тяжёлый опросник здоровья; ломать WoL Frequency Gate (`last_assessed_at` из v1.3.0).
- **Риск:** Phase 1 token budget tight (80 headroom). Если sub-segments inline не помещаются — offload в new Tier 3 ref (Sub-feature A) обязателен. Альтернатива — trim других inline-секций Phase 1.
- **Риск:** Parts Work deferred (RICE 5, низкая evidence); "simplification" deferred (no specific pain identified).

### v1.2 follow-ups (epic) — ✅ Shipped в v1.3.0

- **Описание:** 6 items из code review PRs #2/#3/#5 (v1.2 series). 3 shipped в **v1.3.0**, 3 deferred to v1.4 candidates.
- **Статус:** ✅ Closed. См. CHANGELOG `## [1.3.0]` для shipped items, ROADMAP «v1.4.0 (TBD)» для deferred risks.

**Shipped в v1.3.0:**

1. ✅ **AAR sighted_count runtime** (RICE 120) — PR #17. Skill-instruction в Phase 3 Step 9: load last 4 weekly_reviews → semantic similarity → increment OR append. Surface при ≥ 3 → routing к Phase 2 / Phase 1.5.
2. ✅ **COM-B Phase 0 soft upsell** (RICE 126) — PR #13. `references/emotion_regulation.md` §5: opt-in upsell после ER protocol, 2-decline cutoff. Closes lean_conversation discovery gap.
3. ✅ **Trivial cleanup bundle** (RICE 180 avg) — PR #12. AGENTS §3.6/3.7 + forbidden-words helper + release-checks.yml explicit error.

**Deferred to v1.4 candidates (revisit ~30 дней пост-v1.3):**

4. ⏳ **Premortem triggers rank-order** — RICE 84. Awaiting signal: 2+ reports «Premortem fires слишком часто».
5. ⏳ **lessons_learned category drift** — RICE 56. Awaiting signal: sighted_count produces irrelevant matches.
6. ⏳ **`find dist` fragile pattern** — RICE 70. Awaiting first CI break на новом archive variant.

**Item NOT committed (offered, declined):**

- **ADR-001 budget bumps policy** — RICE 160. Erosion risk остаётся managed через AGENTS §3.6 State Writes Policy (added в v1.3.0); если в v1.4+ потребуется новый budget bump — explicit ADR.

### QA Hardening — надёжность, edge cases, безопасность

- **Описание:** Input validation, MCP timeout handling, prompt-injection reinforcement, human-friendly errors.
- **Триггер:** Внешнее QA-ревью или перед расширением MCP.
- **Статус:** 💡 Идея, аудит завершён.
- **RICE:** Reach 100 × Impact 2.0 × Confidence 70% / Effort M=2 EAS, Context Pressure Medium = **70.0** (Quick Win).
- **Артефакты:** Обновления `SKILL.master.md`, `references/calendar_integration.md`, тесты на invalid input/prompt injection/timeouts.
- **Риск:** Не превратить text-only skill в over-engineered runtime.

### UX Hardening — tone of voice, cognitive load, empty states

- **Описание:** Tone guide, quick-add путь для целей, empty states для первого входа/0 целей/0 привычек/0 прогресса.
- **Триггер:** Внешнее UX-ревью или жалобы на тяжёлый onboarding.
- **Статус:** 💡 Идея, аудит завершён.
- **RICE:** Reach 80 [GUESS] × Impact 1.5 × Confidence 70% / Effort M=2 EAS, Context Pressure Medium = **42.0** (Quick Win).
- **Артефакты:** `references/tone_of_voice_guide.md`, `references/empty_states.md`, tests for forbidden words/tone consistency.
- **Риск:** Слишком жёсткий tone guide может конфликтовать с adaptive communication style.

<!-- The following items have shipped — moved to Archived/Done section below:
     - Templates Rebuild v1.0 → v1.0.0
     - Core Values Discovery (Compass Mode) → v0.18.0
     - Health & Metabolism Track → v0.19.0
     - Goal Concordance / Romantic Relationships → v0.19.0
-->


### Drive Wiki Path A — full skill protocol refactor ✅ Shipped 2026-05-28

- **Статус:** ✅ Closed via `feat/path-a-skill-protocol` branch. Phase modules не редактировались (cross-ref chain через state_v2_schema.md §5 → drive_integration.md §save_state работает без token-budget давления). См. CHANGELOG `[Unreleased]` для shipped items.
- **Shipped artefacts:**
  - `drive_integration.md` — formal `save_state(template, content)` / `read_state(template)` definitions с filename pattern `{template}_{ISO}.md` + Path B/F swap note
  - `templates/AI_Instructions.md` — Протокол записи rewritten в терминах save_state; «Когда какой template писать» таблица с concrete call sites
  - `templates/Hot_Cache.md` + `Progress_Dashboard.md` — legacy «overwrite полностью» / «Автообновляется» wording → save_state framing
  - `templates/Wheel_of_Life_History.md` — «КАК ОБНОВИТЬ» → «КАК СОСТАВИТЬ НОВЫЙ SNAPSHOT» (composition, не in-place edit)
  - `state_v2_schema.md §5` — write-abstraction cross-ref
  - `tests/system/test_path_a_skill_protocol.py` — 14 read-latest semantics + anti-legacy-wording guards
- **RICE (исторически):** Reach 70 × Impact 2.0 × Confidence 80% / Effort M=2 EAS, Context Pressure Medium = **56.0** (Quick Win).

### File Anthropic GitHub issue evidence (Path E lobbying)

- **Описание:** Filing evidence про Drive MCP write-tools gap (`update_file`/`delete_file` missing) с reference на наш `mcp_poc_log.md` §Drive PoC. Aim: усилить signal к Anthropic team на приоритизацию.
- **Триггер:** PoC 2026-05-26 unique quantified evidence; existing [anthropics/claude-code#51040](https://github.com/anthropics/claude-code/issues/51040) labeled `invalid` (wrong repo — claude.ai connector issues belong в [anthropics/claude-ai-mcp](https://github.com/anthropics/claude-ai-mcp)).
- **Статус:** 📋 Ready to file. Draft + one-click prefill URL в [docs/drafts/anthropic_mcp_drive_issue.md](docs/drafts/anthropic_mcp_drive_issue.md); requires user action — нельзя комментить external repo от имени проекта без user OAuth context.
- **RICE:** Reach 100 [GUESS] × Impact 0.5 × Confidence 30% / Effort XS=0.25 EAS, Context Pressure Low = **60.0** (Quick Win).
- **Артефакты:** [docs/drafts/anthropic_mcp_drive_issue.md](docs/drafts/anthropic_mcp_drive_issue.md) — self-contained issue body (title + summary + PoC evidence + workaround + ask) + prefill URL для one-click filing в `anthropics/claude-ai-mcp` + post-filing close-out checklist.
- **Риск:** No guarantee on Anthropic response; low cost regardless.

### Интеграция с Google Tasks MCP

- **Описание:** Синхронизация Daily Top-3 с Google Tasks через MCP.
- **Триггер:** Tasks API становится доступен через MCP в целевой платформе.
- **Статус:** ⏳ Ожидание внешнего события. **PoC 2026-05-26 confirmed:** Google Tasks отсутствует в Anthropic MCP directory (на Max plan). Тем временем — conversational Daily Top-3 (см. `calendar_integration.md` §Daily Top-3 Text-Only).
- **RICE:** Reach 45 [GUESS] × Impact 1.5 × Confidence 40% / Effort L=3 EAS, Context Pressure High = **9.0** (Medium Priority).
- **Риск:** Зависимость от внешней платформы и OAuth scope.

### Групповой коучинг

- **Описание:** Парный или групповой coaching flow для 2+ участников.
- **Триггер:** 5+ пользователей запросят групповой формат.
- **Статус:** 💡 Идея.
- **RICE:** Reach 20 [GUESS] × Impact 1.0 × Confidence 30% / Effort XL=5 EAS, Context Pressure High = **1.2** (Moonshot).
- **Риск:** Сложность privacy, consent и conflict handling.

### Мультиязычность

- **Описание:** Поддержка английского языка или EN/RU toggle.
- **Триггер:** 10+ запросов от англоязычных пользователей.
- **Статус:** 💡 Идея.
- **RICE:** Reach 35 [GUESS] × Impact 1.5 × Confidence 45% / Effort XL=5 EAS, Context Pressure High = **4.7** (Medium Priority).
- **Риск:** Cross-lingual consistency и удвоение тестовой матрицы.

### Social accountability

- **Описание:** Permission-based напоминания партнёру/другу или accountability check-in.
- **Триггер:** 3+ пользователя запросят социальную ответственность.
- **Статус:** 💡 Идея.
- **RICE:** Reach 25 [GUESS] × Impact 1.0 × Confidence 35% / Effort L=3 EAS, Context Pressure High = **2.9** (Moonshot).
- **Риск:** Privacy, consent, эмоциональное давление.

---

## Research Debt

<!-- Token Optimization Audit → addressed в v0.17.0 через tiered IA refactor (cold-load 50K → 4K = ~92% reduction). Moved to Archived/Done. -->


### Cross-Lingual Consistency

- **Описание:** Проверить code-switching артефакты между README, frontmatter, SKILL instructions и platform files.
- **Триггер:** Обнаружена пользователем 2026-05-20.
- **Статус:** 🔍 Идентифицирована проблема.
- **RICE:** Reach 100 × Impact 1.0 × Confidence 70% / Effort S=1 EAS, Context Pressure Medium = **70.0** (Quick Win).
- **TODO:** Retrieval accuracy tests, platform-файлы, решение по языку README.

### Google Health MCP integration research

- **Описание:** Выбрать безопасный путь интеграции health/wearable data: hosted MCP, local bridge или custom connector.
- **Триггер:** v0.16 candidate decision.
- **Статус:** 🔬 Research completed, implementation не утверждена.
- **RICE:** Reach 40 [GUESS] × Impact 2.0 × Confidence 45% / Effort XL=5 EAS, Context Pressure Crit = **7.2** (Medium Priority).
- **Артефакт:** `docs/research/google_health_mcp_integration_research.md`.
- **Риск:** Высокая privacy/security нагрузка.

### Body Doubling via AI

- **Описание:** AI-assisted body doubling prompts/session flow для удержания внимания и начала действий.
- **Триггер:** Retention проблема становится критичной.
- **Статус:** 🔬 Research direction.
- **RICE:** Reach 35 [GUESS] × Impact 1.5 × Confidence 35% / Effort L=3 EAS, Context Pressure High = **6.1** (Medium Priority).

### Wearable Energy Integration

- **Описание:** Подключение wearable signals для energy-aware planning.
- **Триггер:** Wearable MCP servers становятся stable.
- **Статус:** 🔬 Research direction.
- **RICE:** Reach 30 [GUESS] × Impact 2.0 × Confidence 30% / Effort XL=5 EAS, Context Pressure Crit = **3.6** (Medium Priority).

---

## Tech Debt

| Задача | Приоритет | Триггер | RICE | Примечание |
|--------|-----------|---------|------|------------|
| ~~Функциональные тесты календаря~~ | P0 | ✅ 2026-05-28 | 100 × 2.0 × 80% / M=2, CP Med = **80.0** | Shipped. Pre-existing: `tests/system/test_calendar_integration.py` (19 tests — Free Slot Algorithm correctness, JSON constants, event patterns Weekly/WOOP, failure modes) + `test_calendar_tone.py` (3 tests). Extended (this session): `tests/system/test_calendar_functional.py` (31 tests) — Pre-flight Checklist 5 steps + ordering; Conflict Detection forbids overwrite + requires alternatives; Workload thresholds 6h/8h + configurable work hours; Pattern Analyzer read-only contract (only `list_events`; `create_event`/`delete_event`/`update_event` forbidden); consent flow + no inter-session caching; 5 metrics (Meeting Load / Focus Time / Boundary Violation / Recovery Deficit / Chronotype Alignment) + Formula/Threshold/Insight columns; rate limit 1/week + 3-week minimum for trends; anti-patterns (no productivity score / no user comparison / no auto-reschedule). |
| ~~Тесты целостности `SKILL.master.md`~~ | P0 | ✅ 2026-05-28 | 100 × 2.0 × 80% / M=2, CP Med = **80.0** | Shipped: `tests/system/test_master_skill_integrity.py` (20 tests, +12 extended). Базовое covered ранее: frontmatter, version=tag, ≥10 trigger phrases, required H2 sections, generic Assistant examples, reference link existence, platform-agnostic body, Claude SKILL = root SKILL. Extended (this session): all 4 platforms built; Routing Map references every `module_phase*.md` + ER + recovery; all 4 persona modules referenced; Persistence Mode table lists 4 modes; Safety section has warning signs (< 3/10 + самоповреждение); Examples/Troubleshooting не содержат `надо`/`должен`/`провал` outside `«...»` quotes; frontmatter.runtime = `multi-platform`. |
| Coverage report + badge | P1 | v0.15.0 | 80 × 1.0 × 75% / S=1, CP Low = **60.0** | `pytest-cov`, минимум 85%, badge в README |
| Pre-commit hooks | P1 | v0.15.0 | 80 × 1.0 × 70% / S=1, CP Med = **56.0** | `ruff`, `mypy`, whitespace |
| Универсальный скрипт сборки | P2 | v0.15.0+ | 60 × 1.0 × 70% / M=2, CP Med = **21.0** | Единый `build-skill.py` |
| ~~Planning docs guardrails~~ | P2 | ✅ 2026-05-28 | 80 × 0.5 × 80% / XS=0.5, CP Low = **64.0** | Shipped: `tests/system/test_planning_docs_guardrails.py` (11 tests). Guards: ROADMAP «Текущая версия» = latest git tag + present в CHANGELOG; scope sections (planned/TBD/Candidate) без ✅ Shipped / changelog headings / released dates; no consecutive `---`; no duplicate H3 в одной H2-секции. |
| Timezone edge-case hardening | P2 | v0.16 candidate | 60 × 1.0 × 60% / M=2, CP Med = **18.0** | Travel, DST, смена рабочей зоны |

---

## Archived / Done

Детальные completed specs больше не хранятся в активном backlog. Источники:

- [CHANGELOG.md](CHANGELOG.md) — факты по выпущенным версиям.
- [ROADMAP.md](ROADMAP.md) — будущий committed scope.
- [docs/archive/BACKLOG_before_cleanup_2026-05-21.md](docs/archive/BACKLOG_before_cleanup_2026-05-21.md) — архив старого backlog.

Ключевые статусы, зафиксированные при чистке:

| Item | Версия | Details |
|------|--------|---------|
| Habit Loop | v0.8.0 | — |
| PDF export dashboard | — | `window.print()` + print CSS |
| Timezone intelligence | — | Базовый schema/preset support; edge cases → tech debt |
| README rewrite + platform guides | v0.10.2 | — |
| Inclusive coaching references | v0.14.0 | — |
| Token Optimization Audit | v0.17.0 | Tiered IA (cold-load 50K → 4K) |
| Templates Rebuild v1.0 | v1.0.0 | State v2 + 8 wiki + data-driven dashboard |
| Core Values + Compass Mode | v0.18.0 | Phase 1.5 inline |
| Health & Metabolism Track | v0.19.0 | 7 evidence-based рычагов |
| Goal Concordance | v0.19.0 | Transactive Goal Dynamics |
| README rewrite (positioning) | v0.19.0 | Promise + comparison + quickstart |
| PoC MCP (Calendar + Drive) | 2026-05-26 | MCP-first decision; см. `docs/research/mcp_poc_log.md` |
| Verify Zapier MCP availability (Path F) | 2026-05-28 | ✅ Verified available на paid plans ([claude.com/connectors/zapier](https://claude.com/connectors/zapier)). Path F section added в `references/drive_integration.md` §Advanced. |

---

## Как работать с backlog

1. Новая идея попадает в `Active Candidates` или `Research Debt`.
2. У каждой активной записи должны быть триггер, статус и RICE.
3. Когда триггер сработал, задача переносится в `ROADMAP.md` с версией, приоритетом и acceptance criteria.
4. После релиза детали уходят в `CHANGELOG.md`; backlog хранит только активное и research debt.
