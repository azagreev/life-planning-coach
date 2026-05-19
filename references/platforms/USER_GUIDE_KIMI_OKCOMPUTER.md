# User Guide — Kimi OK Computer (Web Agent)

> **Platform:** Kimi OK Computer (kimi.com/agent)  
> **Format:** Single Markdown file (self-contained, inline references)  
> **File size:** ~22 KB (815 lines)  
> **Refs:** Fully inlined (no external files)  
> **Memory:** `memory_space` (long-term memory within agent)  
> **MCP:** Not supported (web platform limitation)

---

## 1. System Requirements

- **Moonshot AI account** (kimi.com)
- Access to **OK Computer** agent feature
- Web browser (Chrome/Firefox/Safari)

---

## 2. Installation

### 2.1 Create Agent

1. Go to [kimi.com/agent](https://kimi.com/agent)
2. Click **"Create Agent"** (创建智能体)
3. Fill in:
   - **Name:** `Life Planning Coach`
   - **Description:** `Evidence-based life coaching with Wheel of Life, goal architecture, and habit tracking`
4. In the **System Prompt** field, paste the entire content of `life-planning-coach-vX.Y.Z-kimi.md`
5. Upload `life-planning-dashboard.html` as a **knowledge file** (if supported)
6. Save and publish

### 2.2 Use Memory Space

Kimi OK Computer supports `memory_space` for long-term memory:

1. In agent settings, enable **Memory** (记忆)
2. The skill uses `KIMI_REF` protocol to store:
   - User's Wheel of Life scores
   - Active goals and milestones
   - Habit tracking data
   - Communication style preferences
3. Memory persists across conversations within the same agent

---

## 3. No MCP — Text-Only Calendar

Kimi OK Computer (web) **does not support MCP**. Calendar integration is text-only:

### 3.1 Manual Calendar Export

When the coach suggests a calendar event, you receive:
```markdown
**📅 Calendar Event**
- Title: Coaching Session — Career Review
- Date: 2024-01-15
- Time: 19:00-20:00
- Description: Review progress on career transition plan
```

Copy this text and manually create the event in your Google/Apple calendar.

### 3.2 No Google Drive Integration

- Session notes must be copied manually
- Use the **Export** button in Kimi chat to save conversations

---

## 4. Usage

### 4.1 Starting a Session

1. Open your **Life Planning Coach** agent at kimi.com/agent
2. Type naturally:
   ```
   Привет! Давай проведём диагностику.
   ```
3. The agent uses inlined references to guide the session

### 4.2 Coaching Flow

Same 4-stage evidence-based flow:
1. **Diagnostic** — Wheel of Life, Values Clarification (inlined)
2. **Goal Architecture** — SMART+ goals with milestones (inlined)
3. **Execution** — Weekly reviews, habit loops (inlined)
4. **Deep Work** — Triggering, emotion regulation (inlined)

### 4.3 Key Limitations vs Kimi Code CLI

| Feature | OK Computer | Code CLI |
|---------|-------------|----------|
| Refs | Inlined (~815 lines) | Directory `references/` |
| Memory | `memory_space` (agent-level) | File system + MCP |
| MCP | ❌ Not supported | ✅ Supported |
| Calendar | Text-only export | Google Calendar MCP |
| Drive | ❌ No integration | Google Drive MCP |
| Step limit | ~10 steps (Base Chat) | High limit (terminal) |
| Setup | Web UI (easy) | Terminal + JSON config |

---

## 5. Why Inlined References?

Kimi OK Computer does **not** support `read_file` or directory-based skills. All references are inlined:

- Critical P0 refs: fully inlined with heading demotion
- `dashboard_guide.md`: ultra-condensed to ~100 lines
- `life-planning-dashboard.html`: uploaded as knowledge file (if UI supports)

---

## 6. Troubleshooting

| Problem | Solution |
|---------|----------|
| "Agent not responding" | Check Kimi service status; try refreshing |
| Memory not saving | Ensure Memory is enabled in agent settings |
| "Message too long" | Kimi K2.6 has ~200K context; large inlined refs fit |
| Dashboard not rendering | Upload `life-planning-dashboard.html` as knowledge file |
| Cannot save to Drive | Copy session text manually; use Export button |

---

## 7. Limitations

- **~10 step limit** in Base Chat mode (use Deep Research for longer sessions)
- **No MCP** — no native Calendar/Drive integration
- **No `read_file`** — all refs must be inlined (larger prompt)
- **Context window:** ~200K tokens (K2.6)
- **Mobile:** Works via mobile browser

---

## 8. Privacy & Data Handling

- Coaching data stored in Moonshot AI cloud
- `memory_space` data tied to your Kimi account
- No third-party integrations (no OAuth to Google)
- See Moonshot AI [Privacy Policy](https://www.moonshot.cn/privacy)
- Full privacy notice in `SKILL.md` → `## Privacy & Data Handling`
