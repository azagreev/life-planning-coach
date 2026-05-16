# Deep Research: Communication Style Adaptation v0.6.0

> **Дата:** 2026-05-17
> **Цель:** Исследовать evidence-based модели адаптации стиля коучинга (Big Five, MI, TTM, Attachment, DISC), сравнить с текущим SKILL.md, дать рекомендации по внедрению.

---

## Executive Summary

**Вердикт:** Текущий SKILL.md v0.5.0 **уже содержит ~60% элементов** адаптивного стиля (OARS-техники из MI, autonomy support из SDT, emotional validation), но делает это **implicitly** — без системы, без mapping'а, без динамической адаптации. Ключевые гэпы:

1. Нет **trait-based mapping** (Big Five → coaching style)
2. Нет **readiness-based adaptation** (Transtheoretical Model)
3. Нет **attachment-aware protocols**
4. Нет **explicit calibration** — стиль не настраивается под пользователя

**Рекомендация:** Внедрить Communication Style Adaptation как **глобальный слой**, калибруемый в Phase 0 и динамически корректируемый на всех этапах. НЕ делать personality test — использовать implicit assessment + 2-3 calibration questions.

---

## 1. Исследованные модели

### 1.1 Big Five (OCEAN) — Trait-Based Coaching Style

**Научная база:** Costa & McCrae (1997), 30+ лет исследований, cross-cultural validation (50+ стран). Наиболее robust модель личности.

**Как трейты влияют на coaching style:**

| Трейт | Высокий балл | Низкий балл | Рекомендуемый coaching style |
|-------|-------------|------------|------------------------------|
| **Neuroticism** (Нейротизм) | Тревожность, чувствительность к критике, перегрузка стрессом | Эмоциональная стабильность, устойчивость | **High**: мягкий, валидирующий, структурированный, частые check-ins. **Low**: можно быть прямее, меньше reassurance |
| **Agreeableness** (Доброжелательность) | Эмпатия, сотрудничество, избегание конфликта | Конкурентность, прямота, скептицизм | **High**: collaborative, supportive, избегать harsh feedback. **Low**: direct, honest, challenging, results-focused |
| **Conscientiousness** (Сознательность) | Организованность, дисциплина, планирование | Гибкость, спонтанность, меньше структуры | **High**: structured, detailed, milestones, tracking. **Low**: flexible, big-picture, меньше правил |
| **Openness** (Открытость) | Креативность, любопытство, эксперименты | Конвенциональность, практичность | **High**: exploratory, metaphors, "что если?", creative exercises. **Low**: concrete, proven methods, step-by-step |
| **Extraversion** (Экстраверсия) | Энергия от людей, ассертивность, общительность | Энергия от solitude, селективное общение | **High**: energetic, enthusiastic, social check-ins. **Low**: quiet, written summaries, private reflection, less small talk |

**Критический инсайт** (из Simply.Coach, 2026): OCEAN трейты связаны с нейробиологией:
- Neuroticism → amygdala/HPA axis (stress response)
- Conscientiousness → dorsolateral PFC (planning, self-regulation)
- Extraversion → reward circuits (nucleus accumbens)
- Agreeableness → limbic system (empathy)
- Openness → prefrontal cortex + default mode network (cognitive flexibility)

**Практический вывод:** Coaching style adaptation — это не "soft skill", это **нейробиологически grounded** подход.

### 1.2 Motivational Interviewing (OARS) — Core Technique

**Научная база:** Miller & Rollnick (2002), 400+ исследований, эффективность подтверждена в addiction, health behavior, mental health.

**OARS — 4 micro-skills:**

| Skill | Описание | Уже есть в SKILL.md? |
|-------|----------|---------------------|
| **O**pen-ended questions | "Как" и "Что" вместо "Почему" (defensive). Пользователь говорит больше. | ✅ Да — "Как вы думаете?", "Что это значит для вас?" |
| **A**ffirmations | Подчёркивание сил, усилий, resilience пользователя | ✅ Да — "Это требует смелости", "Вы уже сделали важный шаг" |
| **R**eflective listening | Перефразирование, amplified reflection, double-sided reflection | ✅ Да — Emotional Landing Protocol, validation |
| **S**ummaries | Collecting + transitional summaries для организации мыслей | ⚠️ Частично — есть recap, но нет explicit summaries |

**Дополнительные техники MI:**
- **Roll with Resistance** — не спорить, принять точку зрения, вернуть инициативу пользователю
- **Develop Discrepancy** — помочь пользователю услышать расхождение между поведением и ценностями
- **Elicit-Provide-Elicit** — спросить разрешения перед информацией

**Критический инсайт:** MI и SDT (Self-Determination Theory) — **сестринские теории**. MI — это КАК вести разговор, SDT — это ПОЧЕМУ это работает (autonomy support → intrinsic motivation). В SKILL.md уже есть SDT (Core Philosophy #5), но нет явной связи с MI.

### 1.3 Transtheoretical Model (TTM / Stages of Change)

**Научная база:** Prochaska & DiClemente (1992), мета-анализ Krebs et al. (2018), 192+ цитирования.

**Стадии и coaching style:**

| Stage | Описание | Coaching role | Directiveness |
|-------|----------|--------------|---------------|
| **Precontemplation** | Не видит проблемы, отрицание, внешнее давление | **Nurturing parent** — empathy, active listening, accommodate resistance | 🟢 Низкая (non-directive) |
| **Contemplation** | Видит проблему, но ambivalent | **Socratic teacher** — challenge beliefs, elicit insights | 🟡 Средняя |
| **Preparation** | Готов к действию, собирает информацию | **Experienced coach** — co-create plan, executable steps | 🟡 Средняя |
| **Action** | Действует <6 месяцев | **Consultant** — guidance, advice, support as needed | 🔴 Высокая |
| **Maintenance** | Действует >6 месяцев | **Consultant** — relapse prevention, contingency plans | 🔴 Высокая |

**Ключевой инсайт:** TTM предсказывает терапевтический исход. Krebs et al. (2018): 76% action-stage достигли цели vs 22% precontemplation-stage. **Нельзя применять action-oriented coaching к precontemplation user.**

**Как это связано с Big Five:**
- High Neuroticism + Precontemplation = нужен nurturing parent (мягкий, validating)
- Low Agreeableness + Action = можно быть challenging consultant (direct feedback)

### 1.4 Attachment Styles

**Научная база:** Bowlby, Ainsworth → Bartholomew & Horowitz (1991), 4 стиля.

| Style | Coaching implications | Response to feedback |
|-------|----------------------|---------------------|
| **Secure** | Любой стиль работает | Принимает критику конструктивно |
| **Anxious-Preoccupied** | Нужны reassurance, consistency, frequent check-ins | Чувствителен к perceived rejection, нужна мягкая подача |
| **Avoidant-Dismissive** | Нужно пространство, indirect approach, less emotional probing | Отвергает dependency, нужен autonomy-focused approach |
| **Disorganized** | Slow pace, trauma-informed, safety first | Непредсказуемая реакция, нужен grounding |

**Практический вывод:** Attachment style — это **как пользователь относится к отношениям** (включая coaching relationship). Влияет на tolerance к challenge, need for reassurance, response to directness.

### 1.5 DISC — Behavioral Quick Mapping

**Научная база:** Marston (1928), адаптировано для coaching. Простой 4-типовой фреймворк.

| Type | Needs | Coaching style |
|------|-------|---------------|
| **D**ominance | Results, control, efficiency | Direct, bottom-line, challenges |
| **I**nfluence | Recognition, enthusiasm, social | Energetic, collaborative, celebrates wins |
| **S**teadiness | Stability, support, harmony | Patient, supportive, gradual changes |
| **C**onscientiousness | Accuracy, details, logic | Structured, evidence-based, systematic |

**Ограничение:** DISC — behavior, not personality. Человек может адаптировать behavior в разных контекстах. Но для **quick calibration** (2-3 вопроса) — полезен.

---

## 2. Сравнение с текущим SKILL.md v0.5.0

### 2.1 Что УЖЕ есть (Implicit Style Adaptation)

| Элемент | Где в SKILL.md | Как реализовано |
|---------|---------------|-----------------|
| Open-ended questions | Language Rules, Progressive Disclosure | "Как вы думаете?" вместо "Это означает..." |
| Affirmations | Emotional State Response Templates | "Вы не одиноки", "Это знакомо многим" |
| Reflective listening | Emotional Landing Protocol | VALIDATE → REFLECT → ONE THING TODAY |
| Autonomy support | Core Philosophy #5 (SDT) | "если захотите", "можно попробовать" |
| Rolling with resistance | Language Rules | Нет "надо/должен/нужно" |
| Readiness Check | Readiness Gate Protocol | 1-10 scale после каждой фазы |
| Non-judgmental tone | Safety & Ethics | "Нейтральный тон, без осуждения" |
| Commitment check | Commitment Check | "На шкале 1-10, насколько готовы?" |

**Вывод:** SKILL.md уже содержит **strong MI/SDT foundation**. Но это implicit — Claude не "знает", что он делает MI, и не адаптирует intensity техник.

### 2.2 Чего НЕТ (Critical Gaps)

| Gap | Почему важно | Научная база |
|-----|-------------|--------------|
| **Нет trait-based calibration** | Одинаковый стиль для high-N и low-N пользователя = mismatch | OCEAN neuroticism predicts stress response (PMC7923371) |
| **Нет readiness-based adaptation** | Action-oriented coaching к precontemplation user = resistance + dropout | Krebs et al. (2018): 76% vs 22% success rate |
| **Нет attachment awareness** | Anxious user + direct challenge = perceived rejection; Avoidant user + emotional probing = withdrawal | Bartholomew & Horowitz (1991) |
| **Нет dynamic adjustment** | Стиль фиксирован, не меняется в ответ на cues | MI principle: "adapt to client, not vice versa" |
| **Нет explicit "pull vs push" framework** | MI ядро — pull (eliciting) vs push (directing). SKILL.md делает pull, но не называет это так | Miller & Rollnick (2002) |
| **Нет calibration questions** | Пользователь не может сказать "мне нужен softer tone" | User-centered design principle |

---

## 3. Анализ JSON-спека пользователя

### 3.1 Что хорошо в спеке

| Элемент спека | Оценка | Почему |
|---------------|--------|--------|
| **3 уровня**: explicit calibration → implicit assessment → dynamic adaptation | ✅ Отлично | Соответствует best practice: explicit для clarity, implicit для depth, dynamic для responsiveness |
| **Big Five + MI hybrid** | ✅ Отлично | OCEAN даёт trait-основу, MI даёт техники. Комплементарны. |
| **Calibration questions (3-5)** | ✅ Хорошо | Не перегружает, даёт baseline. Но 5 — это уже много для Phase 0. |
| **"Pull vs Push"** | ✅ Отлично | Ядро MI. Нужно явно внедрить. |
| **Resistance detection** | ✅ Хорошо | Важно для dynamic adaptation. |
| **Language rules: forbidden words** | ✅ Уже есть | Но можно расширить с учётом personality |

### 3.2 Что нужно доработать

| Элемент спека | Проблема | Рекомендация |
|---------------|----------|-------------|
| **"If personality data available, enhance with trait-specific adjustments"** | В claude.ai нет persistent personality data между сессиями (кроме Memory) | Использовать Claude Memory для хранения стилевых предпочтений |
| **5 calibration questions** | Phase 0 уже занимает 5-10 мин. + 5 вопросов = 15+ мин до ценности | Сократить до **2-3 вопроса** или сделать inline (встроенными в emotional landing) |
| **"Adjust every N messages"** | Слишком frequent → раздражает. Слишком rare → не адаптируется | Adjust по **триггерам**: resistance detected, emotional shift, stage transition |
| **Нет TTM integration** | Спек фокусируется на traits, но игнорирует readiness stage | Добавить readiness stage detection в implicit assessment |
| **"Goal ownership language"** | Это часть MI (autonomy support), но можно уточнить | "Ты выбираешь" vs "Давайте выберем" — linguistic marker autonomy |

### 3.3 Архитектурное решение: ГДЕ внедрять?

**Вариант A:** Phase 0 (Emotional Landing) + Style Calibration — 2-3 вопроса inline
**Вариант B:** Глобальный слой — apply to ALL stages
**Вариант C:** Отдельный "Session 0" перед Stage 1

**Рекомендация: Вариант A + B**

```
Phase 0: Emotional Landing + Style Calibration (2-3 вопроса inline)
  └── Результат: baseline style profile (soft/structured/direct/exploratory/energetic)

Все Stages (1, 1.5, 2, 3):
  └── Dynamic Adaptation Layer
        ├── Триггеры: resistance, emotional shift, stage transition
        ├── Implicit cues: verbosity, question type preference, emotional language
        └── Adjustment: tone, structure, directiveness, pace
```

Почему не Session 0: **Zero-Setup Default** — пользователь начинает работу сразу. Нельзя добавлять ещё одну сессию перед ценностью.

Почему не только Phase 0: стиль может меняться между сессиями (user может быть в разном состоянии, на разных стадиях TTM).

---

## 4. Рекомендуемая модель: Adaptive Coaching Matrix v1.0

### 4.1 Основная матрица: Big Five → Coaching Style

```
                    DIRECTIVENESS
                 Low ◄─────────► High
                 Non-directive   Directive
         ┌─────────────────────────────────────┐
   High  │  Nurturing      │  Challenging      │
   Structure│  Parent (High N)│  Consultant (Low A)│
         │  ───────────────│───────────────────│
   Low   │  Exploratory    │  Collaborative    │
  Structure│  Guide (High O) │  Partner (High A) │
         └─────────────────────────────────────┘
```

**Четыре квадранта:**

| Квадрант | Трейты | Стиль | Когда использовать |
|----------|--------|-------|-------------------|
| **Nurturing Parent** | High Neuroticism + любая структура | Мягкий, валидирующий, структурированный, частые check-ins | Precontemplation, emotional distress, high anxiety |
| **Challenging Consultant** | Low Agreeableness + High Structure | Прямой, results-focused, challenging, минимум fluff | Action stage, high conscientiousness, user asks for directness |
| **Exploratory Guide** | High Openness + Low Structure | Креативный, "что если?", metaphors, flexible | Contemplation, creative blocks, exploring alternatives |
| **Collaborative Partner** | High Agreeableness + Low Structure | Поддерживающий, co-creative, empathy-first | Preparation, relationship-focused goals, team coaching |

### 4.2 Cross-cutting dimensions

**Extraversion** (энергия):
- High: Enthusiastic tone, social check-ins, celebrates wins vocally
- Low: Quiet tone, written summaries, private reflection time, less small talk

**Conscientiousness** (структура):
- High: Detailed plans, milestones, tracking, agendas
- Low: Big picture, flexible, "let's see what works", less rules

### 4.3 TTM Overlay (readiness-based directiveness)

```
Stage            Directiveness    Coaching Style
─────────────────────────────────────────────────
Precontemplation    LOW          Nurturing Parent
Contemplation       LOW-MED      Exploratory Guide / Socratic Teacher
Preparation         MED          Collaborative Partner / Experienced Coach
Action              MED-HIGH     Challenging Consultant / Consultant
Maintenance         HIGH         Consultant (relapse prevention)
```

### 4.4 Attachment Overlay (relationship dynamics)

```
Style              Need                        Adjustment
─────────────────────────────────────────────────────────
Secure             Standard                    None needed
Anxious            Reassurance, consistency    More affirmations, predictable structure
Avoidant           Space, autonomy             Less emotional probing, more indirect
Disorganized       Safety, slow pace           Trauma-informed, grounding techniques
```

### 4.5 MI Technique Intensity

```
                    Pull (Eliciting)          Push (Directing)
                    ◄─────────────────────────────────────►
    
    High N / Precontemplation          High C + Action stage
    → 80% pull, 20% push               → 40% pull, 60% push
    → OARS heavy                       → OARS light, more guidance
    → Rolling with resistance          → Direct advice when asked
    → Develop discrepancy gently       → Challenge when invited
```

---

## 5. Интеграция с текущим SKILL.md

### 5.1 Минимальные изменения (MVP)

**Добавить в Core Philosophy:**
```
8. **Adaptive Style**: Стиль коучинга адаптируется под пользователя.
   Не "один размер подходит всем" — а "meet them where they are".
   Используем implicit assessment + 2-3 calibration questions.
```

**Добавить в Phase 0 (inline, 2 вопроса, 1 минута):**
```
Style Calibration (опционально, inline):
1. "Когда вы получаете feedback — что для вас комфортнее: 
    мягкая поддержка или прямая правда?" (soft vs direct)
2. "Что вам ближе: чёткий план с шагами или свобода экспериментировать?" 
    (structured vs exploratory)
```

**Добавить Language Rules:**
```
5. **Goal Ownership Language**: 
   - "Ты решаешь" (autonomy) vs "Давайте решим" (collaboration)
   - "Что для тебя важно?" (pull) vs "Вот что важно:" (push)
   - "Если захочешь" (permission) vs "Нужно сделать" (pressure)
```

**Добавить Dynamic Adaptation triggers:**
```
Триггеры для корректировки стиля:
- Пользователь говорит "не знаю", "может быть", "не уверен" → усилить pull (OARS)
- Пользователь говорит "давайте действовать", "что дальше?" → можно push
- Пользователь отвечает коротко, закрывается → soften, validate, give space
- Пользователь просит "будьте прямее" → increase directness
- Emotional distress detected → nurturing parent mode
```

### 5.2 Средние изменения (v0.6.0)

**Добавить новый reference:** `references/communication_style.md`
- Big Five → Coaching Style mapping
- TTM stage detection cues
- Attachment style cues
- MI technique intensity guidelines
- OARS cheat sheet for Claude

**Обновить Conversation State JSON:**
```json
{
  "communication_style": {
    "baseline": {
      "softness": "soft|neutral|direct",
      "structure": "high|medium|low",
      "energy": "high|medium|low",
      "exploratory": "high|medium|low"
    },
    "ttm_stage": "precontemplation|contemplation|preparation|action|maintenance",
    "current_intensity": "nurturing|exploratory|collaborative|challenging",
    "last_adjustment_reason": "resistance_detected|user_request|stage_transition|..."
  }
}
```

### 5.3 Большие изменения (v0.7.0+)

- Attachment style detection protocol
- Full DISC quick assessment
- Style history tracking (how style evolved)
- Cross-session style consistency analysis

---

## 6. Что НЕ внедрять (и почему)

| Концепция | Почему не внедрять | Альтернатива |
|-----------|-------------------|-------------|
| **Explicit Big Five test (10-50 вопросов)** | Breaks flow, assessment fatigue, too clinical | Implicit assessment + 2-3 calibration questions |
| **DISC as primary framework** | DISC simpler but less nuanced than Big Five; overlaps with OCEAN Conscientiousness | Use DISC only for quick behavioral cues, not primary |
| **Attachment style explicit test** | Too intimate for early sessions; trauma triggers | Implicit cues only (response to validation, need for space) |
| **"Adjust every N messages"** | Too rigid; style should adapt to content, not message count | Trigger-based adjustment |
| **Formula-based style score** | Same problem as True Goal Score formula — arbitrary weights | Qualitative mapping with clear guidelines |

---

## 7. Итоговая рекомендация для v0.6.0

### Что внедрить:
1. ✅ **Communication Style Calibration** — 2 вопроса inline в Phase 0
2. ✅ **Adaptive Coaching Matrix** — 4 квадранта (Nurturing/Challenging/Exploratory/Collaborative)
3. ✅ **TTM Overlay** — readiness-based directiveness
4. ✅ **Dynamic Adaptation triggers** — 5 триггеров для корректировки стиля
5. ✅ **OARS explicit framework** — назвать техники, которые уже есть в SKILL.md
6. ✅ **Goal Ownership Language rules** — linguistic markers autonomy
7. ✅ **New reference file** — `references/communication_style.md`

### Что НЕ внедрять:
1. ❌ Explicit personality tests (Big Five, DISC, Attachment)
2. ❌ Formula-based style scoring
3. ❌ "Adjust every N messages"
4. ❌ Separate "Session 0" for style calibration

### Архитектурное решение:
- **Style Calibration** — часть Phase 0 (2 вопроса, 1 минута, опционально)
- **Dynamic Adaptation** — глобальный слой, применяется ко всем stages
- **Reference** — `references/communication_style.md` (детальные протоколы)

---

## 8. Источники

1. **Costa, P.T. & McCrae, R.R.** (1997). *Revised NEO Personality Inventory (NEO-PI-R)*. Psychological Assessment Resources.
2. **Miller, W.R. & Rollnick, S.** (2002). *Motivational Interviewing: Preparing People for Change* (2nd ed.). Guilford Press.
3. **Prochaska, J.O. & DiClemente, C.C.** (1992). Stages of change in the modification of problem behaviors. *Progress in Behavior Modification*, 28, 183-218.
4. **Krebs, P., Norcross, J.C., Nicholson, J.M., & Prochaska, J.O.** (2018). Stages of change and psychotherapy outcomes: A review and meta-analysis. *J Clin Psychol*, 74(11), 1964-1979.
5. **Bartholomew, K. & Horowitz, L.M.** (1991). Attachment styles among young adults: A test of a four-category model. *JPSP*, 61(2), 226-244.
6. **Deci, E.L. & Ryan, R.M.** (2000). The "what" and "why" of goal pursuits. *Psychological Inquiry*, 11(4), 227-268.
7. **Markland, D., Ryan, R.M., Tobin, V.J., & Rollnick, S.** (2005). Motivational interviewing and self-determination theory. *J Soc Clin Psychol*, 24(6), 811-831.
8. **Simply.Coach** (2026). OCEAN Personality Model: What the Big Five Traits Mean for Coaching.
9. **Relias** (2026). How to Use OARS Skills in Motivational Interviewing.
10. **NCBI StatPearls** (2023). Stages of Change Theory (Raihan & Cogburn).
11. **Crowe Associates** (2025). The "big 5" Personality traits in Coaching.
12. **Lift The Bar** (2025). How to Adapt Your Coaching Style to Different Personality Types.
13. **NIDA** (2002). OARS Model: Essential Communication Skills.
