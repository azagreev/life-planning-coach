# Changelog

Все значимые изменения проекта отслеживаются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), проект следует [Semantic Versioning](https://semver.org/lang/ru/).

---

## [Unreleased]

### Added
- Системные тесты: консистентность версий, целостность README, синхронизация с GitHub
- Атомарный скрипт релиза: `scripts/release.sh`
- Post-commit hook: предупреждение о незапушенных коммитах
- `VERSION_SOURCES.md` — документация источников версии
- `CHANGELOG.md`, `ROADMAP.md`, `BACKLOG.md` — управление проектом

### Changed
- Удалён `pyproject.toml` как дублирующий `setup.py`

### Fixed
- README.md: версия 0.4.0 → 0.6.0, добавлены Stage 1.5 и адаптация стиля
- GitHub Release v0.6.0: переписан на русский язык

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

## [0.3.0] — 2026-05-15

### Added
- Интерактивный HTML Dashboard (`life-planning-dashboard.html`)
- 4 Life Planning Presets для Google Calendar
- Двухуровневая система goals (BHAG + Life Themes + OKR)
- Weekly Review Protocol (GTD + Scrum Retro)
- Daily WOOP-сессии (Wish-Outcome-Obstacle-Plan)

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

[Unreleased]: https://github.com/azagreev/life-planning-coach/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.6.0
[0.5.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.5.0
[0.4.0]: https://github.com/azagreev/life-planning-coach/releases/tag/v0.4.0
[0.3.0]: https://github.com/azagreev/life-planning-coach/compare/v0.4.0...v0.3.0
[0.2.0]: https://github.com/azagreev/life-planning-coach/compare/v0.3.0...v0.2.0
[0.1.0]: https://github.com/azagreev/life-planning-coach/compare/v0.2.0...v0.1.0
