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

## Backfill / Wiki Update Problem

**No `update_file` tool means:** every "save Hot_Cache.md" via `create_file` creates a NEW file with the same title. Duplicates accumulate.

### Append-only pattern (recommended workaround)

```
Write:  create_file(title="Hot_Cache_2026-05-26T18:45.md", parentId=wiki_id, textContent=...)
Read:   search_files(query="title contains 'Hot_Cache_' and parentId = '...'", orderBy="modifiedTime desc", pageSize=1)
        → take first result as "current Hot_Cache"
Stale:  manual cleanup via Drive UI periodically (no MCP delete)
```

### Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Append-only with timestamp suffix | Works with MCP-only; full history retained | Storage accumulates; manual cleanup |
| Google Doc native + Drive UI revisions | Native versioning | Updates bypass MCP entirely; mixing patterns |
| Local-only state (skip Drive Wiki) | Simple; no Drive limitations | No cross-session persistence beyond conversation memory |

**Skill recommendation:** Append-only model with `*_{YYYY-MM-DD-HHMM}.md` suffix; latest by `modifiedTime` is canonical. Document expectation that Drive Wiki accumulates per-session snapshots.

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
