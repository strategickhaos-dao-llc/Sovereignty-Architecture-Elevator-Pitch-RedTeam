# Sovereign Document Timestamping

This directory contains the **Sovereign Manifest** and associated tooling for anchoring documents to the Bitcoin blockchain using OpenTimestamps.

## Quick Start

### Prerequisites

```bash
# Install OpenTimestamps client
pip install opentimestamps-client

# Verify installation
ots --version
```

### Create Your First Timestamp

```bash
# Option 1: Use the automated script (Linux/Mac)
./timestamp_sovereign_docs.sh stamp

# Option 2: Use PowerShell script (Windows)
.\timestamp_sovereign_docs.ps1 -Action stamp

# Option 3: Manual timestamping
ots stamp SOVEREIGN_MANIFEST_v1.0.md
```

### Upgrade & Verify (after 1-2 hours)

```bash
# Upgrade timestamps to include Bitcoin confirmation
./timestamp_sovereign_docs.sh upgrade

# Verify all timestamps
./timestamp_sovereign_docs.sh verify

# Generate verification report
./timestamp_sovereign_docs.sh report
```

## Files in This Repository

### Core Documents

- **`SOVEREIGN_MANIFEST_v1.0.md`** - The primary sovereignty declaration
  - Defines operational, cognitive, cryptographic, and architectural sovereignty
  - Establishes governance model and decision authority
  - Documents integration requirements and legal framework
  
- **`OPENTIMESTAMPS_GUIDE.md`** - Complete guide to OpenTimestamps
  - Installation instructions for all platforms
  - Detailed usage examples
  - Troubleshooting and best practices
  - Advanced workflows and automation

### Automation Scripts

- **`timestamp_sovereign_docs.sh`** - Linux/Mac automation script
  - Commands: `stamp`, `upgrade`, `verify`, `info`, `report`, `all`
  - Interactive workflow with color-coded output
  - Batch processing of multiple documents
  
- **`timestamp_sovereign_docs.ps1`** - Windows PowerShell script
  - Same functionality as bash script
  - Native Windows integration
  - Color-coded output in PowerShell

### Timestamp Proofs (generated)

- **`*.ots`** - OpenTimestamps proof files
  - Created when running `ots stamp`
  - Contains Merkle tree proof linking document to Bitcoin
  - Small binary files (typically < 1KB)
  - Must be kept with original documents for verification

## Why Timestamp Sovereign Documents?

### Cryptographic Proof of Existence

OpenTimestamps provides **tamper-evident proof** that a document existed at a specific point in time by anchoring it to the Bitcoin blockchain. This is important for:

1. **Legal Protection** - Prove when intellectual property was created
2. **Audit Trail** - Create immutable record of decision points
3. **Trust Minimization** - Don't rely on central authorities
4. **Historical Record** - Document evolution of the project over time

### How It Works

```
Document → SHA256 Hash → Calendar Server → Bitcoin Transaction → Blockchain
   ↓           ↓              ↓                    ↓                  ↓
  You    Proof Only    Aggregation       Merkle Root          Permanent
         Submitted      with Others       in OP_RETURN         Record
```

### Security Properties

- **Tamper-Evident** - Any change to document invalidates proof
- **Decentralized** - No single point of failure
- **Private** - Only hash submitted, not document contents
- **Permanent** - Bitcoin blockchain is immutable
- **Verifiable** - Anyone can independently verify

## Workflow Examples

### Daily Development Workflow

```bash
# 1. Make changes to sovereign documents
vim SOVEREIGN_MANIFEST_v1.0.md

# 2. Commit changes
git add SOVEREIGN_MANIFEST_v1.0.md
git commit -m "Update sovereignty principles"

# 3. Timestamp the finalized document
ots stamp SOVEREIGN_MANIFEST_v1.0.md

# 4. Commit the timestamp proof
git add SOVEREIGN_MANIFEST_v1.0.md.ots
git commit -m "Add timestamp proof for manifest update"
git push

# 5. Later (after 1-2 hours), upgrade the timestamp
ots upgrade SOVEREIGN_MANIFEST_v1.0.md.ots

# 6. Commit upgraded proof
git add SOVEREIGN_MANIFEST_v1.0.md.ots
git commit -m "Upgrade timestamp with Bitcoin confirmation"
git push
```

### Pre-Release Checklist

Before releasing a new version:

```bash
# 1. Finalize all documentation
# 2. Run verification on existing timestamps
./timestamp_sovereign_docs.sh verify

# 3. Timestamp all release documents
./timestamp_sovereign_docs.sh stamp

# 4. Create release tag
git tag -s v1.0.0 -m "Release v1.0.0 with timestamped manifest"

# 5. Push everything
git push --tags

# 6. Wait for Bitcoin confirmation (~1-2 hours)
# 7. Upgrade timestamps
./timestamp_sovereign_docs.sh upgrade

# 8. Generate verification report
./timestamp_sovereign_docs.sh report

# 9. Include report in release notes
```

### Legal/Audit Preparation

When preparing for legal review or audit:

```bash
# 1. Verify all timestamps
./timestamp_sovereign_docs.sh verify

# 2. Generate comprehensive report
./timestamp_sovereign_docs.sh report

# 3. Export repository state
git archive --format=tar.gz --prefix=sovereignty-$(date +%Y%m%d)/ HEAD > sovereignty-archive.tar.gz

# 4. Include timestamp proofs in archive
tar -czf sovereignty-complete-$(date +%Y%m%d).tar.gz *.ots sovereignty-archive.tar.gz

# 5. Verify archive integrity
sha256sum sovereignty-complete-*.tar.gz > checksums.txt

# 6. Timestamp the checksums
ots stamp checksums.txt
```

## Integration with Git

### Git Hooks for Automatic Timestamping

Create `.git/hooks/post-commit`:

```bash
#!/bin/bash
# Automatically timestamp sovereign documents after commit

DOCS=(
    "SOVEREIGN_MANIFEST_v1.0.md"
    "dao_record_v1.0.yaml"
)

for doc in "${DOCS[@]}"; do
    if git diff-tree --no-commit-id --name-only -r HEAD | grep -q "^${doc}$"; then
        echo "Timestamping: $doc"
        ots stamp "$doc"
        git add "${doc}.ots"
        git commit --amend --no-edit --no-verify
    fi
done
```

Make executable:
```bash
chmod +x .git/hooks/post-commit
```

### GitHub Actions Workflow

See `OPENTIMESTAMPS_GUIDE.md` for complete GitHub Actions integration examples.

## Verification for Third Parties

If someone wants to verify your timestamps:

```bash
# 1. Clone repository
git clone https://github.com/YourOrg/YourRepo.git
cd YourRepo

# 2. Install OpenTimestamps
pip install opentimestamps-client

# 3. Verify all timestamps
ots verify SOVEREIGN_MANIFEST_v1.0.md.ots

# 4. Check file hasn't been modified
sha256sum SOVEREIGN_MANIFEST_v1.0.md
# Compare with hash in Bitcoin transaction
```

## Frequently Asked Questions

### Do I need to install Bitcoin to use OpenTimestamps?

**No.** OpenTimestamps client connects to public calendar servers that handle Bitcoin transactions. You only need the `ots` command-line tool.

### How much does timestamping cost?

**Free.** Calendar servers aggregate many timestamps and pay the Bitcoin transaction fees. There's no cost to users.

### How long does it take?

- **Creating timestamp**: Instant (creates `.ots` file immediately)
- **Bitcoin confirmation**: 1-2 hours (calendar servers batch submissions)
- **Full verification**: Available after Bitcoin block is mined

### Can I timestamp private documents?

**Yes.** OpenTimestamps only submits the SHA256 hash of your document, not the document itself. The actual content remains private.

### What if the calendar servers go down?

Timestamps remain valid forever. The `.ots` file contains all information needed to verify against Bitcoin blockchain. You don't need the original calendar servers.

### Can timestamps be faked or backdated?

**No.** The Bitcoin blockchain provides cryptographic proof of when the timestamp was created. You cannot create a timestamp for a past date.

### What about large files?

OpenTimestamps works with any file size. Only the hash (32 bytes) is submitted, regardless of original file size.

## Resources

### Documentation

- [Full OpenTimestamps Guide](./OPENTIMESTAMPS_GUIDE.md) - Complete reference
- [Sovereign Manifest](./SOVEREIGN_MANIFEST_v1.0.md) - Sovereignty declaration
- [OpenTimestamps.org](https://opentimestamps.org) - Official documentation

### Tools

- [OpenTimestamps Client](https://github.com/opentimestamps/opentimestamps-client) - Command-line tool
- [Bitcoin Block Explorer](https://blockstream.info) - Verify transactions
- [Calendar Servers](https://opentimestamps.org) - Public timestamping servers

### Community

- [OpenTimestamps Forum](https://groups.google.com/forum/#!forum/opentimestamps)
- [GitHub Issues](https://github.com/opentimestamps/opentimestamps-client/issues)

## Troubleshooting

### "ots: command not found"

```bash
# Install OpenTimestamps client
pip install opentimestamps-client

# Or on Windows:
pip install opentimestamps-client
# Ensure Python Scripts directory is in PATH
```

### "Calendar server unreachable"

```bash
# Try again later - servers may be temporarily down
# Or specify different server:
ots stamp --calendar https://alice.btc.calendar.opentimestamps.org file.md
```

### "Pending" status persists

```bash
# Wait at least 1-2 hours after stamping
# Then upgrade:
ots upgrade file.md.ots

# Check again in 30 minutes if still pending
```

### Verification fails

```bash
# Ensure file hasn't been modified
sha256sum SOVEREIGN_MANIFEST_v1.0.md

# Check .ots file integrity
ots info SOVEREIGN_MANIFEST_v1.0.md.ots

# Try verbose verification
ots verify --verbose SOVEREIGN_MANIFEST_v1.0.md.ots
```

## Contributing

When contributing to sovereign documents:

1. **Discuss changes first** - Open an issue to discuss proposed changes
2. **Create feature branch** - Work in separate branch
3. **Timestamp final version** - Only timestamp after final review
4. **Include .ots files** - Always commit timestamp proofs with documents
5. **Document changes** - Update version history in manifest

## License

- **Sovereign Manifest**: Legal declaration (not licensed software)
- **Documentation**: CC-BY-4.0
- **Scripts**: MIT License
- **Timestamp Proofs**: Public domain (cryptographic proofs)

---

## Support

For questions or issues:

1. Check [OPENTIMESTAMPS_GUIDE.md](./OPENTIMESTAMPS_GUIDE.md)
2. Review [OpenTimestamps FAQ](https://opentimestamps.org)
3. Open GitHub issue in this repository
4. Contact: [Your Contact Info]

---

**Remember:** Timestamp only finalized documents. Every timestamp creates an immutable record on the Bitcoin blockchain that cannot be undone.
