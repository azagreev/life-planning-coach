# Migration: state v1 → state v2

> **Дата:** 2026-05-26
> **Audience:** Существующие пользователи life-planning-coach с Drive Wiki в legacy формате (state v1)
> **Status:** Active migration guide

---

## Что меняется

v2 — рефакторинг без потери данных. Все ключевые поля v1 имеют v2-эквивалент. Новые блоки (`core_values`, `persona`, `emotion_regulation_log`, `wins_log`, `reward_audit_results`, `calendar_events_log`, `recovery_sessions_log`, полный `habits[]` Loop) — additive, не требуют action от пользователя.

**Главное breaking-change:** Wheel of Life в legacy wiki может иметь 8 сфер. v2 требует 11 canonical sphere IDs.

---

## Migration prompt (при первом запуске после обновления)

```
Skill detects:
  if drive_connected:
    read Wiki/01_Wiki/User_Progress/Wheel_of_Life_History.md
    if spheres_count != 11 OR contains legacy IDs:
      prompt: "Wiki использует старую схему (8 сфер). Обновить до 11 canonical spheres v2?
               Старые данные сохранятся в 05_Archive/."
      if yes → run migrate_v1_to_v2()
      if no  → продолжить в legacy mode, не записывать v2 формат
```

---

## Path mapping (legacy → canonical)

### Sphere IDs

| Legacy (HTML / old wiki) | Canonical (v2) | Notes |
|---|---|---|
| `growth` | `personal_growth` | |
| `spirituality` | `meaning` | |
| `fun` | `fun_recreation` | |
| `environment` | `physical_environment` | |
| (8-sphere wiki: relationships merged) | `family` + `romance` | Split: спросить пользователя как распределить |
| (8-sphere wiki: нет social) | `social` | Default 5/10, предложить переоценить |
| (8-sphere wiki: нет contribution) | `contribution` | Default 5/10, предложить переоценить |

### State schema fields

См. полную таблицу в `references/state_v2_schema.md` §8.

Краткое резюме:

| v1 поле | v2 эквивалент |
|---|---|
| `stage` | `session.current_phase` |
| `life_wheel` | `diagnosis.wheel_of_life.current` |
| `values` | `diagnosis.values_schwartz` |
| `goals.bhag` (string) | `goals.bhag.statement` |
| `goals.themes` | `goals.life_themes` |
| `goals.twelve_week` | `goals.twelve_week_okr` |
| `weekly_reviews[].worked/didnt_work/changes` | `weekly_reviews[].scrum_retro.*` |

### File paths

| Legacy wiki path | v2 path | Action |
|---|---|---|
| `01_Wiki/Concepts/` | (удаляется) | Static knowledge — переехал в `references/` skill |
| `01_Wiki/Frameworks/` | (удаляется) | Static knowledge — переехал в `references/` skill |
| `01_Wiki/Sources/` | (удаляется) | Не используется в v2 |
| `04_References/` | (удаляется) | References поставляются со skill |
| — | `01_Wiki/User_Progress/Core_Values_Compass.md` | **NEW** — заполнится при прохождении Core Values Discovery |
| — | `03_Dashboard/dashboard_data.json` | **NEW** — state v2 snapshot для HTML рендера |

---

## Migration steps (automated)

```python
def migrate_v1_to_v2(wiki_root):
    # 1. Backup
    archive_dir = wiki_root / "05_Archive" / f"v1_backup_{today()}"
    copy_tree(wiki_root / "01_Wiki" / "User_Progress", archive_dir)

    # 2. Wheel of Life: 8 → 11 spheres
    wol_path = wiki_root / "01_Wiki" / "User_Progress" / "Wheel_of_Life_History.md"
    wol = parse_wol(wol_path)
    if len(wol.spheres) == 8:
        # Rename legacy IDs
        wol = rename_spheres(wol, {
            "growth": "personal_growth",
            "spirituality": "meaning",
            "fun": "fun_recreation",
            "environment": "physical_environment",
        })
        # Split "relationships" → ask user
        if "relationships" in wol.spheres:
            ask_user_split("relationships", into=["family", "romance"])
        # Add missing canonical with default 5/10
        for missing in ["social", "contribution"]:
            wol.add_sphere(missing, default=5, note="Добавлено при миграции v2 — переоцените на след. сессии")

    # 3. Goals.md: добавить AGF radar block + Core Values alignment placeholders
    goals_path = wiki_root / "01_Wiki" / "User_Progress" / "Goals.md"
    augment_goals_template(goals_path)  # без потери данных

    # 4. Create new files
    create_from_template(wiki_root / "01_Wiki" / "User_Progress" / "Core_Values_Compass.md")
    create_from_template(wiki_root / "03_Dashboard" / "dashboard_data.json", initial=current_state_v2())

    # 5. Remove deprecated dirs (если пустые)
    safe_remove_if_empty(wiki_root / "01_Wiki" / "Concepts")
    safe_remove_if_empty(wiki_root / "01_Wiki" / "Frameworks")
    safe_remove_if_empty(wiki_root / "01_Wiki" / "Sources")
    safe_remove_if_empty(wiki_root / "04_References")

    # 6. Bump schema_version in all templates
    for template in wiki_root.glob("**/*.md"):
        set_frontmatter(template, "schema_version", "2.0")

    # 7. Update CHANGELOG
    append_changelog(wiki_root / "CHANGELOG.md", "Migrated v1 → v2 on " + today())

    return "Migration complete. Backup в 05_Archive/v1_backup_*"
```

---

## Manual migration (если automated не сработала)

1. **Backup** всего Wiki в `05_Archive/v1_backup_YYYY-MM-DD/`
2. **Wheel_of_Life_History.md:**
   - Переименовать sphere IDs (см. таблицу выше)
   - Добавить недостающие сферы (`social`, `contribution` с дефолтом 5/10)
   - Обновить `spheres_count: 11` в frontmatter
   - Добавить `schema_version: "2.0"` в frontmatter
3. **Goals.md:**
   - Добавить блок «🔍 Authentic Goal Filter (radar)» на каждую цель
   - Заполнить radar при следующем weekly review
4. **Создать** `Core_Values_Compass.md` из шаблона
5. **Создать** `03_Dashboard/dashboard_data.json` из текущего state
6. **Удалить** пустые директории `Concepts/`, `Frameworks/`, `Sources/`, `04_References/`
7. **Bump** `schema_version: "2.0"` во всех `.md` файлах wiki

---

## Что НЕ требует миграции

- `Hot_Cache.md` — overwrite в следующей сессии
- `Raw/*.md` — append-only, новые v2 раскладки уже в v2 формате
- `USER_PROGRESS_JOURNAL.md` — старые записи остаются, новые в v2 формате

---

## Rollback

Если что-то пошло не так:
```
1. Восстановить из 05_Archive/v1_backup_YYYY-MM-DD/ → 01_Wiki/User_Progress/
2. Отключить v2: в conversation: "продолжай в v1 mode"
3. Skill читает frontmatter schema_version и работает в legacy mode
```

---

## Связанные документы

- [`references/state_v2_schema.md`](../references/state_v2_schema.md) — полная v2 схема + §8 migration table
- [`docs/research/plan_v1.0_templates_rebuild.md`](research/plan_v1.0_templates_rebuild.md) — план rebuild
- [`references/conversation_state_schema.md`](../references/conversation_state_schema.md) — legacy v1 (deprecated)
