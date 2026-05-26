## Что нового в v0.15.0 — Templates Rebuild + State v2 Foundation

Подготовительный блок к v1.0 архитектурному рефакторингу. Устраняет structural drift между state schema, HTML dashboard, wiki templates и dashboard_guide. Единый source of truth через state v2.

### Добавлено
- **`references/state_v2_schema.md`** — canonical schema v2.0: 11 spheres (canonical naming), Phase 0-5, блок Core Values (derived_from / compass_question / priority_rank), `persona`, `emotion_regulation_log`, `wins_log`, `reward_audit_results`, `calendar_events_log`, `recovery_sessions_log`, gating + backfill протоколы. Foundation для HTML dashboard, wiki templates и dashboard_guide.
- **`references/templates/Core_Values_Compass.md`** — новый wiki-шаблон Core Values Discovery (5-7 values + compass questions + cross-link с Goals). Из PRD `prd_core_values_discovery.md`.
- **HTML dashboard v1.0.0** — Core Values panel (Overview tab) + скрытые placeholders для Health Track / Goal Concordance (активируются при schema bump 2.1 / 2.2).
- **`docs/migration_v1_to_v2.md`** — миграция legacy 8-sphere wiki → canonical 11 spheres + rollback инструкция.
- **`docs/research/dashboard_architecture_v1.md`** — вынесенный 2538-строчный архитектурный doc (dev-only, не в runtime).
- **`docs/research/plan_v1.0_templates_rebuild.md`** — план rebuild всех 3 шаблонов, RICE 30.0.
- **`docs/research/prd_core_values_discovery.md`, `prd_health_metabolism.md`, `prd_goal_concordance.md`** — три новых PRD (Health/Concordance → schema bumps 2.1 / 2.2 в будущем).
- **`tests/unit/test_templates_v2.py`** — 21 тест: canonical spheres consistency, state v2 schema completeness, HTML data-driven, wiki schema_version, token budgets, dashboard_guide thin, schema versioning.

### Изменено
- **`life-planning-dashboard.html`** — удалены hardcoded `WHEEL_SPHERES` / `EXECUTION_SCORES` / `VELOCITY_DATA` / `STREAK_DATA`; теперь читают `window.lpData`. Sphere IDs приведены к canonical: `growth → personal_growth`, `spirituality → meaning`, `fun → fun_recreation`, `environment → physical_environment`. CSS comment v0.9.1 → v1.0.0. Schema 2.x compatibility check.
- **`references/dashboard_guide.md`** — сжат с 2538 до ~130 строк: runtime-only specification + JSON contract. Heavy архитектура вынесена в `docs/research/dashboard_architecture_v1.md` (−7K токенов из runtime при Phase 4).
- **8 wiki templates** — все frontmatter `schema_version: "2.0"`. `Wheel_of_Life_History.md` — 11 canonical spheres (было 8 с legacy именами). `Goals.md` — AGF radar блок на каждую цель + `core_values_alignment` + закомментированный Concordance placeholder + полный Habit Loop (cue / routine / reward / anchor). `Hot_Cache.md` + `Raw_Session.md` + `USER_PROGRESS_JOURNAL.md` — поля под persona, emotion_regulation, wins, calendar_events. `Index.md` — убраны broken refs на `Concepts/Frameworks/Sources` (не существовали). `Progress_Dashboard.md` — repurposed как text-mode dashboard для Paper Coach Mode.
- **`references/conversation_state_schema.md`** — помечен DEPRECATED, указатель на v2.
- **`SKILL.master.md` + `SKILL.md`** — версия 0.14.0 → 0.15.0; платформы пересобраны.
- **`ROADMAP.md`** — Testing & Integration Hardening сдвинут v0.15.0 → v0.16.0. Health/Concordance PRD добавлены в v0.17.0 Candidate.
- **`BACKLOG.md` + `docs/research/rice_evaluation_backlog.md`** — добавлены 4 entries: Core Values Discovery (#18, RICE 32.7), Health & Metabolism (#19, RICE 11.7), Goal Concordance (#20, RICE 7.5), Templates Rebuild v1.0 (#21, RICE 30.0).

### Исправлено
- **`tests/system/test_v090_features.py`** — добавлен `encoding='utf-8'` в `tempfile.NamedTemporaryFile`. Чинит pre-existing Windows `UnicodeEncodeError` (cp1251) при emoji в JS dashboard.

### Миграция

Legacy wiki пользователи (8 spheres / `schema_version < 2.0`): при первом запуске skill предложит migration prompt. Backup в `05_Archive/v1_backup_*`. Полная инструкция: [docs/migration_v1_to_v2.md](../../docs/migration_v1_to_v2.md).

### Breaking changes

- HTML dashboard перешёл с hardcoded data на `window.lpData` injection. Существующие сохранённые HTML файлы продолжают работать (CSS совместим), но новый рендер требует state v2 JSON.
- Legacy sphere IDs (`growth`, `spirituality`, `fun`, `environment`) → canonical (`personal_growth`, `meaning`, `fun_recreation`, `physical_environment`). Тесты блокируют использование legacy имён.
- `references/conversation_state_schema.md` помечен DEPRECATED; новые имплементации используют `references/state_v2_schema.md`.

### Что дальше

- **v0.16.0** — Testing & Integration Hardening (сдвинуто с v0.15.0).
- **v0.17.0 Candidate** — Health Track (PRD → schema 2.1), Goal Concordance (PRD → schema 2.2), Google Health MCP, Composite Readiness.
- **v1.0** — full architectural refactor (Tier 1-5 IA, lazy-loading модули, новый build pipeline).
