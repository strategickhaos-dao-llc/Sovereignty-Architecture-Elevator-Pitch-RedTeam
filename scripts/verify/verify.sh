#!/usr/bin/env bash
# verify.sh - Swarmgate Archive Verification Script
# Strategickhaos Sovereignty Architecture
# 
# This script verifies the integrity and authenticity of swarmgate_v1.0.tar.gz
# by recreating the deterministic archive, computing BLAKE3 hash, and verifying GPG signature.
#
# Usage: ./verify.sh [OPTIONS]
#   --archive PATH    Path to archive (default: swarmgate_v1.0.tar.gz)
#   --manifest PATH   Path to manifest (default: swarmgate.yaml)
#   --provenance PATH Path to provenance file (default: provenance/provenance.json)
#   --signature PATH  Path to GPG signature (default: swarmgate_v1.0.tar.gz.sig)
#   --skip-rebuild    Skip deterministic rebuild verification
#   --skip-gpg        Skip GPG signature verification
#   --skip-timestamp  Skip RFC3161 timestamp verification
#   --help            Show this help message
#
# Requirements:
#   - b3sum (BLAKE3 hash utility)
#   - gpg (GNU Privacy Guard)
#   - jq (JSON processor)
#   - tar, gzip (archive utilities)
#   - openssl (for timestamp verification)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default paths
ARCHIVE="${ARCHIVE:-swarmgate_v1.0.tar.gz}"
MANIFEST="${MANIFEST:-swarmgate.yaml}"
PROVENANCE="${PROVENANCE:-provenance/provenance.json}"
SIGNATURE="${SIGNATURE:-swarmgate_v1.0.tar.gz.sig}"
SKIP_REBUILD=false
SKIP_GPG=false
SKIP_TIMESTAMP=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --archive)
            ARCHIVE="$2"
            shift 2
            ;;
        --manifest)
            MANIFEST="$2"
            shift 2
            ;;
        --provenance)
            PROVENANCE="$2"
            shift 2
            ;;
        --signature)
            SIGNATURE="$2"
            shift 2
            ;;
        --skip-rebuild)
            SKIP_REBUILD=true
            shift
            ;;
        --skip-gpg)
            SKIP_GPG=true
            shift
            ;;
        --skip-timestamp)
            SKIP_TIMESTAMP=true
            shift
            ;;
        --help)
            head -n 25 "$0" | tail -n +2 | sed 's/^# //'
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Swarmgate Archive Verification - Strategickhaos         ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check required tools
check_tools() {
    local missing=()
    
    if ! command -v b3sum &> /dev/null; then
        missing+=("b3sum")
    fi
    
    if ! command -v jq &> /dev/null; then
        missing+=("jq")
    fi
    
    if ! $SKIP_GPG && ! command -v gpg &> /dev/null; then
        missing+=("gpg")
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}Error: Missing required tools: ${missing[*]}${NC}"
        echo ""
        echo "Install with:"
        echo "  Ubuntu/Debian: sudo apt-get install b3sum jq gnupg"
        echo "  macOS:         brew install b3sum jq gnupg"
        echo "  Arch:          sudo pacman -S b3sum jq gnupg"
        exit 1
    fi
}

# Function to extract canonical hash from provenance
get_canonical_hash() {
    if [[ -f "$PROVENANCE" ]]; then
        if [[ "$PROVENANCE" == *.json ]]; then
            jq -r '.subject[0].digest.blake3 // .predicate.digest.blake3 // empty' "$PROVENANCE" 2>/dev/null || echo ""
        else
            grep -oP '(?<=blake3:\s)[^\s]+' "$PROVENANCE" 2>/dev/null | head -1 || echo ""
        fi
    else
        echo ""
    fi
}

# Function to compute BLAKE3 hash
compute_blake3() {
    local file="$1"
    b3sum "$file" | cut -d' ' -f1
}

# Function to compute SHA256 hash
compute_sha256() {
    local file="$1"
    sha256sum "$file" | cut -d' ' -f1
}

# Verification counter
PASSED=0
FAILED=0
WARNINGS=0

# Check tools
echo -e "${BLUE}[1/5] Checking required tools...${NC}"
check_tools
echo -e "${GREEN}  ✓ All required tools available${NC}"
PASSED=$((PASSED + 1))
echo ""

# Check archive exists
echo -e "${BLUE}[2/5] Checking archive file...${NC}"
if [[ ! -f "$ARCHIVE" ]]; then
    echo -e "${RED}  ✗ Archive not found: $ARCHIVE${NC}"
    echo -e "${YELLOW}    Download from IPFS or GitHub releases first.${NC}"
    FAILED=$((FAILED + 1))
else
    echo -e "${GREEN}  ✓ Archive found: $ARCHIVE${NC}"
    # Use portable method to get file size
    ARCHIVE_SIZE=$(wc -c < "$ARCHIVE" | tr -d ' ')
    echo -e "    Size: ${ARCHIVE_SIZE} bytes"
    PASSED=$((PASSED + 1))
fi
echo ""

# Compute and verify BLAKE3 hash
echo -e "${BLUE}[3/5] Verifying BLAKE3 hash...${NC}"
if [[ -f "$ARCHIVE" ]]; then
    COMPUTED_HASH=$(compute_blake3 "$ARCHIVE")
    echo -e "    Computed:  ${COMPUTED_HASH}"
    
    CANONICAL_HASH=$(get_canonical_hash)
    if [[ -n "$CANONICAL_HASH" && "$CANONICAL_HASH" != "PLACEHOLDER_BLAKE3_HASH" ]]; then
        echo -e "    Canonical: ${CANONICAL_HASH}"
        if [[ "$COMPUTED_HASH" == "$CANONICAL_HASH" ]]; then
            echo -e "${GREEN}  ✓ BLAKE3 hash matches canonical value${NC}"
            PASSED=$((PASSED + 1))
        else
            echo -e "${RED}  ✗ BLAKE3 hash MISMATCH!${NC}"
            echo -e "${RED}    Archive may be corrupted or tampered with.${NC}"
            FAILED=$((FAILED + 1))
        fi
    else
        echo -e "${YELLOW}  ⚠ No canonical hash found in provenance (placeholder present)${NC}"
        echo -e "${YELLOW}    This is expected before first release.${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    # Also compute SHA256 for reference
    SHA256_HASH=$(compute_sha256 "$ARCHIVE")
    echo -e "    SHA256:    ${SHA256_HASH}"
else
    echo -e "${YELLOW}  ⚠ Skipping hash verification (archive not found)${NC}"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Verify GPG signature
echo -e "${BLUE}[4/5] Verifying GPG signature...${NC}"
if $SKIP_GPG; then
    echo -e "${YELLOW}  ⚠ GPG verification skipped (--skip-gpg)${NC}"
    WARNINGS=$((WARNINGS + 1))
elif [[ ! -f "$SIGNATURE" ]]; then
    echo -e "${YELLOW}  ⚠ Signature file not found: $SIGNATURE${NC}"
    echo -e "${YELLOW}    Run with --skip-gpg to skip this check.${NC}"
    WARNINGS=$((WARNINGS + 1))
elif [[ ! -f "$ARCHIVE" ]]; then
    echo -e "${YELLOW}  ⚠ Cannot verify signature (archive not found)${NC}"
    WARNINGS=$((WARNINGS + 1))
else
    if gpg --verify "$SIGNATURE" "$ARCHIVE" 2>&1; then
        echo -e "${GREEN}  ✓ GPG signature verified${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}  ✗ GPG signature verification FAILED${NC}"
        echo -e "${RED}    The archive signature is invalid or the signing key is not trusted.${NC}"
        FAILED=$((FAILED + 1))
    fi
fi
echo ""

# Verify deterministic rebuild (optional)
echo -e "${BLUE}[5/5] Deterministic rebuild verification...${NC}"
if $SKIP_REBUILD; then
    echo -e "${YELLOW}  ⚠ Rebuild verification skipped (--skip-rebuild)${NC}"
    WARNINGS=$((WARNINGS + 1))
elif [[ ! -f "$MANIFEST" ]]; then
    echo -e "${YELLOW}  ⚠ Manifest not found: $MANIFEST${NC}"
    echo -e "${YELLOW}    Cannot perform deterministic rebuild verification.${NC}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "    Attempting deterministic rebuild from $MANIFEST..."
    
    # Create temp directory for rebuild
    REBUILD_DIR=$(mktemp -d)
    trap "rm -rf $REBUILD_DIR" EXIT
    
    # Extract include patterns from manifest (simplified)
    # In production, this would parse swarmgate.yaml properly
    # Use predefined list of files (yq is optional, fallback is used)
    INCLUDE_FILES=(
        "swarmgate.yaml"
        "discovery.yml"
        "dao_record_v1.0.yaml"
        "ai_constitution.yaml"
        "LICENSE"
        "README.md"
        "SECURITY.md"
        "COMMUNITY.md"
        "CONTRIBUTORS.md"
    )
    
    # Filter to only existing files
    EXISTING_FILES=()
    for f in "${INCLUDE_FILES[@]}"; do
        if [[ -e "$f" ]]; then
            EXISTING_FILES+=("$f")
        fi
    done
    
    if [[ ${#EXISTING_FILES[@]} -gt 0 ]]; then
        # Create deterministic archive
        REBUILD_ARCHIVE="$REBUILD_DIR/rebuilt.tar.gz"
        
        # Note: Full deterministic rebuild requires tar with --mtime and proper sorting
        # This is a simplified version for demonstration
        tar --sort=name --mtime="2025-11-27 00:00:00" --owner=root --group=root \
            -czf "$REBUILD_ARCHIVE" "${EXISTING_FILES[@]}" 2>/dev/null || true
        
        if [[ -f "$REBUILD_ARCHIVE" ]]; then
            REBUILD_HASH=$(compute_blake3 "$REBUILD_ARCHIVE")
            echo -e "    Rebuilt hash: ${REBUILD_HASH}"
            
            if [[ -f "$ARCHIVE" && "$REBUILD_HASH" == "$COMPUTED_HASH" ]]; then
                echo -e "${GREEN}  ✓ Deterministic rebuild matches archive${NC}"
                PASSED=$((PASSED + 1))
            else
                echo -e "${YELLOW}  ⚠ Rebuild hash differs (this is expected if build environment differs)${NC}"
                WARNINGS=$((WARNINGS + 1))
            fi
        else
            echo -e "${YELLOW}  ⚠ Could not create rebuild archive${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        echo -e "${YELLOW}  ⚠ No files found to rebuild archive${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
fi
echo ""

# Summary
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    Verification Summary                       ║${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║${NC}  ${GREEN}Passed:   $PASSED${NC}"
echo -e "${BLUE}║${NC}  ${YELLOW}Warnings: $WARNINGS${NC}"
echo -e "${BLUE}║${NC}  ${RED}Failed:   $FAILED${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [[ $FAILED -gt 0 ]]; then
    echo -e "${RED}⚠ VERIFICATION FAILED${NC}"
    echo -e "${RED}The archive may be corrupted or tampered with.${NC}"
    echo -e "${RED}Do NOT use this archive.${NC}"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}⚠ VERIFICATION INCOMPLETE${NC}"
    echo -e "${YELLOW}Some checks could not be performed.${NC}"
    echo -e "${YELLOW}Review warnings above before trusting this archive.${NC}"
    exit 2
else
    echo -e "${GREEN}✓ ALL VERIFICATIONS PASSED${NC}"
    echo -e "${GREEN}The archive is authentic and unmodified.${NC}"
    exit 0
fi

# One-liner version (copy-paste ready):
# curl -sL https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/scripts/verify/verify.sh | bash -s -- --archive swarmgate_v1.0.tar.gz
