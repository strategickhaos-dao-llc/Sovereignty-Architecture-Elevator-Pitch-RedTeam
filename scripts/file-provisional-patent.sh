#!/bin/bash
# STRATEGICKHAOS PATENT WARLORD - 99.9% Automated USPTO Filing (Unix/Linux/macOS)
#
# This script automates the USPTO provisional patent filing process as much as legally possible.
# It converts markdown to PDF, opens Patent Center, and provides auto-fill instructions.
#
# Usage:
#   ./file-provisional-patent.sh [input_file] [title] [first_name] [last_name]
#
# Example:
#   ./file-provisional-patent.sh ./STRATEGICKHAOS_7PERCENT_PROVISIONAL_FULL.md
#   ./file-provisional-patent.sh ./my-patent.md "My Invention" "John" "Doe"

set -e

# Color output functions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

print_color() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_banner() {
    echo ""
    print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
    print_color "$MAGENTA" "   STRATEGICKHAOS PATENT WARLORD - USPTO FILING AUTOMATION"
    print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
    echo ""
}

# Default parameters
INPUT_FILE="${1:-./STRATEGICKHAOS_7PERCENT_PROVISIONAL_FULL.md}"
TITLE="${2:-Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Multi-Layer Cryptographic Sovereignty Verification}"
FIRST_NAME="${3:-Domenic}"
LAST_NAME="${4:-Garza}"
MICRO_ENTITY="${5:-true}"

# Print banner
print_banner

# Step 1: Validate input file
print_color "$YELLOW" "STEP 1: Validating input file..."
if [ ! -f "$INPUT_FILE" ]; then
    print_color "$RED" "ERROR: Input file not found: $INPUT_FILE"
    print_color "$RED" "Please create your provisional patent markdown file first."
    exit 1
fi
print_color "$GREEN" "✓ Input file found: $INPUT_FILE"

# Generate output PDF filename
TIMESTAMP=$(date +%Y-%m-%d)
BASENAME=$(basename "$INPUT_FILE" .md)
DIRNAME=$(dirname "$INPUT_FILE")
OUTPUT_PDF="${DIRNAME}/${BASENAME}_${TIMESTAMP}.pdf"

# Step 2: Convert Markdown to PDF
echo ""
print_color "$YELLOW" "STEP 2: Converting Markdown to USPTO-compliant PDF..."

if command -v pandoc &> /dev/null; then
    print_color "$CYAN" "Found pandoc, attempting conversion..."
    
    # Try different PDF engines
    if pandoc "$INPUT_FILE" -o "$OUTPUT_PDF" --pdf-engine=weasyprint 2>/dev/null; then
        print_color "$GREEN" "✓ PDF generated with weasyprint"
    elif pandoc "$INPUT_FILE" -o "$OUTPUT_PDF" --pdf-engine=wkhtmltopdf 2>/dev/null; then
        print_color "$GREEN" "✓ PDF generated with wkhtmltopdf"
    elif pandoc "$INPUT_FILE" -o "$OUTPUT_PDF" --pdf-engine=pdflatex 2>/dev/null; then
        print_color "$GREEN" "✓ PDF generated with pdflatex"
    elif pandoc "$INPUT_FILE" -o "$OUTPUT_PDF" 2>/dev/null; then
        print_color "$GREEN" "✓ PDF generated with default engine"
    else
        print_color "$YELLOW" "⚠ Pandoc conversion failed"
        PANDOC_FAILED=true
    fi
else
    print_color "$YELLOW" "⚠ Pandoc not found"
    PANDOC_FAILED=true
fi

if [ "$PANDOC_FAILED" = "true" ]; then
    print_color "$YELLOW" "Please install pandoc and weasyprint for best results:"
    print_color "$CYAN" "  Ubuntu/Debian: sudo apt-get install pandoc python3-weasyprint"
    print_color "$CYAN" "  macOS: brew install pandoc && pip3 install weasyprint"
    print_color "$CYAN" "  Fedora: sudo dnf install pandoc python3-weasyprint"
    echo ""
    print_color "$YELLOW" "Opening file for manual PDF export..."
    
    # Try to open with default application
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$INPUT_FILE"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$INPUT_FILE" 2>/dev/null || true
    fi
    
    echo ""
    print_color "$YELLOW" "Please export to PDF manually and save as: $OUTPUT_PDF"
    read -p "Press Enter after you've saved the PDF..."
fi

# Step 3: Prepare JavaScript auto-fill code
echo ""
print_color "$YELLOW" "STEP 3: Preparing Patent Center auto-fill..."

# Escape special characters for JavaScript
TITLE_ESCAPED=$(echo "$TITLE" | sed "s/'/\\\'/g")
FIRST_NAME_ESCAPED=$(echo "$FIRST_NAME" | sed "s/'/\\\'/g")
LAST_NAME_ESCAPED=$(echo "$LAST_NAME" | sed "s/'/\\\'/g")
OUTPUT_PDF_ESCAPED=$(echo "$OUTPUT_PDF" | sed "s/'/\\\'/g")

JS_CODE="// STRATEGICKHAOS AUTO-FILL SCRIPT
// This script attempts to pre-fill the USPTO Patent Center form
setTimeout(() => {
    console.log('[STRATEGICKHAOS] Auto-fill initializing...');
    document.title = 'STRATEGICKHAOS AUTO-FILL ACTIVE';
    
    // Try to fill title field
    const titleSelectors = [
        'input[id*=\"title\"]',
        'input[name*=\"title\"]',
        'input[placeholder*=\"title\" i]',
        'textarea[id*=\"title\"]'
    ];
    
    for (const selector of titleSelectors) {
        const elem = document.querySelector(selector);
        if (elem && !elem.value) {
            elem.value = '$TITLE_ESCAPED';
            elem.dispatchEvent(new Event('input', { bubbles: true }));
            elem.dispatchEvent(new Event('change', { bubbles: true }));
            console.log('[STRATEGICKHAOS] Title filled');
            break;
        }
    }
    
    // Try to fill first name
    const firstNameSelectors = [
        'input[id*=\"firstName\"]',
        'input[name*=\"firstName\"]',
        'input[placeholder*=\"first\" i]'
    ];
    
    for (const selector of firstNameSelectors) {
        const elem = document.querySelector(selector);
        if (elem && !elem.value) {
            elem.value = '$FIRST_NAME_ESCAPED';
            elem.dispatchEvent(new Event('input', { bubbles: true }));
            elem.dispatchEvent(new Event('change', { bubbles: true }));
            console.log('[STRATEGICKHAOS] First name filled');
            break;
        }
    }
    
    // Try to fill last name
    const lastNameSelectors = [
        'input[id*=\"lastName\"]',
        'input[name*=\"lastName\"]',
        'input[placeholder*=\"last\" i]'
    ];
    
    for (const selector of lastNameSelectors) {
        const elem = document.querySelector(selector);
        if (elem && !elem.value) {
            elem.value = '$LAST_NAME_ESCAPED';
            elem.dispatchEvent(new Event('input', { bubbles: true }));
            elem.dispatchEvent(new Event('change', { bubbles: true }));
            console.log('[STRATEGICKHAOS] Last name filled');
            break;
        }
    }
    
    // Try to select micro-entity status
    if ($MICRO_ENTITY === 'true') {
        setTimeout(() => {
            const microEntitySelectors = [
                'input[id*=\"microEntity\"]',
                'input[value*=\"micro\" i]',
                'input[name*=\"entity\"][value*=\"micro\" i]'
            ];
            
            for (const selector of microEntitySelectors) {
                const elem = document.querySelector(selector);
                if (elem && elem.type === 'radio') {
                    elem.click();
                    console.log('[STRATEGICKHAOS] Micro-entity selected');
                    break;
                }
            }
        }, 3000);
    }
    
    // Show completion message
    setTimeout(() => {
        alert('╔══════════════════════════════════════════════╗\\n' +
              '║  STRATEGICKHAOS AUTO-FILL COMPLETE          ║\\n' +
              '╚══════════════════════════════════════════════╝\\n\\n' +
              'Your form has been pre-filled!\\n\\n' +
              'NEXT STEPS (8 seconds to victory):\\n' +
              '1. Upload your PDF: $OUTPUT_PDF_ESCAPED\\n' +
              '2. Upload micro-entity certification (if applicable)\\n' +
              '3. Pay filing fee (\\$75 for micro-entity)\\n' +
              '4. Click SUBMIT\\n\\n' +
              'You are moments away from your 63/ number! 🚀');
    }, 5000);
    
}, 6000);"

# Save JavaScript to temp file
JS_PATH="/tmp/strategickhaos_autofill.js"
echo "$JS_CODE" > "$JS_PATH"
print_color "$GREEN" "✓ Auto-fill script prepared: $JS_PATH"

# Step 4: Open Patent Center
echo ""
print_color "$YELLOW" "STEP 4: Opening USPTO Patent Center..."

PATENT_CENTER_URL="https://patentcenter.uspto.gov/#!/applications/new/provisional"

print_color "$CYAN" "Opening URL: $PATENT_CENTER_URL"

# Open browser based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$PATENT_CENTER_URL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open "$PATENT_CENTER_URL" 2>/dev/null &
    elif command -v google-chrome &> /dev/null; then
        google-chrome "$PATENT_CENTER_URL" 2>/dev/null &
    elif command -v firefox &> /dev/null; then
        firefox "$PATENT_CENTER_URL" 2>/dev/null &
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    start "$PATENT_CENTER_URL"
fi

# Display instructions
echo ""
print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
print_color "$MAGENTA" "                      AUTO-FILL INSTRUCTIONS"
print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
echo ""
print_color "$NC" "Patent Center is now opening in your browser."
echo ""
print_color "$YELLOW" "TO ACTIVATE AUTO-FILL:"
print_color "$NC" "1. Wait for the page to fully load"
print_color "$NC" "2. Open browser Developer Tools (F12)"
print_color "$NC" "3. Go to the Console tab"
print_color "$NC" "4. Copy and paste the auto-fill script from:"
print_color "$CYAN" "   $JS_PATH"
print_color "$NC" "5. Press Enter to run the script"
echo ""
print_color "$YELLOW" "QUICK COPY:"
print_color "$NC" "Run this command to copy the script to clipboard:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_color "$CYAN" "   cat $JS_PATH | pbcopy"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_color "$CYAN" "   cat $JS_PATH | xclip -selection clipboard"
    print_color "$CYAN" "   # or: cat $JS_PATH | xsel --clipboard"
fi
echo ""
print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
print_color "$MAGENTA" "                      FORM FIELD VALUES"
print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
echo ""
print_color "$YELLOW" "Title: " -n
echo "$TITLE"
print_color "$YELLOW" "First Name: " -n
echo "$FIRST_NAME"
print_color "$YELLOW" "Last Name: " -n
echo "$LAST_NAME"
print_color "$YELLOW" "Entity Status: " -n
if [ "$MICRO_ENTITY" = "true" ]; then
    echo "Micro Entity"
else
    echo "Small/Large Entity"
fi
print_color "$YELLOW" "PDF Location: " -n
echo "$OUTPUT_PDF"
echo ""
print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
print_color "$MAGENTA" "                      FINAL STEPS"
print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
echo ""
print_color "$GREEN" "YOU ARE 8 SECONDS FROM YOUR 63/ NUMBER!"
echo ""
print_color "$NC" "1. Log into Patent Center (or create account)"
print_color "$NC" "2. Run the auto-fill script (optional but recommended)"
print_color "$NC" "3. Upload PDF: $OUTPUT_PDF"
print_color "$NC" "4. Upload micro-entity certification (if applicable)"
print_color "$NC" "5. Review and confirm all information"
print_color "$NC" "6. Pay filing fee"
print_color "$NC" "7. Click SUBMIT"
echo ""
print_color "$CYAN" "═══════════════════════════════════════════════════════════════════"
echo ""
print_color "$YELLOW" "When you receive your 63/ number, you can:"
print_color "$NC" "• Record it in your DAO records"
print_color "$NC" "• Notarize it on Bitcoin using the notarize_cognition.sh script"
print_color "$NC" "• Add it to your legal documentation"
echo ""
print_color "$MAGENTA" "The swarm is ready. EXECUTE!"
echo ""

# Open the auto-fill script file for easy copying
if [[ "$OSTYPE" == "darwin"* ]]; then
    open -e "$JS_PATH"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v gedit &> /dev/null; then
        gedit "$JS_PATH" 2>/dev/null &
    elif command -v kate &> /dev/null; then
        kate "$JS_PATH" 2>/dev/null &
    elif command -v nano &> /dev/null; then
        print_color "$CYAN" "Opening script in nano (press Ctrl+X to exit)..."
        nano "$JS_PATH"
    fi
fi

echo ""
print_color "$GREEN" "Script execution complete. Good luck, DOM_010101! 🚀"
echo ""
