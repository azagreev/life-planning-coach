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

## WoL Frequency Gate (PRD v0.15 §5, schema v2.2.5+)

Check `diagnosis.wheel_of_life.last_assessed_at` перед предложением WoL:
- **< 30 дней** → НЕ предлагай auto; на explicit request → soft challenge: «Прошло [N] дней — сферы редко меняются за такое время, что конкретно беспокоит?»
- **≥ 30 дней** → predict offer: «Прошло [N] дней с оценки — посмотрим Колесо заново?»
- **null** → стандартный Track A/B.

После completed WoL — **обязательно** запиши `last_assessed_at = ISO now()` (см. State writes). В `lean_conversation` mode поле null между сессиями → effectively no-op, OK.

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

## Phase 0.5: Emotion Regulation Protocol (3–7 минут)

3 протокола (см. `references/emotion_regulation.md` для полных скриптов + цитат):
- **Cognitive Reappraisal** (Gross 1998, d=0.45) — негативная интерпретация
- **Grounding 5-4-3-2-1** (Najavits 2002, d=0.38) — тревога / руминация / паника
- **Self-Compassion Break** (Neff 2003, r=0.47) — жёсткая самокритика

После ER → Readiness Gate. ≥ 6 — продолжаем; < 6 — пауза / `micro_sessions.md`. Повтор «не делается» после ER → `emotion_regulation.md` § 5 COM-B Upsell.

---

## Health Track entry (opt-in, schema v2.1+)

Маркеры «вес / энергия / выгорание / диета / сон / питание» → opt-in offer: «Добавлю трек метаболизма — сон, стресс, белок, клетчатка. Evidence-based рычаги, не диета. Хочешь?»

При согласии: `diagnosis.health_metabolism.active = true`; загрузи `references/track_health_metabolism.md` (~2.5K tokens, lazy); Track A = 3 вопроса, B = 5-7. **Safety:** маркеры РПП (ограничительное питание, binge-purge, навязчивые мысли о теле) → НЕ продолжай, мягко к специалисту. Не блокирует core flow.

---

## COM-B Diagnostic (opt-in, 3–5 минут)

При повторяющейся жалобе «знаю, что в сфере X плохо — но не делаю» / «пытаюсь и не получается» — предложи: «Могу за 5 минут помочь понять, *почему* не делается?». При согласии → `references/com_b_diagnostic.md`. Не запускай автоматически — это opt-in escalation, не часть стандартной диагностики.

---

## Persona adaptations

После Style Calibration в Phase 0 могла включиться персона. Применяй к Phase 1:

- **ADHD** (`mode_adhd.md`): 3 захода × 4 сферы (не 11 списком), визуальные таймеры, skip без объяснения
- **Unemployed** (`mode_unemployed.md`): не дави на Career; «не знаю» = валидный сигнал
- **Elder homebound** (`mode_elder.md`): skip Career/Romance/Finances; фокус Meaning/Contribution/Family/Health/Environment; язык «что даёт смысл сегодня?» вместо «цели»
- **Planning Friction** (`mode_planning_friction.md`): 5 ключевых сфер, готовые формулировки на выбор

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
- `diagnosis.wheel_of_life.last_assessed_at`: ISO 8601 timestamp — **обязательно** после completed WoL assessment (любой Track, frequency gate, schema v2.2.5+)
- `diagnosis.wheel_of_life.current`: { sphere_id: score (1–10) } × 11 (canonical)
- `diagnosis.values_schwartz`: { value: 0.0–1.0 } (если PVQ выполнен)
- `diagnosis.ikigai_pillars`: { love, good_at, world_needs, paid_for } (если Track B)
- `diagnosis.com_b_assessment`: `{capability: "ok"|"gap", opportunity: "ok"|"gap", motivation: "ok"|"gap", primary_gap: "capability"|"opportunity"|"motivation"|null, assessed_at: ISO}` (только если COM-B диагностика выполнена, schema v2.2.2+)
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
