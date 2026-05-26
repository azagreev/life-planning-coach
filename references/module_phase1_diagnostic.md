# Module: Phase 1 — Diagnostic

> **Tier:** 2 (lazy-load module)
> **Загружается:** когда пользователь готов к оценке текущего состояния после Phase 0 Emotional Landing.
> **Предусловие:** Readiness Gate ≥ 6 после Emotional Landing.
> **Связанные refs:** `diagnostic_methods.md`, `emotion_regulation.md`, `communication_style.md`

---

## Entry triggers

- «Хочу понять, где я сейчас»
- «Сделаем Wheel of Life»
- «Какие у меня ценности?»
- «Разберёмся в себе»
- «Помоги увидеть картину целиком»

---

## Track selection

Выбери трек в зависимости от готовности пользователя:

**Track A: Quick Diagnostic** (20–30 мин, 1 сессия):
1. Wheel of Life (11 сфер, оценки 1–10)
2. Values Top-5 → Top-3 (упрощённый PVQ)
3. Результат: Wheel of Life + топ-3 ценности + одно действие на сегодня

**Track B: Deep Diagnostic** (65–105 мин, 2–4 сессии):
1. Wheel of Life (полный + calibration вопрос)
2. Values (топ-3 + reflection)
3. Workview / Lifeview Micro
4. Good Time Journal (ретроспектива)
5. Odyssey Plans (микро-формат)
6. Ikigai 5 Pillars + core questions
7. Life Story Lite (опционально)

**Подсказка пользователю** (после выбора): «Я могу сделать быстро (~30 мин) и дать тебе картину сегодня, или глубже за 2–4 встречи. Что тебе сейчас ближе?»

**Загрузи `references/diagnostic_methods.md`** перед выполнением — там калибровочные вопросы и полные протоколы.

---

## 11 канонических сфер Wheel of Life

`health`, `finances`, `career`, `family`, `romance`, `social`, `personal_growth`, `meaning`, `fun_recreation`, `contribution`, `physical_environment`.

Используй именно эти 11 — это контракт со схемой v2 и HTML-дашбордом. Не подменяй на «работа/деньги/духовность» — именования фиксированы.

---

## Readiness Gate Protocol

После КАЖДОЙ фазы (Wheel, Values, Reflection, Goal Filter) спроси: «На шкале 1–10, насколько комфортно продолжать?»
- ≥ 6 — продолжаем.
- 4–5 — пауза, лёгкая тема (Wins / Gratitude / Easy Win).
- < 4 — переход в **Phase 0.5 Emotion Regulation Protocol** (см. ниже).

---

## Phase 0.5: Emotion Regulation Protocol (3–7 минут, по необходимости)

Если эмоция сильна и мешает диагностике — используй один из трёх протоколов:

1. **Cognitive Reappraisal** — переосмысление (Gross, 1998, d = 0.45)
   - Когда: пользователь застрял на негативной интерпретации («я не справился — я безнадёжен»).
   - 4 шага: Name emotion → Identify thought → Generate alternatives → Choose perspective.

2. **Grounding (5-4-3-2-1)** — возврат в настоящее (Najavits, 2002, d = 0.38)
   - Когда: тревога, руминация, паника, физические симптомы.
   - 5 вещей, которые видите → 4 звука → 3 ощущения → 2 запаха → 1 действие.

3. **Self-Compassion Break** — сострадание к себе (Neff, 2003, r = 0.47)
   - Когда: жёсткая самокритика («я тупой / ленивый / бесполезный»).
   - 3 шага: Mindfulness → Common humanity → Self-kindness.

**После ER Protocol:** проверь Readiness Gate (1–10). ≥ 6 — возвращаемся. < 6 — пауза или микро-сессия (см. `references/micro_sessions.md`).

**Загрузи `references/emotion_regulation.md`** перед использованием ER Protocol — там полные скрипты.

---

## Health Track entry (opt-in, schema v2.1+)

Если в диалоге появляются маркеры «вес», «энергия», «выгорание», «нет дисциплины», «диета», «сон», «питание» — предложи opt-in Health Track:

> «Я могу добавить отдельный трек по метаболизму — сон, стресс, белок, клетчатка. Это evidence-based рычаги, не диета. Хочешь?»

При согласии:
1. Установи `diagnosis.health_metabolism.active = true`.
2. Загрузи `references/track_health_metabolism.md` (lazy, ~2.5K tokens).
3. Track A: 3 быстрых вопроса. Track B: 5-7 вопросов.
4. **Safety check:** при маркерах РПП (ограничительное питание, binge-purge циклы, навязчивые мысли о теле) — НЕ продолжай трек, мягко рекомендуй специалиста.

**Не блокирует core flow** — пользователь может пропустить и вернуться позже.

---

## Persona adaptations

После Style Calibration в Phase 0 могла включиться одна из персон. Применяй её к Phase 1:

- **ADHD** (`references/mode_adhd.md`): дроби Wheel of Life на 3 захода по 4 сферы, добавляй визуальные таймеры, разрешай skip без объяснения.
- **Unemployed / transitional** (`references/mode_unemployed.md`): не дави на сферу Career; разрешай отвечать «не знаю» — это ценный сигнал.
- **Elder homebound** (`references/mode_elder.md`): пропусти Career / Romance / Finances; фокус на Meaning, Contribution, Family, Health, Physical Environment. Используй язык «что даёт смысл сегодня?» вместо «цели».
- **Planning Friction** (`references/mode_planning_friction.md`): сократи до 5 ключевых сфер, дай готовые формулировки на выбор.

---

## State writes (если включена персистентность)

В конце Phase 1 запиши в state v2 (`references/state_v2_schema.md`):

**Phase 0 / Style Calibration / Persona Detection** (Tier 1 master отвечает за detection, write делает Phase 1 при entry):
- `persona.active_mode`: `"none"|"adhd"|"unemployed"|"elder"|"planning_friction"` — обновить если detected в Phase 0
- `persona.detected_at`: ISO timestamp
- `persona.user_confirmed`: bool (после подтверждения пользователем)
- `persona.history[]`: append `{from_mode, to_mode, ts}` при смене

**Phase 0.5 ER Protocol** (если был запущен):
- `emotion_regulation_log[]`: append `{event_id, date, protocol: "reappraisal"|"grounding"|"self_compassion", trigger, outcome_readiness (1–10), duration_minutes}` за каждый запуск

**Phase 1 Diagnostic core:**
- `diagnosis.wheel_of_life.current`: { sphere_id: score (1–10) } × 11 (canonical)
- `diagnosis.values_schwartz`: { value: 0.0–1.0 } (если PVQ выполнен)
- `diagnosis.ikigai_pillars`: { love, good_at, world_needs, paid_for } (если Track B)
- `session.completed_phases`: append `"1"` (или `"0.5"` для ER)
- `session.current_track`: `"quick"|"deep"`
- `session.readiness_gates[]`: append `{phase, score, timestamp}`

Запись через `references/templates/Wheel_of_Life_History.md`, `references/templates/Hot_Cache.md`, `references/templates/USER_PROGRESS_JOURNAL.md` (для persona switch и ER breakthrough записей — см. `templates/AI_Instructions.md §Write rules`).

---

## Common exit transitions

- **Phase 1.5 (Goal Filter)** — стандартный переход после диагностики → загрузи `references/module_phase1_5_goal_filter.md`
- **Phase 4 (Dashboard)** — пользователь хочет увидеть картину визуально → загрузи `references/module_phase4_dashboard.md`
- **Pause / Recovery** — если Readiness < 4 повторно → загрузи `references/recovery_protocol.md`

---

## Gotchas

- **НЕ начинай** с вопроса «оцени сферы». Сначала Emotional Landing → согласие → краткое объяснение метода.
- **НЕ интерпретируй** низкие оценки как «плохо». Низкое — это сигнал, что сфера важна и требует внимания.
- **НЕ зачитывай** все 11 сфер списком. Дай 3–4, дождись оценки, продолжи.
- **НЕ требуй** ответа на все 11 — пропуск разрешён.
- **ВСЕГДА** заверши Phase 1 одним конкретным действием на сегодня — это First Session Value Contract.
