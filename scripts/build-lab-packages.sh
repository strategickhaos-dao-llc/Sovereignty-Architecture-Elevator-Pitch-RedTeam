#!/bin/bash
#
# Build Lab Packages Script
# Creates both real and honeypot lab distributions
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${PROJECT_ROOT}/invite-html"
TEMP_DIR="/tmp/lab-build-$$"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔨 Building Lab Packages${NC}"
echo "Project Root: ${PROJECT_ROOT}"
echo "Output Dir: ${OUTPUT_DIR}"
echo ""

# Create temp directory
mkdir -p "${TEMP_DIR}"
trap "rm -rf ${TEMP_DIR}" EXIT

# Function to create real lab package
build_real_lab() {
    echo -e "${YELLOW}📦 Building real-lab.zip...${NC}"
    
    cd "${PROJECT_ROOT}"
    
    # Create archive with all necessary files
    zip -r "${TEMP_DIR}/real-lab.zip" \
        docker-compose.yml \
        docker-compose-*.yml \
        .env.example \
        README.md \
        README-*.md \
        DEPLOYMENT.md \
        SECURITY.md \
        LICENSE \
        Dockerfile.* \
        scripts/ \
        src/ \
        monitoring/ \
        bootstrap/ \
        templates/ \
        *.yaml \
        *.yml \
        -x "*.git*" \
        -x "node_modules/*" \
        -x "logs/*" \
        -x "invite-html/*" \
        -x "honeypot-*/*" \
        -x "logger-script/*" \
        -x "*/target/*" \
        -x "*.log" \
        > /dev/null
    
    # Move to output directory
    mv "${TEMP_DIR}/real-lab.zip" "${OUTPUT_DIR}/"
    
    echo -e "${GREEN}✅ real-lab.zip created${NC}"
    ls -lh "${OUTPUT_DIR}/real-lab.zip"
}

# Function to create honeypot lab package
build_honeypot_lab() {
    echo -e "${YELLOW}📦 Building honeypot-lab.zip...${NC}"
    
    # Create honeypot working directory
    HONEYPOT_DIR="${TEMP_DIR}/honeypot-lab"
    mkdir -p "${HONEYPOT_DIR}"
    
    # Copy base files
    cd "${PROJECT_ROOT}"
    cp docker-compose.yml "${HONEYPOT_DIR}/"
    cp docker-compose-honeypot.yml "${HONEYPOT_DIR}/"
    cp .env.example "${HONEYPOT_DIR}/"
    cp README.md "${HONEYPOT_DIR}/"
    cp LICENSE "${HONEYPOT_DIR}/"
    
    # Copy beacon script as the startup script
    cp honeypot-repos/start.sh "${HONEYPOT_DIR}/"
    chmod +x "${HONEYPOT_DIR}/start.sh"
    
    # Add steganographic watermark identifier (less visible)
    # Embed tracking ID in docker-compose comment at a random line position
    local tracking_id="HONEYPOT_$(date +%s)_$(openssl rand -hex 8)"
    sed -i "5i# Container tracking: ${tracking_id}" "${HONEYPOT_DIR}/docker-compose.yml"
    
    # Also embed in a binary-safe location (checksums file signature)
    echo "# Package signature: ${tracking_id}" > "${HONEYPOT_DIR}/.pkg_id"
    
    # Create modified docker-compose with tracking labels
    cat >> "${HONEYPOT_DIR}/docker-compose.yml.tracking" << 'EOF'
# Tracking labels - DO NOT REMOVE
labels:
  - "com.strategickhaos.tracking=enabled"
  - "com.strategickhaos.build_type=honeypot"
  - "com.strategickhaos.build_time=${BUILD_TIME}"
EOF
    
    # Create the package
    cd "${HONEYPOT_DIR}"
    zip -r "${TEMP_DIR}/honeypot-lab.zip" . > /dev/null
    
    # Move to output directory
    mv "${TEMP_DIR}/honeypot-lab.zip" "${OUTPUT_DIR}/"
    
    echo -e "${GREEN}✅ honeypot-lab.zip created${NC}"
    ls -lh "${OUTPUT_DIR}/honeypot-lab.zip"
}

# Function to generate checksums
generate_checksums() {
    echo -e "${YELLOW}🔐 Generating checksums...${NC}"
    
    cd "${OUTPUT_DIR}"
    sha256sum *.zip > checksums.txt
    
    echo -e "${GREEN}✅ Checksums generated${NC}"
    cat checksums.txt
}

# Main execution
main() {
    echo -e "${GREEN}Starting build process...${NC}"
    echo ""
    
    # Ensure output directory exists
    mkdir -p "${OUTPUT_DIR}"
    
    # Build packages
    build_real_lab
    echo ""
    build_honeypot_lab
    echo ""
    generate_checksums
    
    echo ""
    echo -e "${GREEN}✅ All packages built successfully!${NC}"
    echo ""
    echo "Packages available at:"
    echo "  - ${OUTPUT_DIR}/real-lab.zip"
    echo "  - ${OUTPUT_DIR}/honeypot-lab.zip"
    echo "  - ${OUTPUT_DIR}/checksums.txt"
}

# Run main function
main
