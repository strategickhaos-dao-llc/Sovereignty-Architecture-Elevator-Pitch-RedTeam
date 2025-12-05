# Proofs Directory

This directory contains cryptographic proof artifacts for defensive publications:

- `.hash` files: SHA256 hashes of source documents
- `.ots` files: OpenTimestamps proof files (Bitcoin blockchain anchored)
- `.sig` files: GPG detached signatures
- `gpg_pubkey.asc`: Public key for signature verification

## Verification

To verify proofs:

1. **SHA256 Hash**: `sha256sum <file> | diff - <file>.hash`
2. **OpenTimestamps**: `ots verify <file>.ots`
3. **GPG Signature**: `gpg --verify <file>.sig <file>`

## Requirements

- `ots` CLI: `pip install opentimestamps-client`
- `gpg`: GNU Privacy Guard
