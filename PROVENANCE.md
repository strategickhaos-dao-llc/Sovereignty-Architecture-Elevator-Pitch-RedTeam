# Provenance Documentation

This document tracks the cryptographic verification and provenance of artifacts in this repository.

## Hash Verification

Artifacts are verified using BLAKE3 hashes for integrity and authenticity.

### Verification Process

1. Download the official `b3sum` executable for your platform
2. Compute the hash of the artifact
3. Compare with the recorded hash below

### How to Verify

**Windows (PowerShell):**
```powershell
# Download b3sum executable
$b3Url = "https://github.com/BLAKE3-team/BLAKE3/releases/latest/download/b3sum_windows_x64_bin.exe"
Invoke-WebRequest -Uri $b3Url -OutFile "b3sum.exe"

# Verify artifact
.\b3sum.exe <artifact-file>
```

**Linux/macOS:**
```bash
# Install b3sum (Rust required)
cargo install b3sum

# Or download pre-built binary from releases
# https://github.com/BLAKE3-team/BLAKE3/releases

# Verify artifact
b3sum <artifact-file>
```

## Recorded Hashes

<!-- Verified hashes will be appended below this line -->
