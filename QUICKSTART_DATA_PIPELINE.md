# Quick Start: Sovereignty Architecture Data Pipeline

**Transform your manual file workflow into an automated knowledge system in 5 minutes.**

## 🚀 One-Line Setup

```bash
./setup_data_pipeline.sh && python3 ingest_daemon.py
```

That's it! Now drop files in `ingest/` and watch them get automatically classified and routed.

---

## 📋 What This Does

This data pipeline automates the workflow:

```
Manual:     Download → SaveAs → SendTo → GiveToOwner → Organize
Automated:  Download → ingest/ folder → [MAGIC HAPPENS] → Organized in vault
```

The "magic" is:
1. **Watch** - Daemon monitors `ingest/` folder
2. **Classify** - Analyzes filename/content to determine topic
3. **Route** - Moves to appropriate lab (Cyber, Architecture, AI/ML, DevOps, Legal, Business)
4. **Index** - Creates Obsidian note with metadata and tags
5. **Track** - Git commits the change
6. **Notify** - (Optional) Discord notification
7. **Sync** - GitLens propagates to all desktops

---

## 🎬 Interactive Demo

Want to see it in action first?

```bash
./demo_data_pipeline.sh
```

This creates sample files, processes them, and shows you the results.

---

## 📖 Step-by-Step Setup

### Prerequisites

- Python 3.7+ (check with `python3 --version`)
- Git (optional but recommended)
- 2 minutes

### Step 1: Run Setup

```bash
./setup_data_pipeline.sh
```

This will:
- ✅ Check Python version
- ✅ Install PyYAML
- ✅ Create `ingest/` and `logs/` directories
- ✅ Optionally create vault structure
- ✅ Make scripts executable

### Step 2: Start the Daemon

```bash
# Run continuously (recommended)
python3 ingest_daemon.py

# Or run once for testing
python3 ingest_daemon.py --once
```

### Step 3: Add Files

Open another terminal and drop files:

```bash
# Method 1: Command line
cp ~/Downloads/paper.pdf ingest/

# Method 2: File manager
# Drag and drop files into the ingest/ folder

# Method 3: Configure "Send To"
# Set up right-click menu to send files to ingest/
```

### Step 4: Watch the Magic

The daemon will:
```
📥 Processing: paper.pdf
   Size: 2.4 MB
   Lab: Architecture (confidence: 0.87)
   Topics: systems, design, patterns
   ✅ Moved to: vault/labs/architecture/paper.pdf
   📝 Created note: paper_note.md
   🔖 Git commit: chore(ingest): Add paper.pdf to Architecture
   🎉 Processing complete!
```

---

## 🔧 Customization

### Add Your Own Labs

Edit `lab.yaml`:

```yaml
labs:
  - name: "My Research"
    path: "vault/labs/my-research"
    topics: ["research", "experiments"]
    ingest_keywords: ["experiment", "research", "study"]
```

### Change Check Interval

```bash
# Check every 10 seconds instead of 5
python3 ingest_daemon.py --interval 10
```

### Configure Vault Location

Edit `.env.pipeline`:

```bash
VAULT_PATH="$HOME/Documents/MyVault"
```

---

## 📊 Monitoring

### View Logs

```bash
# Follow logs in real-time
tail -f logs/ingest_events.jsonl | jq .

# See recent activity
cat logs/ingest_events.jsonl | tail -5 | jq .

# Statistics
cat logs/ingest_events.jsonl | jq -r '.data.lab' | sort | uniq -c
```

### Check Daemon Status

```bash
# Is it running?
ps aux | grep ingest_daemon

# How many files processed?
wc -l logs/ingest_events.jsonl

# Git activity
git log --oneline | head -10
```

---

## 🎯 Common Use Cases

### Research Papers

```bash
# Download papers to ingest/
wget -P ingest/ https://arxiv.org/pdf/2023.12345.pdf

# Daemon classifies and files it
# Creates note with summary placeholder
```

### Screenshots & Images

```bash
# Screenshot saved to ingest/
# Daemon moves to appropriate lab
# Creates note linking to image
```

### Code Snippets

```bash
# Save code to ingest/cool_algorithm.py
# Daemon routes based on filename
# Note includes code language tags
```

### Meeting Notes

```bash
# Export meeting notes to ingest/
# Daemon files under appropriate project
# Tags with date and attendees
```

---

## 🔗 Integration with Tools

### Obsidian

1. Open vault folder in Obsidian
2. Enable graph view
3. See automatic organization
4. Notes have frontmatter and tags

### GitLens (VS Code)

1. Open vault in VS Code
2. Enable GitLens
3. See file history
4. Track changes across desktops

### Discord (Optional)

1. Set `DISCORD_TOKEN` in `.env.pipeline`
2. Configure webhook URL
3. Get notifications on file ingestion

### Claude / AI Agents (Future)

1. AI reads notes via MCP tools
2. AI can classify ambiguous files
3. AI suggests connections between notes

---

## 🆘 Troubleshooting

### Daemon Won't Start

```bash
# Check Python
python3 --version  # Should be 3.7+

# Install dependencies
pip3 install pyyaml

# Check permissions
chmod +x ingest_daemon.py
```

### Files Not Processing

```bash
# Ensure daemon is running
ps aux | grep ingest_daemon

# Check ingest folder exists
ls -la ingest/

# Run in test mode
python3 ingest_daemon.py --once
```

### Wrong Classification

```bash
# Add more keywords to lab.yaml
# Or manually move file:
mv vault/labs/wrong/file.pdf vault/labs/correct/
```

---

## 📚 Learn More

### Documentation

- **[ARCHITECTURE_DATA_PIPELINE.md](ARCHITECTURE_DATA_PIPELINE.md)** - Complete system architecture
- **[GITLENS_100_WAYS.md](GITLENS_100_WAYS.md)** - GitLens integration guide
- **[lab.yaml](lab.yaml)** - Lab configurations
- **[tools.yaml](tools.yaml)** - MCP tool definitions

### Architecture Diagram

```
Files → ingest/ → Daemon → Vault → Git → Discord → AI Agents
  ↓        ↓        ↓        ↓       ↓      ↓         ↓
Browser  Watch  Classify  Store  Track  Notify  Transform
```

### Key Concepts

- **Lab**: A knowledge domain (e.g., Architecture, AI/ML)
- **Ingest**: Entry point for all files
- **Classification**: Automatic topic detection
- **Vault**: Obsidian knowledge base
- **MCP Tools**: API for AI agents

---

## 🎉 Success!

You now have an automated knowledge pipeline that:

- ✅ Removes manual file organization
- ✅ Creates searchable knowledge base
- ✅ Tracks all changes in git
- ✅ Syncs across all desktops
- ✅ Enables AI agent access
- ✅ Provides complete audit trail

**Next steps:**

1. Start adding your real files
2. Review and adjust lab configurations
3. Set up GitLens for visualization
4. Configure Discord notifications
5. Explore MCP tool integration

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"The best system is the one you actually use. We made it automatic."*
