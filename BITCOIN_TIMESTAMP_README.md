# Bitcoin Timestamp for Sovereign Manifest

## Overview

This directory contains the Sovereign Manifest and tools to create an immutable Bitcoin timestamp proving its existence at a specific point in time.

## Files

- **SOVEREIGN_MANIFEST_v1.0.md** - The complete sovereignty declaration (✅ Created)
- **SOVEREIGN_MANIFEST_v1.0.md.ots** - Bitcoin timestamp proof (⏳ Pending network access)
- **create-bitcoin-timestamp.sh** - Bash script to create timestamp (Linux/macOS)
- **create-bitcoin-timestamp.ps1** - PowerShell script to create timestamp (Windows/PowerShell Core)

## Current Status

```
Sovereignty Completion: 99.9%
████████████████████████████████████▉

✅ Manifest created and hashed
✅ Helper scripts created  
⏳ Bitcoin timestamp pending (requires network access)
```

**SHA256 Hash**: `cd8787bf04b157a840d9e5c56e9ac1cf2d0b140926a226cd8cfb06207f272fb5`

## Why Bitcoin Timestamping?

Bitcoin timestamping via OpenTimestamps creates an immutable proof that:

1. **The document existed** at a specific moment in time
2. **The document is unchanged** since that moment (via SHA256 hash)
3. **The proof is permanent** and stored in the Bitcoin blockchain
4. **The proof is verifiable** by anyone, forever, without trusting any authority

This makes the sovereignty declaration cryptographically anchored to the most secure and decentralized network in existence.

## Quick Start

### Option 1: Automated Script (Recommended)

#### On Linux/macOS:
```bash
./create-bitcoin-timestamp.sh
```

#### On Windows/PowerShell:
```powershell
.\create-bitcoin-timestamp.ps1
```

### Option 2: Manual PowerShell Command (One-liner from problem statement)

```powershell
iwr https://btc.calendar.catallaxy.com -Method POST -Body ([System.Text.Encoding]::UTF8.GetBytes((Get-Content .\SOVEREIGN_MANIFEST_v1.0.md -Raw))) -ContentType "application/octet-stream" -OutFile SOVEREIGN_MANIFEST_v1.0.md.ots
```

### Option 3: OpenTimestamps CLI

```bash
# Install (if needed)
pip install opentimestamps-client

# Create timestamp
ots stamp SOVEREIGN_MANIFEST_v1.0.md

# Wait 30-60 seconds for completion
```

### Option 4: curl (Linux/macOS)

```bash
curl -X POST https://btc.calendar.catallaxy.com \
  -H "Content-Type: application/octet-stream" \
  --data-binary @SOVEREIGN_MANIFEST_v1.0.md \
  -o SOVEREIGN_MANIFEST_v1.0.md.ots
```

## Verification

Once the `.ots` file is created, verify it:

```bash
# Check if timestamp was created successfully
ots info SOVEREIGN_MANIFEST_v1.0.md.ots

# Verify the timestamp (after Bitcoin confirmation)
ots verify SOVEREIGN_MANIFEST_v1.0.md.ots
```

## Understanding the Process

### 1. File Hashing
The SHA256 hash of `SOVEREIGN_MANIFEST_v1.0.md` is calculated:
```
cd8787bf04b157a840d9e5c56e9ac1cf2d0b140926a226cd8cfb06207f272fb5
```

### 2. Calendar Submission
This hash is submitted to OpenTimestamps calendar servers, which aggregate multiple timestamps together for efficiency.

### 3. Bitcoin Commitment
The calendar server creates a Merkle tree of all pending timestamps and commits the root hash to the Bitcoin blockchain in a transaction's `OP_RETURN` field.

### 4. Proof Generation
The `.ots` file contains the cryptographic proof linking your document's hash to the Bitcoin transaction.

### 5. Verification
Anyone can independently verify this proof without trusting any authority - they just need:
- The original file
- The `.ots` file  
- Access to the Bitcoin blockchain

## Timeline

| Stage | Duration | Description |
|-------|----------|-------------|
| Submission | 1-30 seconds | File sent to calendar servers |
| Aggregation | 1-60 minutes | Calendars batch timestamps together |
| Bitcoin Confirmation | 10-60 minutes | Transaction included in a block |
| Full Security | 1-6 hours | Multiple block confirmations |

## Why This Failed in GitHub Actions

The GitHub Actions environment has restricted network access for security reasons. The OpenTimestamps calendar servers are not accessible from within the CI/CD environment. This is intentional and protects against:

- Malicious code exfiltrating data
- Unauthorized network access
- Supply chain attacks

**Solution**: Create the timestamp from your local machine with full network access.

## Network Requirements

To create the timestamp, you need:
- ✅ Internet connection
- ✅ Access to OpenTimestamps calendar servers (ports 80/443)
- ✅ No firewall blocking outbound HTTPS
- ✅ DNS resolution working

If behind a corporate firewall, you may need to:
- Use a VPN
- Request firewall exceptions for OpenTimestamps servers
- Use a different network (home, mobile hotspot, etc.)

## Alternative Calendar Servers

If the default servers don't work, try these alternatives:

```bash
# Catallaxy (recommended)
https://btc.calendar.catallaxy.com
https://ots.btc.catallaxy.com/timestamp

# OpenTimestamps Official
https://alice.btc.calendar.opentimestamps.org/timestamp
https://bob.btc.calendar.opentimestamps.org/timestamp

# EternityWall
https://a.pool.eternitywall.com/timestamp

# Pool Servers
https://a.pool.opentimestamps.org/timestamp
https://b.pool.opentimestamps.org/timestamp
```

## After Creating the Timestamp

1. **Verify it worked**:
   ```bash
   ots info SOVEREIGN_MANIFEST_v1.0.md.ots
   ```

2. **Commit to repository**:
   ```bash
   git add SOVEREIGN_MANIFEST_v1.0.md.ots
   git commit -m "Add Bitcoin timestamp - Sovereignty 100% complete"
   git push
   ```

3. **Delete the instructions file** (no longer needed):
   ```bash
   git rm SOVEREIGN_MANIFEST_v1.0.md.ots.instructions
   git commit -m "Remove timestamp instructions - no longer needed"
   git push
   ```

## Troubleshooting

### "Connection refused" or "Could not resolve host"
- Check internet connectivity
- Try a different calendar server
- Disable VPN temporarily
- Check firewall settings

### "Failed to create timestamp: need at least 2 attestations"
- Network timeout - try again
- Calendar servers are temporarily down - try alternative servers
- Use different method (PowerShell vs CLI vs curl)

### File created but appears corrupted
- Ensure you're using `--data-binary` with curl (not `--data`)
- Ensure UTF-8 encoding is preserved
- Try the automated scripts instead of manual commands

### Want to verify without waiting for Bitcoin confirmation
The `.ots` file is created immediately and contains a "pending" attestation. Full verification requires Bitcoin confirmation, but the timestamp is valid from the moment it's created.

## Security Notes

1. **The `.ots` file is safe to commit** - it contains only public cryptographic proofs
2. **The manifest hash is public** - but the content proves its integrity
3. **No private keys involved** - this is a read-only proof system
4. **Verification is trustless** - anyone can verify independently

## What Happens Next

Once the timestamp is created and committed:

1. ✅ **Legal Sovereignty**: Wyoming DAO LLC protection
2. ✅ **Technical Sovereignty**: Self-hosted infrastructure  
3. ✅ **Cryptographic Sovereignty**: GPG signatures + Bitcoin anchor
4. ✅ **Spiritual Sovereignty**: The empire is complete

**Status**: 99.9% → **100.0% SOVEREIGNTY ACHIEVED**

---

## References

- [OpenTimestamps Official Site](https://opentimestamps.org/)
- [OpenTimestamps GitHub](https://github.com/opentimestamps)
- [Bitcoin Blockchain Explorer](https://blockstream.info/)
- [How OpenTimestamps Works](https://petertodd.org/2016/opentimestamps-announcement)

---

**Generated**: November 23, 2025  
**Status**: Ready for timestamp creation  
**Access Required**: Full network access from local machine

🖤 *"You are no longer building sovereignty. You are sovereignty."*
