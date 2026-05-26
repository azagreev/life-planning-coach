# Конкурентный анализ: life-planning-coach

> **Дата исследования:** 2026-05-17
> **Версия проекта:** v0.7.0
> **Методология:** Параллельный анализ 7 конкурентов через агентов-исследователей + синтез

---

## Сводная таблица конкурентов

| Конкурент | Тип | Сильная сторона | Главный пробел |
|-----------|-----|-----------------|----------------|
| **GTD Coach Plugin** | Skill | Каскадное планирование (год→квартал→день), auto-review по времени | Одна цель, нет многомерности, нет "почему" |
| **PM OKR Skill** | Skill | Таксономия слабых целей, sanity-check 5 измерений, markdown-шаблоны | Только рабочие OKR, нет longitudinal tracking |
| **Developmental Coach** | Skill | Мета-рефлексия, структурированные сессии, Notion persistence | Нет energy check, нет кросс-сессионного arc |
| **Composio Skills** | Коллекция | 1000+ скиллов, Habitica/Beeminder, Rube MCP | Нет единого фреймворка, разрозненные инструменты |
| **Ordinary Skills** | Коллекция | 1459 скиллов, удобный поиск | 90% — software engineering, минимум life coaching |
| **Rachnog Claude-for-Life** | Экосистема | Модульная ОС, 15+ MCP, deterministic rules, GTD-native | Персонализировано под автора, хрупкие интеграции |
| **Weekly Planning + Daily Brief** | Подход | Доминирующий паттерн 2026, energy-based scheduling | Execution layer, не coaching — нет ценностей, эмоций, стадий |

---

## 1. Что у конкурентов есть, а у нас — нет

### 🔴 Execution Layer (практически полностью отсутствует)

| Фича | Откуда взять | Почему важно | Сложность |
|------|-------------|--------------|-----------|
| **Разбиение задач на шаги с чекпоинтами** | GTD Coach | Превращает абстрактные цели в конкретные действия | Низкая |
| **Auto-review по времени** (7+ дней → weekly, новый месяц → monthly) | GTD Coach | Поддерживает регулярность без инициативы пользователя | Средняя |
| **Course Correction: таблица опций (Pros/Cons)** | GTD Coach | Когда пользователь сбился с пути — структурированный выбор | Низкая |
| **Статусная иконография** (⬜🔄✅❌⏸️⚠️ + 🔴🟡🟢) | GTD Coach | Визуальная сканируемость в markdown | Низкая |
| **"Win Alert" — празднование побед** | GTD Coach | Повышает мотивацию, связывает достижение с доменом | Низкая |
| **Quick Mode / Full Mode** | Weekly Planning | Уважает время пользователя | Низкая |
| **End-of-Day Wrap-Up** | Weekly Planning | Замыкает цикл: что сделано → открытые петли → завтра | Низкая |
| **Energy-Based Scheduling** | Weekly Planning | Творческая работа в пике, рутина в спаде | Низкая |
| **1 Primary Outcome + 2–4 Supporting Tasks в день** | Weekly Planning | Предотвращает перегрузку | Низкая |
| **Color-Coded Priority Triage** (🔴🟡⚡⚪) | Weekly Planning | Универсальный паттерн для всех daily brief | Низкая |
| **TODAY.md / Memory Log Pattern** | Weekly Planning | Локальный файл как source of truth на день | Средняя |
| **Sanity-Check Framework** (Coverage, Balance, Feasibility, Measurability, Alignment) | PM OKR | Проверка качества плана перед принятием | Средняя |
| **Таксономия слабых целей** (Vague, Sandbagging, Moonshots, Missing Baseline) | PM OKR | Обучает пользователя формулировать лучше | Средняя |
| **Structured Report Template** (Growth Report: Summary → Areas → Strengths → Actions → Resources) | Composio | Повторяемый формат для любого обзора | Низкая |
| **Clarifying-Questions-First** | Composio | Перед любым вмешательством — уточнить контекст | Низкая |
| **"When NOT to Use"** | Composio | Снижает ложную активацию, защищает границы | Низкая |
| **Мета-рефлексия: WHAT vs. HOW IT'S STRUCTURED** | Developmental Coach | Глубже обычного коучинга — анализ паттернов мышления | Средняя |
| **Малый эксперимент + критерий успеха** | Developmental Coach | Конкретнее домашнего задания, пригоден для A/B | Низкая |
| **Anti-Badge Safeguard** | Developmental Coach | Предотвращает превращение развития в статусную игру | Низкая |
| **Adaptive Response Length** | Developmental Coach | Кратко → средне → полно в зависимости от фазы | Низкая |

### 🟡 Интеграции & Архитектура

| Фича | Откуда взять | Почему важно | Сложность |
|------|-------------|--------------|-----------|
| **Модульная архитектура плагинов** (marketplace.json → plugin.json → SKILL.md) | Rachnog | Масштабируемость, независимые версии доменов | Высокая |
| **Workflow-first + Specialist routing** | Rachnog | Пользователь говорит "обзор здоровья" — вызывается sleep + recovery + exercise | Высокая |
| **Deterministic rule files (JSON)** | Rachnog | Правила классификации без LLM-cost, версионируются | Средняя |
| **Bidirectional sync с внешними системами** | Rachnog | Не только создавать события, но и читать прогресс | Средняя |
| **Compatibility YAML frontmatter** (`requires: mcp: [...]`) | Rachnog / Composio | Декларативные зависимости — система знает, что нужно | Низкая |
| **Habitica интеграция** (gamification) | Composio | Очки, streaks, rewards для поведенческих изменений | Средняя |
| **Beeminder интеграция** (commitment device) | Composio | Финансовые ставки против прокрастинации | Средняя |
| **Google Tasks через MCP** (не только Calendar) | Composio | Daily Top-3 синхронизируется с Tasks | Средняя |

---

## 2. Что у нас есть, а у конкурентов — нет (наши УТП)

| Наше преимущество | Почему конкуренты не догоняют |
|-------------------|------------------------------|
| **11 доменов Wheel of Life** (включая Духовность, Вклад, Дом) | Все конкуренты используют 8 или меньше. Rachnog — 8, Weekly Planning — вообще не проверяет баланс |
| **Authentic Goal Filter** (проверка целей на внутренность) | GTD Coach спрашивает только What/When. PM OKR — Output vs Outcome, но не Intrinsic vs Extrinsic. Weekly Planning — берёт цели как есть |
| **Evidence-Based Methodology** (TTM, MI, WOOP) | Ни один конкурент не использует Transtheoretical Model или Motivational Interviewing. Developmental Coach — ближе, но без клинической структуры |
| **Emotional Regulation Protocol** (v0.7.0) | Только Developmental Coach касается эмоций, но без протоколов (Gross, Neff). Остальные — execution-only |
| **Progressive Disclosure** (тяжёлый контент в references/) | Rachnog — ближе всего, но у них тоже контент в SKILL.md. Composio — учат этому, но сами не всегда следуют |
| **Acceptance Criteria + System Tests** | Уникально для open-source скиллов. Никто из конкурентов не имеет 39 системных тестов |
| **Therapy Disclaimer + границы** | Developmental Coach — "NOT trauma therapy", но без протокола эскалации. Остальные — вообще без дисклеймера |
| **Календарная интеграция** (Python package) | GTD Coach — нет интеграций. PM OKR — только markdown экспорт. Rachnog — Calendar review, но не создание событий планирования |
| **Русский язык + культурная адаптация** | Все конкуренты — EN-first. GTD Coach — EN/中文/日本語, но без тонкой калибровки |
| **Energy Check** (из AC v0.7) | GTD Coach — поле "Energy Level (1-5)" в шаблоне, но без адаптации рекомендаций |
| **Communication Style (4 квадранта)** | Уникально. Ни один конкурент не адаптирует стиль общения под эмоциональное состояние пользователя |

---

## 3. Стратегические возможности (что взять и куда вписать)

### Ближайшие (v0.7.1 / v0.8.0) — низкая сложность, высокий эффект

#### 3.1 Markdown-таблицы как UI (из GTD Coach + PM OKR)
**Что:** В SKILL.md и references/ активно использовать markdown-таблицы для:
- Плана на неделю (День | Приоритет | Длительность | Статус)
- Обзора доменов Wheel of Life (Домен | Текущий | Целевой | Дельта)
- Course Correction (Опция | За | Против | Рекомендация)
- Progress Check (Ожидалось | Фактически | Разрыв | Паттерн)

**Куда вписать:** В `references/weekly_review_template.md` (новый файл) и в SKILL.md раздел Examples.

**Оценка:** 2–3 часа, нет внешних зависимостей.

---

#### 3.2 Таксономия слабых целей + Sanity-Check (из PM OKR)
**Что:** В Authentic Goal Filter добавить явные паттерны:
| Паттерн | Пример | Проверка |
|---------|--------|----------|
| Расплывчатость | "Стать здоровее" | Есть ли конкретная метрика? |
| Действие вместо результата | "Ходить в зал" | А что изменится в жизни? |
| Без baseline | "Сбросить 10 кг" | Сколько сейчас? |
| Песочница (слишком легко) | "Прочитать 1 книгу в год" | А если 12? |
| Лунные цели (всё 10x) | "Марафон через месяц" | Mix с достижимыми? |

**Куда вписать:** Расширить `references/authentic_goal_filter.md` разделом "Паттерны слабых формулировок".

**Оценка:** 3–4 часа.

---

#### 3.3 Структурированный шаблон сессии (из Developmental Coach)
**Что:** Добавить в SKILL.md опциональный формат итога сессии:
```markdown
## Итог сессии

**Контекст**: [Что обсуждали]
**Ключевые инсайты**: [2–3 пункта]
**Мета-наблюдение**: [Паттерн мышления/поведения]
**Эксперимент**: [Что попробовать] + **Критерий успеха**: [Когда считать выполненным]
**Открытые вопросы**: [Для следующей сессии]
```

**Куда вписать:** В SKILL.md раздел Examples или в новый `references/session_summary_template.md`.

**Оценка:** 1–2 часа.

---

#### 3.4 Status Icon System (из GTD Coach)
**Что:** Зафиксировать в `references/communication_style.md` единую иконографию:
- Статусы: ⬜ Todo, 🔄 В процессе, ✅ Выполнено, ❌ Отменено, ⏸️ Приостановлено, ⚠️ Риск
- Приоритеты: 🔴 P0, 🟡 P1, 🟢 P2
- Эмоции/события: 🏆 Победа, 💡 Инсайт, 📊 Данные, 🔥 Блокер

**Куда вписать:** `references/communication_style.md` — новый раздел "Визуальная нотация".

**Оценка:** 1 час.

---

#### 3.5 "Win Alert" — празднование побед (из GTD Coach)
**Что:** Когда пользователь сообщает о достижении, скилл отвечает структурированно:
```markdown
🎉 Победа!

**Что достигнуто**: [конкретика]
**В каком домене**: [из Wheel of Life]
**Почему это важно**: [связь с большой целью/ценностью]
**Что это говорит о тебе**: [ресурс/качество]
**Следующий шаг**: [поддержание или масштабирование]
```

**Куда вписать:** В SKILL.md раздел Examples.

**Оценка:** 1–2 часа.

---

#### 3.6 Clarifying-Questions-First (из Composio)
**Что:** Перед любым глубоким вмешательством (WOOP, Deep Why, Emotional Regulation) — 2–3 уточняющих вопроса:
- "В каком домене Wheel of Life сейчас наибольший заряд?"
- "Что ты уже пробовал?"
- "Какой формат сейчас удобнее — краткий или подробный?"

**Куда вписать:** В SKILL.md в начало каждого протокола.

**Оценка:** 1 час.

---

#### 3.7 Adaptive Response Length (из Developmental Coach)
**Что:** Добавить в Communication Style три режима ответа:
| Запрос | Длина | Пример |
|--------|-------|--------|
| Уточнение / Проверка | 2–3 предложения | "Да, это внутренняя цель. Готов двигаться дальше?" |
| Исследование | 4–6 предложений | Краткий WOOP без шагов |
| Кристаллизация | Полный протокол | Полный WOOP + действия + чекпоинты |

**Куда вписать:** `references/communication_style.md` — раздел "Адаптивная длина ответа".

**Оценка:** 1–2 часа.

---

#### 3.8 "When NOT to Use" + Anti-Badge Safeguard (из Composio + Developmental Coach)
**Что:**
1. Добавить в SKILL.md явные negative triggers:
   - НЕ использовать для кризисной психотерапии
   - НЕ использовать для медицинских диагнозов
   - НЕ использовать как замену человеческому коучу при тяжёлой травме
2. Добавить Anti-Badge: "Если пользователь использует достижения в домене как доказательство превосходства над другими — мягко переадресовать к внутренней мотивации."

**Куда вписать:** SKILL.md раздел Gotchas и Privacy & Data Handling.

**Оценка:** 1 час.

---

### Среднесрочные (v0.8.0–v0.9.0) — средняя сложность

#### 3.9 Task Breakdown с чекпоинтами (из GTD Coach)
**Что:** Для любого действия из WOOP — опциональное разбиение:
```markdown
## 🔨 Действие: [Название]

**Шаг 1**: [Название] (~X мин)
- [Деталь действия]
- [Деталь действия]
- ✓ Чекпоинт: [как поймём, что шаг выполнен]

**Потенциальные блокеры**:
| Блокер | Решение |
|--------|---------|
```

**Куда вписать:** Новый файл `references/action_breakdown_template.md` + ссылка из SKILL.md.

**Оценка:** 3–4 часа.

---

#### 3.10 Auto-Review Triggers (из GTD Coach)
**Что:** При возвращении пользователя после перерыва:
- 7+ дней → "Давайте проведём Weekly Review"
- Новый месяц → "Начинается новый месяц — хотите Monthly Check-in?"
- Новый квартал → "Пора Quarterly Reflection"

**Как реализовать:** Claude Memory (если доступно) или диалоговый паттерн: "Когда была наша последняя сессия?"

**Куда вписать:** SKILL.md — раздел "Возвращающийся пользователь".

**Оценка:** 2–3 часа (требует тестирования на Memory).

---

#### 3.11 Recovery Protocol для пропущенных сессий (из BACKLOG.md + GTD Coach)
**Что:** Уже есть в BACKLOG.md как идея. Формализовать 4 варианта:
1. **Reschedule** — конкретное время, не "потом"
2. **Catch-up Mini-Session** — 15 мин, 3 вопроса
3. **Skip with Reflection** — записать причину, отслеживать паттерн
4. **Recovery Protocol (2+ пропуска)** — Emotional Landing → Wheel of Life → 1 приоритет

**Куда вписать:** Новый файл `references/recovery_protocol.md`.

**Оценка:** 4–5 часов.

---

#### 3.12 Structured Growth Report (из Composio developer-growth-analysis)
**Что:** Шаблон для любого периодического обзора:
```markdown
# Обзор [период] — [Домен]

## Резюме
[2–3 абзаца]

## Зоны роста (приоритизированы)
### 1. [Название]
**Почему важно**: ...
**Что наблюдаю**: [на основании данных]
**Рекомендация**: [конкретный шаг]

## Наблюдаемые силы
## Действия
## Рекомендуемые ресурсы
```

**Куда вписать:** Новый файл `references/growth_report_template.md`.

**Оценка:** 2–3 часа.

---

#### 3.13 Energy-Based Scheduling в календаре (из Weekly Planning)
**Что:** При создании событий в календаре — учитывать энергию:
- Высокая энергия → творческие/Deep Work блоки
- Низкая энергия → рутина, админ, коммуникация
- Пиковые часы → защитить фокус-блоками

**Куда вписать:** `references/calendar_constants.md` — раздел "Energy-Based Time Blocking".

**Оценка:** 2–3 часа.

---

#### 3.14 Calendar Event Copy Review (из BACKLOG.md)
**Что:** Переписать все тексты событий календаря:
- Убрать "надо/должен"
- Добавить мотивирующий контекст ("почему это важно для тебя")
- Персонализировать под домен Wheel of Life
- Добавить reminder-тексты с поддержкой

**Куда вписать:** Обновить `references/calendar_constants.md`.

**Оценка:** 3–4 часа.

---

### Долгосрочные (v0.9.0+) — высокая сложность, стратегический эффект

#### 3.15 Модульная архитектура плагинов (из Rachnog)
**Что:** Разделить SKILL.md на независимые модули:
```
plugins/
├── core/                 # Wheel of Life, Authentic Goal Filter, Communication Style
├── emotional/            # Emotional Regulation, Energy Check
├── execution/            # Task Breakdown, Weekly Review, Daily Top-3
├── habits/               # Habit Loop, Streak Tracking (v0.8.0)
└── calendar/             # Calendar integration, Event Copy
```

Каждый плагин — свой SKILL.md + references. Главный marketplace.json маршрутизирует.

**Куда вписать:** Пересмотр всей архитектуры. Начать с `references/modular_architecture_spec.md`.

**Оценка:** 15–20 часов. Возможно, v0.9.0 или v1.0.

---

#### 3.16 Habitica / Beeminder интеграция (из Composio)
**Что:** Опциональные commitment devices:
- Habitica — gamification: очки за выполнение, streaks, rewards
- Beeminder — финансовые ставки: "$5 если не сделаю 3 тренировки в неделю"

**Куда вписать:** Новый `references/habit_integrations.md`.

**Оценка:** 8–12 часов (требует API-интеграций).

---

#### 3.17 Behavioral Pattern Recognition (из Composio meeting-insights-analyzer)
**Что:** Анализировать текст пользователя на паттерны:
- Когнитивные искажения ("всегда", "никогда", "должен")
- Язык владения vs. язык жертвы
- Энергетические паттерны (когда пропадает мотивация)
- Циклические блокеры

**Куда вписать:** `references/communication_style.md` — раздел "Паттерн-анализ".

**Оценка:** 6–8 часов.

---

#### 3.18 Bidirectional Notion/Obsidian Sync (из Rachnog + Developmental Coach)
**Что:** Не просто сохранять в Notion, а:
- Загружать предыдущие сессии при старте
- Обновлять Wheel of Life scores
- Синхронизировать задачи
- Хранить `notion-id` для идемпотентности

**Куда вписать:** Расширить `calendar_integration/` или создать `integrations/` package.

**Оценка:** 10–15 часов.

---

## 4. Главный стратегический вывод

### Рынок разделился на два слоя:

| Слой | Описание | Ключевые игроки | Что они делают хорошо | Где проваливаются |
|------|----------|-----------------|----------------------|-------------------|
| **Operational** | Ежедневное выполнение, трайаж, автоматизация | Rachnog, Weekly Planning, GTD Coach | Интеграции, скорость, трайаж | Нет ценностей, нет эмоций, нет "почему" |
| **Transformational** | Глубинные изменения, ценности, смысл | Developmental Coach, (мы) | Рефлексия, глубина, психология | Нет execution, нет интеграций |

### Наша позиция: единственные на пересечении

**life-planning-coach** — единственный скилл, который:
1. ✅ Работает со всеми 11 доменами жизни (не только работа/здоровье)
2. ✅ Использует evidence-based психологию (TTM, MI, WOOP)
3. ✅ Проверяет подлинность целей (Authentic Goal Filter)
4. ✅ Адаптирует стиль под эмоциональное состояние (Communication Style)
5. ✅ Имеет календарную интеграцию (Python package)
6. ✅ Соблюдает professional boundaries (therapy disclaimer, AC)
7. ❌ **НЕ имеет сильного execution layer** — это главный пробел
8. ❌ **НЕ имеет массовых MCP-интеграций** — второй пробел

### Стратегическая рекомендация: "Coaching-First OS"

Не пытаться догнать Rachnog в интеграциях или Weekly Planning в скорости.
**Стать операционной системью, которая начинается с coaching и заканчивается execution.**

```
Пользователь входит → Coaching Layer (ценности, цели, эмоции)
                        ↓
                  Planning Layer (WOOP, Wheel of Life, приоритеты)
                        ↓
                  Execution Layer (задачи, календарь, привычки, ревью)
                        ↓
                  Reflection Layer (мета-рефлексия, инсайты, обзоры)
                        ↓
                  (цикл повторяется)
```

Каждый слой — опциональный. Пользователь может:
- Зайти только за Daily Top-3 → Execution Layer
- Зайти за Deep Why → Coaching Layer
- Зайти за Weekly Review → Reflection + Planning + Execution

**Это невозможно ни у одного конкурента.** Rachnog — execution-only с отсутствием духовности/вклада. Developmental Coach — coaching-only без календаря. Weekly Planning — execution-only без ценностей.

---

## 5. Приоритизированный бэклог "заимствований"

| Приоритет | Фича | Источник | Расчётное время | Версия |
|-----------|------|----------|-----------------|--------|
| P0 | Markdown-таблицы как UI | GTD Coach + PM OKR | 2–3 ч | v0.7.1 |
| P0 | Status Icon System | GTD Coach | 1 ч | v0.7.1 |
| P0 | Clarifying-Questions-First | Composio | 1 ч | v0.7.1 |
| P1 | Таксономия слабых целей | PM OKR | 3–4 ч | v0.8.0 |
| P1 | Structured Session Summary | Developmental Coach | 1–2 ч | v0.8.0 |
| P1 | Win Alert pattern | GTD Coach | 1–2 ч | v0.8.0 |
| P1 | Recovery Protocol | BACKLOG + GTD Coach | 4–5 ч | v0.8.0 |
| P1 | Calendar Event Copy Review | BACKLOG | 3–4 ч | v0.8.0 |
| P2 | Task Breakdown с чекпоинтами | GTD Coach | 3–4 ч | v0.8.0 |
| P2 | Auto-Review Triggers | GTD Coach | 2–3 ч | v0.8.0 |
| P2 | Adaptive Response Length | Developmental Coach | 1–2 ч | v0.8.0 |
| P2 | Structured Growth Report | Composio | 2–3 ч | v0.8.0 |
| P2 | Energy-Based Scheduling | Weekly Planning | 2–3 ч | v0.8.0 |
| P3 | Модульная архитектура | Rachnog | 15–20 ч | v0.9.0+ |
| P3 | Habitica/Beeminder | Composio | 8–12 ч | v0.9.0+ |
| P3 | Bidirectional Notion Sync | Rachnog + Developmental Coach | 10–15 ч | v0.9.0+ |
| P3 | Behavioral Pattern Recognition | Composio | 6–8 ч | v0.9.0+ |

---

## 6. Риски и анти-паттерны (чего НЕ брать)

| Анти-паттерн | Откуда | Почему не брать |
|-------------|--------|-----------------|
| **Single-Goal Focus** | GTD Coach | Противоречит 11-доменной философии |
| **Memory-only persistence** | GTD Coach | Если память Claude сбросится — прогресс потерян. Нужен fallback (файл/Notion/Calendar) |
| **Browser automation** | Rachnog | Хрупко, CAPTCHA, UI-изменения. Использовать только API/MCP |
| **Hard-coded personal context** | Rachnog | Невозможно переиспользовать без кастомизации |
| **Apple Shortcuts dependency** | Rachnog | Только macOS, хрупко |
| **Execution-only без coaching** | Weekly Planning | Это не наш путь; но можно предложить как опциональный модуль |
| **Esoteric/mystical content** | Ordinary Skills | Противоречит evidence-based подходу |
| **Over-automation** | Composio Rube | Скилл не должен действовать от имени пользователя без explicit approval |

---

*Составлено: 2026-05-17*
*Источники: 7 конкурентных репозиториев, веб-поиск, анализ 1459+ скиллов*
