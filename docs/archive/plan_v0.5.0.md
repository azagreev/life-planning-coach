# План внедрения: Two-Track Diagnostic (v0.5.0)

> **Название релиза:** Умная Диагностика — Quick vs Deep
> **Цель:** Уменьшить assessment fatigue, добавить гибкость, сохранить глубину для желающих
> **Основа:** research_diagnostic_deep_dive.md

---

## Phase 1: Подготовка (15 мин)

1. Создать acceptance_criteria_v0.5.md
2. Создать developer_task_v0.5.md с атомарными задачами
3. Создать tester_task_v0.5.md с тест-планом
4. Git: создать ветку `feature/v0.5.0-diagnostic`

---

## Phase 2: Разработка (parallel)

### Task 2A: Обновить references/diagnostic_methods.md
- Добавить Two-Track выбор (Quick / Deep)
- Переписать Phase 2 (Values): pairwise → Top-5 → Top-3
- Переписать Phase 3A (Workview/Lifeview): 250 слов → микро-формат
- Обновить Phase 4A (Ikigai): добавить 5 Pillars Ken Mogi
- Сделать Phase 4B (Life Story): обязательный → опциональный
- Добавить Readiness Gate Protocol после каждой фазы
- Обновить Session Breakdown table

### Task 2B: Обновить SKILL.md (Stage 1 section)
- Переписать раздел "Stage 1: Diagnostic"
- Обновить порядок фаз с учётом Two-Track
- Обновить Conversation State JSON (добавить track, readiness gates)
- Обновить Key Metrics

### Task 2C: Обновить templates (если нужно)
- Проверить references/templates/ на релевантность
- Обновить Wheel_of_Life_History.md если нужно

---

## Phase 3: Тестирование

### Test 3A: Структурные тесты
- [ ] diagnostic_methods.md содержит секции Quick и Deep track
- [ ] SKILL.md ссылается на обновлённый протокол
- [ ] Все 5 фаз описаны
- [ ] Readiness Gate Protocol присутствует

### Test 3B: Логические тесты
- [ ] Quick track: ≤30 вопросов, ≤30 мин
- [ ] Deep track: разбит на 2-4 сессии
- [ ] Values: нет pairwise comparison (45 пар)
- [ ] Life Story: помечен как опциональный
- [ ] Ikigai: 5 Pillars присутствуют

### Test 3C: Контентные тесты
- [ ] Нет запрещённых слов ("надо", "должен", "провал", "отстой")
- [ ] Все шаблоны на русском с emoji
- [ ] Emotional Landing сохранён
- [ ] Safety & Ethics сохранены

### Test 3D: Интеграционные тесты
- [ ] ZIP-артефакт билдится без ошибок
- [ ] Все 22 существующих теста проходят
- [ ] Новые файлы попадают в ZIP

---

## Phase 4: Релиз

1. Git commit с conventional commit message
2. Git tag `v0.5.0`
3. Git push
4. GitHub Release с ZIP asset
5. Обновить README если нужно

---

## Definition of Done

- [ ] Все acceptance criteria выполнены
- [ ] Все тесты проходят (22 legacy + новые)
- [ ] ZIP билдится корректно
- [ ] SKILL.md < 5000 слов
- [ ] Git tag `v0.5.0` создан и запушен
- [ ] GitHub Release опубликован
