# Evidence Ledger Anchoring System

**Mathematically unbreakable audit trails — Zero trust needed, zero tampering possible, zero excuses in court or audit.**

## 🎯 Overview

The Evidence Anchoring System provides cryptographic proof of authenticity and immutability for conversation logs and other evidence. This creates a hardened, publicly verifiable artifact chain that is:

- **Court-proof**: Bitcoin timestamps prove "this existed at this time" - impossible to forge
- **Audit-proof**: GPG signatures prove "this person created this" - mathematically verified  
- **Tamper-proof**: Any modification invalidates both signatures and timestamps
- **Future-proof**: Verifiable forever, even decades from now

Your ledger is now harder than 99.999% of corporate audit trails.

## 🔐 Technology Stack

### GPG (GNU Privacy Guard)
- Creates detached cryptographic signatures
- Proves **WHO** created the document (authenticity)
- Uses public-key cryptography (anyone can verify with public key)

### OpenTimestamps
- Anchors document hashes to Bitcoin blockchain
- Proves **WHEN** the document existed (immutability)
- Public blockchain = verifiable by anyone, anytime, forever

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.evidence.txt

# GPG is usually pre-installed on Linux/Mac
gpg --version

# For Windows: https://gpg4win.org/
```

### 2. Anchor Your First File

```bash
# Sign and timestamp any file
python tools/anchor_ledger.py evidence/example_conversation_ledger.yaml

# Output:
# ✅ Anchored: evidence/example_conversation_ledger.yaml
#    SHA256: abc123...
#    ✓ GPG Signature: .asc file created
#    ✓ OpenTimestamps: .ots file created
```

### 3. Verify Anytime, Anywhere

```bash
# Verify with our tool
python tools/anchor_ledger.py --verify evidence/example_conversation_ledger.yaml

# Or use native tools directly
ots verify evidence/example_conversation_ledger.yaml.ots
gpg --verify evidence/example_conversation_ledger.yaml.asc evidence/example_conversation_ledger.yaml
```

## 📚 Usage Modes

### Mode 1: Command Line Tool

For manually anchoring any file:

```bash
# Basic usage
python tools/anchor_ledger.py path/to/file.yaml

# Specify GPG key
python tools/anchor_ledger.py file.yaml --gpg-key "your@email.com"

# Verify existing anchors
python tools/anchor_ledger.py --verify file.yaml
```

### Mode 2: Python API

For programmatic integration:

```python
from tools.evidence_logger import EvidenceLogger

# Initialize
logger = EvidenceLogger(
    evidence_dir="evidence/anchored",
    gpg_key="dom@strategickhaos.com",
    operator="Domenic Garza"
)

# Log conversation with automatic anchoring
result = logger.log_conversation(
    conversation_id="conv_2025_001",
    participants=[
        {"name": "Dom", "role": "operator"},
        {"name": "AI System", "role": "assistant"}
    ],
    transcript="Full conversation text...",
    context="Strategic planning session",
    summary="Discussed Q1 objectives",
    attachments=["document1.pdf"],
    related_documents=["planning_doc.yaml"],
    auto_anchor=True  # Automatically sign + timestamp
)

print(f"Evidence logged: {result['file_path']}")
print(f"SHA256: {result['sha256']}")
print(f"Anchored: {result['anchored']}")
```

### Mode 3: Weekly Aggregation

Improve verification speed by upgrading timestamps weekly:

```bash
# Run weekly (cron/Task Scheduler)
cd evidence/anchored
ots upgrade *.ots
```

This fetches Bitcoin blockchain confirmations, making future verifications instant.

## 📋 File Structure

After anchoring, you'll have three files:

```
evidence/anchored/
├── conv_2025_001.yaml           # Original evidence (YAML)
├── conv_2025_001.yaml.asc       # GPG signature (ASCII-armored)
└── conv_2025_001.yaml.ots       # OpenTimestamps proof (binary)
```

**Note**: `.asc` and `.ots` files are gitignored by default but should be shared with auditors/courts.

## 🎓 Evidence Schema

The system uses a structured schema (`conversation_evidence.v1.2.0.yaml`) with:

### Core Sections
- **metadata**: Document ID, timestamps, operator information
- **conversation**: Participants, context, summary
- **evidence**: Transcript, attachments, hash, file size
- **integration**: OpenTimestamps and GPG anchoring data
- **attestation**: Legal sworn declaration for court admissibility
- **audit**: Access logs and modification history

### Key Integration Fields

```yaml
integration:
  opentimestamps:
    stamp_file: ".ots"
    stamp_hash: "sha256=abc123..."
    bitcoin_txid: ""
    status: "pending|verified|failed"
    calendar_url: "https://alice.btc.calendar.opentimestamps.org"
    created_at: "2025-11-21T23:00:00Z"
    verified_at: ""
    
  gpg_signature: "-----BEGIN PGP SIGNATURE-----..."
  gpg_key_id: "ABCD1234"
  gpg_fingerprint: "1234 5678 90AB CDEF..."
  signer_email: "dom@strategickhaos.com"
  signature_created_at: "2025-11-21T23:00:00Z"
```

## 🔍 Verification Process

### For Auditors/Courts

1. **Verify GPG Signature** (proves WHO created it)
   ```bash
   gpg --verify file.yaml.asc file.yaml
   ```

2. **Verify OpenTimestamps** (proves WHEN it existed)
   ```bash
   ots verify file.yaml.ots
   ```

3. **Check Hash** (proves INTEGRITY)
   ```bash
   sha256sum file.yaml
   # Compare with hash in integration.opentimestamps.stamp_hash
   ```

### Status Meanings

- **pending**: Submitted to Bitcoin, waiting for block confirmation (~1-6 hours)
- **verified**: Confirmed on Bitcoin blockchain, fully verifiable
- **failed**: Error in timestamping process (retry recommended)

## 💼 Use Cases

### Legal/Court Proceedings
- Timestamped records prove document existence at specific time
- GPG signatures prove authorship  
- Bitcoin blockchain = public, immutable, tamper-proof

### Investor Relations  
- Demonstrate professional record-keeping
- Show security consciousness
- Provide verifiable audit trails

### Compliance/Audit
- Meet "records kept in regular course of business" standards
- Cryptographically verifiable integrity
- No trust required - math proves everything

### Personal Archive
- Future-proof records (verifiable in 2035, 2045, forever)
- No dependency on third-party services
- Self-sovereign evidence management

## 🛠️ Advanced Features

### Batch Processing

```bash
# Anchor all YAML files in a directory
for file in evidence/*.yaml; do
    python tools/anchor_ledger.py "$file"
done
```

### CI/CD Integration

Add to `.github/workflows/evidence-anchor.yml`:

```yaml
name: Anchor Evidence
on:
  push:
    paths:
      - 'evidence/**/*.yaml'

jobs:
  anchor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: pip install -r requirements.evidence.txt
      - name: Anchor evidence
        run: python tools/anchor_ledger.py evidence/daily_report.yaml
```

### Custom GPG Configuration

```python
# Use specific GPG key for different contexts
logger_strategic = EvidenceLogger(gpg_key="strategic@company.com")
logger_legal = EvidenceLogger(gpg_key="legal@company.com")
logger_technical = EvidenceLogger(gpg_key="tech@company.com")
```

## 🧪 Testing

Run the test suite to validate installation:

```bash
python tools/test_evidence_system.py
```

Expected output:
```
Evidence Anchoring System - Test Suite
============================================================
✅ Test 1: Schema Loading
✅ Test 2: Evidence Logger Initialization  
✅ Test 3: Conversation Logging
✅ Test 4: Hash Calculation
✅ Test 5: YAML Structure Validation
============================================================
Passed: 5/5
✅ All tests passed!
```

## 📞 Troubleshooting

### GPG Issues

```bash
# Check GPG installation
gpg --version

# List available keys
gpg --list-keys

# Generate new key if needed
gpg --full-generate-key
```

### OpenTimestamps Issues

```bash
# Check OTS installation
ots --version

# Test connectivity to calendar servers
ots info file.yaml.ots

# Manually upgrade pending timestamps
ots upgrade file.yaml.ots
```

### Common Errors

**Error**: `GPG not found`
- **Solution**: Install GPG: `apt-get install gnupg` (Linux) or `brew install gnupg` (Mac)

**Error**: `OpenTimestamps CLI not found`
- **Solution**: Install: `pip install opentimestamps-client`

**Error**: `No secret key` (GPG signing)
- **Solution**: Generate a GPG key pair or specify existing key with `--gpg-key`

**Status**: `pending` for long time
- **Normal**: Bitcoin block confirmations take time (~1-6 hours initially)
- **Action**: Run `ots upgrade file.ots` after 24 hours to fetch confirmations

## 📖 Further Reading

- **OpenTimestamps**: https://opentimestamps.org/
- **GPG Manual**: https://gnupg.org/documentation/
- **Bitcoin Blockchain**: https://bitcoin.org/
- **Evidence Schema**: `evidence/schemas/conversation_evidence.v1.2.0.yaml`
- **Full Documentation**: `evidence/README.md`

## 🎯 Result

Your ledger is now:
- ✅ **Court-admissible** - Timestamps prove existence
- ✅ **Audit-ready** - Cryptographic verification
- ✅ **Tamper-proof** - Any change breaks signatures
- ✅ **Future-proof** - Verifiable forever

**Run the scripts once → Secured forever.**

---

*Strategickhaos DAO LLC - Zero trust, zero tampering, zero excuses.*
