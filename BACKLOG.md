# Backlog

> **Для кого:** Внутреннее планирование, идеи без привязки к конкретной версии.
> **Принцип:** Каждая идея имеет триггер — условие, при котором она переходит в ROADMAP.
> **Баги:** Активные баги — в [BUGS.md](BUGS.md).
> **Язык:** Названия идей — на русском. Английские термины допустимы только в скобках для общепринятых понятий (API, MCP, HTML).

---

## Фичи

### Эмоциональная регуляция
- **Описание:** Инструменты для управления эмоциями на пути к целям (cognitive reappraisal, self-compassion, grounding)
- **Триггер:** Востребовано 3+ пользователями или включено в ROADMAP v0.7.0
- **Статус:** ✅ Реализовано в v0.7.0
- **Источник:** Анализ паттернов в Authentic Goal Filter (энергия как ось радара)

### Интеграция привычек (Habit Loop)
- **Статус:** ✅ Реализовано в v0.8.0 (`references/habit_loop.md`, 254 строки)
- **Описание:** Мост между целями и ежедневными привычками (Tiny Habits, Habit Stacking)
- **Триггер:** Востребовано 3+ пользователями или включено в ROADMAP v0.8.0
- **Статус:** 📋 В ROADMAP v0.8.0
- **Источник:** Литература: Fogg (2019), Clear (2018)

### Интеграция с Google Tasks MCP
- **Описание:** Синхронизация Daily Top-3 с Google Tasks через официальный MCP
- **Триггер:** Google Tasks API станет доступен через MCP в claude.ai
- **Статус:** ⏳ Ожидание внешнего события
- **Источник:** Техническое ограничение v0.2.0 (MCP не поддерживает Tasks)


### Микросессии 5 минут
- **Описание:** Быстрые чек-ины для режима нехватки времени: эмоция → 1 действие. ≤100 строк, opt-in через фразу пользователя "у меня 5 минут". Интеграция с Habit Loop (Tiny Habits: <30 сек).
- **Триггер:** v0.9.0 мобильная адаптация
- **Статус:** 📋 В ROADMAP v0.9.0
- **Источник:** Borrowed from Developmental Coach + Tiny Habits (Fogg)

### Протокол быстрых решений
- **Описание:** 2–3 вопроса для принятия решения «здесь и сейчас». Адаптируется под Communication Style quadrant (High A = больше контекста, High N = больше безопасности).
- **Триггер:** v0.9.0 мобильная адаптация
- **Статус:** 📋 В ROADMAP v0.9.0
- **Источник:** Borrowed from PM Decision Frameworks

### Мобильный дашборд
- **Описание:** Адаптивная версия `life-planning-dashboard.html`: 11 сфер Wheel of Life + Habit streaks + offline-ready. Требует: streak data model inline в HTML + mobile CSS. BUG-001 (8→11) уже исправлен.
- **Триггер:** v0.9.0
- **Статус:** 📋 В ROADMAP v0.9.0 (P0)
- **Источник:** Техдолг BUG-001 + Habit Loop Framework

### Групповой коучинг
- **Описание:** Парный или групповой коучинг (2+ человека + скилл)
- **Триггер:** 5+ пользователей запросят
- **Статус:** 💡 Идея
- **Источник:** Потенциальный enterprise use-case

### Интеграция Fitness API
- **Описание:** Подключение Apple Health / Google Fit для отслеживания энергии и здоровья
- **Триггер:** Расширение сферы «Здоровье» в Wheel of Life до quantitative метрик
- **Статус:** 💡 Идея
- **Источник:** Расширение Wheel of Life

### Мультиязычность
- **Описание:** Поддержка английского языка (EN/RU toggle)
- **Триггер:** 10+ запросов от англоязычных пользователей
- **Статус:** 💡 Идея
- **Источник:** Потенциал международного open source

### Ревизия текстов событий календаря
- **Описание:** Полный ревизия всех событий календаря: названия (summary), описания (description), тексты напоминаний. Сделать их более мотивирующими, персонализированными и aligned с коучинговым тоном скилла. Проверить на отсутствие «надо/должен» в текстах событий.
- **Триггер:** Перед v0.7.0 или при первой жалобе пользователя на «роботизированные» напоминания
- **Статус:** ✅ Реализовано (`tests/system/test_calendar_tone.py`)
- **Источник:** Пользовательская обратная связь, UX-калибровка

### Аудит наград (Бюджет дофамина)
- **Описание:** Модуль для логирования источников «дешёвого дофамина» (сахар, скролл соцсетей, Shorts, игры) и корреляции их с completion rate целей. Dopamine Load Score (0–10), weekly insights, интеграция в planning flow. Фрейминг: «Reward Management для достижения целей», не guilt-trip.
- **Триггер:** Решение автора проекта — killer feature, без pilot/проверки
- **Статус:** ✅ Реализовано в v0.9.0 (`references/reward_audit.md`, 58 строк)
- **Источник:** Научный ресёрч (Rada 2005, Avena 2008, Lembke 2021, Kushlev 2025) + конкурентный анализ (Elqi, Opal, BePresent)
- **Артефакт:** `references/reward_audit.md` (≤120 строк) + hook в SKILL.md (≤3 строки)

---

## Техдолг

| Задача | Приоритет | Триггер | Примечание |
|--------|-----------|---------|------------|
| CI/CD через GitHub Actions | P1 | Перед v0.7.0 | ✅ Исправлено — `.github/workflows/release-checks.yml` |
| Coverage report | P2 | Когда >100 тестов | pytest-cov + badge (376 тестов — пора) |
| Pre-commit hooks (ruff, mypy) | P2 | Перед v0.7.0 | Качество кода |
| ~~Фикс зависших тестов~~ | ~~P1~~ | ~~Сразу~~ | ✅ Исправлено в v0.7.0 |
| Удалить `.build/` из истории | P3 | При чистке репозитория | ✅ Исправлено — `.build/` в `.gitignore` |
| Архивировать старые планы в `references/archive/` | P3 | При накоплении 5+ планов | ✅ Исправлено — все plan_v*.md в archive |

---

### Tech Debt: Зависшие тесты после v0.6.1 cleanup
- **Статус:** ✅ Исправлено в v0.7.0 (коммит f7ca685)
- **Источник:** Аудит тестов после build cleanup (v0.6.1+)

## Исследования

| Тема | Статус | Когда нужно | Источник |
|------|--------|-------------|----------|
| Emotional Regulation эффект-сайзы | ✅ Готово | v0.7.0 | Gross (d=0.45), Neff (r=0.47) — см. `references/emotion_regulation.md` |
| Habit formation литература | 🔍 Не начато | Перед v0.8.0 | Fogg, Clear, Wood |
| Mobile UX для AI-коучинга | 🔍 Не начато | Перед v0.9.0 | Исследования Anthropic |
| Russian NLP для coaching | 🔍 Не начато | При мультиязычности | Тонкости перевода метафор |

---

## Как работать с бэклогом

1. **Добавление:** Создать PR с описанием идеи или запись в этом файле
2. **Продвижение в ROADMAP:** Когда сработал триггер — перенести в `ROADMAP.md` с конкретной версией
3. **Архивация:** Если идея устарела — пометить `[ARCHIVED]` с датой и причиной

---

## Связь с другими документами

- **ROADMAP.md** — идеи с триггером → конкретные версии
- **CHANGELOG.md** — факты о выпущенных версиях
- **BUGS.md** — активные баги и известные проблемы
- **references/plan_vX.Y.Z.md** — детальное планирование конкретного релиза
- **references/release_checklist_vX.Y.Z.md** — чеклист перед выпуском

### Переделка дашборда (Self-Contained)
- **Описание:** Полный пересмотр life-planning-dashboard.html: визуальный дизайн, информационная архитектура, наполнение. Цель — сделать дашборд полностью самодостаточным standalone HTML-файлом без внешних зависимостей (CDN, внешние скрипты, внешние стили). Все данные — inline или встроенные в файл. Дашборд должен открываться и работать локально в браузере без интернета.
- **Триггер:** Перед v0.7.0 или при накоплении 3+ жалоб на UX дашборда
- **Статус:** ✅ Реализовано в v0.9.1 — external dependencies removed (ECharts, Chart.js, Font Awesome), inline SVG/Canvas, dark/light mode, PDF export, offline-ready.
- **Источник:** Технический долг + UX-улучшение
- **Детали:**
  - Убрать зависимость от Font Awesome CDN → inline SVG иконки
  - Убрать зависимость от Google Fonts → system fonts или inline @font-face
  - Убрать зависимость от Chart.js/Plotly CDN → inline Canvas/SVG графики
  - Убрать зависимость от Tailwind CDN → inline CSS
  - Все стили — в `<style>` внутри файла
  - Все скрипты — в `<script>` внутри файла
  - Все данные (WHEEL_SPHERES, EXECUTION_SCORES) — встроены в JS
  - Размер целевой: <500 KB в одном файле
  - Работает offline (file:// protocol)
  - Мобильная адаптивность как first-class citizen
  - Dark/light mode toggle
  - Печать/PDF экспорт одной кнопкой

### Регулярность планирования в календаре — Habit Formation
- **Описание:** Подумать как лучше предложить пользователю регулярность планирования в календаре, особенно недельных сессий (Weekly Review). Ключевая идея: одноразовое создание события недостаточно — нужно формировать привычку через повторение, якоря и микро-шаги.
- **Возможные подходы:**
  1. **Recurring events** — автоматическое создание повторяющихся событий (каждое воскресенье 19:00 Weekly Review)
  2. **Habit anchoring** — привязка к существующей рутине ("после утреннего кофе — 5-минутный check-in")
  3. **Micro-commitments** — начинать с 1 события в неделю, постепенно наращивать
  4. **Social accountability** — опциональное напоминание другу/партнёру
  5. **Streak tracking** — визуализация цепочки выполненных сессий в дашборде
- **Триггер:** v0.9.0 (Mobile Dashboard + Habit Tracker)
- **Статус:** ✅ Реализовано — SUPERSEDED by `references/habit_stack_builder.md` (v0.12.0) + `references/calendar_integration.md` RRULE_PRESETS
- **Источник:** BJ Fogg (Tiny Habits), James Clear (Atomic Habits), Milkman et al. (2021)
### Протокол восстановления после пропуска
- **Описание:** Пропуск Weekly Review (или любой регулярной сессии) — нормально. Но важно иметь чёткий протокол восстановления, чтобы один пропуск не превратился в полный срыв.
- **Варианты поведения при пропуске:**
  1. **Reschedule** — перенести на ближайшее удобное время (не откладывать на "потом", а конкретно: "среда 20:00")
  2. **Catch-up Mini-Session** — ускоренная версия: 15 минут вместо 2 часов. Только 3 вопроса: (1) что было главное на прошлой неделе? (2) что не получилось и почему? (3) один приоритет на эту неделю?
  3. **Skip with Reflection** — не просто пропустить, а записать причину: "пропустил из-за командировки" → данные для анализа паттернов пропусков. Если причина повторяется 3+ раза — это сигнал к изменению расписания или формата сессии.
  5. **Recovery Protocol (2+ пропуска подряд)** — если пропущено 2 и более сессий:
     - Не нагонять всё сразу
     - Начать с Emotional Landing (5 мин) → быстрый Wheel of Life (5 мин) → один приоритет
     - Пересмотреть формат: может, 2 часа — слишком долго? Попробовать 30-минутную версию?
     - Проверить alignment: а актуальны ли ещё цели? Может, пропуски — сигнал, что цели не мои?
- **Триггер:** Вместе с регулярностью (v0.7.0+) или при жалобе "я постоянно пропускаю Weekly Review"
- **Статус:** ✅ Реализовано в v0.7.1 (`references/recovery_protocol.md`, 132 строки)
- **Источник:** Motivational Interviewing (Roll with Resistance), behavioral relapse prevention
- **Дебат:** Advocate/Critic 3 цикла → **IMPLEMENT (MVP)** (conf 7/10). Stack with Next удалён (анти-паттерн). Pattern detection — conversational-only.

### Протокол празднования побед
- **Описание:** Структурированное празднование побед: что достигнуто → домен Wheel of Life → почему важно → ресурсы/качества пользователя → следующий шаг. Адаптируется под Communication Style quadrant. НЕ применяется во время кризиса/Emotional Landing.
- **Триггер:** Пользователь сообщает о достижении или проходит Weekly Review
- **Статус:** ✅ Реализовано в v0.7.1 (`references/win_alert.md`, 112 строк)
- **Источник:** Borrowed from GTD Coach Plugin
- **Дебат:** Advocate/Critic 3 цикла → **IMPLEMENT** (conf 7/10). Научная база: savoring (Bryant & Veroff), SDT competence feedback (Deci & Ryan), VIA character strengths.

### Планирование с учётом энергии
- **Описание:** При создании событий в календаре учитывать энергию пользователя: высокая энергия → творческая/Deep Work блоки, низкая энергия → рутина/админ, пиковые часы → защитить фокус-блоками. Связь с AC-8 (Energy Check) и Seasonal Planning.
- **Триггер:** Пользователь работает с календарём (Phase 5)
- **Статус:** ✅ Реализовано в v0.7.1 (`references/energy_scheduling.md`, 64 строки)
- **Источник:** Borrowed from Weekly Planning approach (popular r/ClaudeAI pattern 2026)
- **Дебат:** Advocate/Critic 3 цикла → **IMPLEMENT** (conf 7/10). Ограничение: ≤80 строк, новый файл `references/energy_scheduling.md`, НЕ append в `calendar_constants.md`.

### Markdown-таблицы как UI
- **Описание:** Использовать markdown-таблицы для Weekly Plan, Wheel of Life Review, Progress Check, Course Correction. Stage-appropriate: только Preparation/Action stages.
- **Триггер:** v0.8.0 Execution Layer
- **Статус:** ✅ Реализовано в v0.8.0 (`references/markdown_tables.md`, 109 строк)
- **Источник:** Borrowed from GTD Coach Plugin + PM OKR Skill
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 8/10). Ждёт: dashboard 8→11 fix, MI-compliance review, zero tables в SKILL.md.

### Система статусных иконок
- **Описание:** Единая визуальная нотация: ⬜ Todo, 🔄 In Progress, ✅ Completed, ❌ Cancelled, ⏸️ Paused, ⚠️ At Risk. Accessibility fallback + High N safety.
- **Триггер:** v0.8.0 Execution Layer
- **Статус:** ✅ Реализовано в v0.8.0 (`references/status_icons.md`, 61 строка)
- **Источник:** Borrowed from GTD Coach Plugin
- **Дебат:** Advocate/Critic 3 цикла → **IMPLEMENT** (conf 7/10). Риски: accessibility, emotional harm для High N, screen readers.

### Автотриггеры ревью
- **Описание:** 7+ дней → Weekly Pulse, новый месяц → Monthly Scan, новый квартал → Quarterly Reflection. Permission-based offer, не mandatory prompt.
- **Триггер:** v0.9.0+
- **Статус:** 📋 В ROADMAP v0.9.0+
- **Источник:** Borrowed from GTD Coach Plugin
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Требует structured session metadata first.

### Адаптивная длина ответов
- **Описание:** Три режима: Clarification (2-3 предложения), Exploration (4-6), Crystallization (полный протокол). Интеграция с Communication Style quadrant.
- **Триггер:** v0.9.0+
- **Статус:** 📋 В ROADMAP v0.9.0+
- **Источник:** Borrowed from Developmental Coach
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Требует спецификации интеграции с Deep Why, Energy Check, Attachment Style.

### Таксономия слабых целей + Sanity-Check
- **Описание:** Паттерны слабых целей: Vague, Output-as-Outcome, Missing Baseline, Sandbagging, Moonshots. Sanity-Check: Coverage, Balance, Feasibility, Measurability, Alignment.
- **Триггер:** v0.7.1 (lightweight pilot, 5 yes/no questions) / v0.8.0 (full taxonomy)
- **Статус:** ✅ Реализовано в v0.8.0 (`references/weak_goal_taxonomy.md`, 133 строки)
- **Источник:** Borrowed from PM OKR Skill
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Пилот возможен в v0.7.1, full — в v0.8.0.

### Разбиение задач с чекпоинтами
- **Описание:** Разбиение действий WOOP на шаги с чекпоинтами (✓ Чекпоинт: [критерий выполнения]). Opt-in, только для Career/Finances/Health/Home/Learning.
- **Триггер:** v0.8.0
- **Статус:** ✅ Реализовано в v0.8.0 (`references/action_breakdown_template.md`, 128 строк)
- **Источник:** Borrowed from GTD Coach Plugin
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 8/10). Требует валидации потребности через GitHub Discussion.

### Структурированный отчёт о росте
- **Описание:** Шаблон периодического обзора: Summary → Prioritized Growth Areas (Why + Evidence + Recommendation) → Observed Strengths → Actions → Recommended Resources.
- **Триггер:** v0.9.0+
- **Статус:** 📋 В ROADMAP v0.9.0+
- **Источник:** Borrowed from Composio developer-growth-analysis
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Требует re-assessment flow для Wheel of Life.

### Сначала уточняющие вопросы
- **Описание:** Перед глубоким протоколом — 2–3 уточняющих вопроса (домен, опыт, формат). Интеграция с Checkpoint-and-Resume.
- **Триггер:** v0.8.0
- **Статус:** 📋 В ROADMAP v0.8.0
- **Источник:** Borrowed from Composio file-organizer skill
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Пересекается с Phase 0 calibration, Track A/B, Readiness Gate. Решение: `references/session_recalibration.md`, ≤2 строки в SKILL.md.

### Единые Release Notes из CHANGELOG
- **Статус:** ✅ Реализовано — `scripts/extract-release-notes.py` генерирует из CHANGELOG.md, `scripts/release.sh` использует `--notes-file`

---

## R&D: Token Optimization Audit

> **RICE:** Reach 100% × Impact 1.5 × Confidence 40% / Effort 10 дней = **6.0** (Medium Priority)
> **Статус:** 🔬 Research (запланировано, не начато)
> **Триггер:** Перед v0.13.0 или когда пользователь жалуется на скорость/стоимость

### Проблема

- Русский язык ~1.5-2x токенов на символ vs английский
- Reference-файлы большие (habit_stack_builder.md = 115 lines)
- Каждая сессия загружает весь контекст skill + references
- Пользователь платит за токены (или ждёт дольше)

### Гипотезы для исследования

| # | Гипотеза | Как проверить |
|---|----------|---------------|
| 1 | Английские термины в русском тексте увеличивают token count из-за непоследовательной токенизации | Сравнить token count "Peak-Trough-Rebound" vs "Пик-Спад-Возврат" |
| 2 | Progressive disclosure через `references/` работает неэффективно — модель загружает всё | Замерить: сколько токенов уходит на "прочитать reference" vs "ответ из памяти" |
| 3 | Few-shot examples в SKILL.md можно сжать без потери качества | A/B: полные examples vs compressed summaries |
| 4 | Структурированные списки vs проза — разница в токенах | Замерить таблицы vs параграфы |
| 5 | Дублирование контента между SKILL.md и references/ | Найти overlap, сжать |
| 6 | YAML frontmatter на английском + instructions на русском = лишние токены на code-switching | Сравнить monolingual vs bilingual prompt token count |

### Методология

```
1. Baseline: Замерить токены на типичную сессию (prompt + completion)
2. Variation: Изменить один параметр (язык, структура, compression)
3. Measure: Токены + качество ответа (human evaluation 1-5)
4. Iterate: Лучший вариант → новый baseline
```

### Quick Wins (ожидаемые)

- [ ] Найти и удалить дублирование между SKILL.md и references/
- [ ] Сжать длинные таблицы в компактные списки
- [ ] Заменить английские термины на русские где возможно без потери clarity
- [ ] Оценить эффект от YAML frontmatter compression

### Deliverables

- `references/research/token_audit_report.md` — findings + recommendations
- PR с оптимизациями (если найдены значимые savings)
- Обновление AGENTS.md — guidelines для token-efficient writing

---

## Localization: Cross-Lingual Consistency

> **RICE:** Reach 100% × Impact 1.0 × Confidence 70% / Effort 2 дня = **35.0** (Quick Win)
> **Статус:** 🔍 Идентифицирована проблема, решение в процессе
> **Триггер:** Обнаружена пользователем 2026-05-20

### Проблема

- `README.md` + структура — английский
- `SKILL.md` frontmatter (`name`, `version`, `description`) — английский
- `SKILL.md` instructions + `references/` — русский
- Mixed context может вызывать cross-lingual галлюцинации у Kimi и других моделей

### Уже сделано

- [x] Исправлено: "Яворонок" → "Жаворонок" (10 вхождений, 6 файлов)

### TODO

- [ ] Зафиксировать языковую политику в `AGENTS.md`
- [ ] Протестировать cross-lingual retrieval accuracy (5 тестов)
- [ ] Оценить, нужно ли перевести README.md на русский или наоборот — унифицировать
- [ ] Проверить platform-файлы (Grok/Kimi) на code-switching артефакты
