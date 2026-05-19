# User Guide — Claude.ai (Primary Platform)

> **Platform:** Claude.ai (Anthropic)  
> **Format:** ZIP skill (MCS — Model Context Protocol Skill)  
> **File size:** ~170 KB  
> **Refs:** Loaded via `read_file` tool (directory-based)  
> **MCP:** Supported (1-click install from Claude desktop app)

---

## 1. System Requirements

- **Claude.ai web** or **Claude desktop app** (macOS/Windows)
- Account with Pro/Team plan (Skills feature required)
- `references/` directory readable by Claude (auto-loaded from ZIP)

---

## 2. Installation

### 2.1 From ZIP (Recommended)

1. Download `life-planning-coach-vX.Y.Z.zip` from [GitHub Releases](https://github.com/azagreev/life-planning-coach/releases)
2. Open Claude → **Settings** → **Capabilities**
3. Enable **"Code execution and file creation"**
4. Go to **Customize** → **Skills** → **+** → **Upload a skill**
5. Select the downloaded ZIP file
6. The skill appears as `/life-planning-coach` in the prompt

### 2.2 From Source (Developers)

```bash
git clone https://github.com/azagreev/life-planning-coach.git
cd life-planning-coach
bash scripts/build-skill.sh
# Upload generated dist/life-planning-coach-v*.zip to Claude
```

---

## 3. MCP Integration (Google Calendar + Drive)

Claude supports MCP servers for external tool integration.

### 3.1 Google Calendar

1. Open Claude desktop app → **Settings** → **Developer** → **Edit Config**
2. Add the [Google Calendar MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/gcalendar):
   ```json
   {
     "mcpServers": {
       "google-calendar": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-gcalendar"],
         "env": {
           "GOOGLE_CLIENT_ID": "your-client-id",
           "GOOGLE_CLIENT_SECRET": "your-client-secret"
         }
       }
     }
   }
   ```
3. Restart Claude → authorize OAuth → Calendar tool appears automatically

### 3.2 Google Drive

1. Install [Google Drive MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive):
   ```json
   {
     "mcpServers": {
       "google-drive": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-gdrive"],
         "env": {
           "GOOGLE_CLIENT_ID": "your-client-id",
           "GOOGLE_CLIENT_SECRET": "your-client-secret"
         }
       }
     }
   }
   ```
2. Same OAuth flow as Calendar

> **Note:** The skill auto-detects Calendar/Drive availability and adjusts coaching flows (e.g., scheduling sessions, saving session notes).

---

## 4. Usage

### 4.1 Starting a Session

Type in any Claude conversation:
```
/life-planning-coach
```
Or mention the skill by name:
```
@life-planning-coach я хочу разобраться с карьерой
```

### 4.2 What Happens Next

1. **Stage 1 — Diagnostic:** Claude asks about your current situation using evidence-based methods (Wheel of Life, Values Clarification, etc.)
2. **Stage 2 — Goal Architecture:** Together you build a structured goal with milestones and habits
3. **Stage 3 — Execution Support:** Weekly reviews, energy checks, habit tracking
4. **Stage 4 — Deep Work:** Triggering precision, emotion regulation, authentic goal filtering

### 4.3 Key Commands (Natural Language)

| What you say | What happens |
|-------------|--------------|
| "Проведи диагностику" | Stage 1 — full diagnostic session |
| "Построй план на 3 месяца" | Stage 2 — goal architecture |
| "Как прошла неделя?" | Stage 3 — weekly review |
| "Почему я прокрастинирую?" | Stage 4 — triggering precision analysis |
| "Сохрани в Drive" | Saves session summary to Google Drive (if MCP connected) |
| "Добавь в календарь" | Creates calendar event (if MCP connected) |

---

## 5. File Structure (Inside ZIP)

```
life-planning-coach/
├── SKILL.md              # Main instructions (311 lines)
├── references/
│   ├── diagnostic_methods.md
│   ├── communication_style.md
│   ├── authentic_goal_filter.md
│   ├── goal_architecture.md
│   ├── weekly_review.md
│   ├── habit_loop.md
│   ├── emotion_regulation.md
│   └── dashboard_guide.md
└── life-planning-dashboard.html
```

Claude loads `references/` files on-demand via `read_file` tool.

---

## 6. Troubleshooting

| Problem | Solution |
|---------|----------|
| "Skill not found" | Check that ZIP uploaded successfully; re-upload if needed |
| "Cannot read references" | Ensure `references/` folder is inside ZIP root, not nested |
| Calendar not working | Check MCP config JSON syntax; restart Claude app |
| Skill responds generically | Start with `/life-planning-coach` to activate context |
| Large file warnings | Normal — dashboard.html is 62 KB, refs are loaded on demand |

---

## 7. Limitations

- **Context window:** ~200K tokens (Claude 3.5 Sonnet) — references loaded on demand
- **No persistent memory** between conversations (use Google Drive MCP to save sessions)
- **Web-only** for now (no mobile app skill support)

---

## 8. Privacy & Data Handling

- All coaching data stays in your Claude conversation
- Google Calendar/Drive access is OAuth-scoped (you control permissions)
- No data is sent to third parties except via your own MCP connections
- See full privacy notice in `SKILL.md` → `## Privacy & Data Handling`
