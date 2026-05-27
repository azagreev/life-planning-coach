# Agent Instructions — life-planning-coach

> Инструкции для AI-агентов, работающих с проектом. Имеют приоритет над общими best practices.

---

## 0. Рабочий контракт

### 0.1 Entry Points

| Команда пользователя | Workflow | Что делать |
|----------------------|----------|------------|
| "спланируй", "plan" | **Plan Mode** | Варианты + plan file + AC → ExitPlanMode для одобрения |
| "ретро", "retrospective" | **Retro Mode** | Факты → root cause → action items → `RETRO_*.md` |
| "пофикси", "fix", "bug" | **Bug Fix Mode** | Plan mode, даже для hotfix'ов |
| "релиз", "release" | **Release Mode** | Только `bash scripts/release.sh X.Y.Z` |
| "проверь", "audit" | **Research Mode** | Только отчёт. **Никакой реализации.** |
| "системное решение" | **Architecture Mode** | Только планирование. **Никаких точечных фиксов.** |

### 0.2 Три критических правила

1. **Release = `scripts/release.sh` ONLY.** Ручные релизы запрещены.
2. **Проверить ≠ Сделать.** Если просят "проверить" — только отчёт. Реализация — только после явного "давай делать".
3. **Рабочее дерево чистое.** Начало и конец сессии — `git status --short` должен быть пустым.

### 0.3 Session Pre-check

```bash
# 1. Состояние репозитория
git status --short          # Должно быть пусто или объяснено
python3 -m pytest tests/ -q  # Должно быть 190+ passed
# 2. Версия
git describe --tags --abbrev=0
```

Если что-то не так — **остановиться и сообщить пользователю**.

### 0.4 Red Lines

- Никакой реализации без plan mode approval
- Никаких костылей при запросе "системного решения"
- Никакого кода без тестов (новый код → новые тесты)

---

## 1. Проект

- **Название:** `life-planning-coach` — evidence-based coaching skill
- **Платформы:** Claude.ai (primary), Grok (xAI), Kimi OK Computer (Moonshot AI), Kimi Code CLI (terminal)
- **Язык:** Русский (primary)
- **Версия:** v1.2.0 (источник правды — git tag)
- **Репозиторий:** https://github.com/azagreev/life-planning-coach
- **Ветка:** `main`

---

## 2. Структура

`SKILL.md` (Claude skill, backward compat), `SKILL.master.md` (platform-agnostic source), `platforms/`, `README.md`, `setup.py`, `life-planning-dashboard.html`, `CHANGELOG.md`, `ROADMAP.md` (только будущее), `BACKLOG.md`, `references/` (incl. `references/platforms/`), `tests/`, `scripts/build-skill.sh`, `scripts/build-platform-skill.py`, `.github/workflows/`.

---

## 3. Критические правила

### 3.1 Version Consistency

Источник правды: `git describe --tags --abbrev=0`

Версия совпадает в: `SKILL.md`, `setup.py`, `README.md`, `AGENTS.md §1`.

Обновление: `bash scripts/sync-version.sh X.Y.Z`.

### 3.2 Acceptance Criteria

P0 (11): Stage 1.5, Authentic Goal Filter, Communication Style, YAML frontmatter, размер ≤500 строк, обязательные разделы, версия.  
P1 (4): Deep Why, TTM, MI, Triggering Precision.  
P2 (4): Energy Check, Wheel of Life 11 доменов, Progressive Disclosure, ZIP структура.

**Проверка:** `python3 -m pytest tests/ -q` → **190+ passed**.

### 3.3 SKILL.md Structure (Anthropic Compliance)

- YAML frontmatter: `name`, `version`, `description`
- Обязательные разделы: `## Instructions`, `## Examples`, `## Gotchas`, `## Troubleshooting`, `## Privacy & Data Handling`
- Размер: ≤500 строк, ≤5000 слов
- Progressive Disclosure: тяжёлый контент в `references/`
- Нет слов "claude" или "anthropic" в инструкциях

### 3.4 ZIP Packaging

Корневая папка `life-planning-coach/` внутри ZIP обязательна. См. `scripts/build-skill.sh`.

### 3.5 Контент: 11 сфер Wheel of Life

См. `SKILL.md` и `references/authentic_goal_filter.md`. Обязательная сфера: Духовность, смысл и ценности.

### 3.6 State Writes Policy (per-module budget pressure)

**Правило:** При создании или редактировании phase-модуля (`references/module_phase*.md`) под per-module token budget pressure (≥ 2400/2500 tokens) — state write rules **ТОЛЬКО** в `references/state_v2_schema.md` (соответствующий §3.x), а в модуле inline-секция «State writes» удаляется или сводится к одной cross-ref ссылке:
```markdown
**State writes:** см. `state_v2_schema.md` §3.X.Y.
```

**Rationale:**
- `state_v2_schema.md` — single source of truth для schema полей. Дублирование в модулях ведёт к drift при schema bumps.
- Per-module budget жёсткий (2500 tokens) — inline state writes тратят 100-300 tokens, которые лучше потратить на routing instructions.
- Precedent: v1.2.0 «State writes inline убраны из Phase 2 + Phase 3 modules под per-module budget pressure» (см. CHANGELOG.md `## [1.2.0]` Architecture decisions).

**Когда inline OK:**
- Модуль ≤ 2200 tokens (есть headroom)
- Краткое (≤ 30 tokens) summary с обязательной cross-ref ссылкой на `state_v2_schema.md` для full schema

### 3.7 Test Authoring: Forbidden Words

При написании новых tests, проверяющих forbidden directive words (`надо` / `должен` / `обязан` / etc.) в content модулей — использовать helper:

```python
from tests.helpers.forbidden_words import assert_no_forbidden

assert_no_forbidden(
    content,
    ["надо", "должен", "обязан"],
    context="references/example.md",
)
```

Helper автоматически whitelists Russian quoted speech `«...»` — позволяет включать directive слова в quoted user examples / anti-patterns без false-positive. Введён в v1.3.0 (PR-D).

**Migration старых tests** (custom whitelist logic в `test_v060_content.py`, `test_v071_features.py`, etc.) — by-need, не массовый refactor.

---

## 4. Git Workflow

### 4.1 Commit style
- Формат: `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`

### 4.2 Release process
```bash
python scripts/build-skill.py release X.Y.Z   # v1.0+ unified CLI
# OR (deprecated, will be removed in v1.1):
# bash scripts/release.sh X.Y.Z
```

**ЗАПРЕЩЕНО создавать релизы вручную.** Title = только тег (`v1.2.0`). Описание генерируется автоматически из CHANGELOG.md.

**Sub-commands `build-skill.py`** (v1.0+):
- `build` — все 4 платформы + ZIP/skill/grok-md/kimi-md/kimi-cli-zip
- `version X.Y.Z` — sync version во все source files (replaces sync-version.sh)
- `verify` — pre-release checks (tests, working tree, version, ZIP freshness)
- `release X.Y.Z` — full flow (verify + version + build + commit + tag + push + gh release)

**Защита:** Git hook + GitHub Actions (`release-guard.yml`) + этот документ.

**Примечание:** `docs/archive/RELEASE_NOTES_*.md` — generated artifacts, создаются автоматически из CHANGELOG.md. Не редактировать вручную.

### 4.3 System tests
`python -m pytest tests/ -q` → **540+ passed**.

### 4.4 Prioritization (RICE)

Все фичи, баги и research-задачи приоритизируются через **RICE**:

```
RICE = (Reach × Impact × Confidence) / Effort

Reach:      % целевой аудитории (0-100) [GUESS]
Impact:     0.25 minimal → 3.0 massive
Confidence: 0-100% на основе evidence
Effort:     AI Sessions (XS/S/M/L/XL/XXL) + Context Pressure
```

**Effort v1.1 (AI Sessions):** Разработчик — AI-агент. Person-days — фикция.
Единица измерения: Estimated AI Sessions (EAS) + Context Pressure (Low/Med/High/Crit).
Шкала: XS=0.5, S=1, M=2, L=3, XL=5, XXL=8.
Подробнее: `docs/research/rice_methodology.md` §4.

**Интерпретация:**

| RICE | Категория | Действие |
|------|----------|----------|
| > 30 | Quick Win | Немедленно |
| 10-30 | High Priority | Следующий спринт |
| 3-10 | Medium Priority | Backlog |
| < 3 | Moonshot | Исследовать позже |

**Баги — Severity mapping:**

| Severity | Impact | SLA |
|----------|--------|-----|
| Critical (crashes, data loss) | 3.0 | Fix same day |
| High (feature broken) | 2.0 | Fix 48h |
| Medium (workaround exists) | 1.0 | Fix 1 week |
| Low (cosmetic) | 0.25 | Best effort |

**Commit:** При добавлении задачи в BACKLOG.md указывать RICE score.

---

## 5. Style Guidelines

- Основной язык: **русский**
- Названия фич в BACKLOG.md и ROADMAP.md — на русском (английские термины только в скобках)
- Tone: поддерживающий, нейтральный, без осуждения
- Therapy disclaimer обязателен в Privacy section
- Python 3.12+, type hints где возможно

### 5.1 Language Policy

| Контекст | Язык | Примечание |
|----------|------|------------|
| README.md, USER_GUIDE, CHANGELOG, ROADMAP, BACKLOG | Русский | User-facing документы |
| SKILL.md frontmatter (`name`, `version`, `description`) | Английский | Требование платформ (Claude, Grok) |
| SKILL.md instructions + `references/` | Русский | Основной контент скилла |
| Технические термины | Английский или скобки | MCP, OAuth, ZIP, JSON, CLI — не переводить |
| Platform SKILL.md (`platforms/*/`) | Инструкции — русский, frontmatter — английский | Собираются автоматически из `SKILL.master.md` |
| Code comments, commit messages | Английский | Git convention |

**Anti-patterns:**
- Code-switching внутри предложения: "Нажми кнопку Submit" → "Нажми кнопку «Отправить»"
- Английские термины без пояснения при первом упоминании в user-facing тексте
- Смешение языков в одном markdown-списке

---

## 6. Quick Commands

```bash
# Проверить версию
git describe --tags --abbrev=0

# Запустить тесты
python3 -m pytest tests/ -q

# Собрать все платформы
bash scripts/build-skill.sh

# Только сгенерировать platform-файлы
python3 scripts/build-platform-skill.py [claude|grok|kimi|kimi-cli|all]

# Релиз
bash scripts/release.sh X.Y.Z
```

---

*Обновлено: 2026-05-20*  
*AGENTS.md v4.3 для life-planning-coach v1.2.0+*
