---
schema_version: "2.0"
template_version: "2.0"
purpose: "Compact session-start cache, читается первым. < 1000 токенов."
---

# Hot Cache

> **Для Claude:** Читай ПЕРВЫМ при старте сессии с Drive. Цель ~500 слов / < 1000 токенов.
> Записывается в конце каждой сессии через `save_state("Hot_Cache", <full snapshot>)` — new file `Hot_Cache_{ISO}.md`, "current" = latest by `modifiedTime`. См. [`AI_Instructions.md` §Протокол записи](AI_Instructions.md).

## 👤 Контекст пользователя

- **Активный режим:** [`none` | `adhd` | `unemployed` | `elder` | `planning_friction`]
- **Текущая фаза:** [`0` | `0.5` | `1` | `1.5` | `2` | `3` | `4` | `5`]
- **Трек диагностики:** [`quick` | `deep` | —]
- **Стиль коммуникации:** softness=[soft/neutral/direct], structure=[high/medium/low], intensity=[nurturing/exploratory/collaborative/challenging]
- **Readiness среднее за сессию:** [N]/10
- **Дней с последней сессии:** [N]

## 🧭 Core Values (топ-3)

1. **[Name]** — *[compass question]*
2. **[Name]** — *[compass question]*
3. **[Name]** — *[compass question]*

> Полный список — `Core_Values_Compass.md`. Используй для daily decision making и AGF.

## 🎯 Активные цели (топ-3 по приоритету)

1. **[G1]** [название] — [прогресс]%, дедлайн: [дата], values_alignment: [CV1, CV3]
2. **[G2]** [название] — [прогресс]%, дедлайн: [дата]
3. **[G3]** [название] — [прогресс]%, дедлайн: [дата]

## 🧠 Текущий фокус

- **Неделя [N] из 12:** [тема недели]
- **Главное препятствие:** [obstacle из активного WOOP]
- **Стратегия:** [if-then plan]

## 💡 Инсайты последней сессии (топ-2)

- «[инсайт 1]»
- «[инсайт 2]»

## 🛡️ Active Emotion Protocols

> Если последняя сессия включала Phase 0.5 ER protocol:

- Последний протокол: [`reappraisal` | `grounding` | `self_compassion`] от [дата]
- Outcome readiness: [N]/10
- Текущая ситуация: [stable | needs follow-up]

## 🏆 Победы за последние 7 дней (топ-5)

- [дата]: [победа] (G[N])
- ...

## 📅 Ближайшие календарные события

- [дата]: [событие] ([weekly_review | woop_morning | habit | milestone])

## 🔑 Что важно помнить

- [пользовательская контекстная заметка 1]
- [пользовательская контекстная заметка 2]

## 🔄 Persistence status

- Drive: [✓ connected | ⚠ retry needed | ✗ disconnected]
- Calendar: [✓ connected | ⚠ N pending events | ✗ disconnected]
- Unsaved sessions: [N]

---

**Schema:** `state_v2`  •  **Обновлён:** [YYYY-MM-DD HH:MM]
