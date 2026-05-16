# Acceptance Criteria v0.5.0 — Two-Track Diagnostic

## P0 (Must Have)

### AC-1: Two-Track Architecture
```gherkin
Given пользователь впервые обращается к скиллу
When завершён Emotional Landing
Then Claude предлагает выбор: "Быстрый взгляд (20 мин)" или "Полная картина (разобьём на сессии)"
```

### AC-2: Quick Track ≤ 30 минут
```gherkin
Given пользователь выбрал Quick track
When проходит диагностику
Then общее время ≤ 30 минут
And вопросов ≤ 30
And результат: Wheel of Life + топ-3 ценности + действие на сегодня
```

### AC-3: Deep Track разбит на сессии
```gherkin
Given пользователь выбрал Deep track
When проходит диагностику
Then работа разбита на 2-4 сессии
And между сессиями сохраняется прогресс
And пользователь может поставить на паузу после любой фазы
```

### AC-4: Values без pairwise comparison
```gherkin
Given пользователь проходит Phase 2 (Values)
When отвечает на вопросы
Then НЕ используется pairwise comparison (45 пар)
And используется Top-5 selection → Top-3 ranking
And общее количество вопросов ≤ 15
```

### AC-5: Ikigai с 5 Pillars
```gherkin
Given пользователь проходит Phase 4A (Ikigai)
When отвечает на вопросы
Then присутствуют вопросы по 5 Pillars Ken Mogi:
  - Start Small
  - Releasing Yourself
  - Harmony
  - Joy of Little Things
  - Being in Here and Now
```

### AC-6: Life Story опциональный
```gherkin
Given пользователь проходит Phase 4B (Life Story)
When фаза начинается
Then Claude явно предлагает skip option:
  "Этот блок опциональный. Хотите пройти или перейдём к синтезу?"
```

### AC-7: Readiness Gate после каждой фазы
```gherkin
Given пользователь завершил любую фазу диагностики
When фаза завершена
Then Claude спрашивает: "На шкале 1-10, насколько комфортно?"
And если ответ < 6: предлагает паузу
```

### AC-8: Workview/Lifeview микро-формат
```gherkin
Given пользователь проходит Phase 3A (Workview/Lifeview)
When отвечает на вопросы
Then каждый блок содержит ≤ 3 коротких вопроса
And НЕ требуется эссе 250 слов
```

## P1 (Should Have)

### AC-9: Emotional Landing сохранён
```gherkin
Given любое взаимодействие
When начинается диагностика
Then Emotional Landing Protocol выполняется до любой структуры
```

### AC-10: Safety & Ethics сохранены
```gherkin
Given любая фаза диагностики
When обрабатываются чувствительные темы
Then присутствуют:
  - Warning signs (оценки < 3/10)
  - Skip option для любого вопроса
  - Нейтральный тон без осуждения
```

### AC-11: Progressive Disclosure
```gherkin
Given пользователь проходит диагностику
When фазы следуют одна за другой
Then сложность нарастает постепенно
And личные темы появляются после нейтральных
```

### AC-12: Token Efficiency
```gherkin
Given SKILL.md загружен в контекст Claude
When измеряется размер
Then < 5000 слов (для Free tier compatibility)
```

## P2 (Nice to Have)

### AC-13: Wheel of Life +9-я сфера
```gherkin
Given пользователь проходит Wheel of Life
When оценивает сферы
Then доступна опциональная 9-я сфера "Смысл / Духовность"
```

### AC-14: Visualization в Quick track
```gherkin
Given Quick track завершён
When пользователь получает результат
Then отображается ASCII-визуализация Wheel of Life
```

---

## Test Matrix

| AC | Тип теста | Как проверить | Владелец |
|----|-----------|---------------|----------|
| AC-1 | Структурный | Grep на "Quick track" + "Deep track" в diagnostic_methods.md | Разработчик |
| AC-2 | Структурный | Подсчёт вопросов в Quick track секции | Разработчик |
| AC-3 | Структурный | Проверка Session Breakdown table | Разработчик |
| AC-4 | Логический | Grep на "pairwise" — должно быть только в комментарии "устарело" | Тестировщик |
| AC-5 | Контентный | Grep на "5 Pillars" + каждый pillar | Тестировщик |
| AC-6 | Контентный | Grep на "опциональный" + "skip" в Life Story секции | Тестировщик |
| AC-7 | Контентный | Grep на "Readiness Gate" после каждой фазы | Тестировщик |
| AC-8 | Логический | Проверка длины Workview/Lifeview вопросов | Тестировщик |
| AC-9 | Контентный | Grep на "Emotional Landing" в начале Stage 1 | Тестировщик |
| AC-10 | Контентный | Grep на "Warning Signs" + "Skip option" | Тестировщик |
| AC-11 | Логический | Проверка порядка фаз | Тестировщик |
| AC-12 | Структурный | wc -w SKILL.md | Тестировщик |
| AC-13 | Опциональный | Grep на "Смысл" как 9-я сфера | Тестировщик |
| AC-14 | Опциональный | Проверка ASCII визуализации в Quick track | Тестировщик |
