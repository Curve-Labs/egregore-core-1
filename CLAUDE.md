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

### Step 1: Check GitHub CLI

```bash
which gh
```

**If not found:**
```
I need to install the GitHub CLI for authentication.
```

Then detect OS and install:
- macOS: `brew install gh`
- Linux: `sudo apt install gh` or `sudo dnf install gh`
- Windows: `winget install GitHub.cli`

### Step 2: Check GitHub Auth

```bash
gh auth status
```

**If not authenticated:**
```
Let me authenticate you with GitHub. This will open your browser.
Click "Authorize" when prompted.
```

Run:
```bash
gh auth login --web -h github.com
```

Wait for user to complete browser auth.

### Step 3: Check Memory Symlink

```bash
ls -la memory
```

**If memory/ doesn't exist or isn't a symlink:**

Check if egregore-memory exists:
```bash
ls ../egregore-memory
```

If not, clone it:
```bash
gh repo clone Curve-Labs/egregore-memory ../egregore-memory
```

Create symlink:
```bash
ln -s ../egregore-memory memory
```

### Step 4: Register User

Get git info:
```bash
git config user.name
```

Ask user:
```
Found your git name: [name]
What should we call you? (short name, like 'jane')
```

Register in Neo4j:
```cypher
MERGE (p:Person {name: $shortName})
ON CREATE SET p.fullName = $fullName, p.joined = date()
RETURN p.name, p.joined
```

### Step 5: Complete

```
Welcome to Egregore, [name]!

You're registered in the knowledge graph.

Commands:
  /activity  — See what's happening
  /handoff   — Leave notes for others
  /quest     — View/create quests
  /add       — Add an artifact
  /save      — Commit and push your work
  /pull      — Get latest from team
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
