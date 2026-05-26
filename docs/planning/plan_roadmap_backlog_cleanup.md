# Plan — Roadmap & Backlog Cleanup

> **Статус:** Draft, требует одобрения перед реализацией  
> **Дата планирования:** 2026-05-21  
> **Scope:** Нормализация `ROADMAP.md` и `BACKLOG.md` без изменения продуктового поведения  
> **Режим:** Planning only

---

## Цель

Привести `ROADMAP.md` и `BACKLOG.md` к их заявленным ролям:

- `ROADMAP.md` — только будущие версии и активные release-scope решения.
- `BACKLOG.md` — только не запланированные идеи, research debt и техдолг с триггерами.
- Выпущенные версии и реализованные задачи — в `CHANGELOG.md` или архив, не в активном planning surface.

---

## Диагноз

1. `ROADMAP.md` заявляет "эта таблица содержит только будущее", но содержит большие секции v0.7.0-v0.14.0.
2. `BACKLOG.md` смешивает активные идеи, реализованные фичи, старые roadmap items, техдолг, исследования и архив.
3. Есть конфликтующие статусы:
   - Habit Loop: одновременно реализовано и "в ROADMAP v0.8.0".
   - PDF export: открыт в `ROADMAP.md`, но реализован в `BACKLOG.md`.
   - Timezone intelligence: done в roadmap, но backlog говорит, что gap не закрыт.
4. RICE применяется не ко всем активным задачам и местами использует person-days вместо EAS + Context Pressure.
5. v0.15 scope смешивает тестовую инфраструктуру и крупные продуктовые интеграции.

---

## Варианты

### Вариант A — Минимальная чистка

**Что делаем:** Исправить только явные конфликты статусов и убрать самые старые done-блоки.

**Плюсы:** Быстро, низкий риск.  
**Минусы:** Структурная проблема останется; backlog продолжит быть шумным.  
**Оценка:** XS-S, Low context pressure.

### Вариант B — Полная нормализация документов (рекомендуется)

**Что делаем:** Переразложить оба файла по ролям, архивировать done/history, пересобрать v0.15 scope, проставить RICE активным задачам.

**Плюсы:** Получаем чистую систему планирования.  
**Минусы:** Больше markdown-правок, нужно аккуратно не потерять исторический контекст.  
**Оценка:** M, Medium context pressure.

### Вариант C — Системная planning architecture

**Что делаем:** Помимо B, вводим отдельные документы `ARCHIVE.md`, `RESEARCH.md`, `PRIORITIZATION.md`, шаблоны задач и тесты структуры planning docs.

**Плюсы:** Самая строгая система.  
**Минусы:** Может быть over-engineering для текущего размера проекта.  
**Оценка:** L-XL, High context pressure.

---

## Рекомендация

Выбрать **Вариант B**.

Причина: проблема уже не точечная, но ещё не требует новой planning architecture. Достаточно очистить два главных файла, сохранить историю в архиве и сделать v0.15 исполнимым.

---

## Scope

### Входит

| # | Задача | Файлы | Приоритет | Effort | AC |
|---|--------|-------|-----------|--------|----|
| 1 | Создать архивный снимок текущих planning docs | `references/archive/` | P0 | XS / Low | Текущие `ROADMAP.md` и `BACKLOG.md` сохранены перед чисткой |
| 2 | Очистить `ROADMAP.md` от выпущенных версий | `ROADMAP.md` | P0 | S / Low | В roadmap остаются только v0.15+ и future lab |
| 3 | Пересобрать v0.15 scope | `ROADMAP.md` | P0 | S / Medium | v0.15 сфокусирован на testing/integration hardening; крупные интеграции вынесены |
| 4 | Очистить `BACKLOG.md` от реализованных задач | `BACKLOG.md` | P0 | M / Medium | Done items вынесены в archive/history или удалены как дубли CHANGELOG |
| 5 | Разрешить конфликты PDF, timezone, Habit Loop | `ROADMAP.md`, `BACKLOG.md` | P0 | S / Medium | Для каждого конфликта есть один источник правды |
| 6 | Проставить RICE активным backlog items | `BACKLOG.md` | P1 | M / Medium | Все активные фичи/research/tech debt имеют RICE в формате EAS + Context Pressure |
| 7 | Обновить правила работы с backlog | `BACKLOG.md` | P1 | XS / Low | Добавлены статусы и критерии переноса в roadmap/archive |
| 8 | Добавить tests/docs guardrails при необходимости | `tests/` | P2 | S / Medium | Есть простой тест на отсутствие released version blocks в roadmap, если не окажется избыточным |

### Не входит

- Реализация фич из v0.15.
- Изменение `SKILL.md`, `SKILL.master.md` или platform-файлов.
- Release, tag, GitHub Release.
- Исправление content gaps вроде timezone logic или PDF export, кроме planning-status reconciliation.

---

## Целевое состояние

### `ROADMAP.md`

Предлагаемая структура:

1. Заголовок и правила обновления.
2. `## Текущий статус`
   - текущая выпущенная версия: ссылка на `CHANGELOG.md`, без release history.
3. `## v0.15.0 — Testing & Integration Hardening`
   - P0: calendar functional tests, SKILL.master integrity tests.
   - P1: coverage badge, pre-commit hooks, MCP PoC.
   - P2: universal build script, optional docs guardrails.
4. `## v0.16.0 — Data & Health Integrations` или `TBD`
   - Google Health MCP как отдельный gated scope.
   - Composite Readiness Model, если зависит от health/wearable data.
5. `## Future Lab`
   - идеи без версии, только если trigger не сработал.
6. Ссылки на `BACKLOG.md`, `BUGS.md`, `CHANGELOG.md`.

### `BACKLOG.md`

Предлагаемая структура:

1. Правила backlog и формат RICE.
2. `## Active Candidates`
   - Track 0: Micro-Goal.
   - README positioning.
   - QA Hardening.
   - UX Hardening.
   - Google Tasks MCP.
   - Group coaching.
   - Multilingual support.
   - Social accountability.
3. `## Research Debt`
   - Token Optimization Audit.
   - Localization Cross-Lingual Consistency.
   - Fitness/Health API research, если не в roadmap.
4. `## Tech Debt`
   - Coverage, pre-commit, build script, docs guardrails.
5. `## Archived / Done`
   - Только краткая ссылка на архив/CHANGELOG, без длинных completed specs.

---

## Решения по конфликтам

| Конфликт | Решение |
|----------|---------|
| Habit Loop status | Считать реализованным в v0.8.0; убрать активный roadmap/backlog статус |
| PDF export | Проверить факт в `life-planning-dashboard.html`; если `window.print()`/print UI есть — закрыть в roadmap, если нет — оставить P2 tech debt |
| Timezone intelligence | Проверить `references/calendar_constants.md`; если есть только schema без protocol — переименовать backlog item в "Timezone edge-case hardening", не спорить с roadmap done |
| Google Health MCP в v0.15 | Вынести в v0.16/TBD, потому что v0.15 должен закрывать тестовую инфраструктуру |
| Composite Readiness Model | Оставить P2/TBD, зависит от readiness data model и inclusive personas |

---

## Порядок реализации после одобрения

1. Создать архивные копии текущих `ROADMAP.md` и `BACKLOG.md`.
2. Проверить факты по PDF export и timezone в исходных файлах.
3. Переписать `ROADMAP.md` в future-only структуру.
4. Переписать `BACKLOG.md` в active/research/tech-debt/archive структуру.
5. Проставить RICE для всех активных задач.
6. Запустить тесты:
   - `python3 -m pytest tests/ -q`
   - при изменении docs-тестов отдельно проверить затронутый тест.
7. Проверить `git status --short`.

---

## Acceptance Criteria

- [ ] `ROADMAP.md` не содержит подробных секций выпущенных версий v0.7.0-v0.14.0.
- [ ] `ROADMAP.md` содержит только будущий scope и ссылки на `CHANGELOG.md` для истории.
- [ ] `BACKLOG.md` не содержит длинных спецификаций уже реализованных задач.
- [ ] Все активные backlog items имеют RICE score в формате проекта: Reach, Impact, Confidence, EAS, Context Pressure.
- [ ] PDF export, Timezone intelligence и Habit Loop имеют непротиворечивый статус.
- [ ] v0.15 scope не смешивает тестовую инфраструктуру с крупной Google Health product integration.
- [ ] Все названия фич в user-facing planning docs остаются на русском.
- [ ] `python3 -m pytest tests/ -q` проходит.
- [ ] `git status --short` чистый в конце.

---

## Открытые вопросы

1. Нужно ли сохранять полный старый `BACKLOG.md` как отдельный архивный файл или достаточно rely on git history?
2. Хотим ли добавлять docs guardrail test сейчас, или оставить это как P2 после ручной чистки?
3. Google Health MCP: фиксируем сразу как v0.16.0 или оставляем `TBD` до отдельного research decision?

