# GPG Signature Guide for AI Conversation Ledgers

**Purpose:** This guide shows you how to use GPG (GNU Privacy Guard) to cryptographically sign your AI conversation ledgers, providing non-repudiation and authenticity.

**Legal Benefit:** GPG signatures demonstrate that you (and only you) created the ledger at a specific time, preventing you from later claiming "I didn't write that."

**Cost:** $0  
**Time:** 30 minutes initial setup, 2 minutes per signing thereafter

---

## Table of Contents

1. [What is GPG and Why Use It?](#what-is-gpg-and-why-use-it)
2. [Installation](#installation)
3. [Creating Your GPG Key](#creating-your-gpg-key)
4. [Signing Your Ledger](#signing-your-ledger)
5. [Verifying Signatures](#verifying-signatures)
6. [Git Integration](#git-integration)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## What is GPG and Why Use It?

### GPG (GNU Privacy Guard)
- Open-source implementation of OpenPGP standard
- Used for cryptographic signing and encryption
- Creates digital signatures that prove authenticity

### Legal Benefits

1. **Non-repudiation:** Once you sign a document, you cannot credibly claim you didn't create it
2. **Integrity:** Any tampering with the document after signing is immediately detectable
3. **Authentication:** Proves the document came from you specifically
4. **Timestamp:** Signing time is embedded in the signature

### Use Cases for Ledger Signing

- **Patent prosecution:** Prove you documented an invention on a specific date
- **Trade secret protection:** Show contemporaneous documentation of proprietary processes
- **Contract disputes:** Authenticate your records against challenges
- **Regulatory compliance:** Demonstrate audit trail integrity

---

## Installation

### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install gnupg
```

### Linux (RHEL/CentOS/Fedora)
```bash
sudo yum install gnupg2
```

### macOS
```bash
brew install gnupg
```

### Windows
1. Download [Gpg4win](https://gpg4win.org/)
2. Run installer
3. Add to PATH: `C:\Program Files (x86)\GnuPG\bin`

### Verify Installation
```bash
gpg --version
```

Expected output:
```
gpg (GnuPG) 2.x.x
...
```

---

## Creating Your GPG Key

### Step 1: Generate Key Pair

```bash
gpg --full-generate-key
```

### Step 2: Follow Prompts

```
Please select what kind of key you want:
   (1) RSA and RSA (default)
   
Your selection? 1

RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096

Key is valid for? (0) 0
Key does not expire at all
Is this correct? (y/N) y

Real name: Domenic Garza
Email address: domenic.garza@snhu.edu
Comment: Strategickhaos DAO LLC - Evidence Signing Key
```

**IMPORTANT:** Use your real name and primary email address. This will be visible in signatures.

### Step 3: Set Strong Passphrase

Choose a strong passphrase (12+ characters, mix of upper/lower/numbers/symbols).

**Security Note:** Your passphrase protects your private key. If compromised, someone could forge your signatures.

### Step 4: Verify Key Creation

```bash
gpg --list-keys
```

Output:
```
pub   rsa4096 2025-11-21 [SC]
      ABCD1234EFGH5678IJKL9012MNOP3456QRST7890
uid           [ultimate] Domenic Garza (Strategickhaos DAO LLC - Evidence Signing Key) <domenic.garza@snhu.edu>
sub   rsa4096 2025-11-21 [E]
```

**Save your key fingerprint:** `ABCD1234EFGH5678IJKL9012MNOP3456QRST7890`

---

## Signing Your Ledger

### Method 1: Detached Signature (Recommended)

Creates a separate `.asc` file alongside your ledger.

```bash
# Sign the ledger
gpg --detach-sign --armor conversation_ledger.yaml

# Creates: conversation_ledger.yaml.asc
```

**Advantages:**
- Original file remains unchanged
- Signature file can be distributed separately
- Standard practice for software releases

### Method 2: Clear-text Signature

Wraps the ledger content with signature markers.

```bash
gpg --clearsign conversation_ledger.yaml

# Creates: conversation_ledger.yaml.asc (contains both content and signature)
```

**Advantages:**
- Single file contains both data and signature
- Human-readable
- Good for email transmission

### Method 3: Inline Signature in YAML

Add signature directly to the YAML file.

```bash
# Sign and capture signature
gpg --detach-sign --armor conversation_ledger.yaml
SIG=$(cat conversation_ledger.yaml.asc)

# Add to YAML (using yq or manually)
yq eval ".integrity.gpg_signature = \"$SIG\"" -i conversation_ledger.yaml
```

### Recommended Workflow

```bash
#!/bin/bash
# sign_ledger.sh - Automated signing script

LEDGER_FILE="conversation_ledger.yaml"

# 1. Sign with detached signature
gpg --detach-sign --armor "$LEDGER_FILE"

# 2. Compute SHA3-256 hash
SHA256=$(sha256sum "$LEDGER_FILE" | cut -d' ' -f1)

# 3. Update ledger with hash and signature metadata
yq eval ".integrity.current_ledger_hash = \"$SHA256\"" -i "$LEDGER_FILE"
yq eval ".integrity.gpg_signature = \"$(cat ${LEDGER_FILE}.asc)\"" -i "$LEDGER_FILE"

# 4. Get key fingerprint
FINGERPRINT=$(gpg --list-keys --with-colons | grep fpr | head -1 | cut -d: -f10)
yq eval ".integrity.gpg_key_fingerprint = \"$FINGERPRINT\"" -i "$LEDGER_FILE"

echo "✓ Ledger signed successfully"
echo "  Hash: $SHA256"
echo "  Fingerprint: $FINGERPRINT"
echo "  Signature: ${LEDGER_FILE}.asc"
```

---

## Verifying Signatures

### Verify Detached Signature

```bash
gpg --verify conversation_ledger.yaml.asc conversation_ledger.yaml
```

**Good signature output:**
```
gpg: Signature made Thu 21 Nov 2025 02:30:00 PM UTC
gpg:                using RSA key ABCD1234EFGH5678IJKL9012MNOP3456QRST7890
gpg: Good signature from "Domenic Garza (Strategickhaos DAO LLC - Evidence Signing Key) <domenic.garza@snhu.edu>" [ultimate]
```

**Tampered file output:**
```
gpg: BAD signature from "Domenic Garza ..."
```

### Verify Clear-text Signature

```bash
gpg --verify conversation_ledger.yaml.asc
```

### Export Public Key for Third-Party Verification

```bash
# Export your public key
gpg --armor --export domenic.garza@snhu.edu > public_key.asc

# Others can import and verify:
gpg --import public_key.asc
gpg --verify conversation_ledger.yaml.asc conversation_ledger.yaml
```

### Publish to Key Server (Optional)

```bash
# Publish to public keyserver
gpg --keyserver keyserver.ubuntu.com --send-keys YOUR_KEY_ID

# Others can then download:
gpg --keyserver keyserver.ubuntu.com --recv-keys YOUR_KEY_ID
```

**Legal Benefit:** Public key publication provides third-party timestamp and public record.

---

## Git Integration

### Configure Git to Sign Commits

```bash
# Set your GPG key for git
git config --global user.signingkey YOUR_KEY_ID

# Enable automatic signing
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

### Sign Individual Commits

```bash
# Manually sign a commit
git commit -S -m "Add conversation entry for 2025-11-21 session"

# Sign a tag
git tag -s v1.0.0 -m "Release version 1.0.0"
```

### Verify Signed Commits

```bash
# Show signature info
git log --show-signature

# Verify specific commit
git verify-commit HEAD
```

### GitHub Integration

1. Add GPG key to GitHub:
   - Settings → SSH and GPG keys → New GPG key
   - Paste your public key (from `gpg --armor --export`)

2. GitHub will show "Verified" badge on signed commits

**Legal Benefit:** GitHub's third-party verification adds credibility to your signatures.

---

## Best Practices

### Key Management

1. **Backup Your Private Key**
   ```bash
   # Export private key (KEEP SECURE!)
   gpg --export-secret-keys --armor your@email.com > private-key-backup.asc
   
   # Store in multiple secure locations:
   # - Encrypted USB drive (offline)
   # - Password manager (encrypted)
   # - Safe deposit box (paper backup)
   ```

2. **Backup Revocation Certificate**
   ```bash
   # Generate revocation certificate
   gpg --gen-revoke your@email.com > revoke.asc
   
   # Store securely (use if key is compromised)
   ```

3. **Set Expiration Date (Optional)**
   ```bash
   # Edit key to add expiration
   gpg --edit-key your@email.com
   gpg> expire
   # Choose duration (e.g., 2 years)
   gpg> save
   ```

### Signing Workflow

1. **Sign contemporaneously:** Sign the ledger on the same day you create entries
2. **Sign before committing:** Add signature, then commit to git
3. **Version control signatures:** Keep `.asc` files in git alongside ledgers
4. **Regular timestamps:** Re-sign monthly to establish ongoing timestamps

### Documentation

Include this in your ledger's README:

```markdown
## GPG Signature Verification

This ledger is signed with GPG key: `ABCD1234EFGH5678IJKL9012MNOP3456QRST7890`

To verify:
1. Import public key: `gpg --import public_key.asc`
2. Verify signature: `gpg --verify conversation_ledger.yaml.asc`

Public key also available at:
- Keyserver: keyserver.ubuntu.com
- GitHub: https://github.com/yourusername.gpg
```

---

## Troubleshooting

### "gpg: signing failed: Inappropriate ioctl for device"

**Solution:**
```bash
export GPG_TTY=$(tty)
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
```

### "No secret key" Error

**Problem:** Private key not found  
**Solution:**
```bash
# List secret keys
gpg --list-secret-keys

# If missing, import backup:
gpg --import private-key-backup.asc
```

### Git Signing Not Working

**Solution:**
```bash
# Tell git where to find gpg
git config --global gpg.program gpg2

# Or specify full path:
git config --global gpg.program /usr/bin/gpg
```

### Forgotten Passphrase

**Problem:** Cannot sign without passphrase  
**Solution:** No recovery possible. You must:
1. Revoke old key (if you have revocation certificate)
2. Generate new key
3. Re-sign all documents with new key

**Prevention:** Store passphrase in password manager with recovery options.

---

## Legal Integration

### In Sworn Declarations

When referencing GPG signatures in legal documents:

```markdown
10.1. I have signed the Ledger file with my GPG key (fingerprint: 
ABCD1234EFGH5678IJKL9012MNOP3456QRST7890), which is registered on 
public keyservers and GitHub, allowing independent verification of the 
signature's authenticity.

10.2. The signature was created contemporaneously with the ledger entries,
as evidenced by the signature timestamp of [DATE].

10.3. My GPG private key is secured with a strong passphrase and has never
been compromised or disclosed to any third party.
```

### In Evidence Presentation

```markdown
## Exhibit C: GPG Signature Verification

1. Public Key: [Attached as public_key.asc]
2. Signature File: [Attached as conversation_ledger.yaml.asc]
3. Verification Command: `gpg --verify conversation_ledger.yaml.asc`
4. Expected Output: "Good signature from [Your Name]"

The GPG signature proves:
- The document was signed by the holder of the private key
- The document has not been altered since signing
- The signature was created on [DATE] at [TIME]
```

---

## Cost-Benefit Summary

| Activity | Time | Cost | Legal Benefit |
|----------|------|------|---------------|
| Initial setup | 30 min | $0 | None (prerequisite) |
| Sign each ledger | 2 min | $0 | Medium (non-repudiation) |
| Git integration | 15 min | $0 | Medium (timestamp + tamper-evidence) |
| Publish to keyserver | 5 min | $0 | Low (public record) |
| **Total** | **52 min** | **$0** | **Medium-High** |

**ROI:** Minimal time investment provides substantial legal protection at zero cost.

---

## Related Resources

- [Appendix C: Legal Status of AI-Generated Evidence](../APPENDIX_C_LEGAL_STATUS_AI_EVIDENCE.md)
- [Conversation Evidence Schema](../templates/conversation_evidence_schema.yaml)
- [Sworn Declaration Template](../templates/sworn_declaration_template.md)
- [OpenTimestamps Guide](OPENTIMESTAMPS_GUIDE.md)
- [GnuPG Official Documentation](https://gnupg.org/documentation/)

---

**Document Version:** 1.0.0  
**Last Updated:** November 21, 2025  
**Maintained By:** Strategickhaos DAO LLC
