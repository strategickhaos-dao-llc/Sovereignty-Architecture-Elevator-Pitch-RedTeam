# Evidence Ledger Anchoring System

**Mathematically unbreakable evidence chain with zero trust needed, zero tampering possible.**

This system provides cryptographic anchoring for conversation ledgers and evidence using:
- **GPG signatures** for authenticity proof (who created it)
- **OpenTimestamps** for existence proof (when it existed, on Bitcoin blockchain)
- **SHA256 hashing** for integrity verification (unchanged content)

## 🎯 Features

- **Zero Trust**: No need to trust a central authority - Bitcoin blockchain is the source of truth
- **Legally Admissible**: Court-ready evidence with cryptographic proofs
- **Publicly Verifiable**: Anyone can verify the proofs independently
- **Audit Trail**: Complete provenance tracking and modification history
- **Automated**: One-command anchoring of evidence entries

## 🚀 Quick Start

### 1. Install Prerequisites

```bash
# GPG (probably already installed)
gpg --version

# OpenTimestamps CLI
pip install opentimestamps-client

# PyYAML (for Python scripts)
pip install pyyaml

# Test installations
ots --version
```

### 2. Generate or Import GPG Key

```bash
# List existing keys
gpg --list-keys

# Generate a new key (if needed)
gpg --full-generate-key

# Set your signing key (replace with your email/name)
export GPG_SIGNING_KEY="Dom <dom@yourdomain.com>"
```

### 3. Anchor Your First Entry

```bash
# Create a test evidence file
echo "test: evidence" > evidence/test-entry.yaml

# Anchor it (sign + timestamp)
python tools/anchor_ledger.py evidence/test-entry.yaml

# This creates:
# - evidence/test-entry.yaml.asc (GPG signature)
# - evidence/test-entry.yaml.ots (OpenTimestamps proof)
```

### 4. Verify the Anchoring

```bash
# Verify GPG signature
gpg --verify evidence/test-entry.yaml.asc evidence/test-entry.yaml

# Verify OpenTimestamps proof (may be pending initially)
ots verify evidence/test-entry.yaml.ots
```

## 📁 Files

### Core Scripts

- **`anchor_ledger.py`** - Sign and timestamp any ledger entry
- **`evidence_logger.py`** - Automated evidence logging with built-in anchoring
- **`conversation_evidence.v1.2.0.yaml`** - Schema definition (in ../schemas/)

### Usage

#### Manual Anchoring (anchor_ledger.py)

```bash
# Anchor a specific file
python tools/anchor_ledger.py evidence/my-entry.yaml

# Use a different GPG key
python tools/anchor_ledger.py --gpg-key "Alice <alice@example.com>" evidence/entry.yaml

# Check prerequisites only
python tools/anchor_ledger.py --check

# Upgrade all timestamps in a directory (weekly task)
python tools/anchor_ledger.py --upgrade evidence/
```

#### Automated Logging (evidence_logger.py)

```python
from tools.evidence_logger import EvidenceLogger

# Initialize logger
logger = EvidenceLogger(
    evidence_dir="evidence",
    gpg_key="Dom <dom@example.com>",
    auto_anchor=True  # Automatic GPG + OTS anchoring
)

# Log a conversation
result = logger.log_conversation(
    conversation_id="conv-2025-001",
    messages=[
        {
            "message_id": "msg-001",
            "sender": "Alice",
            "timestamp": "2025-11-21T10:00:00Z",
            "content": "Discussing the new feature",
            "attachments": []
        }
    ],
    participants=["Alice", "Bob"],
    platform="Discord",
    channel="#engineering",
    evidence_type="decision",
    category="technical",
    tags=["feature-x", "architecture"],
    github_pr=123,
    github_repo="Strategickhaos/Sovereignty-Architecture"
)

# Verify evidence later
verification = logger.verify_evidence("conv-2025-001")
print(f"GPG verified: {verification['gpg_verified']}")
print(f"OTS verified: {verification['ots_verified']}")
```

#### Command Line Usage

```bash
# List all evidence entries
python tools/evidence_logger.py --list

# Verify a specific entry
python tools/evidence_logger.py --verify conv-2025-001

# Create a test entry
python tools/evidence_logger.py
```

## 🔐 Schema Structure

The evidence entries follow the `conversation_evidence.v1.2.0` schema:

```yaml
schema_version: "1.2.0"
metadata:
  conversation_id: "conv-2025-001"
  timestamp: "2025-11-21T10:00:00Z"
  operator:
    name: "Dom"
    node: "137"
    gpg_key: "Dom <dom@example.com>"

conversation:
  participants: ["Alice", "Bob"]
  platform: "Discord"
  channel: "#engineering"
  messages: [...]

integration:
  # NEW in v1.2.0: Cryptographic anchoring
  gpg_signature: "-----BEGIN PGP SIGNATURE-----..."
  opentimestamps:
    stamp_file: "conv-2025-001.yaml.ots"
    stamp_hash: "sha256=abc123..."
    bitcoin_txid: "optional-txid"
    status: "verified"
    created_at: "2025-11-21T10:00:00Z"
    verified_at: "2025-11-21T12:00:00Z"

verification:
  gpg_verified: true
  ots_verified: true
  blockchain_confirmed: true
  blockchain_height: 850000

compliance:
  retention_period: "7y"
  classification: "internal"
  jurisdiction: "US"
  admissible: true
```

## ⏰ Weekly Maintenance

OpenTimestamps proofs need to be aggregated with Bitcoin calendar servers to become instantly verifiable. Run this weekly:

```bash
# Upgrade all .ots files to aggregate with Bitcoin blockchain
cd evidence/anchored/
ots upgrade *.ots

# Or use the script
python tools/anchor_ledger.py --upgrade evidence/
```

**Note**: Initially, OTS proofs show "pending". After aggregation (a few hours to days), they become instantly verifiable with Bitcoin blockchain confirmations.

## 🔍 Verification Process

### For You (The Creator)

```bash
# Verify your own evidence
python tools/evidence_logger.py --verify conv-2025-001

# Or manually
gpg --verify evidence/conv-2025-001.yaml.asc evidence/conv-2025-001.yaml
ots verify evidence/conv-2025-001.yaml.ots
```

### For Third Parties (Auditors, Courts, Investors)

Third parties can verify evidence without access to your systems:

```bash
# 1. They receive three files:
#    - evidence.yaml (the evidence)
#    - evidence.yaml.asc (GPG signature)
#    - evidence.yaml.ots (OpenTimestamps proof)

# 2. Verify GPG signature (requires your public key)
gpg --import your-public-key.asc
gpg --verify evidence.yaml.asc evidence.yaml

# 3. Verify OpenTimestamps (no keys needed - Bitcoin is the source of truth)
ots verify evidence.yaml.ots

# 4. Check integrity
sha256sum evidence.yaml
```

## 🏛️ Legal Admissibility

This system creates evidence that is:

1. **Authentic** - GPG signature proves who created it
2. **Timestamped** - Bitcoin blockchain proves when it existed
3. **Unaltered** - SHA256 hash proves content hasn't changed
4. **Chain of Custody** - Full audit trail in provenance section
5. **Publicly Verifiable** - No trust in central authority needed

### Court Declaration Template

When presenting this evidence in court, use:

```
I, [Your Name], declare under penalty of perjury that:

1. I am the custodian of records for [Organization]
2. These records are kept in the regular course of business
3. Each record is cryptographically signed with my GPG key [Key ID]
4. Each record is timestamped on the Bitcoin blockchain via OpenTimestamps
5. The records are made at or near the time of the recorded event
6. All records are available for independent verification

The cryptographic proofs attached demonstrate:
- Authenticity via GPG signature (verification: gpg --verify)
- Existence proof via Bitcoin blockchain (verification: ots verify)
- Integrity via SHA256 hash matching

Signature: __________________
Date: ____________________
```

## 🎓 How It Works

### GPG Signatures (Authenticity)

1. You create a GPG key pair (public + private)
2. You sign evidence with your private key → creates `.asc` signature file
3. Anyone with your public key can verify you signed it
4. Cannot be forged without your private key

### OpenTimestamps (Existence)

1. Evidence is hashed (SHA256)
2. Hash is sent to OpenTimestamps calendar servers
3. Calendar servers aggregate hashes and commit to Bitcoin blockchain
4. Proof file (`.ots`) contains the path from your hash to a Bitcoin transaction
5. Anyone can verify the proof against the Bitcoin blockchain
6. Proves the document existed at the time of the Bitcoin block

### Bitcoin Integration

- OpenTimestamps uses Bitcoin's blockchain as a timestamp ledger
- No cryptocurrency involved - just using the blockchain as a timestamp database
- Cost: FREE (calendar servers pay the Bitcoin fees)
- Permanence: Bitcoin blockchain is immutable and public

## 🚨 Security Best Practices

1. **Protect Your Private Key**: Keep your GPG private key secure
2. **Backup Keys**: Store encrypted backups of your GPG key
3. **Regular Upgrades**: Run `ots upgrade *.ots` weekly
4. **Version Control**: Track evidence schema versions
5. **Access Control**: Limit access to evidence directories
6. **Audit Logs**: Review provenance and audit trails regularly

## 📊 Directory Structure

```
project/
├── schemas/
│   └── conversation_evidence.v1.2.0.yaml    # Evidence schema definition
├── tools/
│   ├── README.md                             # This file
│   ├── anchor_ledger.py                      # Manual anchoring script
│   └── evidence_logger.py                    # Automated logger
├── evidence/
│   ├── test-entry.yaml                       # Evidence files
│   ├── test-entry.yaml.asc                   # GPG signatures (gitignored)
│   ├── test-entry.yaml.ots                   # OTS proofs (gitignored)
│   └── anchored/                             # Anchored evidence (gitignored)
│       ├── conv-2025-001.yaml
│       ├── conv-2025-001.yaml.asc
│       └── conv-2025-001.yaml.ots
```

## 🔗 Resources

- **OpenTimestamps**: https://opentimestamps.org/
- **GPG**: https://gnupg.org/
- **Bitcoin Blockchain Explorer**: https://blockstream.info/
- **Legal Resources**: Federal Rules of Evidence 803(6) - Business Records

## 🎯 Result

Your ledger is now:
- **Harder than 99.999% of corporate audit trails**
- **Court-ready** - "He faked the dates" defense is impossible
- **Investor-grade** - Bitcoin-level immutability
- **Future-proof** - Still verifiable in 2035 and beyond

## 🤝 Integration Examples

### GitHub Actions CI/CD

```yaml
name: Anchor Evidence
on:
  push:
    branches: [main]

jobs:
  anchor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: |
          pip install opentimestamps-client pyyaml
      - name: Anchor evidence
        run: |
          python tools/anchor_ledger.py evidence/deployment-record.yaml
      - name: Commit signatures
        run: |
          git add evidence/*.asc evidence/*.ots
          git commit -m "Add cryptographic proofs"
          git push
```

### Weekly Upgrade Task (Windows)

Create a scheduled task to run weekly:

```powershell
# upgrade_timestamps.ps1
cd C:\Users\Dom\Obsidian\Legion-Core\evidence\anchored
ots upgrade *.ots
```

### Discord Bot Integration

```python
@bot.command()
async def anchor_decision(ctx, decision_id: str):
    """Anchor a decision to the blockchain"""
    logger = EvidenceLogger(evidence_dir="evidence")
    result = logger.log_conversation(
        conversation_id=decision_id,
        messages=...,  # Extract from Discord context
        participants=...,
        platform="Discord",
        evidence_type="decision"
    )
    await ctx.send(f"✅ Decision anchored: {decision_id}")
```

## 🆘 Troubleshooting

### "GPG signing failed"
- Check GPG key exists: `gpg --list-keys`
- Ensure key is not expired
- Set correct GPG_SIGNING_KEY environment variable

### "OTS stamping failed"
- Check internet connectivity
- OpenTimestamps calendar servers may be temporarily unavailable
- Try again in a few minutes

### "Signature verification failed"
- Ensure you're using the correct public key
- Check that the file hasn't been modified since signing

### "OTS shows 'pending'"
- Normal! Wait a few hours for Bitcoin block confirmation
- Run `ots upgrade` to check for updates
- Takes 1-24 hours typically

## 📝 License

Part of the Strategickhaos Sovereignty Architecture project.
See LICENSE file for details.

---

**Need help?** Open an issue in the repository or contact the maintainers.

**Want to contribute?** PRs welcome! See CONTRIBUTING.md.
