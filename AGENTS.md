# Agent Instructions — life-planning-coach

> Этот файл содержит обязательные инструкции для AI-агентов, работающих с проектом `life-planning-coach`. Инструкции из этого файла имеют приоритет над общими best practices.

---

## 1. Проект: Общая информация

- **Название:** `life-planning-coach` — evidence-based coaching skill for Claude
- **Платформа:** Claude.ai (web), ZIP-архив (`life-planning-coach.zip` или `life-planning-coach.skill` — идентичны, оба ZIP)
- **Язык контента:** Русский (primary), адаптируется под пользователя
- **Версия:** v0.7.1 (источник правды — git tag)
- **Репозиторий:** https://github.com/azagreev/life-planning-coach
- **Ветка:** `main` (единственная)

---

## 2. Структура проекта

```
life-planning-coach/
├── SKILL.md                    # Главный файл скилла (292 строки, ≤5000 слов)
├── README.md                   # Документация для пользователей
├── setup.py                    # Python package metadata (version must match git tag)
├── life-planning-dashboard.html # HTML Dashboard
├── CHANGELOG.md                # История изменений
├── ROADMAP.md                  # План развития
├── BACKLOG.md                  # Идеи без привязки к версии
├── references/                 # Тяжёлый контент (>300 строк на тему)
│   ├── diagnostic_methods.md
│   ├── authentic_goal_filter.md
│   ├── communication_style.md
│   ├── calendar_constants.md
│   ├── conversation_state_schema.md
│   ├── acceptance_criteria_v0.7.md  # Текущие AC
│   ├── emotion_regulation.md
│   ├── energy_scheduling.md
│   ├── recovery_protocol.md
│   ├── win_alert.md
│   └── ...
├── tests/                       # Системные и интеграционные тесты
│   └── system/
│       ├── test_version_consistency.py
│       ├── test_github_sync.py
│       ├── test_readme_integrity.py
│       ├── test_skill_structure.py  # AC v0.7 compliance (23 tests)
│       └── test_v071_features.py
└── scripts/
    ├── build-skill.ps1
    ├── build-skill.sh
    ├── release.sh               # Атомарный релиз
    └── sync-version.sh          # Синхронизация версий
```

---

## 3. Критические правила (MUST)

### 3.1 Version Consistency — источник правды: git tag
```bash
git describe --tags --abbrev=0  # → v0.7.1
```
Версия должна совпадать во всех файлах:
- `SKILL.md` YAML frontmatter `version:`
- `setup.py` `version="..."`
- `README.md` badge

**Как обновить:** запускать `bash scripts/release.sh X.Y.Z` (атомарно).

### 3.2 Acceptance Criteria v0.7 — 19 AC

| Приоритет | Кол-во | Что проверяется |
|-----------|--------|-----------------|
| P0 | 11 | Stage 1.5, Authentic Goal Filter, Communication Style, YAML frontmatter, размер ≤500 строк, обязательные разделы, версия |
| P1 | 4 | Deep Why, TTM, MI, Triggering Precision |
| P2 | 4 | Energy Check, Wheel of Life 11 доменов, Progressive Disclosure, ZIP структура |

**Как проверить:** `python3 -m pytest tests/system/ -v` → **61 passed, 3 skipped**.

### 3.3 SKILL.md Structure (Anthropic Compliance)

- YAML frontmatter: `name`, `version`, `description` (с trigger phrases)
- Обязательные разделы: `## Instructions`, `## Examples`, `## Gotchas`, `## Troubleshooting`, `## Privacy & Data Handling`
- Размер: ≤500 строк, ≤5000 слов
- Progressive Disclosure: тяжёлый контент в `references/`
- Нет слов "claude" или "anthropic" в инструкциях (кроме frontmatter, file names)

### 3.4 ZIP Packaging

```bash
# Правильная структура ZIP:
life-planning-coach.zip
└── life-planning-coach/          # ← корневая папка обязательна
    ├── SKILL.md
    ├── README.md
    ├── references/
    └── ...
```

**Неправильно:** `life-planning-coach/SKILL.md` вложен в ещё одну папку.

### 3.5 Контент: 11 сфер Wheel of Life

В SKILL.md и `references/authentic_goal_filter.md` определены 11 доменов:

1. 🏥 Здоровье и физическая форма
2. 💰 Финансы и материальное благополучие
3. 💼 Карьера и работа
4. 👨‍👩‍👧 Семья и близкие
5. 💕 Романтика и партнёрство
6. 👥 Дружба и социальные связи
7. 🌱 Личностный рост и обучение
8. 🧘 Духовность, смысл и ценности *(обязательный)*
9. 🎉 Отдых, хобби и радость
10. 🌍 Вклад в общество и наследие
11. 🏠 Дом и окружение

---

## 4. Git Workflow

### 4.1 Commit style
- Формат: `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`
- Пример: `feat: add retry persistence to calendar events`

### 4.2 Release process
```bash
bash scripts/release.sh X.Y.Z
```
Шаги: preconditions → sync-version → commit → push → verify → tag → GitHub Release.

### 4.3 Post-commit hook
При коммите выводится предупреждение если есть unpushed commits:
```
⚠️  ВНИМАНИЕ: N commit(s) не запушены на GitHub!
```

### 4.4 System tests
ВСЕ тесты должны проходить перед релизом:
```bash
python3 -m pytest tests/system/ -v
# Expected: 61 passed, 3 skipped
```

---

## 5. Style Guidelines

### 5.1 Language
- Основной язык скилла: **русский**
- Trigger phrases в description: конкретные запросы пользователя
- Tone: поддерживающий, нейтральный, без осуждения
- Therapy disclaimer обязателен в Privacy section

### 5.2 Code / Scripts
- Python 3.12+
- Type hints где возможно
- `calendar_integration/` — standalone package с `requirements.txt`

---

## 6. External APIs & Tools

### 6.1 GitHub API (приоритет #1)
При работе с GitHub — использовать REST/GraphQL API. Authenticated requests для избежания rate limits.

### 6.2 MCP / Context7
Перед архитектурными решениями запрашивать Context7 для актуальной документации.
Если недоступен — предупредить и продолжить с внутренними знаниями.

### 6.3 Web-поиск
1. Kimi WebBridge → 2. MCP Firecrawl → 3. Browser fallback

---

## 7. Security & Privacy

- **Никогда** не хардкодить API-ключи в SKILL.md или скриптах
- User data: только с явного согласия, therapy disclaimer обязателен
- Google Drive/Calendar: graceful fallback при недоступности MCP

---

## 8. Known Issues (Tech Debt)

| Issue | Файл | Приоритет |
|-------|------|-----------|
| Calendar Event Copy Review | `references/calendar_constants.md` | P2 (в BACKLOG) |
| SSH key permissions (0777) | `~/.ssh/id_ed25519_github` | ✅ Fixed |

---

## 9. Quick Commands

```bash
# Проверить версию
git describe --tags --abbrev=0

# Запустить все системные тесты
python3 -m pytest tests/system/ -v

# Собрать ZIP правильно
mkdir -p .tmp_build/life-planning-coach
cp -r SKILL.md README.md setup.py CHANGELOG.md ROADMAP.md BACKLOG.md life-planning-dashboard.html references .tmp_build/life-planning-coach/
cd .tmp_build && zip -r ../life-planning-coach-v$(git describe --tags --abbrev=0 | sed 's/^v//').zip life-planning-coach/
cd .. && rm -rf .tmp_build

# Релиз
bash scripts/release.sh X.Y.Z
```

---

*Обновлено: 2026-05-18*  
*Версия: 2.0 (для life-planning-coach v0.7.1+)*
