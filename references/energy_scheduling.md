# Energy-Based Scheduling

> **When to use:** Пользователь планирует день или неделю, жалуется на усталость, прокрастинирует из-за неправильного тайминга, просит оптимизировать расписание.
> **Integration:** Использует COLOR_MAP из calendar_constants.md. Создаёт события через Google Calendar MCP.

---

## Core Principle

Работайте с энергией, не против неё. Каждый уровень энергии — это данные, а не оценка.

---

## 1. Three Energy Levels

| Level | Signal | Tasks | colorId |
|-------|--------|-------|---------|
| 🟢 HIGH | Лёгкость, фокус | Творческая работа, Deep Work, сложные решения | deep_work |
| 🟡 MEDIUM | Стабильность | Рутина, встречи, email, административные задачи | personal / meeting |
| 🔴 LOW | Тяжесть, заторможенность | Отдых, лёгкие задачи, подготовка, переключение контекста | personal |

---

## 2. Calibration Question

> «Когда ваш пик энергии — утро, день или вечер?»

Ответ определяет, куда ставить фокус-блоки.

---

## 3. Scheduling Heuristics

- Защищайте пиковые часы фокус-блоками (colorId: deep_work)
- При низкой энергии — рутина и встречи (colorId: personal / meeting)
- 15-минутный буфер между переключениями контекста
- Не планируйте Deep Work после тяжёлых встреч

---

## Connection to Existing Features

- **AC-8 Energy Check** — соматический маркер из authentic_goal_filter.md (🟢/🟡/🔴)
- **Seasonal Planning** — циклы Spring/Summer/Fall/Winter в weekly_review.md
- **True Goal Score** — ось «Энергия» (лёгкость = 10, тяжесть = 0)
- **COLOR_MAP** — цвета из calendar_constants.md для визуальной навигации

---

## Anti-patterns

- ❌ Важные задачи в «мёртвой зоне» (после обеда для многих)
- ❌ Встречи подряд без времени на восстановление
- ❌ Игнорировать личные паттерны ради «продуктивности»

---

## Quick Reference

| Energy | colorId | Example |
|--------|---------|---------|
| 🟢 HIGH | deep_work | Написание стратегии, сложный код |
| 🟡 MEDIUM | meeting | Синхронизация, обработка писем |
| 🔴 LOW | personal | Прогулка, чтение, планирование |
