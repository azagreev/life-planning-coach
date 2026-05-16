# Аудит диагностического протокола v0.5.0 vs JSON-спек

> **Дата:** 2026-05-17
> **Цель:** Выявить, что именно "не корректно" в текущем протоколе, и как внедрить концепции из JSON-спека

---

## Executive Summary

**Вердикт:** Текущий протокол v0.5.0 — это **отличная диагностика текущего состояния**, но **слабая фильтрация целей**. Он показывает "где вы" и "что вам важно", но НЕ отвечает на ключевой вопрос: **"Это твоя цель или навязанная?"**

JSON-спек предлагает критически важный недостающий слой — **Authentic Goal Filter** — который должен стоять между диагностикой (Stage 1) и постановкой целей (Stage 2).

---

## 1. Что именно не так в текущем протоколе

### Проблема 1: Диагностика → Цели, без фильтра

**Текущий поток (v0.5.0):**
```
Emotional Landing → Wheel of Life → Values → Workview/Lifeview → Ikigai → ЦЕЛИ (Stage 2)
```

**Что здесь не так:**
- Пользователь после диагностики знает свои ценности и видит "картину жизни"
- Но когда он начинает ставить цели — нет **явного фильтра** на аутентичность
- Пример: человек с высоким Power и Achievement ставит цель "стать CEO" — но это может быть навязанная цель родителей/социума

**Критичность:** 🔴 ВЫСОКАЯ — Self-Concordance Research (Sheldon & Elliot, 1999) показывает, что только самосогласованные цели дают well-being + attainment. Несамосогласованные цели — burnout.

### Проблема 2: Отсутствие Energy Check в моменте

**Текущий протокол:**
- Good Time Journal (Phase 3B) — ретроспектива: "Вспомните последние 3 дня, сколько энергии давало?"
- Это полезно, но это **прошлое**, не **настоящее**

**Что нужно (из спека):**
- Energy Check при выборе цели: "Какое ощущение в теле, когда вы думаете об этой цели? Лёгкость или тяжесть?"
- Это somatic marker (Damasio, 1996) — тело реагирует на аутентичные/неаутентичные цели до того, как мозг осознает

**Критичность:** 🟡 СРЕДНЯЯ — Somatic Marker Hypothesis подтверждена нейробиологически, но в коучинге — дополнительный инструмент, не замена.

### Проблема 3: Нет Deep Why для целей

**Текущий протокол:**
- Values Clarification спрашивает "Что важно?"
- Ikigai спрашивает "Что даёт энергию?"
- Но при постановке конкретной цели — нет "копания" до корневой причины

**Что нужно (из спека):**
- Deep Why (5 уровней) применительно к конкретной цели
- Пример: "Хочу выучить английский" → Why? → Why? → Why? → до корневой мотивации

**Критичность:** 🟡 СРЕДНЯЯ — 5 Whys работает, но может быть избыточно (3 уровня часто достаточно).

### Проблема 4: Нет Societal Pressure Test

**Текущий протокол:**
- Values Clarification (Schwartz PVQ) показывает что важно
- Но НЕ проверяет: "А это твоё или общества?"

**Что нужно (из спека):**
- 4 ключевых вопроса:
  1. "Если бы никто никогда не узнал — хотел бы всё равно?"
  2. "Это моя цель или цель 'успешного человека'?"
  3. "Я хочу или мне стыдно/страшно, что нет?"
  4. "Цель даёт свободу/рост или статус/одобрение?"

**Критичность:** 🔴 ВЫСОКАЯ — напрямую связана с self-concordance и burnout prevention.

### Проблема 5: 8 доменов vs 10 доменов Wheel of Life

**Текущий протокол:** 8 + 1 опциональный (Meaning)
**JSON-спек:** 10 доменов (добавлены Social отдельно, Contribution)

**Анализ:**
- Разделение Family/Friends на Family + Social — логично, семья и друзья — разные сферы
- Добавление Contribution (вклад в общество) — важно для ikigai и смысла (Frankl)
- Meaning уже есть как опциональный — можно сделать обязательным

**Критичность:** 🟢 НИЗКАЯ — улучшение, но не критично для core функционала.

---

## 2. Анализ концепций из JSON-спека

### 2.1 Authentic Goal Filter

**Оценка:** ✅ ОТЛИЧНАЯ КОНЦЕПЦИЯ, НУЖНО ВНЕДРЯТЬ

Это именно то, чего не хватает между Stage 1 (диагностика) и Stage 2 (цели). Структура:
```
1. Values Alignment — оценить по топ-5 ценностям (1-10)
2. Energy Check — ощущения в теле
3. Deep Why (5 уровней)
4. Societal Pressure Test — 4 вопроса
5. True Goal Score — автоматический расчёт
```

**Научная база:**
- Self-Concordance (Sheldon & Elliot, 1999): цели aligned with values → higher well-being + attainment
- SDT (Deci & Ryan): intrinsic goals > extrinsic for well-being
- Somatic Marker Hypothesis (Damasio): тело знает до мозга

**Рекомендация по адаптации:**
- 5 уровней Deep Why → 3 уровня (5 часто избыточно, user fatigue)
- Energy Check — добавить как опциональный (не все чувствуют тело)
- Societal Pressure Test — обязательный, 4 вопроса отличные

### 2.2 HARD ("High Arousal, Reactive Desire")

**⚠️ ВАЖНОЕ РАСХОЖДЕНИЕ**

В JSON-спеке HARD = "High Arousal, Reactive Desire" — это переосмысление/ошибка.

**Настоящий HARD Goals (Mark Murphy, Leadership IQ, 4000+ людей, 397 организаций):**
- **H**eartfelt — эмоциональная связь
- **A**nimated — визуализация (можешь "увидеть" результат)
- **R**equired — чувство срочности
- **D**ifficult — выходит из зоны комфорта

**Research findings:**
- Только 15% людей с SMART goals считают, что они помогут достичь чего-то великого
- HARD goals коррелируют с engagement: +49% (Animated), +57% (Required), +29% (Difficult), +75% (Alignment)

**Рекомендация:**
- Использовать **настоящий** HARD от Mark Murphy (Heartfelt, Animated, Required, Difficult)
- Концепция "High Arousal, Reactive Desire" из спека — это не validated framework
- Можно адаптировать: Heartfelt + Animated уже есть в спеке (Energy Check + Deep Why)

### 2.3 True Goal Score

**Формула из спека:**
```
(values_alignment * 2) + energy_check + impact + (feasibility * 0.8) + (opportunity_window * 0.7)
```

**Критический анализ:**
- Веса (2.0, 1.0, 0.8, 0.7) — **не validated** научно
- Values Alignment * 2 — самый большой вес, логично (self-concordance)
- Energy Check = 1.0 — слишком много для субъективной метрики
- Feasibility * 0.8 — ниже, чем Energy Check — спорно

**Рекомендация:**
- Сохранить концепцию scoring, но **упростить формулу**
- Использовать ранжирование по категориям, не формулу
- Или: Simple Weighted Score с прозрачными весами

### 2.4 10-доменный Wheel of Life

**Сравнение:**

| v0.5.0 (8+1) | JSON-спек (10) | Разница |
|-------------|----------------|---------|
| Health | Health | = |
| Finances | Finances | = |
| Career | Career | = |
| Significant Other / Romance | Romance | = |
| Family / Friends | Family | Разделено |
| — | Social (друзья) | Новый |
| Personal Growth | Growth | = |
| Fun / Recreation | Fun | = |
| Physical Environment | — | Убран? |
| — | Meaning / Spirituality | Был опц. → обязат. |
| — | Contribution | Новый |

**Рекомендация:**
- Разделить Family/Friends ✅
- Добавить Contribution ✅ (важно для ikigai и Frankl)
- Оставить Physical Environment ❌ (нельзя убирать — окружение влияет на well-being)
- Meaning сделать обязательным ✅

**Итого: 11 доменов** или 10 если объединить что-то.

---

## 3. Рекомендуемая архитектура: v0.6.0

### Новый поток: Stage 1 → Stage 1.5 → Stage 2

```
Stage 1: Diagnostic (v0.5.0, без изменений)
  ├── Emotional Landing
  ├── Wheel of Life (10 domains)
  ├── Values Clarification
  ├── Designing Your Life
  └── Ikigai + Life Story

Stage 1.5: Authentic Goal Filter (НОВОЕ)
  ├── 1. Values Alignment Check
  ├── 2. Energy Check (HARD Heartfelt + Somatic)
  ├── 3. Deep Why (3 уровня)
  ├── 4. Societal Pressure Test (4 вопроса)
  └── 5. True Goal Score (simplified)

Stage 2: Goal Architecture (BHAG → OKR → WOOP)
  └── Только цели, прошедшие фильтр
```

### Authentic Goal Filter — детальный протокол

```markdown
## Authentic Goal Filter v1.0

### Когда применять
После Stage 1 (диагностика), перед Stage 2 (цели).
Для КАЖДОЙ цели, которую пользователь хочет поставить.

### Шаг 1: Values Alignment (1-10)
"Оцените, насколько эта цель соответствует вашим топ-3 ценностям:
- [Ценность 1]: ___/10
- [Ценность 2]: ___/10  
- [Ценность 3]: ___/10"

### Шаг 2: Energy Check (HARD Heartfelt + Somatic)
"Закройте глаза и представьте, что цель уже достигнута.
Какое ощущение в теле? Лёгкость, тепло, расширение — или тяжесть, сжатие, напряжение?"

[Если пользователь не чувствует тело — пропустить]

### Шаг 3: Deep Why (3 уровня)
"Почему вы хотите эту цель?"
→ "Почему это важно?"
→ "Почему это важно на самом деле?"

### Шаг 4: Societal Pressure Test (4 вопроса)
1. "Если бы никто никогда не узнал о вашем достижении — вы бы всё равно хотели эту цель?"
2. "Это цель 'успешного человека' в вашем окружении или именно ваша?"
3. "Вы хотите это или вам стыдно/страшно, что у вас этого нет?"
4. "Эта цель даёт свободу и рост или статус и одобрение других?"

### Шаг 5: True Goal Score (Simplified)
```
| Критерий | Балл | Вес | Итого |
|----------|------|-----|-------|
| Соответствие ценностям (среднее) | _/10 | ×2 | __ |
| Энергия (лёгкость = 10, тяжесть = 0) | _/10 | ×1 | __ |
| Влияние на жизнь | _/10 | ×1 | __ |
| Реалистичность | _/10 | ×0.8 | __ |
| Окно возможностей | _/10 | ×0.7 | __ |
| **ИТОГО (макс 44)** | | | **__** |
```

**Интерпретация:**
- ≥ 35 (≥80%) — аутентичная цель, брать в работу
- 25-34 (55-80%) — пересмотреть, возможно навязанная
- < 25 (<55%) — скорее всего навязанная, отсеять

### Результат фильтра
- Зелёные цели (≥35) → Stage 2
- Жёлтые (25-34) → "Давайте посмотрим глубже" → ещё один цикл фильтра
- Красные (<25) → "Отсеяно: [причина]" → добавить в "Отсеянные цели"
```

### Обновление Wheel of Life (10 → 11 доменов)

```markdown
1. 🏥 Здоровье и физическая форма
2. 💰 Финансы и материальное благополучие
3. 💼 Карьера и работа
4. 👨‍👩‍👧 Семья и близкие
5. 💕 Романтика и партнёрство
6. 👥 Дружба и социальные связи
7. 🌱 Личностный рост и обучение
8. 🧘 Духовность, смысл и ценности
9. 🎉 Отдых, хобби и радость
10. 🌍 Вклад в общество и наследие
11. 🏠 Дом и окружение
```

---

## 4. Что НЕ внедрять (и почему)

| Концепция из спека | Почему не внедрять | Альтернатива |
|-------------------|-------------------|-------------|
| HARD = "High Arousal, Reactive Desire" | Не validated, не Mark Murphy | Использовать настоящий HARD (Heartfelt, Animated, Required, Difficult) |
| True Goal Score formula с весами 2.0/0.8/0.7 | Веса произвольны, нет научной базы | Simplified scoring с прозрачной интерпретацией |
| 5 уровней Deep Why | User fatigue, 3 часто достаточно | Deep Why Lite (3 уровня) |

---

## 5. Итоговая рекомендация

### Внедрить в v0.6.0:
1. ✅ **Authentic Goal Filter** как Stage 1.5 — критически важно
2. ✅ **Societal Pressure Test** (4 вопроса) — ядро фильтра
3. ✅ **Energy Check** (сomatic marker) — опционально
4. ✅ **Deep Why (3 уровня)** — для каждой цели
5. ✅ **11-доменный Wheel of Life** — улучшение диагностики
6. ✅ **True Goal Score (упрощённый)** — для прозрачности

### Не внедрять:
1. ❌ "HARD = High Arousal Reactive Desire" — использовать настоящий HARD Mark Murphy
2. ❌ Сложную формулу с произвольными весами — упростить
3. ❌ 5 уровней Deep Why — достаточно 3

### Важное архитектурное решение
**Authentic Goal Filter должен быть отдельным Stage 1.5**, не частью Stage 1 или Stage 2. Это bridge между "пониманием себя" и "постановкой целей".

---

## 6. Источники

1. **Sheldon, K.M. & Elliot, A.J.** (1999). Goal striving, need satisfaction, and longitudinal well-being. *Journal of Personality and Social Psychology*, 76(3), 482-497.
2. **Deci, E.L. & Ryan, R.M.** (2000). The "what" and "why" of goal pursuits. *Psychological Inquiry*, 11(4), 227-268.
3. **Damasio, A.R.** (1996). The somatic marker hypothesis and the possible functions of the prefrontal cortex. *Philosophical Transactions of the Royal Society*, 351, 1413-1420.
4. **Murphy, M.** (2010). *HARD Goals: The Secret to Getting from Where You Are to Where You Want to Be*. McGraw-Hill.
5. **Murphy, M.** (2017). HARD Goals, Not SMART Goals, Are The Key To Career Development. *Forbes*.
6. **Start of Happiness** (2013). The 5 Whys Template and How You Can Create Sustained Motivation.
7. **Frankl, V.E.** (1946). *Man's Search for Meaning*.
