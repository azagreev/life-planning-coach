---
schema_version: "2.0"
template_version: "2.0"
last_updated: "YYYY-MM-DD"
purpose: "Text-mode dashboard для Paper Coach Mode (когда HTML недоступен)"
mode: "text_fallback"
---

# 📊 Прогресс — Life Planning Coach (text-mode)

> **Это text-fallback дашборда** для платформ без HTML rendering (terminal, Paper Coach Mode, печать).  
> HTML-версия живёт в репозитории как `life-planning-dashboard.html` и читает `03_Dashboard/dashboard_data.json`.

> Автообновляется. Последнее обновление: [YYYY-MM-DD HH:MM]

---

## 🧭 Snapshot

```
👤 Persona:        [active_mode]
📅 Phase:          [N] / Track: [quick|deep]
📊 Avg readiness:  [N.N]/10 (за сессию)
🎯 Активных целей: [N]    🏆 Wins за 7 дней: [N]
🔄 Привычек (on_track / total): [N] / [N]
```

---

## 🧭 Core Values (топ-5-7)

| # | Value | Compass question |
|---|---|---|
| 1 | [Name] | *[question]* |
| 2 | [Name] | *[question]* |
| 3 | [Name] | *[question]* |

> Полный compass — `Core_Values_Compass.md`

---

## 🎯 Активные цели (топ-5)

| # | Цель | Сфера | Прогресс | AGF (avg) | Дедлайн | Статус |
|---|------|-------|----------|-----------|---------|--------|
| G1 | [название] | `[sphere_id]` | ████████░░ 40% | 8.2/10 | [дата] | 🟡 В процессе |
| G2 | [...] | `[sphere_id]` | ████░░░░░░ 20% | 7.0/10 | [дата] | 🟡 |

---

## 📊 Wheel of Life (11 spheres, canonical)

```
🏥 health                ████████░░░░░░░░░░░░  [N]/10  [▲▼➡️] [±N]
💰 finances              ██████░░░░░░░░░░░░░░  [N]/10
💼 career                ██████░░░░░░░░░░░░░░  [N]/10
👨‍👩‍👧 family                ███████░░░░░░░░░░░░░  [N]/10
💕 romance               ██████████░░░░░░░░░░  [N]/10
🤝 social                ██████░░░░░░░░░░░░░░  [N]/10
📚 personal_growth       ██████░░░░░░░░░░░░░░  [N]/10
🧘 meaning               █████░░░░░░░░░░░░░░░  [N]/10
🎉 fun_recreation        ███░░░░░░░░░░░░░░░░░  [N]/10
🌍 contribution          █████░░░░░░░░░░░░░░░  [N]/10
🏠 physical_environment  ████████░░░░░░░░░░░░  [N]/10
─────────────────────────────────────────────
📊 Средний:              ██████░░░░░░░░░░░░░░  [N.N]/10  [▲▼➡️] [±N.N]
```

🔥 **Суперсила:** [emoji] [sphere] ([N]/10)  
🌱 **Точка роста:** [emoji] [sphere] ([N]/10)

---

## 🔄 Привычки (Habit Loop)

| Habit | Streak (current/best) | Status | Last completed |
|---|---|---|---|
| H1: [name] | [N] / [N] дней | 🟢 / 🟡 / 🔴 | [дата] |

---

## 📈 12-Week OKR (квартал)

**Objective:** [...]  
**Прогресс:** ████████░░ [N]% — `[on_track|at_risk|off_track]`  
**Confidence:** [N]/10

| KR | Текущее → Цель | Прогресс |
|----|----------------|----------|
| KR1: [...] | [X] → [Y] | ████░░ [N]% |

---

## 💭 Daily WOOP (активная)

- 🌟 **Wish:** [...]
- 🎯 **Outcome:** [...]
- 🚧 **Obstacle:** [...]
- 🛡️ **Plan:** *Если* [...], *то* [...]

---

## 💡 Инсайт недели

> «[инсайт]»

---

## 📅 Ближайшие события (calendar_events_log)

- **[YYYY-MM-DD HH:MM]**: [event_title] (`[event_type]`)

---

## 🏆 Победы за 7 дней (топ-5)

- [YYYY-MM-DD]: [победа] (G[N], `[category]`)

---

## 🛡️ Emotion Regulation за период

- Последний протокол: `[reappraisal|grounding|self_compassion]` от [дата]
- Outcome readiness после: [N]/10

---

## 🔄 Persistence

- Drive: [✓ connected | ⚠ retry | ✗ disconnected]
- Calendar: [✓ | ⚠ N pending | ✗]
- Mode: [`full_persistence` | `wiki_no_execution` | `execution_no_wiki` | `lean_conversation`]

---

[Открыть HTML-дашборд](../../life-planning-dashboard.html) (если поддерживается платформой)  
[Открыть Wiki](Index.md)
