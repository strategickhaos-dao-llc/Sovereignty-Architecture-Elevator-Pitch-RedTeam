# Risk Query Examples

**How to Use the Risk Corpus for Decision Support**

---

## Overview

This document provides example queries for using the risk corpus and current risk inventory with AI systems.

---

## Setup

Before querying, provide context:

```markdown
I'm assessing risks for Strategickhaos using:
- Risk corpus: governance/risks/risks_bibliography.json (100 historical failures)
- Current risks: governance/risks/risks_from_corpus.json (8 active risks)
- Current maturity: 51% (lab-only)

[Your question here]
```

---

## Example Queries

### 1. Change Risk Assessment

**Query:**
```markdown
Using the Strategickhaos risk corpus:

I want to expose our event gateway to the public internet.

Current state:
- Running on Kubernetes
- HMAC validation in place
- Rate limiting configured
- No WAF currently

Question: What historical failures should I consider, and what mitigations are needed?
```

**Expected Response:**
- Relevant historical cases (HF-016, HF-046, etc.)
- Common failure patterns
- Required mitigations
- Risk rating for this change

---

### 2. Dependency Risk Check

**Query:**
```markdown
Using the Strategickhaos risk corpus:

I'm adding these new dependencies:
- PostgreSQL 15
- Redis 7.2
- OpenTelemetry SDK

Question: What historical failures relate to these technologies?
```

**Expected Response:**
- Relevant entries for each technology
- Common issues and mitigations
- Configuration recommendations

---

### 3. Current Risk Status

**Query:**
```markdown
Using governance/risks/risks_from_corpus.json:

What is our current risk status? Which risks need immediate attention?
```

**Expected Response:**
- Summary of 8 active risks
- Priority ranking
- Critical: RISK-001 (single operator)
- Recommendations for next actions

---

### 4. Mitigation Validation

**Query:**
```markdown
Using the Strategickhaos risk corpus:

I've implemented these mitigations for RISK-003 (Security Hardening):
- Network policies in Kubernetes
- Vault for secrets
- TLS everywhere

Question: Based on historical failures, are these mitigations sufficient?
```

**Expected Response:**
- Gap analysis against corpus
- Additional recommendations
- Remaining risk level

---

### 5. Technology Selection

**Query:**
```markdown
Using the Strategickhaos risk corpus:

I need to choose a message queue:
- Option A: Redis Streams
- Option B: Apache Kafka
- Option C: NATS

Question: What historical failures should inform this decision?
```

**Expected Response:**
- Relevant failures for each technology
- Risk comparison
- Recommendation based on our context

---

### 6. New Risk Identification

**Query:**
```markdown
Using the Strategickhaos risk corpus and current risks:

I'm planning to add:
- User authentication (Keycloak)
- API rate limiting
- Public documentation site

Question: What new risks should I add to our inventory?
```

**Expected Response:**
- Identified new risks
- Severity and likelihood assessment
- Related corpus entries
- Suggested risk entries

---

## Query Patterns

### Pattern: Historical Precedent

```markdown
"What historical failures relate to [technology/change]?"
```

### Pattern: Gap Analysis

```markdown
"Given [current state], what risks from the corpus apply?"
```

### Pattern: Mitigation Validation

```markdown
"Are [implemented mitigations] sufficient based on historical failures?"
```

### Pattern: Risk Comparison

```markdown
"Compare risks between [option A] and [option B] based on corpus."
```

---

## Risk Categories in Corpus

| Category | Entries | Key Patterns |
|----------|---------|--------------|
| Security Breaches | 55 | Access control, patching, encryption |
| Data Loss | 8 | Backup, restore testing, redundancy |
| System Outages | 12 | Config management, monitoring, DR |
| Scaling Failures | 3 | Limits, testing, capacity planning |
| Human Error | 3 | Automation, checklists, review |
| Vendor Issues | 19 | Diversity, contracts, alternatives |

---

## Using Results

### Accept Risk Findings:
1. Add to `risks_from_corpus.json`
2. Assign owner
3. Define mitigation plan
4. Update state snapshot

### Override Risk Findings:
1. Document rationale
2. Log accepted risk
3. Define monitoring approach

### Request More Analysis:
1. Ask specific follow-up
2. Provide additional context
3. Request related corpus entries

---

## Best Practices

### DO:
- ✅ Provide specific context
- ✅ Reference specific technologies
- ✅ Ask for historical precedent
- ✅ Request mitigation recommendations
- ✅ Consider our lab-only status

### DO NOT:
- ❌ Ignore corpus warnings
- ❌ Skip mitigation planning
- ❌ Assume risks don't apply
- ❌ Make production decisions without risk review

---

*Examples Version: 1.0*
