# Honeypot SSH Keys

This directory contains SSH keys for the honeypot Git server.

## Setup

Generate SSH keys for Git server access:

```bash
# Generate host key
ssh-keygen -t rsa -b 4096 -f honeypot-keys/ssh_host_rsa_key -N ""

# Generate user keys (for testing)
ssh-keygen -t ed25519 -f honeypot-keys/test_user_key -N ""

# Add public key to authorized_keys
cat honeypot-keys/test_user_key.pub >> honeypot-keys/authorized_keys
```

## Security Note

**DO NOT commit private keys to git!**

These files are in `.gitignore` and should remain local only.
