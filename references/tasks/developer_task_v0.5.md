# Developer Task: v0.5.0 — Two-Track Diagnostic

## Контекст
В `references/research_diagnostic_deep_dive.md` содержатся рекомендации по улучшению диагностического этапа. Нужно применить их к реальным файлам.

## Задачи (атомарные, в порядке выполнения)

### Task 1: Обновить references/diagnostic_methods.md
**Файл:** `references/diagnostic_methods.md`
**Ветка:** `feature/v0.5.0-diagnostic`

#### 1.1 Добавить Two-Track Architecture
- В начало файла добавить раздел "## Stage 1: Diagnostic — Two-Track Approach"
- Описать Track A (Quick, 20-30 мин) и Track B (Deep, 65-105 мин)
- Для каждого трека — что включает, время, вопросы

#### 1.2 Переписать Phase 2 (Values Clarification)
- Убрать pairwise comparison (45 пар)
- Новый протокол: Top-5 Selection → Top-3 Ranking → Reflection
- 3 шага, ~10 вопросов
- Сохранить интеграцию с Wheel of Life

#### 1.3 Обновить Phase 3A (Workview/Lifeview)
- Заменить 250-словные эссе на микро-формат (3 вопроса каждый)
- Сохранить Compass Integration

#### 1.4 Обновить Phase 4A (Ikigai)
- Добавить 5 Pillars Ken Mogi с вопросами
- Сохранить текущие 6 core вопросов
- Переименовать заголовок: "Ikigai: Reason for Being (Ken Mogi + Kamiya)"

#### 1.5 Сделать Phase 4B (Life Story) опциональным
- Добавить явный skip option
- Создать Life Story Lite (3 вопроса)
- Полный McAdams protocol — пометить как "для сессии 3+"

#### 1.6 Добавить Readiness Gate Protocol
- После КАЖДОЙ фазы: проверка 1-10
- Правила: 8-10 продолжить, 5-7 пауза, 1-4 остановить

#### 1.7 Обновить Session Breakdown table
- Два трека: Quick (1 сессия) и Deep (4 сессии)
- Обновить тотал время

### Task 2: Обновить SKILL.md
**Файл:** `SKILL.md`

#### 2.1 Обновить раздел "Stage 1: Diagnostic"
- Заменить описание монолитного протокола на Two-Track
- Обновить список фаз с учётом треков

#### 2.2 Обновить Conversation State JSON
- Добавить поля: `diagnostic_track` ("quick" | "deep"), `readiness_gates` []

#### 2.3 Обновить Key Metrics
- Добавить: Quick track completion rate, Deep track opt-in rate

### Task 3: Проверить и обновить templates
- Проверить `references/templates/` на релевантность
- Если Wheel_of_Life_History.md нуждается в обновлении — обновить

## Критерии готовности
- [ ] diagnostic_methods.md содержит Two-Track Architecture
- [ ] Values Clarification не содержит pairwise comparison
- [ ] Ikigai содержит 5 Pillars
- [ ] Life Story помечен как опциональный
- [ ] Readiness Gate Protocol присутствует после каждой фазы
- [ ] SKILL.md обновлён
- [ ] Все изменения в ветке `feature/v0.5.0-diagnostic`
- [ ] Git commit с conventional message
