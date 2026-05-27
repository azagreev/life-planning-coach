# COM-B Diagnostic (Michie, van Stralen, West)

> **Tier:** 3 (lazy-load deep reference)
> **Загружается:** Phase 0 (opt-in при «не могу начать»), Phase 1 (opt-in после Wheel of Life при повторяющейся жалобе), Phase 3 Weekly Review (escalation если gap повторяется ≥ 2 недели).
> **Связанные refs:** `evidence_map.md` §COM-B, `action_breakdown_template.md`, `habit_loop.md` §1 Tiny Habits, `environment_design.md`, `module_phase2_goal_architecture.md` §Layer 5 WOOP, `module_phase1_5_goal_filter.md` Compass Mode, `implementation_intentions.md`.

---

## Что это

**COM-B Model** — диагностическая рамка, которая объясняет любое поведение через три необходимых компонента: **C**apability (могу), **O**pportunity (среда позволяет), **M**otivation (хочу). Если хоть один компонент «провален» — поведение не запускается, даже когда два других в порядке.

Это **не goal-setting инструмент**, а **диагностика причин бездействия**: когда пользователь говорит «знаю, что важно, но не делаю» — COM-B показывает, где именно сломалось звено, и направляет в правильную интервенцию (а не в очередной мотивирующий разговор).

---

## Evidence base — почему именно это method

> **Источник:** Michie, S., van Stralen, M. M., & West, R. (2011). The behaviour change wheel: A new method for characterising and designing behaviour change interventions. *Implementation Science*, 6(42). [DOI](https://doi.org/10.1186/1748-5908-6-42)
>
> **Статус:** Foundational framework для UK Behaviour Change Wheel — стандарта в public health intervention design (NHS, NICE guidelines).
>
> **Что это значит на практике:** Большинство «провалов выполнения» — не motivation problem (как кажется). Empirical reviews behavior change interventions показывают: ~60% случаев — Capability или Opportunity gap, замаскированный под лень. COM-B заставляет проверить все три компонента, а не сразу прыгать в мотивацию.

### Почему it works (механизм)

1. **Замена «либо/либо» на «и/и/и»** — поведение требует всех трёх компонентов одновременно. Если убрать обвинение «у тебя нет силы воли» и посмотреть на ability/environment — часто оказывается, что мотивация в порядке, а сломан другой элемент.
2. **Targeted intervention** — каждая gap имеет свою proven интервенцию (Capability → skill building; Opportunity → environment design; Motivation → values work / WOOP). Generic «постарайся больше» не работает.
3. **Снижение самокритики** — диагностика структурная, не моральная. Пользователь видит «это решаемая проблема X», а не «я плохой».

---

## Три компонента

| Компонент | Что включает | Типичный сигнал gap |
|-----------|--------------|---------------------|
| **Capability** | *Physical* — физические навыки, тело, инструменты. *Psychological* — знание шагов, понимание как именно делать, working memory для удержания плана. | «Не знаю с чего начать», «первый шаг неясен», «делаю — получается криво» |
| **Opportunity** | *Physical* — среда, время, инструменты под рукой, отсутствие friction. *Social* — поддержка окружения, нормы, accountability. | «Времени нет», «дома никак», «никто вокруг этого не делает», «все отвлекают» |
| **Motivation** | *Reflective* — сознательное «хочу», ценностное обоснование, оценка важности. *Automatic* — эмоциональный pull, привычка, identity (это «я-такой-человек»). | «Понимаю важность, но в моменте — не хочется», «каждый раз себя уговариваю», «это не моё, делаю потому что так принято» |

**Behavior = функция всех трёх.** Если C=10, O=10, M=2 — поведения не будет. Если M=10, C=10, O=2 — не будет тоже. Самое слабое звено определяет результат.

---

## Диагностический протокол (3–5 минут, 9 вопросов)

Задавай по группам, не списком. После каждой группы — короткая интерпретация вслух (юзер видит ход твоей мысли).

### Capability — «могу ли я физически и когнитивно»

1. **Physical:** «Есть ли у тебя физические/практические ресурсы делать это? Время, инструменты, тело в форме?»
2. **Psychological:** «Знаешь ли ты *как* именно это делать? Не "хочу" — а "владею знанием конкретных шагов"?»
3. **First-step calibration:** «Если я скажу — сделай первый шаг прямо сейчас — ты знаешь *что именно* это будет?»

### Opportunity — «среда позволяет»

4. **Physical environment:** «Что в твоей среде делает это поведение лёгким или сложным? Триггеры, пространство, инструменты под рукой — или наоборот?»
5. **Social environment:** «Кто в окружении поддерживает или мешает? Есть ли accountability партнёр? Кто-то рядом делает то же?»
6. **Time/context window:** «В какой момент дня/недели это легче всего? Этот контекст у тебя регулярно есть, или нужно его искать?»

### Motivation — «хочу ли я сознательно и автоматически»

7. **Reflective:** «От 1 до 10 — насколько это для тебя важно сознательно? Почему именно эта оценка, а не на 2 ниже?»
8. **Automatic:** «Хочешь ли ты этого *автоматически*, без уговоров? Или каждый раз приходится себя заставлять?»
9. **Value alignment:** «Это твоя цель — или чьи-то ожидания / долг / "так положено"?»

---

## Determination logic — какой gap primary

После 9 вопросов выбери **один primary gap** (если их несколько — самый блокирующий). Простые сигналы:

- **Capability gap:** ответы 1–3 показывают «не знаю как», «нет навыка», «первый шаг неясен», «делаю криво» → routing в Capability ветку.
- **Opportunity gap:** ответы 4–6 показывают «среда мешает», «времени нет», «нет поддержки», «контекст не складывается» → Opportunity ветка.
- **Motivation gap:** ответы 7–9 показывают важность ≤ 6, «каждый раз уговариваю», «это для других» → Motivation ветка.

**Правило при множественных gap:** начни с **самого блокирующего**. Если gap во всех трёх — **сначала Motivation** (без неё работа над C и O не закрепится). Если C и O оба провалены, а M в порядке — начни с Capability (быстрее win, чем перестройка environment).

Запиши результат в state: `diagnosis.com_b_assessment = {capability, opportunity, motivation: "ok"|"gap", primary_gap, assessed_at}`.

---

## Routing logic — где какая интервенция

| Primary gap | Куда направляем | Почему |
|-------------|------------------|--------|
| **Capability** | `action_breakdown_template.md` (микро-шаги до видимого первого шага) + `habit_loop.md` §1 Tiny Habits (B=MAP — снижаем Ability barrier до ≤ 30 секунд) | Skill-building через decomposition. Tiny Habits = понижение порога сложности до уровня, где Ability перестаёт быть барьером. |
| **Opportunity** | `environment_design.md` (5–7 практик: убрать триггер, добавить friction к нежелаемому, сменить контекст, social accountability, default switching, choice architecture, calendar cues) | Environment design — единственная интервенция, которая работает «без участия» воли. Меняем среду, поведение следует. |
| **Motivation** | `module_phase2_goal_architecture.md` §Layer 5 (WOOP — Wish/Outcome/Obstacle/Plan) + `module_phase1_5_goal_filter.md` Compass Mode (values alignment via Schwartz Top-3) | Motivation gap часто = goal не выровнен с values (интроект). WOOP добавляет mental contrasting и II. Compass проверяет, не чужая ли это цель. |

После routing — **обязательно вернись через 1–2 недели** и переоцени COM-B. Если gap не сдвинулся — пересмотри determination (возможно, primary gap другой).

---

## Где это уже встроено в LPC

COM-B — **диагностический entry point**, не основной flow. Точки входа:

| Phase | Триггер | Что делает |
|-------|---------|------------|
| **Phase 0** (master) | Сигнал «не могу начать», «знаю, что важно, но не делаю», «пытаюсь — не получается» в Emotional Landing | Soft suggestion: «Хочешь, разберём что именно мешает? Есть короткая 5-минутная диагностика». Opt-in, не блокирует flow. |
| **Phase 1** (`module_phase1_diagnostic.md`) | После Wheel of Life: повторяющаяся жалоба «знаю, что в сфере X плохо — не делаю ничего» | Explicit opt-in: «Я могу помочь понять, почему именно "не делаю". Это COM-B диагностика, 3-5 минут». |
| **Phase 3** (`module_phase3_weekly_review.md`) | Step 9 «Why? Three Whys» — если gap повторяется ≥ 2 недели на той же priority | Escalation: «Это не одноразовая проблема — давай разберём через COM-B». |
| **Routing Map** (SKILL.master.md) | Прямой пользовательский запрос «не понимаю почему не делаю», «как себя заставить», «нет силы воли» | Direct entry в COM-B без обхода через phases. |

---

## Промпт patterns для skill

### Short trigger prompt (Phase 0 soft suggestion)

```
"Слышу: знаешь, что важно — а не делается. Это не про лень и не про силу воли,
обычно. Чаще ломается один из трёх элементов: либо ты не знаешь *как*, либо
среда мешает, либо где-то внутри это не твоё.

Хочешь, разберём за 5 минут через короткую диагностику? Это даст конкретное
направление, куда двигаться — вместо общего «собраться и сделать»."
```

### Full 9-question protocol (Phase 1 / explicit opt-in)

```
"Окей, идём по трём блокам. Не спеши — отвечай как есть, не как "правильно".

Блок 1 — Capability (могу ли я):
1. Есть ли у тебя ресурсы делать это — время, инструменты, тело?
2. Знаешь ли ты *как* именно это делать — конкретные шаги?
3. Если бы я сейчас сказал "сделай первый шаг" — ты знаешь что это?

[Дождись ответов, дай микро-интерпретацию: "Похоже, capability в порядке/тут провал"]

Блок 2 — Opportunity (среда):
4. Что в среде делает это лёгким или сложным?
5. Кто рядом — поддерживает или мешает? Есть accountability?
6. В какой момент дня это легче всего? Регулярно ли он есть?

[Интерпретация]

Блок 3 — Motivation (хочу):
7. От 1 до 10 — насколько это важно сознательно? Почему эта оценка?
8. Хочешь автоматически — или каждый раз уговариваешь?
9. Это твоя цель — или чьи-то ожидания?

[Финальная интерпретация: primary gap = X. Routing: ...]"
```

### Routing prompt после determination

```
"Сложилось: твой primary gap — [Capability / Opportunity / Motivation].

[Если Capability]:
Значит, мотивация и среда в порядке, но не хватает навыка/ясности первого
шага. Идём в Tiny Habits — разобьём до уровня "≤ 30 секунд", чтобы Ability
перестал быть барьером. Загружу habit_loop.md.

[Если Opportunity]:
Хочешь и умеешь — но среда сопротивляется. Тут не про "стараться сильнее", а
про переделать контекст. Идём в environment design — 5-7 практик, как убрать
friction и добавить cues. Загружу environment_design.md.

[Если Motivation]:
Знаешь как, среда нормальная — но в моменте не тянет. Это часто значит,
что цель не выровнена с тем, что ты реально ценишь. Идём в WOOP + Compass,
проверим — твоя ли это цель и есть ли у неё внутренний pull.

Через 1-2 недели вернёмся и проверим — сдвинулось ли."
```

---

## Когда **не** использовать

- **Первая сессия с пользователем** — COM-B опt-in, не primary diagnostic. Нарушает Phase 0 contract «5–10 минут до согласия».
- **Эмоциональный block / crisis state** — сначала Phase 0.5 ER Protocol (`emotion_regulation.md`). COM-B requires cognitive engagement.
- **Нет конкретной цели/поведения** — COM-B диагностирует «почему не делаю *вот это*». Если «вот это» неясно — сначала Phase 2 goal definition.
- **Пользователь устал / hostile к структуре** — Reduce to one question: «Если убрать всё лишнее — что главное мешает: не знаешь как, среда давит, или внутри не хочется?»
- **Поведение разовое, не повторяющееся** — COM-B про паттерны бездействия. Для одного решения — overkill.

---

## Cross-references

- **`action_breakdown_template.md`** — primary intervention для Capability gap (декомпозиция до видимого первого шага)
- **`habit_loop.md`** §1 Tiny Habits — Capability gap через B=MAP снижение Ability
- **`environment_design.md`** — primary intervention для Opportunity gap (NEW в v1.2)
- **`module_phase2_goal_architecture.md`** §Layer 5 WOOP — Motivation gap через mental contrasting
- **`module_phase1_5_goal_filter.md`** Compass Mode — Motivation gap через values alignment
- **`implementation_intentions.md`** — coping plans для удержания routing intervention
- **`evidence_map.md`** §COM-B — full evidence citation

---

## TL;DR

COM-B (Michie 2011) — диагностика «почему не делаю» через 3 необходимых компонента: Capability (могу), Opportunity (среда), Motivation (хочу). 9 вопросов за 3–5 минут → primary gap → targeted routing: Capability → Tiny Habits, Opportunity → environment design, Motivation → WOOP/Compass. **Opt-in only**, не primary diagnostic. Заменяет общее «соберись и сделай» на конкретную интервенцию по слабейшему звену.
