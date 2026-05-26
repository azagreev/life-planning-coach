## Что нового в v0.14.0

### Добавлено
- **`references/adhd_mode.md`** — адаптивный коучинг для executive function (ADHD): C.A.R. метод, 5-Minute Rule, визуальный таймер, time buffer 2×, body doubling, external scaffolding. Opt-in ONLY, MI-aligned, без медицинских советов
- **`references/time_structure_unemployed.md`** — структура дня для безработных и переходных периодов: 4-блочный шаблон, Sharp Hours (9–13), 10 принципов, social anchors, small wins. Без вины/стыда
- **`references/elder_homebound_mode.md`** — коучинг для solo aging с ограниченной мобильностью: нормализация solo aging, микро-якоря, mattering, наследие через память, достоинство в ограничениях (Франкл). Без патронизации
- **`references/planning_friction_audit.md`** — аудит трения в планировании: 7 вопросов, 3 шаблона дня (Deep Work/Meeting/Recovery), smart defaults, 10% Adjustment Rule
- **Persona Detection Hooks** — `SKILL.master.md` Phase 0/1: определение персоны (ADHD / unemployed / elder homebound / planning friction) + адаптации Phase 2/3/5
- **`tests/system/test_v140_features.py`** — 45 тестов (4 reference + persona hooks + platform integration)

### Изменено
- **`SKILL.master.md`** — version 0.13.0 → 0.14.0, persona hooks во всех фазах, 4 новых reference в списке
- **Все platform-файлы** — пересобраны через `build-platform-skill.py all` (Claude, Grok, Kimi, Kimi CLI)
