# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.  
> **Как обновлять:** `scripts/release.sh` управляет релизным статусом автоматически. Ручные релизы запрещены.  
> **Правило:** Этот файл содержит только будущий scope. История выпущенных версий живёт в [CHANGELOG.md](CHANGELOG.md).

---

## Текущий статус

- **Текущая версия:** `v0.14.0`
- **Источник правды по версии:** `git describe --tags --abbrev=0`
- **История релизов:** [CHANGELOG.md](CHANGELOG.md)
- **Архив старого roadmap:** [docs/archive/ROADMAP_before_cleanup_2026-05-21.md](docs/archive/ROADMAP_before_cleanup_2026-05-21.md)

---

## v0.16.0 — Testing & Integration Hardening (was committed v0.15.0)

**Цель:** Закрыть техдолг тестирования и release-quality инфраструктуры перед новыми продуктовыми интеграциями.

> **Note:** Этот scope был committed как v0.15.0 (см. историю ROADMAP). Перенесён в v0.16.0 после того, как v0.15.0 поглотила Templates Rebuild + State v2 Foundation как foundational шаг к v1.0 архитектурному рефакторингу.

### P0 (блокирует релиз)

- [ ] **Функциональные тесты календаря** — Free Slot Algorithm, event patterns, conflict detection, JSON validation для `COLOR_MAP`, `REMINDER_PRESETS`, `RRULE_PRESETS`.
- [ ] **Тесты целостности `SKILL.master.md`** — структура, cross-reference validation, platform sync.

### P1 (обязательно в релиз)

- [ ] **Coverage report + badge** — `pytest-cov`, минимальный порог 85%, badge в `README.md`.
- [ ] **Pre-commit hooks** — `ruff`, `mypy`, trailing-whitespace check.
- [ ] **PoC MCP** — Gate 0-2: OAuth, CRUD, `suggest_time`; результаты в `docs/research/mcp_poc_log.md`.

### P2 (желательно)

- [ ] **Универсальный скрипт сборки** — заменить platform-specific билды на единый `build-skill.py`.
- [ ] **Planning docs guardrails** — простой тест, который проверяет, что `ROADMAP.md` не содержит подробных секций выпущенных версий.

### Не входит в v0.16.0

- Google Health MCP implementation.
- Composite Readiness Model.
- Новые coaching protocols.
- Релиз вручную вне `scripts/release.sh`.

---

## v0.17.0 Candidate — Data & Health Integrations

**Статус:** Candidate, требует отдельного research decision перед фиксацией версии.

### Возможный scope

- [ ] **Google Health MCP интеграция** — выбрать один путь из `docs/research/google_health_mcp_integration_research.md`, определить security boundary и тестовый контур.
- [ ] **Composite Readiness Model** — CRI formula, 4 зоны, адаптация весов под персоны (ADHD 30/70, Elder 25/75).
- [ ] **Timezone edge-case hardening** — сценарии путешествий, DST, смена рабочей зоны, человекочитаемые fallback-сообщения.
- [ ] **Health & Metabolism Track** — schema v2.1, см. `docs/research/prd_health_metabolism.md`.
- [ ] **Goal Concordance** — schema v2.2, см. `docs/research/prd_goal_concordance.md`.

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
