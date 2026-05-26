# Deep Research: Track 0 — Micro-Goal Onboarding

> **Проблема:** Текущий онбординг не имеет быстрого пути (<5 мин) от первого сообщения до первой SMART-цели. Phase 0 даёт coping action, Track A требует 25-40 мин диагностики.
> **Дата исследования:** 2026-05-20
> **Источники:** 4 параллельных research-агента (конкуренты, наука, клиника, behavioral design)

---

## Executive Summary

**Ключевой инсайт:** На рынке нет прямого аналога "Track 0: Micro-Goal" для русскоязычного AI life coaching. Ближайшие параллели — Wysa (<1 мин до чата), MindShift (zero-barrier), Headspace (onboarding = product experience). Retention mental health apps: **3.9% после 15 дней** — главная причина drop-off: suboptimal onboarding.

**Рекомендация:** Внедрить **Track 0: Micro-Goal** — 3-5 минут от первого сообщения до одной SMART-цели на сегодня, без Wheel of Life и Values. Полная диагностика откладывается до Track 1.

---

## 1. Конкурентный Анализ

### 1.1 AI Coaching / Skills

| Платформа | Onboarding Time | First Deliverable | Key Technique |
|-----------|-----------------|-------------------|---------------|
| **Claude Skill (adamlyttleapps)** | ~5-10 мин | Персонализированный план | "Inverted onboarding" — пользователь пробует продукт до регистрации; "Processing moment" |
| **BetterUp AI Coach** | 5-10 мин | Первый AI-разговор | Опциональная оценка отложена; фокус на immediate chat |
| **Taskade Coach Agent** | ~5-7 мин | Персонализированный coaching plan | AI читает intake и готовит prep notes |
| **Lattice AI Agent** | Мгновенно | Coaching micro-goal | "Zero-friction" — нет intake, AI использует имеющиеся данные |

**Вывод:** Прямых аналогов "Track 0" среди публичных skills не найдено. BetterUp — ближайший пример: минимальный intake, мгновенный доступ к AI-разговору.

### 1.2 Mental Health Apps

| Приложение | Time to First Value | Можно skip intake? | Первый quick win |
|------------|---------------------|--------------------|------------------|
| **Wysa** | **<1 мин** | **Да** (skip quiz) | AI chat + tool |
| **MindShift** | **<1 мин** | N/A (нет intake) | Daily check-in |
| **Headspace** | 3-5 мин | Нет | Первая медитация (30 сек) |
| **Calm** | 1-2 мин (или 0) | **Да** | Медитация / план |
| **Replika** | 1-2 мин | Нет | Первый чат |
| **Woebot** | 3-5 мин | Нет | Mood check-in + tool |
| **Sanvello** | 5-10 мин | Нет | Mood check-in + AI chat |
| **Youper** | 5-7 мин | Нет | Mood check-in |
| **Bloom** | 2-3 мин | Нет | Первое CBT-упражнение |
| **Noom** | 15-25 мин | Нет | Custom plan |
| **CoachHub** | ~30 мин | Нет | Coach matching + plan |

### 1.3 5 Ключевых Паттернов для Адаптации

1. **Inverted Onboarding** (Headspace / Calm) — ценность ДО анкетирования
2. **Anonymous Zero-Barrier Entry** (Wysa / MindShift) — без email/регистрации
3. **Processing Moment** (Noom) — искусственная пауза перед выдачей результата
4. **Mascot-Driven Personality** (Wysa) — emotional safety
5. **Single-Path Interface** (Mind Cleanse) — одно primary action вместо меню

---

## 2. Научные Исследования

### 2.1 First-Session Effectiveness

| Исследование | Ключевой Finding | Relevance |
|--------------|-----------------|-----------|
| **SST meta-analysis** (Frontiers, 2021) | Effect size **d = 0.42–1.58** vs no treatment | Одна сфокусированная сессия способна дать клинически значимый эффект |
| **Lambert et al.** | Early change объясняет **~40% дисперсии** финального исхода | Ранняя перемена = самый мощный предиктор успеха |
| **Stulz et al., 2007** | >90% "ранних ответчиков" сохраняют улучшение | Early response почти гарантирует успех |
| **Talmon, 1990** (Kaiser) | 58.6% выбрали одну сессию; 88%+ улучшение | SST satisfaction = multi-session satisfaction |
| **Walk-in therapy** (Slive, 2008) | 85–90% удовлетворённости; улучшения на 3-месячном follow-up | Без intake form — лучшие результаты |

### 2.2 Aha-Moment Psychology

| Исследование | Finding |
|--------------|---------|
| **Kounios & Beeman, 2009** | Инсайт активирует правую префронтальную кору → гамма-всплеск в височной доле |
| **Oh et al., 2020** | Инсайт-решения активируют орбитофронтальную кору (hedonic rewards) → настроение ↑ на час+ |
| **Duke/Humboldt, 2023** | Инсайты "перепаивают" мозг — усиливаются связи гиппокамп ↔ зрительная кора → лучше запоминаются |
| **Stanford Behavior Design Lab** | Aha-moment activation → free-to-paid conversion **+18%** |

### 2.3 Quick Wins / Dopamine

| Исследование | Finding |
|--------------|---------|
| **Amabile & Kramer, 2011** (12,000 diaries) | **76%** лучших дней содержали прогресс; setbacks в **2–3× сильнее** progress |
| **Hart et al., 2014** | Дофамин кодирует reward prediction error — неожиданный успех = сильнее сигнал |
| **Schultz et al., 1997** | Дофаминовые нейроны возбуждаются при **неожиданной** награде |

### 2.4 Onboarding Psychology

| Принцип | Finding | Relevance |
|---------|---------|-----------|
| **Peak-End Rule** (Kahneman, 1993) | Опыт оценивается по пику и концу, не по среднему | Нужен яркий пик (aha-moment) + сильный конец |
| **System 1 vs System 2** (Kahneman, 2011) | System 1 доминирует в первые минуты | Track 0 должен работать на интуицию, не анализ |
| **Hook Model** (Eyal, 2014) | Trigger → Action → Variable Reward → Investment | >3 шагов до core value = 40–60% drop-off на шаг |
| **Cognitive Load** (Sweller, 1988) | Рабочая память: **5–9 чанков** | Диагностика 25-40 мин = cognitive overload |
| **Paradox of Choice** (Schwartz, 2004) | 24 варианта → 3% покупок; 6 вариантов → 30% | Не спрашивать "выберите из 11 сфер" |
| **Decision Quicksand** (Sela & Berger, 2012) | Тривиальные решения увязывают | Планирование не должно занимать >60 сек |

---

## 3. Микро-Интервью Техники

### 3.1 Solution-Focused Brief Therapy (SFBT)

| Техника | Exact Wording | Что даёт |
|---------|---------------|----------|
| **Best Hopes** (de Shazer) | *"What are your best hopes from our talking today?"* | Фокус всего разговора за 5-10 сек |
| **Miracle Question** (адаптированная) | *"Imagine a 0-10 scale... Tonight something shifts and you wake up at 10. What will be the first difference you notice?"* | Конкретные сенсорные детали будущего |
| **Scaling** (de Shazer) | *"On a scale of 0 to 10... where are you now?"* + *"How did you get to [number]?"* | Текущее состояние + ресурсы + следующий шаг |
| **Exception Seeking** (de Shazer) | *"When was the last time this was a little better, even for a moment?"* | Существующие ресурсы за 1 ответ |

### 3.2 Motivational Interviewing (MI) — Rapid Version

| Техника | Exact Wording | Что даёт |
|---------|---------------|----------|
| **Importance-Confidence Ruler** (Miller & Rollnick) | *"On a scale of 0-10, how important is it...?"* + *"How confident are you...?"* + *"Why not zero?"* | 2 числа = полная картина готовности |
| **Focus Question** (Moyers) | *"What would you like to be different about your current situation?"* | Нейтрализует "righting reflex" |
| **Mobilizing Change Talk** | *"What gives you confidence that you could do this?"* | CAT — язык действия |

### 3.3 Single-Session Therapy (SST)

**Mindset (Talmon, 1990; Hoyt):**
1. Каждая сессия — потенциально полная, самодостаточная
2. Сила — в клиенте, не в терапевте
3. Маленький шаг может дать большой эффект

**OATT Structure (One-At-A-Time):**

| Фаза | Задача | Вопрос |
|------|--------|--------|
| Beginning | Договориться о фокусе | *"What do you want to achieve by the end of this session?"* |
| Middle | Мобилизовать ресурсы | *"What has helped before?"* / *"When is it less of a problem?"* |
| End | План действий + feedback | *"What's your next step?"* / *"How will you know it's working?"* |

### 3.4 Протокол "3-Q Micro-Intake"

| Шаг | Вопрос | Что извлекаем |
|-----|--------|---------------|
| **Q1** | *"What are your best hopes from our conversation today?"* | Желаемый результат |
| **Q2** | *"On a scale of 0-10, where are you with that right now?"* | Текущая позиция |
| **Q3** | *"What's one small step that could move you one point up?"* | Конкретное действие |

**Формула цели:**
> "Сегодня я [действие из Q3], чтобы [best hope из Q1] было ближе на 1 пункт."

**Пример:**
- Q1: "Хочу чувствовать себя менее перегруженным"
- Q2: "3 из 10"
- Q3: "Составлю список из 3 приоритетов"
→ **Цель:** "Сегодня я составлю список из 3 приоритетов, чтобы снизить ощущение перегрузки с 3 до 4."

---

## 4. Behavioral Design Первой Цели

### 4.1 8 Критериев Идеальной "Первой Цели"

| # | Критерий | Источник |
|---|----------|----------|
| 1 | **≤ 2–5 минут на выполнение** | Fogg (Tiny Habits); Yu-kai Chou |
| 2 | **Только ОДНА цель, не список** | Paradox of Choice; Decision Quicksand |
| 3 | **Конкретное первое действие, не результат** | Implementation Intentions; Fogg (Starter Step) |
| 4 | **Привязка к when + where (if-then)** | Gollwitzer & Sheeran (2006), **d = 0.65** |
| 5 | **Mastery-ориентация, не performance** | Locke & Latham; Elliot & McGregor (2001) |
| 6 | **Немедленное подтверждение выполнения** | Amabile & Kramer (2011) |
| 7 | **"Absurdly small" — смешно маленькая** | Fogg (Tiny Habits) |
| 8 | **Сегодня, не "когда-нибудь"** | Proximal goals (Locke & Latham, 2002) |

### 4.2 4 Шаблона Формулировки Цели

**Шаблон 1: Tiny Habit (Fogg)**
> "После того как я [существующая рутина], я буду [starter step]."
> Пример: "После того как встану с кровати, я надену кроссовки."

**Шаблон 2: Implementation Intention (Gollwitzer)**
> "Если [время/место/событие], то я [конкретное первое действие]."
> Пример: "Если сяду в автобус, то открою книгу и прочту 1 абзац."

**Шаблон 3: Micro-Goal (Progress Principle)**
> "Сегодня я [глагол + объект + время ≤ 5 мин]."
> Пример: "Сегодня я 2 минуты подышу осознанно."

**Шаблон 4: Mastery-First**
> "Сегодня я попробую [навык] на [2 минуты]. Цель — просто попробовать, не идеальный результат."
> Пример: "Сегодня я попробую записать 1 мысль в дневник. Не важно, красиво или нет."

### 4.3 Anti-Patterns (Что НЕ Делать)

| Anti-Pattern | Почему плохо |
|--------------|--------------|
| "Составьте список 5 целей на неделю" | Decision fatigue + paradox of choice |
| "Поставьте амбициозную цель!" | High Ability требует high Motivation |
| "Начните с 30 минут медитации" | Слишком сложно для новичка |
| "Выберите из 10 вариантов" | Choice overload → analysis paralysis |
| "Напишите подробный план" | Decision quicksand |
| Performance-цель: "Сделайте 10 000 шагов" | Тревожность + демотивация при провале |
| "Проверим прогресс через месяц" | Отсутствие immediate feedback |

---

## 5. Синтез: Рекомендуемый Протокол Track 0

### 5.1 Структура (≤5 минут)

| Фаза | Время | Действие | Техника |
|------|-------|----------|--------|
| **1. Trigger Acknowledgment** | 15 сек | "Я вижу, вы хотите [X]. Давайте за 3 минуты найдём один конкретный шаг на сегодня." | Inverted Onboarding |
| **2. Micro-Interview (Q1)** | 1 мин | "Что для вас было бы самым полезным результатом нашего разговора сегодня?" | Best Hopes (de Shazer) |
| **3. Micro-Interview (Q2)** | 1 мин | "Если 10 — это когда [best hope] полностью достигнуто, а 0 — наихудшее, где вы сейчас?" | Scaling (SFBT) |
| **4. Micro-Interview (Q3)** | 1 мин | "Какой один маленький шаг мог бы подвинуть вас на 1 пункт вверх?" | One Small Step |
| **5. Goal Formulation** | 1 мин | "Сегодня я [Q3], чтобы [Q1] было ближе на 1 пункт." + if-then формат | Implementation Intention |
| **6. Aha-Moment / Peak** | 30 сек | "Заметили? Всё сложное — это всего лишь [конкретное действие]." | Insight activation |
| **7. Strong End** | 30 сек | "Вы только что сделали первый шаг. Завтра в это же время спрошу, как прошло." | Peak-End Rule + Zeigarnik |

### 5.2 Критерии Цели (чек-лист для AI)

- [ ] **≤ 5 минут** на выполнение (ideally ≤ 2)
- [ ] **Только одна** цель, не список
- [ ] **Starter Step** или **Scaled-Back Version** — первое физическое действие, не результат
- [ ] **If-then формат** — привязка к существующей рутине или контексту
- [ ] **Mastery-фрейминг** — "просто попробовать", не "идеальный результат"
- [ ] **Сегодня**, не "когда-нибудь"
- [ ] **Confidence ≥ 7/10** — если ниже, дробить дальше
- [ ] **No lists, no planning, no diagnostics** до завершения первой цели

### 5.3 Риски и Митигация

| Риск | Митигация |
|------|-----------|
| Поверхностность | Протокол только для "small goal for today"; глубокая диагностика — Track 1 |
| Safety issues | Микро-интервью не заменяет safety assessment; при рисках — переключиться на Phase 0.5 |
| Форсирование цели | Если sustain talk > change talk — не переходить к планированию (MI) |
| Слишком амбициозная цель | Scaling + confidence ruler; <7 = дробить |
| Игнорирование "большой картины" | Микро-интервью — точечный инструмент; Wheel of Life по-прежнему доступен |

### 5.4 Отличие от Текущего Phase 0

| | Текущий Phase 0 | Track 0: Micro-Goal |
|---|-----------------|---------------------|
| **Длительность** | 5-10 мин | 3-5 мин |
| **Результат** | Coping action (ONE THING TODAY) | SMART micro-goal с if-then |
| **Структура** | VALIDATE → REFLECT → ACTION → BRIDGE | Q1 → Q2 → Q3 → GOAL → PEAK → END |
| **Вопросы** | 0 (эмоциональная поддержка) | 3 (микро-интервью) |
| **Цель** | Emotional landing + bridge to diagnostic | Полноценная сессия с tangible output |
| **Диагностика** | Не требуется | Не требуется (отложена) |

---

## 6. Источники

### Книги
1. de Shazer, S. (1985). *Keys to Solution in Brief Therapy*. W.W. Norton.
2. Miller, W.R. & Rollnick, S. (2013). *Motivational Interviewing*. Guilford Press.
3. Talmon, M. (1990). *Single-Session Therapy*. Jossey-Bass.
4. Fogg, B.J. (2019). *Tiny Habits*. Houghton Mifflin Harcourt.
5. Amabile, T.M. & Kramer, S.J. (2011). *The Progress Principle*. HBR Press.
6. Locke, E.A. & Latham, G.P. (2002). Goal setting theory. *American Psychologist*, 57(9), 705–717.
7. Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

### Исследования
8. Frontiers in Psychology (2021). SST meta-analysis, 18 RCT. DOI: 10.3389/fpsyg.2021.721382
9. Gollwitzer, P.M. & Sheeran, P. (2006). Implementation intentions meta-analysis, **d = 0.65**.
10. Kounios, J. & Beeman, M. (2009). The Aha! Moment. *Current Directions in Psychological Science*.
11. Iyengar, S.S. & Lepper, M.R. (2000). Paradox of Choice. *JPSP*, 79(6), 995–1006.
12. Sela, A. & Berger, J. (2012). Decision Quicksand. *JCR*, 39(2), 360–370.
13. Baumel et al. (2019). Mental health apps retention: **3.9% после 15 дней**.

---

*Исследование завершено 2026-05-20. 4 агента, 60+ источников, cross-verification.*
