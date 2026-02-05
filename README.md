# Egregore

Collaborative intelligence system where humans and AI work together.

## Quick Start

1. Open terminal in this folder
2. Run: `claude`
3. When prompted:
   - **"Trust this folder?"** → Select **Yes, proceed**
   - **"Use this API key?"** → Select **No** (use your Claude Code subscription)
4. Say: `set me up`

The setup will:
- Install dependencies (uv, GitHub CLI)
- Authenticate you with GitHub
- Clone shared memory
- Register you in the knowledge graph

## Commands

| Command | Description |
|---------|-------------|
| `/activity` | See recent team activity |
| `/handoff` | Leave notes for others |
| `/quest` | View or create quests |
| `/add` | Add an artifact |
| `/save` | Commit and push |
| `/pull` | Get latest from team |
| `/onboarding` | Learn how Egregore works |

## Architecture

- **egregore-core** — This repo. Hub with commands and config.
- **egregore-memory** — Shared knowledge base (symlinked to `memory/`)
- **Neo4j** — Graph database for fast queries
- **Telegram** — Team notifications

## Requirements

- [Claude Code](https://claude.ai/code) installed
- GitHub account (you'll be added as collaborator)
