# Implementation Intentions (Gollwitzer)

> **Tier:** 3 (lazy-load deep reference)
> **Загружается:** Phase 5 Execution, Phase 2 Goal Architecture (planning step), Calendar prompts, Habit Loop
> **Связанные refs:** `goal_architecture.md` §Layer 5, `habit_loop.md` §2 (Tiny Habits), `calendar_integration.md` §Prompt Patterns, `module_phase5_execution.md`

---

## Что это

**Implementation Intentions** — формула планирования действия в формате **«Если X — то Y»**, где X — конкретная ситуация-триггер, Y — конкретное действие. Разработана Peter Gollwitzer (NYU/University of Konstanz) с середины 1990-х.

В отличие от «goal intentions» («я хочу больше бегать»), implementation intentions переводят намерение в **автоматический response** на определённый cue. Когда X наступает — Y выполняется без нового решения.

---

## Evidence base — почему именно это method

> **Источник:** Gollwitzer, P. M., & Sheeran, P. (2006). Implementation intentions and goal achievement: A meta-analysis of effects and processes. *Psychological Bulletin*, 119(2), 38–69.
>
> **Размер эффекта:** **d = 0.65** (средний к сильному) по результатам **94 независимых исследований** и **8000+ участников**.
>
> **Что это значит на практике:** Implementation intentions увеличивают вероятность выполнения цели **в 2–3 раза** в сравнении с тем же намерением без if-then формулировки.

Это один из **самых сильных эффектов** в современной поведенческой психологии. Сильнее любого pep talk, mindset работы, или generic «постановки целей».

### Почему it works (механизм)

1. **Снижение нагрузки на исполнительную функцию** — решение принято заранее, в момент cue нужно только execute, не deliberate.
2. **Передача контроля среде** — действие триггерится environmental cue, не мотивацией. Работает даже когда мотивация низкая.
3. **Auto-detection** — мозг начинает scanning среды на trigger X, повышает probability "поймать" момент.

---

## Три формы If-Then plans

| Тип | Шаблон | Пример |
|-----|--------|--------|
| **WHEN** (time-based) | «Когда наступит [время], то я [действие]» | «Когда будильник звонит в 7:00, то я надену кроссовки» |
| **WHERE** (place-based) | «Если я [место], то я [действие]» | «Если я в кухне утром, то я выпью стакан воды до кофе» |
| **WHAT** (situation-based) | «Если я [ситуация/состояние], то я [действие]» | «Если я открыл ноутбук, то сначала 90 минут глубокой работы» |

**WHEN-формы** имеют наибольший эффект (Gollwitzer 1999) — время — самый стабильный cue.

---

## Coping plans (для obstacles)

Особо мощный sub-pattern: if-then plans для **препятствий**. Это «второй слой» — план как реагировать когда возникнет ожидаемое препятствие.

| Шаблон | Пример |
|--------|--------|
| «Если я почувствую [внутреннее препятствие], то я [coping response]» | «Если я почувствую желание отложить, то я начну с 5 минут — потом могу остановиться» |
| «Если я услышу [триггер], то я [reframing]» | «Если услышу внутреннего критика "это бессмысленно", то скажу: "Это шум. Сделай ещё один шаг"» |
| «Если меня перебьют [событие], то я [reset action]» | «Если кто-то напишет в Slack во время deep work, то я не отвечу до окончания блока» |

Coping plans особенно сильны для импульсивных привычек (Sheeran et al., 2005) — снижают relapse rate в 2 раза при addiction recovery.

---

## Где это уже встроено в LPC

Implementation Intentions — backbone нескольких существующих methods:

| Method | Как использует II |
|--------|-------------------|
| **WOOP** (Phase 2) | Шаг 4 (Plan) — всегда if-then format |
| **Tiny Habits** (`habit_loop.md` §2) | Anchor pattern — это implicit if-then: «After [anchor], I will [tiny behavior]» |
| **Calendar events** | Каждое recurring event с reminder = environmental cue → action |
| **Recovery Protocol** | If-then plans для возврата после срыва |
| **Habit Stack Builder** | Цепочки if-then plans — chain of triggers |

II как **standalone tool** добавляется в Phase 5 (Execution) как **primary planning method** — для caseов где нужен план, а полный WOOP overkill.

---

## Использование в Phase 5 (когда применять)

**Применять II separately (не через WOOP):**
- Конкретная задача с понятным action — нужно только зафиксировать формат
- Привычка которая уже хорошо понятна — нужен trigger
- Coping plan для известного препятствия
- Daily Top-3 — каждый top should have if-then format
- Calendar block — каждый recurring event = WHEN-type если переформулировать

**Применять через WOOP:**
- Новая важная цель — нужна ментальная контрастность для motivation
- Сложное препятствие — нужен deep exploration перед planning
- Goal с unclear desired outcome — нужно visualize

---

## Промпт patterns для skill

### Простой II prompt (Phase 5 default)

```
"Давай переведём это в формат "Если — то":

Если [когда/где/что начнётся]
То я [конкретное действие]

Например, для твоей задачи "написать email":
'Если я сяду за компьютер в 14:00, то открою email-клиент и напишу один email прежде чем что-то ещё'

Какой trigger для тебя самый надёжный? Время, место, или действие?"
```

### Coping plan prompt (для известного препятствия)

```
"Хорошо, ты заметил препятствие [X]. Создадим coping plan.

Если [precisely когда X появится]
То я [coping response — не "не делать", а конкретное alternative действие]

Например:
- Препятствие: "хочется проверить телефон во время работы"
- Coping plan: 'Если рука потянется к телефону, то я положу его в другую комнату'

Что для тебя триггер? И что точно сделаешь?"
```

### Calendar block as II (когда планируем time block)

```
"Зафиксируем это как Implementation Intention в календаре:

WHEN trigger: каждый рабочий день, 10:00
THEN action: deep work на проекте X, 90 минут, single tab

Создаю recurring event с reminder за 5 мин — это станет твоим environmental cue."
```

---

## Типичные ошибки и как их избежать

| Ошибка | Что не так | Как исправить |
|--------|-----------|----------------|
| **Vague action** | «...то я постараюсь работать продуктивно» | Конкретное действие: «...то я открою файл X и напишу 200 слов» |
| **Vague trigger** | «Когда у меня будет настроение, то...» | Time/place trigger: «Когда я закончу обед в 13:00, то...» |
| **Multiple actions in Y** | «Если 9:00, то почту, потом задачу, потом meeting» | Один primary action: «Если 9:00, то открою файл X» |
| **Negation in Y** | «Если я устал, то не сяду за телефон» | Replacement: «Если я устал, то лягу на 10 минут таймера» |
| **Trigger не зависит от ситуации** | «Если я буду мотивирован...» | Trigger должен быть external/observable, не internal motivation |
| **Too many II at once** | Создаём 5 if-then plans за раз | 1-2 за раз; больше — research показывает diminishing returns |

---

## Cross-references

- **goal_architecture.md** §Layer 5 — II как часть WOOP Plan step
- **habit_loop.md** §2 (Tiny Habits) — Anchor pattern = implicit If-Then
- **calendar_integration.md** §Prompt Patterns — Calendar events как WHEN-type triggers
- **module_phase5_execution.md** — primary tool для planning step
- **fresh_start_engine.md** — II особо эффективен при fresh start moments (понедельник, начало месяца, после события)

---

## Когда **не** использовать

- User не знает что именно хочет → сначала Phase 2 goal definition, не сразу II
- Эмоциональный block — нужна Phase 0.5 ER (emotion regulation) сначала
- Множественные конфликтующие цели → нужен Phase 2 prioritization
- Crisis state → grounding (`emotion_regulation.md`) до планирования

---

## TL;DR

If-then plans — **самый proven self-regulation tool** (d=0.65, 94 studies). Используй везде где есть конкретный action + identifiable trigger. WOOP — для важных целей; standalone II — для tactical planning, attention к coping plans для известных obstacles.
