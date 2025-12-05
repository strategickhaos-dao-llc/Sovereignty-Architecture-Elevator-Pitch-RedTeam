# How to Verify

This document contains commands to verify the integrity and authenticity of the StrategicKhaos proof evidence.

## Prerequisites

Install required tools:
```bash
pip install blake3
apt-get install gnupg  # or brew install gnupg on macOS
pip install opentimestamps-client  # for OTS verification
```

## Verification Commands

### 1. Verify Blake3 Hashes
```bash
blake3 --check hashes.txt
```

Or using Python:
```bash
python3 -c "import blake3; import pathlib
for line in open('hashes.txt'):
    hash_val, fname = line.strip().split('  ')
    actual = blake3.blake3(pathlib.Path(fname).read_bytes()).hexdigest()
    status = '✓' if actual == hash_val else '✗'
    print(f'{status} {fname}')"
```

### 2. Verify GPG Signature
```bash
gpg --verify anchors/aggregated_2025-11-27_v2.json.asc anchors/aggregated_2025-11-27_v2.json
```

### 3. Verify OpenTimestamps
```bash
ots verify anchors/aggregated_2025-11-27_v2.json.ots anchors/aggregated_2025-11-27_v2.json
```

### 4. Verify Aggregate File Hash
```bash
blake3 anchors/aggregated_2025-11-27_v2.json
```

Expected output:
```
48215cbeff837b9598d75f5ddf2aa2a5cfe867a2c54cedd7e1d834486c1c8434
```

### 5. Verify Canonical Hash (jq sorted)
```bash
jq -S . anchors/aggregated_2025-11-27_v2.json | blake3
```

### 6. Verify GitHub PR Status
```bash
curl -s https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/6 | jq '.merged_at,.title'
```

### 7. Verify GitHub Actions Status
```bash
curl -s "https://api.github.com/repos/StrategicKhaos/cloud-swarm/actions/runs?branch=main" | jq '.workflow_runs[]|.id,.conclusion,.updated_at' | head -n 30
```

## One-Command Verification

Run the automated verification script:
```bash
python3 verify_evidence.py
```

## Manual Cross-Reference

1. Compare `status_snapshot.json` claims against the anchor file
2. Verify the blake3 hash in `status_snapshot.json` matches the computed hash
3. Check GitHub PRs and Actions runs match the claimed sources
