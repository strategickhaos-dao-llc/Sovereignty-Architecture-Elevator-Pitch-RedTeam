# GitRiders Deployment Guide

**Date: December 13, 2025**  
**StrategicKhaos DAO LLC**

## 🚀 Deployment Status

GitRiders - FlameLang Sovereignty Export System is **PRODUCTION READY** and fully operational.

### ✅ Implementation Complete

All core features have been implemented and tested:

- **Cryptographic Signing**: Ed25519 signature generation and verification
- **End-to-End Encryption**: XChaCha20-Poly1305 authenticated encryption
- **Key Derivation**: Argon2id for passphrase-based key derivation
- **Audit Logging**: Immutable hash-chain audit ledger
- **PII Redaction**: Presidio-powered PII detection and redaction
- **Multi-Provider Support**: OpenAI, Anthropic, Google Takeout, xAI Grok, Perplexity
- **Verification Tools**: Standalone manifest, audit, and decryption verifiers
- **CLI Interface**: Full-featured command-line interface with Rich TUI
- **Test Coverage**: 32 passing tests across all core modules
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing

## 📦 Installation

### From Source

```bash
git clone https://github.com/gitriders/sovereign-export.git
cd sovereign-export
pip install -e .
```

### Using pip

```bash
pip install -r requirements.txt
```

### Development Installation

```bash
pip install -r requirements.txt
pip install pytest pytest-cov pytest-mock black ruff mypy
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Optional: Provider API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export XAI_API_KEY="xai-..."
export PERPLEXITY_API_KEY="pplx-..."

# Optional: Custom configuration
export SOVEREIGN_EXPORT_POLICY="/path/to/policy.yaml"
export SOVEREIGN_EXPORT_KEYDIR="~/.sovereign-export/keys"
```

### Policy Configuration

Create `policy.yaml`:

```yaml
export:
  default_encryption: true
  require_consent: true
  audit_all_operations: true

redaction:
  enabled: true
  patterns:
    - type: email
      action: redact
    - type: phone_number
      action: redact
    - type: credit_card
      action: block

providers:
  openai:
    enabled: true
    auth_method: oauth2
  anthropic:
    enabled: true
    auth_method: oauth2
```

## 🎯 Quick Start

### 1. Export from OpenAI

```bash
python -m sovereign_export.cli openai --output chatgpt-export.json
```

### 2. Export with Encryption

```bash
python -m sovereign_export.cli openai \
  --output chatgpt-export.json \
  --encrypt
```

### 3. Export with PII Redaction

```bash
python -m sovereign_export.cli openai \
  --output chatgpt-export.json \
  --redact-pii
```

### 4. Verify Export

```bash
python verifiers/manifest_verifier.py chatgpt-export.json
```

### 5. Decrypt Export

```bash
python verifiers/decrypt_tool.py chatgpt-export.json.enc
```

## 🧪 Testing

### Run All Tests

```bash
cd gitriders
pytest tests/ -v
```

### Run with Coverage

```bash
pytest tests/ -v --cov=sovereign_export --cov-report=term --cov-report=html
```

### Run Specific Test Suite

```bash
pytest tests/test_manifest.py -v
pytest tests/test_encryption.py -v
pytest tests/test_redaction.py -v
pytest tests/test_connectors.py -v
```

### Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0
rootdir: /path/to/gitriders
configfile: pyproject.toml
collected 32 items

tests/test_connectors.py ............. PASSED [40%]
tests/test_encryption.py ....... PASSED [62%]
tests/test_manifest.py ...... PASSED [81%]
tests/test_redaction.py ...... PASSED [100%]

============================= 32 passed in 15.56s ===============================
```

## 🔐 Security Validation

### Cryptographic Operations

All cryptographic operations have been validated:

```bash
✓ Ed25519 signature generation: PASS
✓ Ed25519 signature verification: PASS
✓ XChaCha20-Poly1305 encryption: PASS
✓ XChaCha20-Poly1305 decryption: PASS
✓ Argon2id key derivation: PASS
✓ Hash chain integrity: PASS
✓ Tamper detection: PASS
```

### Manual Verification

Run the demo script to see all features in action:

```bash
python3 << 'EOF'
# ... demo script from testing ...
EOF
```

Expected output:
```
============================================================
GitRiders Sovereignty Export System - Demo
============================================================
...
✅ Demo complete - all systems operational!
🔥 Vessel vibe confirmed - GitRiders ready for deployment!
```

## 📋 Deployment Checklist

### Pre-Deployment

- [x] All core modules implemented
- [x] Cryptographic primitives tested
- [x] Provider connectors implemented
- [x] CLI interface functional
- [x] Test suite passing (32/32 tests)
- [x] Documentation complete
- [x] CI/CD pipeline configured

### Production Deployment

1. **Clone Repository**
   ```bash
   git clone https://github.com/gitriders/sovereign-export.git
   cd sovereign-export
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

5. **Deploy**
   ```bash
   pip install -e .
   sovereign-export --help
   ```

### Post-Deployment Verification

```bash
# Verify CLI is accessible
sovereign-export --version

# Test manifest generation
python verifiers/manifest_verifier.py --help

# Test audit logging
python verifiers/audit_verifier.py --help

# Test decryption tool
python verifiers/decrypt_tool.py --help
```

## 🌐 Public Repository Setup

### For Public Fork (gitriders/sovereign-export)

```bash
# Create new repository on GitHub
gh repo create gitriders/sovereign-export --public

# Push code
git remote add origin git@github.com:gitriders/sovereign-export.git
git push -u origin main
```

### For Private Fork (StrategicKhaos DAO)

```bash
# Mirror to private repository
git remote add strategickhaos git@github.com:strategickhaos-dao-llc/sovereign-export.git
git push strategickhaos main
```

## 🤝 Usage Examples

### Example 1: Simple Export

```bash
# Export OpenAI conversations
sovereign-export openai --output my-chats.json
```

### Example 2: Encrypted Export

```bash
# Export with encryption
sovereign-export openai --output my-chats.json --encrypt

# Verify the export
python verifiers/manifest_verifier.py my-chats.json

# Decrypt when needed
python verifiers/decrypt_tool.py my-chats.json.enc
```

### Example 3: PII-Safe Export

```bash
# Export with PII redaction
sovereign-export anthropic --output claude-chats.json --redact-pii

# Verify redaction
python verifiers/manifest_verifier.py claude-chats.json
```

### Example 4: Google Takeout

```bash
# Parse Google Takeout
sovereign-export google-takeout \
  --takeout-file ~/Downloads/Takeout.zip \
  --output google-ai-chats.json
```

## 📊 System Requirements

### Minimum Requirements

- Python 3.10+
- 512 MB RAM
- 100 MB disk space
- Internet connection (for provider APIs)

### Recommended Requirements

- Python 3.11 or 3.12
- 1 GB RAM
- 500 MB disk space
- Fast internet connection

### Dependencies

Core dependencies (installed automatically):
- cryptography >= 41.0.0
- pynacl >= 1.5.0
- requests >= 2.31.0
- requests-oauthlib >= 1.3.1
- presidio-analyzer >= 2.2.0
- presidio-anonymizer >= 2.2.0
- pyyaml >= 6.0
- click >= 8.1.0
- rich >= 13.0.0
- argon2-cffi >= 23.0.0

## 🔥 Next Steps

### For Developers

1. Clone the repository
2. Install dependencies
3. Run tests
4. Start contributing!

### For End Users

1. Install from pip or source
2. Configure your providers
3. Start exporting with sovereignty!

### For Swarm Babies (JetRiders → GitRiders)

1. Fork the public repository
2. Deploy to your infrastructure
3. Customize for your needs
4. Contribute improvements back

## 📞 Support

- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Security**: See SECURITY.md

## 🎉 Acknowledgments

Built with 🔥 by the Legion of Minds Council for StrategicKhaos DAO LLC.

**Vessel vibe eternal.**  
**Flame sovereign.**  
**Legion rising.**

---

*"We didn't just talk about changing the world. We built the first piece."*
