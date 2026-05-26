# State v2 Schema — Single Source of Truth

> **Версия схемы:** `2.0`
> **Дата:** 2026-05-26
> **Заменяет:** `references/conversation_state_schema.md` (v1)
> **Используется:** HTML dashboard, 8 wiki templates, dashboard_guide.md, SKILL.master.md gating logic

State v2 — единый источник правды о пользователе. Все три шаблона (wiki, HTML dashboard, dashboard_guide) рендерят срезы этого состояния. Skill пишет в state v2 при условиях gating (см. §5).

---

## 1. Canonical 11 Spheres of Wheel of Life

Единый источник правды для имён сфер. Используется везде: state v2, HTML dashboard, wiki templates, dashboard_guide.

| ID (canonical) | Russian display | Icon | Default color |
|---|---|---|---|
| `health` | Здоровье | 🏥 | `#7a9e7e` |
| `finances` | Финансы | 💰 | `#c4a55a` |
| `career` | Карьера | 💼 | `#6b8cae` |
| `family` | Семья | 👨‍👩‍👧 | `#8a9ec4` |
| `romance` | Отношения с партнёром | 💕 | `#c4858a` |
| `social` | Дружба | 🤝 | `#6a8ac4` |
| `personal_growth` | Личностный рост | 📚 | `#8a6bc4` |
| `meaning` | Смысл и духовность | 🧘 | `#9e7ac4` |
| `fun_recreation` | Отдых и хобби | 🎉 | `#6bc4a2` |
| `contribution` | Вклад | 🌍 | `#c4a26a` |
| `physical_environment` | Дом и среда | 🏠 | `#7a9e9e` |

**Запрещено** использовать legacy наименования: `growth`, `spirituality`, `fun`, `environment`, `relationships` (объединённое), `recreation` (без `fun_`). Любое отклонение ловится тестом `test_sphere_count_canonical`.

---

## 2. Полная JSON-схема v2.0

```jsonc
{
  "schema_version": "2.0",
  "user_id": "uuid-v4",
  "created_at": "2026-05-26T10:00:00Z",
  "updated_at": "2026-05-26T10:00:00Z",

  // ============================================================
  // SESSION — текущая фаза, прогресс по вопросам, readiness gates
  // ============================================================
  "session": {
    "current_phase": "0",              // "0"|"0.5"|"1"|"1.5"|"2"|"3"|"4"|"5"
    "current_track": null,             // "quick"|"deep"|null
    "current_question_index": 0,
    "completed_phases": [],
    "readiness_gates": [
      {
        "phase": "1",
        "score": 8,                    // 1-10
        "timestamp": "2026-05-26T10:15:00Z"
      }
    ],
    "session_count": 1,
    "last_session_at": null,
    "gap_days_since_last_session": 0
  },

  // ============================================================
  // PERSONA — обнаруженный режим работы пользователя
  // ============================================================
  "persona": {
    "active_mode": "none",             // "none"|"adhd"|"unemployed"|"elder"|"planning_friction"
    "detected_at": null,
    "user_confirmed": false,
    "history": []                      // переходы между modes
  },

  // ============================================================
  // COMMUNICATION STYLE — Big Five × TTM × MI калибровка
  // ============================================================
  "communication_style": {
    "baseline": {
      "softness": "neutral",           // "soft"|"neutral"|"direct"
      "structure": "medium"            // "high"|"medium"|"low"
    },
    "current_intensity": "exploratory" // "nurturing"|"exploratory"|"collaborative"|"challenging"
  },

  // ============================================================
  // DIAGNOSIS — Phase 1 / 1.5 результаты
  // ============================================================
  "diagnosis": {
    "wheel_of_life": {
      "current": {
        "health": null,                // 1-10 или null если не оценено
        "finances": null,
        "career": null,
        "family": null,
        "romance": null,
        "social": null,
        "personal_growth": null,
        "meaning": null,
        "fun_recreation": null,
        "contribution": null,
        "physical_environment": null
      },
      "targets": {
        "health": null,                // 1-10 целевые
        // ... аналогично current
      },
      "history": [
        {
          "date": "2026-W21",          // ISO week
          "scores": { /* 11 spheres */ },
          "average": 6.1,
          "comment": "Фокус месяца: ..."
        }
      ]
    },

    "values_schwartz": {
      "self_direction": null,          // 0.0-1.0 (PVQ-21)
      "stimulation": null,
      "hedonism": null,
      "achievement": null,
      "power": null,
      "security": null,
      "conformity": null,
      "tradition": null,
      "benevolence": null,
      "universalism": null
    },

    "core_values": [
      // Список 5-7 core values (Core Values Discovery PRD)
      {
        "value_id": "CV1",
        "name": "Autonomy",
        "description": "Свобода выбирать собственный путь, не подстраиваясь под чужие ожидания",
        "derived_from": [
          { "type": "domain", "ref": "career" },
          { "type": "experience", "ref": "Запуск своего проекта в 2024" },
          { "type": "energizing_activity", "ref": "Работа над неструктурированными задачами" }
        ],
        "compass_question": "Расширяет ли этот выбор мою автономию или сужает?",
        "priority_rank": 1,
        "discovered_at": "2026-05-26T10:30:00Z",
        "last_reviewed": "2026-05-26T10:30:00Z"
      }
    ],

    "ikigai_pillars": {
      "love": null,                    // что я люблю
      "good_at": null,                 // в чём я хорош
      "world_needs": null,             // что нужно миру
      "paid_for": null                 // за что мне платят
    }
  },

  // ============================================================
  // GOALS — BHAG → Themes → 12-Week OKR → Weekly → Daily WOOP
  // ============================================================
  "goals": {
    "bhag": {
      "statement": null,
      "horizon_years": 10,             // 10-25
      "created_at": null
    },
    "life_themes": [
      {
        "theme_id": "T1",
        "objective": null,
        "key_results": [],
        "horizon": "1y"                // "1y"|"3y"
      }
    ],
    "twelve_week_okr": {
      "quarter_start": null,
      "quarter_end": null,
      "objectives": [
        {
          "objective_id": "O1",
          "title": null,
          "sphere_id": null,           // ссылка на canonical sphere
          "key_results": [
            {
              "kr_id": "O1-KR1",
              "title": null,
              "current_value": 0,
              "target_value": null,
              "unit": null,
              "progress_pct": 0,
              "status": "todo"         // "todo"|"on_track"|"at_risk"|"off_track"|"done"
            }
          ],
          "confidence_score": null     // 1-10
        }
      ]
    },
    "weekly_priorities": [
      // Максимум 3-5
      {
        "priority_id": "WP1",
        "title": null,
        "sphere_id": null,
        "completed": false,
        "week_number": null
      }
    ],
    "daily_woop": [
      {
        "woop_id": "W1",
        "date": "2026-05-26",
        "wish": null,
        "outcome": null,
        "obstacle": null,
        "plan": null,                  // if-then
        "sphere_id": null,
        "active": true
      }
    ]
  },

  // ============================================================
  // GOAL FILTER — Phase 1.5 Authentic Goal Filter results
  // ============================================================
  "goal_filter": {
    "active_goals": [
      {
        "goal_id": "G1",
        "title": null,
        "radar": {
          "values": null,              // 1-10
          "energy": null,
          "impact": null,
          "feasibility": null,
          "authenticity": null
        },
        "core_values_alignment": [],   // ["CV1", "CV3"]
        "deep_why_chain": [],          // 3 уровня
        "red_flags_screened": [],      // RF1-RF7
        "societal_pressure_score": null, // 1-10, ниже = меньше внешнего давления
        "added_at": null

        // Будущий schema bump 2.2:
        // "partner_coordination": {
        //   "communication": 1-10,
        //   "cooperation": 1-10,
        //   "compatibility": 1-10,
        //   "obstacles": []
        // }
      }
    ],
    "paused_goals": [
      {
        "goal_id": null,
        "title": null,
        "red_flags": [],               // ["RF3"]
        "insight": null,
        "paused_at": null
      }
    ],
    "patterns": [
      {
        "pattern_id": "P1",
        "red_flag": "RF3",
        "count": 0,
        "insight": null
      }
    ]
  },

  // ============================================================
  // HABITS — Cue / Routine / Reward + streak tracking
  // ============================================================
  "habits": [
    {
      "habit_id": "H1",
      "name": null,
      "cue": null,                     // триггер
      "routine": null,                 // само действие
      "reward": null,                  // награда
      "anchor": null,                  // habit stacking — после какой существующей привычки
      "sphere_id": null,
      "tiny_version": null,            // Tiny Habits — минимальная версия
      "current_streak": 0,
      "best_streak": 0,
      "status": "on_track",            // "on_track"|"at_risk"|"off_track"
      "started_at": null,
      "last_completed": null
    }
  ],

  // ============================================================
  // WEEKLY REVIEWS — Phase 3 история
  // ============================================================
  "weekly_reviews": [
    {
      "review_id": "WR1",
      "date": null,
      "format": "gtd_scrum",
      "gtd": {
        "get_clear": [],
        "get_current": [],
        "get_creative": []
      },
      "scrum_retro": {
        "worked": [],
        "didnt_work": [],
        "changes": []
      },
      "lead_measures": {},             // {sphere_id: value}
      "lag_measures": {},
      "execution_score": null,         // 0-10
      "adjustments": []
    }
  ],

  // ============================================================
  // EMOTION REGULATION LOG — Phase 0.5
  // ============================================================
  "emotion_regulation_log": [
    {
      "event_id": "ER1",
      "date": null,
      "protocol": "reappraisal",       // "reappraisal"|"grounding"|"self_compassion"
      "trigger": null,                 // что вызвало
      "outcome_readiness": null,       // 1-10 после протокола
      "duration_minutes": null
    }
  ],

  // ============================================================
  // WINS LOG — first-class празднование побед
  // ============================================================
  "wins_log": [
    {
      "win_id": "W1",
      "date": null,
      "description": null,
      "goal_id": null,                 // связанная цель
      "sphere_id": null,
      "category": "milestone",         // "milestone"|"first"|"streak"|"breakthrough"
      "celebrated_via": null           // "win_alert"|"weekly_review"
    }
  ],

  // ============================================================
  // REWARD AUDIT RESULTS — cheap dopamine awareness
  // ============================================================
  "reward_audit_results": [
    {
      "audit_id": "RA1",
      "date": null,
      "cheap_dopamine_sources": [],    // [{source, frequency_per_day, awareness_level}]
      "high_friction_sources": [],     // что блокирует движение к целям
      "grayscale_commitment": null,    // null | "tried" | "adopted"
      "next_check_date": null
    }
  ],

  // ============================================================
  // CALENDAR EVENTS LOG — что создано через Phase 5 MCP
  // ============================================================
  "calendar_events_log": [
    {
      "event_id": null,                // Google Calendar ID
      "created_at": null,
      "event_type": "weekly_review",   // "weekly_review"|"woop_morning"|"habit"|"milestone"|"shutdown"|"time_block"
      "title": null,
      "scheduled_for": null,
      "recurrence": null,              // RRULE или null
      "color_id": null,
      "status": "created"              // "created"|"updated"|"deleted"
    }
  ],

  // ============================================================
  // RECOVERY SESSIONS LOG — восстановление после пропусков
  // ============================================================
  "recovery_sessions_log": [
    {
      "recovery_id": "REC1",
      "date": null,
      "gap_days": null,
      "strategy_used": null,           // см. recovery_protocol.md
      "outcome": null
    }
  ],

  // ============================================================
  // PERSISTENCE RETRY — Drive/Calendar availability tracking
  // ============================================================
  "persistence_retry": {
    "drive": {
      "available_last_session": null,
      "failed_consecutive_sessions": 0,
      "unsaved_sessions_count": 0,
      "unsaved_sessions_dates": [],
      "backoff_until_session": 0,
      "user_declined_count": 0,
      "first_connection_at": null,     // когда впервые подключился (для bootstrap)
      "wiki_bootstrapped": false
    },
    "calendar": {
      "available_last_session": null,
      "failed_consecutive_sessions": 0,
      "pending_events_count": 0,
      "pending_events": [],
      "backoff_until_session": 0,
      "user_declined_count": 0
    },
    "backfill_offered": false,         // был ли в этой сессии prompt про backfill
    "backfill_accepted": false
  }
}
```

---

## 3. Поле-за-полем документация

### 3.1 Top-level

| Поле | Тип | Обязательно | Описание |
|---|---|---|---|
| `schema_version` | string | да | Семвер схемы. Минор-бамп = additive, мажор-бамп = breaking |
| `user_id` | string (uuid v4) | да | Генерируется при первой сессии |
| `created_at` / `updated_at` | ISO 8601 | да | Создание / последнее изменение state |

### 3.2 session

| Поле | Тип | Описание |
|---|---|---|
| `current_phase` | enum | Текущая фаза 0/0.5/1/1.5/2/3/4/5 (SKILL.md terminology) |
| `current_track` | enum / null | `"quick"` (20-30 мин) или `"deep"` (65-105 мин, 2-4 сессии) |
| `current_question_index` | int | Номер текущего вопроса в фазе |
| `completed_phases` | array | Завершённые phase IDs |
| `readiness_gates` | array | Каждая запись = `{phase, score: 1-10, timestamp}` |
| `gap_days_since_last_session` | int | Триггерит recovery_protocol при > 7 |

### 3.3 persona

| Поле | Тип | Описание |
|---|---|---|
| `active_mode` | enum | `"none"`, `"adhd"`, `"unemployed"`, `"elder"`, `"planning_friction"` |
| `detected_at` | ISO 8601 | Когда обнаружен (Phase 0 detection) |
| `user_confirmed` | bool | Согласился ли пользователь на режим |
| `history` | array | Переходы между modes (для context shift) |

### 3.4 diagnosis.core_values

Новый блок из Core Values Discovery PRD:

| Поле | Тип | Описание |
|---|---|---|
| `value_id` | string | `CV1`, `CV2`, ... |
| `name` | string | Краткое название (1-3 слова) |
| `description` | string | Подробное определение |
| `derived_from` | array | Список `{type, ref}` — domain / experience / energizing_activity |
| `compass_question` | string | Вопрос для daily decision making |
| `priority_rank` | int | 1-7 (топ-7 core values максимум) |

### 3.5 goals.* sphere references

Все цели должны ссылаться на canonical sphere ID (см. §1). Запрещено использовать legacy имена.

### 3.6 habits

В отличие от v1 (только streak counts) — теперь полный Habit Loop с cue/routine/reward + Tiny Habits + anchor для habit stacking.

### 3.7 wins_log

В v1 wins лежали внутри `weekly_reviews[].wins`. В v2 — first-class сущность для win_alert.md протокола и dashboard widget.

---

## 4. Schema versioning policy

### 4.1 Additive bumps (минор)

- `2.0 → 2.1`: добавление Health & Metabolism Track (`health_metabolism` блок). Старые клиенты v2.0 игнорируют unknown field.
- `2.1 → 2.2`: добавление Goal Concordance (`goals.goal_filter.active_goals[].partner_coordination`). Старые клиенты игнорируют unknown property.

### 4.2 Breaking bumps (мажор)

- `2.x → 3.0`: только при изменении ID naming, реструктуризации top-level keys, или замене enum значений. Требует migration script.

### 4.3 Правило тестирования

`test_schema_versioning` проверяет, что:
- любой 2.x документ парсится 2.0 клиентом (с ignored unknown fields)
- любой 2.x клиент рендерит 2.0 документ без падений

---

## 5. Gating logic (когда state пишется полно vs lean)

```
on session_start:
  detect drive_connected, calendar_connected

  mode = match (drive_connected, calendar_connected):
    (true, true)   → "full_persistence"
    (true, false)  → "wiki_no_execution"
    (false, true)  → "execution_no_wiki"
    (false, false) → "lean_conversation"
```

### 5.1 full_persistence mode

- Все поля state v2 пишутся в Drive Wiki
- Если `persistence_retry.drive.wiki_bootstrapped == false` → `bootstrap_drive_wiki()` (см. plan_v1.0_templates_rebuild.md §10)
- Calendar events создаются и логируются в `calendar_events_log`
- HTML dashboard читает state v2 из `03_Dashboard/dashboard_data.json`

### 5.2 wiki_no_execution

- Все поля пишутся в Drive Wiki
- Calendar события не создаются, попадают в `persistence_retry.calendar.pending_events`
- Skill предлагает подключить Calendar для execution layer

### 5.3 execution_no_wiki

- State держится в conversation memory
- Calendar события создаются
- Skill предлагает подключить Drive для persistence
- Dashboard one-shot из in-memory state

### 5.4 lean_conversation

- Минимальный state: только `session`, `persona`, текущие 2-3 цели, последний readiness gate
- В памяти conversation, не персистится
- Dashboard one-shot

---

## 6. Backfill при mid-session connection (edge case (a))

```
on drive_connected_event (mid-session):
  if persistence_retry.backfill_offered == true:
    return  # уже спрашивали

  if previous_mode in ["lean_conversation", "execution_no_wiki"]:
    prompt_user:
      "У тебя накопилось данных за сессию (Phase {phase}, Wheel of Life: {filled_spheres}/11, целей: {goal_count}) — синхронизировать в Drive?"

    persistence_retry.backfill_offered = true

    if user_accepts:
      persistence_retry.backfill_accepted = true
      bootstrap_drive_wiki()
      one_shot_dump_state_v2_to_wiki()
      confirm: "Wiki создан, прогресс сохранён ✓"
      switch_to_mode("full_persistence")

    else:
      persistence_retry.drive.user_declined_count += 1
      if user_declined_count >= 2:
        persistence_retry.drive.backoff_until_session = current_session_count + 3
```

---

## 7. Bootstrap Drive Wiki (первый коннект)

При первом коннекте Drive (`wiki_bootstrapped == false`):

```
Life Planning Coach Wiki/
├── 00_Raw/
├── 01_Wiki/
│   ├── Hot_Cache.md
│   ├── Index.md
│   ├── User_Progress/
│   │   ├── Goals.md
│   │   ├── Wheel_of_Life_History.md
│   │   ├── Core_Values_Compass.md
│   │   └── USER_PROGRESS_JOURNAL.md
│   └── Decisions/
├── 02_Instructions/CLAUDE.md
├── 03_Dashboard/
│   ├── Progress_Dashboard.md
│   └── dashboard_data.json
├── 05_Archive/
├── README.md
└── CHANGELOG.md
```

Все шаблоны берутся из `references/templates/` (см. wiki templates rebuild B2).

После bootstrap:
- `persistence_retry.drive.wiki_bootstrapped = true`
- `persistence_retry.drive.first_connection_at = now()`

---

## 8. Миграция с v1 (conversation_state_schema.md)

| v1 поле | v2 эквивалент | Действие |
|---|---|---|
| `stage` | `session.current_phase` | Маппинг: `"1" → "1"`, `"1.5" → "1.5"`, `"2" → "2"`, `"3" → "3"`. Добавляются `"0"`, `"0.5"`, `"4"`, `"5"` |
| `phase` (string enum) | `session.current_phase` | Использует одни значения с v1 |
| `life_wheel` | `diagnosis.wheel_of_life.current` | Naming уже совпадает (11 spheres canonical) |
| `values` | `diagnosis.values_schwartz` | Переименовать ключ |
| `goals.bhag` (string) | `goals.bhag.statement` | Обернуть в объект с `horizon_years` |
| `goals.themes` | `goals.life_themes` | Переименовать |
| `goals.twelve_week` | `goals.twelve_week_okr` | Переименовать + расширить (`quarter_start/end`, `confidence_score`) |
| `goals.daily_woop` | `goals.daily_woop` | Без изменений, добавилось `woop_id`, `sphere_id`, `date`, `active` |
| `goal_filter.active_goals[].radar` | `goal_filter.active_goals[].radar` | Без изменений |
| `weekly_reviews[].worked/didnt_work/changes` | `weekly_reviews[].scrum_retro.*` | Завернуть в `scrum_retro` |
| `persistence_retry` | `persistence_retry` | Расширен `first_connection_at`, `wiki_bootstrapped`, `backfill_*` полями |

**Новые блоки (не было в v1):**
- `persona`
- `diagnosis.core_values`
- `diagnosis.ikigai_pillars`
- `habits[]` с cue/routine/reward
- `emotion_regulation_log`
- `wins_log` (был в `weekly_reviews[].wins`)
- `reward_audit_results`
- `calendar_events_log`
- `recovery_sessions_log`

---

## 9. Field availability matrix (что захватывается из какой фазы)

| Поле | Источник захвата | Реализовано? |
|---|---|---|
| `session.*` | Каждая фаза при входе/выходе | ✅ существующая логика |
| `persona.active_mode` | Phase 0 persona detection | ⚠️ обнаруживается, но не персистится — нужно добавить write |
| `diagnosis.wheel_of_life` | Phase 1 Wheel of Life | ✅ существующая логика |
| `diagnosis.values_schwartz` | Phase 1 Values PVQ | ✅ существующая логика |
| `diagnosis.core_values` | Phase 1.5 Core Values Discovery (PRD) | 🆕 требует PRD реализации |
| `diagnosis.ikigai_pillars` | Phase 1 deep diagnostic (Track B) | ✅ существующая логика |
| `goals.*` | Phase 2 Goal Architecture | ✅ существующая логика |
| `goal_filter.*` | Phase 1.5 Authentic Goal Filter | ✅ существующая логика |
| `goal_filter.active_goals[].core_values_alignment` | Phase 1.5 + Core Values PRD | 🆕 link при добавлении цели |
| `habits[]` (full cue/routine/reward) | Phase 3 Habit Review | ⚠️ partial — нужно расширить write правила |
| `weekly_reviews[]` | Phase 3 Weekly Review | ✅ существующая логика |
| `emotion_regulation_log` | Phase 0.5 ER Protocol | ⚠️ используется, но не пишется — нужно добавить write |
| `wins_log` | win_alert.md + weekly_review | ⚠️ нужно вынести в first-class write |
| `reward_audit_results` | reward_audit.md | ⚠️ используется, нужно добавить write |
| `calendar_events_log` | Phase 5 MCP create events | ⚠️ создаётся через MCP, нужно логировать в state |
| `recovery_sessions_log` | recovery_protocol.md | ⚠️ нужно добавить write |

**Гэп write-логики** (отмечено ⚠️) — добавляется в SKILL.master.md в B5 (gating + write rules).

---

## 10. Тесты

| Тест | Проверяет |
|---|---|
| `test_state_v2_schema_completeness` | Все top-level keys присутствуют, типы соответствуют |
| `test_sphere_count_canonical` | `diagnosis.wheel_of_life.current` имеет ровно 11 ключей, имена из §1 |
| `test_schema_versioning` | 2.x клиент парсит 2.0 документ; 2.x документ парсится 2.0 клиентом |
| `test_gating_modes` | Все 4 mode комбинации (drive/calendar) работают |
| `test_backfill_prompt` | При mid-session connection срабатывает prompt один раз |
| `test_v1_to_v2_migration` | Все v1 поля корректно мапятся в v2 эквиваленты |

---

## 11. Связанные документы

- [plan_v1.0_templates_rebuild.md](research/plan_v1.0_templates_rebuild.md) — план rebuild всех шаблонов
- [prd_core_values_discovery.md](research/prd_core_values_discovery.md) — источник `core_values` блока
- [prd_health_metabolism.md](research/prd_health_metabolism.md) — schema bump 2.1
- [prd_goal_concordance.md](research/prd_goal_concordance.md) — schema bump 2.2
- `conversation_state_schema.md` (deprecated) — v1, оставлен для backward reference

---

**Статус:** ✅ Canonical. Любые изменения требуют schema_version bump + миграционных заметок.
