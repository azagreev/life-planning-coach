# 🧭 Life Planning Coach

![tests](https://img.shields.io/badge/tests-510%2B%20passed-brightgreen)
![coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)
![schema](https://img.shields.io/badge/state%20schema-v2.2-blue)
![version](https://img.shields.io/badge/version-1.1.0-blue)

> **Превращает диалог с AI в evidence-based личный план:** цели, привычки, ретроспективный ритм. Без приложений, подписок, лишних аккаунтов.
> **Версия:** 1.1.0 | [Релизы](https://github.com/azagreev/life-planning-coach/releases) | [CHANGELOG](CHANGELOG.md)

---

## Чем отличается

|  | Notion / Todoist | Обычный AI-коуч | **Life Planning Coach** |
|---|---|---|---|
| **Метод** | Самодельные системы | Общие советы | 28+ научных публикаций (ACT, CBT, OKR, WOOP, привычки, TGD) |
| **Фокус** | Задачи и списки | Поддержка и тон | Жизненный план + ритм ретроспектив |
| **Хранение** | Файлы | Память внутри чата | Wiki в Диске + Календарь + AI-память (по желанию) |
| **Подстройка** | Один шаблон для всех | Общий | 4 режима: СДВГ, переходный период, пожилые, трудности с планированием |

---

## Что внутри

Модульный коучинг-навык, работающий на разных AI-платформах. Основан на методах с научной валидацией:

- **Колесо жизни** (11 сфер, включая духовность и ценности)
- **Фильтр аутентичных целей** — проверка целей на внутреннюю мотивацию (Этап 1\.5)
- **Поиск ключевых ценностей** — выявление ценностей снизу-вверх + Режим компаса для ежедневных решений
- **Архитектура целей** — BHAG → OKR → WOOP с привычками (триггер–действие–награда)
- **Еженедельный обзор** — 7 шагов GTD + Scrum-ретро + список побед + проверка привычек
- **Регуляция эмоций** — на основе DBT (когнитивная переоценка, заземление, самосочувствие, переоценка конфликтов)
- **Отслеживание здоровья и метаболизма** (по желанию) — сон, стресс, белок, клетчатка как научно подтверждённые рычаги аппетита
- **Согласование целей** — координация целей с партнёром (Transactive Goal Dynamics)
- **Адаптивный стиль общения** — Большая Пятёрка × модель изменений TTM × мотивационное интервью

**4 этапа коучинга:**
1. **Диагностика** → 2. **Архитектура целей** → 3. **Исполнение** → 4. **Глубокая работа**

---

## Выбор платформы

| Платформа | Для кого | Установка | Календарь | Диск | Файл |
|-----------|----------|-----------|-----------|------|------|
| **Claude.ai** | Опытные пользователи, нужны MCP-коннекторы | Загрузка ZIP | ✅ MCP¹ | ✅ MCP¹ | `.zip` / `.skill` |
| **Grok** (xAI) | Пользователи xAI, большой контекст | Скопировать-вставить | ✅ встроенный OAuth | ✅ встроенный OAuth | `-grok.md` |
| **Kimi OK Computer** | Простая настройка через сайт | Веб-агент | ❌ только текст | ❌ нет | `-kimi.md` |
| **Kimi Code CLI** | Разработчики, терминал | Папка + JSON | ✅ MCP (вручную) | ✅ MCP (вручную) | `-kimi-cli/` |

¹ MCP-коннекторы (Google Календарь + Диск) подтверждены на **тарифе Claude Max** (проверка проведена 2026-05-26 — см. [docs/research/mcp_poc_log.md](docs/research/mcp_poc_log.md)). Тарифы Pro/Team не проверялись. На Free, скорее всего, MCP недоступен — запасной вариант — **текстовый режим коуча** (план без интеграций).

**→ [Подробное сравнение платформ](references/platforms/CROSS_PLATFORM_COMPARISON.md)**  
**→ [Дерево решений](references/platforms/CROSS_PLATFORM_COMPARISON.md#decision-tree)**

---

## Быстрый старт

### Claude.ai (ZIP-скилл)

1. Скачайте `life-planning-coach-v1.1.0.zip` из раздела [Релизы](https://github.com/azagreev/life-planning-coach/releases)
2. Claude → Настройки → Возможности → включите «Code execution and file creation»
3. Настроить → Скиллы → + → загрузите ZIP
4. В любом чате наберите `/life-planning-coach`

**→ [Полное руководство для Claude](references/platforms/USER_GUIDE_CLAUDE.md)**

### Grok (xAI) — один файл

1. Скачайте `life-planning-coach-v1.1.0-grok.md`
2. Скопируйте всё содержимое, вставьте на [grok.com](https://grok.com)
3. Добавьте сообщение: `Ты — Life Planning Coach. Начни сессию.`

**→ [Полное руководство для Grok](references/platforms/USER_GUIDE_GROK.md)**

### Kimi OK Computer (веб-агент)

1. Зайдите на [kimi.com/agent](https://kimi.com/agent)
2. Создайте агента → вставьте содержимое `life-planning-coach-v1.1.0-kimi.md` в системный промпт
3. Сохраните и начните диалог

**→ [Полное руководство для Kimi Web](references/platforms/USER_GUIDE_KIMI_OKCOMPUTER.md)**

### Kimi Code CLI (терминал)

```bash
mkdir -p ~/.kimi/skills/life-planning-coach
cp -r platforms/kimi-cli/* ~/.kimi/skills/life-planning-coach/
kimi skill use life-planning-coach
```

**→ [Полное руководство для Kimi CLI](references/platforms/USER_GUIDE_KIMI_CLI.md)**

---

## Структура проекта

```
life-planning-coach/
├── platforms/              # Сборки под платформы
│   ├── claude/SKILL.md     # Папка + чтение файлов по запросу
│   ├── grok/SKILL.md       # Один файл, всё инлайн
│   ├── kimi/SKILL.md       # Один файл, всё инлайн
│   └── kimi-cli/SKILL.md   # Папка + чтение файлов по запросу
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
├── tests/                  # 510+ тестов (unit + system + e2e)
├── scripts/
│   ├── build-skill.sh      # Сборка всех артефактов
│   └── build-platform-skill.py  # Генерация файлов под платформы
├── dist/                   # Готовые файлы релизов
├── SKILL.master.md         # Платформонезависимый исходник
├── CHANGELOG.md
├── ROADMAP.md
└── BACKLOG.md
```

---

## Сборка из исходников

```bash
# Создать все файлы под платформы
python3 scripts/build-platform-skill.py all

# Собрать готовые файлы релизов (ZIP, .skill, .md)
bash scripts/build-skill.sh

# Запустить тесты
python3 -m pytest tests/ -q
```

---

## Тестирование

- **510+ тестов** — покрытие структуры, контента и совместимости с платформами
- **Эталонный набор** (`tests/e2e/`) — 20 поведенческих сценариев
- **Шкала оценки** — LLM в роли судьи для проверки качества коучинга
- **Протокол ручного тестирования** — `tests/e2e/MANUAL_TEST_RUN.md`

```bash
python3 -m pytest tests/ -q
```

---

## Приватность и оговорка

- **Это не терапия.** Это коучинг, а не клиническое лечение. При проблемах с ментальным здоровьем обратитесь к лицензированному специалисту.
- **Ваши данные:** содержимое коучинга остаётся внутри разговора на вашей AI-платформе. Доступ через MCP-коннекторы ограничен OAuth-разрешениями и контролируется вами.
- **Никакого сбора данных.** Проект не собирает статистику использования.
- Полное уведомление о приватности — в `SKILL.md` каждой платформы.

---

## Как внести вклад

См. [CONTRIBUTING.md](CONTRIBUTING.md). Ключевые правила:

- Новый код → новые тесты
- Релиз только через `bash scripts/release.sh X.Y.Z`
- Формат коммитов: `<type>: <описание>` (`feat`, `fix`, `docs`, `chore`, `test`, `refactor`)

---

## Дорожная карта

См. [ROADMAP.md](ROADMAP.md) — предстоящие функции, и [BACKLOG.md](BACKLOG.md) — идеи на будущее.

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
