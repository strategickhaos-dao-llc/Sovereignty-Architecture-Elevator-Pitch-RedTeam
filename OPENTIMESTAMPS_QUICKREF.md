# OpenTimestamps Quick Reference Card

Quick lookup for common OpenTimestamps operations.

## Installation

```bash
pip install opentimestamps-client
```

## Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ots stamp <file>` | Create timestamp | `ots stamp manifest.md` |
| `ots upgrade <file.ots>` | Get Bitcoin confirmation | `ots upgrade manifest.md.ots` |
| `ots verify <file.ots>` | Verify timestamp | `ots verify manifest.md.ots` |
| `ots info <file.ots>` | Show details | `ots info manifest.md.ots` |

## Automation Scripts

### Linux/Mac
```bash
# Timestamp all sovereign docs
./timestamp_sovereign_docs.sh stamp

# Upgrade pending timestamps
./timestamp_sovereign_docs.sh upgrade

# Verify all timestamps
./timestamp_sovereign_docs.sh verify

# Generate report
./timestamp_sovereign_docs.sh report

# Interactive complete workflow
./timestamp_sovereign_docs.sh all
```

### Windows PowerShell
```powershell
# Same commands, PowerShell syntax
.\timestamp_sovereign_docs.ps1 -Action stamp
.\timestamp_sovereign_docs.ps1 -Action upgrade
.\timestamp_sovereign_docs.ps1 -Action verify
.\timestamp_sovereign_docs.ps1 -Action report
.\timestamp_sovereign_docs.ps1 -Action all
```

## Typical Workflow

```bash
# 1. Finalize document
vim SOVEREIGN_MANIFEST_v1.0.md

# 2. Commit to git
git add SOVEREIGN_MANIFEST_v1.0.md
git commit -m "Finalize manifest v1.0"

# 3. Create timestamp
ots stamp SOVEREIGN_MANIFEST_v1.0.md

# 4. Commit .ots file
git add SOVEREIGN_MANIFEST_v1.0.md.ots
git commit -m "Add timestamp proof"
git push

# 5. Wait 1-2 hours...

# 6. Upgrade timestamp
ots upgrade SOVEREIGN_MANIFEST_v1.0.md.ots

# 7. Commit upgraded proof
git add SOVEREIGN_MANIFEST_v1.0.md.ots
git commit -m "Upgrade timestamp with Bitcoin confirmation"
git push

# 8. Verify
ots verify SOVEREIGN_MANIFEST_v1.0.md.ots
```

## Common Options

```bash
# Verbose output
ots verify --verbose file.ots

# Specify calendar server
ots stamp --calendar https://alice.btc.calendar.opentimestamps.org file.md

# Timestamp from stdin
echo "data" | ots stamp -

# Batch operations
ots stamp *.md
ots upgrade *.ots
```

## Verification States

| Output | Meaning | Action |
|--------|---------|--------|
| `Success! Bitcoin block...` | ✅ Fully verified | None - proof complete |
| `Pending confirmation...` | ⏳ Waiting for Bitcoin | Run `ots upgrade` after 1-2 hours |
| `Bad file hash` | ❌ File modified | File doesn't match timestamp |
| `Calendar unreachable` | ⚠️ Network issue | Try again later |

## File Hash Check

```bash
# Linux/Mac
sha256sum SOVEREIGN_MANIFEST_v1.0.md

# Windows PowerShell
Get-FileHash SOVEREIGN_MANIFEST_v1.0.md -Algorithm SHA256

# Expected output
b027929c3a591a8dd2296e272b602caa1d2d96cd61a1380f4e948fc0cdf494bf
```

## Important Files

| File | Description |
|------|-------------|
| `SOVEREIGN_MANIFEST_v1.0.md` | Original document |
| `SOVEREIGN_MANIFEST_v1.0.md.ots` | Timestamp proof |
| Both must be kept together for verification |

## Calendar Servers

Public servers (built into `ots` client):
- `https://alice.btc.calendar.opentimestamps.org`
- `https://bob.btc.calendar.opentimestamps.org`
- `https://finney.calendar.opentimestamps.org`

## Timing

| Stage | Duration | What Happens |
|-------|----------|--------------|
| Create timestamp | Instant | `.ots` file created with pending status |
| Calendar batching | ~1 hour | Multiple timestamps aggregated |
| Bitcoin confirmation | ~10 min | Transaction included in block |
| Total wait time | 1-2 hours | Before `ots upgrade` succeeds |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ots: command not found` | `pip install opentimestamps-client` |
| Stuck at "Pending" | Wait longer, then `ots upgrade` |
| "Calendar unreachable" | Check internet, try different server |
| "Bad file hash" | File was modified after timestamping |
| Verification fails | Ensure both `.md` and `.ots` files present |

## Git Integration

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
ots stamp SOVEREIGN_MANIFEST_v1.0.md
git add SOVEREIGN_MANIFEST_v1.0.md.ots
```

### Post-commit Hook
```bash
#!/bin/bash
# .git/hooks/post-commit
# Schedule upgrade for later
echo "ots upgrade *.ots" | at now + 2 hours
```

## Cron Jobs

```bash
# Upgrade timestamps every hour
0 * * * * cd /path/to/repo && ots upgrade *.ots

# Weekly verification
0 0 * * 0 cd /path/to/repo && ots verify *.ots | mail -s "Timestamp Report" you@example.com
```

## Documentation

- **Full Guide:** [OPENTIMESTAMPS_GUIDE.md](./OPENTIMESTAMPS_GUIDE.md)
- **Quick Start:** [SOVEREIGN_TIMESTAMPING_README.md](./SOVEREIGN_TIMESTAMPING_README.md)
- **Example Workflow:** [TIMESTAMPING_EXAMPLE.md](./TIMESTAMPING_EXAMPLE.md)
- **Official Site:** https://opentimestamps.org

## Key Concepts

| Term | Meaning |
|------|---------|
| **Hash** | SHA256 fingerprint of document |
| **Calendar Server** | Aggregates timestamps and submits to Bitcoin |
| **Merkle Tree** | Efficient way to batch many timestamps together |
| **OP_RETURN** | Bitcoin transaction field storing Merkle root |
| **Block Height** | Bitcoin block number containing timestamp |
| **.ots File** | Proof file linking hash to Bitcoin block |

## Security Properties

✅ **Tamper-Evident** - Any change breaks verification  
✅ **Decentralized** - No central authority  
✅ **Private** - Only hash submitted, not content  
✅ **Permanent** - Bitcoin blockchain is immutable  
✅ **Verifiable** - Anyone can independently verify  
✅ **Free** - No cost to users  

## One-Liner Commands

```bash
# Timestamp and commit
ots stamp file.md && git add file.md.ots && git commit -m "Add timestamp"

# Upgrade all timestamps
find . -name "*.ots" -exec ots upgrade {} \;

# Verify all timestamps
find . -name "*.ots" -exec ots verify {} \;

# Generate report
for f in *.ots; do echo "=== $f ==="; ots verify "$f"; done > report.txt
```

## Python Integration

```python
import subprocess

# Timestamp a file
subprocess.run(['ots', 'stamp', 'manifest.md'])

# Verify
result = subprocess.run(['ots', 'verify', 'manifest.md.ots'], 
                       capture_output=True, text=True)
if 'Success' in result.stdout:
    print("✓ Verified")
```

## API Libraries

- **Python:** `opentimestamps`
- **JavaScript:** `javascript-opentimestamps`
- **Java:** `java-opentimestamps`
- **Go:** `go-opentimestamps`

## Resources

- 📖 [OpenTimestamps.org](https://opentimestamps.org)
- 💻 [GitHub](https://github.com/opentimestamps/opentimestamps-client)
- 🔍 [Bitcoin Explorer](https://blockstream.info)
- 💬 [Forum](https://groups.google.com/forum/#!forum/opentimestamps)

---

**Print this card and keep it handy!** 📋
