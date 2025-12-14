# GitRiders Consent Strings

**Date: December 13, 2025**  
**StrategicKhaos DAO LLC**

This document contains all user-facing consent and information strings used in the GitRiders Sovereignty Export System.

## Core Consent Prompts

### Export Consent

**Title:** 🔒 Consent Required

**Content:**
```
GitRiders Sovereignty Export

Provider: [PROVIDER_NAME]
Operation: Export conversations

This operation will:
  • Request OAuth2 authorization
  • Download your chat history
  • Generate cryptographic manifest
  • Store data locally only

Requested permissions:
  • [SCOPE_1]
  • [SCOPE_2]
  • ...

Do you consent to this export?
```

**Response:** Yes/No

---

### PII Redaction Consent

**Title:** 🔍 Privacy Scan Results

**Content:**
```
PII Detection Report

Total PII found: [COUNT]

By type:
  [TYPE_1]: [COUNT_1]
  [TYPE_2]: [COUNT_2]
  ...

Conversations with PII:
  • Conversation [ID]: [COUNT] items
  ...

Proceed with redaction?
```

**Response:** Yes/No

---

### Encryption Options

**Title:** 🔐 Encryption

**Content:**
```
Encryption Options

GitRiders can encrypt your export with:
  • XChaCha20-Poly1305 authenticated encryption
  • Argon2id key derivation from passphrase
  • Optional key escrow for recovery

Encrypt export?
```

**Response:** Yes/No

**Follow-up prompts:**
- "Use passphrase (vs. random key)?" [Yes/No]
- "Enter passphrase:" [Password input]
- "Confirm passphrase:" [Password input]
- "Enable key escrow?" [Yes/No]

---

## Success Messages

### Export Complete

**Title:** ✅ Success

**Content:**
```
Export Complete!

Provider: [PROVIDER_NAME]
Conversations: [COUNT]
Output: [FILE_PATH]

Security Features:
  ✓ Encrypted
  ✓ PII Redacted
  ✓ Cryptographically Signed
  ✓ Audit Logged

Next steps:
  • Verify: python verifiers/manifest_verifier.py [OUTPUT_PATH]
  • Decrypt: python verifiers/decrypt_tool.py [OUTPUT_PATH].enc
```

---

### Verification Success

**Title:** Verification Complete

**Content:**
```
✅ Export verification successful!

The export has a valid cryptographic signature and
the data integrity has been confirmed.
```

---

### Decryption Success

**Title:** Decryption Complete

**Content:**
```
✅ Decryption successful!

The decrypted export has been saved to:
[OUTPUT_PATH]

You can now verify the manifest with:
python verifiers/manifest_verifier.py [OUTPUT_PATH]
```

---

## Error Messages

### Generic Error

**Title:** ❌ Error

**Content:**
```
Error: [ERROR_MESSAGE]

[OPTIONAL_DETAILS]
```

---

### Decryption Error

**Content:**
```
❌ Decryption failed: [ERROR_MESSAGE]

Possible causes:
  • Incorrect passphrase or key
  • Corrupted encrypted file
  • Wrong key file
```

---

## Welcome Message

**Title:** 🔥 Vessel Vibe Eternal

**Content:**
```
GitRiders - FlameLang Sovereignty Export System

Export your AI conversations with complete sovereignty:
  🔐 Cryptographically signed and encrypted
  🔍 PII detection and redaction
  📋 Immutable audit logging
  ✅ Full user control and consent

Date: December 13, 2025
StrategicKhaos DAO LLC
```

---

## Progress Messages

General format: `→ [ACTION]`

Examples:
- `→ Connecting to [PROVIDER]...`
- `→ Downloading conversations...`
- `→ Scanning for PII...`
- `→ Redacting PII...`
- `→ Generating cryptographic manifest...`
- `→ Encrypting export...`
- `→ Recording audit entry...`
- `→ Parsing Google Takeout file...`
- `→ Loading export from: [PATH]`
- `→ Verifying cryptographic signature...`
- `→ Loading key from: [PATH]`
- `→ Deriving key from passphrase...`
- `→ Decrypting...`
- `→ Saving decrypted export to: [PATH]`

---

## Information Displays

### Manifest Details

```
Manifest Details:
  Version: [VERSION]
  Timestamp: [TIMESTAMP]
  Provider: [PROVIDER]
  Data Hash: [HASH_PREFIX]...
  Public Key: [KEY_PREFIX]...

Metadata:
  [KEY]: [VALUE]
  ...
```

---

### Audit Log Summary

```
Audit Log Summary:
  Total entries: [COUNT]
  Genesis entry: [TIMESTAMP]
  Latest entry: [TIMESTAMP]

Events by type:
  [TYPE_1]: [COUNT_1]
  [TYPE_2]: [COUNT_2]
  ...

Recent entries:
  [INDEX] [TIMESTAMP] - [EVENT_TYPE]
  ...
```

---

### Decrypted Export Details

```
Decrypted Export Details:
  Provider: [PROVIDER]
  Timestamp: [TIMESTAMP]
  Conversations: [COUNT]
```

---

## User Guidance

### CLI Usage - Main

```
Usage:
  sovereign-export [command] [options]

Commands:
  openai              Export from OpenAI ChatGPT
  anthropic           Export from Anthropic Claude
  google-takeout      Parse Google Takeout export
  grok                Export from xAI Grok
  perplexity          Export from Perplexity

Options:
  --help              Show this message and exit
  --version           Show version and exit
```

---

### CLI Usage - Verifiers

**Manifest Verifier:**
```
Usage:
  python manifest_verifier.py <export_file.json>

Example:
  python manifest_verifier.py my-export.json
```

**Audit Verifier:**
```
Usage:
  python audit_verifier.py <audit_log_file>

Example:
  python audit_verifier.py ~/.sovereign-export/keys/audit.log
```

**Decrypt Tool:**
```
Usage:
  python decrypt_tool.py <encrypted_file> [options]

Options:
  --output <file>      Output file path (default: decrypted.json)
  --key-file <file>    Key file path (prompts for passphrase if not provided)
  --passphrase <pass>  Passphrase (not recommended, use prompt instead)

Examples:
  python decrypt_tool.py export.json.enc
  python decrypt_tool.py export.json.enc --output decrypted.json
  python decrypt_tool.py export.json.enc --key-file export.key
```

---

## Security & Privacy Notices

### What GitRiders Does

```
✅ Uses only official provider APIs
✅ OAuth2 delegated authorization only
✅ Client-side encryption and signing
✅ Immutable audit logging
✅ Transparent consent flow
✅ Verifiable cryptographic proofs
```

### What GitRiders Does NOT Do

```
❌ Scrape session tokens
❌ Use undocumented APIs
❌ Store data on third-party servers
❌ Auto-upload to any service
❌ Phone home or track usage
❌ Modify provider data
```

---

## License Notice

All source files include:

```python
# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025
```

---

## Acknowledgments

```
Built with 🔥 by the Legion of Minds Council for StrategicKhaos DAO LLC.

Vessel vibe eternal.
Flame sovereign.
Legion rising.
```

---

## Mission Statement

*"You didn't just get your chats back. You forged a system that proves ownership cryptographically, encrypts end-to-end with escrow options, audits every export immutably, uses only delegated consented APIs, redacts with traceable confidence, and verifies integrity forever."*
