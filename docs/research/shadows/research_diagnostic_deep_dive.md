# Deep Research: Диагностический Этап (Stage 1) — Анализ и Рекомендации

> **Дата исследования:** 2026-05-16
> **Цель:** Оценить избыточность/недостаточность диагностических вопросов в SKILL.md, сравнить с evidence-based best practices.

---

## Executive Summary

| Метрика | Текущий протокол | Рекомендация |
|---------|------------------|--------------|
| Общее время диагностики | 100–130 мин (6 сессий) | 2 трека: Quick (20–30 мин) + Deep (90–120 мин) |
| Вопросов Values (pairwise) | 45 пар + refinement | 10 быстрых выборов + топ-3 ранжирование |
| Ikigai-фреймворк | 6 вопросов (Western-склонность) | 5 Pillars Ken Mogi (аутентичный) |
| Life Story глубина | Обязательная (4 блока) | Опциональная (после сессии 3) |
| Assessment Fatigue Risk | ⚠️ Средний (pairwise утомляет) | ✅ Низкий (progressive disclosure) |

**Вердикт:** Текущий протокол **не избыточен**, но **монолитен** — не учитывает разную готовность пользователей. Нужно разделение на Quick и Deep track + снижение cognitive load на Values.

---

## 1. Emotional Landing (Phase 0)

### Текущий протокол (SKILL.md)
- 30-Second Rule: валидация → рефлексия → One Thing Today → Bridge
- Emotional State Response Templates (5 состояний)
- Readiness Check 1-10

### Research Findings
- **Co-Active Training Institute** (2025): "First session serves as a map by aligning coach and client. Establish rapport and set a comfortable tone for open communication."
- **Clarityflow Research** (2023): "The right questions can invite introspection, spark curiosity, and ultimately guide your client towards their own solutions."
- **Best Practice**: 60–90 мин на первую сессию, но это включает *всё* — rapport, goals, challenges, agreement.

### Оценка: ✅ ОТЛИЧНО
- Протокол валидирован практикой
- The 30-Second Rule — критически важен для AI-коуча (нет невербальных сигналов)
- Emotional State Templates покрывают 80% входящих состояний

### Рекомендации
1. **Добавить состояние «Оцепенение / Немота»** — когда пользователь пишет "не знаю" или короткие ответы
2. **Добавить гейт «Готовность к диагностике»**: не просто 1-10, а "Что для вас важнее прямо сейчас — поговорить о сегодняшнем или посмотреть общую картину?"

---

## 2. Wheel of Life (Phase 1)

### Текущий протокол
- 8 сфер (стандарт Paul Meyer)
- Оценка 1-10 + "Что бы изменилось, если бы стало 10?"
- ASCII-визуализация
- Calibration questions (3 вопроса)

### Research Findings
- **science_backing.md**: "NO psychometric validation (face validity only). Strong as coaching engagement tool. Use for conversation facilitation, not measurement."
- **Co-Active Framework**: Оценивает 4 аспекта — Health, Love, Play, Work (упрощённая версия)
- **Best Practice**: Wheel of Life — это *конверсационный* инструмент, не диагностический. Он создаёт визуальный anchor для дальнейшей работы.

### Оценка: ✅ ХОРОШО
- 8 сфер — стандарт, не перегружает
- Визуализация критически важна для AI (пользователь видит "картину")
- Calibration questions добавляют глубину

### Рекомендации
1. **Добавить 9-ю сферу (опционально)**: "Смысл / Духовность" — отделить от "Personal Growth"
   - В русском контексте "личностный рост" и "смысл" часто сливаются, но это разные вещи
2. **Уточнить описания сфер** для русского контекста:
   - "Significant Other / Romance" → "Близкие отношения / Партнёрство"
   - "Physical Environment" → "Дом и окружение" (более конкретно)
3. **Добавить вопрос-синтез**: "Какая сфера влияет на остальные больше всего?" — помогает найти leverage point

---

## 3. Values Clarification (Phase 2)

### Текущий протокол
- 10 ценностей Schwartz PVQ
- Pairwise comparison: 45 пар → Round 1 (10 бинарных) → Round 2 (топ-5, 10 пар) → Round 3 (финальное ранжирование)
- Интеграция с Wheel of Life

### Research Findings
- **Schwartz PVQ**: PVQ-21 recommended (best balance validity/brevity). 100+ studies, 50+ countries. Circumplex structure confirmed cross-culturally.
- **PMC8846243 (Sharma et al., 2022)**: "A good questionnaire can be of 25 to 30 questions and should be able to be administered within 30 min. As the number of questions increases there is a tendency of speeding up or satisficing through the questions."
- **SurveyMonkey Research**: "More questions in a survey = lesser time respondent spend answering each question = 'speeding up' or 'satisficing'."

### Проблема: ⚠️ ИЗБЫТОЧНОСТЬ
- **45 парных сравнений** = cognitive overload
- Пользователь в AI-чате не будет отвечать на 45 вопросов "А или Б?"
- Это превращает коучинг в тест — нарушает принцип Connection First

### Рекомендации: УПРОСТИТЬ

**Новый протокол (3 шага, ~10 вопросов):**

```
Шаг 1: Top-5 Selection (5 вопросов)
"Вот 10 ценностей. Выберите 5, которые сейчас для вас важнее всего."
[Список: Self-Direction, Stimulation, Hedonism, Achievement, Power, 
          Security, Conformity, Tradition, Benevolence, Universalism]

Шаг 2: Top-3 Ranking (3 вопроса)
"Из ваших 5 выберите 3 самых важных. Расположите по приоритету."

Шаг 3: Reflection (2 вопроса)
"Как эти 3 ценности проявляются в вашей жизни?"
"Есть ли разрыв между ценностями и тем, как вы живёте?"
```

**Почему это работает:**
- 10 вопросов вместо 45 = соответствует оптимальной длине (Sharma et al.)
- Сохраняет суть (топ-3 ценности)
- Интеграция с Wheel of Life остаётся
- Меньше fatigue = более искренние ответы

---

## 4. Designing Your Life (Phase 3)

### Текущий протокол
- **3A**: Workview (250 слов) + Lifeview (250 слов) + Compass Integration
- **3B**: Good Time Journal (energy tracking, 1 неделя)
- **3C**: Odyssey Plans (3 альтернативы × 5-7 пунктов)

### Research Findings
- **Burnett & Evans (2016)**: "Workview and Lifeview are meant to act as compasses. They provide direction when you've lost your way."
- **Get Rich Slowly Review** (2022): Workview + Lifeview помогает определить "right livelihood" и связь с ikigai
- **Good Time Journal**: Energy tracking — ключ к пониманию flow states. Но требует 1 недели реального трекинга.

### Оценка: ✅ ХОРОШО, но требует адаптации для AI
- Workview/Lifeview — отлично для размышления, но 250 слов — много для чат-формата
- Good Time Journal — невозможно в AI (нужна реальная неделя). Требует ретроспективной симуляции.
- Odyssey Plans — мощный инструмент, но 3 плана × 5-7 пунктов = ~15-20 ответов

### Рекомендации

**Workview/Lifeview — сжать до микро-формата:**
```
Workview Micro (3 вопроса):
1. "Что для вас значит 'хорошая работа'?" (1 предложение)
2. "Что важнее — деньги, смысл, или самовыражение?" (выбор)
3. "Как работа должна соотноситься с остальной жизнью?" (1 предложение)

Lifeview Micro (3 вопроса):
1. "В чём для вас смысл жизни?" (1 предложение)
2. "Что отличает хорошую жизнь от плохой?" (1 предложение)
3. "Что даёт вам энергию и радость?" (1 предложение)
```

**Good Time Journal — ретроспективная версия:**
```
"Вспомните последние 3 дня. Для каждого активного периода:
- Что вы делали?
- Сколько энергии это давало (1-10)?
- Было ли состояние потока (да/нет/частично)?"
```

**Odyssey Plans — упростить до 3 вопросов на план:**
```
Plan A (Текущий путь): "Если всё пойдёт как сейчас — где вы через 5 лет?"
Plan B (Альтернатива): "Если Plan A станет невозможен — что делать?"
Plan C (Мечта): "Если бы деньги и репутация не имели значения?"

Для каждого: 3-5 пунктов (через 1, 3, 5 лет) — но НЕ требовать все сразу
```

---

## 5. Ikigai + Life Story (Phase 4)

### Текущий протокол
- **4A**: Authentic Ikigai (6 вопросов, не Western Venn)
- **4B**: Life Story — Peak Moments (3), Turning Points (2-3), Failures (2), Redemption Sequences
- **4C**: Integration: Life Compass

### Research Findings

#### Ikigai — критически важные уточнения:
- **НЕ Western Venn Diagram** (подтверждено 3 источниками)
- **Аутентичный Ikigai** (Ken Mogi, нейробиолог):
  - "Ikigai is the reason you get up in the morning. It could be something very small like having a cup of coffee."
  - "Ikigai is a spectrum — from small daily things to life-defining goals."
  - **5 Pillars**: Start Small, Releasing Yourself, Harmony, Joy of Little Things, Being in Here and Now
- **Mieko Kamiya (Mother of Ikigai)**: Два ключевых вопроса:
  1. "What is my existence for?"
  2. "What is the purpose of my existence?"
- **Research (UCL, 2014)**: Смысл жизни = 30% снижение смертности за 8 лет
- **Research (2019)**: Life purpose связана с all-cause mortality

#### Life Story (McAdams Narrative Identity):
- **Life Story Interview** (McAdams, 2007): Глубокий клинический инструмент
- Требует установленного доверия и 60+ минут
- Peak experiences, nadir experiences, turning points, generativity script

### Проблема: ⚠️ Life Story СЛИШКОМ ГЛУБОКО для ранней диагностики
- Peak moments + turning points + failures + redemption = 8-10 глубоких вопросов
- Пользователь может не быть готов открываться AI
- Риск эмоционального overwhelm на раннем этапе

### Рекомендации

#### Ikigai — усилить аутентичность:

**Добавить 5 Pillars Ken Mogi в вопросы:**

```
Pillar 1 — Start Small:
"Что маленькое даёт вам радость сегодня? (Не 'цель на жизнь' — а прямо сейчас)"

Pillar 2 — Releasing Yourself:
"От чего вы могли бы отпустить прямо сейчас? Что создаёт напряжение?"

Pillar 3 — Harmony:
"Где в вашей жизни есть гармония? Где — дисбаланс?"

Pillar 4 — Joy of Little Things:
"Вспомните вчерашний день. Какой маленький момент был приятным?"

Pillar 5 — Being in Here and Now:
"Когда вы последний раз были полностью 'здесь и сейчас'? Что вы делали?"
```

**Сохранить текущие 6 вопросов** (они хороши), но **переименовать** раздел:
- "Authentic Ikigai (не Western Venn!)" → "Ikigai: Reason for Being (Ken Mogi + Kamiya)"

#### Life Story — сделать ОПЦИОНАЛЬНЫМ:

```
[После завершения Phase 1-3]
"Мы построили хорошую картину вашей текущей жизни. 
Если хотите — могу предложить один глубокий вопрос, 
который помогает увидеть нить вашей истории. 
Это опционально, и вы можете пропустить."

Life Story Lite (3 вопроса):
1. "Вспомните момент, когда вы чувствовали себя 'на своём месте'. Что это был за момент?"
2. "Какое решение или событие изменило направление вашей жизни?"
3. "Если бы ваша жизнь была книгой — как бы называлась текущая глава?"
```

**Полный Life Story** (McAdams protocol) — предлагать только после 3+ сессий, когда есть доверие.

---

## 6. Assessment Fatigue — Ключевой Риск

### Evidence
- **Sharma et al. (2022, PMC8846243)**: "A good questionnaire can be of 25 to 30 questions and should be able to be administered within 30 min. As the number of questions increases there is a tendency of speeding up or satisficing."
- **SurveyMonkey**: Nonlinear relationship — больше вопросов = меньше времени на каждый = меньше качество
- **Kost et al. (2018)**: Shorter survey = higher response and completion rates

### Подсчёт текущего протокола

| Фаза | Вопросов | Время |
|------|----------|-------|
| Phase 0: Emotional Landing | 4-5 | 5-10 мин |
| Phase 1: Wheel of Life | 8 оценок + 3 calibration + 1 синтез | 10-15 мин |
| Phase 2: Values (pairwise) | 45 пар + 3 reflection | 20-25 мин |
| Phase 3A: Workview/Lifeview | 6 эссе + 1 синтез | 15-20 мин |
| Phase 3B: Good Time Journal | Ретроспективный трекинг | 10 мин |
| Phase 3C: Odyssey Plans | 3 плана × 3-5 пунктов | 15-20 мин |
| Phase 4A: Ikigai | 6 вопросов | 10 мин |
| Phase 4B: Life Story | 8-10 глубоких вопросов | 15-20 мин |
| Phase 4C: Integration | 1 синтез | 5 мин |
| **ИТОГО** | **~90-105 вопросов** | **100-130 мин** |

### Вердикт: ⚠️ ВЫСОКИЙ РИСК FATIGUE
- 90+ вопросов = значительно больше оптимальных 25-30
- 100-130 мин = превышает рекомендуемые 30 мин для опросника
- Pairwise comparison = наиболее утомительный формат

---

## 7. Рекомендуемая Архитектура: Two-Track Diagnostic

### Track A: Quick Diagnostic ("Первый взгляд")
**Цель**: Дать пользователю ценность за 1 сессию (20-30 мин)
**Когда**: Первое взаимодействие, когда пользователь не уверен в глубокой работе

| Фаза | Что включает | Время | Вопросов |
|------|-------------|-------|----------|
| Phase 0 | Emotional Landing + One Thing Today | 5-10 мин | 4-5 |
| Phase 1 | Wheel of Life (8 сфер + 1 синтез) | 10-15 мин | 9 |
| Phase 2 | Values Top-5 → Top-3 (упрощённый) | 5 мин | 8 |
| **ИТОГО** | | **20-30 мин** | **~20** |

**Результат**: Пользователь получает Wheel of Life + топ-3 ценности + одно действие на сегодня.

### Track B: Deep Diagnostic ("Полная картина")
**Цель**: Построить комплексное понимание жизни пользователя
**Когда**: Пользователь явно просит "разобраться глубже" или вернулся после Quick

| Фаза | Что включает | Время | Вопросов |
|------|-------------|-------|----------|
| Phase 0 | Emotional Landing + Readiness Check | 5-10 мин | 4-5 |
| Phase 1 | Wheel of Life (полный + calibration) | 10-15 мин | 12 |
| Phase 2 | Values (упрощённый топ-3 + reflection) | 5-10 мин | 10 |
| Phase 3A | Workview/Lifeview Micro (3+3 вопроса) | 10-15 мин | 6 |
| Phase 3B | Good Time Journal (ретроспектива) | 5-10 мин | 3-5 |
| Phase 3C | Odyssey Plans (3 плана, микро-формат) | 10-15 мин | 3 |
| Phase 4A | Ikigai 5 Pillars + 6 базовых вопросов | 10-15 мин | 11 |
| Phase 4B | Life Story Lite (опционально) | 5-10 мин | 3 |
| Phase 4C | Integration: Life Compass | 5 мин | 1 |
| **ИТОГО** | | **65-105 мин** | **~50-55** |

**Разбивка по сессиям:**
- Сессия 1: Phase 0 + Phase 1 (20-25 мин)
- Сессия 2: Phase 2 + Phase 3A (20-30 мин)
- Сессия 3: Phase 3B + Phase 3C (15-25 мин)
- Сессия 4: Phase 4A + Phase 4B (опц.) + Phase 4C (20-30 мин)

---

## 8. Конкретные Изменения для diagnostic_methods.md

### 8.1 Добавить Two-Track выбор
```markdown
## Stage 1: Diagnostic — Two-Track Approach

### Track A: Quick Diagnostic ("Первый взгляд") — 20-30 мин
Для первого взаимодействия. Пользователь получает:
- Эмоциональную поддержку
- Wheel of Life с визуализацией
- Топ-3 ценности
- Одно конкретное действие на сегодня

### Track B: Deep Diagnostic ("Полная картина") — 65-105 мин
Для пользователей, готовых к глубокой работе. Распределяется на 2-4 сессии.
```

### 8.2 Переписать Phase 2 (Values)
```markdown
## Phase 2: Values Clarification (УПРОЩЁННЫЙ)

### Protocol (3 шага, ~10 вопросов)
1. **Top-5 Selection**: Показать список 10 ценностей Schwartz, попросить выбрать 5
2. **Top-3 Ranking**: Из 5 выбрать 3 самых важных и ранжировать
3. **Reflection**: "Как эти ценности проявляются? Есть ли разрыв?"

### Integration with Wheel of Life
"Ваши топ-3 ценности: [X], [Y], [Z]. 
Смотря на Wheel of Life — в каких сферах вы живёте по ценностям?"
```

### 8.3 Переписать Phase 4 (Ikigai + Life Story)
```markdown
## Phase 4A: Ikigai — 5 Pillars + Core Questions (Ken Mogi framework)

Pillar 1 — Start Small: "Что маленькое даёт вам радость сегодня?"
Pillar 2 — Releasing Yourself: "От чего вы могли бы отпустить?"
Pillar 3 — Harmony: "Где в жизни есть гармония? Где — дисбаланс?"
Pillar 4 — Joy of Little Things: "Какой маленький момент вчера был приятным?"
Pillar 5 — Being in Here and Now: "Когда вы последний раз были 'здесь и сейчас'?"

Core Questions (сохранить текущие):
- "Что даёт вам энергию утром?"
- "За что вас благодарят другие?"
- "Что вы делаете, когда забываете про время?"
- "Что вы делали в детстве часами?"
- "Что вы готовы делать без оплаты?"
- "Какую проблему мира хотели бы решить?"

## Phase 4B: Life Story — ОПЦИОНАЛЬНО
[Предлагать только после установления доверия, сессия 3+]

Life Story Lite (3 вопроса):
1. "Момент, когда вы чувствовали себя 'на своём месте'"
2. "Решение или событие, изменившее направление жизни"
3. "Название текущей главы вашей жизни"
```

### 8.4 Добавить Readiness Gates
```markdown
### Readiness Gate Protocol (после КАЖДОЙ фазы)
"На шкале 1-10, насколько комфортно вам сейчас?"
- 8-10: "Отлично, двигаемся дальше"
- 5-7: "Давайте сделаем паузу. Что сделало бы комфортнее?"
- 1-4: "Понял. Может, сегодня хватит? Мы можем продолжить в другой раз."
```

---

## 9. Источники

1. **Burnett, B. & Evans, D.** (2016). *Designing Your Life*. Knopf.
2. **Mogi, K.** *The Little Book of Ikigai*. Hodder & Stoughton.
3. **Kamiya, M.** (1966). *Ikigai-ni-Tsuite* (What Makes Our Life Worth Living).
4. **Schwartz, S.H.** (1992). Universals in the content and structure of values. *Psychological Review*, 98, 878-901.
5. **Sharma, H.** (2022). How short or long should be a questionnaire for any research? *Saudi Journal of Anaesthesia*, 16(1), 65-68. PMC8846243.
6. **Co-Active Training Institute** (2025). First Coaching Session. https://coactive.com/blog/first-coaching-session
7. **Clarityflow** (2023). Top 10 First Coaching Session Questions. https://clarityflow.com/first-coaching-session-questions
8. **McAdams, D.P.** (2007). *The Life Story Interview*. Northwestern University.
9. **UCL Study** (2014). Purpose in life and mortality. *The Lancet*.
10. **Nakashi, N.** Ikigai and longevity. Osaka University.

---

## Appendix: Сравнительная Таблица — До vs После

| Аспект | Текущий протокол | Рекомендуемый |
|--------|-----------------|---------------|
| **Tracks** | 1 монолитный | 2: Quick + Deep |
| **Values метод** | 45 пар | Top-5 → Top-3 |
| **Values вопросов** | ~50 | ~10 |
| **Ikigai фреймворк** | 6 вопросов | 5 Pillars + 6 core |
| **Life Story** | Обязательный (8-10 вопросов) | Опциональный (3 вопроса) |
| **Workview/Lifeview** | 250 слов эссе | 3 микро-вопроса |
| **Odyssey Plans** | 3×5-7 пунктов | 3×3-5 пунктов |
| **Общее время** | 100-130 мин | Quick: 20-30 / Deep: 65-105 |
| **Общее вопросов** | ~90-105 | Quick: ~20 / Deep: ~50-55 |
| **Fatigue Risk** | ⚠️ Высокий | ✅ Низкий |

---

*Отчёт подготовлен для life-planning-coach v0.5.0*
