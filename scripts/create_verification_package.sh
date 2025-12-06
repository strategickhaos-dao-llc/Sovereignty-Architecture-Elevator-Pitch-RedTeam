#!/bin/bash
# create_verification_package.sh - Bundle ledger files for third-party verification
# Part of Appendix C: Legal Standards for AI Conversation Logs
# Usage: ./create_verification_package.sh [ledger_files...]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PACKAGE_NAME="verification_package_$(date +%Y%m%d_%H%M%S)"
REPO_URL=$(git config --get remote.origin.url 2>/dev/null || echo "N/A")
# Get email from git config or environment variable
DEFAULT_EMAIL="$(git config user.email 2>/dev/null)"
GPG_EMAIL="${GPG_EMAIL:-${DEFAULT_EMAIL}}"

echo -e "${YELLOW}Creating verification package: ${PACKAGE_NAME}${NC}"
echo ""

# Create package directory
mkdir -p "$PACKAGE_NAME"

# If no files specified, find all ledger files
if [ $# -eq 0 ]; then
    echo "No files specified, searching for ledger entries..."
    LEDGER_FILES=$(find . -name "*ledger*.yml" -o -name "*ledger*.yaml" -o -name "*entry*.yml" -o -name "*entry*.yaml" 2>/dev/null)
    
    if [ -z "$LEDGER_FILES" ]; then
        echo -e "${RED}Error: No ledger files found${NC}"
        echo "Usage: $0 [ledger_files...]"
        exit 1
    fi
else
    LEDGER_FILES="$@"
fi

FILE_COUNT=0
for file in $LEDGER_FILES; do
    if [ -f "$file" ]; then
        echo "Adding: $file"
        cp "$file" "$PACKAGE_NAME/"
        FILE_COUNT=$((FILE_COUNT + 1))
        
        # Copy associated signature files if they exist
        if [ -f "${file}.asc" ]; then
            cp "${file}.asc" "$PACKAGE_NAME/"
            echo "  + Signature: ${file}.asc"
        fi
        
        # Copy associated timestamp files if they exist
        if [ -f "${file}.ots" ]; then
            cp "${file}.ots" "$PACKAGE_NAME/"
            echo "  + Timestamp: ${file}.ots"
        fi
    fi
done

echo ""
echo "Added $FILE_COUNT ledger file(s)"

# Export public GPG key if available
if command -v gpg &> /dev/null; then
    echo ""
    echo "Exporting GPG public key..."
    if gpg --armor --export "$GPG_EMAIL" > "$PACKAGE_NAME/public_key.asc" 2>/dev/null; then
        echo -e "${GREEN}✓ Public key exported${NC}"
        
        # Get key info
        KEY_ID=$(gpg --list-keys --keyid-format LONG "$GPG_EMAIL" 2>/dev/null | grep pub | awk '{print $2}' | cut -d'/' -f2 | head -1)
        FINGERPRINT=$(gpg --fingerprint "$GPG_EMAIL" 2>/dev/null | grep -A 1 "pub" | grep -v "pub" | tr -d ' ')
    else
        echo -e "${YELLOW}Warning: Could not export GPG key for $GPG_EMAIL${NC}"
        KEY_ID="N/A"
        FINGERPRINT="N/A"
    fi
else
    echo -e "${YELLOW}GPG not available, skipping key export${NC}"
    KEY_ID="N/A"
    FINGERPRINT="N/A"
fi

# Create verification instructions
echo ""
echo "Creating verification instructions..."

cat > "$PACKAGE_NAME/VERIFICATION_INSTRUCTIONS.md" << 'EOF'
# Verification Instructions

This package contains AI conversation ledger entries with cryptographic verification.

## Quick Verification

```bash
# 1. Verify GPG signatures
gpg --import public_key.asc
for file in *.yml *.yaml; do
    if [ -f "${file}.asc" ]; then
        echo "Verifying: $file"
        gpg --verify "${file}.asc" "$file"
    fi
done

# 2. Verify blockchain timestamps (requires opentimestamps-client)
pip3 install opentimestamps-client
for file in *.ots; do
    echo "Verifying: $file"
    ots verify "$file"
done
```

## Detailed Verification Steps

### 1. Verify GPG Signatures

Signatures prove the ledger was created by the keyholder and has not been altered.

**Import the public key:**
```bash
gpg --import public_key.asc
```

**Verify each ledger entry:**
```bash
gpg --verify ledger_entry.yml.asc ledger_entry.yml
```

**Successful output should show:**
```
gpg: Good signature from "Domenic Garza <domenic.garza@snhu.edu>"
```

**What this proves:**
- File was signed by the GPG key holder
- File has not been altered since signing
- Signature timestamp shows when file was signed

**Note:** You may see "WARNING: This key is not certified with a trusted signature!"  
This is normal for keys you haven't personally verified. The signature is still cryptographically valid.

### 2. Verify Blockchain Timestamps

Timestamps prove the document existed at a specific time via Bitcoin blockchain.

**Install OpenTimestamps client:**
```bash
pip3 install opentimestamps-client
```

**Verify each timestamp:**
```bash
ots verify ledger_entry.yml.ots
```

**Successful output should show:**
```
Success! Bitcoin block 850123 attests existence as of 2025-11-21 14:31:33 EST
```

**Independent verification:**
1. Note the Bitcoin block number from output
2. Visit: https://blockstream.info/block/[BLOCK_NUMBER]
3. Confirm the block timestamp matches the claim

**What this proves:**
- Document existed at or before the block timestamp
- Document has not been altered since timestamp
- Timestamp is anchored in immutable Bitcoin blockchain

### 3. Verify Git Repository History (if applicable)

**Clone the repository:**
```bash
EOF

echo "git clone $REPO_URL" >> "$PACKAGE_NAME/VERIFICATION_INSTRUCTIONS.md"

cat >> "$PACKAGE_NAME/VERIFICATION_INSTRUCTIONS.md" << 'EOF'
cd [repository-name]
```

**View signed commits:**
```bash
git log --show-signature
```

**What this proves:**
- GitHub independently recorded commit timestamps
- Commits were signed with same GPG key
- Development history shows chronological progression

### 4. Verify Share URLs

**For each ledger entry:**
1. Find the `share_url` field in the YAML
2. Access the URL in your browser
3. Compare the AI conversation content with the ledger summary
4. Note: Some URLs may require authentication

**What this proves:**
- Actual AI conversations exist on provider platforms
- Ledger entries correspond to real conversations
- Provider timestamps corroborate ledger timestamps

### 5. Verify Hash Chain Integrity

**Check chronological chain:**
For each entry, verify:
- `previous_entry_hash` field matches the `content_hash` of the previous entry
- Chain forms an unbroken sequence

**What this proves:**
- Entries form tamper-evident chain
- Entries created in chronological order
- Chain cannot be altered retroactively without detection

## Verification Summary

If all verifications pass:

✅ Files signed by authentic GPG key  
✅ Files timestamped to Bitcoin blockchain at claimed dates  
✅ Git history corroborates timestamps  
✅ Share URLs link to actual AI conversations  
✅ Hash chain proves chronological integrity

**This provides strong evidence that:**
1. Documents created at or before claimed times
2. Documents not altered since creation
3. Documents created by GPG key holder
4. AI conversations actually occurred as documented

## Key Information

EOF

echo "- **GPG Key ID:** $KEY_ID" >> "$PACKAGE_NAME/VERIFICATION_INSTRUCTIONS.md"
echo "- **Fingerprint:** $FINGERPRINT" >> "$PACKAGE_NAME/VERIFICATION_INSTRUCTIONS.md"
echo "- **Email:** $GPG_EMAIL" >> "$PACKAGE_NAME/VERIFICATION_INSTRUCTIONS.md"
if [ "$REPO_URL" != "N/A" ]; then
    echo "- **Repository:** $REPO_URL" >> "$PACKAGE_NAME/VERIFICATION_INSTRUCTIONS.md"
fi

cat >> "$PACKAGE_NAME/VERIFICATION_INSTRUCTIONS.md" << 'EOF'

## Questions or Issues?

If verification fails or you have questions:
1. Check that you've imported the correct public key
2. Ensure you have the latest version of GPG and OpenTimestamps
3. Verify you're using the correct ledger file (not a modified copy)
4. Contact the ledger maintainer for assistance

## Legal Value

These verification methods provide cryptographic proof of:
- **Authentication:** Files created by specific person (GPG signature)
- **Integrity:** Files not altered (GPG + hash chain)
- **Timestamp:** Files existed at specific time (blockchain + git)
- **Source:** AI conversations verifiable (share URLs)

However, they do not automatically make the ledger court-admissible.  
For legal use, human testimony is still required to establish:
- Context and purpose of the ledger
- Regular business practice of maintaining records
- Reliability of the verification system
- Accuracy of the ledger content

Consult with qualified legal counsel for specific legal matters.

---

**Package Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ)  
**For:** AI Conversation Ledger Verification  
**Reference:** Appendix C - Legal Standards for AI Conversation Logs
EOF

# Create SHA256 manifest
echo ""
echo "Creating cryptographic manifest..."
find "$PACKAGE_NAME" -type f ! -name "SHA256SUMS*" -exec sha256sum {} \; | sort > "$PACKAGE_NAME/SHA256SUMS"

# Sign the manifest if GPG available
if command -v gpg &> /dev/null && [ "$KEY_ID" != "N/A" ]; then
    if gpg --clearsign "$PACKAGE_NAME/SHA256SUMS" 2>&1; then
        echo -e "${GREEN}✓ Manifest signed${NC}"
    fi
fi

# Create archive
echo ""
echo "Creating archive..."
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"
ARCHIVE_SIZE=$(ls -lh "${PACKAGE_NAME}.tar.gz" | awk '{print $5}')

# Calculate archive hash
ARCHIVE_HASH=$(sha256sum "${PACKAGE_NAME}.tar.gz" | awk '{print $1}')

# Timestamp the package if OpenTimestamps available
if command -v ots &> /dev/null; then
    echo ""
    echo "Timestamping verification package..."
    ots stamp "${PACKAGE_NAME}.tar.gz"
    echo -e "${GREEN}✓ Package timestamped${NC}"
    echo "  Upgrade in ~1 hour with: ots upgrade ${PACKAGE_NAME}.tar.gz.ots"
fi

# Print summary
echo ""
echo -e "${GREEN}✓ Verification package created successfully!${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Package: ${PACKAGE_NAME}.tar.gz"
echo "  Size: $ARCHIVE_SIZE"
echo "  Hash: $ARCHIVE_HASH"
echo "  Files: $FILE_COUNT ledger entries"
if [ "$KEY_ID" != "N/A" ]; then
    echo "  GPG Key: $KEY_ID"
fi
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Package contents:"
echo "  - Ledger files (.yml/.yaml)"
echo "  - GPG signatures (.asc)"
echo "  - OpenTimestamps proofs (.ots)"
echo "  - Public GPG key (public_key.asc)"
echo "  - Verification instructions (VERIFICATION_INSTRUCTIONS.md)"
echo "  - Signed SHA256 manifest (SHA256SUMS.asc)"
echo ""
echo "To distribute:"
echo "  1. Share: ${PACKAGE_NAME}.tar.gz"
if [ -f "${PACKAGE_NAME}.tar.gz.ots" ]; then
    echo "  2. Share: ${PACKAGE_NAME}.tar.gz.ots (after ~1 hour)"
fi
echo ""
echo "Recipients can verify:"
echo "  tar -xzf ${PACKAGE_NAME}.tar.gz"
echo "  cd ${PACKAGE_NAME}"
echo "  cat VERIFICATION_INSTRUCTIONS.md"
