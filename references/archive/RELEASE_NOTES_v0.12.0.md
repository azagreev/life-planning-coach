## Что нового в v0.12.0

### Added
- **Chronotype-native planning** (`references/chronotype_native_planning.md`) — 3 профиля (Жаворонок/Промежуточный/Сова), Peak-Trough-Rebound эвристики, bedtime to-do list
- **Habit Stack Builder** (`references/habit_stack_builder.md`) — progressive ritual escalation (2→5→10→15 мин), Two-Day Rule, habit anchoring (B = MAP)
- **Shutdown Ritual** (`references/shutdown_ritual.md`) — 5 шагов (Capture→Review→Plan→Celebrate→Close), Zeigarnik elimination, psychological detachment
- **Fresh Start Engine** (`references/fresh_start_engine.md`) — temporal landmarks (Monday, 1st, New Year, birthday), dark side protection
- **Calendar Integration Audit** (`references/audit/AUDIT_CALENDAR_INTEGRATION.md`) — 15 gaps, 4 критических
- **Planning Research synthesis** (`references/research/planning_research_2026-05-20.md`) — 12 evidence-based идей с RICE-оценками
- **RICE Methodology v1.1** (`references/research/rice_methodology.md`) — AI Session-based effort estimation (XS/S/M/L/XL/XXL) + Context Pressure
- **4 platform USER_GUIDEs** (`references/platforms/USER_GUIDE_*.md`) + `CROSS_PLATFORM_COMPARISON.md` — feature matrix, decision tree
- **E2E behavioral testing framework** (`tests/e2e/`) — golden dataset (20 cases), evaluation rubric, manual test protocol
- **Release automation** — `scripts/release.sh` (7-step atomic release) + `scripts/extract-release-notes.py`
- **Tests** — chronotype integration (16 tests), v0.12 features (26 tests), calendar tone check

### Changed
- `references/energy_scheduling.md` — chronotype-adapted peak hours
- `references/diagnostic_methods.md` — chronotype calibration questions (Phase 0/1)
- `references/habit_loop.md` — cross-reference to `habit_stack_builder.md`
- All 4 `platforms/*/SKILL.md` — Phase 0 chronotype calibration + Phase 5 time adaptation
- `README.md` — full rewrite: value prop, quick-start, platform table
- `AGENTS.md` — Kimi Code CLI support, RICE Effort methodology update
- `ROADMAP.md` — v0.11–v0.14 structured roadmap
- `scripts/build-skill.sh` + `build-platform-skill.py` — release integration, kimi-cli artifact
- Calendar event texts — tone check, removed prescriptive «надо/должен»

### Fixed
- Typo: Яворонок → Жаворонок (10 occurrences, 6 files)
- `references/calendar_integration.md` — removed "Runtime: claude.ai only", added Kimi CLI MCP
- CI workflows — pytest install, removed stale step, use `build-skill.sh`

### Removed
- `RETRO_v091_v092.md` — moved out of public repository
- `references/platforms/grok_user_guide.md` — replaced by `USER_GUIDE_GROK.md`
