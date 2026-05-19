# User Guide — Kimi Code CLI (Terminal Agent)

> **Platform:** Kimi Code CLI (terminal-based AI agent)  
> **Format:** Directory-based skill (`SKILL.md` + `references/`)  
> **File size:** ~90 KB (SKILL.md 28 KB + refs 62 KB)  
> **Refs:** Loaded via `read_file` tool (directory-based)  
> **MCP:** Supported (manual JSON configuration)  
> **No `memory_space`** — uses file system for persistence

---

## 1. System Requirements

- **Kimi Code CLI** installed (`pip install kimi-cli` or via package manager)
- Terminal with Unicode support
- Python 3.10+
- Node.js (for MCP servers via npx)

### 1.1 Install Kimi Code CLI

```bash
pip install kimi-cli
# Or via uv:
uv tool install kimi-cli
```

Verify installation:
```bash
kimi --version
```

---

## 2. Installation

### 2.1 Create Skill Directory

```bash
mkdir -p ~/.kimi/skills/life-planning-coach
cd ~/.kimi/skills/life-planning-coach
```

### 2.2 Download Files

From GitHub Releases:
```bash
# Download and extract the kimi-cli directory
wget https://github.com/azagreev/life-planning-coach/releases/download/vX.Y.Z/life-planning-coach-vX.Y.Z-kimi-cli.zip
unzip life-planning-coach-vX.Y.Z-kimi-cli.zip
# Or copy from local build:
cp -r /path/to/platforms/kimi-cli/* ~/.kimi/skills/life-planning-coach/
```

Expected structure:
```
~/.kimi/skills/life-planning-coach/
├── SKILL.md
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

### 2.3 Verify Setup

```bash
kimi skill list
# Should show: life-planning-coach
```

---

## 3. MCP Configuration (Manual JSON)

> ⚠️ **Warning:** Kimi Code CLI MCP setup is "super non-friendly" — requires manual JSON editing. Unlike Claude's 1-click install, you must edit config files directly.

### 3.1 Locate Config Directory

```bash
ls ~/.config/kimi/mcp/  # or ~/.kimi/mcp/
```

### 3.2 Google Calendar MCP

Create `~/.config/kimi/mcp/google-calendar.json`:

```json
{
  "name": "google-calendar",
  "transport": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-gcalendar"]
  },
  "env": {
    "GOOGLE_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "your-client-secret"
  }
}
```

### 3.3 Google Drive MCP

Create `~/.config/kimi/mcp/google-drive.json`:

```json
{
  "name": "google-drive",
  "transport": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-gdrive"]
  },
  "env": {
    "GOOGLE_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "your-client-secret"
  }
}
```

### 3.4 Restart Kimi CLI

```bash
kimi mcp reload
# Or restart the kimi CLI session
```

### 3.5 Verify MCP Tools

```bash
kimi mcp list
# Should show: google-calendar, google-drive
```

### 3.6 Getting Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → Enable **Google Calendar API** and **Google Drive API**
3. Go to **Credentials** → **Create OAuth 2.0 Client ID** (Desktop app)
4. Copy `Client ID` and `Client Secret` to the JSON configs above
5. On first use, Kimi CLI will prompt for OAuth authorization

---

## 4. Usage

### 4.1 Starting a Session

```bash
kimi skill use life-planning-coach
```

Or in an existing Kimi CLI session:
```
@life-planning-coach проведи диагностику
```

### 4.2 Natural Language Commands

| What you type | What happens |
|--------------|--------------|
| `Проведи диагностику` | Stage 1 — full diagnostic |
| `Построй цель на 6 месяцев` | Stage 2 — goal architecture |
| `Как прошла неделя?` | Stage 3 — weekly review |
| `Сохрани в Drive` | Saves to Google Drive (if MCP configured) |
| `Добавь в календарь` | Creates calendar event (if MCP configured) |
| `Покажи дашборд` | Opens `life-planning-dashboard.html` |

### 4.3 File System Persistence

Unlike Kimi OK Computer's `memory_space`, Kimi CLI uses the file system:

```bash
# The coach can create local files:
~/.kimi/skills/life-planning-coach/sessions/
├── session-2024-01-15.md
├── wheel-of-life-latest.json
└── goals-active.md
```

---

## 5. Key Differences from Kimi OK Computer

| Feature | Code CLI | OK Computer |
|---------|----------|-------------|
| Refs | `read_file` (directory) | Inlined (single file) |
| MCP | ✅ Supported (manual config) | ❌ Not supported |
| Memory | File system | `memory_space` |
| Calendar | Google Calendar MCP | Text-only export |
| Drive | Google Drive MCP | ❌ No integration |
| Step limit | High (terminal) | ~10 steps (Base Chat) |
| Setup | Terminal + JSON | Web UI (easy) |
| Environment | Local file system | Cloud-only |

---

## 6. Troubleshooting

| Problem | Solution |
|---------|----------|
| "Skill not found" | Check `~/.kimi/skills/` path; run `kimi skill list` |
| `read_file` fails | Ensure `references/` directory exists alongside `SKILL.md` |
| MCP not loading | Check JSON syntax; verify `npx` is installed; check env vars |
| OAuth errors | Regenerate credentials in Google Cloud Console |
| "Command not found" | Ensure `kimi` is in PATH: `which kimi` |
| Large output cut off | Kimi CLI has high token limits; use `kimi --max-tokens` if needed |

---

## 7. Limitations

- **Manual MCP setup** — no GUI for configuration
- **No `memory_space`** — persistence via file system only
- **Requires local setup** — not cloud-based like OK Computer
- **Context window:** Depends on model (K2.6 ~200K tokens)
- **Terminal UI** — no rich HTML rendering (dashboard opens in browser)

---

## 8. Privacy & Data Handling

- Coaching data stored locally on your machine
- Google Calendar/Drive access via your own OAuth credentials
- No data sent to Moonshot AI beyond conversation content
- Full control over MCP servers and their permissions
- See full privacy notice in `SKILL.md` → `## Privacy & Data Handling`
