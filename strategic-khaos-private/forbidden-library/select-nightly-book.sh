#!/bin/bash

# 🌙 Nightly Book Selection Script
# Randomly selects one book from the 100-Book Ascension Library
# Usage: ./select-nightly-book.sh [--obsidian-vault PATH]

set -euo pipefail

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_FILE="${SCRIPT_DIR}/100-ascension-books.md"

# Parse arguments
OBSIDIAN_VAULT=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --obsidian-vault)
            OBSIDIAN_VAULT="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Unknown option: $1${RESET}"
            exit 1
            ;;
    esac
done

# Check if library file exists
if [[ ! -f "$LIBRARY_FILE" ]]; then
    echo -e "${RED}Error: Library file not found at $LIBRARY_FILE${RESET}"
    exit 1
fi

# Extract all books (lines starting with numbers 1-100 followed by a period)
mapfile -t BOOKS < <(grep -E '^[0-9]{1,3}\.\s+\*\*' "$LIBRARY_FILE")

# Total number of books
TOTAL_BOOKS=${#BOOKS[@]}

if [[ $TOTAL_BOOKS -eq 0 ]]; then
    echo -e "${RED}Error: No books found in library file${RESET}"
    exit 1
fi

# Select a random book
RANDOM_INDEX=$((RANDOM % TOTAL_BOOKS))
SELECTED_BOOK="${BOOKS[$RANDOM_INDEX]}"

# Parse book details
BOOK_NUMBER=$(echo "$SELECTED_BOOK" | grep -oE '^[0-9]+')
BOOK_TITLE=$(echo "$SELECTED_BOOK" | sed -E 's/^[0-9]+\.\s+\*\*(.+)\*\*.*/\1/')
BOOK_AUTHOR=$(echo "$SELECTED_BOOK" | sed -E 's/^[0-9]+\.\s+\*\*.+\*\*\s+–\s+(.+)/\1/' || echo "")

# Determine chamber
CHAMBER_NUM=$(((BOOK_NUMBER - 1) / 10 + 1))
CHAMBER_NAMES=(
    "Pattern Recognition & Metacognition"
    "Sacred Geometry & Mathematics as Magic"
    "Forbidden History & Lost Civilizations"
    "Consciousness Engineering & Reality Hacking"
    "Hermeticism & Western Esotericism"
    "Eastern & Shamanic Paths"
    "Extreme Polymath Lives"
    "Frequency, Sound, Cymatics, 369"
    "Future / Transhuman / Sovereign Mind"
    "The Final 10"
)
CHAMBER_NAME="${CHAMBER_NAMES[$((CHAMBER_NUM - 1))]}"

# Display selection
echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${RESET}"
echo -e "${CYAN}🌙 Tonight's Book Selection from the Ascension Library 🌙${RESET}"
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "${YELLOW}Book #${BOOK_NUMBER} of 100${RESET}"
echo -e "${GREEN}Title:${RESET} ${BLUE}${BOOK_TITLE}${RESET}"
if [[ -n "$BOOK_AUTHOR" ]]; then
    echo -e "${GREEN}Author:${RESET} ${BOOK_AUTHOR}"
fi
echo -e "${GREEN}Chamber ${CHAMBER_NUM}:${RESET} ${CHAMBER_NAME}"
echo ""
echo -e "${CYAN}⚡ This book called to you tonight. ⚡${RESET}"
echo -e "${CYAN}⚡ That's the next key turning in your DNA. ⚡${RESET}"
echo ""
echo -e "${YELLOW}📖 Read by sunrise flag: ACTIVE${RESET}"
echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${RESET}"
echo ""

# Create reading note if Obsidian vault specified
if [[ -n "$OBSIDIAN_VAULT" ]]; then
    if [[ -d "$OBSIDIAN_VAULT" ]]; then
        TIMESTAMP=$(date +"%Y-%m-%d")
        NOTE_FILE="${OBSIDIAN_VAULT}/Nightly Reading ${TIMESTAMP}.md"
        
        cat > "$NOTE_FILE" << EOF
# 🌙 Nightly Reading: ${BOOK_TITLE}

**Date**: ${TIMESTAMP}
**Book Number**: ${BOOK_NUMBER}/100
**Chamber**: ${CHAMBER_NUM} - ${CHAMBER_NAME}
**Author**: ${BOOK_AUTHOR}

## 🎯 Read by Sunrise Flag: ACTIVE

## Key Insights

- 

## Resonances & Synchronicities

- 

## Questions Arising

- 

## Integration Notes

- 

---

*This book called to you tonight. That's the next key turning in your DNA.*

**Frequency**: 432 Hz  
**Status**: 🔥 Active Reading
EOF
        
        echo -e "${GREEN}✅ Created reading note in Obsidian vault:${RESET}"
        echo -e "   ${NOTE_FILE}"
        echo ""
    else
        echo -e "${RED}Warning: Obsidian vault path not found: ${OBSIDIAN_VAULT}${RESET}"
        echo ""
    fi
fi

# Log selection to history file
HISTORY_FILE="${SCRIPT_DIR}/reading-history.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "${TIMESTAMP} | Book #${BOOK_NUMBER} | ${BOOK_TITLE} | Chamber ${CHAMBER_NUM}" >> "$HISTORY_FILE"

echo -e "${GREEN}📚 Selection logged to reading history${RESET}"
echo ""

# Optionally display a motivational message
MESSAGES=(
    "The legion is downloading this wisdom into your consciousness."
    "You are ascending faster than light."
    "Trust the swarm. It knows what you need."
    "Every book is a frequency adjustment."
    "This synchronicity is not a coincidence."
    "The pattern recognizes itself in you."
    "Your DNA is already decoding this knowledge."
    "The right book at the right time is destiny."
)
RANDOM_MSG_INDEX=$((RANDOM % ${#MESSAGES[@]}))
echo -e "${CYAN}💫 ${MESSAGES[$RANDOM_MSG_INDEX]} 💫${RESET}"
echo ""

exit 0
