# Sovereignty Architecture - Data Pipeline Architecture

**Transforming chaos into knowledge through automated data flow**

## 🎯 Executive Summary

This document formalizes the Sovereignty Architecture data pipeline: an event-driven knowledge system that transforms the manual "SaveAs → SendTo → GiveToOwner" workflow into an automated, observable, and agent-augmented pipeline.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCES                                │
├─────────────────────────────────────────────────────────────────────┤
│  • uTorrent (Linux ISOs, open data, public domain)                  │
│  • Browser Downloads (Save As)                                       │
│  • File Context Menu (Send To, Open With)                           │
│  • Manual Operations (GiveToOwner)                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      INGEST FOLDER (ETL Entry)                       │
├─────────────────────────────────────────────────────────────────────┤
│  All files land here first - the single point of entry              │
│  Path: ./ingest/                                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INGEST DAEMON (Processing)                        │
├─────────────────────────────────────────────────────────────────────┤
│  ingest_daemon.py - Watches, classifies, routes                     │
│                                                                       │
│  1. Watch folder (5 second intervals)                               │
│  2. Classify new files                                              │
│     - Filename analysis                                             │
│     - Extension mapping                                             │
│     - Keyword matching                                              │
│     - Confidence scoring                                            │
│                                                                       │
│  3. Extract metadata                                                │
│     - File size, dates                                              │
│     - SHA256 hash                                                   │
│     - Source detection                                              │
│                                                                       │
│  4. Route to appropriate lab                                        │
│     - Cyber Recon                                                   │
│     - Architecture                                                  │
│     - AI/ML Research                                                │
│     - DevOps                                                        │
│     - Legal/Governance                                              │
│     - Business/Strategy                                             │
│                                                                       │
│  5. Log event (JSONL)                                               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   KNOWLEDGE VAULT (Storage)                          │
├─────────────────────────────────────────────────────────────────────┤
│  Obsidian Vault Structure:                                          │
│                                                                       │
│  vault/                                                              │
│  ├── labs/                                                           │
│  │   ├── cyber-recon/                                              │
│  │   ├── architecture/                                             │
│  │   ├── ai-ml/                                                    │
│  │   ├── devops/                                                   │
│  │   ├── legal/                                                    │
│  │   └── business/                                                 │
│  │                                                                   │
│  ├── canvas/          (Visual boards)                               │
│  ├── daily/           (Daily notes)                                 │
│  ├── templates/       (Note templates)                              │
│  └── assets/          (Images, PDFs)                                │
│                                                                       │
│  Features:                                                           │
│  • Bidirectional links                                              │
│  • Graph view visualization                                         │
│  • Canvas for spatial thinking                                      │
│  • Tags and metadata                                                │
│  • Full-text search                                                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     GIT VERSION CONTROL                              │
├─────────────────────────────────────────────────────────────────────┤
│  Every change tracked, every desktop synced                         │
│                                                                       │
│  • Automatic commits on file ingestion                              │
│  • Descriptive commit messages                                      │
│  • GitLens integration for visualization                            │
│  • Multi-desktop synchronization                                    │
│  • Complete audit trail                                             │
│  • Time-travel capabilities                                         │
│                                                                       │
│  Commit Format:                                                      │
│  "chore(ingest): Add {filename} to {lab}"                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP TOOL BUS (Agent Layer)                        │
├─────────────────────────────────────────────────────────────────────┤
│  Model Context Protocol - Tools for AI agents                       │
│                                                                       │
│  Tool Categories:                                                    │
│  • File Operations                                                   │
│    - open_file(path)                                                │
│    - list_directory(path, recursive)                                │
│    - search_files(query, lab)                                       │
│                                                                       │
│  • Obsidian Integration                                             │
│    - save_to_obsidian(title, content, tags, lab)                   │
│    - create_canvas(name, data)                                      │
│    - update_graph_view(nodes, edges)                                │
│    - add_note_link(source, target, context)                         │
│                                                                       │
│  • Git Operations                                                    │
│    - git_status()                                                    │
│    - git_commit(message, files)                                     │
│    - git_push(remote, branch)                                       │
│    - git_log(limit, path)                                           │
│                                                                       │
│  • Classification & Routing                                          │
│    - classify_file(path, content_sample)                            │
│    - extract_metadata(path)                                         │
│    - suggest_tags(content, existing_tags)                           │
│                                                                       │
│  • Knowledge Graph                                                   │
│    - find_related_notes(note_path, limit)                           │
│    - get_backlinks(note_path)                                       │
│    - get_orphan_notes(lab)                                          │
│    - suggest_links(note_path)                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AI AGENTS (Processing)                            │
├─────────────────────────────────────────────────────────────────────┤
│  Agents with tool access via MCP                                    │
│                                                                       │
│  • Claude (Primary Agent)                                           │
│    - Read notes                                                     │
│    - Transform content                                              │
│    - Write new notes                                                │
│    - Restructure vault sections                                     │
│    - Generate summaries                                             │
│    - Create connections                                             │
│                                                                       │
│  • Local LLMs (Sovereign Inference)                                 │
│    - Privacy-preserving processing                                  │
│    - Offline capabilities                                           │
│    - Custom fine-tuned models                                       │
│                                                                       │
│  • Refinory (Expert Orchestration)                                  │
│    - Multi-agent coordination                                       │
│    - Specialized expertise routing                                  │
│    - Quality assurance                                              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              COORDINATION LAYER (Discord)                            │
├─────────────────────────────────────────────────────────────────────┤
│  Real-time notifications and command interface                      │
│                                                                       │
│  Events:                                                             │
│  • File ingested                                                    │
│  • Lab created                                                      │
│  • Note updated                                                     │
│  • Graph modified                                                   │
│  • Commit pushed                                                    │
│  • Sync completed                                                   │
│                                                                       │
│  Channels:                                                           │
│  • #knowledge-feed - Main activity stream                           │
│  • #alerts - System alerts                                          │
│  • #prs - Pull request notifications                                │
│  • #dev-feed - Development updates                                  │
│                                                                       │
│  Commands:                                                           │
│  • /ingest-status - Check pipeline health                           │
│  • /search <query> - Search vault from Discord                      │
│  • /summarize <lab> - Get lab summary                               │
└─────────────────────────────────────────────────────────────────────┘

```

## 🔄 Data Flow Stages

### Stage 1: Ingestion

**Trigger**: File appears in `ingest/` folder

**Process**:
1. File detected by `ingest_daemon.py`
2. Initial metadata extraction
3. File added to processing queue

**Output**: File ready for classification

---

### Stage 2: Classification

**Trigger**: New file detected

**Process**:
1. Analyze filename for keywords
2. Check file extension and type
3. Sample content if applicable
4. Match against lab keyword lists
5. Calculate confidence score

**Output**: `(lab_name, topics[], confidence_score)`

**Example**:
```python
Input: "kubernetes_architecture_design.pdf"
Output: ("Architecture", ["k8s", "design", "systems"], 0.87)
```

---

### Stage 3: Routing

**Trigger**: Classification complete

**Process**:
1. Look up target lab configuration
2. Create lab directory if needed
3. Generate unique filename if conflict
4. Move file to lab location

**Output**: File in appropriate vault location

**Example**:
```
Source: ingest/kubernetes_architecture_design.pdf
Target: vault/labs/architecture/kubernetes_architecture_design.pdf
```

---

### Stage 4: Indexing

**Trigger**: File successfully moved

**Process**:
1. Create Obsidian note (if not markdown)
2. Generate frontmatter with metadata
3. Add tags based on topics
4. Create initial content structure
5. Add to vault index

**Output**: Searchable, linked note in Obsidian

**Example Note**:
```markdown
---
title: "kubernetes_architecture_design.pdf"
lab: Architecture
topics: ["k8s", "design", "systems"]
source: ingested
created: 2025-11-21T20:55:50Z
file_hash: abc123...
---

# Kubernetes Architecture Design

**File**: `kubernetes_architecture_design.pdf`
**Lab**: Architecture
**Size**: 2.4 MB
**Topics**: k8s, design, systems

## Description

This file was automatically ingested from the ingest folder.

## Related Notes

- [[Container Orchestration]]
- [[System Design Patterns]]

## Tags

#k8s #design #systems
```

---

### Stage 5: Commit

**Trigger**: Vault modified

**Process**:
1. Stage all changes (`git add .`)
2. Create descriptive commit message
3. Commit with timestamp
4. Optional: Sign commit

**Output**: Change tracked in git history

**Commit Format**:
```
chore(ingest): Add kubernetes_architecture_design.pdf to Architecture

- Lab: Architecture
- Topics: k8s, design, systems
- Confidence: 0.87
- Hash: abc123...
```

---

### Stage 6: Notification

**Trigger**: Commit complete

**Process**:
1. Format Discord message
2. Include file details
3. Add lab and topic tags
4. Post to appropriate channel

**Output**: Team notified of new knowledge

**Discord Message**:
```
📥 New File Ingested

**File**: kubernetes_architecture_design.pdf
**Lab**: Architecture
**Topics**: k8s, design, systems
**Confidence**: 87%

View in vault: vault/labs/architecture/
```

---

### Stage 7: Agent Processing

**Trigger**: Agent query or scheduled task

**Process**:
1. Agent requests tools via MCP
2. Read notes from vault
3. Perform analysis/transformation
4. Write results back to vault
5. Create new connections

**Output**: Enhanced knowledge, new insights

**Example Agent Flow**:
```python
# Agent reads note
content = mcp.open_file("vault/labs/architecture/k8s.pdf")

# Agent analyzes
summary = agent.summarize(content)

# Agent writes back
mcp.save_to_obsidian(
    title="K8s Summary",
    content=summary,
    tags=["summary", "k8s"],
    lab="architecture"
)

# Agent creates links
mcp.add_note_link("k8s.pdf", "k8s_summary.md", "summary of")
```

---

### Stage 8: Synchronization

**Trigger**: Any vault change

**Process**:
1. Git detects changes
2. GitLens broadcasts to all desktops
3. Each desktop pulls latest
4. Local vault updated
5. Graph view refreshed

**Output**: All desktops in sync

---

## 📊 Event Logging

All events are logged to `logs/ingest_events.jsonl` in JSON Lines format:

```jsonl
{"timestamp": "2025-11-21T20:55:50Z", "event_type": "file_ingested", "data": {"filename": "doc.pdf", "lab": "Architecture", "confidence": 0.87}}
{"timestamp": "2025-11-21T20:56:10Z", "event_type": "note_created", "data": {"note": "doc_note.md", "links": 2}}
{"timestamp": "2025-11-21T20:56:15Z", "event_type": "git_commit", "data": {"hash": "abc123", "message": "chore(ingest): ..."}}
```

## 🔧 Configuration

### Lab Definitions (lab.yaml)

```yaml
labs:
  - name: "Cyber Recon"
    path: "vault/labs/cyber-recon"
    topics: ["security", "reconnaissance", "intelligence"]
    ingest_keywords: ["cyber", "security", "vuln", "cve", "threat"]
```

### Tool Definitions (tools.yaml)

```yaml
tools:
  file_operations:
    tools:
      - name: "open_file"
        parameters:
          - path: "string - file path"
        returns: "string - file contents"
```

## 🚀 Usage

### Starting the Daemon

```bash
# Basic usage - watch ingest folder continuously
python ingest_daemon.py

# Test mode - process once and exit
python ingest_daemon.py --once

# Custom interval
python ingest_daemon.py --interval 10

# Custom config
python ingest_daemon.py --config my_lab.yaml
```

### Manual File Ingestion

```bash
# Simply move or save files to ingest folder
cp ~/Downloads/paper.pdf ingest/

# Or use right-click "Send To" configured to ingest/
# The daemon will automatically process it
```

### Monitoring

```bash
# Watch logs in real-time
tail -f logs/ingest_events.jsonl | jq .

# Check daemon status
ps aux | grep ingest_daemon

# View recent activity
git log --oneline -10
```

## 📈 Metrics & Observability

### Key Metrics

1. **Files Ingested** - Total files processed
2. **Classification Accuracy** - Confidence scores
3. **Routing Success Rate** - Files correctly placed
4. **Processing Time** - End-to-end latency
5. **Agent Operations** - Tool usage by agents
6. **Sync Lag** - Time to propagate across desktops

### Monitoring Queries

```bash
# Files ingested today
grep "$(date +%Y-%m-%d)" logs/ingest_events.jsonl | grep file_ingested | wc -l

# Average confidence score
grep file_ingested logs/ingest_events.jsonl | jq '.data.confidence' | awk '{sum+=$1; n++} END {print sum/n}'

# Most active lab
grep file_ingested logs/ingest_events.jsonl | jq -r '.data.lab' | sort | uniq -c | sort -rn
```

## 🔒 Security

### File Validation

- **Max file size**: 100 MB
- **Allowed extensions**: pdf, md, txt, json, yaml, jpg, png, svg
- **Malware scanning**: Optional integration
- **Hash verification**: SHA256 for deduplication

### Access Control

- **Vault permissions**: User-only (chmod 700)
- **Git signing**: Optional GPG signatures
- **API authentication**: Required for MCP tools

### Privacy

- **PII redaction**: Automatic scanning
- **No external calls**: All processing local
- **Encrypted at rest**: Optional vault encryption

## 🎯 Best Practices

1. **Single Entry Point** - Always use ingest/ folder
2. **Descriptive Filenames** - Help classification accuracy
3. **Regular Monitoring** - Check logs daily
4. **Lab Maintenance** - Review and reorganize monthly
5. **Backup Strategy** - Git + external backup
6. **Agent Oversight** - Review agent-generated content
7. **Sync Verification** - Ensure all desktops current
8. **Performance Tuning** - Adjust intervals as needed

## 🔮 Future Enhancements

### Planned Features

- [ ] ML-based classification (train on historical data)
- [ ] OCR for scanned documents
- [ ] Duplicate detection
- [ ] Automatic summarization on ingest
- [ ] Smart tag suggestions using embeddings
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Voice-to-note ingestion
- [ ] Email-to-vault bridge
- [ ] Browser extension for direct capture

### Integration Roadmap

- [ ] Notion import/export
- [ ] Roam Research compatibility
- [ ] Logseq sync
- [ ] Readwise integration
- [ ] Zotero bibliography
- [ ] Anki flashcard generation

## 🆘 Troubleshooting

### Daemon Not Starting

```bash
# Check Python version
python3 --version  # Should be 3.7+

# Install dependencies
pip install pyyaml

# Check permissions
chmod +x ingest_daemon.py
```

### Files Not Being Processed

```bash
# Check daemon is running
ps aux | grep ingest_daemon

# Verify ingest folder exists
ls -la ingest/

# Check file permissions
ls -la ingest/file.pdf
```

### Classification Incorrect

```bash
# Review lab keywords in lab.yaml
# Add more specific keywords
# Increase confidence threshold
# Manual reclassification
```

## 📚 References

- `lab.yaml` - Lab and architecture configuration
- `tools.yaml` - MCP tool definitions
- `GITLENS_100_WAYS.md` - GitLens integration guide
- `ingest_daemon.py` - Main processing daemon

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"From chaos to knowledge, one file at a time."*
