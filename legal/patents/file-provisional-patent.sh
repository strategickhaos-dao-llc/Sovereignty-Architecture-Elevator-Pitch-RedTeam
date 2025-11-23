#!/bin/bash
# USPTO Provisional Patent Filing Automation Script (Bash)
# For Strategickhaos DAO LLC - Autonomous Charitable Revenue Distribution System
# 
# This script automates the preparation steps for filing a provisional patent application
# with the USPTO. It does NOT submit the application (that must be done manually via EFS-Web).
#
# Usage: ./file-provisional-patent.sh

set -e

# Configuration
INVENTOR_NAME="${INVENTOR_NAME:-Domenic Garza}"
PATENT_TITLE="Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Cryptographic Verification"
APPLICATION_DATE=$(date +%Y-%m-%d)

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PATENT_DIR="$REPO_ROOT/legal/patents"
PROVISIONAL_DIR="$PATENT_DIR/provisional"
RECEIPTS_DIR="$PATENT_DIR/receipts"
TEMPLATES_DIR="$PATENT_DIR/templates"

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

header "USPTO Provisional Patent Filing Preparation"
info "Inventor: $INVENTOR_NAME"
info "Title: $PATENT_TITLE"
info "Date: $APPLICATION_DATE"
echo ""

# Step 0: Check and create directories
header "Step 0: Directory Setup"
for dir in "$PROVISIONAL_DIR" "$RECEIPTS_DIR" "$TEMPLATES_DIR"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        success "Created directory: $dir"
    else
        info "Directory exists: $dir"
    fi
done

# Step 1: Download Micro-Entity Certification Form
header "Step 1: Micro-Entity Certification (SB/15A)"
MICRO_ENTITY_FORM_URL="https://www.uspto.gov/sites/default/files/documents/sb0015a.pdf"
MICRO_ENTITY_FORM_PATH="$RECEIPTS_DIR/SB15A_MICRO_ENTITY_FORM.pdf"

if [ ! -f "$MICRO_ENTITY_FORM_PATH" ]; then
    info "Opening micro-entity certification form in browser..."
    
    # Detect OS and open browser
    if command -v xdg-open &> /dev/null; then
        xdg-open "$MICRO_ENTITY_FORM_URL" 2>/dev/null || true
    elif command -v open &> /dev/null; then
        open "$MICRO_ENTITY_FORM_URL" 2>/dev/null || true
    else
        info "Please manually download from: $MICRO_ENTITY_FORM_URL"
    fi
    
    success "Opened micro-entity form in browser"
    warning "ACTION REQUIRED: Download and save the form as: $MICRO_ENTITY_FORM_PATH"
    warning "Fill in your name, sign, and date the form"
else
    info "Micro-entity form already exists: $MICRO_ENTITY_FORM_PATH"
fi

# Step 2: Check for provisional application document
header "Step 2: Provisional Application Document"
PROVISIONAL_APP_PATH="$PROVISIONAL_DIR/PROVISIONAL_PATENT_APPLICATION.md"
PROVISIONAL_PDF_PATH="$PROVISIONAL_DIR/STRATEGICKHAOS_PROVISIONAL_${APPLICATION_DATE}.pdf"

if [ ! -f "$PROVISIONAL_APP_PATH" ]; then
    warning "Provisional application not found at: $PROVISIONAL_APP_PATH"
    info "Creating template provisional application..."
    
    cat > "$PROVISIONAL_APP_PATH" << EOF
# $PATENT_TITLE

**Inventor**: $INVENTOR_NAME  
**Date**: $APPLICATION_DATE  
**Application Type**: Provisional Patent Application

## Field of the Invention

This invention relates to autonomous charitable revenue distribution systems that utilize artificial intelligence governance, distributed autonomous organization (DAO) architecture, and cryptographic verification mechanisms.

## Background

[Describe the problem your invention solves and the current state of the art]

## Summary of the Invention

[Provide a brief summary of your invention - what it does and how it's novel]

## Detailed Description

### System Architecture

[Describe the technical architecture of your system]

### Components

#### 1. DAO Governance Layer
[Describe the DAO structure and governance mechanisms]

#### 2. AI Decision Engine
[Describe how AI is used in the system]

#### 3. Charitable Distribution Mechanism
[Describe how charitable distributions work]

#### 4. Cryptographic Verification System
[Describe the cryptographic elements]

### Operation

[Describe how the system operates step-by-step]

### Novel Features

1. [List novel feature 1]
2. [List novel feature 2]
3. [List novel feature 3]

## Claims (for future utility patent)

[Optional: Draft preliminary claims]

## Figures

[Include system diagrams, flowcharts, or screenshots]

## Best Mode

[Describe your preferred implementation method]

## Advantages

[List the advantages of your invention over prior art]

---

**End of Provisional Patent Application**
EOF
    
    success "Created template at: $PROVISIONAL_APP_PATH"
    warning "ACTION REQUIRED: Edit the template with your invention details"
    
    # Open in default editor
    if command -v xdg-open &> /dev/null; then
        xdg-open "$PROVISIONAL_APP_PATH" 2>/dev/null || true
    elif command -v open &> /dev/null; then
        open "$PROVISIONAL_APP_PATH" 2>/dev/null || true
    fi
else
    info "Provisional application found: $PROVISIONAL_APP_PATH"
fi

# Step 3: Convert to PDF using available tools
header "Step 3: Convert to USPTO-Ready PDF"

if [ -f "$PROVISIONAL_APP_PATH" ]; then
    info "Checking for PDF conversion tools..."
    
    # Check for Pandoc
    if command -v pandoc &> /dev/null; then
        success "Found Pandoc - attempting conversion..."
        
        # Try with weasyprint first, fall back to other engines
        if pandoc "$PROVISIONAL_APP_PATH" -o "$PROVISIONAL_PDF_PATH" --pdf-engine=weasyprint -V geometry:margin=1in 2>/dev/null; then
            success "Created PDF using weasyprint: $PROVISIONAL_PDF_PATH"
        elif pandoc "$PROVISIONAL_APP_PATH" -o "$PROVISIONAL_PDF_PATH" -V geometry:margin=1in 2>/dev/null; then
            success "Created PDF: $PROVISIONAL_PDF_PATH"
        else
            warning "Pandoc conversion failed. Try manually:"
            info "pandoc $PROVISIONAL_APP_PATH -o $PROVISIONAL_PDF_PATH"
        fi
    else
        warning "Pandoc not found. Install from: https://pandoc.org/"
        info "Alternative: Open the markdown file in Word/Google Docs and export as PDF"
        info "  - Set page size to US Letter (8.5 x 11)"
        info "  - Set margins to 1 inch on all sides"
        info "  - Use 12-point font or larger"
        info "  - Save as: $PROVISIONAL_PDF_PATH"
    fi
fi

# Step 4: Open USPTO EFS-Web
header "Step 4: USPTO EFS-Web Filing"
EFS_WEB_URL="https://efs.uspto.gov/EFS-Web2/"

info "When you're ready to file, this script will open the USPTO EFS-Web portal"
echo ""
warning "Before proceeding, ensure you have:"
echo "  [1] Completed and signed micro-entity form (SB/15A)"
echo "  [2] Your provisional application as a PDF"
echo "  [3] USPTO.gov account credentials"
echo "  [4] Payment method ready (\$75 for micro-entity)"
echo ""

read -p "Open USPTO EFS-Web now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Detect OS and open browser
    if command -v xdg-open &> /dev/null; then
        xdg-open "$EFS_WEB_URL" 2>/dev/null || true
    elif command -v open &> /dev/null; then
        open "$EFS_WEB_URL" 2>/dev/null || true
    else
        info "Please manually open: $EFS_WEB_URL"
    fi
    
    success "Opened USPTO EFS-Web in browser"
    echo ""
    info "Follow these steps in EFS-Web:"
    echo "  1. Login or create account"
    echo "  2. Click 'New Application'"
    echo "  3. Select 'Provisional Application'"
    echo "  4. Select 'Micro Entity (SB/15A)'"
    echo "  5. Upload your micro-entity certification PDF"
    echo "  6. Enter inventor information:"
    echo "     - Name: $INVENTOR_NAME"
    echo "     - Address: [Your Wyoming DAO address]"
    echo "  7. Enter title: $PATENT_TITLE"
    echo "  8. Upload provisional application PDF: $PROVISIONAL_PDF_PATH"
    echo "  9. Validate submission"
    echo " 10. Pay \$75 filing fee"
    echo " 11. Submit application"
    echo " 12. Save confirmation and filing receipt"
else
    info "Skipped opening EFS-Web. You can open it manually: $EFS_WEB_URL"
fi

# Step 5: Post-filing instructions
header "Step 5: After Filing - Proof Chain Setup"
echo ""
warning "AFTER you receive your USPTO filing receipt:"
echo ""
info "1. Save your filing receipt as: $RECEIPTS_DIR/USPTO_Receipt.pdf"
info "2. Note your application number (format: 63/XXXXXX)"
echo ""
info "3. Run the proof chain script:"
echo "   $PATENT_DIR/create-proof-chain.sh 63/XXXXXX"
echo ""
info "Or manually:"
echo "   git add legal/patents/provisional/*.pdf"
echo "   git add legal/patents/receipts/*.pdf"
echo "   git commit -S -m 'PATENT PENDING: Provisional 63/XXXXXX filed $APPLICATION_DATE'"
echo "   git push"
echo ""
info "4. Create OpenTimestamps (if ots available):"
echo "   ots stamp $PROVISIONAL_PDF_PATH"
echo "   ots stamp $RECEIPTS_DIR/USPTO_Receipt.pdf"

# Step 6: Summary
header "Summary"
echo ""
success "Preparation complete!"
echo ""
info "Next Steps:"
echo "  1. Complete and sign micro-entity form if not done"
echo "  2. Review and finalize your provisional application"
echo "  3. Convert to PDF with proper formatting"
echo "  4. File via USPTO EFS-Web (https://efs.uspto.gov/EFS-Web2/)"
echo "  5. Save filing receipt when received"
echo "  6. Run proof chain script to establish cryptographic verification"
echo ""
info "Cost: \$75 (micro-entity filing fee)"
info "Time: 15-45 minutes to file"
info "Result: Patent Pending status + priority date"
echo ""
success "You will be able to state: 'Patent Pending (U.S. Provisional Application 63/XXXXXX)'"
echo ""
warning "IMPORTANT: File utility patent within 12 months to maintain priority!"
echo ""

# Open the guide
GUIDE_PATH="$PATENT_DIR/USPTO_FILING_GUIDE.md"
if [ -f "$GUIDE_PATH" ]; then
    info "Opening filing guide..."
    if command -v xdg-open &> /dev/null; then
        xdg-open "$GUIDE_PATH" 2>/dev/null || true
    elif command -v open &> /dev/null; then
        open "$GUIDE_PATH" 2>/dev/null || true
    fi
fi

echo -e "${GREEN}Script complete. Review the USPTO_FILING_GUIDE.md for detailed instructions.${NC}"
