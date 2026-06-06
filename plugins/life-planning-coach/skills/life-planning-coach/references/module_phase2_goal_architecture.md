# Module: Phase 2 — Goal Architecture

> **Tier:** 2 (lazy-load module)
> **Загружается:** после Phase 1.5 — только для целей со статусом 🟢 Active.
> **Предусловие:** Goal Portfolio из Phase 1.5 содержит хотя бы одну 🟢 Active цель.
> **Связанные refs:** `goal_architecture.md`, `habit_loop.md`, `action_breakdown_template.md`, `markdown_tables.md`

---

## Entry triggers

- «Поставь мне цели»
- «Хочу сделать план»
- «Как мне дойти до этого?»
- «Разбей мою цель на шаги»
- «BHAG», «OKR», «WOOP»

---

## Goal Layer Stack (5 уровней)

Создаём систему целей сверху вниз, от 25-летнего горизонта до сегодняшнего дня:

### 1. BHAG (Big Hairy Audacious Goal) — 10–25 лет
- Одна цель на десятилетие, North Star.
- Формула: «К [году] я [глагол] [образ результата], потому что [связь с ценностями]».
- Не SMART, скорее эмоционально-визуальная картина.
- Пример: «К 50 годам я выпускаю книги, которые меняют, как родители разговаривают с детьми.»

### 2. Life Themes — 1–3 года
- 3–5 тем в стиле OKR (но с большим горизонтом).
- Формат: «Тема: [имя]. Objective: [качественная цель]. Indicator: [как пойму, что движение есть].»
- Темы покрывают разные сферы Wheel of Life (не только Career).

### 3. 12-Week Quarter — 12 недель
- 1–3 Objectives, каждый с 2–3 Key Results.
- KR должны быть **измеримыми**: «прочитать 4 книги», «провести 12 сессий», «дойти до 80 кг».
- Прогресс ≥ 70% к концу квартала = успех (не 100% — иначе цели слишком лёгкие).
- **Premortem** при `confidence ≤ 6` / horizon ≥ 1y → `references/premortem.md`.

### 4. Weekly Priorities — 3–5 в неделю
- НЕ задачи, а **приоритеты** недели — на чём фокус.
- Привязаны к KR из 12-Week.
- Каждый priority декомпозируется в 1–3 конкретных действия.

### 5. Daily WOOP — ежедневно
- **W**ish: одно желание на сегодня.
- **O**utcome: что почувствую / получу, когда сделаю.
- **O**bstacle: что реально может помешать сегодня (внутреннее).
- **P**lan: «если [obstacle], то [действие]» — if-then implementation intention.

WOOP — единственный научно валидированный формат ежедневного планирования с эффектом (Oettingen et al., d = 0.31).

---

## KR Quality Check (measurability + alignment)

Каждый KR проходит 6 critérios:
- **Specific** — конкретное наблюдаемое поведение
- **Measurable** — number/binary/threshold
- **Achievable stretch** ~70% confidence
- **Relevant** — связан с топ-3 ценностей
- **Time-bound** — deadline/cadence
- **Authentic** — прошёл Phase 1.5 фильтр (не "должен")

> Overlap с SMART, но focus — **execution probability + values alignment**, не клерийность. WOOP (Phase 5) добавляет obstacle/plan.

Если KR не проходит → `references/weak_goal_taxonomy.md`.

---

## Habit Loop (для повторяющихся действий)

Для KR типа «писать каждый день», «бегать 3×/нед», «медитировать утром» — строй привычку, а не цель.

**Cue → Routine → Reward → Anchor**:
- Cue: триггер (время, место, предыдущее действие)
- Routine: само действие (≤ 2 мин на старте — Tiny Habits)
- Reward: что получаешь сразу (не отложенное)
- Anchor: к какому существующему ритуалу привязываем (Habit Stacking)

Пример: «После того как налил кофе утром (anchor + cue) — пишу одно предложение в дневнике (routine, ≤ 2 мин) — отмечаю крестиком в календаре (reward).»

**Загрузи `references/habit_loop.md`** для полных протоколов Tiny Habits / Habit Stacking / Identity-based habits.

---

## Partner Discussion Checkpoint (если цель партнёрская)

Если у цели заполнен `goal_filter.active_goals[].partner_coordination` (schema v2.2+) — добавь явный шаг в декомпозицию:

> **Discussion checkpoint:** «Когда обсудишь это с партнёром — до или после первого милстона?» Запиши в `key_results` как отдельный KR `discuss_with_partner` (target_value: date, status: todo).

Это закрепляет communication из Goal Coordination в исполняемом плане, не оставляя её как «по ходу обсудим».

---

## Action Breakdown (для сложных целей)

Если цель из WOOP сложная (Career / Finances / Health / Home / Learning) и Daily WOOP не получается сформулировать — разбей на шаги.

Загрузи `references/action_breakdown_template.md`:
- Каждый шаг ≤ 30 минут ИЛИ с бинарным критерием выполнения.
- Чекпоинты после 3-го и 6-го шага: «всё ещё актуально?»
- Opt-in: предлагай, не навязывай.

---

## Persona adaptations

- **ADHD** (`references/mode_adhd.md`): C.A.R. method — Capture / Action / Review. Tasks ≤ 2 минут или с body double. Никаких «список из 10 шагов на день». Time buffer × 2 для любых оценок.
- **Unemployed / transitional** (`references/mode_unemployed.md`): фокус на purpose exploration, не на «карьерные цели». Micro-contribution и service — источники смысла на переходе.
- **Elder homebound** (`references/mode_elder.md`): НЕ цели в смысле SMART. Якоря дня и meaning. «Что даёт reason to get up today?» Legacy through memory — а не achievement.
- **Planning Friction** (`references/mode_planning_friction.md`): Smart defaults — 25 мин на митинг, 45 мин на задачу, 15 мин буфер. Готовые шаблоны дня (Deep Work / Meeting / Recovery).

---

## State writes

В конце Phase 2 запиши в state v2 (`references/state_v2_schema.md`):

**Goals layer stack:**
- `goals.bhag`: `{statement, horizon_years (10–25), created_at}` (если создан / обновлён)
- `goals.life_themes[]`: `[{theme_id, objective, key_results[], horizon: "1y"|"3y"}]`
- `goals.twelve_week_okr`: `{quarter_start, quarter_end, objectives[{objective_id, title, sphere_id, key_results[{kr_id, title, target_value, unit, progress_pct, status}], confidence_score (1–10)}]}`
- `goals.weekly_priorities[]`: `[{priority_id, title, sphere_id, completed, week_number}]` (max 3–5)
- `goals.daily_woop[]`: append `{woop_id, date, wish, outcome, obstacle, plan (if-then), sphere_id, active: true}`

**Habits — полный Habit Loop (cue/routine/reward/anchor/tiny_version, обязательно):**
- `habits[]`: append `{habit_id, name, cue (триггер), routine (само действие), reward (немедленная), anchor (existing ritual), sphere_id (canonical), tiny_version (≤2 мин старт), current_streak: 0, best_streak: 0, status: "on_track", started_at, last_completed: null}`
- Все 5 полей Habit Loop (cue+routine+reward+anchor+tiny_version) — **обязательны**. Без anchor/tiny_version привычка остаётся декларацией.

**Session:**
- `session.completed_phases`: append `"2"`

Запись через `references/templates/Goals.md` (секции Goals + Habits) и `references/templates/Hot_Cache.md` (активные приоритеты + Daily WOOP).

---

## Common exit transitions

- **Phase 5 (Execution)** — стандартный переход: цели → календарь → ежедневное исполнение → `references/module_phase5_execution.md`
- **Phase 3 (Weekly Review)** — если идём в первый Weekly Review, чтобы установить ритм → `references/module_phase3_weekly_review.md`
- **Phase 4 (Dashboard)** — пользователь хочет визуально увидеть всю архитектуру → `references/module_phase4_dashboard.md`

---

## Gotchas

- **НЕ строй** Phase 2 без Phase 1.5. Архитектура для интроектов = ускоренный путь к выгоранию.
- **НЕ заполняй** все 5 уровней сразу. Минимум: BHAG + 1 квартальный Objective + Daily WOOP на завтра. Остальное — позже.
- **НЕ навязывай** SMART, если пользователь органически живёт темами. Themes могут оставаться качественными.
- **НЕ обещай** 100% выполнения KR. 70% — целевая планка.
- **НЕ путай** habit и goal. «Пробежать марафон» — goal. «Бегать 3×/нед» — habit, лежащая под goal.
- **ВСЕГДА** связывай каждый KR с конкретной топ-ценностью (`owner_value`) — без этого мотивация распадается.
- **ВСЕГДА** в конце Phase 2 спроси: «Что сделаем сегодня? Один шаг.» — First Session Value Contract.
