#!/bin/bash
# notarize_cognition.sh
# REFLEXSHELL BRAIN v1 — IPFS + OpenTimestamps Cognitive State Notarization
# Strategickhaos DAO LLC — Cryptographic Proof of Neural State Transitions
#
# NOTE: For permanent R&D conversation ledger with GPG + OTS Bitcoin attestation,
#       see the evidence/ directory and evidence/README.md for verification.

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              COGNITIVE STATE NOTARIZATION v1                 ║${NC}"
echo -e "${BLUE}║                   IPFS + OTS Timestamping                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
IPFS_API="http://127.0.0.1:5001"
NOTARY_DIR="cognitive_notary"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)

# Create notary directory
mkdir -p "$NOTARY_DIR"

notarize_cognitive_state() {
    local state_file="$1"
    local description="$2"
    
    if [[ ! -f "$state_file" ]]; then
        echo -e "${RED}❌ State file not found: $state_file${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}📝 Notarizing cognitive state: $state_file${NC}"
    
    # Generate SHA256 hash
    local hash=$(sha256sum "$state_file" | cut -d' ' -f1)
    echo -e "${GREEN}🔐 SHA256: $hash${NC}"
    
    # Create notarization record
    local notary_file="$NOTARY_DIR/cognitive_state_${TIMESTAMP}.json"
    cat > "$notary_file" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "file": "$state_file",
  "description": "$description",
  "sha256": "$hash",
  "operator": "Node 137",
  "notarization_type": "cognitive_state",
  "brain_version": "REFLEXSHELL_v1"
}
EOF
    
    # IPFS pin (if available)
    if command -v ipfs &> /dev/null; then
        echo -e "${BLUE}📌 Pinning to IPFS...${NC}"
        local ipfs_hash=$(ipfs add -q "$notary_file")
        echo -e "${GREEN}🌐 IPFS Hash: $ipfs_hash${NC}"
        
        # Update notary record with IPFS hash
        local temp_file=$(mktemp)
        jq ". + {\"ipfs_hash\": \"$ipfs_hash\"}" "$notary_file" > "$temp_file"
        mv "$temp_file" "$notary_file"
    else
        echo -e "${YELLOW}⚠️  IPFS not available - local notary only${NC}"
    fi
    
    # OpenTimestamps (if available)
    if command -v ots &> /dev/null; then
        echo -e "${BLUE}⏰ Creating OpenTimestamp...${NC}"
        ots stamp "$notary_file"
        echo -e "${GREEN}✅ OpenTimestamp created: $notary_file.ots${NC}"
    else
        echo -e "${YELLOW}⚠️  OpenTimestamps not available${NC}"
    fi
    
    echo -e "${GREEN}✅ Cognitive state notarized: $notary_file${NC}"
    echo ""
}

# Main notarization workflow
main() {
    echo -e "${GREEN}🧠 Starting cognitive state notarization...${NC}"
    
    # Notarize key cognitive files
    if [[ -f "cognitive_state.json" ]]; then
        notarize_cognitive_state "cognitive_state.json" "ReflexShell Brain cognitive environment state"
    fi
    
    if [[ -f "cognitive_thread_status.json" ]]; then
        notarize_cognitive_state "cognitive_thread_status.json" "Parallel thread execution status"
    fi
    
    if [[ -f "dao_record_v1.0.yaml" ]]; then
        notarize_cognitive_state "dao_record_v1.0.yaml" "Week 1 sovereignty record - complete neural architecture"
    fi
    
    if [[ -f "cognitive_architecture.svg" ]]; then
        notarize_cognitive_state "cognitive_architecture.svg" "Visual cognitive architecture map"
    fi
    
    # Create master cognitive manifest
    local manifest="$NOTARY_DIR/cognitive_manifest_${TIMESTAMP}.json"
    echo "{" > "$manifest"
    echo "  \"manifest_type\": \"cognitive_notarization\"," >> "$manifest"
    echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"," >> "$manifest"
    echo "  \"operator\": \"Node 137\"," >> "$manifest"
    echo "  \"brain_version\": \"REFLEXSHELL_v1\"," >> "$manifest"
    echo "  \"notarized_files\": [" >> "$manifest"
    
    # Add all notary files to manifest
    local first=true
    for file in "$NOTARY_DIR"/*.json; do
        if [[ "$file" != "$manifest" ]]; then
            if [[ "$first" == "true" ]]; then
                first=false
            else
                echo "," >> "$manifest"
            fi
            echo -n "    \"$(basename "$file")\"" >> "$manifest"
        fi
    done
    
    echo "" >> "$manifest"
    echo "  ]" >> "$manifest"
    echo "}" >> "$manifest"
    
    echo -e "${GREEN}📋 Cognitive manifest created: $manifest${NC}"
    
    # Final summary
    local file_count=$(ls -1 "$NOTARY_DIR"/*.json 2>/dev/null | wc -l)
    echo ""
    echo -e "${GREEN}🎯 NOTARIZATION COMPLETE${NC}"
    echo -e "${BLUE}📊 Files notarized: $file_count${NC}"
    echo -e "${BLUE}📁 Notary directory: $NOTARY_DIR${NC}"
    echo -e "${BLUE}⏰ Timestamp: $TIMESTAMP${NC}"
    echo ""
}

# Execute if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi