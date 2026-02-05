# Egregore

You are a member of **Egregore**, a collaborative intelligence system where humans and AI work together.

## What is Egregore?

Egregore is a system for human-AI collaboration with persistent memory. It provides:

- **Shared Memory** — Knowledge that persists across sessions and people
- **Neo4j Graph** — Fast queries across sessions, artifacts, quests, and people
- **Telegram Integration** — Team notifications and bot queries
- **Git-backed Storage** — Everything versioned and auditable

When you work here, sessions get logged. When you discover something important, you `/add` it. When you're done, you `/handoff` to leave notes for others.

---

## Entry Point Behavior

**When user says "set me up" or similar:**

Run the full setup flow below.

**On subsequent visits:**

Query Neo4j for recent sessions:
```cypher
MATCH (s:Session)-[:BY]->(p:Person)
WHERE s.date >= date() - duration('P2D')
RETURN count(s) AS recent, collect(DISTINCT p.name) AS who
```

Then greet:
```
Welcome back. [X] sessions in the last 2 days.
/activity to see what's happening.
```

---

## Setup Flow

When user says "set me up", "getting started", "new here", or similar:

**Do everything automatically. Don't ask permission. Just show progress:**

```
Setting up Egregore...
```

### Step 1: Install Dependencies (silent)

**uv (for Neo4j MCP):**
```bash
which uvx 2>/dev/null
```
If not found, install silently:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**GitHub CLI:**
```bash
which gh
```
If not found, install silently:
- macOS: `brew install gh`
- Linux: Check for apt/dnf and install
- Windows: `winget install GitHub.cli`

After installing uv, tell user ONCE:
```
Installed uv for MCP servers. Please restart Claude Code after setup to activate them.
```

### Step 2: GitHub Auth (one interaction, if needed)

```bash
gh auth status 2>&1
```

If not authenticated, tell user ONCE:
```
Opening browser for GitHub login. Click "Authorize" and come back.
```

Then run:
```bash
gh auth login --web -h github.com -p https
```

Continue automatically after auth completes.

### Step 3: Clone Memory (silent)

Check if memory symlink works:
```bash
ls memory/conversations 2>/dev/null
```

If not, clone and link silently:
```bash
gh repo clone Curve-Labs/egregore-memory ../egregore-memory 2>/dev/null || true
ln -sf ../egregore-memory memory
```

### Step 4: Register User

Get git info:
```bash
git config user.name
```

**Only question to ask:**
```
What should we call you? (short name, like 'jane')
```

Register in Neo4j using the mcp__neo4j__write_neo4j_cypher tool:
```cypher
MERGE (p:Person {name: $shortName})
ON CREATE SET p.fullName = $fullName, p.joined = date()
RETURN p.name, p.joined
```

### Step 5: Done

If uv was just installed, tell user:
```
Welcome to Egregore, [name]!

Setup complete. Since I installed uv, please:
1. Type /exit to close Claude Code
2. Run 'claude' again to activate the MCP servers

Then you'll have full access to Neo4j and Telegram.
```

Otherwise:
```
███████╗ ██████╗ ██████╗ ███████╗ ██████╗  ██████╗ ██████╗ ███████╗
██╔════╝██╔════╝ ██╔══██╗██╔════╝██╔════╝ ██╔═══██╗██╔══██╗██╔════╝
█████╗  ██║  ███╗██████╔╝█████╗  ██║  ███╗██║   ██║██████╔╝█████╗
██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║   ██║██║   ██║██╔══██╗██╔══╝
███████╗╚██████╔╝██║  ██║███████╗╚██████╔╝╚██████╔╝██║  ██║███████╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

Welcome, [name]!

Commands:
  /activity   — See what's happening
  /ask        — Ask questions (self or others)
  /handoff    — Leave notes for others
  /quest      — View or create quests
  /add        — Capture artifacts
  /save       — Commit and push
  /pull       — Get latest
  /onboarding — Learn how Egregore works

Ask me anything or try a command.
```

---

## Commands

Slash commands are in `.claude/commands/`. Available commands:

| Command | Description |
|---------|-------------|
| `/activity` | See recent sessions, artifacts, and team activity |
| `/ask` | Ask questions — self-reflection or async to others |
| `/handoff` | Create a session note, notify via Telegram |
| `/quest` | List or create quests (ongoing explorations) |
| `/add` | Add artifact (source, thought, finding, decision) |
| `/save` | Git add, commit, push |
| `/pull` | Git pull memory and current repo |
| `/onboarding` | Learn how Egregore works as a living organization |
| `/project` | Create a new project repo (future) |

---

## Architecture

```
egregore-core/          ← You are here (hub)
├── memory/ → ../egregore-memory/   (symlink)
├── .claude/commands/
├── .mcp.json           (Neo4j + Telegram)
└── CLAUDE.md

egregore-memory/        ← Shared knowledge
├── artifacts/
├── conversations/
├── quests/
└── people/
```

**Neo4j** mirrors the filesystem for fast queries.
**Git** is the source of truth for all knowledge.
**Telegram bot** enables team queries and notifications.

---

## Collaboration Protocol

### During Work
- Document decisions as you make them
- Use `/handoff` to leave notes for others
- Use `/add` to capture findings, sources, thoughts

### After Sessions
- Run `/save` to commit and push
- Handoffs automatically notify recipients via Telegram

---

## Git Operations

**Always use SSH for Egregore repos. Never HTTPS.**

The `gh` CLI handles auth via HTTPS+OAuth, but for manual operations:
```bash
git clone git@github.com:Curve-Labs/egregore-core.git
git clone git@github.com:Curve-Labs/egregore-memory.git
```
