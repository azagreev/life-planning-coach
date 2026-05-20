# 🧭 Life Planning Coach

> **Evidence-based life coaching** across Claude.ai, Grok (xAI), and Kimi (OK Computer + Code CLI).  
> **Версия:** 0.12.0 | [Releases](https://github.com/azagreev/life-planning-coach/releases) | [CHANGELOG](CHANGELOG.md)

---

## What Is This?

A modular, cross-platform coaching skill built on peer-reviewed methods:

- **Wheel of Life** (11 сфер, incl. spirituality & values)
- **Authentic Goal Filter** (Stage 1&period;5 / Фильтр аутентичных целей) — screens goals against intrinsic motivation
- **Goal Architecture** — SMART+ goals with milestones and habits
- **Weekly Review** — evidence-based retrospective protocol
- **Habit Loop** — Cue-Routine-Reward with tracking
- **Emotion Regulation** — DBT-informed techniques
- **Triggering Precision** — pinpoint procrastination root causes
- **Communication Style** — адаптивный стиль коучинга под пользователя

**4-Stage Coaching Flow:**
1. **Diagnostic** → 2. **Goal Architecture** → 3. **Execution** → 4. **Deep Work**

---

## Quick Platform Selector

| Platform | Best For | Setup | Calendar | Drive | File |
|----------|----------|-------|----------|-------|------|
| **Claude.ai** | Power users, MCP | ZIP upload | ✅ MCP | ✅ MCP | `.zip` / `.skill` |
| **Grok** (xAI) | xAI users, large context | Copy-paste | ✅ Native OAuth | ✅ Native OAuth | `-grok.md` |
| **Kimi OK Computer** | Easy web setup | Web agent | ❌ Text-only | ❌ No | `-kimi.md` |
| **Kimi Code CLI** | Developers, terminal | Dir + JSON | ✅ MCP (manual) | ✅ MCP (manual) | `-kimi-cli/` |

**→ [Detailed Comparison](references/platforms/CROSS_PLATFORM_COMPARISON.md)**  
**→ [Decision Tree](references/platforms/CROSS_PLATFORM_COMPARISON.md#decision-tree)**

---

## Quick Start

### Claude.ai (ZIP Skill)

1. Download `life-planning-coach-v0.10.2.zip` from [Releases](https://github.com/azagreev/life-planning-coach/releases)
2. Claude → Settings → Capabilities → enable "Code execution and file creation"
3. Customize → Skills → + → Upload ZIP
4. Type `/life-planning-coach` in any chat

**→ [Full Claude Guide](references/platforms/USER_GUIDE_CLAUDE.md)**

### Grok (xAI) — Single File

1. Download `life-planning-coach-v0.10.2-grok.md`
2. Copy all content, paste into [grok.com](https://grok.com)
3. Add: `Ты — Life Planning Coach. Начни сессию.`

**→ [Full Grok Guide](references/platforms/USER_GUIDE_GROK.md)**

### Kimi OK Computer (Web Agent)

1. Go to [kimi.com/agent](https://kimi.com/agent)
2. Create Agent → paste `life-planning-coach-v0.10.2-kimi.md` into system prompt
3. Save and chat

**→ [Full Kimi OK Computer Guide](references/platforms/USER_GUIDE_KIMI_OKCOMPUTER.md)**

### Kimi Code CLI (Terminal)

```bash
mkdir -p ~/.kimi/skills/life-planning-coach
cp -r platforms/kimi-cli/* ~/.kimi/skills/life-planning-coach/
kimi skill use life-planning-coach
```

**→ [Full Kimi CLI Guide](references/platforms/USER_GUIDE_KIMI_CLI.md)**

---

## Project Structure

```
life-planning-coach/
├── platforms/              # Platform-specific builds
│   ├── claude/SKILL.md     # 311 lines, directory + read_file
│   ├── grok/SKILL.md       # 1,190 lines, fully inlined
│   ├── kimi/SKILL.md       # 815 lines, fully inlined
│   └── kimi-cli/SKILL.md   # 323 lines, directory + read_file
├── references/             # Coaching methods & guides
│   ├── diagnostic_methods.md
│   ├── communication_style.md
│   ├── authentic_goal_filter.md
│   ├── goal_architecture.md
│   ├── weekly_review.md
│   ├── habit_loop.md
│   ├── emotion_regulation.md
│   ├── dashboard_guide.md
│   ├── science_backing.md
│   ├── calendar_integration.md
│   └── platforms/          # User guides & comparisons
│       ├── USER_GUIDE_CLAUDE.md
│       ├── USER_GUIDE_GROK.md
│       ├── USER_GUIDE_KIMI_OKCOMPUTER.md
│       ├── USER_GUIDE_KIMI_CLI.md
│       └── CROSS_PLATFORM_COMPARISON.md
├── tests/                  # 248+ tests (unit + system + e2e)
├── scripts/
│   ├── build-skill.sh      # Build all platform artifacts
│   └── build-platform-skill.py  # Generate platform SKILls
├── dist/                   # Release artifacts
├── SKILL.master.md         # Platform-agnostic source
├── CHANGELOG.md
├── ROADMAP.md
└── BACKLOG.md
```

---

## Building from Source

```bash
# Generate all platform files
python3 scripts/build-platform-skill.py all

# Build release artifacts (ZIP, .skill, .md files)
bash scripts/build-skill.sh

# Run tests
python3 -m pytest tests/ -q
```

---

## Testing

- **248+ tests** covering structure, content, and platform compliance
- **Golden dataset** (`tests/e2e/`) — 20 behavioral test cases
- **Evaluation rubric** — LLM-as-a-Judge for coaching quality
- **Manual test protocol** — `tests/e2e/MANUAL_TEST_RUN.md`

```bash
python3 -m pytest tests/ -q
```

---

## Privacy & Disclaimer

- **Not therapy.** This is coaching, not clinical treatment. For mental health concerns, consult a licensed professional.
- **Your data:** Coaching content stays in your AI platform conversation. MCP/connector access is OAuth-scoped and controlled by you.
- **No telemetry.** This project does not collect usage data.
- See full privacy notice in each platform's `SKILL.md`.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Key rules:

- New code → new tests
- Release only via `bash scripts/release.sh X.Y.Z`
- Commit format: `<type>: <description>` (`feat`, `fix`, `docs`, `chore`, `test`, `refactor`)

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for upcoming features and [BACKLOG.md](BACKLOG.md) for ideas.

---

## License

MIT License — see [LICENSE](LICENSE)

---

<p align="center">
  <a href="references/platforms/CROSS_PLATFORM_COMPARISON.md">Compare Platforms</a> •
  <a href="references/platforms/USER_GUIDE_CLAUDE.md">Claude Guide</a> •
  <a href="references/platforms/USER_GUIDE_GROK.md">Grok Guide</a> •
  <a href="references/platforms/USER_GUIDE_KIMI_OKCOMPUTER.md">Kimi Web Guide</a> •
  <a href="references/platforms/USER_GUIDE_KIMI_CLI.md">Kimi CLI Guide</a>
</p>
