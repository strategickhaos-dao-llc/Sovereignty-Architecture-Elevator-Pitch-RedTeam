# Security Policy

**Last Updated:** 2025-11-21  
**Security Contact:** admin@strategickhaos.com  
**Discord:** #alerts channel

---

## 🔒 Overview

This document outlines the security policies and procedures for the Strategickhaos Sovereignty Architecture project. Security is critical to our mission of building sovereign, trustworthy infrastructure.

---

## 📋 Supported Versions

We provide security updates for the following versions:

| Component | Version | Supported | Notes |
|-----------|---------|-----------|-------|
| Sovereignty Architecture | latest (main) | ✅ | Active development |
| Discord Bot | v1.x | ✅ | Production |
| Event Gateway | v1.x | ✅ | Production |
| Kubernetes Manifests | latest | ✅ | Rolling updates |
| Legacy/archived branches | < 1.0 | ❌ | Not supported |

---

## 🐛 Reporting a Vulnerability

### Where to Report

**DO NOT** open public GitHub issues for security vulnerabilities.

Instead, report security issues through one of these channels:

1. **Email (Preferred):** admin@strategickhaos.com
2. **Discord (Private DM):** Contact @Strategickhaos
3. **GitHub Security Advisory:** Use the "Security" tab → "Report a vulnerability"

### What to Include

Please include as much information as possible:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information

### What to Expect

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 5 business days
- **Status Updates:** Every 7 days until resolved
- **Public Disclosure:** Coordinated after fix is deployed (typically 30-90 days)

### If Vulnerability is Accepted

1. We'll work on a fix and coordinate disclosure timeline
2. You'll be credited in the security advisory (unless you prefer anonymity)
3. We'll notify you before public disclosure
4. Critical vulnerabilities will be fast-tracked

### If Vulnerability is Declined

- We'll explain why we don't consider it a vulnerability
- You're welcome to discuss or provide additional information
- We'll document the discussion for transparency

---

## 🤖 GitHub Copilot Agent Security

### Agent Authorization Model

GitHub Copilot Agents operating in this repository have **limited permissions** by design:

✅ **Agents CAN:**
- Read repository code and issues
- Create branches (prefixed with `copilot/*` or `agent/*`)
- Open pull requests
- Comment on PRs and issues
- Edit files via PR branches

❌ **Agents CANNOT:**
- Merge pull requests (requires human approval)
- Push to protected branches (`main`, `develop`, `release/*`)
- Access GitHub Secrets
- Trigger deployments directly
- Access Kubernetes clusters
- Modify repository settings
- Delete branches or repositories

### How We Protect Against Agent Misuse

1. **Branch Protection:** All critical branches require PR reviews
2. **CODEOWNERS:** Critical files require specific approver review
3. **No Direct Deployment Access:** Agents cannot trigger deployments
4. **Audit Logging:** All agent actions are logged and monitored
5. **Secret Isolation:** Agents never see secrets or credentials
6. **Human-in-the-Loop:** All production changes require manual approval

**Full Details:** See [AGENT_AUTHORIZATION_MODEL.md](./AGENT_AUTHORIZATION_MODEL.md)

### Reporting Agent Security Issues

If you observe suspicious agent behavior:

1. **Document:** Screenshot or copy the behavior
2. **Report:** Use vulnerability reporting channels above
3. **Tag:** Label report as "agent-security"
4. **Urgent:** For active incidents, contact immediately via Discord #alerts

---

## 🔐 Security Best Practices

### For Contributors

When contributing to this project:

- ❌ **NEVER** commit secrets, API keys, or credentials
- ❌ **NEVER** commit kubeconfig files or TLS certificates
- ✅ Use `.env.example` for environment variable templates
- ✅ Use GitHub Secrets for sensitive values in workflows
- ✅ Use Vault references in configurations (e.g., `vault://kv/path`)
- ✅ Review PR diffs for accidental secret exposure before submitting
- ✅ Enable 2FA on your GitHub account

### For Maintainers

When managing this project:

- ✅ Rotate secrets quarterly
- ✅ Review branch protection rules monthly
- ✅ Audit GitHub App permissions quarterly
- ✅ Monitor agent activity for anomalies
- ✅ Keep dependencies up to date
- ✅ Review and approve all Kubernetes manifest changes
- ✅ Require manual approval for production deployments

### Detecting Leaked Secrets

We use automated scanning to detect secrets:

- **Pre-commit hooks:** `.pre-commit-config.yaml`
- **GitHub Actions:** Gitleaks scan on every commit
- **Local scanning:** Run `gitleaks detect --source . --verbose`

If secrets are detected:

1. **Immediately rotate** the exposed secret
2. **Remove from git history** using `git filter-repo` or BFG
3. **Audit access logs** for potential misuse
4. **Document incident** for postmortem

---

## 🛡️ Infrastructure Security

### Kubernetes RBAC

Our Kubernetes deployments use **least-privilege RBAC**:

- Service accounts with minimal permissions
- Network policies for pod isolation
- No `cluster-admin` access for bots
- Resource quotas to prevent exhaustion
- Audit logging enabled

**Configuration:** See `bootstrap/k8s/rbac.yaml`

### Secrets Management

Secrets are managed using:

1. **GitHub Secrets:** For CI/CD workflows
2. **HashiCorp Vault:** For application secrets (recommended)
3. **Kubernetes Secrets:** For pod-level secrets (encrypted at rest)

**Never:**
- ❌ Hardcode secrets in code
- ❌ Log secrets to console or files
- ❌ Store secrets in environment files committed to git

### Network Security

- **Discord Bot:** Egress to Discord API only (HTTPS)
- **Event Gateway:** Ingress with HMAC signature verification
- **Kubernetes:** Network policies restrict inter-pod communication
- **TLS:** All external communication uses TLS 1.2+

---

## 🔍 Security Auditing

### What We Log

- All PR creations, reviews, and merges
- All deployment events (success/failure)
- All kubectl commands executed by CI/CD
- All pod creations/deletions in production namespaces
- All webhook events and API calls

### Where Logs Go

- **GitHub Actions:** Workflow logs (90-day retention)
- **Kubernetes:** Audit logs → Loki
- **Discord:** Notifications to `#alerts` and `#deployments`
- **Prometheus:** Metrics and alerting

### Monitoring & Alerting

We monitor for:

- Unauthorized access attempts
- Failed deployments
- Unusual agent PR volume
- Secret access attempts
- Resource exhaustion
- Pod crash loops

**Alerts go to:** Discord `#alerts`, PagerDuty (production)

---

## 🚨 Incident Response

### Severity Levels

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Active exploit, data breach, production down | Immediate |
| **High** | Potential exploit, elevated risk | 4 hours |
| **Medium** | Vulnerability identified, no active exploit | 24 hours |
| **Low** | Minor issue, low impact | 7 days |

### Response Process

1. **Detect:** Alert triggered or vulnerability reported
2. **Triage:** Assess severity and impact
3. **Contain:** Isolate affected systems, revoke compromised credentials
4. **Eradicate:** Deploy fix, patch vulnerability
5. **Recover:** Restore normal operations, verify fix
6. **Postmortem:** Document incident, improve defenses

### Emergency Contacts

- **Primary:** Domenic Garza (Discord @Strategickhaos)
- **Discord:** #alerts channel
- **Email:** admin@strategickhaos.com

---

## 📚 Additional Security Resources

### Internal Documentation

- [Agent Authorization Model](./AGENT_AUTHORIZATION_MODEL.md) - Agent permissions and boundaries
- [Vault Security Playbook](./VAULT_SECURITY_PLAYBOOK.md) - Secrets management
- [Governance Access Matrix](./governance/access_matrix.yaml) - Role-based access
- [Agent Permissions Config](./governance/agent_permissions.yaml) - Agent-specific permissions

### External References

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Kubernetes Security Checklist](https://kubernetes.io/docs/concepts/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)

---

## ✅ Security Checklist for New Features

Before merging new features:

- [ ] No hardcoded secrets or credentials
- [ ] Secrets use GitHub Secrets or Vault
- [ ] RBAC permissions follow least privilege
- [ ] Network policies updated if new services added
- [ ] Logging and monitoring configured
- [ ] Security tests pass (if applicable)
- [ ] Documentation updated
- [ ] Reviewed by CODEOWNERS

---

## 📞 Questions?

If you have questions about this security policy:

1. **Check:** [AGENT_AUTHORIZATION_MODEL.md](./AGENT_AUTHORIZATION_MODEL.md) for agent-specific questions
2. **Ask:** Discord #agents channel for general questions
3. **Email:** admin@strategickhaos.com for private inquiries

---

**Built with 🔒 by Strategickhaos DAO LLC**  
*Security through transparency, sovereignty through design*
