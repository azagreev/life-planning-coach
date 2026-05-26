# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.  
> **Как обновлять:** `scripts/release.sh` управляет релизным статусом автоматически. Ручные релизы запрещены.  
> **Правило:** Этот файл содержит только будущий scope. История выпущенных версий живёт в [CHANGELOG.md](CHANGELOG.md).

---

## Текущий статус

- **Текущая версия:** `v1.0.0` 🎉
- **Источник правды по версии:** `git describe --tags --abbrev=0`
- **История релизов:** [CHANGELOG.md](CHANGELOG.md)
- **Архив старого roadmap:** [docs/archive/ROADMAP_before_cleanup_2026-05-21.md](docs/archive/ROADMAP_before_cleanup_2026-05-21.md)

---

## v1.1.0 (planned) — Methodology Foundation + Deprecation

**Тема:** Поднять buried evidence-based methods + cleanup legacy. Низкий риск, additive.
**Базис:** [PRD v0.15 Methodology Upgrade](docs/research/prd_v0.15_methodology_upgrade.md), обсуждён 2026-05-26.

### Methodology (PRD v0.15 surface & cleanup)

- [ ] **Implementation Intentions promote** (RICE 180) — извлечь в standalone ref или поднять в Phase 5 как primary planning protocol. If-Then format в Calendar prompts и WOOP Plan step.
- [ ] **Tiny Habits primary framing** (RICE 112) — переписать `habit_loop.md`: Tiny Habits (B=MAP) §1, classical Cue-Routine-Reward §2 (diagnostic для existing habits).
- [ ] **Cut SMART references** (RICE 90) — grep + remove vestigial SMART mentions; вместо них — BHAG/OKR/WOOP architecture.
- [ ] **Evidence citations** (RICE 35) — в каждом методе add evidence box с источником + effect size (Gollwitzer d=0.65, Michie COM-B citation, WOOP meta-analyses).

### Deprecation cleanup (existing planned)

- [ ] Удалить `scripts/build-skill.sh` (replaced by `build-skill.py build`)
- [ ] Удалить `scripts/sync-version.sh` (replaced by `build-skill.py version`)
- [ ] Удалить `references/conversation_state_schema.md` (v1 schema, replaced by v2)
- [ ] Coverage target → 70-85% (extend build-skill.py unit tests)

### Drive Wiki follow-ups (from Drive PoC 2026-05-26)

- [ ] Skill module refactor под Path A append-only protocol (RICE 56)
- [ ] Verify Zapier MCP availability на claude.ai web (Path F, RICE 45)
- [ ] File Anthropic GitHub issue evidence (Path E lobbying, RICE 60)

**Estimated effort:** ~5 EAS. Estimated release: ближайший спринт.

---

## v1.2.0 (planned) — New Evidence-Based Methods

**Тема:** Заполнить genuine gaps в evidence-strong methods. Additive — старые paths не ломаем.

- [ ] **COM-B Model diagnostic** (RICE 60) — новый `references/com_b_diagnostic.md`; Phase 0 integration; routing к right intervention (Capability gap → skill building, Opportunity gap → environment design, Motivation gap → WOOP/Compass).
- [ ] **AAR principles integration** (RICE 31.5) — merge "gap analysis" в existing 7-step Weekly Review (steps 8-11: planned vs actual, why gap, what to change).
- [ ] **Premortem trigger** (RICE 42) — Phase 2 для важных OKR; "представь через 3 мес. цель провалена — 5 причин" → mitigation Implementation Intentions.

**Estimated effort:** ~5 EAS.

---

## v1.3.0 (planned) — Architectural Refactor

**Тема:** Address PRD's WoL concern. Требует state schema bump (additive).

- [ ] **Wheel of Life frequency gate** (RICE 35) — add `diagnosis.wheel_of_life.last_assessed_at` поле; Phase 1 gating: skip WoL если assessed < 30 days ago; offer re-assess после 30 days.

**Estimated effort:** ~3 EAS.

---

## v0.17.x Candidate — Data & Health Integrations

**Статус:** Candidate, требует отдельного research decision перед фиксацией версии.

### Возможный scope

- [x] **PoC MCP** — ✅ Completed 2026-05-26. Decision: MCP-first. См. `docs/research/mcp_poc_log.md`.
- [ ] **Google Health MCP интеграция** — выбрать один путь из `docs/research/google_health_mcp_integration_research.md`, определить security boundary и тестовый контур.
- [ ] **Composite Readiness Model** — CRI formula, 4 зоны, адаптация весов под персоны (ADHD 30/70, Elder 25/75).
- [ ] **Timezone edge-case hardening** — сценарии путешествий, DST, смена рабочей зоны, человекочитаемые fallback-сообщения.

### Gate перед переносом в committed roadmap

- Есть RICE score по каждому item.
- Есть acceptance criteria и test plan.
- Есть решение: интеграция идёт как product feature, research spike или откладывается.

---

## Future Lab

| Идея | Триггер | Где вести |
|------|---------|-----------|
| Body Doubling via AI | Retention проблема становится критичной | `BACKLOG.md` |
| Wearable Energy Integration | Wearable MCP servers становятся stable | `BACKLOG.md` |
| Google Tasks MCP | Tasks API становится доступен через MCP | `BACKLOG.md` |
| Групповые сессии | 5+ пользователей запросят парный/групповой формат | `BACKLOG.md` |
| Мультиязычность | 10+ запросов от англоязычных пользователей | `BACKLOG.md` |
| Parts Work (IFS) | User demand для resistance-work, или RCT base улучшится | `BACKLOG.md` (PRD v0.15, RICE 5) |
| Skill structure simplification | Identified specific pain (currently no concrete signal) | `BACKLOG.md` (PRD v0.15, RICE 15, defer) |

---

## Как предложить фичу

1. Проверьте [BACKLOG.md](BACKLOG.md) — возможно, идея уже записана.
2. Создайте GitHub Issue с тегом `enhancement`.
3. Или напишите в Telegram: [@zagreev](https://t.me/zagreev).

---

## Связанные документы

- [BACKLOG.md](BACKLOG.md) — идеи, research debt и техдолг без committed версии.
- [BUGS.md](BUGS.md) — активные баги и известные проблемы.
- [CHANGELOG.md](CHANGELOG.md) — факты о выпущенных версиях.
- [references/plan_roadmap_backlog_cleanup.md](references/plan_roadmap_backlog_cleanup.md) — план нормализации roadmap/backlog.
