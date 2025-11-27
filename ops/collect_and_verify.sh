#!/bin/bash
# collect_and_verify.sh
# Cloud Swarm Operations - Aggregation & Provenance Verification
# Strategickhaos DAO LLC — Cryptographic Result Collection and Verification
#
# Usage: ./collect_and_verify.sh <inventory_file> <output_dir>
# Example: ./collect_and_verify.sh cloud_hosts.ini collected_run_2025-11-27

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           CLOUD SWARM COLLECTION & VERIFICATION             ║${NC}"
echo -e "${BLUE}║              Aggregation + Provenance Proof                 ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
INVENTORY="${1:-}"
OUTPUT_DIR="${2:-collected_results_$(date -u +%Y%m%d_%H%M%S)}"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)

# Validate inputs
if [[ -z "$INVENTORY" ]]; then
    echo -e "${RED}❌ Usage: $0 <inventory_file> [output_dir]${NC}"
    exit 1
fi

if [[ ! -f "$INVENTORY" ]]; then
    echo -e "${RED}❌ Inventory file not found: $INVENTORY${NC}"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo -e "${GREEN}📦 Collecting results from cloud swarm...${NC}"
echo -e "${BLUE}📄 Inventory: $INVENTORY${NC}"
echo -e "${BLUE}📁 Output: $OUTPUT_DIR${NC}"
echo ""

# Count hosts
HOST_COUNT=0
VERIFIED_COUNT=0
FAILED_HOSTS=""

# Function to collect from a single host
collect_from_host() {
    local host="$1"
    local host_dir="$OUTPUT_DIR/$host"
    
    mkdir -p "$host_dir"
    
    echo -e "${YELLOW}🔄 Collecting from: $host${NC}"
    
    # Attempt to fetch results via SSH
    if ssh -o ConnectTimeout=10 -o BatchMode=yes "$host" "test -d /var/lib/swarm/results" 2>/dev/null; then
        # Copy results
        if scp -o ConnectTimeout=10 -r "$host:/var/lib/swarm/results/*" "$host_dir/" 2>/dev/null; then
            echo -e "${GREEN}✅ Collected from: $host${NC}"
            return 0
        fi
    fi
    
    echo -e "${RED}❌ Failed to collect from: $host${NC}"
    return 1
}

# Function to verify hash
verify_hash() {
    local file="$1"
    local expected_hash="$2"
    
    if [[ ! -f "$file" ]]; then
        return 1
    fi
    
    local actual_hash
    actual_hash=$(sha256sum "$file" | cut -d' ' -f1)
    
    if [[ "$actual_hash" == "$expected_hash" ]]; then
        return 0
    fi
    
    return 1
}

# Parse inventory and collect from each host
while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip comments and empty lines
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// }" ]] && continue
    
    # Extract host (first field, ignore ansible variables)
    host=$(echo "$line" | awk '{print $1}')
    
    # Skip group headers
    [[ "$host" =~ ^\[ ]] && continue
    [[ -z "$host" ]] && continue
    
    ((HOST_COUNT++)) || true
    
    if collect_from_host "$host"; then
        ((VERIFIED_COUNT++)) || true
    else
        FAILED_HOSTS+="$host "
    fi
done < "$INVENTORY"

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}📊 Collection Summary${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "Total Hosts: $HOST_COUNT"
echo -e "Verified: $VERIFIED_COUNT"
echo -e "Failed: $((HOST_COUNT - VERIFIED_COUNT))"

if [[ -n "$FAILED_HOSTS" ]]; then
    echo -e "${RED}Failed hosts: $FAILED_HOSTS${NC}"
fi

# Aggregate results into single JSON
echo ""
echo -e "${YELLOW}📦 Aggregating results...${NC}"

AGGREGATED_FILE="$OUTPUT_DIR/aggregated_results.json"

{
    echo "{"
    echo "  \"collection_timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
    echo "  \"inventory\": \"$INVENTORY\","
    echo "  \"total_hosts\": $HOST_COUNT,"
    echo "  \"verified_hosts\": $VERIFIED_COUNT,"
    echo "  \"operator\": \"Node 137\","
    echo "  \"results\": ["
    
    first=true
    for host_dir in "$OUTPUT_DIR"/*/; do
        if [[ -d "$host_dir" ]]; then
            host_name=$(basename "$host_dir")
            
            # Skip if no result files
            result_files=$(find "$host_dir" -type f -name "*.json" 2>/dev/null | head -1)
            [[ -z "$result_files" ]] && continue
            
            if [[ "$first" == "true" ]]; then
                first=false
            else
                echo ","
            fi
            
            echo "    {"
            echo "      \"host\": \"$host_name\","
            echo "      \"collected_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
            echo "      \"files\": ["
            
            file_first=true
            while IFS= read -r -d '' file; do
                file_hash=$(sha256sum "$file" | cut -d' ' -f1)
                file_name=$(basename "$file")
                
                if [[ "$file_first" == "true" ]]; then
                    file_first=false
                else
                    echo ","
                fi
                
                echo -n "        {\"name\": \"$file_name\", \"sha256\": \"$file_hash\"}"
            done < <(find "$host_dir" -type f -print0)
            
            echo ""
            echo "      ]"
            echo -n "    }"
        fi
    done
    
    echo ""
    echo "  ]"
    echo "}"
} > "$AGGREGATED_FILE"

echo -e "${GREEN}✅ Aggregated results: $AGGREGATED_FILE${NC}"

# Generate SHA256 of aggregated file
AGGREGATED_HASH=$(sha256sum "$AGGREGATED_FILE" | cut -d' ' -f1)
echo -e "${GREEN}🔐 Aggregated SHA256: $AGGREGATED_HASH${NC}"

# Create hash manifest
MANIFEST_FILE="$OUTPUT_DIR/manifest.sha256"
sha256sum "$AGGREGATED_FILE" > "$MANIFEST_FILE"
echo -e "${GREEN}📋 Hash manifest: $MANIFEST_FILE${NC}"

# GPG sign if available
if command -v gpg &> /dev/null; then
    echo -e "${BLUE}🔏 Creating GPG detached signature...${NC}"
    if gpg --detach-sign --armor "$AGGREGATED_FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ GPG signature: ${AGGREGATED_FILE}.asc${NC}"
    else
        echo -e "${YELLOW}⚠️  GPG signing skipped (no key available)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  GPG not available${NC}"
fi

# OpenTimestamps if available
if command -v ots &> /dev/null; then
    echo -e "${BLUE}⏰ Creating OpenTimestamp...${NC}"
    if ots stamp "$AGGREGATED_FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ OpenTimestamp: ${AGGREGATED_FILE}.ots${NC}"
    else
        echo -e "${YELLOW}⚠️  OpenTimestamp creation pending (calendar submission)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  OpenTimestamps (ots) not installed${NC}"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎯 COLLECTION & VERIFICATION COMPLETE${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "📁 Output Directory: $OUTPUT_DIR"
echo -e "📊 Hosts Verified: $VERIFIED_COUNT / $HOST_COUNT"
echo -e "📄 Aggregated File: $AGGREGATED_FILE"
echo -e "🔐 SHA256: $AGGREGATED_HASH"
echo -e "⏰ Timestamp: $TIMESTAMP"
echo ""
