# 🧭 Life Planning Coach

> **Интерактивный evidence-based life coach** для Claude.ai, Grok (xAI) и Kimi (OK Computer + Code CLI).  
> **Версия:** 0.12.1 | [Релизы](https://github.com/azagreev/life-planning-coach/releases) | [CHANGELOG](CHANGELOG.md)

---

## Что это?

Модульный кросс-платформенный коучинг-скилл, основанный на методах с научной валидацией:

- **Wheel of Life** (11 сфер жизни, включая духовность и ценности)
- **Фильтр аутентичных целей** — проверка целей на внутреннюю мотивацию (Stage 1\.5)
- **Архитектура целей** — SMART+ цели с этапами и привычками
- **Weekly Review** — evidence-based ретроспектива
- **Habit Loop** — Cue-Routine-Reward с отслеживанием
- **Регуляция эмоций** — техники, информированные DBT
- **Triggering Precision** — точное определение корней прокрастинации
- **Адаптивный стиль коммуникации** — калибровка под личность пользователя (Big Five × TTM × MI)

**4-этапный коучинговый поток:**
1. **Диагностика** → 2. **Архитектура целей** → 3. **Исполнение** → 4. **Глубокая работа**

---

## Быстрый выбор платформы

| Платформа | Для кого | Установка | Календарь | Диск | Файл |
|-----------|----------|-----------|-----------|------|------|
| **Claude.ai** | Продвинутые пользователи, MCP | ZIP upload | ✅ MCP | ✅ MCP | `.zip` / `.skill` |
| **Grok** (xAI) | Пользователи xAI, большой контекст | Копировать-вставить | ✅ Native OAuth | ✅ Native OAuth | `-grok.md` |
| **Kimi OK Computer** | Простая веб-настройка | Веб-агент | ❌ Текстовый | ❌ Нет | `-kimi.md` |
| **Kimi Code CLI** | Разработчики, терминал | Директория + JSON | ✅ MCP (ручной) | ✅ MCP (ручной) | `-kimi-cli/` |

**→ [Подробное сравнение платформ](references/platforms/CROSS_PLATFORM_COMPARISON.md)**  
**→ [Дерево решений](references/platforms/CROSS_PLATFORM_COMPARISON.md#decision-tree)**

---

## Быстрый старт

### Claude.ai (ZIP Skill)

1. Скачайте `life-planning-coach-v0.12.0.zip` из [Релизов](https://github.com/azagreev/life-planning-coach/releases)
2. Claude → Settings → Capabilities → включить "Code execution and file creation"
3. Customize → Skills → + → Upload ZIP
4. Наберите `/life-planning-coach` в любом чате

**→ [Полное руководство по Claude](references/platforms/USER_GUIDE_CLAUDE.md)**

### Grok (xAI) — Один файл

1. Скачайте `life-planning-coach-v0.12.0-grok.md`
2. Скопируйте всё содержимое, вставьте в [grok.com](https://grok.com)
3. Добавьте: `Ты — Life Planning Coach. Начни сессию.`

**→ [Полное руководство по Grok](references/platforms/USER_GUIDE_GROK.md)**

### Kimi OK Computer (Веб-агент)

1. Перейдите на [kimi.com/agent](https://kimi.com/agent)
2. Создайте агента → вставьте `life-planning-coach-v0.12.0-kimi.md` в системный промпт
3. Сохраните и начните диалог

**→ [Полное руководство по Kimi Web](references/platforms/USER_GUIDE_KIMI_OKCOMPUTER.md)**

### Kimi Code CLI (Терминал)

```bash
mkdir -p ~/.kimi/skills/life-planning-coach
cp -r platforms/kimi-cli/* ~/.kimi/skills/life-planning-coach/
kimi skill use life-planning-coach
```

**→ [Полное руководство по Kimi CLI](references/platforms/USER_GUIDE_KIMI_CLI.md)**

---

## Структура проекта

```
life-planning-coach/
├── platforms/              # Платформенные сборки
│   ├── claude/SKILL.md     # 311 строк, директория + read_file
│   ├── grok/SKILL.md       # 1 190 строк, полностью инлайн
│   ├── kimi/SKILL.md       # 815 строк, полностью инлайн
│   └── kimi-cli/SKILL.md   # 323 строки, директория + read_file
├── references/             # Методики и руководства
│   ├── diagnostic_methods.md
│   ├── communication_style.md
│   ├── authentic_goal_filter.md
│   ├── goal_architecture.md
│   ├── weekly_review.md
│   ├── habit_loop.md
│   ├── emotion_regulation.md
│   ├── dashboard_guide.md
│   ├── science_backing.md
│   ├── calendar_integration.md
│   └── platforms/          # Руководства и сравнения
│       ├── USER_GUIDE_CLAUDE.md
│       ├── USER_GUIDE_GROK.md
│       ├── USER_GUIDE_KIMI_OKCOMPUTER.md
│       ├── USER_GUIDE_KIMI_CLI.md
│       └── CROSS_PLATFORM_COMPARISON.md
├── tests/                  # 300+ тестов (unit + system + e2e)
├── scripts/
│   ├── build-skill.sh      # Сборка всех артефактов
│   └── build-platform-skill.py  # Генерация платформенных SKILL
├── dist/                   # Релизные артефакты
├── SKILL.master.md         # Платформонезависимый исходник
├── CHANGELOG.md
├── ROADMAP.md
└── BACKLOG.md
```

---

## Сборка из исходников

```bash
# Генерация всех платформенных файлов
python3 scripts/build-platform-skill.py all

# Сборка релизных артефактов (ZIP, .skill, .md файлы)
bash scripts/build-skill.sh

# Запуск тестов
python3 -m pytest tests/ -q
```

---

## Тестирование

- **300+ тестов** — покрытие структуры, контента и платформенной совместимости
- **Golden dataset** (`tests/e2e/`) — 20 поведенческих тест-кейсов
- **Evaluation rubric** — LLM-as-a-Judge для оценки качества коучинга
- **Протокол ручного тестирования** — `tests/e2e/MANUAL_TEST_RUN.md`

```bash
python3 -m pytest tests/ -q
```

---

## Приватность и дисклеймер

- **Это не терапия.** Это коучинг, а не клиническое лечение. При проблемах с ментальным здоровьем обратитесь к лицензированному специалисту.
- **Ваши данные:** Контент коучинга остаётся внутри разговора на вашей AI-платформе. Доступ через MCP/коннекторы ограничен OAuth и контролируется вами.
- **Никакой телеметрии.** Проект не собирает данные об использовании.
- Полное privacy-уведомление — в `SKILL.md` каждой платформы.

---

## Как внести вклад

См. [CONTRIBUTING.md](CONTRIBUTING.md). Ключевые правила:

- Новый код → новые тесты
- Релиз только через `bash scripts/release.sh X.Y.Z`
- Формат коммитов: `<type>: <description>` (`feat`, `fix`, `docs`, `chore`, `test`, `refactor`)

---

## Дорожная карта

См. [ROADMAP.md](ROADMAP.md) — предстоящие фичи, и [BACKLOG.md](BACKLOG.md) — идеи.

---

## Лицензия

MIT License — см. [LICENSE](LICENSE)

---

<p align="center">
  <a href="references/platforms/CROSS_PLATFORM_COMPARISON.md">Сравнение платформ</a> •
  <a href="references/platforms/USER_GUIDE_CLAUDE.md">Руководство Claude</a> •
  <a href="references/platforms/USER_GUIDE_GROK.md">Руководство Grok</a> •
  <a href="references/platforms/USER_GUIDE_KIMI_OKCOMPUTER.md">Руководство Kimi Web</a> •
  <a href="references/platforms/USER_GUIDE_KIMI_CLI.md">Руководство Kimi CLI</a>
</p>
