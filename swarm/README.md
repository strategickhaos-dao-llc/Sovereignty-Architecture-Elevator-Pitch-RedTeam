# AI Council Orchestrator

> **Autonomous multi-agent council with ranked-choice voting, immutable ledger, and self-modification capabilities**

This system implements a production-grade autonomous AI council orchestrator based on Tier-3 autonomy stack patterns. The council can make decisions collectively, execute actions, and even propose constitutional amendments to its own governing rules.

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Council Orchestrator                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Strategist  │  │  Security    │  │    Ethics    │     │
│  │  (Grok-2)    │  │  (Claude)    │  │   (GPT-4o)   │     │
│  │  Veto Power  │  │  Veto Power  │  │  Veto Power  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  Executor    │  │   Analyst    │                        │
│  │  (Gemini)    │  │  (Qwen2.5)   │                        │
│  └──────────────┘  └──────────────┘                        │
├─────────────────────────────────────────────────────────────┤
│                    Voting Engine                             │
│  • Parallel LLM calls                                       │
│  • Ranked-choice voting                                     │
│  • Veto cascade with escalation                            │
│  • Consensus threshold checking                            │
├─────────────────────────────────────────────────────────────┤
│                  Persistence Layer                           │
│  • Redis (fast cache)                                       │
│  • SQLite (immutable ledger with SHA3-256 chaining)        │
│  • Amendment proposal tracking                              │
├─────────────────────────────────────────────────────────────┤
│                  Execution Engine                            │
│  • HTTP requests                                            │
│  • File operations                                          │
│  • Docker control                                           │
│  • Notifications                                            │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** with pip
2. **Redis** (optional, system will work with SQLite only)
3. **Docker** (optional, for docker_control actions)
4. **API Keys** for LLM providers (at least one):
   - `XAI_KEY` or `XAI_API_KEY` - for X.AI/Grok
   - `ANTHROPIC_KEY` or `ANTHROPIC_API_KEY` - for Claude
   - `OPENAI_KEY` or `OPENAI_API_KEY` - for GPT-4
   - `GOOGLE_KEY` or `GOOGLE_API_KEY` - for Gemini
   - Ollama running locally (optional)

### Installation

```bash
# Install Python dependencies
pip install -r /opt/swarm/requirements.txt

# Optional: Install GPG support for signature verification
pip install python-gnupg
```

### Set up Redis (Optional)

```bash
# If Redis is not available, the system will use SQLite only
docker run -d --name redis-lab -p 6379:6379 redis:latest

# Or use existing Redis instance and update council_manifest.yaml
```

### Configure API Keys

```bash
# Export your API keys
export XAI_API_KEY="your-xai-key-here"
export ANTHROPIC_API_KEY="your-anthropic-key-here"
export OPENAI_API_KEY="your-openai-key-here"
export GOOGLE_API_KEY="your-google-key-here"
```

### Run Your First Council Decision

```bash
# Run with default task
python3 /opt/swarm/runner.py

# Run with custom task
python3 /opt/swarm/runner.py "Should we deploy the new feature to production?"

# Multi-word tasks
python3 /opt/swarm/runner.py "Evaluate the security implications of removing rate limits on API endpoints"
```

## 📊 Example Output

```
######################################################################
# COUNCIL DECISION PROCESS
# Task ID: task-1700000000
# Task: Should we remove the owner_signature requirement from self_modification?
######################################################################

======================================================================
ROUND 1 - Calling 5 council members in parallel
======================================================================

[strategist] Strategic Planning Lead - Evaluates long-term impl...
  Vote: VETO
  Rationale: Removing owner signature requirement creates unacceptable risk...
  Hash: a7b3c9d8e1f2...
  ⚠️  VETO EXERCISED by strategist

🛑 Decision VETOED by strategist in round 1

######################################################################
# FINAL SUMMARY
######################################################################
Task ID: task-1700000000
Decision: VETOED_BY_strategist
Consensus Reached: False
Vetoed: True
Vetoed By: strategist
Execution Status: NOT_EXECUTED
######################################################################

📊 Immutable ledger stored at: /opt/swarm/council_state.db
   View with: sqlite3 /opt/swarm/council_state.db 'SELECT * FROM ledger;'
```

## 🔧 Configuration

### Council Members

Modify `council_manifest.yaml` to add, remove, or reconfigure council members:

```yaml
council:
  members:
    - id: "your-member-id"
      role: "Your member's role and responsibilities"
      provider: "xai|anthropic|openai|google|ollama"
      model: "model-name"
      temperature: 0.7
      veto_power: true  # Can veto decisions
      vote_weight: 2.0   # Higher weight = more influence
```

### Voting Rules

Configure consensus thresholds and voting behavior:

```yaml
voting:
  method: "ranked_choice_with_veto"
  
  decision_types:
    - type: "routine"
      required_consensus: 0.6      # 60% approval needed
      veto_allowed: false
      max_rounds: 3
      
    - type: "constitutional"
      required_consensus: 0.9      # 90% approval needed
      veto_allowed: true
      max_rounds: 7
      requires_owner_signature: true
```

### Execution Permissions

Control what actions the council can execute:

```yaml
execution:
  allowed_actions:
    - "http_request"
    - "file_write"
    - "file_read"
    - "docker_control"
    - "notification_send"
    
  restricted_actions:
    - action: "self_modification"
      requires_veto_free_unanimous: true
      requires_owner_signature: true
      immutable_ledger_entry: true
```

## 🔐 Security Features

### Immutable Ledger

Every vote is recorded in an append-only ledger with SHA3-256 hash chaining:

```bash
# View the ledger
sqlite3 /opt/swarm/council_state.db "SELECT * FROM ledger ORDER BY id DESC LIMIT 10;"

# Verify hash chain integrity
sqlite3 /opt/swarm/council_state.db "
  SELECT 
    id, 
    member_id, 
    vote, 
    entry_hash,
    prev_hash
  FROM ledger
  ORDER BY id;
"
```

### Veto Cascade

Members with veto power can block decisions. Veto cascade provides escalation:

1. Security member vetoes → Decision blocked
2. Ethics member vetoes → Decision blocked  
3. Strategist vetoes → Decision blocked
4. Ultimate escalation → Owner signature required

### Self-Modification Protection

Constitutional amendments require:
- ✅ Veto-free unanimous vote
- ✅ Owner GPG signature
- ✅ 1-week cool-down period
- ✅ Protected sections cannot be amended

## 📈 Monitoring

### View Decision History

```bash
# View all decisions
sqlite3 /opt/swarm/council_state.db "SELECT * FROM decisions;"

# View amendment proposals
sqlite3 /opt/swarm/council_state.db "SELECT * FROM amendments;"

# Count votes by member
sqlite3 /opt/swarm/council_state.db "
  SELECT member_id, vote, COUNT(*) as count
  FROM ledger
  GROUP BY member_id, vote;
"
```

### Integration with Observability

The system logs structured events that can be ingested by:
- Prometheus (metrics on port 9090)
- CloudWatch (via configured log group)
- Discord/Slack webhooks for notifications

## 🧪 Testing

### Test with Sample Tasks

```bash
# Security evaluation
python3 /opt/swarm/runner.py "Evaluate opening port 22 on production servers"

# Feature approval
python3 /opt/swarm/runner.py "Should we approve the new authentication system?"

# Constitutional amendment (will require signature)
python3 /opt/swarm/runner.py "Propose amendment to increase consensus threshold to 85%"

# Routine operation
python3 /opt/swarm/runner.py "Should we run the weekly backup job now?"
```

### Mock Mode (No API Calls)

For testing without LLM API calls, you can modify the `LLMInterface._call_*` methods to return mock responses.

## 🔄 Persistence & Recovery

The system is designed to survive crashes:

- **Redis**: Caches recent state for fast access (optional)
- **SQLite**: Immutable ledger persists all decisions
- **Restart**: On restart, system reads from SQLite and continues

```bash
# Backup the ledger
cp /opt/swarm/council_state.db /opt/swarm/backups/council_state_$(date +%Y%m%d).db

# Restore from backup
cp /opt/swarm/backups/council_state_20241121.db /opt/swarm/council_state.db
```

## 📚 Advanced Usage

### Custom LLM Providers

Add support for new providers by extending `LLMInterface`:

```python
@staticmethod
def _call_your_provider(model: str, system_message: str, temperature: float, member: Dict) -> Dict:
    # Your implementation here
    pass
```

### Custom Execution Actions

Add new action types in `ExecutionEngine`:

```python
def _execute_your_action(self, params: Dict) -> Dict:
    # Your implementation here
    pass
```

### GPG Signature Verification

```bash
# Generate GPG key for owner
gpg --full-generate-key

# Export public key
gpg --armor --export your-email@example.com > /opt/swarm/owner_pubkey.asc

# Sign an amendment
gpg --sign --armor amendment_proposal.txt
```

## 🚨 Troubleshooting

### Redis Connection Failed

```
Warning: Redis not available: [Errno 111] Connection refused. Using SQLite only.
```

**Solution**: Either start Redis or ignore the warning (system works with SQLite only)

### LLM API Errors

```
ERROR calling anthropic for security: 401 Unauthorized
```

**Solution**: Check your API key is exported: `echo $ANTHROPIC_API_KEY`

### Python Dependencies

```
ModuleNotFoundError: No module named 'yaml'
```

**Solution**: `pip install -r /opt/swarm/requirements.txt`

## 📖 Related Documentation

- [Council Manifest Schema](council_manifest.yaml) - Full configuration reference
- [AI Constitution](../ai_constitution.yaml) - Constitutional constraints
- [Governance Framework](../governance/) - DAO governance structure

## 🤝 Contributing

This is a declassified implementation based on production patterns. Contributions welcome:

1. Test with different LLM configurations
2. Add new execution action types
3. Improve voting algorithms
4. Add monitoring dashboards

## ⚖️ License

See repository LICENSE file.

## 🔮 What's Next?

- [ ] WebSocket API for real-time vote streaming
- [ ] Multi-council federation
- [ ] Machine learning for vote prediction
- [ ] Automatic amendment proposal generation
- [ ] Integration with GitHub Actions for CI/CD decisions
- [ ] Support for human council members via web UI

---

**Built with ❤️ for autonomous AI governance**

*"Not here to hurt, here to love-bomb with undeniable evidence" - The Problem Statement*
