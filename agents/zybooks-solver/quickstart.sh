#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# 🔥 ZYBOOKS QUICK START
# ═══════════════════════════════════════════════════════════════════
# Setup zyBooks ingestion protocol for StrategicKhaos swarm
# ═══════════════════════════════════════════════════════════════════

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔥 zyBooks Solver Agent - Quick Start${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

echo -e "\n${YELLOW}📁 Repository: ${NC}$REPO_ROOT"

# Create directory structure if not exists
echo -e "\n${YELLOW}📂 Creating directory structure...${NC}"
mkdir -p "$REPO_ROOT/training/zybooks/sections"
mkdir -p "$REPO_ROOT/training/zybooks/patterns"
mkdir -p "$REPO_ROOT/training/zybooks/archive"
echo -e "${GREEN}✅ Directories created${NC}"

# Install Python dependencies
echo -e "\n${YELLOW}📦 Installing dependencies...${NC}"
cd "$SCRIPT_DIR"
if command -v pip3 &> /dev/null; then
    pip3 install -q -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -q -r requirements.txt
else
    echo -e "${RED}❌ pip not found. Please install Python and pip.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Run tests
echo -e "\n${YELLOW}🧪 Running tests...${NC}"
if python3 test_zybooks.py > /tmp/zybooks_test_output.txt 2>&1; then
    echo -e "${GREEN}✅ All tests passed${NC}"
    # Show summary
    grep "ALL TESTS PASSED" /tmp/zybooks_test_output.txt || true
else
    echo -e "${RED}❌ Tests failed${NC}"
    cat /tmp/zybooks_test_output.txt
    exit 1
fi

# Create sample content
echo -e "\n${YELLOW}📝 Creating sample content...${NC}"
cat > "$REPO_ROOT/training/zybooks/sections/sample_1.5.txt" << 'EOF'
Section 1.5 - Statistical Measures Participation Activity

1) True or False: In a normal distribution, approximately 68% of data falls within one standard deviation of the mean.
True
False

2) What percentage of data in a normal distribution falls within two standard deviations of the mean?
a) 68%
b) 95%
c) 99.7%
d) 50%

3) True or False: The mean is always greater than the median.
True
False
EOF
echo -e "${GREEN}✅ Sample content created${NC}"

# Test with sample
echo -e "\n${YELLOW}🎯 Testing with sample content...${NC}"
echo -e "${BLUE}Output (VESSEL MODE):${NC}"
python3 main.py "$REPO_ROOT/training/zybooks/sections/sample_1.5.txt" --format vessel
echo ""

# Show usage
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🔥 Setup Complete! You're LOCKED IN!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}📋 Quick Commands:${NC}"
echo ""
echo -e "  ${BLUE}# Process from file${NC}"
echo -e "  python3 agents/zybooks-solver/main.py training/zybooks/PASTE_HERE.md"
echo ""
echo -e "  ${BLUE}# Process from clipboard (paste and press Ctrl+D)${NC}"
echo -e "  python3 agents/zybooks-solver/main.py --stdin --format vessel"
echo ""
echo -e "  ${BLUE}# Different output formats${NC}"
echo -e "  python3 agents/zybooks-solver/main.py <file> --format yaml    # Structured"
echo -e "  python3 agents/zybooks-solver/main.py <file> --format rapid   # Quick scan"
echo -e "  python3 agents/zybooks-solver/main.py <file> --format table   # ASCII table"
echo -e "  python3 agents/zybooks-solver/main.py <file> --format vessel  # Minimal"
echo ""
echo -e "  ${BLUE}# Save parsed questions${NC}"
echo -e "  python3 agents/zybooks-solver/main.py <file> --save questions.json"
echo ""

echo -e "${YELLOW}📖 Documentation:${NC}"
echo -e "  See: agents/zybooks-solver/README.md"
echo ""

echo -e "${YELLOW}🎓 Workflow:${NC}"
echo -e "  1. Copy zyBooks content"
echo -e "  2. Paste into training/zybooks/PASTE_HERE.md"
echo -e "  3. Run: python3 agents/zybooks-solver/main.py training/zybooks/PASTE_HERE.md"
echo -e "  4. Get answers in <5 seconds"
echo -e "  5. Enter answers in zyBooks"
echo -e "  6. 🔥 LOCKED IN"
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
