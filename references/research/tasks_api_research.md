# Tasks API Research

**Gate:** 3 — Tasks API Investigation  
**Date:** 2026-05-16  
**Researcher:** Kimi Code CLI (subagent)  
**Method:** Web sources + GitHub API (no HTML scraping)

---

## Official Calendar MCP

**Scopes (confirmed from official docs):**
- `https://www.googleapis.com/auth/calendar.calendarlist.readonly`
- `https://www.googleapis.com/auth/calendar.events.freebusy`
- `https://www.googleapis.com/auth/calendar.events.readonly`

**Available tools (8 total):**
- `create_event`
- `delete_event`
- `get_event`
- `list_calendars`
- `list_events`
- `respond_to_event`
- `suggest_time`
- `update_event`

**Tasks support:** ❌ No  
**Google Workspace MCP (all products):** Also does NOT include Tasks API scopes. Listed scopes: Gmail, Drive, Calendar, Chat, People — no Tasks.

**Source confirmation:**
- https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server
- https://developers.google.com/workspace/guides/configure-mcp-servers

---

## Community MCP Options

### Option 1: `taylorwilsdon/google_workspace_mcp`

| Attribute | Detail |
|-----------|--------|
| **URL** | https://github.com/taylorwilsdon/google_workspace_mcp |
| **Stars** | ⭐ 2,412 |
| **Language** | Python 3.10+ |
| **License** | MIT |
| **Transport** | `stdio` (legacy) / `streamable-http` (recommended) |
| **Self-hosted** | ✅ Yes — runs locally via `uvx workspace-mcp` or deployed to cloud (Docker, Helm chart, reverse proxy) |
| **Claude setup** | **Desktop:** `claude_desktop_config.json` (stdio) or **Connector** (streamable HTTP). Also supports Claude Code, VS Code, LM Studio |
| **Last updated** | 2026-05-14 |
| **Open issues** | 110 |

**Tasks tools (6 total):**
| Tool | Tier | Description |
|------|------|-------------|
| `list_tasks` | Core | List tasks with filtering (completed, due date, pagination) |
| `get_task` | Core | Get task details |
| `manage_task` | Core | **Create, update, delete, move** tasks |
| `list_task_lists` | Complete | List all task lists |
| `get_task_list` | Complete | Get task list details |
| `manage_task_list` | Complete | Create, update, delete task lists; clear completed |

**Tasks CRUD:** ✅ Full (Create, Read, Update, Delete, Move)  
**Subtasks:** ✅ Yes — `parent` parameter in `manage_task` (create/move subtasks). Hierarchical serialization with placeholder-parent handling for orphaned subtasks.  
**Task lists management:** ✅ Yes  
**Scopes used:** `tasks` / `tasks_read` (granular permissions supported: `readonly`, `manage`, `full`)  
**Notes:** Supports OAuth 2.0 and OAuth 2.1 (PKCE). Can run in stateless mode. Has CLI tool `workspace-cli`. Tool tiers: `core` / `extended` / `complete`.  

**Pro/con for this project:**
- ✅ Covers **both** Calendar AND Tasks in a single MCP server
- ✅ Most feature-complete Google Workspace MCP available
- ✅ Active development (updated May 2026)
- ⚠️ Requires self-hosting (Python + uv/uvx or Docker)
- ⚠️ 110 open issues (but actively maintained)

---

### Option 2: `zcaceres/gtasks-mcp`

| Attribute | Detail |
|-----------|--------|
| **URL** | https://github.com/zcaceres/gtasks-mcp |
| **Stars** | ⭐ 132 |
| **Language** | TypeScript (Bun runtime) |
| **License** | MIT |
| **Transport** | `stdio` only (local Bun/Node process) |
| **Self-hosted** | ✅ Yes — runs locally, requires `bun` or `node` |
| **Claude setup** | `claude_desktop_config.json` only |
| **Last updated** | 2026-03-10 |
| **Open issues** | 18 |

**Tasks tools (6 total):**
| Tool | Description |
|------|-------------|
| `search` | Search tasks by query (client-side filter on title/notes) |
| `list` | List all tasks across all task lists |
| `create` | Create task (title, notes, due date) |
| `update` | Update task (title, notes, status, due date) — uses `patch` |
| `delete` | Delete task by ID |
| `clear` | Clear completed tasks from a list |

**Tasks CRUD:** ✅ Full (Create, Read, Update, Delete, Clear)  
**Subtasks:** ❌ No explicit support — no `parent` parameter in create/update. Raw `parent` field is returned in output but cannot be set.  
**Task lists management:** ❌ No — can list tasks across lists, but cannot create/delete/rename lists.  
**Scopes used:** `https://www.googleapis.com/auth/tasks`  
**Notes:** Simple, lightweight. Distributed via Smithery (`npx @smithery/cli install`). Uses Bun for build/run. Auth via `gcp-oauth.keys.json` + `.gdrive-server-credentials.json`.

**Pro/con for this project:**
- ✅ Simple setup, small codebase
- ✅ Tasks-only, no bloat
- ❌ No subtask creation/management
- ❌ No task list CRUD
- ❌ Only stdio transport (no HTTP/remote)
- ❌ Less active (last update March 2026)

---

### Option 3: Other Google Tasks MCP Servers

| Repository | Stars | Language | Notes |
|------------|-------|----------|-------|
| `sudohakan/gtasks-mcp` | ⭐ 1 | Python | Fork/clone of zcaceres, minimal changes |
| `qaware/mcp-server-gtasks` | ⭐ 0 | Go | Based on go-mcp, early stage |
| `abenke/gtasks-mcp` | ⭐ 0 | TypeScript | Fast MCP server for Google Tasks |

**Verdict:** None of these offer meaningful advantages over Option 1 or 2. Option 1 (`taylorwilsdon`) dominates in features and maturity.

---

## Comparison Table

| MCP | Tasks CRUD | Subtasks | Task Lists CRUD | Self-hosted | Free Plan Compatible | Transport | Stars |
|-----|:----------:|:--------:|:---------------:|:-----------:|:--------------------:|-----------|-------|
| **Official Google Calendar MCP** | ❌ | ❌ | ❌ | ❌ No (remote Google-hosted) | ✅ Yes (but requires Pro+ for custom connectors) | HTTP (Remote) | N/A |
| **`taylorwilsdon/google_workspace_mcp`** | ✅ | ✅ | ✅ | ✅ Yes | ✅ Yes (single connector covers Calendar + Tasks) | stdio / streamable-http | 2,412 |
| **`zcaceres/gtasks-mcp`** | ✅ | ❌ | ❌ | ✅ Yes | ⚠️ No (requires 2nd connector if Calendar MCP also used) | stdio only | 132 |
| `sudohakan/gtasks-mcp` | ✅ | ❌ | ❌ | ✅ Yes | ⚠️ No | stdio | 1 |

---

## Claude Free Plan Limit: 1 Custom Connector

**Fact:** Claude Free tier allows **~1 custom connector** (App Connector / MCP server).  
**Source:** Anthropic documentation and community reports (2026).

### Can Calendar MCP + Tasks MCP coexist on Free?

**Scenario A: Official Calendar MCP + gtasks-mcp**
- ❌ **No** — requires **2 separate connectors** (1 for Calendar, 1 for gtasks)
- Free plan cannot mount both simultaneously
- **Workaround:** Upgrade to **Claude Pro ($20/mo)** for multiple connectors

**Scenario B: `taylorwilsdon/google_workspace_mcp` ONLY**
- ✅ **Yes** — single connector exposes **both Calendar and Tasks** (plus Gmail, Drive, Docs, etc.)
- Uses **one** custom connector slot
- Works on Free plan (if Free plan allows at least 1 custom connector)
- **Caveat:** Must self-host the server (local Python process or cloud instance)

**Claude plan requirements for Custom Connectors:**
- Free: 1 connector (confirmed 2026)
- Pro ($20/mo): Multiple connectors
- Max / Team / Enterprise: Unlimited connectors

**Recommendation for Free users:** If you need both Calendar AND Tasks, use a **unified Workspace MCP** (`taylorwilsdon`) instead of separate official + community servers.

---

## Alternatives Without MCP

### 1. All-day Events in Google Calendar
- **Approach:** Create tasks as all-day calendar events with a special title prefix (e.g., `[TASK] Review quarterly goals`)
- **Pros:** Works with Official Calendar MCP natively; visible in Calendar UI; no extra connector needed
- **Cons:**
  - ❌ No completion tracking (events don't have "done" state)
  - ❌ No subtasks/hierarchy
  - ❌ No task lists separation
  - ❌ Clutters calendar view
  - ❌ Hard to distinguish from real events
- **Verdict:** Poor substitute for real task management

### 2. Generate `.ics` Files with Tasks
- **Approach:** Export tasks as `.ics` (iCalendar format) and import to Google Calendar
- **Pros:** Standard format; works offline; can set VTODO components
- **Cons:**
  - ❌ Google Calendar **ignores VTODO** — only imports VEVENT
  - ❌ One-way sync (no updates back to Tasks)
  - ❌ Manual import process
- **Verdict:** Not viable for bi-directional task sync

### 3. Google Apps Script Automation
- **Approach:** Write Apps Script that bridges Calendar events ↔ Tasks via Google APIs
- **Pros:** Free; runs on Google's servers; can trigger on schedule or event changes
- **Cons:**
  - ❌ Requires separate coding and maintenance
  - ❌ No MCP integration (Claude can't invoke it directly)
  - ❌ Latency (runs on triggers, not real-time)
- **Verdict:** Useful for background sync, but not a replacement for direct Tasks API access

### 4. Python Module (`calendar_integration/tasks_manager.py`)
- **Approach:** Keep existing Python module with direct Google Tasks API calls
- **Pros:** Full API coverage; subtasks support; custom business logic; no connector limits
- **Cons:** Requires OAuth setup; not integrated into Claude's tool ecosystem
- **Verdict:** Best fallback if MCP route is blocked

---

## Recommendation

### For the `life-planning-coach` project

| Goal | Recommended Path |
|------|------------------|
| **Use Tasks via MCP + stay on Free plan** | Use **`taylorwilsdon/google_workspace_mcp`** as a **single unified connector**. It covers Calendar + Tasks + more in one server. Self-host locally or via Docker. |
| **Use official Google Calendar MCP + Tasks** | Requires **Claude Pro ($20/mo)** to add a 2nd connector for a Tasks-only MCP (e.g., `zcaceres/gtasks-mcp`). |
| **Avoid MCP entirely** | Keep **`calendar_integration/tasks_manager.py`** as the canonical Tasks implementation. It already supports full CRUD, subtasks, and task lists. |

### Key Finding

> **The Official Google Calendar MCP does NOT support Tasks API.** This is confirmed by the absence of Tasks scopes in both the Calendar-specific and Workspace-wide MCP documentation.

> **The best MCP-based workaround is a unified community server** (`taylorwilsdon/google_workspace_mcp`), which exposes 6 Tasks tools including full CRUD, subtasks (via `parent` parameter), and task list management — all within a single connector.

> **For Free Claude users**, this is the only viable MCP path that preserves both Calendar and Tasks functionality without upgrading to Pro.

---

## Sources

1. Google Calendar MCP docs: https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server
2. Google Workspace MCP docs: https://developers.google.com/workspace/guides/configure-mcp-servers
3. GitHub API — `taylorwilsdon/google_workspace_mcp`: https://api.github.com/repos/taylorwilsdon/google_workspace_mcp
4. GitHub API — `zcaceres/gtasks-mcp`: https://api.github.com/repos/zcaceres/gtasks-mcp
5. GitHub Search — `google tasks mcp`: https://api.github.com/search/repositories?q=google+tasks+mcp
6. Claude pricing/limit references (web search, March–May 2026)
