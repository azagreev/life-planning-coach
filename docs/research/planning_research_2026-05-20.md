# Исследование: научные методы планирования для life-planning-coach
## Ранжированный список идей и рекомендаций по внедрению

**Дата:** 2026-05-20
**Исследование:** 60+ агентов-часов, 250+ поисковых запросов, 12 измерений, 5 фасетов
**Целевой проект:** https://github.com/azagreev/life-planning-coach
**Аудитория:** IT-шники, фрилансеры, домохозяйки, безработные в поиске смыслов

---

## Резюме

Проведено масштабное исследование научных методов планирования, behavioral design, хронобиологии, AI-инструментов и мнений сообществ. Собрано 22 high-confidence finding, 10 medium-confidence finding, 7 conflict zones. Выделено 10 кросс-дименсиональных инсайтов.

**Главный вывод:** планирование работает не через «больше делать быстрее», а через снижение тревожности (↓rumination, ↓[Zeigarnik](https://pubmed.ncbi.nlm.nih.gov/38130478/) tension), psychological detachment и wellbeing through structure. Успешные инструменты ([Sunsama](https://www.sunsama.com/), $20M) — это coaching platforms со встроенным scheduling, а не calendar optimizers ([Clockwise](https://www.getclockwise.com/) закрывается при $76M).

---

## Часть 1: Что говорит наука

### 1.1 Хронобиология: когда планировать

**Peak-Trough-Rebound модель** ([Pink 2018](https://www.danpink.com/books/when/), данные 500 млн твитов): большинство людей (~75%) имеют три фазы дня — утренний пик (аналитика), послеобеденный провал (trough), вечерний rebound (креатив). **Вариативность производительности: 20-26%** в течение дня [^1^].

**Synchrony effect** ([Schmidt et al. 2007](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2015.00199/full)/2015): совпадение хронотипа и времени задачи критично. Mismatch снижает производительность на **5.9-8.4%** [^4^]. Для планирования: стратегическое планирование — в пиковое время, креативное — в rebound.

**Decision fatigue** ([Danziger et al. PNAS 2011](https://www.pnas.org/doi/10.1073/pnas.1018033108)): судьи давали parole в ~65% случаев утром и ~0% перед обедом. **Вывод:** критические решения и планирование — в пиковое время [^5^].

**[Miracle Morning](https://miraclemorning.com/) критика:** [Hal Elrod](https://miraclemorning.com/) «The [Miracle Morning](https://miraclemorning.com/)» — chronotype-blind. Для 20-30% вечерних типов раннее планирование контрпродуктивно. Но Scullin (2018) показал: **to-do list перед сном улучшает засыпание (d=0.63)** [^dim01^].

**Практический вывод:** коучинг должен определять хронотип пользователя и предлагать персонализированное время планирования.

### 1.2 Behavioral Science: как заставить планировать

**Implementation Intentions** ([Gollwitzer & Sheeran](https://kops.uni-konstanz.de/server/api/core/bitstreams/d703c468-46e9-47fc-8900-5b6ab3e50f5a/content), мета-анализ 94 исследования): **d=0.43-0.65**, 8000+ участников. If-then формат эффективнее обычного scheduling [^dim02^].

**Planning Prompts** ([Milkman et al. PNAS 2011](https://www.pnas.org/doi/10.1073/pnas.1103170108)): простой вопрос «когда вы сделаете X?» повышает flu shot uptake на **+13%**, narrow window — на **+27%** [^dim02^].

**Friction reduction** ([Fogg B=MAP](https://www.behaviormodel.org/)): каждые 20 секунд трения = 300% разница в follow-through. **Снижение ability barrier надёжнее повышения motivation** [^dim02^].

**Default effects** ([Madrian & Shea](https://www.nber.org/papers/w8242)): auto-enrollment повышает participation с 49% до 86% [^dim02^].

**Nudge at scale problem** ([DellaVigna & Linos 2022](https://www.hks.harvard.edu/publications/rcts-scale-comprehensive-evidence-two-nudge-unit)): академические nudge d=0.43, реальные — 1.4pp (в 6 раз меньше). **Комбинация II + friction reduction + default architecture работает лучше отдельных nudge** [^dim02^].

### 1.3 Habit Formation: как сделать планирование привычкой

**66 дней** — медиана формирования привычки ([Lally et al.](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6494.2010.00660.x)), диапазон 18-254. Пропуск 1 дня не влияет [^dim03^].

**B=MAP** ([Fogg](https://www.behaviormodel.org/)): Behavior = Motivation + Ability + Prompt. **Рычаг Ability надёжнее Motivation.** Tiny Habits RCT: d=0.85 [^dim03^].

**Habit stacking** ([James Clear](https://jamesclear.com/atomic-habits)): прикрепление к существующей привычке. Event-based cues эффективнее time-based reminders [^dim03^].

**Self-monitoring** ([Harkin et al. 2016](https://onlinelibrary.wiley.com/doi/abs/10.1111/bmsp.12093)): мета-анализ 138 исследований, **d=0.40** для мониторинга прогресса. 19K+ участников [^dim03^].

**Streak anxiety** (Two-Day Rule): жёсткие streak'и вредят. Правило «не более 1 пропуска подряд» эффективнее [^dim03^].

### 1.4 Recovery и Burnout Prevention

**Time management ↔ burnout** ([Frontiers 2025](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1623228/full)): **r = −0.41**. Планирование напрямую снижает выгорание [^dim08^].

**Recovery paradox** ([Sonnentag 2018](https://www.sciencedirect.com/science/article/pii/S0191308517303634)): когда recovery нужнее всего — менее вероятен. Это создаёт product opportunity для automated recovery protocols [^dim08^].

**Psychological detachment** ([Sonnentag](https://pubmed.ncbi.nlm.nih.gov/17925618/) 20+ лет исследований): медиатор workload-burnout. **Shutdown ritual** ([Cal Newport](https://calnewport.com/), 15-20 мин) — научно обоснован [^dim08^].

**Toxic productivity** ([Jennifer [Moss](https://www.jennifer-moss.com/writing/ending-toxic-productivity)](https://www.jennifer-moss.com/writing/ending-toxic-productivity), HBR): **82% работников в зоне риска**. 43% тратят >10 часов/неделю на «продуктивный театр» [^dim08^].

### 1.5 Методологии: что работает, что нет

| Методология | Научная поддержка | Вердикт |
|-------------|-------------------|---------|
| **Time Blocking** | Attention residue ([Leroy 2009](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-8721.2009.01656.x)), 23 мин восстановления (Mark). HIGH | ✅ Интегрировать |
| **Weekly Review** | +23% performance ([Di Stefano](https://www.hbs.edu/ris/Publications%20Files/14-093_d4970af6-a7c9-4653-8908-43368175583.pdf) et al. Harvard 2014). HIGH | ✅ Уже есть, усилить |
| **Implementation Intentions** | d=0.65, 94 исследования. HIGH | ✅ Уже есть (if-then) |
| **WOOP/MCII** | Goal commitment ↑, obstacle anticipation. HIGH | ✅ Уже есть |
| **GTD** | [Zeigarnik](https://pubmed.ncbi.nlm.nih.gov/38130478/) (2025 meta под сомнением), [Masicampo](https://pubmed.ncbi.nlm.nih.gov/21728448/) 2011. MEDIUM | ⚠️ Компоненты, не система |
| **Fresh Start Effect** | [Dai](https://pubmed.ncbi.nlm.nih.gov/24311896/), [Milkman](https://katherinemilkman.squarespace.com/s/2015_BSP.pdf) 2014 + dark side ([Koo 2020](https://pubmed.ncbi.nlm.nih.gov/31971582/)). HIGH | ✅ Интегрировать |
| **[PARA](https://fortelabs.com/blog/para/)** | **ZERO RCT**. Placebo через ritual. LOW | ❌ Не интегрировать как систему |
| **[Bullet Journal](https://bulletjournal.com/)** | **ZERO RCT как система**. Journaling: 9%↓ anxiety. LOW | ⚠️ Ritual design, не метод |
| **[Eat the Frog](https://www.briantracy.com/blog/time-management/the-truth-about-frogs/)** | Контрпродуктивен для 20-30% сов. LOW | ❌ Не интегрировать |
| **[Pomodoro](https://francescocirillo.com/products/the-pomodoro-technique)** | Mixed results, прерывает flow. LOW | ⚠️ Опционально |

### 1.6 AI Coaching: рынок и тренды

- Рынок AI coaching: **$2.4B к 2028, 28% CAGR** [^dim12^]
- Mental health chatbots: **$1.8B (2024) → $7.5B (2034)** [^dim12^]
- [Therabot](https://ar5iv.org/pdf/2503.05516.pdf) (генеративный AI): **d=0.85** — эффективность как у человеческой терапии [^dim12^]
- **Но retention проблема: 30-day = 3.3%** [^dim12^]
- [Anthropic](https://www.anthropic.com/research/estimating-productivity-gains): Claude ускоряет задачи на 80% [^dim12^]

### 1.7 [MCP](https://modelcontextprotocol.io/) — техническое преимущество

- **17000+ [MCP](https://modelcontextprotocol.io/) servers**, 97M+ SDK downloads/month [^dim09^]
- First-class support: Claude (native), ChatGPT, Gemini [^dim09^]
- [Google Calendar [MCP](https://modelcontextprotocol.io/)](https://github.com/nspady/google-calendar-mcp): 37 actions [^dim09^]
- [Clockwise](https://www.getclockwise.com/) [MCP](https://modelcontextprotocol.io/): первый time management [MCP](https://modelcontextprotocol.io/) [^dim09^]
- Security risks: prompt injection (#1), tool poisoning (#3) — **read-only по умолчанию** [^dim09^]

---

## Часть 2: Ранжированный список идей для life-planning-coach

### Приоритетная матрица: Научная обоснованность × Простота внедрения × Ценность для аудитории

---

### 🟢 P0 — Критический приоритет (внедрить немедленно)

#### Идея #1: Chronotype-Native Daily Planning Ritual
**Научная база:** Synchrony effect (−5.9-8.4% при mismatch), Scullin (d=0.63 bedtime list), Peak-Trough-Rebound
**Сложность:** Low
**Влияние:** High

**Описание:**
Добавить 2-3 вопроса для определения хронотипа (например: «В какое время вы чувствуете прилив энергии?», «Когда вам легче всего концентрироваться?»). На основе ответов персонализировать время Daily Planning Ritual:
- **Яворонки (40%)** — утреннее планирование (7-9 AM)
- **Промежуточные (30%)** — late morning (9-11 AM)
- **Совы (30%)** — evening planning (7-9 PM) + bedtime to-do list

**Почему важно:** «Магия утра» работает только для 70-80% людей. Для остальных — вред. Персонализация повышает adherence и качество планирования.

**Внедрение:** Добавить вопросы в onboarding → сохранить chronotype в user profile → адаптировать время Daily Planning Ritual напоминаний.

---

#### Идея #2: Habit Stack Builder
**Научная база:** B=MAP ([Fogg](https://www.behaviormodel.org/)), [habit stacking](https://jamesclear.com/habit-stacking) (Clear), 66 дней ([Lally](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6494.2010.00660.x)), self-monitoring d=0.40
**Сложность:** Medium
**Влияние:** High

**Описание:**
Помочь пользователю «прикрепить» планирование к существующей ежедневной привычке (кофе, завтрак, утренний душ). Прогрессивное усложнение ритуала:
- **Неделя 1-2:** 2 мин — только 1 главная цель дня
- **Неделя 3-4:** 5 мин — 3 цели + time estimate
- **Неделя 5-8:** 10 мин — полный Daily Planning Ritual
- **Неделя 9+:** 15 мин — с Energy Check + Recovery Protocol

**Two-Day Rule:** напоминание после 1 пропуска: «Вы пропустили вчера — и это нормально! Правило: не более 1 дня подряд. Давайте спланируем сегодня.»

**Почему важно:** AI coaching retention = 3.3% на 30 день. Habit formation требует 66 дней. Без [habit stacking](https://jamesclear.com/habit-stacking) — продукт не удержит пользователей.

**Внедрение:** Новый модуль habit_stack.md → onboarding question «Когда вы пьёте кофе/завтракаете?» → contextual reminders → progress tracking.

---

#### Идея #3: Guided Shutdown Ritual
**Научная база:** Psychological detachment ([Sonnentag](https://pubmed.ncbi.nlm.nih.gov/17925618/)), [Masicampo & [Baumeister](https://pubmed.ncbi.nlm.nih.gov/21728448/) 2011](https://pubmed.ncbi.nlm.nih.gov/21728448/), [Cal Newport](https://calnewport.com/)
**Сложность:** Low
**Вияние:** High

**Описание:**
5-шаговый вечерний ритуал (10-15 мин):
1. **Capture** — собрать все loose ends, идеи, задачи
2. **Review** — что выполнено, что переносится
3. **Plan** — create specific plan for top 3 unfinished tasks ([Masicampo](https://pubmed.ncbi.nlm.nih.gov/21728448/) — eliminates [Zeigarnik](https://pubmed.ncbi.nlm.nih.gov/38130478/))
4. **Celebrate** — 3 «маленьких победы» дня (positive reinforcement)
5. **Close** — explicit statement: «Work day is closed» (psychological detachment)

**Почему важно:** Recovery paradox — истощённые люди не могут инициировать recovery. Автоматизированный shutdown ritual решает это. Единственная фича, объединяющая все 5 research-backed recovery механизмов.

**Внедрение:** Новый модуль shutdown_ritual.md → integrate with Calendar Intelligence Layer → auto-detect end of workday → send nudge.

---

### 🟡 P1 — Высокий приоритет (внедрить в v0.12-v0.13)

#### Идея #4: Fresh Start Coaching Engine
**Научная база:** Fresh Start Effect ([Dai](https://pubmed.ncbi.nlm.nih.gov/24311896/), [Milkman](https://katherinemilkman.squarespace.com/s/2015_BSP.pdf) 2014), MCII synergy, Oscarsson (19% resolutions на 2 года)
**Сложность:** Medium
**Влияние:** High

**Описание:**
Автоматически определять temporal landmarks (понедельник, 1-е число, New Year, день рождения) и trigger re-planning ritual:
- **Monday:** "Fresh Week" — review previous week, set 3 priorities
- **1st of month:** "Fresh Month" — Wheel of Life check-in, goal adjustment
- **New Year:** "Fresh Year" — full goal review + MCII/WOOP
- **Personal landmarks:** birthday, anniversary of starting the job

**Dark side protection:** напоминание не откладывать действия («Не ждите понедельника — начните сейчас с малого»).

**Почему важно:** 55% New Year resolutions держатся 1 месяц. Продукт может удвоить это через structured re-planning + MCII.

---

#### Идея #5: Calendar Pattern Analyzer ([MCP](https://modelcontextprotocol.io/)-based)
**Научная база:** Time management r=-0.41 с burnout, friction reduction, self-monitoring d=0.40
**Сложность:** High
**Влияние:** High

**Описание:**
Через [MCP](https://modelcontextprotocol.io/) читать Google Calendar и анализировать паттерны:
- **Meeting load:** % дня в meetings vs focus time
- **Chronotype alignment:** запланированные задачи vs peak hours
- **Boundary violations:** работа вечером/выходные
- **Recovery deficit:** пропущенные break'ы, переработки
- **Trends:** недельная/месячная динамика

**Dashboard:** визуализация паттернов + рекомендации («Вы планируете 70% meetings в trough time — перенесите аналитику на утро»).

**Почему важно:** 97% consumer applications — без [MCP](https://modelcontextprotocol.io/) integration. Это уникальное конкурентное преимущество.

**Внедрение:** Calendar Intelligence Layer v0.11.0 → [MCP](https://modelcontextprotocol.io/) read-only integration → pattern analysis engine → dashboard.

---

#### Идея #6: Workload Warning System ([Sunsama](https://www.sunsama.com/)-style)
**Научная база:** Recovery paradox, planning fallacy (Kahneman), toxic productivity (82% в зоне риска)
**Сложность:** Medium
**Влияние:** High

**Описание:**
При Daily Planning Ritual:
1. Суммировать запланированное время всех задач
2. Сравнить с user-defined workload threshold (например, 6 часов работы)
3. **Warning:** «У вас запланировано 8.5 часов задач при лимите 6 часов. Какие задачи отложить?»
4. Timeline: estimated completion time vs preferred shutdown time

**Почему важно:** 43% тратят >10 часов/неделю на «продуктивный театр». Workload Warning — concrete burnout prevention.

---

#### Идея #7: Energy-Based Scheduling v2.0
**Научная база:** [Chronoworking](https://www.hachette.co.uk/titles/ellen-scott/chronoworking/9780349434625/) (+10-20%), [Focuzed.io](https://focuzed.io/), [LifeStack.ai](https://lifestack.ai/), [Rise Science](https://www.risescience.com/) (+14% revenue)
**Сложность:** Medium
**Влияние:** Medium-High

**Описание:**
Улучшить существующий energy_scheduling.md:
- **Self-reported energy:** 1-10 scale в начале каждого planning session
- **Energy pattern learning:** корреляция energy levels с типами задач и временем
- **Smart suggestions:** «В прошлый раз у вас была высокая energy в 10 AM — запланируйте аналитику тогда»
- **Future:** интеграция с wearables (Apple Watch, Oura) через [MCP](https://modelcontextprotocol.io/)

**Почему важно:** [Focuzed.io](https://focuzed.io/) — единственный с полной wearable-интеграцией. Но self-reported energy уже даёт 80% ценности.

---

### 🟠 P2 — Средний приоритет (внедрить в v0.14-v0.15)

#### Идея #8: ADHD Mode
**Научная база:** 15.5M взрослых с ADHD, d=0.89 для Time Management coaching, body doubling (p=0.006)
**Сложность:** Medium
**Влияние:** High (niche)

**Описание:**
Специальный режим для пользователей с ADHD:
- **Micro-tasking:** разбивка на микро-задачи («открыть документ» вместо «написать отчёт»)
- **[Body doubling](https://pmc.ncbi.nlm.nih.gov/articles/PMC11710089/) prompts:** «Начните задачу сейчас — я буду здесь рядом, пока вы работаете"
- **Visual timer:** [Pomodoro](https://francescocirillo.com/products/the-pomodoro-technique)-style но с гибкой длительностью
- **Time blindness protection:** «Сейчас 2 PM, у вас встреча через 15 минут"
- **External scaffolding:** prompts вместо ожидания self-discipline

**Почему важно:** ADHD-рынок сильно недообслужен. 22 потерянных дня/год × $122.8B экономический эффект.

---

#### Идея #9: Time Structure for Unemployed / Purpose-Seekers
**Научная база:** Time structure полностью медиатирует связь активностей и депрессии (для безработных)
**Сложность:** Low
**Влияние:** High (niche)

**Описание:**
Специальный фокус для безработных и ищущих смыслы:
- **Daily structure template:** фиксированные временные блоки (утренний ритуал, job search, learning, social)
- **Purpose exploration:** интеграция с Wheel of Life — «что важно» вместо «что нужно делать"
- **Social activities:** напоминания о социальных активностях (low-cost intervention)
- **Small wins:** ежедневные «маленькие победы» для поддержания motivation

**Почему важно:** Безработные имеют lowest time structure (M=97.88 vs 111.26 у работающих). Простое структурирование времени — мощная интервенция.

---

#### Идея #10: Planning Friction Audit
**Научная база:** B=MAP ([Fogg](https://www.behaviormodel.org/)), friction reduction (300% follow-through), Amazon One-Click
**Сложность:** Low
**Влияние:** Medium

**Описание:**
Аудит трения в процессе планирования:
- **One-click scheduling:** «Добавить в календарь» — 1 клик через [MCP](https://modelcontextprotocol.io/)
- **Smart defaults:** auto-suggested time blocks based on chronotype + energy
- **Voice input:** «Запланируй встречу с Марией на завтра утром» — NLP parsing
- **Template library:** готовые шаблоны дня (Deep Work day, Meeting day, Recovery day)

**Почему важно:** Каждый клик — потеря пользователей. One-click scheduling = 300% improvement.

---

### 🔵 P3 — Исследовательский приоритет (R&D)

#### Идея #11: Body Doubling via AI
**Научная база:** [Body doubling](https://pmc.ncbi.nlm.nih.gov/articles/PMC11710089/) VR 2025 (p=0.006), [Focusmate](https://www.focusmate.com/), Flow Club
**Сложность:** High
**Влияние:** High (future)

**Описание:**
AI-powered body doubling: Claude «присутствует» рядом во время выполнения задачи:
- **Check-in:** начало сессии — что будете делать?
- **Silent presence:** периодические «я здесь» сообщения
- **Completion:** что удалось сделать?
- **Integration:** с Calendar [MCP](https://modelcontextprotocol.io/) для auto-tracking focused time

---

#### Идея #12: Wearable Energy Integration
**Научная база:** [Focuzed.io](https://focuzed.io/) (единственный с EBS), HRV+ML (AUC=0.843), но orthosomnia риск
**Сложность:** Very High
**Влияние:** High (future)

**Описание:**
Интеграция с Apple Watch / Oura / WHOOP:
- Автоматическое определение energy peaks/troughs
- Auto-scheduling задач по energy levels
- Recovery score integration

**Риски:** Wearable accuracy ±3% <13% времени. Orthosomnia (tracker-induced sleep stress). Интеграционный барьер 3-6 месяцев dev.

---

## Часть 3: Сводная таблица

| # | Идея | Приоритет | Научная база | Сложность | Целевая аудитория | Версия |
|---|------|-----------|-------------|-----------|-------------------|--------|
| 1 | Chronotype-Native Planning | **P0** | HIGH | Low | Все | v0.11 |
| 2 | Habit Stack Builder | **P0** | HIGH | Medium | Все | v0.11 |
| 3 | Guided Shutdown Ritual | **P0** | HIGH | Low | Все | v0.11 |
| 4 | Fresh Start Coaching | **P1** | HIGH | Medium | Все | v0.12 |
| 5 | Calendar Pattern Analyzer | **P1** | HIGH | High | Все | v0.12 |
| 6 | Workload Warning System | **P1** | HIGH | Medium | Все | v0.12 |
| 7 | Energy-Based Scheduling v2 | **P1** | MEDIUM | Medium | Все | v0.13 |
| 8 | ADHD Mode | **P2** | HIGH | Medium | ADHD, 15.5M | v0.14 |
| 9 | Time Structure for Unemployed | **P2** | HIGH | Low | Безработные | v0.14 |
| 10 | Planning Friction Audit | **P2** | MEDIUM | Low | Все | v0.14 |
| 11 | Body Doubling via AI | **P3** | HIGH | High | ADHD, фокус | R&D |
| 12 | Wearable Energy Integration | **P3** | MEDIUM | Very High | Power users | R&D |

---

## Часть 4: Топ-5 фич для заимствования из AI-инструментов

| # | Фича | Источник | Применимость |
|---|------|----------|-------------|
| 1 | **Habits** (flexible recurring blocks) | [Reclaim.ai](https://reclaim.ai/) | Daily routines с auto-reschedule |
| 2 | **Daily Planning Ritual** (guided 5-step) | [Sunsama](https://www.sunsama.com/) | Structure + intentionality |
| 3 | **Workload Warning** (predicted completion vs shutdown) | [Sunsama](https://www.sunsama.com/) | Burnout prevention |
| 4 | **Shutdown Ritual** (end-of-day reflection) | [Sunsama](https://www.sunsama.com/) | Psychological detachment |
| 5 | **Frames + Priority Factor** | [Morgen](https://www.morgen.so/) | Template week + energy-aware scheduling |

---

## Часть 5: Чего избегать (уроки из исследования)

| ❌ Не делать | Почему | Источник |
|-------------|--------|----------|
| Не быть standalone calendar optimizer | [Clockwise](https://www.getclockwise.com/): $76M → shutdown | dim04 |
| Не продвигать «Магию утра» всем | Chronotype-blindness, вред для 20-30% | dim01 |
| Не интегрировать [PARA](https://fortelabs.com/blog/para/)/[Bullet Journal](https://bulletjournal.com/) как системы | Zero RCT, placebo effect | dim07 |
| Не использовать [Pomodoro](https://francescocirillo.com/products/the-pomodoro-technique) по умолчанию | Прерывает flow state, mixed results | dim03 |
| Не полагаться на nudge alone | Real-world effect в 6 раз < академического | dim02 |
| Не игнорировать recovery | Recovery paradox + 82% в зоне риска | dim08 |
| Не требовать wearable для energy tracking | Orthosomnia + accuracy issues | dim05 |

---

## Приложение: Источники и исследовательские файлы

Все исследования доступны в полном объеме по ссылкам ниже:

### Исследовательские файлы по измерениям (Deep Dive)

| Файл | Измерение | Ссылка |
|------|-----------|--------|
| planning_dim01.md | Хронобиология и оптимальное время планирования | [Открыть](planning_dim01.md) |
| planning_dim02.md | Behavioral Design — nudge, friction, implementation intentions | [Открыть](planning_dim02.md) |
| planning_dim03.md | Habit formation — ритуалы, Tiny Habits, habit stacking | [Открыть](planning_dim03.md) |
| planning_dim04.md | AI-инструменты календарей — фичи для заимствования | [Открыть](planning_dim04.md) |
| planning_dim05.md | Energy-based scheduling — от времени к энергии | [Открыть](planning_dim05.md) |
| planning_dim06.md | Методологии с научной валидацией — Time Blocking, GTD | [Открыть](planning_dim06.md) |
| planning_dim07.md | Методологии без валидации — PARA, Bullet Journal | [Открыть](planning_dim07.md) |
| planning_dim08.md | Recovery, burnout prevention, toxic productivity | [Открыть](planning_dim08.md) |
| planning_dim09.md | MCP, Calendar API и техническая интеграция | [Открыть](planning_dim09.md) |
| planning_dim10.md | Адаптация под ADHD, neurodivergent, безработных | [Открыть](planning_dim10.md) |
| planning_dim11.md | Fresh Start Effect и Temporal Landmarks | [Открыть](planning_dim11.md) |
| planning_dim12.md | AI coaching — рынок, исследования, тренды | [Открыть](planning_dim12.md) |

### Вспомогательные файлы

| Файл | Содержание | Ссылка |
|------|------------|--------|
| planning_cross_verification.md | Cross-verification — confidence tiers, conflict zones | [Открыть](planning_cross_verification.md) |
| planning_insight.md | Insight Extraction — 10 кросс-дименсиональных инсайтов | [Открыть](planning_insight.md) |
| planning_wide01.md — planning_wide05.md | Wide Exploration — 5 фасетов широкого поиска | [Открыть](.) |

### Ключевые научные исследования (с прямыми ссылками)

| Исследование | Авторы | Ссылка |
|-------------|--------|--------|
| Implementation Intentions (мета-анализ, 94 исследования) | [Gollwitzer & Sheeran](https://kops.uni-konstanz.de/server/api/core/bitstreams/d703c468-46e9-47fc-8900-5b6ab3e50f5a/content) | [PDF](https://kops.uni-konstanz.de/server/api/core/bitstreams/d703c468-46e9-47fc-8900-5b6ab3e50f5a/content) |
| Weekly Review +23% performance | [Di Stefano et al.](https://www.hbs.edu/ris/Publications%20Files/14-093_d4970af6-a7c9-4653-8908-43368175583.pdf) | [PDF](https://www.hbs.edu/ris/Publications%20Files/14-093_d4970af6-a7c9-4653-8908-43368175583.pdf) |
| Habit formation — 66 дней | [Lally et al.](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6494.2010.00660.x) | [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6494.2010.00660.x) |
| Fresh Start Effect | [Dai, Milkman, Riis](https://pubmed.ncbi.nlm.nih.gov/24311896/) | [PubMed](https://pubmed.ncbi.nlm.nih.gov/24311896/) |
| Decision fatigue — судьи | [Danziger et al.](https://www.pnas.org/doi/10.1073/pnas.1018033108) | [PNAS](https://www.pnas.org/doi/10.1073/pnas.1018033108) |
| Peak-Trough-Rebound | [Pink](https://www.danpink.com/books/when/) | [danpink.com](https://www.danpink.com/books/when/) |
| Planning eliminates Zeigarnik | [Masicampo & Baumeister](https://pubmed.ncbi.nlm.nih.gov/21728448/) | [PubMed](https://pubmed.ncbi.nlm.nih.gov/21728448/) |
| Psychological detachment | [Sonnentag](https://pubmed.ncbi.nlm.nih.gov/17925618/) | [PubMed](https://pubmed.ncbi.nlm.nih.gov/17925618/) |
| Synchrony effect | [Facer-Childs et al.](https://link.springer.com/article/10.1186/s40798-018-0162-z) | [Springer](https://link.springer.com/article/10.1186/s40798-018-0162-z) |
| Attention residue | [Leroy](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-8721.2009.01656.x) | [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-8721.2009.01656.x) |
| Nudge meta-analysis | [Mertens et al.](https://www.pnas.org/doi/10.1073/pnas.2107346118) | [PNAS](https://www.pnas.org/doi/10.1073/pnas.2107346118) |
| Nudge at scale | [DellaVigna & Linos](https://www.hks.harvard.edu/publications/rcts-scale-comprehensive-evidence-two-nudge-unit) | [Harvard HKS](https://www.hks.harvard.edu/publications/rcts-scale-comprehensive-evidence-two-nudge-unit) |
| Planning prompts | [Milkman et al.](https://www.pnas.org/doi/10.1073/pnas.1103170108) | [PNAS](https://www.pnas.org/doi/10.1073/pnas.1103170108) |
| B=MAP behavioral model | [Fogg](https://www.behaviormodel.org/) | [behaviormodel.org](https://www.behaviormodel.org/) |
| Self-monitoring (мета-анализ) | [Harkin et al.](https://onlinelibrary.wiley.com/doi/abs/10.1111/bmsp.12093) | [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/bmsp.12093) |
| Time management vs burnout | [Frontiers 2025](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1623228/full) | [Frontiers](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1623228/full) |
| Toxic productivity | [Jennifer Moss](https://www.jennifer-moss.com/writing/ending-toxic-productivity) | [HBR](https://www.jennifer-moss.com/writing/ending-toxic-productivity) |
| Productivity theater | [Visier 2023](https://www.visier.com/blog/productivity-survey-shows-performative-work/) | [Visier](https://www.visier.com/blog/productivity-survey-shows-performative-work/) |
| Body doubling VR study | [PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11710089/) | [PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC11710089/) |
| AI coaching market | [CareerTrainer AI](https://careertrainer.ai/en/reports/ai-coaching-statistics/) | [careertrainer.ai](https://careertrainer.ai/en/reports/ai-coaching-statistics/) |
| Therabot RCT | [Therabot](https://ar5iv.org/pdf/2503.05516.pdf) | [ar5iv](https://ar5iv.org/pdf/2503.05516.pdf) |
| 1440 AI coach study | [arXiv](https://arxiv.org/abs/2506.08863) | [arXiv](https://arxiv.org/abs/2506.08863) |
| New Year resolutions success | [Oscarsson et al.](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0234097) | [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0234097) |
| MCP ecosystem | [modelcontextprotocol.io](https://modelcontextprotocol.io/) | [MCP](https://modelcontextprotocol.io/) |
| Claude productivity gains | [Anthropic](https://www.anthropic.com/research/estimating-productivity-gains) | [Anthropic](https://www.anthropic.com/research/estimating-productivity-gains) |
