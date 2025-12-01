# Irrevocable Royalty Assignment Agreement

**⚠️ TEMPLATE ONLY — NOT LEGAL ADVICE — ATTORNEY REVIEW MANDATORY ⚠️**

**Status:** Draft Template v1.0  
**Last Updated:** 2025-11-23  
**Next Review:** Pre-execution legal review required

---

## IRREVOCABLE ROYALTY ASSIGNMENT AND LICENSE AGREEMENT

**This Agreement** is entered into as of \_\_\_\_\_\_\_\_\_\_\_\_ (the "Effective Date") by and between:

**ASSIGNOR:**  
[NinjaTrader IP Holding Entity Legal Name]  
[Address]  
[State of Formation]  
("Assignor")

**AND**

**ASSIGNEE:**  
[Wyoming 501(c)(3) Nonprofit Legal Name]  
[Wyoming Registered Office Address]  
State of Formation: Wyoming  
("Assignee" or "Nonprofit")

---

## RECITALS

**WHEREAS**, Assignor owns certain intellectual property rights, including but not limited to software code, algorithms, trading systems, and related documentation (collectively, the "IP Assets");

**WHEREAS**, Assignee is a nonprofit organization organized under Section 501(c)(3) of the Internal Revenue Code, operating for charitable, educational, and scientific purposes;

**WHEREAS**, Assignor desires to support Assignee's mission by assigning certain royalty streams from the IP Assets;

**WHEREAS**, the parties intend this assignment to be **irrevocable** and recorded on-chain for transparency and enforceability;

**NOW, THEREFORE**, in consideration of the mutual covenants contained herein and other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties agree as follows:

---

## ARTICLE I: DEFINITIONS

**1.1 "IP Assets"** means all intellectual property owned or controlled by Assignor as of the Effective Date, including:
- Software source code and binaries
- Trading algorithms and strategies
- Documentation and user manuals
- Trademarks, trade names, and branding
- Derivative works and improvements

**1.2 "Gross Revenue"** means all revenue received by Assignor or its affiliates from:
- Software license fees
- Subscription payments
- Consulting services utilizing the IP Assets
- Derivative product sales
- Any other commercial exploitation of the IP Assets

**1.3 "Royalty Rate"** means \_\_\_\_% of Gross Revenue, as defined in Section 2.1. *[Must match Section 2.1(a) - typical range 5-20% based on IP type and nonprofit mission alignment]*

**1.4 "Smart Contract"** means the Ethereum-based smart contract deployed at address [TO BE DEPLOYED] that automates royalty calculation and payment.

**1.5 "On-Chain Recording"** means publication of this agreement's hash, key terms, and payment records on the Ethereum blockchain for transparency and auditability.

---

## ARTICLE II: ASSIGNMENT OF ROYALTIES

**2.1 Royalty Assignment**

Assignor hereby irrevocably assigns, transfers, and conveys to Assignee:

(a) **\_\_\_\_% of all Gross Revenue** derived from the IP Assets, whether received before or after the Effective Date;

    *[ATTORNEY NOTE: Typical rates are 5-20% depending on IP value and nonprofit purpose. Must be determined with valuation expert and counsel. Common ranges: Software/SaaS: 10-15%, Trading Systems: 15-20%, General IP: 5-10%]*

(b) All rights to collect, enforce, and receive such royalty payments;

(c) The right to audit Assignor's books and records to verify Gross Revenue calculations;

(d) The right to enforce this Agreement through specific performance, injunctive relief, or other equitable remedies.

**2.2 Irrevocability**

This assignment is **IRREVOCABLE** and may not be:
- Rescinded or cancelled by Assignor
- Modified or amended without Assignee's written consent
- Terminated except as provided in Article VIII (Dissolution)
- Subordinated to other creditor claims without Assignee's consent

**2.3 Priority and Seniority**

Assignee's royalty interest shall be:
- Senior to all other royalty or revenue-sharing arrangements
- Secured by a first-priority security interest in the IP Assets
- Protected by a UCC-1 financing statement filed in [Wyoming/Delaware]
- Enforceable against Assignor's successors, assigns, and bankruptcy estate

---

## ARTICLE III: PAYMENT TERMS

**3.1 Payment Schedule**

Royalty payments shall be made:
- **Frequency:** Monthly, within 15 days after month-end
- **Method:** Automated transfer via Smart Contract (primary) or wire transfer (backup)
- **Currency:** US Dollars (USD) or USDC stablecoin at Assignee's election
- **Minimum Payment:** $0 (no minimum threshold)

**3.2 Smart Contract Automation**

The parties agree to utilize a smart contract for automated payment processing:

```solidity
// Conceptual smart contract structure (actual implementation TBD)
contract RoyaltyAssignment {
    address public assignor;
    address public assignee;
    uint256 public royaltyRateBPS; // Basis points (e.g., 1000 = 10%)
    
    function reportRevenue(uint256 grossRevenue) external onlyAssignor {
        uint256 royaltyAmount = (grossRevenue * royaltyRateBPS) / 10000;
        require(transferToAssignee(royaltyAmount), "Transfer failed");
        emit RoyaltyPaid(block.timestamp, grossRevenue, royaltyAmount);
    }
    
    // Multi-sig controls, audit trail, dispute resolution...
}
```

**3.3 Revenue Reporting**

Assignor shall:
- Report Gross Revenue monthly via Smart Contract or written statement
- Maintain accurate books and records for 7 years
- Provide Assignee with quarterly financial statements
- Grant Assignee audit rights upon 30 days' notice

---

## ARTICLE IV: AUDIT RIGHTS

**4.1 Audit Scope**

Assignee (or its designated auditors) may audit Assignor's:
- Revenue records and financial statements
- License agreements and customer contracts
- Bank account statements and payment processing records
- Blockchain transaction history (if applicable)

**4.2 Audit Frequency**

- **Annual Audit:** Once per calendar year at Assignee's expense
- **For Cause Audit:** Unlimited if Assignee has reasonable suspicion of underpayment, at Assignor's expense if discrepancy >5%

**4.3 Audit Remedies**

If audit reveals underpayment:
- Assignor shall pay shortfall + interest at 10% per annum within 30 days
- If discrepancy >10%, Assignor pays audit costs
- Repeated violations constitute material breach

---

## ARTICLE V: BLOCKCHAIN RECORDING

**5.1 On-Chain Publication**

Within 30 days of execution, parties shall:

(a) Deploy Smart Contract to Ethereum mainnet  
(b) Publish agreement hash (SHA-256) on-chain  
(c) Record key terms in Smart Contract storage:
    - Parties' addresses (ENS names or wallet addresses)
    - Royalty rate
    - Effective date
    - IPFS/Arweave link to full agreement text

**5.2 Public Transparency**

The parties acknowledge and agree:
- This agreement's existence and key terms are **publicly visible** on blockchain
- Payment history is recorded on-chain for community verification
- Anonymity is **not preserved** (wallet addresses are pseudonymous but traceable)

**5.3 Multi-Sig Controls**

Smart Contract shall implement:
- 3-of-5 multi-sig for administrative functions
- 4-of-7 multi-sig for emergency stop or parameter changes
- Time-locked upgrades (minimum 7-day delay)

---

## ARTICLE VI: REPRESENTATIONS AND WARRANTIES

**6.1 Assignor Representations**

Assignor represents and warrants:

(a) It is duly organized and in good standing in its state of formation  
(b) It has full right, title, and interest in the IP Assets  
(c) The IP Assets are free from liens, encumbrances, or adverse claims  
(d) This Agreement does not violate any other contract or court order  
(e) All Gross Revenue reports will be accurate and complete  

**6.2 Assignee Representations**

Assignee represents and warrants:

(a) It is a 501(c)(3) nonprofit organization in good standing  
(b) Acceptance of royalties is consistent with its tax-exempt purpose  
(c) It will use royalty proceeds for charitable, educational, or scientific purposes  
(d) It has authority to enter into this Agreement  

**6.3 No Other Warranties**

Except as expressly stated, **NO WARRANTIES** are made regarding:
- Amount or timing of future Gross Revenue
- Tax treatment of royalty payments
- Regulatory compliance (parties responsible for own compliance)

---

## ARTICLE VII: INDEMNIFICATION

**7.1 Mutual Indemnification**

Each party agrees to indemnify and hold harmless the other from:
- Breach of representations or warranties
- Violation of third-party IP rights
- Failure to comply with applicable laws
- Gross negligence or willful misconduct

**7.2 Procedure**

Indemnified party must:
- Provide prompt written notice of claim
- Allow indemnifying party to control defense
- Cooperate reasonably in defense

---

## ARTICLE VIII: TERM, TERMINATION, AND DISSOLUTION

**8.1 Perpetual Term**

This Agreement shall remain in effect **perpetually**, unless:

(a) **Assignee Dissolution:** If Assignee dissolves pursuant to its articles of incorporation, royalty interests shall transfer to another 501(c)(3) organization designated in Assignee's dissolution clause.

(b) **IP Asset Sale:** If Assignor sells IP Assets to third party, this Agreement binds the buyer (assignment runs with the IP).

(c) **Mutual Written Agreement:** Both parties consent in writing to termination (requires board vote by Assignee).

**8.2 Dead Man's Switch**

If Assignee's board is coerced or prevented from performing duties:
- Smart Contract automatically activates distribution mode
- Royalty interests convert to proportional distribution to [$CHAOS] token holders
- Full agreement published to IPFS/Arweave
- Legal deadhand provisions execute (notify authorities of coercion)

**8.3 No Unilateral Termination**

Assignor has **NO RIGHT** to terminate this Agreement unilaterally, even for:
- Convenience
- Change in business strategy
- Bankruptcy or insolvency (royalty survives bankruptcy)
- Change of control or acquisition

---

## ARTICLE IX: DISPUTE RESOLUTION

**9.1 Governing Law**

This Agreement shall be governed by the laws of **Wyoming**, without regard to conflicts of law principles.

**9.2 Binding Arbitration**

All disputes shall be resolved by **binding arbitration** under JAMS rules:
- **Venue:** Cheyenne, Wyoming (or remote via videoconference)
- **Arbitrator:** Single arbitrator with IP and nonprofit experience
- **Discovery:** Limited to documents, no depositions
- **Timeline:** Decision within 90 days of filing

**9.3 Specific Performance**

Parties agree:
- Monetary damages are inadequate remedy for breach
- Assignee entitled to specific performance and injunctive relief
- No bond required for injunctive relief

**9.4 Attorney's Fees**

Prevailing party in any dispute shall recover:
- Reasonable attorney's fees
- Costs of arbitration or litigation
- Expert witness fees

---

## ARTICLE X: MISCELLANEOUS

**10.1 Entire Agreement**

This Agreement constitutes the entire understanding between the parties and supersedes all prior negotiations, understandings, or agreements.

**10.2 Amendment**

May only be amended by:
- Written instrument signed by both parties
- On-chain governance vote (if applicable)
- Smart Contract upgrade with time-lock

**10.3 Severability**

If any provision is invalid or unenforceable, the remainder shall continue in full force.

**10.4 Waiver**

No waiver of any provision shall be deemed a waiver of any other provision or subsequent breach.

**10.5 Notices**

All notices shall be sent to:

**Assignor:**  
[Legal Name]  
[Address]  
[Email]

**Assignee:**  
[Wyoming 501(c)(3) Legal Name]  
[Registered Office Address]  
[Email]

**10.6 Counterparts**

This Agreement may be executed in counterparts (including electronic signatures), each of which shall be deemed an original.

**10.7 Public Filing**

Parties acknowledge this Agreement will be:
- Filed with IRS as part of 501(c)(3) application
- Published on blockchain (IPFS/Arweave)
- Disclosed in annual Form 990 filings
- Available for public inspection

---

## SIGNATURES

**IN WITNESS WHEREOF**, the parties have executed this Agreement as of the Effective Date.

**ASSIGNOR:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
[Name of Authorized Signatory]  
[Title]  
Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**ASSIGNEE:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
[Name of Authorized Signatory]  
[Title: Managing Member / Board President]  
Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## EXHIBIT A: IP ASSETS SCHEDULE

[Detailed list of IP Assets covered by this Agreement, including:]

1. **Software Code:**
   - NinjaTrader Indicators (list specific indicators)
   - Trading Strategies (list specific strategies)
   - Custom Libraries (list libraries)

2. **Documentation:**
   - User manuals
   - API documentation
   - White papers and research

3. **Trademarks and Branding:**
   - [Trademark Name] (Registration #\_\_\_\_\_\_)
   - Domain names
   - Social media handles

4. **Derivative Works:**
   - Future improvements
   - Modifications and adaptations
   - Translations and localizations

---

## EXHIBIT B: SMART CONTRACT SPECIFICATION

**Smart Contract Requirements:**

```yaml
smart_contract:
  blockchain: "Ethereum Mainnet"
  language: "Solidity 0.8.x"
  auditor: "Trail of Bits or equivalent"
  
  key_functions:
    - reportRevenue(uint256 grossRevenue)
    - claimRoyalty() // Assignee claims accrued royalties
    - updateRoyaltyRate(uint256 newRate) // Multi-sig only
    - emergencyStop() // 4-of-7 multi-sig
    
  events:
    - RoyaltyPaid(timestamp, grossRevenue, royaltyAmount)
    - RevenueReported(timestamp, grossRevenue)
    - AuditRequested(timestamp, auditor)
    - DisputeFiled(timestamp, claimAmount)
    
  access_control:
    assignor_admin: [address1, address2]  # 2-of-2 multi-sig
    assignee_admin: [address3, address4, address5]  # 2-of-3 multi-sig
    emergency_council: [7 addresses]  # 4-of-7 multi-sig
```

---

## EXHIBIT C: UCC-1 FINANCING STATEMENT

**Debtor:** [Assignor Legal Name and Address]  
**Secured Party:** [Assignee Legal Name and Address]  
**Collateral:** All intellectual property rights described in Exhibit A, including all accounts, general intangibles, and payment rights arising therefrom.

**Filing Jurisdiction:** Wyoming Secretary of State  
**Filing Date:** [To be completed upon filing]  
**File Number:** [To be completed upon filing]

---

## LEGAL DISCLAIMERS

**⚠️ CRITICAL NOTICES ⚠️**

This document is a **TEMPLATE ONLY** and:

- **NOT LEGAL ADVICE** - Must be reviewed and customized by Wyoming-licensed attorney
- **NOT TAX ADVICE** - Consult CPA for 501(c)(3) compliance and IRS implications
- **NOT SECURITIES ADVICE** - May have securities law implications requiring counsel
- **NOT FINAL** - Subject to material revision based on professional review

**No representations or warranties are made regarding:**
- Legal enforceability of any provision
- Tax treatment of royalty assignment
- Securities law compliance
- Smart contract security or functionality

**MANDATORY PROFESSIONAL REVIEW REQUIRED BEFORE EXECUTION**

---

## DOCUMENT CONTROL

**Version:** 1.0 (Template Draft)  
**Last Updated:** 2025-11-23  
**Next Review:** Pre-execution (attorney review mandatory)  
**Owner:** Managing Member + Wyoming Counsel  
**Classification:** Confidential (until executed and published)

---

**Questions:** Contact legal@strategickhaos.dao

---

*Template created for Strategickhaos DAO LLC / Wyoming 501(c)(3) planning purposes*  
*Professional legal review mandatory before execution*
