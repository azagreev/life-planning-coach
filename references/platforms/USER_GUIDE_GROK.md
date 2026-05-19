# User Guide — Grok 4.3 (xAI)

> **Platform:** Grok 4.3 via xAI (x.com / grok.com)  
> **Format:** Single Markdown file (self-contained, inline references)  
> **File size:** ~28 KB (1190 lines)  
> **Refs:** Fully inlined (no external files)  
> **Connectors:** Native xAI connectors (OAuth, not MCP)

---

## 1. System Requirements

- **xAI account** (free tier available)
- Access to Grok 4.3 (web or mobile app)
- **Native connectors** feature enabled (see below)

---

## 2. Installation

### 2.1 Direct Prompt (Current Method)

Grok does not yet support native "Skills" (forthcoming feature). Use **Direct Prompt** method:

1. Download `life-planning-coach-vX.Y.Z-grok.md` from [GitHub Releases](https://github.com/azagreev/life-planning-coach/releases)
2. Open the file, **copy all content** (Ctrl+A, Ctrl+C)
3. Go to [grok.com](https://grok.com) or x.com Grok
4. Paste the entire content into the first message
5. Add: `"Ты — Life Planning Coach. Начни сессию."`

### 2.2 Grok Projects (Recommended for Repeat Use)

1. Create a **Grok Project** (if available in your region)
2. Paste the SKILL.md content into the Project system prompt
3. Save — now every conversation in this Project starts with the coach context

### 2.3 Future: Native Skills (Leaked UI)

xAI is testing native Skills/Custom GPTs. When available:
- Upload `life-planning-coach-vX.Y.Z-grok.md` as a Skill
- Enable in conversations via `@life-planning-coach`

---

## 3. Native Connectors (Not MCP)

Grok uses **xAI Native Connectors**, not MCP. These are pre-built integrations:

### 3.1 Google Calendar Connector

1. Go to [grok.com/connectors](https://grok.com/connectors) (or Settings → Connectors)
2. Find **Google Calendar** → Click **Connect**
3. OAuth with your Google account
4. Grant calendar read/write permissions

> The Google Calendar connector is managed by xAI, not via MCP.

### 3.2 Google Drive Connector

1. Same [grok.com/connectors](https://grok.com/connectors) page
2. Find **Google Drive** → Click **Connect**
3. OAuth + grant Drive permissions

> The Google Drive connector uses native OAuth, not MCP.

### 3.3 Other Connectors

Grok may support additional connectors (Spotify, Notion, etc.). The skill auto-adapts to available connectors.

> **Difference from MCP:** Native connectors are managed by xAI, not via JSON config. One-click OAuth, no manual setup.

---

## 4. Usage

### 4.1 Starting a Session

With Direct Prompt method:
```
[Вставлено содержимое grok.md]

Начни диагностику. Я чувствую застой в карьере.
```

With Grok Projects:
```
Проведи диагностику Wheel of Life
```

### 4.2 Coaching Flow

Same 4-stage flow as Claude:
1. **Diagnostic** — inlined references include all methods
2. **Goal Architecture** — structured planning
3. **Execution** — weekly reviews, habits
4. **Deep Work** — triggering, emotions, authentic goals

### 4.3 Key Differences from Claude

| Feature | Grok | Claude |
|---------|------|--------|
| Ref loading | Inlined (instant) | `read_file` (on-demand) |
| File size | ~28 KB single file | ~170 KB ZIP |
| Connectors | Native connector (OAuth) | MCP JSON config |
| Setup | Copy-paste prompt | ZIP upload |
| Persistence | Projects (if available) | Conversation only |

### 4.4 Cross-Platform Transition

Moving from Claude or Kimi to Grok? Your data stays in Google Drive (if you used Drive MCP/connector). Ask Grok to read your existing `Life Planning Coach Wiki` folder and continue from where you left off.

---

## 5. Why Single File?

Grok does **not** support directory-based skills or `read_file` tool. All 7 critical references are **inlined** into SKILL.md:

- `diagnostic_methods.md` → inlined with heading demotion
- `communication_style.md` → inlined
- `authentic_goal_filter.md` → inlined
- `goal_architecture.md` → inlined
- `weekly_review.md` → inlined
- `habit_loop.md` → inlined
- `emotion_regulation.md` → inlined
- `dashboard_guide.md` → ultra-condensed (~100 lines)

This makes the file larger (~1190 lines) but ensures Grok has immediate access to all coaching methods.

---

## 6. Troubleshooting

| Problem | Solution |
|---------|----------|
| "Message too long" | Grok has large context window (~1M tokens), but if hit — use Direct Prompt in chunks |
| Connectors not showing | Check if your region has connector access; try web vs mobile |
| Skill "forgets" context | Use Grok Projects for persistence; otherwise re-paste in new conversation |
| Calendar events not created | Ensure connector is connected and has write permissions |

---

## 7. Limitations

- **No native Skills yet** — rely on Direct Prompt or Projects
- **Connector availability varies by region**
- **Context window:** ~1M tokens (very large; memory is conversation-scoped — use Grok Projects for cross-session persistence)
- **Mobile:** Copy-paste is harder on mobile; use desktop for initial setup

---

## 8. Privacy & Data Handling

- Coaching data stays in xAI/Grok conversation
- Google Calendar/Drive access via OAuth (you control scopes)
- xAI may use conversation data per their [Privacy Policy](https://x.ai/privacy)
- See full privacy notice in `SKILL.md` → `## Privacy & Data Handling`
