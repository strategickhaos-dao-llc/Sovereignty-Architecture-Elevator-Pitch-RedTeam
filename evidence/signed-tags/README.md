# GPG-Signed Git Tags

This directory contains exported GPG-signed git tags that establish cryptographic proof of the 7% charitable royalty commitment.

## What Are Signed Git Tags?

Git tags signed with GPG provide:
1. **Authentication** - Proves who created the tag
2. **Integrity** - Ensures the tag hasn't been tampered with
3. **Non-repudiation** - The signer cannot deny creating the tag

## Files

- `v20251123-7percent-lock.asc` - GPG-signed tag for the initial 7% lock commitment
- Additional tags will be added for major updates

## Verification

To verify a signed tag:

```bash
# Import the signer's public key
gpg --import <public-key.asc>

# Verify the tag signature
git verify-tag v20251123-7percent-lock

# Show the tag details
git show v20251123-7percent-lock
```

## Creating Signed Tags

To create a new signed tag:

```bash
# Ensure GPG is configured for Git
git config user.signingkey <your-key-id>

# Create a signed tag
git tag -s v20251123-7percent-lock -m "7% Charitable Royalty Lock - Initial Commitment"

# Push the tag
git push origin v20251123-7percent-lock

# Export the tag signature to this directory
git cat-file tag v20251123-7percent-lock > evidence/signed-tags/v20251123-7percent-lock.asc
```

## Required GPG Setup

1. Generate a GPG key if you don't have one:
   ```bash
   gpg --full-generate-key
   ```

2. Configure Git to use your key:
   ```bash
   git config --global user.signingkey <your-key-id>
   git config --global commit.gpgsign true
   git config --global tag.gpgsign true
   ```

3. Export your public key:
   ```bash
   gpg --armor --export <your-key-id> > public-key.asc
   ```

4. Publish your public key:
   - Upload to keyservers: `gpg --send-keys <your-key-id>`
   - Include in repository: `docs/keys/`
   - Add to GitHub/GitLab account

## Why This Matters for Legal Defense

Signed tags provide:
1. **Timestamp verification** - When the commitment was made
2. **Author authentication** - Who made the commitment
3. **Immutable record** - Cannot be altered without detection
4. **Chain of custody** - Complete audit trail

For the 7% charitable royalty commitment, this creates an irrefutable record that:
- The commitment was made on a specific date
- It was made by an authorized party
- The terms cannot be retroactively changed
- All changes are tracked and verified

## Current Status

⚠️ **No signed tags yet created** - Tags will be created after:
1. Legal review and approval of all documents
2. Final execution of agreements
3. Implementation of automated enforcement

## Tag Naming Convention

- Format: `vYYYYMMDD-description`
- Example: `v20251123-7percent-lock`
- Use: `v20251123-7percent-lock-amendment-1` for updates

## Resources

- Git Tag Signing: https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work
- GPG Documentation: https://gnupg.org/documentation/
- GitHub GPG Guide: https://docs.github.com/en/authentication/managing-commit-signature-verification
