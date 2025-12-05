# Risk Query Examples

**Reference guide for querying the risk corpus and threat model**

---

## 📋 Quick Reference

| Query Type | Use Case | Returns |
|------------|----------|---------|
| `risk_by_id` | Get specific risk details | Single risk object |
| `risks_by_category` | All risks in category | Risk array |
| `critical_risks` | All critical severity risks | Risk array |
| `risks_by_owner` | Risks owned by entity | Risk array |
| `risk_score` | Calculate risk score | Score and interpretation |
| `mitigations_for` | Controls for specific risk | Mitigation array |

---

## 🔍 Example Queries

### 1. Get All Critical Risks

**Question:** "What are our critical risks?"

```json
{
  "query_type": "critical_risks",
  "context": {
    "requested_by": "domenic",
    "timestamp": "2025-11-28T12:00:00Z"
  }
}
```

**Expected Response:**
```json
{
  "result": {
    "count": 7,
    "risks": [
      {
        "id": "RISK-LR-001",
        "name": "Unauthorized Practice of Law",
        "category": "legal_regulatory",
        "severity": "critical",
        "likelihood": "medium",
        "owner": "Managing Member"
      },
      {
        "id": "RISK-LR-003",
        "name": "Securities Law Violation",
        "category": "legal_regulatory",
        "severity": "critical",
        "likelihood": "low",
        "owner": "Managing Member"
      },
      {
        "id": "RISK-FT-001",
        "name": "Catastrophic Trading Loss",
        "category": "financial_trading",
        "severity": "critical",
        "likelihood": "medium",
        "owner": "Trading System"
      },
      {
        "id": "RISK-CS-001",
        "name": "Credential Compromise",
        "category": "cybersecurity",
        "severity": "critical",
        "likelihood": "medium",
        "owner": "DevOps"
      },
      {
        "id": "RISK-CS-002",
        "name": "Infrastructure Breach",
        "category": "cybersecurity",
        "severity": "critical",
        "likelihood": "low",
        "owner": "DevOps"
      },
      {
        "id": "RISK-AI-001",
        "name": "Autonomous Action Without Authorization",
        "category": "ai_governance",
        "severity": "critical",
        "likelihood": "medium",
        "owner": "Managing Member"
      },
      {
        "id": "RISK-TECH-002",
        "name": "Data Loss",
        "category": "technical",
        "severity": "critical",
        "likelihood": "low",
        "owner": "DevOps"
      }
    ]
  }
}
```

---

### 2. Get Risks by Category

**Question:** "What financial trading risks do we have?"

```json
{
  "query_type": "risks_by_category",
  "parameters": {
    "category": "financial_trading"
  },
  "context": {
    "requested_by": "domenic",
    "timestamp": "2025-11-28T12:00:00Z"
  }
}
```

**Expected Response:**
```json
{
  "result": {
    "category": "financial_trading",
    "category_name": "Financial & Trading Risk",
    "severity_baseline": "high",
    "risks": [
      {
        "id": "RISK-FT-001",
        "name": "Catastrophic Trading Loss",
        "severity": "critical",
        "likelihood": "medium",
        "controls": [
          "Daily loss killswitch (2% max)",
          "ATR-based position sizing",
          "No leverage beyond approved limits"
        ]
      },
      {
        "id": "RISK-FT-002",
        "name": "Algorithm Malfunction",
        "severity": "high",
        "likelihood": "medium",
        "controls": [
          "Extensive backtesting",
          "Simulation before live trading",
          "Manual override capability"
        ]
      },
      {
        "id": "RISK-FT-003",
        "name": "Broker Counterparty Risk",
        "severity": "high",
        "likelihood": "low",
        "controls": [
          "Use regulated brokers",
          "Segregated customer funds",
          "SIPC/FDIC coverage where applicable"
        ]
      }
    ]
  }
}
```

---

### 3. Calculate Risk Score

**Question:** "What's the risk score for deploying live trading?"

```json
{
  "query_type": "risk_score",
  "parameters": {
    "risk_id": "RISK-FT-001"
  },
  "context": {
    "requested_by": "domenic",
    "timestamp": "2025-11-28T12:00:00Z"
  }
}
```

**Expected Response:**
```json
{
  "result": {
    "risk_id": "RISK-FT-001",
    "risk_name": "Catastrophic Trading Loss",
    "severity": "critical",
    "severity_weight": 4,
    "likelihood": "medium",
    "likelihood_weight": 2,
    "risk_score": 8,
    "interpretation": "requires_mitigation",
    "recommendation": "Ensure all controls are in place and functioning before proceeding",
    "controls_required": [
      "Daily loss killswitch (2% max)",
      "ATR-based position sizing",
      "No leverage beyond approved limits"
    ]
  }
}
```

---

### 4. Get Mitigations for Risk

**Question:** "How do we mitigate credential compromise risk?"

```json
{
  "query_type": "mitigations_for",
  "parameters": {
    "risk_id": "RISK-CS-001"
  },
  "context": {
    "requested_by": "devops",
    "timestamp": "2025-11-28T12:00:00Z"
  }
}
```

**Expected Response:**
```json
{
  "result": {
    "risk_id": "RISK-CS-001",
    "risk_name": "Credential Compromise",
    "controls": [
      {
        "control": "Secrets management (no hardcoding)",
        "implementation": "Use Vault or environment variables",
        "status": "implemented"
      },
      {
        "control": "Regular credential rotation",
        "implementation": "90-day rotation policy",
        "status": "partial"
      },
      {
        "control": "Audit logging of credential usage",
        "implementation": "CloudWatch/Loki logging",
        "status": "implemented"
      }
    ],
    "monitoring": "Credential usage monitoring, anomaly detection",
    "owner": "DevOps",
    "residual_risk": "medium"
  }
}
```

---

### 5. Get Risks by Owner

**Question:** "What risks am I responsible for as Managing Member?"

```json
{
  "query_type": "risks_by_owner",
  "parameters": {
    "owner": "Managing Member"
  },
  "context": {
    "requested_by": "domenic",
    "timestamp": "2025-11-28T12:00:00Z"
  }
}
```

**Expected Response:**
```json
{
  "result": {
    "owner": "Managing Member",
    "risk_count": 11,
    "by_severity": {
      "critical": 3,
      "high": 4,
      "medium": 4
    },
    "risks": [
      {"id": "RISK-LR-001", "name": "Unauthorized Practice of Law", "severity": "critical"},
      {"id": "RISK-LR-002", "name": "DAO LLC Compliance Failure", "severity": "high"},
      {"id": "RISK-LR-003", "name": "Securities Law Violation", "severity": "critical"},
      {"id": "RISK-FT-002", "name": "Algorithm Malfunction", "severity": "high"},
      {"id": "RISK-FT-003", "name": "Broker Counterparty Risk", "severity": "high"},
      {"id": "RISK-AI-001", "name": "Autonomous Action Without Authorization", "severity": "critical"},
      {"id": "RISK-AI-003", "name": "AI Hallucination Impact", "severity": "high"},
      {"id": "RISK-ORG-001", "name": "Key Person Risk", "severity": "high"},
      {"id": "RISK-ORG-002", "name": "Governance Failure", "severity": "medium"},
      {"id": "RISK-ORG-003", "name": "Conflict of Interest", "severity": "medium"},
      {"id": "RISK-COMP-002", "name": "Tax Reporting Error", "severity": "high"}
    ]
  }
}
```

---

### 6. Risk Summary Query

**Question:** "Give me an overview of our risk posture."

```json
{
  "query_type": "risk_summary",
  "context": {
    "requested_by": "domenic",
    "timestamp": "2025-11-28T12:00:00Z"
  }
}
```

**Expected Response:**
```json
{
  "result": {
    "total_risks": 24,
    "by_severity": {
      "critical": 7,
      "high": 12,
      "medium": 5
    },
    "by_category": {
      "legal_regulatory": 3,
      "financial_trading": 3,
      "cybersecurity": 3,
      "ai_governance": 3,
      "organizational": 3,
      "technical": 3,
      "compliance": 3,
      "operational": 3
    },
    "requiring_immediate_action": [
      {"id": "RISK-FT-001", "score": 8, "reason": "Live trading preparation"},
      {"id": "RISK-CS-001", "score": 8, "reason": "Credential management gaps"}
    ],
    "top_mitigations_needed": [
      "Complete credential rotation policy",
      "Document succession plan",
      "Finalize trading system kill switch testing"
    ]
  }
}
```

---

## 📊 Risk Score Interpretation

| Score Range | Level | Action Required |
|-------------|-------|-----------------|
| 1-3 | Acceptable | Monitor, no immediate action |
| 4-6 | Requires Mitigation | Implement controls, review quarterly |
| 7-9 | Requires Immediate Action | Prioritize mitigation, review monthly |
| 10-12 | Critical | Stop activity until mitigated |

---

## 🔧 Integrating Risk Queries

### In Governance Board Agent

The risk corpus is automatically consulted during:
- `risk_check` queries
- `deployment_ready` assessments
- `covenant_verify` operations

### In CI/CD Pipeline

```yaml
# .github/workflows/risk-check.yml
- name: Check deployment risks
  run: |
    # Query risk corpus for deployment-related risks
    jq '.categories.financial_trading.risks[] | select(.severity == "critical")' governance/risks/risks_from_corpus.json
```

### In Discord

```
/gov risk-check "Deploy BabySolvern to live trading"
/gov risks critical
/gov risks category financial_trading
```

---

*This document provides examples for querying the risk corpus and is part of the Strategickhaos governance framework.*
