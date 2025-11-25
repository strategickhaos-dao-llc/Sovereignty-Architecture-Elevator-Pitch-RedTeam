# USPTO Provisional Patent Filing Guide

**Strategickhaos DAO LLC / Valoryield Engine**

This guide documents the process for filing provisional patent applications with the United States Patent and Trademark Office (USPTO) as a micro-entity.

## Overview

Provisional patent applications provide:
- **12-month "patent pending" status** from filing date
- **Priority date** for subsequent non-provisional filings
- **Lower filing fees** ($75 for micro-entities)
- **No formal claims required** (but recommended for clarity)

## Pre-Filing Checklist

### 1. Micro-Entity Eligibility Verification

To qualify as a micro-entity (37 CFR 1.29), you must:

- [ ] Not have been named as inventor on more than four previously filed patent applications
- [ ] Not have a gross income exceeding 3x the median household income
- [ ] Not have assigned/licensed rights to an entity exceeding the gross income limit
- [ ] Complete Form PTO/SB/15A (Micro Entity Certification)

### 2. Required Documents

- [ ] **Specification document** (description of invention)
- [ ] **Drawings** (if applicable to understanding the invention)
- [ ] **Cover sheet** (Form PTO/SB/16)
- [ ] **Micro-entity certification** (Form PTO/SB/15A)
- [ ] **Application Data Sheet** (Form PTO/AIA/14)

### 3. GPG-Signed Evidence Documents

For prior art protection and proof of conception, ensure these are GPG-signed before filing:

- [ ] Research documentation
- [ ] Company/entity verification (e.g., Bizapedia records)
- [ ] Technical specifications
- [ ] Timestamp proofs (OpenTimestamps/Bitcoin anchored)

## Filing Process

### Step 1: Prepare Account

1. Navigate to [USPTO.gov](https://www.uspto.gov)
2. Log in with your registered email (e.g., domenic.garza@snhu.edu)
3. Access **Patent Center** or **EFS-Web**

### Step 2: Create New Application

1. Select "Provisional Application for Patent"
2. Upload specification PDF
3. Complete cover sheet information
4. Submit micro-entity certification

### Step 3: Payment

| Entity Type | Filing Fee |
|-------------|------------|
| Large Entity | $320 |
| Small Entity | $160 |
| **Micro Entity** | **$75** |

Payment methods: Credit card, deposit account, or EFT

### Step 4: Confirmation

Upon successful submission:
- Receive **Application Number** (format: 63/XXXXXX for provisionals)
- Download filing receipt
- Mark all materials as "Patent Pending"

## Post-Filing Requirements

### Within 12 Months

You must file a non-provisional application claiming priority to the provisional, or the provisional expires without patent rights.

### Documentation Best Practices

1. **GPG Sign** all correspondence and amendments
2. **Timestamp** revisions using OpenTimestamps
3. **Maintain chain of custody** via Git commit history
4. **Store securely** in encrypted repository/backup

## Integration with Strategickhaos Infrastructure

### Automated Timestamping

The repository includes workflows for:
- Bitcoin-anchored OpenTimestamps on commits
- GPG signature verification via `hooks/require_gpg.sh`
- Hash-chained audit trails

### DAO Governance

Patent-related decisions follow the governance framework:
- `governance/` - Ethics committee oversight
- `dao_record.yaml` - Entity structure and compliance

## Legal Disclaimer

This guide is for informational purposes only and does not constitute legal advice. Consult a registered patent attorney or agent for specific legal guidance on patent applications.

---

**Contact**: domenic.garza@snhu.edu  
**Entity**: Strategickhaos DAO LLC  
**ORCID**: 0009-0005-2996-3526

*Document generated for USPTO provisional patent filing preparation.*
