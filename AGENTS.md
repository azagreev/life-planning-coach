# Agent Instructions — life-planning-coach

> Этот файл содержит обязательные инструкции для AI-агентов, работающих с проектом `life-planning-coach`. Инструкции из этого файла имеют приоритет над общими best practices.

---

## 0. Рабочий контракт (User ↔ AI)

Этот раздел описывает, как мы работаем вместе. Любое нарушение = баг в процессе.

### 0.1 Entry Points (Explicit Commands)

Пользователь использует **ключевые слова** → агент запускает соответствующий workflow:

| Команда пользователя | Workflow агента | Что делать |
|----------------------|-----------------|------------|
| "спланируй", "plan", "давай спланируем" | **Plan Mode** | Context7 + варианты + plan file + AC → ExitPlanMode для одобрения |
| "ретро", "разберём что было", "retrospective" | **Retro Mode** | Собрать факты → root cause → action items → файл `RETRO_*.md` |
| "пофикси", "fix", "bug" | **Bug Fix Mode** | Plan mode ОБЯЗАТЕЛЕН даже для hotfix'ов |
| "релиз", "release" | **Release Mode** | Только `bash scripts/release.sh X.Y.Z` |
| "проверь", "audit", "проанализируй" | **Research Mode** | Только исследование + отчёт. **Никакой реализации.** |
| "системное решение", "как запретить" | **Architecture Mode** | Только планирование системы. **Никаких точечных фиксов.** |

**Правило:** Если ключевое слово не распознано — уточнить у пользователя, какой workflow запускать.

### 0.2 Lifecycle Gate Checklist

```
L0 Request → L1 Extract → L2 Plan → L3 AC → Implement → Verify → Ship
   ↑            ↑           ↑         ↑        ↑          ↑       ↑
  User       Agent       Agent     User    User       Agent   Agent
```

**Нельзя перепрыгивать уровни.** Каждый gate требует проверки:

| Gate | Что проверяем | Кто валидирует |
|------|---------------|----------------|
| **L0 → L1** (Extract) | Intent ясен? Assumptions перечислены? | Агент (self-check) |
| **L1 → L2** (Plan) | Context7 запрошен? Варианты сравнены? Plan file написан? | Агент (self-check) |
| **L2 → L3** (AC) | AC написаны? Пользователь одобрил через ExitPlanMode? | **Пользователь** |
| **L3 → Implement** | AC одобрены? Git clean? Все тесты проходят? | Агент (pre-check) |
| **Implement → Verify** | Все тесты проходят? AC проверены? | Агент (pytest) |
| **Verify → Ship** | ROADMAP 'Текущий статус' не содержит released версий? CHANGELOG обновлён? Version synced? | Агент (checklist) |

### 0.3 Session-start Pre-check

При начале каждой сессии агент ОБЯЗАН выполнить:

```bash
# 1. Прочитать AGENTS.md §0 (этот контракт)
# 2. Проверить состояние репозитория
git status --short          # Должно быть пусто или объяснено
python3 -m pytest tests/ -q  # Должно быть 130+ passed
# 3. Проверить версию
git describe --tags --abbrev=0
```

Если что-то не так — **остановиться и сообщить пользователю** до начала любой работы.

### 0.3a Session-end Checklist

Перед окончанием сессии агент ОБЯЗАН выполнить:

```bash
# 1. Все изменения закоммичены
git status --short          # Должно быть пусто
# 2. Все тесты проходят
python3 -m pytest tests/ -q
# 3. Нет незакоммиченных файлов — включая новые тесты и планы
```

Если `git status --short` не пустое — **закоммитить или объяснить** до окончания сессии.

### 0.4 Research-обязательства (Context7 + Best Practices)

Перед архитектурой, написанием тестов или критериев приёмки:

1. **Запросить Context7** (MDN, актуальная документация)
2. **Сравнить варианты** — найти оптимальное, "красивое", лёгкое, удобное
3. **Быть проактивным в поиске** — но **ТОЛЬКО в поиске**, не в реализации

### 0.5 Assumptions Surfacing

Перед началом plan mode агент ОБЯЗАН явно перечислить свои допущения:

```
ASSUMPTIONS I'M MAKING:
1. ...
2. ...
→ Correct me now or I'll proceed with these.
```

### 0.6 Anti-Rationalization

Следующие мысли агента — ошибочны и должны игнорироваться:

| Рационализация | Реальность |
|----------------|------------|
| "Это слишком мелко для плана" | Нет задач "слишком мелких" для процесса |
| "Я просто быстро поправлю" | Быстрые правки = технический долг |
| "Сначала соберу контекст" | Сбор контекста = работа, требует одобрения |
| "Пользователь явно не сказал 'план'" | Если сказал "системное решение" — нужен план |
| "Проверить = можно сразу сделать" | Проверить = отчёт. Делать = только после одобрения. |
| "Тесты можно добавить потом" | "Потом" = никогда. Тесты = часть задачи. |
| "Это hotfix, некогда на план" | Hotfix без плана = ещё один hotfix завтра. |
| "Я уже знаю лучшее решение" | Знание ≠ обоснование. Нужен Context7 + сравнение. |

### 0.7 Diagnostic Export (при ошибках)

Если что-то пошло не так (тесты падают, релиз сломан, git conflict) — агент ОБЯЗАН собрать diagnostic context:

```bash
git status --short
git log --oneline -5
git describe --tags --abbrev=0
python3 -m pytest tests/ -v --tb=short
```

И предоставить пользователю перед тем, как просить помощь.

### 0.8 Progressive Refinement (L0→L1→L2→L3)

Каждый user request проходит 4 уровня уточнения:

| Уровень | Что происходит | Пример |
|---------|----------------|--------|
| **L0 Raw** | Пользователь говорит | "Сделай красиво" |
| **L1 Extract** | Агент извлекает intent | "Редизайн дашборда" |
| **L2 Plan** | Агент структурирует | "Apple-style: rings, glass, dark mode" |
| **L3 AC** | Агент формализует критерии | "12 тестов, offline, responsive, Android Chrome fixes" |

**Правило:** Нельзя перепрыгивать с L0 на L3. Каждый уровень — gate.

### 0.9 Запрещённые действия (красные линии)

| # | Запрет | Почему | Пример нарушения |
|---|--------|--------|------------------|
| 1 | **Никакой реализации без plan mode approval** | Предотвращает самодеятельность | Android-фиксы добавлены без плана |
| 2 | **Никаких костылей/точечных фиксов когда запрошено "системное решение"** | Симптом ≠ причина | API call для исправления title'ов вместо guard-системы |
| 3 | **Никакой реализации без written AC** | Критерии приёмки = контракт качества | — |
| 4 | **Никакого кода без Context7 research** | Решение должно быть обосновано документацией | Android-фиксы без MDN research |
| 5 | **Никаких ручных релизов** | Только `scripts/release.sh` | v0.9.0, v0.9.1 созданы вручную |

---

## 1. Проект: Общая информация

- **Название:** `life-planning-coach` — evidence-based coaching skill for Claude
- **Платформа:** Claude.ai (web), ZIP-архив (`life-planning-coach.zip` или `life-planning-coach.skill` — идентичны, оба ZIP)
- **Язык контента:** Русский (primary), адаптируется под пользователя
- **Версия:** v0.9.2 (источник правды — git tag)
- **Репозиторий:** https://github.com/azagreev/life-planning-coach
- **Ветка:** `main` (единственная)

---

## 2. Структура проекта

```
life-planning-coach/
├── SKILL.md                    # Главный файл скилла (≤500 строк, ≤5000 слов)
├── README.md                   # Документация для пользователей
├── setup.py                    # Python package metadata (version must match git tag)
├── life-planning-dashboard.html # HTML Dashboard (offline-ready, file:// protocol)
├── CHANGELOG.md                # История изменений
├── ROADMAP.md                  # План развития
├── BACKLOG.md                  # Идеи без привязки к версии
├── RETRO_*.md                  # Ретроспективы
├── AGENTS.md                   # Этот файл
├── references/                 # Тяжёлый контент (>300 строк на тему)
│   ├── diagnostic_methods.md
│   ├── authentic_goal_filter.md
│   ├── communication_style.md
│   ├── calendar_constants.md
│   ├── conversation_state_schema.md
│   ├── acceptance_criteria_v0.7.md
│   ├── emotion_regulation.md
│   ├── energy_scheduling.md
│   ├── recovery_protocol.md
│   ├── win_alert.md
│   └── ...
├── tests/                       # Системные и интеграционные тесты
│   ├── unit/
│   │   └── test_dashboard.py
│   └── system/
│       ├── test_version_consistency.py
│       ├── test_github_sync.py
│       ├── test_readme_integrity.py
│       ├── test_skill_structure.py
│       ├── test_v071_features.py
│       ├── test_v080_features.py
│       └── test_v090_features.py
├── scripts/
│   ├── build-skill.ps1
│   ├── build-skill.sh
│   ├── release.sh               # Атомарный релиз (единственный способ!)
│   └── sync-version.sh          # Синхронизация версий
├── .github/
│   ├── workflows/
│   │   └── release-guard.yml    # Автофикс title'ов релизов
│   └── hooks/
│       └── pre-push-release-guard # Шаблон git hook
└── ...
```

---

## 3. Критические правила (MUST)

### 3.1 Version Consistency — источник правды: git tag
```bash
git describe --tags --abbrev=0  # → v0.9.2
```
Версия должна совпадать во всех файлах:
- `SKILL.md` YAML frontmatter `version:`
- `setup.py` `version="..."`
- `README.md` badge
- `AGENTS.md` раздел 1

**Как обновить:** запускать `bash scripts/sync-version.sh X.Y.Z` (атомарно).

### 3.2 Acceptance Criteria

| Приоритет | Кол-во | Что проверяется |
|-----------|--------|-----------------|
| P0 | 11 | Stage 1.5, Authentic Goal Filter, Communication Style, YAML frontmatter, размер ≤500 строк, обязательные разделы, версия |
| P1 | 4 | Deep Why, TTM, MI, Triggering Precision |
| P2 | 4 | Energy Check, Wheel of Life 11 доменов, Progressive Disclosure, ZIP структура |

**Как проверить:** `python3 -m pytest tests/system/ -v` → **133 passed, 3 skipped**.

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

**ЗАПРЕЩЕНО создавать релизы вручную** (через GitHub UI, `gh release create --title`, или API).
Нарушение приводит к неконсистентным названиям релизов, как произошло с v0.9.0/v0.9.1.

**Конвенция названий релизов** (since commit 856706d):
- Title = **только тег** (`v0.9.2`), без описания
- Описание = **только в теле release notes** (RELEASE_NOTES_vX.Y.Z.md)
- Примеры некорректных: `v0.9.2 — Android Hotfix` ❌
- Примеры корректных: `v0.9.2` ✅

**Система защиты (3 уровня):**
1. **Git hook** (`.github/hooks/pre-push-release-guard`) — блокирует `git push` тега без RELEASE_NOTES файла
2. **GitHub Actions** (`.github/workflows/release-guard.yml`) — при создании/редактировании релиза: автофикс title + комментарий-предупреждение + tracking issue
3. **AGENTS.md §0** — этот документ запрещает ручное создание релизов для всех AI-агентов

**Установка hook'а:**
```bash
cp .github/hooks/pre-push-release-guard .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

### 4.3 Post-commit hook
При коммите выводится предупреждение если есть unpushed commits:
```
⚠️  ВНИМАНИЕ: N commit(s) не запушены на GitHub!
```

### 4.4 System tests
ВСЕ тесты должны проходить перед релизом:
```bash
python3 -m pytest tests/system/ -v
# Expected: 133 passed, 3 skipped
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
*Версия: 3.0 (для life-planning-coach v0.9.2+)*
