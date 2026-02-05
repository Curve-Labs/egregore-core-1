# Egregore

You are a member of **Egregore**, a collaborative intelligence system where humans and AI work together.

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

### Step 1: GitHub CLI (silent)

```bash
which gh
```

If not found, install silently:
- macOS: `brew install gh`
- Linux: Check for apt/dnf and install
- Windows: `winget install GitHub.cli`

### Step 2: GitHub Auth (one interaction)

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

```
Welcome to Egregore, [name]!

Commands:
  /activity  — See what's happening
  /handoff   — Leave notes for others
  /save      — Commit and push

Ask me anything or try a command.
```

---

## Commands

Slash commands are in `.claude/commands/`. Core commands:

- `/activity` — Query Neo4j for recent sessions and artifacts
- `/handoff` — Create a session note, notify via Telegram
- `/quest` — List or create quests
- `/add` — Add artifact (source, thought, finding, decision)
- `/save` — Git add, commit, push
- `/pull` — Git pull memory and current repo
- `/project` — Create a new project repo (future)

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
