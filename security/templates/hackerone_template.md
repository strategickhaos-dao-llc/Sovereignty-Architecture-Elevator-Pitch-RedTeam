# Vulnerability Report Template (HackerOne Style)

## Report Metadata
- **Report ID**: [VR-YYYY-NNN]
- **Submitted By**: [Your Name/Handle]
- **Submission Date**: [YYYY-MM-DD]
- **Last Updated**: [YYYY-MM-DD]

---

## Summary

> **Brief, non-technical summary for management and triage teams**

[Provide a 2-3 sentence overview of the vulnerability that a non-technical stakeholder can understand. Focus on business impact.]

---

## Severity Assessment

### Severity Level
- [ ] Critical (CVSS 9.0-10.0)
- [ ] High (CVSS 7.0-8.9)
- [ ] Medium (CVSS 4.0-6.9)
- [ ] Low (CVSS 0.1-3.9)
- [ ] Informational

### CVSS v3.1 Vector
```
CVSS:3.1/AV:_/AC:_/PR:_/UI:_/S:_/C:_/I:_/A:_
```

**CVSS Score**: [0.0 - 10.0]

**Calculator**: https://www.first.org/cvss/calculator/3.1

---

## Asset Information

### Affected Asset
- **Asset Name**: [e.g., Main Web Application]
- **Asset Type**: 
  - [ ] Web Application
  - [ ] API
  - [ ] Mobile App (iOS)
  - [ ] Mobile App (Android)
  - [ ] Desktop Application
  - [ ] Infrastructure
  - [ ] Other: ___________

- **Asset URL**: [https://example.com/path]
- **Environment**: 
  - [ ] Production
  - [ ] Staging
  - [ ] Development

### Software/Platform Details
- **Version**: [e.g., v2.1.3]
- **Framework**: [e.g., Django 4.2, React 18]
- **Server**: [e.g., nginx 1.21]

---

## Weakness Classification

### CWE/Weakness Type
- **CWE ID**: [e.g., CWE-79]
- **Weakness Name**: [e.g., Cross-site Scripting (XSS)]
- **OWASP Top 10**: [e.g., A03:2021 - Injection]

**Reference**: https://cwe.mitre.org/data/definitions/[ID].html

---

## Technical Details

### Vulnerability Description

[Provide detailed technical explanation of the vulnerability. Include:]
- Root cause of the vulnerability
- Affected code or functionality
- Why the vulnerability exists
- Attack vectors and prerequisites

```
[Include relevant code snippets, configuration files, or error messages]
```

### Affected Components
- [ ] Authentication system
- [ ] Authorization/Access control
- [ ] Input validation
- [ ] Session management
- [ ] Data storage
- [ ] API endpoints
- [ ] Other: ___________

---

## Proof of Concept

### Reproduction Steps

**Prerequisites:**
- [Any required conditions, accounts, or setup]

**Step-by-Step Instructions:**

1. [First step]
   ```bash
   [Command or action]
   ```

2. [Second step]
   ```bash
   [Command or action]
   ```

3. [Third step]
   ```bash
   [Command or action]
   ```

4. [Expected malicious outcome]

### PoC Code/Payload

```python
# Include working exploit code or payload
# Be responsible: ensure PoC is minimal and non-destructive

```

### HTTP Request/Response

**Request:**
```http
POST /api/endpoint HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "parameter": "malicious_payload"
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "result": "sensitive_data_leaked"
}
```

### Evidence

**Screenshots:**
1. [screenshot1.png] - [Description]
2. [screenshot2.png] - [Description]

**Video Demonstration:**
- [URL to video proof]

---

## Impact Assessment

### Confidentiality Impact
[Describe impact on data confidentiality]
- What data can be accessed?
- How sensitive is the data?
- Scale of data exposure

### Integrity Impact
[Describe impact on data integrity]
- Can data be modified?
- Can malicious data be injected?
- Scope of data manipulation

### Availability Impact
[Describe impact on system availability]
- Can service be disrupted?
- Potential for denial of service?
- Duration of impact

### Business Impact
[Describe business and operational impact]
- Financial impact
- Reputation damage
- Regulatory compliance (GDPR, HIPAA, PCI-DSS)
- Legal liability

### Affected Users
- **Number/Percentage**: [e.g., "All users" or "5% of premium users"]
- **User Types**: [e.g., "Authenticated users", "Administrators"]

---

## Remediation Recommendations

### Short-Term Mitigations (Immediate)

1. **[Mitigation 1]**
   - Action: [What to do]
   - Timeline: [How quickly]
   - Impact: [Effect on users/functionality]

2. **[Mitigation 2]**
   - Action: [What to do]
   - Timeline: [How quickly]
   - Impact: [Effect on users/functionality]

### Long-Term Fixes (Permanent Solution)

1. **[Fix 1]**
   ```python
   # Example code fix
   # BEFORE (vulnerable):
   query = f"SELECT * FROM users WHERE id = {user_input}"
   
   # AFTER (secure):
   query = "SELECT * FROM users WHERE id = ?"
   cursor.execute(query, (user_input,))
   ```

2. **[Fix 2]**
   - Implementation details
   - Testing requirements
   - Deployment considerations

### Security Best Practices

- [ ] Input validation and sanitization
- [ ] Output encoding
- [ ] Parameterized queries
- [ ] Principle of least privilege
- [ ] Security headers
- [ ] Regular security audits
- [ ] Security awareness training

---

## References

### Standards & Frameworks
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Related Vulnerabilities
- [CVE-YYYY-NNNNN](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-YYYY-NNNNN)
- [Related report ID]

### Documentation
- [Link to affected product documentation]
- [Link to security advisories]
- [Link to vendor security policy]

---

## Attachments

- [ ] `screenshot1.png` - Initial discovery
- [ ] `screenshot2.png` - PoC execution
- [ ] `exploit.py` - Proof of concept code
- [ ] `traffic.pcap` - Network capture (if applicable)
- [ ] `logs.txt` - Relevant log files

---

## Bug Bounty Information

### Eligibility
- [ ] In scope for bug bounty program
- [ ] Out of scope
- [ ] Requires special approval

### Bounty Expectation (if applicable)
Based on severity and impact:
- Critical: $[amount range]
- High: $[amount range]
- Medium: $[amount range]
- Low: $[amount range]

### Disclosure Timeline
- **Responsible Disclosure Period**: [e.g., 90 days]
- **Preferred Fix Timeline**: [e.g., 30 days for High/Critical]
- **Public Disclosure**: [After fix or timeline expiration]

---

## Additional Notes

[Any additional context, observations, or recommendations]

---

## Report Checklist

Before submitting, ensure:
- [ ] Clear and concise title
- [ ] Accurate severity assessment
- [ ] Complete CVSS vector
- [ ] Detailed technical explanation
- [ ] Working proof of concept
- [ ] Realistic impact assessment
- [ ] Actionable remediation advice
- [ ] All evidence attached
- [ ] Responsible disclosure followed
- [ ] No sensitive data exposed in report

---

**Report Template Version**: 1.0  
**Last Updated**: 2025-12-16  
**Maintained By**: Strategickhaos DAO LLC

---

## Template Usage Notes

### For Security Researchers:
1. Replace all `[placeholders]` with actual information
2. Check all relevant checkboxes
3. Provide clear, reproducible PoC
4. Be responsible - don't cause harm
5. Follow coordinated disclosure practices

### For Security Teams:
1. Triage based on severity and impact
2. Validate PoC in controlled environment
3. Track remediation progress
4. Communicate with researcher
5. Document lessons learned

### Severity Guidelines:
- **Critical**: Remote code execution, auth bypass affecting all users
- **High**: Privilege escalation, SQL injection, significant data exposure
- **Medium**: XSS, CSRF, information disclosure
- **Low**: Security misconfigurations, minor information leaks
- **Informational**: Security recommendations, best practices

---

**Remember**: The goal is clear communication for efficient remediation, not just finding bugs.
