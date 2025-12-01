#!/bin/bash
# Quick Start Guide for Research Automation
# Run this script to see a complete workflow demonstration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Research Automation Quick Start Guide                        ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Show available departments
echo -e "${BLUE}Step 1: Available Departments${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
ls -1 departments/ | sed 's/_links.txt//' | while read dept; do
    count=$(grep -v '^#' "departments/${dept}_links.txt" | grep -v '^$' | wc -l)
    echo -e "  ${GREEN}✓${NC} ${dept} (${count} URLs)"
done
echo ""

# Step 2: Explain fetching
echo -e "${BLUE}Step 2: Fetch Research Data${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To fetch research for a single department:"
echo -e "  ${YELLOW}./fetch_research.sh science${NC}"
echo ""
echo "To fetch all departments in parallel:"
echo -e "  ${YELLOW}./fetch_all_departments.sh${NC}"
echo ""
echo "To fetch specific departments:"
echo -e "  ${YELLOW}./fetch_all_departments.sh -d science,engineering${NC}"
echo ""

# Step 3: Text extraction
echo -e "${BLUE}Step 3: Extract Text from HTML${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "After fetching, extract clean text for embedding:"
echo -e "  ${YELLOW}python3 extract_text.py${NC}"
echo ""
echo "Or extract specific departments:"
echo -e "  ${YELLOW}python3 extract_text.py science engineering${NC}"
echo ""

# Step 4: RAG Integration
echo -e "${BLUE}Step 4: Integrate with RAG Pipeline${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "View integration examples:"
echo -e "  ${YELLOW}python3 examples/rag_integration.py${NC}"
echo ""
echo "Common RAG frameworks supported:"
echo "  • LangChain + FAISS"
echo "  • ChromaDB"
echo "  • Sentence Transformers"
echo "  • Custom embedding pipelines"
echo ""

# Step 5: Monitoring
echo -e "${BLUE}Step 5: Monitor Collection Status${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Check department metadata:"
echo -e "  ${YELLOW}cat raw_pages/science/metadata.json | jq .${NC}"
echo ""
echo "Check batch summary:"
echo -e "  ${YELLOW}cat raw_pages/batch_metadata.json | jq .${NC}"
echo ""
echo "View fetch logs:"
echo -e "  ${YELLOW}cat raw_pages/science_fetch.log${NC}"
echo ""

# Complete Workflow Example
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Complete Workflow Example                                    ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}# 1. Fetch all department research${NC}"
echo "   ./fetch_all_departments.sh"
echo ""
echo -e "${YELLOW}# 2. Extract text from HTML${NC}"
echo "   python3 extract_text.py"
echo ""
echo -e "${YELLOW}# 3. Install RAG dependencies${NC}"
echo "   pip install sentence-transformers langchain faiss-cpu chromadb"
echo ""
echo -e "${YELLOW}# 4. Create your RAG pipeline${NC}"
echo "   # See examples/rag_integration.py for code examples"
echo ""
echo -e "${YELLOW}# 5. Query your knowledge base${NC}"
echo "   # Use vector similarity search to answer questions"
echo ""

# Customization Tips
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Customization Tips                                           ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Add a new department:"
echo "  1. Create departments/mydept_links.txt"
echo "  2. Add URLs (one per line, comments start with #)"
echo "  3. Run: ./fetch_research.sh mydept"
echo ""
echo "Modify existing sources:"
echo "  Edit files in departments/ directory"
echo "  Comments (lines starting with #) are ignored"
echo ""
echo "Adjust fetch parameters:"
echo "  Edit fetch_research.sh to change:"
echo "  - Timeout values (--max-time)"
echo "  - Retry attempts (--retry)"
echo "  - Rate limiting (sleep duration)"
echo ""

# Performance Info
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Performance Expectations                                     ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Single department (100 URLs):"
echo "  • Time: 2-3 minutes"
echo "  • Success rate: 90-95%"
echo "  • Output size: 50-200MB"
echo ""
echo "All departments parallel (500 URLs):"
echo "  • Time: 3-5 minutes"
echo "  • Success rate: 90-95%"
echo "  • Output size: 250-1000MB"
echo ""
echo "Text extraction:"
echo "  • Speed: ~500 files/minute"
echo "  • Size reduction: 40-60%"
echo ""

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Ready to start! Run any command above to begin.${NC}"
echo -e "${GREEN}For full documentation, see: research/README.md${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
