# Key Custody and Recovery Procedures

**CONFIDENTIAL - AUTHORIZED PERSONNEL ONLY**

This document outlines the procedures for managing the Strategickhaos Sovereignty Architecture signing keys, including custody, recovery, and revocation protocols.

## Key Overview

| Key | Purpose | Algorithm | Location |
|-----|---------|-----------|----------|
| Primary Signing Key | Release signatures | RSA-4096 | Air-gapped HSM |
| Backup Key | Disaster recovery | RSA-4096 | Encrypted cold storage |
| Revocation Certificate | Key compromise response | N/A | Secure vault |

## Key Custody Model

### Multi-Person Control

The primary signing key uses **M-of-N threshold control**:
- **N = 3** total key custodians
- **M = 2** required for any key operation
- No single person can access the full key

### Custodian Requirements

Each key custodian must:
1. Complete security training annually
2. Use hardware security keys for authentication
3. Store key shares in geographically separate locations
4. Report any suspected compromise immediately

## Signing Procedures

### Standard Release Signing

1. **Prepare release** on air-gapped workstation
2. **Verify archive hash** before signing
3. **Create detached signature**: `gpg --detach-sign -a archive.tar.gz`
4. **Transfer signature** via QR code or USB (never network)
5. **Verify signature** on separate machine before publishing

### Emergency Signing

If normal procedures cannot be followed:
1. Document the emergency circumstances
2. Notify all custodians
3. Use backup signing key
4. Publish explanation with release

## Recovery Procedures

### Scenario 1: Lost Key Share

If a single custodian loses their key share:

1. **Verify identity** of the custodian reporting loss
2. **Revoke the lost share** using remaining M shares
3. **Generate new share** for replacement custodian
4. **Update key share registry**
5. **No key rotation required** (threshold not compromised)

### Scenario 2: Key Compromise Suspected

If key compromise is suspected:

1. **IMMEDIATELY**:
   - Publish revocation certificate
   - Notify community via multiple channels
   - Halt all signing operations

2. **WITHIN 24 HOURS**:
   - Convene emergency custodian meeting
   - Assess scope of compromise
   - Begin key rotation procedure

3. **WITHIN 7 DAYS**:
   - Generate new signing key
   - Update all public key references
   - Re-sign recent releases with new key
   - Publish post-incident report

### Scenario 3: Disaster Recovery

If primary signing infrastructure is unavailable:

1. **Retrieve backup key** from cold storage
2. **Decrypt using custodian quorum**
3. **Verify key fingerprint** against published records
4. **Resume signing operations**
5. **Document the recovery event**

## Revocation Certificate

The revocation certificate is stored:

1. **Primary**: Physical safe at [REDACTED LOCATION]
2. **Secondary**: Bank safety deposit box at [REDACTED]
3. **Tertiary**: Encrypted in attorney escrow

### Publishing Revocation

To revoke the signing key:

```bash
# Import revocation certificate
gpg --import revocation.asc

# Upload to keyservers
gpg --keyserver keyserver.ubuntu.com --send-keys 0x137SOVEREIGN

# Publish announcement
# - GitHub repository SECURITY.md
# - Project website
# - Mailing list
# - Social media channels
```

## Backup Procedures

### Key Material Backups

| Material | Format | Locations | Rotation |
|----------|--------|-----------|----------|
| Private key (encrypted) | GPG-encrypted file | 3 USB drives | Never |
| Key shares | Paper (QR codes) | 3 separate vaults | On custodian change |
| Revocation cert | Paper + digital | 3 locations | Never (one-time) |
| Passphrase | Memory only | N/A | Never share |

### Backup Verification

Quarterly backup verification:
1. Retrieve one backup copy
2. Verify decryption succeeds
3. Verify key fingerprint matches
4. Return to secure storage
5. Log verification in audit trail

## Security Requirements

### Air-Gapped Workstation

The signing workstation must:
- Never connect to any network
- Use verified boot (Tails or similar)
- Wipe all storage after each use
- Be physically secured when not in use

### Transfer Methods

Approved methods for transferring data to/from air-gapped system:
- **QR codes** (preferred for small data)
- **USB drive** (single-use, destroyed after)
- **SD card** (single-use, destroyed after)

**NEVER** use:
- Network connections
- Bluetooth
- NFC
- Audio/visual steganography

## Audit Trail

All key operations must be logged:

```yaml
operation_log:
  - timestamp: "2025-11-27T00:00:00Z"
    operation: "release_signing"
    custodians: ["custodian_1", "custodian_2"]
    artifact: "swarmgate_v1.0.tar.gz"
    signature: "swarmgate_v1.0.tar.gz.sig"
    hash_blake3: "<hash>"
    witnesses: ["witness_1"]
```

Logs are:
- Signed by all participating custodians
- Stored in append-only ledger
- Replicated to multiple locations

## Contact Information

### Key Custodians

| Role | Contact | Backup Contact |
|------|---------|----------------|
| Primary | security@strategickhaos.com | [REDACTED] |
| Secondary | [REDACTED] | [REDACTED] |
| Tertiary | [REDACTED] | [REDACTED] |

### Emergency Contacts

- **Security Hotline**: [REDACTED]
- **Legal Counsel**: [REDACTED]
- **Technical Lead**: [REDACTED]

## Document Control

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2025-11-27 | Strategickhaos | Initial version |

---

**This document is signed and notarized. Any modification requires approval from the custodian quorum.**

---

*Strategickhaos DAO LLC - Sovereignty Architecture*
*"Cryptographic verification, decentralized custody, sovereign control."*
