## Что нового в v0.16.0 — Testing & Integration Hardening

Закрыли committed roadmap-scope: тесты календаря расширены edge-кейсами, починен Windows-блокер `python3` хардкода, добавлена coverage-инфраструктура, pre-commit hooks и planning-docs guardrails.

### Added

- **`pyproject.toml`** — минимальная конфигурация pytest + coverage + ruff. `setup.py` остаётся источником правды по package version.
- **`.pre-commit-config.yaml`** — hooks: ruff (lint + format), trailing-whitespace, end-of-file-fixer, check-yaml, check-json, check-merge-conflict, check-added-large-files, mixed-line-ending. Pre-push: `pytest tests/unit + light system`.
- **Coverage infrastructure** — `pytest-cov` с `fail_under = 75`. Текущее покрытие: **80.91%** (2675 statements).
- **Coverage badges в `README.md`** — tests, coverage, schema, version.
- **9 новых тестов Free Slot Algorithm** (`test_calendar_integration.py`):
  - События вне рабочего окна игнорируются
  - Частичное пересечение с границами окна корректно клипуется
  - Gap ровно по длительности — возвращается
  - Длинный duration фильтрует короткие gaps
  - Окно короче duration — нет слотов
  - `limit` ограничивает результаты
  - Несортированные busy intervals обрабатываются
- **3 новых planning-docs guardrails** (`test_roadmap_integrity.py`):
  - `test_roadmap_has_only_future_versions`
  - `test_backlog_done_section_is_pointer_only`
  - `test_changelog_has_each_released_version`

### Fixed

- **Windows `python3` хардкод** — заменён на `sys.executable` (Python тесты) и cross-platform детект (`command -v python3 || command -v python || command -v py`) с проверкой `--version` (shell скрипты). Разблокирует 22+ ранее ERROR'ивших тестов на Windows.
- **`scripts/build-platform-skill.py`** — `sys.stdout.reconfigure(encoding='utf-8')`. Чинит `UnicodeEncodeError` на Windows cp1251 при subprocess выводе emoji/check-marks.
- **`test_master_version_is_014`** → `test_master_version_is_at_least_014` (semver-aware).
- **`test_no_pyproject_toml_exists`** → `test_pyproject_toml_has_no_version` (разрешает pyproject.toml без `[project]` table).

### Changed

- **`CONTRIBUTING.md`** — инструкция для pre-commit + актуализированы тестовые команды.
- **`scripts/release.sh`**, **`scripts/build-skill.sh`** — cross-platform Python detection.

### Roadmap progress

✅ P0: Функциональные тесты календаря (22 теста, было 12)
✅ P0: Тесты целостности SKILL.master.md (все passed на Windows)
✅ P1: Coverage report + badge
✅ P1: Pre-commit hooks
✅ P2: Planning docs guardrails

⏳ Deferred:
- P1 PoC MCP — отдельный research spike, candidate в v0.17.x
- P2 Универсальный скрипт сборки — частично (build-skill.sh кросс-платформенный); полная унификация в v1.0 build pipeline rework

### Что дальше

- **v0.17.0** — IA decomposition (Tier 1 Core ≤ 4K + 6 phase modules)
- **v0.18.0** — Gating + state writes в SKILL.master.md
- **v0.19.0** — Реализация 3 PRD (Core Values Discovery flow + Health Track + Goal Concordance)
- **v1.0.0** — Build pipeline rework + platform lazy-loading + polish
