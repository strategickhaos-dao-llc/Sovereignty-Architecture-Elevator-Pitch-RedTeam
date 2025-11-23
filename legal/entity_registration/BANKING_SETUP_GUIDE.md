# Banking Setup Guide
**Multi-Jurisdiction Nonprofit Entity and Banking Structure**

> **INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED**
> 
> This guide outlines the process for establishing nonprofit entities in Wyoming, New Mexico, and Estonia with dedicated banking infrastructure.

## Overview

Separating personal and nonprofit finances is critical for:
- **Legal Protection**: Clear separation limits personal liability
- **Tax Compliance**: Required for 501(c)(3) status and IRS reporting
- **Credibility**: Demonstrates professionalism to donors and partners
- **Audit Trail**: Essential for financial transparency and accountability

**Deadline**: All entities registered and banks operational within 10 days  
**Fund Transfer**: Complete within 72-hour window (Days 8-10)

---

## Multi-Jurisdiction Strategy

### Why Multiple Jurisdictions?

| Jurisdiction | Primary Benefit | Use Case |
|--------------|----------------|----------|
| **Wyoming** | Strong legal protections, DAO-friendly | Primary 501(c)(3), main operations |
| **New Mexico** | Privacy protections, business-friendly | Secondary entity, diversification |
| **Estonia** | E-residency, digital infrastructure | International operations, crypto-friendly |

### Entity Structure

```yaml
entity_hierarchy:
  primary:
    name: "Strategickhaos DAO LLC"
    jurisdiction: Wyoming
    type: 501(c)(3) Nonprofit Corporation
    purpose: Primary operations, treasury, governance
    
  secondary:
    name: "Strategickhaos New Mexico Foundation"
    jurisdiction: New Mexico
    type: Nonprofit Corporation
    purpose: Backup operations, grant-making
    
  international:
    name: "Strategickhaos OÜ"
    jurisdiction: Estonia
    type: Private Limited Company (nonprofit structure)
    purpose: International operations, EU presence
```

---

## Wyoming Entity Registration

### Requirements

```yaml
wyoming_nonprofit:
  entity_type: Nonprofit Corporation (501c3)
  
  required_documents:
    - Articles of Incorporation
    - Bylaws
    - Initial Board Resolution
    - Registered Agent designation
    
  costs:
    filing_fee: $100
    registered_agent: $50-150/year
    attorney_review: $500-2000
    
  timeline: 5-10 business days for approval
```

### Step-by-Step Process

#### Day 1: Document Preparation

```markdown
## Articles of Incorporation Checklist

- [ ] Corporate name: "Strategickhaos DAO LLC" (check availability)
- [ ] Purpose clause (charitable, educational, scientific)
- [ ] Dissolution clause (assets to similar 501c3)
- [ ] No private benefit clause
- [ ] Board size and initial directors
- [ ] Registered agent name and address
- [ ] Incorporator signature

Reference: Wyoming Statute §17-19-202
```

**Sample Purpose Clause**:
```
The corporation is organized exclusively for charitable, educational, and 
scientific purposes within the meaning of Section 501(c)(3) of the Internal 
Revenue Code, specifically to:

1. Advance open-source software development and decentralized technologies
2. Provide educational resources on digital sovereignty and self-governance
3. Support research into distributed systems and autonomous organizations
4. Foster community-driven innovation in software and organizational design
```

#### Day 2: File with Wyoming Secretary of State

```bash
# Online filing: https://wyobiz.wyo.gov/business/fileonline.aspx
# Or by mail: Herschler Building East, 122 W 25th St, Cheyenne, WY 82002

# Required information:
ENTITY_NAME="Strategickhaos DAO LLC"
REGISTERED_AGENT="Wyoming Registered Agent Service"
AGENT_ADDRESS="123 Main St, Cheyenne, WY 82001"

# Filing fee: $100 (check or credit card)
```

#### Day 3-5: Await Approval

- Monitor email for approval confirmation
- Receive Certificate of Incorporation
- File copy in corporate records

#### Day 6: Obtain EIN

```bash
# Apply online: https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online

# SS-4 Form information needed:
# - Legal name of entity
# - Trade name (if different)
# - Mailing address
# - Responsible party (name, SSN)
# - Business type: 501(c)(3) nonprofit
# - Reason for applying: Started new business
# - Date business started
# - Accounting year end: December 31

# Approval: Immediate online
```

### Wyoming Bank Account Setup

#### Day 7: Select Bank

**Recommended Banks**:
1. **Wyoming Bank & Trust**: Local, understands LLCs and nonprofits
2. **Mercury**: Tech-friendly, online banking, no physical branch needed
3. **Relay**: Designed for startups and nonprofits, good online features

#### Day 7-8: Open Account

```yaml
required_documents:
  - Certificate of Incorporation
  - EIN confirmation letter
  - Articles of Incorporation
  - Bylaws
  - Board resolution authorizing bank account
  - ID for authorized signers (founder)
  - Initial deposit: $1,000 minimum
```

**Board Resolution Template**:
```
RESOLUTION OF THE BOARD OF DIRECTORS
Strategickhaos DAO LLC

RESOLVED, that the corporation establish a bank account with [Bank Name], 
and that [Founder Name], as President, is authorized to:
- Open and close bank accounts
- Make deposits and withdrawals
- Sign checks and authorize electronic transfers
- Obtain debit cards and online banking access

Adopted this [Date] by the Board of Directors.
```

---

## New Mexico Entity Registration

### Requirements

```yaml
new_mexico_nonprofit:
  entity_type: Nonprofit Corporation
  
  required_documents:
    - Articles of Incorporation (Form RA)
    - Registered Agent acceptance
    - Initial Report (within 15 days)
    
  costs:
    filing_fee: $25
    registered_agent: $50-125/year
    
  timeline: 3-7 business days
```

### Filing Process

```bash
# Online portal: https://portal.sos.state.nm.us/BFS/online/Account/Login

# File Articles of Incorporation
# Entity name: "Strategickhaos New Mexico Foundation"
# Purpose: Same charitable purposes as Wyoming entity
# Registered agent: NM-based service

# Filing fee: $25 (credit card)
```

### New Mexico Bank Account

**Recommended**: Ally Bank (online, no physical branch, nonprofit-friendly)

```yaml
account_setup:
  - Open online at ally.com
  - Upload incorporation documents
  - Provide EIN from New Mexico entity
  - Initial deposit: $500
  - Set up online banking and ACH
```

---

## Estonia E-Residency & Entity

### E-Residency Application

#### Day 1-30: Apply for E-Residency

```bash
# Apply online: https://apply.e-resident.gov.ee

# Required information:
# - Personal details and passport
# - Photo
# - Reason for application: "Establishing digital business"
# - Processing time: 4-8 weeks
# - Cost: €100 (application) + €30 (pickup)

# Note: This is the longest part - begin immediately
```

#### After E-Residency Approval: Company Formation

```yaml
estonian_entity:
  company_type: Osaühing (OÜ) - Private Limited Company
  minimum_capital: €2,500
  
  formation_options:
    option_1: 
      service: LeapIN (e-Residency recommended)
      cost: €200-300
      timeline: 1-3 days
      
    option_2:
      service: 1Office
      cost: €150-250
      timeline: 1-2 days
      
  ongoing_costs:
    accounting: €50-100/month
    registered_address: €30-50/month
    annual_report: €200-300/year
```

### Estonian Bank Account

**Challenge**: Estonian banks require physical presence or substantial business.

**Solutions**:
1. **Wise Business** (formerly TransferWise):
   ```yaml
   - Multi-currency account
   - No physical presence needed
   - E-residency digital ID sufficient
   - IBAN for SEPA transfers
   - Cost: Free account, per-transaction fees
   ```

2. **LHV Bank** (via e-residency):
   ```yaml
   - Estonian bank with e-resident program
   - Requires video call verification
   - Full banking services
   - Cost: €5-10/month
   ```

3. **Payoneer**:
   ```yaml
   - Business account for e-residents
   - Multi-currency support
   - Easy setup process
   - Cost: Free account, withdrawal fees
   ```

---

## 72-Hour Fund Transfer Plan

### Pre-Transfer Preparation (Days 1-7)

```yaml
preparation_checklist:
  - [ ] All three entities registered and approved
  - [ ] All bank accounts opened and verified
  - [ ] Online banking access configured
  - [ ] Transfer limits verified with banks
  - [ ] Documentation of personal funds to transfer
  - [ ] Accounting software ready (QuickBooks, Xero)
  - [ ] Board resolutions authorizing fund transfers
```

### Hour 0-24: Verification Phase

```bash
#!/bin/bash
# verify-accounts.sh - Verify all accounts are operational

# Test Wyoming account
echo "Testing Wyoming account..."
# Small test transfer ($1) to verify routing
# Verify online banking access
# Confirm debit card active

# Test New Mexico account
echo "Testing New Mexico account..."
# Small test transfer ($1)
# Verify online banking
# Confirm ACH setup

# Test Estonian account
echo "Testing Estonian account..."
# Verify IBAN details
# Test small SEPA transfer (€1)
# Confirm multi-currency access

echo "All accounts verified and operational"
```

### Hour 24-48: Main Transfer

```yaml
transfer_sequence:
  step_1:
    from: Personal checking account
    to: Wyoming nonprofit account
    amount: $XX,XXX (primary funds)
    method: ACH transfer
    notes: "Initial operating capital"
    documentation: "Receipt and bank confirmation"
    
  step_2:
    from: Personal savings account
    to: New Mexico foundation account
    amount: $X,XXX (reserve funds)
    method: ACH transfer
    notes: "Reserve fund allocation"
    
  step_3:
    from: Personal account (USD)
    to: Estonian Wise account (EUR)
    amount: €X,XXX (international operations)
    method: Wire transfer
    notes: "International operations fund"
    
  step_4:
    from: Personal crypto wallet
    to: Organizational Gnosis Safe
    amount: X.XX ETH + tokens
    method: Blockchain transfer
    notes: "Treasury diversification"
```

**Transfer Tracking Sheet**:
```csv
Timestamp,From,To,Amount,Method,Confirmation,Status
2025-11-24 08:00,Personal-Checking,WY-Nonprofit,$50000,ACH,#ABC123,Pending
2025-11-24 08:15,Personal-Savings,NM-Foundation,$10000,ACH,#DEF456,Pending
2025-11-24 09:00,Personal-USD,EE-Wise,€5000,Wire,#GHI789,Pending
2025-11-24 10:00,Personal-Wallet,Gnosis-Safe,2.5 ETH,Blockchain,0xjkl012,Confirmed
```

### Hour 48-72: Reconciliation

```yaml
reconciliation_tasks:
  - [ ] Verify all transfers completed successfully
  - [ ] Confirm balances match expected amounts
  - [ ] Document all transfers in accounting system
  - [ ] Generate initial financial statements
  - [ ] File copies of all confirmations
  - [ ] Update board with transfer completion
  - [ ] Close or zero-out personal accounts used for nonprofit
```

---

## Post-Transfer Setup

### Payment Processor Updates

```yaml
update_payment_accounts:
  stripe:
    - Log into Stripe Dashboard
    - Update bank account to nonprofit account
    - Change business name and EIN
    - Upload nonprofit documentation
    
  paypal:
    - Convert to Business/Nonprofit account
    - Update bank account
    - Provide 501(c)(3) determination letter (when received)
    
  github_sponsors:
    - Update payout account
    - Change to nonprofit entity name
    
  other:
    - Update any subscription payments
    - Notify regular payees of new account info
```

### Vendor Notifications

```markdown
Subject: Bank Account Update - Strategickhaos DAO LLC

Dear [Vendor Name],

This email is to inform you that Strategickhaos DAO LLC has established 
dedicated nonprofit bank accounts. Please update your records:

**Old Account**: [Personal account - being closed]
**New Account**: 
  Bank: Wyoming Bank & Trust
  Account: [Account Number]
  Routing: [Routing Number]
  
All future payments should be directed to the new account effective 
[Date]. The old account will be closed on [Date + 30 days].

If you have any questions, please contact us at finance@strategickhaos.org.

Thank you for your partnership.

Best regards,
Domenic Garza
Founder, Strategickhaos DAO LLC
```

---

## Ongoing Compliance

### Monthly Reconciliation

```yaml
monthly_tasks:
  week_1:
    - [ ] Reconcile all bank accounts with accounting software
    - [ ] Review all transactions for proper categorization
    - [ ] Generate bank reconciliation reports
    
  week_2:
    - [ ] Review credit card statements (if applicable)
    - [ ] Categorize all expenses by program/fundraising/admin
    - [ ] Check for any fraudulent or unauthorized transactions
    
  week_3:
    - [ ] Generate monthly financial statements
    - [ ] Review cash flow and budget vs. actual
    - [ ] Identify any budget variances
    
  week_4:
    - [ ] Board treasurer review and approval
    - [ ] File monthly reports in financial records
    - [ ] Plan for upcoming expenses
```

### Annual Requirements

```yaml
annual_compliance:
  wyoming:
    - Annual Report to Secretary of State ($50-100)
    - CPA review of financial statements
    - Board approval of annual budget
    
  new_mexico:
    - Annual Report to Secretary of State ($25)
    - Update registered agent if needed
    
  estonia:
    - Annual Report to Commercial Register
    - Tax declaration (even if no tax owed)
    - Accounting firm annual review
    
  irs:
    - Form 990 (annual information return)
    - Form 1023 (501c3 application - one time)
    - State charitable registration renewals
```

---

## Security & Fraud Prevention

### Account Security Measures

```yaml
security_controls:
  access_control:
    - Minimum two authorized signers (founder + core team)
    - Dual approval for transactions >$1,000
    - Hardware security keys for online banking
    - Strong unique passwords + password manager
    
  monitoring:
    - Daily balance checks
    - Real-time transaction alerts via SMS/email
    - Monthly review of all statements
    - Quarterly external review by CPA
    
  fraud_prevention:
    - Never share login credentials
    - Beware of phishing emails
    - Verify all payment requests out-of-band
    - Use whitelisted ACH recipients only
```

### Incident Response

```yaml
fraud_response_plan:
  unauthorized_transaction:
    - Immediately contact bank fraud department
    - File police report
    - Notify board within 24 hours
    - Document incident thoroughly
    - Review and update security measures
    
  account_compromise:
    - Freeze account immediately
    - Change all passwords and security questions
    - Review all recent transactions
    - File insurance claim (if applicable)
    - Engage cybersecurity firm for investigation
```

---

## Success Metrics

### Implementation Success (Days 1-10)

- [ ] Wyoming entity registered and EIN obtained
- [ ] New Mexico entity registered and EIN obtained
- [ ] Estonia e-residency approved (or in process)
- [ ] All bank accounts opened and operational
- [ ] 72-hour fund transfer completed successfully
- [ ] Zero commingling of personal and nonprofit funds
- [ ] All payment processors updated

### Ongoing Health

- [ ] 100% of transactions through nonprofit accounts
- [ ] Monthly reconciliations completed on time
- [ ] Zero fraud or unauthorized transactions
- [ ] Annual reports filed on time in all jurisdictions
- [ ] Clean audit findings

---

## Costs Summary

```yaml
one_time_costs:
  wyoming_formation: $100-2500
  new_mexico_formation: $25-1000
  estonia_e_residency: €130
  estonia_company_formation: €200-300
  legal_review: $1000-3000
  accounting_setup: $500-1000
  total_estimate: $2,500-7,930

annual_costs:
  wyoming_annual_report: $50-100
  wyoming_registered_agent: $50-150
  new_mexico_annual_report: $25
  new_mexico_registered_agent: $50-125
  estonia_accounting: €600-1200
  estonia_registered_address: €360-600
  bank_account_fees: $0-500
  total_annual: $1,500-3,000
```

---

## Resources

### Wyoming
- Secretary of State: https://sos.wyo.gov
- Online Filing: https://wyobiz.wyo.gov
- Statutes: https://wyoleg.gov

### New Mexico
- Secretary of State: https://www.sos.state.nm.us
- Business Services: https://portal.sos.state.nm.us

### Estonia
- E-Residency: https://e-resident.gov.ee
- Company Formation: https://www.leapin.eu
- Business Register: https://ariregister.rik.ee

---

## Document Control

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Implementation Ready |
| Owner | Strategickhaos DAO LLC |
| Legal Review | Required |
| Created | 2025-11-23 |
| Next Review | Monthly |

---

*© 2025 Strategickhaos DAO LLC. Internal use only.*
