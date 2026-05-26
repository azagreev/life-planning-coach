# Module: Phase 1.5 — Authentic Goal Filter + Core Values Discovery

> **Tier:** 2 (lazy-load module)
> **Загружается:** после Phase 1, перед Phase 2. Цель — отделить аутентичные цели от интроектов.
> **Предусловие:** Wheel of Life и хотя бы Top-3 ценности уже определены.
> **Связанные refs:** `authentic_goal_filter.md`, `weak_goal_taxonomy.md`, `win_alert.md`

---

## Entry triggers

- «Хочу поставить цели» (после диагностики)
- «У меня есть цель, проверь её»
- «Не знаю, что я на самом деле хочу»
- «Мне всё время кажется, что это не моё»
- Обнаружение Red Flag в формулировке цели (см. ниже)

---

## Core Values Discovery (bottom-up, опционально, 15–20 минут)

> Используй ТОЛЬКО если у пользователя нет ясности по топ-3 ценностям, либо если он сам сомневается («это вроде мои ценности, но не уверен»).

Альтернатива top-down PVQ — три шага снизу вверх:

### Шаг 1: Life Domains (5 минут)
Спроси: «В каких сферах жизни ты ощущаешь себя живым / целым? Назови 2–3.»
Запиши **дословно** — это сигналы.

### Шаг 2: Meaningful Experiences (5–7 минут)
Для каждого домена: «Вспомни конкретный момент за последние 12 месяцев, когда ты в этой сфере чувствовал — да, это оно».
Слушай **что именно** в моменте было ценно: автономия? связь? мастерство? щедрость? честность?

### Шаг 3: Energizing Activities (5–7 минут)
«Какие действия за последний месяц давали тебе энергию, а не забирали?»
Связь между активностью и ценностью часто прямая: «помогал брату с переездом» → contribution / family / mastery.

### Synthesis
Из 3 источников (домены + моменты + активности) собери 3–5 кандидатов в core values. Дай пользователю подтвердить или скорректировать.

Запиши каждую ценность в `state.diagnosis.core_values[]` с полями:
- `value_id`: `CV1`, `CV2`, ... (стабильный, не переиспользовать)
- `name` (1–3 слова), `description` (2–3 предложения)
- `derived_from[]`: `[{type: "domain"|"experience"|"energizing_activity", ref}]` — обязательно ≥ 1 запись на ценность
- `priority_rank` (1–7), `discovered_at`, `last_reviewed`
- `compass_question` — формулируется в **Compass Mode** ниже

---

## Compass Mode (FR-04 Practical Application)

3–5 core values → инструмент ежедневных решений (FR-04 из `docs/research/prd_core_values_discovery.md`).

### Compass Questions (по 1 на ценность)

Шаблоны: «Расширяет ли этот выбор моё [name], или сужает?» / «Действую сейчас из [name] или против?»
Примеры: Autonomy → «Увеличивает мою свободу?»; Mastery → «Я расту или повторяю?»; Contribution → «Что от этого получает кто-то кроме меня?»

Запиши в `state.diagnosis.core_values[i].compass_question`.

### Daily Decision Protocol (3 шага, ≤ 60 сек)

1. **Pause** — назови выбор.
2. **Compass question** — задай вопрос топ-ценности.
3. **Decision** — действие, согласное с ответом. Не сходится — назови цену и решай осознанно.

Не «правильно/неправильно» — «алигнед или нет».

### Alignment Audit (в Phase 3, 3-5 мин)

Таблица: Ценность | Где жил из неё | Где разъезд | Что в понедельник. Шаблон — `references/templates/Core_Values_Compass.md`.

### Link с Authentic Goal Filter

При добавлении цели — **обязательно** `core_values_alignment: ["CV1", "CV3"]` (≥ 1). Без alignment цель не проходит без явного «почему важно несмотря на».

---

## Authentic Goal Filter (для каждой цели)

### 1. Red Flag Detector (6+1)
Скрининг шести паттернов навязанности + общий маркер:
1. «Все вокруг…» (social comparison)
2. «Я должен…» (introjected obligation)
3. «Если не сделаю — я неудачник» (contingent self-worth)
4. «Так положено в моём возрасте» (developmental script)
5. «Родители / партнёр ждут» (external pressure)
6. «Я когда-то этого хотел» (fossilized goal)
+ Общий: телесная тяжесть, а не лёгкость

≥ 2 флага → высокая вероятность интроекта. Углубляйся через Deep Why.

### 2. Values Alignment (1–10)
По каждой топ-3 ценности: «Насколько цель служит X?» < 5 хотя бы по одной → конфликт, обсуди.

### 3. Energy Check (соматический, опционально)
«Закрой глаза, представь цель достигнутой. Расширение или сжатие?» Сжатие — стоп-сигнал, данные.

### 4. Deep Why (3 уровня)
Спрашивай «почему?» три раза подряд:
- L1: внешняя («больше зарабатывать»)
- L2: функциональная («стабильность»)
- L3: бытийная («не бояться»)

L3 = страх / стыд / долг → цель введена извне.

### 5. Societal Pressure Test (4 вопроса)
1. Если бы никто не узнал — ты бы её делал?
2. Если ещё 10 лет жизни — отложил или ускорил?
3. Эта цель из внешних сигналов или из тишины?
4. Что теряешь, отказавшись? — статус? облегчение?

### 7. Partner Coordination Check (опц., schema v2.2+)

**Триггер:** маркеры «партнёр / жена / муж / семья / we / наш / вместе» в формулировке цели.

3 вопроса (Goal Concordance, Rosta-Filep 2023):
1. **Communication (1-10):** «Насколько обсуждал цель с партнёром?»
2. **Cooperation (1-10):** «Где может поддержать / препятствия со стороны отношений?»
3. **Compatibility (1-10):** «Совместимость с приоритетами партнёра?»

**Disclaimer:** «Это coaching, не therapy. При кризисе в отношениях — к специалисту.»

Запиши в `goal_filter.active_goals[].partner_coordination = {communication, cooperation, compatibility, obstacles[]}`. Индивидуальная цель → `null`.

---

### 8. True Goal Score — Радар (НЕ формула!)
5 осей (1–10): **Ценности** / **Энергия** / **Влияние** (на Wheel of Life) / **Реалистичность** / **Аутентичность**. Радар асимметричный → цель требует доработки. Не суммируй — показывай форму.

---

## Goal Portfolio + Weak Patterns

Корзины: 🟢 Active → Phase 2 | 🟡 On Pause (re-check 3 мес) | 🔍 Pattern Analysis. 🎉 Прошедшая фильтр цель + инсайт → `references/win_alert.md`.

**Weak formulations** (vague / negation / no-time / external / unrealistic) → `references/weak_goal_taxonomy.md` + Sanity-Check.

---

## State writes

В конце Phase 1.5 запиши в state v2 (`references/state_v2_schema.md`):

**Core Values:**
- `diagnosis.core_values[]`: `[{value_id (CV1+), name, description, derived_from: [{type: "domain"|"experience"|"energizing_activity", ref}], compass_question, priority_rank (1–7), discovered_at, last_reviewed}]`
- `diagnosis.core_values_source`: `"pvq_topdown"|"bottomup_discovery"|"mixed"`

**Goal Filter portfolio:**
- `goal_filter.active_goals[]`: `{goal_id, title, radar{values,energy,impact,feasibility,authenticity}, core_values_alignment: ["CV1","CV3"] (≥ 1 обязательно), deep_why_chain, red_flags_screened, societal_pressure_score (1–10), partner_coordination: null|{communication,cooperation,compatibility,obstacles} (v2.2+, для партнёрских целей), added_at}`
- `goal_filter.paused_goals[]`: `{goal_id, title, red_flags, insight, paused_at}` для 🟡 On Pause
- `goal_filter.patterns[]`: `{pattern_id, red_flag, count, insight}` для 🔍 — инкрементируй counter

**Session:** `completed_phases` append `"1.5"`.

Запись через `references/templates/Goals.md` (radar блок) и `references/templates/Core_Values_Compass.md` (compass per value).

---

## Common exit transitions

- **Phase 2** — для 🟢 Active целей → `references/module_phase2_goal_architecture.md`
- **Phase 0.5 ER** — если всплыла сильная эмоция; **Pause** — если ≥ 50% = интроекты.

---

## Gotchas

- **НЕ обесценивай** цели пользователя. Фильтр = «твоя или чужая», не «плохая».
- **НЕ оценивай** Goal Score числом. Форма радара, не сумма.
- **НЕ выкидывай** 🟡 On Pause — часто становятся 🟢 через 3–6 мес.
- **НЕ применяй** Core Values Discovery если есть ясные топ-3.
- **ВСЕГДА** skip option, особенно для соматики.
- **ВСЕГДА** Red Flags ДО Phase 2 Architecture.
