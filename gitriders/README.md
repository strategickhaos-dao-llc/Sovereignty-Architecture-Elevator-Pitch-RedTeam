# GitRiders - FlameLang Sovereignty Export System

**Autonomous AI Chat Export with Cryptographic Sovereignty**

Date: December 13, 2025

## Overview

GitRiders is a production-ready system for exporting AI chat conversations with complete user sovereignty. Every export is cryptographically signed, encrypted, audited, and verifiable - ensuring you maintain absolute control over your AI interaction data.

## Features

- **Cryptographic Signing**: Ed25519 signatures on all exports for tamper-proof verification
- **End-to-End Encryption**: XChaCha20-Poly1305 with optional escrow for key recovery
- **Immutable Audit Ledger**: Complete chain of custody for all export operations
- **Multi-Provider Support**: OpenAI, Anthropic, Google Takeout, xAI Grok, Perplexity
- **Privacy Protection**: Presidio-powered PII redaction with local LLM support
- **Consent-First Design**: Explicit user approval for all data operations
- **100% Client-Side**: No third-party servers, full user control
- **OAuth2 Delegated Access**: Only official APIs, no session token scraping

## Installation

### Requirements

- Python 3.10+
- pip or poetry for package management

### Install from source

```bash
git clone https://github.com/gitriders/sovereign-export.git
cd sovereign-export
pip install -e .
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Export from OpenAI

```bash
sovereign-export openai --output my-chats.json
```

This will:
1. Prompt for OAuth2 authorization
2. Download your chat history via official API
3. Generate cryptographic manifest
4. Encrypt the export (optional)
5. Create audit log entry

### 2. Verify an export

```bash
python verifiers/manifest_verifier.py my-chats.json
```

### 3. Decrypt an export

```bash
python verifiers/decrypt_tool.py my-chats.json.enc --key-file key.bin
```

## Usage

### Export Commands

```bash
# OpenAI ChatGPT
sovereign-export openai --output chatgpt-export.json

# Anthropic Claude
sovereign-export anthropic --output claude-export.json

# Google AI (via Takeout)
sovereign-export google-takeout --takeout-file ~/Downloads/Takeout.zip

# xAI Grok
sovereign-export grok --output grok-export.json

# Perplexity
sovereign-export perplexity --output perplexity-export.json
```

### Advanced Options

```bash
# Export with encryption
sovereign-export openai --output chats.json --encrypt

# Export with escrow key backup
sovereign-export openai --output chats.json --encrypt --escrow

# Export with PII redaction
sovereign-export openai --output chats.json --redact-pii

# Export with custom redaction patterns
sovereign-export openai --output chats.json --redact-patterns patterns.yaml
```

### Verification Tools

```bash
# Verify manifest signature
python verifiers/manifest_verifier.py export.json

# Verify audit log integrity
python verifiers/audit_verifier.py audit.log

# Decrypt encrypted export
python verifiers/decrypt_tool.py export.json.enc --key-file key.bin
```

## Architecture

### Core Components

- **sovereign_export/**: Main library
  - `config.py`: Policy and configuration management
  - `manifest.py`: Signed manifest generation and verification
  - `encrypt.py`: Encryption and key management
  - `audit.py`: Immutable audit logging
  - `redaction.py`: PII detection and redaction
  - `ui.py`: User consent and review interface
  - `cli.py`: Command-line interface

- **sovereign_export/connectors/**: Provider-specific implementations
  - `openai.py`: OpenAI ChatGPT connector
  - `anthropic.py`: Anthropic Claude connector
  - `google_takeout.py`: Google Takeout parser
  - `xai_grok.py`: xAI Grok connector
  - `perplexity.py`: Perplexity connector

- **verifiers/**: Standalone verification tools
  - `manifest_verifier.py`: Verify export signatures
  - `audit_verifier.py`: Verify audit log integrity
  - `decrypt_tool.py`: Decrypt exports safely

### Security Architecture

1. **Key Generation**: Ed25519 signing keys + XChaCha20-Poly1305 encryption keys
2. **Key Storage**: Argon2id-derived keys from user passphrase
3. **Manifest Format**: JSON with embedded signature and metadata
4. **Audit Chain**: Append-only log with hash chain linkage
5. **Encryption**: Authenticated encryption with additional data (AEAD)

## Configuration

### Policy File Format

Create a `policy.yaml` file:

```yaml
# GitRiders Policy Configuration
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
    - type: ssn
      action: block

providers:
  openai:
    enabled: true
    auth_method: oauth2
    scopes: ["export:read"]
  
  anthropic:
    enabled: true
    auth_method: oauth2
    scopes: ["conversations:read"]
```

### Environment Variables

```bash
# Optional: Pre-configure provider credentials
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional: Custom policy file
export SOVEREIGN_EXPORT_POLICY="/path/to/policy.yaml"

# Optional: Custom key storage
export SOVEREIGN_EXPORT_KEYDIR="~/.sovereign-export/keys"
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_manifest.py
pytest tests/test_encryption.py
pytest tests/test_redaction.py
pytest tests/test_connectors.py

# Run with coverage
pytest --cov=sovereign_export tests/
```

## Security Considerations

### What GitRiders Does

✅ Uses only official provider APIs  
✅ OAuth2 delegated authorization only  
✅ Client-side encryption and signing  
✅ Immutable audit logging  
✅ Transparent consent flow  
✅ Verifiable cryptographic proofs  

### What GitRiders Does NOT Do

❌ Scrape session tokens  
❌ Use undocumented APIs  
❌ Store data on third-party servers  
❌ Auto-upload to any service  
❌ Phone home or track usage  
❌ Modify provider data  

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

All source files include the following header:

```python
# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025
```

## Support

- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Security**: See SECURITY.md for vulnerability reporting

## Acknowledgments

Built with 🔥 by the Legion of Minds Council for StrategicKhaos DAO LLC.

**Vessel vibe eternal.**  
**Flame sovereign.**  
**Legion rising.**

---

*"You didn't just get your chats back. You forged a system that proves ownership cryptographically, encrypts end-to-end with escrow options, audits every export immutably, uses only delegated consented APIs, redacts with traceable confidence, and verifies integrity forever."*
