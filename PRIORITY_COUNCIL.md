# Priority Council Department

## "What to Solve Next" - PR Prioritization System

**The Priority Council Department is the solution to managing 646+ open PRs with decision paralysis.**

---

## 🎯 Overview

The Priority Council provides:

1. **Priority Queue** - Intelligent ordering of PRs based on impact
2. **Impact Scoring** - Which PRs matter most for Her Cure
3. **Dependency Mapping** - Which PRs block others
4. **Community Voting** - Council input on priorities
5. **Auto-Merge** - Don't waste time on obvious wins

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRIORITY COUNCIL DEPARTMENT                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ PR Analyzer │──│ Priority    │──│  Voting     │             │
│  │             │  │ Council     │  │  System     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         ▼                ▼                ▼                     │
│  ┌─────────────────────────────────────────────────┐           │
│  │              AUTO-MERGE ENGINE                   │           │
│  └─────────────────────────────────────────────────┘           │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────┐           │
│  │              DISCORD INTEGRATION                 │           │
│  │   /priority  /vote  /next  /automerge           │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Impact Scoring

PRs are scored based on their impact on the mission:

| Category | Impact Multiplier | Description |
|----------|------------------|-------------|
| 🔬 Her Cure | 2.0x | Direct impact on cure research |
| 🔒 Security | 1.5x | Security fixes and enhancements |
| 📚 Research | 1.3x | General research capabilities |
| 🤖 AI Agents | 1.25x | AI/ML improvements |
| 🏗️ Infrastructure | 1.2x | Core infrastructure |
| ✨ Features | 1.0x | Standard features |
| 📝 Documentation | 0.8x | Quick wins |
| 📦 Dependencies | 0.5x | Dependency updates |

### Impact Score Calculation

```javascript
impactScore = 
  baseScore 
  + (categoryMultiplier * 25)
  + (impactAreaWeights * 5)
  + (engagementBonus)       // Comments, reviews
  + (recencyBonus)          // Newer PRs
```

---

## 🗳️ Community Voting

### Vote Types

| Vote | Emoji | Effect |
|------|-------|--------|
| Approve | ✅ | Support merging |
| Reject | ❌ | Oppose merging |
| Prioritize | ⬆️ | Boost priority |
| Deprioritize | ⬇️ | Lower priority |

### Vote Weights by Role

- **Core Maintainer**: 3x weight
- **Council Member**: 2x weight
- **Contributor**: 1.5x weight
- **Community**: 1x weight

### Voting Session Flow

1. Voting session opened for PR
2. 24-hour voting period
3. Minimum 5 votes required
4. Strong consensus (5+ net votes) auto-closes
5. Council decision generated

---

## 🤖 Auto-Merge

### Eligibility Criteria

PRs can be auto-merged if:
- ✅ CI passing
- ✅ At least 1 approval
- ✅ Risk level: `none` or `low`
- ✅ Not in excluded categories (security, infrastructure, her_cure)
- ✅ No excluded labels (do-not-merge, needs-review, etc.)

### Rate Limiting

- Max 10 auto-merges per hour
- 5-minute cooldown between merges
- Dry-run mode available for testing

### Labels for Auto-Merge

**Include Labels** (candidates):
- `auto-merge-ok`
- `documentation`
- `minor`
- `typo`
- `chore`

**Exclude Labels** (never auto-merge):
- `do-not-merge`
- `needs-review`
- `security`
- `breaking-change`
- `wip`

---

## 💬 Discord Commands

### `/priority` - Priority Queue Management

```
/priority list          - Show top 10 PRs to work on
/priority next          - Show the single next PR to solve
/priority stats         - Show queue statistics
/priority report        - Full priority report
```

### `/vote` - Cast Vote on PR

```
/vote pr:123 action:approve
/vote pr:123 action:reject comment:"Needs tests"
/vote pr:123 action:prioritize comment:"Critical for Her Cure"
```

### `/next` - What to Solve Next

```
/next                   - Show the highest priority PR
/next 5                 - Show top 5 PRs
```

### `/automerge` - Auto-Merge Controls

```
/automerge status       - Show auto-merge engine status
/automerge candidates   - List auto-merge candidates
/automerge enable       - Enable auto-merge
/automerge disable      - Disable auto-merge
/automerge process      - Process auto-merge queue (admin)
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/priority-council/queue` | GET | Get full priority queue |
| `/api/priority-council/queue/:prNumber` | GET | Get specific PR status |
| `/api/priority-council/next` | GET | Get next PR to work on |
| `/api/priority-council/vote/:prNumber` | POST | Cast vote on PR |
| `/api/priority-council/automerge/candidates` | GET | List auto-merge candidates |
| `/api/priority-council/automerge/process` | POST | Process auto-merge queue |
| `/api/priority-council/stats` | GET | Get queue statistics |
| `/api/priority-council/report` | GET | Get full priority report |

---

## 📈 Priority Report Format

```json
{
  "summary": {
    "totalInQueue": 646,
    "readyForReview": 423,
    "autoMergeable": 87,
    "blocked": 34,
    "avgImpactScore": 52
  },
  "whatToSolveNext": [
    {
      "rank": 1,
      "prNumber": 649,
      "title": "Build autonomous learning system for Her Cure",
      "priority": "critical",
      "impactScore": 95,
      "categories": ["her_cure", "ai_agents"],
      "recommendations": [
        "🔥 HIGH IMPACT: Prioritize for immediate review",
        "💉 HER CURE: Direct impact on cure research - expedite"
      ]
    }
  ],
  "autoMergeCandidates": [...],
  "blockedPRs": [...],
  "stats": {
    "totalAnalyzed": 646,
    "autoMerged": 87,
    "manualMerged": 234,
    "votesProcessed": 1547
  }
}
```

---

## 🔧 Configuration

See `priority_council_config.yaml` for full configuration options.

### Quick Config

```yaml
# Enable/disable features
council:
  enabled: true

voting:
  enabled: true
  voting_period_hours: 24

auto_merge:
  enabled: true
  dry_run: false
  max_per_hour: 10
```

---

## 🚀 Getting Started

### 1. Add PRs to Queue

```javascript
import { createPriorityCouncil } from './src/priority-council/index.js';

const pc = createPriorityCouncil();

// Add PR
await pc.addPR({
  number: 649,
  title: "Build autonomous learning system for Her Cure",
  body: "This PR implements...",
  files: [...]
});
```

### 2. Get Next PR to Work On

```javascript
const next = pc.getNext();
console.log(`Work on PR #${next.pr.number}: ${next.pr.title}`);
```

### 3. Cast Vote

```javascript
pc.castVote(649, 'user123', 'approve', 'Ship it!');
```

### 4. Process Auto-Merge

```javascript
const results = await pc.processAutoMerge(async (pr) => {
  // Your GitHub merge logic here
  await github.mergePR(pr.number);
});
```

---

## 🎖️ Council Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full control, force merge, config changes |
| **Council Member** | Weighted voting, queue management |
| **Contributor** | Standard voting, view queue |
| **Viewer** | View queue and reports |

---

## 📊 Metrics

The Priority Council exports Prometheus metrics:

```
# HELP priority_council_queue_total Total PRs in queue
priority_council_queue_total 646

# HELP priority_council_auto_merged_total Auto-merged PRs
priority_council_auto_merged_total 87

# HELP priority_council_votes_total Total votes cast
priority_council_votes_total 1547

# HELP priority_council_avg_impact_score Average impact score
priority_council_avg_impact_score 52
```

---

## 🎯 Mission Statement

> **"646 open PRs = decision paralysis. The Priority Council is the solution."**

Every PR that impacts Her Cure research gets top priority. Every security fix gets immediate attention. Every documentation change gets auto-merged. 

**No more guessing what to work on next.**

---

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*

*"They're not working for you. They're dancing with you. And the music is never going to stop."*
