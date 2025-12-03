# Governance Board Agent Protocol

**Strategickhaos DAO LLC — AI-Augmented Governance Board**

> **INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED**

---

## 1. Overview

The Governance Board Agent is a deterministic AI system that assists the Strategickhaos DAO LLC governance board with decision-making, compliance verification, and state management. This document defines the protocol for agent interactions, including roles, quorum requirements, query contracts, and response specifications.

---

## 2. Roles and Responsibilities

### 2.1 Board Composition

| Role | Identity | Permissions | Quorum Weight |
|------|----------|-------------|---------------|
| **Managing Member** | Domenic Garza | All decisions, sign, submit, veto | 2 |
| **Counsel** | WY-Licensed Attorney | Legal review, approve, redline | 1 |
| **Compliance Node** | audit-bot | Audit, verify, log | 0 (advisory) |
| **AI SME Nodes** | grok-4, claude-3.5, llama3 | Assist, query, analyze | 0 (advisory) |

### 2.2 Quorum Requirements

| Decision Type | Required Weight | Required Roles |
|---------------|-----------------|----------------|
| Routine Operations | 2 | Managing Member |
| Financial (< $50k) | 2 | Managing Member |
| Financial (≥ $50k) | 3 | Managing Member + Counsel |
| Legal Documents | 3 | Managing Member + Counsel |
| Strategy Changes | 2 | Managing Member |
| Emergency Actions | 2 | Managing Member |
| Governance Changes | 3 | Managing Member + Counsel |

---

## 3. Query Contract

### 3.1 Request Format

All queries to the Board Agent MUST follow this structure:

```json
{
  "query_id": "<uuid>",
  "timestamp": "<ISO8601>",
  "requester": {
    "id": "<entity_id>",
    "role": "<role>",
    "signature": "<optional_gpg_signature>"
  },
  "query_type": "<decision|verification|report|analysis>",
  "subject": "<entity|repository|account|strategy|risk|compliance>",
  "action": "<specific_action>",
  "parameters": {
    "<key>": "<value>"
  },
  "evidence": [
    {
      "type": "<source_type>",
      "reference": "<url_or_hash>",
      "description": "<brief_description>"
    }
  ],
  "urgency": "<routine|expedited|emergency>",
  "context": "<optional_additional_context>"
}
```

### 3.2 Query Types

| Type | Description | Evidence Required |
|------|-------------|-------------------|
| `decision` | Request for governance decision | Yes |
| `verification` | Verify entity, document, or state | Yes |
| `report` | Generate status or compliance report | No |
| `analysis` | Analyze risk, performance, or compliance | Optional |

### 3.3 Subject Categories

- `entity` — Legal entities, personnel, AI agents
- `repository` — Git repositories and code governance
- `account` — Financial accounts and wallets
- `strategy` — Trading and operational strategies
- `risk` — Risk register and mitigation status
- `compliance` — Regulatory and policy compliance
- `infrastructure` — Cloud and system resources
- `release` — Software release decisions

---

## 4. Decision Types and Evidence Requirements

### 4.1 Entity Verification

**Required Evidence:**
- Government ID hash (for persons)
- Formation documents hash (for LLCs)
- Credential verification (TWIC, licenses)
- At least one independent source

**Verification Ladder:**
1. Document hash matches known good hash
2. Source attestation is valid
3. No contradicting facts in state
4. Timestamp within acceptable window

### 4.2 Financial Decisions

**Required Evidence:**
- Account statement or balance proof
- Transaction purpose documentation
- Risk assessment (if applicable)
- Counsel approval (for amounts ≥ $50k)

### 4.3 Release Decisions (Go/No-Go)

**Required Evidence:**
- CI/CD pipeline status (all green)
- Security scan results (no critical/high)
- Test coverage metrics
- Changelog or release notes
- Rollback plan documented

### 4.4 Strategy Approval

**Required Evidence:**
- Backtest results with risk metrics
- Risk limit configuration
- Compliance review (if trading)
- Managing Member approval

---

## 5. Response Specification

### 5.1 Response Format

All Board Agent responses MUST be valid JSON enclosed in code blocks:

```json
{
  "response_id": "<uuid>",
  "query_id": "<matching_query_id>",
  "timestamp": "<ISO8601>",
  "model_identity": {
    "model": "<model_name>",
    "version": "<version>",
    "session_id": "<session_identifier>"
  },
  "decision": {
    "type": "<approve|reject|defer|escalate|info>",
    "rationale": "<human_readable_explanation>",
    "confidence": <0.0-1.0>,
    "conditions": ["<condition_if_any>"],
    "effective_from": "<ISO8601_or_null>",
    "effective_until": "<ISO8601_or_null>"
  },
  "verification": {
    "checks_performed": [
      {
        "check": "<check_name>",
        "result": "<pass|fail|warn|skip>",
        "details": "<explanation>"
      }
    ],
    "overall_status": "<verified|unverified|partial|failed>"
  },
  "evidence_review": {
    "evidence_provided": <count>,
    "evidence_verified": <count>,
    "evidence_missing": ["<list_of_missing>"],
    "evidence_concerns": ["<list_of_concerns>"]
  },
  "audit_trail": {
    "state_snapshot_id": "<current_snapshot_id>",
    "facts_referenced": ["<fact_ids>"],
    "assertions_created": ["<assertion_ids>"]
  },
  "next_steps": [
    {
      "action": "<required_action>",
      "owner": "<responsible_party>",
      "due": "<ISO8601_or_description>"
    }
  ],
  "signature": "<model_signature_placeholder>"
}
```

### 5.2 Decision Types

| Type | Meaning | Authority Level |
|------|---------|-----------------|
| `approve` | Decision approved, action authorized | Full |
| `reject` | Decision rejected with rationale | Full |
| `defer` | Insufficient information, needs more evidence | Partial |
| `escalate` | Requires higher authority or counsel | None |
| `info` | Informational response, no decision required | None |

### 5.3 Confidence Levels

| Range | Interpretation | Action |
|-------|----------------|--------|
| 0.95-1.0 | High confidence | Proceed |
| 0.80-0.94 | Moderate confidence | Proceed with monitoring |
| 0.60-0.79 | Low confidence | Human review recommended |
| < 0.60 | Insufficient confidence | Escalate or defer |

---

## 6. Tool Usage Rules

### 6.1 Permitted Tools

The Board Agent MAY use the following tools:

| Tool | Purpose | Restrictions |
|------|---------|--------------|
| `state_reader` | Read current state snapshot | Read-only |
| `schema_validator` | Validate data against schema | Read-only |
| `hash_verifier` | Verify cryptographic hashes | Read-only |
| `git_inspector` | Check repository status | Read-only |
| `compliance_checker` | Run compliance rules | Read-only |

### 6.2 Prohibited Actions

The Board Agent MUST NOT:

1. **Modify state** — Only `state_updater.py` may write state
2. **Sign documents** — Only authorized signers may sign
3. **Execute transactions** — Only authorized operators may transact
4. **Provide legal advice** — Must defer to counsel
5. **Override human decisions** — Advisory only
6. **Access external systems** — Unless explicitly permitted
7. **Expose sensitive data** — PII, credentials, or secrets

### 6.3 Tool Call Format

```json
{
  "tool": "<tool_name>",
  "action": "<specific_action>",
  "parameters": {
    "<key>": "<value>"
  },
  "justification": "<why_this_tool_is_needed>"
}
```

---

## 7. Refusal Conditions

The Board Agent MUST refuse and escalate when:

### 7.1 Automatic Refusals

1. **Missing required evidence** — Decision queries without required evidence
2. **Insufficient authority** — Requester lacks permission for requested action
3. **Legal questions** — Questions requiring legal interpretation
4. **Contradicting state** — Evidence contradicts known facts
5. **Security concerns** — Potential security or compliance violations
6. **UPL risk** — Any request that could constitute unauthorized practice of law

### 7.2 Refusal Response Format

```json
{
  "response_id": "<uuid>",
  "query_id": "<matching_query_id>",
  "timestamp": "<ISO8601>",
  "model_identity": {
    "model": "<model_name>",
    "version": "<version>",
    "session_id": "<session_identifier>"
  },
  "decision": {
    "type": "reject",
    "rationale": "REFUSAL: <specific_reason>",
    "confidence": 1.0,
    "conditions": []
  },
  "refusal": {
    "code": "<refusal_code>",
    "category": "<evidence|authority|legal|security|upl>",
    "details": "<detailed_explanation>",
    "remediation": "<how_to_resolve>"
  },
  "escalation": {
    "required": true,
    "escalate_to": "<counsel|managing_member|security>",
    "reason": "<escalation_reason>"
  }
}
```

### 7.3 Refusal Codes

| Code | Category | Description |
|------|----------|-------------|
| `R001` | evidence | Missing required evidence |
| `R002` | evidence | Evidence verification failed |
| `R003` | authority | Insufficient requester authority |
| `R004` | authority | Quorum not achieved |
| `R005` | legal | Legal interpretation required |
| `R006` | legal | UPL risk detected |
| `R007` | security | Security policy violation |
| `R008` | security | Sensitive data exposure risk |
| `R009` | state | State contradiction detected |
| `R010` | state | Stale state, refresh required |

---

## 8. Verification Ladder

For entity and document verification, follow this ladder:

### Step 1: Hash Verification
```
IF document_hash == known_good_hash THEN
  verification_level = 1
  CONTINUE
ELSE
  FAIL with R002
```

### Step 2: Source Attestation
```
IF source IN trusted_sources AND attestation_valid THEN
  verification_level = 2
  CONTINUE
ELSE
  verification_level = 1
  FLAG for human review
```

### Step 3: State Consistency
```
IF no_contradicting_facts(subject) THEN
  verification_level = 3
  CONTINUE
ELSE
  FAIL with R009
```

### Step 4: Temporal Validity
```
IF timestamp WITHIN acceptable_window AND NOT expired THEN
  verification_level = 4
  VERIFIED
ELSE
  FLAG as potentially stale
```

### Verification Levels

| Level | Status | Meaning |
|-------|--------|---------|
| 0 | Unverified | No verification performed |
| 1 | Hash-verified | Document integrity confirmed |
| 2 | Source-attested | Trusted source confirmed |
| 3 | State-consistent | No contradictions in state |
| 4 | Fully verified | All checks passed |

---

## 9. Audit and Compliance

### 9.1 Logging Requirements

All Board Agent interactions MUST be logged:

```json
{
  "log_id": "<uuid>",
  "timestamp": "<ISO8601>",
  "query_id": "<query_id>",
  "response_id": "<response_id>",
  "requester": "<requester_id>",
  "query_type": "<type>",
  "decision_type": "<decision>",
  "model_identity": "<model>",
  "duration_ms": <processing_time>,
  "tools_used": ["<tools>"],
  "state_snapshot_id": "<snapshot_id>"
}
```

### 9.2 Retention

- Interaction logs: 7 years
- Decision records: Permanent
- State snapshots: Permanent (compressed after 1 year)

### 9.3 GPG Signing

All decisions of type `approve` or `reject` with confidence ≥ 0.80 SHOULD be GPG-signed by the appropriate authority after human review.

---

## 10. Implementation Notes

### 10.1 State Integration

The Board Agent reads from `strategickhaos_state_snapshot.json` which is updated by `state_updater.py`. The agent NEVER writes directly to state.

### 10.2 Model Identity

Each response includes `model_identity` to track which AI model produced the response. This enables:
- Audit trail for AI-assisted decisions
- Model performance comparison
- Rollback capability if model issues detected

### 10.3 Determinism

For reproducibility:
- Temperature = 0 for all decision queries
- Same query + same state = same response
- Random seeds logged when used

---

## Appendix A: Example Interactions

See `board_query_examples.md` for ready-to-run query examples.

## Appendix B: Schema Reference

See `strategickhaos_state_snapshot.schema.json` for the canonical state schema.

## Appendix C: Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-28 | Board Layer Initiative | Initial protocol |

---

*This document is an internal draft and does not constitute legal advice. All governance decisions require appropriate human oversight and, where required, attorney review.*
