# Migration Guide: v0.x → v1.0

> **Audience:** пользователи, которые форкали или интегрировали `life-planning-coach` версии v0.x. Если ты используешь project из GitHub releases без модификаций — ничего делать не нужно, обновись на v1.0 и всё.

## TL;DR

v1.0 не вводит breaking changes семантики. Все изменения **additive** и **backward compat**:

- ✅ Skill API стабилен — Routing Map, 4 gating modes, Phase 0–5 flow остались как в v0.19.
- ✅ Schema v2.x совместим — `schema_version` 2.0 doc парсится 2.2 клиентом (additive bumps).
- ⚠ **Persona modules переименованы** в v0.19.0 — если ты ссылался на `references/adhd_mode.md` etc., нужен grep'n'replace.
- ⚠ **Build CLI новый** — `python scripts/build-skill.py` заменяет bash hybrid. Старые bash-скрипты deprecated, удалены в v1.1.
- ⚠ **Schema v1 (`conversation_state_schema.md`) deprecated** — удалён в v1.1.

API freeze: с v1.0 любые breaking changes требуют major bump (v2.0). Schema 2.x останется compat до v2.0.

---

## 1. Persona modules — переименование (v0.19.0)

Если в твоём форке/интеграции есть refs на старые имена:

| Old name | New name | Locations to update |
|---|---|---|
| `references/adhd_mode.md` | `references/mode_adhd.md` | SKILL files, prompts, docs |
| `references/time_structure_unemployed.md` | `references/mode_unemployed.md` | — |
| `references/elder_homebound_mode.md` | `references/mode_elder.md` | — |
| `references/planning_friction_audit.md` | `references/mode_planning_friction.md` | — |

**Auto-migrate** через скрипт из repo:

```bash
# Скачай scripts/rename_persona_modules.py из v1.0
python scripts/rename_persona_modules.py            # dry-run
python scripts/rename_persona_modules.py --apply    # actually rename + replace
```

Скрипт переименует файлы через `git mv` и заменит cross-refs во всех `.md`/`.py`/`.yaml`/`.json` файлах (skip: `.git/`, `dist/`, `docs/archive/`).

---

## 2. Schema migrations — v1 → v2.0 → v2.2

`life-planning-coach` использует semver для state schema независимо от skill version.

### Cumulative path

| From | To | Bump type | Что меняется |
|---|---|---|---|
| **v1** (legacy) | 2.0 | major | Canonical 11 spheres, persona block, core_values, full habit loop, wins_log first-class, persistence_retry tracking. **Не automated**, требует migration script. |
| 2.0 | 2.0.1 | patch | `session.gating_mode` tracker. Additive. Старые клиенты игнорируют unknown field. |
| 2.0.1 | 2.1 | minor | `diagnosis.health_metabolism` opt-in блок (v0.19.0). Additive. Не активируется без user opt-in. |
| 2.1 | 2.2 | minor | `goal_filter.active_goals[].partner_coordination` optional sub-block (v0.19.0). Additive. `null` для индивидуальных целей. |

### Backward compat guarantees

- Любой `schema_version: 2.x` документ парсится `2.{y}` клиентом где y ≥ x (forward compat для unknown fields).
- 2.0 → 2.2: unknown fields игнорируются. Все required fields из 2.0 остались.
- 2.x → 3.0 (будущее): потребует migration script. **API freeze: до v2.0 skill release-а — никакого 3.0.**

### v1 → v2.0 миграция (если у тебя legacy wiki)

См. `references/state_v2_schema.md §8 Миграция с v1`. Mapping table:
- `stage` → `session.current_phase`
- `life_wheel` → `diagnosis.wheel_of_life.current` (naming совпадает)
- `values` → `diagnosis.values_schwartz`
- `goals.bhag` (string) → `goals.bhag.statement` (wrap в объект)
- `weekly_reviews[].worked/didnt_work/changes` → `weekly_reviews[].scrum_retro.*`

Новые блоки v2.0 (не было в v1): `persona`, `diagnosis.core_values`, `diagnosis.ikigai_pillars`, full `habits[]` с cue/routine/reward, `emotion_regulation_log`, `wins_log`, `reward_audit_results`, `calendar_events_log`, `recovery_sessions_log`.

---

## 3. Build pipeline — новый unified CLI (v1.0)

### Что устарело

| Старая команда | Новая команда | Что меняется |
|---|---|---|
| `bash scripts/build-skill.sh` | `python scripts/build-skill.py build` | Cross-platform, no rsync, no bash dependency |
| `bash scripts/sync-version.sh X.Y.Z` | `python scripts/build-skill.py version X.Y.Z` | Pure Python regex, не `sed -i` (вариабельный синтаксис macOS/Linux) |
| `bash scripts/release.sh X.Y.Z` | `python scripts/build-skill.py release X.Y.Z` | + integrated verify + release notes generation |

### Что осталось

- `scripts/build-platform-skill.py` — генератор platform-specific SKILL files (вызывается из `build-skill.py`).
- `scripts/extract-release-notes.py` — извлечение секции из CHANGELOG (вызывается из `build-skill.py release`).
- `scripts/rename_persona_modules.py` — one-shot migration script для v0.19.0 (можно удалить если уже мигрировал).

### Deprecation timeline

- **v1.0:** Старые bash-скрипты оставлены с deprecation warning header. Continue работать.
- **v1.1:** Удалены окончательно. Используйте `build-skill.py`.

---

## 4. Deprecated paths

| Path | Replacement | Removed in |
|---|---|---|
| `references/conversation_state_schema.md` | `references/state_v2_schema.md` | v1.1 |
| `scripts/build-skill.sh` | `python scripts/build-skill.py build` | v1.1 |
| `scripts/sync-version.sh` | `python scripts/build-skill.py version X.Y.Z` | v1.1 |

---

## 5. API stability promise (v1.x)

С v1.0 проект следует semver строго:

- **Patch (v1.0.x):** только bug fixes. Не меняет contract.
- **Minor (v1.x.0):** additive features. Старые интеграции продолжают работать без изменений.
- **Major (v2.0.0):** breaking changes — но **только если schema 3.0 потребуется**. Прежде чем major будет release-нут, deprecated paths должны быть документированы 2 minor релиза.

Стабильные поверхности (стабильные ≥ v1.0):
- Routing Map в SKILL.master.md §2 (6 phase modules)
- 4 gating modes naming (`full_persistence` / `wiki_no_execution` / `execution_no_wiki` / `lean_conversation`)
- Canonical 11 spheres (`state_v2_schema.md §1`)
- Persona naming `mode_<short>` (v0.19+)
- Build CLI `python scripts/build-skill.py {build,version,verify,release}`
- Schema 2.x additive bump policy

---

## 6. Forked users — checklist

Если ты форкал v0.x в production:

```bash
# 1. Скачай свежий ROADMAP + CHANGELOG, прочитай v0.19/v1.0 секции

# 2. Auto-migrate persona renames
python scripts/rename_persona_modules.py --apply

# 3. Обнови schema_version (опционально, но рекомендуется)
sed -i 's/"schema_version": "2\.0"/"schema_version": "2.2"/' your-state.json
# (или просто игнорируй — 2.0 client совместим с 2.2)

# 4. Если используешь bash build:
#    замени `bash scripts/build-skill.sh` на `python scripts/build-skill.py build`
#    в твоём CI или Makefile

# 5. Run tests на своём форке — должны pass без изменений если ты не модифицировал phase modules
pytest tests/ -q

# 6. Update docs/README links на новые persona paths
```

Возникли вопросы? Открой Issue с тегом `migration-help`: https://github.com/azagreev/life-planning-coach/issues

---

## Связанные документы

- [CHANGELOG.md](CHANGELOG.md) — полная история изменений
- [ROADMAP.md](ROADMAP.md) — будущий scope post-v1.0
- [AGENTS.md](AGENTS.md) — рабочий контракт для AI-агентов
- [references/state_v2_schema.md](references/state_v2_schema.md) — canonical schema спецификация
- [references/templates/AI_Instructions.md](references/templates/AI_Instructions.md) — operational protocol (gating, bootstrap, backfill, write rules)
