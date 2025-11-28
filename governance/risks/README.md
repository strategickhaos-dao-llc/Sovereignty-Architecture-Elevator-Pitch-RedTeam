# Risk Assessment Framework

**Historical Analysis and Current Risk Inventory**

---

## Purpose

This directory contains the risk assessment framework for Strategickhaos:

1. **Risk Bibliography** - 100 historical failures from tech industry
2. **Current Risks** - Active risks for this system
3. **Query Examples** - How to assess risks using AI

---

## Files

| File | Purpose |
|------|---------|
| `risks_bibliography.json` | Historical failure corpus (100 cases) |
| `risks_from_corpus.json` | Current risk inventory (8 active) |
| `risk_query_examples.md` | Risk query patterns |

---

## Risk Inventory Summary

### Current Status

| Severity | Count | Status |
|----------|-------|--------|
| Critical | 1 | Accepted |
| High | 3 | Mitigating |
| Medium | 3 | Monitoring |
| Low | 1 | Accepted |
| **Total** | **8** | |

### Top Risks

1. **RISK-001: Single Point of Failure** (Critical)
   - One operator, no redundancy
   - Mitigation: Documentation, automation

2. **RISK-002: No Disaster Recovery** (High)
   - No tested backup/restore
   - Mitigation: In progress

3. **RISK-003: Incomplete Security Hardening** (High)
   - Security audit not complete
   - Mitigation: Scheduled

4. **RISK-004: Missing Compliance Framework** (High)
   - No SOC2, HIPAA, etc.
   - Mitigation: Research phase

---

## Using the Risk Corpus

### Query Pattern

```markdown
Using the risk corpus at governance/risks/risks_bibliography.json:

I'm planning to [describe change].

Question: What historical failures should inform this decision?
```

### Response Pattern

- Relevant historical cases
- Common failure patterns
- Recommended mitigations
- Confidence level

---

## Risk Categories

The corpus covers these failure categories:

| Category | Cases | Key Lessons |
|----------|-------|-------------|
| Security Breaches | 20 | Access control, encryption |
| Data Loss | 15 | Backup, redundancy |
| System Outages | 18 | Monitoring, DR |
| Scaling Failures | 12 | Load testing, limits |
| Integration Failures | 10 | API contracts, versioning |
| Human Error | 15 | Automation, checklists |
| Vendor Issues | 10 | Redundancy, contracts |

---

## Adding New Risks

### Format

```json
{
  "id": "RISK-XXX",
  "title": "Brief description",
  "category": "security|infrastructure|operational|compliance",
  "severity": "critical|high|medium|low",
  "likelihood": "high|medium|low",
  "impact": "Description of potential impact",
  "status": "identified|mitigating|accepted|resolved",
  "mitigation": "Current mitigation strategy",
  "owner": "Person responsible",
  "created": "YYYY-MM-DD",
  "updated": "YYYY-MM-DD"
}
```

### Process

1. Identify risk
2. Assess severity and likelihood
3. Document in `risks_from_corpus.json`
4. Update state snapshot
5. Assign owner
6. Track mitigation

---

## Integration

Risks integrate with:

- `/governance/board/` - Decision support
- `/LAB_RULES.md` - Operational rules
- `/governance/README.md` - Governance overview

---

## Maintenance

### Monthly Review
- Assess new risks
- Update existing risks
- Check mitigation progress
- Update state snapshot

### Quarterly Review
- Full risk audit
- Corpus updates
- Process improvements

---

*Framework Version: 1.0*
