## Что нового в v0.19.0 — Health Track + Goal Concordance + Persona Rename + README Positioning

Содержательный апдейт после v0.18.0: добавлены три evidence-based фичи (Health & Metabolism Track, Goal Concordance, Compass Mode уже был в v0.18.0), закрыт технический долг по naming персон, переписано первое впечатление в README, и зафиксирована Drive terminology consistency.

### Added

- **Schema 2.0.1 → 2.2** — два additive bumps:
  - **2.1:** `diagnosis.health_metabolism` блок (opt-in трек метаболического здоровья): sleep/stress/protein/fiber/chewing/caffeine + micro_experiments_log
  - **2.2:** `goal_filter.active_goals[].partner_coordination` optional sub-block (Goal Concordance): communication/cooperation/compatibility/obstacles
- **`references/track_health_metabolism.md`** — новый Tier 3 ref (~2.5K tokens):
  - 7 evidence-based рычагов: Сон (Spiegel 2004), Стресс (Epel 2001, Sominsky 2014), Белок (Leidy 2015), Клетчатка (Wanders 2011), Жевание (Chmiel 2025), Кофеин (Drake 2013), Хлорогеновая кислота (Kanchanasurakit 2023)
  - Диагностические вопросы Track A/B + 3 шаблона рефрейминга самокритики + 3 микро-эксперимента
  - Safety boundary: трек НЕ для расстройств пищевого поведения
- **Phase 1 Health Track opt-in entry** — триггеры «вес/энергия/выгорание/диета/сон» → загрузка Tier 3 ref
- **Phase 3 Health Track Review (optional step 6.5)** — еженедельная оценка sleep/stress/питание
- **Phase 1.5 Partner Coordination Check (step 7)** — opt-in vetting партнёрских целей (Rosta-Filep 2023 + Transactive Goal Dynamics Fitzsimons & Finkel)
- **Phase 2 Partner Discussion Checkpoint** — фиксирует communication в плане при наличии `partner_coordination`
- **emotion_regulation.md** — добавлена Conflict Reappraisal technique (Finkel et al. 2013) + Gottman repair attempts
- **3 новых test файла, 40 тестов:**
  - `test_v019_health_concordance.py` (27 тестов)
  - `test_persona_renames.py` (7 тестов)
  - `test_cross_lingual_consistency.py` (6 тестов)

### Changed

- **Persona modules renamed** (16 файлов affected, 169 cross-ref replacements):
  - `adhd_mode.md` → `mode_adhd.md`
  - `time_structure_unemployed.md` → `mode_unemployed.md`
  - `elder_homebound_mode.md` → `mode_elder.md`
  - `planning_friction_audit.md` → `mode_planning_friction.md`
- **README.md** — first impression rewrite:
  - Новый promise: «Превращает диалог с AI в evidence-based личный план: цели, привычки, ретроспективный ритм»
  - Comparison table: Notion/Todoist vs Generic AI-coach vs Life Planning Coach
  - Quick-start компактнее (3 платформы в 5 строк)
  - Полный список методик (расширенный) — ниже первого экрана
- **SKILL.master.md** — Drive terminology consistency (replaced "Cloud Storage" в prose с "Drive"), persona paths updated, master = 3981 tokens (≤ 4000 budget)
- **Platform builds** — все 4 платформы пересобраны для v0.19.0 (claude/grok/kimi/kimi-cli)
- **`tests/unit/test_v018_gating_state_writes.py`** — `test_schema_version_2_0_1` переведён на semver regex 2.0.1+ (accepts 2.1, 2.2 и далее)
- **`tests/system/test_v140_features.py`** — fixture обновлён для новых persona имён (52 refs)

### Fixed

- Persona module naming наконец-то consistent — все 4 файла начинаются с `mode_`, sort order чёткий.
- README первое впечатление переделано: promise → comparison → quick-start (порядок), методики раскрыты после первого экрана.
- Drive terminology консистентен в SKILL.master.md и `templates/AI_Instructions.md`.
- Phase 1.5 module остался в budget (2478/2500) после добавления Partner Coordination Check — урезание verbose Compass Mode + Authentic Goal Filter секций.

### Tooling

- **Новый скрипт** `scripts/rename_persona_modules.py` — atomic migration для persona renames с dry-run по умолчанию. Self-skip + archive-skip + UTF-8 encoding safety. Шаблон для будущих rename-операций.

### Roadmap progress

✅ Health & Metabolism Track (schema 2.1)
✅ Goal Concordance (schema 2.2)
✅ Persona modules consolidation
✅ Quick wins: README rewrite + Cross-Lingual fixes (Drive terminology)

### Acceptance criteria

- ✅ Schema bumped 2.0.1 → 2.2 (additive, backward compat: 2.0 doc парсится 2.2 клиентом)
- ✅ Health Track file ≤ 2500 tokens (2494)
- ✅ Phase 1/3/1.5/2 интеграция реализована, все модули ≤ 2500 tokens
- ✅ 4 persona переименованы, 0 old-path refs в runtime files (тест-проверено)
- ✅ README первые 30 строк: promise → comparison → quick-start (порядок проверен тестом)
- ✅ SKILL.master.md = 3981 tokens (≤ 4000)
- ✅ 40 новых тестов pass, 0 real test failures
- ✅ Все 4 платформы пересобраны

### Что дальше

- **v1.0.0** — Build pipeline rework (unified Python script, replace bash+rsync hybrid) + platform lazy-loading для Claude.ai (−7K tokens на платформенный файл) + production-ready polish.
