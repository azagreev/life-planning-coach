# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.  
> **Как обновлять:** `scripts/release.sh` управляет релизным статусом автоматически. Ручные релизы запрещены.  
> **Правило:** Этот файл содержит только будущий scope. История выпущенных версий живёт в [CHANGELOG.md](CHANGELOG.md).

---

## Текущий статус

- **Текущая версия:** `v1.4.4` 🎉 (released 2026-06-07)
- **Источник правды по версии:** `git describe --tags --abbrev=0`
- **История релизов:** [CHANGELOG.md](CHANGELOG.md)
- **Архив старого roadmap:** [docs/archive/ROADMAP_before_cleanup_2026-05-21.md](docs/archive/ROADMAP_before_cleanup_2026-05-21.md)

---

## v1.5.0 (TBD) — Awaiting v1.2/v1.3 Usage Feedback

**Тема:** Revisit deferred items от v1.2/v1.3 code reviews после ~30 дней production usage. Decide scope based на user signal — currently no committed scope. Pushed back from v1.4 в swap 2026-05-28 (v1.4 теперь занят Health Assessment Methodology — concrete PRD ready).

### Candidates (revisit after 30d usage signal, ≥ 2026-06-27)

- [ ] **Premortem trigger rank-order / AND logic** (RICE 84, defer'd от v1.3) — 5 OR conditions могут trigger слишком часто для junior users. Revisit если получим 2+ feedback reports что «Premortem fires слишком часто».
- [ ] **lessons_learned category drift** (RICE 56, defer'd от v1.3) — free-text без validation. Будет surface через AAR sighted_count runtime (v1.3.0+) если drift станет проблемой. Revisit если sighted_count produces irrelevant matches.
- [ ] **`find dist -name -not` fragile pattern** (RICE 70, defer'd от v1.3) — explicit regex `dist/life-planning-coach-v[0-9.]+\.zip`. Revisit при first CI break добавлением нового archive variant.

### Gate перед commit к v1.5.0 scope

- Есть concrete signal что Premortem fires «слишком часто» для junior users (хотя бы 2 user reports)?
- Есть signal что `lessons_learned.sighted_count` matching produces irrelevant matches (semantic drift)?
- Какой-то новый item из user feedback заслуживает committed slot?

**Estimated effort:** TBD после signal review.

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
- [docs/planning/plan_roadmap_backlog_cleanup.md](docs/planning/plan_roadmap_backlog_cleanup.md) — план нормализации roadmap/backlog.
