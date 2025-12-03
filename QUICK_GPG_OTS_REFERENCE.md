# Quick GPG + OTS Reference Card

**60-Second Workflow for Ledger Updates**

## Every Time You Update a Ledger

```bash
# 1. Sign it
gpg --local-user "YourName" --armor --detach-sign ledger_file.yaml

# 2. Timestamp it
ots stamp ledger_file.yaml

# 3. Get new hash (update in YAML metadata)
sha256sum ledger_file.yaml        # Linux/Mac
certutil -hashfile ledger_file.yaml SHA256   # Windows

# 4. Update these fields in ledger_metadata:
#    - sha256: [paste hash from step 3]
#    - hardened_on: [today's date]
```

**Total time:** Less than 60 seconds

---

## One-Time Setup (If You Haven't Done This Yet)

```bash
# 1. Install OpenTimestamps
pip install opentimestamps-client

# 2. Create GPG key (if you don't have one)
gpg --full-generate-key
# Choose: RSA 4096, no expiration

# 3. Export your public key
gpg --armor --export YourName > your_public_key.asc

# 4. Get your fingerprint (add to metadata)
gpg --fingerprint YourName
```

---

## Verification (Anyone Can Do This)

```bash
# Verify signature
gpg --verify ledger_file.yaml.asc ledger_file.yaml

# Verify timestamp
ots verify ledger_file.yaml.ots

# Verify hash
sha256sum ledger_file.yaml
```

---

## Common Commands

### List Your GPG Keys
```bash
gpg --list-secret-keys
```

### Sign with Specific Key
```bash
gpg --local-user "email@example.com" --armor --detach-sign file.yaml
```

### Upgrade OTS Proof (If Pending)
```bash
ots upgrade file.yaml.ots
```

### Export Public Key for Sharing
```bash
gpg --armor --export YourName > public_key.asc
```

---

## File Structure

After signing and timestamping, you'll have:

```
evidence/
├── conversation_ledger.yaml           ← Your ledger
├── conversation_ledger.yaml.asc       ← GPG signature
├── conversation_ledger.yaml.ots       ← OTS timestamp
└── your_public_key.asc                ← Share this for verification
```

---

## Metadata Block Template

Add this to the top of every ledger file:

```yaml
ledger_metadata:
  version: "1.0"
  hardened_on: "YYYY-MM-DD"
  sha256: "paste_hash_here"
  integrity:
    gpg_signed: true
    gpg_key_fingerprint: "paste_fingerprint_here"
    gpg_signature_file: "filename.yaml.asc"
    opentimestamps:
      proof_file: "filename.yaml.ots"
      status: "stamped_and_verified"
      note: "Existence proven on Bitcoin blockchain – verifiable by anyone forever"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No secret key" error | Use `gpg --list-secret-keys` and specify correct name/email |
| "ots: command not found" | Install: `pip install opentimestamps-client` |
| OTS shows "Pending" | Wait a few hours, then: `ots upgrade file.yaml.ots` |
| Can't find fingerprint | Run: `gpg --fingerprint YourName` |

---

## Full Documentation

See **[GPG_OTS_INSTRUCTIONS.md](./GPG_OTS_INSTRUCTIONS.md)** for:
- Complete setup instructions
- Advanced usage scenarios
- Sworn declaration templates
- Third-party verification guides
- Troubleshooting details

---

**Your ledger is now mathematically unbreakable. 🔒**
