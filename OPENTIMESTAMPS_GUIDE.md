# OpenTimestamps Guide for Sovereign Documents

This guide explains how to use OpenTimestamps to anchor sovereign documents to the Bitcoin blockchain, creating cryptographic proof that a document existed at a specific point in time.

---

## Table of Contents

1. [What is OpenTimestamps?](#what-is-opentimestamps)
2. [Installation](#installation)
3. [Creating Timestamps](#creating-timestamps)
4. [Verifying Timestamps](#verifying-timestamps)
5. [Upgrading Timestamps](#upgrading-timestamps)
6. [Workflow Integration](#workflow-integration)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## What is OpenTimestamps?

### Overview
OpenTimestamps (OTS) is a free, open-source, decentralized timestamping service that creates cryptographic proof that data existed at a specific time, without revealing the data itself.

### How It Works
1. **Hash Creation**: Computes SHA256 hash of your document
2. **Calendar Submission**: Submits hash to public calendar servers
3. **Bitcoin Anchoring**: Calendar servers aggregate hashes and anchor to Bitcoin blockchain
4. **Proof Generation**: Creates `.ots` file containing Merkle tree proof linking your hash to a Bitcoin transaction

### Key Benefits
- **Decentralized**: No central authority controls the timestamps
- **Private**: Only the hash is submitted, not the document content
- **Permanent**: Bitcoin blockchain is immutable and widely distributed
- **Free**: No cost to create timestamps (only Bitcoin transaction fees, paid by calendar operators)
- **Verifiable**: Anyone can independently verify the timestamp

### Security Model
- **Trust-minimized**: Verification only requires Bitcoin blockchain data
- **Tamper-evident**: Any modification to the document invalidates the proof
- **Future-proof**: Proofs remain valid as long as Bitcoin exists

---

## Installation

### Option 1: Python Client (Recommended)

```bash
# Install via pip
pip install opentimestamps-client

# Verify installation
ots --version
```

### Option 2: From Source

```bash
# Clone repository
git clone https://github.com/opentimestamps/opentimestamps-client.git
cd opentimestamps-client

# Install dependencies
pip install -r requirements.txt

# Install client
python setup.py install
```

### Option 3: Docker

```bash
# Pull Docker image
docker pull opentimestamps/ots-client

# Create alias for convenience
alias ots='docker run --rm -v $(pwd):/data opentimestamps/ots-client'
```

### Option 4: PowerShell (Windows)

```powershell
# Install Python first from python.org
# Then in PowerShell:
pip install opentimestamps-client

# Verify
ots --version
```

---

## Creating Timestamps

### Basic Timestamping

```bash
# Timestamp a single file
ots stamp SOVEREIGN_MANIFEST_v1.0.md

# This creates: SOVEREIGN_MANIFEST_v1.0.md.ots
```

**What happens:**
1. SHA256 hash computed from file
2. Hash submitted to multiple calendar servers
3. `.ots` file created immediately (with pending status)
4. After ~1 hour, Bitcoin block confirmation occurs

### Timestamping Multiple Files

```bash
# Timestamp all markdown files
ots stamp *.md

# Timestamp specific files
ots stamp SOVEREIGN_MANIFEST_v1.0.md README.md SECURITY.md
```

### Batch Timestamping Script

```bash
#!/bin/bash
# timestamp_all_docs.sh - Timestamp all documentation files

FILES=(
    "SOVEREIGN_MANIFEST_v1.0.md"
    "README.md"
    "SECURITY.md"
    "CONTRIBUTORS.md"
    "dao_record_v1.0.yaml"
)

for file in "${FILES[@]}"; do
    echo "Timestamping: $file"
    ots stamp "$file"
    echo "Created: ${file}.ots"
done

echo "All files timestamped. Run 'ots upgrade *.ots' after 1 hour to get Bitcoin confirmation."
```

### PowerShell Version

```powershell
# timestamp_all_docs.ps1
$files = @(
    "SOVEREIGN_MANIFEST_v1.0.md",
    "README.md",
    "SECURITY.md"
)

foreach ($file in $files) {
    Write-Host "Timestamping: $file"
    ots stamp $file
    Write-Host "Created: $file.ots"
}

Write-Host "All files timestamped. Run upgrade after 1 hour for Bitcoin confirmation."
```

---

## Verifying Timestamps

### Basic Verification

```bash
# Verify a timestamp
ots verify SOVEREIGN_MANIFEST_v1.0.md.ots

# Verify with verbose output
ots verify --verbose SOVEREIGN_MANIFEST_v1.0.md.ots
```

**Expected output (after Bitcoin confirmation):**
```
Success! Bitcoin block 820000 attests data existed as of 2025-11-24 UTC
```

**Before Bitcoin confirmation:**
```
Timestamp is pending confirmation in Bitcoin blockchain
```

### Verification Without Original File

```bash
# If you only have the .ots file and the original document:
ots verify --hash sha256:abc123def456... timestamp.ots

# Or specify the original file explicitly
ots verify --file SOVEREIGN_MANIFEST_v1.0.md timestamp.ots
```

### Detailed Information

```bash
# Show detailed timestamp information
ots info SOVEREIGN_MANIFEST_v1.0.md.ots

# Shows:
# - Calendar servers used
# - Merkle tree structure
# - Bitcoin block information
# - Transaction ID
```

### Verification Script

```bash
#!/bin/bash
# verify_all_timestamps.sh

for ots_file in *.ots; do
    echo "Verifying: $ots_file"
    if ots verify "$ots_file"; then
        echo "✓ Valid timestamp"
    else
        echo "✗ Verification failed"
    fi
    echo "---"
done
```

---

## Upgrading Timestamps

### Why Upgrade?

When you first create a timestamp with `ots stamp`, the `.ots` file is created immediately but doesn't yet contain Bitcoin blockchain proof. Calendar servers batch multiple timestamps together and submit them to Bitcoin every ~1 hour.

### Upgrade Process

```bash
# Upgrade a single timestamp (after ~1 hour)
ots upgrade SOVEREIGN_MANIFEST_v1.0.md.ots

# Upgrade all timestamps
ots upgrade *.ots

# Upgrade with verbose output
ots upgrade --verbose SOVEREIGN_MANIFEST_v1.0.md.ots
```

**What happens:**
1. Queries calendar servers for Bitcoin confirmation
2. Downloads complete Merkle tree proof
3. Updates `.ots` file with blockchain data
4. File becomes fully verified (no longer "pending")

### Automated Upgrade Script

```bash
#!/bin/bash
# auto_upgrade.sh - Automatically upgrade timestamps every hour

while true; do
    echo "$(date): Checking for timestamp upgrades..."
    
    for ots_file in *.ots; do
        if ots upgrade "$ots_file" 2>&1 | grep -q "Success"; then
            echo "✓ Upgraded: $ots_file"
        fi
    done
    
    echo "Sleeping for 1 hour..."
    sleep 3600
done
```

### Cron Job for Automatic Upgrades

```bash
# Add to crontab (runs every hour)
0 * * * * cd /path/to/repo && ots upgrade *.ots >> /var/log/ots-upgrade.log 2>&1
```

---

## Workflow Integration

### Git Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Automatically timestamp important files before commit

IMPORTANT_FILES=(
    "SOVEREIGN_MANIFEST_v1.0.md"
    "dao_record_v1.0.yaml"
)

for file in "${IMPORTANT_FILES[@]}"; do
    if git diff --cached --name-only | grep -q "^${file}$"; then
        echo "Timestamping: $file"
        ots stamp "$file"
        git add "${file}.ots"
    fi
done
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions Workflow

Create `.github/workflows/opentimestamps.yml`:

```yaml
name: OpenTimestamps

on:
  push:
    branches: [main]
    paths:
      - 'SOVEREIGN_MANIFEST_v1.0.md'
      - 'dao_record_v1.0.yaml'
      - '*.md'

jobs:
  timestamp:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install OpenTimestamps
        run: pip install opentimestamps-client
      
      - name: Timestamp changed files
        run: |
          git diff --name-only HEAD~1 HEAD | grep -E '\.(md|yaml)$' | while read file; do
            echo "Timestamping: $file"
            ots stamp "$file"
          done
      
      - name: Commit timestamp files
        run: |
          git config user.name "OTS Bot"
          git config user.email "bot@example.com"
          git add *.ots
          git commit -m "Add OpenTimestamps proofs" || echo "No new timestamps"
          git push
```

### CI/CD Integration

```bash
# In your deployment pipeline
#!/bin/bash
# deploy_with_timestamp.sh

# 1. Timestamp manifest before deployment
ots stamp SOVEREIGN_MANIFEST_v1.0.md

# 2. Deploy application
./deploy.sh

# 3. Wait for Bitcoin confirmation (in background)
nohup bash -c '
    sleep 3600
    ots upgrade SOVEREIGN_MANIFEST_v1.0.md.ots
    git add SOVEREIGN_MANIFEST_v1.0.md.ots
    git commit -m "Update timestamp with Bitcoin confirmation"
    git push
' &

echo "Deployment complete. Timestamp will be upgraded in ~1 hour."
```

---

## Best Practices

### 1. Timestamp Finalized Documents Only

```bash
# DON'T timestamp work-in-progress files
# DO timestamp only after final review

# Good workflow:
git add SOVEREIGN_MANIFEST_v1.0.md
git commit -m "Finalize manifest v1.0"
ots stamp SOVEREIGN_MANIFEST_v1.0.md
git add SOVEREIGN_MANIFEST_v1.0.md.ots
git commit -m "Add timestamp proof for manifest v1.0"
```

### 2. Keep .ots Files With Documents

```bash
# Store .ots files in the same directory as originals
SOVEREIGN_MANIFEST_v1.0.md
SOVEREIGN_MANIFEST_v1.0.md.ots

# Track them in git
git add *.ots
```

### 3. Verify Before Important Actions

```bash
# Before legal proceedings, verify all timestamps
ots verify --verbose *.ots > timestamp_verification_report.txt
```

### 4. Document Timestamp Information

Add to your manifest:
```markdown
## Cryptographic Attestation

**Document Hash (SHA256):** [hash]
**OpenTimestamps File:** SOVEREIGN_MANIFEST_v1.0.md.ots
**Bitcoin Block Height:** [block]
**Timestamp:** [date/time]
**Verification Command:** `ots verify SOVEREIGN_MANIFEST_v1.0.md.ots`
```

### 5. Regular Upgrades

```bash
# Run weekly to ensure all timestamps are upgraded
0 0 * * 0 cd /repo && ots upgrade *.ots
```

### 6. Backup .ots Files

```bash
# .ots files are small but critical - back them up
tar czf ots_backups_$(date +%Y%m%d).tar.gz *.ots

# Or push to separate backup repo
git clone https://github.com/YourOrg/timestamp-proofs-backup.git
cp *.ots timestamp-proofs-backup/
cd timestamp-proofs-backup
git add *.ots
git commit -m "Backup timestamps $(date +%Y-%m-%d)"
git push
```

---

## Troubleshooting

### Issue: "Calendar server unreachable"

```bash
# Try upgrading later
ots upgrade --verbose SOVEREIGN_MANIFEST_v1.0.md.ots

# Or specify different calendar servers
ots stamp --calendar https://alice.btc.calendar.opentimestamps.org SOVEREIGN_MANIFEST_v1.0.md
```

### Issue: "Pending" status persists

```bash
# Wait at least 1-2 hours after stamping
# Then try upgrading
ots upgrade SOVEREIGN_MANIFEST_v1.0.md.ots

# Check Bitcoin network status
# (If Bitcoin network is congested, confirmation may take longer)
```

### Issue: "Verification failed"

```bash
# Ensure file hasn't been modified
sha256sum SOVEREIGN_MANIFEST_v1.0.md

# Try verbose verification
ots verify --verbose SOVEREIGN_MANIFEST_v1.0.md.ots

# Check if .ots file is corrupted
ots info SOVEREIGN_MANIFEST_v1.0.md.ots
```

### Issue: "File not found" during verification

```bash
# Verification requires both the original file AND .ots file in same directory
ls -la SOVEREIGN_MANIFEST_v1.0.md*

# If original file is missing, verification will fail
# You must have the exact original file to verify
```

### Issue: Multiple calendar servers timeout

```bash
# Check your internet connection
ping calendar.opentimestamps.org

# Try stamping with specific calendar
ots stamp --calendar https://bob.btc.calendar.opentimestamps.org file.md

# Or wait and try again later
```

---

## Advanced Usage

### Creating Detached Timestamps

```bash
# Create timestamp from raw hash (doesn't require original file)
echo "abc123..." | ots stamp -

# Useful for timestamping secrets without revealing them
sha256sum secret_file.txt | ots stamp -
```

### Multi-Calendar Redundancy

```bash
# Stamp to multiple calendar servers for redundancy
ots stamp \
    --calendar https://alice.btc.calendar.opentimestamps.org \
    --calendar https://bob.btc.calendar.opentimestamps.org \
    --calendar https://finney.calendar.opentimestamps.org \
    SOVEREIGN_MANIFEST_v1.0.md
```

### Programmatic Integration (Python)

```python
#!/usr/bin/env python3
from opentimestamps.core.timestamp import Timestamp
from opentimestamps.core.op import OpSHA256
import hashlib

# Compute file hash
with open('SOVEREIGN_MANIFEST_v1.0.md', 'rb') as f:
    file_hash = hashlib.sha256(f.read()).digest()

# Create timestamp
timestamp = Timestamp(file_hash)

# Submit to calendar servers
# ... (see opentimestamps-client source for details)

print(f"Timestamp created for hash: {file_hash.hex()}")
```

---

## Resources

### Official Documentation
- [OpenTimestamps Website](https://opentimestamps.org)
- [GitHub Repository](https://github.com/opentimestamps/opentimestamps-client)
- [Python API Docs](https://github.com/opentimestamps/python-opentimestamps)

### Public Calendar Servers
- `https://alice.btc.calendar.opentimestamps.org`
- `https://bob.btc.calendar.opentimestamps.org`
- `https://finney.calendar.opentimestamps.org`

### Bitcoin Blockchain Explorers
- [Blockstream.info](https://blockstream.info)
- [Blockchain.com](https://blockchain.com)
- [BTC.com](https://btc.com)

### Community
- [OpenTimestamps Forum](https://groups.google.com/forum/#!forum/opentimestamps)
- [Bitcoin Talk Thread](https://bitcointalk.org/index.php?topic=1662466)

---

## Summary

OpenTimestamps provides **cryptographic proof** that your sovereign documents existed at a specific point in time by anchoring them to the Bitcoin blockchain.

**Key Commands:**
```bash
ots stamp file.md          # Create timestamp
ots upgrade file.md.ots    # Get Bitcoin confirmation (after 1 hour)
ots verify file.md.ots     # Verify timestamp
ots info file.md.ots       # Show timestamp details
```

**Remember:**
- Timestamp finalized documents only
- Keep .ots files with original documents
- Upgrade after 1-2 hours for Bitcoin confirmation
- Verify regularly to ensure integrity
- Back up both original files and .ots proofs

---

**This guide itself can be timestamped:**
```bash
ots stamp OPENTIMESTAMPS_GUIDE.md
```
