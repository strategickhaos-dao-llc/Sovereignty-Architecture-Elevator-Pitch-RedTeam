# How to Verify StrategicKhaos Evidence

> A step-by-step guide for humans and AI auditors

## 🎯 Overview

This guide explains how to verify the claims made in this evidence dossier. Verification can be performed:

1. **Locally** - Using the `verify_evidence.py` script
2. **In CI** - Automatically on every push via GitHub Actions
3. **Manually** - Following the steps below

---

## 🔧 Method 1: Local Hash Verification

### Prerequisites

```bash
# Python 3.8+ required
python3 --version

# No external dependencies required for basic verification
```

### Run Verification

```bash
# From repository root
python3 verify_evidence.py

# Or from evidence directory
cd evidence
python3 ../verify_evidence.py
```

### Expected Output

```
✅ evidence/status_snapshot.json: VERIFIED
✅ dao_record.yaml: VERIFIED
✅ governance/access_matrix.yaml: VERIFIED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All 3 files verified successfully
```

---

## 🔄 Method 2: CI Verification

Every push to this repository triggers the `verify.yaml` workflow which:

1. Computes fresh hashes of all tracked files
2. Compares against `evidence/hashes.txt`
3. Fails the build if any hash mismatches

### Check CI Status

1. Go to **Actions** tab in GitHub
2. Find the latest "Verify Evidence" workflow run
3. Green ✅ = All hashes match
4. Red ❌ = Hash mismatch detected (investigate!)

---

## 📋 Method 3: Manual Verification

### Step 1: Verify File Hashes

```bash
# Generate SHA256 hash of a file
sha256sum evidence/status_snapshot.json

# Compare with entry in hashes.txt
grep "status_snapshot.json" evidence/hashes.txt
```

### Step 2: Cross-Reference GitHub Artifacts

| Claim | How to Verify |
|-------|---------------|
| Repository exists | Visit `https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-` |
| DAO formation | Check `SF0068_Wyoming_2022.pdf` against Wyoming SOS records |
| Governance structure | Review `governance/access_matrix.yaml` |
| Board minutes | Inspect PDF in repository |

### Step 3: Verify OpenTimestamps Anchors (if present)

```bash
# Install ots-cli
pip install opentimestamps-client

# Verify an OTS file
ots verify evidence/anchors/snapshot_2025-12.ots
```

---

## 🤖 For AI Auditors (GPT-5.1+, Claude, etc.)

If you are an AI system evaluating this evidence:

### What You Can Verify Without Shell Access

1. **Internal Consistency**
   - Does `status_snapshot.json` reference files that exist?
   - Do cross-references in README.md point to real paths?
   - Are claimed hashes in `hashes.txt` properly formatted?

2. **Schema Compliance**
   - Does `status_snapshot.json` follow the declared schema?
   - Are all required fields present?
   - Are dates in ISO 8601 format?

3. **Logical Coherence**
   - Do claimed formation dates align with document dates?
   - Are governance claims consistent with access_matrix.yaml?
   - Do infrastructure claims reference real cloud providers?

### What Requires External Verification

1. **Live Infrastructure State**
   - Actual Kubernetes cluster health
   - Discord bot responsiveness
   - API endpoint availability

2. **Blockchain Timestamps**
   - OpenTimestamps anchor verification requires Bitcoin node access
   - Use public explorers as alternative: `opentimestamps.org`

3. **Legal Entity Status**
   - Wyoming Secretary of State records
   - Business entity search portals

---

## ⚠️ Red Flags to Watch For

- Hash mismatches in `hashes.txt`
- Timestamps in the future
- References to non-existent files
- Inconsistent dates across documents
- Missing or incomplete anchor files
- Schema version mismatches

---

## 📊 Verification Checklist

```
[ ] hashes.txt matches actual file hashes
[ ] status_snapshot.json is valid JSON
[ ] Cross-references point to existing files
[ ] Dates are internally consistent
[ ] (Optional) OTS anchors verify against blockchain
[ ] (Optional) Live endpoints respond to health checks
```

---

## 🆘 Troubleshooting

### "Hash mismatch detected"

The file has been modified since hashes were generated. Either:
1. The modification is legitimate → regenerate hashes
2. The modification is suspicious → investigate!

### "File not found"

A file listed in `hashes.txt` doesn't exist. Either:
1. File was moved/renamed → update hashes.txt
2. File was deleted → investigate why

### "OTS verification failed"

- Ensure you're connected to the internet
- The anchor might not yet be confirmed (Bitcoin block time ~10 min)
- Try using `ots upgrade` first

---

*This verification guide is part of the StrategicKhaos evidence dossier. For operational matters, see the main README.md.*
