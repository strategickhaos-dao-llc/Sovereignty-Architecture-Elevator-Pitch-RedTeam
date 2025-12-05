# Royalty Management Guide
## NinjaTrader Dividends and Technology Licensing

This document provides specific guidance for managing royalty income from NinjaTrader dividends and other technology licensing arrangements for the nonprofit organization.

## Table of Contents
1. [Royalty Agreement Management](#royalty-agreement-management)
2. [Payment Processing and Tracking](#payment-processing-and-tracking)
3. [Legal Framework for Royalties](#legal-framework-for-royalties)
4. [Tax Considerations](#tax-considerations)
5. [Risk Management](#risk-management)
6. [Reporting and Transparency](#reporting-and-transparency)

---

## Royalty Agreement Management

### NinjaTrader Dividend Agreement Structure

#### Essential Agreement Components
```yaml
royalty_agreement:
  parties:
    licensor: "Technology Creator/Developer"
    licensee: "NinjaTrader or equivalent platform"
    beneficiary: "Strategickhaos DAO LLC / Valoryield Engine"
    
  key_terms:
    royalty_rate:
      percentage: "To be negotiated"
      calculation_basis: "Net revenue, gross revenue, or per-transaction"
      
    payment_schedule:
      frequency: "Monthly, Quarterly, or Annual"
      payment_date: "Specific date each period"
      grace_period: "15 days"
      late_payment_penalty: "X% per month"
      
    minimum_guarantee:
      amount: "$X per period"
      purpose: "Ensures baseline revenue stream"
      
    audit_rights:
      frequency: "Annual"
      notice_period: "30 days"
      cost_allocation: "Per agreement terms"
      
    term_and_renewal:
      initial_term: "X years"
      renewal_options: "Automatic or negotiated"
      termination_notice: "X days/months"
```

### Agreement Lifecycle Management

#### Pre-Execution Phase
```markdown
## Due Diligence Checklist

### Legal Review
- [ ] Agreement reviewed by qualified IP attorney
- [ ] Nonprofit counsel reviews tax and charitable implications
- [ ] All terms clearly defined and understood
- [ ] Payment calculations independently verified
- [ ] Termination provisions reviewed and acceptable

### Financial Analysis
- [ ] Revenue projections modeled (conservative, expected, optimistic)
- [ ] Payment schedule assessed for cash flow impact
- [ ] Tax implications analyzed
- [ ] Accounting treatment determined
- [ ] Budget impact assessed

### Risk Assessment
- [ ] Counterparty financial stability verified
- [ ] Market risk for underlying product evaluated
- [ ] Legal risks identified and mitigation planned
- [ ] Dependency risk assessed (is this >40% of revenue?)
- [ ] Exit strategy defined
```

#### Execution Phase
```yaml
execution_checklist:
  documentation:
    - "Fully executed agreement (all parties signed)"
    - "Board resolution authorizing agreement"
    - "W-9 or tax forms exchanged"
    - "Banking information for payment processing"
    - "Contact information for all parties"
    
  internal_setup:
    - "Dedicated royalty receiving account confirmed"
    - "Accounting system configured for royalty tracking"
    - "Payment schedule added to financial calendar"
    - "Key dates added to monitoring system"
    - "Responsible personnel assigned and trained"
    
  external_coordination:
    - "Payment confirmation process established"
    - "Reporting requirements clarified"
    - "Audit procedures agreed upon"
    - "Dispute resolution process understood"
```

#### Ongoing Management
```yaml
ongoing_management:
  monthly:
    - "Verify payment receipt on scheduled date"
    - "Reconcile payment to expected amount"
    - "Document any discrepancies"
    - "Follow up on late or missing payments"
    - "Update financial reports"
    
  quarterly:
    - "Review payment trends and variances"
    - "Assess counterparty performance"
    - "Update revenue projections"
    - "Review agreement terms for needed amendments"
    
  annual:
    - "Comprehensive agreement review"
    - "Exercise audit rights if warranted"
    - "Legal review of terms and market conditions"
    - "Renewal or renegotiation planning"
    - "Board report on royalty performance"
```

### Multiple Royalty Stream Management

#### Portfolio Approach
```yaml
royalty_portfolio:
  current_agreements:
    ninjatrader:
      status: "Active/Pending"
      annual_value: "$X"
      percentage_of_revenue: "X%"
      risk_level: "Medium"
      
  target_agreements:
    software_licensing:
      target_value: "$Y"
      timeframe: "12-18 months"
      
    technology_patents:
      target_value: "$Z"
      timeframe: "24-36 months"
      
  portfolio_goals:
    - "No single royalty source exceeds 30% of total revenue"
    - "Minimum of 3 active royalty agreements"
    - "Geographic and sector diversification"
    - "Staggered renewal dates to reduce concentration risk"
```

---

## Payment Processing and Tracking

### Payment Receipt Process

#### Standard Operating Procedure
```markdown
## Royalty Payment Receipt SOP

### Step 1: Payment Verification (Within 3 business days of due date)
- [ ] Check dedicated royalty account for deposit
- [ ] Verify amount matches expected payment
- [ ] Confirm payment source identification
- [ ] Note any discrepancies immediately

### Step 2: Documentation
- [ ] Create payment record in accounting system
- [ ] Scan/attach any accompanying documentation
- [ ] Code to appropriate revenue account
- [ ] Flag for month-end reconciliation

### Step 3: Discrepancy Resolution (if applicable)
- [ ] Document variance from expected amount
- [ ] Contact licensor for clarification within 5 days
- [ ] Track resolution in issue log
- [ ] Update expectations if needed

### Step 4: Reporting
- [ ] Include in weekly cash receipt summary
- [ ] Update monthly financial dashboard
- [ ] Notify leadership of significant variances
- [ ] Prepare for monthly financial reports
```

### Tracking System Requirements

#### Royalty Management Database
```yaml
tracking_system:
  required_fields:
    agreement_tracking:
      - "Agreement name/identifier"
      - "Counterparty name"
      - "Execution date"
      - "Term length"
      - "Renewal date"
      - "Key contact information"
      
    financial_tracking:
      - "Expected payment amount"
      - "Expected payment date"
      - "Actual payment date"
      - "Actual payment amount"
      - "Variance amount and reason"
      - "Year-to-date total"
      
    document_repository:
      - "Executed agreement (scanned)"
      - "Board authorization"
      - "Payment confirmations"
      - "Correspondence"
      - "Audit reports"
      
  reporting_capabilities:
    - "Payment variance report"
    - "Year-over-year comparison"
    - "Forecast vs. actual"
    - "Aging of missing payments"
    - "Agreement expiration calendar"
```

### Reconciliation Procedures

#### Monthly Reconciliation Checklist
```markdown
## Monthly Royalty Reconciliation

### Data Gathering
- [ ] Extract bank statements for royalty account
- [ ] Pull royalty payment register from accounting system
- [ ] Gather expected payment schedule
- [ ] Collect any payment notifications received

### Reconciliation
- [ ] Match each bank deposit to payment register
- [ ] Verify amounts match expectations
- [ ] Identify any missing expected payments
- [ ] Flag any unexpected deposits for investigation
- [ ] Calculate total royalty revenue for month

### Variance Analysis
- [ ] Document all variances >5% or $1,000
- [ ] Investigate causes of variances
- [ ] Update future expectations if needed
- [ ] Escalate significant issues to leadership

### Documentation
- [ ] Prepare reconciliation summary
- [ ] Obtain review signature from Treasurer
- [ ] File with monthly financial package
- [ ] Update tracking database with actual results
```

---

## Legal Framework for Royalties

### Intellectual Property Foundation

#### IP Documentation Requirements
```yaml
ip_foundation:
  ownership_documentation:
    - "Copyright registrations"
    - "Patent filings and grants"
    - "Trademark registrations"
    - "Trade secret protection protocols"
    - "Work-for-hire agreements with developers"
    
  chain_of_title:
    - "Creator → Nonprofit assignment agreements"
    - "Board resolutions authorizing IP strategy"
    - "Documentation of IP development funding"
    - "Records of all IP licensing agreements"
    
  protection_measures:
    - "Confidentiality agreements with all personnel"
    - "Access controls on proprietary information"
    - "Regular IP audits"
    - "Monitoring for infringement"
```

### Nonprofit-Specific Legal Considerations

#### Unrelated Business Income Tax (UBIT)
```yaml
ubit_analysis:
  general_rules:
    taxable_if:
      - "Income from trade or business"
      - "Regularly carried on"
      - "Not substantially related to exempt purpose"
    
    exceptions:
      - "Royalties generally excluded from UBIT"
      - "Passive income exception"
      - "Must not involve substantial services"
    
  ninjatrader_analysis:
    classification: "Likely royalty (passive income)"
    ubit_risk: "Low to Medium"
    factors:
      supporting_exclusion:
        - "Payment for use of IP (passive)"
        - "No substantial services provided"
        - "Similar to traditional royalty"
      
      risk_factors:
        - "If active involvement in product required"
        - "If ongoing services bundled with license"
        
  recommendations:
    - "Structure as pure licensing arrangement"
    - "Minimize nonprofit's active involvement"
    - "Document passive nature of income"
    - "Annual review with tax counsel"
    - "File Form 990-T if UBIT exceeds $1,000"
```

#### Private Benefit and Inurement Issues
```markdown
## Compliance Requirements

### Private Benefit Prevention
- Royalty agreements must benefit the nonprofit's mission
- Terms must be at fair market value (arm's length)
- Cannot primarily benefit private individuals
- Must advance charitable purposes

### Due Diligence
- [ ] Independent valuation of IP if material
- [ ] Comparables research for royalty rates
- [ ] Board approval with conflict-free vote
- [ ] Documentation of public benefit purpose
- [ ] Annual review of arrangement

### Red Flags to Avoid
- ❌ Royalty payments to insiders at above-market rates
- ❌ Agreements that primarily benefit private parties
- ❌ Lack of board oversight or approval
- ❌ Insufficient documentation of terms
- ❌ Failure to use royalty income for exempt purposes
```

### Contract Protection Clauses

#### Essential Protective Terms
```yaml
protective_clauses:
  payment_security:
    - clause: "Personal guarantee (if appropriate)"
      purpose: "Additional payment security"
      
    - clause: "Security interest in underlying IP"
      purpose: "Collateral for payment obligations"
      
    - clause: "Right to terminate for non-payment"
      purpose: "Leverage for payment enforcement"
      
  audit_rights:
    - clause: "Right to audit licensee books"
      frequency: "Annual or as needed"
      cost_allocation: "Licensee pays if variance >5%"
      
  termination_rights:
    - clause: "Termination for material breach"
      notice_period: "30 days to cure"
      
    - clause: "Termination for convenience"
      notice_period: "90-180 days"
      
    - clause: "Bankruptcy termination"
      effect: "Immediate or specified period"
      
  dispute_resolution:
    - clause: "Arbitration provision"
      venue: "Specified location"
      rules: "AAA or other"
      
    - clause: "Attorney's fees"
      allocation: "Prevailing party recovers"
```

---

## Tax Considerations

### Income Recognition

#### Accounting Methods
```yaml
income_recognition:
  accrual_method:
    recognition: "When earned, not when received"
    advantages:
      - "Matches revenue to period earned"
      - "Better financial planning"
      - "Required for audited statements"
    application:
      - "Record receivable when payment due"
      - "Accrue even if payment delayed"
      
  cash_method:
    recognition: "When payment received"
    advantages:
      - "Simpler bookkeeping"
      - "Tax deferral opportunity"
    limitations:
      - "Not acceptable for audited financials"
      - "Distorts financial position"
```

### Tax Reporting Requirements

#### Annual Reporting (Form 990)
```markdown
## Form 990 Reporting

### Revenue Reporting
- **Line 2** (Program Service Revenue): If royalties relate to exempt purpose
- **Line 6d** (Royalties): Specific line for royalty income
- **Schedule G**: Required if royalty income exceeds $15,000

### Schedule G Requirements
- Description of IP licensed
- Licensing arrangement details
- Relationship to exempt purpose
- Unrelated business income analysis

### Supporting Documentation
- [ ] Copy of royalty agreements
- [ ] Payment documentation
- [ ] UBIT analysis
- [ ] Board approval minutes
```

#### UBIT Reporting (Form 990-T)
```yaml
form_990t_requirements:
  filing_threshold: "$1,000 of unrelated business income"
  
  required_if:
    - "Royalty includes substantial services"
    - "Licensing arrangement is active business"
    - "Income not within royalty exception"
    
  key_sections:
    part_1:
      - "Gross receipts from royalties"
      - "Deductions directly connected to income"
      - "Net UBIT calculation"
      
    part_2:
      - "Deductions not directly connected"
      - "Charitable contribution deduction"
      
    part_3:
      - "Tax computation"
      - "Estimated tax payments"
```

### Tax Planning Strategies

#### Maximizing Tax Efficiency
```markdown
## Tax Optimization Strategies

### Ensure Royalty Classification
- Structure as passive licensing, not active business
- Minimize nonprofit's ongoing involvement
- Document lack of substantial services
- Obtain tax opinion if significant income

### Utilize Charitable Deduction
- If UBIT applies, maximize deductions
- Charitable contribution deduction up to 10% of UBTI
- Properly allocate direct and indirect expenses

### Timing Strategies
- Consider deferring large payments across tax years
- Accelerate deductible expenses when UBIT expected
- Quarterly estimated tax payments if needed

### State Tax Considerations
- Review state-specific UBIT rules (may differ from federal)
- Consider nexus issues if licensee in multiple states
- Sales and use tax analysis (generally not applicable to IP royalties)
```

---

## Risk Management

### Royalty-Specific Risks

#### Risk Matrix
```yaml
royalty_risks:
  payment_default:
    likelihood: "Medium"
    impact: "High"
    mitigation:
      - "Strong contract enforcement provisions"
      - "Payment security (guarantee, security interest)"
      - "Regular financial monitoring of licensee"
      - "Adequate reserves to cover potential loss"
      
  revenue_volatility:
    likelihood: "Medium-High"
    impact: "Medium"
    mitigation:
      - "Minimum payment guarantees in contract"
      - "Diversified royalty portfolio"
      - "Conservative revenue budgeting"
      - "Flexible expense structure"
      
  ip_infringement:
    likelihood: "Low-Medium"
    impact: "High"
    mitigation:
      - "Strong IP registration and protection"
      - "Regular monitoring for infringement"
      - "Legal counsel on retainer"
      - "Insurance coverage for IP litigation"
      
  contract_termination:
    likelihood: "Low"
    impact: "Critical"
    mitigation:
      - "Long initial term with renewals"
      - "Strong performance by nonprofit"
      - "Good relationship management"
      - "Revenue diversification strategy"
      
  tax_reclassification:
    likelihood: "Low-Medium"
    impact: "Medium-High"
    mitigation:
      - "Proper structuring from outset"
      - "Annual tax counsel review"
      - "Documentation of passive nature"
      - "Reserves for potential UBIT"
```

### Contingency Planning

#### Revenue Interruption Response
```markdown
## If Royalty Payments Stop

### Immediate Actions (Days 1-7)
- [ ] Confirm payment was actually due (check agreement)
- [ ] Contact licensee to determine cause
- [ ] Send formal payment demand letter
- [ ] Notify board and leadership team
- [ ] Assess immediate cash flow impact

### Short-term Actions (Days 8-30)
- [ ] Engage legal counsel if needed
- [ ] Review contract enforcement options
- [ ] Implement expense reduction measures
- [ ] Tap reserves if necessary
- [ ] Communicate with stakeholders

### Medium-term Actions (Months 2-6)
- [ ] Pursue legal remedies if appropriate
- [ ] Accelerate revenue diversification efforts
- [ ] Seek emergency funding if needed
- [ ] Restructure operations for lower royalty dependency
- [ ] Update risk management strategies
```

---

## Reporting and Transparency

### Internal Reporting

#### Board Reporting Package
```yaml
board_royalty_report:
  frequency: "Quarterly"
  
  required_sections:
    executive_summary:
      - "Total royalty revenue for period"
      - "Comparison to budget and prior year"
      - "Key trends and issues"
      
    detailed_analysis:
      - "Revenue by royalty agreement"
      - "Payment timeliness metrics"
      - "Variance explanations"
      - "Year-to-date performance"
      
    risk_assessment:
      - "Dependency risk update (% of total revenue)"
      - "Counterparty financial health"
      - "Legal or compliance issues"
      - "Market conditions affecting IP value"
      
    forward_looking:
      - "Updated projections"
      - "Upcoming agreement renewals"
      - "New opportunities"
      - "Risk mitigation actions"
```

### Public Reporting and Transparency

#### Stakeholder Communications
```markdown
## Transparency Guidelines

### What to Share Publicly
- General description of royalty arrangements
- Percentage of revenue from royalties (in ranges)
- How royalty income supports mission
- High-level financial performance

### What to Keep Confidential
- Specific royalty rates and payment amounts
- Counterparty identities (unless public)
- Detailed contract terms
- Strategic plans for IP licensing

### Annual Report Disclosure Example
"Technology royalties, representing approximately 30-40% of our annual revenue, provide crucial funding for our mission. These royalties result from proprietary software and methods developed by our organization. All royalty income is used exclusively to advance our charitable purposes in accordance with our tax-exempt status."
```

#### Donor and Funder Communication
```yaml
donor_communication:
  key_messages:
    sustainability:
      - "Royalty income provides sustainable funding"
      - "Reduces dependency on donations for operations"
      - "Allows donated funds to go directly to programs"
      
    mission_alignment:
      - "IP developed as part of mission fulfillment"
      - "Royalties from mission-related innovation"
      - "Creates virtuous cycle of innovation and funding"
      
    diversification:
      - "One of multiple revenue streams"
      - "Part of comprehensive sustainability strategy"
      - "Complements, not replaces, philanthropic support"
      
  transparency_commitments:
    - "Annual reporting of royalty revenue percentage"
    - "Clear explanation of IP ownership and licensing"
    - "Regular updates on financial sustainability"
    - "Open to questions from major donors"
```

---

## Conclusion

Effective royalty management requires attention to legal, financial, tax, and operational considerations. By implementing these strategies, the nonprofit can maximize the value of NinjaTrader dividends and other royalty streams while minimizing risks.

### Key Success Factors

1. **Strong Legal Foundation**: Well-drafted agreements with appropriate protections
2. **Rigorous Tracking**: Systematic monitoring and reconciliation of all payments
3. **Tax Compliance**: Proper classification and reporting of royalty income
4. **Risk Management**: Proactive identification and mitigation of royalty-specific risks
5. **Transparency**: Clear communication with stakeholders about royalty arrangements

### Next Steps

- [ ] Review existing NinjaTrader agreement (or draft if not yet executed)
- [ ] Implement tracking and reconciliation procedures
- [ ] Conduct tax analysis with qualified counsel
- [ ] Establish reporting protocols
- [ ] Integrate with broader financial safeguards framework

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-23  
**Review Frequency**: Annual or with any agreement changes  
**Owner**: Board Treasurer / Executive Director
