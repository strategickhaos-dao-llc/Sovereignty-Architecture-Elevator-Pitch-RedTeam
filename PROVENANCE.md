# Provenance and Integrity Verification

This document describes how to verify the integrity and provenance of artifacts in this repository using BLAKE3 cryptographic hashing.

## Overview

We use [BLAKE3](https://github.com/BLAKE3-team/BLAKE3) for cryptographic hashing of release artifacts. BLAKE3 is a fast, secure cryptographic hash function that provides:
- High performance across all platforms
- Security against length extension attacks
- 256-bit output (64 hex characters)

## Installing BLAKE3

### Linux (Recommended: via Cargo)

```bash
# Install Rust's cargo package manager if not already installed
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install b3sum (BLAKE3 command-line utility)
cargo install b3sum

# Verify installation
b3sum --version
```

### Linux (Alternative: Pre-built Binary)

```bash
# Download latest release
curl -LO https://github.com/BLAKE3-team/BLAKE3/releases/latest/download/b3sum_linux_x64_bin
chmod +x b3sum_linux_x64_bin
sudo mv b3sum_linux_x64_bin /usr/local/bin/b3sum
```

### Windows (via Scoop)

```powershell
scoop install blake3
blake3.exe <filename>
```

### Windows (Portable)

```powershell
Invoke-WebRequest -Uri https://github.com/BLAKE3-team/BLAKE3/releases/latest/download/blake3-win64.zip -OutFile blake3-win64.zip
Expand-Archive blake3-win64.zip -DestinationPath .\blake3
.\blake3\blake3.exe <filename>
```

### macOS (via Homebrew)

```bash
brew install b3sum
```

## Artifact Hashes

### swarmgate_v1.0.tar.gz

| Field | Value |
|-------|-------|
| Filename | `swarmgate_v1.0.tar.gz` |
| BLAKE3 Hash | `caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698` |
| Algorithm | BLAKE3 (256-bit) |

## Verifying Artifacts

### Using b3sum (Linux/macOS)

```bash
# Compute hash
b3sum swarmgate_v1.0.tar.gz

# Expected output:
# caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698  swarmgate_v1.0.tar.gz

# Verify against expected hash
echo "caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698  swarmgate_v1.0.tar.gz" | b3sum -c
```

### Using blake3.exe (Windows)

```powershell
blake3.exe swarmgate_v1.0.tar.gz
# Compare output to: caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698
```

## Creating Archives with Reproducible Hashes

To create a reproducible archive:

```bash
# Set consistent timestamp for reproducibility
export SOURCE_DATE_EPOCH=1700000000

# Create tarball with deterministic settings
tar --sort=name \
    --mtime="@${SOURCE_DATE_EPOCH}" \
    --owner=0 --group=0 --numeric-owner \
    -czf swarmgate_v1.0.tar.gz \
    src/event-gateway.js \
    src/event-gateway.ts \
    src/config.js \
    src/config.ts \
    Dockerfile.gateway \
    discovery.yml

# Compute and record hash
b3sum swarmgate_v1.0.tar.gz >> BLAKE3SUMS
```

## Verification Script

A helper script `scripts/verify_blake3.sh` is provided:

```bash
./scripts/verify_blake3.sh swarmgate_v1.0.tar.gz caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698
```

## Security Considerations

- Always verify hashes before deploying artifacts
- Use HTTPS when downloading artifacts
- Compare hashes from multiple trusted sources when possible
- Store hash values in version control for auditability

## References

- [BLAKE3 Official Repository](https://github.com/BLAKE3-team/BLAKE3)
- [BLAKE3 Paper](https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf)
- [b3sum Documentation](https://github.com/BLAKE3-team/BLAKE3/tree/master/b3sum)
