# SwarmGate Change Policy

**Strategickhaos DAO LLC — SwarmGate 7% Engine Governance**

Version: 1.0.0  
Effective: 2025-11-27  
Last Review: 2025-11-27

## 1. Overview

This document defines the change management procedures for SwarmGate, the Eternal 7% Revenue Split Engine. All modifications to contracts, parameters, or configuration must follow this policy.

## 2. Version Bump Rules

### 2.1 Semantic Versioning

SwarmGate follows semantic versioning (MAJOR.MINOR.PATCH):

| Change Type | Version Bump | Example | Approval Required |
|------------|--------------|---------|-------------------|
| Breaking changes to contract interface | MAJOR | 1.0.0 → 2.0.0 | Full audit + governance vote |
| New features, non-breaking changes | MINOR | 1.0.0 → 1.1.0 | Security review + admin approval |
| Bug fixes, documentation updates | PATCH | 1.0.0 → 1.0.1 | Admin approval |

### 2.2 Version Update Process

1. Create PR with version bump in `swarmgate/status.yaml`
2. Update CHANGELOG entries
3. Generate new checksums
4. Sign release artifacts
5. Obtain required approvals
6. Merge and tag release

## 3. Split Parameter Changes

### 3.1 Immutable Parameters

The following parameters are **immutable** once deployed:

- Total split percentage (7% / 700 basis points)
- Distribution ratios (40/30/20/10)
- Recipient addresses (set at deployment)

> ⚠️ To modify immutable parameters, a new contract must be deployed.

### 3.2 Configurable Parameters

These parameters can be changed via the control plane:

| Parameter | Change Process | Approval |
|-----------|---------------|----------|
| Feature toggles | PR to `swarmgate/config.yaml` | Admin |
| Environment settings | PR to `swarmgate/config.yaml` | Admin |
| Monitoring thresholds | PR to `swarmgate/config.yaml` | Admin |
| Emergency pause | Direct admin action | Admin (emergency) |

### 3.3 Parameter Change Workflow

```
1. Proposal submitted (GitHub Issue)
       ↓
2. Technical review (security implications)
       ↓
3. Governance review (if applicable)
       ↓
4. Implementation PR created
       ↓
5. CI checks pass (build, test, provenance)
       ↓
6. Required approvals obtained
       ↓
7. Merge and deploy
       ↓
8. Post-deployment verification
```

## 4. Signing Keys and Quorum

### 4.1 Authorized Signers

| Role | Name | Key ID | Authority |
|------|------|--------|-----------|
| Primary Signer | Domenic Garza | domenic-garza-gpg | Full deployment authority |
| Emergency Admin | Managing Member | admin-key | Emergency pause/unpause |

### 4.2 Quorum Requirements

| Action | Required Signers | Quorum |
|--------|-----------------|--------|
| Patch release | 1 | 1/1 |
| Minor release | 1 | 1/1 |
| Major release | 1 + external audit | 1/1 + audit sign-off |
| Contract deployment (testnet) | 1 | 1/1 |
| Contract deployment (mainnet) | 1 + verification | 1/1 |
| Emergency pause | 1 | 1/1 |
| Parameter change | 1 | 1/1 |

> **Note**: Single-operator quorum reflects current organizational structure.
> Quorum requirements will be updated as the organization grows.

### 4.3 Key Management

- GPG keys stored in secure hardware (YubiKey recommended)
- Key IDs registered in `governance/access_matrix.yaml`
- Annual key rotation required
- Key compromise procedure documented

## 5. Contract Modification Process

### 5.1 Pre-Modification Checklist

- [ ] Change documented in GitHub Issue
- [ ] Impact assessment completed
- [ ] Security implications reviewed
- [ ] Backward compatibility verified (or breaking change acknowledged)
- [ ] Test coverage adequate

### 5.2 Code Review Requirements

All contract changes require:

1. **Automated checks**: CI must pass (lint, test, build)
2. **Manual review**: At least one reviewer must approve
3. **Security review**: For any logic changes
4. **Audit**: For major changes or new deployments

### 5.3 Deployment Approval

| Environment | Approver | Additional Requirements |
|-------------|----------|------------------------|
| Development | Any maintainer | None |
| Testnet | Admin | Successful dev testing |
| Mainnet | Admin | Testnet verification + audit (major changes) |

## 6. Provenance and Verification

### 6.1 Artifact Checksums

All release artifacts must include SHA-256 checksums:

```bash
# Generate checksums
sha256sum contracts/SwarmGate.sol > swarmgate/checksums.txt

# Verify checksums
sha256sum -c swarmgate/checksums.txt
```

### 6.2 Commit Signing

All commits to protected branches must be GPG signed:

```bash
# Configure signing
git config user.signingkey YOUR_KEY_ID
git config commit.gpgsign true

# Sign commit
git commit -S -m "feat: description"
```

### 6.3 Release Signing

Release tags must be signed:

```bash
# Sign tag
git tag -s swarmgate/v1.0.0 -m "SwarmGate v1.0.0 release"

# Verify tag
git tag -v swarmgate/v1.0.0
```

## 7. Emergency Procedures

### 7.1 Emergency Pause

In case of critical security issues:

1. Admin calls `pause()` on contract
2. Incident documented in GitHub Issue
3. Root cause analysis conducted
4. Fix developed and tested
5. Admin calls `unpause()` after verification

### 7.2 Emergency Contacts

| Role | Contact Method |
|------|---------------|
| Primary Admin | Discord DM / Emergency channel |
| Security Team | security@strategickhaos.com |
| On-call | PagerDuty (if configured) |

## 8. Audit Trail

All changes must be logged:

- Git commit history (signed commits)
- GitHub PR records
- Deployment logs
- Configuration change history

## 9. Policy Updates

This policy may be updated by:

1. Creating PR to modify this document
2. Obtaining admin approval
3. Version bump in document header
4. Announcement in governance channel

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-27 | Strategickhaos | Initial version |
