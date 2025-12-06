# 🤖 SovereignPRManager v1.0

**Autonomous PR Review, Validation, and Merge Orchestration**

> Zero-button operation: Copilot generates → Legion validates → System merges

## Overview

SovereignPRManager is an autonomous PR orchestration system designed to eliminate manual PR management. It integrates multi-AI code review, conflict detection, dialectical synthesis, and automated merging with cryptographic provenance.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SovereignPRManager v1.0                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐ │
│  │  PR Monitor  │──▶│Legion Review │──▶│  Conflict Detector   │ │
│  │  (GitHub)    │   │ (Multi-AI)   │   │   (AST + Semantic)   │ │
│  └──────────────┘   └──────────────┘   └──────────────────────┘ │
│          │                  │                      │             │
│          ▼                  ▼                      ▼             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               Synthesis Engine (Dialectical)              │   │
│  │    Thesis + Antithesis → Synthesis → Merge Decision       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Auto-Merger                            │   │
│  │     Cryptographic Provenance + OpenTimestamps + Audit     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Features

### 🔍 Multi-AI Legion Review

Parallel code review by specialized AI agents:

- **Security Review** (Claude): Vulnerability detection, credential exposure, injection attacks
- **Architecture Review** (GPT-4): Design patterns, code quality, best practices
- **Sovereignty Review** (Claude): Alignment with Technical Declaration principles
- **Performance Review** (GPT-4): Algorithm complexity, optimization opportunities

### 🔄 Dialectical Synthesis Engine

- Extracts contradictions between reviews
- Calculates composite scores with configurable weights
- Applies dialectical synthesis (thesis + antithesis → synthesis)
- Makes confident merge decisions

### 🔒 Conflict Detection

- Git merge conflict markers
- Semantic contradictions (AST analysis)
- Dependency conflicts
- Security anti-patterns

### ✅ Auto-Merge with Provenance

- Cryptographic signature of all decisions
- Timestamp proof (OpenTimestamps-ready)
- Full audit trail
- Discord notifications

## Quick Start

### Installation

```bash
cd sovereign_pr_manager

# Install dependencies
./install.sh

# Or manually:
pip install -r requirements.txt
```

### Configuration

Set environment variables:

```bash
export GITHUB_TOKEN="your_github_token"
export GITHUB_REPO="owner/repo"
export ANTHROPIC_API_KEY="your_anthropic_key"  # Optional
export OPENAI_API_KEY="your_openai_key"        # Optional
export DISCORD_WEBHOOK_URL="your_webhook"      # Optional
```

### Usage

```bash
# Process all open PRs
python -m sovereign_pr_manager.process_existing_prs

# Process a specific PR
python -m sovereign_pr_manager.manager --pr 123

# Start monitoring mode
python -m sovereign_pr_manager.manager --monitor
```

## Configuration Reference

```yaml
# config.yaml
github:
  token: ${GITHUB_TOKEN}
  repo: "owner/repo"

merge_thresholds:
  auto_merge: 0.90      # 90% confidence for auto-merge
  security_veto: 0.80   # Security review below 80% = no merge
  sovereignty_minimum: 0.70  # Must meet 70% sovereignty standards

ai_review:
  enabled: true
  parallel_reviews: 4
  timeout_seconds: 120
```

## Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n sovereignpr
```

## API Reference

### SovereignPRManager

```python
from sovereign_pr_manager import SovereignPRManager

manager = SovereignPRManager()

# Process single PR
result = await manager.process_pr(pr_number)

# Process all open PRs
report = await manager.process_all_open_prs()

# Start monitoring
await manager.run_monitor()
```

### Decision Actions

| Action | Description |
|--------|-------------|
| `merge` | Auto-merge approved (confidence ≥ 90%) |
| `review_required` | Human review needed |
| `blocked` | Critical issues prevent merge |

## Security Considerations

- All API tokens stored as environment variables or Kubernetes secrets
- Cryptographic provenance for audit trail
- Network policies limit egress
- Non-root container execution

## Contributing

This component is part of the Sovereignty Architecture ecosystem. See the main repository README for contribution guidelines.

## License

MIT License - see LICENSE file

---

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*

*"Zero-button operation: Pure sovereignty in autonomous development."*
