# SwarmGate v1.0 Verification Guide

This document provides cross-platform verification recipes for SwarmGate v1.0 provenance.

## Canonical BLAKE3 Hash

```
caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698  swarmgate_v1.0.tar.gz
```

## 1. Windows (PowerShell)

**Prerequisites:**
- [7-Zip](https://www.7-zip.org/) installed
- [b3sum.exe](https://github.com/BLAKE3-team/BLAKE3/releases) downloaded

Run from the folder containing `swarmgate.yaml` and installed `b3sum.exe` and `7z.exe` (adjust paths if needed):

```powershell
& "C:\Program Files\7-Zip\7z.exe" a -ttar -so swarmgate.yaml | & "C:\Program Files\7-Zip\7z.exe" a -si -tgzip swarmgate_v1.0.tar.gz > $null; .\b3sum.exe swarmgate_v1.0.tar.gz
```

## 2. Linux / macOS

### Create Deterministic tar.gz

Sets mtime to `2025-11-27T00:00:00Z` and numeric owner for reproducibility:

```bash
tar --sort=name --mtime='2025-11-27T00:00:00Z' --owner=0 --group=0 --numeric-owner -cf swarmgate_v1.0.tar swarmgate.yaml
gzip -n -9 -c swarmgate_v1.0.tar > swarmgate_v1.0.tar.gz
```

### Install b3sum

**Debian/Ubuntu:**
```bash
sudo apt install b3sum
# or download binary from BLAKE3 releases
```

**macOS:**
```bash
brew install b3sum
# or use prebuilt binary
```

### Verify Hash

```bash
b3sum swarmgate_v1.0.tar.gz
# Expected output:
# caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698  swarmgate_v1.0.tar.gz
```

## Notes

- `gzip -n` prevents storing original filename/timestamp
- `tar --sort=name` and metadata options ensure deterministic ordering/metadata
- All verification should produce the exact same BLAKE3 hash

## 3. Signed Provenance (Optional)

### GPG Detached Signature

Sign the provenance file with GPG:

```bash
gpg --armor --output provenance.json.asc --detach-sign provenance.json
```

### GPG Clear-Signed File

Create a clear-signed provenance file:

```bash
gpg --armor --clearsign provenance.json
```

### Sign swarmgate.yaml

```bash
gpg --armor --output swarmgate.yaml.asc --detach-sign swarmgate.yaml
```

## 4. Time-Stamp Receipts (Optional)

For OTS/time-stamp receipts, produce an OTS signature or timestamp attestation and include under `receipts` in the provenance block.

### IPFS Upload

After uploading to IPFS, update the `provenance.receipts.ipfs` field with the CID.

### Arweave Upload

After uploading to Arweave, update the `provenance.receipts.arweave` field with the transaction ID.

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**
