# Security Policy

## 🚨 Emergency Security Issues

### Exposed API Keys or Credentials
If you have accidentally exposed an API key, credential, or secret:

1. **STOP IMMEDIATELY** - Do not commit or push
2. **Follow the Emergency Response Guide**: [API_KEY_SECURITY.md](./API_KEY_SECURITY.md)
3. **Revoke the compromised credential** at the provider immediately
4. **Notify the repository maintainers** via private channel
5. **Document the incident** for security audit trail

**CRITICAL**: Time is of the essence. Exposed keys should be revoked within minutes, not hours.

---

## 🔐 API Key & Secret Management

### Never Commit Secrets
The following must **NEVER** be committed to this repository:

- ❌ API keys (xAI, OpenAI, Anthropic, etc.)
- ❌ Authentication tokens
- ❌ Private keys (.pem, .key files)
- ❌ Passwords or passphrases
- ❌ OAuth secrets
- ❌ Database credentials
- ❌ Encryption keys
- ❌ Screenshots containing sensitive data

### Secure Storage Methods
✅ Use environment variables (`.env` files - added to `.gitignore`)  
✅ Use password managers (Bitwarden, 1Password)  
✅ Use secret management tools (HashiCorp Vault)  
✅ Use cloud secret managers (AWS Secrets Manager, Azure Key Vault)

**See detailed guidance**: [API_KEY_SECURITY.md](./API_KEY_SECURITY.md)

---

## 🛡️ Supported Versions

Current security support status:

| Component | Version | Supported          |
| --------- | ------- | ------------------ |
| Core Platform | main branch | :white_check_mark: |
| Discord Bot | latest | :white_check_mark: |
| Event Gateway | latest | :white_check_mark: |
| Refinory Agent | latest | :white_check_mark: |
| Legacy Branches | < v1.0 | :x:                |

---

## 🔍 Reporting a Vulnerability

### Scope
We take security seriously. Please report any of the following:

- Exposed secrets in repository history
- Authentication/authorization bypasses
- Code injection vulnerabilities
- Dependency vulnerabilities (high/critical severity)
- Container security issues
- Infrastructure misconfigurations
- Data exposure risks

### How to Report

**For Critical/High Severity Issues:**
1. **DO NOT** create a public GitHub issue
2. **DO NOT** disclose publicly before patch
3. **Contact**: [Repository Owner] via private/secure channel
4. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

**For Low/Medium Severity Issues:**
1. Open a GitHub issue with label `security`
2. Provide detailed description
3. Tag repository maintainers

### Response Timeline

| Severity | Acknowledgment | Initial Response | Patch Target |
|----------|---------------|------------------|--------------|
| Critical | < 4 hours | < 24 hours | < 7 days |
| High | < 24 hours | < 72 hours | < 30 days |
| Medium | < 72 hours | < 1 week | < 60 days |
| Low | < 1 week | < 2 weeks | Best effort |

### What to Expect

1. **Acknowledgment**: We'll confirm receipt of your report
2. **Assessment**: We'll evaluate severity and impact
3. **Fix Development**: We'll develop and test a patch
4. **Disclosure**: We'll coordinate disclosure timeline with you
5. **Credit**: We'll credit you in security advisories (if desired)
6. **Resolution**: We'll notify when patch is deployed

---

## 🔄 Security Maintenance

### Regular Security Practices

- **Dependency Scanning**: Automated via GitHub Dependabot
- **Secret Scanning**: Automated via GitHub Advanced Security
- **Code Scanning**: Automated via CodeQL
- **Container Scanning**: Trivy scans on all Docker images
- **Key Rotation**: Quarterly rotation schedule (see [VAULT_SECURITY_PLAYBOOK.md](./VAULT_SECURITY_PLAYBOOK.md))
- **Audit Logs**: Continuous monitoring of Vault and service logs

### Security Audits

- **Monthly**: Dependency vulnerability review
- **Quarterly**: API key rotation and access review
- **Annually**: Full security architecture review

---

## 📚 Security Resources

- **API Key Security Guide**: [API_KEY_SECURITY.md](./API_KEY_SECURITY.md)
- **Vault Security Playbook**: [VAULT_SECURITY_PLAYBOOK.md](./VAULT_SECURITY_PLAYBOOK.md)
- **Secret Scanning Tools**:
  - [Gitleaks](https://github.com/gitleaks/gitleaks)
  - [TruffleHog](https://github.com/trufflesecurity/trufflehog)
  - [Git-Secrets](https://github.com/awslabs/git-secrets)

---

## 🎯 Security Principles

### Defense in Depth
We implement multiple layers of security:
1. **Prevention**: Strict .gitignore, pre-commit hooks
2. **Detection**: Secret scanning, audit logging
3. **Response**: Emergency procedures, rotation playbooks
4. **Recovery**: Backup strategies, incident response plans

### Principle of Least Privilege
- Service accounts have minimal required permissions
- API keys restricted to specific use cases
- Database credentials scoped to specific operations
- Time-limited access tokens where possible

### Zero Trust
- No hardcoded credentials
- All secrets in secure vaults
- Continuous verification
- Audit all access

---

**Last Updated**: 2025-11-23  
**Version**: 2.0  
**Owner**: Strategickhaos

For questions or concerns about this security policy, please contact the repository maintainers.
