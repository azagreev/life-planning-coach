# Life Planning Coach

Интерактивный evidence-based life coach для постановки целей и планирования жизни. Помогает разобраться, куда двигаться, построить систему целей от 25 лет до сегодняшнего дня и поддерживать регулярную ретроспективу.

**Чем отличается от простого промпта к Claude:**
- **Emotional Landing Protocol** — никаких тестов и оценок до эмоционального контакта. Скилл начинает с валидации, а не с вопросов.
- **Без давления** — в диалоге не используются слова «надо», «должен», «нужно». Только «можно», «если захотите», «попробовать».
- **Stage 1.5: Фильтр аутентичных целей** — перед постановкой целей скилл проверяет: чья это цель, есть ли энергия, нет ли социального давления. Радар из 5 осей + портфель целей (активные / на паузе / паттерны).
- **Адаптация стиля коммуникации** — скилл калибруется под вашу личность (Big Five × TTM × MI): от «Нежного родителя» до «Провокационного консультанта».
- **Evidence-based foundation** — каждая методика (Wheel of Life, WOOP, OKR) имеет научную валидацию с указанием эффект-сайзов.
- **Habit Tracker / Dashboard Streaks** — визуализация серий привычек (active_habits, digital, sugar, focus)
- **Mobile Dashboard (responsive)** — адаптивный дашборд для телефонов
- **5-Minute Micro-Sessions** — быстрые чек-ины на 5 минут для сохранения momentum
- **Quick Decision Protocol** — 2–3 вопроса для принятия решения «здесь и сейчас»
- **Reward Audit (Grayscale Guide)** — осознанность cheap dopamine: инструкции Grayscale для iOS/Android

**Версия:** 0.9.2  
**Автор:** Andrey Zagreev — [@zagreev](https://t.me/zagreev)  
**Лицензия:** [MIT](LICENSE)  
**Целевая платформа:** Claude.ai (Free, Pro, Max, Team, Enterprise — skills доступны на всех планах)

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
- Полная диагностика 11 сфер жизни (Wheel of Life) с числовыми оценками
- Ранжирование личных ценностей (Schwartz PVQ)
- Калибровка стиля коммуникации (2 вопроса)
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
- Аккаунт Claude.ai (любой план — Free, Pro, Max)
- Современный браузер (для дашборда)
- Google-аккаунт — опционально (для календаря и автосохранения в Drive)

**Не нужно:**
- ❌ Устанавливать Python, зависимости, credentials.json
- ❌ Платить за API Google
- ❌ Заполнять таблицы вручную — всё ведёт скилл

---

## Как проходит работа после диагностики

```
Неделя 0: Диагностика
├── Emotional Landing (эмоциональный контакт)
├── Style Calibration (калибровка стиля коммуникации)
├── Wheel of Life (оценка 11 сфер 1-10)
├── Values Clarification (10 ценностей Schwartz)
├── Designing Your Life (Workview + Odyssey Plans)
└── Ikigai + Life Story (пиковые моменты, провалы)

Неделя 0.5: Фильтр целей (Stage 1.5)
├── Red Flag Detector (6+1 красных флагов)
├── Deep Why (3 уровня «почему»)
├── Societal Pressure Test (4 вопроса)
├── True Goal Score (радар из 5 осей)
└── Goal Portfolio (активные / на паузе / паттерны)

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
- Wheel of Life scores (11 чисел 1-10)
- Values ranking (10 ценностей с весами)
- BHAG текст
- Life Themes: objective + 3-5 key results каждая
- 12-Week OKR: objectives + key results с дедлайнами
- Weekly priorities (список строк)
- Daily WOOP: wish + outcome + obstacle + plan (4 строки)
- Weekly reviews: что работало / не работало / корректировки
- Daily Top-3: список задач со статусом выполнения

**Сохранение данных:**
- **По умолчанию:** ключевые факты автоматически сохраняются в Claude Memory. При возвращении скилл вспомнит контекст через естественный диалог.
- **Опционально:** подключите Google Drive — скилл создаст личную wiki с целями, прогрессом и инсайтами в вашем облаке. Данные не потеряются при смене устройства или закрытии вкладки.
- При длинных диалогах контекст может сжиматься — для надёжности рекомендуется подключить Google Drive после 1-2 сессий.

---

## Установка скилла (пошагово)

### Шаг 1. Скачать скилл

1. Открой [GitHub Releases](https://github.com/azagreev/life-planning-coach/releases)
2. Скачай файл `life-planning-coach-vX.Y.Z.zip` (где X.Y.Z — последняя версия, например `0.7.0`)

> **Примечание:** доступны два файла:
> - `life-planning-coach-vX.Y.Z.zip` — ZIP-архив
> - `life-planning-coach-vX.Y.Z.skill` — тот же ZIP-архив с расширением `.skill`
>
> Оба файла идентичны — выбирай любой. Anthropic рекомендует ZIP.
>
> **Для разработчиков:** собрать из исходников: `bash scripts/build-skill.sh`

### Шаг 2. Загрузить в Claude

> **Skills доступны на всех планах: Free, Pro, Max, Team, Enterprise.** Подписка Pro не требуется.

1. Войди в [claude.ai](https://claude.ai)
2. Включи **Code execution**:
   - **Settings → Capabilities → Code execution and file creation** → ON
   - (Для Team/Enterprise: владелец организации обязан включить в **Organization settings > Skills**)
3. Перейди в **Customize → Skills**
4. Нажми **+** → **+ Create skill**
5. Выбери **Upload a skill**
6. Выбери скачанный ZIP-файл (`life-planning-coach-vX.Y.Z.zip` или `.skill`)
7. Дождись сообщения об успешной загрузке
8. Включи скилл тумблером в списке Skills

### Шаг 3. Активировать

- Скилл активируется автоматически при фразах: "помоги спланировать жизнь", "не знаю куда двигаться", "wheel of life", "life planning"
- Или напиши напрямую: `/life-planning-coach` или "запусти life coach"

---

## Настройка Google Drive (опционально)

Если хочешь, чтобы скилл автоматически сохранял прогресс между сессиями в облаке:

> **Без облака:** скилл работает полностью в текстовом режиме. Данные сохраняются в памяти Claude (Claude Memory) и в файле разговора. Google Drive/Calendar — опционально, для тех, кто хочет внешнее хранилище.

### Шаг 1. Подключить Google Drive

1. В claude.ai открой **Settings → MCP**
2. Найди **Google Drive** в списке доступных коннекторов
3. Нажми **Authorize**
4. Войди в свой Google-аккаунт и дай разрешение
5. Вернись в Claude — коннектор покажет статус "Connected"

### Шаг 2. Согласиться на сохранение

Во время сессии скилл предложит: "Хочешь, чтобы я сохранял твой прогресс в Google Drive?"

Нажмите **Да** — скилл создаст папку "Life Planning Coach Wiki" в вашем Google Drive и будет автоматически обновлять файлы с целями, инсайтами и прогрессом.

**Что вы получите:**
- 📁 Папка "Life Planning Coach Wiki" в вашем Google Drive
- 📄 Файлы на русском: цели, Wheel of Life, инсайты, дашборд
- 🔄 Автоматическое обновление в конце каждой сессии
- 📱 Доступ с любого устройства

**Безопасность:** данные хранятся в вашем Google Drive, скилл только обновляет файлы.

---

## Настройка Google Calendar (настоятельно рекомендуется)

Calendar — это **Execution Backbone** скилла. Запланированное событие имеет 80% вероятность выполнения vs 30% для списка задач (Milkman et al., 2021). Без календаря цели остаются намерениями без временных якорей.

После подключения скилл автоматически создаст события:

### Шаг 1. Подключить MCP

1. В claude.ai открой **Settings → MCP**
2. Найди **Google Calendar** в списке доступных коннекторов
3. Нажми **Authorize**
4. Войди в свой Google-аккаунт и дай разрешение
5. Вернись в Claude — коннектор должен показать статус "Connected"

**Что автоматически попадёт в календарь:**
- Weekly Review (воскресенье, 1.5–2 часа)
- WOOP-сессии (ежедневно, 10 минут)
- Time Blocks для важных целей
- Deadline-напоминания по OKR

### Если подключение не работает

- Скилл продолжит работу в текстовом режиме — все планы остаются в разговоре
- Попробуй переподключить: Settings → MCP → Google Calendar → Disconnect → Authorize

---

## Быстрый старт

### Первый разговор со скиллом (1 минута)

После установки напишите Claude любую фразу-триггер:
> «Я чувствую, что жизнь проходит мимо, помоги разобраться»

Скилл начнёт с **Emotional Landing** — эмоционального контакта, а не с тестов. Первые 5–10 минут — валидация вашего состояния и одно конкретное действие на сегодня.

Другие рабочие триггеры:
- «Не знаю, куда двигаться»
- «Хочу поставить цели на год»
- «Сделай Wheel of Life»
- `/life-planning-coach`

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
Stage 1: Diagnostic        Stage 1.5: Goal Filter       Stage 2: Goal Architecture   Stage 3: Weekly Review
+-- Emotional Landing      +-- Red Flag Detector        +-- BHAG (10-25 лет)         +-- GTD: Get Clear/Current/Creative
+-- Style Calibration      +-- Deep Why (3 levels)      +-- OKR Life Themes (1-3 г.) +-- Scrum Retro
+-- Wheel of Life (11)     +-- Societal Pressure Test   +-- 12-Week Quarter          +-- Progress Audit
+-- Values Clarification   +-- True Goal Score (radar)  +-- Weekly Priorities        +-- Adjustment Protocol
+-- Designing Your Life    +-- Goal Portfolio           +-- Daily WOOP
+-- Ikigai + Life Story

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
├── CHANGELOG.md                       # История изменений проекта
├── ROADMAP.md                         # Планы будущих релизов
├── BACKLOG.md                         # Бэклог идей
├── SKILL.md                           # Основной skill (для AI-агента)
├── life-planning-dashboard.html       # Интерактивный дашборд
├── dist/                                # Сборочные артефакты (не в git)
│   ├── life-planning-coach-vX.Y.Z.zip   # Упакованный skill (ZIP по требованиям Anthropic)
│   └── life-planning-coach-vX.Y.Z.skill # Тот же ZIP с расширением .skill
│
├── references/                        # Документация методик
│   ├── diagnostic_methods.md          # Stage 1 протоколы
│   ├── authentic_goal_filter.md       # Stage 1.5 протоколы
│   ├── communication_style.md         # Адаптация стиля коммуникации
│   ├── goal_architecture.md           # Stage 2 протоколы
│   ├── weekly_review.md              # Stage 3 протоколы
│   ├── science_backing.md            # Научная валидация
│   ├── dashboard_guide.md            # Гайд по дашборду
│   ├── calendar_integration.md       # Гайд по Calendar MCP
│   └── USER_GUIDE_DRIVE.md           # Гайд по подключению Google Drive
│
└── setup.py                           # Python package installer
```

---

## Требования

| Компонент | Требования |
|-----------|-----------|
| Claude.ai | Любой план (Free+) — skills доступны на всех тарифах |
| Дашборд | Любой современный браузер (Chrome, Firefox, Safari) |
| Google Calendar | Аккаунт Google, авторизация через MCP в claude.ai |

---

## Безопасность

**Техническая:**
- **OAuth 2.0** через официальный MCP-коннектор Google (управляется Anthropic)
- **Никакие credentials не хранятся в коде скилла**
- **Zero-trust**: скилл не имеет прямого доступа к токенам, все вызовы через MCP

**Психологическая:**
- Этот скилл — инструмент для самопознания и планирования, **не замена психотерапии или психиатрической помощи**.
- Если вы испытываете устойчивое чувство безысходности, мысли о самоповреждении или все сферы жизни оцениваются на 1–2 из 10 — скилл порекомендует обратиться к профессионалу.
- Вы можете пропустить любой вопрос или прервать сессию в любой момент.

---

## FAQ и устранение неполадок

**Скилл не активируется на триггер-фразы**
- Убедитесь, что файл загружен: Settings → Capabilities → Skills → life-planning-coach должен быть в списке.
- Попробуйте прямую команду: `/life-planning-coach` или «запусти life coach».

**Данные пропали после закрытия вкладки**
- Скилл использует Claude Memory для сохранения ключевых фактов между сессиями. При возвращении скилл вспомнит контекст через естественный диалог.
- Для полной сохранности рекомендуется подключить Google Drive (1 клик в Settings → MCP → Google Drive).
- Если данные всё же потеряны — просто расскажите скиллу, над чем работали, и он подхватит контекст.

**Как обновить скилл до новой версии**
1. Settings → Capabilities → Skills → life-planning-coach → Remove.
2. Загрузите новый файл `life-planning-coach.zip`.
3. Активация сохранится автоматически.

**Как удалить скилл**
- Settings → Capabilities → Skills → life-planning-coach → Remove. Все данные останутся в истории разговоров Claude.

---

## Лицензия

MIT License — свободное использование для личных и коммерческих целей.
