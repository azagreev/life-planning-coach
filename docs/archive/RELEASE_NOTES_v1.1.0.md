## Что нового в v1.1.0

**Тема:** Methodology Foundation + MCP PoC integration + первая чистка после v1.0. Surface evidence-based methods which были buried; complete PoC of Google Calendar + Drive MCP с decision committed; remove deprecated v1 schema.

### Added (Methodology — PRD v0.15)

- **`references/implementation_intentions.md`** (NEW, Tier 3, ~1500 tokens) — standalone deep ref. Gollwitzer & Sheeran 2006 meta-analysis (d=0.65, n=8000+). 3 forms (WHEN/WHERE/WHAT), coping plans, skill prompt patterns. Implementation Intentions promoted к primary planning tool в Phase 5 (previously buried в `goal_architecture.md` subsection).
- **`references/evidence_map.md`** (NEW, Tier 3, ~3200 tokens) — unified catalog всех методов skill с honest evidence levels (🟢-🔴), sources, effect sizes. 5-level framework. Explicit "honest framing" section для методов которые NOT следует claim "research-backed" (Parts Work, Body Doubling, Wheel of Life).
- **`references/templates/lpc_wiki_cleanup.gs`** (NEW) — Google Apps Script ready-to-paste для append-only Wiki cleanup. ~3 min one-time setup; daily trigger keeps last 5 per category + < 30 days.

### Added (PoC MCP — Google Calendar + Drive)

- **PoC MCP (Google Calendar) completed** — `docs/research/mcp_poc_log.md` заполнен real measurements на Claude Max plan. Decision: **MCP-first**. 14/14 ops functional через Gates 1+2. `suggest_time` подтверждён доступным (singular form). Tool inventory: 8 confirmed (4 read + 4 write). PoC выполнен AI-assisted hybrid через Claude_in_Chrome (Chrome Claude драйвил browser + claude.ai chat, current session orchestrated).
- **PoC MCP (Google Drive) completed** — same-day extension. 13 ops executed direct via MCP from current session (sub-second per op). Tool inventory: 8 confirmed (6 read + 2 write). **Critical gap**: NO `update_file`, NO `delete_file` exposed by Anthropic connector. Decision: **MCP-first for bootstrap + reads; Wiki updates require append-only redesign**. 10 schema quirks documented.
- **`references/drive_integration.md`** (NEW, ~190 lines) — analog of `calendar_integration.md` for Drive: 8 tools, 10 quirks, troubleshooting, prompt patterns (bootstrap + append-only save + read-latest). Documents 4-mode cleanup strategy (apps_script / batch_weekly / reminder default / ignore) as Layered defaults для users разной tech-savviness.
- **`docs/research/mcp_poc_log.md`** (NEW, ~500 lines) — full PoC execution log с per-op latencies, request/response samples, 31 cumulative quirks across Calendar + Drive.
- **`docs/research/prd_v0.15_methodology_upgrade.md`** (NEW) — user-uploaded PRD preserved для traceability + roadmap integration.

### Changed (Methodology)

- **`references/module_phase5_execution.md`** — Implementation Intentions credited as primary tool фазы. Mode A (Calendar Connected) маркирован как primary path. Recurring fallback gotcha обновлён.
- **`references/habit_loop.md`** — restructure: §1 Tiny Habits (PRIMARY для создания new habits при низкой мотивации), §2 Cue-Routine-Reward (DIAGNOSTIC для existing habits). Intro paragraph maps task → framework. Anchor pattern explicitly framed as WHEN-type Implementation Intention.
- **`references/module_phase2_goal_architecture.md`** — "SMART+ check" renamed к "KR Quality Check (measurability + alignment)". Same 6 criteria, reframed around execution probability + values alignment (not classical SMART acronym).
- **`references/calendar_integration.md`** — Prompt Patterns intro frames recurring events as WHEN-type II с cross-ref к `implementation_intentions.md`. PLUS bumped v0.2.1 → v0.3.0 с 10 connector-specific schema quirks (recurrenceData vs recurrence, UNTIL must be UTC-Z, attendeeEmails for suggest_time, etc.). Free Slot Algorithm с двумя путями.

### Changed (PoC + cleanup)

- **`references/calendar_constants.md`** — Tools table обновлён с PoC schema notes. Event Data Schema split на request vs response. Failure Modes +7 новых сценариев.
- **`README.md`** — добавлен footnote¹ о Max plan для MCP коннекторов с link на PoC log.
- **`BACKLOG.md`** — PoC MCP перенесён в Archived/Done. Google Tasks MCP отмечен. Added v0.15 PRD epic. Archived 6 shipped items (Templates Rebuild, Core Values Discovery, Health Track, Goal Concordance, README rewrite, Token Optimization).
- **`references/templates/AI_Instructions.md`** — ⚠️ MCP Drive limitations note; write rules table обновлена под append-only pattern.
- **`references/state_v2_schema.md`** — schema bump 2.2 → 2.2.1 (additive). Добавлены `persistence_retry.drive.wiki_cleanup_mode` (enum: apps_script/batch_weekly/reminder/ignore), `wiki_cleanup_last_reminder_at`, `wiki_cleanup_chosen_at`. Bootstrap protocol §7.1 prompts user for cleanup mode choice.
- **`ROADMAP.md`** — integrated PRD v0.15 в v1.1/v1.2/v1.3 plan. Future Lab + tensions documented.

### Removed

- **`references/conversation_state_schema.md`** — v1 schema удалён per plan announced в v1.0.0. state_v2_schema.md §8 migration table сохранена для legacy forks.

### Deferred к v1.2 (не сделано в v1.1)

- `scripts/build-skill.sh` deletion — release.sh still calls it; requires release.sh migration к python build-skill.py release.
- `scripts/sync-version.sh` deletion — same dependency.
Both retain DEPRECATED stderr warnings.

### Architecture decisions

**Drive Wiki persistence (Path A):** После Grok research synthesis (Karpathy LLM Wiki, Justin Norris Apps Script mirroring, event-sourcing patterns) committed append-only с timestamp suffix + user-side Apps Script cleanup. Forward-compat: when Anthropic ships `update_file`, swap is one-line change в `save_state(template, content)` abstraction. Documented в `drive_integration.md` §Path A. Alternative paths (B Desktop CRUD, C conversation-only, D Obsidian, F Zapier hybrid) documented для context но not chosen.

**Methodology shift (PRD v0.15 partial):** Surface 3 buried/missing evidence-based methods (Implementation Intentions promote, Tiny Habits primary framing, evidence map). v1.2 будет добавлять COM-B diagnostic + AAR integration + Premortem. v1.3 — Wheel of Life frequency gate.
