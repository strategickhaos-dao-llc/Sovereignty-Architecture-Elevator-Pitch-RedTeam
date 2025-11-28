# Board Query Examples

**How to Use the Board Layer for Decision Support**

---

## Overview

This document provides example queries for the governance board layer. Use these patterns when seeking AI-assisted decision support.

---

## Setup

Before querying, ensure the AI system has context:

```markdown
I'm working with the Strategickhaos governance framework.

State snapshot: governance/board/strategickhaos_state_snapshot.json
Risk corpus: governance/risks/risks_bibliography.json
Current maturity: 51% (lab-only)

[Your question here]
```

---

## Example Queries

### 1. Architecture Decision

**Query:**
```markdown
Using the Strategickhaos state snapshot:

I want to add a Redis cache layer for session management.

Current state:
- Kubernetes deployment operational
- Vault integration working
- No current caching layer

Question: Should I proceed, and what risks should I consider?
```

**Expected Response Pattern:**
- Assessment of fit with current architecture
- Relevant risks from corpus
- Recommendation with conditions
- Next steps

---

### 2. Security Assessment

**Query:**
```markdown
Using the Strategickhaos state snapshot and risk corpus:

I'm considering exposing the event gateway to the public internet 
with rate limiting and HMAC validation.

Current security posture: 45% maturity
Current status: lab-only

Question: What security risks should I address before this change?
```

**Expected Response Pattern:**
- Current security gaps
- Specific risks from exposing the gateway
- Required mitigations
- Whether this is appropriate for lab status

---

### 3. Maturity Evaluation

**Query:**
```markdown
Using the Strategickhaos state snapshot:

I've completed the following:
- Security audit by external firm
- Added integration tests (coverage now 75%)
- Completed disaster recovery documentation

Question: What is my updated maturity score, and what remains 
for production readiness (80%)?
```

**Expected Response Pattern:**
- Updated maturity calculation
- Gap analysis to 80%
- Prioritized remaining tasks
- Timeline estimate

---

### 4. Risk Analysis

**Query:**
```markdown
Using the Strategickhaos risk corpus:

I'm evaluating whether to use a new AI model provider 
(switching from OpenAI to Anthropic).

Question: What historical failures should I consider when 
changing AI providers?
```

**Expected Response Pattern:**
- Relevant historical failures from corpus
- Risk categories to evaluate
- Migration considerations
- Recommendation

---

### 5. Compliance Check

**Query:**
```markdown
Using the Strategickhaos state snapshot and LAB_RULES.md:

A potential customer wants to use our Discord bot for their 
production server.

Question: Can we offer this service given our current status?
```

**Expected Response Pattern:**
- Clear NO - lab-only status
- Explanation of risks
- What would need to change
- Reference to LAB_RULES.md

---

### 6. Decision Logging

**Query:**
```markdown
Using the Strategickhaos state snapshot:

Decision made: Adopted PostgreSQL for persistent storage

Details:
- Added to docker-compose
- Vault integration for credentials
- Backup strategy documented
- Testing complete

Question: Please generate a decision record for the state snapshot.
```

**Expected Response Pattern:**
- Formatted decision record
- Suggested state snapshot updates
- Any follow-up actions

---

## Query Best Practices

### DO:
- ✅ Provide specific context
- ✅ Reference relevant files
- ✅ State constraints clearly
- ✅ Ask focused questions
- ✅ Request specific output formats

### DO NOT:
- ❌ Ask for legal advice
- ❌ Request production approval (while lab-only)
- ❌ Skip context setup
- ❌ Ask vague questions
- ❌ Ignore risk warnings

---

## Advanced Queries

### Multi-Part Analysis

```markdown
Using the Strategickhaos state snapshot and risk corpus:

I'm planning a series of changes:
1. Add PostgreSQL database
2. Implement user authentication
3. Enable public API access

Question: 
a) What is the combined risk profile of these changes?
b) What order should I implement them?
c) What must be in place before step 3?
```

### Comparative Analysis

```markdown
Using the Strategickhaos state snapshot:

I need to choose between:
Option A: Self-hosted Prometheus + Grafana
Option B: Managed Datadog integration

Current state:
- Kubernetes operational
- Budget constraints exist
- Team size: 1 operator

Question: Which option better fits our current maturity 
and constraints?
```

---

## Response Handling

### Accept Recommendation:
1. Implement suggested changes
2. Update state snapshot
3. Log decision

### Reject Recommendation:
1. Document rationale
2. Identify accepted risks
3. Log decision with override reason

### Request Clarification:
1. Ask specific follow-up
2. Provide additional context
3. Re-query with new information

---

*Examples Version: 1.0*
