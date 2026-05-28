# State v2 Schema — Single Source of Truth

> **Версия схемы:** `2.2.7`
> **Дата:** 2026-05-28
> **Заменяет:** `references/conversation_state_schema.md` (v1 — удалён в v1.1.0; migration таблица в §8 ниже)
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
  "schema_version": "2.2.7",
  "user_id": "uuid-v4",
  "created_at": "2026-05-26T10:00:00Z",
  "updated_at": "2026-05-27T10:00:00Z",

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
    "gap_days_since_last_session": 0,
    "gating_mode": "lean_conversation" // "full_persistence"|"wiki_no_execution"|"execution_no_wiki"|"lean_conversation" (v2.0.1+)
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
      "last_assessed_at": null,        // ISO 8601 / null (NEW v2.2.5) — frequency gate для re-assessment (PRD v0.15 §5: skip < 30d, offer re-assess ≥ 30d)
      "current": {
        "health": null,                // 1-10 или null если не оценено (Health Index если sub-segments заполнены, иначе single-score)
        "health_subsegments": null,    // NEW v2.2.6 — opt-in detailed health assessment, см. §3.4.5 + `wol_health_subsegments.md`
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
    },

    // ====================================
    // COM-B ASSESSMENT — v2.2.2 (opt-in diagnostic)
    // ====================================
    // Заполняется ТОЛЬКО если COM-B диагностика была выполнена
    // (см. references/com_b_diagnostic.md). Если null — не выполнялась.
    "com_b_assessment": null,          // {capability, opportunity, motivation: "ok"|"gap", primary_gap, assessed_at}

    // ====================================
    // HEALTH_METABOLISM — v2.1 (opt-in track)
    // ====================================
    "health_metabolism": {
      "active": false,                 // включён ли трек у пользователя
      "sleep_quality": null,           // 1-10
      "sleep_hours": null,             // float, e.g. 7.5
      "stress_level": null,            // 1-10 (10 = максимальный стресс)
      "protein_target_met": null,      // bool (~0.8-1.2 г/кг)
      "fiber_target_met": null,        // bool (~25-30 г/день)
      "chewing_awareness": null,       // 1-10 (сколько раз пережёвывает осознанно)
      "caffeine_cutoff_hour": null,    // 0-23 (час после которого не пьёт кофеин)
      "last_assessed": null,           // ISO timestamp
      "micro_experiments_log": []      // [{date, lever, hypothesis, outcome, duration_days}]
    },

    // ====================================
    // HEALTH_SNAPSHOT — v2.2.7+ (light 4-question opt-in tool)
    // ====================================
    "health_snapshot": {
      "last": null                     // {date, average_score, weakest_question, answered_count, declined_count} — см. §3.4.6
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
    ],

    // ====================================
    // PREMORTEM ASSESSMENTS — v2.2.3 (opt-in для важных OKR)
    // ====================================
    // Запускается через Premortem trigger в Phase 2 (confidence ≤ 6 / horizon ≥ 1y /
    // partner_coord / explicit request / mid-quarter stagnation). См. references/premortem.md.
    "premortem_assessments": [
      {
        "premortem_id": "PM1",
        "goal_id": "O1",               // ссылка на 12-Week OKR objective
        "conducted_at": "2026-05-27T15:30:00Z",
        "trigger": "low_confidence",   // "low_confidence"|"long_horizon"|"partner_coord"|"explicit_request"|"mid_quarter_stagnation"
        "top_risks": [
          {
            "risk": "забил после двух плохих недель",
            "category": "internal",    // "internal"|"external"|"missed_inputs"|"scope_creep"|"motivation_drift"
            "mitigation_intention": "Если пропущу 2 недели подряд, то открою premortem.md → Step 5 и переоценю scope."
          }
        ],
        "next_review_date": "2026-07-08"  // обычно week 6 для 12-week OKR
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
        "added_at": null,

        // v2.2 — Goal Concordance / Partner Coordination (optional)
        // Заполняется ТОЛЬКО если цель затрагивает партнёра/семью (маркеры
        // в формулировке: «партнёр», «жена», «муж», «семья», «we», «наш»).
        // Если null — цель индивидуальная.
        "partner_coordination": null    // {communication: 1-10, cooperation: 1-10, compatibility: 1-10, obstacles: []}
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
      "adjustments": [],
      // AAR (Lean) — v2.2.4 (опц., skip при execution_score ≥ 70%)
      "gap_analysis": [
        {
          "gap_id": "GA1",
          "what": "не дошёл до OKR weekly KR #2",
          "why_three_levels": ["переоценил время", "не блокировал утренние слоты", "нет pre-commit к chronotype scheduling"],
          "category": "internal"        // "internal"|"external"|"both"
        }
      ],
      "lessons_learned": [
        {
          "lesson": "блокируй 2-3 утренних deep work слота в вс вечером",
          "category": "planning",       // free-text для группировки
          "sighted_count": 1            // surface при ≥ 3
        }
      ]
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
      "first_connection_at": null,         // когда впервые подключился (для bootstrap)
      "wiki_bootstrapped": false,
      "wiki_cleanup_mode": null,           // null | "apps_script" | "batch_weekly" | "reminder" | "ignore" (см. drive_integration.md §Layered cleanup)
      "wiki_cleanup_last_reminder_at": null,  // ISO timestamp последнего reminder (для quarterly cadence)
      "wiki_cleanup_chosen_at": null       // ISO timestamp когда user сделал выбор
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
| `gating_mode` | enum | **(v2.0.1+)** Detected mode по комбинации Drive × Calendar: `"full_persistence"`, `"wiki_no_execution"`, `"execution_no_wiki"`, `"lean_conversation"`. Пишется skill'ом на старте сессии (SKILL.master.md §3). |

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

### 3.4.1 diagnosis.health_metabolism (v2.1+)

Opt-in трек метаболического здоровья. Активируется явно через Phase 1 Health Track entry. Если `active=false` — поля игнорируются HTML dashboard и phase modules.

| Поле | Тип | Описание |
|---|---|---|
| `active` | bool | Флаг включения трека (default false) |
| `sleep_quality` | 1-10 / null | Субъективная оценка качества сна |
| `sleep_hours` | float / null | Часов сна за последнюю ночь |
| `stress_level` | 1-10 / null | Субъективный стресс |
| `protein_target_met` | bool / null | ~0.8-1.2 г/кг достигнуто за последние 7 дней |
| `fiber_target_met` | bool / null | ~25-30 г/день |
| `chewing_awareness` | 1-10 / null | Осознанность жевания |
| `caffeine_cutoff_hour` | int 0-23 / null | Час, после которого не пьёт кофеин |
| `last_assessed` | ISO 8601 / null | Когда последний раз обновлено |
| `micro_experiments_log` | array | `[{date, lever, hypothesis, outcome, duration_days}]` |

PRD: `docs/research/prd_health_metabolism.md`. Tier 3 ref: `references/track_health_metabolism.md`. **Ограничение:** трек не для расстройств пищевого поведения; coach даёт coaching, не therapy.

### 3.4.3 diagnosis.com_b_assessment (v2.2.2+, optional)

Opt-in результат COM-B диагностики (Michie, van Stralen, West 2011). Заполняется ТОЛЬКО если пользователь прошёл COM-B протокол (см. `references/com_b_diagnostic.md`). Если null — диагностика не выполнялась. Используется для routing к targeted интервенциям (Capability → Tiny Habits; Opportunity → environment_design; Motivation → WOOP/Compass) и для tracking повторных gap в Phase 3 Weekly Review.

| Поле | Тип | Описание |
|---|---|---|
| `capability` | `"ok"` / `"gap"` | Capability компонент: знание шагов + физические ресурсы |
| `opportunity` | `"ok"` / `"gap"` | Opportunity: среда (физическая + социальная) поддерживает |
| `motivation` | `"ok"` / `"gap"` | Motivation: рефлексивная (важность) + автоматическая (pull) |
| `primary_gap` | `"capability"` / `"opportunity"` / `"motivation"` / null | Самое блокирующее звено (если все три gap — обычно motivation first) |
| `assessed_at` | ISO 8601 | Когда диагностика выполнена. После 14 дней — re-assess рекомендован. |

Источник методологии: `docs/research/prd_v0.15_methodology_upgrade.md` §8 COM-B Model.

### 3.4.4 diagnosis.wheel_of_life.last_assessed_at (v2.2.5+, optional)

Frequency gate для Wheel of Life re-assessment. PRD v0.15 §5: WoL — опциональный инструмент, не routine; «не чаще 1 раза в 30 дней». Phase 1 module проверяет это поле перед предложением WoL.

| Поле | Тип | Описание |
|---|---|---|
| `last_assessed_at` | ISO 8601 / null | Timestamp последней completed Wheel of Life assessment. `null` = never assessed. |

**Gating logic в `module_phase1_diagnostic.md` §WoL Frequency Gate:**
- `now() - last_assessed_at < 30 days` → skip auto-offer; explicit user request → soft challenge
- `≥ 30 days` → predict offer re-assess
- `null` → стандартный Track A/B flow

**Write trigger:** обязательно после completed WoL assessment (любой Track A/B), set `last_assessed_at = now()` ISO 8601.

Additive, без миграции — старые v2.2.x клиенты игнорируют unknown field. Существующие пользователи получают `null` → стандартный flow на первом entry, затем gate активен.

Источник методологии: PRD v0.15 §5 Wheel of Life refactor.

### 3.4.5 diagnosis.wheel_of_life.current.health_subsegments (v2.2.6+, optional)

Детальная оценка сферы `health` через 6 sub-segments. PRD Health Assessment v1.0: разделение здоровья на multiple dimensions повышает точность самооценки и эффективность targeted изменений (modeled wellness). Phase 1 module loads `wol_health_subsegments.md` при opt-in сценариях (user shows interest ИЛИ single-score ≤ 6).

| Поле | Тип | Описание |
|---|---|---|
| `health_subsegments` | object \| null | `null` = single-score mode (default); object = detailed mode |
| `health_subsegments.energy` | 1-10 \| null | Энергия и бодрость днём (стабильность уровня) |
| `health_subsegments.recovery` | 1-10 \| null | Качество восстановления (сон + общее самочувствие) |
| `health_subsegments.physical_wellbeing` | 1-10 \| null | Физическое самочувствие (боли, подвижность) |
| `health_subsegments.stress_resilience` | 1-10 \| null | Стрессоустойчивость (управление стрессом) |
| `health_subsegments.nutrition` | 1-10 \| null | Питание и самочувствие от еды |
| `health_subsegments.reserve` | 1-10 \| null | Общий резерв (скорость восстановления после нагрузок) |

**Health Index:** `current.health` становится `avg(filled sub-segments)` (округление до десятых) если ≥ 4 заполнены. Иначе остаётся single-score (legacy). **4 категории:** ≥8 Отличный / 6.5-7.9 Хороший / 5.0-6.4 Средний / ≤5 Низкий. **Weakest sub-segment** определяется `min(filled)` с persona tie-break (ADHD → energy/recovery; Elder → recovery/physical_wellbeing).

**Write trigger:** после completed detailed-mode WoL health assessment. Same `last_assessed_at` reset (один WoL = один frequency gate trigger).

**Routing logic в `wol_health_subsegments.md` §«Routing после Health Index»:**
- Низкий (≤5) → strongly recommend Health Snapshot (Sub-feature B, v1.4.x) или Health Track (v0.19.0)
- Средний (5.0-6.4) → offer Health Snapshot
- Хороший/Отличный → surface weakest или strongest; продолжай WoL

Additive, без миграции — старые v2.2.x клиенты игнорируют unknown field. Существующие пользователи получают `health_subsegments: null` → single-score path.

Источник методологии: `docs/research/prd_health_assessment_wol_subsegments.md` v1.0.

### 3.4.6 diagnosis.health_snapshot.last (v2.2.7+, optional)

Лёгкий 4-вопросный Health Snapshot — opt-in tool, запускается при Health Index ≤ 5.5 (WoL detailed mode) ИЛИ explicit user request ИЛИ Phase 3 opt-in. Sub-feature B из PRD Health Assessment v1.0 §4.

| Поле | Тип | Описание |
|---|---|---|
| `health_snapshot.last` | object \| null | `null` = Snapshot не запускался; object = last completed Snapshot record |
| `health_snapshot.last.date` | ISO 8601 date | Дата completed Snapshot |
| `health_snapshot.last.average_score` | 1-10 \| null | `avg(filled answers)`; `null` если < 3 из 4 заполнены |
| `health_snapshot.last.weakest_question` | `"energy_stability"` \| `"recovery"` \| `"stress_management"` \| `"resilience"` \| null | Canonical ID самого слабого вопроса; `null` если 0 заполнено |
| `health_snapshot.last.answered_count` | 0-4 | Сколько вопросов получили ответ (skip allowed) |
| `health_snapshot.last.declined_count` | int ≥ 0 | Session-level counter: incremented при отказе от offer (2-decline cutoff per session) |

**Snapshot Index categories:** ≥8 Отличный / 6.5-7.9 Хороший / 5.0-6.4 Средний / ≤5 Низкий. **Safety:** все 4 ≤ 3 → escalate per SKILL.master Safety section (не оффер Health Track автоматически).

**Routing logic в `health_snapshot.md` §«Routing after Snapshot»:**
- ≤ 5.0 → strongly offer `track_health_metabolism.md` (если accept → activate `health_metabolism.active = true`)
- 5.0-6.4 → offer same; soft tone
- ≥ 6.5 → habit tweak suggestion (light); no Health Track offer

**Write trigger:** после completed Snapshot (≥ 1 ответ); декремент `declined_count` только session-level (resets per session).

**Frequency note:** Snapshot НЕ связан с WoL Frequency Gate (`last_assessed_at`). Можно запускать чаще — это lighter touch.

Additive, без миграции — `null` = Snapshot никогда не запускался. Существующие пользователи получают `null` → стандартный flow.

Источник методологии: `docs/research/prd_health_assessment_wol_subsegments.md` §4 + PHQ-2/GAD-2 short-screening patterns.

### 3.4.2 goal_filter.active_goals[].partner_coordination (v2.2+, optional)

Заполняется ТОЛЬКО для целей, затрагивающих партнёра/семью (триггеры в формулировке: «партнёр», «жена/муж», «семья», «we», «наш»). Если цель индивидуальная — поле остаётся `null` и не валидируется.

| Поле | Тип | Описание |
|---|---|---|
| `communication` | 1-10 | Насколько обсуждаешь эту цель с партнёром |
| `cooperation` | 1-10 | В чём партнёр поддерживает / препятствует |
| `compatibility` | 1-10 | Совместимость с целями/приоритетами партнёра |
| `obstacles` | array | Список препятствий со стороны отношений (свободный текст) |

Источник методологии: Transactive Goal Dynamics (Fitzsimons & Finkel) + Rosta-Filep et al. 2023. PRD: `docs/research/prd_goal_concordance.md`.

### 3.5 goals.* sphere references

Все цели должны ссылаться на canonical sphere ID (см. §1). Запрещено использовать legacy имена.

### 3.5.2 weekly_reviews[].gap_analysis + lessons_learned (v2.2.4+, opt-in)

AAR Gap Analysis (Step 8) и Lessons Learned (Step 9) из `module_phase3_weekly_review.md`. `gap_analysis` skip при `execution_score ≥ 70%`. **COM-B escalation:** тот же gap (по what/category) повторяется ≥ 2 недели → загрузить `references/com_b_diagnostic.md`. **Lessons surface:** `sighted_count ≥ 3` → quarterly OKR adjustment. Источник: After Action Review (US Army TC 25-20, 1993) + Garvin (2000) *Learning in Action*.

| Поле gap_analysis[] | Описание |
|---|---|
| `gap_id` | `GA1`, `GA2`, ... |
| `what` | Краткое описание провала |
| `why_three_levels` | Three Whys: поверхностный → глубже → системный |
| `category` | `"internal"` / `"external"` / `"both"` |

| Поле lessons_learned[] | Описание |
|---|---|
| `lesson` | Конкретный insight (≤ 1 предложение, action-oriented) |
| `category` | `"planning"` / `"habits"` / `"energy"` / `"environment"` / etc. (free-text) |
| `sighted_count` | Инкремент при semantic match с previous lesson (same category + общая тема: «time blocking», «morning routine», «recovery») в last 4 weekly_reviews. Иначе append с `sighted_count: 1`. Surface threshold ≥ 3 → quarterly OKR adjustment. Pattern-matching protocol — `module_phase3_weekly_review.md` Step 9 (v1.3.0+, runtime skill-instruction, не Python algorithm). |

### 3.5.1 goals.premortem_assessments (v2.2.3+, opt-in)

Результаты Premortem упражнения (Klein 2007 HBR). Запускается через Phase 2 trigger для важных OKR. Если список пуст — Premortem не проводился. Используется для tracking realized risks на mid-quarter review (Phase 3, week 6).

| Поле | Тип | Описание |
|---|---|---|
| `premortem_id` | string | `PM1`, `PM2`, ... |
| `goal_id` | string | Ссылка на `goals.twelve_week_okr.objectives[].objective_id` или `goals.life_themes[].theme_id` |
| `conducted_at` | ISO 8601 | Когда упражнение было проведено |
| `trigger` | enum | `"low_confidence"` / `"long_horizon"` / `"partner_coord"` / `"explicit_request"` / `"mid_quarter_stagnation"` |
| `top_risks[]` | array | Top-3 risks с mitigation: `{risk (string), category, mitigation_intention (if-then format, ссылается на II)}` |
| `top_risks[].category` | enum | `"internal"` / `"external"` / `"missed_inputs"` / `"scope_creep"` / `"motivation_drift"` |
| `top_risks[].mitigation_intention` | string | Coping plan в формате `«Если [precisely момент], то [конкретный action]»` (см. `implementation_intentions.md` §Coping plans) |
| `next_review_date` | ISO 8601 (date) | Когда проверить реализацию рисков (обычно week 6 для 12-week OKR) |

Источник методологии: Klein, G. (2007). *Performing a Project Premortem*. HBR. См. `references/premortem.md` для полного протокола.

### 3.6 habits

В отличие от v1 (только streak counts) — теперь полный Habit Loop с cue/routine/reward + Tiny Habits + anchor для habit stacking.

### 3.7 wins_log

В v1 wins лежали внутри `weekly_reviews[].wins`. В v2 — first-class сущность для win_alert.md протокола и dashboard widget.

---

## 4. Schema versioning policy

### 4.1 Additive bumps (минор и patch)

- `2.0 → 2.0.1`: добавление `session.gating_mode` tracker для observability persistence mode. Старые клиенты v2.0 игнорируют unknown field. Не требует миграции.
- `2.0.1 → 2.1`: добавление Health & Metabolism Track (`diagnosis.health_metabolism` блок). Старые клиенты игнорируют unknown field. **Реализован в v0.19.0.**
- `2.1 → 2.2`: добавление Goal Concordance (`goal_filter.active_goals[].partner_coordination` optional sub-block). Старые клиенты игнорируют unknown property. **Реализован в v0.19.0.**
- `2.2 → 2.2.2`: добавление `diagnosis.com_b_assessment` optional поле (COM-B диагностика, PRD v0.15 §COM-B). Старые клиенты игнорируют unknown field. **Реализован в v1.2.0.** (2.2.1 был внутренний bump без публичной фиксации.)
- `2.2.2 → 2.2.3`: добавление `goals.premortem_assessments[]` optional массив (Premortem упражнение, Klein 2007 HBR). Старые клиенты игнорируют unknown field. **Реализован в v1.2.0** (PR2/3).
- `2.2.3 → 2.2.4`: добавление `weekly_reviews[].gap_analysis[]` + `weekly_reviews[].lessons_learned[]` optional полей (AAR Gap Analysis + pattern capture, US Army TC 25-20). Старые клиенты игнорируют unknown fields. **Реализован в v1.2.0** (PR3/3).
- `2.2.4 → 2.2.5`: добавление `diagnosis.wheel_of_life.last_assessed_at` optional ISO 8601 поле (PRD v0.15 §5 frequency gate). Phase 1 module skips WoL auto-offer < 30 days, offers re-assess ≥ 30 days. Старые клиенты игнорируют unknown field. **Реализован в v1.3.0** (PR-A).

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

**Write abstraction.** Все Wiki-записи в `full_persistence` / `wiki_no_execution` modes проходят через `save_state(template, content)` — single skill-instruction call site, definition в [`drive_integration.md` §save_state](drive_integration.md#save_statetemplate-content--write-abstraction). Path A backend (default): new file `{template}_{ISO}.md`; "current" = latest by `modifiedTime` через `read_state(template)`. Path B/F variants swap backend без переписывания call sites в phase modules.

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
- Skill спрашивает user о `wiki_cleanup_mode` (см. §7.1)

### 7.1 Cleanup mode choice (после bootstrap)

После создания Wiki structure, skill промптит user:

```
"Skill пишет snapshots в Drive (Hot_Cache_TS.md и т.д.) и они накапливаются.
Как ты хочешь управлять файлами?
  1. apps_script   — установлю Apps Script (3 min, auto-cleanup forever)
  2. batch_weekly  — skill пишет реже (раз в неделю — меньше файлов)
  3. reminder      — skill quarterly напомнит почистить (по умолчанию)
  4. ignore        — skill пишет per-session, файлы накапливаются (norm Drive storage)"

Запиши выбор:
  persistence_retry.drive.wiki_cleanup_mode = "<choice>"
  persistence_retry.drive.wiki_cleanup_chosen_at = now()
```

Behavior per mode:

| Mode | Write cadence | Skill notifications | Setup required |
|------|---------------|--------------------|-----------------| 
| `apps_script` | per-session | one-time link к `templates/lpc_wiki_cleanup.gs` setup | ~3 min user setup |
| `batch_weekly` | end-of-week только | "сохраню в воскресенье" mention | none |
| `reminder` | per-session | quarterly: "N файлов, вот query для cleanup" | none |
| `ignore` | per-session | none | none |

Если user не выбрал — default = `reminder`.

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
| `session.gating_mode` | SKILL.master.md §3 (на старте сессии) | ✅ **(v0.18.0)** master detect + write |
| `persona.active_mode` | Phase 0 persona detection | ✅ **(v0.18.0)** `module_phase1_diagnostic.md` State Writes |
| `diagnosis.wheel_of_life` | Phase 1 Wheel of Life | ✅ существующая логика |
| `diagnosis.values_schwartz` | Phase 1 Values PVQ | ✅ существующая логика |
| `diagnosis.core_values` | Phase 1.5 Core Values Discovery | ✅ `module_phase1_5_goal_filter.md` |
| `diagnosis.ikigai_pillars` | Phase 1 deep diagnostic (Track B) | ✅ существующая логика |
| `goals.*` | Phase 2 Goal Architecture | ✅ существующая логика |
| `goal_filter.*` | Phase 1.5 Authentic Goal Filter | ✅ существующая логика |
| `goal_filter.active_goals[].core_values_alignment` | Phase 1.5 (link при добавлении цели) | ✅ **(v0.18.0)** `module_phase1_5_goal_filter.md` |
| `habits[]` (full cue/routine/reward/anchor/tiny_version) | Phase 2 Habit creation + Phase 3 review | ✅ **(v0.18.0)** `module_phase2_goal_architecture.md` State Writes |
| `weekly_reviews[]` | Phase 3 Weekly Review | ✅ существующая логика |
| `emotion_regulation_log` | Phase 0.5 ER Protocol | ✅ **(v0.18.0)** `module_phase1_diagnostic.md` State Writes |
| `wins_log` | Phase 3 Celebration + win_alert.md | ✅ **(v0.18.0)** `module_phase3_weekly_review.md` State Writes |
| `reward_audit_results` | Phase 3 Step 7 (optional) + reward_audit.md | ✅ **(v0.18.0)** `module_phase3_weekly_review.md` State Writes |
| `calendar_events_log` | Phase 5 MCP create events | ✅ **(v0.18.0)** `module_phase5_execution.md` State Writes |
| `recovery_sessions_log` | Phase 5 + recovery_protocol.md | ✅ **(v0.18.0)** `module_phase5_execution.md` State Writes |
| `persistence_retry.*` | SKILL.master.md (bootstrap, backfill) | ✅ **(v0.18.0)** master + `templates/AI_Instructions.md` |
| `diagnosis.health_metabolism.*` | Phase 1 Health Track entry (opt-in) + Phase 3 Health review | ✅ **(v0.19.0, schema 2.1)** `module_phase1_diagnostic.md` + `module_phase3_weekly_review.md` + `track_health_metabolism.md` |
| `goal_filter.active_goals[].partner_coordination` | Phase 1.5 Partner Coordination Check (step 7) | ✅ **(v0.19.0, schema 2.2)** `module_phase1_5_goal_filter.md` |
| `diagnosis.com_b_assessment` | Phase 0 / Phase 1 / Phase 3 COM-B opt-in diagnostic | ✅ **(v1.2.0, schema 2.2.2)** `module_phase1_diagnostic.md` + `com_b_diagnostic.md` |
| `goals.premortem_assessments[]` | Phase 2 Premortem trigger (confidence ≤ 6 / horizon ≥ 1y / partner_coord) | ✅ **(v1.2.0, schema 2.2.3)** `module_phase2_goal_architecture.md` + `premortem.md` |
| `weekly_reviews[].gap_analysis[]` + `lessons_learned[]` | Phase 3 AAR steps 8–9 (Lean Gap Analysis + pattern capture) | ✅ **(v1.2.0, schema 2.2.4)** `module_phase3_weekly_review.md` шаги 8–9 |
| `diagnosis.wheel_of_life.last_assessed_at` | Phase 1 Wheel of Life completion (любой Track A/B) | ✅ **(v1.3.0, schema 2.2.5)** `module_phase1_diagnostic.md` §WoL Frequency Gate |
| `diagnosis.wheel_of_life.current.health_subsegments` | Phase 1 WoL `health` detailed mode (opt-in, single-score ≤ 6 ИЛИ explicit interest) | ✅ **(v1.4.0, schema 2.2.6)** `module_phase1_diagnostic.md` + `wol_health_subsegments.md` |
| `diagnosis.health_snapshot.last` | Phase 1 после Health Index ≤ 5.5 ИЛИ explicit request ИЛИ Phase 3 opt-in (Sub-feature C) | ✅ **(v1.4.0, schema 2.2.7)** `module_phase1_diagnostic.md` + `health_snapshot.md` |

**Все write-rules** теперь явно прописаны в соответствующих модулях. Tests (`tests/unit/test_v018_gating_state_writes.py`, `tests/unit/test_v019_health_concordance.py`) гарантируют, что каждое поле имеет write-trigger.

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

- [plan_v1.0_templates_rebuild.md](../docs/research/plan_v1.0_templates_rebuild.md) — план rebuild всех шаблонов
- [prd_core_values_discovery.md](../docs/research/prd_core_values_discovery.md) — источник `core_values` блока + Compass Mode (FR-04)
- [prd_health_metabolism.md](../docs/research/prd_health_metabolism.md) — schema bump 2.1
- [prd_goal_concordance.md](../docs/research/prd_goal_concordance.md) — schema bump 2.2
- `conversation_state_schema.md` — v1 schema удалён в v1.1.0. Migration таблица сохранена в §8 выше для legacy forks.
- `tests/unit/test_v018_gating_state_writes.py` — гарантирует write-rules для всех полей §9
- `tests/unit/test_tier_token_budgets.py` — Tier 1/2 budgets check
- `references/templates/AI_Instructions.md` — bootstrap + backfill + gating protocols (operational layer)

---

**Статус:** ✅ Canonical. Любые изменения требуют schema_version bump + миграционных заметок.

## 12. Changelog схемы

- **2.2.7** (2026-05-28) — Add `diagnosis.health_snapshot.last` optional object (PRD Health Assessment v1.0 §4). Lightweight 4-question Snapshot tool: average score, weakest question ID, answered/declined counts. Запускается при WoL Health Index ≤ 5.5 ИЛИ explicit user request ИЛИ Phase 3 opt-in (Sub-feature C). 2-decline cutoff per session. Routing: ≤ 5.0 → strongly offer `track_health_metabolism.md`; 5.0-6.4 → soft offer; ≥ 6.5 → light habit tweak. **Safety:** все 4 ≤ 3 → escalate per SKILL.master Safety. Tier 3 ref: `references/health_snapshot.md`. Phase 1 module routes к нему опционально. Additive, без миграции — `null` = Snapshot не запускался. Source: PRD §4 + PHQ-2/GAD-2 short-screening patterns. Реализовано в **v1.4.0** Sub-feature B.
- **2.2.6** (2026-05-28) — Add `diagnosis.wheel_of_life.current.health_subsegments` optional object (PRD Health Assessment v1.0 §7). 6 sub-segments (energy / recovery / physical_wellbeing / stress_resilience / nutrition / reserve), 1-10 каждый, для opt-in detailed health assessment. `current.health` становится Health Index (avg) если ≥ 4 sub-segments заполнены; иначе single-score (legacy). 4 категории + weakest sub-segment surface. Source: PRD Health Assessment v1.0 (2026-05-27) + Schultchen et al. (2019) bidirectional stress-activity. Tier 3 ref: `references/wol_health_subsegments.md`. Phase 1 module loads ref при opt-in. Additive, без миграции — `null` = single-score path. Реализовано в **v1.4.0** Sub-feature A.
- **2.2.5** (2026-05-27) — Add `diagnosis.wheel_of_life.last_assessed_at` optional ISO 8601 timestamp поле (PRD v0.15 §5 frequency gate). Phase 1 module gates WoL auto-offer: skip < 30 days; offer re-assess ≥ 30 days; null = never assessed → standard flow. Source: PRD v0.15 §5 «WoL не чаще 1 раза в 30 дней». Additive, без миграции — поле остаётся null для existing users. Реализовано в **v1.3.0** (PR-A).
- **2.2.4** (2026-05-27) — Add `weekly_reviews[].gap_analysis[]` + `weekly_reviews[].lessons_learned[]` optional полей (AAR Gap Analysis + pattern capture, PRD v0.15 §After Action Review). Источник: After Action Review (US Army TC 25-20, 1993) + Garvin (2000) *Learning in Action*. Lean integration — 7-step → 9-step Weekly Review с Step 8 Gap Analysis (Three Whys + COM-B escalation) и Step 9 Lessons Learned (`sighted_count ≥ 3` → quarterly adjustment). Skip при `execution_score ≥ 70%`. ADHD persona opt-out. Additive. Реализовано в **v1.2.0** (PR3/3).
- **2.2.3** (2026-05-27) — Add `goals.premortem_assessments[]` optional массив (Premortem упражнение для важных OKR, PRD v0.15 §Premortem). Источник: Klein, G. (2007). *Performing a Project Premortem*. HBR. Активируется через Phase 2 trigger (confidence ≤ 6 / horizon ≥ 1y / partner_coord / explicit_request / mid_quarter_stagnation). Mitigation через if-then coping plans (Implementation Intentions). Additive, без миграции — массив пуст если упражнение не запускалось. Реализовано в **v1.2.0**.
- **2.2.2** (2026-05-27) — Add `diagnosis.com_b_assessment` optional поле (COM-B диагностика причин бездействия, PRD v0.15 §COM-B). Источник: Michie, van Stralen, West (2011) *Implementation Science* 6(42). Активируется через opt-in COM-B протокол в Phase 0/1/3. Additive, без миграции — поле остаётся `null` если диагностика не выполнялась. Реализовано в **v1.2.0**.
- **2.2** (2026-05-28) — Add `goal_filter.active_goals[].partner_coordination` optional sub-block (Goal Concordance, PRD v2.0). Источник: Transactive Goal Dynamics (Fitzsimons & Finkel) + Rosta-Filep 2023. Additive, без миграции — поле остаётся `null` для индивидуальных целей.
- **2.1** (2026-05-28) — Add `diagnosis.health_metabolism` opt-in блок (PRD v2.1): sleep/stress/protein/fiber/chewing/caffeine метрики + micro_experiments_log. Activate через Phase 1 Health Track entry. Additive, не активируется без opt-in.
- **2.0.1** (2026-05-27) — Add `session.gating_mode` tracker. Close 7 write-rule gaps в §9 (persona.active_mode, emotion_regulation_log, wins_log, reward_audit_results, calendar_events_log, recovery_sessions_log, core_values_alignment). Additive, без миграции.
- **2.0** (2026-05-26) — Initial v2 release. Canonical 11 spheres, persona block, core_values, full habits cue/routine/reward, wins_log first-class, persistence_retry tracking.
