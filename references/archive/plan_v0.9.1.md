# План релиза v0.9.1 — Apple-style Dashboard Redesign

> **Статус:** Draft  
> **Дата планирования:** 2026-05-18  
> **Ожидаемая дата релиза:** TBD  
> **Scope:** 1 фича (dashboard redesign), 2 агента  
> **Зависимости:** Agent 2 (Tests) → Agent 1 (Dashboard)

---

## Цель

Заменить существующий `life-planning-dashboard.html` на новый Apple-style дизайн (Activity Rings, Liquid Glass, dark mode, responsive).

---

## Задачи

| # | Задача | Приоритет | Агент | Объём | Файлы |
|---|--------|-----------|-------|-------|-------|
| 1 | **Apple-style Dashboard** | P0 | A1 | 3–4ч | `life-planning-dashboard.html` |
| 2 | **Tests + Integration Check** | P0 | A2 | 1–2ч | `tests/unit/test_dashboard.py` |

---

## Agent 1: Apple-style Dashboard

### Что меняем
Полная замена `life-planning-dashboard.html` на новый дизайн от автора.

### Что сохраняем из v0.9.0
- **11 сфер Wheel of Life** — новый дизайн уже содержит 11 сфер в Sphere Grid ✅
- **Streak-блок** — нужно интегрировать в новый дизайн (отсутствует в макете)
- **Offline-ready** — убрать Google Fonts, всё остальное inline
- **Mobile responsive** — новый дизайн уже имеет `@media (max-width: 768px)` и `@media (max-width: 992px)` ✅

### Что добавляется (уже в макете)
- Activity Rings (Apple Health style) для OKR Progress
- Liquid Glass карточки (`backdrop-filter: blur(40px)`)
- Dark/Light mode toggle с `localStorage` persistence
- macOS Tahoe-style sidebar
- Segmented Control tabs
- Confidence Gauges (SVG)
- Activity Heatmap (365 дней)
- 12-Week Tracker
- WOOP Cards
- BHAG Roadmap (timeline)
- Weekly Priorities с чекбоксами
- Export button placeholder

### Что нужно адаптировать

#### 1. Убрать Google Fonts (offline requirement)
```html
<!-- УДАЛИТЬ -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

Системные шрифты уже прописаны в CSS и достаточны:
```css
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
```
→ Заменить на:
```css
--font-body: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', system-ui, sans-serif;
```

#### 2. Добавить Streak-блок из v0.9.0
Новый макет НЕ содержит streak-блок. Нужно интегрировать:
- Место: под Sphere Grid или в боковой панель
- Данные: `STREAK_DATA` (active_habits, digital, sugar, focus)
- Визуал: компактные карточки с иконкой, streak count, статус

#### 3. Проверить данные
Убедиться, что новый дизайн использует те же данные:
- `WHEEL_SPHERES` с 11 сферами ✅ (есть в макете)
- `STREAK_DATA` — нужно добавить
- Execution scores, weeks data — проверить совместимость

#### 4. Убедиться, что старые данные работают
Новый макет содержит sample data inline. Нужно либо:
- Оставить sample data как fallback
- Либо подготовить структуру для JSON input от скилла

### Критерий приёмки
- [ ] Dashboard открывается без ошибок в консоли
- [ ] Нет внешних CDN (проверить `test_no_external_cdn_urls`)
- [ ] 11 сфер Wheel of Life отображаются корректно
- [ ] Streak-блок присутствует и работает
- [ ] Dark/Light toggle работает и сохраняется в localStorage
- [ ] Responsive на 375px (iPhone SE) — нет горизонтального скролла
- [ ] Responsive на 992px (планшет) — sidebar скрыт, grid адаптивен
- [ ] Desktop (1200px+) — sidebar виден, полная раскладка
- [ ] Activity Rings анимированы (`ringFill` animation)
- [ ] Heatmap генерируется динамически
- [ ] 12-Week Tracker генерируется динамически
- [ ] WOOP Cards отображаются
- [ ] Weekly Priorities с чекбоксами (визуально)

---

## Agent 2: Tests + Integration Check

### Что проверяем
1. **Существующие тесты проходят:**
   - `test_file_exists_and_is_large` (>1000 строк)
   - `test_no_external_cdn_urls_or_documented` (zero CDN или задокументировано)
   - `test_doctype_and_html_lang`
   - `test_contains_expected_chart_keywords` (ECharts/Chart.js/radar/heatmap)
   - `test_wheel_has_11_domains`
   - `test_wheel_avg_divides_by_11`

2. **Новые проверки (вручную или в тестах):**
   - Dark mode toggle присутствует
   - Activity Rings SVG присутствуют
   - Streak-блок присутствует
   - Mobile CSS присутствует

### Критерий приёмки
- [ ] Все 6 dashboard тестов проходят
- [ ] SKILL.md не затронут (или обновлён если нужно)
- [ ] README.md обновлён (скриншот/dashboard описание)
- [ ] CHANGELOG.md обновлён

---

## Не входит в v0.9.1

| Задача | Почему отложено |
|--------|-----------------|
| Интерактивные чекбоксы (действительно работающие) | Требует JS state management + persistence |
| Экспорт в PNG/PDF | Placeholder в макете, реализация отдельно |
| Интеграция с реальными данными от скилла | Требует JSON data contract v2 |
| Sidebar навигация (реальные ссылки) | Декоративная, табы — основная навигация |

---

## Чеклист перед релизом

- [ ] Agent 1: Dashboard создан и проверен вручную
- [ ] Agent 2: Все тесты проходят
- [ ] SKILL.md не превышает лимиты (если обновлялся)
- [ ] README.md обновлён
- [ ] CHANGELOG.md обновлён
- [ ] `bash scripts/build-skill.sh` собирает ZIP
- [ ] `bash scripts/sync-version.sh 0.9.1` — версия синхронизирована
- [ ] Commit, tag `v0.9.1`, push
- [ ] GitHub Release создан
