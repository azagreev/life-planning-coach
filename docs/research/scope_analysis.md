# MCP Scope & Documentation Analysis

**Research Date:** 2026-05-16  
**Researcher:** Sub-agent (Gate 5b)  
**Scope:** Official Google Calendar Remote MCP (`https://calendarmcp.googleapis.com/mcp/v1`) + Anthropic Custom Connectors

---

## Official Calendar MCP

### Setup Steps

1. **Create a Google Cloud project** (or select existing).
2. **Enable APIs:**
   - `calendar-json.googleapis.com` — Google Calendar API
   - `calendarmcp.googleapis.com` — Google Calendar MCP API
3. **Configure OAuth consent screen:**
   - Go to **Google Auth Platform > Branding**
   - App name: e.g. "Calendar MCP Server"
   - Audience: Internal (Workspace) or External (personal accounts)
   - Add contact info, agree to policy, click Create
   - If External: add test users under **Audience > Test users**
4. **Add OAuth scopes to consent screen:**
   - Go to **Data Access > Add or Remove Scopes**
   - Under *Manually add scopes*, paste the scopes listed below
   - Click **Add to Table > Update > Save**
5. **Create OAuth 2.0 Client ID/Secret for Claude:**
   - Go to **Google Auth Platform > Clients > Create Client**
   - Select **Web application** as the application type
   - Enter a name
   - In **Authorized redirect URIs**, add:
     ```
     https://claude.ai/api/mcp/auth_callback
     ```
   - Click Create and copy Client ID + Client Secret
6. **Configure in Claude:**
   - Go to **Settings > Connectors > Add custom connector**
   - Server name: e.g. "Google Calendar"
   - Remote MCP server URL: `https://calendarmcp.googleapis.com/mcp/v1`
   - In **Advanced settings**, enter OAuth Client ID and Client Secret
   - Click Add, then authenticate via the OAuth flow

> ⚠️ **Important:** Google docs note that for **Gemini CLI** you create a **Desktop app** OAuth client, but for **Claude.ai / Claude Desktop** you MUST create a **Web application** client with the redirect URI above.

---

### OAuth Scopes

Google's official documentation lists **only the following read-only scopes** for the Calendar MCP server:

```
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/calendar.events.freebusy
https://www.googleapis.com/auth/calendar.events.readonly
```

**Critical Discrepancy:** The same official documentation confirms 8 tools including **write operations** (`create_event`, `delete_event`, `update_event`, `respond_to_event`). Read-only OAuth scopes alone are insufficient for write operations.

**Hypotheses:**
1. **Documentation gap:** Google may have omitted write scopes (`calendar.events`, `calendar`) from the public docs. The Japanese developer article about Claude Code's Calendar connector notes "OAuth grants calendar read/write access at the Google API level" — implying broader scopes are actually requested during the OAuth flow.
2. **Server-side augmentation:** The remote MCP server (hosted by Google) may transparently request additional Google-internal scopes after the initial user consent.
3. **Tool-level permission model:** Anthropic's connector framework may enforce a second permission layer. The Japanese article explicitly states: *"Tool permissions (viewable post-authentication) allow blocking specific operations like event creation/modification"* and describes a *"granularity mismatch: Google OAuth scopes operate at the API resource level, while tool permissions operate at the semantic level."*

**Recommendation for PoC:** During Gate 1 (OAuth flow), capture the **actual consent screen** to verify which scopes are truly requested.

---

### Tools Reference

The official Google Calendar MCP server exposes **8 tools** (confirmed in Google's docs):

| Tool | Parameters (inferred from community schemas + API patterns) | Notes |
|------|-----------------------------------------------------------|-------|
| `create_event` | `summary` (string, required), `start`/`end` (datetime objects with `dateTime` + optional `timeZone`), `calendarId` (string, optional, default: "primary"), `description` (string), `location` (string), `attendees` (array of `{email, displayName}`), `recurrence` (array of RRULE strings) | **Recurrence support unconfirmed** for official server; community servers support `recurrence: ["RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR"]` |
| `delete_event` | `eventId` (string, required), `calendarId` (string, optional) | Idempotent — 404 on already-deleted event is a no-op |
| `get_event` | `eventId` (string, required), `calendarId` (string, optional) | Returns full event object including reminders, transparency, visibility |
| `list_calendars` | No parameters (or pagination token) | Returns calendars accessible to the user; supports pagination |
| `list_events` | `calendarId` (string, optional, default: "primary"), `timeMin`/`timeMax` (RFC3339), `maxResults` (number), `orderBy` ("startTime" or "updated"), `singleEvents` (boolean, expand recurring instances), `pageToken` (string) | Google Calendar API default `maxResults` is 250, max is 2500. Returns `nextPageToken` for pagination |
| `respond_to_event` | `eventId` (string, required), `calendarId` (string, optional), `responseStatus` (enum: "accepted", "tentative", "declined") | Likely mirrors Google Calendar API `events.patch` with `attendees[].responseStatus` |
| `suggest_time` | Likely `timeMin`/`timeMax`, `attendees` (array of emails), `duration` (minutes), `calendarId` | Wraps Google Calendar API `freebusy.query` |
| `update_event` | `eventId` (string, required), `calendarId` (string, optional), plus any of: `summary`, `description`, `start`, `end`, `location`, `attendees` | Likely uses PATCH semantics (partial update) |

> ⚠️ **Caveat:** Exact parameter schemas for the **official** remote MCP server are **not published** in Google's docs. The table above synthesizes patterns from:
> - Community MCP servers that wrap Google Calendar API v3 (`peadams21/Google-Calendar-MCP-Server`, `guinacio/mcp-google-calendar`, `nspady/google-calendar-mcp`)
> - Google Calendar API v3 reference documentation
> - The `calendarmcp.ai` third-party service docs (unrelated to Google's official server)
>
> **Gate 1 PoC must call `tools/list` via MCP to capture the actual JSON schemas.**

---

### Limitations

#### Rate Limits
- **No MCP-specific rate limits documented.** The server delegates to Google Calendar API v3, which has:
  - **1,000,000 queries/day** per project (default quota)
  - **500 requests per 100 seconds** per user
  - **3,000 requests per 100 seconds** per project
- High-volume usage (e.g. scanning full year) can trigger `403/429` errors. Exponential backoff recommended.

#### Pagination
- `list_events`: Returns `nextPageToken` for pagination. Google Calendar API max is **2,500 events per request**.
- `list_calendars`: Also paginated via `pageToken`.
- **Claude does not natively support MCP pagination yet** (as of 2024-12-13 per `mcp-golang` docs). The LLM must explicitly handle `nextPageToken` in follow-up tool calls.

#### Multiple Calendar Support
- **Supported.** Every tool accepts an optional `calendarId` parameter (defaults to `"primary"`).
- `list_calendars` returns all accessible calendars including shared and secondary calendars.
- `suggest_time` / `list_events` can theoretically query across multiple calendars by ID.

#### Read-Only Mode
- **Not explicitly documented** for the official Calendar MCP server.
- **Two ways to enforce read-only behavior:**
  1. **OAuth scope selection:** If the user only grants read-only scopes (`calendar.events.readonly`), write tools will fail at the API level.
  2. **Claude org-level restrictions:** Team/Enterprise plan owners can restrict connector actions (e.g. allow read, block write) under **Organization settings > Connectors**.
- Anthropic's connector framework shows read/write capability badges per connector.

#### Recurring Events (RRULE)
- **Official docs do not mention recurrence support.**
- Community servers universally support `recurrence: ["RRULE:..."]` arrays.
- Google Calendar API v3 natively supports RRULE, EXRULE, RDATE, EXDATE.
- **Status: UNCONFIRMED for official Calendar MCP.** Must be tested in Gate 2 PoC.

#### No Tasks API Support
- The official Calendar MCP server does **not** include Google Tasks API tools.
- This aligns with the project's stated concern: Tasks would require a **second connector** (community MCP server) or direct API integration.

---

### User Experience

#### Known Issues (from public bug reports)
- **Claude Code repo used as catch-all:** There is no public repo for Claude Desktop / web UI / connector bugs. Users file everything in `anthropics/claude-code`. Issue #32056 documents this.
- **"Tools not exposed despite successful connection":** Issue #30457 (Google Drive) and `modelcontextprotocol#1675` (Claude.ai custom connectors) describe cases where the connector shows "Connected" but tools are invisible to the model.
- **Permission prompt fatigue:** Per the Japanese developer article (2026-03-08), *"Every calendar query triggers a permission prompt unless explicitly disabled with `--dangerously-skip-permissions`"*. This applies to Claude Code CLI; web UI behavior may differ.

#### Platform Availability
- **Claude.ai web:** ✅ Supported (requires Web app OAuth client with redirect URI `https://claude.ai/api/mcp/auth_callback`)
- **Claude Desktop:** ✅ Supported (same custom connector setup)
- **Claude Code CLI:** ⚠️ Supported but with friction — the `/mcp` command provides connection status, but connector management requires context-switching to Claude.ai settings
- **Claude Mobile (iOS/Android):** ✅ Once connected on web/desktop, available on mobile via account sync

#### Latency
- **No published benchmarks** for Calendar MCP specifically.
- Google Calendar API v3 latency is typically **200–800 ms** for simple operations.
- Remote MCP adds one network hop (Anthropic's cloud → Google's MCP server → Calendar API), likely adding **100–300 ms**.
- **Estimated total latency per tool call: 300 ms – 1.2 s** depending on complexity and pagination.

---

## Anthropic Custom Connectors

### Plan Requirements

| Plan | Custom Connectors | Notes |
|------|-------------------|-------|
| **Free** | **1 custom connector only** | Confirmed by Anthropic support docs and multiple third-party sources. Select directory connectors (including Google Workspace) recently added to Free plan (Feb 2026). |
| **Pro** ($20/mo) | Unlimited directory + custom | Individual setup |
| **Max** ($100–200/mo) | Unlimited + higher usage limits | 5× or 20× Pro message limits |
| **Team** ($30/user/mo) | Unlimited, org-managed | Owner must enable connectors at org level first |
| **Enterprise** | Unlimited, org-managed + admin controls | Custom pricing |

### Free Plan Implication for This Project
- If the user is on **Claude Free**, they can add **only ONE custom connector**.
- **Google Calendar MCP would consume the single slot.**
- **Google Tasks would require a second connector** (or a community server that bundles both, but the official Calendar MCP does not include Tasks).
- **Decision point:** If Tasks API is required, the user must either:
  1. Upgrade to Pro ($20/mo), OR
  2. Use a single community MCP server that bundles Calendar + Tasks (e.g. `taylorwilsdon/google_workspace_mcp`), OR
  3. Keep the Python module for Tasks and use MCP only for Calendar.

### How to Add a Remote MCP Connector in claude.ai
1. Navigate to **Customize > Connectors** (or click "+" in chat → "Add connectors")
2. Click **"Add custom connector"**
3. Enter:
   - **Server name:** e.g. "Google Calendar"
   - **Remote MCP server URL:** `https://calendarmcp.googleapis.com/mcp/v1`
4. Click **Advanced settings** → enter OAuth Client ID and Client Secret
5. Click **Add**
6. Complete the OAuth consent flow in the popup
7. The connector appears in your conversation via the "+" → "Connectors" menu

---

## Sources

- [https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server](https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server) — Official Google Calendar MCP setup guide (scopes, redirect URI, tools list)
- [https://developers.google.com/workspace/guides/configure-mcp-servers](https://developers.google.com/workspace/guides/configure-mcp-servers) — Google Workspace MCP overview (multi-product setup, OAuth consent screen)
- [https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) — Anthropic custom connectors guide (network requirements, plan info)
- [https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) — Anthropic connectors directory guide (Free plan = 1 custom connector limit)
- [https://claudecode.jp/en/news/engineer/claude-code-google-calendar-connector](https://claudecode.jp/en/news/engineer/claude-code-google-calendar-connector) — Japanese developer article on Claude Code + Google Calendar connector (permission prompts, granularity mismatch, read/write access)
- [https://github.com/anthropics/claude-code/issues/32056](https://github.com/anthropics/claude-code/issues/32056) — GitHub issue documenting lack of dedicated connector bug repo; references connector bugs filed in claude-code
- [https://github.com/anthropics/claude-code/issues/30457](https://github.com/anthropics/claude-code/issues/30457) — "Google Drive connector shows connected but tools not exposed"
- [https://github.com/modelcontextprotocol/specification/issues/1675](https://github.com/modelcontextprotocol/specification/issues/1675) — "Claude.ai custom connectors tools not visible despite successful connection"
- [https://github.com/peadams21/Google-Calendar-MCP-Server](https://github.com/peadams21/Google-Calendar-MCP-Server) — Community MCP server with published tool schemas (recurrence, attendees, calendarId)
- [https://github.com/guinacio/mcp-google-calendar](https://github.com/guinacio/mcp-google-calendar) — Community MCP server with RRULE support documentation
- [https://calendarmcp.ai/docs](https://calendarmcp.ai/docs) — Third-party CalendarMCP service docs (pagination patterns, multi-calendar support) — **NOT Google's official server; used for pattern reference only**
- [https://www.getpassionfruit.com/blog/how-to-connect-claude-mcp-to-your-entire-marketing-stack-with-claude-connector](https://www.getpassionfruit.com/blog/how-to-connect-claude-mcp-to-your-entire-marketing-stack-with-claude-connector) — Third-party pricing matrix confirming Free = 1 custom connector
- [https://help.vwo.com/hc/en-us/articles/56850624406297](https://help.vwo.com/hc/en-us/articles/56850624406297) — VWO help article confirming "Free plan allows configuring only one custom connector"
- [https://rebeccamdeprey.com/blog/build-custom-connector-claude-cowork](https://rebeccamdeprey.com/blog/build-custom-connector-claude-cowork) — Blog confirming "Free users can connect one custom connector"
- [https://developers.google.com/calendar/api/v3/reference](https://developers.google.com/calendar/api/v3/reference) — Google Calendar API v3 reference (underlying API for rate limits, pagination, event fields)
- [https://www.cnet.com/tech/services-and-software/anthropic-expands-claudes-free-tier-with-more-features/](https://www.cnet.com/tech/services-and-software/anthropic-expands-claudes-free-tier-with-more-features/) — CNET article (Feb 2026) confirming Free plan now includes select connectors including Google Workspace apps

---

## Open Questions Requiring PoC Verification

1. **OAuth scope verification:** Does the actual OAuth consent screen request write scopes (`calendar.events`, `calendar`) or only the three read-only scopes documented?
2. **Tool schemas:** What are the exact JSON Schema parameters for each of the 8 official tools? Must capture via `tools/list`.
3. **Recurrence support:** Does `create_event` accept `recurrence` array with RRULE strings?
4. **Latency baseline:** What is real-world latency for `create_event`, `list_events`, `update_event` via the remote MCP endpoint?
5. **Error formats:** How are token expiry, rate limits, and permission denied surfaced in tool responses?
6. **Read-only enforcement:** If only read-only scopes are granted, do write tools fail gracefully with a clear error message?
7. **Multi-calendar behavior:** Can `list_events` query shared calendars the user has access to but does not own?
8. **Free plan directory vs custom:** Is Google's Calendar MCP available as a pre-built directory connector (no custom connector slot needed) or must it always be added as a custom connector?
