#!/bin/bash
# Create Cryptographic Proof Chain for Patent Filing
# 
# This script establishes an immutable proof chain for your USPTO patent filing
# using Git commits, GPG signatures, and OpenTimestamps (Bitcoin blockchain proof)
#
# Usage: ./create-proof-chain.sh [application_number]
# Example: ./create-proof-chain.sh 63/123456

set -e

# Configuration
APPLICATION_NUMBER="${1}"
FILING_DATE=$(date +%Y-%m-%d)

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PATENT_DIR="$REPO_ROOT/legal/patents"
PROVISIONAL_DIR="$PATENT_DIR/provisional"
RECEIPTS_DIR="$PATENT_DIR/receipts"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

function success() { echo -e "${GREEN}✓ $1${NC}"; }
function info() { echo -e "${CYAN}ℹ $1${NC}"; }
function warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
function error() { echo -e "${RED}✗ $1${NC}"; }
function header() { echo -e "\n${MAGENTA}=== $1 ===${NC}"; }

# Calculate future date (handles both GNU and BSD date)
function add_months_to_date() {
    local base_date="$1"
    local months="$2"
    
    # Try GNU date first (Linux)
    if date -d "$base_date + $months months" +%Y-%m-%d 2>/dev/null; then
        return
    fi
    
    # Try BSD date (macOS)
    if date -v +${months}m -j -f "%Y-%m-%d" "$base_date" +%Y-%m-%d 2>/dev/null; then
        return
    fi
    
    # Fallback
    echo "[Filing Date + $months months]"
}

header "Cryptographic Proof Chain Creation"

# Validate application number
if [ -z "$APPLICATION_NUMBER" ]; then
    error "Application number required"
    echo ""
    echo "Usage: $0 [application_number]"
    echo "Example: $0 63/123456"
    echo ""
    exit 1
fi

info "Application Number: $APPLICATION_NUMBER"
info "Filing Date: $FILING_DATE"
info "Repository: $REPO_ROOT"
echo ""

# Check if we're in a git repository
cd "$REPO_ROOT"
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    error "Not in a git repository"
    exit 1
fi

# Step 1: Check for required files
header "Step 1: Verify Files"

FILES_TO_ADD=()

# Check for provisional application PDFs
if ls "$PROVISIONAL_DIR"/*.pdf 1> /dev/null 2>&1; then
    for file in "$PROVISIONAL_DIR"/*.pdf; do
        success "Found: $file"
        FILES_TO_ADD+=("$file")
    done
else
    warning "No PDF files found in $PROVISIONAL_DIR"
fi

# Check for USPTO receipt
if ls "$RECEIPTS_DIR"/USPTO_Receipt*.pdf 1> /dev/null 2>&1; then
    for file in "$RECEIPTS_DIR"/USPTO_Receipt*.pdf; do
        success "Found: $file"
        FILES_TO_ADD+=("$file")
    done
else
    warning "No USPTO receipt found in $RECEIPTS_DIR"
fi

# Check for micro-entity certification
if ls "$RECEIPTS_DIR"/MICRO_ENTITY*.pdf 1> /dev/null 2>&1 || ls "$RECEIPTS_DIR"/SB15A*.pdf 1> /dev/null 2>&1; then
    for file in "$RECEIPTS_DIR"/MICRO_ENTITY*.pdf "$RECEIPTS_DIR"/SB15A*.pdf; do
        if [ -f "$file" ]; then
            success "Found: $file"
            FILES_TO_ADD+=("$file")
        fi
    done
else
    warning "No micro-entity certification found in $RECEIPTS_DIR"
fi

if [ ${#FILES_TO_ADD[@]} -eq 0 ]; then
    error "No patent files found to add to proof chain"
    echo ""
    info "Make sure you have:"
    echo "  - Provisional application PDF in: $PROVISIONAL_DIR"
    echo "  - USPTO filing receipt in: $RECEIPTS_DIR"
    echo "  - Micro-entity certification in: $RECEIPTS_DIR"
    exit 1
fi

# Step 2: Git add files
header "Step 2: Stage Files in Git"

for file in "${FILES_TO_ADD[@]}"; do
    git add "$file"
    success "Staged: $file"
done

# Also stage the guide and scripts
git add "$PATENT_DIR/USPTO_FILING_GUIDE.md" 2>/dev/null || true
git add "$PATENT_DIR"/*.sh 2>/dev/null || true
git add "$PATENT_DIR"/*.ps1 2>/dev/null || true

# Step 3: Create GPG-signed commit
header "Step 3: Create GPG-Signed Commit"

COMMIT_MESSAGE="PATENT PENDING: Provisional $APPLICATION_NUMBER filed $FILING_DATE – micro-entity"

info "Commit message: $COMMIT_MESSAGE"
echo ""

# Check if GPG is configured
if git config --get user.signingkey > /dev/null 2>&1; then
    info "GPG signing key configured"
    
    # Try to create a signed commit
    if git commit -S -m "$COMMIT_MESSAGE"; then
        success "Created GPG-signed commit"
    else
        warning "GPG signing failed, creating unsigned commit"
        git commit -m "$COMMIT_MESSAGE"
    fi
else
    warning "No GPG signing key configured"
    info "To enable GPG signing:"
    echo "  1. Generate a GPG key: gpg --full-generate-key"
    echo "  2. List keys: gpg --list-secret-keys --keyid-format=long"
    echo "  3. Configure git: git config user.signingkey [KEY_ID]"
    echo "  4. Configure git: git config commit.gpgsign true"
    echo ""
    
    # Create unsigned commit
    git commit -m "$COMMIT_MESSAGE"
    warning "Created unsigned commit (consider enabling GPG signing)"
fi

# Step 4: Push to remote
header "Step 4: Push to Remote Repository"

if git remote get-url origin > /dev/null 2>&1; then
    info "Pushing to remote..."
    
    if git push; then
        success "Pushed to remote repository"
        
        # Get the commit hash
        COMMIT_HASH=$(git rev-parse HEAD)
        info "Commit hash: $COMMIT_HASH"
    else
        warning "Failed to push to remote. You can push manually later:"
        echo "  git push"
    fi
else
    warning "No remote repository configured"
fi

# Step 5: Create OpenTimestamps (if available)
header "Step 5: Create OpenTimestamps"

if command -v ots &> /dev/null; then
    success "Found ots command"
    echo ""
    
    for file in "${FILES_TO_ADD[@]}"; do
        if [ -f "$file" ]; then
            info "Creating OpenTimestamp for: $file"
            
            if ots stamp "$file"; then
                success "Created timestamp: ${file}.ots"
            else
                warning "Failed to create timestamp for: $file"
            fi
        fi
    done
    
    echo ""
    info "OpenTimestamps created. These can be verified against the Bitcoin blockchain."
    info "To upgrade timestamps later: ots upgrade [file].ots"
    info "To verify timestamps: ots verify [file].ots"
else
    warning "OpenTimestamps (ots) not found"
    info "To install OpenTimestamps:"
    echo "  - Python: pip install opentimestamps-client"
    echo "  - Download: https://github.com/opentimestamps/opentimestamps-client"
    echo ""
    info "OpenTimestamps provides Bitcoin blockchain proof of existence"
    info "This creates an independent, verifiable timestamp that cannot be altered"
fi

# Step 6: Create patent tracking document
header "Step 6: Create Patent Tracking Document"

TRACKING_FILE="$PATENT_DIR/PATENT_TRACKING.md"

cat > "$TRACKING_FILE" << EOF
# Patent Tracking Document

## Active Provisional Patents

### 1. Autonomous Charitable Revenue Distribution System

- **Application Number**: $APPLICATION_NUMBER
- **Filing Date**: $FILING_DATE
- **Status**: Patent Pending
- **Type**: Provisional Patent Application
- **Entity Status**: Micro-Entity
- **Filing Fee**: \$75

#### Details

- **Title**: Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Cryptographic Verification
- **Inventor**: [Your Name]
- **Assignee**: Strategickhaos DAO LLC

#### Important Dates

- **Filing Date**: $FILING_DATE
- **Expiration Date**: $(add_months_to_date "$FILING_DATE" 12)
- **Utility Patent Deadline**: $(add_months_to_date "$FILING_DATE" 11)

#### Documents

- Provisional Application: \`provisional/STRATEGICKHAOS_PROVISIONAL_${FILING_DATE}.pdf\`
- USPTO Receipt: \`receipts/USPTO_Receipt.pdf\`
- Micro-Entity Cert: \`receipts/MICRO_ENTITY_CERT.pdf\`

#### Proof Chain

- **Git Commit**: $(git rev-parse HEAD 2>/dev/null || echo "[commit hash]")
- **Git Signature**: $(git log -1 --format="%G?" HEAD 2>/dev/null | grep -q "G" && echo "GPG Signed" || echo "Unsigned")
- **OpenTimestamps**: $(ls "$PROVISIONAL_DIR"/*.ots 2>/dev/null | wc -l | xargs) file(s) stamped

#### Next Steps

- [ ] Continue product development and testing
- [ ] Document improvements and iterations
- [ ] Consider international protection (PCT)
- [ ] Begin utility patent preparation (Month 6-9)
- [ ] File utility patent (by Month 11)

#### Notes

[Add any additional notes about the patent here]

---

## Patent Pending Statement

**Use this statement in all materials:**

> **Strategickhaos DAO LLC – Patent Pending (U.S. Provisional Application $APPLICATION_NUMBER)**

---

**Last Updated**: $(date +%Y-%m-%d)  
**Tracking Version**: 1.0
EOF

success "Created patent tracking document: $TRACKING_FILE"

# Add and commit the tracking document
git add "$TRACKING_FILE"
git commit -m "Add patent tracking document for $APPLICATION_NUMBER" 2>/dev/null || true

# Step 7: Summary
header "Proof Chain Complete"
echo ""
success "Successfully established proof chain for patent filing"
echo ""
info "What was created:"
echo "  ✓ Git commits with patent documents"
echo "  ✓ $(git log -1 --format="%G?" HEAD 2>/dev/null | grep -q "G" && echo "GPG-signed commit" || echo "Unsigned commit")"
echo "  ✓ Remote backup (if pushed)"
echo "  ✓ OpenTimestamps (if available): $(ls "$PROVISIONAL_DIR"/*.ots "$RECEIPTS_DIR"/*.ots 2>/dev/null | wc -l | xargs) files"
echo "  ✓ Patent tracking document"
echo ""
info "You can now legally state:"
echo ""
echo "    Patent Pending (U.S. Provisional Application $APPLICATION_NUMBER)"
echo ""
warning "IMPORTANT REMINDERS:"
echo "  1. File utility patent within 12 months (by $(add_months_to_date "$FILING_DATE" 12))"
echo "  2. Continue documenting improvements and iterations"
echo "  3. Keep all communications about the patent confidential or under NDA"
echo "  4. Review patent tracking document regularly: $TRACKING_FILE"
echo ""
success "Proof chain established successfully!"
