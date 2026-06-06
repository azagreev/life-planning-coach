# Track: Health & Metabolism (opt-in)

> **Tier:** 3 (lazy-load ref)
> **Загружается:** Phase 1 Diagnostic при триггерах «вес», «энергия», «выгорание», «нет дисциплины», «диета», «сон», «питание»; либо явно по запросу пользователя.
> **Предусловие:** Phase 0 Readiness ≥ 6 + opt-in согласие пользователя.
> **Schema:** v2.1+ `diagnosis.health_metabolism.*`
> **PRD:** `docs/research/prd_health_metabolism.md`

---

## Зачем трек

Метаболизм — это **система** с обратными связями (гормоны сытости, кортизол, инсулин), а не вопрос силы воли. Когда пользователь говорит «нет дисциплины» — часто это сигнал, что система рассинхронизирована: лептин/грелин нарушены недосыпом, кортизол поднял аппетит из-за хронического стресса, нет белка/клетчатки для сигнала сытости.

**Рефрейминг:** не «слабая воля», а «нет сигнала из-за сломанного контура». Контур чинится по рычагам ниже.

**Ограничения:** Этот трек **не для расстройств пищевого поведения**. При признаках РПП (ограничительное питание, циклы binge-purge, навязчивые мысли о теле) → загрузи `references/emotion_regulation.md` и рекомендуй специалиста.

---

## 7 рычагов (по убыванию доказательной базы)

### 1. Сон (high priority)

**Механизм:** Недосып → ↓ лептин (гормон сытости) + ↑ грелин (гормон голода) → переедание (+300-500 ккал/день).
**Evidence:** Spiegel et al. 2004, *Annals of Internal Medicine*.
**Targets:** 7-9 часов; стабильное время засыпания (±30 мин); тёмная прохладная спальня.
**Запиши в state:** `sleep_quality (1-10)`, `sleep_hours`.

### 2. Стресс (high priority)

**Механизм:** Хронический стресс → ↑ кортизол → тяга к high-calorie comfort foods + abdominal fat storage.
**Evidence:** Epel et al. 2001 *Psychoneuroendocrinology*; Sominsky & Spencer 2014 *Frontiers in Psychology*.
**Targets:** Daily de-stress micro-rituals (5-15 мин), `stress_level ≤ 6/10` baseline.
**Запиши в state:** `stress_level (1-10)`.

### 3. Белок (high priority)

**Механизм:** Высокий thermic effect + длинная сытость (ускоряет высвобождение PYY/GLP-1). Снижает спонтанное потребление на ~10-15 %.
**Evidence:** Leidy et al. 2015 *AJCN*; Westerterp-Plantenga et al. 2006 *Int J Obesity*.
**Targets:** ~0.8-1.2 г/кг веса в день (для активных — до 1.6 г/кг). 25-40 г белка на каждый приём пищи.
**Запиши в state:** `protein_target_met (bool)`.

### 4. Клетчатка (high priority)

**Механизм:** Растворимая клетчатка ферментируется в кишечнике → ↑ короткоцепочечные жирные кислоты → ↑ GLP-1, PYY → сытость. Нерастворимая увеличивает объём пищи.
**Evidence:** Wanders et al. 2011 *Obesity Reviews*; Slavin 2005 *Nutrition*.
**Targets:** 25-30 г/день из овощей, фруктов, цельнозерновых, бобовых.
**Запиши в state:** `fiber_target_met (bool)`.

### 5. Тщательное жевание (medium priority)

**Механизм:** Каждый дополнительный укус (≥ 30 пережёвываний) → ↑ гормоны сытости + время для центрального сигнала «я наелся» (~20 мин).
**Evidence:** Chmiel et al. 2025 *Brain Sciences* (neuroimaging review).
**Targets:** Осознанное жевание ≥ 1 приёма пищи в день, без экранов.
**Запиши в state:** `chewing_awareness (1-10)`.

### 6. Кофеин — тайминг (medium priority)

**Механизм:** Кофеин блокирует аденозин → ↑ бодрость. Период полураспада ~5 часов → кофеин в 15:00 = 50 % всё ещё в крови в 20:00 → нарушает фазы глубокого сна.
**Evidence:** Drake et al. 2013 *Journal of Clinical Sleep Medicine*; Astrup 1990, Dulloo 1989 *AJCN*.
**Targets:** Cut-off за 6-8 часов до сна. Для большинства — последний кофе до 14:00.
**Запиши в state:** `caffeine_cutoff_hour (0-23)`.

### 7. Хлорогеновая кислота (low priority)

**Механизм:** Антиоксидант из зелёного кофе → скромное снижение всасывания глюкозы → -1-2 кг за 12 недель (краткосрочный эффект).
**Evidence:** Kanchanasurakit et al. 2023 *Systematic Reviews* — meta-analysis с умеренной evidence base.
**Targets:** Не первый рычаг. Использовать как добавку к 1-4, а не вместо.

---

## Диагностические вопросы (5-7 мин)

Track A (быстро, 3 вопроса):
1. «Сколько часов спал последнюю неделю в среднем?» (sleep_hours)
2. «Уровень стресса на этой неделе 1-10?» (stress_level)
3. «Что в питании ощущается самым тяжёлым: голод между едой, тяга вечером, переедание стрессом?» (open)

Track B (полно, 5-7 вопросов): + добавь
4. «Белок есть в каждом приёме пищи или большая часть — углеводы?» (protein_target_met)
5. «Сколько порций овощей/фруктов в день?» (fiber_target_met)
6. «До какого часа пьёшь кофе/чай с кофеином?» (caffeine_cutoff_hour)
7. «Сколько обычно времени уделяешь приёму пищи: 10 минут перед экраном или больше?» (chewing_awareness)

---

## Рефрейминг самокритики (3 шаблона)

- «Я не могу остановиться, когда начинаю есть» → «Тело долго не получает сигнал сытости — это лептин/грелин, не сила воли. Что в контуре сейчас сломано: сон, стресс, белок?»
- «Я постоянно хочу сладкое к вечеру» → «Это может быть кортизол после стрессового дня или дефицит белка с утра. Не моральный провал, а биологическая компенсация.»
- «Я не дисциплинирован в питании» → «Контур регуляции аппетита — это не про дисциплину, а про сигналы. Сигналы чинятся 4 рычагами: сон, стресс, белок, клетчатка.»

---

## Микро-эксперименты (3 примера, ≤ 1 неделя, обратимы)

1. **Sleep anchor** (7 дней): фиксированное время в постели ±30 мин. Замер: `sleep_quality` до/после.
2. **Protein-first breakfast** (5 дней): 25-30 г белка на завтрак. Замер: голод в 11:00, тяга к сладкому вечером.
3. **Caffeine cut-off 14:00** (7 дней): последний кофе до 14:00. Замер: время засыпания, `sleep_quality`.

Записывай в `diagnosis.health_metabolism.micro_experiments_log[]`: `{date, lever, hypothesis, outcome, duration_days}`.

---

## Integration touch-points

- **Phase 1 Diagnostic** — opt-in entry при триггерах (см. `module_phase1_diagnostic.md`)
- **Phase 3 Weekly Review** — optional Health Review между Habit Review (step 6) и Reward Audit (step 7): «Как был сон? Стресс? Самое тяжёлое в питании?»
- **Emotion Regulation** (`emotion_regulation.md`) — при разговорах о теле/еде → рефрейминг, а не валидация самокритики
- **State writes** — `diagnosis.health_metabolism.*` (schema v2.1+)

---

## State writes

```jsonc
"diagnosis.health_metabolism": {
  "active": true,                 // активируется на opt-in
  "sleep_quality": 6,             // 1-10
  "sleep_hours": 6.5,             // float
  "stress_level": 7,              // 1-10
  "protein_target_met": false,    // bool
  "fiber_target_met": true,       // bool
  "chewing_awareness": 4,         // 1-10
  "caffeine_cutoff_hour": 16,     // int 0-23
  "last_assessed": "2026-05-28T10:00:00Z",
  "micro_experiments_log": [
    {"date": "2026-05-28", "lever": "sleep", "hypothesis": "fixed time", "outcome": "+1 to quality", "duration_days": 7}
  ]
}
```

---

## Limits & disclaimers

- **Не для РПП.** Если пользователь описывает ограничительное питание, циклы binge-purge, навязчивые мысли о теле/весе — рекомендуй специалиста.
- **Не диета.** Coach не предписывает калорий/макроев. Работает с системой регуляции, а не с потреблением.
- **Coaching, не клиника.** При устойчивых проблемах с питанием/весом — врач/диетолог/психотерапевт.
- **Evidence umbrella:** рычаги 1-4 имеют сильную базу; 5 (жевание) — среднюю; 7 (хлорогеновая) — слабую. Эффекты кофеина и жевания преимущественно краткосрочные.

---

## Refs

- PRD: `docs/research/prd_health_metabolism.md`
- Schema: `references/state_v2_schema.md` §3.4.1
- Phase 1: `references/module_phase1_diagnostic.md` Health Track entry
- Phase 3: `references/module_phase3_weekly_review.md` Health Review step
