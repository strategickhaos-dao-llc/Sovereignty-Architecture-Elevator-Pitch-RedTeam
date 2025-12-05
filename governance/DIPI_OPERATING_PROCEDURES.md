# DIPI Operating Procedures
# Department of Intellectual Property Intelligence
## Strategickhaos DAO LLC — Operational Guidelines

**Document Version:** 1.0  
**Effective Date:** 2025-12-05  
**Classification:** Operational – Non-Legal  
**Status:** Active

---

## ⚠️ CRITICAL DISCLAIMER

> **DIPI is NOT a legal department.**  
> This department CANNOT provide legal advice, interpret law, or make legal determinations.  
> All activities are operational, administrative, and preparatory in nature.  
> All filings, enforcement actions, and legal conclusions require a licensed attorney.

---

## 1. Purpose & Scope

The Department of Intellectual Property Intelligence (DIPI, pronounced "Dippy") is responsible for:

- **Monitoring** intellectual property usage and potential conflicts
- **Documenting** first-use evidence and provenance records
- **Preparing** filing packets and evidence packages
- **Alerting** stakeholders to potential IP concerns
- **Supporting** outside counsel with organized, timestamped documentation

### What DIPI CAN Do

| Activity | Description | Output |
|----------|-------------|--------|
| Trademark Scanning | Monitor USPTO TESS for similar marks | Alert reports |
| Evidence Collection | Archive screenshots, commits, pages | Timestamped folders |
| Filing Preparation | Prepare ITU packets | Checklist + specimens |
| Prior Art Research | Collect prior art for patent prep | Research packets |
| Nonprofit IP Tracking | Track IP for 7% charity compliance | Compliance reports |

### What DIPI CANNOT Do

| Prohibited Activity | Reason |
|---------------------|--------|
| Interpret trademark law | Requires licensed attorney |
| Claim statutory damages | Legal determination |
| Assert priority rights | Legal conclusion |
| Send C&D letters | Legal enforcement |
| File as an attorney | UPL violation |
| Draft legal agreements | Requires counsel |

---

## 2. Standard Operating Procedures

### 2.1 Daily Trademark Monitoring

**Frequency:** Daily (automated)  
**Responsible:** DIPI Automation System

1. **Query USPTO TESS** for marks similar to Strategickhaos portfolio
2. **Compare results** against registered and pending marks
3. **Score similarity** using defined criteria
4. **Generate alert** if similarity score exceeds threshold
5. **Log all queries** in monitoring audit trail
6. **Weekly summary** to Board and counsel

**Output:** `trademark_monitoring_report_YYYY-MM-DD.yaml`

### 2.2 Intent-To-Use Filing Preparation

**Trigger:** New brand/mark identified for protection  
**Responsible:** DIPI Operator

#### Preparation Checklist

- [ ] Mark name clearly documented
- [ ] International classes identified
- [ ] Goods/services descriptions drafted
- [ ] Specimens of use collected
- [ ] Evidence of first use documented
- [ ] USPTO search completed
- [ ] Conflict analysis prepared
- [ ] Filing checklist reviewed

**Output:** Complete ITU packet for attorney review

**IMPORTANT:** Actual filing must be performed by:
- Managing Member (self-filing), OR
- Licensed trademark attorney

### 2.3 First-Use Evidence Documentation

**Trigger:** Product launch, brand first use, or significant release  
**Responsible:** DIPI Operator

#### Documentation Steps

1. **Create timestamped commit**
   ```bash
   git add -A
   git commit -m "DIPI: First-use documentation for [MARK_NAME]"
   git log --format="%H %ci" -1 >> provenance/first_use_log.txt
   ```

2. **Capture website screenshots**
   - Full page capture
   - Include URL bar showing domain
   - Include timestamp in filename

3. **Archive product pages**
   - Save HTML source
   - Save rendered screenshots
   - Capture any pricing/availability info

4. **Generate SHA256 hash**
   ```bash
   sha256sum evidence/* >> provenance/hashes_YYYY-MM-DD.txt
   ```

5. **Create provenance record**
   - Fill `proof_of_non_hallucination_template.yaml`
   - Include all evidence references
   - Log in IP provenance folder

**Output:** Complete first-use evidence package in `ip_provenance/[MARK_NAME]/`

### 2.4 Patent Research Preparation

**Trigger:** Novel invention or feature identified  
**Responsible:** DIPI Operator

#### Invention Disclosure Process

1. **Document the invention**
   - Use `invention_disclosure_template.yaml`
   - Include technical description
   - Document problem solved
   - List novel aspects

2. **Collect prior art**
   - Search USPTO patent database
   - Search Google Patents
   - Search academic literature
   - Document all findings

3. **Create timeline**
   - Date of conception
   - Date of first disclosure
   - Date of first implementation
   - Witnesses/corroborators

4. **Prepare packet for patent counsel**
   - Invention disclosure form
   - Prior art summary
   - Timeline documentation
   - Technical drawings/diagrams

**Output:** Complete invention disclosure packet

### 2.5 NFT Evidence Anchoring (Optional)

**Trigger:** High-value IP requiring additional evidence  
**Responsible:** DIPI Operator

> **NOTE:** NFT anchoring is evidence of creation date ONLY.  
> It is NOT legally binding and does NOT establish legal rights.

#### Anchoring Process

1. **Generate hash** of evidence package
2. **Create metadata** including:
   - Hash value
   - Creation timestamp
   - Description of contents
   - Strategickhaos identifier
3. **Mint to designated chain**
4. **Record transaction ID** in provenance folder
5. **Include disclaimer** that this is evidence, not legal proof

### 2.6 Nonprofit IP Compliance

**Frequency:** Quarterly  
**Responsible:** DIPI Operator + Nonprofit Counsel

#### Compliance Tasks

- [ ] Track which IP belongs to nonprofit entity
- [ ] Log donations and allocations
- [ ] Classify revenue as UBIT vs non-UBIT
- [ ] Document compliance status
- [ ] Prepare Form 990 notes
- [ ] Generate quarterly report

**Output:** `nonprofit_ip_compliance_Q[N]_YYYY.yaml`

---

## 3. Alert Escalation Procedures

### Severity Levels

| Level | Description | Response Time | Escalation |
|-------|-------------|---------------|------------|
| 🟢 Low | Similar mark in different class | 7 days | Weekly report |
| 🟡 Medium | Similar mark in related class | 48 hours | Board + counsel alert |
| 🔴 High | Confusingly similar mark | 24 hours | Immediate counsel contact |
| ⚫ Critical | Direct infringement detected | Immediate | Emergency counsel contact |

### Escalation Path

1. **DIPI Automation** detects potential issue
2. **DIPI Operator** reviews and confirms severity
3. **Board notification** via designated channel
4. **Counsel notification** with prepared documentation
5. **Attorney determines** legal response

---

## 4. Documentation Standards

### Folder Structure

```
ip_provenance/
├── trademarks/
│   ├── [MARK_NAME]/
│   │   ├── first_use_evidence/
│   │   ├── specimens/
│   │   ├── filing_preparation/
│   │   └── monitoring_alerts/
│   └── monitoring_reports/
├── patents/
│   ├── [INVENTION_NAME]/
│   │   ├── disclosure/
│   │   ├── prior_art/
│   │   └── timeline/
│   └── research_notes/
├── copyrights/
│   ├── code/
│   ├── documentation/
│   └── registrations/
└── nonprofit_compliance/
    ├── quarterly_reports/
    └── ip_allocations/
```

### File Naming Convention

```
[TYPE]_[MARKNAME]_[YYYY-MM-DD]_[VERSION].[ext]

Examples:
- specimen_strategickhaos_2025-12-05_v1.png
- first_use_log_valoryield_2025-12-05_v1.yaml
- monitoring_report_2025-12-05.yaml
```

### Required Metadata

Every DIPI document must include:
- Creation timestamp
- Creator identifier
- SHA256 hash
- Version number
- Classification (Operational – Non-Legal)

---

## 5. Audit Trail Requirements

All DIPI activities must be logged with:

- **Timestamp** (ISO 8601 format)
- **Actor** (operator or automation system)
- **Action** (what was done)
- **Target** (IP asset affected)
- **Output** (files created/modified)
- **Hash** (SHA256 of outputs)

### Audit Log Format

```yaml
audit_entry:
  timestamp: "2025-12-05T23:40:00Z"
  actor: "dipi-ops"
  action: "trademark_monitoring_scan"
  target: "strategickhaos-portfolio"
  output:
    - "monitoring_report_2025-12-05.yaml"
  hash: "sha256:abc123..."
  notes: "Weekly automated scan - no conflicts detected"
```

---

## 6. Integration with Governance

DIPI operates within the existing Strategickhaos governance framework:

- **Reports to:** Founder & Board
- **Access Matrix:** See `governance/access_matrix.yaml`
- **Charter:** See `governance/dipi_charter.yaml`
- **External Coordination:** IP Counsel, Tax Counsel, Nonprofit Counsel

### Approval Workflow

1. DIPI prepares documentation
2. DIPI operator reviews completeness
3. Board reviews strategic decisions
4. Attorney reviews legal aspects
5. Authorized signer executes (if filing)

---

## 7. Contacts & Resources

### Internal

- **DIPI Operations:** dipi-ops@strategickhaos.internal
- **Board Alerts:** board@strategickhaos.internal
- **Audit Trail:** dipi-audit@strategickhaos.internal

### External Resources

- **USPTO TESS:** https://tmsearch.uspto.gov/
- **USPTO Patent Search:** https://www.uspto.gov/patents/search
- **Google Patents:** https://patents.google.com/

### Emergency Contacts

- **IP Counsel:** [Designated Attorney]
- **Managing Member:** Domenic Garza

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-05 | DIPI | Initial operating procedures |

---

*"Preparing everything before the lawyer — staying safe and compliant."*

**Department of Intellectual Property Intelligence (DIPI)**  
Strategickhaos DAO LLC
