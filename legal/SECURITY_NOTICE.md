# Security Notice - Legal Documentation

## Sensitive Information Handling

### ⚠️ IMPORTANT: Information Classification

The legal documentation in this repository contains **sensitive business information** that must be handled appropriately:

### Employer Identification Numbers (EINs)

**EINs Disclosed:**
- StrategicKhaos DAO LLC: 39-2900295
- ValorYield Engine: 39-2923503

**Security Considerations:**

1. **Public Record:** EINs are similar to business Social Security Numbers and are often publicly available for registered entities.

2. **Documentation Context:** EINs are disclosed in this documentation because:
   - They appear in public Wyoming Secretary of State filings
   - They appear in IRS 501(c)(3) determination letters (ValorYield)
   - They are necessary for attorney review and legal filings
   - They are required for banking and financial integrations

3. **No Inherent Risk:** Unlike personal SSNs, EINs alone cannot be used to:
   - Open bank accounts
   - File fraudulent tax returns
   - Access confidential information
   - Commit identity theft

4. **Risk Context:** EINs become sensitive only when combined with:
   - Bank account information
   - Tax filing credentials
   - IRS online account access
   - Financial institution passwords

### Best Practices

**For Internal Use:**
- ✅ Keep banking credentials separate and secured
- ✅ Use multi-factor authentication for IRS/state accounts
- ✅ Limit access to financial systems
- ✅ Monitor for unauthorized tax filings or account access

**For Public Distribution:**
- ✅ EINs may be shared in legal filings and contracts
- ✅ Always include proper business context
- ❌ Never share with EIN + banking details together
- ❌ Never share IRS online account credentials

### Other Sensitive Information

**Items Requiring Protection:**
- [ ] Bank account numbers
- [ ] Sequence.io API keys
- [ ] Discord webhook URLs  
- [ ] Internal financial statements
- [ ] Unreleased strategic plans
- [ ] Attorney-client privileged communications

**Items Safe for Attorney Review:**
- [x] Entity formation documents
- [x] EINs with business context
- [x] Technical architecture descriptions
- [x] Board resolutions (approved for disclosure)
- [x] Public trademark information

### Repository Security

**This Repository:**
- Contains documentation prepared for attorney review
- Intended for limited distribution to qualified legal counsel
- Should not be made publicly accessible until attorney review complete
- Contains draft documents marked "INTERNAL DRAFT"

**Access Control:**
- Limit repository access to board members and authorized personnel
- Use GitHub's private repository features
- Consider using separate repository for public-facing materials
- Implement branch protection for sensitive documentation

### Disclosure to Legal Counsel

When providing this documentation package to attorneys:

✅ **Safe to Share:**
- Complete attorney package in `/legal/attorney-package/`
- Entity formation documents
- Technical architecture descriptions
- Board resolutions
- EINs with business context

⚠️ **Requires NDA First:**
- Proprietary technical implementations
- Financial projections and strategies
- Unreleased product roadmaps
- Competitive analysis

🔒 **Never Share:**
- Banking API credentials
- Production system passwords
- Private encryption keys
- Attorney-client privileged emails from other counsel

### Incident Response

**If Credentials Are Compromised:**

1. **Immediate Actions:**
   - Rotate Sequence.io API keys immediately
   - Change Discord webhook URLs
   - Update Kubernetes secrets
   - Monitor banking accounts for unauthorized activity

2. **Notification:**
   - Notify board members
   - Notify banking partners (Thread Bank, Sequence.io)
   - Document incident per compliance requirements

3. **Recovery:**
   - Deploy updated secrets to Kubernetes
   - Review audit logs for unauthorized access
   - Implement additional security controls

**If EINs Are Publicly Disclosed:**
- Generally low risk as EINs are public for registered entities
- Monitor for tax filing fraud (set up IRS PIN if concerned)
- No immediate action required in most cases

### Questions?

**For Security Concerns:**
- Contact: Board of Directors
- Escalate: Immediately for credential compromise
- Document: All security incidents

**For Attorney Coordination:**
- Contact: Domenic Garza (authorized representative)
- Purpose: Coordination of legal document distribution

---

## Compliance with UPL-Safe Framework

This notice is part of the UPL-Safe governance framework:
- Attorney review gates: Active
- Access control matrix: Enforced
- 30-point compliance checklist: Implemented
- Pre-commit hooks: PII scanning enabled

---

**Classification:** Internal Use - Attorney Review Package  
**Distribution:** Board members, authorized legal counsel (under NDA)  
**Date:** December 5, 2025

**INTERNAL DRAFT — ATTORNEY REVIEW REQUIRED — NOT LEGAL ADVICE**

---

END OF SECURITY NOTICE
