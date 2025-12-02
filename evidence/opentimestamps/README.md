# OpenTimestamps Evidence

This directory contains OpenTimestamps (OTS) proofs for legal and governance documents.

## What is OpenTimestamps?

OpenTimestamps provides cryptographic proof that a document existed at a specific point in time by anchoring its hash to the Bitcoin blockchain.

## Files

- `*.ots` - OpenTimestamps proof files
- Each `.ots` file corresponds to a document in `/legal` or `/governance`

## Verification

To verify a timestamp:

```bash
# Install OpenTimestamps client
pip install opentimestamps-client

# Verify a timestamp
ots verify <document> -f <document>.ots

# Example:
ots verify ../governance/royalty-lock.yaml -f royalty-lock.yaml.ots
```

## Creating Timestamps

To create new timestamps:

```bash
# Stamp a file
ots stamp <document>

# This creates <document>.ots which should be moved to this directory
```

## Why This Matters

For legal purposes, OpenTimestamps provides:
1. **Immutable proof** of when a commitment was made
2. **Third-party verification** via Bitcoin blockchain
3. **Court admissibility** as evidence of document existence
4. **Zero cost** - only requires one transaction to Bitcoin

This is especially important for the irrevocable 7% charitable royalty commitment, as it establishes:
- When the commitment was made
- That it cannot be backdated or altered
- Independent verification by anyone

## Current Status

⚠️ **No timestamps yet created** - This directory will be populated after legal review and finalization of all documents.

## Next Steps

1. Finalize all legal documents with attorney review
2. Generate SHA-256 hashes
3. Create OpenTimestamps proofs
4. Verify timestamps are properly recorded on Bitcoin blockchain
5. Store `.ots` files in this directory

## Resources

- OpenTimestamps: https://opentimestamps.org/
- GitHub: https://github.com/opentimestamps
- Documentation: https://opentimestamps.org/docs/
