---
status: ready_to_file
target_repo: anthropics/claude-ai-mcp
drafted: 2026-05-28
backlog_item: File Anthropic GitHub issue evidence (Path E lobbying)
rice: 60
related:
  - docs/research/mcp_poc_log.md (source evidence — Drive PoC §)
  - references/drive_integration.md (Path A workaround we shipped)
---

# Draft: Drive connector evidence issue for `anthropics/claude-ai-mcp`

> **Status:** Ready to file. Requires user action — Claude cannot post on external repos from the project's automation context.
> **Why this repo (not `anthropics/claude-code`):** The existing report [anthropics/claude-code#51040](https://github.com/anthropics/claude-code/issues/51040) is labeled `invalid` because Claude Code (CLI) is not where claude.ai web connectors live. `anthropics/claude-ai-mcp` is the repo explicitly for MCP-integration feedback ("Report issues related to MCP integration with Claude here").

## One-click filing

Open this URL in a browser — it prefills the title and body on GitHub's new-issue form so you can review and submit:

<https://github.com/anthropics/claude-ai-mcp/issues/new?title=Drive+connector%3A+confirm%2Fprioritize+update_file+%2B+delete_file+%28with+PoC+evidence%29&body=Filing+this+with+reproducible+evidence+from+a+2026-05-26+PoC+on+a+Claude+Max+account%2C+in+case+it+helps+prioritize+the+Drive+connector+write-tools+surface.+Cross-references+the+closed-as-invalid+%5Banthropics%2Fclaude-code%2351040%5D%28https%3A%2F%2Fgithub.com%2Fanthropics%2Fclaude-code%2Fissues%2F51040%29%2C+moved+here+as+this+seems+to+be+the+right+repo+for+connector+feedback.%0A%0A%23%23+Summary%0A%0AThe+Google+Drive+connector+exposes+8+tools%2C+but+the+write+group+is+incomplete%3A%0A%0A%7C+Group+%7C+Tools+available+%7C+Tools+NOT+available+%7C%0A%7C-------%7C----------------%7C---------------------%7C%0A%7C+Read+%7C+%60get_file_metadata%60%2C+%60read_file_content%60%2C+%60download_file_content%60%2C+%60search_files%60%2C+%60list_recent_files%60%2C+%60get_file_permissions%60+%7C+%E2%80%94+%7C%0A%7C+Write+%7C+%60create_file%60%2C+%60copy_file%60+%7C+%2A%2A%60update_file%60+%2F+%60append_to_file%60+%2F+%60create_revision%60%2A%2A%2C+%2A%2A%60delete_file%60+%2F+%60move_to_trash%60%2A%2A%2C+explicit+folder+ops+%7C%0A%0AWithout+%60update_file%60+or+%60delete_file%60%2C+%22Wiki-like%22+use+cases+%28persistent+state+that+updates+over+time%29+require+client-side+workarounds+%E2%80%94+timestamp-suffixed+append-only+writes+plus+a+user-managed+Apps+Script+for+cleanup.%0A%0AFor+comparison%2C+the+%2A%2AGoogle+Calendar%2A%2A+connector+has+full+CRUD+%288+tools+incl.+%60update_event%60%2C+%60delete_event%60+%E2%80%94+these+%2Ado%2A+work%2C+despite+the+original+issue%27s+claim%29.+The+Drive+asymmetry+is+the+actual+blocker.%0A%0A%23%23+Reproducible+PoC+evidence%0A%0AFull+log+with+13+Drive+ops+%2B+10+schema+findings%3A+https%3A%2F%2Fgithub.com%2Fazagreev%2Flife-planning-coach%2Fblob%2Fmain%2Fdocs%2Fresearch%2Fmcp_poc_log.md%23drive-poc-2026-05-26-same-day%0A%0ASpecific+evidence+relevant+to+this+gap%3A%0A%0A-+%2A%2ASame-title+%60create_file%60+does+NOT+overwrite%2A%2A+%E2%80%94+two+files+coexist+in+the+same+folder+with+identical+title%2C+different+IDs+%28verified+at+Gate+D-4%29%0A-+%2A%2ANo+%60update_file%60+tool+exists%2A%2A+%E2%80%94+explored+every+documented+tool+surface%0A-+%2A%2ANo+%60delete_file%60+tool+exists%2A%2A+%E2%80%94+cleanup+blocked+at+PoC+end+%28Gate+D-5%29%2C+required+manual+Drive+UI+multi-select+%E2%86%92+trash%0A-+%2A%2A%60copy_file%60+ignores+%22same+folder%22+default%2A%2A+%E2%80%94+files+copied+to+root+unless+explicit+%60parentId%60+passed+%28quirk+%2327%29%0A%0A%23%23+Why+this+matters%0A%0AThe+connector+description+%28%22organizing+files+scattered+across+your+Drive%22%29+is+hard+to+reconcile+with+the+actual+tool+surface%2C+where+the+only+%22organizing%22+action+is+%60copy_file%60.+Use+cases+that+work+today+%28read+existing+user+docs%2C+bootstrap+initial+folder+structure%29+are+stable%3B+use+cases+that+require+any+modification+of+existing+files+fall+back+to+manual+Drive+UI.%0A%0A%23%23+Workaround+we+shipped%0A%0AFor+our+skill%2C+we+built+%2A%2APath+A%2A%2A+%28documented+in+%5Breferences%2Fdrive_integration.md%5D%28https%3A%2F%2Fgithub.com%2Fazagreev%2Flife-planning-coach%2Fblob%2Fmain%2Freferences%2Fdrive_integration.md%29%29%3A%0A%0A-+Each+save+%3D+new+%60create_file%60+with+timestamp-suffixed+title%0A-+Reads+pick+latest+by+%60modifiedTime%60%0A-+User-side+Apps+Script+%28paste-once%2C+~3+min%29+prunes+to+last-N-per-prefix%0A%0AWorks%2C+but+requires+extra+user+setup+that+wouldn%27t+be+needed+if+%60update_file%60+existed.%0A%0A%23%23+Requested%0A%0APrioritization+signal%3A+consider+adding+%60update_file%60+%28or+%60replace_file_content%60%29+and+%60delete_file%60+%28or+%60move_to_trash%60%29+to+the+Drive+connector+tool+surface.+The+semantics+are+well-defined+in+the+underlying+Google+API+and+the+asymmetry+vs+Calendar+suggests+this+isn%27t+a+fundamental+design+constraint.%0A%0AHappy+to+provide+more+PoC+data+if+useful.%0A>

## Optional: redirect comment on `#51040`

Once filed, a short comment on the existing [#51040](https://github.com/anthropics/claude-code/issues/51040) helps anyone searching land in the right place:

> Filed with PoC evidence at `anthropics/claude-ai-mcp#NN` (where NN = new issue number). Partial correction: Calendar `update_event` / `delete_event` *do* work — the actual gap is Drive-only.

## Manual filing (if the prefill URL fails)

If GitHub rejects the prefill (rare, but the body is ~3.9 KB encoded), file manually with the title and body below.

### Title

```
Drive connector: confirm/prioritize update_file + delete_file (with PoC evidence)
```

### Body

Filing this with reproducible evidence from a 2026-05-26 PoC on a Claude Max account, in case it helps prioritize the Drive connector write-tools surface. Cross-references the closed-as-invalid [anthropics/claude-code#51040](https://github.com/anthropics/claude-code/issues/51040), moved here as this seems to be the right repo for connector feedback.

## Summary

The Google Drive connector exposes 8 tools, but the write group is incomplete:

| Group | Tools available | Tools NOT available |
|-------|----------------|---------------------|
| Read | `get_file_metadata`, `read_file_content`, `download_file_content`, `search_files`, `list_recent_files`, `get_file_permissions` | — |
| Write | `create_file`, `copy_file` | **`update_file` / `append_to_file` / `create_revision`**, **`delete_file` / `move_to_trash`**, explicit folder ops |

Without `update_file` or `delete_file`, "Wiki-like" use cases (persistent state that updates over time) require client-side workarounds — timestamp-suffixed append-only writes plus a user-managed Apps Script for cleanup.

For comparison, the **Google Calendar** connector has full CRUD (8 tools incl. `update_event`, `delete_event` — these *do* work, despite the original issue's claim). The Drive asymmetry is the actual blocker.

## Reproducible PoC evidence

Full log with 13 Drive ops + 10 schema findings: https://github.com/azagreev/life-planning-coach/blob/main/docs/research/mcp_poc_log.md#drive-poc-2026-05-26-same-day

Specific evidence relevant to this gap:

- **Same-title `create_file` does NOT overwrite** — two files coexist in the same folder with identical title, different IDs (verified at Gate D-4)
- **No `update_file` tool exists** — explored every documented tool surface
- **No `delete_file` tool exists** — cleanup blocked at PoC end (Gate D-5), required manual Drive UI multi-select → trash
- **`copy_file` ignores "same folder" default** — files copied to root unless explicit `parentId` passed (quirk #27)

## Why this matters

The connector description ("organizing files scattered across your Drive") is hard to reconcile with the actual tool surface, where the only "organizing" action is `copy_file`. Use cases that work today (read existing user docs, bootstrap initial folder structure) are stable; use cases that require any modification of existing files fall back to manual Drive UI.

## Workaround we shipped

For our skill, we built **Path A** (documented in [references/drive_integration.md](https://github.com/azagreev/life-planning-coach/blob/main/references/drive_integration.md)):

- Each save = new `create_file` with timestamp-suffixed title
- Reads pick latest by `modifiedTime`
- User-side Apps Script (paste-once, ~3 min) prunes to last-N-per-prefix

Works, but requires extra user setup that wouldn't be needed if `update_file` existed.

## Requested

Prioritization signal: consider adding `update_file` (or `replace_file_content`) and `delete_file` (or `move_to_trash`) to the Drive connector tool surface. The semantics are well-defined in the underlying Google API and the asymmetry vs Calendar suggests this isn't a fundamental design constraint.

Happy to provide more PoC data if useful.

---

## After filing — close-out checklist

- [ ] Issue filed at `anthropics/claude-ai-mcp#__` (record number here)
- [ ] (Optional) Redirect comment on `anthropics/claude-code#51040`
- [ ] Update `BACKLOG.md` Active Candidates entry "File Anthropic GitHub issue evidence" → Archived/Done with filed-issue link
- [ ] Update this draft's frontmatter `status:` from `ready_to_file` to `filed_YYYY-MM-DD_#NN`
