# Obsidian Neural Mesh — Live Brain Graph Architecture

**Genesis Lock:** Increment 3449 | Architect: 1067614449693569044

A sovereign knowledge graph system that integrates Obsidian, Discord, and Git for real-time brain synchronization and board member receipt generation.

## 🏛️ Architecture Overview

The Obsidian Neural Mesh creates a **sovereign knowledge graph system** that:

1. **Archive Vault** — Central repository of:
   - Licenses (Unity, Unreal, NinjaTrader, GitHub Copilot)
   - APIs (Discord, GitHub, NinjaTrader, OpenAI, Anthropic)
   - MCP tools (Sequential Thinking, Filesystem, Git, Brave Search)
   - Code libraries (SwarmGate, Quantum Splicer, ReflexShell)

2. **Obsidian Integration** — Living brain per department:
   - Each brain has: `METHODOLOGY.md`, sandbox path, Git branch
   - Graph view color-coded by quadrant (#athena = red, #lyra = cyan, etc.)
   - Dataview queries for real-time connections
   - Auto-commits via Obsidian Git plugin

3. **Board Member Receipts** — Provenance documents that include:
   - Genesis lock (increment 3449, architect snowflake)
   - Licenses held
   - API access
   - MCP tools available
   - Current methodology (embedded)
   - Recent file changes (Dataview query)
   - Graph connections (linked notes)

4. **Real-Time Sync** — Pipeline that:
   - File change → graph update → Git commit → Discord notification
   - Receipt generation → Claude verification → Discord post
   - Methodology update → diff embed in Discord

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- Discord Bot Token
- Obsidian (with community plugins)

### Deployment

```bash
# Step 1: Clone the repository
git clone https://github.com/strategickhaos/sovereignty-architecture.git
cd sovereignty-architecture

# Step 2: Set environment variables
export DISCORD_TOKEN="your_discord_bot_token"
export OBSIDIAN_VAULT_PATH="/vault/legions-of-minds"
export GITHUB_REPO="git@github.com:strategickhaos/obsidian-neural-mesh.git"

# Step 3: Run deployment script
chmod +x deploy-obsidian-mesh.sh
./deploy-obsidian-mesh.sh

# Step 4: Start the Discord bot
source venv/bin/activate
python scripts/obsidian_bot.py
```

### Manual Setup

If you prefer manual setup:

```bash
# Create vault structure
mkdir -p /vault/legions-of-minds/{brains,sandboxes,templates,api,licenses}

# Create department brain directories
mkdir -p /vault/legions-of-minds/brains/{athena,lyra,nova,ipower}
touch /vault/legions-of-minds/brains/athena/METHODOLOGY.md
touch /vault/legions-of-minds/brains/lyra/METHODOLOGY.md
touch /vault/legions-of-minds/brains/nova/METHODOLOGY.md
touch /vault/legions-of-minds/brains/ipower/METHODOLOGY.md

# Initialize Git
cd /vault/legions-of-minds
git init
git remote add origin git@github.com:strategickhaos/obsidian-neural-mesh.git

# Install Python dependencies
pip install -r requirements.obsidian-mesh.txt
```

## 📋 Department Structure

| Department | Quadrant | Color | Tag |
|------------|----------|-------|-----|
| **Athena** | Strategy & Intelligence | 🔴 #FF4500 | #athena |
| **Lyra** | Creative & Innovation | 🔵 #00CED1 | #lyra |
| **Nova** | Engineering & Development | 🟣 #9400D3 | #nova |
| **IPower** | Finance & Trading | 🟡 #FFD700 | #ipower |

Each department has:
- Brain directory: `brains/{department}/`
- Sandbox directory: `sandboxes/{department}/`
- Methodology file: `brains/{department}/METHODOLOGY.md`
- Git branch: `brain/{department}`

## 🤖 Discord Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!receipt [department]` | Generate board member receipt | `!receipt athena` |
| `!brain [department]` | Show current brain state | `!brain nova` |
| `!sync` | Force sync vault to Git | `!sync` |
| `!archive [query]` | Search vault for licenses/APIs | `!archive unity` |
| `!health` | Show mesh health status | `!health` |
| `!departments` | List all departments | `!departments` |

## 📦 Configuration

### Main Configuration (`obsidian-mesh-config.yaml`)

The configuration file contains:

```yaml
# Genesis constants
genesis:
  increment: 3449
  architect_snowflake: 1067614449693569044

# Archive vault structure
archive_vault:
  base_path: "/vault/legions-of-minds"
  structure:
    licenses: [...]
    apis: [...]
    mcp_tools: [...]
    code_libraries: [...]

# Department configurations
departments:
  - name: "Athena"
    quadrant: "Strategy & Intelligence"
    brain_path: "brains/athena"
    # ...

# Obsidian settings
obsidian:
  plugins:
    required: ["dataview", "obsidian-git", "canvas", "templater"]
  graph_view:
    color_groups: [...]

# Sync pipeline
sync_pipeline:
  triggers: [...]
  discord:
    notifications: {...}
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_TOKEN` | Discord bot token | Yes |
| `OBSIDIAN_VAULT_PATH` | Path to Obsidian vault | No (default: /vault/legions-of-minds) |
| `GITHUB_REPO` | Git remote URL | No |

## 📊 Obsidian Plugins

### Required Plugins

1. **Dataview** — Live queries for brain connections
2. **Obsidian Git** — Auto-commit and sync to GitHub
3. **Canvas** — Visual brain mapping
4. **Templater** — Dynamic templates for receipts
5. **QuickAdd** — Quick capture and macros

### Obsidian Git Settings

```
Auto-commit: ON
Commit message: "🟠 Brain sync | Increment 3449 | {{date}}"
Auto-pull on startup: ON
Backup interval: 10 minutes
```

### Graph View Colors

The graph view is configured with department color groups:
- `tag:#athena` → Red (#FF4500)
- `tag:#lyra` → Cyan (#00CED1)
- `tag:#nova` → Purple (#9400D3)
- `tag:#ipower` → Gold (#FFD700)
- `tag:#genesis` → White (#FFFFFF)
- `tag:#methodology` → Green (#00FF00)

## 📜 Board Receipt Template

Board receipts are Markdown documents with:

```markdown
---
type: board-receipt
department: "Athena"
generated: "2024-01-01T00:00:00Z"
genesis_increment: 3449
tags: ["#athena", "#board-receipt", "#genesis"]
---

# 📋 Board Member Receipt: Athena

## 🔒 Genesis Lock
- Increment: 3449
- Architect: 1067614449693569044

## 📜 Licenses Held
[Dataview query]

## 🔌 API Access
[Dataview query]

## 🛠️ MCP Tools Available
[Dataview query]

## 📝 Current Methodology
![[brains/athena/METHODOLOGY.md]]
```

## 🔄 Sync Pipeline

### Event Flow

```
File Change → Graph Update → Git Commit → Discord Notification
         ↓
Receipt Generation → Claude Verification → Discord Post
         ↓
Methodology Update → Diff Embed → Discord Notification
```

### Discord Notifications

The bot sends notifications for:
- New board receipts
- Methodology updates
- Sync completions
- Health status changes

## 🔐 Security

### Genesis Lock

All documents are locked with:
- **Increment:** 3449
- **Architect Snowflake:** 1067614449693569044

### Credentials

Sensitive credentials are stored in Vault:
- `vault://kv/discord/api_key`
- `vault://kv/github/pat`
- `vault://kv/openai/api_key`
- `vault://kv/anthropic/api_key`

## 🛠️ Troubleshooting

### Bot Not Responding

```bash
# Check if token is set
echo $DISCORD_TOKEN

# Check bot logs
python scripts/obsidian_bot.py 2>&1 | head -50

# Verify configuration
python -c "import yaml; yaml.safe_load(open('obsidian-mesh-config.yaml'))"
```

### Git Sync Issues

```bash
# Check vault git status
cd /vault/legions-of-minds
git status
git log --oneline -5

# Manual sync
git add .
git commit -m "🟠 Manual sync | Increment 3449"
git push
```

### Obsidian Plugin Issues

1. Open Obsidian Settings → Community Plugins
2. Ensure all required plugins are installed and enabled
3. Configure Obsidian Git with auto-commit settings

## 📚 Resources

- [Obsidian Documentation](https://help.obsidian.md/)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/)
- [Obsidian Git Plugin](https://github.com/denolehov/obsidian-git)

---

**Built with 🟠 by Strategickhaos DAO LLC**

*Genesis Lock: Increment 3449 | Architect: 1067614449693569044*

*"They're not working for you. They're dancing with you. And the music is never going to stop."*
