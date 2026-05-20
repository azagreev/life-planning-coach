# Adaptive Scheduling Zones + Chronotype Integration

> **Статус:** [SKILL-READY] — адаптировано для text-based AI skill
> **Источники:** `whoop_trainingpeaks_pattern.md` §4.2, §4.5 + `body_doubling_wearable_methodology.md` §2.5
> **Дата:** 2026-05-20

---

## 4-Zone Adaptive Logic

**[SKILL-READY]** Map Energy Score → типы задач + длительность блоков:

### 🟢 Peak Performance (80-100)

| Параметр | Значение |
|----------|----------|
| **Типы задач** | Deep work, аналитика, стратегия, креатив, важные переговоры |
| **Длительность** | 90-120 мин фокус-блоки |
| **Breaks** | 10 мин / 50 мин работы (Ultradian Sprint) |
| **Body Doubling** | Solo deep work лучше; BD только если нужен внешний якорь |
| **Сообщение AI** | "Пик энергии. Самое время для [сложная задача]. Блок 90 мин." |

### 🟡 Moderate Energy (60-79)

| Параметр | Значение |
|----------|----------|
| **Типы задач** | Стандартная работа, email, админ, митинги, рутинный кодинг |
| **Длительность** | 60-90 мин блоки |
| **Breaks** | 15 мин / 45 мин работы |
| **Body Doubling** | ✅ Идеально: социальная энергия совпадает, задачи средней сложности |
| **Сообщение AI** | "Средняя энергия. Нормальный рабочий день. Стандартные задачи + один митинг." |

### 🟠 Low Energy (40-59)

| Параметр | Значение |
|----------|----------|
| **Типы задач** | Лёгкие задачи, email triage, чтение, планирование завтра |
| **Длительность** | 30-45 мин блоки MAX |
| **Breaks** | 20 мин / 30 мин работы |
| **Body Doubling** | ✅ Микро-сессии 10-15 мин; social recovery через лёгкие задачи |
| **Сообщение AI** | "Энергия ниже обычного. Лёгкие задачи + частые перерывы. Сложное перенесём." |

### 🔴 Recovery Needed (0-39)

| Параметр | Значение |
|----------|----------|
| **Типы задач** | Только urgent + критические дедлайны |
| **Длительность** | 20-30 мин блоки MAX |
| **Breaks** | Частые, 10 мин каждые 20 мин |
| **Body Doubling** | ❌ Не рекомендуется; или 10-мин микро-сессия на самое простое |
| **Сообщение AI** | "Бережный режим. Только срочное, остальное перенесём. Отдых важнее." |

---

## Chronotype-Aware Optimal Windows

**[SKILL-READY]** Комбинация Energy Score + Chronotype Profile (v0.11):

### Жаворонок (40% пользователей)

| Время | Ожидаемая зона | Тип задач |
|-------|---------------|-----------|
| 07:00-09:00 | 🟢 Peak | Deep work, стратегия |
| 09:00-12:00 | 🟡 Moderate | Стандартные задачи |
| 12:00-14:00 | 🟠 Low | Lunch + лёгкие задачи |
| 14:00-16:00 | 🟡 Moderate | Митинги, рутина |
| 16:00-18:00 | 🟠 Low | Завершение, планирование |
| 18:00+ | 🔴 Recovery | Личное время |

**Адаптация по Energy Score:**
- Утро + score 85 → "Пик плюс отличная энергия — бери самое сложное"
- Утро + score 45 → "Несмотря на хронотип, энергия низкая — начни с лёгкого"

### Промежуточный (30% пользователей)

| Время | Ожидаемая зона | Тип задач |
|-------|---------------|-----------|
| 08:00-10:00 | 🟡 Moderate | Разогрев, лёгкие задачи |
| 10:00-13:00 | 🟢 Peak | Deep work, аналитика |
| 13:00-15:00 | 🟠 Low | Post-lunch dip |
| 15:00-17:00 | 🟡 Moderate | Митинги, коммуникация |
| 17:00-19:00 | 🟠 Low | Завершение |

### Сова (30% пользователей)

| Время | Ожидаемая зона | Тип задач |
|-------|---------------|-----------|
| 10:00-12:00 | 🟠 Low | Медленный старт |
| 12:00-14:00 | 🟡 Moderate | Разогрев |
| 14:00-18:00 | 🟢 Peak | Deep work, креатив |
| 18:00-20:00 | 🟡 Moderate | Стандартные задачи |
| 20:00-22:00 | 🟠 Low | Планирование |
| 22:00+ | 🔴 Recovery | Bedtime to-do list |

---

## Scheduling Algorithm (Text-Based)

**[SKILL-READY]** Как AI skill применяет зоны при планировании дня:

```
Вход: Energy Score, Chronotype, Список задач на сегодня

1. Определить зону: score_to_level(energy_score)
2. Получить chronotype windows: get_optimal_windows(chronotype)
3. Классифицировать задачи по cognitive load:
   - Deep: требует высокой концентрации (>75%)
   - Standard: обычная работа (50-75%)
   - Light: рутина, email (<50%)
   - Admin: минимум когниции (<25%)

4. Map задачи к слотам:
   IF zone == 'peak':
     peak_windows → Deep tasks
     other_windows → Standard tasks
   IF zone == 'moderate':
     peak_windows → Standard tasks
     other_windows → Light/Admin
   IF zone == 'low':
     all_windows → Light tasks only
     defer Deep tasks → tomorrow
   IF zone == 'recovery':
     only urgent tasks
     suggest rest blocks

5. Добавить body doubling:
   IF zone == 'moderate' AND есть трудная Standard-задача:
     suggest BD session 25-45 мин
   IF zone == 'low' AND есть прокрастинируемая задача:
     suggest BD micro-session 10-15 мин
   IF zone == 'peak':
     prefer solo deep work

6. Добавить breaks по шаблону зоны

7. Output: текстовый план дня с эмодзи-индикаторами зон
```

---

## Recovery Impact Flow

**[SKILL-READY]** Что делать, когда Energy Score меняется:

```
Energy Score Change
        │
        ▼
┌───────────────────┐
│ Score Transition? │
└─────────┬─────────┘
          │
    ┌─────┴─────┐
    ▼           ▼
  Same       Changed
  Zone        Zone
    │           │
    ▼           ▼
 No-op    ┌──────────────┐
          │ Recalculate  │
          │ Schedule     │
          └──────┬───────┘
                 │
         ┌──────┴──────┐
         ▼             ▼
     Improved      Declined
     (e.g. 45→75)  (e.g. 75→35)
         │             │
         ▼             ▼
    ┌─────────┐   ┌──────────────┐
    │ Upgrade │   │ Downgrade    │
    │ Tasks   │   │ Alerts       │
    │ Add deep│   │ Reschedule   │
    │ work    │   │ Cancel       │
    └─────────┘   │ non-essential│
                  └──────────────┘
```

**Примеры сообщений AI:**

**Improved:**
> "Отличные новости! Твоя энергия выросла с 45 до 78. Я возвращаю [сложную задачу] обратно в план на сегодня. Блок 10:00-11:30."

**Declined:**
> "Вижу, что энергия упала с 75 до 40. Переношу [презентацию] на завтра, оставляю только [urgent email]. Добавляю 30-минутный перерыв в 14:00."

---

## Body Doubling + Recovery Integration

**[SKILL-READY]** Recovery-aware body doubling:

| Recovery Zone | BD Format | Почему |
|---------------|-----------|--------|
| 🟢 Peak | Solo deep work > BD | Пик энергии — лучше использовать для индивидуального фокуса |
| 🟡 Moderate | ✅ Standard BD 25-45 мин | Социальная энергия достаточна, задачи средние |
| 🟠 Low | ✅ Micro BD 10-15 мин | Лёгкий социальный контакт помогает начать |
| 🔴 Recovery | ❌ BD не рекомендуется | Нужен отдых, не фокус |

**Mutual Adaptation (групповой BD):**
- Оба участника low recovery → co-working light (нет цели, просто присутствие)
- Один peak, другой low → короткая сессия на лёгкие задачи

---

## WOOP / MCII Preemptive Adaptation

**[SKILL-READY]** Mental Contrasting + Implementation Intentions:

```
Wish: Запланировать [сложную задачу] на high-energy slot
Outcome: Успешное выполнение с высоким фокусом
Obstacle: Энергия утром ниже ожидаемой
Plan: IF energy < 60 THEN switch to admin batch OR schedule BD session

Wish: Провести 3 фокус-блока сегодня
Outcome: Почувствовать продуктивность
Obstacle: Прокрастинация на старте
Plan: IF не могу начать в течение 5 мин THEN запустить 10-мин BD micro-session
```

---

## [APP-ONLY] MCP Calendar Event Types

При переходе к mobile app / Telegram-бот с Calendar API:

| Event Type | Триггер | Цвет | Длительность |
|------------|---------|------|-------------|
| Recovery Badge | Утренний score рассчитан | Dynamic (green/yellow/orange/red) | All-day |
| Energy Block | Score + gaps в календаре | Blue | 90-120 мин |
| Rest Block | Score < 50 | Gray | 30-60 мин |
| Alert | Score < 40 ИЛИ Stress > 80 | Red | 15 мин |
| Weekly Trend | Агрегация за неделю | Bold Blue | All-day |

---

*Адаптировано для life-planning-coach skill format*
*Оригинал: whoop_trainingpeaks_pattern.md §4.2, §4.5*
