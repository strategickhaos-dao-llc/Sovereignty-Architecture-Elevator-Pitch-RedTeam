# Threat Model and Risk Assessment
## Adversarial Risk Analysis for Nonprofit Operations

This document provides a comprehensive threat model for the nonprofit organization, identifying potential adversarial risks and mitigation strategies to protect against threats to operations, funding, and mission fulfillment.

## Table of Contents
1. [Threat Modeling Framework](#threat-modeling-framework)
2. [Financial Threats](#financial-threats)
3. [Legal and Regulatory Threats](#legal-and-regulatory-threats)
4. [Operational Threats](#operational-threats)
5. [Reputational Threats](#reputational-threats)
6. [Technical and Infrastructure Threats](#technical-and-infrastructure-threats)
7. [Insider Threats](#insider-threats)
8. [Mitigation Strategies](#mitigation-strategies)

---

## Threat Modeling Framework

### Methodology

#### STRIDE Threat Model Adaptation
```yaml
threat_categories:
  spoofing:
    nonprofit_context: "Identity fraud, impersonation of organization"
    
  tampering:
    nonprofit_context: "Financial records manipulation, contract alteration"
    
  repudiation:
    nonprofit_context: "Denial of agreements, transaction disputes"
    
  information_disclosure:
    nonprofit_context: "Donor data breach, confidential information leak"
    
  denial_of_service:
    nonprofit_context: "Operational disruption, funding interruption"
    
  elevation_of_privilege:
    nonprofit_context: "Unauthorized access to assets, governance manipulation"
```

### Risk Assessment Matrix

#### Likelihood × Impact Framework
```markdown
| Likelihood / Impact | Low Impact | Medium Impact | High Impact | Critical Impact |
|---------------------|------------|---------------|-------------|-----------------|
| **Very Likely**     | Medium     | High          | Critical    | Critical        |
| **Likely**          | Low        | Medium        | High        | Critical        |
| **Possible**        | Low        | Medium        | Medium      | High            |
| **Unlikely**        | Low        | Low           | Medium      | Medium          |
| **Rare**            | Low        | Low           | Low         | Medium          |

**Risk Scoring:**
- Critical: Immediate action required, board notification
- High: Action within 30 days, leadership notification
- Medium: Action within 90 days, include in planning
- Low: Monitor and document, address opportunistically
```

### Threat Actor Categories

#### Adversary Profiles
```yaml
threat_actors:
  competitors:
    motivation: "Market advantage, IP theft"
    capabilities: "Moderate to high"
    likely_attacks:
      - "IP infringement or reverse engineering"
      - "Poaching of key personnel"
      - "Negative marketing campaigns"
      
  disgruntled_insiders:
    motivation: "Revenge, personal gain"
    capabilities: "High (insider knowledge)"
    likely_attacks:
      - "Data theft or destruction"
      - "Fraud or embezzlement"
      - "Disclosure of confidential information"
      
  cybercriminals:
    motivation: "Financial gain"
    capabilities: "Moderate to high"
    likely_attacks:
      - "Ransomware"
      - "Financial fraud"
      - "Data breach and extortion"
      
  nation_state_actors:
    motivation: "Espionage, disruption"
    capabilities: "Very high"
    likely_attacks:
      - "Advanced persistent threats"
      - "Supply chain attacks"
      - "Infrastructure disruption"
      
  activists:
    motivation: "Ideological opposition"
    capabilities: "Low to moderate"
    likely_attacks:
      - "DDoS attacks"
      - "Reputation attacks"
      - "Nuisance lawsuits"
      
  opportunists:
    motivation: "Crime of opportunity"
    capabilities: "Low to moderate"
    likely_attacks:
      - "Phishing and social engineering"
      - "Basic fraud schemes"
      - "Opportunistic theft"
```

---

## Financial Threats

### Royalty Payment Threats

#### Threat T-F-001: Royalty Payment Interruption
```yaml
threat_t_f_001:
  description: "Licensee stops or reduces royalty payments"
  
  threat_actors:
    - "Licensee (NinjaTrader or equivalent)"
    - "Licensee's bankruptcy trustee"
    
  attack_vectors:
    - "Financial distress of licensee"
    - "Contract dispute or interpretation"
    - "Strategic decision to breach contract"
    - "Acquisition or merger changes terms"
    
  likelihood: "Medium"
  impact: "High"
  risk_level: "High"
  
  indicators:
    early_warning:
      - "Delayed payments (even if small delays)"
      - "Reduced payment amounts without explanation"
      - "Poor communication from licensee"
      - "News of licensee financial difficulties"
      - "Change in licensee leadership"
    
  mitigation:
    preventive:
      - "Strong contract with payment guarantees"
      - "Regular financial monitoring of licensee"
      - "Diversified royalty portfolio"
      - "Adequate reserves (12 months royalty income)"
      
    detective:
      - "Daily payment monitoring"
      - "Financial news alerts for licensee"
      - "Regular check-ins with licensee contacts"
      
    responsive:
      - "Immediate escalation protocol"
      - "Legal counsel engagement within 7 days"
      - "Reserve fund activation"
      - "Revenue diversification acceleration"
```

#### Threat T-F-002: Fraudulent Claims Against Assets
```yaml
threat_t_f_002:
  description: "False claims of ownership or rights to nonprofit assets"
  
  threat_actors:
    - "Former employees or contractors"
    - "Competitors"
    - "Opportunistic litigants"
    
  attack_vectors:
    - "Claim of IP ownership"
    - "Disputed contract terms"
    - "Alleged oral agreements"
    - "Work-for-hire disputes"
    
  likelihood: "Low-Medium"
  impact: "High"
  risk_level: "Medium-High"
  
  mitigation:
    preventive:
      - "Clear IP assignment agreements"
      - "Work-for-hire documentation"
      - "IP audit and chain of title documentation"
      - "Regular legal review of agreements"
      
    detective:
      - "Monitor for USPTO filings by others"
      - "Google Alerts for organization name + legal terms"
      - "Regular review of potential claims"
      
    responsive:
      - "Immediate legal counsel engagement"
      - "Preservation of all relevant documents"
      - "Proactive communication with stakeholders"
      - "D&O insurance claim if applicable"
```

#### Threat T-F-003: Banking Access Restrictions
```yaml
threat_t_f_003:
  description: "Loss of banking services or account freezes"
  
  threat_actors:
    - "Financial institution"
    - "Regulatory agencies"
    - "Legal adversaries obtaining court orders"
    
  attack_vectors:
    - "Bank de-risking due to sector"
    - "Account freeze due to investigation"
    - "Garnishment or levy"
    - "Regulatory action"
    
  likelihood: "Low"
  impact: "Critical"
  risk_level: "Medium"
  
  mitigation:
    preventive:
      - "Relationships with multiple banks"
      - "Backup banking arrangements"
      - "Cryptocurrency/alternative payment systems"
      - "Regular compliance reviews"
      - "Maintain excellent bank relationship"
      
    detective:
      - "Daily account access verification"
      - "Monitoring for unusual bank communications"
      
    responsive:
      - "Emergency banking activation plan"
      - "Legal counsel engagement"
      - "Immediate payroll protection measures"
      - "Stakeholder communication protocol"
```

### Investment and Reserve Threats

#### Threat T-F-004: Investment Loss
```yaml
threat_t_f_004:
  description: "Significant loss of reserve fund investments"
  
  threat_actors:
    - "Market forces"
    - "Investment advisor fraud"
    - "Economic crisis"
    
  attack_vectors:
    - "Market downturn"
    - "Unsuitable investment strategy"
    - "Fraudulent investment schemes"
    - "Poor investment oversight"
    
  likelihood: "Medium"
  impact: "Medium-High"
  risk_level: "Medium"
  
  mitigation:
    preventive:
      - "Conservative investment policy"
      - "Diversified portfolio"
      - "Qualified investment advisors"
      - "Regular investment committee review"
      - "Prohibition on high-risk investments"
      
    detective:
      - "Quarterly investment performance review"
      - "Comparison to benchmarks"
      - "Due diligence on advisors"
      
    responsive:
      - "Investment policy adjustment"
      - "Advisor replacement if needed"
      - "Stakeholder communication"
      - "Spending policy adjustment"
```

---

## Legal and Regulatory Threats

### Litigation Threats

#### Threat T-L-001: Strategic Lawsuit (SLAPP)
```yaml
threat_t_l_001:
  description: "Frivolous lawsuit intended to intimidate or drain resources"
  
  threat_actors:
    - "Competitors"
    - "Disgruntled former personnel"
    - "Ideological opponents"
    
  attack_vectors:
    - "Defamation claims"
    - "IP infringement allegations"
    - "Employment disputes"
    - "Contract claims"
    
  likelihood: "Medium"
  impact: "Medium-High"
  risk_level: "Medium-High"
  
  indicators:
    - "Demands for unreasonable settlements"
    - "Vague or overbroad allegations"
    - "High-profile public filing"
    - "Extensive discovery requests"
    
  mitigation:
    preventive:
      - "Anti-SLAPP law protection (where available)"
      - "D&O and liability insurance"
      - "Legal counsel on retainer"
      - "Document preservation practices"
      - "Clear policies and procedures"
      
    detective:
      - "Legal filing monitoring"
      - "Media monitoring for threats"
      
    responsive:
      - "Immediate legal counsel engagement"
      - "Anti-SLAPP motion filing (if applicable)"
      - "Insurance claim notification"
      - "Public communications strategy"
      - "Board notification and involvement"
```

#### Threat T-L-002: Loss of Nonprofit Status
```yaml
threat_t_l_002:
  description: "Revocation or challenge of tax-exempt status"
  
  threat_actors:
    - "IRS"
    - "State regulators"
    - "Complainants to regulators"
    
  attack_vectors:
    - "Private benefit or inurement"
    - "Excessive lobbying or political activity"
    - "Failure to file required returns"
    - "Unrelated business income issues"
    - "Operating outside exempt purpose"
    
  likelihood: "Low"
  impact: "Critical"
  risk_level: "Medium"
  
  mitigation:
    preventive:
      - "Strict compliance program"
      - "Annual tax counsel review"
      - "Conflict of interest policy"
      - "Lobbying activity tracking"
      - "UBIT analysis for all income"
      - "Timely filing of all returns"
      
    detective:
      - "Quarterly compliance checklist"
      - "Annual independent audit"
      - "Regular board training"
      
    responsive:
      - "Immediate tax counsel engagement"
      - "Voluntary compliance efforts"
      - "Cooperation with regulators"
      - "Remediation plan development"
      - "Stakeholder communication strategy"
```

### Regulatory Threats

#### Threat T-L-003: Regulatory Investigation
```yaml
threat_t_l_003:
  description: "Investigation by state or federal regulators"
  
  threat_actors:
    - "State Attorney General"
    - "IRS"
    - "Other regulatory agencies"
    
  attack_vectors:
    - "Complaint from stakeholder"
    - "Routine audit selection"
    - "Media reports triggering inquiry"
    - "Cross-referral from other investigation"
    
  likelihood: "Low-Medium"
  impact: "High"
  risk_level: "Medium"
  
  mitigation:
    preventive:
      - "Robust compliance program"
      - "Regular self-audits"
      - "Transparent operations"
      - "Strong governance practices"
      
    detective:
      - "Monitor for regulatory inquiries"
      - "Track regulatory priorities"
      
    responsive:
      - "Cooperate fully with investigation"
      - "Immediate legal counsel engagement"
      - "Document preservation"
      - "Board notification and oversight"
      - "Corrective action if issues found"
```

---

## Operational Threats

### Personnel Threats

#### Threat T-O-001: Key Personnel Loss
```yaml
threat_t_o_001:
  description: "Loss of critical personnel through resignation, death, or disability"
  
  threat_actors:
    - "Competitors (poaching)"
    - "Natural circumstances"
    
  attack_vectors:
    - "Better offers from competitors"
    - "Burnout or dissatisfaction"
    - "Health issues"
    - "Personal circumstances"
    
  likelihood: "Medium"
  impact: "High"
  risk_level: "Medium-High"
  
  mitigation:
    preventive:
      - "Succession planning for all key roles"
      - "Cross-training and documentation"
      - "Competitive compensation and benefits"
      - "Key person insurance"
      - "Strong organizational culture"
      
    detective:
      - "Employee satisfaction surveys"
      - "Regular one-on-one meetings"
      - "Monitor for burnout indicators"
      
    responsive:
      - "Activation of succession plan"
      - "Interim leadership appointment"
      - "Knowledge transfer acceleration"
      - "External recruitment if needed"
```

### Technology and Infrastructure Threats

#### Threat T-O-002: Service Provider Restrictions
```yaml
threat_t_o_002:
  description: "Loss of critical service access (e.g., GitHub ban, cloud provider suspension)"
  
  threat_actors:
    - "Service providers"
    - "Regulators pressuring providers"
    - "Complainants to providers"
    
  attack_vectors:
    - "Terms of service violation (real or alleged)"
    - "Regulatory pressure on provider"
    - "Mass reporting campaign"
    - "Provider policy changes"
    
  likelihood: "Low-Medium"
  impact: "Medium-High"
  risk_level: "Medium"
  
  indicators:
    - "Warning notices from providers"
    - "Unusual account restrictions"
    - "Communication from abuse teams"
    
  mitigation:
    preventive:
      - "Decentralized infrastructure"
      - "Multiple provider redundancy"
      - "Regular backups to independent storage"
      - "Self-hosting capabilities"
      - "Clear ToS compliance"
      
    detective:
      - "Monitor provider communications"
      - "Regular backup verification"
      
    responsive:
      - "Rapid provider migration plan"
      - "Backup infrastructure activation"
      - "Appeal to provider decision"
      - "Legal review if appropriate"
```

#### Threat T-O-003: API Rate Limiting Impact
```yaml
threat_t_o_003:
  description: "Operational disruption due to API rate limits"
  
  threat_actors:
    - "API providers enforcing limits"
    
  attack_vectors:
    - "Exceeding rate limits"
    - "Rate limit policy changes"
    - "DDoS causing rate limit hits"
    
  likelihood: "Medium"
  impact: "Low-Medium"
  risk_level: "Low-Medium"
  
  mitigation:
    preventive:
      - "Intelligent caching strategies"
      - "Rate limit monitoring and alerting"
      - "Efficient API usage patterns"
      - "Multiple API keys/accounts"
      
    detective:
      - "Real-time usage monitoring"
      - "Trend analysis"
      
    responsive:
      - "Fallback mechanisms"
      - "Manual processes as backup"
      - "Escalation to provider if needed"
```

---

## Reputational Threats

### Public Perception Threats

#### Threat T-R-001: Misinformation Campaign
```yaml
threat_t_r_001:
  description: "Coordinated effort to spread false information about the organization"
  
  threat_actors:
    - "Competitors"
    - "Ideological opponents"
    - "Disgruntled former personnel"
    
  attack_vectors:
    - "Social media campaigns"
    - "False news stories"
    - "Review bombing"
    - "Astroturfing"
    
  likelihood: "Medium"
  impact: "Medium-High"
  risk_level: "Medium"
  
  indicators:
    - "Sudden increase in negative mentions"
    - "Coordinated posting patterns"
    - "Spread of specific false narratives"
    
  mitigation:
    preventive:
      - "Strong, transparent communications"
      - "Positive stakeholder relationships"
      - "Regular proactive storytelling"
      - "Social media presence"
      
    detective:
      - "Social media monitoring"
      - "Brand mention tracking"
      - "Sentiment analysis"
      
    responsive:
      - "Rapid response team activation"
      - "Fact-based corrections"
      - "Stakeholder outreach"
      - "Legal action if defamatory"
      - "Platform reporting for ToS violations"
```

#### Threat T-R-002: Scandal or Controversy
```yaml
threat_t_r_002:
  description: "Legitimate or fabricated scandal affecting reputation"
  
  threat_actors:
    - "Media"
    - "Whistleblowers"
    - "Bad actors within organization"
    
  attack_vectors:
    - "Actual misconduct exposure"
    - "Misrepresented facts"
    - "Lack of transparency fueling speculation"
    
  likelihood: "Low-Medium"
  impact: "High"
  risk_level: "Medium"
  
  mitigation:
    preventive:
      - "Strong ethics and compliance program"
      - "Whistleblower policy"
      - "Regular audits and oversight"
      - "Transparent operations"
      - "Crisis communications plan"
      
    detective:
      - "Internal reporting mechanisms"
      - "Regular compliance reviews"
      - "Media monitoring"
      
    responsive:
      - "Crisis communications activation"
      - "Immediate investigation if warranted"
      - "Transparent communication"
      - "Corrective actions"
      - "Stakeholder engagement"
```

---

## Technical and Infrastructure Threats

### Cybersecurity Threats

#### Threat T-T-001: Ransomware Attack
```yaml
threat_t_t_001:
  description: "Encryption of organizational data with ransom demand"
  
  threat_actors:
    - "Cybercriminal groups"
    - "Opportunistic attackers"
    
  attack_vectors:
    - "Phishing emails"
    - "Unpatched vulnerabilities"
    - "RDP compromise"
    - "Supply chain attack"
    
  likelihood: "Medium"
  impact: "High"
  risk_level: "Medium-High"
  
  mitigation:
    preventive:
      - "Regular backups (3-2-1 rule)"
      - "Email filtering and security"
      - "Patch management"
      - "Network segmentation"
      - "User security training"
      - "Endpoint protection"
      
    detective:
      - "Security monitoring (SIEM)"
      - "Anomaly detection"
      - "Regular security assessments"
      
    responsive:
      - "Incident response plan"
      - "Isolate affected systems"
      - "Activate backups"
      - "Law enforcement notification"
      - "Cyber insurance claim"
      - "Stakeholder communication"
```

#### Threat T-T-002: Data Breach
```yaml
threat_t_t_002:
  description: "Unauthorized access to sensitive data (donor info, financial data, etc.)"
  
  threat_actors:
    - "External hackers"
    - "Malicious insiders"
    
  attack_vectors:
    - "Hacking attacks"
    - "Social engineering"
    - "Insider theft"
    - "Lost/stolen devices"
    - "Misconfigured systems"
    
  likelihood: "Medium"
  impact: "High"
  risk_level: "Medium-High"
  
  mitigation:
    preventive:
      - "Data encryption (at rest and in transit)"
      - "Access controls and MFA"
      - "Data minimization"
      - "Security awareness training"
      - "Regular security assessments"
      - "Incident response plan"
      
    detective:
      - "Security monitoring"
      - "Access logging and review"
      - "Anomaly detection"
      
    responsive:
      - "Incident response activation"
      - "Forensic investigation"
      - "Breach notification (per legal requirements)"
      - "Credit monitoring for affected parties"
      - "Regulatory notifications"
      - "Cyber insurance claim"
```

---

## Insider Threats

### Internal Threat Scenarios

#### Threat T-I-001: Fraud or Embezzlement
```yaml
threat_t_i_001:
  description: "Theft of organizational funds by trusted insider"
  
  threat_actors:
    - "Employees with financial access"
    - "Board members"
    - "Volunteers with access"
    
  attack_vectors:
    - "False expense claims"
    - "Check fraud"
    - "Electronic payment manipulation"
    - "Vendor kickback schemes"
    
  likelihood: "Low-Medium"
  impact: "Medium-High"
  risk_level: "Medium"
  
  mitigation:
    preventive:
      - "Segregation of duties"
      - "Dual authorization requirements"
      - "Regular audits"
      - "Background checks"
      - "Clear policies and procedures"
      - "Ethics training"
      
    detective:
      - "Regular reconciliations"
      - "Audit trails review"
      - "Anomaly detection"
      - "Whistleblower hotline"
      
    responsive:
      - "Immediate investigation"
      - "Personnel action"
      - "Legal action if warranted"
      - "Recovery efforts"
      - "Control improvements"
```

#### Threat T-I-002: Confidential Information Disclosure
```yaml
threat_t_i_002:
  description: "Unauthorized disclosure of sensitive information"
  
  threat_actors:
    - "Current employees"
    - "Former employees"
    - "Board members"
    - "Contractors"
    
  attack_vectors:
    - "Intentional leaking"
    - "Careless handling"
    - "Social engineering victim"
    - "Post-employment revenge"
    
  likelihood: "Medium"
  impact: "Medium"
  risk_level: "Medium"
  
  mitigation:
    preventive:
      - "Confidentiality agreements"
      - "Access controls"
      - "Data classification"
      - "Security training"
      - "Exit procedures"
      
    detective:
      - "Access logging"
      - "Data loss prevention tools"
      - "Media monitoring"
      
    responsive:
      - "Investigation"
      - "Damage control"
      - "Legal action if warranted"
      - "Stakeholder communication"
```

---

## Mitigation Strategies

### Comprehensive Risk Treatment

#### Four Strategies for Each Threat
```yaml
risk_treatment_options:
  avoid:
    description: "Eliminate the risk by not engaging in activity"
    example: "Don't pursue certain high-risk revenue streams"
    
  reduce:
    description: "Implement controls to lower likelihood or impact"
    example: "Strong contracts, insurance, technical controls"
    
  transfer:
    description: "Shift risk to third party"
    example: "Insurance, outsourcing, indemnification"
    
  accept:
    description: "Acknowledge and monitor risk without active mitigation"
    example: "Low-priority risks with acceptable impact"
```

### Continuous Threat Modeling

#### Regular Review Cycle
```markdown
## Threat Model Maintenance Schedule

### Monthly
- Review threat indicators
- Update dashboard with new intelligence
- Assess effectiveness of controls

### Quarterly
- Full threat model review with leadership
- Update risk ratings based on changes
- Training on identified threats
- Tabletop exercise for high-priority threats

### Annual
- Comprehensive threat landscape analysis
- External threat assessment
- Penetration testing and security audit
- Board presentation on threat environment
- Update to threat model documentation
```

### Stakeholder Training

#### Threat Awareness Program
```yaml
training_program:
  all_personnel:
    frequency: "Annual"
    topics:
      - "Phishing and social engineering"
      - "Physical security"
      - "Data protection"
      - "Incident reporting"
      
  financial_personnel:
    frequency: "Semi-annual"
    topics:
      - "Fraud detection"
      - "Financial controls"
      - "Vendor verification"
      
  leadership:
    frequency: "Quarterly"
    topics:
      - "Threat landscape updates"
      - "Risk management strategies"
      - "Crisis response"
      
  board:
    frequency: "Annual + ad-hoc"
    topics:
      - "Governance risks"
      - "Fiduciary duties"
      - "Strategic risk decisions"
```

---

## Conclusion

This threat model provides a framework for understanding and managing risks to the nonprofit organization. Regular review and update of this document ensures continued relevance and effectiveness.

### Key Takeaways

1. **Proactive Stance**: Don't wait for threats to materialize
2. **Layered Defense**: Multiple controls for each significant threat
3. **Continuous Monitoring**: Regular review of threat indicators
4. **Stakeholder Involvement**: Training and awareness at all levels
5. **Regular Updates**: Threat landscape constantly evolves

### Integration with Other Documentation

This threat model should be used in conjunction with:
- [NONPROFIT_SECURITY_GUIDE.md](./NONPROFIT_SECURITY_GUIDE.md) - Overall security framework
- [FINANCIAL_SAFEGUARDS.md](./FINANCIAL_SAFEGUARDS.md) - Financial protection measures
- [CONTINGENCY_PLANS.md](./CONTINGENCY_PLANS.md) - Response procedures
- [VAULT_SECURITY_PLAYBOOK.md](./VAULT_SECURITY_PLAYBOOK.md) - Technical security

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-23  
**Review Frequency**: Quarterly  
**Owner**: Board Risk Committee / Executive Director
