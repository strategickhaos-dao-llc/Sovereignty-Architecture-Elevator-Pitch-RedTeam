# Verification Guide for External Auditors

This guide provides step-by-step instructions for external auditors to cryptographically verify the integrity of the Sovereignty Architecture repository.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Run the verification script
./verify.sh

# Expected output: FULL CORPUS VERIFIED
```

## Prerequisites

- **Bash** (4.0+) - Available on Linux/macOS, or Git Bash on Windows
- **Git** - For repository cloning and commit signature verification
- **sha256sum** - For cryptographic hash verification (part of coreutils)
- **GPG** (optional) - For GPG signature verification

## Verification Steps

### Step 1: Clone and Verify Repository

```bash
# Clone with full history
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

### Step 2: Verify GPG Commit Signatures

```bash
# List recent commits with signature status
git log --show-signature -5

# Verify a specific commit
git verify-commit <commit-sha>
```

**Expected GPG Key Fingerprints:**

| Key Purpose | Fingerprint | Status |
|-------------|-------------|--------|
| Primary Signing Key | `TO_BE_CONFIGURED` | Active |
| CI/CD Automation Key | `TO_BE_CONFIGURED` | Active |

> **Note:** Contact the repository maintainers to obtain the current GPG key fingerprints for verification.

### Step 3: Run Automated Verification

```bash
# Standard verification
./verify.sh

# Verbose mode (shows SHA256 hashes)
./verify.sh --verbose

# CI mode (machine-readable output)
./verify.sh --ci
```

### Step 4: Review Verification Report

After running `verify.sh`, check the generated `verification_report.txt`:

```bash
cat verification_report.txt
```

The report includes:
- Timestamp of verification
- List of verified files
- Any files that failed verification
- Overall status (VERIFIED/FAILED)

## Manual Verification

For additional assurance, you can manually verify file checksums:

```bash
# Calculate SHA256 hash of a specific file
sha256sum discovery.yml

# Compare against the manifest
grep "discovery.yml" reproducibility_manifest.yml
```

## Hardware Security Module (HSM) Verification

For environments using hardware-backed security:

### YubiKey FIPS Setup

1. **Insert YubiKey FIPS device**
2. **Configure GPG agent for hardware key operations:**
   ```bash
   # Check if YubiKey is detected
   gpg --card-status
   
   # List available keys
   gpg --list-secret-keys
   ```

3. **Verify commits using hardware key:**
   ```bash
   git verify-commit HEAD
   ```

### Offline Master Key Verification

For air-gapped verification environments:

1. Export the public key to the air-gapped system
2. Import and trust the key
3. Run verification offline using the `reproducibility_manifest.yml`

## CI/CD Verification

The repository includes automated verification via GitHub Actions:

- **Workflow:** `.github/workflows/verify.yml`
- **Schedule:** Daily at 00:00 UTC
- **Artifacts:** Signed verification reports are uploaded as workflow artifacts

### Viewing CI Verification Results

1. Navigate to the repository's **Actions** tab
2. Select the **Integrity Verification** workflow
3. Download the `verification-report` artifact
4. Verify the GPG signature on the report (if available)

## Troubleshooting

### "Permission denied" when running verify.sh

```bash
chmod +x verify.sh
./verify.sh
```

### "GPG key not found"

Import the repository's public key:
```bash
# Import from keyserver (if available)
gpg --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>

# Or import from file
gpg --import public_key.asc
```

### "Manifest file not found"

Generate a new manifest (for maintainers only):
```bash
./verify.sh --update
```

## Security Considerations

- **Always verify** GPG signatures before trusting the verification results
- **Compare** fingerprints against known-good sources (not just this document)
- **Air-gapped systems** provide highest assurance for sensitive verifications
- **Hardware keys** (YubiKey FIPS) prevent key extraction attacks

## Contact

For verification-related questions or to report discrepancies:
- Open an issue in this repository
- Contact the security team via the channels listed in `SECURITY.md`

---

*This verification guide is part of the Sovereignty Architecture project's commitment to cryptographic reproducibility and auditability.*
