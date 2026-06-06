---
schema_version: "2.0"
template_version: "2.0"
session_date: "YYYY-MM-DD"
purpose: "Append-only session capture (00_Raw/)"
---

# Сессия [YYYY-MM-DD]

## Контекст сессии

- **Phase в начале:** [`0`|`0.5`|`1`|`1.5`|`2`|`3`|`4`|`5`]
- **Phase в конце:** [...]
- **Track:** [`quick`|`deep`|—]
- **Длительность:** [N] минут
- **Persona mode:** [`none`|`adhd`|`unemployed`|`elder`|`planning_friction`]

## Эмоциональное состояние

- **Начало:** [состояние, 1-2 фразы]
- **Конец:** [состояние]
- **Δ:** [сдвиг — позитивный / нейтральный / нужна follow-up]

## Темы обсуждения

- [тема 1]
- [тема 2]

## Цели и прогресс (изменения за сессию)

- **G[N]** [название]: [+X% / новый KR / WOOP обновлён / paused]

## Core Values (если работали)

- Discovery: [новые values выявлены — CV?, CV?]
- Compass used: [какой compass question применили к решению]

## 🛡️ Emotion Regulation events (Phase 0.5)

> Если в сессии использовался ER protocol:

| Протокол | Trigger | Outcome readiness (1-10) | Duration |
|---|---|---|---|
| `reappraisal` / `grounding` / `self_compassion` | [что вызвало] | [N] | [мин] |

## Readiness gates за сессию

| Phase | Score |
|---|---|
| [phase_id] | [N]/10 |

## Инсайты

- «[инсайт 1]»
- «[инсайт 2]»

## Действия (committed)

- [действие 1] — дедлайн [...]
- [действие 2]

## 🏆 Wins captured (в wins_log)

| Описание | Цель | Категория |
|---|---|---|
| [победа] | G[N] | milestone / first / streak / breakthrough |

## 📅 Calendar events created

> Если работали в режиме `full_persistence` или `execution_no_wiki`:

| Type | Title | Scheduled for | Recurrence |
|---|---|---|---|
| `weekly_review` / `woop_morning` / `habit` / `milestone` / `shutdown` | [...] | [datetime] | RRULE или — |

## Следующая сессия — фокус

- [что обсудить / что проверить]
- Предлагаемая phase: [...]

## Persistence status в конце сессии

- Drive: [✓ / ⚠ / ✗]
- Calendar: [✓ / ⚠ / ✗]
- Backfill: [не нужен / предложен / выполнен]

---

*Файл append-only. Этот raw capture — основа для обновления Hot_Cache, Goals, Wheel_of_Life_History, USER_PROGRESS_JOURNAL.*
