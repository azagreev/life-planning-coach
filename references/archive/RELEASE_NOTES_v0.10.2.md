## Что нового в v0.10.2

### Added
- **Kimi Code CLI support** — новая платформа (terminal-based agent):
  - `platforms/kimi-cli/SKILL.md` (323 lines) — directory-based skill с `references/` через `read_file`
  - `references/platforms/kimi-cli.overlay.yaml` — overlay без inline, без `memory_space`
  - MCP поддержка (Google Calendar + Google Drive) через manual JSON config
  - Включён в `scripts/build-platform-skill.py` и `scripts/build-skill.sh`
- **Полный rewrite README.md** — короткий value prop + quick-start + таблица платформ + ссылки на USER_GUIDE
- **4 USER_GUIDE файла** (`references/platforms/`):
  - `USER_GUIDE_CLAUDE.md` — ZIP upload, MCP 1-click, directory-based refs
  - `USER_GUIDE_GROK.md` — Direct Prompt / Projects, native connectors (не MCP)
  - `USER_GUIDE_KIMI_OKCOMPUTER.md` — web agent, `memory_space`, text-only calendar
  - `USER_GUIDE_KIMI_CLI.md` — terminal setup, manual MCP JSON config
- **`CROSS_PLATFORM_COMPARISON.md`** — feature matrix, decision tree, quick selector
- **E2E behavioral testing framework** (`tests/e2e/`):
  - `golden_dataset.json` — 20 тест-кейсов (LPC-001..LPC-020)
  - `evaluation_rubric.md` — 5 критериев LLM-as-a-Judge
  - `MANUAL_TEST_RUN.md` — протокол ручного прогона

### Fixed
- **README integrity** — все system tests проходят (11 доменов, Stage 1.5, communication style, core refs list, version format)
- **`references/calendar_integration.md`** — убрано "Runtime: claude.ai only", добавлена поддержка Kimi CLI MCP
- **`AGENTS.md`** — обновлены платформы (добавлен Kimi Code CLI), build-команда

### Removed
- `references/platforms/grok_user_guide.md` — заменён на `USER_GUIDE_GROK.md`
- `RETRO_v091_v092.md` — удалён из публичного репозитория
