# Swarmgate Archive Verification Guide

This guide explains how to independently verify the authenticity and integrity of Strategickhaos Sovereignty Architecture releases.

## Quick Verification

### POSIX (Linux/macOS/Unix)

**One-liner:**
```bash
curl -sL https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/scripts/verify/verify.sh | bash
```

**Or download and run:**
```bash
# Download verification script
curl -O https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/scripts/verify/verify.sh
chmod +x verify.sh

# Download archive and provenance
curl -O https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases/latest/download/swarmgate_v1.0.tar.gz
curl -O https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases/latest/download/provenance.json

# Run verification
./verify.sh --archive swarmgate_v1.0.tar.gz --provenance provenance.json
```

### Windows (PowerShell)

**One-liner:**
```powershell
irm https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/scripts/verify/verify.ps1 | iex
```

**Or download and run:**
```powershell
# Download verification script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/scripts/verify/verify.ps1" -OutFile "verify.ps1"

# Download archive and provenance
Invoke-WebRequest -Uri "https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases/latest/download/swarmgate_v1.0.tar.gz" -OutFile "swarmgate_v1.0.tar.gz"
Invoke-WebRequest -Uri "https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases/latest/download/provenance.json" -OutFile "provenance.json"

# Run verification
.\verify.ps1 -Archive swarmgate_v1.0.tar.gz -Provenance provenance.json
```

## Manual Verification Steps

### 1. Verify BLAKE3 Hash

The BLAKE3 hash is the primary cryptographic verification method.

**Install b3sum:**
```bash
# Ubuntu/Debian
sudo apt-get install b3sum

# macOS
brew install b3sum

# Windows
winget install BLAKE3team.b3sum
```

**Compute and compare:**
```bash
# Compute hash
b3sum swarmgate_v1.0.tar.gz

# Compare with canonical hash in provenance.json
cat provenance.json | jq -r '.subject[0].digest.blake3'
```

### 2. Verify GPG Signature

**Import signing key:**
```bash
# Import the Strategickhaos signing key
gpg --keyserver keyserver.ubuntu.com --recv-keys 0x137SOVEREIGN

# Or import from the repository
curl -sL https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/KEYS | gpg --import
```

**Verify signature:**
```bash
gpg --verify swarmgate_v1.0.tar.gz.sig swarmgate_v1.0.tar.gz
```

**Expected output:**
```
gpg: Signature made <date> using RSA key ID 137SOVEREIGN
gpg: Good signature from "Strategickhaos DAO <security@strategickhaos.com>"
```

### 3. Verify SHA256 (Alternative)

For systems without b3sum:
```bash
sha256sum swarmgate_v1.0.tar.gz

# Compare with provenance
cat provenance.json | jq -r '.subject[0].digest.sha256'
```

### 4. Fetch from IPFS

IPFS provides content-addressed retrieval, ensuring you get exactly what was published:

```bash
# Using local IPFS node
ipfs get <CID> -o swarmgate_v1.0.tar.gz

# Using IPFS gateways
curl -O https://ipfs.io/ipfs/<CID>
curl -O https://dweb.link/ipfs/<CID>
curl -O https://cloudflare-ipfs.com/ipfs/<CID>
```

### 5. Fetch from Arweave

Arweave provides permanent storage:

```bash
curl -O https://arweave.net/<TXID>
```

## Deterministic Build Verification

For maximum assurance, you can recreate the archive from source:

```bash
# Clone repository at the tagged version
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
git checkout v1.0.0

# Create deterministic archive
export SOURCE_DATE_EPOCH=1732665600  # 2025-11-27T00:00:00Z
tar --sort=name \
    --mtime="@${SOURCE_DATE_EPOCH}" \
    --owner=root:0 \
    --group=root:0 \
    --numeric-owner \
    -czf rebuilt.tar.gz \
    swarmgate.yaml \
    discovery.yml \
    dao_record_v1.0.yaml \
    ai_constitution.yaml \
    LICENSE \
    README.md \
    SECURITY.md \
    COMMUNITY.md \
    CONTRIBUTORS.md \
    bootstrap \
    governance \
    .github/workflows \
    scripts \
    provenance

# Compare hashes
b3sum swarmgate_v1.0.tar.gz rebuilt.tar.gz
```

**Note:** Exact hash match requires identical build environment (same tar version, gzip settings, etc.). The important thing is that the content matches.

## Trust Model

### What This Verification Proves

1. **Integrity**: The archive has not been modified since signing
2. **Authenticity**: The archive was signed by the Strategickhaos private key
3. **Provenance**: The build process and inputs are documented
4. **Availability**: The archive is pinned across multiple independent storage networks

### What This Does NOT Prove

1. **Source code audit**: Verification does not audit the actual code for security
2. **Key custody**: You must trust that the signing key is properly secured
3. **Runtime safety**: Verification does not guarantee the code is safe to execute

### Key Trust

The GPG key `0x137SOVEREIGN` is:
- Published in this repository (`KEYS` file)
- Cross-referenced on key servers
- Used consistently for all releases

If you suspect key compromise, verify through multiple independent channels.

## Checksums Reference

Find canonical checksums in:
- `provenance/provenance.json` - Machine-readable format
- `provenance/provenance.yaml` - Human-readable format
- GitHub Release notes - Published with each release

## Reporting Issues

If verification fails or you suspect tampering:

1. **Do NOT use the archive**
2. Compare checksums from multiple sources (GitHub, IPFS, Arweave)
3. Report to security@strategickhaos.com
4. Open an issue on GitHub

## Tool Installation Summary

| Tool | Ubuntu/Debian | macOS | Windows |
|------|---------------|-------|---------|
| b3sum | `apt install b3sum` | `brew install b3sum` | `winget install BLAKE3team.b3sum` |
| gpg | `apt install gnupg` | `brew install gnupg` | `winget install GnuPG.GnuPG` |
| jq | `apt install jq` | `brew install jq` | `winget install jqlang.jq` |
| ipfs | [docs.ipfs.tech](https://docs.ipfs.tech/install/) | `brew install ipfs` | [docs.ipfs.tech](https://docs.ipfs.tech/install/) |

---

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*
