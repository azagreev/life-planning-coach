# WoL Health Sub-segments — детальная оценка сферы Здоровье

> **Tier:** 3 (lazy-load ref)
> **Загружается:** Phase 1 Diagnostic — при оценке сферы `health` ≤ 6 ИЛИ explicit user interest в детальном анализе здоровья. NOT loaded for single-score WoL flow (default).
> **Schema:** v2.2.6+ `diagnosis.wheel_of_life.current.health_subsegments`
> **PRD:** `docs/research/prd_health_assessment_wol_subsegments.md` (v1.0, 2026-05-27)
> **Не дублирует:** `track_health_metabolism.md` (v0.19.0) — это deep 7-рычаговый трек; sub-segments здесь — light pre-screening (4-6 вопросов).

---

## Когда использовать

При WoL оценке сферы `health` есть 3 пути:

| Сценарий | Использовать |
|----------|--------------|
| Single-score (default, fast WoL) | Один балл 1-10. `health_subsegments = null`. |
| User shows interest («хочу понять, что именно проседает») | Этот ref — 6 sub-segments + Health Index |
| Health Index ≤ 5.5 ИЛИ user struggles | Этот ref + предложить `health_snapshot.md` (4 вопроса, light) |

**Default — single-score.** Sub-segments — opt-in path для users которые хотят precision. Не навязывай.

---

## 6 суб-сегментов

| ID (canonical) | Russian display | Что оценивается |
|---|---|---|
| `energy` | Энергия и бодрость днём | Стабильность уровня энергии в течение дня |
| `recovery` | Качество восстановления | Насколько хорошо восстанавливается организм |
| `physical_wellbeing` | Физическое самочувствие | Боли, дискомфорт, подвижность, общее состояние |
| `stress_resilience` | Стрессоустойчивость | Уровень стресса и способность им управлять |
| `nutrition` | Питание и самочувствие от еды | Как питание влияет на энергию и самочувствие |
| `reserve` | Общий резерв организма | Скорость восстановления после нагрузок |

Каждый sub-segment — балл **1-10**. Allow `null` если пользователь не хочет/не может оценить.

---

## Health Index

```
Health Index = avg(filled sub-segments)
```

Округлять до одной десятой. Если все 6 заполнены — divide by 6. Если часть `null` (skipped) — divide by N filled. **Минимум 4 sub-segments** заполнены, иначе skip Health Index (использовать single-score path).

### 4 категории

| Health Index | Категория | Действие |
|--------------|-----------|----------|
| 8.0 – 10.0 | Отличный | Поддержка текущих привычек; surface наиболее сильный sub-segment |
| 6.5 – 7.9 | Хороший | Фокус на 1–2 слабых sub-segments; light habit tweak |
| 5.0 – 6.4 | Средний | Предложить Health Snapshot (`health_snapshot.md`) — 4-вопросная light interview |
| ≤ 5.0 | Низкий | Strongly recommend Health Snapshot; затем decision про Health Track (`track_health_metabolism.md`) |

### Weakest sub-segment

Найди min(filled sub-segments). Surface в conversation:
> «По твоим оценкам проседает [weakest_display] ([score]/10). Есть смысл посмотреть глубже?»

Если несколько sub-segments с одинаковым минимумом — выбери по persona priority:
- **ADHD** → `energy` или `recovery`
- **Elder** → `recovery` или `physical_wellbeing`
- **Default** → first match по порядку из таблицы выше

---

## Persona adaptations

Стиль вопросов и подачи зависит от detected persona (см. `mode_*.md`).

### ADHD (`mode_adhd.md`)

- **Стиль:** Короткий, конкретный, минимум текста.
- **Подача 6 sub-segments:** 3 за раз с визуальным таймером.
- **Примеры формулировок:**
  - «Энергия днём — стабильная или скачет? 1-10.»
  - «Восстанавливаешься нормально после стресса? 1-10.»
- **Routing:** Health Index ≤ 5.5 → быстрый переход к Health Track decision (без длинного объяснения).

### Transitional / Unemployed (`mode_unemployed.md`)

- **Стиль:** Эмпатичный, с учётом изменений (декрет, переход карьеры, безработица).
- **Подача:** Свяжи с привычками и рутиной — «Когда меньше структуры, что с энергией днём?»
- **Routing:** ≤ 5.5 → soft offer Health Snapshot («Иногда переход выматывает body — посмотрим конкретно?»).

### Elder homebound (`mode_elder.md`)

- **Стиль:** Простой язык, акцент на восстановление и якори дня.
- **Подача 6 sub-segments:** избирательно (4 ключевых: `energy`, `recovery`, `physical_wellbeing`, `reserve`). Skip `stress_resilience` и `nutrition` если irrelevant.
- **Routing:** Focus на `recovery` и `physical_wellbeing` как entry для conversation про сон / mobility / hydration.

### Planning Friction (`mode_planning_friction.md`)

- **Стиль:** Чёткий, структурированный, с примерами.
- **Подача:** Готовые формулировки на выбор (a/b/c) вместо open-ended.
  - «Энергия днём: (a) стабильная и хватает, (b) есть провалы днём, (c) почти всегда мало?»
- **Routing:** Связь sub-segments с привычками — «Sleep affects recovery and reserve; protein affects energy. Хочешь посмотреть конкретный рычаг?»

---

## State writes

После completed sub-segments scoring запиши в state v2:

```jsonc
"diagnosis": {
  "wheel_of_life": {
    "current": {
      "health": 6.5,                       // Health Index (avg sub-segments) если detailed mode; иначе single-score
      "health_subsegments": {              // v2.2.6+ (null если single-score path)
        "energy": 5,
        "recovery": 7,
        "physical_wellbeing": 8,
        "stress_resilience": 4,
        "nutrition": 7,
        "reserve": 6
      }
      // ...rest of 11 spheres
    },
    "last_assessed_at": "2026-05-28T..."   // обязательно (v1.3.0 frequency gate)
  }
}
```

Полная спецификация — `state_v2_schema.md §3.4.5`.

---

## Routing после Health Index

| Категория | Next |
|-----------|------|
| Отличный (≥ 8) | Surface strongest; continue WoL остальные сферы |
| Хороший (6.5–7.9) | Surface weakest как habit tweak candidate; continue |
| Средний (5.0–6.4) | Offer Light Health Snapshot (`health_snapshot.md` — Sub-feature B, v1.4.x); если decline → continue WoL |
| Низкий (≤ 5.0) | Strongly recommend Health Snapshot ИЛИ Health Track (`track_health_metabolism.md`) — ask user |

---

## Научная база

- **Многомерный wellness:** разделение здоровья на несколько измерений (энергия, восстановление, стресс, физическое состояние) повышает точность самооценки и эффективность targeted изменений.
- **Wheel of Life эффективность:** [The Wheel of Life as a Coaching Tool to Audit Life Priorities (2022)](https://www.researchgate.net/publication/365375169_The_Wheel_of_Life_as_a_Coaching_Tool_to_Audit_Life_Priorities) — улучшение self-insight и motivation для habit change.
- **Subjective measures валидны:** Schultchen et al. (2019) — bidirectional relationship of stress and physical activity. Субъективные оценки энергии / восстановления / стресса коррелируют с реальным поведением и adherence к привычкам.

---

## Не делаем (per PRD §9)

- **Не дублируем `track_health_metabolism.md`** (deep 7-рычаговый трек для users с low score + agreed deep dive).
- **Не создаём тяжёлый опросник** — этот ref максимум 6 вопросов в одной сессии.
- **Не нарушаем WoL Frequency Gate** — sub-segments tied к same `last_assessed_at` timestamp (один WoL = один frequency reset).
- **Не surfaceim Health Index как «балл» / «оценку личности»** — это observability tool, не judgment. Формулировки: «по твоим оценкам проседает X» вместо «у тебя плохое здоровье».
- **Не запускаем automatically** — opt-in path. Default остаётся single-score.

---

## Связанные

- `state_v2_schema.md §3.4.5 health_subsegments` — schema spec
- `module_phase1_diagnostic.md` — loading point (Phase 1 WoL flow)
- `track_health_metabolism.md` — deep 7-рычаговый трек (v0.19.0)
- `health_snapshot.md` — light 4-вопросный tool (Sub-feature B, v1.4.x)
- `mode_*.md` — persona adaptations
- `evidence_map.md` § «WoL Health Sub-segments»
- PRD: `docs/research/prd_health_assessment_wol_subsegments.md`
