#!/bin/bash
# index-wings.sh - Index all Alexandria knowledge wings
# Usage: ./scripts/index-wings.sh [wing_name]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ALEXANDRIA_DATA_PATH="${ALEXANDRIA_DATA_PATH:-/data/alexandria}"

echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Alexandria Wing Indexing               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Available wings
WINGS=("medical" "physics_chemistry" "biology_genomics" "forbidden_knowledge" "tinker_labs")

# If specific wing provided, index only that
if [ $# -eq 1 ]; then
    SELECTED_WING=$1
    if [[ ! " ${WINGS[@]} " =~ " ${SELECTED_WING} " ]]; then
        echo -e "${RED}Error: Unknown wing '$SELECTED_WING'${NC}"
        echo -e "${YELLOW}Available wings: ${WINGS[*]}${NC}"
        exit 1
    fi
    WINGS=("$SELECTED_WING")
    echo -e "${YELLOW}Indexing single wing: $SELECTED_WING${NC}"
else
    echo -e "${YELLOW}Indexing all wings${NC}"
fi

echo ""

index_wing() {
    local wing=$1
    local wing_path="$ALEXANDRIA_DATA_PATH/$wing"
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Indexing wing: ${NC}${GREEN}$wing${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Check if wing directory exists
    if [ ! -d "$wing_path" ]; then
        echo -e "${RED}✗ Wing directory not found: $wing_path${NC}"
        echo -e "${YELLOW}  Creating directory...${NC}"
        mkdir -p "$wing_path"
        echo -e "${GREEN}✓ Directory created${NC}"
    fi
    
    # Check for files
    FILE_COUNT=$(find "$wing_path" -type f 2>/dev/null | wc -l)
    if [ "$FILE_COUNT" -eq 0 ]; then
        echo -e "${YELLOW}⚠ No files found in $wing${NC}"
        echo -e "${BLUE}  Please populate $wing_path with data${NC}"
        return
    fi
    
    echo -e "${BLUE}Found ${FILE_COUNT} files to index${NC}"
    
    # Get size
    WING_SIZE=$(du -sh "$wing_path" 2>/dev/null | cut -f1 || echo "0")
    echo -e "${BLUE}Wing size: ${WING_SIZE}${NC}"
    
    # Run indexing via Docker
    echo -e "${YELLOW}Starting indexing process...${NC}"
    
    if docker-compose -f docker-compose-alexandria.yml run --rm \
        -e WING_NAME="$wing" \
        -e WING_PATH="/data/$wing" \
        ingestor python ingest.py \
            --wing "$wing" \
            --path "/data/$wing" \
            --collection "alexandria-$wing" \
            --verbose; then
        echo -e "${GREEN}✓ Successfully indexed $wing wing${NC}"
        
        # Get collection stats
        if COLLECTION_INFO=$(curl -s "http://localhost:6333/collections/alexandria-$wing" 2>/dev/null); then
            VECTOR_COUNT=$(echo "$COLLECTION_INFO" | grep -o '"vectors_count":[0-9]*' | cut -d':' -f2 || echo "0")
            echo -e "${GREEN}  Vectors created: ${VECTOR_COUNT}${NC}"
        fi
    else
        echo -e "${RED}✗ Failed to index $wing wing${NC}"
        return 1
    fi
    
    echo ""
}

# Index each wing
TOTAL_WINGS=${#WINGS[@]}
SUCCESSFUL=0
FAILED=0

for wing in "${WINGS[@]}"; do
    if index_wing "$wing"; then
        ((SUCCESSFUL++))
    else
        ((FAILED++))
    fi
done

# Summary
echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Indexing Complete                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "Total wings: ${TOTAL_WINGS}"
echo -e "${GREEN}Successful: ${SUCCESSFUL}${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: ${FAILED}${NC}"
fi

# Show collection summary
echo ""
echo -e "${YELLOW}Collection Summary:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

for wing in "${WINGS[@]}"; do
    if COLLECTION_INFO=$(curl -s "http://localhost:6333/collections/alexandria-$wing" 2>/dev/null); then
        VECTOR_COUNT=$(echo "$COLLECTION_INFO" | grep -o '"vectors_count":[0-9]*' | cut -d':' -f2 || echo "0")
        printf "%-25s %s vectors\n" "$wing:" "$VECTOR_COUNT"
    else
        printf "%-25s ${RED}Not indexed${NC}\n" "$wing:"
    fi
done

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All wings indexed successfully! 📚${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  • Test queries: curl -X POST http://localhost:7000/query -d '{\"q\":\"test query\"}'"
    echo "  • Access WebUI: http://localhost:3000"
    echo "  • Create researcher invites: ./scripts/create-researcher-invite.sh"
    exit 0
else
    echo -e "${RED}Some wings failed to index${NC}"
    echo -e "${YELLOW}Check logs: docker-compose -f docker-compose-alexandria.yml logs ingestor${NC}"
    exit 1
fi
