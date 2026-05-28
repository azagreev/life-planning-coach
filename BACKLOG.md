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


### Drive Wiki Path A — full skill protocol refactor

- **Описание:** Architecture committed (`references/drive_integration.md` §Path A): append-only с timestamp suffix + Apps Script auto-cleanup (`templates/lpc_wiki_cleanup.gs`). Осталось: refactor active session write protocols в `module_phase*.md` чтобы actually использовать pattern (currently legacy "overwrite"/"section update" wording in some modules).
- **Триггер:** Path A commit 2026-05-26 (после Drive PoC + Grok research).
- **Статус:** 📋 Architecture documented + Apps Script ready. Skill modules ещё не refactored под Path A protocol.
- **RICE:** Reach 70 × Impact 2.0 × Confidence 80% / Effort M=2 EAS, Context Pressure Medium = **56.0** (Quick Win).
- **Артефакты:** Update each `module_phase*.md` State Writes section с filename pattern `{Template}_{ISO}.md`; add `save_state(template, content)` abstraction helper для forward-compat; tests на read-latest semantics.
- **Риск:** Skill prompts длиннее (более explicit filename gen logic); legacy users могут нуждаться migration helper.

### File Anthropic GitHub issue evidence (Path E lobbying)

- **Описание:** Filing evidence про Drive MCP write-tools gap (`update_file`/`delete_file` missing) с reference на наш `mcp_poc_log.md` §Drive PoC. Aim: усилить signal к Anthropic team на приоритизацию.
- **Триггер:** PoC 2026-05-26 unique quantified evidence; existing [anthropics/claude-code#51040](https://github.com/anthropics/claude-code/issues/51040) labeled `invalid` (wrong repo — claude.ai connector issues belong в [anthropics/claude-ai-mcp](https://github.com/anthropics/claude-ai-mcp)).
- **Статус:** 📋 Ready to file. Draft text готов (см. session 2026-05-28); requires user action — нельзя комментить external repo от имени проекта без user OAuth context.
- **RICE:** Reach 100 [GUESS] × Impact 0.5 × Confidence 30% / Effort XS=0.25 EAS, Context Pressure Low = **60.0** (Quick Win).
- **Артефакты:** New issue в `anthropics/claude-ai-mcp` (preferred) ИЛИ comment на #51040 redirecting к right repo. Self-contained body с PoC findings highlights; link к public mcp_poc_log.md.
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
| Функциональные тесты календаря | P0 | v0.15.0 | 100 × 2.0 × 80% / M=2, CP Med = **80.0** | Free Slot Algorithm, event patterns, conflict detection, JSON validation |
| Тесты целостности `SKILL.master.md` | P0 | v0.15.0 | 100 × 2.0 × 80% / M=2, CP Med = **80.0** | Structure, cross-reference validation, platform sync |
| Coverage report + badge | P1 | v0.15.0 | 80 × 1.0 × 75% / S=1, CP Low = **60.0** | `pytest-cov`, минимум 85%, badge в README |
| Pre-commit hooks | P1 | v0.15.0 | 80 × 1.0 × 70% / S=1, CP Med = **56.0** | `ruff`, `mypy`, whitespace |
| Универсальный скрипт сборки | P2 | v0.15.0+ | 60 × 1.0 × 70% / M=2, CP Med = **21.0** | Единый `build-skill.py` |
| Planning docs guardrails | P2 | v0.15.0+ | 80 × 0.5 × 80% / XS=0.5, CP Low = **64.0** | Проверка, что roadmap не превращается в changelog |
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
