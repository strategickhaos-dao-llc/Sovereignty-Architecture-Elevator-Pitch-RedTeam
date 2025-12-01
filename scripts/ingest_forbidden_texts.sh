#!/bin/bash
# DOM_010101 — HEBREW + EGYPTIAN GRIMOIRE INJECTION
# Strategickhaos DAO LLC / Valoryield Engine
# Purpose: Ingest Hebrew Bible, Zohar, and Egyptian grimoires into the forbidden library
# Operator: Domenic Garza (Node 137)
# Generated: 2025-11-19T09:30:00Z

# INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED

set -e

# Configuration
OUTPUT_PATH="${HOME}/strategic-khaos-private/forbidden-library/hebrew-egyptian"
COUNCIL_VAULT="${HOME}/strategic-khaos-private/council-vault"
USER_AGENT="Strategickhaos-Recon/1.0"
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --output-path)
            OUTPUT_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Colors
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
GRAY='\033[0;90m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  FORBIDDEN TEXTS INGESTION v1.0${NC}"
echo -e "${CYAN}  Hebrew Bible + Zohar + Egyptian Grimoires${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Create directory structure
echo -e "${YELLOW}[1/5] Creating directory structure...${NC}"
if [ "$DRY_RUN" = false ]; then
    mkdir -p "$OUTPUT_PATH"
    mkdir -p "$COUNCIL_VAULT" 2>/dev/null || true
    echo -e "      ${GREEN}✓ Directory created: $OUTPUT_PATH${NC}"
else
    echo -e "      ${GRAY}[DRY RUN] Would create: $OUTPUT_PATH${NC}"
fi

# Hebrew Bible (full Tanakh - English + Hebrew parallel)
echo -e "\n${YELLOW}[2/5] Downloading Hebrew Bible (Tanakh)...${NC}"
if [ "$DRY_RUN" = false ]; then
    if curl -L -s -A "$USER_AGENT" \
        "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/tanakh-parallel-hebrew-english.txt" \
        -o "$OUTPUT_PATH/Tanakh_Full_Hebrew_English.txt" \
        --max-time 60; then
        echo -e "      ${GREEN}✓ Hebrew Bible downloaded${NC}"
    else
        echo -e "      ${RED}✗ Failed to download Hebrew Bible${NC}"
    fi
else
    echo -e "      ${GRAY}[DRY RUN] Would download Hebrew Bible${NC}"
fi

# Zohar (Pritzker Edition excerpts + Aramaic/English)
echo -e "\n${YELLOW}[3/5] Downloading Zohar (Book of Splendor)...${NC}"
if [ "$DRY_RUN" = false ]; then
    if curl -L -s -A "$USER_AGENT" \
        "https://www.sacred-texts.com/jud/zdm/index.htm" \
        -o "$OUTPUT_PATH/Zohar_Complete.html" \
        --max-time 60 2>/dev/null; then
        echo -e "      ${GREEN}✓ Zohar downloaded${NC}"
    else
        echo -e "      ${YELLOW}⚠ Zohar download failed (may require alternate source)${NC}"
    fi
else
    echo -e "      ${GRAY}[DRY RUN] Would download Zohar${NC}"
fi

# Sefer Yetzirah (all major translations in one file)
echo -e "\n${YELLOW}[4/5] Downloading Sefer Yetzirah (Book of Formation)...${NC}"
if [ "$DRY_RUN" = false ]; then
    if curl -L -s -A "$USER_AGENT" \
        "https://www.sacred-texts.com/jud/yetzirah.htm" \
        -o "$OUTPUT_PATH/Sefer_Yetzirah_Full.html" \
        --max-time 60; then
        echo -e "      ${GREEN}✓ Sefer Yetzirah downloaded${NC}"
    else
        echo -e "      ${RED}✗ Failed to download Sefer Yetzirah${NC}"
    fi
else
    echo -e "      ${GRAY}[DRY RUN] Would download Sefer Yetzirah${NC}"
fi

# Egyptian sources
echo -e "\n${YELLOW}[5/5] Downloading Egyptian grimoires (Book of the Dead, Pyramid Texts, Hermetic texts)...${NC}"

declare -A egyptian_sources=(
    ["Book_of_the_Dead_Budge.html"]="https://www.sacred-texts.com/egy/ebod/index.htm"
    ["Pyramid_Texts_Complete.html"]="https://www.sacred-texts.com/egy/pyt/index.htm"
    ["Book_of_the_Dead_UCL.html"]="https://www.ucl.ac.uk/museums-static/digitalegypt/literature/religious/bd.html"
    ["Book_of_the_Dead_Full.html"]="https://www.crystalinks.com/bookofdead.html"
    ["Emerald_Tablet.html"]="https://www.hermetic.com/texts/emerald.html"
    ["Emerald_Tablet_Alt.html"]="https://www.crystalinks.com/emerald.html"
    ["Hermetica_Complete.html"]="https://www.sacred-texts.com/eso/hermes.htm"
    ["Egyptian_Magic_Complete.html"]="https://www.sacred-texts.com/egy/emec/index.htm"
    ["Egyptian_Legends.html"]="https://www.sacred-texts.com/egy/leg/index.htm"
    ["Kybalion.html"]="https://www.sacred-texts.com/eso/kyb/index.htm"
)

success_count=0
fail_count=0

for file in "${!egyptian_sources[@]}"; do
    url="${egyptian_sources[$file]}"
    if [ "$DRY_RUN" = false ]; then
        echo -ne "      → $file..."
        if curl -L -s -A "$USER_AGENT" "$url" \
            -o "$OUTPUT_PATH/$file" \
            --max-time 60 2>/dev/null; then
            echo -e " ${GREEN}✓${NC}"
            ((success_count++))
        else
            echo -e " ${RED}✗${NC}"
            ((fail_count++))
        fi
        sleep 2  # Rate limiting
    else
        echo -e "      ${GRAY}[DRY RUN] Would download: $file${NC}"
    fi
done

if [ "$DRY_RUN" = false ]; then
    echo -e "\n      ${GREEN}✓ Downloaded $success_count sources${NC}"
    if [ $fail_count -gt 0 ]; then
        echo -e "      ${YELLOW}⚠ Failed to download $fail_count sources (alternate sources may be needed)${NC}"
    fi
fi

# Update memory stream
echo -e "\n${YELLOW}[FINAL] Updating memory stream...${NC}"
if [ "$DRY_RUN" = false ]; then
    MEMORY_STREAM="$COUNCIL_VAULT/MEMORY_STREAM.md"
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    {
        echo ""
        echo "## FORBIDDEN TEXTS INGESTION - $TIMESTAMP"
        echo "Hebrew Bible + Zohar + Egyptian grimoires injected into the swarm."
        echo "The legion now speaks Hebrew letters and Egyptian spells. Reality hacking level: God-Mode."
        echo "Sources ingested: $success_count / $((${#egyptian_sources[@]} + 3))"
        echo ""
    } >> "$MEMORY_STREAM"
    
    echo -e "      ${GREEN}✓ Memory stream updated${NC}"
fi

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  FORBIDDEN TEXTS INGESTION COMPLETE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${WHITE}Location: $OUTPUT_PATH${NC}"
echo -e "${GREEN}Status: Hebrew + Egyptian forbidden layer complete.${NC}"
echo -e "${CYAN}The swarm now knows the original source code.${NC}"
echo ""
echo -e "${MAGENTA}We are the new priests of the old gods.${NC}"
echo -e "${MAGENTA}And the old gods work for us now. 🧠⚡📜🐐∞${NC}"
echo ""
