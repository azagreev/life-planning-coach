# Google Drive Integration Reference (MCP)

> **Runtime**: Claude.ai web/desktop + Kimi Code CLI (requires Google Drive MCP server)
> **Not supported**: Grok (uses native connectors), Kimi OK Computer (web, no MCP)
> **Setup**: Claude — Settings → Customize → Connectors → Google Drive → Connect (Max plan); Kimi CLI — manual JSON config
> **Version**: 0.1.0
> **PoC verified**: 2026-05-26 on Claude Max — see [docs/research/mcp_poc_log.md §Drive PoC](../docs/research/mcp_poc_log.md). Direct MCP execution via current session. 13 ops, 10 schema quirks. **Critical gap: no update/delete tools.**

---

## MCP Tools (8 confirmed)

| Tool | Group | Description |
|------|-------|-------------|
| `get_file_metadata` | Read | Metadata only (name, MIME, parent, dates, size, owner). Optional `excludeContentSnippets`. |
| `read_file_content` | Read | "Natural language representation" — **strips markdown markup**. Supported MIME: Google native, Office, PDF, images. **NOT text/markdown → silent `{}`**. |
| `download_file_content` | Read | **Faithful round-trip** as base64-encoded raw bytes. Use for text/markdown. |
| `search_files` | Read | Structured query (`title`, `fullText`, `mimeType`, `parentId`, `owner`, dates). |
| `list_recent_files` | Read | Sort by `recency` / `lastModified` / `lastModifiedByMe`. |
| `get_file_permissions` | Read | List sharing/ACL. No `set_file_permissions` (aligned with safety rules). |
| `create_file` | Write | Files AND folders (mimeType `application/vnd.google-apps.folder`). |
| `copy_file` | Write | Duplicate. **Defaults to ROOT, not source folder** — always pass explicit `parentId`. |

### ❌ NOT available (critical gaps)

- `update_file` / `append_to_file` / `create_revision` — **NO content modification**
- `delete_file` / `move_to_trash` — **NO file removal**
- Explicit folder tools (`create_folder`, `list_folder_contents`, `move_to_folder`)

---

## Schema Quirks (must follow exactly)

PoC 2026-05-26 discovered:

1. **`text/markdown` NOT in `read_file_content` supported list** → silent `{}` empty response. **For .md files ALWAYS use `download_file_content`** and decode base64.
2. **`download_file_content` returns base64** even for plain text — decode required.
3. **`text/plain` and `text/csv` auto-convert to Google formats** by default — set `disableConversionToGoogleType: true` to keep raw MIME.
4. **Files identified by ID, NOT title** — same title can have many duplicate files. Title is just metadata.
5. **`canAddChildren: false` in folder metadata is MISLEADING** — child creation may still succeed.
6. **`copy_file` ignores "same folder" promise** — defaults to root. ALWAYS pass `parentId`.
7. **`fullText contains` searches entire Drive** — no auto-scope; combine with `parentId =` for folder-scope.
8. **`nextPageToken` appears even when results < pageSize** — phantom pagination.
9. **`fileSize` returned as string** — parse to int if needed.
10. **`search_files` returns `contentSnippet`** with truncated body — use `excludeContentSnippets: true` for speed/privacy.

---

## Wiki Persistence Architecture — Path A (committed 2026-05-26)

After research synthesis (PoC findings + community precedents — Karpathy LLM Wiki, Justin Norris Apps Script mirroring, Zapier hybrid pattern), the skill commits to **Path A: append-only with timestamp suffix + Apps Script auto-cleanup**.

### Write protocol (skill side)

```
create_file(
  parentId=<wiki_subfolder_id>,
  title="<Category>_<ISO8601_compact>.md",   // e.g. "Hot_Cache_2026-05-26T18-45.md"
  textContent=<rendered_snapshot>,
  contentMimeType="text/markdown",
  disableConversionToGoogleType=true
)
```

ISO format: `YYYY-MM-DDTHH-MM` (colons replaced with `-` для совместимости с filename conventions).

### Read protocol (skill side)

```
search_files(
  query="title contains '<Category>_' and parentId = '<wiki_subfolder_id>'",
  orderBy="modifiedTime desc",
  pageSize=1
)
→ first result = "current" state
→ download_file_content(fileId) → base64-decode → parse markdown
```

⚠️ **NEVER use `read_file_content` для `.md`** — returns `{}` silently. ALWAYS `download_file_content`.

### Cleanup protocol (user side, one-time setup)

Pre-built Apps Script: [`references/templates/lpc_wiki_cleanup.gs`](templates/lpc_wiki_cleanup.gs).

User setup (~3 min, paste-once):
1. <https://script.google.com> → New project
2. Paste contents of `lpc_wiki_cleanup.gs` в Code.gs
3. `dryRun()` once для preview
4. `installTrigger()` once → daily 03:00 trigger
5. Forget about it

Поведение: keeps last 5 most recent per category + всё < 30 дней. Surplus → Drive trash (recoverable 30 days). Configurable via constants in script.

### Why this architecture

| Concern | Path A address |
|---------|----------------|
| MCP no `update_file` | Each write = new file with timestamp; "current" = latest by modifiedTime |
| MCP no `delete_file` | User-side Apps Script (independent of MCP) автоматически handles cleanup |
| File accumulation | Apps Script keeps 5+recent + 30-day window; bounded growth |
| Cross-session persistence | Drive holds state server-side; survives device/context loss |
| Audit trail | 5+ snapshots per category = built-in undo / inspection |
| Works on all platforms | Pure MCP read/create only; no Desktop dependency |
| Forward compat | When Anthropic ships `update_file`, swap `create_file` call site — no architecture change |

### Trade-offs accepted

- Storage: ~365×N×size/year если user never cleanups; bounded если daily trigger running
- 3-min one-time Apps Script setup (skippable → degrades к manual cleanup)
- Reads have extra `search_files` call vs known-ID direct read (sub-second через direct MCP)
- 5-snapshot retention may not be enough для users wanting full history — increase `MIN_RETAIN_PER_PREFIX` в script

---

## Alternative architectures (НЕ chosen — documented для context)

| Path | Brief | Why not |
|------|-------|---------|
| **B: Tiered Desktop community MCP** | [piotr-agier/google-drive-mcp](https://github.com/piotr-agier/google-drive-mcp) full CRUD на Desktop | Power-user only; ~30 min OAuth+GCloud setup. **§Advanced below.** |
| **C: State в conversation memory only** | Drive read-only; state в memory + JSON on demand | Loses cross-session persistence |
| **D: Migrate в Obsidian+Git** | Per Karpathy LLM Wiki pattern | Requires Desktop + local file MCP; defeats portable cloud Wiki |
| **F: Zapier MCP hybrid** | Native Drive reads + Zapier MCP для writes | Не verified Zapier MCP available на web; **BACKLOG investigation** |

---

## Advanced: Path B (Desktop power-user setup с full CRUD)

Для users на **Claude Desktop** / **Claude Code CLI** (NOT claude.ai web) кто хочет native `update_file`/`delete_file`:

### Community MCP servers с full CRUD

- **[piotr-agier/google-drive-mcp](https://github.com/piotr-agier/google-drive-mcp)** — Drive/Docs/Sheets/Slides/Calendar в одном. Tools: `updateTextFile`, `deleteItem`, `renameItem`, `moveItem`.
- **[a-bonus/google-docs-mcp](https://github.com/a-bonus/google-docs-mcp)** — "Ultimate" Google Suite MCP.
- **[StackOne](https://www.stackone.com/connectors/googledrive/mcp/)** — Managed, 53 actions, commercial.

### Setup outline (piotr-agier example, ~30 min)

1. Google Cloud Project, enable Drive/Docs/Sheets/Slides/Calendar APIs
2. OAuth credentials — Desktop app type (NOT Web)
3. Place в `~/.config/google-drive-mcp/gcp-oauth.keys.json`
4. Install MCP server (npm/clone)
5. Add to `claude_desktop_config.json` или Claude Code config
6. First run triggers browser OAuth
7. Skill detects `update_file` tool availability → switches от Path A appended к direct overwrite

⚠️ **Не для claude.ai web** — custom MCP servers not supported (только Anthropic-curated). Web users stay на Path A.

### Future: when Anthropic ships `update_file` natively

Skill abstraction (`save_state(template, content)` wrapper) позволяет swap Path A → direct overwrite в одном месте. No protocol re-write needed.

---

## Prompt Patterns

### Bootstrap LPC_Wiki (first-time, on first Drive connect)

```
1. create_file(parentId=root, title="Life Planning Coach Wiki",
               contentMimeType="application/vnd.google-apps.folder")
   → save wiki_root_id

2. For each subfolder in ["00_Raw", "01_Wiki", "02_Instructions", "03_Dashboard", "05_Archive"]:
   create_file(parentId=wiki_root_id, title=subfolder,
               contentMimeType="application/vnd.google-apps.folder")
   → save subfolder_ids

3. For each template in 8 templates:
   create_file(parentId=target_subfolder_id, title="{template}_{date}.md",
               textContent=rendered_template_content,
               contentMimeType="text/markdown",
               disableConversionToGoogleType=true)
   → record IDs in conversation_state.persistence_retry.drive.template_ids
```

### Append-only save (Hot_Cache pattern)

```
create_file(
  parentId=wiki_01_id,
  title="Hot_Cache_2026-05-26T19:15.md",
  textContent={rendered_hot_cache},
  contentMimeType="text/markdown",
  disableConversionToGoogleType=true
)
```

### Read current state (latest by modifiedTime)

```
search_files(
  query="title contains 'Hot_Cache_' and parentId = '{wiki_01_id}'",
  orderBy="modifiedTime desc",
  pageSize=1
)
→ first result.id → download_file_content(fileId) → base64-decode
```

### Read existing user document (Google Doc)

```
search_files(query="title contains '{name}' and mimeType = 'application/vnd.google-apps.document'")
→ get id → read_file_content(fileId)  // OK for Google Docs, strips markup acceptable
```

---

## Latency Expectations (from PoC 2026-05-26)

Direct MCP execution (this session): **all ops sub-second** wall-clock.

User-experience latency (via claude.ai chat with LLM round-trip): expect 5-15s per op (analog to Calendar's 20-35s but Drive ops are simpler/faster).

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `read_file_content` returns `{}` | MIME not in supported list (e.g. text/markdown) | Use `download_file_content` + decode base64 |
| Markdown markup stripped (`#` → `\#`) | `read_file_content` is natural-lang repr | Use `download_file_content` for faithful round-trip |
| Created file but appears as Google Doc | Auto-conversion for text/plain | Set `disableConversionToGoogleType: true` |
| Same-title file created instead of updated | No `update_file` tool exists | Use append-only with timestamp suffix |
| Cannot delete test file | No `delete_file` tool | Manual via Drive UI (right-click → trash) |
| `copy_file` landed in root, not source folder | "Same folder" default doesn't work | ALWAYS pass explicit `parentId` |
| `fullText` search returned files from other folders | No auto-scope to parent | Add `parentId = 'X'` to query |
| `nextPageToken` present despite no more results | Phantom pagination | Following may return empty; don't auto-recurse |
| `fileSize` is string, not number | API quirk | Parse to int: `parseInt(file.fileSize, 10)` |
| Search returned my private files | Connector has full Drive scope | Skill should scope queries to `parentId = wiki_root_id` |

---

## Daily Top-3 / Tasks (NOT in Drive scope)

Google Tasks is in separate Google product, **NOT covered by Drive connector**. Per Calendar PoC: Tasks MCP also absent from Anthropic directory. Conversational tasks (Claude as proxy) remain the path.

---

## See also

- [`calendar_integration.md`](calendar_integration.md) — sibling reference for Google Calendar MCP
- [`docs/research/mcp_poc_log.md` §Drive PoC](../docs/research/mcp_poc_log.md) — full PoC log with ops + responses
- [`templates/AI_Instructions.md`](templates/AI_Instructions.md) — Bootstrap + Backfill protocols (updated 2026-05-26 with PoC findings)
