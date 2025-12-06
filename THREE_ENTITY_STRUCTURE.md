# Three-Entity Legal Structure

**StrategicKhaos DAO LLC / ValorYield Engine**

> *Legal-compliant multi-entity structure for sustainable AI ecosystem operations*

---

## INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED

---

## Executive Summary

This document defines the three-entity structure that enables legal separation of nonprofit, for-profit, and governance functions while maintaining operational synergy.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     THREE-ENTITY STRUCTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        🏛️ ENTITY 1: NONPROFIT                        │   │
│  │                     ValorYield Engine 501(c)(3)                      │   │
│  │                                                                       │   │
│  │   Purpose: R&D, Education, Open-Source, Public Benefit               │   │
│  │   EIN: 39-2923503                                                    │   │
│  │   Tax Status: Tax-Exempt                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    │ IP License (Fair Market Value)         │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     💼 ENTITY 2: FOR-PROFIT                          │   │
│  │                  StrategicKhaos Commercial LLC                       │   │
│  │                                                                       │   │
│  │   Purpose: Commercialization, Consulting, Trading, Services          │   │
│  │   State: Wyoming (or C-Corp election)                                │   │
│  │   Tax Status: Pass-through or Corporate                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    │ Governance Protocol                    │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      ⚖️ ENTITY 3: DAO LLC                            │   │
│  │                      StrategicKhaos DAO LLC                          │   │
│  │                                                                       │   │
│  │   Purpose: Governance, IP Ownership, Protocol Management             │   │
│  │   Wyoming ID: 2025-001708194                                         │   │
│  │   Structure: Member-Managed DAO                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏛️ Entity 1: Nonprofit (ValorYield Engine)

### Legal Details

| Field | Value |
|-------|-------|
| **Legal Name** | ValorYield Engine |
| **Entity Type** | 501(c)(3) Nonprofit Corporation |
| **EIN** | 39-2923503 |
| **Tax Status** | Tax-Exempt |
| **State** | [To be confirmed] |

### Permitted Activities

Under IRS 501(c)(3) guidelines:

| Activity Category | Examples | IRS Requirement |
|-------------------|----------|-----------------|
| **Scientific Research** | AI safety, quantum computing, neural-symbolic systems | Public benefit |
| **Educational** | Intern training, curriculum development, workshops | Open to public |
| **Charitable** | Open-source software, public documentation | Community benefit |

### Investment Policy

Nonprofits ARE permitted to invest under IRS rules:

```yaml
investment_policy:
  permitted: true
  standards:
    - prudent_investor_rule: true
    - diversification_required: true
    - mission_alignment_preferred: true
  returns_usage:
    - mission_support: true
    - private_benefit: false
    - individual_distribution: false
  oversight:
    - board_approval: "Required for new investments"
    - annual_review: "Required"
    - audit_trail: "Maintained"
```

### Restrictions

| Prohibited Activity | Consequence |
|--------------------|-------------|
| Private Inurement | Loss of tax-exempt status |
| Political Campaigning | Loss of tax-exempt status |
| Substantial Lobbying | Penalties or loss of status |
| Unrelated Business Income (excessive) | UBIT taxation |

---

## 💼 Entity 2: For-Profit (Commercial LLC)

### Legal Details

| Field | Value |
|-------|-------|
| **Legal Name** | StrategicKhaos Commercial LLC |
| **Entity Type** | Limited Liability Company |
| **State** | Wyoming |
| **Tax Election** | Pass-through (default) or C-Corp (optional) |

### Business Activities

| Activity | Description | Revenue Model |
|----------|-------------|---------------|
| **AI Consulting** | Advisory services for enterprises | Hourly/Project |
| **Custom Development** | Private AI system builds | Contract |
| **Software Licensing** | Proprietary tool licenses | Subscription |
| **Managed Services** | Swarm node deployments | Service Fee |
| **Trading Operations** | NinjaTrader, equities, crypto | Investment Returns |
| **Infrastructure Services** | Cloud/edge computing | Hosting Fee |

### Relationship to Nonprofit

```yaml
nonprofit_relationship:
  type: "Arm's Length"
  transactions:
    ip_licensing:
      description: "License nonprofit-developed IP for commercial use"
      pricing: "Fair Market Value"
      documentation: "Required"
    service_agreements:
      description: "Contracted services between entities"
      pricing: "Market Rate"
      documentation: "Required"
  prohibited:
    - below_market_transactions: true
    - commingled_funds: true
    - shared_governance_without_separation: true
```

### Tax Considerations

| Scenario | Tax Treatment |
|----------|---------------|
| **Pass-through (default)** | Income flows to members |
| **C-Corp election** | Corporate taxation + dividend tax |
| **License fees to nonprofit** | Deductible business expense |

---

## ⚖️ Entity 3: DAO LLC (Governance)

### Legal Details

| Field | Value |
|-------|-------|
| **Legal Name** | StrategicKhaos DAO LLC |
| **Wyoming ID** | 2025-001708194 |
| **Structure** | Member-Managed |
| **State** | Wyoming |
| **Formation Date** | 2025-06-25 |

*Note: Formation date reflects the incorporation filing date per Wyoming Secretary of State records.*

### Purpose

The DAO LLC serves as the governance layer:

| Function | Description |
|----------|-------------|
| **IP Ownership** | Holds intellectual property rights |
| **Protocol Management** | Governs SwarmGate and ecosystem rules |
| **Token Governance** | (If applicable) Manages any governance tokens |
| **Cross-Entity Coordination** | Facilitates nonprofit/for-profit alignment |

### Wyoming DAO LLC Advantages

Wyoming SF0068 (2021) provides:

- Legal recognition of DAOs as LLCs
- Smart contract governance validity
- Limited liability for members
- Flexible management structures
- No requirement for centralized management

### Governance Structure

```yaml
governance:
  type: "Member-Managed DAO"
  voting_mechanisms:
    - proposal_submission: "Any member"
    - voting_period: "7 days default"
    - quorum: "51% of voting power"
    - passage: "Simple majority"
  roles:
    managing_member:
      name: "Domenic Garza"
      authority: "Day-to-day operations"
    board_nodes:
      - "Claude Prime (Verification)"
      - "Grok 4.1 (Boundary Enforcement)"
      - "GPT-5.1 (Compliance Analysis)"
  amendments:
    operating_agreement: "2/3 majority"
    fundamental_changes: "Unanimous consent"
```

---

## 🔄 Inter-Entity Relationships

### Flow of Value

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INTER-ENTITY VALUE FLOWS                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     NONPROFIT                FOR-PROFIT               DAO LLC               │
│  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐         │
│  │ ValorYield  │          │ Commercial  │          │ StrategicK  │         │
│  │   Engine    │          │    LLC      │          │  haos DAO   │         │
│  └─────────────┘          └─────────────┘          └─────────────┘         │
│        │                        │                        │                  │
│        │                        │                        │                  │
│        ├────── IP License ──────►                        │                  │
│        │      (Fair Market)     │                        │                  │
│        │                        │                        │                  │
│        ◄─── License Fees ───────┤                        │                  │
│        │     (Deductible)       │                        │                  │
│        │                        │                        │                  │
│        │                        ├─── Governance ────────►│                  │
│        │                        │     Protocol           │                  │
│        │                        │                        │                  │
│        ├──────────────────────── IP Rights ─────────────►│                  │
│        │                        │                        │                  │
│        │                        │                        │                  │
│        ◄────────── Mission Alignment Coordination ───────►                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Required Documentation

| Transaction Type | Documentation Required |
|------------------|------------------------|
| **IP Licensing** | Written license agreement, valuation basis |
| **Service Contracts** | Service agreement, fair market rate justification |
| **Governance Decisions** | Board minutes, voting records |
| **Fund Transfers** | Purpose documentation, board approval |

---

## 📋 Compliance Checklist

### Nonprofit Compliance

- [ ] Annual Form 990 filing
- [ ] State registration maintenance
- [ ] Board meeting minutes
- [ ] Conflict of interest policy enforcement
- [ ] Investment policy adherence
- [ ] Public disclosure compliance

### For-Profit Compliance

- [ ] Annual report filing (Wyoming)
- [ ] Tax return filing
- [ ] Operating agreement updates
- [ ] Member meeting records
- [ ] Financial record keeping

### DAO LLC Compliance

- [ ] Wyoming annual report
- [ ] Smart contract audits (if applicable)
- [ ] Governance record keeping
- [ ] Member voting documentation
- [ ] Operating agreement compliance

---

## ⚠️ Risk Mitigation

### Private Inurement Prevention

```yaml
private_inurement_controls:
  salary_caps:
    benchmark: "Comparable nonprofit salaries"
    documentation: "Annual review required"
  transaction_review:
    threshold: "$50,000"
    approval: "Board approval required"
  conflict_of_interest:
    policy: "Written policy required"
    disclosure: "Annual disclosure forms"
    recusal: "Required for conflicted decisions"
```

### Arm's Length Transaction Requirements

| Requirement | Implementation |
|-------------|----------------|
| **Fair Market Value** | Independent valuation or comparable pricing |
| **Written Agreements** | All transactions documented |
| **Board Approval** | Material transactions require board vote |
| **No Self-Dealing** | Conflicted parties must recuse |

---

## 📚 Legal References

### Wyoming DAO LLC Law

- **SF0068 (2021)**: Wyoming DAO LLC Recognition Act
- **W.S. 17-31-101 et seq.**: Wyoming DAO Company Act

### IRS Nonprofit Rules

- **IRC 501(c)(3)**: Tax-exempt organization requirements
- **IRC 4958**: Excess benefit transaction rules
- **Form 990**: Annual information return

### Relevant Case Law

- *Helvering v. Horst* - Investment income treatment
- *Bob Jones University v. United States* - Public policy compliance

---

## 🚀 Next Steps

### Immediate Actions

1. [ ] Engage Wyoming-licensed attorney for review
2. [ ] Confirm ValorYield Engine 501(c)(3) status details
3. [ ] Draft IP licensing agreement template
4. [ ] Create inter-entity service agreement templates
5. [ ] Establish conflict of interest policy

### Ongoing Requirements

1. [ ] Quarterly inter-entity transaction review
2. [ ] Annual compliance audit
3. [ ] Board minutes for all entity decisions
4. [ ] Tax return coordination

---

**Document Status:** DRAFT  
**Requires:** Attorney Review  
**Classification:** Internal Legal Framework

*This document contains internal drafts only and does not constitute legal advice.*
