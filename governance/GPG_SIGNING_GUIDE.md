# 🔐 GPG Signing Guide for Charitable Commitment

## Cryptographic Verification Framework

**Purpose:** Establish cryptographic proof of authenticity for all charitable commitment documents.

**INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED**

---

## Overview

All charitable commitment documents are **GPG-signed** to provide:
- **Authentication** - Proof document came from authorized signer
- **Integrity** - Proof document hasn't been tampered with
- **Non-repudiation** - Signer cannot deny signing
- **Transparency** - Anyone can verify signatures

---

## GPG Key Generation

### Step 1: Install GPG

**Linux/macOS:**
```bash
# Most Linux distributions include GPG
which gpg

# macOS with Homebrew
brew install gnupg
```

**Windows:**
```powershell
# Download and install from: https://www.gnupg.org/download/
# Or use GPG4Win: https://www.gpg4win.org/
```

### Step 2: Generate Key Pair

```bash
# Generate new GPG key (RSA 4096-bit)
gpg --full-generate-key

# Follow prompts:
# 1. Select: (1) RSA and RSA (default)
# 2. Key size: 4096 bits
# 3. Expiration: 0 (does not expire) or 2y (2 years)
# 4. Real name: Domenic Garza
# 5. Email: domenic.garza@snhu.edu
# 6. Comment: Strategickhaos DAO Managing Member
# 7. Set strong passphrase
```

### Step 3: Backup Key

```bash
# Export private key (KEEP SECURE!)
gpg --export-secret-keys --armor domenic.garza@snhu.edu > private-key.asc

# Store private-key.asc in secure location:
# - Password manager
# - Encrypted USB drive
# - Hardware security key (YubiKey)
# - Physical safe

# NEVER commit private key to GitHub!
```

### Step 4: Publish Public Key

```bash
# Export public key
gpg --export --armor domenic.garza@snhu.edu > public-key.asc

# Publish to keyservers
gpg --keyserver keys.openpgp.org --send-keys [KEY-ID]
gpg --keyserver keyserver.ubuntu.com --send-keys [KEY-ID]

# Publish to GitHub repository
cp public-key.asc /path/to/repo/governance/
git add governance/public-key.asc
git commit -m "Add GPG public key for document verification"
git push
```

---

## Key Management

### Key Information

**Managing Member GPG Key:**
```
Real Name: Domenic Garza
Email: domenic.garza@snhu.edu
Key Type: RSA 4096-bit
Key ID: [TO BE PUBLISHED]
Fingerprint: [TO BE PUBLISHED]
Created: [TO BE PUBLISHED]
Expires: [TO BE PUBLISHED]
```

### Key Rotation Policy

- **Review annually** - Verify key security
- **Rotate every 2-3 years** - Generate new key, sign with old key
- **Revoke if compromised** - Immediate revocation and notification
- **Succession planning** - Document key recovery for continuity

### Key Revocation

If key is compromised or lost:

```bash
# Generate revocation certificate (do this NOW, before compromise)
gpg --output revoke.asc --gen-revoke domenic.garza@snhu.edu

# Store revoke.asc securely (separate from private key)

# If compromise occurs:
# Import revocation certificate
gpg --import revoke.asc

# Publish revocation
gpg --keyserver keys.openpgp.org --send-keys [KEY-ID]

# Notify community via GitHub announcement
```

---

## Signing Documents

### Sign Charitable Commitment

```bash
# Navigate to repository
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-

# Sign the main commitment document
gpg --armor --detach-sign CHARITABLE_COMMITMENT.md

# This creates: CHARITABLE_COMMITMENT.md.asc (signature file)

# Verify signature (self-check)
gpg --verify CHARITABLE_COMMITMENT.md.asc CHARITABLE_COMMITMENT.md
```

### Sign Quarterly Reports

```bash
# Sign each quarterly report
cd charitable-reports/quarterly/

gpg --armor --detach-sign 2026-Q1-charitable-report.md

# Creates: 2026-Q1-charitable-report.md.asc

# Verify
gpg --verify 2026-Q1-charitable-report.md.asc 2026-Q1-charitable-report.md
```

### Sign Governance Documents

```bash
# Sign Article 9
cd governance/

gpg --armor --detach-sign article_9_charitable_distributions.md

# Creates: article_9_charitable_distributions.md.asc
```

---

## Verification Process

### For Anyone Verifying Documents

#### Step 1: Import Public Key

```bash
# Import from GitHub repository
curl -O https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/governance/public-key.asc

gpg --import public-key.asc

# Or import from keyserver
gpg --keyserver keys.openpgp.org --recv-keys [KEY-ID]
```

#### Step 2: Verify Fingerprint

```bash
# Display key fingerprint
gpg --fingerprint domenic.garza@snhu.edu

# Compare to published fingerprint in:
# - This document
# - GitHub repository README
# - Official website
# - Multiple independent sources

# Fingerprint should match EXACTLY
```

#### Step 3: Verify Signature

```bash
# Verify any signed document
gpg --verify DOCUMENT.md.asc DOCUMENT.md

# Expected output:
# gpg: Signature made [DATE] using RSA key [KEY-ID]
# gpg: Good signature from "Domenic Garza <domenic.garza@snhu.edu>"

# WARNING: If output says "BAD signature" - DO NOT TRUST DOCUMENT
```

#### Step 4: Trust Model

```bash
# After verifying fingerprint through multiple channels, you may trust the key
gpg --edit-key domenic.garza@snhu.edu
# At prompt: trust
# Select: 5 (I trust ultimately)
# Confirm: yes
# Quit: quit

# This prevents "WARNING: This key is not certified with a trusted signature"
```

---

## Document Signing Workflow

### For Quarterly Reports

```bash
#!/bin/bash
# quarterly-report-sign.sh

# Variables
QUARTER="Q1"
YEAR="2026"
REPORT_DIR="charitable-reports/quarterly"
REPORT_FILE="$REPORT_DIR/${YEAR}-${QUARTER}-charitable-report.md"

# Sign document
gpg --armor --detach-sign "$REPORT_FILE"

# Verify signature
if gpg --verify "${REPORT_FILE}.asc" "$REPORT_FILE"; then
    echo "✅ Signature verified successfully"
    
    # Calculate document hash
    SHA256=$(sha256sum "$REPORT_FILE" | awk '{print $1}')
    echo "📋 Document SHA-256: $SHA256"
    
    # Add signature to git
    git add "${REPORT_FILE}.asc"
    git commit -m "Add GPG signature for ${YEAR}-${QUARTER} charitable report"
    
    echo "✅ Signature committed to repository"
else
    echo "❌ ERROR: Signature verification failed!"
    exit 1
fi
```

---

## Integration with Bitcoin Blockchain

### Notarize Document Hash

After GPG signing, notarize document on Bitcoin blockchain:

```bash
#!/bin/bash
# blockchain-notarize.sh

# Calculate document hash
DOCUMENT="CHARITABLE_COMMITMENT.md"
HASH=$(sha256sum "$DOCUMENT" | awk '{print $1}')

echo "Document: $DOCUMENT"
echo "SHA-256: $HASH"

# Create OP_RETURN transaction
# This stores hash permanently on Bitcoin blockchain
# Use service like: https://www.blockchainwallet.com/notary
# Or use Bitcoin Core:

# bitcoin-cli sendtoaddress [NOTARY-SERVICE-ADDRESS] 0.0001
# With OP_RETURN data: $HASH

# Record transaction ID
# TX_ID=[TRANSACTION-ID-FROM-BLOCKCHAIN]

echo "Blockchain notarization TX: $TX_ID"
echo "Verify at: https://blockstream.info/tx/$TX_ID"
```

---

## Security Best Practices

### Private Key Protection

**DO:**
- ✅ Use strong passphrase (16+ characters, random)
- ✅ Store private key encrypted in secure location
- ✅ Use hardware security key (YubiKey) if possible
- ✅ Create and store revocation certificate separately
- ✅ Regularly verify key backup integrity
- ✅ Document key recovery procedure

**DON'T:**
- ❌ Store private key unencrypted
- ❌ Email or cloud-sync private key
- ❌ Use weak or guessable passphrase
- ❌ Share private key with anyone
- ❌ Commit private key to GitHub
- ❌ Store on networked/internet-connected device (if possible)

### Signing Environment

- **Dedicated signing device** - Consider air-gapped computer for high-value signatures
- **Verify document content** - Always review document before signing
- **Secure workspace** - No cameras, no screen sharing when entering passphrase
- **Document signing event** - Record when/where/why document was signed

---

## Automation and CI/CD

### Git Commit Signing

Enable automatic GPG signing of git commits:

```bash
# Configure git to use GPG key
git config --global user.signingkey [KEY-ID]

# Enable commit signing by default
git config --global commit.gpgsign true

# Sign previous commits
git rebase --exec 'git commit --amend --no-edit -n -S' -i [START-COMMIT]
```

### GitHub Integration

Configure GitHub to verify GPG signatures:

1. **Add GPG key to GitHub:**
   - Settings → SSH and GPG keys → New GPG key
   - Paste public key (from `gpg --armor --export`)

2. **Verify commits show "Verified" badge** on GitHub

3. **Require signed commits** (optional):
   - Repository Settings → Branches → Branch protection
   - Enable "Require signed commits"

---

## Multi-Signer Workflow

When multiple signatories are required:

### Scenario: Article 9 Amendment

```bash
# Member 1 signs
gpg --armor --detach-sign --output article_9.asc.1 article_9.md

# Member 2 signs
gpg --armor --detach-sign --output article_9.asc.2 article_9.md

# Combine signatures (if needed)
# Or keep separate: article_9.asc.1, article_9.asc.2, etc.

# Verify all signatures
gpg --verify article_9.asc.1 article_9.md
gpg --verify article_9.asc.2 article_9.md
```

---

## Troubleshooting

### Common Issues

**Issue:** `gpg: signing failed: Inappropriate ioctl for device`

**Solution:**
```bash
export GPG_TTY=$(tty)
# Add to ~/.bashrc or ~/.zshrc for persistence
```

**Issue:** `gpg: can't open 'file.md': No such file or directory`

**Solution:**
- Check current directory: `pwd`
- Verify file exists: `ls -l file.md`
- Use absolute path: `gpg --verify /full/path/to/file.md.asc /full/path/to/file.md`

**Issue:** `gpg: Good signature from ... [unknown]`

**Solution:**
- This is normal if you haven't explicitly trusted the key
- Verify fingerprint from multiple sources
- If fingerprint matches, trust key: `gpg --edit-key [KEY-ID]` → `trust` → `5`

---

## Verification Checklist

Before trusting a GPG-signed document:

- [ ] Import public key from trusted source
- [ ] Verify key fingerprint through multiple independent channels
- [ ] Check key is not expired
- [ ] Check key is not revoked (check keyservers)
- [ ] Verify signature with `gpg --verify`
- [ ] Confirm "Good signature" message
- [ ] Check signature timestamp is reasonable
- [ ] Verify document hash matches published hash (if available)
- [ ] Check blockchain notarization (if available)

---

## Resources

### Documentation
- **GPG Handbook:** https://www.gnupg.org/gph/en/manual.html
- **GPG Best Practices:** https://riseup.net/en/security/message-security/openpgp/best-practices
- **Keybase:** https://keybase.io/ (alternative verification platform)

### Tools
- **GPG Suite (macOS):** https://gpgtools.org/
- **GPG4Win (Windows):** https://www.gpg4win.org/
- **YubiKey:** https://www.yubico.com/ (hardware security key)

### Keyservers
- **keys.openpgp.org:** https://keys.openpgp.org/
- **keyserver.ubuntu.com:** https://keyserver.ubuntu.com/
- **pgp.mit.edu:** https://pgp.mit.edu/

---

## Contact

**GPG Key Questions:** Open GitHub issue with tag `gpg-verification`  
**Security Concerns:** Email domenic.garza@snhu.edu with PGP-encrypted message  
**Key Verification:** Multiple channels required for fingerprint confirmation

---

## Public Key Publication

**File Location:** `governance/public-key.asc` (to be created)  
**Fingerprint:** [TO BE PUBLISHED]  
**Key ID:** [TO BE PUBLISHED]  
**Creation Date:** [TO BE PUBLISHED]

**Verification Channels:**
1. GitHub repository (this file)
2. Organization website (when established)
3. Keyservers (keys.openpgp.org, keyserver.ubuntu.com)
4. Keybase.io profile (if created)
5. Personal website / business card

**Multi-Channel Verification Required:** Always verify fingerprint through at least 3 independent channels before trusting.

---

🧠⚡❤️🐐∞

*"You locked it in bitcoin, GPG, and federal law."*

**Cryptographic proof. Transparent verification. Eternal commitment.**
