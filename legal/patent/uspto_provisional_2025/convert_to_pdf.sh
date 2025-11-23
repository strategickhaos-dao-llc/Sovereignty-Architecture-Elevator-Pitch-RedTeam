#!/bin/bash
# USPTO Patent Document Conversion Script
# Converts markdown documents to PDF for USPTO filing

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "USPTO Patent Document Converter"
echo "=========================================="
echo ""

# Check for required tools
echo "Checking for conversion tools..."

HAS_PANDOC=false
HAS_MARKDOWN_PDF=false
HAS_WKHTMLTOPDF=false

if command -v pandoc &> /dev/null; then
    HAS_PANDOC=true
    echo "✓ pandoc found: $(pandoc --version | head -n1)"
fi

if command -v markdown-pdf &> /dev/null; then
    HAS_MARKDOWN_PDF=true
    echo "✓ markdown-pdf found"
fi

if command -v wkhtmltopdf &> /dev/null; then
    HAS_WKHTMLTOPDF=true
    echo "✓ wkhtmltopdf found: $(wkhtmltopdf --version | head -n1)"
fi

echo ""

# Determine which tool to use
TOOL=""
if $HAS_PANDOC; then
    TOOL="pandoc"
    echo "Using: pandoc (recommended)"
elif $HAS_WKHTMLTOPDF; then
    TOOL="wkhtmltopdf"
    echo "Using: wkhtmltopdf"
elif $HAS_MARKDOWN_PDF; then
    TOOL="markdown-pdf"
    echo "Using: markdown-pdf (npm)"
else
    echo "❌ ERROR: No PDF conversion tool found!"
    echo ""
    echo "Please install one of the following:"
    echo ""
    echo "Option 1 - Pandoc (recommended):"
    echo "  Ubuntu/Debian: sudo apt-get install pandoc texlive-latex-base"
    echo "  macOS:         brew install pandoc basictex"
    echo "  Windows:       Download from https://pandoc.org/installing.html"
    echo ""
    echo "Option 2 - wkhtmltopdf:"
    echo "  Ubuntu/Debian: sudo apt-get install wkhtmltopdf"
    echo "  macOS:         brew install wkhtmltopdf"
    echo "  Windows:       Download from https://wkhtmltopdf.org/downloads.html"
    echo ""
    echo "Option 3 - markdown-pdf (npm):"
    echo "  npm install -g markdown-pdf"
    echo ""
    exit 1
fi

echo ""
echo "=========================================="
echo "Converting Documents to PDF"
echo "=========================================="
echo ""

# Function to convert with pandoc
convert_with_pandoc() {
    local input=$1
    local output=$2
    echo "Converting: $input → $output"
    pandoc "$input" \
        -o "$output" \
        --pdf-engine=pdflatex \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        --toc \
        --toc-depth=2 \
        2>&1 | grep -v "Missing character" || true
}

# Function to convert with wkhtmltopdf
convert_with_wkhtmltopdf() {
    local input=$1
    local output=$2
    echo "Converting: $input → $output"
    
    # First convert markdown to HTML
    local html_file="${input%.md}.html"
    
    # Simple markdown to HTML conversion
    cat > "$html_file" << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>USPTO Patent Document</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 1in; font-size: 11pt; line-height: 1.5; }
        h1 { font-size: 18pt; font-weight: bold; margin-top: 20pt; }
        h2 { font-size: 14pt; font-weight: bold; margin-top: 15pt; }
        h3 { font-size: 12pt; font-weight: bold; margin-top: 10pt; }
        code { background: #f4f4f4; padding: 2px 4px; font-family: monospace; }
        pre { background: #f4f4f4; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
HTMLEOF
    
    # Convert markdown to HTML body (simple conversion)
    sed -e 's/^# \(.*\)/<h1>\1<\/h1>/' \
        -e 's/^## \(.*\)/<h2>\1<\/h2>/' \
        -e 's/^### \(.*\)/<h3>\1<\/h3>/' \
        -e 's/^\* \(.*\)/<li>\1<\/li>/' \
        -e 's/^- \(.*\)/<li>\1<\/li>/' \
        -e 's/\*\*\(.*\)\*\*/<strong>\1<\/strong>/g' \
        -e 's/\*\(.*\)\*/<em>\1<\/em>/g' \
        -e 's/`\([^`]*\)`/<code>\1<\/code>/g' \
        "$input" >> "$html_file"
    
    echo "</body></html>" >> "$html_file"
    
    # Convert HTML to PDF
    wkhtmltopdf \
        --page-size Letter \
        --margin-top 1in \
        --margin-bottom 1in \
        --margin-left 1in \
        --margin-right 1in \
        "$html_file" "$output" 2>&1 | grep -v "Exit with code" || true
    
    # Clean up temporary HTML
    rm -f "$html_file"
}

# Function to convert with markdown-pdf
convert_with_markdown_pdf() {
    local input=$1
    local output=$2
    echo "Converting: $input → $output"
    markdown-pdf "$input" -o "$output"
}

# Convert the two main documents
SPEC_MD="PROVISIONAL_PATENT_SPECIFICATION.md"
SPEC_PDF="PROVISIONAL_PATENT_SPECIFICATION.pdf"

CERT_MD="MICRO_ENTITY_CERTIFICATION_SB15A.md"
CERT_PDF="MICRO_ENTITY_CERTIFICATION_SB15A.pdf"

if [ ! -f "$SPEC_MD" ]; then
    echo "❌ ERROR: $SPEC_MD not found!"
    exit 1
fi

if [ ! -f "$CERT_MD" ]; then
    echo "❌ ERROR: $CERT_MD not found!"
    exit 1
fi

# Convert documents based on available tool
case "$TOOL" in
    pandoc)
        convert_with_pandoc "$SPEC_MD" "$SPEC_PDF"
        convert_with_pandoc "$CERT_MD" "$CERT_PDF"
        ;;
    wkhtmltopdf)
        convert_with_wkhtmltopdf "$SPEC_MD" "$SPEC_PDF"
        convert_with_wkhtmltopdf "$CERT_MD" "$CERT_PDF"
        ;;
    markdown-pdf)
        convert_with_markdown_pdf "$SPEC_MD" "$SPEC_PDF"
        convert_with_markdown_pdf "$CERT_MD" "$CERT_PDF"
        ;;
esac

echo ""
echo "=========================================="
echo "Conversion Complete!"
echo "=========================================="
echo ""
echo "Generated files:"
echo "  1. $SPEC_PDF (~200-300 KB)"
echo "  2. $CERT_PDF (~50-100 KB)"
echo ""
echo "Next steps:"
echo "  1. Review the PDFs to ensure formatting is correct"
echo "  2. Go to: https://patentcenter.uspto.gov/applications/provisional"
echo "  3. Upload both PDF files"
echo "  4. Complete the filing process"
echo ""
echo "See USPTO_FILING_INSTRUCTIONS.md for detailed filing guide."
echo ""

# Check file sizes
if [ -f "$SPEC_PDF" ]; then
    SIZE=$(ls -lh "$SPEC_PDF" | awk '{print $5}')
    echo "✓ Specification PDF: $SIZE"
fi

if [ -f "$CERT_PDF" ]; then
    SIZE=$(ls -lh "$CERT_PDF" | awk '{print $5}')
    echo "✓ Certification PDF: $SIZE"
fi

echo ""
echo "Ready to file! Good luck! 🚀"
echo ""
