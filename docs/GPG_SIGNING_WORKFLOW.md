# GPG Signing Workflow

**Cryptographic Document Verification for Strategickhaos DAO**

This document describes the GPG signing workflow used to establish provenance, integrity, and non-repudiation for critical documents in the Strategickhaos ecosystem.

## Purpose

GPG (GNU Privacy Guard) signing provides:

- **Proof of authorship** - Cryptographically verifies document origin
- **Integrity verification** - Detects any modification after signing
- **Non-repudiation** - Author cannot deny having signed the document
- **Timestamp anchoring** - When combined with OpenTimestamps, provides provable existence at a point in time

## Signing Workflow

### Prerequisites

1. **GPG Key Pair** - Generate or import your signing key
2. **Kleopatra** (Windows) or `gpg` CLI - For signing operations
3. **Key published to keyserver** - For third-party verification

### Document Categories Requiring Signatures

| Document Type | Required | Purpose |
|--------------|----------|---------|
| Research publications (Zenodo) | ✅ | Prior art establishment |
| Legal entity proofs (Bizapedia) | ✅ | Corporate identity verification |
| USPTO submissions | ✅ | Patent filing provenance |
| Commit signatures | ✅ | Code authorship verification |
| DAO governance decisions | ✅ | Voting/approval audit trail |

### Signing with Kleopatra (Windows)

1. Open Kleopatra
2. Select **Sign/Encrypt Files**
3. Choose file(s) to sign
4. Select your signing key
5. Choose output format:
   - `.asc` - ASCII-armored detached signature
   - `.sig` - Binary detached signature
6. Click **Sign**

### Signing with GPG CLI

```bash
# Detached ASCII signature (recommended)
gpg --armor --detach-sign document.pdf

# Creates: document.pdf.asc

# Verify signature
gpg --verify document.pdf.asc document.pdf
```

### Verification Script

The repository includes `hooks/require_gpg.sh` for automated verification:

```bash
# Verify a signed document
./hooks/require_gpg.sh document.pdf.asc

# Output on success:
# ✅ Valid GPG signature from: Signer Name <signer@example.com>
#    File: document.pdf
#    Signature: document.pdf.asc
```

## Git Commit Signing

### Configuration

```bash
# Set signing key
git config --global user.signingkey YOUR_KEY_ID

# Enable automatic commit signing
git config --global commit.gpgsign true

# Enable tag signing
git config --global tag.gpgsign true
```

### Signed Commits

```bash
# Sign a commit manually
git commit -S -m "Your commit message"

# Verify commit signature
git log --show-signature
```

## Integration with Defensive Publication

### Prior Art Protection Chain

1. **Create document** → Research, specification, or proof
2. **GPG sign** → Establishes authorship
3. **Git commit** → Records in immutable history
4. **OpenTimestamps** → Bitcoin-anchored timestamp
5. **Publish/archive** → Zenodo, arXiv, or repository

### Timestamp Workflow

```bash
# Install OpenTimestamps
pip install opentimestamps-client

# Timestamp a signed document
ots stamp document.pdf.asc

# Creates: document.pdf.asc.ots

# Verify timestamp (after Bitcoin confirmation)
ots verify document.pdf.asc.ots
```

## Key Management Best Practices

### Key Security

- [ ] Store private key in secure location
- [ ] Use strong passphrase
- [ ] Keep offline backup of private key
- [ ] Set key expiration date (1-2 years recommended)
- [ ] Publish public key to keyservers

### Keyserver Publication

```bash
# Send to keyserver
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_KEY_ID

# Or upload directly at:
# https://keys.openpgp.org/upload
```

### Key Revocation

In case of compromise:

```bash
# Generate revocation certificate (do this at key creation)
gpg --gen-revoke YOUR_KEY_ID > revoke.asc

# If needed, import and publish revocation
gpg --import revoke.asc
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_KEY_ID
```

## Document Signing Checklist

Before USPTO filing or publication:

- [ ] Document finalized and reviewed
- [ ] GPG signature created (`.asc` file)
- [ ] Signature verified with `require_gpg.sh`
- [ ] Committed to Git with signed commit
- [ ] OpenTimestamps proof generated
- [ ] Backup stored in encrypted location

## Flow State Execution Pattern

For efficient signing during high-focus periods:

```
┌─────────────────────────────────────────┐
│         FLOW STATE SIGNING              │
├─────────────────────────────────────────┤
│ 1. Queue documents in Kleopatra         │
│ 2. Batch sign all queued items          │
│ 3. Commit signatures to Git             │
│ 4. Timestamp batch with OpenTimestamps  │
│ 5. Push to remote repository            │
└─────────────────────────────────────────┘
```

This pattern enables parallel execution across:
- Research document signing
- USPTO preparation
- Corporate proof verification
- Code commit signing

## Verification Resources

- **Key fingerprint**: Verify via [keys.openpgp.org](https://keys.openpgp.org)
- **Repository verification**: `hooks/require_gpg.sh`
- **Timestamp verification**: `ots verify <file>.ots`

---

**Primary Key**: Contact repository owner for public key fingerprint  
**Entity**: Strategickhaos DAO LLC  
**Contact**: See [dao_record.yaml](../dao_record.yaml) for entity contact information
