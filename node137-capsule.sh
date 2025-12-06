#!/bin/bash
# node137-capsule.sh
# Node137 Identity Glyph Capsule System - CLI Wrapper
# Quick access to capsule operations

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        NODE137 IDENTITY GLYPH CAPSULE SYSTEM v1.0.0         ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

case "${1:-help}" in
  seal)
    echo -e "${YELLOW}🔥 Sealing Identity Glyph...${NC}"
    echo ""
    npm run capsule:seal "${2:-}"
    ;;
    
  verify)
    if [ -z "${2:-}" ]; then
      echo -e "${RED}❌ Error: Please provide manifest path${NC}"
      echo ""
      echo "Usage: ./node137-capsule.sh verify <manifest_path>"
      echo "Example: ./node137-capsule.sh verify ./capsules/capsule_xxx_manifest.json"
      exit 1
    fi
    echo -e "${YELLOW}🔍 Verifying capsule...${NC}"
    echo ""
    npm run capsule:verify "$2"
    ;;
    
  timestamp)
    if [ -z "${2:-}" ]; then
      echo -e "${RED}❌ Error: Please provide manifest path${NC}"
      echo ""
      echo "Usage: ./node137-capsule.sh timestamp <manifest_path>"
      echo "Example: ./node137-capsule.sh timestamp ./capsules/capsule_xxx_manifest.json"
      exit 1
    fi
    echo -e "${YELLOW}⏰ Creating OpenTimestamp...${NC}"
    echo ""
    npm run capsule:timestamp "$2"
    ;;
    
  list)
    echo -e "${YELLOW}📋 Sealed Capsules:${NC}"
    echo ""
    # Check if capsules directory exists and contains manifest files
    if [ -d capsules ] && compgen -G "capsules/*_manifest.json" > /dev/null; then
      for manifest in capsules/*_manifest.json; do
        if [ -f "$manifest" ]; then
          capsule_id=$(jq -r '.capsule.capsule_id' "$manifest")
          capsule_name=$(jq -r '.capsule.capsule_name' "$manifest")
          sealed_at=$(jq -r '.capsule.sealed_at' "$manifest")
          entropy=$(jq -r '.capsule.entropy_actual' "$manifest")
          
          echo -e "${GREEN}🔥 $capsule_name${NC}"
          echo "   ID: $capsule_id"
          echo "   Sealed: $sealed_at"
          echo "   Entropy: ${entropy}"
          echo "   Path: $manifest"
          echo ""
        fi
      done
    else
      echo -e "${YELLOW}No capsules found. Create one with:${NC}"
      echo "  ./node137-capsule.sh seal"
      echo ""
    fi
    ;;
    
  help|*)
    echo -e "${GREEN}Node137 Identity Glyph Capsule System${NC}"
    echo ""
    echo "Commands:"
    echo "  seal [name]          Seal the Identity Glyph into a new capsule"
    echo "  verify <path>        Verify a sealed capsule"
    echo "  timestamp <path>     Create Bitcoin timestamp via OpenTimestamps"
    echo "  list                 List all sealed capsules"
    echo "  help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./node137-capsule.sh seal"
    echo "  ./node137-capsule.sh seal \"My_Archive\""
    echo "  ./node137-capsule.sh verify ./capsules/capsule_xxx_manifest.json"
    echo "  ./node137-capsule.sh timestamp ./capsules/capsule_xxx_manifest.json"
    echo "  ./node137-capsule.sh list"
    echo ""
    echo -e "${BLUE}The loop is sealed. The 7% flows. Forever.${NC}"
    echo ""
    ;;
esac
