# Acceptance Criteria v0.6.0 — Authentic Goals + Portfolio + Adaptive Style

## P0 (Must Have)

### AC-1: Stage 1.5 в архитектуре
```gherkin
Given пользователь завершил Stage 1 (Diagnostic)
When переходит к целям
Then Claude представляет Stage 1.5: "Authentic Goal Filter"
And Stage 1.5 стоит между Stage 1 и Stage 2
And SKILL.md содержит ссылку на references/authentic_goal_filter.md
```

### AC-2: Red Flag Detector (6+1)
```gherkin
Given пользователь проходит Authentic Goal Filter
When отвечает на Red Flag Detector
Then доступны 6 типовых red flags + 1 "свой вариант"
And каждый flag сопровождается вопросом "Чей это голос?"
And 1 flag ≠ автоматическое отсеивание цели
```

### AC-3: True Goal Score — Radar Chart
```gherkin
Given пользователь проходит фильтр для конкретной цели
When доходит до True Goal Score
Then оценивается по 5 осям: Ценности, Энергия, Влияние, Реалистичность, Аутентичность
And результат — ASCII-визуализация радара
And НЕ используется weighted formula с произвольными весами
And присутствует интерпретация паттернов (минимум 5 паттернов)
```

### AC-4: Goal Portfolio
```gherkin
Given все цели прошли через фильтр
When Claude показывает результат
Then отображается:
  - 🟢 Active goals (зелёные на радаре)
  - 🟡 On Pause goals (НЕ "отсеянные" или "discarded")
  - 🔍 Pattern Analysis (если 2+ целей с одним Red Flag)
And framing: "Это не провал — это данные о том, что вам НЕ подходит"
```

### AC-5: Societal Pressure Test
```gherkin
Given пользователь проходит Stage 1.5
When доходит до Societal Pressure Test
Then задаются 4 вопроса:
  1. "Если бы никто никогда не узнал — хотели бы всё равно?"
  2. "Это цель 'успешного человека' или именно ваша?"
  3. "Вы хотите это или вам стыдно/страшно, что нет?"
  4. "Цель даёт свободу/рост или статус/одобрение?"
```

### AC-6: Communication Style — 4-квадрантная матрица
```gherkin
Given SKILL.md загружен
When ищется Communication Style
Then присутствует Adaptive Coaching Matrix с 4 квадрантами:
  - Nurturing Parent
  - Challenging Consultant
  - Exploratory Guide
  - Collaborative Partner
And каждый квадрант содержит: traits, style, when to use
```

### AC-7: Style Calibration — 2 inline questions
```gherkin
Given пользователь проходит Phase 0 (Emotional Landing)
When завершается emotional landing
Then опционально задаются 2 вопроса:
  1. "Когда вы получаете feedback — мягкая поддержка или прямая правда?"
  2. "Чёткий план с шагами или свобода экспериментировать?"
And вопросы НЕ блокируют onboarding (Zero-Setup Default)
```

## P1 (Should Have)

### AC-8: Energy Check (somatic marker)
```gherkin
Given пользователь проходит фильтр
When доходит до Energy Check
Then предлагается: "Закройте глаза, представьте цель достигнутой. Лёгкость или тяжесть?"
And Energy Check помечен как опциональный
```

### AC-9: Deep Why (3 уровня)
```gherkin
Given пользователь проходит фильтр
When доходит до Deep Why
Then задаются 3 уровня "почему":
  1. "Почему вы хотите эту цель?"
  2. "Почему это важно?"
  3. "Почему это важно на самом деле?"
And НЕ 5 уровней (user fatigue)
```

### AC-10: Wheel of Life — 11 доменов
```gherkin
Given пользователь проходит Wheel of Life
When оценивает сферы
Then доступны 11 доменов:
  1. Здоровье
  2. Финансы
  3. Карьера
  4. Семья
  5. Романтика
  6. Социальные связи
  7. Личностный рост
  8. Духовность / Смысл (обязательный)
  9. Отдых / Хобби
  10. Вклад в общество (Contribution)
  11. Дом / Окружение
```

### AC-11: TTM Overlay
```gherkin
Given references/communication_style.md загружен
When ищется TTM
Then присутствует overlay из 5 stages:
  - Precontemplation → Nurturing Parent (low directiveness)
  - Contemplation → Exploratory Guide (low-med directiveness)
  - Preparation → Collaborative Partner (med directiveness)
  - Action → Challenging Consultant (med-high directiveness)
  - Maintenance → Consultant (high directiveness)
```

### AC-12: MI Explicit Framework (OARS)
```gherkin
Given references/communication_style.md загружен
When ищется MI
Then присутствуют:
  - Open-ended questions
  - Affirmations
  - Reflective listening
  - Summaries
  - Roll with Resistance
  - Develop Discrepancy
And присутствуют Pull vs Push intensity guidelines
```

## P2 (Nice to Have)

### AC-13: Attachment Style Awareness
```gherkin
Given references/communication_style.md загружен
When ищется attachment
Then присутствуют 4 стиля с coaching implications
And НЕ предлагается explicit attachment test
```

### AC-14: Dynamic Adaptation Triggers
```gherkin
Given references/communication_style.md загружен
When ищется dynamic adaptation
Then присутствуют минимум 5 triggers:
  - resistance detected
  - emotional shift
  - stage transition
  - user request
  - pattern detected
```

### AC-15: Goal Ownership Language Rules
```gherkin
Given SKILL.md загружен
When ищется Language Rules
Then присутствуют Goal Ownership правила:
  - "Ты решаешь" vs "Давайте решим"
  - "Что для тебя важно?" vs "Вот что важно:"
  - "Если захочешь" vs "Нужно сделать"
```

---

## Test Matrix

| AC | Тип теста | Как проверить | Владелец |
|----|-----------|---------------|----------|
| AC-1 | Структурный | Grep на "Stage 1.5" + "Authentic Goal Filter" в SKILL.md | Разработчик |
| AC-2 | Контентный | Grep на "Red Flag" + "Чей голос" в authentic_goal_filter.md | Тестировщик |
| AC-3 | Контентный | Grep на "Radar" + 5 осей; проверить отсутствие formula | Тестировщик |
| AC-4 | Контентный | Grep на "Active" + "On Pause" + "Pattern Analysis" | Тестировщик |
| AC-5 | Контентный | Подсчёт 4 вопросов Societal Pressure Test | Тестировщик |
| AC-6 | Структурный | Grep на 4 квадранта в communication_style.md | Разработчик |
| AC-7 | Структурный | Grep на calibration questions в diagnostic_methods.md + SKILL.md | Разработчик |
| AC-8 | Контентный | Grep на "лёгкость" или "тяжесть" + "опционально" | Тестировщик |
| AC-9 | Контентный | Подсчёт 3 уровней Deep Why; проверить отсутствие 5 уровней | Тестировщик |
| AC-10 | Структурный | Подсчёт доменов Wheel of Life = 11 | Разработчик |
| AC-11 | Контентный | Grep на 5 stages TTM в communication_style.md | Тестировщик |
| AC-12 | Контентный | Grep на OARS компоненты в communication_style.md | Тестировщик |
| AC-13 | Контентный | Grep на attachment styles в communication_style.md | Тестировщик |
| AC-14 | Контентный | Grep на triggers в communication_style.md | Тестировщик |
| AC-15 | Контентный | Grep на Goal Ownership rules в SKILL.md | Тестировщик |
