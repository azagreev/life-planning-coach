# Dashboard Guide (Phase 4 runtime module)

> **Версия:** 2.0  
> **Дата:** 2026-05-26  
> **Statu:** Runtime module — загружается только при триггере «покажи дашборд» / «визуализируй прогресс».  
> **Heavy архитектурный doc (2538 строк):** перенесён в [docs/research/dashboard_architecture_v1.md](../docs/research/dashboard_architecture_v1.md) — dev-only, не загружается в runtime.

---

## Когда загружать этот файл

Триггеры Phase 4:
- «покажи дашборд», «визуализируй прогресс», «открой дашборд», «html-дашборд»
- После Weekly Review при наличии полного state v2
- При запросе экспорта прогресса в PDF

## Что делать

1. **Прочитай** текущий state v2 из conversation memory или Drive Wiki (`03_Dashboard/dashboard_data.json`)
2. **Сгенерируй** HTML, используя шаблон [`life-planning-dashboard.html`](../life-planning-dashboard.html)
3. **Инжектируй** state v2 как `window.lpData = { ... }` ПЕРЕД основным `<script>` блоком
4. **Сохрани** в файл и предложи открыть в браузере (работает offline)
5. Если режим `full_persistence` — обновить `03_Dashboard/dashboard_data.json` в Drive

## Injection протокол

Дашборд — stateless view. Вся логика на стороне HTML. Skill инжектит данные:

```html
<!-- Перед основным <script> блоком вставь: -->
<script>
window.lpData = {
  "schema_version": "2.0",
  "wheel_of_life": {
    "current": { "health": 7, "finances": 5, ... },  // 11 canonical spheres
    "previous": { ... },
    "targets":  { ... },
    "sphere_goals": { "health": [{title, progress, status}, ...], ... }
  },
  "core_values": [
    { "value_id": "CV1", "name": "Autonomy", "compass_question": "...", "priority_rank": 1 }
  ],
  "execution_scores": [{ week, planned, done, score, current?, future? }, ...],
  "velocity": [{ week: "W1", planned, completed }, ...],
  "streaks":  [{ category, label, current, best, status, icon }, ...]
  // Optional (schema 2.1+):
  // "health_metabolism": { sleep_avg_hours, stress_level, protein_target_g, fiber_target_g, caffeine_cutoff_time }
  // Optional (schema 2.2+):
  // "goal_filter": { "active_goals": [{ goal_id, title, partner_coordination: { communication, cooperation, compatibility } }] }
};
</script>
```

Если `window.lpData` не инжектится — HTML рендерит `SAMPLE_FALLBACK` (sample preview). Skill всегда должен инжектить реальные данные.

## Canonical 11 spheres

| ID | Display | Icon |
|---|---|---|
| `health` | Здоровье | 💚 |
| `finances` | Финансы | 💰 |
| `career` | Карьера | 💼 |
| `family` | Семья | 👨‍👩‍👧 |
| `romance` | Отношения с партнёром | 💕 |
| `social` | Дружба | 🤝 |
| `personal_growth` | Личностный рост | 📚 |
| `meaning` | Смысл и духовность | 🧘 |
| `fun_recreation` | Отдых и хобби | 🎉 |
| `contribution` | Вклад | 🌍 |
| `physical_environment` | Дом и среда | 🏠 |

**Запрещено** использовать legacy: `growth`, `spirituality`, `fun`, `environment`. Если в state встречаются — это v1 данные, требуется миграция (см. `state_v2_schema.md` §8).

## Структура дашборда (3 таба)

| Tab | Содержит | Источник из state v2 |
|---|---|---|
| **Overview** | Activity Rings (OKR), Sphere Grid (11), Core Values Compass, Weekly Priorities, Streaks | `wheel_of_life`, `core_values`, `weekly_priorities`, `streaks` |
| **Retrospective** | Confidence Gauges, Heatmap, 12W Tracker, Velocity, Burndown | `weekly_reviews`, `execution_scores`, `velocity` |
| **Goals** | WOOP cards, BHAG Roadmap, OKR cards | `goals.bhag`, `goals.daily_woop`, `goals.twelve_week_okr` |

## Schema version compatibility

Дашборд поддерживает `2.x` через additive bumps:
- `2.0` — baseline (11 spheres, core_values)
- `2.1` — добавит `health_metabolism` (Health Track panel станет видимой)
- `2.2` — добавит `partner_coordination` в active_goals (Concordance panel станет видимой)

Major bump `3.0` — потребует нового шаблона.

## Fallback и graceful degradation

Если skill не может сгенерировать HTML (terminal-only, нет файловой системы):
- Загрузи `references/templates/Progress_Dashboard.md` — text-mode dashboard
- Заполни шаблон тем же state v2
- Предложи пользователю скопировать в заметки

## Paper Coach Mode

Когда нет ни HTML, ни persistence:
- Используй `Progress_Dashboard.md` шаблон
- Минимальный set: топ-3 цели + Wheel of Life snapshot + 3 wins за неделю
- Объясни: «В этом режиме дашборд — текстовый. Скопируй в заметки.»

## Связанные документы

- [state_v2_schema.md](state_v2_schema.md) — canonical schema, single source of truth
- [life-planning-dashboard.html](../life-planning-dashboard.html) — runtime template (v1.0.0)
- [templates/Progress_Dashboard.md](templates/Progress_Dashboard.md) — text-mode fallback
- [docs/research/dashboard_architecture_v1.md](../docs/research/dashboard_architecture_v1.md) — полная архитектура (dev-only, 2538 строк)
- [research/plan_v1.0_templates_rebuild.md](research/plan_v1.0_templates_rebuild.md) — план rebuild
