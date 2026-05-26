# Plan: v1.0 Templates Rebuild — Wiki + Dashboard + Guide

**Дата:** 2026-05-26
**Контекст:** Подготовительный блок v1.0 архитектурного рефакторинга. Пересборка 3 шаблонов (8 wiki templates + HTML dashboard + dashboard_guide.md) в связке через единый state v2 schema.
**Статус:** 📋 Plan ready, ждёт реализации (B1 → B5).
**Связанные:** [prd_core_values_discovery.md](prd_core_values_discovery.md), [prd_health_metabolism.md](prd_health_metabolism.md), [prd_goal_concordance.md](prd_goal_concordance.md)

---

## 1. Цели

- Устранить **структурный drift** между state schema, HTML dashboard, wiki templates и dashboard_guide.md.
- Привести все артефакты к **canonical 11 spheres** с единым naming.
- Перейти к **single source of truth**: state v2 → HTML / wiki / guide через автоматизированный data flow.
- Интегрировать **Core Values Discovery** (опциональные секции под Health Track и Goal Concordance — позже, при реализации этих PRD).
- Внедрить **gating-логику**: полное логирование state и Drive Wiki bootstrap активируются только при подключении Drive + Calendar.
- **Backfill при mid-session connection** — не теряем данные, накопленные до подключения.

## 2. Non-goals

- Реализация Health & Metabolism Track и Goal Concordance PRD (отдельные релизы → schema bumps 2.1 / 2.2).
- Полная декомпозиция SKILL.md на Tier 1-5 модули (см. основной refactor plan).
- Замена ECharts / Chart.js (текущий стек сохраняется).
- Изменение визуального стиля dashboard (Apple-like дизайн сохраняется).

---

## 3. Текущее состояние — drift inventory

### 3.1 Sphere count mismatch

| Артефакт | Sphere count | Статус |
|---|---|---|
| SKILL.md | 11 | ✅ canonical |
| conversation_state_schema.md | 11 | ✅ canonical |
| life-planning-dashboard.html (`WHEEL_SPHERES`) | 11 | ⚠️ count ok, naming drift |
| dashboard_guide.md §4.4 | **8** | ❌ stale |
| references/templates/Wheel_of_Life_History.md | **8** | ❌ stale |

### 3.2 Naming drift внутри 11 spheres

| state_schema (canonical) | HTML | wiki |
|---|---|---|
| `personal_growth` | `growth` | «Личностный рост» |
| `meaning` | `spirituality` | «Смысл» |
| `fun_recreation` | `fun` | «Развлечения» |
| `physical_environment` | `environment` | «Окружение» |

### 3.3 Версии out of sync

- `dashboard_guide.md` header: «Версия 1.0, 2026-01-15, Статус: Проект»
- `life-planning-dashboard.html` CSS-комментарий: «DASHBOARD v0.9.1»
- Skill: v0.14.0
- `conversation_state_schema.md`: без version header

### 3.4 Broken refs в `templates/Index.md`

Ссылается на несуществующие файлы:
- `01_Wiki/Concepts/Wheel_of_Life.md`
- `01_Wiki/Concepts/WOOP.md`
- `01_Wiki/Concepts/OKR.md`
- `01_Wiki/Frameworks/Weekly_Review.md`
- `01_Wiki/Frameworks/Focus_Blocks.md`

### 3.5 JSON contract mismatch (guide vs HTML)

- Guide: `currentScore` / `previousScore` / `targetScore`
- HTML: `current` / `prev` / `target`
- Guide описывает `dailyScores: DailyScore[]` для heatmap; HTML генерирует синтетику внутри `renderHeatmap`
- HTML хардкодит данные в `<script>` → data contract игнорируется

### 3.6 Stage vs Phase терминология

- `conversation_state_schema.md`: `stage: "1|1.5|2|3"`
- `SKILL.md`: Phase 0, 0.5, 1, 1.5, 2, 3, 4, 5 (8 фаз)

### 3.7 Поля, которых нет (нужны для v2)

| Поле | Источник | Зачем |
|---|---|---|
| `core_values` | PRD Core Values Discovery | Compass mode + alignment per goal |
| `active_persona_mode` | Phase 0 persona detection | Адаптация шаблонов |
| `emotion_regulation_log` | Phase 0.5 | История ER-протоколов |
| `habit_cue_routine_reward` | habit_loop.md | Полноценный Habit Loop (не только streak) |
| `wins_log` | win_alert.md | First-class wins, не вложено в weekly_reviews |
| `reward_audit_results` | reward_audit.md | Cheap dopamine awareness |
| `calendar_events_log` | Phase 5 MCP | Какие события созданы и когда |
| `recovery_sessions_log` | recovery_protocol.md | История восстановлений после пропусков |

Health Track и Goal Concordance поля добавятся в их PRD-релизах через additive schema bump.

---

## 4. Стратегия — Single Source of Truth + Gating

```
                       state_v2.json (canonical)
                              ↓
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
       HTML dashboard    8 wiki templates  module_phase4_dashboard
       (data-driven)     (markdown views)  (specification)
```

### 4.1 Gating логика

```
on session_start:
  detect drive_connected, calendar_connected

  if drive && calendar:
    mode = "full_persistence"
    if first_connection:
      bootstrap_drive_wiki()
    enable_full_state_logging()
    enable_template_population()

  elif drive && !calendar:
    suggest: "Подключи Calendar для execution layer"
    mode = "wiki_no_execution"
    enable_full_state_logging()

  elif !drive && calendar:
    suggest: "Подключи Drive для persistence wiki"
    mode = "execution_no_wiki"
    lean_state_only()

  else:
    mode = "lean_conversation"
    минимальный state в conversation memory
    dashboard генерируется one-shot из in-memory state
```

### 4.2 Backfill при mid-session connection (edge case (a) — выбран)

```
on mid_session_drive_connection:
  if previously_lean:
    prompt: "У тебя накопилось данных за сессию (Phase 0, Wheel of Life, N целей) —
             синхронизировать в Drive?"
    if yes:
      bootstrap_drive_wiki()
      one_shot_dump_current_state_v2_to_wiki()
      confirm: "Wiki создан, прогресс сохранён"
      enable_full_state_logging()
    if no:
      user_declined_count += 1
      if >= 2: backoff 3 sessions
```

---

## 5. State v2 schema (concept)

Полная схема выйдет в `references/state_v2_schema.md` (deliverable B1). Здесь — top-level keys.

```jsonc
{
  "schema_version": "2.0",
  "user_id": "uuid",

  "session": {
    "current_phase": "0|0.5|1|1.5|2|3|4|5",
    "current_track": "quick|deep",
    "current_question_index": 0,
    "readiness_gates": [{"phase": "1", "score": 8, "timestamp": "..."}]
  },

  "persona": {
    "active_mode": "none|adhd|unemployed|elder|planning_friction",
    "detected_at": "...",
    "user_confirmed": true
  },

  "communication_style": {
    "baseline": {"softness": "soft|neutral|direct", "structure": "high|medium|low"},
    "current_intensity": "nurturing|exploratory|collaborative|challenging"
  },

  "diagnosis": {
    "wheel_of_life": {
      "health": 7, "finances": 6, "career": 4, "family": 8,
      "romance": 7, "social": 6, "personal_growth": 5,
      "meaning": 6, "fun_recreation": 3, "contribution": 5,
      "physical_environment": 6,
      "history": [{"date": "2026-W18", "scores": {...}}]
    },
    "values_schwartz": {"self_direction": 0.85, "...": "..."},
    "core_values": [
      {
        "name": "Autonomy",
        "description": "...",
        "derived_from": [
          {"type": "domain", "ref": "career"},
          {"type": "experience", "ref": "..."},
          {"type": "energizing_activity", "ref": "..."}
        ],
        "compass_question": "Does this choice expand or shrink my autonomy?",
        "priority_rank": 1
      }
    ],
    "ikigai_pillars": {"love": "...", "good_at": "...", "world_needs": "...", "paid_for": "..."}
  },

  "goals": {
    "bhag": "...",
    "themes": [{"objective": "...", "key_results": []}],
    "twelve_week_okr": {"objectives": [], "key_results": []},
    "weekly_priorities": ["..."],
    "daily_woop": [{"wish": "...", "outcome": "...", "obstacle": "...", "plan": "..."}]
  },

  "goal_filter": {
    "active_goals": [
      {
        "goal_id": "G1",
        "title": "...",
        "radar": {"values": 9, "energy": 8, "impact": 9, "feasibility": 7, "authenticity": 8},
        "core_values_alignment": ["Autonomy", "Growth"],
        "deep_why_chain": ["...", "...", "..."],
        "red_flags_screened": []
      }
    ],
    "paused_goals": [{"goal": "...", "red_flags": ["RF3"], "insight": "..."}],
    "patterns": [{"red_flag": "RF3", "count": 2, "insight": "..."}]
  },

  "habits": [
    {
      "habit_id": "H1",
      "name": "...",
      "cue": "...",
      "routine": "...",
      "reward": "...",
      "anchor": "...",
      "current_streak": 5,
      "best_streak": 12,
      "status": "on_track|at_risk|off_track"
    }
  ],

  "weekly_reviews": [
    {
      "date": "2026-05-16",
      "format": "gtd_scrum",
      "worked": ["..."],
      "didnt_work": ["..."],
      "changes": ["..."],
      "lead_measures": {},
      "lag_measures": {},
      "adjustments": []
    }
  ],

  "emotion_regulation_log": [
    {
      "date": "...",
      "protocol": "reappraisal|grounding|self_compassion",
      "trigger": "...",
      "outcome_readiness": 8
    }
  ],

  "wins_log": [
    {"date": "...", "win": "...", "goal_id": "G1", "category": "milestone|first|streak"}
  ],

  "reward_audit_results": [
    {"date": "...", "cheap_dopamine_sources": ["..."], "commitment": "..."}
  ],

  "calendar_events_log": [
    {"created_at": "...", "event_type": "weekly_review|woop|habit|...", "event_id": "..."}
  ],

  "recovery_sessions_log": [
    {"date": "...", "gap_days": 14, "strategy_used": "...", "outcome": "..."}
  ],

  "persistence_retry": {
    "drive": {"available_last_session": true, "failed_consecutive_sessions": 0, "..."},
    "calendar": {"available_last_session": true, "pending_events_count": 0, "..."}
  }
}
```

**Будущие schema bumps (additive):**
- `2.1` — Health & Metabolism Track: `health_metabolism: {sleep_avg_hours, stress_level, caffeine_cutoff_time, protein_target_g, fiber_target_g, chewing_practice, active_experiments}`
- `2.2` — Goal Concordance: `goals[].partner_coordination: {communication: 1-10, cooperation: 1-10, compatibility: 1-10, obstacles[]}`

---

## 6. Canonical 11 spheres

| ID (canonical) | Russian display | Icon |
|---|---|---|
| `health` | Здоровье | 🏥 |
| `finances` | Финансы | 💰 |
| `career` | Карьера | 💼 |
| `family` | Семья | 👨‍👩‍👧 |
| `romance` | Отношения с партнёром | 💕 |
| `social` | Дружба | 🤝 |
| `personal_growth` | Личностный рост | 📚 |
| `meaning` | Смысл и духовность | 🧘 |
| `fun_recreation` | Отдых и хобби | 🎉 |
| `contribution` | Вклад | 🌍 |
| `physical_environment` | Дом и среда | 🏠 |

Этот список — единственный источник правды для всех 3 шаблонов и state v2.

---

## 7. Wiki templates rebuild — diff «было → станет»

### 7.1 `AI_Instructions.md`
- + reference на state v2 schema
- + gating logic (когда писать полно vs lean)
- + backfill protocol
- + canonical sphere naming
- + Core Values handling rules

### 7.2 `Hot_Cache.md`
- + `active_persona_mode`
- + `core_values` топ-3 (с compass questions)
- + `active_emotion_protocols` (если идёт работа в Phase 0.5)
- + `readiness_average` за сессию

### 7.3 `Index.md`
- **Убрать broken refs** на `Concepts/` и `Frameworks/` (static knowledge, не user data — не нужны в wiki)
- Добавить ссылку на новый `Core_Values_Compass.md`

### 7.4 `Goals.md`
- + Authentic Goal Filter radar блок на каждую цель (values / energy / impact / feasibility / authenticity)
- + `core_values_alignment` поле (какие core values поддерживает цель)
- + optional placeholder для Goal Concordance (`partner_coordination` секция — закомментирована, активируется при PRD)

### 7.5 `Wheel_of_Life_History.md`
- **11 сфер вместо 8** с canonical naming
- Обновить визуализации, таблицу динамики, архивные оценки

### 7.6 `Raw_Session.md`
- + `persona_mode` использовался ли
- + `emotion_regulation_used` (какие протоколы)
- + `calendar_events_created` (список ID)
- + `wins_captured`
- + `readiness_gates_in_session`

### 7.7 `Progress_Dashboard.md`
- **Repurpose**: становится **text-mode dashboard** для Paper Coach Mode (когда HTML недоступен)
- Расширить до полной картины state v2 в text-only формате
- Используется как fallback для платформ без HTML rendering

### 7.8 `USER_PROGRESS_JOURNAL.md`
- + категории: `Core_Values_Discovery`, `Persona_Transition`, `Emotion_Regulation_Breakthrough`
- + placeholder категории для будущих PRD: `Health_Milestone`, `Concordance_Insight`

### 7.9 NEW: `Core_Values_Compass.md`
- Список 5-7 core values с descriptions
- Compass questions для каждой
- Alignment per goal (cross-link с Goals.md)
- История пересмотров values

---

## 8. HTML Dashboard rebuild

### 8.1 Удалить
- Hardcoded `WHEEL_SPHERES`, `EXECUTION_SCORES`, `VELOCITY_DATA`, `STREAK_DATA`
- Хардкод-контент в WOOP cards, BHAG roadmap, OKR cards
- CSS-комментарий «v0.9.1»

### 8.2 Добавить
- `window.lpData` injection point (skill инжектит state v2 JSON)
- **Core Values panel** (новая секция в Overview): топ-5-7 values + compass questions
- Placeholder hooks для Health Track / Goal Concordance (collapsed by default, активируются при `schema_version >= 2.1 / 2.2`)
- Version bump → `v1.0.0`
- Schema version compatibility check в `renderDashboard()`

### 8.3 Сохранить
- Apple-style CSS (light + dark themes)
- 3 таба (Overview / Retrospective / Goals)
- Modal для drill-down
- Print CSS для PDF export
- ECharts / Chart.js stack

### 8.4 Canonical naming в HTML
Переименовать в `WHEEL_SPHERES`:
- `growth` → `personal_growth`
- `spirituality` → `meaning`
- `fun` → `fun_recreation`
- `environment` → `physical_environment`

---

## 9. dashboard_guide.md split

| Было | Станет |
|---|---|
| 2538 строк, монолитный design doc от 2026-01-15 | Тонкий `references/module_phase4_dashboard.md` (≤ 300 строк): когда генерировать, как читать state v2, JSON-контракт sync с schema. Heavy дизайн-документ → `docs/research/dashboard_architecture_v1.md` (dev-only). |

**Эффект:** -7K tokens из runtime при загрузке Phase 4.

---

## 10. Drive Wiki bootstrap (структура при первом коннекте)

```
Life Planning Coach Wiki/
├── 00_Raw/                              # append-only session captures
├── 01_Wiki/
│   ├── Hot_Cache.md                     # short summary (<1000 tokens)
│   ├── Index.md                         # navigation
│   ├── User_Progress/
│   │   ├── Goals.md
│   │   ├── Wheel_of_Life_History.md     # 11 spheres canonical
│   │   ├── Core_Values_Compass.md       # NEW
│   │   └── USER_PROGRESS_JOURNAL.md
│   └── Decisions/                       # session decisions log
├── 02_Instructions/CLAUDE.md
├── 03_Dashboard/
│   ├── Progress_Dashboard.md            # text mode dashboard
│   └── dashboard_data.json              # state v2 snapshot for HTML render
├── 05_Archive/
├── README.md
└── CHANGELOG.md
```

**Снято** (по сравнению с текущим `AI_Instructions.md`):
- `04_References/` — не нужен (references поставляются со skill)
- `01_Wiki/Concepts/`, `01_Wiki/Frameworks/`, `01_Wiki/Sources/` — static knowledge, не user data

**Добавлено:**
- `Core_Values_Compass.md`
- `03_Dashboard/dashboard_data.json` — state snapshot, который читает HTML

---

## 11. Acceptance criteria

- [ ] Sphere count = 11 во всех артефактах (тест проходит)
- [ ] Naming sphere IDs идентичен в state_v2 / HTML / wiki / guide (тест проходит)
- [ ] HTML dashboard data-driven: нет hardcoded `const WHEEL_SPHERES` / `EXECUTION_SCORES` в `<script>`
- [ ] `Index.md` содержит только существующие refs
- [ ] state_v2 schema содержит блок Core Values + persona + emotion_log + wins_log + reward_audit + calendar_log + recovery_log
- [ ] `dashboard_guide.md` split: новый `module_phase4_dashboard.md` ≤ 300 строк
- [ ] Bootstrap создаёт ровно 8 файлов + 4 директории при первом коннекте
- [ ] Backfill prompt появляется при mid-session connection (тест с моком)
- [ ] Все wiki templates версионированы (frontmatter с `schema_version: 2.0`)
- [ ] Deprecation map: old paths → new (для wiki пользователей legacy 8 spheres)

---

## 12. Тестовая матрица

| Тест | Проверяет |
|---|---|
| `test_sphere_count_canonical` | 11 spheres везде, ID names match |
| `test_state_v2_schema_completeness` | Все обязательные поля присутствуют |
| `test_html_data_driven` | Нет hardcoded data в `<script>` (только `window.lpData`) |
| `test_wiki_template_token_budget` | Hot_Cache < 1000 tokens, Goals < 1500, остальные < 800 |
| `test_index_refs_resolve` | Все ссылки в Index.md существуют |
| `test_dashboard_guide_size` | `module_phase4_dashboard.md` ≤ 300 строк |
| `test_bootstrap_structure` | Drive Wiki bootstrap создаёт canonical структуру |
| `test_backfill_prompt` | Mid-session connection триггерит prompt |
| `test_schema_versioning` | Schema bumps additive (не ломают v2.0 clients) |
| `test_html_schema_compat` | HTML рендерит v2.0 / v2.1 / v2.2 корректно |

---

## 13. Phasing & estimates

| Блок | EAS | Содержание | Зависимости |
|---|---|---|---|
| **B1** | 1 | `references/state_v2_schema.md` (полная схема с Core Values) | — |
| **B2** | 1.5 | 8 wiki templates rebuild + новый `Core_Values_Compass.md` | B1 |
| **B3** | 1.5 | HTML dashboard data-driven rebuild + canonical naming + Core Values panel | B1 |
| **B4** | 0.5 | `dashboard_guide.md` split на `module_phase4_dashboard.md` + `docs/research/dashboard_architecture_v1.md` | B1 |
| **B5** | 0.5 | Tests + deprecation map + bootstrap-логика в `SKILL.master.md` | B2, B3, B4 |

**Итого:** ~5 EAS. Scope = minor v0.16.0 (или подготовительный блок major v1.0).

---

## 14. RICE

- **Reach:** 100 — все пользователи зависят от консистентности шаблонов и точности дашборда
- **Impact:** 2.0 — устраняет drift, разблокирует Core Values, готовит фундамент под Health/Concordance
- **Confidence:** 75% — чёткий scope, понятный путь; риск hidden edge cases при 3-way sync
- **Effort:** 5 EAS, Context Pressure Medium
- **RICE = 100 × 2.0 × 75% / 5 = 30.0 (Quick Win)**

---

## 15. Риски и митигация

| Риск | Митигация |
|---|---|
| Legacy wiki пользователи (8 spheres) сломаются при обновлении | Deprecation map + migration prompt при первом запуске после обновления: «Wiki schema обновлён до v2 — мигрировать?» |
| HTML breaking changes ломают сохранённые дашборды | Bump major version v1.0.0; v0.x продолжает работать для существующих файлов; новый HTML только для свежесгенерированных |
| Backfill дамп при mid-session connection крадёт ~10-20K токенов | Лимит на bootstrap: только Hot_Cache + Goals + Wheel_of_Life_History в первой пачке; остальное при batch-write в конце сессии |
| Schema drift возвращается при добавлении Health/Concordance PRD | Тест `test_schema_versioning` — schema bumps только additive, mandatory CI check |
| Core Values секция пустая у новых пользователей до прохождения discovery | Placeholder с CTA: «Пройди Core Values Discovery в Phase 1.5 → секция заполнится» |

---

## 16. Связанные документы

- [prd_core_values_discovery.md](prd_core_values_discovery.md) — источник Core Values блока
- [prd_health_metabolism.md](prd_health_metabolism.md) — будущий schema bump 2.1
- [prd_goal_concordance.md](prd_goal_concordance.md) — будущий schema bump 2.2
- [rice_evaluation_backlog.md](rice_evaluation_backlog.md) — RICE entry (#21)
- `BACKLOG.md` — Active Candidates entry «Templates Rebuild v1.0»
- `SKILL.master.md` — целевой файл для добавления gating + backfill логики
- `references/conversation_state_schema.md` — текущая схема, будет заменена на state_v2

---

**Готовность:** Plan ready. Следующий шаг — B1 (state_v2_schema.md), foundational для B2-B4.
