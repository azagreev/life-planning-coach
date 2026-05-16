# Life Planning Coach

Интерактивный evidence-based life coach для диагностики жизни, постановки целей, еженедельных ретроспектив, визуализации прогресса и интеграции с Google Calendar.

---

## Быстрый старт

### 1. Дашборд (без установки)

Открой `life-planning-dashboard.html` в браузере. Все данные встроены, интернет не нужен.

```bash
open life-planning-dashboard.html        # macOS
xdg-open life-planning-dashboard.html    # Linux
start life-planning-dashboard.html       # Windows
```

### 2. Google Calendar интеграция

```bash
cd calendar_integration
pip install -r requirements.txt

# Первая настройка (один раз)
export CALENDAR_ENCRYPTION_KEY="your-secret-key-here"

# Запуск примеров
python example_usage.py
```

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
├── calendar_integration/              # Python модуль
│   ├── __init__.py
│   ├── auth.py                        # OAuth + Fernet encryption
│   ├── calendar_manager.py            # CRUD событий + presets
│   ├── tasks_manager.py               # CRUD задачи + presets
│   ├── config.py                      # Цвета, настройки
│   ├── models.py                      # Dataclasses
│   ├── exceptions.py                  # Иерархия ошибок
│   ├── example_usage.py               # 7 примеров
│   └── requirements.txt               # Зависимости
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

### 1. Создать проект в Google Cloud

1. Открой [Google Cloud Console](https://console.cloud.google.com/)
2. Создай новый проект: **Life Planning Coach**
3. Включи API:
   - **Google Calendar API**
   - **Google Tasks API**
4. Настрой **OAuth Consent Screen** (External)
5. Создай **OAuth 2.0 Credentials** (Desktop app)
6. Скачай `credentials.json` и положи в `calendar_integration/`

### 2. Установить зависимости

```bash
cd calendar_integration
pip install -r requirements.txt
```

### 3. Запустить первую авторизацию

```python
from calendar_integration import CalendarAuth

auth = CalendarAuth(
    client_secrets_file="credentials.json",
    encryption_key="your-secure-password-here"
)
auth.authenticate()  # Откроется браузер для авторизации
```

Токен сохранится в зашифрованном виде. При следующих запусках браузер не понадобится.

### 4. Использовать

```python
from calendar_integration import CalendarAuth, CalendarManager, TasksManager

auth = CalendarAuth(client_secrets_file="credentials.json",
                    encryption_key="your-secure-password")
calendar = CalendarManager(auth)
tasks = TasksManager(auth)

# Weekly Review каждое воскресенье в 19:00
calendar.create_weekly_review_reminder(timezone="Europe/Moscow")

# WOOP каждый будний день в 7:00
calendar.create_woop_reminder(timezone="Europe/Moscow")

# 3 приоритета на сегодня в Google Tasks
tasks.create_daily_top3(
    priorities=["Написать главу книги", "Позвонить клиенту", "Пробежать 5км"],
    due=date.today()
)

# Найти свободные слоты на сегодня
free_slots = calendar.get_free_slots(
    target_date=date.today(),
    duration_minutes=90,
    work_start=9,
    work_end=18
)
```

---

## Требования

| Компонент | Требования |
|-----------|-----------|
| Дашборд | Любой современный браузер (Chrome, Firefox, Safari) |
| Python модуль | Python 3.9+, `google-api-python-client`, `google-auth-oauthlib`, `cryptography` |
| Google Calendar | Аккаунт Google, проект в Google Cloud Console |

---

## Безопасность

- **Fernet-шифрование** (AES-128-CBC + HMAC) для токенов
- **Случайный salt** для PBKDF2 (хранится отдельно, права 0o600)
- **Encryption key обязателен** — нет insecure fallback
- **OAuth 2.0** с автоматическим refresh токена
- **Никакие credentials не хранятся в коде**

---

## Лицензия

MIT License — свободное использование для личных и коммерческих целей.
