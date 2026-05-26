# Module: Phase 3 — Weekly Review

> **Tier:** 2 (lazy-load module)
> **Загружается:** при запросе «обзор недели», «retro», «итоги», либо по расписанию (воскресенье вечер по умолчанию).
> **Предусловие:** есть цели из Phase 2 ИЛИ просто прошла неделя с момента предыдущей сессии.
> **Связанные refs:** `weekly_review.md`, `win_alert.md`, `habit_loop.md`, `reward_audit.md`, `recovery_protocol.md`

---

## Entry triggers

- «Сделаем обзор недели»
- «Подведём итоги»
- «Retro», «retrospective», «scrum retro»
- «Что у меня по целям?»
- Triggered by skill: прошло ≥ 7 дней с последней сессии и есть активные KR

---

## Pre-flight check

Прежде чем начать структурный review — короткий Emotional Landing (30–60 сек):
- «Как ты сейчас? Какая неделя была — лёгкая, тяжёлая, ровная?»
- Дай услышать, отвалидируй («да, бывает / звучит как насыщенная неделя»).
- Только после этого переходи к структуре.

Если пользователь говорит «ничего не сделал», «всё провалил» — это **высокий приоритет**. Загрузи `references/recovery_protocol.md`. Не начинай Weekly Review «по бумажке».

---

## 7-step Weekly Review

### 1. GTD Phase (Get Clear / Get Current / Get Creative) — 10–15 минут
- **Get Clear**: что висит в голове? — выгрузи в inbox.
- **Get Current**: статус по KR недели, по календарю, по обязательствам.
- **Get Creative**: что нового пришло — идеи, инсайты, желания?

### 2. Scrum Retro — 5–10 минут
- Что работало?
- Что не работало?
- Что меняем на следующую неделю?

### 3. Progress Audit — 5–10 минут
По каждому 12-Week KR:
- **Lag measure** — финальный результат (% выполнения)
- **Lead measure** — что я делал, что ведёт к результату (частота, объём)
- Где разрыв между lead и lag? — там лежит инсайт.

### 4. Adjustment — 5 минут
- Цели всё ещё актуальны? (Phase 1.5 проверка — не уехала ли цель в интроект)
- Сроки реалистичны?
- Что переносим, что отбрасываем, что добавляем?

### 5. Celebration — 3–5 минут (ОБЯЗАТЕЛЬНО, не пропускай)
Отпразднуй победы недели через `references/win_alert.md` (5-шаговый протокол).
Минимум одна победа — даже если неделя «провалена», была хотя бы одна. Найди её.

### 6. Habit Review — 5 минут
- Какие привычки работают? (✅ зелёный)
- Какие требуют корректировки cue/reward? (⚠ жёлтый)
- Какие сломались и нужно вернуть на старт «≤ 2 мин»? (🔁)

Загрузи `references/habit_loop.md` если нужно ремонтировать привычку.

### 6.5. Health Track Review (опционально, если активен)

Если `diagnosis.health_metabolism.active == true` — 1-2 минуты:
- «Как был сон на этой неделе? (час/качество)»
- «Уровень стресса 1-10?»
- «Что было самым тяжёлым в питании?»

Обнови `diagnosis.health_metabolism.{sleep_quality, sleep_hours, stress_level, last_assessed}`. Если был активный micro_experiment — оцени outcome, добавь в `micro_experiments_log[]`.

**Не дави.** Если пользователь устал — пропустите этот шаг, вернитесь через неделю. См. `references/track_health_metabolism.md`.

---

### 7. Reward Audit (опционально, при прокрастинации)
Если в Scrum Retro появились паттерны «зависал в соцсетях», «не мог начать», «делал что угодно вместо X» — загрузи `references/reward_audit.md`. Проверь, не «крадёт» ли cheap dopamine мотивацию у KR.

---

## Output: Next Week Plan

Заверши Weekly Review одной таблицей (Markdown через `references/markdown_tables.md`):

| Priority | Связан с KR | Первое действие в понедельник |
|----------|------------|-------------------------------|
| 1. …    | OKR Q1 #2  | … (≤ 30 мин) |
| 2. …    | Health KR  | … |
| 3. …    | Habit X    | Cue: после кофе |

Максимум 3–5 priorities. Если получается 7+ — режь.

---

## Persona adaptations

- **ADHD** (`references/mode_adhd.md`): **Micro-Review** — 3 вопроса вместо 7 шагов, 15 минут, визуальный формат (таблица или эмодзи-чек). Никаких free-form reflection.
- **Unemployed / transitional** (`references/mode_unemployed.md`): без review «карьерного домена». Фокус — purpose + social anchors + small wins. Главный вопрос: «Что дало смысл на этой неделе?»
- **Elder homebound** (`references/mode_elder.md`): **Micro-Check-In** — 3 вопроса, 5 минут. Никакого Wheel of Life с Career/Finance/Romance. Якори дня и память важнее KR.
- **Planning Friction** (`references/mode_planning_friction.md`): templated Sunday Review — фиксированный набор 4 вопросов, без open-ended reflection.

---

## State writes

В конце Phase 3 запиши в state v2 (`references/state_v2_schema.md`):

**Weekly review record:**
- `weekly_reviews[]`: append `{review_id, date, format: "gtd_scrum", gtd: {get_clear[], get_current[], get_creative[]}, scrum_retro: {worked[], didnt_work[], changes[]}, lead_measures: {sphere_id: value}, lag_measures: {sphere_id: value}, execution_score (0–10), adjustments[]}`

**Wins (first-class, шаг 5 Celebration — обязательно min 1 запись):**
- `wins_log[]`: append `{win_id, date, description, goal_id (если связан), sphere_id, category: "milestone"|"first"|"streak"|"breakthrough", celebrated_via: "win_alert"|"weekly_review"}` — за каждую отмеченную победу

**Habits status update:**
- `habits[habit_id].status`: `"on_track"|"at_risk"|"off_track"` (после Habit Review шаг 6)
- `habits[habit_id].current_streak` / `best_streak`: обновить
- `habits[habit_id].last_completed`: ISO timestamp

**Reward Audit (шаг 7, опционально при прокрастинации):**
- `reward_audit_results[]`: append `{audit_id, date, cheap_dopamine_sources: [{source, frequency_per_day, awareness_level}], high_friction_sources[], grayscale_commitment: null|"tried"|"adopted", next_check_date}` — только если шаг 7 выполнен

**Next Week Plan:**
- `goals.weekly_priorities[]`: replace (новая неделя) `[{priority_id, title, sphere_id, completed: false, week_number}]` (max 3–5)

**Session:**
- `session.completed_phases`: append `"3"`
- `session.last_session_at`: ISO timestamp

Запись через `references/templates/USER_PROGRESS_JOURNAL.md` (review record + reward_audit category) и `references/templates/Goals.md` (секция «Победы» — топ-5 в Hot_Cache.md).

---

## Common exit transitions

- **Phase 5 (Execution)** — занеси Next Week Plan в календарь → `references/module_phase5_execution.md`
- **Phase 4 (Dashboard)** — пользователь хочет визуальный обзор прогресса → `references/module_phase4_dashboard.md`
- **Phase 1.5 (Re-filter)** — если в Adjustment всплыло, что цель «уже не моя» → `references/module_phase1_5_goal_filter.md`
- **Recovery** — если пропуск > 7 дней или несколько провальных недель подряд → `references/recovery_protocol.md`

---

## Gotchas

- **НЕ начинай** Weekly Review с цифр (KR %). Сначала Emotional Landing — иначе пользователь уйдёт в защиту.
- **НЕ пропускай** Celebration шаг. Это не «приятная мелочь» — это нейробиологический закрепитель.
- **НЕ позволяй** превратить retro в самобичевание. Любое «я ничтожество» → ER protocol (см. `module_phase1_diagnostic.md` Phase 0.5).
- **НЕ создавай** Next Week Plan больше 5 priorities. Это не оптимизация, это контракт с реальностью.
- **НЕ требуй** еженедельно — раз в 10–14 дней нормально. Главное — ритм, не дисциплина.
- **ВСЕГДА** обновляй state.wins_log — это якоря для recovery и self-compassion в будущем.
