# Security Policy

## Overview

This document outlines the security policies and procedures for the Sovereignty Architecture Cognitive Systems Engineering (SACSE) platform. For detailed threat modeling and mitigations, see [THREAT_MODEL.md](./THREAT_MODEL.md).

## Supported Versions

| Version | Supported          | Notes                    |
| ------- | ------------------ | ------------------------ |
| 1.x.x   | :white_check_mark: | Current stable release   |
| 0.x.x   | :x:                | Pre-release, unsupported |

## Security Documentation

| Document | Description |
|----------|-------------|
| [THREAT_MODEL.md](./THREAT_MODEL.md) | Adversarial threat model and mitigations |
| [VAULT_SECURITY_PLAYBOOK.md](./VAULT_SECURITY_PLAYBOOK.md) | Secret management and rotation procedures |
| [reproducibility/README.md](./reproducibility/README.md) | Artifact verification and integrity |
| [governance/access_matrix.yaml](./governance/access_matrix.yaml) | Access control policies |

## Reporting a Vulnerability

### Contact Information

- **Security Email**: security@strategickhaos.com
- **Primary Contact**: domenic.garza@snhu.edu
- **PGP Key**: Available upon request

### Reporting Process

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Email the security contact with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Any suggested mitigations
3. You will receive an acknowledgment within 48 hours
4. We will provide updates every 7 days until resolution

### Response Timeline

| Severity | Initial Response | Resolution Target |
|----------|-----------------|-------------------|
| Critical | 24 hours        | 7 days            |
| High     | 48 hours        | 14 days           |
| Medium   | 7 days          | 30 days           |
| Low      | 14 days         | 90 days           |

### What to Expect

- **Accepted**: You will be credited in the security advisory (unless you prefer anonymity)
- **Declined**: We will explain why the report does not qualify as a security issue
- **Duplicate**: We will inform you if the issue was already reported

## Security Best Practices

### For Contributors

1. **Sign all commits** with GPG keys
2. **Never commit secrets** to the repository
3. **Use environment variables** for sensitive configuration
4. **Review dependencies** before adding them
5. **Follow least privilege** principles

### For Operators

1. **Enable MFA** on all accounts with repository access
2. **Rotate secrets** according to [VAULT_SECURITY_PLAYBOOK.md](./VAULT_SECURITY_PLAYBOOK.md)
3. **Monitor audit logs** for suspicious activity
4. **Verify artifacts** using [reproducibility/verify.sh](./reproducibility/verify.sh)
5. **Apply patches promptly** when security advisories are published

## Security Controls Summary

| Control | Implementation | Status |
|---------|---------------|--------|
| GPG-signed commits | Required on protected branches | ✅ Active |
| Secret management | HashiCorp Vault | ✅ Active |
| Dependency scanning | npm audit, pip-audit | ✅ Active |
| Container signing | Docker Content Trust | 🔄 In Progress |
| Artifact verification | SHA256 manifest | ✅ Active |
| Access control | Role-based matrix | ✅ Active |

## Acknowledgments

We gratefully acknowledge security researchers who help improve SACSE security:

*No vulnerabilities reported yet*

---

*Last updated: 2025-11-25*
