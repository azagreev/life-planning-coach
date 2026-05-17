# Backlog

> **Для кого:** Внутреннее планирование, идеи без привязки к конкретной версии.
> **Принцип:** Каждая идея имеет триггер — условие, при котором она переходит в ROADMAP.
> **Баги:** Активные баги — в [BUGS.md](BUGS.md).

---

## Фичи

### Эмоциональная регуляция
- **Описание:** Инструменты для управления эмоциями на пути к целям (cognitive reappraisal, self-compassion, grounding)
- **Триггер:** Востребовано 3+ пользователями или включено в ROADMAP v0.7.0
- **Статус:** ✅ Реализовано в v0.7.0
- **Источник:** Анализ паттернов в Authentic Goal Filter (энергия как ось радара)

### Habit Loop Integration
- **Статус:** ✅ Реализовано в v0.8.0 (`references/habit_loop.md`, 254 строки)
- **Описание:** Мост между целями и ежедневными привычками (Tiny Habits, Habit Stacking)
- **Триггер:** Востребовано 3+ пользователями или включено в ROADMAP v0.8.0
- **Статус:** 📋 В ROADMAP v0.8.0
- **Источник:** Литература: Fogg (2019), Clear (2018)

### Google Tasks MCP Integration
- **Описание:** Синхронизация Daily Top-3 с Google Tasks через официальный MCP
- **Триггер:** Google Tasks API станет доступен через MCP в claude.ai
- **Статус:** ⏳ Ожидание внешнего события
- **Источник:** Техническое ограничение v0.2.0 (MCP не поддерживает Tasks)

### Voice-Optimized Output
- **Описание:** Ответы скилла, удобные для голосового чтения на мобильных
- **Триггер:** 50%+ сессий на мобильных устройствах или запрос 3+ пользователей
- **Статус:** 📋 В ROADMAP v0.9.1+ (отложено из v0.9.0)
- **Источник:** Пользовательский опыт (мобильное использование)

### 5-Minute Micro-Sessions
- **Описание:** Быстрые чек-ины для режима нехватки времени: эмоция → 1 действие. ≤100 строк, opt-in через фразу пользователя "у меня 5 минут". Интеграция с Habit Loop (Tiny Habits: <30 сек).
- **Триггер:** v0.9.0 мобильная адаптация
- **Статус:** 📋 В ROADMAP v0.9.0
- **Источник:** Borrowed from Developmental Coach + Tiny Habits (Fogg)

### Quick Decision Protocol
- **Описание:** 2–3 вопроса для принятия решения «здесь и сейчас». Адаптируется под Communication Style quadrant (High A = больше контекста, High N = больше безопасности).
- **Триггер:** v0.9.0 мобильная адаптация
- **Статус:** 📋 В ROADMAP v0.9.0
- **Источник:** Borrowed from PM Decision Frameworks

### Mobile Dashboard
- **Описание:** Адаптивная версия `life-planning-dashboard.html`: 11 сфер Wheel of Life + Habit streaks + offline-ready. Требует: streak data model inline в HTML + mobile CSS. BUG-001 (8→11) уже исправлен.
- **Триггер:** v0.9.0
- **Статус:** 📋 В ROADMAP v0.9.0 (P0)
- **Источник:** Техдолг BUG-001 + Habit Loop Framework

### Group Coaching Mode
- **Описание:** Парный или групповой коучинг (2+ человека + скилл)
- **Триггер:** 5+ пользователей запросят
- **Статус:** 💡 Идея
- **Источник:** Потенциальный enterprise use-case

### Fitness API Integration
- **Описание:** Подключение Apple Health / Google Fit для отслеживания энергии и здоровья
- **Триггер:** Расширение сферы «Здоровье» в Wheel of Life до quantitative метрик
- **Статус:** 💡 Идея
- **Источник:** Расширение Wheel of Life

### Multilingual Support
- **Описание:** Поддержка английского языка (EN/RU toggle)
- **Триггер:** 10+ запросов от англоязычных пользователей
- **Статус:** 💡 Идея
- **Источник:** Потенциал международного open source

### Calendar Event Copy Review
- **Описание:** Полный ревизия всех событий календаря: названия (summary), описания (description), тексты напоминаний. Сделать их более мотивирующими, персонализированными и aligned с коучинговым тоном скилла. Проверить на отсутствие «надо/должен» в текстах событий.
- **Триггер:** Перед v0.7.0 или при первой жалобе пользователя на «роботизированные» напоминания
- **Статус:** 📋 В ROADMAP v0.8.0
- **Источник:** Пользовательская обратная связь, UX-калибровка
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 8/10). Причина: scope ambiguity (generic warm vs dynamic personalized), требуется v0.8.0 habit integration для holistic design.

### Reward Audit (Бюджет Дофамина / Cheap Dopamine Tracker)
- **Описание:** Модуль для логирования источников «дешёвого дофамина» (сахар, скролл соцсетей, Shorts, игры) и корреляции их с completion rate целей. Dopamine Load Score (0–10), weekly insights, интеграция в planning flow. Фрейминг: «Reward Management для достижения целей», не guilt-trip.
- **Триггер:** Решение автора проекта — killer feature, без pilot/проверки
- **Статус:** 🎯 **Решение принято: IMPLEMENT** (авторский override после Advocate/Critic дебата)
- **Источник:** Научный ресёрч (Rada 2005, Avena 2008, Lembke 2021, Kushlev 2025) + конкурентный анализ (Elqi, Opal, BePresent)
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 6/10). **Авторский override:** реализовать без пилота, как killer feature.
- **Scope для скилла (после анализа PRD v7.0):**
  - **Главное:** Grayscale Guide — one-time recommendation с инструкцией (iOS/Android) + научный backing (Holte –37.9 min, NYT –40%). Zero tracking.
  - **Дополнительно:** Conversational check-in (4 категории cheap dopamine) + qualitative insight.
  - **Не делаем:** Dopamine Load Score, графики, Screen Time API, Libre, MCP, геймификация.
  - **Артефакт:** `references/reward_audit.md` (≤120 строк) + hook в SKILL.md (≤3 строки).
- **Полный PRD:** [`references/research/prd_reward_audit.md`](references/research/prd_reward_audit.md)
- **Анализ PRD:** [`references/research/prd_reward_audit_analysis.md`](references/research/prd_reward_audit_analysis.md) — разбор каждого раздела PRD v7.0: что берём, что откладываем

---

## Техдолг

| Задача | Приоритет | Триггер | Примечание |
|--------|-----------|---------|------------|
| CI/CD через GitHub Actions | P1 | Перед v0.7.0 | Автоматический запуск тестов при PR |
| Coverage report | P2 | Когда >100 тестов | pytest-cov + badge |
| Pre-commit hooks (ruff, mypy) | P2 | Перед v0.7.0 | Качество кода |
| ~~Фикс зависших тестов~~ | ~~P1~~ | ~~Сразу~~ | ✅ Исправлено в v0.7.0 |
| Удалить `.build/` из истории | P3 | При чистке репозитория | Сейчас `.build/` не в `.gitignore` |
| Архивировать старые планы в `references/archive/` | P3 | При накоплении 5+ планов | Упорядочить references |

---

### Tech Debt: Зависшие тесты после v0.6.1 cleanup
- **Описание:** После изменений в build-skill.sh (убраны dev-only файлы из ZIP, версия в имени файла) и релизном процессе (tag-only titles) 3 теста устарели или стали неполными.
- **Проблемы:**
  1. **`tests/release/test_metadata.py::test_skill_archive_structure`** — УСТАРЕЛ
     - Ищет `life-planning-coach.zip` в корне (старое имя), а сейчас `dist/life-planning-coach-v0.6.1.zip`
     - Требует внутри ZIP: README.md, LICENSE, CONTRIBUTING.md, SECURITY.md — мы их удрали из скилла
     - **Результат:** Всегда `skipTest("not built yet")` — тест никогда не проверяет реальную структуру
     - **Фикс:** Обновить путь на `dist/life-planning-coach-v*.zip`, убрать dev-файлы из `required`, добавить проверку `references/templates/`
  2. **`tests/unit/test_dashboard.py`** — НЕПОЛНЫЙ (не ловит BUG-001)
     - Проверяет размер, CDN, doctype, ключевые слова чартов
     - **Не проверяет:** количество доменов Wheel of Life (8 vs 11)
     - Дашборд явно делит сумму на 8: `(reduce(...) / 8).toFixed(1)`
     - **Фикс:** Добавить `test_wheel_has_11_domains` — проверить что `WHEEL_SPHERES.length === 11` и что присутствуют: Здоровье, Карьера, Финансы, Романтика, Семья, Социальная, Вклад, Смысл, Рост, Развлечения, Среда
  3. **`tests/system/test_version_consistency.py::test_github_release_exists_for_tag`** — ХРУПКИЙ
     - Проверяет что для `git describe --tags --abbrev=0` есть GitHub Release
     - После cleanup: v0.2.0 — только тег, без релиза (мы удалили дубль)
     - Если checkout на v0.2.0 и запуск тестов → `gh release view v0.2.0` вернёт ошибку
     - **Фикс:** Добавить whitelist тегов без релиза (`v0.2.0`) или проверять `git tag -l` отдельно от `git describe`
- **Триггер:** Перед v0.7.0 или при первом же падении тестов на checkout к старому тегу
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

### Dashboard Redesign — Self-Contained & Dependency-Free
- **Описание:** Полный пересмотр life-planning-dashboard.html: визуальный дизайн, информационная архитектура, наполнение. Цель — сделать дашборд полностью самодостаточным standalone HTML-файлом без внешних зависимостей (CDN, внешние скрипты, внешние стили). Все данные — inline или встроенные в файл. Дашборд должен открываться и работать локально в браузере без интернета.
- **Триггер:** Перед v0.7.0 или при накоплении 3+ жалоб на UX дашборда
- **Статус:** 🔄 Частично выполнено — ECharts и Font Awesome уже inline, Google Fonts не используются. Осталось: мобильная адаптивность, dark/light mode, PDF экспорт.
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
- **Статус:** 📋 В ROADMAP v0.9.0 (через Habit Tracker / Dashboard Streaks)
- **Источник:** BJ Fogg (Tiny Habits), James Clear (Atomic Habits), Milkman et al. (2021) — planning fallacy + implementation intentions
### Recovery Protocol — что делать если пропустил сессию
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

### Win Alert Protocol
- **Описание:** Структурированное празднование побед: что достигнуто → домен Wheel of Life → почему важно → ресурсы/качества пользователя → следующий шаг. Адаптируется под Communication Style quadrant. НЕ применяется во время кризиса/Emotional Landing.
- **Триггер:** Пользователь сообщает о достижении или проходит Weekly Review
- **Статус:** ✅ Реализовано в v0.7.1 (`references/win_alert.md`, 112 строк)
- **Источник:** Borrowed from GTD Coach Plugin
- **Дебат:** Advocate/Critic 3 цикла → **IMPLEMENT** (conf 7/10). Научная база: savoring (Bryant & Veroff), SDT competence feedback (Deci & Ryan), VIA character strengths.

### Energy-Based Scheduling
- **Описание:** При создании событий в календаре учитывать энергию пользователя: высокая энергия → творческая/Deep Work блоки, низкая энергия → рутина/админ, пиковые часы → защитить фокус-блоками. Связь с AC-8 (Energy Check) и Seasonal Planning.
- **Триггер:** Пользователь работает с календарём (Phase 5)
- **Статус:** ✅ Реализовано в v0.7.1 (`references/energy_scheduling.md`, 64 строки)
- **Источник:** Borrowed from Weekly Planning approach (popular r/ClaudeAI pattern 2026)
- **Дебат:** Advocate/Critic 3 цикла → **IMPLEMENT** (conf 7/10). Ограничение: ≤80 строк, новый файл `references/energy_scheduling.md`, НЕ append в `calendar_constants.md`.

### Markdown Tables as Structured UI
- **Описание:** Использовать markdown-таблицы для Weekly Plan, Wheel of Life Review, Progress Check, Course Correction. Stage-appropriate: только Preparation/Action stages.
- **Триггер:** v0.8.0 Execution Layer
- **Статус:** ✅ Реализовано в v0.8.0 (`references/markdown_tables.md`, 109 строк)
- **Источник:** Borrowed from GTD Coach Plugin + PM OKR Skill
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 8/10). Ждёт: dashboard 8→11 fix, MI-compliance review, zero tables в SKILL.md.

### Status Icon System
- **Описание:** Единая визуальная нотация: ⬜ Todo, 🔄 In Progress, ✅ Completed, ❌ Cancelled, ⏸️ Paused, ⚠️ At Risk. Accessibility fallback + High N safety.
- **Триггер:** v0.8.0 Execution Layer
- **Статус:** ✅ Реализовано в v0.8.0 (`references/status_icons.md`, 61 строка)
- **Источник:** Borrowed from GTD Coach Plugin
- **Дебат:** Advocate/Critic 3 цикла → **IMPLEMENT** (conf 7/10). Риски: accessibility, emotional harm для High N, screen readers.

### Auto-Review Triggers
- **Описание:** 7+ дней → Weekly Pulse, новый месяц → Monthly Scan, новый квартал → Quarterly Reflection. Permission-based offer, не mandatory prompt.
- **Триггер:** v0.9.0+
- **Статус:** 📋 В ROADMAP v0.9.0+
- **Источник:** Borrowed from GTD Coach Plugin
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Требует structured session metadata first.

### Adaptive Response Length
- **Описание:** Три режима: Clarification (2-3 предложения), Exploration (4-6), Crystallization (полный протокол). Интеграция с Communication Style quadrant.
- **Триггер:** v0.9.0+
- **Статус:** 📋 В ROADMAP v0.9.0+
- **Источник:** Borrowed from Developmental Coach
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Требует спецификации интеграции с Deep Why, Energy Check, Attachment Style.

### Weak Goal Taxonomy + Sanity-Check
- **Описание:** Паттерны слабых целей: Vague, Output-as-Outcome, Missing Baseline, Sandbagging, Moonshots. Sanity-Check: Coverage, Balance, Feasibility, Measurability, Alignment.
- **Триггер:** v0.7.1 (lightweight pilot, 5 yes/no questions) / v0.8.0 (full taxonomy)
- **Статус:** ✅ Реализовано в v0.8.0 (`references/weak_goal_taxonomy.md`, 133 строки)
- **Источник:** Borrowed from PM OKR Skill
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Пилот возможен в v0.7.1, full — в v0.8.0.

### Task Breakdown with Checkpoints
- **Описание:** Разбиение действий WOOP на шаги с чекпоинтами (✓ Чекпоинт: [критерий выполнения]). Opt-in, только для Career/Finances/Health/Home/Learning.
- **Триггер:** v0.8.0
- **Статус:** ✅ Реализовано в v0.8.0 (`references/action_breakdown_template.md`, 128 строк)
- **Источник:** Borrowed from GTD Coach Plugin
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 8/10). Требует валидации потребности через GitHub Discussion.

### Structured Growth Report
- **Описание:** Шаблон периодического обзора: Summary → Prioritized Growth Areas (Why + Evidence + Recommendation) → Observed Strengths → Actions → Recommended Resources.
- **Триггер:** v0.9.0+
- **Статус:** 📋 В ROADMAP v0.9.0+
- **Источник:** Borrowed from Composio developer-growth-analysis
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Требует re-assessment flow для Wheel of Life.

### Clarifying-Questions-First
- **Описание:** Перед глубоким протоколом — 2–3 уточняющих вопроса (домен, опыт, формат). Интеграция с Checkpoint-and-Resume.
- **Триггер:** v0.8.0
- **Статус:** 📋 В ROADMAP v0.8.0
- **Источник:** Borrowed from Composio file-organizer skill
- **Дебат:** Advocate/Critic 3 цикла → **DEFER** (conf 7/10). Пересекается с Phase 0 calibration, Track A/B, Readiness Gate. Решение: `references/session_recalibration.md`, ≤2 строки в SKILL.md.

### Unified Release Notes — CHANGELOG.md как единый источник правды (Вариант B)
- **Описание:** Сейчас релиз-ноты дублируются: CHANGELOG.md содержит всю историю, а отдельные файлы `RELEASE_NOTES_vX.Y.Z.md` (в `references/archive/`) используются для GitHub Release. Это приводит к:
  - Дублированию информации (одно и то же в двух местах)
  - Риску рассинхронизации (CHANGELOG обновлён, а RELEASE_NOTES — нет)
  - Загрязнению репозитория (каждый релиз = новый файл)
- **Цель:** Сделать CHANGELOG.md единым источником правды. Релиз-ноты для GitHub Release генерируются автоматически — извлечением секции `[X.Y.Z]` из CHANGELOG.md.
- **Текущее состояние (что есть сейчас):**
  - `CHANGELOG.md` — Keep a Changelog формат, секции `[Unreleased]`, `[0.6.0]`, `[0.5.0]` и т.д.
  - `references/archive/RELEASE_NOTES_v0.6.1.md` — отдельный файл для GitHub Release
  - `scripts/release.sh:118` — жёстко ищет `RELEASE_NOTES_$TAG.md` в корне (уже частично fixed — теперь `references/archive/`)
- **Предлагаемое решение:**
  1. **Формат CHANGELOG.md** — добавить маркеры для автоматического извлечения:
     ```markdown
     ## [0.7.0] — 2026-06-01
     <!-- release-notes-start -->
     ### 🎯 Главное
     - Фича A
     - Фича B
     <!-- release-notes-end -->
     ### Added
     - ...
     ```
  2. **Скрипт `scripts/extract-release-notes.py`** — извлекает секцию между маркерами для указанной версии
  3. **Обновить `scripts/release.sh`** — вместо `--notes-file RELEASE_NOTES_$TAG.md` использовать `--notes "$(python3 scripts/extract-release-notes.py $TAG)"`
  4. **Удалить все `RELEASE_NOTES*.md`** из репозитория (они в `references/archive/`)
  5. **Обновить `AGENTS.md`** — документировать новый процесс
- **Альтернативный формат (без маркеров):**
  - Извлекать всю секцию `## [X.Y.Z]` целиком (включая Added/Changed/Fixed)
  - Плюс: ничего не менять в CHANGELOG.md
  - Минус: GitHub Release будет содержать raw markdown с заголовками, что менее читаемо
- **Триггер:** Перед v0.7.0 или при создании следующего релиза
- **Статус:** 💡 Идея
- **Источник:** Техдолг — устранение дублирования после фикса root cause (RELEASE_NOTES_v0.6.1.md в корне)
- **Связанные файлы:** `CHANGELOG.md`, `scripts/release.sh`, `references/archive/RELEASE_NOTES*.md`
