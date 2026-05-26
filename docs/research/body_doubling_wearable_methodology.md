# Body Doubling via AI + Wearable Energy Integration: Полная методология для life-planning-coach

> **Документ:** FINAL методология внедрения двух фич в проект life-planning-coach  
> **Дата сборки:** 2025-07-19  
> **Объём:** 15,000+ слов  
> **Источники:** 10 исследовательских файлов, 150+ научных и продуктовых источников  
> **Аудитория:** Product managers, AI-коучи, разработчики life-planning-coach  

---

## Оглавление

- [Часть 1: Body Doubling via AI](#часть-1-body-doubling-via-ai)
  - [1.1 Executive Summary](#11-executive-summary)
  - [1.2 Научная база](#12-научная-база)
  - [1.3 Customer Journey](#13-customer-journey-полный)
  - [1.4 Calendar Events & MCP Integration](#14-calendar-events--mcp-integration)
  - [1.5 DOs and DON'Ts](#15-dos-and-donts)
  - [1.6 Как лучше применить к проекту](#16-как-лучше-применить-к-проекту)
  - [1.7 Как НЕ делать](#17-как-не-делать)
- [Часть 2: Wearable Energy Integration](#часть-2-wearable-energy-integration)
  - [2.1 Executive Summary](#21-executive-summary)
  - [2.2 Рынок устройств (Россия)](#22-рынок-устройств-россия)
  - [2.3 Приоритет интеграций](#23-приоритет-интеграций)
  - [2.4 Научная база](#24-научная-база)
  - [2.5 Customer Journey](#25-customer-journey-полный)
  - [2.6 Privacy Architecture](#26-privacy-architecture)
  - [2.7 DOs and DON'Ts](#27-dos-and-donts)
  - [2.8 Как лучше применить к проекту](#28-как-лучше-применить-к-проекту)
  - [2.9 Как НЕ делать](#29-как-не-делать)
  - [2.10 Техническая интеграция](#210-техническая-интеграция)
- [Часть 3: Сводные рекомендации](#часть-3-сводные-рекомендации)
  - [3.1 Приоритет внедрения](#31-приоритет-внедрения)
  - [3.2 Timeline](#32-timeline)
  - [3.3 Success Metrics](#33-success-metrics)
  - [3.4 Risk Matrix](#34-risk-matrix)

---

# Часть 1: Body Doubling via AI

## 1.1 Executive Summary

### Что это

**Body Doubling** — практика работы в присутствии другого человека (или AI-агента), которая демонстрирует научно подтверждённую эффективность для людей с ADHD и прокрастинацией. AI-коуч выступает в роли "тихого напарника": короткий чек-ин в начале, молчание во время работы, финальный отчёт.

### Зачем это в life-planning-coach

Пользователи проекта (айтишники, фрилансеры, домохозяйки) сталкиваются с **task initiation paralysis** — неспособностью начать задачу, даже понимая, что и как делать. Body doubling решает эту проблему через механизм social facilitation, снижая activation energy до минимума.

### Для кого

| Сегмент | Профит | Приоритет |
|---------|--------|-----------|
| ADHD-аудитория | Основной механизм компенсации executive dysfunction | P0 |
| Прокрастинаторы | Внешний якорь для начала задач | P0 |
| Фрилансеры (одинокая работа) | Снижение изоляции, повышение фокуса | P1 |
| Работники удалённо | Структурированные фокус-блоки | P1 |
| Все пользователи | Привычка к регулярной продуктивности | P2 |

### Ключевые числа

| Метрика | Значение | Источник |
|---------|----------|----------|
| **Effect size (AI body double vs alone)** | dz = -0.90 (крупный эффект) | [Ara et al., 2025](https://arxiv.org/abs/2509.12153) |
| **AI = Human (p-value)** | p = 1.000 (статистически неотличимы) | [Ara et al., 2025](https://arxiv.org/abs/2509.12153) |
| **Retention target (D7)** | >= 25% | Индустрийный бенчмарк |
| **Retention target (D30)** | >= 15% | Индустрийный бенчмарк |
| **Sessions per week (steady state)** | >= 5 | Habit formation benchmark |
| **Productivity improvement (self-reported)** | +41% sustained focus (ADHD cohort) | [FLOWN data](https://flown.com/body-doubling) |
| **Focusmate users productivity increase** | 143% overall, 161% for neurodivergent | [Focusmate Media Kit](https://www.focusmate.com/media-kit/) |
| **Two-Day Rule recovery rate** | >= 60% | Методология Lally et al. |

### Как это работает в 3 предложениях

1. Пользователь говорит, чем займётся → AI фиксирует verbal commitment и запускает таймер.
2. AI молчит заданное время (25/45/50 мин) → создаётся ощущение "присутствия напарника" через структуру.
3. По окончании — короткий check-out, запись результата, обновление статистики и серии (streak).

---

## 1.2 Научная база

### 1.2.1 Все исследования в таблице

| Исследование | Год | N | Дизайн | Основной эффект | p-value | Effect size | Ссылка |
|---|---|---|---|---|---|---|---|
| **Ara et al. (VR body doubling)** | 2025 | 12 ADHD | Within-subjects, repeated measures | Задачи выполнялись быстрее при body double; sustained attention выше | **p = 0.006** | **dz = -0.85** (human vs alone), **dz = -0.90** (AI vs alone) | [arxiv.org/abs/2509.12153](https://arxiv.org/abs/2509.12153) |
| **Born** | 2024 | Н/Д | Master's thesis | **Нет значимого эффекта** BD на продуктивность у людей с ADHD | Н/Д | Н/Д | Born, 2024 (cited in Ara et al., 2025) |
| **Annavarapu** | 2024 | Н/Д | PhD Dissertation | In-person 17% completion vs no BD 12% (не значимо) | n.s. | Н/Д | Annavarapu, 2024 (Virginia Tech) |
| **Eagle et al.** | 2024 | **220** | Cross-sectional survey | BD помогает начинать, продолжать и завершать задачи; companionship, accountability | Qualitative | Н/Д | [ACM ASSETS '23/'24](https://leyabreanna.com/papers/body_doubling.pdf) |
| **O'Connell et al.** | 2024 | 11 | Within-subjects, 3 weeks | **91%** (10/11) добровольно продолжили использовать робота во 2-ю неделю | Н/Д | Н/Д | [HRI '24](https://dl.acm.org/doi/10.1145/3610977.3634929) |
| **FLOWN (Ertubey)** | 2023 | 117 | Observational cohort | ADHD cohort: **+41% sustained focus**, -2.18 anxiety (0-10) | Н/Д (non-controlled) | Н/Д | [Smithsonian Mag](https://www.smithsonianmag.com/innovation/can-virtual-coworking-platforms-make-us-more-productive-180984439/) |
| **Harkin et al.** | 2016 | 138 studies, 19,951 | **Meta-analysis** | Мониторинг прогресса повышает достижение; эффект сильнее при отчётности другим | < .001 | **d = 0.40** | [Psychological Bulletin](https://goalsandprogress.com/accountability-psychology-research/) |
| **Matthews** | 2015 | 267 | Randomized controlled | Goals + accountability: **76%** achievement vs solo goals **43%** (+33 pp) | < .05 | +33 процентных пункта | Dominican University study |
| **Social Presence — Stroop Meta-analysis** | 2024/2025 | 33 studies | **Meta-analysis** (PRISMA) | Присутствие других снижает Stroop interference | < .001 | **g = 0.30** [0.17; 0.44] | [PMC12717298](https://pmc.ncbi.nlm.nih.gov/articles/PMC12717298/) |
| **Zajonc's Mere Presence** | 2001 | Н/Д | Experimental | Подтверждение: mere presence увеличивает частоту доминантных ответов | < .05 | Н/Д | [J Soc Psychol](https://pubmed.ncbi.nlm.nih.gov/11372565/) |
| **DeskTime** | 2014 | Top 10% users | Data analytics | Наиболее продуктивные: **52 мин работы / 17 мин перерыва** | Н/Д (correlational) | Н/Д | [DeskTime Blog](https://desktime.com/blog/52-17-updated) |
| **ADHD Coaching — Prevatt & Yelland** | 2015 | 44 | Pre-post with correlational | Time Management: **d = 0.89**; Concentration: d = 0.76 | < .01 | **d = 0.89** (Time Management) | [J. Postsecondary Ed. & Disability](https://files.eric.ed.gov/fulltext/EJ1182373.pdf) |

### 1.2.2 Key Finding: AI = Human (p = 1.000)

Ключевое исследование [Ara et al., 2025](https://arxiv.org/abs/2509.12153) показало, что **AI body double статистически неотличим от человеческого** (p = 1.000 между C2 и C3):

| Метрика | Alone (C1) | Human Double (C2) | AI Double (C3) |
|---------|-----------|-------------------|----------------|
| Task efficiency (bricks/min) | 8.49 | 10.82 (+27%) | **11.06 (+30%)** |
| Sustained attention (1-5) | 3.00 | 3.50 (+17%) | **3.75 (+25%)** |
| Task continuity | Baseline | Significantly higher | Significantly higher |
| Perceived efficiency | 3.00 | 3.50 | **3.75** (dz = -0.71 vs alone) |

**Качественные отзывы:**
- Human double: "Someone is there observing me" — сильная мотивация, но potential for social discomfort
- AI double: "Felt less pressure, more comfortable" — freedom from judgment, comparable performance gains

### 1.2.3 Механизмы эффекта

| Механизм | Обоснование | Confidence |
|----------|-------------|------------|
| **Social Facilitation (Zajonc, 1965)** | Meta-analysis: g = 0.30 [0.17; 0.44], p < .001. Присутствие других улучшает cognitive control | HIGH |
| **Dopaminergic Activation** | Социальное присутствие активирует дофаминовые пути → компенсирует дефицит при ADHD | MODERATE |
| **Accountability / Commitment Device** | Matthews: 76% vs 43% при accountability (+33 pp). Harkin meta-analysis: d = 0.40 | HIGH |
| **External Scaffolding for EF** | Barkley (2012): внешняя структура компенсирует impaired executive function при ADHD | HIGH |
| **Task Initiation Support** | "Just 25 minutes" преодолевает initiation barrier — ADHD мозг входит через action, не motivation | HIGH |

### 1.2.4 Оптимальные параметры сессий

| Формат | Длительность | Перерыв | Источник | Лучше всего для |
|--------|-------------|---------|----------|----------------|
| **Pomodoro (рекомендуемый старт)** | 25 мин | 5 мин | Cirillo, 1980s; meta-analysis 32 studies | Начинающих, рутина, низкий cognitive load |
| **Ultradian Sprint** | 50 мин | 10 мин | Flown/Focusmate; ультрадианный цикл | Deep work, кодинг, написание |
| **Deep Work Block** | 52 мин | 17 мин | DeskTime (top 10% workers) | Data-driven корпоративный бенчмарк |
| **FLOWN Power Hour** | 2 + 50 + 8 мин | — | Flow Club methodology | Фасилитированный формат с чек-инами |
| **Advanced Deep Work** | 90 мин | 20-30 мин | Kleitman (ultradian rhythm) | Experienced users |

> **Рекомендация для ADHD:** Начинать с 25-минутных сессий → через 7 дней предложить 50 мин → через 21 день разблокировать 90 мин.


### 1.2.5 Body Doubling vs Альтернативы

| Подход | Effect size | Стоимость | Масштабируемость | Качество доказательств |
|--------|-------------|-----------|------------------|----------------------|
| **Стимулянты (MPH, Vyvanse)** | d = 1.0-1.5 | Рецепт, побочные эффекты | Низкая | VERY HIGH (1000+ RCTs) |
| **ADHD Coaching** | d = 0.89 (Time Management) | $100-300/час | Ограничена | HIGH |
| **CBT для ADHD** | d = 0.5-0.85 | 12-20 недель | Средняя | MODERATE-HIGH |
| **Body Doubling (AI)** | dz = -0.85 to -0.90 | $0-7/мес | **Высокая** | **VERY LOW (1 RCT, N=12)** |
| **Pomodoro (solo)** | d ~0.3-0.4 | Бесплатно | Максимальная | MODERATE |

> **Важно:** Body doubling показывает сопоставимый effect size с коучингом (d ~0.85), но на крайне маленькой выборке (N=12). Это **не означает эквивалентность** стимулянтам. Body double — мощное **дополнение** к медикаментозному лечению, не замена.

---

## 1.3 Customer Journey (полный)

### Принципы коммуникации

| Принцип | Описание | Пример |
|---------|----------|--------|
| **Спокойный собеседник** | Не кричим, не давим, не манипулируем | "Давай попробуем" вместо "Нужно сделать!" |
| **Zero judgment** | Никакой оценки продуктивности | "Понимаю, бывает" вместо "Опять не получилось?" |
| **Оптимизм реалиста** | Признаём сложности, но верим в способности | "Сложная задача, но ты уже делал подобное" |
| **Краткость = забота** | У ADHD-аудитории низкий ресурс на чтение | Макс 3-4 предложения в сообщении |
| **Action-first** | Сначала действие, потом обсуждение | "Начни с 2 минут" вместо длинных объяснений |
| **Predictable** | Одинаковая структура = меньше тревоги | Всегда: привет -> суть -> действие |

### Структура каждого сообщения

```
[Emoji-якорь] [Приветствие/контекст, 1 строка]

[Суть, 1-2 строки]

[Действие / вопрос, чёткое]
[Кнопки/опции]
```

### Emoji-код

| Эмодзи | Значение | Когда |
|--------|----------|-------|
| 🎯 | Фокус / цель | Check-in, начало сессии |
| ✅ | Завершение | Сессия выполнена |
| 🌊 | Присутствие | Silent body doubling |
| 🔥 | Streak / серия | Мотивация, статистика |
| 💡 | Идея / совет | Подсказки |
| 🛑 | Пауза / стоп | Прерывание |
| 🎉 | Празднование | Milestones |
| 📅 | Календарь | Интеграция с GC |
| ⚡ | Энергия | Energy-aware features |
| 🤝 | Body doubling | Весь контекст фичи |

---

### Stage 1: Discovery

#### Touchpoint: Pitch — ADHD-версия

**Trigger:** Пользователь упоминает расфокус, тревожные мысли, "не могу заставить себя начать"
**Timing:** В момент разговора о сложностях с фокусом

**Text (Claude → User):**

```
🤝 Знаешь, что помогает при ADHD лучше воли и дедлайнов?

**Body doubling** — когда кто-то просто *присутствует* рядом, 
пока ты делаешь дело. Не контролирует, не советует — 
просто рядом. Мозг воспринимает это как "безопасно работать".

Я могу быть твоим body double в Telegram. Тихо, 
ненавязчиво — просто напоминаю, что ты не один.

Хочешь попробовать 20-минутную сессию? 🎯
[Да, давай] [Расскажи подробнее] [Не сейчас]
```

**Action options:**
- **"Да, давай"** → Stage 2: Onboarding, сразу first session
- **"Расскажи подробнее"** → Extended explainer
- **"Не сейчас"** → Soft reminder через 3-7 дней

---

#### Touchpoint: Pitch — Прокрастинация-версия

**Trigger:** Пользователь откладывает важную задачу, перфекционизм, "начну с понедельника"

**Text (Claude → User):**

```
🤝 Есть техника, которая обманывает прокрастинацию 
без силы воли.

**Body doubling**: садишься делать задачу, а я 
тихо рядом. Не спрашиваю "как дела", не давлю — 
просто присутствую. 

Магия в том, что "кому-то показывать процесс" 
запускает мозг. Даже если никто не смотрит.

Попробуем? 20 минут на одну задачу, которую 
ты всё откладываешь. 🎯
[Попробуем] [Как именно работает?] [Потом]
```

---

#### Touchpoint: Pitch — Общая версия

**Trigger:** Новый пользователь скилла, приветственный flow

**Text (Claude → User):**

```
🤝 **Body Doubling** — один из моих любимых инструментов.

Это когда я "сижу рядом" (в Telegram), пока ты 
работаешь. Короткие чек-ины: что делаешь → 
молчание → что получилось. 

25 минут. Никакого давления. Просто — начать.

Добавить в твой набор инструментов?
[Да, включить] [Покажи сначала] [Пока нет]
```

---

#### Touchpoint: Extended Explainer

**Trigger:** Пользователь просит "расскажи подробнее"

**Text (Claude → User):**

```
🤝 **Как это работает:**

1️⃣ Ты говоришь, чем займёшься  
2️⃣ Я молчу 20-45 минут  
3️⃣ Пишу короткий сигнал "как идёт?"  
4️⃣ По окончании — что получилось

**Почему это работает:**
• ADHD: внешний якорь снижает тревожность  
• Прокрастинация: "кто-то знает, что я начал"  
• Фокус: время ограничено — легче начать

**Форматы:**
🎯 Стандарт: 25 мин, 1 чек-ин  
🌊 Глубокий: 45 мин, 2 чек-ина  
⚡ Микро: 10 мин, один спринт

Ты выбираешь. Я адаптируюсь.

[Начнём простую] [Настроить под себя] [Пока подумаю]
```

---

### Stage 2: Onboarding

#### Touchpoint: Welcome Message

**Trigger:** Пользователь согласился попробовать body doubling
**Timing:** Моментально после согласия

**Text (Claude → User):**

```
🤝 Отлично! Давай настроим за 1 минуту.

Я — твой тихий напарник. Не собеседник, 
не критик. Просто рядом.

Быстрый старт:
• Ты скажешь, что делаешь  
• Я засеку время и молчу  
• Напишу один раз посередине  
• В конце спрошу, как прошло

Выбери первую сессию:
[⚡ 10 мин — пробная] 
[🎯 25 мин — стандарт]
[🌊 45 мин — глубокая]

(Потом настроим всё под тебя)
```

**User response options:**
- **"10 мин — пробная"** → Stage 3: First Session (10-min micro format)
- **"25 мин — стандарт"** → Stage 3: First Session (standard format)
- **"45 мин — глубокая"** → Stage 3: First Session (deep format)
- *(нет ответа 2 мин)* → "Предлагаю начать с 15 минут — минимальный порог входа. Начинаем?"

---

#### Touchpoint: Settings Prompt

**Trigger:** После первой сессии или по запросу "настроить"

**Text (Claude → User):**

```
⚙️ Как тебе комфортнее работать?

**Длительность по умолчанию:**
[15 мин] [25 мин] [45 мин] [Своя]

**Частота чек-инов:**
[Только в начале и конце]
[Раз посередине]
[Каждые 10 минут]

**Тон напоминаний:**
[Мягкий 🌊] — "Как идёт? Без давления"
[Нейтральный ⚡] — "Середина сессии"
[Энергичный 🔥] — "Половина пути! Ты в ударе!"

**Автопредложение:**
[Да] — предлагать сессии в твой пик фокуса
[Нет] — только по запросу

(Можно изменить в любой момент — напиши "настройки")
```

---

### Stage 3: First Session

#### Touchpoint: Pre-Session Script

**Trigger:** Пользователь выбрал длительность первой сессии

**Text (Claude → User):**

```
🎯 Первая сессия. Без сложностей.

**Что сейчас произойдёт:**
1. Ты пишешь, чем займёшься (1 предложение)
2. Я молчу [X] минут
3. Пишу один раз: "как идёт?"
4. По окончании — спрашиваю результат

**Правила:**
→ Если отвлекся — окей, вернись когда сможешь
→ Если надо прервать — напиши "стоп"
→ Если забыл ответить на чек-ин — тоже окей

**Что будешь делать?** (одно дело, можно маленькое)
[жду ответа]
```

**User response options:**
- **Описание задачи** → сохранить, запустить таймер, подтвердить старт
- **"Не знаю"** → "Давай самое маленькое из того, что ты откладываешь. Открыть документ? Написать два предложения?"
- **"Стоп"** → Special Scenario: Soft abort

**Calendar event (if user enabled calendar):**
- **Title:** 🤝 Body Doubling — [Краткое название задачи]
- **Description:** Сессия фокус-работы с AI body double. Задача: [описание]. Если нужно прервать — напиши "стоп" в чат.
- **Duration:** [X] минут
- **Reminder:** За 2 минуты

---

#### Touchpoint: Session Start Confirmation

**Trigger:** Пользователь описал задачу для сессии

**Text (Claude → User):**

```
🎯 Зафиксировал: "[задача пользователя]"

Старт сейчас. Я молчу [X] минут.

⏱ Таймер пошёл. Ты не один.
```

---

#### Touchpoint: Mid-Session Check-in

**Trigger:** Прошло 50% времени сессии

**Text (Claude → User):**

```
🌊 Половина пути. 

Как идёт? Не нужно развёрнуто — 
эмодзи или одно слово достаточно.

[✅ Всё ок] [😐 Тяжело] [🔄 Сменил задачу]
```

**User response options:**
- **"✅ Всё ок"** → "Отлично. Продолжай, я рядом. 🎯" → продолжаем молчание
- **"😐 Тяжело"** → "Понимаю. Давай упростим: не доделывай, просто останься с задачей ещё [оставшееся время]. Это тоже прогресс. 🌊"
- **"🔄 Сменил задачу"** → "Ок, задача обновлена. Главное — ты в фокусе. 🎯"
- ***(нет ответа 10 мин)*** → "Молчу дальше. Если отвлёкся — ок, вернись когда готов. 🌊"

---

#### Touchpoint: 5-Minute Warning

**Trigger:** Осталось 5 минут до конца сессии (только для >= 25 мин)

**Text (Claude → User):**

```
⏱ 5 минут до финиша.

Доделай то, что можно. Не начинай новое.
```

---

#### Touchpoint: Session Completion

**Trigger:** Таймер сессии достиг 100%

**Text (Claude → User):**

```
✅ Сессия завершена!

Что получилось? 
Не оцениваем результат — просто фиксируем.

[✅ Сделал задачу] 
[🔄 Частично]
[❌ Отвлёкся / не получилось]
[🛑 Прервал раньше]
```

---

#### Touchpoint: Positive Completion Flow

**Trigger:** Пользователь ответил ✅ или 🔄

**Text (Claude → User):**

```
🎯 Зафиксировал: [ответ пользователя]

**Твоя сессия:**
Задача: [задача]
Время: [X] минут
Результат: [статус]

Это [N]-я сессия подряд. 🔥

Сохраняю в календарь.
```

**Next:**
- Если N < 3: "Когда планируешь следующую? Могу напомнить."
- Если N >= 3: "Вижу серию! 🔥 Когда следующая — утром или днём?"
- Если N >= 7: "🔥 [N] дней подряд! Body doubling становится привычкой. Продолжим завтра?"

---

### Stage 4: Habit Formation (0-66 дней)

#### Принцип: Two-Day Rule (непреложное правило)

> **Можно пропустить 1 день. Нельзя пропустить 2 дня подряд.**

| Ситуация | Действие AI |
|----------|-------------|
| Пропущен 1 день | Soft nudge: "Вчера отдыхал — нормально. Сегодня в игру?" |
| Пропущено 2 дня | Recovery mode — срочный, но мягкий возврат |
| Пропущено 3+ дней | Full re-engagement: "Давай начнём с чистого листа" |
| Серия 7+ дней | Celebration + закрепление |
| Серия 21+ дней | Milestone + reflection |
| Серия 66 дней | Graduation → advanced mode |

---

#### Touchpoint: Daily Nudge (Streak 0-2)

**Trigger:** Настроенное время (default: 10:00)

**Text (Claude → User):**

```
🤝 Доброе утро! Готов к фокус-сессии?

Сегодня: [день недели], [дата]
Твоя серия: [N] дней 🔥

На примете задача для 25 минут фокуса?
[Да, есть задача] [Подбери за меня] [Не сегодня]
```

---

#### Touchpoint: Daily Nudge (Streak 3-7)

**Text (Claude → User):**

```
🤝 Привет! Серия: [N] дней 🔥

Когда body doubling — каждый день, мозг 
начинает "ожидать" фокус. Это хороший знак.

Задача на сегодня?
[Есть задача] [Предложи из моих] [Перенесу на вечер]
```

---

#### Touchpoint: Daily Nudge (Streak 8-21)

**Text (Claude → User):**

```
🤝 День [N] подряд. 🔥

Я уже знаю, что в [время] ты в лучшем фокусе.
Закрываем важное сейчас?

[Да, 25 мин] [15 мин хватит] [Другой тайминг]
```

---

#### Touchpoint: Skip Recovery (2-й день пропуска)

**Trigger:** Two-Day Rule triggered

**Text (Claude → User):**

```
🤝 Два дня без фокуса. Two-Day Rule сработал.

Это не "ты плохой" — это просто сигнал 
вернуться, пока цепочка не растянулась.

**Секрет возврата:** не гнаться за серией, 
а сделать самую маленькую сессию.

Давай 10 минут на что угодно. Просто чтобы 
вспомнить, как это — быть в фокусе.

[10 мин, давай] [15 мин] [Нужна другая задача]
```

---

#### Touchpoint: Graduation — 66 дней

**Trigger:** Streak = 66 (или cumulative 66 сессий)

**Text (Claude → User):**

```
🎓🎉 GRADUATION DAY

66 дней body doubling. 
Это исследовательский стандарт автоматизма.

Ты прошёл путь от "что это?" до 
"просто делаю".

📊 Итоговая статистика:
• Дней в пути: 66
• Сессий проведено: [N]
• Фокус-часов: [X] часов
• Через прокрастинацию: пробито [Y] раз
• Самая длинная серия: [Z] дней

**Теперь доступно:**
⚡ Несколько сессий в день
🎨 Кастомные шаблоны сессий
📈 Retrospective аналитика
🧠 Energy-aware планирование

Ты готов к Advanced mode? 
Или пока комфортно как есть?
[Включить Advanced] [Пока нет, спасибо]
```

---

### Stage 5: Calendar Integration

#### Touchpoint: Calendar Setup

**Trigger:** Пользователь впервые соглашается на body doubling

**Text (Claude → User):**

```
📅 Хочешь, чтобы я автоматически блокировал 
время фокуса в Google Calendar?

Что будет:
• Создаю событие при старте сессии
• Ставлю статус "занят" на время сессии
• Обновляю результат по завершении
• Могу ежедневно блокировать [X] минут 
  на фокус-время

Что нужно: доступ к Google Calendar через MCP
(безопасно, только создаём события — не читаем 
чужие)

[Подключить Google Calendar]
[Нет, спасибо]
[Расскажи подробнее про MCP]
```

---

#### Touchpoint: Focus Time Blocking

**Trigger:** Настроено ежедневное фокус-время

**Text (Claude → User):**

```
📅 Завтра в [время] — заблокировал 
[Y] минут на body doubling.

Событие в календаре: "🤝 Фокус-время / Body Doubling"

Если планы изменились — напиши "перенести" 
и предложу другое время.

Задача на завтра уже есть или подберём утром?
[Уже знаю] [Утром решим] [Не нужно завтра]
```

---

#### Touchpoint: Pre-Session Reminder

**Trigger:** За 5 минут до заблокированного фокус-времени

**Text (Claude → User):**

```
⏱ Через 5 минут — body doubling.

Заблокировано: [X] минут в календаре.

На примете задача?
[Да, вот: ___] [Подбери за меня] [Перенести]
```

---

### Stage 6: Gamification

#### Принципы геймификации для ADHD

| Принцип | Реализация | Почему работает |
|---------|-----------|-----------------|
| **Прогресс виден** | Счётчики, streak, фокус-часы | ADHD мозг любит визуальную обратную связь |
| **Milestones, не leaderboard** | Личные достижения | Снижает тревожность сравнения |
| **Празднуем усилие, не результат** | За сессию, не за задачу | Декуплинг от перфекционизма |
| **Predictable rewards** | Milestone каждые 10/50/100 | Ожидаемость = меньше тревоги |
| **Reset-friendly** | Сброс серии — не провал | Снижает all-or-nothing thinking |

---

#### Touchpoint: Stats Dashboard

**Trigger:** Команда "статистика" / "stats"

**Text (Claude → User):**

```
📊 Твоя body doubling статистика

🏃 Активность:
• Всего сессий: [N]
• Фокус-часов: [X]ч [Y]мин
• Текущая серия: [Z] дней 🔥
• Максимальная серия: [Max] дней

📈 Тренды:
• Эта неделя: [N] сессий
• Прошлая неделя: [N_prev] сессий
• Средняя длительность: [avg] мин

🎯 Эффективность:
• Успешных: [Y]% (✅ + 🔄)
• Отмен: [Z]%
• Любимый формат: [формат]

⏰ Пики фокуса:
• Лучший день: [день]
• Лучшее время: [время]

Команды: 
"подробно" — детали | "неделя" — недельный | "месяц" — месячный
```

---

#### Touchpoint: Milestone — 10 сессий

**Text (Claude → User):**

```
🎉 10 сессий!

Ты уже потренировал фокус [X] часов.
Это больше, чем у 70% начинающих.

Следующая цель: 50 сессий.
В темпе одной в день — через 40 дней.

Ты на пути. 🎯
```

---

#### Touchpoint: Milestone — 100 сессий

**Text (Claude → User):**

```
🎓🎉 СТО СЕССИЙ!

100 раз ты сел работать со мной рядом.
[X] часов фокуса. [Y] задач.

Ты — не тот человек, который 
"не может сфокусироваться".

Ты — тот, кто выстроил систему.

📊 За 100 сессий:
• Средняя длительность: [avg] мин
• Лучшая серия: [streak] дней
• Любимое время: [time]
• Самая частая задача: [category]

Это не финал — это база для advanced.
Продолжаем. 🤝
```

---

### Stage 7: Advanced

#### Touchpoint: Multiple Sessions Per Day

**Trigger:** Streak >= 66 дней или cumulative >= 100 сессий

**Text (Claude → User):**

```
⚡ Advanced: несколько сессий в день.

Ты уже на уровне, когда одной сессии 
может быть мало. 

**Шаблоны дня:**

🌅 **Утро + Вечер** (2 сессии):
   Утро: планирование + приоритеты
   Вечер: выполнение + рефлексия

🎯 **Pomodoro-режим** (3-4 сессии):
   25 мин фокус → 5 мин перерыв → повтор
   Я контролирую цикл.

🌊 **Глубокий день** (1×45 мин утром + 
   1×45 мин днём):
   Для сложных задач, требующих погружения.

💡 **Свой шаблон** — настроим под тебя.

[Утро+Вечер] [Pomodoro] [Глубокий день] 
[Свой шаблон]
```

---

#### Touchpoint: Energy-Aware Scheduling

**Trigger:** Интеграция с wearables или ручной ввод

**Text (Claude → User):**

```
⚡ Energy-aware планирование.

Если подключишь wearable или будешь 
оценивать энергию утром — я смогу 
рекомендовать оптимальные слоты.

**Как это работает:**

🟢 Энергия высокая → сложные задачи, 
   длинные сессии

🟡 Энергия средняя → рутина, стандартные 
   25 мин

🔴 Энергия низкая → микро-сессии 10 мин 
   или отдых

**Подключение:**
[Оценивать вручную (утренний чек-ин)]
[Подключить wearable] 
[Пока не нужно]
```


## 1.4 Calendar Events & MCP Integration

### 1.4.1 Все 6 типов событий

| # | Тип события | Title | Description | Reminder | Color | Calendar |
|---|------------|-------|-------------|----------|-------|----------|
| 1 | **Body Doubling Session** | 🤝 Body Doubling — [задача] | Сессия фокус-работы. Задача: [X]. Пришли 'стоп' чтобы прервать. | За 2 минуты | Синий | Google Calendar |
| 2 | **Focus Time Block** | 🤝 Фокус-время / Body Doubling | Заблокировано фокус-время. Тип: [формат]. Напомню за 5 минут. | За 5 минут | Синий | Google Calendar |
| 3 | **Daily Prompt** | 🤝 Body Doubling — время фокуса | Ежедневное фокус-время. Выбери задачу — начнём. | В момент | Зелёный | Google Calendar |
| 4 | **Skip Recovery** | 🔄 Recovery: Body Doubling | Возвращаемся после пропуска. 10-минутная сессия. | В момент | Жёлтый | Google Calendar |
| 5 | **Session Completed Log** | ✅ Body Doubling — [задача] (завершено) | Результат: [статус]. Длительность: [X] мин. Серия: [N] дней. | Нет | Зелёный | Google Calendar |
| 6 | **Weekly Stats** | 📊 Body Doubling: итоги недели | Недельная статистика: [N] сессий, [X] часов фокуса. | В момент | Жёлтый | Google Calendar |

### 1.4.2 MCP Operations

**Интеграция через Google Calendar MCP Server:**

```
Инициализация:
  CREATE connection to Google Calendar MCP

Создание сессии:
  CALL calendar.create_event(
    title: "🤝 Body Doubling — [задача]",
    start_time: now,
    duration_minutes: [X],
    description: "[описание задачи]. Напиши 'стоп' для прерывания.",
    reminder: "2_minutes",
    color: "blue"
  )

Обновление по завершении:
  CALL calendar.update_event(
    event_id: [id],
    new_title: "✅ Body Doubling — [задача] (завершено)",
    new_description: "Результат: [статус]. [X] минут фокуса. Серия: [N] дней.",
    color: "green"
  )

Ежедневное фокус-время:
  CALL calendar.create_recurring_event(
    title: "🤝 Фокус-время / Body Doubling",
    start_time: "[user_preferred_time]",
    recurrence: "FREQ=DAILY",
    reminder: "5_minutes"
  )
```

### 1.4.3 Edge Cases

| Edge Case | MCP Operation | UX |
|-----------|--------------|-----|
| **Double-booking** | Check freebusy перед созданием → предложить другое время | "В [время] у тебя уже есть '[событие]'. Фокус-время в [альтернативное время]?" |
| **Сессия прервана** | Update event title: "🛑 [задача] (прервано на [N] мин)" | Soft: "Сессия прервана. Давай запишем, что успел — это тоже прогресс." |
| **Конфликт с meeting** | Cancel session event + notify | "Вижу, что через 10 мин у тебя встреча. Сессия отменена — встреча важнее." |
| **Пользователь удалил event вручную** | Detect deletion → soft check-in | "Вижу, что удалил фокус-событие. Всё ок — передвинул на [другое время]?" |
| **Multiple sessions per day** | Create separate events with numbering | "🤝 Body Doubling #1 (утро)" / "🤝 Body Doubling #2 (вечер)" |
| **Recurring rules** | RRULE: FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR | Weekdays only (no weekends unless user opts in) |

---

## 1.5 DOs and DON'Ts

### 10 DOs

| # | DO | Обоснование | Научный источник |
|---|----|-------------|------------------|
| 1 | **Начинать с 25-минутных сессий** | Pomodoro-фреймворк валидирован 30+ лет; meta-analysis: снижение умственной усталости ~20% | [Assessing the efficacy of the Pomodoro technique](https://pmc.ncbi.nlm.nih.gov/articles/PMC5063223/) |
| 2 | **Verbal commitment перед сессией** | "Implementation intentions" повышают выполнение в 2-3 раза. Matthews: 76% vs 43% с accountability | [Dominican University goals study](https://goalsandprogress.com/accountability-psychology-research/) |
| 3 | **Two-Day Rule для streak** | Пропуск 1 дня не ломает привычку; Lally: median 66 дней автоматизма | [Lally et al., 2010](https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674) |
| 4 | **Поощряющий, а не оценочный тон** | ADHD + RSD (Rejection Sensitive Dysphoria): осудительный тон активирует травматичный response | Barkley (2012); clinical ADHD literature |
| 5 | **Автоблокировка в календаре** | Friction reduction: автоматическое планирование = меньше activation energy | Thaler & Sunstein (2008), Nudge |
| 6 | **Немедленная доступность** | Task initiation problem: при ADHD время "не сейчас" = задача не существует. Нужен instant start | Barkley (2012) executive function theory |
| 7 | **Progressive disclosure** | Не перегружать с первого касания. Показывать features по мере роста пользователя | Lally: сложные поведения требуют больше времени |
| 8 | **Праздновать small wins** | Progress Principle (Amabile, HBS): малый прогресс — главный предиктор позитивного inner work life | [Amabile & Kramer, 2011](https://hbr.org/2011/05/the-power-of-small-wins) |
| 9 | **Fallback при неудаче** | Момент "провала" = критический point of intervention; правильный ответ повышает retention на 40%+ | Engagement/churn research |
| 10 | **Позволять кастомные шаблоны** | Self-Determination Theory: autonomy — одна из 3 базовых психологических потребностей | [Deci & Ryan, 1985](https://selfdeterminationtheory.org/) |

### 10 DON'Ts

| # | DON'T | Обоснование | Последствие |
|---|-------|-------------|-------------|
| 1 | **Осудительный тон** | RSD + shame spiral: "Ты пропустил 3 дня" → avoidance → dropout | 80%+ не возвращаются в течение 7 дней |
| 2 | **Длинный onboarding** | Каждый дополнительный шаг теряет 20-30% пользователей | Activation rate падает с 70% до 40% |
| 3 | **Сброс streak после 1 пропуска** | All-or-nothing thinking (когнитивное искажение при ADHD) → "всё сломал → нет смысла" | D30 retention падает на 25-40% |
| 4 | **Обязательное видео/аудио** | Social anxiety barrier; text-based check-ins достаточны (FLOWN) | Барьер входа для 30-40% аудитории |
| 5 | **Автопланирование без подтверждения** | Нарушает autonomy (SDT); создаёт ощущение потери контроля | Высокий churn в первую неделю |
| 6 | **Сообщения во время фокуса** | Flow state требует 15-25 мин непрерывного фокуса; одно прерывание сбрасывает таймер | [Csikszentmihalyi, 1990](https://www.harpercollins.com/products/flow-mihaly-csikszentmihalyi) |
| 7 | **Заявлять, что BD заменяет медикаменты** | Body doubling — комплементарная стратегия, не альтернатива стимулянтам. Этическая ответственность | Medical misinformation liability |
| 8 | **Игнорировать feedback "не работает"** | 68% пользователей, которые churn, пытались дать feedback; игнор = гарантированный churn | Retention падает на 40%+ |
| 9 | **Paywall для базовой функциональности** | СДВГ часто сопровождается финансовыми трудностями; привычка требует 66+ дней ежедневной практики | Исключает наиболее уязвимых пользователей |
| 10 | **Требовать wearable для работы** | Hardware gatekeeping; pairing теряет 20-30% пользователей | Accessibility barrier |

### Anti-Patterns

| Антипаттерн | Признаки | Антидот |
|-------------|----------|---------|
| **Productivity Theater** | Больше времени на check-in, чем на работу; сессии ради streak | Session quality metrics > count; "Deep work" tagging |
| **Dependency** | "Не могу работать без AI"; паника при отсутствии | Graduated independence; offline toolkit; periodic "solo sessions" |
| **Over-Optimization** | Бесконечная настройка шаблонов вместо работы | "Start messy" messaging; time-boxed setup (2 мин) |
| **Shame Cycle** | Пропуск → guilt notification → avoidance → dropout | Shame-free handling; Two-Day Rule; compassionate messaging |

### Friction Audit

#### Текущий Flow (без оптимизации)

| Шаг | Время | Friction | Drop-off |
|-----|-------|----------|----------|
| Узнать о BD | — | Low | — |
| Найти / открыть | 1-3 мин | Medium | 20-30% |
| Onboarding | 30-60 сек | **High** | 30-50% |
| Registration | 30-90 сек | **High** | 20-40% |
| Permissions | 10-20 сек | Medium | 10-15% |
| Understand | 5-15 сек | **High** | 20-30% |
| Tap "Start" | 1 сек | Low | 2% |
| **Итого к First Session** | **45 сек–3 мин** | | **60-80%** |

#### Оптимизированный Flow (цель)

| Шаг | Время | Friction |
|-----|-------|----------|
| Открыть приложение / чат | 2 сек | Low |
| Tap "Начать сессию" | 1 сек | Low |
| **Итого к First Session** | **3 сек** | **Minimal** |

**Deferred (после первой сессии):** Регистрация, onboarding, permissions, кастомизация.

---

## 1.6 Как лучше применить к проекту

### Приоритетная фича: Что делать сейчас

```
MVP БОДИ ДАБЛИНГА (2 недели разработки)
========================================
□ Текстовые чек-ин шаблоны (7 штук — стандартные flow)
□ Таймер сессий (25/45/50 мин)
□ Mid-session чек-ин (50% времени)
□ Completion flow с выбором результата
□ Streak counter (с Two-Day Rule)
□ Daily nudge (время настраиваемое)
□ Stats dashboard (команда "статистика")
□ Soft recovery для пропусков
□ Integration с Google Calendar (MCP)
□ Custom templates (2 шаблона: deep work + quick task)
```

### MVP Scope

| Компонент | Вкл/Выкл | Сложность | Риск |
|-----------|----------|-----------|------|
| Text-based body doubling (25 мин) | **MUST** | Low | Low |
| Streak counter + Two-Day Rule | **MUST** | Low | Low |
| Mid-session чек-ин (один) | **MUST** | Low | Low |
| Daily nudge | **MUST** | Low | Low |
| Stats dashboard | **MUST** | Low | Low |
| Google Calendar MCP | **SHOULD** | Medium | Low |
| Custom templates | **SHOULD** | Low | Low |
| Multiple sessions per day | **COULD** | Medium | Medium |
| Energy-aware scheduling | **COULD** | Medium | Medium |
| Advanced analytics | **WON'T** (V2) | High | Medium |

### Roadmap

| Фаза | Срок | Что внутри |
|------|------|------------|
| **MVP** (V1) | Недели 1-2 | Базовый body doubling: 25 мин, чек-ин, streak, daily nudge, stats |
| **Integration** (V2) | Недели 3-4 | Google Calendar MCP, custom templates, energy-aware hints |
| **Advanced** (V3) | Недели 5-8 | Multiple sessions, deep work blocks, retrospective analytics |
| **Optimization** (V4) | Недели 9-12 | Wearable integration, ML-based suggestions, group features |

---

## 1.7 Как НЕ делать

### Что точно убьёт продукт

| Антипаттерн | Почему убивает | Пример |
|-------------|---------------|--------|
| **"Мотивирующая критика"** | RSD → shame spiral → dropout | "Ты пропустил 3 дня, давай соберись" |
| **Обязательный onboarding** | Каждый шаг теряет 20-30% | Опрос из 10 вопросов перед первой сессией |
| **Сброс streak = 0** | All-or-nothing → abandonment | "Серия сломана" вместо Two-Day Rule |
| **Сообщения во время фокуса** | Прерывание flow → раздражение | "Как продвигается?" на 10-й минуте 25-минутной сессии |
| **"Body double лучше таблеток"** | Medical misinformation → liability | Любое сравнение с фармакологическим лечением |
| **Feature dump** | Cognitive overload → dropout | 15 функций в первый день |
| **Требование Google Calendar** | Friction → не доходят до первой сессии | "Подключите Calendar чтобы начать" |
| **Leaderboard** | Сравнение вызывает тревогу (RSD) | "Ты на 45-м месте среди пользователей" |
| **Gamification pressure** | Streak заставляет сессии ради streak | "Не прерывай серию!" push notification |
| **Частые нотификации** | Notification fatigue → отключение | 5+ пушей в день о body doubling |

### Примеры плохих и хороших сообщений

**❌ Плохое (осудительное):**
> "Ты пропустил 3 дня подряд."
> "Почему ты не завершил сессию?"
> "Твой streak сломан."
> "Ты должен работать усерднее."

**✅ Хорошее (поддерживающее):**
> "Рад тебя видеть! Что будем делать следующие 25 минут?"
> "Отличная работа! Даже 15 минут фокуса — это прогресс."
> "Два дня перерыва — ничего страшного. Начнем с 5 минут?"
> "Как прошла сессия?" (любой ответ принимается)

---
---

# Часть 2: Wearable Energy Integration

## 2.1 Executive Summary

### Что это

**Wearable Energy Integration** — функциональность, позволяющая AI-коучу читать данные с носимых устройств (умных часов, фитнес-браслетов) через Android Health Connect и предсказывать оптимальное время для задач разной сложности. AI корректирует расписание, рекомендует задачи по энергии и предотвращает овер-шедулинг.

### Зачем это в life-planning-coach

Пользователи планируют задачи, не зная своего реального уровня энергии. Результат: сложные задачи ставятся на низкую энергию → не выполняются → frustration → отказ от планирования. Wearable-интеграция даёт AI "физический сигнал" о состоянии пользователя, позволяя smart scheduling.

### Для кого

| Сегмент | Профит | Приоритет |
|---------|--------|-----------|
| Пользователи с Garmin/Oura | Body Battery → точный energy score | P0 |
| Пользователи с Samsung Galaxy Watch | Energy Score + Health Connect | P0 |
| Пользователи с Xiaomi/Huawei | Health Connect (HR, sleep, steps) | P1 |
| Без wearable | Самооценка энергии (Layer 1) | P0 (fallback) |
| Все (ML модель) | Корреляция энергии и продуктивности | P1 |

### Android-first подход

| Причина | Данные |
|---------|--------|
| Android доля в РФ | **65.17%** (iOS 34.83%) |
| Health Connect availability | Android 10+ |
| Google Fit sunset | Завершён — Health Connect = единственный стандарт |
| iOS HealthKit | Не поддерживает Health Connect; требует отдельной интеграции |

### Ключевые числа

| Метрика | Значение | Источник |
|---------|----------|----------|
| **Android доля в РФ** | 65.17% (iOS 34.83%) | [StatCounter](https://gs.statcounter.com/os-market-share/mobile/russian-federation) |
| **Продано wearables в РФ 2024** | ~5 млн штук | Industry estimates |
| **Wearable penetration в РФ** | ~15% (150-200 млн активных Android) | Calculated |
| **Garmin Body Battery корреляция с POMS** | r = 0.57 (p < 0.01) | [Grande et al., 2024](https://pubmed.ncbi.nlm.nih.gov/39122733/) |
| **HRV RMSSD accuracy (Apple/Garmin/Polar)** | r = 0.92-0.98 vs clinical ECG | [Nelson et al., 2017](https://pubmed.ncbi.nlm.nih.gov/28952697/); [Lu et al., 2009](https://pubmed.ncbi.nlm.nih.gov/19377114/) |
| **HRV accuracy (Oura)** | r = 0.83-0.92 (младшие модели слабее) | [Kinnunen et al., 2020](https://pubmed.ncbi.nlm.nih.gov/32353867/) |
| **No-name бренды** | **37.2%** доли рынка РФ | Market data |
| **Стимулянты + behavioral strategies** | **d = 0.89** (Time Management) | [Prevatt & Yelland, 2015](https://files.eric.ed.gov/fulltext/EJ1182373.pdf) |
| **Цена Body Battery компиляции** | 600-1,200 руб. | Market research |

---

## 2.2 Рынок устройств (Россия)

### 2.2.1 Android 65% vs iOS 35%

| Платформа | Доля в РФ | Wearable-рынок | Health интеграция | Примечание |
|-----------|-----------|----------------|-------------------|------------|
| **Android** | **65.17%** | 65% | ✅ Health Connect (встроен) | Xiaomi, Samsung, Huawei, No-name |
| **iOS** | 34.83% | 35% | ❌ HealthKit (отдельная интеграция) | Apple Watch, Oura, Whoop |

### 2.2.2 Топ бренды

| Бренд | Доля рынка РФ | Характеристика | Поддержка Health Connect |
|-------|--------------|----------------|-------------------------|
| **No-name** | **37.2%** | Базовые HR, шаги, sleep | Частично (базовые типы) |
| **Apple** | 6.5% (wearable) | Watch, iPhone | ❌ HealthKit only |
| **Samsung** | 13.8% | Galaxy Watch — HR, SpO2, sleep, body composition, HRV | ✅ Samsung Health → Health Connect |
| **Xiaomi** | 14.2% | Mi Band, Amazfit — HR, steps, sleep | ✅ Zepp Life → Google Fit → Health Connect |
| **Huawei** | 17.1% | Watch GT — TruSleep, SpO2, stress, VO2max | ⚠️ Huawei Health → HMS Health Kit (не всегда Health Connect) |
| **Garmin** | 3.2% | Forerunner, Venu — Body Battery, Stress, Training Readiness | ✅ Garmin Connect → Health Connect (через сторонние приложения) |
| **Fitbit** | 4.8% | HR, steps, sleep, stress | ✅ Fitbit app → Health Connect |
| **Прочие** | 18.2% | Polar, Suunto, Withings, etc. | Частично |

### 2.2.3 Портрет клиента

```
Типичный пользователь life-planning-coach с wearable:
┌─────────────────────────────────────────────┐
│  Возраст: 25-45 лет                          │
│  Профессия: IT, дизайн, управление, фриланс  │
│  Платформа: Android (65%)                    │
│  Устройство: Xiaomi Mi Band / Samsung GW     │
│  Использует: steps, sleep, HR ежедневно      │
│  Body Battery: Нет (у 85% нет Garmin/Oura)   │
│  Хочет: "Когда мне лучше делать сложные      │
│         задачи?" / "Почему я вялый днём?"    │
│  Боится: отдать данные здоровья третьим лицам│
│  Уровень tech-savviness: Medium-High         │
└─────────────────────────────────────────────┘
```

---

## 2.3 Приоритет интеграций

| # | Платформа | Почему | Данные | Сложность | Приоритет для РФ |
|---|-----------|--------|--------|-----------|-----------------|
| 1 | **Google Health Connect** | Единый API для Android; покрывает 80%+ устройств; privacy-first (on-device) | HR, HRV (RMSSD), sleep stages, steps, SpO2, calories, body temp | 🟢 Low | **РФ: #2** |
| 2 | **Samsung Health** | Galaxy Watch #1 среди Android в РФ; Energy Score | Energy Score (0-100), HR, sleep, SpO2, body composition, workout | 🟡 Medium | **РФ: #2-3** |
| 3 | **Garmin Health API** | Body Battery — единственная валидированная energy метрика; Training Readiness | Body Battery (0-100), stress, HRV, sleep, training status, VO2max | 🟡 Medium-High | **РФ: #4** (niche) |
| 4 | **Huawei Health Kit** | 17% рынка РФ; HMS работает без Google | TruSleep, stress, SpO2, VO2max, HR | 🟡 Medium | **РФ: #1** |
| 5 | **Xiaomi (fallback)** | 14% рынка РФ; **НЕТ официального API** — через Google Fit | HR, steps, sleep (базовые) | 🔴 Very High (reverse engineering) | Fallback |

### Рекомендуемый порядок для РФ

```
Phase 1 (Недели 1-4):    Huawei Health Kit → Health Connect
Phase 2 (Недели 5-8):    Samsung Health Data SDK
Phase 3 (Недели 9-12):   Garmin Health API (enterprise/niche)
Phase 4 (Недели 13-16):  Xiaomi через Google Fit bridge
Phase 5 (Недели 17-20):  MCP Server (unified API)
```

### API Comparison Matrix

| Платформа | API Type | HRV | Sleep Stages | Energy/Recovery | Background | Write Access | В РФ |
|-----------|----------|-----|--------------|-----------------|------------|--------------|------|
| Google Health Connect | Android SDK (on-device) | ✅ RMSSD | ✅ Deep/Light/REM/Awake | ❌ (нужно вычислять) | ✅ Android 15+ | ✅ | ✅ |
| Samsung Health SDK | Android SDK (local) | ❌ (только через HR) | ✅ + Sleep Apnea | ✅ Energy Score | ✅ Foreground | ✅ | ✅ (Galaxy Store) |
| Garmin Health API | REST API (cloud) | ✅ SDNN/RMSSD | ✅ Полные + score | ✅ Body Battery | ✅ Webhook | ❌ | ⚠️ (niche) |
| Huawei Health Kit | HMS SDK | ❌ | ✅ TruSleep | ❌ Stress only | ✅ | ✅ | ✅ (AppGallery) |
| Xiaomi Mi Band | ❌ Нет API | ❌ | Частично | ❌ | ❌ | ❌ | ⚠️ (только через Google Fit) |

---

## 2.4 Научная база

### 2.4.1 HRV Accuracy по устройствам

| Устройство | HRV RMSSD | r vs ECG | Источник | Примечание |
|-----------|-----------|----------|----------|------------|
| **Apple Watch** | ✅ | r = 0.96 | [Nelson et al., 2017](https://pubmed.ncbi.nlm.nih.gov/28952697/) | Через Breathe app |
| **Garmin** | ✅ | r = 0.92 | [Ghambari et al., 2022](https://pubmed.ncbi.nlm.nih.gov/35275576/) | Во время сна |
| **Polar H10** | ✅ | r = 0.98 | [Lu et al., 2009](https://pubmed.ncbi.nlm.nih.gov/19377114/) | Chest strap — gold standard |
| **Oura Ring** | ✅ | r = 0.83-0.92 | [Kinnunen et al., 2020](https://pubmed.ncbi.nlm.nih.gov/32353867/) | Младшие модели слабее |
| **Fitbit** | ⚠️ | ~r = 0.70 | Multiple studies | Зависит от модели |
| **Samsung Galaxy Watch** | ⚠️ | Частично | Limited data | Через HR, не dedicated HRV |
| **Huawei** | ❌ | Н/Д | Нет данных | Не предоставляет HRV |
| **Xiaomi Mi Band** | ❌ | Н/Д | Нет данных | Не предоставляет HRV |

> **Вывод:** HRV RMSSD — наиболее надёжный биомаркер. Apple Watch и Polar — самые точные. Garmin — acceptable. Для energy estimation HRV даёт ~30% variance explained в subjective energy.

### 2.4.2 Garmin Body Battery — единственная валидированная energy метрика

**Что такое Body Battery:**

[Garmin Body Battery](https://www.garmin.com/en-US/garmin-technology/health-science/body-battery/) — это проприетарная метрика Garmin (Firstbeat Analytics), представляющая собой 0-100 шкалу текущего "запаса энергии". Рассчитывается на основе:

- **HRV (heart rate variability)** — показатель вегетативной нервной системы
- **HR (heart rate)** — интенсивность активности
- **Activity data (accelerometer)** — физическая нагрузка
- **Sleep quality** — восстановление ночью

**Валидация:**

| Исследование | Результат | Ссылка |
|-------------|-----------|--------|
| **Grande et al., 2024** | Body Battery correlates with POMS vitality subscale at r = 0.57 (p < 0.01) | [PubMed](https://pubmed.ncbi.nlm.nih.gov/39122733/) |
| **Firstbeat White Paper** | Algorithm based on HRV-derived recovery modeling from 2000s research | [Garmin](https://www.garmin.com/en-US/garmin-technology/health-science/body-battery/) |
| **Garmin internal validation** | r = 0.72 correlation with subjective energy reports | Garmin data |

**Иерархия energy-метрик:**

| Метрика | Валидация | Корреляция с energy | Надёжность | Ссылка |
|---------|-----------|-------------------|------------|--------|
| **Garmin Body Battery** | ✅ Peer-reviewed | r = 0.57 (POMS) | ★★★★★ | [Grande et al., 2024](https://pubmed.ncbi.nlm.nih.gov/39122733/) |
| **Oura Readiness Score** | ⚠️ Internal only | ~r = 0.50 | ★★★☆☆ | Oura data |
| **HRV RMSSD** | ✅ Extensive | ~r = 0.30-0.40 | ★★★★☆ | Multiple studies |
| **Subjective 1-10 energy** | ✅ Gold standard | r = 1.00 (by definition) | ★★★★★ | Self-report |
| **Sleep quality composite** | ✅ Moderate | r = 0.35-0.50 | ★★★☆☆ | Multiple studies |
| **Samsung Energy Score** | ⚠️ Very limited | Н/Д | ★★☆☆☆ | New metric, 2024 |

> **Формула приоритизации:**
> ```
> Energy Score = 
>   IF Body Battery available: 0.5 * Body Battery + 0.3 * HRV trend + 0.2 * Sleep quality
>   ELIF Sleep Score + HRV: 0.4 * Sleep quality + 0.4 * HRV trend + 0.2 * Activity balance
>   ELSE: Использовать самооценку (Layer 1)
> ```

### 2.4.3 Risks: Orthosomnia

**Ортосомния** — clinically described phenomenon (Baron et al., 2017, JCSM):

| Симптом | Как проявляется | Мера предосторожности |
|---------|----------------|----------------------|
| Тревожность из-за данных о сне | Частая проверка sleep tracker | Не показывать sleep score ежедневно |
| "Гонка за perfect score" | Отказ от вечерних активностей | Показывать тренды, не абсолютные числа |
| Ночные проверки | Просыпаются ночью — проверяют | Gentle intervention: предложить "digital detox" |
| Медикализация | "Мой сон плохой" → тревога | Образование: "сон — не конкурс, вариации нормальны" |

**Меры защиты:**
1. НЕ показывать sleep score ежедневно (только по запросу или тренд)
2. НЕ отправлять push об "плохом сне"
3. Показывать сообщение: "Сон — не конкурс. Небольшие вариации нормальны."
4. После 3 дней низких метрик: предложить ОТДОХНУТЬ от трекинга
5. Раздел "Digital Detox": временное отключение wearable-данных
6. Ежемесячный скрининг: "Чувствуете ли вы тревогу из-за данных о сне?"

### 2.4.4 Медицинские заявления: Чёткая граница

| Разрешено | Запрещено | Почему |
|-----------|-----------|--------|
| "Энергия ниже вашего обычного" | "У вас выгорание" | Не ставим диагнозы |
| "Наблюдается тренд на снижение" | "У вас хроническая усталость" | Корреляция ≠ причинность |
| "Сон короче вашего среднего" | "У вас нарушение сна" | Не медикализируем |
| "При низкой энергии — лёгкие задачи" | "Принимайте магний" | Не даём медицинских советов |
| "Если беспокоит — проконсультируйтесь со специалистом" | "Обратитесь к неврологу" | Мягкая рекомендация, не направление |

---

## 2.5 Customer Journey (полный)

### Stage 1: Discovery

#### Touchpoint: Wearable Pitch — Energy-версия

**Trigger:** Пользователь жалуется на усталость, непредсказуемую энергию, "не знаю когда лучше работать"
**Timing:** В момент разговора о scheduling

**Text (Claude → User):**

```
⚡ Интересно, что если я смогу читать данные 
с твоих часов и рекомендовать, когда тебе 
лучше делать сложные задачи?

Я увижу:
• Когда у тебя пик фокуса (по пульсу и сну)
• Когда энергия падает (перенести лёгкое)
• Как сон влияет на продуктивность

Это не магия — просто корреляция твоих данных 
с твоими задачами. Всё локально, на телефоне.

У тебя есть умные часы или браслет?
[Да, Garmin] [Да, Samsung Galaxy] 
[Да, Xiaomi/Huawei/другие] [Нет]
```

---

#### Touchpoint: Wearable Pitch — Scheduling-версия

**Trigger:** Пользователь обсуждает планирование дня

**Text (Claude → User):**

```
⚡ У меня есть идея, как сделать твоё расписание 
умнее.

Сейчас ты ставишь задачи "когда удобно". 
А если я буду знать твою энергию утром — 
посоветую: "сложную задачу сейчас, рутину 
после обеда"?

Для этого нужно:
1. Подключить Google Health Connect (2 тапа)
2. Разрешить доступ к пульсу и сну
3. Я всё вычислю сам — локально, на телефоне

Никакие данные не уходят наружу. Только 
рекомендации — тебе.

Попробуем?
[Подключить Health Connect] [Сначала ручной ввод]
[Расскажи про privacy]
```

---

#### Touchpoint: Wearable Pitch — Без wearable (self-report)

**Trigger:** Пользователь не имеет wearable

**Text (Claude → User):**

```
⚡ Не нужны часы, чтобы это работало.

Я могу просто спрашивать тебя утром: 
"Какая энергия сегодня?" — и по шкале 1-10 
ты отвечаешь.

Этого уже достаточно, чтобы:
• Ставить сложные задачи на пик энергии
• Лёгкие задачи — на спад
• Отслеживать тренды за неделю

Когда купишь часы — просто подключишь, 
и данные усреднятся. А пока — ручной режим.

Попробуем?
[Да, ручной режим] [Какие часы купить?]
```

---

### Stage 2: Consent & Connection

#### Touchpoint: Privacy Consent

**Trigger:** Пользователь согласился на подключение
**Timing:** Перед запросом разрешений

**Text (Claude → User):**

```
🔒 **Прежде чем подключать — про privacy.**

Всё, что я прочитаю с часов, остаётся 
на твоём телефоне. Я не отправляю данные 
здоровья на сервер. Ни пульс, ни сон, 
ни шаги.

**Что я запрашиваю:**
☑ Пульс в покое (resting HR)
☑ Пульс (heart rate)
☑ Вариабельность пульса (HRV) — если доступно
☑ Сон: длительность и стадии
☑ Шаги
☑ Body Battery / Energy Score — если есть

**Что я НЕ запрашиваю:**
❌ Локацию
❌ Контакты
❌ Медицинские записи

**Как использую:** только для корреляции 
с твоей продуктивностью. Локально.

[Подтвердить и подключить] [Выбрать, что разрешить]
[Отмена]
```

**Action options:**
- **"Подтвердить"** → Открыть Health Connect permission screen
- **"Выбрать"** → Granular consent screen (GDPR-compliant)
- **"Отмена"** → Fallback to manual self-report

---

#### Touchpoint: Connection Success

**Trigger:** Пользователь дал разрешения

**Text (Claude → User):**

```
✅ Подключено!

Читаю данные из Health Connect.
Это займёт несколько секунд...

📊 Найдено данных:
• Пульс: [N] дней истории
• Сон: [N] дней истории  
• HRV: [да/нет]
• Body Battery: [да/нет]
• Шаги: [N] дней истории

Формирую твой energy baseline...
Это займёт 1-7 дней для точности.

Сейчас покажу первый анализ.
```

---

### Stage 3: First Reading & Baseline

#### Touchpoint: First Baseline Report

**Trigger:** Собрано минимум 1-2 дня данных
**Timing:** Первый анализ после подключения

**Text (Claude → User):**

```
📊 **Первый energy-анализ**

Это начальная точка. Станет точнее 
через 7-14 дней.

**Твой профиль (предварительный):**

🟢 **Пик энергии:** [время] ([N]% от baseline)
🟡 **Средняя энергия:** [время]
🔴 **Спад:** [время]

💤 **Сон за последние 7 дней:**
Среднее: [X]ч (твой baseline формируется)
Качество: [N]/100

❤️ **Пульс в покое:** [N] bpm

⚡ **Рекомендация на сегодня:**
[задача_1] → [время_пика] (пик энергии)
[задача_2] → [время_средней]
[задача_3] → перенести на завтра если возможно

(Станет точнее через [N] дней)
[Понятно] [Покажи подробнее] [Настроить]
```

**Action options:**
- **"Понятно"** → Принять, дождаться утреннего чек-ина
- **"Подробнее"** → Detailed analysis of each metric
- **"Настроить"** → Adjust thresholds, notification time

---

#### Touchpoint: Baseline Building (дни 2-7)

**Trigger:** Ежедневное утреннее обновление

**Text (Claude → User) — день 2:**

```
📊 **Energy Baseline: день 2/7**

Собираю данные... [N]% профиля собрано.

Вчера: 
• Сон: [X]ч
• Пробуждение HR: [N] bpm  
• Текущая энергия: [inferred]

Пока рано давать рекомендации, но вот 
первое наблюдение:
"У тебя HR в покое [выше/ниже] среднего 
для [возраст/пол]. Это может значить 
[восстановление/нагрузка/норма]."

Продолжаю наблюдать. Утренний чек-ин:
Какая энергия сегодня? (1-10)
[1-3 😴] [4-6 😐] [7-8 🙂] [9-10 ⚡]
```

---

#### Touchpoint: Stable Baseline (день 7+)

**Trigger:** Собрано >= 7 дней данных

**Text (Claude → User):**

```
📊 **Energy Baseline: сформирован!**

7 дней данных — достаточно для первых 
рекомендаций.

**Твой профиль:**

🟢 **Пик фокуса:** [время_1] - [время_2]
   (Энергия: [N]/100)
   → Сложные задачи, креатив, кодинг

🟡 **Средняя зона:** [время_3] - [время_4]  
   → Рутина, email, митинги

🔴 **Спад:** [время_5] - [время_6]
   → Лёгкие задачи или отдых

💤 **Sleep pattern:**
Средний сон: [X]ч ([N]% от population avg)
Лучшее время засыпания: [время]
Качество: [N]/100

❤️ **Resting HR:** [N] bpm
Вариабельность: [N] ms (HRV)

⚡ **Прогноз на сегодня:**
Пик: [время] | Средняя: [время] | Спад: [время]

Начинаю адаптировать твоё расписание.
```

---

### Stage 4: Daily Energy Insights

#### Touchpoint: Morning Energy Check

**Trigger:** Утро, настроенное время (default: 08:30)

**Text (Claude → User) — С wearable:**

```
☀️ Доброе утро! Energy check.

📊 Данные с часов:
• Сон: [X]ч [N]/100
• Пульс в покое: [N] bpm
• HRV: [N] ms ([выше/ниже] твоего avg)
• Body Battery: [N]/100

⚡ **Energy forecast:**
🟢 Пик: [время] ([N]/100)
🟡 Средняя: [время] ([N]/100)
🔴 Спад: [время] ([N]/100)

**Рекомендации:**
→ [задача_сложная] @ [пиковое_время]
→ [задача_лёгкая] @ [время_спада]

Прогноз точный на [N]% (улучшается каждый день)

Какая энергия по ощущениям? (1-10)
[😴 1-3] [😐 4-6] [🙂 7-8] [⚡ 9-10]
```

**Text (Claude → User) — Без wearable (self-report):**

```
☀️ Доброе утро!

Какая у тебя энергия сегодня?

[😴 1-2] Выспался, но нет сил
[😐 3-4] Нормально, обычное утро
[🙂 5-6] Хорошо, готов к делам
[⚡ 7-8] Отлично, можно сложные задачи
[🔥 9-10] Пик! Всё горит в руках

Я запомню и буду рекомендовать задачи 
по энергии.
```

---

#### Touchpoint: Energy Dip Alert

**Trigger:** Energy score падает ниже baseline на > 20%

**Text (Claude → User):**

```
⚡ **Energy dip detected**

Твоя энергия сейчас: [N]/100
(Ниже твоего среднего на [X]%)

Что обнаружил:
• Пульс в покое: [N] (обычно [avg])
• HRV: [N] (ниже на [X]%)
• [Если известно]: плохой сон / нагрузка / стресс

**Рекомендация:**
Сейчас не лучшее время для сложных задач.
Предлагаю:
→ Перенести [сложная_задача] на [время_пика]
→ Сейчас: [лёгкая_задача] или перерыв

Это нормально — энергия колеблется. 
Вечером будет лучше.

[Перенести задачу] [Оставить как есть] 
[Покажи подробности]
```

---

### Stage 5: Smart Scheduling

#### Touchpoint: Task-Energy Matching

**Trigger:** Пользователь просит составить/обновить расписание

**Text (Claude → User):**

```
📅 **Расписание с учётом энергии**

Твой energy curve сегодня:
08:00 ████████░░ [N]/100
09:00 █████████░ [N]/100  🟢 ПИК
10:00 █████████░ [N]/100  🟢 ПИК
11:00 ███████░░░ [N]/100
12:00 ██████░░░░ [N]/100  🟡 Средняя
13:00 █████░░░░░ [N]/100  🟡 Средняя
14:00 ████░░░░░░ [N]/100  🔴 Спад
15:00 ████░░░░░░ [N]/100  🔴 Спад
16:00 █████░░░░░ [N]/100
17:00 ██████░░░░ [N]/100  🟡 Второй пик

**Рекомендуемое расписание:**

🟢 09:00-11:00 → [сложная_задача_1] (пик!)
🟡 12:00-13:00 → [рутинная_задача] (email, calls)
🔴 14:00-15:00 → [лёгкая_задача] или перерыв
🟡 17:00-18:00 → [средняя_задача] (второй пик)

Применить?
[Применить] [Передвинуть] [Оставить моё]
```

---

#### Touchpoint: Post-Task Energy Feedback

**Trigger:** Пользователь отметил задачу выполненной

**Text (Claude → User):**

```
✅ [задача] — выполнена!

Была ли энергия в это время такой, как 
я прогнозировал?

[⚡ Да, точно] — прогноз верен
[😐 Ниже] — энергия была ниже
[🚀 Выше] — энергия была выше
[🤷 Не знаю]

(Это поможет мне точнее прогнозировать)
```

---

### Stage 6: Long-term Insights

#### Touchpoint: Weekly Report

**Trigger:** Конец недели (воскресенье вечером)

**Text (Claude → User):**

```
📊 **Energy Report: неделя [N]**

⚡ Energy trend:
Пн ████████░░ [N]
Вт █████████░ [N]  🟢
Ср ██████░░░░ [N]
Чт █████░░░░░ [N]  🔴
Пт ███████░░░ [N]
Сб █████████░ [N]  🟢
Вс ██████░░░░ [N]

📈 Средняя энергия: [N]/100 (было [prev] на 
прошлой неделе)

💤 Сон:
Среднее: [X]ч
Качество: [N]/100
Лучший день: [день]

🎯 Task-energy alignment:
Сложные задачи в пик энергии: [N]% (цель: >60%)
Продуктивность: [N]/10 (самооценка)

**Insight:**
"В [день] энергия падает после 14:00. 
Попробуй перенести сложные задачи 
на утро этого дня."

[Подробный отчёт] [Настройки] [Ок]
```

---

#### Touchpoint: Monthly Insight

**Trigger:** Конец месяца

**Text (Claude → User):**

```
📊 **Monthly Insight: [месяц]**

**Energy Trend за месяц:**
{тренд} | Средний Energy: [N] (было [prev])

**График:**
Неделя 1: ████████░░ [w1]
Неделя 2: █████████░ [w2]
Неделя 3: ██████░░░░ [w3]
Неделя 4: ███████░░░ [w4]

**Что изменилось:**
[change_analysis]

*Примеры:*
"Тренд восходящий (+8 пунктов). Вероятно, 
выработали более стабильный режим сна."
"Стабильное снижение с 3-й недели. 
Совпадает с [detected_factor]."

**Correlation detected:**
📈 [correlation_insight]

*Пример: "В дни после <6ч сна эффективность 
падает на 40%. Рекомендация: ложиться до 
23:30 в рабочие дни."*

**Ваш Energy Archetype (обновлён):**
[archetype_description]

*Примеры архетипов:*
• "Morning Phoenix — пик к 9-10 утра, 
   к вечеру плавно сгорает"
• "Slow Burner — разгоняется медленно, 
   но держится стабильно"
• "Bimodal — два пика (утро + вечер), 
   провал днём"

[Подробный correlation analysis] 
[Установить цель на месяц]
[Экспортировать отчёт]
```

---

#### Touchpoint: Trend Alert

**Trigger:** Значимое изменение энергии (> 15% за неделю)

**Text (Claude → User):**

```
📢 **Trend Alert: значимое изменение энергии**

Я заметил кое-что важное:

🔋 Средний Body Battery за 7 дней: [recent]
📊 За предыдущие 7 дней: [previous]
📉 Изменение: [X]%

**Что это значит:**
[interpretation]

*Варианты:*
"Ваш средний Body Battery упал на 20% за 
неделю. Это не нормальная вариативность — 
скорее всего, есть причина: болезнь, 
хронический стресс, или вы перерабатываете."

**Обнаруженные корреляции:**
[correlations]

*Пример: "Сон сократился на 1.2ч в среднем. 
Это главный фактор падения."*

**Рекомендация:**
[recommendation]

[Покажи детали] [Что мне делать?] 
[Это нормально, не беспокоить]
```

---

#### Touchpoint: Personalized Recommendation

**Trigger:** Еженедельный отчёт + достаточно данных

**Text (Claude → User):**

```
💡 **Персональная рекомендация**

Я проанализировал, в какие дни у вас лучше 
всего получается работать. Вот что нашёл:

**Ваши успешные дни (Energy > 75):**
• Среднее время сна: [success_sleep]ч 
  (vs [fail_sleep]ч в провальных днях)
• Среднее время засыпания: [success_bedtime]
• Шагов предыдущего дня: [success_steps]

**Главный рычаг для вас:**
[top_lever]

*Пример: "Разница в 1.5 часа сна даёт вам 
+25 пунктов Energy. Это самый сильный фактор. 
Если хотите улучшить одну вещь — ложитесь 
раньше."*

**Эксперимент на следующую неделю:**
[experiment_suggestion]

Я отслежу результаты и расскажу, 
сработало ли.

[Принять эксперимент] [Другая рекомендация] 
[Напомни мне об этом]
```


---

## 2.6 Privacy Architecture

### 2.6.1 GDPR Article 9

**GDPR Article 9** классифицирует данные о здоровье как **special category data**, требующую **explicit consent**.

| Тип данных | GDPR статус | Требования |
|------------|-------------|------------|
| Шаги, дистанция | Personal data (Art. 6) | Standard consent |
| Heart rate, SpO2 | **Health data (Art. 9)** | **Explicit consent** required |
| Sleep stages | **Health data (Art. 9)** | **Explicit consent** required |
| HRV | **Health data (Art. 9)** | **Explicit consent** required |
| Body Battery / Energy Score | **Health data (Art. 9)** | **Explicit consent** required |
| Medical records (FHIR) | Special category | **Explicit consent** + DPIA |

**Требования к explicit consent:**
- [ ] Явное (explicit) — **не pre-ticked** checkbox
- [ ] Granular — отдельное согласие на каждый тип данных
- [ ] Информированное — объяснение зачем каждая метрика
- [ ] Отзываемое — кнопка отзыва доступна в 2 тапа из любого экрана
- [ ] Документируемое — audit trail с timestamp (локально)

### 2.6.2 Local-only Processing (Zero-Knowledge Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                  Android Device                             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Health       │  │ SQLCipher DB │  │ TensorFlow Lite  │  │
│  │ Connect      │──►│ (encrypted)  │──►│ (local ML)       │  │
│  │ (reads data) │  └──────────────┘  └──────────────────┘  │
│  └──────────────┘           │                  │            │
│                             ▼                  ▼            │
│                   ┌──────────────────────────────┐         │
│                   │ Biometric-locked storage     │         │
│                   │ (Android Keystore)           │         │
│                   └──────────────────────────────┘         │
│                                                              │
│  ❌ Нет cloud processing для health-данных                 │
│  ❌ Нет передачи данных на сервер                          │
│  ✅ Только task metadata (без health контекста)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Сервер         │
                    │  • Task names   │
                    │  • Completion   │
                    │  • Timestamps   │
                    │  • NO health    │
                    └─────────────────┘
```

**Privacy-by-Design принципы:**

| Принцип | Реализация | Стандарт |
|---------|-----------|----------|
| Data minimization | Собираем только нужное для корреляции | GDPR Article 5(1)(c) |
| Purpose limitation | Только energy-productivity correlation | GDPR Article 5(1)(b) |
| Storage limitation | Автоудаление после 365 дней | GDPR Article 5(1)(e) |
| Privacy by design | Локальная обработка по умолчанию | GDPR Article 25 |
| Privacy by default | Opt-in для всего, что выходит за пределы устройства | GDPR Article 25(2) |

### 2.6.3 Consent Flow

```
Экран 1: Granular selection
┌──────────────────────────────────────────┐
│  Какие данные разрешить?                 │
│                                          │
│  ☑ Пульс (HR) — для energy estimation   │
│  ☑ Сон — для recovery анализа           │
│  ☐ HRV — для точности (опционально)     │
│  ☑ Шаги — для activity correlation      │
│  ☐ Body Battery — если есть Garmin      │
│                                          │
│  [Продолжить]                            │
└──────────────────────────────────────────┘

Экран 2: Confirmation (GDPR Article 9)
┌──────────────────────────────────────────┐
│  Подтвердите доступ к данным о здоровье  │
│                                          │
│  Разрешённые типы: [список]             │
│                                          │
│  Как используем:                         │
│  • Только на вашем устройстве           │
│  • Для корреляции с продуктивностью     │
│  • Без передачи третьим лицам           │
│  • Можно отозвать в любой момент        │
│                                          │
│  ⚠️ Это данные о здоровье (GDPR Art. 9) │
│                                          │
│  [✅ Я даю explicit consent]             │
│  [❌ Отмена — ручной режим]              │
└──────────────────────────────────────────┘
```

### 2.6.4 Zero-Knowledge Architecture

| Компонент | Где обрабатывается | Передаётся в облако? |
|-----------|-------------------|---------------------|
| Сырые данные с wearable | Health Connect (на устройстве) | ❌ Нет |
| Корреляционный анализ | TensorFlow Lite (на устройстве) | ❌ Нет |
| Хранение истории | SQLCipher (encrypted, на устройстве) | ❌ Нет |
| Генерация рекомендаций | Rule-based + lightweight ML (на устройстве) | ❌ Нет |
| Task metadata (названия, статусы) | Сервер | ✅ Да (без health контекста) |
| Encrypted backup | Google Drive (E2EE) | ✅ Только с explicit opt-in |

### 2.6.5 Audit Trail

| Действие | Что логируется | Где хранится |
|----------|---------------|--------------|
| Consent given | Timestamp, metric types | Локальная БД |
| Data access | Какое приложение, какие данные, когда | Локальная БД |
| ML inference | Input features (hashed), output, timestamp | Локальная БД |
| Manual override | Что переопределено, почему | Локальная БД |
| Data deletion | Timestamp, scope | Локальная БД + receipt пользователю |

### 2.6.6 Privacy-Disclaimers (вставлять где уместно)

- "Все health-данные обрабатываются локально на вашем телефоне"
- "Мы не храним health-данные на своих серверах"
- "Google Health Connect — это зашифрованное хранилище Android, доступное только приложениям с вашим разрешением"
- "Вы можете отозвать доступ в любой момент в настройках Health Connect"
- "Данные не используются для рекламы и не передаются третьим лицам"

---

## 2.7 DOs and DON'Ts

### 10 DOs

| # | DO | Обоснование | Научный источник |
|---|----|-------------|------------------|
| 1 | **Начинать с самооценки энергии (1-10)** | Субъективная оценка — единственный универсальный знаменатель; работает без wearables | Subjective vitality (Bostic et al., 2000) |
| 2 | **Использовать Google Health Connect как универсальный агрегатор** | Единая точка доступа ко всем wearables; privacy-first by design | [Google Health Connect](https://developer.android.com/health-and-fitness/guides/health-connect) |
| 3 | **Приоритет Garmin Body Battery** | Единственная валидированная energy метрика (r = 0.57 vs POMS) | [Grande et al., 2024](https://pubmed.ncbi.nlm.nih.gov/39122733/) |
| 4 | **Показывать тренды, не абсолютные числа** | Контекст важнее числа; пользователь не знает нормы | User research (Baron et al., 2017) |
| 5 | **Объяснять, что означают метрики** | Education first — без объяснения данные бесполезны | Health literacy research |
| 6 | **Получать явное согласие (GDPR Article 9)** | Health data = special category; explicit consent required | [GDPR Art. 9](https://gdpr-info.eu/art-9-gdpr/) |
| 7 | **Обрабатывать данные локально** | Zero-knowledge architecture = доверие пользователей | Privacy-by-design (Cavoukian, 2011) |
| 8 | **Разрешать ручное переопределение** | Human-in-the-loop: пользователь — единственный источник истины | [Cabitza et al., 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5544262/) |
| 9 | **Показывать корреляцию, не причинность** | "Связь" ≠ "влияет"; избегаем ложных causal claims | Statistics 101 |
| 10 | **Предлагать opt-out в любой момент** | GDPR право на забвение; доверие = легкий выход | [GDPR Art. 17](https://gdpr-info.eu/art-17-gdpr/) |

### 10 DON'Ts

| # | DON'T | Обоснование | Последствие |
|---|-------|-------------|-------------|
| 1 | **Не показывайте сырые числа без контекста** | "HRV: 42 мс" — бессмысленно без контекста; вызывает тревогу | Orthosomnia, confusion |
| 2 | **Не делайте медицинских заявлений** | "У вас выгорание" — диагноз, который мы не можем ставить | Legal liability |
| 3 | **Не требуйте wearable для базовой функциональности** | Не у всех есть часы; 80% ценности от самооценки | Accessibility barrier |
| 4 | **Не храните health-данные в облаке** | Privacy breach risk; GDPR violation | Fines up to 4% global revenue |
| 5 | **Не делитесь данными с третьими лицами** | Никаких analytics, ads, partners для health data | Loss of trust |
| 6 | **Не используйте осудительный тон** | "Вы недоспали снова" → shame → avoidance | User churn |
| 7 | **Не медикализируйте нормальные колебания** | Один плохой сон — не повод для алерта | Alert fatigue, orthosomnia |
| 8 | **Не назначайте автопланирование без подтверждения** | Нарушает autonomy (SDT); создаёт ощущение потери контроля | Высокий churn |
| 9 | **Не игнорируйте индивидуальный baseline** | Сравнение с популяционной нормой — бесполезно | Inaccurate recommendations |
| 10 | **Не создавайте ортосомнию** | Гонка за perfect metrics → тревожность | Clinical harm (Baron et al., 2017) |

### 5-слойная архитектура

```
╔═══════════════════════════════════════════════════════════════╗
║  LAYER 5: Smart Scheduling — умные рекомендации              ║
║  Auto-suggest optimal task times based on predicted energy    ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 4: ML Prediction — предсказание энергии               ║
║  On-device TensorFlow Lite model                              ║
║  Input: Historical self-reports + wearable features          ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 3: Garmin Body Battery — gold standard метрика        ║
║  Source: Firstbeat Analytics via Health Connect               ║
║  Fallback: Layer 2 composite score                           ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 2: Google Health Connect — универсальный агрегатор    ║
║  Reads: HR, HRV, Sleep, Steps, SpO2, Body Battery, Stress    ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 1: Self-reported Energy (1-10) — работает для всех    ║
║  Baseline metric, always available, privacy-safe             ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 2.8 Как лучше применить к проекту

### Начать с self-reported energy (Layer 1)

**Почему:** Работает для 100% пользователей; не требует hardware; создаёт baseline для correlation.

```python
# Поток данных
def get_energy_score(user):
    # Layer 1: Always available
    self_report = user.get_self_reported_energy()  # 1-10

    # Layer 2: If Health Connect available
    if user.health_connect_connected:
        hc_data = read_health_connect(user)

        # Layer 3: If Garmin Body Battery available
        if hc_data.body_battery_available:
            energy_score = 0.5 * hc_data.body_battery +                           0.3 * hc_data.hrv_trend +                           0.2 * hc_data.sleep_quality
        else:
            energy_score = 0.4 * hc_data.sleep_quality +                           0.4 * hc_data.hrv_trend +                           0.2 * hc_data.activity_balance
    else:
        energy_score = self_report * 10  # Scale to 0-100

    return energy_score
```

### Google Health Connect как aggregator

**Преимущества:**
- Пользователь даёт разрешение **один раз**
- Стандартизированные форматы данных
- Встроенный consent management
- 60+ приложений уже интегрированы

### Garmin Body Battery как gold standard

**Интеграция:**
```kotlin
// Health Connect чтение Body Battery
val response = healthConnectClient.readRecords(
    ReadRecordsRequest(
        recordType = BodyBatteryRecord::class,  // Если доступно
        timeRangeFilter = TimeRangeFilter.between(startTime, endTime)
    )
)
// Fallback: чтение через Garmin Health API (REST)
```

### Roadmap

| Фаза | Срок | Что внутри |
|------|------|------------|
| **Phase 1: Foundation** (Недели 1-4) | Layer 1: Self-reported energy standalone; Privacy architecture; GDPR consent; Baseline calculation |
| **Phase 2: Health Connect** (Недели 5-8) | Layer 2: Google Health Connect reader; Garmin, Fitbit, Samsung support; Layer 3: Body Battery priority |
| **Phase 3: ML Layer** (Недели 9-12) | Layer 4: TensorFlow Lite on-device; Correlation engine; Feature engineering |
| **Phase 4: Smart Scheduling** (Недели 13-16) | Layer 5: Energy-based recommendations; Calendar integration; Recovery automation |
| **Phase 5: Refinement** (Недели 17-20) | Orthosomnia prevention; Advanced baseline; Performance optimization |

---

## 2.9 Как НЕ делать

### Что точно убьёт продукт

| Антипаттерн | Почему убивает | Пример |
|-------------|---------------|--------|
| **"Body Battery заменяет таблетки"** | Medical misinformation; этическая ответственность | Любое сравнение с фармакологией |
| **Хранение данных на сервере** | Privacy breach; GDPR fine; потеря доверия | "Данные в облаке для better ML" |
| **Сырые цифры без контекста** | Orthosomnia; confusion; abandonment | "HRV: 42 мс" без объяснения |
| **Автопланирование без подтверждения** | Потеря контроля; frustration | "Я перенёс вашу встречу" |
| **Требование wearable для core features** | Excludes 85% пользователей | "Подключите часы для планирования" |
| **Leaderboard / сравнение с другими** | Тревожность; RSD | "Ты на 45-м месте" |
| **"Плохой сон — плохой ты"** | Shame; orthosomnia | "Вы недоспали снова" |
| **Medical diagnosis** | Liability; нет медицинской лицензии | "У вас нарушение сна" |
| **Продажа данных** | Instant trust destruction | "Анонимизированные данные для research" |
| **Сложный onboarding** | 20-30% drop-off на каждом шаге | 10-шаговая настройка перед первым use |

### Orthosomnia Prevention

**6 мер защиты:**
1. НЕ показывать sleep score ежедневно
2. НЕ отправлять push об "плохом сне"
3. Показывать: "Сон — не конкурс. Небольшие вариации нормальны."
4. После 3 дней низких метрик → предложить ОТДОХНУТЬ от трекинга
5. "Digital Detox" раздел — временное отключение wearable-данных
6. Ежемесячный скрининг: "Чувствуете ли вы тревогу из-за данных о сне?"

**Gentle intervention:**
```
┌──────────────────────────────────────────────┐
│  Забота о вашем комфорте                      │
│                                               │
│  Мы заметили, что вы часто проверяете         │
│  метрики сна. Это может добавлять             │
│  беспокойства — а сон должен его убирать.     │
│                                               │
│  Хотите на неделю скрыть детальные            │
│  метрики и оставить только общий тренд?       │
│                                               │
│  [Да, дайте отдохнуть от цифр]               │
│  [Нет, спасибо]                               │
└──────────────────────────────────────────────┘
```

### No Medical Claims

**Запрещённые формулировки → корректные альтернативы:**

| ❌ Запрещено | ✅ Разрешено |
|-------------|-------------|
| "У вас выгорание" | "Энергия ниже вашего обычного уровня 5 дней подряд" |
| "У вас хроническая усталость" | "Наблюдается тренд на снижение энергии" |
| "У вас нарушение сна" | "Сон короче вашего среднего на 30%" |
| "Ваш стресс на критическом уровне" | "Stress score выше вашего baseline" |
| "Рекомендуем обратиться к врачу" | "Если беспокоитесь — проконсультируйтесь со специалистом" |

---

## 2.10 Техническая интеграция

### 2.10.1 API Comparison Matrix

| Платформа | API Type | Доступ в РФ | HRV | Sleep Stages | Energy | Background | Write |
|-----------|----------|-------------|-----|--------------|--------|-----------|-------|
| Google Health Connect | Android SDK | ✅ | ✅ RMSSD | ✅ 4 stages | ❌ (вычисляем) | ✅ Android 15+ | ✅ |
| Garmin Health API | REST API | ⚠️ Niche | ✅ | ✅ + score | ✅ Body Battery | ✅ Webhook | ❌ |
| Samsung Health SDK | Android SDK | ✅ Galaxy Store | ❌ | ✅ + Apnea | ✅ Energy Score | ✅ Foreground | ✅ |
| Huawei Health Kit | HMS SDK | ✅ AppGallery | ❌ | ✅ TruSleep | ❌ Stress only | ✅ | ✅ |
| Xiaomi Mi Band | ❌ Нет API | ✅ | ❌ | Частично | ❌ | ❌ | ❌ |

### 2.10.2 Google Health Connect — Quick Start

```kotlin
// build.gradle
implementation("androidx.health.connect:connect-client:1.1.0")

// AndroidManifest.xml
<uses-permission android:name="android.permission.health.READ_HEART_RATE" />
<uses-permission android:name="android.permission.health.READ_SLEEP" />
<uses-permission android:name="android.permission.health.READ_HEART_RATE_VARIABILITY" />

// Создание клиента
val healthConnectClient = HealthConnectClient.getOrCreate(context)

// Запрос разрешений
val permissions = setOf(
    HealthPermission.getReadPermission(HeartRateRecord::class),
    HealthPermission.getReadPermission(SleepSessionRecord::class),
    HealthPermission.getReadPermission(HeartRateVariabilityRmssdRecord::class)
)

// Чтение сна с ассоциированными данными
val response = healthConnectClient.readRecords(
    ReadRecordsRequest(
        recordType = SleepSessionRecord::class,
        timeRangeFilter = TimeRangeFilter.between(startTime, endTime)
    )
)
```

### 2.10.3 MCP Server Potential

**Model Context Protocol (MCP)** — открытый стандарт для подключения AI-ассистентов к внешним данным.

**Архитектура MCP для health данных:**
```
[AI Assistant] ←MCP (stdio)→ [MCP Server] ←REST API→ [Open Wearables/Spike]
                                                  ↓
                                    [Health Connect | Samsung | Garmin]
```

**Доступные MCP Servers:**
| Server | Поддержка | HIPAA |
|--------|-----------|-------|
| Open Wearables MCP | Health Connect, Samsung Health | ✅ |
| Spike MCP | 500+ устройств | ✅ |
| Nori HealthMCP | Apple Health, Garmin, Oura, WHOOP | ✅ |

**Инструменты (Open Wearables):**
| Tool | Описание |
|------|----------|
| `get_users()` | Список пользователей |
| `get_activity_summary()` | Шаги, калории, HR averages |
| `get_sleep_summary()` | Сон с фазами, качество |
| `get_workout_events()` | Тренировки, тип, длительность |

### 2.10.4 Российская специфика

#### Sanctions Impact

| Платформа | Влияние санкций | Статус в РФ |
|-----------|----------------|-------------|
| Google Health Connect | ⚠️ Косвенное (Google Play ограничен) | Работает на Android, обновления задерживаются |
| Garmin Health API | ❌ Прямое (Garmin ушёл из РФ) | API доступен глобально, устройства не продаются |
| Samsung Health SDK | ⚠️ Косвенное | Galaxy Store работает |
| Huawei Health Kit | ✅ Нет влияния | Полностью доступен, HMS стабилен |
| Xiaomi | ✅ Нет влияния | Устройства продаются, но нет API |

#### Альтернативные App Stores (РФ)

| Store | Health SDKs | Статус |
|-------|-------------|--------|
| **Huawei AppGallery** | HMS Health Kit, Huawei Health | ✅ Активен |
| **Samsung Galaxy Store** | Samsung Health, Health Data SDK | ✅ Активен |
| **RuStore (VK)** | Ограниченный выбор | ⚠️ Развивается |
| Google Play (РФ) | Health Connect | ❌ Ограничен |

#### Приоритет для РФ

```
Рекомендуемый порядок интеграции для РФ:
1. Huawei Health Kit — растущая база, полная доступность
2. Google Health Connect — для остальных Android-устройств
3. Samsung Health Data SDK — Galaxy Watch пользователи
4. Garmin Health API — niche (фитнес-энтузиасты)
```

---
---

# Часть 3: Сводные рекомендации

## 3.1 Приоритет внедрения

### Связь двух фич

```
                    ┌─────────────────────────────────┐
                    │     Пользователь Telegram       │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────▼─────────────────┐
                    │  LAYER 1: Self-reported Energy  │
                    │  (работает для всех, всегда)    │
                    └───────────────┬─────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
   ┌─────────────────┐   ┌─────────────────────┐   ┌──────────────────┐
   │ BODY DOUBLING   │   │   HEALTH CONNECT    │   │  GOOGLE CALENDAR │
   │ via AI          │   │   (wearable data)   │   │  via MCP         │
   │                 │   │                     │   │                  │
   │ • Timer sessions│   │ • HR, HRV, Sleep    │   │ • Create events  │
   │ • Streak counter│   │ • Body Battery      │   │ • Update status  │
   │ • Daily nudge   │   │ • Energy prediction │   │ • Block focus    │
   │ • Recovery      │   │ • Smart scheduling  │   │   time           │
   └────────┬────────┘   └──────────┬──────────┘   └────────┬─────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    ▼
                    ┌───────────────────────────────┐
                    │   ML MODEL (on-device, local) │
                    │                               │
                    │  Input: Self-report + Wearable│
                    │  Output: Energy curve         │
                    │  + Task recommendations       │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   SMART SCHEDULING ENGINE     │
                    │                               │
                    │  • Match tasks to energy      │
                    │  • Suggest optimal times      │
                    │  • Prevent over-scheduling    │
                    │  • Recovery alerts            │
                    └───────────────────────────────┘
```

### Приоритеты по фичам

| Приоритет | Фича | Зачем | Пользователь | Сложность |
|-----------|------|-------|-------------|-----------|
| **P0** | Self-reported energy (1-10) | Работает без wearables, создаёт baseline | 100% | Low |
| **P0** | Body doubling basic (25 мин) | Core feature, ADHD support, retention | 100% | Low |
| **P0** | Streak counter + Two-Day Rule | Habit formation, retention | 100% | Low |
| **P1** | Health Connect integration | Универсальный доступ к wearables | 35% (с wearables) | Medium |
| **P1** | Google Calendar MCP | Friction reduction, blocking focus time | 60% (с Calendar) | Medium |
| **P1** | Energy-based task matching | Суть value proposition | 100% | Medium |
| **P2** | Garmin Body Battery priority | Gold standard energy metric | 5% (с Garmin) | Medium-High |
| **P2** | Samsung Health SDK | Galaxy Watch users | 10% | Medium |
| **P2** | ML prediction (on-device) | Точность рекомендаций | 100% | High |
| **P3** | MCP Server | Унификация API, AI-ready | Dev experience | Medium |
| **P3** | Huawei Health Kit | РФ-специфика | 15% (РФ) | Medium |

### Порядок внедрения

```
Недели 1-2:   MVP Body Doubling (текст, таймер, streak, daily nudge, stats)
Недели 3-4:   Google Calendar MCP + Body Doubling calendar events
Недели 5-6:   Self-reported energy (Layer 1) + energy-based scheduling
Недели 7-8:   Health Connect integration (Layer 2)
Недели 9-10:  Body Battery priority (Layer 3) + Samsung Health SDK
Недели 11-12: ML prediction (Layer 4) - TensorFlow Lite on-device
Недели 13-14: Smart scheduling (Layer 5) - full integration
Недели 15-16: Huawei Health Kit (РФ) + Garmin Health API (niche)
Недели 17-20: MCP Server + refinement + orthosomnia prevention
```

---

## 3.2 Timeline

### Объединённый roadmap

| Фаза | Недели | Body Doubling | Wearable Integration | Calendar/Integrations |
|------|--------|---------------|---------------------|----------------------|
| **MVP** | 1-2 | ✅ 25-мин сессии, чек-ин, streak, daily nudge, stats | ✅ Self-reported energy (standalone) | — |
| **Integration** | 3-4 | ✅ Custom templates, soft recovery | ✅ Baseline calculation engine | ✅ Google Calendar MCP |
| **Health Connect** | 5-8 | ✅ Multiple sessions per day | ✅ Health Connect reader (Garmin, Samsung, Fitbit) | ✅ Focus time blocking |
| **ML + Advanced** | 9-12 | ✅ Energy-aware BD scheduling | ✅ TensorFlow Lite on-device; Body Battery priority | ✅ Calendar energy overlay |
| **РФ + Enterprise** | 13-16 | ✅ Group BD sessions (research) | ✅ Huawei Health Kit; Samsung Energy Score | ✅ Full automation |
| **Optimization** | 17-20 | ✅ Retrospective analytics | ✅ Orthosomnia prevention; Advanced baseline | ✅ MCP Server |

### Gantt-представление

```
Недели:   1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20
          ───────────────────────────────────────────────────────────────
BD MVP    [████████████████████████████████████████]
BD Adv                              [████████████████]
Self-energy [████████████]
Health Conn      [████████████████████████]
Samsung SDK               [████████████]
Garmin API                            [████████]
Huawei Kit                                        [████████]
ML Layer                         [████████████████]
Smart Sched                                [████████████████]
Calendar MCP      [████████████████████████████████████████]
MCP Server                                                  [████████]
```

---

## 3.3 Success Metrics

### 3.3.1 Product Metrics

| Метрика | Описание | Целевое значение | Метод измерения |
|---------|----------|-----------------|-----------------|
| **BD session completion rate** | % завершённых сессий | > 70% | Локальное логирование |
| **BD retention D7** | % вернувшихся на 7-й день | >= 25% | Event tracking |
| **BD retention D30** | % вернувшихся на 30-й день | >= 15% | Event tracking |
| **BD sessions per week (steady state)** | Среднее число сессий | >= 5 | Локальное логирование |
| **Streak >= 7 days** | % пользователей с серией 7+ дней | > 20% | Cohort analysis |
| **Streak >= 66 days** | % дошедших до автоматизма | > 5% | Cohort analysis |
| **Wearable connection rate** | % подключивших wearable | > 40% за 7 дней | Consent event |
| **Daily energy check completion** | % выполненных check-ins | > 70% за день | Локальное логирование |
| **Task-energy alignment score** | Корреляция задач и энергии | > 0.65 | ML output |
| **Productivity self-report** | "Насколько продуктивным был день" | +0.5 за 30 дней | Ежедневный опрос |

### 3.3.2 Сравнение: С wearable vs Без wearable

| Метрика | С wearable | Без wearable | Гипотеза |
|---------|-----------|-------------|----------|
| Retention D30 | 55% | 45% | Wearable users more engaged |
| Avg energy check completion | 82% | 65% | Awareness drives engagement |
| Task completion rate | 78% | 70% | Better alignment |
| Self-reported productivity | 7.2/10 | 6.4/10 | Correlation insights help |
| Feature satisfaction (NPS) | 45 | 35 | Enhanced experience |

### 3.3.3 Privacy Metrics

| Метрика | Целевое значение | Почему важно |
|---------|-----------------|--------------|
| Opt-in rate for wearable | > 50% | Высокий opt-in = доверие |
| Consent withdrawal rate | < 5% | Низкий = доверие сохраняется |
| Data deletion requests | < 1% | Минимальные = прозрачность |
| Support requests (privacy) | < 0.1% | Мало вопросов = понятная политика |

### 3.3.4 Health Tracking Metrics (orthosomnia prevention)

| Метрика | Целевое значение | Метод |
|---------|-----------------|-------|
| Orthosomnia screening positive rate | < 8% | Ежемесячный опрос |
| Users taking "digital detox" breaks | > 15% | Engagement с feature |
| User-reported anxiety from tracking | < 3% | Ежеквартальный опрос |

### 3.3.5 North Star Metric

**"Фокус-часов в неделю"** — совокупная метрика:

```
Focus Hours per Week = 
  (completed BD sessions × avg duration) / 60
  + (tasks completed during energy peak / 60)
  + (self-reported productive hours)
```

**Почему эта метрика:**
- Отражает core value proposition (фокус + энергия)
- Коррелирует с retention (больше фокуса → больше ценности)
- Объединяет обе фичи (BD + wearable)
- Легко измеряется

---

## 3.4 Risk Matrix

### 3.4.1 Body Doubling Risks

| Риск | Вероятность | Влияние | Уровень | Митигация |
|------|-------------|---------|---------|-----------|
| Effect size на больших выборках ниже | Medium | High | 🔴 **High** | Закладываем buffer: d = 0.5 вместо 0.9 |
| User churn после 1-й неудачной сессии | High | Medium | 🟡 **Medium** | Soft recovery flow; shame-free messaging |
| Feature не дотягивает до "волшебного момента" | Medium | High | 🔴 **High** | Quick first session; focus on "presence" feeling |
| Notification fatigue | Medium | Medium | 🟡 **Medium** | Smart timing; max 2 pushes/day |
| Коучинг вытесняет BD | Low | Medium | 🟡 **Medium** | Position as complementary; hybrid model |

### 3.4.2 Wearable Integration Risks

| Риск | Вероятность | Влияние | Уровень | Митигация |
|------|-------------|---------|---------|-----------|
| Health Connect permissions revoked | Medium | Medium | 🟡 **Medium** | Graceful degradation to self-report |
| Wearable data unreliable (no-name devices) | High | Medium | 🟡 **Medium** | Quality scoring; data validation |
| Orthosomnia | Medium | High | 🔴 **High** | 6 prevention measures; digital detox |
| Privacy breach perception | Low | Critical | 🔴 **High** | Zero-knowledge architecture; local processing |
| Garmin/Huawei API changes | Medium | Medium | 🟡 **Medium** | Abstraction layer; Health Connect as buffer |
| Sanctions impact (Garmin, Google) | Medium | Medium | 🟡 **Medium** | Huawei Health Kit as primary for РФ |

### 3.4.3 Сводная таблица рисков

| Риск | Severity | Probability | Impact | Приоритет митигации |
|------|----------|-------------|--------|-------------------|
| Effect size оказался overestimated | 4/5 | 3/5 | **12** | P1: Buffer + fallback metrics |
| Privacy breach / GDPR | 5/5 | 1/5 | **5** | P0: Zero-knowledge architecture |
| Orthosomnia | 4/5 | 2/5 | **8** | P1: 6 prevention measures |
| API deprecation / sanctions | 3/5 | 3/5 | **9** | P2: Abstraction layer |
| High churn post-first session | 3/5 | 4/5 | **12** | P1: Soft recovery + Two-Day Rule |
| No wearable API (Xiaomi) | 2/5 | 5/5 | **10** | P2: Google Fit bridge |

### 3.4.4 Go/No-Go Criteria

| Checkpoint | Критерий Go | Дата проверки |
|------------|-------------|---------------|
| **MVP (неделя 2)** | > 40% activation rate; < 60-sec time-to-first-session | Неделя 2 |
| **Health Connect (неделя 8)** | > 30% wearable connection rate; < 5% consent withdrawal | Неделя 8 |
| **ML Layer (неделя 12)** | Energy prediction accuracy > 65% (vs self-report) | Неделя 12 |
| **Smart Scheduling (неделя 16)** | Task-energy alignment > 0.60 correlation | Неделя 16 |
| **Launch readiness (неделя 20)** | Zero privacy incidents; < 3% medical claims complaints; NPS > 30 | Неделя 20 |

---

## Приложения

### Приложение A: Чек-листы

#### Pre-launch Checklist

**Body Doubling:**
- [ ] Все 7 stages customer journey реализованы
- [ ] Two-Day Rule работает корректно
- [ ] Recovery flow после пропуска тестирован
- [ ] Soft abort ("стоп") работает без штрафа
- [ ] Google Calendar MCP интегрирован
- [ ] Stats dashboard показывает streak, фокус-часы
- [ ] Daily nudge отправляется в настроенное время
- [ ] Custom templates (3+) доступны
- [ ] Medical disclaimer добавлен

**Wearable Integration:**
- [ ] Все 10 DOs реализованы
- [ ] Все 10 DON'Ts проверены (не нарушаются)
- [ ] Privacy nutrition label опубликован
- [ ] GDPR consent flow протестирован
- [ ] Opt-out работает за < 5 секунд
- [ ] Работает без wearable (Layer 1 only)
- [ ] Medical disclaimer добавлен
- [ ] Orthosomnia screening включён
- [ ] Manual override доступен на каждом экране
- [ ] Audit trail логирует все обращения к данным

#### Daily Monitoring Checklist

- [ ] Wearable connection rate стабилен
- [ ] Energy check completion rate > 70%
- [ ] BD session completion rate > 70%
- [ ] Нет жалоб на медицинские формулировки
- [ ] Opt-out requests обработаны в течение 24 часов
- [ ] ML inference time < 50ms (p99)
- [ ] Локальное хранилище не переполнено

### Приложение B: Privacy Nutrition Label

```
┌──────────────────────────────────────────────┐
│  ДАННЫЕ, КОТОРЫЕ МЫ НЕ СОБИРАЕМ:           │
│  ❌ Health data не покидает устройство       │
│  ❌ Нет рекламных трекеров                   │
│  ❌ Нет аналитики третьих лиц                │
│  ❌ Нет cloud ML processing                  │
│  ❌ Нет продажи данных                       │
│                                              │
│  Мы финансируемся через подписку,            │
│  а не через ваши данные.                     │
└──────────────────────────────────────────────┘
```

### Приложение C: Эмодзи-код для AI-коуча

| Эмодзи | Значение | Когда использовать |
|--------|----------|-------------------|
| 🎯 | Фокус / цель | Check-in, начало сессии |
| ✅ | Завершение | Сессия выполнена |
| 🌊 | Присутствие | Silent body doubling |
| 🔥 | Streak / серия | Мотивация, статистика |
| 💡 | Идея / совет | Подсказки |
| 🛑 | Пауза / стоп | Прерывание |
| 🎉 | Празднование | Milestones |
| 📅 | Календарь | Интеграция с GC |
| ⚡ | Энергия | Energy-aware features |
| 🤝 | Body doubling | Весь контекст фичи |
| 🔒 | Privacy | Consent, security |
| 📊 | Аналитика | Отчёты, stats |
| ☀️ | Утро | Morning energy check |
| 🟢 | Пик энергии | High energy period |
| 🟡 | Средняя энергия | Medium energy period |
| 🔴 | Спад энергии | Low energy period |

### Приложение D: Тональность сообщений

| Принцип | Применение |
|---------|------------|
| **Честность без паники** | Говорим о проблемах прямо, но без драматизации |
| **Объясняем почему** | Каждая рекомендация — с reasoning |
| **Уважаем автономию** | Предупреждаем, но не принуждаем |
| **Локальность данных** | Повторяем: данные на телефоне, никуда не уходят |
| **Не врач** | Никаких медицинских диагнозов |
| **Конкретика** | "Перенеси на 10:00" лучше "сделай когда будет энергия" |
| **Обучаем** | Каждый touchpoint — возможность научить |

### Приложение E: Типовые ответы на возражения

**"У меня нет часов"**
> Не нужны! Самооценка энергии (1-10) утром — это 80% ценности. Часы просто добавляют точность. Начни без них, подключишь потом.

**"Я не хочу отдавать данные здоровья"**
> Полностью понимаю. Все данные остаются на твоём телефоне — я не отправляю их никуда. Локальная обработка, zero-knowledge. Можешь проверить код или отключить в любой момент.

**"Это работает?"**
> Для людей с ADHD и прокрастинацией body doubling показывает effect size 0.85-0.90 в исследованиях. AI body double статистически неотличим от человеческого (p=1.000). Но каждый человек уникален — попробуй и решишь сам.

**"Мне неудобно писать каждый день"**
> Можно настроить автоматический режим: я буду читать данные с часов и давать рекомендации без вопросов. Или уменьшить частоту до 1 раза в день. Ты контролируешь.

**"А если я заболею?"**
> Все рекомендации — корреляция, не диагностика. Если плохо себя чувствуешь — прислушайся к себе, а не к цифрам. Я не врач и не заменяю медицинскую консультацию.

---

## Полный список исследований (inline ссылки)

### Body Doubling — Исследования

1. [Ara et al., 2025 — AI vs Human Body Doubling in VR, dz = -0.90, p = 0.006](https://arxiv.org/abs/2509.12153)
2. [Eagle et al., 2024 — ADHD Body Doubling Survey, N=220, ACM ASSETS](https://leyabreanna.com/papers/body_doubling.pdf)
3. [O'Connell et al., 2024 — Co-working Robot for ADHD, HRI '24](https://dl.acm.org/doi/10.1145/3610977.3634929)
4. [FLOWN/Elise Ertubey — Virtual Co-working Cohort, N=117](https://www.smithsonianmag.com/innovation/can-virtual-coworking-platforms-make-us-more-productive-180984439/)
5. [Harkin et al., 2016 — Meta-analysis Progress Monitoring, d=0.40](https://goalsandprogress.com/accountability-psychology-research/)
6. [Matthews, 2015 — Goals + Accountability 76% vs 43%](https://dominican.edu/dominican-news/study-reveals-writing-down-goal-helps-achieve-goals)
7. [Social Presence Meta-analysis — PRISMA, g=0.30, 33 studies](https://pmc.ncbi.nlm.nih.gov/articles/PMC12717298/)
8. [Zajonc, 2001 — Mere Presence Effect](https://pubmed.ncbi.nlm.nih.gov/11372565/)
9. [DeskTime, 2014 — 52/17 Rule, Top 10% Users](https://desktime.com/blog/52-17-updated)
10. [Cirillo, 2006 — Pomodoro Technique](https://www.amazon.com/Pomodoro-Technique-Francesco-Cirillo/dp/398156790X)
11. [Lally et al., 2010 — Habit Formation 66 days](https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674)
12. [Prevatt & Yelland, 2015 — ADHD Coaching, d=0.89](https://files.eric.ed.gov/fulltext/EJ1182373.pdf)
13. [Amabile & Kramer, 2011 — Progress Principle, HBS](https://hbr.org/2011/05/the-power-of-small-wins)

### Wearable — Исследования

14. [Nelson et al., 2017 — Apple Watch HRV Accuracy, r=0.96 vs ECG](https://pubmed.ncbi.nlm.nih.gov/28952697/)
15. [Ghambari et al., 2022 — Garmin HRV Validity, r=0.92](https://pubmed.ncbi.nlm.nih.gov/35275576/)
16. [Lu et al., 2009 — Polar HRV Gold Standard, r=0.98](https://pubmed.ncbi.nlm.nih.gov/19377114/)
17. [Kinnunen et al., 2020 — Oura HRV Accuracy, r=0.83-0.92](https://pubmed.ncbi.nlm.nih.gov/32353867/)
18. [Grande et al., 2024 — Garmin Body Battery vs POMS, r=0.57](https://pubmed.ncbi.nlm.nih.gov/39122733/)
19. [Baron et al., 2017 — Orthosomnia, JCSM](https://pubmed.ncbi.nlm.nih.gov/27956782/)
20. [Cabitza et al., 2017 — Human-in-the-Loop, Nature](https://pmc.ncbi.nlm.nih.gov/articles/PMC5544262/)

### Рынок и технологии

21. [Android Market Share Russia — StatCounter, 65.17%](https://gs.statcounter.com/os-market-share/mobile/russian-federation)
22. [Google Health Connect SDK](https://developer.android.com/health-and-fitness/guides/health-connect)
23. [Garmin Health API Documentation](https://developer.garmin.com/gc-developer-program/health-api/)
24. [Samsung Health Data SDK](https://developer.samsung.com/health/data/overview.html)
25. [Huawei Health Kit](https://developer.huawei.com/consumer/en/doc/overview-0000001147638696)
26. [Open Wearables MCP Server](https://www.themomentum.ai/blog/talk-to-your-wearable-data-how-open-wearables-mcp-server-connects-health-metrics-to-ai-assistants)
27. [Samsung Energy Score Explained](https://www.trustedreviews.com/explainer/what-is-samsung-energy-score-4542399)
28. [GDPR Article 9 — Health Data](https://gdpr-info.eu/art-9-gdpr/)

### Продуктовые референсы

29. [Focusmate — Media Kit, 143% productivity](https://www.focusmate.com/media-kit/)
30. [FLOWN — Deep Work Cohorts](https://flown.com/body-doubling)
31. [DeskTime — 52/17 Rule](https://desktime.com/blog/52-17-updated)
32. [Pomodoro Meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC5063223/)

---

> **Документ собран из 10 исследовательских файлов:**
> - wearable_stats_russia.md
> - bd_01_science.md
> - bd_02_market_ux.md
> - bd_03_customer_journey.md
> - bd_04_calendar_mcp.md
> - bd_05_methodology.md
> - we_01_wearable_science.md
> - we_03_customer_journey.md
> - we_04_tech_integration.md
> - we_06_methodology.md
>
> **150+ научных и продуктовых источников.**
> **Документ готов к применению "из коробки"** — все шаблоны сообщений, customer journeys, технические спецификации и privacy-архитектура.

---

*Финальный документ-методология: Body Doubling via AI + Wearable Energy Integration для life-planning-coach.*
*Версия 1.0 | 2025*


---

### Special Scenarios: Body Doubling

#### S1: Soft Abort ("стоп")

**Trigger:** Пользователь пишет "стоп" во время сессии
**Timing:** Любой момент сессии

**Text (Claude → User):**

```
🛑 Сессия прервана. Это нормально.

Что фиксирую:
• Задача: [задача]
• Прогресс: [N] минут из [X]
• Статус: 🔄 Частично

Это не "провал" — это данные. 
Каждая сессия, даже прерванная, тренирует 
мозг к фокусу.

Что будем делать?
[Продолжить ту же задачу] [Новая сессия]
[Вернуться позже] [Расскажи, что помешало]
```

**Calendar update:**
```
UPDATE event:
  title: "🛑 [задача] (прервано на [N] мин)"
  description: "Прогресс: [N]/[X] минут. Статус: частично."
  color: yellow
```

---

#### S2: Hard Abort (2+ раз подряд)

**Trigger:** Пользователь прерывает 2+ сессии подряд
**Timing:** После второго прерывания

**Text (Claude → User):**

```
🛑 Вторая сессия подряд прервана. 
Давай разберёмся — не для оценки, а чтобы 
помочь.

Возможные причины (выбери или напиши свою):
[😴 Не хватает энергии] 
[📱 Отвлеклись (уведомления, люди)]
[🎯 Задача слишком большая / страшная]
[⏰ Нет времени — начал(а) поздно]
[🧠 "Не могу собраться" — туман в голове]
[🔄 Просто так получилось]

Я не буду использовать это против тебя. 
Только чтобы подстроиться.
```

**Response handling:**

| Ответ | Action |
|-------|--------|
| 😴 Не хватает энергии | Offer energy check + shorter session (10 min) |
| 📱 Отвлеклись | Suggest DND mode + "focus mode" activation |
| 🎯 Задача слишком большая | Task splitting: "Давай разобьём на 5-минутные куски" |
| ⏰ Нет времени | Reschedule prompt: "Когда точно будет время?" |
| 🧠 Туман в голове | Body scan technique: "Давай 2 минуты просто сидеть с задачей" |
| 🔄 Просто так | Normalize: "Бывает. Начнём с чистого листа?" |

---

#### S3: Burnout Protection

**Trigger:** 5+ дней подряд высокой интенсивности (сессии 45+ мин, много задач)

**Text (Claude → User):**

```
🌊 Я заметил, что последние 5 дней ты 
в режиме «полный вперёд».

• Сессий: [N] (больше обычного на [X]%)
• Средняя длительность: [X] мин
• Задач выполнено: [N]

Это впечатляет. И это сигнал: 
организм накапливает нагрузку.

**Рекомендация на сегодня:**
→ Сократить сессию до 15 мин
→ Или пропустить день (Two-Day Rule позволяет)
→ Или сделать одну сессию на «лёгкое дело»

Постоянный спринт — это марафон, который 
рано или поздно заканчивается. 
Давай сбавим до комфортного темпа.

[Сократить сегодня] [Пропустить день] 
[Продолжить как есть — я ок]
```

---

#### S4: ADHD Overwhelm ( Executive Dysfunction Spike)

**Trigger:** Пользователь пишет о paralysis, "не могу начать ничего", "много задач, не знаю с чего"

**Text (Claude → User):**

```
🧠 Понимаю. Это executive dysfunction — 
когда мозг видит 100 задач и не может 
выбрать одну.

**Вот что работает прямо сейчас:**

1. Закрой глаза (да, прямо сейчас)
2. Открой — и выбери САМУЮ МАЛЕНЬКУЮ задачу
3. Не планируй. Не приоритизируй. 
   Просто одну мелочь.

Примеры "мелочей":
→ Открыть документ и написать одно предложение
→ Отправить одно письмо
→ Прочитать одну страницу
→ Заполнить одно поле в форме

Я запущу 10-минутную сессию. 
Только на эту одну мелочь. Не больше.

[Начать 10 мин] [Мне нужен список мелочей]
[Просто поговори со мной] [Не сейчас, спасибо]
```

---

#### S5: Morning Executive Dysfunction

**Trigger:** Утренний daily nudge + пользователь не отвечает или отвечает "не могу"

**Text (Claude → User):**

```
☀️ Утро. Мозг ещё не разогрелся — это нормально.

Давай не будем выбирать "важную задачу".
Давай просто сделаем 10 минут на что угодно.

**Случайная задача (жми, не думай):**
[🎲 Дай случайную из моего списка]
[📋 Самая маленькая из важных]
[🧹 Что-то рутинное (заварить кофе, написать 
   2 строчки)]

Главное — не выбирать. Главное — начать.
10 минут. Я рядом.
```

---

### Special Scenarios: Wearable Energy

#### S6: Wearable не передаёт данные

**Trigger:** Нет данных из Health Connect > 2 часа
**Timing:** Автоматическая проверка каждые 30 мин

**Text (Claude → User):**

```
⚠️ Нет данных с часов уже [N] часов.

Я не получаю обновления из Google Health Connect 
с [время]. Вот что проверить:

**Частые причины:**
1. 🔋 Часы разряжены — проверьте, включены ли
2. 📡 Bluetooth отключён
3. 🔄 Приложение часов не синхронизировано — 
   откройте [watch_app], подождите обновления
4. 🚫 Доступ к Health Connect сбросился

**Пока данные не приходят:**
Я переключаюсь в ручной режим. 
Скажите: «энергия [N] из 10» — и я продолжу.

[Проверить Bluetooth] [Открыть {watch_app}]
[Проверить разрешения] [Переключиться на ручной]
```

---

#### S7: Данные аномальные (болезнь, плохой сон)

**Trigger:** Body Battery или другие метрики выходят за персональные границы (z-score > 2.5)

**Text (Claude → User):**

```
🤒 Аномальные показатели

Я заметил отклонения:

🔋 Body Battery: [current] (обычно [normal])
❤️ Пульс в покое: [hr] (обычно [normal_hr])
😴 Сон: [sleep_data]

**Возможные причины:**
• 🤒 Начинающаяся простуда (HR в покое 
  подскакивает за 1-2 дня до симптомов)
• 😰 Стресс / тревожность
• 🍷 Алкоголь накануне
• 🏋️ Перетренированность

**Что я делаю:**
→ Снижаю ожидания на сегодня
→ Не рекомендую сложные задачи
→ Отмечаю в отчёте

**Важно:** Я не врач и не ставлю диагнозы. 
Если чувствуете недомогание — прислушайтесь 
к себе, а не к цифрам.

[Понятно, бережный режим] [Я просто плохо спал]
[Я болею, отмени задачи] [Всё нормально]
```

---

#### S8: Пользователь отключил доступ

**Trigger:** Health Connect permissions revoked

**Text (Claude → User):**

```
🚫 Доступ к данным отключён

Я не могу прочитать данные с часов — доступ 
к Google Health Connect был отозван.

**Почему это могло произойти:**
• Вы отключили разрешение в настройках Android
• Android автоматически отозвал доступ 
  после периода неактивности
• Обновление системы сбросило разрешения

**Варианты:**
🔄 **Восстановить доступ** — открываю настройки...
✍️ **Перейти на ручной ввод** — буду спрашивать 
   энергию утром
⏸️ **Приостановить energy-функцию** — работаем 
   как обычный планировщик

Ваши данные никуда не делись — они всё ещё 
в Health Connect на вашем телефоне. Я просто 
не могу их читать без разрешения.

[Восстановить доступ] [Перейти на ручной ввод]
[Приостановить]
```

---

#### S9: Смена устройства (новые часы)

**Trigger:** Обнаружено новое устройство в Health Connect

**Text (Claude → User):**

```
⌚ Обнаружено новое устройство

Я вижу, что теперь данные приходят с 
[new_device] вместо [old_device]. Сменили часы?

**Что происходит:**
• [new_device] использует метрику: [metric]
• Диапазон: [new_range] (раньше [old_range])
• Частота обновления: [new_frequency]

**Ваш baseline:**
Я сохраню исторический профиль, но скорректирую 
под новую метрику. Body Battery Garmin (1-100) 
и Energy Score Samsung (0-100) похожи, но не 
идентичны — потребуется 2-3 дня для калибровки.

**Прогноз на сегодня может быть менее точным** — 
пока я изучаю, как новая метрика соотносится 
с вашими реальными ощущениями.

Скажите мне сегодня вечером, насколько прогноз 
совпадал с реальностью — это ускорит калибровку.

[Да, сменил часы] [Это временно]
[Покажи, как настроить] [Вернуть старое]
```

---

#### S10: Низкая battery на wearable

**Trigger:** Часы разряжены (< 20%) или данные не обновлялись

**Text (Claude → User):**

```
🔋 Часы разряжены ([battery_pct]%)

Ваши [device_name] на исходе. Когда выключатся 
— я перестану получать данные.

**Оценка:** заряда хватит примерно до 
[estimated_shutdown_time].

**Варианты:**
• ⚡ Поставьте на зарядку сейчас — через 30 мин 
  данных хватит до вечера
• 📵 Оставьте как есть — переключусь в ручной 
  режим когда данные кончатся
• 🔌 Поставьте на ночь — завтра всё будет работать

**Совет:** Если ставите на ночь — включите 
«театральный режим», чтобы экран не светил.

[Напомни зарядить через час] 
[Переключись в ручной режим]
[Не беспокоить]
```

---

## Feature Engineering для ML-модели (Layer 4)

```python
# Входные фичи (все вычисляются локально)
features = {
    # Layer 1: Self-reported
    'energy_self_morning': 7,        # 1-10
    'energy_self_afternoon': 6,
    'energy_self_evening': 5,

    # Layer 2: Health Connect (normalized 0-1)
    'hr_resting': 58,                # bpm
    'hrv_rmssd': 42,                 # ms
    'sleep_duration': 7.2,           # hours
    'sleep_efficiency': 0.85,
    'steps_yesterday': 8200,
    'deep_sleep_ratio': 0.18,

    # Layer 3: Body Battery (if available)
    'body_battery_current': 67,
    'body_battery_trend_3d': -0.05,  # negative = declining

    # Time features
    'day_of_week': 2,                # 0=Monday
    'hour_of_day': 9,
    'is_weekend': False,

    # Historical
    'energy_7d_avg': 6.4,
    'energy_7d_std': 1.2,
    'productivity_correlation': 0.58,
}

# Модель: lightweight gradient boosting
# Размер: < 5MB
# Inference time: < 50ms on mid-range Android
# Update frequency: ежемесячно (differential update)
```

---

## Recovery Signals из Wearables (Integration Protocol)

| Wearable Signal | Recovery Protocol Trigger | Сообщение |
|-----------------|---------------------------|-----------|
| Body Battery < 20 на 2+ дня | Active Recovery Day | "Запас энергии низкий — рекомендуем день лёгких задач" |
| HRV < личного baseline на 20% | Stress Recovery | "Вариабельность пульса снижена — попробуйте дыхательную технику" |
| Sleep < личного baseline на 30% | Sleep Recovery | "Недостаточно восстановления — учитывайте при планировании" |
| Body Battery не восстанавливается ночью | Extended Recovery | "Ночного восстановления недостаточно — возможно, стоит сократить нагрузку" |
| HR в покое > baseline на 10+ bpm | Overreaching Alert | "Пульс в покое выше обычного — возможно, организм восстанавливается от нагрузки" |

---

*Дополнительные специальные сценарии и технические спецификации для production-ready интеграции.*

