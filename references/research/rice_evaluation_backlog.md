# RICE Evaluation: Backlog & ROADMAP Features

> **Дата:** 2026-05-20
> **Формула:** RICE = Reach × Impact × Confidence / Effort
> **Методология:** Оценка по всем открытым фичам BACKLOG.md и ROADMAP.md v0.15.0

---

## Методология

| Параметр | Шкала | Пояснение |
|----------|-------|-----------|
| **Reach** | 1–100 | % пользователей, которых затронет фича |
| **Impact** | 0.25–3 | 0.25=минимальный, 0.5=низкий, 1=средний, 2=высокий, 3=массовый |
| **Confidence** | 10–100% | Насколько уверены в оценке |
| **Effort** | 1–10 | Относительная трудоёмкость (человеко-недели) |

---

## Результаты

| # | Фича | Reach | Impact | Confidence | Effort | **RICE** | Категория |
|---|------|-------|--------|------------|--------|----------|-----------|
| 1 | **Переписать позиционирование README.md** | 100 | 2.0 | 90% | 1 | **180.0** | 🔥 Critical |
| 2 | **Track 0: Micro-Goal (быстрый онбординг)** | 100 | 3.0 | 80% | 3 | **80.0** | 🔥 Critical |
| 3 | **Тесты целостности SKILL.master.md** | 100 | 2.0 | 90% | 3 | **60.0** | 🔥 Critical |
| 4 | **UX Hardening (tone, cognitive load, empty states)** | 100 | 2.0 | 80% | 3 | **53.3** | 🔥 Critical |
| 5 | **Localization: Cross-Lingual Consistency** | 100 | 1.0 | 70% | 2 | **35.0** | ⚡ High |
| 6 | **Функциональные тесты календаря** | 50 | 1.5 | 90% | 4 | **16.875** | ⚡ High |
| 7 | **QA Hardening (timezones, edge cases, injection)** | 75 | 1.5 | 70% | 5 | **15.75** | ⚡ High |
| 8 | **Composite Readiness Model в скилл** | 40 | 2.0 | 70% | 4 | **14.0** | ⚡ High |
| 9 | **MCP PoC (Gate 0–2)** | 50 | 2.0 | 60% | 5 | **12.0** | ⚡ High |
| 10 | **R&D: Token Optimization Audit** | 100 | 1.5 | 40% | 5 | **12.0** | ⚡ High |
| 11 | **Coverage report + badge** | 25 | 0.5 | 95% | 1 | **11.875** | 📋 Medium |
| 12 | **Pre-commit hooks (ruff, mypy)** | 25 | 0.5 | 95% | 1 | **11.875** | 📋 Medium |
| 13 | **Google Health MCP интеграция** | 30 | 2.0 | 50% | 5 | **6.0** | 📋 Medium |
| 14 | **Social accountability** | 20 | 1.0 | 50% | 3 | **3.33** | 📋 Medium |
| 15 | **Мультиязычность (EN/RU toggle)** | 30 | 2.0 | 40% | 8 | **3.0** | 📋 Medium |
| 16 | **Интеграция с Google Tasks MCP** | 40 | 1.0 | 30% | 4 | **3.0** | 📋 Medium |
| 17 | **Универсальный скрипт сборки** | 10 | 0.5 | 80% | 3 | **1.33** | 💤 Low |
| 18 | **Core Values Discovery Exercise** | 70 | 2.0 | 70% | 3 | **32.67** | 🔥 Critical |
| 19 | **Health & Metabolism Track** | 45 | 2.0 | 65% | 5 | **11.7** | ⚡ High |
| 20 | **Goal Concordance / Romantic Relationships** | 25 | 1.5 | 60% | 3 | **7.5** | 📋 Medium |
| 21 | **Templates Rebuild v1.0 (Wiki + HTML + Guide)** | 100 | 2.0 | 75% | 5 | **30.0** | 🔥 Critical |

---

## Группировка по категориям

### 🔥 Critical (RICE ≥ 40)

| # | Фича | RICE | Почему critical |
|---|------|------|-----------------|
| 1 | Переписать позиционирование README.md | **180.0** | 1 неделя работы → 100× reach → конверсия всех новых пользователей |
| 2 | Track 0: Micro-Goal | **80.0** | Исследование done, research готов — нужна только реализация |
| 3 | Тесты целостности SKILL.master.md | **60.0** | Блокер для всех платформ; без тестов — regressions |
| 4 | UX Hardening | **53.3** | Tone + empty states влияют на retention всех пользователей |
| 18 | Core Values Discovery Exercise | **32.67** | PRD готов, evidence-based синтез (ACT/VC/Life Design), напрямую усиливает Authentic Goal Filter |
| 21 | Templates Rebuild v1.0 | **30.0** | Подготовительный блок v1.0 — единый state v2 устраняет drift между 4 артефактами и разблокирует Core Values + будущие PRD |

### ⚡ High (RICE 10–40)

| # | Фича | RICE | Почему high |
|---|------|------|-------------|
| 5 | Cross-Lingual Consistency | **35.0** | Low effort (2), high reach (100), фиксит галлюцинации |
| 6 | Функциональные тесты календаря | **16.875** | P0 для v0.15.0, но reach ограничен calendar users |
| 7 | QA Hardening | **15.75** | Scope большой (5 проблем), confidence средняя |
| 8 | Composite Readiness Model | **14.0** | Research done, но интеграция в скилл — не ясна |
| 9 | MCP PoC | **12.0** | Открывает дверь для всех интеграций, но MCP landscape нестабилен |
| 10 | Token Optimization Audit | **12.0** | High reach, но low confidence (не ясен scope savings) |
| 19 | Health & Metabolism Track | **11.7** | Новый трек, evidence base сильна по top-4 рычагам, но XL effort и нишевая аудитория |

### 📋 Medium (RICE 3–10)

| # | Фича | RICE | Почему medium |
|---|------|------|---------------|
| 11 | Coverage report + badge | **11.875** | Dev-only, но effort = 1 (quick win) |
| 12 | Pre-commit hooks | **11.875** | Dev-only, effort = 1 (quick win) |
| 20 | Goal Concordance / Romantic Relationships | **7.5** | PRD готов, но reach ограничен Портретами 2/3; требует мягкой подачи |
| 13 | Google Health MCP | **6.0** | Research done, но reach ограничен, выбор пути не сделан |
| 14 | Social accountability | **3.33** | Нишевый запрос, low confidence |
| 15 | Мультиязычность | **3.0** | High effort (8), low confidence (scope перевода) |
| 16 | Google Tasks MCP | **3.0** | Блокировано внешним событием (Tasks API не доступен) |

### 💤 Low (RICE < 3)

| # | Фича | RICE | Почему low |
|---|------|------|------------|
| 17 | Универсальный скрипт сборки | **1.33** | Только автор/CI, low impact |

---

## Рекомендуемый порядок реализации

| Приоритет | Фича | RICE | Обоснование |
|-----------|------|------|-------------|
| **1** | Переписать позиционирование README.md | 180.0 | 1 день работы, максимальный эффект на конверсию |
| **2** | Track 0: Micro-Goal | 80.0 | Research done, реализация — 2-3 дня, максимальный эффект на retention |
| **3** | Cross-Lingual Consistency | 35.0 | 1-2 дня, фиксит галлюцинации для всех пользователей |
| **4** | UX Hardening | 53.3 | Параллельно с Track 0 — tone guide + empty states |
| **5** | Тесты целостности SKILL.master.md | 60.0 | Блокер для v0.15.0, но dev-only effort |
| **6** | Coverage report + badge | 11.875 | 2-3 часа, quick win для dev credibility |
| **7** | Pre-commit hooks | 11.875 | 2-3 часа, quick win для dev experience |
| **8** | Функциональные тесты календаря | 16.875 | P0 для v0.15.0 |
| **9** | QA Hardening | 15.75 | Scope большой, но timezone — high priority |
| **10** | MCP PoC | 12.0 | Открывает дверь для future интеграций |

---

## Сравнение с текущими приоритетами ROADMAP v0.15.0

| ROADMAP v0.15.0 приоритет | RICE рейтинг | Расхождение |
|---------------------------|--------------|-------------|
| P0: Функциональные тесты календаря | #6 (16.875) | Расхождение: RICE говорит medium, но P0 потому что блокер стабильности |
| P0: Тесты целостности SKILL.master.md | #3 (60.0) | ✅ Совпадает — high RICE = P0 |
| P1: Coverage report + badge | #11 (11.875) | Расхождение: RICE medium, но P1 из-за 376 тестов |
| P1: Pre-commit hooks | #12 (11.875) | Расхождение: RICE medium, P1 из-за dev-experience |
| P1: MCP PoC | #9 (12.0) | ✅ Совпадает — medium-high |
| P1: Google Health MCP | #13 (6.0) | Расхождение: RICE low, P1 из-за research done |
| P2: Composite Readiness | #8 (14.0) | Расхождение: RICE выше, чем P2, но reach ограничен |
| P2: Универсальный скрипт сборки | #17 (1.33) | ✅ Совпадает — lowest priority |

**Вывод:** RICE подтверждает P0 для тестов SKILL.master.md, но предлагает поднять README positioning и Track 0 до критичного приоритета — выше, чем calendar tests.

---

*Оценка проведена 2026-05-20. Фичи взяты из BACKLOG.md и ROADMAP.md v0.15.0.*
