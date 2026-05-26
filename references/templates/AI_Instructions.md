---
schema_version: "2.0.1"
template_version: "2.0.1"
last_updated: "2026-05-27"
purpose: "Инструкции для Claude по работе с Drive Wiki"
---

# Инструкции для Claude: Управление Wiki

## Schema reference

Все данные wiki соответствуют `references/state_v2_schema.md`. **Canonical 11 spheres** (см. §1 schema) — единственно допустимый набор имён сфер:
`health, finances, career, family, romance, social, personal_growth, meaning, fun_recreation, contribution, physical_environment`.

Запрещены legacy имена: `growth`, `spirituality`, `fun`, `environment`.

## Gating: когда писать в Wiki

```
on session_start:
  detect (drive_connected, calendar_connected)
  if drive && calendar:
      mode = "full_persistence"   → пиши ВСЁ
  elif drive:
      mode = "wiki_no_execution"  → пиши state, calendar events в pending
  elif calendar:
      mode = "execution_no_wiki"  → НЕ пиши в Wiki, lean state в conversation
  else:
      mode = "lean_conversation"  → минимум в conversation memory, ничего в Drive
  write session.gating_mode = mode   // state v2.0.1+ observability
```

При смене коннекторов в середине сессии — пересчитай mode и обнови `session.gating_mode`.

## Bootstrap (первый коннект Drive)

При `persistence_retry.drive.wiki_bootstrapped == false`:

1. Создать структуру:
   ```
   Life Planning Coach Wiki/
   ├── 00_Raw/
   ├── 01_Wiki/
   │   ├── Hot_Cache.md, Index.md
   │   ├── User_Progress/{Goals.md, Wheel_of_Life_History.md, Core_Values_Compass.md, USER_PROGRESS_JOURNAL.md}
   │   └── Decisions/
   ├── 02_Instructions/CLAUDE.md
   ├── 03_Dashboard/{Progress_Dashboard.md, dashboard_data.json}
   ├── 05_Archive/
   ├── README.md, CHANGELOG.md
   ```
2. Заполнить шаблоны текущим state v2 (если есть)
3. Установить `persistence_retry.drive.wiki_bootstrapped = true`, `first_connection_at = now()`

## Backfill (mid-session connection)

Если Drive подключился в середине сессии и `persistence_retry.backfill_offered == false`:

```
prompt: "У тебя накопилось данных за сессию (Phase {phase}, Wheel of Life: {filled}/11, целей: {count}) — синхронизировать в Drive?"
backfill_offered = true

if yes:
    bootstrap_drive_wiki()
    one_shot_dump_state_v2_to_wiki()
    confirm: "Wiki создан, прогресс сохранён ✓"
    switch_to_mode("full_persistence")
if no:
    drive.user_declined_count += 1
    if >= 2: backoff 3 sessions
```

## Протокол чтения (start of session)

1. Прочитать `01_Wiki/Hot_Cache.md` → `01_Wiki/Index.md`
2. Синтезировать emotional summary
3. При необходимости — прочитать 1-2 релевантные wiki-страницы из `User_Progress/`
4. **НЕ читать** `00_Raw/` напрямую (только через Hot_Cache)

## Протокол записи

| Файл | Режим | Когда |
|---|---|---|
| `00_Raw/{session_date}.md` | append-only | Конец каждой сессии (новый файл) |
| `01_Wiki/Hot_Cache.md` | overwrite полностью | Конец сессии, < 1000 токенов |
| `01_Wiki/User_Progress/*.md` | section update | После релевантной фазы |
| `03_Dashboard/dashboard_data.json` | overwrite | После каждого значимого изменения state |
| `03_Dashboard/Progress_Dashboard.md` | overwrite | Конец сессии (text fallback дашборда) |
| `CHANGELOG.md` | append | Каждое значимое изменение |

## Write rules per state v2 field

Source-of-write — соответствующий `module_phase*.md` (см. State Writes секции там).

| State поле | Куда писать |
|---|---|
| `session.*` (incl. `gating_mode`) | `Hot_Cache.md` |
| `persona.active_mode` | `Hot_Cache.md` + `USER_PROGRESS_JOURNAL.md` при смене |
| `diagnosis.wheel_of_life` | `Wheel_of_Life_History.md` |
| `diagnosis.core_values` (+ `compass_question`) | `Core_Values_Compass.md` + `Hot_Cache.md` |
| `goals.*` | `Goals.md` + `dashboard_data.json` |
| `goal_filter.*` (incl. `core_values_alignment`) | `Goals.md` (radar блок) |
| `habits[]` (cue/routine/reward/anchor/tiny_version) | `Goals.md` (секция Habits) |
| `weekly_reviews[]` | `USER_PROGRESS_JOURNAL.md` «Сессия» |
| `emotion_regulation_log[]` | `USER_PROGRESS_JOURNAL.md` `Emotion_Regulation_Breakthrough` (Δ≥3) |
| `wins_log[]` | `Goals.md` «Победы» + `Hot_Cache.md` топ-5 |
| `reward_audit_results[]` | `USER_PROGRESS_JOURNAL.md` `Reward_Audit` |
| `calendar_events_log[]` | `00_Raw/{session_date}.md` + ссылка в `Hot_Cache.md` |
| `recovery_sessions_log[]` | `USER_PROGRESS_JOURNAL.md` `Recovery` |
| `persistence_retry.*` (incl. `wiki_bootstrapped`, `backfill_offered`) | `Hot_Cache.md` |

## Токен-бюджеты

| Файл | Лимит |
|---|---|
| Hot_Cache.md | < 1000 токенов |
| Index.md | < 200 токенов |
| Одна wiki-страница в User_Progress/ | < 1500 токенов |
| Progress_Dashboard.md (text fallback) | < 2000 токенов |

При превышении — архивировать старые секции в `05_Archive/`.

## Приоритет источников (конфликт данных)

1. Если Drive подключён И доступен → данные с Drive
2. Если Drive недоступен → Memory + диалог
3. Если расхождение между Drive и conversation memory → спросить пользователя

## Язык и тон

- Все файлы — на русском
- Эмодзи для навигации (не для эмоций)
- Прогресс-бары ASCII (`█░`) для визуализации
- Стагнация → «стабильность», «база для роста»
- Снижение → «временный спад», «переключение фокуса»
- **Запрещено**: «провал», «отстой», «ужасно», «должен», «надо»

## Сигналы для скилла

При записи в Wiki Claude добавляет в conversation для пользователя:
- ✓ при успешной записи: «Сохранил в Wiki»
- ⚠ при retry: «Не удалось записать в Drive — данные в памяти сессии»
- 🔄 при backfill: «Wiki создан, прогресс сохранён»

## Schema version handling

Если Wiki содержит файлы со старым `schema_version < 2.0`:
1. Предложить миграцию: «Wiki schema обновлён до v2 — мигрировать данные?»
2. Если согласен → запустить migration (см. `state_v2_schema.md` §8)
3. Если отказался → продолжить чтение в legacy mode, не записывать новый формат

---

**Связанные:** `references/state_v2_schema.md` (canonical schema), `docs/research/plan_v1.0_templates_rebuild.md` (план rebuild)
