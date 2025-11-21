# Appendix C.1: GPG Signature Guide and Commands

**Purpose:** Cryptographically sign AI conversation ledger entries to prove authorship and integrity  
**Last Updated:** November 2025  
**Skill Level:** Intermediate (step-by-step instructions provided)

---

## Overview

GPG (GNU Privacy Guard) digital signatures provide:
- **Authentication:** Proves you created the document
- **Integrity:** Proves the document hasn't been altered
- **Non-repudiation:** You cannot later deny creating the document
- **Timestamp:** Shows when the signature was created

**Legal Value:** GPG signatures are recognized by courts worldwide as reliable authentication methods, approaching the level of "advanced electronic signatures" under eIDAS and similar frameworks.

---

## Initial Setup (One-Time)

### 1. Install GPG

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install gnupg
```

**macOS (with Homebrew):**
```bash
brew install gnupg
```

**Windows:**
Download from https://www.gpg4win.org/

**Verify Installation:**
```bash
gpg --version
```

### 2. Generate Your GPG Key Pair

**Generate Key:**
```bash
gpg --full-generate-key
```

**Interactive Prompts:**
1. **Key type:** Select `(1) RSA and RSA` (default)
2. **Key size:** Enter `4096` (maximum security)
3. **Expiration:** Enter `0` (key does not expire) or `2y` (expires in 2 years)
4. **Real name:** Enter your full legal name: `Domenic Garza`
5. **Email:** Enter your primary email: `domenic.garza@snhu.edu`
6. **Comment:** Optional, e.g., `Strategickhaos DAO - R&D`
7. **Passphrase:** **CRITICAL** - Choose a strong passphrase and store it securely

**Expected Output:**
```
pub   rsa4096 2025-11-21 [SC]
      1234567890ABCDEF1234567890ABCDEF12345678
uid           Domenic Garza (Strategickhaos DAO - R&D) <domenic.garza@snhu.edu>
sub   rsa4096 2025-11-21 [E]
```

**Save Your Key ID:**
```bash
# List your keys
gpg --list-secret-keys --keyid-format LONG

# Example output:
# sec   rsa4096/0x1234567890ABCDEF 2025-11-21 [SC]
#       Key fingerprint = 1234 5678 90AB CDEF 1234  5678 90AB CDEF 1234 5678
# uid                   Domenic Garza <domenic.garza@snhu.edu>

# Your Key ID is: 0x1234567890ABCDEF
```

**Export Your Public Key (for verification by others):**
```bash
gpg --armor --export domenic.garza@snhu.edu > domenic_garza_public_key.asc
```

### 3. Configure Git to Use Your GPG Key

**Set GPG Key for Git:**
```bash
# Replace with your actual key ID
git config --global user.signingkey 0x1234567890ABCDEF

# Enable automatic signing of all commits
git config --global commit.gpgsign true

# Enable automatic signing of all tags
git config --global tag.gpgsign true
```

**Verify Configuration:**
```bash
git config --get user.signingkey
git config --get commit.gpgsign
```

---

## Signing Ledger Entries

### Method 1: Sign Individual YAML Entry (Detached Signature)

**Use Case:** Sign a specific ledger entry file

**Command:**
```bash
# Sign the entry (creates .asc signature file)
gpg --detach-sign --armor -u domenic.garza@snhu.edu ai_conversation_ledger.yml

# This creates: ai_conversation_ledger.yml.asc
```

**Verify Signature:**
```bash
gpg --verify ai_conversation_ledger.yml.asc ai_conversation_ledger.yml
```

**Expected Output:**
```
gpg: Signature made Thu 21 Nov 2025 02:31:33 PM EST
gpg:                using RSA key 1234567890ABCDEF
gpg: Good signature from "Domenic Garza <domenic.garza@snhu.edu>"
```

### Method 2: Clearsign Entry (Inline Signature)

**Use Case:** Create a single file with content and signature combined

**Command:**
```bash
# Create clearsigned version
gpg --clearsign -u domenic.garza@snhu.edu ai_conversation_ledger.yml

# This creates: ai_conversation_ledger.yml.asc
# Original file is unchanged
```

**Verify Clearsigned File:**
```bash
gpg --verify ai_conversation_ledger.yml.asc
```

### Method 3: Embed Signature in YAML (Recommended for Ledger)

**Use Case:** Include signature directly in the YAML file for portable verification

**Process:**
```bash
# 1. Create a temporary copy for signing
cp ai_conversation_ledger.yml ledger_for_signing.yml

# 2. Generate detached signature
gpg --detach-sign --armor -u domenic.garza@snhu.edu ledger_for_signing.yml

# 3. Extract signature content
SIGNATURE=$(cat ledger_for_signing.yml.asc)

# 4. Add signature to original YAML file (manual or script)
# See "Signature Embedding Script" below
```

**Signature Embedding Script:**
```bash
#!/bin/bash
# sign_ledger_entry.sh - Sign and embed GPG signature in YAML

LEDGER_FILE="${1:-ai_conversation_ledger.yml}"
EMAIL="${2:-domenic.garza@snhu.edu}"

if [ ! -f "$LEDGER_FILE" ]; then
    echo "Error: File $LEDGER_FILE not found"
    exit 1
fi

# Create temp file without existing signature block
grep -v "^signatures:" "$LEDGER_FILE" | grep -v "^  gpg:" | grep -v "^    signer:" | grep -v "^    key_id:" | grep -v "^    signature:" | grep -v "^    signed_at:" > temp_ledger.yml

# Generate signature
gpg --detach-sign --armor -u "$EMAIL" temp_ledger.yml 2>&1

if [ $? -ne 0 ]; then
    echo "Error: GPG signing failed"
    rm temp_ledger.yml*
    exit 1
fi

# Get key ID
KEY_ID=$(gpg --list-secret-keys --keyid-format LONG "$EMAIL" | grep sec | awk '{print $2}' | cut -d'/' -f2)

# Create signature block
echo "" >> temp_ledger.yml
echo "signatures:" >> temp_ledger.yml
echo "  gpg:" >> temp_ledger.yml
echo "    signer: \"$(gpg --list-keys "$EMAIL" | grep uid | sed 's/uid.*] //')\"" >> temp_ledger.yml
echo "    key_id: \"$KEY_ID\"" >> temp_ledger.yml
echo "    signed_at: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" >> temp_ledger.yml
echo "    signature: |" >> temp_ledger.yml
sed 's/^/      /' temp_ledger.yml.asc >> temp_ledger.yml

# Replace original file
mv temp_ledger.yml "$LEDGER_FILE"
rm temp_ledger.yml.asc

echo "✓ Ledger signed successfully: $LEDGER_FILE"
echo "  Key ID: $KEY_ID"
echo "  Signer: $EMAIL"
```

**Usage:**
```bash
chmod +x sign_ledger_entry.sh
./sign_ledger_entry.sh ai_conversation_ledger.yml domenic.garza@snhu.edu
```

---

## Verifying Signatures

### Verify Detached Signature

```bash
gpg --verify signature_file.asc original_file.yml
```

**Successful Verification Output:**
```
gpg: Signature made Thu 21 Nov 2025 02:31:33 PM EST
gpg:                using RSA key 1234567890ABCDEF1234567890ABCDEF12345678
gpg: Good signature from "Domenic Garza <domenic.garza@snhu.edu>" [ultimate]
```

**Failed Verification Output:**
```
gpg: BAD signature from "Domenic Garza <domenic.garza@snhu.edu>" [ultimate]
```

### Verify Embedded YAML Signature

**Manual Extraction and Verification:**
```bash
# Extract signature block from YAML
grep -A 100 "signature: |" ai_conversation_ledger.yml | grep -v "signature: |" | sed 's/^      //' > extracted_signature.asc

# Extract content (everything before signature block)
sed '/^signatures:/,$d' ai_conversation_ledger.yml > content_to_verify.yml

# Verify
gpg --verify extracted_signature.asc content_to_verify.yml
```

**Automated Verification Script:**
```bash
#!/bin/bash
# verify_ledger_signature.sh - Verify embedded GPG signature in YAML

LEDGER_FILE="${1:-ai_conversation_ledger.yml}"

if [ ! -f "$LEDGER_FILE" ]; then
    echo "Error: File $LEDGER_FILE not found"
    exit 1
fi

# Extract content before signature
sed '/^signatures:/,$d' "$LEDGER_FILE" > /tmp/ledger_content.yml

# Extract signature
grep -A 100 "signature: |" "$LEDGER_FILE" | grep -v "signature: |" | sed 's/^      //' > /tmp/ledger_signature.asc

# Verify signature
if gpg --verify /tmp/ledger_signature.asc /tmp/ledger_content.yml 2>&1; then
    echo "✓ Signature verification PASSED"
    rm /tmp/ledger_content.yml /tmp/ledger_signature.asc
    exit 0
else
    echo "✗ Signature verification FAILED"
    rm /tmp/ledger_content.yml /tmp/ledger_signature.asc
    exit 1
fi
```

**Usage:**
```bash
chmod +x verify_ledger_signature.sh
./verify_ledger_signature.sh ai_conversation_ledger.yml
```

---

## Git Commit Signing

### Sign Individual Commit

```bash
# Stage your changes
git add ai_conversation_ledger.yml

# Commit with signature
git commit -S -m "Add AI conversation entry: Claude discussion on legal evidence standards"

# Push to remote
git push
```

### Verify Signed Commits

**View Signature on Latest Commit:**
```bash
git log --show-signature -1
```

**Expected Output:**
```
commit abc123def456...
gpg: Signature made Thu 21 Nov 2025 02:31:33 PM EST
gpg:                using RSA key 1234567890ABCDEF
gpg: Good signature from "Domenic Garza <domenic.garza@snhu.edu>"
Author: Domenic Garza <domenic.garza@snhu.edu>
Date:   Thu Nov 21 14:31:33 2025 -0500

    Add AI conversation entry: Claude discussion on legal evidence standards
```

**View All Signed Commits:**
```bash
git log --show-signature --pretty=format:"%h %G? %s" --abbrev-commit
```

**Signature Status Codes:**
- `G` = Good signature
- `B` = Bad signature
- `U` = Good signature, unknown validity
- `X` = Good signature, expired
- `Y` = Good signature, expired key
- `R` = Good signature, revoked key
- `E` = Signature can't be checked
- `N` = No signature

---

## Key Management Best Practices

### Backup Your Private Key

**Critical:** If you lose your private key, you cannot prove you created past signatures.

**Export Private Key:**
```bash
# This command will ask for your passphrase
gpg --export-secret-keys --armor domenic.garza@snhu.edu > private_key_backup.asc

# Store in secure location:
# - Password manager (encrypted)
# - Hardware token (YubiKey)
# - Encrypted USB drive in safe
# - DO NOT store in cloud unencrypted
# - DO NOT commit to git repository
```

**Restore Private Key:**
```bash
gpg --import private_key_backup.asc
```

### Publish Your Public Key

**Upload to Key Server:**
```bash
# Send to Ubuntu key server
gpg --keyserver keyserver.ubuntu.com --send-keys 0x1234567890ABCDEF

# Alternative servers:
# gpg --keyserver keys.openpgp.org --send-keys 0x1234567890ABCDEF
# gpg --keyserver pgp.mit.edu --send-keys 0x1234567890ABCDEF
```

**Include in Repository:**
```bash
# Export public key
gpg --armor --export domenic.garza@snhu.edu > keys/domenic_garza_public_key.asc

# Add to repository
git add keys/domenic_garza_public_key.asc
git commit -S -m "Add public GPG key for signature verification"
git push
```

**Include in Documentation:**
Add to your README or CONTRIBUTORS file:
```markdown
## Signature Verification

Ledger entries and commits are signed with GPG key:
- **Key ID:** 0x1234567890ABCDEF
- **Fingerprint:** 1234 5678 90AB CDEF 1234 5678 90AB CDEF 1234 5678
- **Public Key:** [keys/domenic_garza_public_key.asc](keys/domenic_garza_public_key.asc)

Import key:
\`\`\`bash
curl https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/keys/domenic_garza_public_key.asc | gpg --import
\`\`\`
```

### Key Expiration and Renewal

**Extend Key Expiration:**
```bash
# Edit key
gpg --edit-key domenic.garza@snhu.edu

# At GPG prompt:
gpg> expire
# Follow prompts to set new expiration

gpg> save

# Upload updated key to key server
gpg --keyserver keyserver.ubuntu.com --send-keys 0x1234567890ABCDEF
```

**Revoke Compromised Key:**
```bash
# Generate revocation certificate (do this when creating key!)
gpg --output revoke_cert.asc --gen-revoke domenic.garza@snhu.edu

# If key is compromised, import and publish revocation:
gpg --import revoke_cert.asc
gpg --keyserver keyserver.ubuntu.com --send-keys 0x1234567890ABCDEF
```

---

## Troubleshooting

### Problem: "gpg: signing failed: Inappropriate ioctl for device"

**Solution:**
```bash
export GPG_TTY=$(tty)
# Add to ~/.bashrc or ~/.zshrc for permanent fix
```

### Problem: "gpg: signing failed: No secret key"

**Solution:**
```bash
# Verify your key exists
gpg --list-secret-keys

# If missing, import backup or generate new key
gpg --import private_key_backup.asc
```

### Problem: Git asks for passphrase every time

**Solution (Linux):**
```bash
# Install and configure GPG agent
sudo apt-get install gnupg-agent pinentry-curses

# Add to ~/.gnupg/gpg-agent.conf:
default-cache-ttl 34560000
max-cache-ttl 34560000

# Reload agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

### Problem: Signature verification fails after file edit

**Explanation:** This is expected behavior. Any change to the file invalidates the signature.

**Solution:** Re-sign the file after making changes.

---

## Complete Example Workflow

**Scenario:** Create and sign a new AI conversation ledger entry

```bash
# 1. Create/edit ledger entry
nano ai_conversation_ledger.yml

# 2. Calculate hash for previous entry chain
PREV_HASH=$(sha256sum previous_entry.yml | awk '{print $1}')
echo "previous_entry_hash: $PREV_HASH"

# 3. Sign the entry
./sign_ledger_entry.sh ai_conversation_ledger.yml

# 4. Verify signature
./verify_ledger_signature.sh ai_conversation_ledger.yml

# 5. Commit with signed commit
git add ai_conversation_ledger.yml
git commit -S -m "Add conversation: Legal standards for AI evidence"

# 6. Verify git signature
git log --show-signature -1

# 7. Push to remote
git push

# 8. Verify on GitHub (look for "Verified" badge)
```

---

## Integration with AI Conversation Ledger Schema

**Updated YAML Schema with GPG Signature:**

```yaml
entry:
  id: "conv_20251121_001"
  timestamp: "2025-11-21T14:31:33Z"
  
  conversation:
    platform: "Claude (Anthropic)"
    model: "claude-3-opus-20240229"
    share_url: "https://claude.ai/share/abc123def456"
    topic: "Legal Standards for AI Evidence"
    
  content_hash:
    algorithm: "SHA3-256"
    hash: "1234567890abcdef..."
    
  chain:
    previous_entry_hash: "abcdef1234567890..."
    entry_number: 42
    
  attestation:
    statement: "I certify that this entry accurately reflects my conversation with Claude, accessed via the share URL above. I verified the content and created this entry contemporaneously."
    verified_by: "Domenic Garza"
    verification_date: "2025-11-21T14:31:33Z"
    
  signatures:
    gpg:
      signer: "Domenic Garza <domenic.garza@snhu.edu>"
      key_id: "0x1234567890ABCDEF"
      fingerprint: "1234 5678 90AB CDEF 1234 5678 90AB CDEF 1234 5678"
      signed_at: "2025-11-21T14:31:33Z"
      signature: |
        -----BEGIN PGP SIGNATURE-----
        
        iQIzBAABCAAdFiEEEjMEVYZHiEmJmrs+Kw4MbTtSwDcFAmZGnj0ACgkQKw4MbTtS
        [... signature data ...]
        -----END PGP SIGNATURE-----
        
  git_commit:
    sha: "abc123def456789..."
    signed: true
    author: "Domenic Garza <domenic.garza@snhu.edu>"
    timestamp: "2025-11-21T14:31:33Z"
```

---

## Legal Value Summary

**What GPG Signatures Provide:**

✅ **Authentication** - Cryptographically proves you created the document  
✅ **Integrity** - Proves document hasn't been altered since signing  
✅ **Non-repudiation** - You cannot credibly deny creating the signature  
✅ **Timestamp** - Shows when signature was created  
✅ **Legal Recognition** - Widely accepted in courts as reliable authentication

**Legal Framework:**
- **eIDAS (EU):** Advanced Electronic Signature - High legal weight
- **ESIGN Act (US):** Electronic signature with legal effect
- **UETA (US States):** Electronic signature = handwritten signature
- **UK/CA/AU:** Recognized as reliable authentication method

**Court Admissibility:**
- GPG signatures help authenticate documents
- Still require human testimony to explain the system
- Significantly strengthens FRE 901(b)(9) "process or system" foundation
- Makes tampering/fabrication claims much harder to prove

---

## Quick Reference Card

```bash
# Generate key (one time)
gpg --full-generate-key

# Export public key
gpg --armor --export you@email.com > public_key.asc

# Sign file (detached)
gpg --detach-sign --armor -u you@email.com file.yml

# Verify signature
gpg --verify file.yml.asc file.yml

# Configure git signing
git config --global user.signingkey 0xYOURKEYID
git config --global commit.gpgsign true

# Signed commit
git commit -S -m "message"

# View signatures
git log --show-signature

# Backup private key (SECURE STORAGE!)
gpg --export-secret-keys --armor you@email.com > private_backup.asc
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-21  
**Part Of:** Appendix C - Legal Standards for AI Conversation Logs
