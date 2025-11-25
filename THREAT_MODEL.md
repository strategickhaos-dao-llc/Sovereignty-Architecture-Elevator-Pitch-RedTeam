# SACSE Adversarial Threat Model

## Overview

This document formalizes the adversarial threat model for the Sovereignty Architecture Cognitive Systems Engineering (SACSE) methodology. It addresses key compromise, model poisoning, supply-chain attacks, insider threats, repository compromise, and network-level attacks with specific mitigations.

---

## 1. Key Compromise

### Threat Description
Compromise of GPG signing keys used for artifact provenance and commit signing could allow adversaries to forge artifacts, impersonate operators, or inject malicious commits into the chain-of-custody.

### Attack Vectors
- Stolen private keys from unencrypted storage
- Keylogger capture during passphrase entry
- Social engineering to obtain key backups
- Memory extraction from compromised systems

### Mitigations

| Control | Implementation | Priority |
|---------|---------------|----------|
| Hardware Security Module (HSM) | Store signing keys in YubiKey 5 or Nitrokey HSM2 | **Critical** |
| Key rotation schedule | Rotate subkeys every 90 days; master key every 2 years | High |
| Passphrase policy | Minimum 20 characters, stored in Vault with MFA | High |
| Revocation certificates | Pre-generate and store offline in sealed envelope | **Critical** |
| Key usage monitoring | Alert on unexpected signing activity via audit logs | Medium |

### Verification Commands
```bash
# Verify GPG key is on hardware token
gpg --card-status

# Check key expiration
gpg --list-keys --with-colons | grep -E "^pub|^sub"

# Verify commit signature
git verify-commit HEAD
```

---

## 2. Model Poisoning

### Threat Description
Adversarial manipulation of LLM training data, fine-tuning datasets, or RAG knowledge bases to embed backdoors, bias outputs, or degrade model performance for specific queries.

### Attack Vectors
- Injection of malicious content into vector stores (Qdrant/pgvector)
- Compromise of artifact corpus (.htm files) before embedding
- Prompt injection through user-supplied context
- Supply-chain poisoning of pre-trained model weights

### Mitigations

| Control | Implementation | Priority |
|---------|---------------|----------|
| Input validation | Sanitize all artifacts before vectorization; reject malformed content | **Critical** |
| Hash verification | Verify SHA256 of all ingested artifacts against manifest | **Critical** |
| Embedding isolation | Namespace RAG collections by trust level; quarantine untrusted | High |
| Output filtering | Apply Constitutional AI guardrails on all LLM outputs | High |
| Model provenance | Only use models with verified checksums from trusted sources | High |
| Drift detection | Monitor embedding distribution for anomalies (KL divergence) | Medium |

### Verification Commands
```bash
# Verify artifact integrity before ingestion
sha256sum -c reproducibility/artifact_hashes.sha256

# Check vector store collection integrity
curl -X GET "http://qdrant:6333/collections/runbooks" | jq '.result.vectors_count'

# Validate model checksum
sha256sum models/*.gguf | diff - models/checksums.sha256
```

---

## 3. Repository Compromise

### Threat Description
Unauthorized modification of source code, configuration, or deployment artifacts through compromised credentials, CI/CD pipeline manipulation, or direct repository access.

### Attack Vectors
- Stolen GitHub App credentials or personal access tokens
- Malicious GitHub Actions in forked workflows
- Branch protection bypass through force push
- Dependency confusion attacks via typosquatting

### Mitigations

| Control | Implementation | Priority |
|---------|---------------|----------|
| Signed commits required | Enforce GPG-signed commits on all protected branches | **Critical** |
| Branch protection | Require PR review + status checks; disable force push | **Critical** |
| Token scoping | Minimum-privilege GitHub tokens; rotate every 30 days | High |
| Action pinning | Pin all GitHub Actions to SHA, not tags | High |
| Dependency verification | Use `npm audit`, `pip-audit`, lockfile verification | High |
| CODEOWNERS | Require approval from designated maintainers for sensitive paths | Medium |

### Verification Commands
```bash
# Verify all commits are signed
git log --show-signature -5

# Check branch protection status via GitHub API
gh api repos/:owner/:repo/branches/main/protection

# Audit GitHub Action versions
grep -r "uses:" .github/workflows/ | grep -v "@[a-f0-9]\{40\}"
```

---

## 4. Supply Chain Attacks

### Threat Description
Compromise of dependencies, container images, or external services that SACSE relies upon, leading to code execution or data exfiltration.

### Attack Vectors
- Malicious npm/pip package updates
- Compromised Docker base images
- Typosquatting on package registries
- Backdoored CI/CD runners

### Mitigations

| Control | Implementation | Priority |
|---------|---------------|----------|
| Lockfile integrity | Commit `package-lock.json`, `requirements.txt` with hashes | **Critical** |
| Image signing | Use Docker Content Trust (DCT) for all container images | High |
| Private registry | Mirror critical dependencies in private registry (Artifactory/Harbor) | High |
| SBOM generation | Generate Software Bill of Materials for each release | Medium |
| Reproducible builds | Ensure builds are deterministic; verify across environments | Medium |

### Verification Commands
```bash
# Verify npm package integrity
npm ci --ignore-scripts && npm audit

# Check Docker image signature
docker trust inspect --pretty ghcr.io/strategickhaos/sovereignty-architecture:latest

# Generate SBOM
syft packages dir:. -o spdx-json > sbom.spdx.json
```

---

## 5. Insider Threats

### Threat Description
Malicious or negligent actions by authorized operators that compromise system integrity, exfiltrate data, or disrupt operations.

### Attack Vectors
- Privilege escalation through role abuse
- Data exfiltration via legitimate access
- Sabotage through destructive commands
- Credential sharing or weak access controls

### Mitigations

| Control | Implementation | Priority |
|---------|---------------|----------|
| Least privilege | Role-based GPG keys; separate signing authorities | **Critical** |
| Audit logging | Comprehensive logging of all privileged operations | **Critical** |
| Separation of duties | Require multiple signers for production changes | High |
| Access review | Quarterly review of all access grants | High |
| Behavioral monitoring | Alert on unusual access patterns or off-hours activity | Medium |

### Access Control Matrix
```yaml
roles:
  operator:
    permissions: [read_logs, query_rag, deploy_dev]
    key_type: subkey_sign_only
  
  maintainer:
    permissions: [operator, approve_pr, deploy_staging]
    key_type: subkey_sign_certify
  
  admin:
    permissions: [maintainer, deploy_prod, rotate_keys, manage_roles]
    key_type: master_key_required
    requires: [mfa, hardware_token]
```

---

## 6. Network-Level Attacks

### Threat Description
Man-in-the-middle attacks, DNS poisoning, or network interception targeting communications between SACSE components, external APIs, or artifact storage.

### Attack Vectors
- TLS downgrade attacks
- DNS hijacking of API endpoints
- BGP hijacking for traffic interception
- Rogue WiFi access points

### Mitigations

| Control | Implementation | Priority |
|---------|---------------|----------|
| TLS 1.3 enforcement | Disable TLS 1.2 and below; configure strong cipher suites | **Critical** |
| Certificate pinning | Pin certificates for critical external APIs (OpenAI, GitHub) | High |
| DNSSEC validation | Enable DNSSEC for all owned domains | High |
| Zero-trust networking | mTLS between all internal services; no implicit trust | High |
| VPN/WireGuard | Require VPN for administrative access | Medium |

### Verification Commands
```bash
# Test TLS configuration
nmap --script ssl-enum-ciphers -p 443 events.strategickhaos.com

# Verify DNSSEC
dig +dnssec strategickhaos.com

# Check mTLS certificate validity
openssl s_client -connect service:443 -cert client.crt -key client.key
```

---

## 7. Mitigation Checklist

### Critical (Implement Immediately)
- [ ] Deploy YubiKey/HSM for GPG signing keys
- [ ] Enable signed commits requirement on all protected branches
- [ ] Hash-verify all artifacts before vectorization
- [ ] Generate and store offline revocation certificates
- [ ] Enforce TLS 1.3 with strong cipher suites
- [ ] Implement comprehensive audit logging

### High Priority (Within 30 Days)
- [ ] Establish 90-day subkey rotation schedule
- [ ] Pin all GitHub Actions to SHA versions
- [ ] Configure Constitutional AI guardrails for LLM outputs
- [ ] Enable Docker Content Trust for image signing
- [ ] Implement role-based access control matrix
- [ ] Set up embedding drift detection monitoring

### Medium Priority (Within 90 Days)
- [ ] Generate SBOM for each release
- [ ] Establish quarterly access review process
- [ ] Configure behavioral anomaly detection
- [ ] Mirror critical dependencies to private registry
- [ ] Enable DNSSEC for all owned domains

---

## 8. Incident Response

### Compromise Response Playbook

1. **Detection**: Alert from audit logs, external report, or anomaly detection
2. **Containment**: Revoke compromised keys/tokens immediately
3. **Analysis**: Determine scope of compromise from audit trails
4. **Eradication**: Remove malicious artifacts; rotate all potentially exposed secrets
5. **Recovery**: Restore from verified backups; re-establish trust anchors
6. **Lessons Learned**: Document incident; update threat model

### Emergency Contacts
```yaml
security_contacts:
  primary: security@strategickhaos.com
  escalation: domenic.garza@snhu.edu
  external_ir: [retained IR firm TBD]

incident_channels:
  discord: "#security-incidents"
  pagerduty: [integration TBD]
```

---

## References

- NIST SP 800-53 Rev. 5: Security and Privacy Controls
- MITRE ATT&CK Framework: Enterprise Matrix
- OWASP LLM Top 10: Security Risks for AI Applications
- CIS Controls v8: Implementation Groups
- Constitutional AI: Anthropic's Approach to AI Safety

---

*Last updated: 2025-11-25*
*Version: 1.0*
*Maintainer: SACSE Security Working Group*
