# 🔐 Sovereignty Stack Validation Module v1.0

**A portable, self-verifying sovereign compute environment that performs hash-proven integrity checks on critical stack files and validates execution readiness across a full cloud-to-local pipeline.**

---

## 🌟 Overview

The Sovereignty Stack Validation Module is a comprehensive self-verification system for sovereign computing infrastructure. It provides:

- **File Integrity Checks** - Verify existence, content, and byte count of critical files
- **Syntax Validation** - Pre-flight validation of shell and Python scripts
- **Environment Verification** - Platform-level tool and dependency checks
- **Network Diagnostics** - Connectivity testing with graceful offline mode
- **Tamper Detection** - SHA-256 hash verification for supply-chain security
- **Configuration Audit** - Policy and governance file validation

This is what DevOps engineers, cybersecurity architects, and site reliability engineers call a **self-validating sovereign software stack**.

---

## 🚀 Quick Start

```bash
# Run full verification
./verify_sovereignty.sh

# Quick health check
./verify_sovereignty.sh --quick

# Generate hash baseline (first time)
./verify_sovereignty.sh --hash

# Verify file integrity
./verify_sovereignty.sh --verify

# Check environment only
./verify_sovereignty.sh --env

# Network connectivity test
./verify_sovereignty.sh --network
```

---

## 📋 Stack Architecture

The Sovereignty Stack operates across six logical layers:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: CLOUD INTEGRATION                                   │
│ Codespaces · GitHub Actions · Kubernetes Deployment          │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: NETWORK                                             │
│ Connectivity Diagnostic · Offline Mode · External Services   │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: CONFIGURATION                                       │
│ Config Audit · Policy Enforcement · Governance Matrix        │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: INTEGRITY & SECURITY                                │
│ SHA-256 Hash Verification · Syntax Validation · SBOM         │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: PLATFORM VERIFICATION                               │
│ Git · Python · Bash · Docker · Node.js · kubectl             │
├─────────────────────────────────────────────────────────────┤
│ Layer 0: BOOT / HARDWARE                                     │
│ Portable Runtime · USB Boot · Air-Gapped Operation           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Components

### 📁 Core Files

| File | Description |
|------|-------------|
| `verify_sovereignty.sh` | Main verification script |
| `sovereignty_stack.yaml` | YAML specification for architecture |
| `sbom.yaml` | Software Bill of Materials |
| `TRUST_DECLARATION.md` | Trust and provenance documentation |
| `.sovereignty_hashes.sha256` | Hash baseline for tamper detection |
| `.sovereignty_verification.log` | Verification audit log |

### 🛠️ Verification Modules

1. **File Integrity Module**
   - Checks critical file existence
   - Validates file content (non-empty)
   - Records file byte counts

2. **Syntax Validation Module**
   - Shell scripts: `bash -n`
   - Python scripts: `python3 -m py_compile`
   - Pre-flight validation before execution

3. **Environment Module**
   - Git version check
   - Python version check
   - Bash version check
   - Docker daemon status
   - Node.js availability
   - kubectl availability

4. **Network Module**
   - Internet connectivity test
   - GitHub API reachability
   - Package registry access
   - Graceful offline mode support

5. **Hash Verification Module**
   - SHA-256 hash generation
   - Baseline comparison
   - Tamper detection alerts

6. **Configuration Audit Module**
   - discovery.yml validation
   - Docker Compose file checks
   - Kubernetes manifest audit
   - Governance file verification

---

## 🔒 Security Features

### Tamper-Evident Design

The stack generates and verifies SHA-256 hashes for all critical files:

```bash
# Generate baseline hashes
./verify_sovereignty.sh --hash

# Verify against baseline
./verify_sovereignty.sh --verify
```

If any file is modified, the system detects and reports the tampering:

```
✘ FAIL: README.md MODIFIED - potential tampering detected!
⚠️  TAMPER WARNING: File modifications detected!
   Review changes before proceeding.
```

### Supply Chain Security

The module supports:
- **SBOM (Software Bill of Materials)** - Track all dependencies
- **SLSA Compliance** - Build provenance tracking
- **Hash-based Integrity** - Cryptographic verification

---

## 📊 Output Files

### Verification Log

Located at `.sovereignty_verification.log`:

```
=== Sovereignty Stack Verification Log ===
Started: 2025-01-15 10:30:00 UTC

[2025-01-15 10:30:01] HEADER: FILE INTEGRITY VERIFICATION
[2025-01-15 10:30:01] PASS: README.md exists (8542 bytes)
[2025-01-15 10:30:01] PASS: LICENSE exists (1082 bytes)
[2025-01-15 10:30:02] PASS: validate-config.sh syntax valid
...
```

### Hash Baseline

Located at `.sovereignty_hashes.sha256`:

```
a1b2c3d4...  README.md
e5f6g7h8...  LICENSE
i9j0k1l2...  verify_sovereignty.sh
...
```

---

## 🌐 Execution Modes

### Online Mode
Full stack operation with network connectivity:
- Cloud IDE integration (Codespaces)
- Remote registry access
- Live updates and patches

### Offline Mode
Air-gapped operation for secure environments:
- Local validation only
- Cached dependencies
- No external network calls

### Portable Mode
USB boot device execution:
- Minimal footprint
- Self-contained environment
- Tamper-evident design

---

## 📝 YAML Specification

The stack architecture is formally defined in `sovereignty_stack.yaml`:

```yaml
apiVersion: sovereignty.strategickhaos.io/v1
kind: SovereigntyStack
metadata:
  name: strategickhaos-sovereignty-stack
  version: "1.0.0"
spec:
  layers:
    - name: boot-layer
      level: 0
    - name: platform-layer
      level: 1
    # ... additional layers
  validation:
    modules:
      - name: file-integrity
        required: true
      # ... additional modules
```

---

## 🔄 Integration

### GitHub Codespaces

The stack integrates seamlessly with GitHub Codespaces for cloud-based development:

```bash
# In Codespaces terminal
./verify_sovereignty.sh --full
```

### CI/CD Pipeline

Add to your GitHub Actions workflow:

```yaml
- name: Verify Sovereignty Stack
  run: |
    chmod +x verify_sovereignty.sh
    ./verify_sovereignty.sh --full
```

### Kubernetes Deployment

Verify before deploying to K8s:

```bash
./verify_sovereignty.sh --full && ./bootstrap/deploy.sh
```

---

## 🆘 Troubleshooting

### Common Issues

**Hash verification fails after intentional changes:**
```bash
# Regenerate baseline after legitimate changes
./verify_sovereignty.sh --hash
```

**Network checks fail (air-gapped environment):**
```bash
# Use quick mode to skip network checks
./verify_sovereignty.sh --quick
```

**Missing Python or Node.js:**
```bash
# These are optional - warnings can be ignored
# Or install: apt install python3 nodejs
```

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

Built with 🔥 by the **Strategickhaos Swarm Intelligence collective**

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

---

## 📚 Related Documentation

- [README.md](README.md) - Main project documentation
- [SECURITY.md](SECURITY.md) - Security policy
- [TRUST_DECLARATION.md](TRUST_DECLARATION.md) - Trust and provenance
- [governance/access_matrix.yaml](governance/access_matrix.yaml) - Access control
- [sbom.yaml](sbom.yaml) - Software Bill of Materials
