# Инвентаризация: Полный RICE-аудит проекта

> **Дата:** 2026-05-20 (Effort обновлён: person-days → AI Sessions v1.1)
> **Метод:** RICE = (Reach × Impact × Confidence) / Effort
> **Effort:** XS=0.5 / S=1 / M=2 / L=3 / XL=5 / XXL=8 (AI Sessions + Context Pressure)
> **Источники:** ROADMAP.md, BACKLOG.md, planning_research_2026-05-20.md, BUGS.md
> **Статус:** [RESEARCH] — living document, обновляется при изменении приоритетов

---

## Легенда

| RICE | Категория | Действие |
|------|----------|----------|
| > 30 | 🟢 Quick Win | Немедленно |
| 10-30 | 🟡 High Priority | Следующий спринт |
| 3-10 | 🟠 Medium Priority | Backlog |
| < 3 | 🔴 Moonshot | Исследовать позже |

**Reach:** % целевой аудитории (0-100) [GUESS]
**Impact:** 0.25 minimal → 3.0 massive
**Confidence:** 0-100% на основе evidence
**Effort:** XS/S/M/L/XL/XXL — AI Sessions + Context Pressure (Low/Med/High/Crit)

---

## Quick Wins (RICE > 30)

| # | Задача | Источник | Reach | Impact | Conf | Effort | RICE | Примечание |
|---|--------|----------|-------|--------|------|--------|------|------------|
| 1 | **Workload Warning System** — суммирование времени + threshold | ROADMAP v0.13 | 100 | 2.0 | 75% | L (3) | **50.0** | Sunsama-style, natural trigger |
| 2 | **Обновить habit_loop.md** — cross-reference на habit_stack_builder | ROADMAP v0.12 | 100 | 0.5 | 90% | S (1) | **45.0** | Уже частично сделано |
| 3 | **Energy Score (Layer 1)** — ручной ввод + task-energy matching | R&D synthesis | 100 | 1.5 | 70% | L (3) | **35.0** | Адаптация для skill-формата |
| 4 | **Cross-Lingual Consistency** — зафиксировать языковую политику + тесты | BACKLOG (новое) | 100 | 1.0 | 70% | M (2) | **35.0** | Зависит от #2 (typo уже fixed) |
| 5 | **Fresh Start Engine** — temporal landmarks + dark side protection | ROADMAP v0.12 P1 | 100 | 1.0 | 70% | M (2) | **35.0** | ✅ Уже реализовано, нужно интегрировать в platform files |
| 6 | **Adaptive Zones + Chronotype Integration** — 4-zone scheduling | R&D synthesis | 100 | 1.5 | 60% | L (3) | **30.0** | Research готов, адаптация для skill |
| 7 | **Ревизия текстов событий календаря** — убрать "надо/должен" | ROADMAP v0.10 | 100 | 0.75 | 80% | M (2) | **30.0** | Граница Quick Win/High |
| 8 | **User preference для work hours** — вместо hardcoded 9-18 | ROADMAP v0.11 P2 | 100 | 0.75 | 80% | M (2) | **30.0** | Настройка в Phase 0 |

---

## High Priority (RICE 10-30)

| # | Задача | Источник | Reach | Impact | Conf | Effort | RICE | Примечание |
|---|--------|----------|-------|--------|------|--------|------|------------|
| 9 | **CI/CD через GitHub Actions** — автотесты при push/PR | ROADMAP v0.10 / BACKLOG | 100 | 0.75 | 80% | L (3) | **20.0** | Техдолг P1 |
| 10 | **Обновить platforms/*/SKILL.md** — Phase 5 calendar check + Phase 0/1 chronotype | ROADMAP v0.11 P0 | 100 | 1.0 | 50% | L (3) | **16.7** | Partially done (v0.11, v0.12) |
| 11 | **Self-Contained Dashboard** — остатки: mobile, dark/light, PDF | BACKLOG (переделка) | 75 | 1.0 | 60% | L (3) | **15.0** | Частично выполнено в v0.9.1 |
| 12 | **Calendar Pattern Analyzer** — meeting load %, chronotype alignment | ROADMAP v0.13 P1 | 100 | 1.5 | 50% | XL (5) | **15.0** | [APP-ONLY]: MCP read-only |
| 13 | **Автотриггеры ревью** — Weekly Pulse / Monthly Scan / Quarterly Reflection | BACKLOG (v0.9.0+) | 100 | 0.75 | 50% | L (3) | **12.5** | Permission-based |
| 14 | **Token Optimization Audit** — 6 гипотез, token count analysis | BACKLOG (новое) | 100 | 1.5 | 40% | XL (5) | **12.0** | Research task, High pressure |
| 15 | **Body Doubling Scripts** — text-based silent sessions | R&D / ROADMAP Future Lab | 40 | 1.5 | 60% | L (3) | **12.0** | Для ADHD + прокрастинация |
| 16 | **ADHD Mode** — micro-tasking, body doubling prompts, time blindness | ROADMAP v0.14 | 40 | 2.0 | 60% | L (3) | **16.0** | Граница High/Medium; 15.5M ADHD |
| 17 | **Calendar Intelligence (pre-flight protocol)** — list → density → conflict → smart proposal | ROADMAP v0.11 P0 | 100 | 1.5 | 50% | L (3) | **25.0** | [APP-ONLY]: MCP-dependent |
| 18 | **Timezone intelligence** — DST handling, user timezone | ROADMAP v0.11 P2 | 75 | 0.5 | 60% | M (2) | **11.25** | Граница High/Medium |
| 19 | **Единые Release Notes из CHANGELOG** — автоизвлечение секций | BACKLOG / ROADMAP v0.10 | 25 | 0.5 | 70% | M (2) | **4.4** | Техдолг, dev-experience |
| 20 | **Архивация старых планов** — перенос plan_v*.md в references/archive/ | ROADMAP v0.10 / BACKLOG | 25 | 0.25 | 90% | S (1) | **5.6** | Cleanup |

---

## Medium Priority (RICE 3-10)

| # | Задача | Источник | Reach | Impact | Conf | Effort | RICE | Примечание |
|---|--------|----------|-------|--------|------|--------|------|------------|
| 21 | **Time Structure for Unemployed** — daily template, purpose exploration | ROADMAP v0.14 P0 | 20 | 1.5 | 60% | L (3) | **6.0** | Ниша, но high impact |
| 22 | **Planning Friction Audit** — smart defaults, template library | ROADMAP v0.14 P1 | 100 | 0.75 | 50% | XL (5) | **7.5** | B=MAP, friction reduction |
| 23 | **Аудит наград (Dopamine Budget)** — grayscale guide + conversational check-in | BACKLOG (авторский override) | 100 | 1.0 | 50% | XL (5) | **10.0** | PRD готов, но scope сокращён |
| 24 | **Адаптивная длина ответов** — Clarification/Exploration/Crystallization | BACKLOG (v0.9.0+) | 100 | 0.5 | 50% | L (3) | **8.3** | Communication Style integration |
| 25 | **Структурированный отчёт о росте** — periodic growth review | BACKLOG (v0.9.0+) | 50 | 0.75 | 40% | L (3) | **5.0** | Near Medium/Moonshot boundary |
| 26 | **Kimi-CLI в multi-platform tests** — добавить в PLATFORMS | ROADMAP v0.11 P2 | 25 | 0.5 | 80% | M (2) | **5.0** | Тестовое покрытие |
| 27 | **Coverage report** — pytest-cov + badge | BACKLOG техдолг | 25 | 0.25 | 90% | M (2) | **2.8** | Near Medium/Moonshot |
| 28 | **Pre-commit hooks** — ruff, mypy | BACKLOG техдолг | 25 | 0.25 | 80% | M (2) | **2.5** | Техдолг, near Moonshot |
| 29 | **Регулярность планирования в календаре** — Habit Formation для recurring events | BACKLOG (v0.9.0) | 75 | 0.75 | 40% | L (3) | **7.5** | Habit anchoring |
| 30 | **Сначала уточняющие вопросы** — 2-3 вопроса перед глубоким протоколом | BACKLOG (v0.8.0) | 100 | 0.5 | 50% | L (3) | **8.3** | Checkpoint-and-Resume |
| 31 | **Исправить platforms/kimi/SKILL.md** — удалить retry protocol | ROADMAP v0.11 P0 | 25 | 0.5 | 80% | M (2) | **5.0** | Platform-specific fix |
| 32 | **Исправить dangling references** — calendar_constants.md | ROADMAP v0.11 P0 | 25 | 0.25 | 80% | M (2) | **2.5** | Cleanup, near Moonshot |
| 33 | **Функциональные тесты календаря** — Free Slot, conflict detection, JSON validation | ROADMAP v0.11 P1 | 50 | 0.5 | 60% | L (3) | **5.0** | Тестовое покрытие |
| 34 | **Обновить build-skill.yml** — гонить ВСЕ тесты | ROADMAP v0.11 P1 | 25 | 0.25 | 80% | M (2) | **2.5** | CI fix, near Moonshot |
| 35 | **PoC MCP** — Gate 0-2: OAuth + CRUD + suggest_time | ROADMAP v0.11 P1 | 10 | 1.0 | 30% | L (3) | **1.0** | [APP-ONLY] |
| 36 | **Интегрировать energy_scheduling.md с calendar reading** — energy peak → free slot | ROADMAP v0.11 P2 | 50 | 0.75 | 40% | L (3) | **5.0** | [APP-ONLY] |
| 37 | **Body Doubling via AI** — silent sessions, check-in/check-out | ROADMAP R&D / research #11 | 40 | 1.5 | 40% | XL (5) | **4.8** | Ara et al. 2025, dz=-0.90 |
| 38 | **PDF экспорт дашборда** — кнопка печати/PDF | ROADMAP v0.10 | 50 | 0.5 | 60% | L (3) | **5.0** | Граница Medium/Moonshot |
| 39 | **Микросессии 5 минут** — quick check-ins | BACKLOG (v0.9.0) | 75 | 0.5 | 50% | L (3) | **6.25** | Tiny Habits integration |
| 40 | **Протокол быстрых решений** — 2-3 вопроса для decisions | BACKLOG (v0.9.0) | 75 | 0.5 | 50% | L (3) | **6.25** | Communication Style adaptive |
| 41 | **Мобильный дашборд** — адаптивная версия HTML | BACKLOG (v0.9.0) | 75 | 1.0 | 40% | XL (5) | **6.0** | Частично в v0.9.0-0.9.1 |

---

## Moonshots (RICE < 3)

| # | Задача | Источник | Reach | Impact | Conf | Effort | RICE | Примечание |
|---|--------|----------|-------|--------|------|--------|------|------------|
| 42 | **Wearable Energy Integration** — Health Connect, Body Battery | ROADMAP R&D / research #12 | 10 | 2.0 | 30% | XXL (8) | **0.75** | [APP-ONLY] |
| 43 | **Интеграция с Google Tasks MCP** — Daily Top-3 sync | ROADMAP / BACKLOG | 25 | 0.75 | 20% | XL (5) | **0.75** | Техническое ограничение — ждём MCP |
| 44 | **Голосовые напоминания** — voice output | ROADMAP / BACKLOG | 50 | 0.5 | 10% | XL (5) | **0.5** | Ждём Claude voice API |
| 45 | **Групповые сессии** — парный/групповой коучинг | ROADMAP / BACKLOG | 10 | 1.0 | 20% | XL (5) | **0.4** | 5+ запросов trigger |
| 46 | **Интеграция Fitness API** — Apple Health / Google Fit | ROADMAP / BACKLOG | 15 | 0.75 | 15% | XL (5) | **0.34** | [APP-ONLY] |
| 47 | **Мультиязычность (EN/RU toggle)** | ROADMAP / BACKLOG | 25 | 1.0 | 20% | XXL (8) | **0.625** | 10+ запросов trigger |
| 48 | **Attachment Style Awareness** — 4 стиля взрослой привязанности | ROADMAP Advanced | 50 | 1.0 | 20% | XL (5) | **2.0** | Требует психометрии |
| 49 | **Dynamic Adaptation Triggers** — 5+ триггеров адаптации | ROADMAP Advanced | 75 | 0.75 | 20% | XL (5) | **2.25** | Мета-уровень |
| 50 | **Goal Ownership Language Rules** — language ownership guide | ROADMAP Advanced | 100 | 0.25 | 30% | L (3) | **2.5** | Дублирует Communication Style |
| 51 | **Удалить .build/ из истории git** | BACKLOG техдолг | 0 | 0.25 | 90% | M (2) | **0.0** | Repo cleanup, no user impact |

---

## Рекомендуемый порядок (по RICE, группами)

### Немедленно (Quick Wins)

```
1.  Workload Warning System .......................... RICE 50.0
2.  Обновить habit_loop.md ........................... RICE 45.0
3.  Energy Score (Layer 1, manual) ................... RICE 35.0
4.  Cross-Lingual Consistency ........................ RICE 35.0
5.  Fresh Start Engine (интеграция в platforms) ...... RICE 35.0
6.  Adaptive Zones + Chronotype Integration ........... RICE 30.0
7.  Ревизия текстов событий календаря ................ RICE 30.0
8.  User preference для work hours ................... RICE 30.0
```

### Следующий спринт (High Priority)

```
9.  CI/CD через GitHub Actions ....................... RICE 20.0
10. Обновить platforms/*/SKILL.md ................... RICE 16.7
11. Self-Contained Dashboard (остатки) .............. RICE 15.0
12. Calendar Pattern Analyzer ....................... RICE 15.0
13. Автотриггеры ревью .............................. RICE 12.5
14. Token Optimization Audit ........................ RICE 12.0
15. Body Doubling Scripts ........................... RICE 12.0
16. ADHD Mode ....................................... RICE 16.0
17. Calendar Intelligence (pre-flight) .............. RICE 25.0
18. Timezone intelligence ........................... RICE 11.25
19. Единые Release Notes ............................ RICE 4.4
20. Архивация старых планов ......................... RICE 5.6
```

### Backlog (Medium Priority)

```
21. Time Structure for Unemployed ................... RICE 6.0
22. Planning Friction Audit ......................... RICE 7.5
23. Аудит наград (Dopamine Budget) .................. RICE 10.0
24. Адаптивная длина ответов ........................ RICE 8.3
25. Структурированный отчёт о росте ................. RICE 5.0
26. Kimi-CLI в multi-platform tests ................. RICE 5.0
27. Регулярность планирования в календаре ........... RICE 7.5
28. Сначала уточняющие вопросы ...................... RICE 8.3
29. Исправить platforms/kimi/SKILL.md ............... RICE 5.0
30. Функциональные тесты календаря .................. RICE 5.0
31. Body Doubling via AI ............................ RICE 4.8
32. PDF экспорт дашборда ............................ RICE 5.0
33. Микросессии 5 минут ............................. RICE 6.25
34. Протокол быстрых решений ........................ RICE 6.25
35. Мобильный дашборд ............................... RICE 6.0
36. Интегрировать energy_scheduling.md .............. RICE 5.0
```

### Исследовать позже (Moonshots)

```
37. Wearable Energy Integration ..................... RICE 0.75 [APP-ONLY]
38. Google Tasks MCP ................................ RICE 0.75
39. Голосовые напоминания ........................... RICE 0.5
40. Групповые сессии ................................ RICE 0.4
41. Fitness API ..................................... RICE 0.34 [APP-ONLY]
42. Мультиязычность ................................. RICE 0.625
43. Attachment Style Awareness ...................... RICE 2.0
44. Dynamic Adaptation Triggers ..................... RICE 2.25
45. Goal Ownership Language Rules ................... RICE 2.5
46. Coverage report ................................. RICE 2.8
47. Pre-commit hooks ................................ RICE 2.5
48. Исправить dangling references ................... RICE 2.5
49. Обновить build-skill.yml ........................ RICE 2.5
50. PoC MCP ......................................... RICE 1.0 [APP-ONLY]
51. Удалить .build/ из истории git .................. RICE 0.0
```

---

## Выводы и рекомендации

### 1. Переоценка текущего ROADMAP

**Текущий ROADMAP ставит в P0 задачи, которые по RICE — Medium или Moonshot:**

| ROADMAP P0 | Фактический RICE | Рекомендация |
|------------|-----------------|-------------|
| calendar_intelligence.md | 25.0 (High) | Не P0, [APP-ONLY] |
| Обновить platforms/*/SKILL.md | 16.7 (High) | Делается постепенно |
| ADHD Mode | 16.0 (High) | ✅ Обоснованно P0/P1 |
| Time Structure for Unemployed | 6.0 (Medium) | P1, не P0 |
| Workload Warning | 50.0 (Quick Win) | ✅ Должно быть P0 |

### 2. Quick Wins вне ROADMAP

Пять задач с RICE > 30 не были в ROADMAP как P0:
- **Workload Warning (50.0)** — в ROADMAP v0.13, не P0
- **Energy Score (35.0)** — в R&D, не в ROADMAP
- **Cross-Lingual Consistency (35.0)** — только в BACKLOG
- **Fresh Start Engine (35.0)** — считалось "done"
- **Adaptive Zones (30.0)** — в R&D, не в ROADMAP

### 3. Эффект перехода на AI Sessions

После перехода с person-days на AI Sessions:
- **Quick Wins выросли с 3 до 8** (больше задач стало "немедленно")
- **High Priority выросло с 10 до 12**
- **Moonshots сократились с 18 до 11** (много задач «поднялось»)
- Calendar Intelligence вырос с 7.5 до 25.0 (effort снизился с 10 дней до 3 сессий)

### 4. Ключевое несоответствие

ROADMAP v0.11 P0 "calendar_intelligence.md" — RICE 25.0 (High), но **[APP-ONLY]** — невозможен в skill-формате. Для [SKILL-READY] списка это задача с Reach=0.

### 5. Рекомендуемые перестановки

```
v0.11 (Calendar + Chronotype) → Переименовать в "Chronotype + Smart Scheduling"
  P0: Workload Warning (RICE 50.0) — перенести из v0.13
  P0: User preference work hours (RICE 30.0)
  P0: Adaptive Zones + Chronotype (RICE 30.0)
  P1: Energy Score Layer 1 (RICE 35.0) — добавить
  P1: Calendar Intelligence (RICE 25.0) — downgraded, [APP-ONLY]

v0.12 (Behavioral Science) → В основном done
  Осталось: Fresh Start интеграция (RICE 35.0)

v0.13 (Smart Scheduling) → Переосмыслить
  P0: Workload Warning → перенести в v0.11
  P0: Body Doubling Scripts (RICE 12.0)
  P1: Calendar Pattern Analyzer → [APP-ONLY]

v0.14 (Inclusive Coaching) → Сохранить
  P0: ADHD Mode (RICE 16.0)
  P1: Time Structure Unemployed (RICE 6.0)
  P1: Planning Friction Audit (RICE 7.5)
```

---

*Инвентаризация обновлена: 2026-05-20 (Effort v1.1: AI Sessions)*
*Метод: RICE (Reach × Impact × Confidence / Effort)*
*Всего задач: 51, из них активных: 35 (16 ✅ уже сделаны)*
