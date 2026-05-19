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
- **Платформы:** Claude.ai (primary), Grok 4.3 (xAI), Kimi K2.6 (Moonshot AI)
- **Язык:** Русский (primary)
- **Версия:** v0.10.0 (источник правды — git tag)
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

---

## 4. Git Workflow

### 4.1 Commit style
- Формат: `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`

### 4.2 Release process
```bash
bash scripts/release.sh X.Y.Z
```

**ЗАПРЕЩЕНО создавать релизы вручную.** Title = только тег (`v0.10.1`). Описание — в release notes.

**Защита:** Git hook + GitHub Actions (`release-guard.yml`) + этот документ.

### 4.3 System tests
`python3 -m pytest tests/ -q` → **190+ passed**.

---

## 5. Style Guidelines

- Основной язык: **русский**
- Названия фич в BACKLOG.md и ROADMAP.md — на русском (английские термины только в скобках)
- Tone: поддерживающий, нейтральный, без осуждения
- Therapy disclaimer обязателен в Privacy section
- Python 3.12+, type hints где возможно

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
python3 scripts/build-platform-skill.py [claude|grok|kimi|all]

# Релиз
bash scripts/release.sh X.Y.Z
```

---

*Обновлено: 2026-05-18*  
*AGENTS.md v4.0 (lean) для life-planning-coach v0.10.1+*
