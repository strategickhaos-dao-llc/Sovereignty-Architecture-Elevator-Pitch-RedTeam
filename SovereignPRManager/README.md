# SovereignPRManager v1.0

## Autonomous Pull Request Orchestration System

**Philosophy:** Zero-button operation through multi-AI synthesis

**Status:** 🟢 ACTIVE

**Confidence Threshold:** 90% for auto-merge

## Legion Members

- **Claude**: Security + Sovereignty review
- **GPT-4**: Architecture + Performance review
- **Grok**: Pattern recognition + Synthesis
- **Gemini**: Compliance validation

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOVEREIGNPRMANAGER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌─────────────────┐    ┌───────────────┐  │
│  │  PR Monitor  │───▶│  NATS JetStream │───▶│  AI Legion    │  │
│  │  (GitHub)    │    │  (Event Bus)    │    │  (Reviewers)  │  │
│  └──────────────┘    └─────────────────┘    └───────────────┘  │
│                                                      │          │
│                              ┌───────────────────────┘          │
│                              ▼                                   │
│                    ┌─────────────────┐                          │
│                    │   Synthesizer   │                          │
│                    │  (Consensus)    │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│                             ▼                                    │
│                    ┌─────────────────┐                          │
│                    │  Auto-Merge     │                          │
│                    │  (90%+ conf)    │                          │
│                    └─────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
export GITHUB_TOKEN="your_github_token"
export ANTHROPIC_API_KEY="your_anthropic_key"
export OPENAI_API_KEY="your_openai_key"
export NATS_URL="nats://localhost:4222"

# 3. Start the system
python -m core.pr_monitor
```

## Components

### Core PR Monitor (`core/pr_monitor.py`)

Watches GitHub repositories for new pull requests and publishes events to NATS JetStream for processing by the AI Legion.

### AI Legion Reviewer (`ai_legion/legion_reviewer.py`)

Coordinates multiple AI agents for comprehensive PR review:
- **Security Review**: Vulnerability scanning, credential detection
- **Sovereignty Review**: Architecture alignment verification
- **Performance Review**: Code quality and optimization analysis
- **Compliance Review**: Policy and standard validation

### Synthesizer

Combines reviews from multiple AI agents using dialectical synthesis:
1. Collect all reviews
2. Identify conflicts and agreements
3. Generate consensus recommendation
4. Apply cryptographic provenance

### Auto-Merge Gate

When synthesis achieves 90%+ confidence:
1. Post consolidated review comment
2. Request final human approval (optional)
3. Execute merge with full audit trail

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | Yes |
| `ANTHROPIC_API_KEY` | Anthropic API Key for Claude | Yes |
| `OPENAI_API_KEY` | OpenAI API Key for GPT-4 | Yes |
| `NATS_URL` | NATS JetStream server URL | Yes |
| `CONFIDENCE_THRESHOLD` | Auto-merge threshold (default: 0.9) | No |
| `REVIEW_INTERVAL` | PR check interval in seconds (default: 10) | No |

### Repository Configuration

Create `.sovereignty/config.yaml` in your repository:

```yaml
pr_manager:
  enabled: true
  auto_merge: false  # Set true for fully autonomous operation
  confidence_threshold: 0.9
  
  reviewers:
    security:
      enabled: true
      model: claude-sonnet-4-20250514
    sovereignty:
      enabled: true
      model: claude-sonnet-4-20250514
    architecture:
      enabled: true
      model: gpt-4
    performance:
      enabled: true
      model: gpt-4
      
  notifications:
    discord: true
    channel_id: "your_channel_id"
```

## Integration with Sovereignty Architecture

SovereignPRManager aligns with the core principles of the Sovereignty Architecture:

1. **Zero-Trust**: Every review is verified independently
2. **Self-Hosted**: Runs on your infrastructure
3. **Cryptographic Verification**: All decisions are signed
4. **Audit Trail**: Complete history of all reviews
5. **880x Cost Reduction**: AI automation at sovereign scale

## License

MIT License - Built by Domenic G. Garza (StrategicKhaos DAO LLC)

---

*"Dialectical synthesis → Cryptographic provenance → Auto-merge"*
