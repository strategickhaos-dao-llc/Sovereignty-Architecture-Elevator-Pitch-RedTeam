# Legal Documentation

This directory contains legal research, compliance documentation, and guides for the Sovereignty Architecture project.

## AI Logs as Legal Evidence

### 📋 Core Documentation

- **[AI_LOGS_LEGAL_STATUS.md](AI_LOGS_LEGAL_STATUS.md)** - Comprehensive legal status table showing how AI logs are treated as evidence in courts (November 2025)
- **[GPG_SIGNING_GUIDE.md](GPG_SIGNING_GUIDE.md)** - Complete setup guide for cryptographic commit signing to achieve 9.5/10 legal admissibility

### 📝 Templates

See also: `../templates/ai_logs_sworn_declaration.md`
- One-page sworn declaration template for authenticating AI logs and ledger entries
- Achieves 9.5/10 admissibility strength when combined with GPG signing and hash chains

### 🎯 Quick Start for Legal Compliance

To achieve **9.5/10 admissibility strength** for your AI logs:

1. **Set up GPG signing** (5 minutes)
   ```bash
   # Follow GPG_SIGNING_GUIDE.md
   gpg --full-generate-key
   git config --global commit.gpgsign true
   ```

2. **Use the sworn declaration template**
   - Fill in: `../templates/ai_logs_sworn_declaration.md`
   - Include: Your GPG key fingerprint
   - Attach: Relevant ledger entries as exhibits

3. **Maintain hash chains**
   - Use SHA3 for log entries
   - Keep cryptographic integrity records
   - Document in regular course of business

4. **Preserve evidence**
   - Screenshots of AI outputs
   - Share URLs when available
   - Full context and metadata

### 📊 Legal Status Summary

| Evidence Type | Admissibility | Implementation |
|--------------|--------------|----------------|
| Raw AI Outputs | 3/10 | Add human affidavit |
| Screenshots + URLs | 8/10 | Already implemented |
| Hashed/Timestamped | 9/10 | SHA3 + GPG commits |
| Business Records | 9/10 | Regular logging + testimony |
| **Full Package** | **9.5/10** | All of the above |

### 🔐 Cryptographic Standards

- **GPG Signing:** RSA 4096-bit keys recommended
- **Hashing:** SHA3 for log entries
- **Timestamps:** Git commits + optional OpenTimestamps
- **Verification:** Public key publishing and verification reports

## Research Archives

### Cybersecurity Research
`cybersecurity_research/` - Compiled HTML archives of security standards, frameworks, and advisories
- MITRE ATT&CK, NIST, CIS, OWASP, and more
- Used for threat modeling and security compliance

### Wyoming Legal Research
`wyoming_sf0068/` - Research on Wyoming Senate File 0068 (2022)
- DAO LLC legislation and blockchain legal framework
- State statutes and regulatory guidance

## Legal Frameworks

### Federal Rules of Evidence (FRE)

**FRE 803(6) - Business Records:**
- Records kept in regular course of business are admissible
- Applies to AI logs when maintained systematically
- Requires custodian testimony

**FRE 901(b)(4) - Distinctive Characteristics:**
- Authentication through distinctive characteristics
- Applies to cryptographically signed records
- Supports GPG-signed commits as self-authenticating

### International Precedents

- **United States:** Business records + cryptographic proof admitted
- **Ukraine, Czech Republic:** Raw AI outputs rejected, but authenticated logs admitted
- **IP/Blockchain Cases:** Hash chains and timestamps routinely admitted

## Compliance Certifications

### Security Standards
- NIST Cybersecurity Framework (CSF)
- NIST SP 800-53 (Security Controls)
- NIST SP 800-171 (CUI Protection)
- CIS Controls v8
- OWASP ASVS (Application Security)

### Industry Frameworks
- ISO 27001 (Information Security)
- SOC 2 Type II (Service Organization Controls)
- GDPR (Data Protection - EU)
- CCPA (Privacy - California)

## Contributing

When adding legal documentation:

1. **Research Sources:** Always cite authoritative sources (statutes, case law, official guidance)
2. **Date Information:** Include "Last Updated" dates on all documents
3. **Disclaimers:** Add appropriate disclaimers for legal information
4. **Templates:** Use existing templates in `../templates/` as models
5. **Review:** Have legal counsel review when possible

## Disclaimer

**IMPORTANT:** This documentation is provided for informational purposes only and does not constitute legal advice. Consult with qualified legal counsel in your jurisdiction before relying on this information in legal proceedings.

The legal landscape for AI evidence is evolving. Always verify current law and precedent in your specific jurisdiction.

---

**Maintained by:** Strategickhaos DAO LLC  
**Primary Contact:** Domenic Garza  
**Purpose:** Legal compliance and evidence admissibility for AI research operations  
**Last Updated:** November 2025
