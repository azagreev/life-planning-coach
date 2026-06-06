# Environment Design — проектирование среды под поведение

> **Tier:** 3 (lazy-load deep reference)
> **Загружается:** из `com_b_diagnostic.md` при Opportunity gap routing; из `habit_loop.md` при работе с anchor habits в физическом контексте; Phase 5 Execution при создании deep work setup.
> **Связанные refs:** `com_b_diagnostic.md` §Routing logic, `habit_loop.md` §1.2 Anchor, `implementation_intentions.md` §WHERE/WHEN types, `calendar_integration.md`.

---

## Что это

**Environment Design** — изменение **физической, цифровой и социальной среды** так, чтобы желаемое поведение становилось путём наименьшего сопротивления, а нежелаемое — путём максимального. Это интервенция «без участия воли»: меняем контекст один раз, поведение следует автоматически.

Это **primary intervention для Opportunity gap** в COM-B диагностике. Когда пользователь хочет и умеет, но среда сопротивляется — никакая мотивирующая беседа не помогает. Помогает только перепроектировать контекст.

---

## Evidence base — почему это работает

> **Источники:**
> - Lally, P., van Jaarsveld, C., Potts, H., & Wardle, J. (2010). How are habits formed: Modelling habit formation in the real world. *European Journal of Social Psychology*. — habit formation требует stable context; нестабильность среды удлиняет формирование вдвое.
> - Fogg, BJ (2019). *Tiny Habits*. — Prompt компонент B=MAP — это environment trigger. Без правильного prompt поведение не запускается даже при высокой Motivation и Ability.
> - Wood, W., Quinn, J. M., & Kashy, D. A. (2002). Habits в everyday life. — **43% ежедневных действий — привычки в стабильном контексте**. Меняешь контекст → ломается до 80% автоматизмов.
> - Thaler, R., & Sunstein, C. (2008). *Nudge*. — choice architecture и default switching как low-effort high-impact интервенции.
>
> **Что это значит на практике:** Self-control — исчерпаемый ресурс (Baumeister effect questioned, но «не полагайся на волю» как design principle стоит). Environment design снимает нагрузку с воли, переводя её на one-time decision. Это **самая sustainable форма behavior change** — не требует ежедневного усилия.

---

## 7 практик environment design

### 1. Friction asymmetry — асимметрия трения

**Принцип:** добавь friction к нежелаемому поведению, убери friction с желаемого. Разница даже в 20 секунд решает.

| Поведение | Friction убрать | Friction добавить |
|-----------|------------------|--------------------|
| Меньше телефон утром | Кроссовки рядом с кроватью, книга на тумбочке | Телефон в другой комнате на зарядке |
| Больше воды | Бутылка на столе, заполненная вечером | Кофе на верхней полке |
| Deep work | Закладка на проекте открыта с вечера | Slack/email закрыты, сайты заблокированы |

> **Правило:** если поведение требует > 20 секунд подготовки — оно проиграет alternative с меньшим friction. Сократи setup до нуля.

### 2. Cue removal — убрать триггеры нежелаемого

Привычка = cue → routine → reward. Без cue routine не запускается.

- Соцсети: удалить приложения с домашнего экрана (cue = иконка)
- Сладкое: не покупать в магазин (cue = вид в холодильнике)
- Бесцельный браузинг: закрыть вкладки, очистить bookmarks bar
- Курение: убрать пепельницу с балкона

Это сильнее, чем «бороться с триггером» — триггера просто нет.

### 3. Cue placement — добавить triggers для желаемого

Зеркальная практика: положи cue желаемого поведения **на путь существующей привычки** (см. anchor pattern в `habit_loop.md` §1.2).

- Витамины рядом с кофемашиной (cue после morning coffee)
- Книга на подушке (cue перед сном)
- Спортивная форма на стуле с вечера (cue утром)
- Список Top-3 на ноутбуке закрытом (cue после открытия)

Это **физическая Implementation Intention** — environmental WHERE/WHEN trigger.

### 4. Context switching — смена контекста ломает паттерн

Стабильный контекст = автоматизм. Хочешь сломать привычку → измени контекст. Хочешь закрепить новую → стабилизируй контекст.

- Не можешь сосредоточиться дома → работай из кафе/коворкинга (новый контекст = чистая Ability)
- Хочешь меньше есть вечером → перестань есть на диване перед ТВ (контекст = ассоциация)
- Хочешь больше читать → читай только в одном кресле (стабилизация cue)

**Travel и переезд — natural fresh start window** (см. `fresh_start_engine.md`). Старые контексты исчезли → окно для перепрошивки.

### 5. Social architecture — спроектировать окружение

«Ты — среднее из 5 людей вокруг» (Rohn, не RCT, но direction correct: Christakis & Fowler 2007 — поведение распространяется в социальных сетях на 3 уровня).

- **Accountability partner** — еженедельный 15-мин check-in. Не coach, а peer на том же пути.
- **Identity groups** — running club, book club, языковые встречи. Норма группы становится твоей normal.
- **Информационная диета** — кого читаешь/слушаешь? Подписки = social environment.
- **Remove dampeners** — есть человек, который активно saboтirует (партнёр пьёт когда ты бросаешь)? Честный разговор или дистанция.

### 6. Default switching — opt-out вместо opt-in

Defaults побеждают намерения. Меняй defaults в свою пользу.

- Auto-перевод на сберегательный счёт 1-го числа (default = save, не default = spend)
- Recurring доставка продуктов (default = здоровая еда дома)
- Calendar по умолчанию = deep work блоки утром, meetings только после 14:00
- Phone settings: grayscale, no notifications, screen time limits (default = меньше залипания)

### 7. Calendar as environment — время как контекст

Recurring calendar events = recurring environment. Это **environment design в time-domain**.

- Eженедельный sport-block (вт/чт 18:00) → cue = напоминание
- Daily deep work (10:00-11:30) → cue = блок в календаре + auto-DND
- Sunday review (вс 18:00) → cue = recurring event с интегрированным template
- Quarterly review (1-я суббота квартала) → cue = invite за 3 дня

См. `calendar_integration.md` §Prompt Patterns для конкретных шаблонов.

---

## Когда применять — Opportunity gap из COM-B

Загружай этот ref когда `diagnosis.com_b_assessment.primary_gap == "opportunity"`. Сигналы:

- «Времени нет» (на самом деле — нет защищённого блока)
- «Дома никак» (среда не настроена)
- «Все отвлекают» (нет social/digital boundaries)
- «Каждый раз забываю» (нет cue в среде)
- «Хочу, но как-то не складывается» (нет recurring context)

**Не нужно делать все 7 практик.** Выбери **1–2 самых высоких leverage** для конкретного поведения юзера. Спроси: «Какая из этих 7 даст наибольший сдвиг для твоего случая?» — пусть юзер выберет (autonomy supports adoption).

---

## Промпт patterns для skill

### Diagnostic prompt после COM-B Opportunity gap

```
"Сложилось: дело не в мотивации и не в навыке — среда против тебя.
Это решаемо без 'стараться больше'. Давай переделаем контекст один раз
— и поведение пойдёт без усилия.

Есть 7 ходов:
1. Асимметрия friction — сделать желаемое легче на 20 сек, нежелаемое сложнее
2. Убрать cue нежелаемого
3. Поставить cue желаемого на путь существующей привычки
4. Сменить контекст
5. Перепроектировать окружение (accountability, identity group)
6. Поменять defaults в свою пользу
7. Использовать календарь как recurring environment

Какие 1-2 из этих для твоей ситуации дадут максимум? Подумай — какой
момент конкретно сейчас тормозит?"
```

### Friction asymmetry prompt

```
"Берём конкретное поведение: [X].

Вопрос 1: что нужно сделать прямо сейчас, чтобы X занимал в подготовке
≤ 20 секунд? (например: положить инструмент рядом, открыть файл с вечера,
заполнить бутылку заранее)

Вопрос 2: что у нежелаемой альтернативы [Y] сделать на 20+ секунд сложнее?
(например: убрать в другую комнату, выйти из аккаунта, удалить приложение)

Это разовое действие — сделай сегодня. Завтра проверим разницу."
```

### Cue placement prompt (anchor + environment)

```
"Найдём anchor — действие, которое ты гарантированно делаешь каждый день
без напоминаний. Не "хотел бы делать" — а реально делаешь.

[Дождись ответа — обычно: утренний кофе, чистка зубов, открытие ноутбука]

Теперь физический cue: что положить *в место* выполнения anchor, чтобы
оно напомнило о [новом поведении]?

Не приложение, не напоминание в телефоне — физический объект. Какой?"
```

---

## Когда **не** использовать

- **Capability gap primary** — environment без skill не сработает; сначала Tiny Habits.
- **Motivation gap primary** — environment design «работает на автоматизме», но если внутри нет pull, юзер быстро откатит изменения среды (купит сладкое обратно). Сначала WOOP/Compass.
- **Crisis/burnout state** — переделка environment требует энергии. Дай recovery сначала.
- **Юзер живёт не один** — изменения общего пространства требуют переговоров с домашними. Не предлагай unilateral overhaul.
- **Travel / нестабильный контекст** — стабилизировать нечего. Дождись Fresh Start window (новый дом, переезд, новая работа).

---

## Cross-references

- **`com_b_diagnostic.md`** §Routing logic — primary entry point из Opportunity gap
- **`habit_loop.md`** §1.2 Anchor to Existing Routine — anchor pattern = cue placement
- **`implementation_intentions.md`** §Три формы — WHERE/WHEN types напрямую используют environment cues
- **`calendar_integration.md`** §Prompt Patterns — calendar as environment (практика 7)
- **`fresh_start_engine.md`** — context change windows (переезд, новый год, понедельник)
- **`evidence_map.md`** §Tiny Habits, §Habit Timeline — evidence для environmental cues

---

## TL;DR

Environment design — primary intervention для Opportunity gap (COM-B). Меняешь среду один раз → поведение следует без усилия. 7 практик: friction asymmetry, cue removal, cue placement, context switching, social architecture, default switching, calendar as environment. **Не нужны все 7** — выбери 1–2 highest leverage для конкретного поведения. Работает только если C и M в норме; иначе сначала закрой их.
