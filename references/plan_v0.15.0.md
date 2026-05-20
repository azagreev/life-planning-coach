# План v0.15.0 — Testing & Integration Hardening

> **Статус:** Draft for approval  
> **Дата:** 2026-05-21  
> **База:** `ROADMAP.md` v0.15.0, `BACKLOG.md` Tech Debt, текущий tag `v0.14.0`  
> **Цель релиза:** закрыть техдолг тестирования и release-quality инфраструктуры перед продуктовыми интеграциями.

---

## 1. Контекст

`v0.15.0` не должен добавлять новые coaching protocols или health/data features. Это hardening-релиз: он повышает доверие к календарному контуру, `SKILL.master.md`, platform build pipeline и будущему MCP-направлению.

Текущий baseline:

- Pre-check на 2026-05-21 проходит: `377 passed, 5 skipped, 15 subtests passed`.
- `ROADMAP.md` уже нормализован как future-only.
- `BACKLOG.md` использует RICE через Estimated AI Sessions (EAS) + Context Pressure.
- `.planning/` в репозитории отсутствует, поэтому план ведётся как обычный `references/plan_v0.15.0.md`.

---

## 2. Варианты scope

### Вариант A — Минимальный релиз качества

**Scope:** только P0 из roadmap.

- Функциональные тесты календаря.
- Тесты целостности `SKILL.master.md`.

**Плюсы:** самый короткий путь к релизу, низкий риск расползания.  
**Минусы:** coverage/pre-commit/MCP остаются в долге, следующий релиз снова начнётся с инфраструктурных задач.  
**Оценка:** 1-2 EAS, Context Pressure Medium.

### Вариант B — Рекомендуемый hardening-релиз

**Scope:** P0 + P1, без P2.

- Функциональные тесты календаря.
- Тесты целостности `SKILL.master.md`.
- Coverage report + badge.
- Pre-commit hooks.
- PoC MCP Gate 0-2 с записью результатов в `references/research/mcp_poc_log.md`.

**Плюсы:** закрывает release-quality базу и даёт факты для решения по интеграциям.  
**Минусы:** MCP PoC может зависеть от внешней доступности OAuth/connector и потребовать ручной проверки.  
**Оценка:** 3-4 EAS, Context Pressure High.

### Вариант C — Полный v0.15.0+

**Scope:** P0 + P1 + P2.

- Всё из варианта B.
- Универсальный build script.
- Planning docs guardrails.

**Плюсы:** максимально чистая инфраструктура после релиза.  
**Минусы:** повышенный риск расползания, build-script refactor может затронуть release path.  
**Оценка:** 5-6 EAS, Context Pressure High/Crit.

### Решение

Рекомендуется **Вариант B**. P2 оставить stretch scope и выполнять только если P0/P1 закрыты без отклонений.

---

## 3. Acceptance Criteria

### AC-1: Calendar constants validation

- `COLOR_MAP`, `REMINDER_PRESETS`, `RRULE_PRESETS` из `references/calendar_constants.md` и `references/calendar_integration.md` парсятся как валидные JSON-like блоки или проверяются через структурированный extractor.
- Все `colorId` находятся в диапазоне Google Calendar `1..11`.
- Все reminder methods принадлежат допустимому набору `popup|email`.
- Все reminder minutes являются неотрицательными integer.
- Все RRULE presets начинаются с `RRULE:` и содержат `FREQ=`.

### AC-2: Free Slot Algorithm tests

- Есть unit/system tests для merge overlapping busy intervals.
- Есть tests для gap detection внутри рабочего окна.
- Есть tests для коротких gaps, которые меньше requested duration.
- Есть tests для top-3 слотов и сортировки по времени.
- Edge cases: пустой день, полностью занятый день, back-to-back events, overlapping events.

### AC-3: Calendar event patterns

- Weekly Review и WOOP examples имеют корректные поля `summary`, `description`, `start`, `end`, `colorId`, `reminders`, `recurrence`.
- Тон календарных описаний остаётся поддерживающим: существующие запреты из `tests/system/test_calendar_tone.py` не ослабляются.
- Failure modes для OAuth decline, 403, 429 и recurrence fallback покрыты проверками текста.

### AC-4: `SKILL.master.md` integrity

- `SKILL.master.md` имеет валидный YAML frontmatter.
- Master file сохраняет platform-agnostic contract: без запрещённых platform-specific терминов в body.
- Все ссылки на `references/*.md` из master существуют.
- `scripts/build-platform-skill.py all` создаёт platform files без cross-contamination.
- Root `SKILL.md` остаётся совместимым с текущими Anthropic structure tests.

### AC-5: Coverage report + badge

- Добавлен `pytest-cov` workflow без дублирующего источника metadata.
- Минимальный порог coverage: 85%.
- README содержит актуальный coverage badge или локально поддерживаемую строку статуса coverage.
- Full test suite проходит с coverage gate.

### AC-6: Pre-commit hooks

- Добавлен конфиг pre-commit для `ruff`, `mypy` и trailing whitespace.
- Hooks можно запустить локально одной командой.
- Конфиг не требует непредсказуемых внешних сервисов во время обычного запуска.
- Existing suite остаётся зелёной.

### AC-7: MCP PoC Gate 0-2

- `references/research/mcp_poc_log.md` обновлён фактами по Gate 0-2.
- Gate 0 фиксирует доступность MCP по целевым платформам: claude.ai web, Claude Desktop, Claude Code CLI, free plan.
- Gate 1 фиксирует OAuth + CRUD: connect, OAuth, create/get/list/update/delete.
- Gate 2 фиксирует recurring events, pagination, `suggest_time`, `respond_to_event`, multi-calendar, read-only fallback.
- Если внешний connector недоступен, это фиксируется как blocked evidence, а не заменяется предположением.

---

## 4. План работ

### Task 0 — Baseline gate

1. Проверить чистое дерево: `git status --short`.
2. Запустить `python3 -m pytest tests/ -q`.
3. Проверить текущий tag: `git describe --tags --abbrev=0`.
4. Зафиксировать baseline в summary будущего work log.

**Done when:** suite зелёная, tag `v0.14.0`, грязные изменения отсутствуют или объяснены.

### Task 1 — Calendar functional tests

1. Добавить тестовый helper для извлечения JSON-блоков из calendar reference files.
2. Покрыть `COLOR_MAP`, `REMINDER_PRESETS`, `RRULE_PRESETS`.
3. Добавить чистые функции или test-local helpers для Free Slot Algorithm, если production runtime отсутствует.
4. Проверить event patterns и failure modes.

**Файлы-кандидаты:** `tests/system/test_calendar_integration.py`, `references/calendar_constants.md`, `references/calendar_integration.md`.

**Commit:** `test: add calendar integration hardening tests`

### Task 2 — `SKILL.master.md` integrity tests

1. Расширить `tests/system/test_multi_platform.py` или добавить отдельный `tests/system/test_master_skill_integrity.py`.
2. Проверить frontmatter, mandatory sections, reference links, platform neutrality.
3. Проверить build sync: root/platform generated files не расходятся после `build-platform-skill.py all`.

**Файлы-кандидаты:** `tests/system/test_master_skill_integrity.py`, `tests/system/test_multi_platform.py`, `scripts/build-platform-skill.py`.

**Commit:** `test: add master skill integrity checks`

### Task 3 — Coverage gate

1. Добавить минимальную зависимость/config для `pytest-cov`.
2. Настроить команду coverage без введения `pyproject.toml`, потому что текущие tests явно запрещают duplicate metadata.
3. Добавить README badge/status.
4. Проверить, что `python3 -m pytest tests/ -q` и coverage-команда проходят.

**Файлы-кандидаты:** `requirements-dev.txt` или существующий dependency mechanism, `README.md`, CI workflow.

**Commit:** `test: add coverage gate`

### Task 4 — Pre-commit hooks

1. Добавить `.pre-commit-config.yaml`.
2. Настроить `ruff`, `mypy`, trailing-whitespace/end-of-file checks.
3. Если `mypy` на текущем коде шумит из-за отсутствия typed package config, ограничить scope до scripts/tests с явным documented rationale.
4. Запустить hooks локально, если dependencies доступны.

**Файлы-кандидаты:** `.pre-commit-config.yaml`, optional `mypy.ini` или `setup.cfg`.

**Commit:** `chore: add pre-commit quality hooks`

### Task 5 — MCP PoC Gate 0-2

1. Проверить фактическую доступность MCP по платформам без записи секретов.
2. Провести или явно заблокировать OAuth/CRUD checks.
3. Провести или явно заблокировать advanced checks: recurrence, pagination, `suggest_time`, RSVP, multi-calendar, read-only.
4. Обновить `references/research/mcp_poc_log.md` только фактами: дата, среда, результат, ошибка/блокер.

**Файлы-кандидаты:** `references/research/mcp_poc_log.md`, возможно `references/calendar_integration.md` если PoC выявит documented limitation.

**Commit:** `docs: record mcp poc gate results`

### Task 6 — Stretch: planning guardrails

Выполнять только после P0/P1.

1. Проверить, достаточно ли текущего `tests/system/test_roadmap_integrity.py`.
2. Если нет, добавить проверки future-only contract для `ROADMAP.md`.

**Commit:** `test: strengthen roadmap guardrails`

### Task 7 — Release readiness

1. Full suite: `python3 -m pytest tests/ -q`.
2. Build: `bash scripts/build-skill.sh`.
3. Проверить `git status --short`.
4. Подготовить changelog entry для `v0.15.0`.
5. Релиз выполнять только отдельной командой: `bash scripts/release.sh 0.15.0`.

**Commit:** `docs: prepare v0.15.0 release notes`

---

## 5. Риски и mitigations

| Риск | Вероятность | Влияние | Mitigation |
|------|-------------|---------|------------|
| MCP PoC заблокирован внешним OAuth/connector | Medium | High | Фиксировать blocked evidence, не блокировать P0 tests |
| Coverage добавит нестабильность из-за отсутствия dependency lock | Medium | Medium | Минимальный config, не вводить `pyproject.toml`, проверять локально |
| `mypy` даст много legacy warnings | High | Medium | Ограничить scope и явно расширять позже |
| Build script refactor затронет release path | Medium | High | Оставить universal build script в stretch scope |
| Tests будут проверять markdown через хрупкие regex | Medium | Medium | Использовать структурированные extractors, минимизировать snapshot-like checks |

---

## 6. Definition of Done

- Все P0 и P1 acceptance criteria закрыты или явно помечены blocked с evidence.
- `python3 -m pytest tests/ -q` проходит.
- Coverage gate проходит с минимумом 85%.
- `bash scripts/build-skill.sh` создаёт artifacts для Claude/Grok/Kimi/Kimi CLI.
- `references/research/mcp_poc_log.md` содержит фактический статус Gate 0-2.
- `ROADMAP.md` остаётся future-only.
- `BACKLOG.md` не содержит дублирующих completed specs для v0.15.0.
- `git status --short` чистый.

---

## 7. Вопросы перед execution

1. Утверждаем **Вариант B** как основной scope?
2. Считаем MCP PoC release-blocking, если connector/OAuth недоступен, или достаточно documented blocked evidence?
3. Coverage badge должен быть CI-driven badge или достаточно локального status line в README на первом шаге?
4. `mypy` включаем сразу в strict-ish mode для scripts/tests или мягко через limited scope?

---

## 8. Рекомендуемый порядок approval

1. Сначала утвердить scope: A/B/C.
2. Затем утвердить policy по MCP blocker.
3. После этого переходить к execution wave 1: Task 0-2.
4. После зелёного P0 перейти к P1: Task 3-5.
5. P2 выполнять только при свободном budget и чистой suite.
