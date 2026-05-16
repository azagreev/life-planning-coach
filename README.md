# Life Planning Coach

Интерактивный evidence-based life coach для постановки целей и планирования жизни. Помогает разобраться, куда двигаться, построить систему целей от 25 лет до сегодняшнего дня и поддерживать регулярную ретроспективу.

**Версия:** 0.2.0  
**Автор:** Andrey Zagreev — [@zagreev](https://t.me/zagreev)  
**Лицензия:** [MIT](LICENSE)  
**Целевая платформа:** Claude.ai (требуется подписка Pro для MCP)

---

## Для кого этот скилл

- Чувствуешь, что "жизнь проходит мимо", но не понимаешь, что именно хочешь изменить
- На перепутье: смена профессии, релокация, развод, выгорание
- Есть амбиции, но нет чёткой системы: цели расплывчатые, мотивация падает
- Пробовал планировать, но бросал: таблицы, трекеры, приложения не прижились
- Хочешь регулярную ретроспективу жизни, но нет инструмента, который бы не бросить

---

## Какую ценность принесёт

**После первой сессии (20-40 минут)**
- Полная диагностика 8 сфер жизни (Wheel of Life) с числовыми оценками
- Ранжирование личных ценностей (Schwartz PVQ)
- Первый инсайт: "вот почему я чувствую то, что чувствую"

**После 2-3 сессий**
- BHAG — одна большая цель на 10-25 лет
- 3-5 жизненных тем (Life Themes) на 1-3 года
- Конкретные OKR на 12 недель
- Система еженедельных приоритетов

**После 4+ сессий**
- Еженедельная ретроспектива (GTD + Scrum Retro)
- Ежедневные WOOP-сессии (Wish-Outcome-Obstacle-Plan)
- Интеграция с Google Calendar: автоматические напоминания, time blocks
- Интерактивный дашборд прогресса (HTML, offline)

---

## Что нужно на входе

**От пользователя:**
- Готовность честно отвечать на вопросы (5-10 минут на блок)
- 20-40 минут на первую диагностику
- Желание регулярно возвращаться (еженедельно или по мере необходимости)

**Технически:**
- Аккаунт Claude.ai (Pro для подключения Google Calendar)
- Google-аккаунт (если нужна календарная интеграция)
- Современный браузер (для дашборда)

**Не нужно:**
- ❌ Устанавливать Python, зависимости, credentials.json
- ❌ Платить за API Google
- ❌ Заполнять таблицы вручную — всё ведёт скилл

---

## Как проходит работа после диагностики

```
Неделя 0: Диагностика
├── Emotional Landing (эмоциональный контакт)
├── Wheel of Life (оценка 8 сфер 1-10)
├── Values Clarification (10 ценностей Schwartz)
├── Designing Your Life (Workview + Odyssey Plans)
└── Ikigai + Life Story (пиковые моменты, провалы)

Неделя 1: Архитектура целей
├── BHAG — одна цель на всю жизнь
├── 3-5 Life Themes (1-3 года)
├── 12-Week Objectives + Key Results
├── Weekly Priorities
└── Daily WOOP (if-then намерения)

Неделя 2+: Поддержка ритма
├── Weekly Review (каждое воскресенье, можно в календаре)
├── Daily Top-3 (три приоритета на день)
├── Time Blocks (блокировка времени на важное)
├── Корректировка целей по ходу
└── Dashboard — визуализация прогресса
```

**Данные, которые собирает скилл:**
- Wheel of Life scores (8 чисел 1-10)
- Values ranking (10 ценностей с весами)
- BHAG текст
- Life Themes: objective + 3-5 key results каждая
- 12-Week OKR: objectives + key results с дедлайнами
- Weekly priorities (список строк)
- Daily WOOP: wish + outcome + obstacle + plan (4 строки)
- Weekly reviews: что работало / не работало / корректировки
- Daily Top-3: список задач со статусом выполнения

Все данные хранятся в контексте разговора с Claude. Пользователь может экспортировать в Markdown или JSON в любой момент.

---

## Установка скилла (пошагово)

### Шаг 1. Скачать скилл

1. Открой [GitHub Releases](https://github.com/azagreev/life-planning-coach/releases)
2. Скачай файл `life-planning-coach.skill`

### Шаг 2. Загрузить в Claude

1. Войди в [claude.ai](https://claude.ai) (нужна подписка Pro)
2. Открой **Settings** (шестерёнка в правом верхнем углу)
3. Перейди во вкладку **Capabilities**
4. В разделе **Skills** нажми **Upload skill**
5. Выбери скачанный файл `life-planning-coach.skill`
6. Дождись сообщения "Skill uploaded successfully"

### Шаг 3. Активировать

- Скилл активируется автоматически при фразах: "помоги спланировать жизнь", "не знаю куда двигаться", "wheel of life", "life planning"
- Или напиши напрямую: `/life-planning-coach` или "запусти life coach"

---

## Настройка Google Calendar (опционально)

Если хочешь, чтобы скилл автоматически создавал события (Weekly Review, WOOP, Time Blocks):

### Шаг 1. Подключить MCP

1. В claude.ai открой **Settings → MCP**
2. Найди **Google Calendar** в списке доступных коннекторов
3. Нажми **Authorize**
4. Войди в свой Google-аккаунт и дай разрешение
5. Вернись в Claude — коннектор должен показать статус "Connected"

### Шаг 2. Проверить

Скажи скиллу: "Создай напоминание о Weekly Review каждое воскресенье в 19:00"

Если MCP работает — скилл создаст событие в календаре и подтвердит.

### Если подключение не работает

- Скилл продолжит работу в текстовом режиме
- Все планы останутся в разговоре с Claude
- Попробуй переподключить: Settings → MCP → Google Calendar → Disconnect → Authorize

---

## Быстрый старт

### Дашборд (без установки)

Открой `life-planning-dashboard.html` в браузере — все данные встроены, интернет не нужен.

```bash
open life-planning-dashboard.html        # macOS
xdg-open life-planning-dashboard.html    # Linux
start life-planning-dashboard.html       # Windows
```

---

## Архитектура: 5 Stage

```
Stage 1: Diagnostic        Stage 2: Goal Architecture   Stage 3: Weekly Review
+-- Emotional Landing      +-- BHAG (10-25 лет)         +-- GTD: Get Clear/Current/Creative
+-- Wheel of Life          +-- OKR Life Themes (1-3 г.) +-- Scrum Retro
+-- Values Clarification   +-- 12-Week Quarter          +-- Progress Audit
+-- Designing Your Life    +-- Weekly Priorities        +-- Adjustment Protocol
+-- Ikigai + Life Story    +-- Daily WOOP

Stage 4: Dashboard              Stage 5: Calendar Integration (MCP)
+-- Tab: Overview               +-- Zero-setup OAuth via claude.ai
|   +-- Wheel of Life Radar     +-- CRUD Events
|   +-- OKR Progress Rings      +-- Free/ Busy Slots
|   +-- Confidence Gauges       +-- 4 Life Planning Presets
+-- Tab: Retrospective          |   +-- Weekly Review Reminder
|   +-- Calendar Heatmap        |   +-- WOOP Morning Session
|   +-- Velocity Chart          |   +-- 12-Week Milestones
|   +-- Burndown Chart          |   +-- Deep Work Time Blocks
+-- Tab: Goals                  +-- Daily Top-3 (text, conversation state)
    +-- 12-Week Tracker
    +-- Weekly Priorities
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
│   └── calendar_integration.md       # Гайд по Calendar MCP
│
└── setup.py                           # Python package installer
```

---

## Требования

| Компонент | Требования |
|-----------|-----------|
| Claude.ai | Подписка Pro (для загрузки skills + MCP) |
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
