# Roadmap

> **Для кого:** Пользователи скилла, контрибьюторы, планирование разработки.  
> **Как обновлять:** `scripts/release.sh` управляет релизным статусом автоматически. Ручные релизы запрещены.  
> **Правило:** Этот файл содержит только будущий scope. История выпущенных версий живёт в [CHANGELOG.md](CHANGELOG.md).

---

## Текущий статус

- **Текущая версия:** `v1.2.0` 🎉 (releasing 2026-05-27)
- **Источник правды по версии:** `git describe --tags --abbrev=0`
- **История релизов:** [CHANGELOG.md](CHANGELOG.md)
- **Архив старого roadmap:** [docs/archive/ROADMAP_before_cleanup_2026-05-21.md](docs/archive/ROADMAP_before_cleanup_2026-05-21.md)

---

## v1.3.0 (planned) — WoL Refactor + v1.2 Follow-ups

**Тема:** Address PRD's WoL concern + close v1.2 code review gaps. Требует state schema bump (additive).

### Core (existing)

- [ ] **Wheel of Life frequency gate** (RICE 35) — add `diagnosis.wheel_of_life.last_assessed_at` поле; Phase 1 gating: skip WoL если assessed < 30 days ago; offer re-assess после 30 days.

### v1.2 follow-ups (из code review)

- [ ] **AAR sighted_count runtime pattern matching** (RICE 120) — skill-instruction в Step 9: при write нового lesson — search в last 4 weekly_reviews по similar lesson+category, increment counter если match. Без этого Step 9 = simple journal, surface threshold (`sighted_count ≥ 3`) никогда не trigger'ся. ~1 EAS.
- [ ] **COM-B Phase 0 soft upsell** (RICE 126) — секция в `references/emotion_regulation.md` cross-ref к `com_b_diagnostic.md` для пользователей которые застряли на «не могу начать» в Phase 0.5 ER protocol (lean conversation mode не проходит через Phase 1 trigger). ~0.5 EAS.
- [ ] **Trivial cleanup bundle** (RICE 180 в среднем, ~0.75 EAS total) — три trivial items одним PR:
  - State writes inline policy в AGENTS.md §IA decomposition («при per-module budget pressure → state writes ТОЛЬКО в state_v2_schema.md»)
  - Whitelist quoted speech (`«[^»]*»`) в `test_no_forbidden_words` чтобы перестать переформулировать user quotes
  - Explicit error для `git branch -f main origin/main` в `.github/workflows/release-checks.yml` (silent failure → diagnosable)

### Observed risks (revisit после месяца использования v1.2)

- [ ] **Premortem trigger rank-order/AND logic** (RICE 84) — 5 OR conditions могут trigger слишком часто для junior users. Defer до user feedback.
- [ ] **lessons_learned category drift** (RICE 56) — free-text без validation. Defer до first real usage data (что они реально category используют).
- [ ] **`find dist -name -not` fragile pattern** (RICE 70) — explicit regex `dist/life-planning-coach-v[0-9.]+\.zip`. Defer до first break при добавлении нового archive variant.

**Estimated effort:** ~5 EAS (core 3 + follow-ups 2).

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
