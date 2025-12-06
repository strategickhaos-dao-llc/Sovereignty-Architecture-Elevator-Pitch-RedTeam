# Ledger Verification Scripts

Automation scripts for AI conversation ledger signing, verification, and timestamping.

**Part of:** Appendix C - Legal Standards for AI Conversation Logs

## Available Scripts

### 1. sign_ledger_entry.sh

**Purpose:** Sign a ledger entry with GPG and embed the signature in the YAML file

**Usage:**
```bash
./sign_ledger_entry.sh ledger_entry.yml [email@address.com]
```

**What it does:**
- Extracts content without existing signatures
- Generates GPG detached signature
- Embeds signature in YAML structure
- Updates file with signature block

**Example:**
```bash
./sign_ledger_entry.sh my_conversation.yml domenic.garza@snhu.edu
```

**Output:**
```
✓ Ledger signed successfully: my_conversation.yml
  Key ID: 0x1234567890ABCDEF
  Signer: domenic.garza@snhu.edu

Next steps:
  1. Verify signature: ./verify_ledger_signature.sh my_conversation.yml
  2. Commit: git add my_conversation.yml && git commit -S -m 'Add signed ledger entry'
  3. Timestamp: ots stamp my_conversation.yml (optional)
```

**Requirements:**
- GPG installed and configured
- Private key for signing email

---

### 2. verify_ledger_signature.sh

**Purpose:** Verify the embedded GPG signature in a ledger entry

**Usage:**
```bash
./verify_ledger_signature.sh ledger_entry.yml
```

**What it does:**
- Extracts content without signature block
- Extracts embedded signature
- Verifies signature against content
- Reports verification status

**Example:**
```bash
./verify_ledger_signature.sh my_conversation.yml
```

**Success output:**
```
✓ Signature verification PASSED
  Ledger entry is authentic and unmodified

Signature details:
  Signer: Domenic Garza <domenic.garza@snhu.edu>
  Key ID: 0x1234567890ABCDEF
  Signed at: 2025-11-21T14:31:33Z
```

**Failure output:**
```
✗ Signature verification FAILED
  Warning: Ledger may have been tampered with!
```

**Requirements:**
- GPG installed
- Public key imported for verification

---

### 3. monthly_timestamp.sh

**Purpose:** Create monthly root hash and timestamp all entries cost-effectively

**Usage:**
```bash
./monthly_timestamp.sh [ledger_directory]
```

**What it does:**
- Finds all ledger entries for current month
- Calculates root hash of all entries
- Signs root hash with GPG
- Timestamps via OpenTimestamps
- Commits to git repository

**Example:**
```bash
./monthly_timestamp.sh ./ledger_entries
```

**Output:**
```
Creating monthly root hash timestamp for: 2025-11
Found 15 entries for 2025-11
✓ Root hash calculated: abc123def456...
  Saved to: root_hash_2025-11.txt
  Entries: 15
✓ Root hash signed: root_hash_2025-11.txt.asc
✓ Timestamp created: root_hash_2025-11.txt.asc.ots
✓ Committed to git with signed commit

Monthly timestamp complete!

Summary:
  Month: 2025-11
  Entries: 15
  Root hash: abc123def456...
  Hash file: root_hash_2025-11.txt
  Signature: root_hash_2025-11.txt.asc
  Timestamp: Created (upgrade in ~1 hour)
```

**Requirements:**
- GPG installed (optional but recommended)
- OpenTimestamps client (optional but recommended)
- Git repository (optional but recommended)

**Cost:** ~$0.01-0.10 per month (Bitcoin transaction fees)

---

### 4. create_verification_package.sh

**Purpose:** Bundle ledger files for third-party verification (auditors, investors, courts)

**Usage:**
```bash
./create_verification_package.sh [ledger_files...]
```

**What it does:**
- Copies specified ledger files (or finds all if none specified)
- Includes associated signatures and timestamps
- Exports public GPG key
- Creates comprehensive verification instructions
- Generates signed SHA256 manifest
- Creates compressed archive
- Optionally timestamps the package

**Example:**
```bash
# Package specific files
./create_verification_package.sh entry1.yml entry2.yml entry3.yml

# Package all ledger files found
./create_verification_package.sh
```

**Output:**
```
✓ Verification package created successfully!

═══════════════════════════════════════════════════════════
  Package: verification_package_20251121_143133.tar.gz
  Size: 156K
  Hash: xyz789...
  Files: 15 ledger entries
  GPG Key: 0x1234567890ABCDEF
═══════════════════════════════════════════════════════════

Package contents:
  - Ledger files (.yml/.yaml)
  - GPG signatures (.asc)
  - OpenTimestamps proofs (.ots)
  - Public GPG key (public_key.asc)
  - Verification instructions (VERIFICATION_INSTRUCTIONS.md)
  - Signed SHA256 manifest (SHA256SUMS.asc)

To distribute:
  1. Share: verification_package_20251121_143133.tar.gz
  2. Share: verification_package_20251121_143133.tar.gz.ots (after ~1 hour)
```

**Use cases:**
- Investor due diligence packages
- Court evidence submissions
- Academic committee reviews
- Patent application support
- Trade secret documentation

**Requirements:**
- GPG (recommended)
- OpenTimestamps (recommended)
- Git repository (optional)

---

## Automated Workflows

### Daily: Sign and Commit New Entries

```bash
#!/bin/bash
# daily_ledger_maintenance.sh

for entry in ledger_entries/*.yml; do
    if ! grep -q "signatures:" "$entry"; then
        echo "Signing: $entry"
        ./sign_ledger_entry.sh "$entry"
        git add "$entry"
    fi
done

if git status --porcelain | grep -q "^M"; then
    git commit -S -m "Sign new ledger entries: $(date +%Y-%m-%d)"
    git push
fi
```

### Monthly: Root Hash Timestamp

Add to crontab:
```bash
# Run on 1st of each month at 3am
0 3 1 * * /path/to/monthly_timestamp.sh /path/to/ledger_entries

# Upgrade timestamps 2 hours later
0 5 1 * * cd /path/to/project && ots upgrade root_hash_*.ots
```

### On-Demand: Verification Package

Before investor meeting, court filing, or academic submission:
```bash
./create_verification_package.sh
# Share the generated .tar.gz file
```

---

## Complete Example Workflow

### 1. Create Ledger Entry

```bash
# Use schema template
cp legal/APPENDIX_C5_EXAMPLE_LEDGER_ENTRY.yaml ledger_entries/conv_20251121_001.yml

# Edit with your conversation details
nano ledger_entries/conv_20251121_001.yml
```

### 2. Sign Entry

```bash
./scripts/sign_ledger_entry.sh ledger_entries/conv_20251121_001.yml
```

### 3. Verify Signature

```bash
./scripts/verify_ledger_signature.sh ledger_entries/conv_20251121_001.yml
```

### 4. Timestamp (Optional)

```bash
# Individual entry timestamp
ots stamp ledger_entries/conv_20251121_001.yml

# Or wait for monthly root hash
```

### 5. Commit to Git

```bash
git add ledger_entries/conv_20251121_001.yml
git commit -S -m "Add AI conversation: Legal standards discussion"
git push
```

### 6. Verify Git Signature

```bash
git log --show-signature -1
```

### 7. Create Verification Package (when needed)

```bash
./scripts/create_verification_package.sh ledger_entries/conv_20251121_001.yml
```

---

## Troubleshooting

### GPG: "No secret key"

```bash
# Generate key if you don't have one
gpg --full-generate-key

# List your keys to verify
gpg --list-secret-keys
```

### GPG: "Inappropriate ioctl for device"

```bash
export GPG_TTY=$(tty)

# Add to ~/.bashrc for permanent fix
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
```

### OpenTimestamps: "Command not found"

```bash
# Install opentimestamps-client
pip3 install opentimestamps-client

# Verify installation
ots --version
```

### Git: "Commit signature verification failed"

```bash
# Configure git with your GPG key
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Test with a commit
git commit --allow-empty -S -m "Test signed commit"
```

---

## Security Best Practices

### Protect Your Private Key

**Do:**
- ✅ Use strong passphrase for GPG key
- ✅ Back up private key to secure location
- ✅ Store backup encrypted (password manager, hardware token)
- ✅ Never commit private key to git

**Don't:**
- ❌ Share private key with anyone
- ❌ Store unencrypted in cloud
- ❌ Use weak/no passphrase
- ❌ Lose the key (can't prove past signatures!)

### Verify Before Trusting

**Always verify:**
- GPG signatures before accepting ledger as authentic
- OpenTimestamps proofs against blockchain
- Git commit signatures
- Share URLs still accessible

**Be suspicious if:**
- Signature verification fails
- Timestamps don't match claimed dates
- Share URLs are broken/inaccessible
- Hash chain is broken

---

## Script Dependencies

### Required
- `bash` - Shell interpreter
- `grep`, `sed`, `awk` - Text processing (standard on Unix systems)

### Optional but Recommended
- `gpg` - GNU Privacy Guard for signatures
- `ots` - OpenTimestamps client for blockchain timestamps
- `git` - Version control for commit signing

### Installation

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install gnupg git
pip3 install opentimestamps-client
```

**macOS:**
```bash
brew install gnupg git
pip3 install opentimestamps-client
```

**Windows:**
- GPG: https://www.gpg4win.org/
- Git: https://git-scm.com/download/win
- OpenTimestamps: `pip install opentimestamps-client`

---

## Legal Value of Scripts

These scripts automate the cryptographic verification framework described in Appendix C:

**What they provide:**
- ✅ Consistent, reliable signing process
- ✅ Automated verification procedures
- ✅ Cost-effective blockchain timestamping
- ✅ Professional verification packages

**What they don't provide:**
- ❌ Legal advice (consult attorney)
- ❌ Automatic court admissibility
- ❌ Proof AI outputs are true
- ❌ Substitute for human testimony

**Best for:**
- R&D documentation
- Investor due diligence
- Academic research
- Internal compliance
- IP timeline evidence

---

## Contributing

Improvements welcome! Please:
1. Test scripts thoroughly
2. Maintain backward compatibility
3. Update documentation
4. Follow existing code style

---

## License

MIT License - Free to use and modify

**Disclaimer:** These scripts are provided as-is for educational and research purposes. They do not constitute legal advice. Consult qualified legal counsel for specific legal matters.

---

**Version:** 1.0  
**Last Updated:** 2025-11-21  
**Part Of:** Appendix C - Legal Standards for AI Conversation Logs  
**Author:** Domenic Garza / Strategickhaos DAO LLC
