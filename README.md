# Life Planning Coach

Интерактивный evidence-based life coach для диагностики жизни, постановки целей, еженедельных ретроспектив, визуализации прогресса и интеграции с Google Calendar.

**Версия:** 0.2.0
**Автор:** Andrey Zagreev — [@zagreev](https://t.me/zagreev)
**Лицензия:** [MIT](LICENSE)
**Целевая платформа:** Claude.ai

---

## Установка скилла для Claude

1. Скачайте `life-planning-coach.skill` из [GitHub Releases](https://github.com/azagreev/life-planning-coach/releases)
2. В claude.ai: **Settings → Capabilities → Skills → Upload skill**
3. Выберите файл `.skill` — он развернётся автоматически
4. После установки скилл будет триггериться автоматически — отдельно вызывать не нужно

---

## Быстрый старт

### 1. Дашборд (без установки)

Открой `life-planning-dashboard.html` в браузере. Все данные встроены, интернет не нужен.

```bash
open life-planning-dashboard.html        # macOS
xdg-open life-planning-dashboard.html    # Linux
start life-planning-dashboard.html       # Windows
```

### 2. Google Calendar интеграция (через MCP)

В claude.ai: **Settings → MCP → Google Calendar → Authorize** (один клик).

Скилл автоматически создаёт события (Weekly Review, WOOP, Time Blocks) через встроенный MCP-коннектор. Нет необходимости в credentials.json, Python-зависимостях или encryption key.

---

## Архитектура: 5 Stage

```
Stage 1: Diagnostic        Stage 2: Goal Architecture   Stage 3: Weekly Review
+-- Emotional Landing      +-- BHAG (10-25 лет)         +-- GTD: Get Clear/Current/Creative
+-- Wheel of Life          +-- OKR Life Themes (1-3 г.)  +-- Scrum Retro
+-- Values Clarification   +-- 12-Week Quarter           +-- Progress Audit
+-- Designing Your Life    +-- Weekly Priorities         +-- Adjustment Protocol
+-- Ikigai + Life Story    +-- Daily WOOP

Stage 4: Dashboard              Stage 5: Calendar Integration
+-- Tab: Overview               +-- OAuth 2.0 + Fernet encryption
|   +-- Wheel of Life Radar     +-- CRUD Events
|   +-- OKR Progress Rings      +-- CRUD Tasks
|   +-- Confidence Gauges       +-- Free/ Busy Slots
+-- Tab: Retrospective          +-- 6 Life Planning Presets
|   +-- Calendar Heatmap        |   +-- Weekly Review Reminder
|   +-- Velocity Chart          |   +-- WOOP Morning Session
|   +-- Burndown Chart          |   +-- 12-Week Milestones
+-- Tab: Goals                  |   +-- Daily Top-3 Tasks
    +-- 12-Week Tracker         |   +-- Deep Work Time Blocks
    +-- Weekly Priorities       |   +-- Find Available Slots
    +-- WOOP Cards
    +-- BHAG Roadmap
```

---

## Методики (Evidence-Based)

| Методика | Эффект | Источник | Применение |
|----------|--------|----------|------------|
| Goal-Setting Theory | d = 0.42-0.80 | Locke & Latham, 2002 | BHAG, OKR |
| Implementation Intentions | d = 0.65 | Gollwitzer & Sheeran, 94 studies | Daily if-then plans |
| WOOP / Mental Contrasting | g = 0.336 | Wang et al., 2021 | Daily WOOP sessions |
| Self-Determination Theory | r = .46-.60 | Deci & Ryan, 2000 | Coaching framework |
| Weekly Reflection | +23% performance | Di Stefano et al., Harvard | Weekly Review |

---

## Структура проекта

```
life-planning-coach/
├── README.md                          # Этот файл
├── SKILL.md                           # Основной skill (для AI-агента)
├── life-planning-dashboard.html       # Интерактивный дашборд
├── life-planning-coach.skill          # Упакованный skill
│

├── references/                        # Документация методик
│   ├── diagnostic_methods.md          # Stage 1 протоколы
│   ├── goal_architecture.md           # Stage 2 протоколы
│   ├── weekly_review.md              # Stage 3 протоколы
│   ├── science_backing.md            # Научная валидация
│   ├── dashboard_guide.md            # Гайд по дашборду
│   └── calendar_integration.md       # Гайд по Calendar API
│
└── setup.py                           # Python package installer
```

---

## Настройка Google Calendar

1. В claude.ai открой **Settings → MCP → Google Calendar**
2. Нажми **Authorize** — один клик, без скачивания файлов
3. Скилл автоматически получит доступ к календарю через MCP

Если подключение недоступно — скилл продолжит работу в текстовом режиме без синхронизации с календарём.

---

## Требования

| Компонент | Требования |
|-----------|-----------|
| Дашборд | Любой современный браузер (Chrome, Firefox, Safari) |
| Google Calendar | Аккаунт Google, авторизация через MCP в claude.ai |

---

## Безопасность

- **OAuth 2.0** через официальный MCP-коннектор Google (управляется Anthropic)
- **Никакие credentials не хранятся в коде скилла**
- **Zero-trust**: скилл не имеет прямого доступа к токенам, все вызовы через MCP

---

## Лицензия

MIT License — свободное использование для личных и коммерческих целей.
