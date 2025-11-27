# How to Verify Dossier

Use only public data/tools. Run these commands in order for complete verification.

## Prerequisites

Install required tools:
```bash
# Blake3 hash tool
pip install b3sum
# or: cargo install b3sum

# OpenTimestamps client
pip install opentimestamps-client

# GPG (usually pre-installed)
gpg --version

# jq for JSON parsing
apt-get install jq  # or: brew install jq
```

## Verification Steps

### 1. Verify Dossier Integrity (Blake3 Hashes)

```bash
# Check all file hashes
blake3 --check hashes.txt

# Or manually verify individual files
blake3 README.md
blake3 status_snapshot.json
blake3 anchors/aggregated_2025-11-27.json
```

### 2. Verify Aggregate GPG Signature

```bash
# Import the signer's public key first (if not already imported)
# gpg --recv-keys <KEY_ID>

# Verify detached signature
gpg --verify anchors/aggregated_2025-11-27.json.asc anchors/aggregated_2025-11-27.json
```

### 3. Verify OpenTimestamps Proof

```bash
# Verify OTS (requires Bitcoin connection or calendar servers)
ots verify anchors/aggregated_2025-11-27.json.ots anchors/aggregated_2025-11-27.json

# If pending, check status
ots info anchors/aggregated_2025-11-27.json.ots
```

### 4. Recompute Blake3 Hash

```bash
# Compute and compare to status_snapshot.json claims.anchors.blake3
blake3 anchors/aggregated_2025-11-27.json
```

### 5. Check JSON Determinism (Optional)

```bash
# Sort JSON keys and compute hash (should match if deterministic)
jq -S . anchors/aggregated_2025-11-27.json | blake3
```

### 6. Cross-Check GitHub (Public API)

```bash
# Check if PRs are merged
curl -s https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/6 | jq '.merged_at,.title'

# Check GitHub Actions runs
curl -s "https://api.github.com/repos/StrategicKhaos/cloud-swarm/actions/runs?branch=main" | jq '.workflow_runs[]|.id,.conclusion,.updated_at' | head -n 30
```

### 7. One-Command Verification (Python)

```bash
# Run the automated verifier
python3 verify_evidence.py
```

## Verification Checklist

- [ ] `blake3 --check hashes.txt` passes
- [ ] GPG signature valid
- [ ] OTS proof verified (or pending confirmation)
- [ ] Blake3 of aggregate matches `status_snapshot.json`
- [ ] GitHub PRs show `merged_at` timestamps
- [ ] GitHub Actions runs show `success` conclusion

## Troubleshooting

**Blake3 not found:**
```bash
pip install b3sum
# or
cargo install b3sum
```

**GPG signature fails - key not found:**
```bash
# Import the public key
gpg --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>
```

**OTS verification fails:**
```bash
# Check if proof is pending (not yet anchored in Bitcoin)
ots info anchors/aggregated_2025-11-27.json.ots

# Upgrade pending proof
ots upgrade anchors/aggregated_2025-11-27.json.ots
```

**GitHub API rate limited:**
```bash
# Use authenticated requests
curl -H "Authorization: token $GITHUB_TOKEN" ...
```
