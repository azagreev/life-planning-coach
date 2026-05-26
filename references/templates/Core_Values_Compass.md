---
schema_version: "2.0"
template_version: "1.0"
last_updated: "YYYY-MM-DD"
purpose: "Core Values Compass — 5-7 core values + compass questions для daily decision making"
source_prd: "docs/research/prd_core_values_discovery.md"
---

# 🧭 Core Values Compass

> **Что это:** Твои 5-7 core values, выявленные через bottom-up discovery (Life Domains → Meaningful Experiences → Energizing Activities). Не абстрактные ценности из списка — а персональный компас, выведенный из твоей жизни.

> **Как использовать:** Перед важным решением задай себе compass question соответствующей value. Перед постановкой новой цели — проверь alignment.

> **Когда пересматривать:** Раз в 6-12 месяцев или после life transition.

---

## 🌟 Топ-3 (главные ориентиры)

### 1. **[Value Name]** *(CV1)*

**Описание:** [1-2 предложения, что эта value для тебя]

**Откуда выявлена:**
- 🏛️ **Domain:** `[sphere_id]`
- 💫 **Experience:** «[значимый опыт]»
- ⚡ **Energizing activity:** «[что даёт энергию]»

**Compass question:** *«[вопрос для daily decisions]»*

**Aligned goals:** G1, G3 (см. `Goals.md`)

---

### 2. **[Value Name]** *(CV2)*

**Описание:** [...]

**Откуда выявлена:**
- 🏛️ **Domain:** `[sphere_id]`
- 💫 **Experience:** «[опыт]»
- ⚡ **Energizing activity:** «[активность]»

**Compass question:** *«[...]»*

**Aligned goals:** [...]

---

### 3. **[Value Name]** *(CV3)*

**Описание:** [...]

**Откуда выявлена:**
- 🏛️ **Domain:** `[sphere_id]`
- 💫 **Experience:** «[...]»
- ⚡ **Energizing activity:** «[...]»

**Compass question:** *«[...]»*

**Aligned goals:** [...]

---

## 🌿 Расширенный набор (4-7)

### 4. **[Value Name]** *(CV4)*
- Compass: *«[question]»*
- Origin: [краткое объяснение]

### 5. **[Value Name]** *(CV5)*
- Compass: *«[question]»*
- Origin: [...]

### 6. **[Value Name]** *(CV6)*  *(optional)*
### 7. **[Value Name]** *(CV7)*  *(optional)*

---

## 🎯 Compass Mode — практическое применение

### При daily decisions
Задай compass question релевантной value перед решением. Ответ «да/нет/неясно» — индикатор alignment.

### При постановке новой цели
1. Запиши цель
2. Пройди по топ-3 values: «Эта цель усиливает [CV1], [CV2], [CV3]?»
3. Если ≥ 2 из 3 говорят «да» → high alignment
4. Если 0-1 → пересмотри Deep Why цели

### При конфликте values
Бывает, что две values тянут в разные стороны (например, Autonomy vs Security). Это не ошибка — это сигнал важного выбора. Опции:
- Найти третий путь, который удовлетворяет обе
- Принять временный приоритет одной с явным trade-off
- Обсудить в follow-up сессии

---

## 📊 Alignment Audit (по сферам Wheel of Life)

> Где твои values **проявляются** в жизни сейчас, а где — **подавляются**?

| Value | Где проявляется (sphere → как) | Где подавляется (sphere → как) |
|---|---|---|
| CV1: [Name] | `career` → ... | `social` → ... |
| CV2: [Name] | ... | ... |
| CV3: [Name] | ... | ... |

**Insight:** [куда направить энергию для большего congruence]

---

## 📜 История пересмотров

| Дата | Изменение | Контекст |
|---|---|---|
| [YYYY-MM-DD] | Initial discovery | Phase 1.5 Deep Diagnostic |
| [YYYY-MM-DD] | CV4 переименована | Уточнение после Weekly Review |
| [YYYY-MM-DD] | Добавлена CV6 | Life transition: смена работы |

---

## 🔬 Methodology footprint

Этот compass построен через гибридный синтез:
- **Values Clarification (ACT)** — психологическая гибкость
- **Meaningful Experiences** — peak experiences (Маслоу)
- **Good Time Journal** — энергия и flow (Designing Your Life, Stanford)
- **Schwartz PVQ** — кросс-культурная база (10 базовых ценностей)

Полная методология: [prd_core_values_discovery.md](../../docs/research/prd_core_values_discovery.md)

---

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  CLAUDE UPDATE RULES                                                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  1. Максимум 7 core values (приоритезация важнее inclusion).                 ║
║  2. ID: CV1, CV2, ... (стабильны, не меняются при перестановке)              ║
║  3. priority_rank в state_v2 определяет порядок в этом файле                 ║
║  4. compass_question — должен быть actionable, проверяемым в моменте         ║
║  5. derived_from — минимум 1 элемент (domain | experience | energizing)      ║
║  6. При cross-link с Goals.md — используй CV[N] идентификаторы               ║
║  7. При пересмотре — добавь запись в «История пересмотров»                   ║
║  8. Compass Mode сессии логируй в USER_PROGRESS_JOURNAL → Core_Values_Discovery║
╚══════════════════════════════════════════════════════════════════════════════╝
-->
