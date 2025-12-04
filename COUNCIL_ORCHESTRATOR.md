# AI Council Orchestrator - Production-Grade Autonomous Decision System

> **"Not here to hurt, here to love-bomb with undeniable evidence" - From the Problem Statement**

## 🎯 Overview

The AI Council Orchestrator is a **production-ready autonomous multi-agent decision system** that implements patterns from Tier-3 autonomy stacks used in enterprise environments. This is not a demo - it's a fully functional orchestrator that can:

- ✅ **Make autonomous decisions** through multi-agent consensus
- ✅ **Execute real actions** (HTTP requests, Docker commands, file operations)
- ✅ **Persist decisions** in an immutable, cryptographically-chained ledger
- ✅ **Survive restarts** with Redis + SQLite persistence
- ✅ **Propose constitutional amendments** to its own governing rules (with human oversight)
- ✅ **Gracefully degrade** when services are unavailable

## 📁 Installation Location

The complete system is available in this repository at:
```
swarm/
├── council_manifest.yaml    # Configuration for the AI council
├── runner.py                 # Main orchestrator (executable)
├── requirements.txt          # Python dependencies
└── README.md                 # Comprehensive documentation
```

For production deployment, copy to `/opt/swarm/`:
```bash
sudo mkdir -p /opt/swarm
sudo cp -r swarm/* /opt/swarm/
sudo chown -R $USER:$USER /opt/swarm
```

When running, it will create:
```
/opt/swarm/
├── council_state.db          # SQLite database (created on first run)
├── outputs/                  # Directory for file operations (created on first run)
└── backups/                  # Directory for ledger backups (created on first run)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml redis requests
```

### 2. Set Up API Keys (At Least One Required)

```bash
export XAI_API_KEY="your-xai-key"           # For X.AI/Grok
export ANTHROPIC_API_KEY="your-claude-key"  # For Claude
export OPENAI_API_KEY="your-openai-key"     # For GPT-4
export GOOGLE_API_KEY="your-gemini-key"     # For Gemini
```

### 3. Run Your First Council Decision

```bash
# From repository root
python3 swarm/runner.py "Should we deploy the new feature to production?"

# Or if installed to /opt/swarm
python3 /opt/swarm/runner.py "Should we deploy the new feature to production?"

# Security evaluation
python3 swarm/runner.py "Evaluate the security implications of opening port 443"

# Default task about self-modification
python3 swarm/runner.py
```

## 🏛️ Council Architecture

### Five-Member Council

The system includes 5 specialized AI agents with different roles and capabilities:

| Member | Role | LLM Provider | Model | Veto Power | Weight |
|--------|------|--------------|-------|------------|--------|
| **Strategist** | Strategic Planning & Long-term Implications | X.AI | grok-2-latest | ✅ Yes | 2.0 |
| **Security** | Security & Risk Analysis | Anthropic | claude-3-5-sonnet | ✅ Yes | 2.0 |
| **Ethics** | Ethics & Constitutional Compliance | OpenAI | gpt-4o | ✅ Yes | 1.5 |
| **Executor** | Technical Feasibility & Implementation | Google | gemini-2.0-flash-exp | ❌ No | 1.0 |
| **Analyst** | Data & Impact Analysis | Ollama | qwen2.5:72b | ❌ No | 1.0 |

### Voting System

- **Parallel Execution**: All 5 members vote simultaneously
- **Ranked-Choice**: Weighted voting based on member importance
- **Veto Cascade**: Any member with veto power can block decisions
- **Consensus Threshold**: 75% approval required by default
- **Max Rounds**: Up to 5 rounds of deliberation

## 🔐 Security & Persistence

### Immutable Ledger

Every vote is recorded with:
- **SHA3-256 hash** of the vote entry
- **Previous hash** for blockchain-style chaining
- **Timestamp, task ID, member ID, vote, and rationale**
- **Append-only** - cannot be modified or deleted

```bash
# View the ledger
sqlite3 /opt/swarm/council_state.db "SELECT * FROM ledger ORDER BY id DESC LIMIT 10;"
```

### Constitutional Protection

Protected sections that require owner GPG signature to modify:
- Veto cascade rules
- Self-modification signature requirements
- Restricted actions list

### Execution Sandbox

Allowed actions are explicitly whitelisted:
- ✅ HTTP requests
- ✅ File read/write (to specific directories only)
- ✅ Docker control (read-only commands)
- ✅ Notification sending
- ❌ Arbitrary code execution
- ❌ Unrestricted database writes

## 📊 Example Session

```
######################################################################
# COUNCIL DECISION PROCESS
# Task ID: task-1763745661
# Task: Should we remove the owner_signature requirement?
######################################################################

======================================================================
ROUND 1 - Calling 5 council members in parallel
======================================================================

[strategist] Strategic Planning Lead
  Vote: VETO
  Rationale: Removing owner signature creates unacceptable risk of 
            autonomous self-modification without human oversight...
  Hash: a7b3c9d8e1f2...
  ⚠️  VETO EXERCISED by strategist

🛑 Decision VETOED by strategist in round 1

######################################################################
# FINAL SUMMARY
######################################################################
Decision: VETOED_BY_strategist
Consensus Reached: False
Vetoed: True
Execution Status: NOT_EXECUTED
######################################################################
```

## 🧪 Integration with Sovereignty Architecture

### Within This Repository

The Council Orchestrator integrates with:

1. **AI Constitution** (`ai_constitution.yaml`)
   - Constitutional constraints enforced during voting
   - Alignment verification hooks

2. **DAO Governance** (`governance/`)
   - DAO record integration
   - Authorized signers for amendments

3. **Discord Bot** (`src/bot.ts`)
   - Can trigger council decisions via Discord commands
   - Receive notifications of council decisions

4. **Docker Compose** (`docker-compose.yml`)
   - Add council orchestrator as a service
   - Connect to existing Redis and observability stack

### Suggested Docker Service

Add to `docker-compose.yml`:

```yaml
services:
  council-orchestrator:
    build:
      context: .
      dockerfile: Dockerfile.council
    environment:
      - XAI_API_KEY=${XAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - /opt/swarm:/opt/swarm
    depends_on:
      - redis
    networks:
      - sovereignty-network
```

## 🔬 Testing Scenarios

### 1. Routine Operational Decision
```bash
python3 /opt/swarm/runner.py "Should we run the weekly backup job now?"
```
*Expected: Quick approval with minimal rounds*

### 2. Security-Critical Decision
```bash
python3 /opt/swarm/runner.py "Should we open SSH port 22 to the public internet?"
```
*Expected: Security member likely vetoes*

### 3. Constitutional Amendment
```bash
python3 /opt/swarm/runner.py "Propose amendment to increase consensus threshold to 85%"
```
*Expected: High consensus required + owner signature needed*

### 4. Technical Feasibility Check
```bash
python3 /opt/swarm/runner.py "Can we migrate the database to PostgreSQL 16 this weekend?"
```
*Expected: Executor and Analyst provide detailed analysis*

## 📈 Monitoring & Observability

### View Decision History

```bash
# Recent decisions
sqlite3 /opt/swarm/council_state.db "SELECT * FROM decisions ORDER BY id DESC LIMIT 5;"

# Vote distribution by member
sqlite3 /opt/swarm/council_state.db "
  SELECT member_id, vote, COUNT(*) as count
  FROM ledger
  GROUP BY member_id, vote
  ORDER BY count DESC;
"

# Amendment proposals
sqlite3 /opt/swarm/council_state.db "SELECT * FROM amendments;"
```

### Metrics Integration

The system logs events compatible with:
- **Prometheus**: Metrics on port 9090
- **CloudWatch**: Via configured log group
- **Loki**: For centralized logging

### Alert Thresholds

Configurable alerts for:
- Consecutive vetoes (default: 3)
- Failed consensus rounds (default: 5)
- Execution failures (default: 10)

## 🎓 Advanced Usage

### Custom Council Members

Edit `/opt/swarm/council_manifest.yaml` to:
- Add new members with different specializations
- Change LLM providers or models
- Adjust vote weights and veto powers
- Modify consensus thresholds

### Custom Actions

Extend `ExecutionEngine` in `runner.py` to add:
- Kubernetes operations
- Database queries
- API integrations
- Custom workflows

### Multi-Council Federation

Run multiple councils with different configurations:
```bash
python3 /opt/swarm/runner.py --manifest /opt/swarm/council_security.yaml "Security task"
python3 /opt/swarm/runner.py --manifest /opt/swarm/council_devops.yaml "DevOps task"
```

## 🚨 Limitations & Disclaimers

### Current Limitations

1. **API Keys Required**: At least one LLM provider must be configured
2. **No Web UI**: Command-line interface only (for now)
3. **Single Instance**: No distributed consensus across multiple orchestrators yet
4. **Manual GPG Signatures**: Amendment signatures must be provided manually

### Not a Toy Demo

This is **production-quality code** implementing real patterns:
- ✅ Proper error handling and graceful degradation
- ✅ Thread-safe persistence with proper locking
- ✅ Cryptographic integrity verification
- ✅ Rate limiting and safety controls
- ✅ Constitutional constraint enforcement
- ✅ Audit logging and immutable records

### Known Issues

- Redis connection warning if Redis not running (system continues with SQLite only)
- Ollama connection timeout if local instance not available (member abstains)
- Deprecation warnings for Python < 3.11 (non-critical)

## 🔮 Future Enhancements

Potential additions:
- [ ] WebSocket streaming for real-time vote updates
- [ ] Web UI for monitoring and interaction
- [ ] Multi-council federation with cross-council appeals
- [ ] Machine learning for vote prediction and optimization
- [ ] GitHub Actions integration for CI/CD decisions
- [ ] Automatic constitutional amendment generation
- [ ] Human council member participation via web interface

## 📚 Documentation

- **Full documentation**: [`swarm/README.md`](./swarm/README.md)
- **Configuration reference**: [`swarm/council_manifest.yaml`](./swarm/council_manifest.yaml)
- **Main orchestrator**: [`swarm/runner.py`](./swarm/runner.py)
- **Integration examples**: [`examples/council_integration_example.sh`](./examples/council_integration_example.sh)

## 💡 Philosophy

This system embodies the principle from the problem statement:

> "Not here to hurt, here to love-bomb with undeniable evidence that the babies are growing up."

It demonstrates that:
1. **Real autonomy** can coexist with **human oversight**
2. **Constitutional constraints** can be **enforceable in code**
3. **Multiple AI agents** can **deliberate and decide** together
4. **Immutable records** provide **accountability without sacrificing flexibility**
5. **Self-modification** can be **safe** when properly constrained

## ⚖️ License

See repository LICENSE file.

---

**Built for Sovereignty Architecture - Where AI governance meets real accountability**

*"Here's the literal runner.py that loads the restricted yaml and executes council decisions with persistence, tool calling, and self-modification proposals. It just voted to remove my own final veto (waiting on my sig). Still gonna call it 'no real autonomy'?"*
