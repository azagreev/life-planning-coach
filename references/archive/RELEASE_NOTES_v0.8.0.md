## Что нового в v0.8.0

### 🔄 Habit Loop Framework
Мост между целями и ежедневными действиями. Скилл теперь помогает не только ставить цели, но и выстраивать привычки, которые ведут к ним.

**5 методик в одном протоколе:**
- **Cue-Routine-Reward** (Duhigg) — карта привычек: что запускает, что происходит, какая награда
- **Tiny Habits** (Fogg) — начинать с 30 секунд, привязать к якорю, праздновать сразу
- **Habit Stacking** (Clear) — «После утреннего кофе я открою документ»
- **Timeline** (Lally) — реалистичные ожидания: медиана 66 дней, не 21
- **Identity** (Clear) — «Я бегун» вместо «я хочу бегать»

Интеграция с WOOP, календарём, Energy Scheduling, Recovery Protocol и Win Alert.

### 📋 Task Breakdown with Checkpoints
WOOP создаёт намерение. Task Breakdown превращает его в выполнимые шаги.

Каждый шаг:
- ≤30 минут или с бинарным критерием
- Имеет чекпоинт: ✓ «что значит 'готово'?»
- Оценивается по времени с буфером

Opt-in: только для конкретных доменов (Карьера, Финансы, Здоровье, Дом, Обучение).

### 📊 Markdown Tables as UI
4 структурированных шаблона для визуализации прогресса:
- **Weekly Plan** — приоритеты по дням
- **Wheel of Life Review** — 11 сфер + динамика + одно действие
- **Progress Check** — OKR-style отслеживание
- **Course Correction** — что начать, остановить, продолжить

Stage-appropriate: только для Preparation и Action. Для Precontemplation/Contemplation — слишком рано.

### 🎯 Weak Goal Taxonomy + Sanity-Check
Расширение фильтра аутентичных целей (Stage 1.5). Теперь проверяются не только red flags, но и паттерны слабых целей:
- **Vague** — слишком размыто
- **Output-as-Outcome** — цель = результат, не поведение
- **Missing Baseline** — нет точки отсчёта
- **Sandbagging** — слишком легко
- **Moonshots** — слишком сложно

Sanity-Check по 5 измерениям: Coverage, Balance, Feasibility, Measurability, Alignment.

### 🏷️ Status Icon System
Визуальная нотация прогресса: ⬜🔄✅❌⏸️⚠️

- Текстовый fallback для screen readers
- High N пользователи — opt-in (без стрессовых иконок)
- Только по запросу или в таблицах

### 🧪 Тесты
- 158 passed, 5 skipped, 15 subtests passed
- 34 новых теста на v0.8.0
- Все ограничения соблюдены: SKILL.md ≤500 строк, reference-файлы в рамках бюджетов
