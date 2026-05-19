# Cross-Platform Comparison — Life Planning Coach

> Quick reference: which platform is right for you?

---

## At a Glance

| Feature | Claude.ai | Grok 4.3 | Kimi OK Computer | Kimi Code CLI |
|---------|-----------|----------|------------------|---------------|
| **Best for** | Power users, MCP fans | xAI ecosystem, large context | Easy web setup | Developers, terminal users |
| **Setup difficulty** | Medium (ZIP upload) | Easy (copy-paste) | Very Easy (web UI) | Hard (terminal + JSON) |
| **Skill format** | ZIP (directory) | Single `.md` | Single `.md` | Directory (`SKILL.md` + `references/`) |
| **Ref loading** | `read_file` (on-demand) | Inlined (instant) | Inlined (instant) | `read_file` (on-demand) |
| **File size** | ~170 KB | ~28 KB | ~22 KB | ~90 KB |
| **Context efficiency** | ⭐⭐⭐ Excellent | ⭐⭐ Good | ⭐⭐ Good | ⭐⭐⭐ Excellent |
| **Lines in SKILL.md** | 311 | 1,190 | 815 | 323 |

---

## Integrations

| Integration | Claude.ai | Grok 4.3 | Kimi OK Computer | Kimi Code CLI |
|-------------|-----------|----------|------------------|---------------|
| **Google Calendar** | ✅ MCP (1-click) | ✅ Native OAuth | ❌ Text-only | ✅ MCP (manual JSON) |
| **Google Drive** | ✅ MCP (1-click) | ✅ Native OAuth | ❌ No integration | ✅ MCP (manual JSON) |
| **Save sessions** | Auto (MCP Drive) | Auto (connector) | Manual copy | File system |
| **Persistent memory** | ❌ Conversation only | ❌ Conversation only | ✅ `memory_space` | ✅ File system |

---

## Coaching Capabilities

All platforms run the **same 4-stage evidence-based flow**:

1. **Diagnostic** — Wheel of Life, Values Clarification
2. **Goal Architecture** — SMART+ goals, milestones, habits
3. **Execution Support** — Weekly reviews, energy checks, habit tracking
4. **Deep Work** — Triggering precision, emotion regulation, authentic goals

| Capability | Claude.ai | Grok 4.3 | Kimi OK Computer | Kimi Code CLI |
|------------|-----------|----------|------------------|---------------|
| All 4 stages | ✅ | ✅ | ✅ | ✅ |
| 11 Wheel of Life domains | ✅ | ✅ | ✅ | ✅ |
| Authentic Goal Filter | ✅ | ✅ | ✅ | ✅ |
| Communication Style | ✅ | ✅ | ✅ | ✅ |
| Dashboard (`life-planning-dashboard.html`) | ✅ | ✅ | ✅ | ✅ |
| Deep Why / 5 Whys | ✅ | ✅ | ✅ | ✅ |
| TTM / MI techniques | ✅ | ✅ | ✅ | ✅ |

---

## Model & Performance

| Spec | Claude.ai | Grok 4.3 | Kimi OK Computer | Kimi Code CLI |
|------|-----------|----------|------------------|---------------|
| **Model** | Claude 3.5/4 Sonnet | Grok 4.3 | Kimi K2.6 | Kimi K2.6 |
| **Context window** | ~200K tokens | ~1M tokens | ~200K tokens | ~200K tokens |
| **Step limit** | High | High | ~10 (Base Chat) | High |
| **Response speed** | Fast | Very Fast | Fast | Fast |
| **Reasoning** | Excellent | Excellent | Excellent | Excellent |

---

## Platform-Specific Notes

### Claude.ai (Primary)
- **Pros:** Best MCP ecosystem, clean directory structure, on-demand ref loading
- **Cons:** Requires Pro/Team plan for Skills; ZIP upload step
- **Unique:** Most mature integration ecosystem

### Grok 4.3
- **Pros:** Largest context window (~1M), native connectors (easy OAuth), fast responses
- **Cons:** No native Skills yet (use Direct Prompt); single large file
- **Unique:** Best for users already in xAI ecosystem

### Kimi OK Computer
- **Pros:** Easiest setup (web UI), `memory_space` for persistence, no config files
- **Cons:** No MCP, ~10 step limit, text-only calendar, all refs inlined
- **Unique:** Best for beginners who want immediate coaching without technical setup

### Kimi Code CLI
- **Pros:** Directory-based (efficient), MCP support, file system persistence, high step limit
- **Cons:** Hardest setup (terminal + manual JSON), no GUI
- **Unique:** Best for developers who want full control and local data

---

## Decision Tree

```
Are you comfortable with terminal and JSON config?
├── YES → Kimi Code CLI (most powerful, local control)
└── NO → Do you have Claude Pro/Team?
    ├── YES → Claude.ai (best ecosystem)
    └── NO → Do you use xAI/Grok regularly?
        ├── YES → Grok 4.3 (largest context, native connectors)
        └── NO → Kimi OK Computer (easiest setup, web-only)
```

---

## Quick Start by Platform

| Platform | Time to first session | Steps |
|----------|----------------------|-------|
| **Claude.ai** | ~5 min | Download ZIP → Upload to Claude → Start chat |
| **Grok 4.3** | ~2 min | Copy `.md` → Paste to Grok → Start chat |
| **Kimi OK Computer** | ~3 min | Go to kimi.com/agent → Create agent → Paste `.md` → Start chat |
| **Kimi Code CLI** | ~15 min | Install CLI → Create skill dir → Configure MCP JSON → Start session |

---

## File Naming in Releases

| Platform | Release File |
|----------|--------------|
| Claude.ai | `life-planning-coach-vX.Y.Z.zip` or `.skill` |
| Grok 4.3 | `life-planning-coach-vX.Y.Z-grok.md` |
| Kimi OK Computer | `life-planning-coach-vX.Y.Z-kimi.md` |
| Kimi Code CLI | `life-planning-coach-vX.Y.Z-kimi-cli/` (directory) |

---

*Last updated: v0.10.2*
