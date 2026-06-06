# Premortem (Klein) — выявление рисков через prospective hindsight

> **Tier:** 3 (lazy-load deep reference)
> **Загружается:** Phase 2 для важных OKR (confidence ≤ 6 или horizon ≥ 1 год); explicit запрос «что может пойти не так»; mid-quarter check при stagnation.
> **Связанные refs:** `implementation_intentions.md` §Coping plans (mitigation pattern), `module_phase2_goal_architecture.md` §Premortem Trigger, `evidence_map.md` §Premortem, `emotion_regulation.md` (closing self-compassion если упражнение давит эмоционально).

---

## Что это

**Premortem** — техника prospective hindsight: представь, что цель уже провалена, и объясни *почему*. Перевёрнутая логика postmortem: вместо разбора post-факта работаем с проекцией будущего. Это снимает блок «слепого оптимизма», который мешает увидеть реальные риски на этапе планирования.

В отличие от обычного risk analysis («перечисли возможные риски»), Premortem использует **future-perfect frame**: «прошло 3 месяца, цель провалена — теперь объясни». Этот сдвиг времени снимает defensive thinking и достаёт причины, которые в обычном планировании остаются невидимыми.

---

## Evidence base

> **Источник:** Klein, G. (2007). Performing a Project Premortem. *Harvard Business Review*. [Статья](https://hbr.org/2007/09/performing-a-project-premortem)
>
> **Theoretical backing:** prospective hindsight literature (Mitchell, Russo & Pennington 1989) — представление события как уже случившегося повышает способность генерировать причины на **~30%** vs forward-looking планирование.
>
> **Что это значит на практике:** Premortem за 10–15 минут типично достаёт 2–4 риска, которые не появляются в обычной planning беседе. Эти риски не «новая информация» — пользователь их знал, но не озвучивал, потому что forward-frame активирует confirmation bias и optimism.

### Почему it works (механизм)

1. **Снимает defense mechanism** — «если бы провалилось» psychologically безопаснее чем «как может провалиться» (не обвинение, а thought experiment).
2. **Активирует concrete reasoning** — мозг описывает конкретный sequence событий, не abstract категории риска.
3. **Generates mitigations naturally** — для каждой причины мозг сразу предлагает контр-меру (the next obvious thought).
4. **Mitigation через Implementation Intentions** — каждый identified risk → coping plan в формате if-then. Это и есть критическая связка с уже существующим `implementation_intentions.md` §Coping plans.

---

## Когда применять (explicit gates)

Premortem — **не для каждой цели**. Это диагностика важных goals, иначе превращается в overhead. Запускай при выполнении хотя бы одного gate:

| Gate | Триггер |
|------|---------|
| **Low confidence** | 12-Week OKR с `confidence_score ≤ 6` (см. KR Quality Check) |
| **Long horizon** | BHAG (10–25 лет) или Life Theme (1–3 года) — высокая uncertainty по умолчанию |
| **Partner coordination** | Цель с заполненным `partner_coordination` блоком (зависит от другого человека) |
| **Explicit request** | Пользователь сам спрашивает «что может пойти не так» / «риски» |
| **Mid-quarter stagnation** | На Phase 3 Weekly Review цель показывает прогресс < 30% после 6+ недель (escalation) |

**НЕ применять** для daily WOOP / weekly priorities — overkill. Эти уровни уже имеют obstacle/coping plan в WOOP-формате.

---

## Протокол (5 шагов, 10–15 минут)

Веди упражнение неспешно. Не сваливайся в «список рисков» — держи time-travel frame на всех 5 шагах.

### Step 1 — Time travel framing (1 мин)

> «Закрой глаза на 10 секунд. Представь: прошло [3 месяца / 1 год — горизонт OKR]. Цель провалена. Не "почти получилось" — провалена. Что чувствуешь? Какой первый образ?»

Зафиксируй reaction (эмоция + первый образ). Это якорь для упражнения — возвращайся к нему, если пользователь сваливается в abstract.

### Step 2 — Brainstorm 5 reasons (5 мин)

> «Теперь объясни, *почему* провалилось. Минимум **5 причин**. Не цензурируй — чем "глупее" причина, тем ценнее. "Я просто забил" — это причина. "Заболел в январе" — это причина. "Партнёр расстроился и я съехал" — причина.»

**Правило:** не меньше 5, лучше 7–8. Первые 2–3 — поверхностные. Реальные insights приходят на 4–6 причине, когда поверхностный список исчерпан.

### Step 3 — Cluster reasons по категориям (2 мин)

Сгруппируй причины в 5 типов (это даёт structural picture):

| Категория | Что включает |
|-----------|---------------|
| **Internal obstacles** | Привычки, мотивация, самосаботаж, прокрастинация |
| **External obstacles** | События вне контроля: болезнь, работа, семья, экономика |
| **Missed inputs** | Не было информации/навыка/ресурса; не консультировался |
| **Scope creep** | Цель распухла, добавились side-projects, потеряли focus |
| **Motivation drift** | Цель перестала быть актуальной/важной; смена приоритетов |

Distribution показывает где лежит главная уязвимость. Чисто Internal → COM-B Capability/Motivation. Чисто External → planning buffer / contingency. Motivation drift → re-check Phase 1.5 (authentic goal filter).

### Step 4 — Mitigation через Implementation Intentions (5 мин) ⭐ critical

Возьми **top-3 risks** (самые вероятные × самые impact). Для каждой — coping plan в формате if-then. Это прямой переход в `implementation_intentions.md` §Coping plans.

**Шаблон:**
> «Если [precisely момент когда риск проявится], то я [конкретное действие — не "постараюсь", а исполняемое].»

**Примеры:**
- Risk: «забил после двух плохих недель»
  → Coping plan: «Если пропущу 2 недели подряд, то открою premortem.md → Step 5 запись и переоценю scope.»
- Risk: «партнёр расстроится из-за времени на цель»
  → Coping plan: «Если партнёр озвучит недовольство, то я не защищаюсь — назначаю 30 мин разговор в течение 48 часов и пересматриваю partner_coordination.»
- Risk: «scope раздуется на середине квартала»
  → Coping plan: «Если в week 6 review я добавил > 1 нового KR — drop самый новый или пересмотри cycle.»

**Каждая mitigation = одна записанная II.** Не «учту риски» — конкретный if-then.

### Step 5 — State writes + next review (1 мин)

Зафиксируй Premortem в state (см. §State writes ниже). Назначь **next_review_date** — обычно середина OKR cycle (week 6 для 12-week). На этом review проверяем: realизовался ли какой risk, сработал ли coping plan.

---

## Промпт patterns для skill

### Trigger prompt (для OKR с confidence ≤ 6)

```
"Confidence у этой цели — 6 (или ниже). Это не плохо — это сигнал, что есть
unaddressed риски. Прежде чем планировать execution, давай 10 минут на
Premortem. Это не negative thinking — это диагностика, которая обычно
вытаскивает 2-3 риска, которые ты знал, но не озвучил.

Готов? Если да — закрой глаза на 10 секунд и представь: прошло 3 месяца,
цель провалена. Что чувствуешь? Какой первый образ?"
```

### Mitigation prompt (Step 4)

```
"У нас [N] рисков. Возьмём top-3 — те, что одновременно высоковероятны и
сильно бьют по цели. Для каждого — coping plan в формате if-then.

Не «постараюсь учесть». Конкретное действие: 'Если [precisely момент], то я
[конкретный response]'. Это то же, что мы делали в WOOP step 4 — теперь
применяем к рискам.

Какой риск первый?"
```

### Mid-quarter escalation prompt (Phase 3)

```
"Цель идёт медленнее, чем планировали — прогресс [X]% после [N] недель.
Это нормальный момент для Premortem не-постфактум. Не "что пошло не так",
а "если я ничего не изменю — что будет к концу квартала?"

Пройдём 5 шагов за 10-15 мин и достанем 2-3 specific риска. Готов?"
```

---

## Когда **не** использовать

- **Daily WOOP / weekly priorities** — WOOP уже содержит obstacle/plan, Premortem дублирует. Overkill.
- **Эмоциональный block / depressive state** — упражнение представления провала может ухудшить состояние. Сначала ER protocol (`emotion_regulation.md`). После — закрывай Premortem **Self-Compassion Break** ритуалом.
- **Нет конкретной цели** — Premortem требует measurable target. Если цель в формате «хочу больше энергии» — сначала Phase 2 → SMART-ish formulation.
- **Перфекционист с высокой тревожностью** — для них Premortem может стать новым источником ruminating. Используй upfront opt-in и short version (3 risks вместо 5).
- **Цель уже завершена** — это postmortem, не premortem. Используй AAR (Phase 3 Weekly Review, шаги 8–9).

---

## State writes

В конце Premortem запиши:

`goals.premortem_assessments[]`: append:
```json
{
  "premortem_id": "PM1",
  "goal_id": "O1",              // ссылка на 12-Week OKR objective
  "conducted_at": "2026-05-27T15:30:00Z",
  "trigger": "low_confidence",  // "low_confidence"|"long_horizon"|"partner_coord"|"explicit_request"|"mid_quarter_stagnation"
  "top_risks": [
    {
      "risk": "забил после двух плохих недель",
      "category": "internal",   // "internal"|"external"|"missed_inputs"|"scope_creep"|"motivation_drift"
      "mitigation_intention": "Если пропущу 2 недели подряд, то открою premortem.md → Step 5 запись и переоценю scope."
    }
  ],
  "next_review_date": "2026-07-08"   // середина OKR cycle, или week 6 для 12-week
}
```

См. `state_v2_schema.md` §3.5.1 (schema v2.2.3+) для full документации.

---

## Cross-references

- **`implementation_intentions.md`** §Coping plans — critical mitigation pattern (Step 4)
- **`module_phase2_goal_architecture.md`** §3 12-Week Quarter — trigger по confidence ≤ 6
- **`module_phase3_weekly_review.md`** — mid-quarter escalation trigger (after PR3 lean AAR)
- **`emotion_regulation.md`** — Self-Compassion Break как closing ritual
- **`evidence_map.md`** §Premortem — full evidence citation

---

## TL;DR

Premortem (Klein 2007) — 5-step упражнение через future-perfect frame: «прошло 3 мес., цель провалена — объясни». За 10–15 мин достаёт 2–4 риска, не появляющихся в обычном планировании. Mitigation = coping plans через `implementation_intentions.md`. Применять для важных OKR (confidence ≤ 6 / horizon ≥ 1y / partner_coord), не для daily WOOP. Closing self-compassion при эмоциональной нагрузке.
