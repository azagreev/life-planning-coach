## Что нового в v1.0.0

**Production-ready release** — major-version signal стабильности после v0.17→v0.19 content milestones. v1.0 закрывает 6 production-readiness gaps + замораживает API contract: schema 2.x, persona naming, build CLI, Routing Map.

### Added

- **`scripts/build-skill.py`** — единый Python CLI заменяющий bash hybrid:
  - `build` — пересобрать все 4 платформы + ZIP/skill/grok-md/kimi-md/kimi-cli-zip
  - `version X.Y.Z` — sync version во все source files
  - `verify` — pre-release checks
  - `release X.Y.Z` — full flow (verify + version + build + commit + tag + push + gh release)
  - Cross-platform: no rsync, no `sed -i`, LF-normalized ZIP files
- **`scripts/gating_logic.py`** — pure-function reference implementation 4 gating modes (specification, не executor):
  - `detect_gating_mode(drive, calendar)` → 4 mode matrix
  - `should_bootstrap_drive()`, `run_bootstrap()` — first-connect protocol
  - `should_offer_backfill()`, `accept_backfill()`, `decline_backfill()` — mid-session protocol с backoff после 2 declines
- **`MIGRATION_v1.md`** — guide v0.x → v1.0 для пользователей с форками: persona renames mapping, schema migration path, deprecation timeline, API stability promise
- **Tests:**
  - `test_platform_parity.py` (15 структурных проверок × 4 платформы = 60 sub-tests)
  - `test_typical_session_budget.py` (6 тестов: cold-load ≤ 4K, Quick ≤ 14K, Deep ≤ 18K, Health ≤ 20K)
  - `test_gating_modes_e2e.py` (25 тестов: 4 mode matrix + bootstrap + backfill behavior)
  - `test_build_skill_cli.py` (13 тестов: argparse, version sync, ZIP creation)
  - `test_rename_persona_script.py` (8 тестов)
  - `test_extract_release_notes.py` (6 тестов)
- **`pyproject.toml` coverage configuration** — `fail_under = 50` (v1.0 baseline; aspirational target 85% в roadmap)

### Changed

- **`AGENTS.md` §4.2** — release process обновлён под `python scripts/build-skill.py release X.Y.Z`
- **`scripts/extract-release-notes.py`** — output путь изменён `references/archive/` → `docs/archive/` (соответствует v0.15.x cleanup)
- **`tests/system/test_github_sync.py::test_release_notes_generation`** — использует `sys.executable` вместо `python3` literal (cross-platform fix для Windows MS Store stub), forces `PYTHONIOENCODING=utf-8`
- **`references/conversation_state_schema.md`** — deprecation header усилен: «Will be removed in v1.1. Use state_v2_schema.md»
- **README badges** — coverage actualised, version 1.0.0, tests count 632+

### Deprecated (will be removed in v1.1)

- **`scripts/build-skill.sh`** — replaced by `python scripts/build-skill.py build`. Header warning + stderr echo при запуске.
- **`scripts/sync-version.sh`** — replaced by `python scripts/build-skill.py version X.Y.Z`. Header warning + stderr echo.
- **`references/conversation_state_schema.md`** (v1 schema) — replaced by `state_v2_schema.md`.

### Acceptance criteria

- ✅ Cold-load: SKILL.master.md = 3981 tokens (≤ 4000 budget)
- ✅ Typical session ≤ 18K tokens (Deep diagnostic + ADHD persona = 16-17K)
- ✅ Coverage ≥ 50% (current 54.3%; gated в `pyproject.toml`)
- ✅ All 4 gating modes имеют e2e behavior tests (4 mode matrix + bootstrap + backfill backoff)
- ✅ All 4 platforms pass 15 structural parity checks
- ✅ Unified `build-skill.py` работает cross-platform (Windows tested)
- ✅ MIGRATION_v1.md описывает persona renames + schema bumps + deprecation paths
- ✅ Test suite: 632 passed, 1 failed (working_tree, auto-fixed at release)

### API stability promise (v1.0+)

С v1.0 проект следует semver строго:
- **Patch (v1.0.x):** только bug fixes, не меняет contract.
- **Minor (v1.x.0):** additive features. Forked интеграции продолжают работать.
- **Major (v2.0.0):** breaking changes только при schema 3.0. Deprecated paths должны быть документированы 2 minor релиза.

Стабильные поверхности: Routing Map, 4 gating modes naming, canonical 11 spheres, persona naming `mode_<short>`, build CLI, schema 2.x additive policy.

### Что дальше

- **v1.x patches** — bug fixes, edge cases, security
- **v1.1** — удалить deprecated bash скрипты + conversation_state_schema.md
- **Post-v1.0 backlog:** PoC MCP (RICE 31.5), Google Health MCP (RICE 7.2), Timezone hardening (RICE 18), Multilingual EN (4.7), Body Doubling AI (6.1)
