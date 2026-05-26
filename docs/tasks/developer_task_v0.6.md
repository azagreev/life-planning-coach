# Developer Task: v0.6.0 — Authentic Goals + Portfolio + Adaptive Style

## Контекст
На основе трёх research-отчётов нужно создать Stage 1.5 (Authentic Goal Filter), Goal Portfolio и Communication Style Adaptation.

**Research-файлы:**
- `references/research_diagnostic_audit_v0.5.md`
- `references/research_stage_1.5_enhanced_spec.md`
- `references/research_communication_style_v0.6.md`

**AC:** `references/acceptance_criteria_v0.6.md`

---

## Задачи (атомарные, в порядке выполнения)

### Task 1: Создать references/authentic_goal_filter.md
**Файл:** `references/authentic_goal_filter.md` (новый)
**Ветка:** `feature/v0.6.0-authentic-goals`

#### 1.1 Заголовок и мета-информация
- Версия: v0.6.0
- База: research_stage_1.5_enhanced_spec.md
- Цель: Bridge между диагностикой и целями

#### 1.2 Red Flag Detector v1.0
- 6 типовых red flags (см. research_stage_1.5_enhanced_spec.md секцию 1.1)
- 1 "свой вариант"
- Каждый с вопросом "Чей это голос?"
- Framing: heuristic, не диагностика

#### 1.3 Energy Check
- Somatic marker protocol
- Опциональный
- Связь с HARD Heartfelt (Mark Murphy)

#### 1.4 Deep Why (3 уровня)
- 3 уровня "почему" (не 5)
- Inline в протоколе фильтра

#### 1.5 Societal Pressure Test
- 4 вопроса (см. AC-5)
- Каждый с пояснением, что проверяет

#### 1.6 True Goal Score — Radar Chart
- 5 осей: Ценности, Энергия, Влияние, Реалистичность, Аутентичность
- ASCII-визуализация (бар-чарт для Claude-чата)
- 5 паттернов интерпретации
- НЕ формула с весами

#### 1.7 Goal Portfolio
- 🟢 Active goals — критерии отбора
- 🟡 On Pause goals — framing (не "отсеянные")
- 🔍 Pattern Analysis — алгоритм (2+ цели с одним RF)
- Шаблон таблиц для ASCII

#### 1.8 Protocol Flow
- Step-by-step для КАЖДОЙ цели
- Step-by-step после ВСЕХ целей (Portfolio + Patterns)
- Time estimates

#### 1.9 Wheel of Life 11 domains
- Разделить Family/Friends → Family + Social
- Добавить Contribution
- Сделать Meaning обязательным
- Сохранить Environment

---

### Task 2: Создать references/communication_style.md
**Файл:** `references/communication_style.md` (новый)

#### 2.1 Big Five → Coaching Style Mapping
- 5 traits × 2 poles = 10 adaptations
- Таблица с нейробиологическими основами (из Simply.Coach)

#### 2.2 Adaptive Coaching Matrix
- 4 квадранта: Nurturing Parent, Challenging Consultant, Exploratory Guide, Collaborative Partner
- Таблица: traits, style, when to use

#### 2.3 TTM Overlay
- 5 stages × coaching role × directiveness
- Evidence: Krebs et al. (2018)

#### 2.4 MI Explicit Framework (OARS)
- Open-ended questions, Affirmations, Reflective listening, Summaries
- Roll with Resistance, Develop Discrepancy
- Pull vs Push guidelines

#### 2.5 Attachment Style Awareness
- 4 styles × implications
- Implicit cues only

#### 2.6 Dynamic Adaptation Triggers
- 5 triggers с примерами
- How to adjust style

#### 2.7 Calibration Protocol
- 2 inline questions for Phase 0
- Optional, 1 minute

---

### Task 3: Обновить SKILL.md
**Файл:** `SKILL.md`

#### 3.1 Версия
- `version: 0.5.0` → `version: 0.6.0`

#### 3.2 3-Stage Architecture → 4-Stage
- Insert Stage 1.5 между Stage 1 и Stage 2
- Краткое описание (2-3 предложения) + ссылка на authentic_goal_filter.md

#### 3.3 Обновить Stage 1
- Wheel of Life: 8+1 → 11 domains
- Обновить Conversation State JSON (goal_filter, goal_portfolio)

#### 3.4 Core Philosophy
- Добавить Philosophy #8: Adaptive Style
- Кратко + ссылка на communication_style.md

#### 3.5 Phase 0 Enhancement
- Добавить Style Calibration (2 inline questions)
- Сохранить Zero-Setup Default

#### 3.6 Language Rules
- Добавить Goal Ownership rules

#### 3.7 Key Metrics
- Добавить v0.6.0 metrics

#### 3.8 References section
- Добавить authentic_goal_filter.md
- Добавить communication_style.md

#### 3.9 Token Budget
- Проверить: SKILL.md < 5000 слов
- Если превышает — вынести детали в reference-файлы

---

### Task 4: Обновить references/diagnostic_methods.md
**Файл:** `references/diagnostic_methods.md`

#### 4.1 Wheel of Life domains
- Обновить список сфер: 8+1 → 11

#### 4.2 Phase 0 Style Calibration
- Добавить 2 inline questions

#### 4.3 Session Breakdown
- Добавить Stage 1.5 timing

---

## Критерии готовности
- [ ] authentic_goal_filter.md создан и содержит все 6 компонентов
- [ ] communication_style.md создан и содержит все 7 секций
- [ ] SKILL.md обновлён (version 0.6.0, Stage 1.5, Communication Style)
- [ ] diagnostic_methods.md обновлён (11 domains, calibration)
- [ ] SKILL.md < 5000 слов
- [ ] Все изменения в ветке `feature/v0.6.0-authentic-goals`
- [ ] Git commit с conventional message
