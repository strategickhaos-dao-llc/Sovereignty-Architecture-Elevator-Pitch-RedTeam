# Bug Bounty Program Policy
# StrategicKhaos DAO LLC
# Version: 1.0 | Effective: 2025-11-30

## Program Overview

StrategicKhaos DAO LLC operates a bug bounty program to identify security vulnerabilities in our systems. This program is authorized by board resolution (2025-11-30) and operates under strict defensive-only guidelines.

---

## Scope Definition

### Assets in Scope

| Asset Type | Identifier | Criticality |
|------------|------------|-------------|
| Web Application | *.strategickhaos.io | High |
| API Endpoints | api.strategickhaos.io/* | Critical |
| Mobile Apps | Official apps only | Medium |
| Cloud Infrastructure | AWS/GCP resources we own | High |

### Vulnerability Types

**In Scope:**
- Cross-site scripting (XSS)
- SQL injection
- Authentication/authorization flaws
- Server-side request forgery (SSRF)
- Remote code execution
- Information disclosure
- Business logic flaws

**Out of Scope:**
- Rate limiting issues (unless critical)
- Missing security headers (informational)
- Outdated software versions (unless exploitable)
- Issues requiring physical access
- Social engineering

---

## Rules

1. **Authorization Required:** Only test assets explicitly in scope
2. **No Data Access:** Do not access, modify, or exfiltrate user data
3. **Minimal Impact:** Use the least invasive methods possible
4. **Confidentiality:** Do not disclose findings until remediated
5. **Good Faith:** Act honestly and ethically throughout

---

## Rewards

Bounty amounts are determined by:
- Severity of the vulnerability
- Quality of the report
- Potential impact if exploited
- Complexity of discovery

See Safe Harbor Policy for reward ranges.

---

## Compliance

This program operates in full compliance with:
- Computer Fraud and Abuse Act (CFAA)
- Digital Millennium Copyright Act (DMCA)
- Electronic Communications Privacy Act (ECPA)
- Board resolution on defensive-only operations

---

*StrategicKhaos DAO LLC*
*Bug Bounty Program - Defensive Operations*
