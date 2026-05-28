---
schema_version: "2.0.1"
template_version: "2.0.1"
last_updated: "2026-05-27"
purpose: "Инструкции для Claude по работе с Drive Wiki"
---

# Инструкции для Claude: Управление Wiki

> ⚠️ MCP Drive: no update/delete. Overwrite = append-only с timestamp suffix; latest по `modifiedTime`. См. `drive_integration.md`.

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

Все записи в Wiki проходят через единую skill-instruction abstraction **`save_state(template, content)`** — полное определение в [`drive_integration.md` §save_state](../drive_integration.md#save_statetemplate-content--write-abstraction). Path A behaviour (default):

```
save_state(template, content):
  iso = now_utc → "YYYY-MM-DDTHH-MM"   // colons replaced с "-"
  create_file(
    parentId=<subfolder per Write rules table below>,
    title=f"{template}_{iso}.md",       // e.g. Hot_Cache_2026-05-26T18-45.md
    textContent=content,
    contentMimeType="text/markdown",
    disableConversionToGoogleType=true
  )
```

«Current» state = latest by `modifiedTime` через `read_state(template)`. Старые snapshots — audit trail (Apps Script cleanup управляет retention).

**Forward-compat:** call sites в phase modules используют термин `save_state(...)`; concrete backend swaps по detected MCP surface (Path A → Path B Desktop community MCP с native update_file → Path F Zapier replace), без переписывания module instructions.

### Когда какой template писать

| Файл | Режим | Когда |
|---|---|---|
| `00_Raw/{session_date}_{TS}.md` | `save_state("Raw", ...)` | Конец каждой сессии |
| `01_Wiki/Hot_Cache_{TS}.md` | `save_state("Hot_Cache", ...)` | Конец сессии, < 1000 токенов |
| `01_Wiki/User_Progress/Goals_{TS}.md` | `save_state("Goals", ...)` | После Phase 2 / Phase 3 (изменение целей или wins) |
| `01_Wiki/User_Progress/Wheel_of_Life_History_{TS}.md` | `save_state("Wheel_of_Life_History", ...)` | После Phase 1 (новая WoL оценка) |
| `01_Wiki/User_Progress/USER_PROGRESS_JOURNAL_{TS}.md` | `save_state("USER_PROGRESS_JOURNAL", ...)` | После значимых событий (persona switch, ER breakthrough, weekly review) |
| `01_Wiki/User_Progress/Core_Values_Compass_{TS}.md` | `save_state("Core_Values_Compass", ...)` | После Phase 1.5 (core values + compass questions) |
| `03_Dashboard/dashboard_data_{TS}.json` | `save_state("dashboard_data", ...)` | После значимого изменения state |
| `03_Dashboard/Progress_Dashboard_{TS}.md` | `save_state("Progress_Dashboard", ...)` | Конец сессии |

## Write rules per state v2 field

Source-of-write — соответствующий `module_phase*.md` (см. State Writes секции там). Каждая запись = один вызов `save_state(template, content)` с подходящим template из таблицы выше.

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
