# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.  
> **Как обновлять:** `scripts/release.sh` управляет релизным статусом автоматически. Ручные релизы запрещены.  
> **Правило:** Этот файл содержит только будущий scope. История выпущенных версий живёт в [CHANGELOG.md](CHANGELOG.md).

---

## Текущий статус

- **Текущая версия:** `v0.19.0`
- **Источник правды по версии:** `git describe --tags --abbrev=0`
- **История релизов:** [CHANGELOG.md](CHANGELOG.md)
- **Архив старого roadmap:** [docs/archive/ROADMAP_before_cleanup_2026-05-21.md](docs/archive/ROADMAP_before_cleanup_2026-05-21.md)

---

## v1.0.0 — Build Pipeline + Platform Optimization

**Цель:** Polish + major-version signal зрелости проекта.

- [ ] **Build pipeline rework** — единый `build-skill.py`, замена legacy platform-specific сборок.
- [ ] **Platform lazy-loading** — для платформ умеющих dynamic refs (Claude.ai) — не инлайнить P0 в SKILL.md (−7K токенов в каждом платформенном файле).
- [ ] **Platform parity test** — automated, все 4 платформы рендерятся идентично.
- [ ] **Acceptance criteria для v1.0:**
  - cold-load ≤ 4K
  - typical session ≤ 18K
  - тесты ≥ 85% coverage
  - все 4 gating mode комбинации работают

---

## v0.17.x Candidate — Data & Health Integrations

**Статус:** Candidate, требует отдельного research decision перед фиксацией версии.

### Возможный scope

- [ ] **PoC MCP** — Gate 0-2: OAuth, CRUD, `suggest_time`; результаты в `docs/research/mcp_poc_log.md`. Deferred из v0.16.0.
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
