# План релиза v0.9.0 — Мобильная адаптация + Habit Tracker + Reward Audit

> **Статус:** Draft  
> **Дата планирования:** 2026-05-17  
> **Ожидаемая дата релиза:** TBD  
> **Scope:** 5 фич, 4 агента, wave-based execution  
> **Зависимости:** Agent 2 (Mobile) → Agent 1 (Streaks). Agent 4 (Tests/Release) → Agents 1–3.

---

## Задачи

| # | Задача | Приоритет | Агент | Объём | Файлы |
|---|--------|-----------|-------|-------|-------|
| 1 | **Habit Tracker / Dashboard Streaks** | P0 | A1 | 2–3ч | `life-planning-dashboard.html` |
| 2 | **Mobile Dashboard (responsive CSS)** | P0 | A2 | 2–3ч | `life-planning-dashboard.html` |
| 3 | **5-Minute Micro-Sessions** | P1 | A3 | 1ч | `references/micro_sessions.md` |
| 4 | **Quick Decision Protocol** | P1 | A3 | 1ч | `references/quick_decision.md` |
| 5 | **Reward Audit (Grayscale Guide)** | P2 | A3 | 1ч | `references/reward_audit.md`, `SKILL.md` |
| 6 | **Tests + Release** | P0 | A4 | 2ч | `tests/`, `README.md`, `CHANGELOG.md`, `SKILL.md` |

---

## Wave 1 (параллельно)

### Agent 1: Dashboard Streaks Data Model

**Что меняем:** `life-planning-dashboard.html`

**Добавляем:**
- `STREAK_DATA` inline JS-массив: категория → текущий streak → лучший streak → статус
- Категории (4): 🟢 Active Habits, 📱 Digital, 🍬 Sugar, 🎯 Focus
- Визуал: мини-бар или emoji-ряд под Wheel of Life (не отдельный таб)
- Offline-ready: все данные inline, не требуют ввода пользователя

**Критерий приёмки:**
- [ ] Dashboard открывается без ошибок
- [ ] Виден streak-блок (хотя бы placeholder с sample data)
- [ ] 4 категории отображаются корректно
- [ ] Не ломает существующие 11 сфер Wheel of Life

---

### Agent 3: Reference Files (3 файла)

**3.1 `references/micro_sessions.md` (≤100 строк)**
- When to use: «у меня 5 минут», «быстро», «срочно"
- Protocol: эмоция (1 слово) → 1 действие (≤30 сек, Tiny Habits)
- Integration: Habit Loop anchor
- Opt-in, не заменяет полную сессию

**Критерий приёмки:**
- [ ] Файл существует и ≤100 строк
- [ ] Содержит trigger phrases
- [ ] Содержит 3-шаговый protocol
- [ ] Не дублирует Recovery Protocol

**3.2 `references/quick_decision.md` (≤100 строк)**
- When to use: «не знаю что выбрать», «сомневаюсь», «здесь и сейчас"
- Protocol: 2–3 вопроса (Values alignment → Feasibility → One action)
- Adaptation: Communication Style quadrant (High A = больше контекста)

**Критерий приёмки:**
- [ ] Файл существует и ≤100 строк
- [ ] Содержит 2–3 вопроса
- [ ] Упоминает Communication Style

**3.3 `references/reward_audit.md` (≤120 строк)**
- Core: Grayscale Guide (Holte –37.9 min, NYT –40%)
- Optional: conversational check-in (4 категории cheap dopamine)
- Safety: opt-in, no guilt, «Reward Management» framing
- Science: citations (Rada, Avena, Lembke, Kushlev + grayscale studies)

**Критерий приёмки:**
- [ ] Файл существает и ≤120 строк
- [ ] Содержит iOS + Android инструкции
- [ ] Содержит ≥3 научных citations
- [ ] Не использует термин «dopamine detox"

---

## Wave 2 (после Wave 1)

### Agent 2: Mobile Dashboard CSS

**Что меняем:** `life-planning-dashboard.html`

**Добавляем:**
- `@media (max-width: 768px)` breakpoints
- Wheel of Life radar → меньший размер или упрощённый вид
- Streak-блок → вертикальный stack
- Шрифты: уменьшение на mobile
- Touch-friendly: кликабельные области ≥44px

**Критерий приёмки:**
- [ ] Dashboard читаем на 375px ширины (iPhone SE)
- [ ] Нет горизонтального скролла
- [ ] Все 11 сфер видны без перекрытия
- [ ] Streak-блок не ломает layout

---

## Wave 3 (после Wave 2)

### Agent 4: Tests + Release

**4.1 Новые тесты**

```
tests/system/test_v090_features.py
├── TestMicroSessions (5 тестов)
│   ├── test_file_exists
│   ├── test_line_count_under_100
│   ├── test_trigger_phrases_present
│   └── test_protocol_steps_present
├── TestQuickDecision (5 тестов)
│   ├── test_file_exists
│   ├── test_line_count_under_100
│   ├── test_question_count
│   └── test_communication_style_link
├── TestRewardAudit (7 тестов)
│   ├── test_file_exists
│   ├── test_line_count_under_120
│   ├── test_grayscale_ios_instruction
│   ├── test_grayscale_android_instruction
│   ├── test_scientific_citations_present
│   ├── test_no_dopamine_detox_term
│   └── test_opt_in_framing
├── TestDashboardStreaks (4 теста)
│   ├── test_streak_data_array_exists
│   ├── test_four_categories_present
│   └── test_no_console_errors
└── TestSkillMdIntegration (3 теста)
    ├── test_reward_audit_reference_in_skill_md
    ├── test_micro_sessions_reference_in_skill_md
    └── test_skill_md_line_count_under_500
```

**4.2 SKILL.md обновление**
- Добавить 3 reference-файла в секцию References
- Добавить hook в Phase 3 (Weekly Review) для Reward Audit
- Добавить hook в Phase 0/Session Management для Micro-Sessions
- Убедиться: строк ≤500, слов ≤5000

**4.3 README.md обновление**
- Добавить v0.9.0 фичи в список
- Обновить badge версии
- Обновить changelog ссылку

**4.4 CHANGELOG.md**
- Секция `[0.9.0]` с перечислением всех 5 фич

**4.5 Release**
- `bash scripts/sync-version.sh 0.9.0`
- `bash scripts/build-skill.sh`
- Commit, tag `v0.9.0`, push
- `gh release create v0.9.0`

**Критерий приёмки:**
- [ ] Все новые тесты проходят (≥24 теста)
- [ ] Все существующие тесты проходят (95 passed, 3 skipped)
- [ ] SKILL.md ≤500 строк, ≤5000 слов
- [ ] ZIP собирается без ошибок
- [ ] GitHub Release создан с release notes

---

## Не входит в v0.9.0 (отложено)

| Задача | Почему отложено | Когда |
|--------|-----------------|-------|
| Voice-Optimized Output | conf 6/10, ждёт мобильных метрик | v0.9.1+ |
| Auto-Review Triggers | Требует session metadata persistence | v0.9.0+ |
| Structured Growth Report | Требует re-assessment flow | v0.9.0+ |
| Adaptive Response Length | Требует Deep Why + Energy Check интеграции | v0.9.0+ |
| Dopamine Load Score | Требует daily tracking engine | Standalone app |
| Screen Time API | Требует native app permissions | Standalone app |
| Freestyle Libre | Медицинские данные + API | Standalone app v2+ |
| Custom MCP-сервер | Архитектура отдельного продукта | v2.5+ standalone |

---

## Чеклист перед релизом

- [ ] Wave 1 завершена (Agent 1 + Agent 3)
- [ ] Wave 2 завершена (Agent 2)
- [ ] Wave 3 завершена (Agent 4)
- [ ] Все тесты проходят (≥119 passed)
- [ ] SKILL.md обновлён (version: 0.9.0)
- [ ] README.md обновлён
- [ ] CHANGELOG.md обновлён
- [ ] `bash scripts/build-skill.sh` собирает ZIP
- [ ] `bash scripts/release.sh 0.9.0` проходит
