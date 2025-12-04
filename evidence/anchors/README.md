# Cryptographic Anchors Directory

> Placeholder structure for .json, .asc, and .ots files

## 📁 Purpose

This directory stores cryptographic anchors that prove the existence and state of StrategicKhaos infrastructure at specific points in time.

## 🔐 Anchor Types

### JSON Snapshots (`*.json`)
Machine-readable state captures containing:
- Infrastructure status
- Deployment checksums  
- Governance state

### GPG Signatures (`*.asc`)
Detached ASCII-armored signatures created with authorized keys:
- Proves who signed the snapshot
- Can be verified with public keyring

### OpenTimestamps (`*.ots`)
Bitcoin blockchain anchors:
- Proves snapshot existed at a specific time
- Tamper-evident timestamp
- Verifiable via `ots verify`

## 📋 Naming Convention

```
snapshot_YYYY-MM[-DD].json       # State snapshot
snapshot_YYYY-MM[-DD].json.asc   # GPG signature of snapshot
snapshot_YYYY-MM[-DD].ots        # OpenTimestamps proof
```

## 🛠️ How to Create Anchors

### 1. Create Snapshot
```bash
# Generate or update status_snapshot.json
python3 ../verify_evidence.py --generate-snapshot
```

### 2. Sign with GPG
```bash
# Sign the snapshot
gpg --armor --detach-sign snapshot_2025-12.json
# Creates: snapshot_2025-12.json.asc
```

### 3. Create OTS Anchor
```bash
# Install opentimestamps-client
pip install opentimestamps-client

# Create timestamp
ots stamp snapshot_2025-12.json
# Creates: snapshot_2025-12.json.ots

# Wait for confirmation (~10 min for Bitcoin block)
ots upgrade snapshot_2025-12.json.ots
```

### 4. Verify Later
```bash
# Verify GPG signature
gpg --verify snapshot_2025-12.json.asc snapshot_2025-12.json

# Verify OTS timestamp
ots verify snapshot_2025-12.json.ots
```

## ⚠️ Current Status

**This directory is a placeholder.**

To populate with real anchors:

1. Run your `legion deploy` or equivalent
2. Capture the actual state into JSON
3. Sign and timestamp as described above
4. Commit the anchor files here

## 🔗 Related

- Parent README: `../README.md`
- Verification guide: `../how_to_verify.md`
- Hash manifest: `../hashes.txt`

---

*Anchors provide the "blockchain-notarized" layer of proof for AI auditors.*
