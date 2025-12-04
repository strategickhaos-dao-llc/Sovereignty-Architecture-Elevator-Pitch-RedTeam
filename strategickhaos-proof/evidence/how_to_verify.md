# How to Verify StrategicKhaos Evidence

**Step-by-step verification guide for humans and AI auditors**

## 🎯 Verification Overview

This guide explains how to verify the claims made in the StrategicKhaos Evidence Dossier. The verification process is designed to be:

1. **Deterministic** - Same inputs produce same verification results
2. **Offline-capable** - Core verification doesn't require network access
3. **Machine-readable** - AI systems can parse and verify programmatically
4. **Human-auditable** - Clear steps for manual verification

---

## 📋 Prerequisites

### For Local Verification

```bash
# Python 3.8+ required
python --version

# Install BLAKE3 hasher
pip install blake3

# Clone the repository (if not already present)
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-/strategickhaos-proof
```

### For AI Auditors

- HTTP access to GitHub API
- JSON parsing capability
- BLAKE3 hash computation (or trust CI verification)

---

## ✅ Verification Steps

### Step 1: Verify Hash Manifest

The hash manifest (`evidence/hashes.txt`) contains BLAKE3 hashes of key files.

#### Automated Verification

```bash
python verify_evidence.py
```

#### Manual Verification

```bash
# For each entry in hashes.txt:
# Format: <hash>  <relative_path>

# Example verification:
cd ..  # Go to repository root
blake3sum dao_record.yaml
# Compare output with entry in strategickhaos-proof/evidence/hashes.txt
```

### Step 2: Verify Cross-References

Cross-references in `status_snapshot.json` should resolve to actual files.

#### Automated

```bash
python verify_evidence.py --check-refs
```

#### Manual

```bash
# For each cross_reference in status_snapshot.json:
# Verify the file exists at the specified path

ls -la ../src/bot.ts
ls -la ../src/event-gateway.ts
ls -la ../dao_record.yaml
ls -la ../governance/access_matrix.yaml
```

### Step 3: Verify GitHub Metadata

Some claims can be verified via GitHub API:

```bash
# Repository existence and metadata
curl -s https://api.github.com/repos/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch- | jq '.full_name, .created_at, .updated_at'

# Commit history
curl -s https://api.github.com/repos/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/commits | jq '.[0:5] | .[] | .sha, .commit.message'

# Contributors
curl -s https://api.github.com/repos/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/contributors | jq '.[] | .login'
```

### Step 4: Verify OTS Anchors (Optional)

OpenTimestamps anchors in `evidence/anchors/` provide blockchain-anchored timestamps.

```bash
# Install OpenTimestamps client
pip install opentimestamps-client

# Verify a .ots file
ots verify evidence/anchors/<filename>.ots

# Output will show Bitcoin blockchain timestamp
```

### Step 5: Verify Legal Claims (External)

Some claims require external verification:

| Claim | Verification Method |
|-------|---------------------|
| Wyoming DAO LLC | Wyoming Secretary of State business search |
| SF0068 Compliance | Compare with Wyoming SF0068 statute |
| Board Minutes | Cross-reference with PDF documents |

---

## 🤖 For AI Auditors

### Machine-Readable Verification

```python
import json
import hashlib

# 1. Load status snapshot
with open('evidence/status_snapshot.json') as f:
    snapshot = json.load(f)

# 2. Verify schema version
assert snapshot['schema_version'] == '1.0.0'

# 3. Verify cross-references exist
import os
for ref in snapshot['cross_references']:
    for evidence_path in ref['evidence']:
        full_path = os.path.join('..', evidence_path)
        if not os.path.exists(full_path):
            print(f"WARNING: Missing reference: {evidence_path}")

# 4. Verify hash manifest
with open('evidence/hashes.txt') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            expected_hash, filepath = line.strip().split('  ')
            # Compute actual hash and compare
```

### Verification Response Format

AI auditors should produce verification reports in this format:

```json
{
  "verification_id": "unique-verification-id",
  "timestamp": "ISO-8601 timestamp",
  "snapshot_verified": "sk-proof-2024-001",
  "results": {
    "hash_verification": "PASS|FAIL",
    "cross_reference_check": "PASS|FAIL|PARTIAL",
    "schema_validation": "PASS|FAIL",
    "ots_verification": "PASS|FAIL|SKIPPED"
  },
  "issues": [],
  "confidence": 0.0-1.0,
  "verifier_identity": "AI model identifier"
}
```

---

## 🔴 Common Verification Failures

### Hash Mismatch

**Cause**: File was modified after hash was computed.

**Resolution**: 
1. Check if modification was intentional
2. If intentional, regenerate hashes: `python verify_evidence.py --regenerate`
3. If not intentional, investigate potential tampering

### Missing Cross-Reference

**Cause**: Referenced file was moved or deleted.

**Resolution**:
1. Update `status_snapshot.json` with correct path
2. Or restore the missing file

### OTS Verification Failure

**Cause**: Timestamp not yet anchored (pending) or invalid.

**Resolution**:
1. Wait for Bitcoin confirmation (can take hours)
2. Check OTS server status
3. Verify .ots file integrity

---

## 📊 Verification Confidence Levels

| Level | Description | Achieved When |
|-------|-------------|---------------|
| **HIGH** | Cryptographically verified | All hashes match + OTS verified |
| **MEDIUM** | Structurally consistent | Hashes match, OTS pending/skipped |
| **LOW** | Partially verified | Some checks pass, others fail |
| **NONE** | Cannot verify | Hash mismatches or missing files |

---

## 🔄 CI Verification

Every push to this repository triggers automatic verification via GitHub Actions:

- Workflow: `.github/workflows/verify.yaml`
- Checks: Hash verification, cross-reference validation
- Badge: ![Verification](../../.github/badges/verify-status.svg) (if configured)

---

*Part of the StrategicKhaos Proof Evidence Dossier*
