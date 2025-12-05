# How to Verify the StrategicKhaos Evidence Dossier

This document provides exact commands for verifying the integrity and authenticity of the evidence dossier. All commands use public data only—no trust required.

## Prerequisites

Install the required tools:

```bash
# Install blake3 hash tool
pip install blake3

# Install OpenTimestamps client
pip install opentimestamps-client

# GPG should be pre-installed on most systems
gpg --version
```

## 1. Verify Dossier Integrity

Check all file hashes against the recorded values:

```bash
# Navigate to the evidence directory
cd evidence/

# Verify all hashes
blake3 --check hashes.txt
```

Expected output: All files should show `OK`.

## 2. Verify Aggregate GPG Signature

Verify the GPG detached signature on the aggregate file:

```bash
cd evidence/anchors/

# Verify signature (requires signer's public key)
gpg --verify aggregated_2025-11-27.json.asc aggregated_2025-11-27.json
```

Expected output: `Good signature from...`

## 3. Verify OpenTimestamps Proof

Verify the Bitcoin blockchain timestamp:

```bash
cd evidence/anchors/

# Verify OTS proof
ots verify aggregated_2025-11-27.json.ots
```

Expected output: Shows Bitcoin block confirmation details.

Note: If the timestamp is pending, you'll see `Pending attestation`.

## 4. Recompute Hashes Manually

Verify hashes independently:

```bash
cd evidence/anchors/

# Compute blake3 hash of aggregate
blake3 aggregated_2025-11-27.json

# Compare with value in hashes.txt and status_snapshot.json
```

## 5. Verify JSON Determinism

Ensure the JSON is canonically formatted:

```bash
cd evidence/anchors/

# Compute hash of sorted JSON
jq -S . aggregated_2025-11-27.json | blake3
```

The hash should match the recorded value if JSON was canonically formatted.

## 6. Cross-Check GitHub API

Verify PR and Actions data via public GitHub API:

```bash
# Check PR merge status (replace with actual repo)
curl -s "https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/6" | jq '.merged_at,.title'

# Check recent Actions runs
curl -s "https://api.github.com/repos/StrategicKhaos/cloud-swarm/actions/runs?branch=main" | jq '.workflow_runs[]|.id,.conclusion,.updated_at' | head -n 30
```

For private repos, exported metadata is available in `actions_runs.json`.

## 7. One-Command Verification

Run the automated verification script:

```bash
cd evidence/
python3 verify_evidence.py
```

Exit code 0 = all checks passed.

## 8. Manual File Hash Verification

Generate hashes for individual files:

```bash
cd evidence/

# Hash the status snapshot
blake3 status_snapshot.json

# Hash the README
blake3 README.md

# Hash the aggregate
blake3 anchors/aggregated_2025-11-27.json

# Hash the provenance file
blake3 anchors/aggregated_2025-11-27.json.prov.json
```

## Verification Summary

| Check | Command | Expected Result |
|-------|---------|-----------------|
| Integrity | `blake3 --check hashes.txt` | All OK |
| GPG Sig | `gpg --verify *.asc *.json` | Good signature |
| OTS | `ots verify *.ots` | Confirmed block |
| GitHub PRs | `curl ... \| jq '.merged_at'` | Non-null date |
| CI Status | `curl ... \| jq '.conclusion'` | "success" |

## Troubleshooting

**"blake3: command not found"**
```bash
pip install blake3
# Or use: python3 -c "import blake3; print(blake3.blake3(open('file','rb').read()).hexdigest())"
```

**"ots: command not found"**
```bash
pip install opentimestamps-client
```

**GPG signature verification fails**
```bash
# Import the signer's public key first
gpg --import signer-public-key.asc
gpg --verify aggregated_2025-11-27.json.asc aggregated_2025-11-27.json
```

**GitHub API rate limited**
```bash
# Use authenticated requests
curl -H "Authorization: token YOUR_TOKEN" "https://api.github.com/..."
```
