# Sovereign Swarm Governance Protocol

**Version:** 1.0.0  
**Last Updated:** 2025-11-24  
**Author:** Strategickhaos DAO LLC

## Overview

This document defines the governance protocol for managing the Sovereign Swarm architecture, including:
- Branch naming conventions
- PR scoping and workflow
- CI/CodeQL maintenance
- Swarm mutation governance

The goal is to maintain a clean, secure, and organized repository as the swarm generates and evolves code.

---

## 🌿 Branch Naming Conventions

### Pattern
```
<type>/<description>
```

### Branch Types

| Type | Purpose | Examples | Auto-Delete on Merge |
|------|---------|----------|---------------------|
| `feature/` | New features or capabilities | `feature/yaml-dna-config` | ✅ Yes |
| `bugfix/` | Bug fixes | `bugfix/memory-leak-athena` | ✅ Yes |
| `hotfix/` | Critical production fixes | `hotfix/security-cve-2024` | ✅ Yes |
| `docs/` | Documentation only | `docs/api-reference` | ✅ Yes |
| `refactor/` | Code restructuring | `refactor/mind-kernel-cleanup` | ✅ Yes |
| `test/` | Test additions/fixes | `test/integration-coverage` | ✅ Yes |
| `chore/` | Maintenance tasks | `chore/dependency-update` | ✅ Yes |
| `wip/` | Work in progress (experimental) | `wip/quantum-entanglement` | ⚠️ Manual |
| `experiment/` | Experimental features | `experiment/new-orchestration` | ⚠️ Manual |

### Rules
- Use lowercase letters, numbers, and hyphens only
- Keep descriptions concise but meaningful
- No spaces or special characters (except hyphens)
- Maximum length: 50 characters

### Examples
✅ **Good:**
```
feature/swarm-dna-loader
bugfix/agent-spawn-timeout
docs/governance-protocol
```

❌ **Bad:**
```
feature/New_Feature_123
my-branch
fix bug
feature/this-is-a-very-long-branch-name-that-exceeds-the-character-limit
```

---

## 📋 Pull Request Scoping

### PR Size Guidelines

| Size | Lines Changed | Review Time | Recommendation |
|------|---------------|-------------|----------------|
| **XS** | 1-50 | 5-10 min | Ideal for quick iterations |
| **S** | 51-200 | 15-30 min | Good size for most changes |
| **M** | 201-500 | 30-60 min | Acceptable but consider splitting |
| **L** | 501-1000 | 1-2 hours | Should be split if possible |
| **XL** | 1000+ | 2+ hours | ⚠️ Must be split |

### PR Checklist

Before opening a PR, ensure:

- [ ] **Single Responsibility**: PR addresses one concern
- [ ] **Description**: Clear explanation of what and why
- [ ] **Scope**: Changes are minimal and focused
- [ ] **Tests**: Added/updated tests for new code
- [ ] **Documentation**: Updated relevant docs
- [ ] **Linting**: Code passes lint checks
- [ ] **Build**: Code builds successfully
- [ ] **Security**: No new vulnerabilities introduced
- [ ] **Labels**: Appropriate labels applied

### PR Template

```markdown
## Description
[Brief description of changes]

## Type of Change
- [ ] Feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactor
- [ ] Test

## Trinity Role
- [ ] Thesis (Creator)
- [ ] Antithesis (Critic)
- [ ] Synthesis (Integrator)

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Security
- [ ] No secrets committed
- [ ] Dependencies scanned
- [ ] CodeQL checks pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### PR Labels

| Label | Purpose | When to Use |
|-------|---------|-------------|
| `swarm-generated` | Created by agent | All agent-generated PRs |
| `needs-review` | Awaiting human review | When ready for review |
| `wip` | Work in progress | Not ready for review |
| `blocked` | Blocked by dependency | Waiting on something |
| `security` | Security-related | Vulnerabilities, fixes |
| `breaking-change` | Breaking API change | User-facing changes |
| `documentation` | Docs only | No code changes |
| `dependencies` | Dependency updates | Package updates |

---

## 🚀 CI/CD Workflow

### Required Checks

All PRs must pass these checks before merge:

1. **Lint** - Code style and formatting
2. **Build** - Code compiles/builds successfully
3. **Test** - All tests pass
4. **Security** - CodeQL and dependency scanning

### GitHub Actions Workflow

```yaml
on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run lint
  
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm test
  
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: github/codeql-action/init@v2
      - uses: github/codeql-action/analyze@v2
```

### Status Badges

Add to README.md:
```markdown
![Build](https://github.com/Strategickhaos/repo/workflows/build/badge.svg)
![Tests](https://github.com/Strategickhaos/repo/workflows/test/badge.svg)
![Security](https://github.com/Strategickhaos/repo/workflows/security/badge.svg)
```

---

## 🔒 CodeQL Maintenance

### When to Run

- **On every commit** to any PR branch
- **On merge** to main branch
- **Scheduled** daily for main branch
- **Manually** when investigating issues

### Handling Alerts

#### 1. Triage New Alerts

```bash
# List all open alerts
gh api repos/:owner/:repo/code-scanning/alerts --jq '.[] | {number, rule_id, state}'
```

For each alert:
1. **Review** - Understand the vulnerability
2. **Classify** - False positive or real issue?
3. **Prioritize** - Critical, High, Medium, Low
4. **Assign** - Who should fix it?

#### 2. Fix Real Issues

```bash
# Create branch
git checkout -b bugfix/codeql-alert-123

# Fix the issue
# ... make changes ...

# Reference in commit
git commit -m "fix: resolve CodeQL alert #123 - SQL injection"

# Push and create PR
git push origin bugfix/codeql-alert-123
```

#### 3. Dismiss False Positives

In GitHub UI:
1. Go to Security → Code scanning
2. Select the alert
3. Click "Dismiss alert"
4. Select reason: "False positive"
5. Add comment explaining why

#### 4. Track Progress

Create a tracking issue:
```markdown
## CodeQL Alert Remediation

### Critical (0)
- None

### High (2)
- [ ] #123 SQL injection in user input
- [ ] #124 Command injection in shell exec

### Medium (5)
- [ ] #125 Path traversal in file handler
- ...

### Low (3)
- [ ] #130 Weak cryptography
- ...
```

### CodeQL Configuration

`.github/codeql/codeql-config.yml`:
```yaml
name: "CodeQL Config"
queries:
  - uses: security-extended
  - uses: security-and-quality

paths-ignore:
  - node_modules/**
  - dist/**
  - coverage/**
  - benchmarks/reports/**
```

---

## 🐝 Swarm Mutation Governance

### Agent-Generated PR Workflow

1. **Agent Creates Branch**
   - Follow branch naming conventions
   - Use `swarm-generated` label

2. **Agent Commits Changes**
   - Follow conventional commit format
   - Keep commits atomic and focused

3. **Agent Opens PR**
   - Use PR template
   - Mark as `[WIP]` initially
   - Add relevant labels

4. **Automated Checks Run**
   - Lint, build, test, security
   - Agent monitors check results

5. **Human Gatekeeper Review**
   - **Thesis PRs**: Quick review, merge if good
   - **Antithesis PRs**: Thorough security review
   - **Synthesis PRs**: Full integration validation

6. **Merge or Request Changes**
   - If approved: Squash and merge
   - If changes needed: Agent iterates
   - If unrecoverable: Close and start fresh

### Cleanup Strategy

#### Weekly Cleanup
```bash
#!/bin/bash
# cleanup-prs.sh

echo "🧹 Cleaning up stale PRs..."

# Close failed WIP PRs older than 7 days
gh pr list --state open --label wip --search "updated:<$(date -d '7 days ago' +%Y-%m-%d)" \
  | awk '{print $1}' \
  | xargs -I {} gh pr close {} -c "Closing stale WIP PR"

# Archive completed PRs
gh pr list --state closed --limit 100 --json number,title,closedAt \
  > .github/archived-prs-$(date +%Y%m%d).json
```

#### Branch Protection

`.github/branch-protection.json`:
```json
{
  "main": {
    "required_reviews": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_status_checks": [
      "lint",
      "test",
      "security"
    ],
    "enforce_admins": false,
    "allow_force_pushes": false,
    "allow_deletions": false
  }
}
```

### Mutation Rate Control

From `config/swarm_dna.yaml`:
```yaml
swarm_behavior:
  mutation_rate: 0.1  # 10% of PRs can be experimental
  learning_enabled: true
  memory_persistence: true
```

**Mutation Guidelines:**
- **10% experimental** - Allow agents to try new approaches
- **90% conservative** - Follow established patterns
- Monitor mutation success rate
- Adjust mutation_rate based on outcomes

### Human Gatekeeping Points

| Stage | Automated | Human Required | Rationale |
|-------|-----------|----------------|-----------|
| Branch Creation | ✅ | ❌ | Low risk |
| Commit | ✅ | ❌ | Reversible |
| PR Open | ✅ | ❌ | Reviewable |
| CI Checks | ✅ | ❌ | Automated |
| Security Scan | ✅ | ⚠️ If alerts | Critical path |
| Code Review | ❌ | ✅ | Quality gate |
| Merge | ❌ | ✅ | Final approval |
| Production Deploy | ❌ | ✅ | Critical gate |

---

## 📊 Metrics and Monitoring

### Key Metrics

Track these metrics to monitor swarm health:

```yaml
swarm_health_metrics:
  pr_metrics:
    - open_prs_count
    - merged_prs_count
    - closed_without_merge_count
    - average_pr_size
    - average_review_time
    
  quality_metrics:
    - test_coverage_percentage
    - lint_pass_rate
    - security_scan_pass_rate
    - build_success_rate
    
  agent_metrics:
    - active_agents_count
    - tasks_completed_per_agent
    - agent_success_rate
    - convergence_rate
```

### Dashboard

Create `.github/swarm-dashboard.md`:
```markdown
## Swarm Health Dashboard

**Last Updated:** [Auto-generated timestamp]

### PR Statistics
- 📊 Open: 12 PRs
- ✅ Merged (7d): 25 PRs
- ❌ Closed (7d): 3 PRs
- ⏱️ Avg Review Time: 4.5 hours

### Quality Gates
- ✅ Tests: 98.5% passing
- ✅ Lint: 100% passing
- ⚠️ Security: 2 medium alerts
- ✅ Build: 100% passing

### Agent Activity
- 🤖 Active Agents: 5/5
- 📈 Convergence Rate: 92%
- 🎯 Tasks Completed: 127
```

### Alerts

Set up notifications for:
- PR open > 7 days
- Failed security scan
- Build failure on main
- More than 10 open WIP PRs
- Test coverage drop > 5%

---

## 🎯 Best Practices

### For Human Gatekeepers

1. **Review Promptly** - Don't let PRs sit for days
2. **Be Specific** - Give actionable feedback
3. **Trust the Process** - Let agents iterate
4. **Focus on Architecture** - Don't nitpick style (lint does that)
5. **Security First** - Never compromise on security
6. **Document Decisions** - Explain why you approved/rejected

### For Agents

1. **Follow DNA** - Respect the swarm configuration
2. **Stay Focused** - One task per PR
3. **Test Everything** - Don't skip tests
4. **Document Changes** - Explain what and why
5. **Iterate on Feedback** - Learn from reviews
6. **Fail Fast** - Don't continue if blocked

### For the Swarm

1. **Maintain Hygiene** - Regular cleanup of stale PRs
2. **Monitor Health** - Track metrics continuously
3. **Evolve DNA** - Update configuration as you learn
4. **Balance Autonomy** - Not too aggressive, not too timid
5. **Preserve Memory** - Keep institutional knowledge
6. **Stay Secure** - Security is non-negotiable

---

## 🆘 Troubleshooting

### "Too Many Open PRs"

**Symptom:** More than 20 open PRs, mostly WIP

**Solution:**
```bash
# Triage all WIP PRs
gh pr list --label wip --state open

# Close obvious failures
gh pr close <number> --comment "Closing due to [reason]"

# Merge ready ones
gh pr merge <number> --squash
```

### "CI Always Failing"

**Symptom:** All PRs failing CI checks

**Solution:**
1. Check if main branch is broken
2. Fix the root cause on main
3. Rebase/merge main into PR branches
4. Rerun checks

### "CodeQL Alert Storm"

**Symptom:** Hundreds of new CodeQL alerts

**Solution:**
1. Don't panic - likely a new query added
2. Review sample of alerts
3. Batch fix common patterns
4. Dismiss false positives
5. Create tracking issue for rest

### "Agent Stuck in Loop"

**Symptom:** Agent keeps recreating same PR

**Solution:**
1. Check agent logs
2. Review quantum loop convergence
3. Adjust convergence threshold
4. Manually close stuck PRs
5. Update DNA configuration

---

## 📚 References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Swarm DNA Configuration](./config/swarm_dna.yaml)
- [Mind Kernel Documentation](./swarm/sovereign_mind_kernel.py)

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-24 | Initial governance protocol |

---

**Questions or feedback?** Open an issue with label `governance-feedback`
