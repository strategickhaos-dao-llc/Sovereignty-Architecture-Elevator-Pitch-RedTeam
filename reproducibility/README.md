# SACSE Reproducibility Manifest

## Overview

This document describes the reproducibility framework for the Sovereignty Architecture Cognitive Systems Engineering (SACSE) methodology. It enables third-party verification of artifacts, experiments, and system state through cryptographic proofs and automated verification scripts.

---

## 1. Artifact Verification

### Hash Manifest Structure

All SACSE artifacts are tracked in `reproducibility/artifact_hashes.sha256`. This file contains SHA256 checksums for:

- Configuration files (YAML, JSON)
- Source code files (TypeScript, Python)
- Documentation (Markdown)
- AI/ML model files (when applicable)
- Legal/compliance artifacts

### Verification Process

```bash
# Clone repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Run automated verification
./reproducibility/verify.sh

# Or manually verify specific files
sha256sum -c reproducibility/artifact_hashes.sha256
```

### Expected Output
```
discovery.yml: OK
dao_record.yaml: OK
governance/access_matrix.yaml: OK
[... additional files ...]
All artifacts verified successfully.
```

---

## 2. Commit Signing Verification

All commits to protected branches must be GPG-signed. Verify the signing chain:

```bash
# Verify latest commit signature
git verify-commit HEAD

# Verify entire branch history
git log --show-signature --oneline main

# Check signer identity
gpg --recv-keys <KEY_ID>
gpg --verify-commit HEAD
```

### Trusted Signers
See `governance/article_7_authorized_signers.md` for the list of authorized GPG key fingerprints.

---

## 3. Container Image Verification

### Docker Content Trust

```bash
# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Pull verified images only
docker pull ghcr.io/strategickhaos/sovereignty-architecture:latest

# Verify image digest
docker images --digests | grep sovereignty-architecture
```

### Image Checksums
```yaml
container_images:
  discord-bot:
    registry: ghcr.io/strategickhaos/discord-ops-bot
    tag: v1.0.0
    digest: sha256:placeholder_digest_to_be_updated
    
  event-gateway:
    registry: ghcr.io/strategickhaos/event-gateway
    tag: v1.0.0
    digest: sha256:placeholder_digest_to_be_updated
    
  refinory-api:
    registry: ghcr.io/strategickhaos/refinory-api
    tag: v1.0.0
    digest: sha256:placeholder_digest_to_be_updated
```

---

## 4. Dependency Verification

### Node.js Dependencies
```bash
# Verify package-lock.json integrity
npm ci --ignore-scripts

# Audit for vulnerabilities
npm audit --audit-level=high

# Generate SBOM
npm sbom --sbom-format=spdx
```

### Python Dependencies
```bash
# Verify requirements with hashes
pip install --require-hashes -r requirements.txt

# Audit for vulnerabilities
pip-audit -r requirements.txt
```

---

## 5. RAG Corpus Verification

### Vector Store Integrity

```bash
# Verify corpus artifact hashes before ingestion
sha256sum -c reproducibility/corpus_hashes.sha256

# Check vector count matches expected
curl -s http://qdrant:6333/collections/runbooks | \
  jq -r '.result.vectors_count'

# Compare with manifest
grep "vectors_count" reproducibility/reproducibility.yaml
```

### Embedding Model Verification
```bash
# Verify embedding model checksum
sha256sum models/embedding-model.gguf | \
  diff - reproducibility/model_checksums.sha256
```

---

## 6. Public Archives

### Artifact Archives

| Archive | URL | Purpose |
|---------|-----|---------|
| GitHub Release | `https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases` | Tagged releases with artifacts |
| Zenodo DOI | `[TBD upon publication]` | Academic citation and archival |
| IPFS CID | `[TBD upon deployment]` | Immutable distributed storage |

### Archive Contents
- Source code snapshot
- Configuration files
- Documentation
- Hash manifests
- GPG signatures

---

## 7. Experiment Reproducibility

### Running Benchmarks
```bash
# Execute full benchmark suite
python scripts/run_benchmarks.py --config benchmarks_config.yaml

# Output comparison
diff benchmarks/reports/expected_results.json \
     benchmarks/reports/actual_results.json
```

### Expected Results Reference
See `benchmarks/reports/baseline_results.json` for expected benchmark outputs with acceptable variance thresholds.

---

## 8. Verification Script Usage

```bash
# Full verification (recommended)
./reproducibility/verify.sh --full

# Quick verification (hashes only)
./reproducibility/verify.sh --quick

# Verbose output
./reproducibility/verify.sh --verbose

# Generate new manifest (maintainer only)
./reproducibility/verify.sh --generate
```

### Exit Codes
- `0`: All verifications passed
- `1`: Hash verification failed
- `2`: Signature verification failed
- `3`: Dependency verification failed
- `4`: Configuration error

---

## 9. Continuous Verification

### CI/CD Integration

The verification script runs automatically on:
- Every pull request
- Every push to `main` branch
- Weekly scheduled verification

### Verification Badge
[![Reproducibility](https://img.shields.io/badge/reproducibility-verified-brightgreen)](./reproducibility/verify.sh)

---

## 10. Reporting Issues

If verification fails:

1. Check network connectivity (for signature key retrieval)
2. Ensure Git LFS files are pulled (`git lfs pull`)
3. Verify you have the correct branch/tag
4. Report issues to: `security@strategickhaos.com`

Include in your report:
- Verification script output
- Git commit SHA
- Operating system and version
- Tool versions (`gpg --version`, `sha256sum --version`)

---

*Last updated: 2025-11-25*
*Version: 1.0*
*Maintainer: SACSE Reproducibility Working Group*
