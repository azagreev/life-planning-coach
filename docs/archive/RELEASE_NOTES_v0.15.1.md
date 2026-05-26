## Что нового в v0.15.1 — Dev-only cleanup

`references/` теперь содержит только runtime-артефакты. Dev-only содержимое перенесено в `docs/`. Уменьшает шум в IDE/grep, упрощает build-скрипт, улучшает git diff.

### Перемещено

| Откуда | Куда | Файлов |
|---|---|---|
| `references/research/` | `docs/research/` | 26 (research notes, PRD, RICE methodology) |
| `references/tasks/` | `docs/tasks/` | 9 (dev/tester/test_report v0.4-v0.6) |
| `references/audit/` | `docs/audit/` | 1 (calendar integration audit) |
| `references/archive/` | `docs/archive/` | 21 (incl. RELEASE_NOTES_v*.md) |
| `references/acceptance_criteria_v0.4/v0.5/v0.6/v0.7.md` | `docs/archive/release/` | 4 |
| `references/release_checklist_v0.4/v0.6.md` | `docs/archive/release/` | 2 |
| `references/plan_v0.15.0.md`, `plan_roadmap_backlog_cleanup.md` | `docs/planning/` | 2 |
| `references/research_communication_style_*`, `research_diagnostic_*`, `research_stage_*.md` (shadow-версии runtime) | `docs/research/shadows/` | 4 |
| `references/competitive_research_2026.md`, `persistence_research_plan.md` | `docs/research/` | 2 |

### Обновлены пути в

- `scripts/release.sh` — release notes path
- `scripts/sync-version.sh` — stale-version exclusions
- `.github/hooks/pre-push-release-guard` + `.git/hooks/pre-push` — release-guard path
- `tests/system/test_roadmap_integrity.py` — error message
- Active md: `BACKLOG.md`, `ROADMAP.md`, `CHANGELOG.md`, `AGENTS.md`, `references/templates/AI_Instructions.md`, `references/templates/Core_Values_Compass.md`, `references/state_v2_schema.md`, `docs/migration_v1_to_v2.md`

### Добавлено

- **`tests/unit/test_references_runtime_only.py`** — инвариант-тест cleanup. Запрещает возврат `research/`, `tasks/`, `audit/`, `archive/` subdirs в `references/`. Ловит legacy filename patterns. Поймает регрессию при будущих PR.

### Эффект

- `references/` теперь 34 markdown файла (было 75+ с поддиректориями).
- Из runtime namespace убрано ~50K токенов dev-only артефактов.
- Build-скрипт не подгружает dev content в platform SKILL.md.

### Breaking changes

Нет breaking changes для пользователей skill'а (runtime поведение не меняется). Только репозиторная структура.

### Что дальше

- **v0.16.0** — Testing & Integration Hardening (тесты календаря, SKILL.master integrity, coverage, pre-commit, MCP PoC).
- **v0.17.0** — IA decomposition (Tier 1-5, SKILL.md ≤ 4K tokens).
- **v0.18.0** — Gating + state writes (SKILL.master.md учится писать в state v2 при Drive+Calendar).
- **v0.19.0** — Реализация Health Track + Goal Concordance (schema 2.1 / 2.2).
- **v1.0.0** — Build pipeline rework + platform lazy-loading.
