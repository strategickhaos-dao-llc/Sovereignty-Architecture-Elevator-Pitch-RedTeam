# SovereignPRManager Architecture

## Overview

SovereignPRManager is an autonomous pull request orchestration system that coordinates multiple AI agents to review and process pull requests with high confidence.

## System Components

### 1. PR Monitor (`core/pr_monitor.py`)

The PR Monitor watches GitHub repositories for new pull requests and publishes events to NATS JetStream.

**Key Features:**
- Continuous polling of GitHub API
- Deduplication of processed PRs
- Event publishing to NATS

### 2. Legion Reviewer (`ai_legion/legion_reviewer.py`)

The Legion Reviewer coordinates parallel reviews from multiple AI systems:

- **Claude Security Review**: Scans for vulnerabilities, credential exposure
- **Claude Sovereignty Review**: Checks alignment with architecture principles
- **GPT-4 Architecture Review**: Evaluates design patterns and structure
- **GPT-4 Performance Review**: Analyzes efficiency and optimization

### 3. Synthesizer (planned)

Will combine reviews using dialectical synthesis:
1. Collect all reviews
2. Identify conflicts
3. Generate consensus
4. Apply cryptographic provenance

## Data Flow

```
GitHub PR → PR Monitor → NATS → Legion Reviewer → Synthesis → GitHub Comment
```

## Event Schema

### pr.detected

```json
{
  "type": "pr.new",
  "pr_number": 123,
  "title": "Feature: Add new capability",
  "author": "username",
  "created_at": "2025-12-04T00:00:00Z",
  "updated_at": "2025-12-04T00:00:00Z",
  "url": "https://github.com/...",
  "diff_url": "https://github.com/.../pull/123.diff",
  "files_changed": 5,
  "additions": 100,
  "deletions": 50,
  "timestamp": "2025-12-04T00:00:00Z"
}
```

### Review Result

```json
{
  "pr_number": 123,
  "title": "Feature: Add new capability",
  "reviews": [...],
  "synthesis": {
    "total_reviewers": 4,
    "approvals": 4,
    "rejections": 0,
    "average_confidence": 0.95,
    "recommendation": "approve",
    "auto_merge_eligible": true
  },
  "timestamp": "2025-12-04T00:00:00Z"
}
```

## Security Considerations

- API keys stored as environment variables
- NATS communication can be secured with TLS
- All AI interactions logged for audit
- No credentials stored in code
