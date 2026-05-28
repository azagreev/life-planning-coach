# Health Snapshot — лёгкий 4-вопросный инструмент

> **Tier:** 3 (lazy-load ref)
> **Загружается:** Phase 1 после WoL Health Index ≤ 5.5 (см. `wol_health_subsegments.md` routing) ИЛИ explicit user request ИЛИ Phase 3 opt-in (Sub-feature C v1.4.x).
> **Schema:** v2.2.7+ `diagnosis.health_snapshot.last`
> **PRD:** `docs/research/prd_health_assessment_wol_subsegments.md` §4 (v1.0)
> **Не дублирует:** `track_health_metabolism.md` (v0.19.0, deep track) — Snapshot тоньше: 4 вопроса вместо 7-рычаговой системы. Snapshot decides **whether** to enter Health Track.

---

## Когда запускать

| Сценарий | Запуск |
|----------|--------|
| Health Index ≤ 5.5 после WoL detailed (sub-segments mode) | Auto-offer: «По твоим оценкам ... есть смысл посмотреть глубже?» |
| User explicit request («расскажи про здоровье», «как у меня с энергией?») | По запросу |
| Phase 3 Weekly Review opt-in (Sub-feature C v1.4.x) | После Step 4 Reflect, если `health` сфера упоминается |

**2-decline cutoff per session:** если пользователь отказался 2 раза в одной сессии → не предлагай больше. Increment `health_snapshot.last.declined_count` при каждом отказе.

---

## 4 вопроса

Каждый — балл **1-10**. Allow skip (null).

| # | Вопрос (default formulation) | ID | Что оценивает |
|---|------------------------------|-----|---------------|
| 1 | «Насколько стабильным был твой уровень энергии за последние 7–10 дней?» | `energy_stability` | Energy stability over 7-10 day window |
| 2 | «Насколько хорошо ты восстанавливаешься (сон + общее самочувствие)?» | `recovery` | Recovery quality (sleep + general) |
| 3 | «Насколько стресс влияет на тебя сейчас и насколько ты им управляешь?» | `stress_management` | Current stress impact + management capacity |
| 4 | «Насколько быстро ты приходишь в норму после нагрузки или сложного периода?» | `resilience` | Bounce-back speed after load/hard period |

---

## Snapshot Index

```
Snapshot Index = avg(filled answers)   // round to one decimal
```

Минимум **3 из 4** вопросов заполнены, иначе skip Index (записывай `average_score: null`, но `weakest_question` всё равно можно identify).

### Weakest question

`weakest_question = min(filled answers).id`. Surface в conversation:
> «По твоим оценкам проседает [weakest_display] ([score]/10). Есть смысл посмотреть более targeted трек по метаболизму. Хочешь?»

---

## 4 категории + routing

| Snapshot Index | Категория | Next action |
|----------------|-----------|-------------|
| 8.0 – 10.0 | Отличный | Acknowledge; continue без offer Health Track |
| 6.5 – 7.9 | Хороший | Surface weakest как habit tweak candidate |
| 5.0 – 6.4 | Средний | Strongly offer Health Track (`track_health_metabolism.md`) |
| 1.0 – 4.9 | Низкий | Strongly offer Health Track; **safety**: если ВСЕ ответы ≤ 3 → SKILL.master Safety section (depression screen pattern + рекомендация специалиста) |

### Universal формулировка после Snapshot

> «По твоим оценкам проседает [weakest_display] ([score]/10). Есть смысл посмотреть более targeted трек по метаболизму. Хочешь?»

Если пользователь соглашается → load `track_health_metabolism.md` + set `health_metabolism.active = true`. Если отказался → respect, continue WoL/Phase 1 без friction.

---

## Persona adaptations (per PRD §5)

### ADHD (`mode_adhd.md`)

- **Стиль:** Минимум текста. 4 вопроса одним блоком, allow skip любого.
- **Подача:** «Быстрый health snapshot — 4 вопроса, 1-10 каждый. Skip любой если не знаешь. Поехали?»
- **Routing:** ≤ 6 → быстрый переход в Health Track без длинного объяснения.

### Transitional / Unemployed (`mode_unemployed.md`)

- **Стиль:** Эмпатичный, с учётом изменений (декрет, переход карьеры, безработица).
- **Подача:** Свяжи с привычками и рутиной — «Иногда переход выматывает body, давай посмотрим конкретно. 4 вопроса».
- **Reword Q3** (stress): «Сейчас особый период — насколько стресс пробивает структуру дня?»
- **Routing:** Soft offer Health Track, не давить.

### Elder homebound (`mode_elder.md`)

- **Стиль:** Простой язык, акцент на восстановление и якори дня.
- **Подача 4 вопросов:** медленнее, по одному за раз; allow recall help («подумай о вчера и позавчера»).
- **Reword Q3** (stress): «Что больше всего истощает на этой неделе?»
- **Routing:** Фокус на energy + recovery как entry для conversation про сон / гидратацию / mobility.

### Planning Friction (`mode_planning_friction.md`)

- **Стиль:** Чёткий, структурированный, с примерами (a/b/c для каждого вопроса).
- **Подача Q1 example:**
  - «Энергия за 7-10 дней: (a) стабильная и хватает, (b) есть провалы днём, (c) почти всегда мало?»
- **Routing:** Связь sub-segments с привычками — «Sleep affects recovery; protein affects energy. Хочешь посмотреть конкретный рычаг?»

---

## State writes

После completed Snapshot (даже частичного — ≥ 1 ответ):

```jsonc
"diagnosis": {
  "health_snapshot": {
    "last": {
      "date": "2026-05-28",                  // ISO date
      "average_score": 5.3,                  // 1-10 (null если < 3 filled)
      "weakest_question": "stress_management", // canonical ID
      "answered_count": 4,                   // 1-4
      "declined_count": 0                    // session-level: incremented per decline
    }
  }
}
```

См. `state_v2_schema.md §3.4.6` для полной спецификации.

**Frequency note:** Snapshot **не** связан с WoL Frequency Gate (`last_assessed_at`). Snapshot можно запускать чаще (например, monthly check-in через Phase 3 opt-in) — это lighter touch, отдельный кадет от полного WoL.

---

## Routing after Snapshot

| Snapshot Index | Если пользователь хочет deep dive | Если отказался |
|----------------|----------------------------------|-----------------|
| < 5.0 | Load `track_health_metabolism.md` → activate Health Track. **Safety:** проверь ВСЕ ≤ 3 → escalate. | Acknowledge; soft note про availability later. Increment `declined_count`. |
| 5.0–6.4 | Same as above если соглашается | Continue WoL / Phase 1 без friction. Increment `declined_count`. |
| 6.5–7.9 | Habit tweak suggestion (light, weakest-targeted) | Continue. No decline tracking (offer is soft). |
| ≥ 8.0 | No offer — acknowledge strength | Continue. |

---

## Научная база

- См. `wol_health_subsegments.md §«Научная база»` — same evidence base (Wheel of Life 2022 + Schultchen 2019).
- **Short questionnaires reduce friction without losing signal:** PHQ-2 / GAD-2 patterns в behavioral health screening валидированы как effective gating tools перед full assessments. 4-вопросный Snapshot — same paradigm для wellness self-assessment.

---

## Не делаем (per PRD §9)

- **Не дублируем `track_health_metabolism.md`** — Snapshot decides whether to enter that track, не competes с ним
- **Не создаём тяжёлый опросник** — strict 4 questions, allow skip любого
- **Не запускаем automatically** без trigger (≤ 5.5 OR explicit request OR Phase 3 opt-in)
- **Не surfaceim Snapshot Index как «балл / оценку личности»** — это observability tool, не judgment
- **Не нарушаем 2-decline cutoff** — respects user autonomy; second decline → no more offers в этой session
- **Не запускаем без WoL Frequency Gate respect** для full WoL — Snapshot separate, но это не excuse для частого full re-assessment

---

## Safety escalation

Если **ВСЕ 4 ответа ≤ 3** ИЛИ Q3 (stress) ≤ 2 + Q4 (resilience) ≤ 2:
- **НЕ оффер** Health Track автоматически
- Surface concern softly: «Звучит как тяжёлый период. Это коучинг, не терапия — если устойчиво тяжело, есть смысл поговорить со специалистом.»
- См. `SKILL.master.md` § Safety & Ethics → low-score escalation pattern.

---

## Связанные

- `wol_health_subsegments.md` (Sub-feature A v1.4.0) — entry point for low-score routing → Snapshot
- `track_health_metabolism.md` (v0.19.0) — deep 7-рычаговый трек, activated post-Snapshot если user agrees
- `state_v2_schema.md §3.4.6 health_snapshot.last` — schema spec
- `mode_*.md` — persona adaptations
- `evidence_map.md` § «WoL Health Sub-segments» — shared evidence
- PRD: `docs/research/prd_health_assessment_wol_subsegments.md` §4
