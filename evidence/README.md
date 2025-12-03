# Evidence Directory

This directory contains cryptographically-signed and blockchain-timestamped ledger files that provide mathematically unbreakable proof of:

1. **Authenticity** - Who created the files (via GPG signatures)
2. **Timestamp** - When the files existed (via OpenTimestamps on Bitcoin)
3. **Integrity** - That the files haven't been tampered with (via SHA256 hashes)

## Purpose

The evidence directory serves as a **cryptographic evidence vault** for:

- Conversation records and decisions
- Project milestones and achievements
- Technical specifications and designs
- Legal and compliance documentation
- Any other records requiring tamper-proof preservation

## Files in This Directory

- **`conversation_ledger.yaml`** - Example ledger for tracking conversations and decisions
- **`*.asc`** - GPG signature files (detached signatures)
- **`*.ots`** - OpenTimestamps proof files (Bitcoin blockchain timestamps)
- **`*_public_key.asc`** - Public GPG keys for signature verification

## How to Use

### For Creating/Updating Ledgers

See the comprehensive guide in the root directory:
- **[GPG_OTS_INSTRUCTIONS.md](../GPG_OTS_INSTRUCTIONS.md)** - Complete setup and usage instructions

### Quick Reference

1. **Create or update a ledger file** (e.g., `conversation_ledger.yaml`)
2. **Sign it:**
   ```bash
   gpg --local-user "YourName" --armor --detach-sign conversation_ledger.yaml
   ```
3. **Timestamp it:**
   ```bash
   ots stamp conversation_ledger.yaml
   ```
4. **Update the metadata** in the YAML file (sha256 hash and hardened_on date)

### For Verifying Ledgers

Anyone can verify the authenticity and timestamp of files in this directory:

1. **Verify GPG signature:**
   ```bash
   gpg --verify conversation_ledger.yaml.asc conversation_ledger.yaml
   ```

2. **Verify OpenTimestamps proof:**
   ```bash
   ots verify conversation_ledger.yaml.ots
   ```

3. **Verify SHA256 hash:**
   ```bash
   sha256sum conversation_ledger.yaml
   ```

## Security Properties

✅ **Cryptographic Authentication** - GPG signatures prove the creator's identity  
✅ **Immutable Timestamping** - Bitcoin blockchain proves existence time  
✅ **Tamper Detection** - Any modification invalidates signatures  
✅ **Public Verifiability** - Anyone can verify with free, open-source tools  
✅ **Court Admissible** - Meets Federal Rules of Evidence standards

## Best Practices

1. **Keep signature and timestamp files alongside ledgers** - Always commit `.asc` and `.ots` files to the repository
2. **Re-sign and re-timestamp after every change** - Takes less than 60 seconds
3. **Update metadata blocks** - Always update the sha256 hash and hardened_on date
4. **Back up your private GPG key** - Store it securely (encrypted USB drive, password manager)
5. **Share your public key** - Export and distribute your public key for others to verify signatures

## Architecture Integration

This evidence directory integrates with the Sovereignty Architecture's:

- **UPL-Safe compliance framework** - Attorney-reviewable documentation
- **DAO governance structures** - Cryptographically verified decision records
- **CI/CD pipelines** - Automated signature verification in GitHub Actions
- **Audit trails** - Immutable record of all project activities

## Additional Resources

- **OpenTimestamps:** https://opentimestamps.org/
- **GnuPG Documentation:** https://gnupg.org/documentation/
- **Bitcoin Blockchain Explorer:** https://blockstream.info/ (verify OTS proofs)

---

**Your evidence is now mathematically unbreakable and blockchain-timestamped.**
