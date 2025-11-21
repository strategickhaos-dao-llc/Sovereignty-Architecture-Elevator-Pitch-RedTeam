#!/bin/bash
#
# Complete Workflow Test for PsycheVille
# Tests the entire system from log generation to report creation
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    PsycheVille Complete Workflow Test                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Generate sample logs
echo -e "${BLUE}[1/4]${NC} Generating sample logs..."
python3 "$SCRIPT_DIR/test_logging.py" > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Sample logs generated"
echo ""

# Step 2: Test the PsycheVille logger module
echo -e "${BLUE}[2/4]${NC} Testing PsycheVille logger module..."
python3 "$SCRIPT_DIR/psycheville_logger.py" > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Logger module working"
echo ""

# Step 3: Run reflection worker
echo -e "${BLUE}[3/4]${NC} Running reflection worker..."
python3 "$SCRIPT_DIR/test_reflection_standalone.py" > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Reflection completed successfully"
echo ""

# Step 4: Verify report generation
echo -e "${BLUE}[4/4]${NC} Verifying report generation..."
REPORT_DIR="$SCRIPT_DIR/obsidian_vault/PsycheVille/Departments/Tools_Refinery"
REPORT_COUNT=$(find "$REPORT_DIR" -name "reflection_*.md" 2>/dev/null | wc -l)

if [ "$REPORT_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Found $REPORT_COUNT reflection report(s)"
    echo ""
    echo -e "${YELLOW}Latest Report:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    LATEST_REPORT=$(find "$REPORT_DIR" -name "reflection_*.md" -type f | sort -r | head -1)
    cat "$LATEST_REPORT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo -e "${YELLOW}⚠${NC} No reports found"
    exit 1
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           All Tests Passed Successfully! ✓              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "PsycheVille is ready for deployment!"
echo ""
echo "Next steps:"
echo "  1. Deploy: ./psycheville/deploy-psycheville.sh deploy"
echo "  2. Check status: ./psycheville/deploy-psycheville.sh status"
echo "  3. View reports: cat psycheville/obsidian_vault/PsycheVille/Departments/Tools_Refinery/reflection_*.md"
echo ""
