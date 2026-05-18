# Changelog

Все значимые изменения проекта отслеживаются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), проект следует [Semantic Versioning](https://semver.org/lang/ru/).

---

## [Unreleased]

### Added
- **Multi-Platform Skill Adaptation** — скилл адаптирован под три платформы:
  - **Claude.ai** (primary) — ZIP-архив `.skill`, MCP-интеграция, Claude Memory
  - **Grok 4.3** (xAI) — plain `SKILL.md`, sandbox file I/O, session-only persistence, `render_file` для дашборда
  - **Kimi K2.6** (Moonshot AI) — plain `SKILL.md`, `memory_space` tool, `KIMI_REF` для артефактов, OK Computer / Base Chat guidance
  - Архитектура: `SKILL.master.md` (platform-agnostic) + `references/platforms/{claude,grok,kimi}.overlay.yaml` + генератор `scripts/build-platform-skill.py`
  - 42 consistency tests: `tests/system/test_multi_platform.py`
- Системные тесты: консистентность версий, целостность README, синхронизация с GitHub
- Атомарный скрипт релиза: `scripts/release.sh`
- Post-commit hook: предупреждение о незапушенных коммитах
- `VERSION_SOURCES.md` — документация источников версии
- `CHANGELOG.md`, `ROADMAP.md`, `BACKLOG.md` — управление проектом

### Changed
- `scripts/build-skill.sh` теперь собирает артефакты для всех платформ: `.skill` (Claude), `-grok.md`, `-kimi.md`
- `SKILL.md` вычищен от platform-specific терминов, теперь является generated из `SKILL.master.md` + `claude.overlay.yaml`
- `references/templates/CLAUDE_Instructions.md` → `AI_Instructions.md` (platform-agnostic)
- Удалён `pyproject.toml` как дублирующий `setup.py`

### Fixed
- README.md: версия 0.4.0 → 0.6.0, добавлены Stage 1.5 и адаптация стиля
- GitHub Release v0.6.0: переписан на русский язык

### Removed
- Удалена секция `[0.3.0]` — этот релиз никогда не существовал. Все описанные в нём фичи (dashboard, presets, goals, weekly review, WOOP) фактически были выпущены в v0.1.0–v0.2.0. Секция была ошибочно добавлена в CHANGELOG задним числом.

---

## [0.9.2] — 2026-05-18

### Fixed
- **Android Chrome compatibility** — 5 mobile-specific fixes, missed in v0.9.1:
  - `-webkit-tap-highlight-color: transparent` — removes blue tap flash overlay on every touch
  - `overscroll-behavior-y: contain` — prevents pull-to-refresh while scrolling dashboard content
  - `100dvh` with `100vh` fallback — fixes content jumping as Chrome dynamic toolbar shows/hides
  - `<meta name="theme-color">` with light/dark variants — colors Android address bar to match app theme
  - `viewport-fit=cover` — enables edge-to-edge display on notched Android devices
  - JS dynamic sync: `theme-color` updates instantly when user toggles dark/light mode

### Added
- **7 new dashboard tests** for mobile platform compatibility:
  - Android Chrome: tap highlight, overscroll behavior, theme-color, viewport-fit, dvh units
  - iOS Safari: `-webkit-backdrop-filter` regression guard

---

## [0.9.1] — 2026-05-18

### Added
- **Apple-style Dashboard Redesign** — полностью переработанный `life-planning-dashboard.html`
  - Activity Rings (SVG) — 3 кольца прогресса: Баланс, Исполнение, Консистентность
  - Liquid Glass карточки — `backdrop-filter: blur(40px)` с graceful degradation
  - Dark/Light mode toggle — переключение темы с сохранением в `localStorage`
  - macOS-style sidebar + segmented control tabs (Обзор / Ретроспектива / Цели)
  - Confidence Gauges (SVG) — 4 показателя уверенности
  - CSS Grid Heatmap — 365 дней активности без внешних библиотек
  - 12-Week Tracker — бары прогресса по 12 неделям
  - WOOP Cards + BHAG Roadmap + OKR Summary
  - Velocity & Burndown sparklines (SVG)
  - Weekly Priorities с чекбоксами
  - Accessibility: `prefers-reduced-motion`, focus-visible, aria-labels, semantic HTML
  - Mobile-first responsive: breakpoints 375px / 768px / 992px / 1200px+

### Changed
- **Удалены внешние зависимости** — ECharts (~1 MB), Chart.js (~200 KB), Font Awesome (~100 KB) заменены на чистый SVG + CSS
- **Размер файла**: 1,403 KB → ~61 KB (уменьшение в 23×)
- **Шрифты**: системный стек вместо Google Fonts (Inter) — полная offline-совместимость
- **System font stack**: `-apple-system`, `BlinkMacSystemFont`, `SF Pro Display`, `Segoe UI`, Roboto

### Fixed
- `test_contains_expected_chart_keywords` обновлён под новую архитектуру (SVG вместо ECharts/Chart.js)
- `test_doctype_and_html_lang` поддерживает атрибуты в теге `<html>`

---

## [0.9.0] — 2026-05-18

### Added
- **Habit Tracker / Dashboard Streaks** — 4 категории серий привычек (active_habits, digital, sugar, focus) в `life-planning-dashboard.html`
- **Mobile Dashboard (responsive)** — адаптивная вёрстка: шрифты, layout, touch-friendly элементы, отключение горизонтального скролла
- **5-Minute Micro-Sessions** (`references/micro_sessions.md`, 44 строки) — быстрые чек-ины: эмоция → 1 действие ≤30 сек → якорь
- **Quick Decision Protocol** (`references/quick_decision.md`, 45 строк) — 2–3 вопроса для принятия решения «здесь и сейчас» (Values, Feasibility, One Action)
- **Reward Audit (Grayscale Guide)** (`references/reward_audit.md`, 58 строк) — осознанность cheap dopamine
  - Grayscale Experiment: инструкции iOS (Settings → Accessibility → Color Filters) и Android (Settings → Accessibility → Color Correction)
  - Научная база: Holte et al. (2021), Wickord (2023), Myers (2022), NYT (2025), Rada (2005), Avena (2008), Lembke (2021), Kushlev (2025)
  - 4 категории check-in: скролл, сахар, шопинг, игры
  - Opt-in only, без слов «бросай», без термина «dopamine detox»
- Интеграция в `SKILL.md`: 3 новые ссылки в References + hook в Phase 3 (Weekly Review)
- 26 системных тестов на v0.9.0 контент (`tests/system/test_v090_features.py`)

---

## [0.8.0] — 2026-05-18

### Added
- **Habit Loop Framework** (`references/habit_loop.md`, 254 строки) — мост между целями и ежедневными действиями
  - Cue-Routine-Reward (Duhigg, Wood & Neal)
  - Tiny Habits (Fogg): B = MAP, ≤30 секунд, anchor, celebration
  - Habit Stacking (Clear): "После [X], я [Y]"
  - Timeline: median 66 дней (Lally)
  - Integration with WOOP, Calendar, Energy Scheduling, Recovery Protocol, Win Alert
- **Task Breakdown with Checkpoints** (`references/action_breakdown_template.md`, 128 строк) — разбиение WOOP на шаги
  - 5 шагов: finish line → sub-steps → checkpoints → time estimate → first step
  - Checkpoints: verifiable, binary (да/нет)
  - Opt-in: Career/Finances/Health/Home/Learning
- **Markdown Tables as UI** (`references/markdown_tables.md`, 109 строк) — 4 шаблона
  - Weekly Plan, Wheel of Life Review (11 доменов), Progress Check (OKR), Course Correction
  - Stage-appropriate: только Preparation/Action stages
  - Zero tables в SKILL.md
- **Weak Goal Taxonomy + Sanity-Check** (`references/weak_goal_taxonomy.md`, 133 строки)
  - 5 паттернов слабых целей: Vague, Output-as-Outcome, Missing Baseline, Sandbagging, Moonshots
  - Sanity-Check: Coverage, Balance, Feasibility, Measurability, Alignment
  - Integration: расширение `authentic_goal_filter.md` (Stage 1.5)
- **Status Icon System** (`references/status_icons.md`, 61 строка)
  - ⬜🔄✅❌⏸️⚠️ + 🔴🟡🟢 priority
  - Accessibility: текстовый fallback для screen readers
  - Emotional safety: High N users — opt-in, без ❌/⚠️
- Интеграция в `SKILL.md`: 5 новых ссылок + хуки в Phase 1.5, 2, 3, 5
- 34 системных теста на v0.8.0 контент (`tests/system/test_v080_features.py`)

### Changed
- `AGENTS.md` — полная актуализация после v0.7.1 (version, test counts, structure, removed fixed bugs)
- `ROADMAP.md` — v0.8.0 scope сокращён с 12 до 6 фич (realistic minor release)

### Research
- Habit formation: Fogg (Tiny Habits), Clear (Atomic Habits), Wood (context-dependent repetition), Lally (66-day timeline), Duhigg (habit loop)

---

## [0.7.1] — 2026-05-18

### Added
- **Win Alert Protocol** (`references/win_alert.md`) — структурированное празднование побед
  - 5 шагов: WHAT → WHEEL DOMAIN → WHY IT MATTERS → RESOURCES/QUALITIES → NEXT STEP
  - Адаптация под 4 квадранта стиля коммуникации (Nurturing/Challenging/Exploratory/Collaborative)
  - Научная база: savoring (Bryant & Veroff), SDT competence feedback, growth mindset (Dweck)
  - Safety: не trait-based похвала, не пустые комплименты
- **Recovery Protocol MVP** (`references/recovery_protocol.md`) — восстановление после пропусков
  - 3 стратегии по тяжести: LIGHT (Reschedule) → MEDIUM (Catch-up Mini-Session, 15 мин) → HEAVY (Recovery Protocol)
  - Без streak tracking, без shame language, без «нагонять пропущенное»
  - Pattern detection — только conversational, не декларативный
  - Научная база: MI Roll with Resistance, relapse prevention (Marlatt), self-compassion (Neff)
- **Energy-Based Scheduling** (`references/energy_scheduling.md`) — планирование с учётом энергии
  - 3 уровня энергии → маппинг на тип задачи → colorId из COLOR_MAP
  - 1 калибровочный вопрос о пике энергии
  - Связь с AC-8 (Energy Check), Seasonal Planning, True Goal Score
- Интеграция в `SKILL.md`: 3 новые ссылки в References + хуки в Phase 1.5, 3, 5, 9
- 23 системных теста на v0.7.1 контент (`tests/system/test_v071_features.py`)

### Changed
- `ROADMAP.md`: добавлена секция v0.7.1, обновлены v0.8.0/v0.9.0
- `BACKLOG.md`: результаты конкурентного анализа (12 фич, 3 IMPLEMENT → v0.7.1, 9 DEFER → v0.8.0+)

### Research
- `references/competitive_research_2026.md` — анализ 7 конкурентных скиллов + capability mapping

---

## [0.6.0] — 2026-05-16

### Added
- **Stage 1.5: Фильтр аутентичных целей** (`references/authentic_goal_filter.md`)
  - Детектор красных флагов (6+1) с экстернализацией «Чей голос?»
  - Энергетическая проверка (соматический маркер, опционально)
  - Глубокое «Почему» (3 уровня)
  - Тест социального давления (4 вопроса)
  - Истинная оценка цели — радар из 5 осей
  - Портфель целей: Активные / На паузе / Анализ паттернов
- **Адаптация стиля коммуникации** (`references/communication_style.md`)
  - Гибрид Big Five × TTM × MI
  - 4-квадрантная матрица адаптивного коучинга
  - Явный фреймворк OARS
  - 2 вопроса калибровки стиля в Phase 0
- **Обновление колеса жизни**: 8+1 → 11 сфер
  - Семья и Социальная разделены
  - Добавлена сфера «Вклад»
  - «Смысл» стал обязательным
- Тесты v0.6.0: 30 тестов на контент (`tests/release/test_v060_content.py`)

### Changed
- SKILL.md: 4644 слова, добавлен Stage 1.5 между Stage 1 и Stage 2
- Языковые правила: «Ты решаешь» вместо «Давайте решим», запрещены «надо», «должен», «провал»
- Conversation State JSON: добавлены `goal_filter`, `goal_portfolio`

---

## [0.5.0] — 2026-05-16

### Added
- **Two-Track Diagnostic Architecture**
  - Track A — Quick Diagnostic (20–30 мин, 1 сессия)
  - Track B — Deep Diagnostic (65–105 мин, 2–4 сессии)
- **Values Clarification**: pairwise 45 пар → Top-5 → Top-3 (10 вопросов)
- **Ikigai**: аутентичный фреймворк Ken Mogi (5 Pillars)
- **Life Story**: опциональный блок + Lite версия (3 вопроса)
- **Readiness Gate**: проверка комфорта после каждой фазы
- **Workview/Lifeview**: микро-формат (3 вопроса)

### Changed
- Полная реструктуризация Stage 1 (Diagnostic)

---

## [0.4.0] — 2026-05-16

### Added
- **Двухуровневая система персистентности**
  - Уровень 1: Claude Memory (работает сразу)
  - Уровень 2: Google Drive + персональная wiki (opt-in)
- **Структура персональной wiki** на Google Drive
- **Автоматическое создание** Progress Dashboard, README wiki, Index
- **Graceful degradation**: при недоступности Drive — мягкий переход в режим памяти

---

## [0.2.0] — 2026-05-14

### Added
- Интеграция с Google Calendar MCP
- OAuth 2.0 через claude.ai
- CRUD Events, Free/Busy Slots
- Calendar Presets: Weekly Review, WOOP, Milestones, Time Blocks

### Removed
- Кастомный Python-пакет `calendar_integration/` (заменён на MCP)

---

## [0.1.0] — 2026-05-13

### Added
- Базовый скилл life-planning-coach для Claude.ai
- Stage 1: Diagnostic (Wheel of Life 8+1, Values Clarification Schwartz)
- Stage 2: Goal Architecture (BHAG, OKR, WOOP)
- Stage 3: Weekly Review
- Stage 4: Dashboard
- Stage 5: Google Calendar интеграция (Python API)
- Emotional Landing Protocol
- Evidence-based методики с эффект-сайзами

---

[Unreleased]: https://github.com/azagreev/life-planning-coach/compare/v0.6.1...HEAD
[0.6.1]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.6.1
[0.6.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.6.0
[0.5.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.5.0
[0.4.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.4.0
[0.2.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.2.0
[0.1.0]: https://github.com/azagreev/life-planning-coach/compare/v0.2.0...v0.1.0
