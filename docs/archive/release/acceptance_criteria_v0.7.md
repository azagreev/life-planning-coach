# Acceptance Criteria v0.7.0 — Skill Structure + Anthropic Compliance

> **Scope:** Функциональные критерии (AC-1–AC-12) унаследованы из v0.6.0. Новые критерии (AC-16–AC-22) добавлены на основе официальных рекомендаций Anthropic по созданию Claude Skills (2026).
>
> **Removed from v0.6:** AC-13 (Attachment Style), AC-14 (Dynamic Adaptation Triggers), AC-15 (Goal Ownership Language Rules) — перенесены в `references/communication_style.md` как advanced patterns без формальных AC.

---

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

### AC-16: YAML Frontmatter валидность [NEW]
```gherkin
Given SKILL.md открыт
When проверяется начало файла
Then присутствует валидный YAML frontmatter между --- и ---
And содержит обязательные поля: name, version, description
And version совпадает с git tag (X.Y.Z)
And name в kebab-case совпадает с именем папки скилла
And description содержит ≥3 триггерные фразы (конкретные запросы пользователя)
And description содержит маркер "Используй при:" или "Триггеры:" или аналог
```

### AC-17: SKILL.md размер в рамках бюджета [NEW]
```gherkin
Given SKILL.md загружен
When подсчитываются строки и слова
Then строк ≤ 500 (hard fail при >500)
And warning при >400 (recommendation: перенести в references/)
And слов ≤ 5000
```

### AC-18: Обязательные разделы SKILL.md [NEW]
```gherkin
Given SKILL.md загружен
When проверяется структура
Then присутствуют разделы:
  - ## Instructions (нумерованные шаги, imperative mood)
  - ## Examples (минимум 2 примера Input → Output)
  - ## Gotchas или ## Troubleshooting
  - ## Privacy & Data Handling (содержит therapy disclaimer и правило о не-сохранении данных без согласия)
And отсутствуют слова "claude" или "anthropic" внутри инструкций
```

### AC-22: Version Consistency [NEW]
```gherkin
Given git tag vX.Y.Z
Then version в YAML frontmatter SKILL.md == X.Y.Z
And version в setup.py == X.Y.Z
And version в README badge == X.Y.Z
And отсутствуют другие хардкод-версии в исходниках, отличающиеся от X.Y.Z
```

---

## P1 (Should Have)

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

### AC-20: Triggering Precision — Description Pushiness [NEW]
```gherkin
Given description в YAML frontmatter
When оценивается quality
Then description содержит конкретные триггеры, а не общие описания
And после маркера "Используй при:" перечислено ≥3 конкретные фразы
And отсутствуют абстрактные слова без контекста: "помогает", "улучшает", "оптимизирует"
```

---

## P2 (Nice to Have)

### AC-8: Energy Check (somatic marker)
```gherkin
Given пользователь проходит фильтр
When доходит до Energy Check
Then предлагается: "Закройте глаза, представьте цель достигнутой. Лёгкость или тяжесть?"
And Energy Check помечен как опциональный
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

### AC-19: Progressive Disclosure [NEW]
```gherkin
Given контент SKILL.md + references/
When анализируется структура
Then "тяжёлый" контент (>300 строк на тему) вынесен в references/
And SKILL.md содержит явные ссылки на эти references/ (например: "Смотри references/authentic_goal_filter.md")
And references/ файлы подгружаются по требованию, а не всегда
```

### AC-21: ZIP-структура [NEW]
```gherkin
Given собран ZIP-архив
When распаковывается
Then корень содержит папку life-planning-coach/ напрямую
And внутри обязательно SKILL.md
And нет nested папок (life-planning-coach/life-planning-coach/)
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
| **AC-16** | **Структурный** | **Parse YAML frontmatter; assert name, version, description** | **CI/CD** |
| **AC-17** | **Структурный** | **`wc -l < SKILL.md`; assert ≤ 500** | **CI/CD** |
| **AC-18** | **Структурный** | **Grep на "## Instructions", "## Examples", "## Gotchas\|Troubleshooting", "## Privacy"** | **CI/CD** |
| **AC-22** | **Структурный** | **`git describe --tags` == version в YAML/setup.py/README`** | **CI/CD** |
| AC-9 | Контентный | Подсчёт 3 уровней Deep Why; проверить отсутствие 5 уровней | Тестировщик |
| AC-11 | Контентный | Grep на 5 stages TTM в communication_style.md | Тестировщик |
| AC-12 | Контентный | Grep на OARS компоненты в communication_style.md | Тестировщик |
| **AC-20** | **Структурный** | **Grep description на маркер + ≥3 фразы после него** | **CI/CD** |
| AC-8 | Контентный | Grep на "лёгкость" или "тяжесть" + "опционально" | Тестировщик |
| AC-10 | Структурный | Подсчёт доменов Wheel of Life = 11 | Разработчик |
| **AC-19** | **Структурный** | **Сравнить размер sections в SKILL.md vs references/** | **CI/CD** |
| **AC-21** | **Структурный** | **`unzip -l` → assert корень == life-planning-coach/`** | **CI/CD** |

---

## Sources

| Критерий | Источник в руководстве Anthropic |
|----------|----------------------------------|
| AC-16 | "YAML frontmatter (обязательно): name, description" |
| AC-17 | "SKILL.md: Предпочтительно не более 300–500 строк" |
| AC-18 | "Рекомендуемая структура: Instructions + Examples + Troubleshooting" |
| AC-19 | "Progressive Disclosure — главный принцип" |
| AC-20 | "Description — самое важное для triggering. Делай pushy" |
| AC-21 | "ZIP-структура критична: папка скилла должна быть КОРНЕМ архива" |
| AC-22 | Версионирование: "Добавляй поле version в YAML frontmatter" |
