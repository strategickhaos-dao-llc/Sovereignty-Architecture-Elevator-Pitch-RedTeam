# Client Zero Protocols

**Strategickhaos DAO LLC / Valoryield Engine**  
**Case Initiation and Selection Framework**

**INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED**

---

## Overview

Client Zero represents the first case handled by the Valoryield Engine to demonstrate capabilities and establish operational precedent. This document outlines the protocols for selecting, initiating, and executing Client Zero engagements.

---

## Target Selection Criteria

### Mandatory Requirements

All Client Zero targets must satisfy **ALL** of the following criteria:

| # | Criterion | Description |
|---|-----------|-------------|
| 1 | **Legal Compliance** | All investigation methods must be 100% lawful |
| 2 | **Public Data** | OSINT relies exclusively on publicly available information |
| 3 | **Consent-Based** | Any red-team activities require explicit written consent |
| 4 | **Pro Bono/DAO-Funded** | Services provided free to vulnerable populations |
| 5 | **Ethics Committee Approval** | Case reviewed and approved by DAO Ethics Committee |
| 6 | **Documented Impact** | Clear potential benefit to vulnerable populations |

### Disqualifying Factors

Cases will be **rejected** if they involve:

- ❌ Unauthorized system access
- ❌ Private data without consent
- ❌ Illegal surveillance methods
- ❌ Vigilante activities
- ❌ Personal vendettas without public interest
- ❌ Activities outside NAICS 561611 scope

---

## Target Categories

### Category A: Compliance Service Providers

**Target Examples:**
- Harbor Compliance
- LegalZoom
- Northwest Registered Agent

**Service Type:** Public-facing audit + pricing transparency report

**Methodology:**
- OSINT analysis of public pricing structures
- Comparison with actual service costs
- Public filing analysis
- Consumer review aggregation

**Expected Output:**
- Pricing transparency report
- Public value analysis
- Consumer guidance document

**Legal Basis:**
- Public records analysis
- Consumer protection research
- No system access required

---

### Category B: Cloud/Compute Providers

**Target Examples:**
- CoreWeave
- Lambda Labs
- Vast.ai

**Service Type:** Pricing vs. spot cost exposé (100% public data)

**Methodology:**
- Public API pricing analysis
- Spot H100 cost comparison
- Marketing claim verification
- Public benchmark analysis

**Expected Output:**
- Cost transparency report
- Marketing claim verification
- Consumer price comparison

**Legal Basis:**
- Public pricing data
- Publicly available benchmarks
- No proprietary data access

---

### Category C: Predatory Service Providers

**Target Examples:**
- Predatory landlords
- Predatory lenders
- Exploitative employers

**Service Type:** Victim intake-based investigation

**Methodology:**
- Victim interview (with consent)
- Public records research
- Court filing analysis
- Regulatory complaint aggregation

**Expected Output:**
- Evidence packet for legal action
- Regulatory complaint support
- Public awareness report

**Legal Basis:**
- Victim-authorized investigation
- Public records analysis
- Legal advocacy support

---

### Category D: Surveillance Technology Companies

**Target Examples:**
- Companies selling surveillance tech to abusive governments
- Spyware vendors
- Mass surveillance providers

**Service Type:** OSINT + coordinated vulnerability disclosure

**Methodology:**
- Public export records analysis
- Government contract research
- Open-source vulnerability research
- Coordinated disclosure to regulators

**Expected Output:**
- Export analysis report
- Vulnerability disclosure (coordinated)
- Policy recommendations

**Legal Basis:**
- Public trade data
- Coordinated disclosure protocols
- Policy research

---

## Case File Structure

### Initiation Command

To open a Client Zero case, submit the following to the DAO:

```yaml
case_initiation:
  command: "CLIENT ZERO"
  target: "[Target Name]"
  category: "[A/B/C/D]"
  services_requested:
    - "[Service ID from 1-100]"
    - "[Additional services as needed]"
  authorization:
    ethics_committee: "[pending/approved]"
    dao_vote: "[pending/approved]"
  lead_investigator: "[Assigned investigator]"
  timeline: "[Expected duration]"
  budget: "[DAO treasury allocation]"
```

### Case File Contents

Each active case file must contain:

1. **Case Summary**
   - Target identification
   - Service type(s) requested
   - Expected outcomes

2. **Legal Authorization**
   - Ethics committee approval
   - DAO vote record
   - Consent forms (if applicable)

3. **Methodology Documentation**
   - Data sources (all public)
   - Tools and techniques
   - Chain of custody for evidence

4. **Progress Logs**
   - Timestamped activity logs
   - SHA256 checksums
   - GPG signatures

5. **Deliverables**
   - Reports and findings
   - Evidence packets
   - Recommendations

---

## Ethics Committee Approval Process

### Pre-Approval Checklist

Before any case can proceed, the Ethics Committee must verify:

- [ ] Target selection criteria satisfied
- [ ] No disqualifying factors present
- [ ] Legal counsel consultation completed
- [ ] Methodology review passed
- [ ] Potential harm assessment conducted
- [ ] Public benefit documented

### Approval Workflow

```
Case Proposal → Ethics Committee Review → Legal Counsel Consultation
                                                   ↓
      DAO Vote ← Committee Recommendation ← Legal Clearance
         ↓
   Case Initiation (if approved)
```

### Ongoing Oversight

- Weekly progress reviews
- Immediate halt authority for ethical concerns
- Post-case impact assessment

---

## Operational Security

### Data Handling

- All data stored on air-gapped systems
- Evidence chain-of-custody maintained
- SHA256 checksums for all documents
- GPG signing for all official communications

### Communication Protocols

- Secure channels for victim communication
- Pseudonymization of vulnerable parties
- No public disclosure without consent

### Infrastructure

- 32TB/300+ RAM sovereign compute
- Air-gapped forensics environment
- RECON stack integration

---

## Case Closure

### Closure Requirements

A case can only be closed when:

1. All deliverables completed
2. Final report approved by Ethics Committee
3. Victim notification completed (if applicable)
4. DAO transparency report published
5. Lessons learned documented

### Post-Case Actions

- Impact assessment report
- Public transparency update (anonymized)
- Process improvement recommendations
- Archive with full audit trail

---

## Client Zero Shortlist

### Recommended First Targets

Based on maximum impact and minimal legal risk, the following are recommended Client Zero candidates:

| Priority | Target | Category | Service | Rationale |
|----------|--------|----------|---------|-----------|
| 1 | Harbor Compliance | A | #81 | Public pricing data, consumer impact |
| 2 | CoreWeave | B | #86 | Public claim verification, market transparency |
| 3 | Predatory lender (intake-based) | C | #34 | Victim advocacy, class-action support |
| 4 | Surveillance vendor | D | #84 | Human rights impact, regulatory disclosure |

### Decision Command

To select Client Zero, submit:

```
CLIENT ZERO: [Target Name]
Category: [A/B/C/D]
Primary Service: [Service #]
Secondary Services: [Additional service #s]
```

---

## Legal Disclaimer

This document describes operational protocols for services provided under NAICS 561611 licensing. All activities:

- Comply with applicable federal, state, and local laws
- Require proper authorization before initiation
- Are subject to DAO governance and ethics committee oversight
- Do not constitute legal advice

**Law is the weapon. No vigilante activities.**

---

*"Maximizing legal power to protect the vulnerable through transparent, ethical investigation."*

---

**Document Version**: 1.0  
**Generated**: 2025-11-25  
**Status**: Awaiting DAO Ethics Committee Activation
