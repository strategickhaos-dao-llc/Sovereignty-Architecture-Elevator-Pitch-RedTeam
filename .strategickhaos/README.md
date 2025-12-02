# Strategickhaos Legions of Minds OS

A distributed cognitive governance operating system where codespaces connect to a shared intelligence layer backed by Git.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│         STRATEGICKHAOS LEGIONS OS (Kernel)          │
│  Git Repo = Shared Memory | Commits = Thoughts      │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌──▼──────────┐
│  Codespace 1 │ │ Local   │ │ Cloud VM    │
│  (GitHub)    │ │ Dev Env │ │ (Any Host)  │
└───────┬──────┘ └──┬──────┘ └──┬──────────┘
        │           │            │
        └───────────┼────────────┘
                    │
        ┌───────────▼───────────┐
        │   GitLens Integration │
        │  (Visual Memory Map)  │
        └───────────┬───────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───▼────┐  ┌──────▼──────┐  ┌────▼─────┐
│ Legal  │  │  Technical  │  │ Finance  │
│  Dept  │  │    Dept     │  │   Dept   │
│(Agent) │  │  (Agents)   │  │ (Agent)  │
└───┬────┘  └──────┬──────┘  └────┬─────┘
    │              │               │
    └──────────────┼───────────────┘
                   │
         ┌─────────▼─────────┐
         │   VOTING LAYER    │
         │  (Consensus Req)  │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │  EXECUTION LAYER  │
         │ (Approved Actions)│
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │  DISCORD CONTROL  │
         │  (Human Oversight)│
         └───────────────────┘
```

## Quick Start

### One-Command Deploy (Any Codespace)

```bash
# Run this in ANY codespace to connect to the Legion
./.strategickhaos/kernel/init.sh
```

Or via curl:

```bash
curl -sSL https://raw.githubusercontent.com/<repo>/main/.strategickhaos/kernel/init.sh | bash
```

## Directory Structure

```
.strategickhaos/
├── kernel/
│   ├── config.yml       # Core configuration (departments, voting rules)
│   ├── connect.py       # LegionKernel class - connection protocol
│   ├── daemon.py        # Background service for proposals
│   ├── init.sh          # One-command deployment script
│   └── requirements.txt # Python dependencies
├── proposals/           # Proposal files (JSON)
├── logs/               # Runtime logs
├── discord_bot.py      # Discord human interface
└── README.md           # This file
```

## Components

### 1. Kernel (`kernel/`)

The core of the Legion OS. Provides:

- **LegionKernel** class for connecting any workspace to the collective
- Proposal creation and submission
- Department voting coordination
- Consensus calculation (weighted voting with veto support)
- Execution of approved actions
- Git-backed persistence (every decision is versioned)

### 2. Departments (AI Agents)

Five AI departments vote on proposals:

| Department | Agent | Weight | Veto Power |
|------------|-------|--------|------------|
| Legal | Claude Opus 4 | 3 | ✅ |
| Technical | Qwen/DeepSeek | 2 | ❌ |
| Finance | GPT-4 | 2 | ✅ |
| Ethics | Claude Sonnet 4 | 3 | ✅ |
| Operations | Llama 3.1 | 1 | ❌ |

### 3. Voting Rules

- **Quorum:** 3 departments must participate
- **Threshold:** 60% weighted approval required
- **Veto Blocks:** Any department with veto power can block
- **Timeout:** 5 minutes to gather votes

### 4. Discord Bot (`discord_bot.py`)

Human interface commands:

| Command | Description |
|---------|-------------|
| `!propose <text>` | Submit a new proposal |
| `!status <id>` | Check proposal status |
| `!list [status]` | List all proposals |
| `!departments` | Show departments and voting power |
| `!vote <id> <dept> <decision>` | Manual vote (admin) |
| `!override <id> <action>` | Manual override (admin) |
| `!execute <id>` | Execute approved proposal |

### 5. GitLens Integration

Visual layer showing:

- Proposals as branches (`proposal/<id>`)
- Votes as commit annotations
- Consensus status as branch protection
- Execution history as merge commits

## Configuration

Edit `kernel/config.yml` to customize:

- Departments and their weights
- Voting rules (quorum, threshold, timeout)
- Integration settings (Discord, GitHub)
- Execution policies

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DISCORD_WEBHOOK_URL` | Discord webhook for notifications |
| `DISCORD_BOT_TOKEN` | Token for Discord bot |
| `GOVERNANCE_CHANNEL` | Discord channel ID for governance |
| `GITHUB_TOKEN` | GitHub token for Git operations |
| `GPG_KEY_ID` | GPG key for signed commits |

## Academic Context

> **"Distributed Cognitive Governance: A Git-Native Operating System for Multi-Agent Consensus"**

This system demonstrates that version control can serve as both memory substrate and governance protocol, enabling reproducible, auditable, multi-agent decision-making across heterogeneous compute environments.

## License

Part of the Strategickhaos DAO LLC / Valoryield Engine ecosystem.
