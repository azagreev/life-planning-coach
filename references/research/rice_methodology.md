# RICE Methodology для life-planning-coach

> **Статус:** [SKILL-READY] — действующий стандарт проекта (AGENTS.md §4.4)
> **Версия:** 1.1
> **Дата:** 2026-05-20 (Effort обновлён: person-days → AI Sessions)
> **Обоснование:** FeatBench (Tsinghua, 2025), Context Rot (Chroma, 2025), Tokalator (Kariyer.net, 2026)
> **Применение:** Все фичи, баги, research-задачи, техдолг

---

## Формула

```
RICE = (Reach × Impact × Confidence) / Effort

Где:
  Reach      — % целевой аудитории, которая получит ценность
  Impact     — множитель эффекта (0.25 minimal → 3.0 massive)
  Confidence — уверенность в оценках, % (0-100)
  Effort     — трудозатраты в AI Sessions (XS/S/M/L/XL/XXL)
```

**Единица измерения RICE:** "очки приоритета" (dimensionless). Сравнение имеет смысл только внутри одного проекта.

---

## 1. Reach — Охват

> **⚠️ Критическое ограничение:** У проекта **нет user analytics**. Нет MAU, нет cohort data, нет A/B tests. Все Reach-оценки — **[GUESS]** (educated guess) на основе архитектуры skill, golden dataset и здравого смысла.
>
> **RICE работает для relative prioritization** (сравнение A vs B), даже если обе оценки — guesses. Не используйте для absolute prioritization ("это объективно важнее всего").

### Источники данных для Reach (по приоритету)

| Приоритет | Источник | Что даёт | Доступно сейчас? |
|-----------|----------|----------|-----------------|
| 1 | **User analytics** (MAU, feature activation, cohorts) | Реальные % | ❌ Нет |
| 2 | **GitHub Issues** (фич-реквесты, баг-репорты) | Сигнал спроса | ⚠️ Мало данных |
| 3 | **Golden dataset** (20 cases) | % cases с relevance | ✅ Есть |
| 4 | **SKILL.md trigger phrases** | Частота активации | ✅ Есть |
| 5 | **Архитектура skill** (Phase coverage) | Guaranteed reach | ✅ Есть |
| 6 | **Expert judgment** (educated guess) | Proxy | ✅ Всегда |

### Первичная шкала: Категории (без %)

Поскольку % — не проверяемы, используем **категории с документированной логикой**:

| Код | Название | Логика | Конверсия в число | Примеры |
|-----|----------|--------|-------------------|---------|
| **A** | All | Core flow, нет opt-in, каждая сессия | 100 | Phase 0 improvements, Energy Score |
| **M** | Majority | Natural trigger, большинство активирует | 75 | Workload Warning (при планировании), Adaptive Zones |
| **H** | Half | Требует explicit context (календарь, wearable) | 50 | Calendar features, dashboard |
| **N** | Niche | Чёткая ниша по self-report или платформе | 25 | ADHD Mode, Body Doubling, Kimi-CLI fixes |
| **S** | Small | Маленькая ниша, специфический статус | 15 | Безработные, time structure |
| **F** | Future | [APP-ONLY], не для текущего skill | 0 (skill) / отдельный список | Wearable, MCP Calendar |

### Правила присвоения категории

```
1. Фича в Phase 0 (Emotional Landing) или Phase 1 (Deep Why)?
   → A (All) — каждая сессия проходит через Phase 0/1

2. Фича срабатывает при естественном trigger ("планирую день", "устал")?
   → M (Majority) — большинство пользователей попадают в эту ситуацию

3. Фича требует explicit opt-in или external tool (календарь, дашборд)?
   → H (Half) — только те, кто использует интеграцию

4. Фича для специфического сегмента (ADHD, безработные, прокрастинаторы)?
   → N (Niche) — требует self-identification

5. Фича требует hardware или mobile app?
   → F (Future) — отдельный список [APP-ONLY]
```

### Proxy-метрики (когда нет реальных данных)

| Proxy | Как использовать | Пример |
|-------|-----------------|--------|
| **Golden dataset relevance** | Если 15/20 cases релевантны → M (75%) | Body Doubling релевантен для 8/20 cases → N (40%) |
| **SKILL.md trigger phrases** | Если фича в 5+ trigger phrases → A или M | "планирую", "устал", "не могу начать" → M |
| **Phase coverage** | Если фича в Phase 0-1 → A; Phase 5 → H | Chronotype calibration → A (Phase 0) |
| **Platform coverage** | Если для 4/4 платформ → A; 1/4 → N | Kimi-CLI specific → N |
| **Reference file cross-references** | Если 3+ других файлов ссылаются → M или H | Habit Stack Builder → M (3 references) |

### [GUESS] Маркировка

Каждая Reach-оценка должна содержать маркер источника:

```markdown
Reach: M (75%) [GUESS: архитектура skill — Phase 0 coverage]
Reach: N (25%) [GUESS: golden dataset 4/20 cases + no user data on ADHD %]
Reach: H (50%) [GUESS: trigger phrases "календарь" в 3/10 activation phrases]
```

### [APP-ONLY] = отдельный список

**Неверно:** Reach = 0% для APP-ONLY задач в общем списке.
**Верно:** APP-ONLY задачи — отдельный список с собственным RICE (для future app).

```
[SKILL-READY] список: Wearable Integration → не включаем, Reach не применим
[APP-ONLY] список: Wearable Integration → Reach = 10% (future app users), Impact = 3.0
```

### Validation Roadmap (как получить реальные Reach)

| Этап | Что делаем | Когда | Результат |
|------|-----------|-------|-----------|
| 1 | Добавить в `SKILL.md` analytics hook: "Если готовы — нажмите [поделиться feedback]" | v0.13 | User feedback channel |
| 2 | GitHub Issues template с feature request + use case | Сейчас | Сигнал спроса |
| 3 | Golden dataset expansion до 50 cases | v0.13 | Лучший proxy для Reach |
| 4 | User interviews (5-10 человек) per major feature | v0.14 | Qualitative Reach data |
| 5 | Platform analytics (если появится) | Future | Real MAU, feature activation |

### Правила оценки Reach

1. **Не путать Reach с Impact.** Reach = "сколько людей", Impact = "насколько сильно".
2. **Для багов:** Reach = категория, где баг проявляется. Critical bug в Phase 0 → A. Cosmetic bug в Kimi-CLI → N.
3. **Для техдолга:** Reach = кого затрагивает процесс. CI/CD → A (все PR). Coverage badge → N (только dev).
4. **Всегда маркировать [GUESS].** Если не можешь указать источник — это guess.
5. **Не завышать из-за энтузиазма.** Если сомневаешься — взять нижнюю категорию.

---

## 2. Impact — Эффект (0.25 → 3.0)

**Определение:** Насколько сильно фича/исправление улучшает опыт пользователя или проект.

### Шкала Impact (единая для фич и багов)

| Значение | Название | Описание | Примеры фич | Примеры багов |
|----------|----------|----------|-------------|---------------|
| **3.0** | Massive | Изменяет core experience или устраняет blocker | Workload Warning (предотвращает выгорание), Body Doubling для ADHD | Critical: skill не запускается, data loss |
| **2.0** | High | Значимое улучшение ключевого flow | Energy Score, ADHD Mode, Shutdown Ritual | High: основная фича сломана, нет workaround |
| **1.5** | Medium-High | Хорошее улучшение важного flow | Adaptive Zones, Calendar Pattern Analyzer | — |
| **1.0** | Medium | Nice to have, но заметно | Fresh Start Engine, Timezone intelligence | Medium: есть workaround, но неудобный |
| **0.75** | Low-Medium | Улучшение secondary flow | User preference work hours, Self-Contained Dashboard | — |
| **0.5** | Low | Минорное улучшение | Ревизия текстов календаря, архивация планов | Low: cosmetic, не влияет на функциональность |
| **0.25** | Minimal | Едва заметно | Coverage badge, pre-commit hooks, .build cleanup | Minimal: typo в комментарии |

### Правила оценки Impact

1. **Impact ≠ Reach.** Фича для 10% пользователей с Massive impact (ADHD Mode = 3.0) может обогнать фичу для 100% с Low impact (архивация = 0.25).
2. **Для багов:** Impact определяется severity, не частотой. Critical bug = 3.0 всегда, даже если Reach маленький.
3. **Research задачи:** Impact = потенциальная ценность результата. Token audit может дать 10-20% экономии токенов → Impact = 1.5 (для 100% Reach).
4. **Не завышать Impact из-за энтузиазма.** Если сомневаешься — взять нижнюю границу диапазона и поднять Confidence.

---

## 3. Confidence — Уверенность (0% → 100%)

**Определение:** Насколько мы уверены в оценках Reach и Impact. Это защита от энтузиазма и speculative фич.

### Шкала Confidence

| Значение | Уровень | Когда применять | Что требуется |
|----------|---------|----------------|---------------|
| **100%** | Certain | Прямая evidence, уже проверено | Фича уже реализована и протестирована, осталось интегрировать |
| **90%** | Very High | Есть evidence + похожий опыт | Аналогичная фича работает в другом модуле, тесты проходят |
| **80%** | High | Хорошая evidence, небольшие риски | Есть research, научные исследования, прототип не делали |
| **70%** | Good | Moderate evidence, известные риски | Есть user feedback, но не масштабировали |
| **60%** | Moderate | Частичная evidence | Есть гипотеза, но нет валидации на реальных пользователях |
| **50%** | Low-Moderate | Мало evidence | Research есть, но не для нашей аудитории / домена |
| **40%** | Low | Преимущественно speculative | Новая область, нет прямых аналогов |
| **30%** | Very Low | Высокая неопределённость | Нет evidence, много неизвестных |
| **10-20%** | Guesswork | Почти нет evidence | Фича зависит от внешних факторов (API, platform support) |

### Множители Confidence (корректирующие факторы)

Применить к базовой оценке:

| Фактор | Коррекция | Примечание |
|--------|-----------|------------|
| Есть научное исследование (meta-analysis, RCT) | +10% | Но проверить sample size |
| Есть продуктовый аналог (конкурент) | +5% | Но проверить market fit для нашей аудитории |
| Есть user feedback / запросы | +5-15% | 1 запрос = +5%, 5+ = +15% |
| Требует внешнего API / platform | -10-30% | Зависимость от Claude.ai, MCP, etc. |
| Требует hardware (wearable) | -20% | [APP-ONLY] barrier |
| Нет способа измерить success | -10% | Нет метрики = нет feedback loop |

### Примеры Confidence

| Задача | Базовая | Коррекции | Итог |
|--------|---------|-----------|------|
| Workload Warning | 70% | +10% (научная база: recovery paradox) | **80%** |
| Calendar Pattern Analyzer | 60% | -20% (MCP dependency) | **40%** |
| Body Doubling | 50% | +10% (Ara et al. 2025, dz=-0.90) | **60%** |
| Wearable Integration | 30% | -20% (hardware) -10% (no API) | **0%** → [APP-ONLY] |

### Примеры Reach [GUESS]

| Задача | Категория | Reach | Источник | Проверяемо? |
|--------|-----------|-------|----------|-------------|
| Energy Score (manual) | A (All) | 100% | Phase 0 coverage | ⚠️ Предположение: все проходят Phase 0 |
| Workload Warning | M (Majority) | 75% | Natural trigger ("планирую день") | ⚠️ Предположение: 75% доходят до Phase 5 |
| Body Doubling | N (Niche) | 25% | Golden dataset 8/20 + ADHD self-report | ❌ Нет данных о % ADHD в аудитории |
| Calendar Intelligence | H (Half) | 50% | Требует calendar integration | ⚠️ Предположение: 50% используют календарь |
| ADHD Mode | N (Niche) | 25% | ADHD prevalence ~15-20% | ⚠️ Не знаем overlap с нашей аудиторией |
| Wearable Integration | F (Future) | 0% [SKILL] | [APP-ONLY] | ✅ Технически верно для skill |
| Token Audit | 50% | +0% (нет прецедентов) | **40%** |

---

## 4. Effort — Трудозатраты (AI Sessions)

> **Почему не person-days:** Проект life-planning-coach разрабатывается исключительно AI-агентом. Person-days — фикция, когда разработчик — LLM. У AI-агента нет 8-часового рабочего дня; есть **context window**, **token budget** и **compaction risk** (context rot).
>
> **Исследовательская основа:** FeatBench (Tsinghua, 2025) показал, что success rate coding agents обратно коррелирует с complexity (файлы × LOC). Context Rot (Chroma, 2025) доказал деградацию модели при росте input length. Tokalator (Kariyer.net, 2026) формализовал cost как O(T²) по turns. Всё это указывает: реальное ограничение AI-разработки — не календарное время, а **context window pressure**.

### Метрика: Estimated AI Sessions (EAS) + Context Pressure

**Primary metric:** Сколько AI-сессий (dialogs) нужно от начала до коммита.
**Secondary indicator:** Context Pressure (Low / Medium / High / Critical) — насколько сильно задача давит на context window.

| Категория | EAS (сессий) | Context Pressure | Файлы | LOC | Примеры из проекта |
|-----------|-------------|------------------|-------|-----|-------------------|
| **XS** | 0.5 | Low | 1 | <50 | Typo fix (Жаворонок) |
| **S** | 1 | Low | 1-2 | <100 | Новый reference-файл |
| **M** | 2 | Low–Medium | 3-5 | 100-200 | Интеграция reference в SKILL.md |
| **L** | 3 | Medium–High | 5-10 | 200-400 | Новая фича + тесты + platform files |
| **XL** | 5 | High–Critical | 10-20 | 400+ | Multi-file refactor, research-heavy |
| **XXL** | 8 | Critical | 20+ | Архитектура | Major rewrite, [APP-ONLY] full stack |

**Числовые значения для RICE:** XS=0.5, S=1, M=2, L=3, XL=5, XXL=8. Fibonacci-like последовательность для relative estimation.

### Правила оценки EAS

1. **EAS ≠ Duration.** 1 сессия может быть 30 минут или 2 часа. EAS измеряет context management, не хронометраж.
2. **Context Pressure определяет риск.** Low = вся задача влезает в один turn. Critical = compaction неизбежен, нужен context handoff между сессиями.
3. **Включать verification loops.** Если задача требует итераций "write → test → fix → test" — каждый цикл = +0.5-1 сессия. FeatBench: success rate падает до 0% при патчах >50 LOC.
4. **Включать cross-file analysis.** Чтение 5+ файлов перед изменениями = overhead сессии. Tokalator: irrelevant tabs занимают 21% context.
5. **Для багов:**
   - Critical: EAS = XS (0.5) — hotfix в конце текущей сессии
   - High: EAS = S (1) — 1 сессия на диагностику + fix
   - Medium: EAS = S–M (1-2)
   - Low: EAS = XS (0.5)

### Anti-patterns в оценке EAS

| ❌ Неправильно | ✅ Правильно |
|---------------|-------------|
| "Это просто, 1 день" (person-day фикция) | "1 сессия, Low pressure, 1-2 файла" |
| "Неделя работы" (абстракция) | "L (3 сессии) + High pressure — нужен compaction handoff" |
| "30 дней" (инициатива) | "XXL (8+ сессий), Critical pressure — разбить на подзадачи" |

### Context Pressure: оценка и индикаторы

| Pressure | Критерии | Индикаторы при разработке |
|----------|----------|---------------------------|
| **Low** | < 5 файлов, < 100 строк изменений, 1-2 turns | Не нужно читать файлы перед изменениями |
| **Medium** | 5-10 файлов, 100-300 строк, 2-3 turns | Нужно читать файлы, но context window не критичен |
| **High** | 10-20 файлов, 300+ строк, 3-5 turns | Риск compaction, нужен context management |
| **Critical** | 20+ файлов, архитектурные изменения, 5+ turns | Нужно разбивать на подзадачи, иначе context rot |

**Context Rot thresholds (по Chroma 2025):** Performance degrades non-uniformly as input length grows. При High/Critical pressure ожидайте увеличение verification loops на 30-50%.

---

## 5. Интерпретация RICE

### Категории приоритета

| RICE | Категория | Действие | SLA |
|------|----------|----------|-----|
| **> 30** | 🟢 Quick Win | Немедленно, в текущей сессии или следующей | Same day / Next session |
| **10-30** | 🟡 High Priority | Следующий спринт / версия | Within 1-2 weeks |
| **3-10** | 🟠 Medium Priority | Backlog, делается когда есть ресурс | Within 1 month |
| **< 3** | 🔴 Moonshot | Исследовать позже, не коммитить ресурсы | No SLA, trigger-based |

### Граничные случаи

**RICE = 30.0 ровно:** 🟡 High Priority (не Quick Win). Граница — 30.0 включительно в High.

**RICE = 10.0 ровно:** 🟠 Medium Priority. Граница — 10.0 включительно в Medium.

**RICE = 3.0 ровно:** 🟠 Medium Priority. Граница — 3.0 включительно в Medium.

### Два списка: [SKILL-READY] и [APP-ONLY]

**[SKILL-READY]:** Задачи, которые можно реализовать в текущем text-based AI skill формате. Этот список — основной.

**[APP-ONLY]:** Задачи, требующие mobile app / Telegram-бот / desktop client. Reach = 0% для skill, но можно оценить Reach для future app (отдельная колонка). Эти задачи не соревнуются с [SKILL-READY] — отдельный список, отдельные приоритеты.

| Задача | RICE [SKILL-READY] | RICE [APP-ONLY] | Примечание |
|--------|-------------------|-----------------|------------|
| Wearable Integration | 0 (Reach=0) | 2.0 (Reach=10%, Impact=3.0, Conf=30%, Effort=15) | Разные списки |
| Calendar MCP | 0 (Reach=0) | 7.5 (Reach=25%, Impact=1.5, Conf=50%, Effort=10) | Разные списки |

---

## 6. Calibration — Примеры оценок

### Quick Wins (RICE > 30)

| Задача | Reach | Impact | Conf | Effort | RICE | Обоснование |
|--------|-------|--------|------|--------|------|-------------|
| Workload Warning | 75 [GUESS: M] | 2.0 | 80% | L (3) | **40.0** | Natural trigger, Sunsama proven |
| Energy Score Layer 1 | 100 [GUESS: A] | 1.5 | 70% | L (3) | **35.0** | Phase 0 coverage, manual input |
| Cross-Lingual Consistency | 100 [GUESS: A] | 1.0 | 70% | M (2) | **35.0** | Kimi users affected, but % unknown |
| Fresh Start Engine (интеграция) | 100 [GUESS: A] | 1.0 | 70% | M (2) | **35.0** | ✅ Уже реализовано, осталась интеграция |
| Typo fix (Жаворонок) | 100 [GUESS: A] | 0.25 | 100% | XS (0.5) | **50.0** | Phase 0 coverage, minimal effort |
| Ревизия текстов календаря | 100 [GUESS: A] | 0.75 | 80% | M (2) | **30.0** | Phase 5 coverage, tone improvement |

### High Priority (RICE 10-30)

| Задача | Reach | Impact | Conf | Effort | RICE | Обоснование |
|--------|-------|--------|------|--------|------|-------------|
| User preference work hours | 75 [GUESS: M] | 0.75 | 80% | M (2) | **30.0** | Natural trigger, simple config |
| Adaptive Zones + Chronotype | 100 [GUESS: A] | 1.5 | 60% | L (3) | **30.0** | 4-zone scheduling, research готов |
| ADHD Mode | 40 [GUESS: N] | 2.0 | 60% | L (3) | **16.0** | 15.5M ADHD, но nichе |
| CI/CD GitHub Actions | 100 [GUESS: A] | 0.75 | 80% | L (3) | **20.0** | All PRs, quality gate |
| Calendar Pattern Analyzer | 50 [GUESS: H] | 1.5 | 50% | XL (5) | **15.0** | [APP-ONLY]: MCP read-only |
| Self-Contained Dashboard | 75 [GUESS: M] | 1.0 | 60% | L (3) | **15.0** | Частично выполнено в v0.9.1 |
| Calendar Intelligence | 50 [GUESS: H] | 1.5 | 50% | L (3) | **12.5** | [APP-ONLY]: MCP-dependent |
| Body Doubling Scripts | 25 [GUESS: N] | 1.5 | 60% | L (3) | **7.5** | Golden dataset 8/20 |
| Token Audit | 100 [GUESS: A] | 1.5 | 40% | XL (5) | **12.0** | All users, but speculative |
| Обновить platforms/*/SKILL.md | 100 [GUESS: A] | 1.0 | 50% | L (3) | **16.7** | Partially done (v0.11, v0.12) |
| Автотриггеры ревью | 100 [GUESS: A] | 0.75 | 50% | L (3) | **12.5** | Permission-based |

### Medium Priority (RICE 3-10)

| Задача | Reach | Impact | Conf | Effort | RICE | Обоснование |
|--------|-------|--------|------|--------|------|-------------|
| Timezone intelligence | 50 [GUESS: H] | 0.5 | 60% | M (2) | **7.5** | Calendar users only |
| Time Structure for Unemployed | 20 [GUESS: N] | 1.5 | 60% | L (3) | **6.0** | Ниша, но high impact |
| Адаптивная длина ответов | 100 [GUESS: A] | 0.5 | 50% | L (3) | **8.3** | Communication Style integration |
| Регулярность планирования | 75 [GUESS: M] | 0.75 | 40% | L (3) | **7.5** | Habit anchoring |
| Аудит наград (Dopamine Budget) | 100 [GUESS: A] | 1.0 | 50% | XL (5) | **10.0** | PRD готов, но scope сокращён |
| Planning Friction Audit | 100 [GUESS: A] | 0.75 | 50% | XL (5) | **7.5** | B=MAP, friction reduction |
| Body Doubling via AI | 40 [GUESS: N] | 1.5 | 40% | XL (5) | **4.8** | Ara et al. 2025, dz=-0.90 |
| PDF экспорт дашборда | 50 [GUESS: H] | 0.5 | 60% | L (3) | **5.0** | Граница Medium/Moonshot |
| Микросессии 5 минут | 75 [GUESS: M] | 0.5 | 50% | L (3) | **6.25** | Tiny Habits integration |
| Протокол быстрых решений | 75 [GUESS: M] | 0.5 | 50% | L (3) | **6.25** | Communication Style adaptive |
| Мобильный дашборд | 75 [GUESS: M] | 1.0 | 40% | XL (5) | **6.0** | Частично в v0.9.0-0.9.1 |

### Moonshots (RICE < 3)

| Задача | Reach | Impact | Conf | Effort | RICE | Обоснование |
|--------|-------|--------|------|--------|------|-------------|
| Wearable Integration | 0 [SKILL] / 10 [APP] | 3.0 | 30% | XXL (8) | **0** [SKILL] | [APP-ONLY] |
| Google Tasks MCP | 25 [GUESS: N] | 0.75 | 20% | XL (5) | **0.75** | External dependency |
| Голосовые напоминания | 50 [GUESS: H] | 0.5 | 10% | XL (5) | **0.5** | Voice API unavailable |
| Мультиязычность | 25 [GUESS: N] | 1.0 | 20% | XXL (8) | **0.625** | No demand signal |
| Attachment Style Awareness | 50 [GUESS: H] | 1.0 | 20% | XL (5) | **2.0** | Требует психометрии |
| Dynamic Adaptation Triggers | 75 [GUESS: M] | 0.75 | 20% | XL (5) | **2.25** | Мета-уровень |
| Goal Ownership Language Rules | 100 [GUESS: A] | 0.25 | 30% | L (3) | **2.5** | Дублирует Communication Style |
| Fitness API | 15 [GUESS: S] | 0.75 | 15% | XL (5) | **0.34** | [APP-ONLY] |

---

## 7. Процесс оценки

### Шаг 1: Описать задачу

```
Задача: [что делаем]
Тип: [фича / баг / research / техдолг]
Формат: [SKILL-READY] или [APP-ONLY]
```

### Шаг 2: Оценить каждый параметр

```
Reach: [0-100]% — почему именно это значение?
Impact: [0.25-3.0] — какой уровень? Почему?
Confidence: [0-100]% — на чём основано?
Effort: [N] days — из чего складывается?
```

### Шаг 3: Рассчитать RICE

```
RICE = (Reach × Impact × Confidence) / Effort
```

### Шаг 4: Определить категорию

```
RICE > 30  → 🟢 Quick Win (немедленно)
10-30      → 🟡 High Priority (следующий спринт)
3-10       → 🟠 Medium Priority (backlog)
< 3        → 🔴 Moonshot (исследовать позже)
```

### Шаг 5: Записать обоснование

Каждая оценка должна иметь **обоснование в 1-2 предложения**. Если не можешь объяснить — переоцени.

---

## 8. Проверка на bias

### Частые ошибки

| Bias | Признак | Антидот |
|------|---------|---------|
| **Optimism bias** | Effort занижен в 2-3 раза | Умножить effort на 1.5, если новая область |
| **Recency bias** | Недавняя идея имеет высокий Impact | Подождать 48 часов, переоценить |
| **Sunk cost fallacy** | "Мы уже столько вложили" | Оценивать только future effort, не past |
| **HiPPO effect** | Авторская идея автоматически P0 | Применить RICE без exemptions |
| **Tech fascination** | Новая технология = высокий Impact | Проверить user value, не tech novelty |
| **Niche overestimation** | "ADHD-рынок огромен" → Reach 80% | Реальный Reach = % от наших пользователей |

### Advocate / Critic дебат (для задач RICE > 20)

Если задача получает RICE > 20, обязательно провести 3 цикла:

1. **Advocate:** Почему RICE должен быть ВЫШЕ?
2. **Critic:** Почему RICE должен быть НИЖЕ?
3. **Synthesis:** Усреднённая оценка

Записать в BACKLOG.md: "Advocate/Critic 3 цикла → [результат] (conf X/10)"

---

## 9. Обновление оценок

RICE — **living score**. Переоценивать при:

- Новых данных (user feedback, research)
- Изменении внешних условий (API доступен / недоступен)
- Завершении related задач (confidence растёт)
- Каждые 2 недели для активного backlog

**Не менять RICE без записи причины.** В BACKLOG.md добавлять:
```
[2026-05-20] RICE изменён с 15.0 → 35.0: причина — обнаружена проблема cross-lingual consistency
```

---

## 10. Интеграция с workflow

### AGENTS.md (§4.4)

```
Приоритизация: RICE (Reach × Impact × Confidence / Effort)
Все фичи, баги, research-задачи → оценка перед добавлением в ROADMAP
Quick Win (>30) → немедленно
High (10-30) → следующий спринт
Medium (3-10) → backlog
Moonshot (<3) → исследовать позже
```

### BACKLOG.md

Каждая новая задача должна содержать:
```markdown
> **RICE:** Reach X% × Impact Y × Confidence Z% / Effort N дней = **RICE-score**
> **Категория:** 🟢 Quick Win / 🟡 High / 🟠 Medium / 🔴 Moonshot
> **Обоснование:** 1-2 предложения
```

### ROADMAP.md

Версии формируются из задач High Priority и выше. Medium → backlog версии. Moonshot → Future Lab.

### Коммиты

Если коммит добавляет фичу с RICE — указать в сообщении:
```
feat: Workload Warning System (RICE 32.0)
```

---

*Методология v1.0 для life-planning-coach*
*Стандарт действует с 2026-05-20 (AGENTS.md v4.2)*
