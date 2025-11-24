#!/usr/bin/env bash
#
# LLM Safety Audit Runner - Bash Version
#
# Interactive script to conduct a comprehensive LLM safety audit based on the 100-point framework.
# Generates client-specific audit reports and evidence vault.
#
# Usage: ./run_audit.sh [CLIENT_NAME] [OUTPUT_DIR]
#
# Version: 1.0
# Author: Strategickhaos Sovereignty Architecture
# Part of: Sovereign LLM Safety & Evidence Vault

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Output functions
print_header() {
    echo -e "\n${CYAN}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}[✓] $1${NC}"
}

print_info() {
    echo -e "${YELLOW}[i] $1${NC}"
}

print_error() {
    echo -e "${RED}[✗] $1${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(dirname "$SCRIPT_DIR")"

# Banner
clear
cat << "EOF"
╔════════════════════════════════════════════════════════════════╗
║   Sovereign LLM Safety & Evidence Vault - Audit Runner        ║
║   Version 1.0                                                  ║
╚════════════════════════════════════════════════════════════════╝
EOF
echo ""

# Parse arguments
CLIENT_NAME="${1:-}"
OUTPUT_DIR="${2:-}"

# Gather client information
if [ -z "$CLIENT_NAME" ]; then
    print_header "Client Information"
    read -p "Enter client name: " CLIENT_NAME
fi

if [ -z "$CLIENT_NAME" ]; then
    print_error "Client name is required."
    exit 1
fi

# Generate engagement ID
DATE_STAMP=$(date +%Y%m%d)
CLIENT_SLUG=$(echo "$CLIENT_NAME" | tr -cd '[:alnum:]' | cut -c1-20)
ENGAGEMENT_ID="ENG-${DATE_STAMP}-${CLIENT_SLUG}"

print_success "Engagement ID: $ENGAGEMENT_ID"

# Setup output directory
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="${VAULT_ROOT}/clients/${CLIENT_NAME}"
fi

if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    print_success "Created output directory: $OUTPUT_DIR"
fi

# Create subdirectories
DOCS_DIR="${OUTPUT_DIR}/docs"
COMPLIANCE_DIR="${DOCS_DIR}/compliance"
PATENT_DIR="${DOCS_DIR}/patent"

for dir in "$DOCS_DIR" "$COMPLIANCE_DIR" "$PATENT_DIR"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
done

# Collect client information interactively
print_header "Collecting Client Information"

read -p "Primary contact name (press Enter to skip): " PRIMARY_CONTACT
read -p "Contact email (press Enter to skip): " CONTACT_EMAIL
read -p "Brief system description (press Enter to skip): " SYSTEM_DESC

echo ""
print_info "LLM Provider(s) - Select all that apply (comma-separated numbers):"
echo "1. OpenAI"
echo "2. Anthropic"
echo "3. Local/Open Source"
echo "4. Azure OpenAI"
echo "5. Other"
read -p "Selection: " LLM_PROVIDERS

echo ""
print_info "Deployment Type:"
echo "1. Cloud"
echo "2. On-Premises"
echo "3. Hybrid"
echo "4. Edge"
read -p "Selection: " DEPLOYMENT_TYPE

echo ""
print_info "Data Sensitivity Level:"
echo "1. Public"
echo "2. Internal"
echo "3. Confidential"
echo "4. Regulated"
read -p "Selection: " DATA_SENSITIVITY

# Copy and customize templates
print_header "Preparing Audit Documents"

TEMPLATE_CHECKLIST="${VAULT_ROOT}/docs/compliance/AUDIT_CHECKLIST_TEMPLATE.md"
CLIENT_CHECKLIST="${COMPLIANCE_DIR}/AUDIT_RESULTS_${CLIENT_NAME}.md"

if [ -f "$TEMPLATE_CHECKLIST" ]; then
    cp "$TEMPLATE_CHECKLIST" "$CLIENT_CHECKLIST"
    
    # Replace placeholders
    AUDIT_DATE=$(date +%Y-%m-%d)
    sed -i.bak \
        -e "s/\[CLIENT_NAME\]/${CLIENT_NAME}/g" \
        -e "s/\[ENGAGEMENT_ID\]/${ENGAGEMENT_ID}/g" \
        -e "s/\[DATE\]/${AUDIT_DATE}/g" \
        "$CLIENT_CHECKLIST"
    rm -f "${CLIENT_CHECKLIST}.bak"
    
    print_success "Created audit checklist: $CLIENT_CHECKLIST"
else
    print_error "Template checklist not found at: $TEMPLATE_CHECKLIST"
fi

# Copy safety techniques reference
SAFETY_TECH="${VAULT_ROOT}/docs/compliance/100_llm_safety_techniques.md"
CLIENT_SAFETY="${COMPLIANCE_DIR}/100_llm_safety_techniques.md"

if [ -f "$SAFETY_TECH" ]; then
    cp "$SAFETY_TECH" "$CLIENT_SAFETY"
    print_success "Copied safety techniques reference"
fi

# Copy and customize patent template
PATENT_TEMPLATE="${VAULT_ROOT}/docs/patent/APPENDIX_B_SAFETY_TEMPLATE.md"
CLIENT_PATENT="${PATENT_DIR}/APPENDIX_B_SAFETY_${CLIENT_NAME}.md"

if [ -f "$PATENT_TEMPLATE" ]; then
    cp "$PATENT_TEMPLATE" "$CLIENT_PATENT"
    
    # Replace placeholders
    sed -i.bak \
        -e "s/\[CLIENT_NAME\]/${CLIENT_NAME}/g" \
        -e "s/\[DATE\]/${AUDIT_DATE}/g" \
        "$CLIENT_PATENT"
    rm -f "${CLIENT_PATENT}.bak"
    
    print_success "Created patent documentation template"
fi

# Create client README
CLIENT_README="${OUTPUT_DIR}/README.md"
cat > "$CLIENT_README" << EOF
# LLM Safety Audit - ${CLIENT_NAME}

**Engagement ID**: ${ENGAGEMENT_ID}  
**Audit Date**: $(date +%Y-%m-%d)  
**Auditor**: Strategickhaos Sovereignty Architecture

---

## Audit Package Contents

This directory contains your complete LLM Safety & Evidence Vault:

### 📋 Compliance Documentation
- **docs/compliance/AUDIT_RESULTS_${CLIENT_NAME}.md** - Your completed 100-point safety audit
- **docs/compliance/100_llm_safety_techniques.md** - Complete safety framework reference

### 📄 Patent & IP Documentation
- **docs/patent/APPENDIX_B_SAFETY_${CLIENT_NAME}.md** - Technical specifications for patent/IP use

### 📊 Dashboards & Monitoring (if applicable)
- Grafana dashboard configurations
- Alert rule templates
- Monitoring setup guides

---

## Next Steps

1. **Review the Audit Results**: Open \`docs/compliance/AUDIT_RESULTS_${CLIENT_NAME}.md\`
2. **Prioritize Findings**: Focus on Critical and High priority items first
3. **Implement Remediations**: Follow the 30/60/90 day roadmap
4. **Re-audit**: Schedule follow-up assessment after remediation

---

## Using This Documentation

### For Investors & Due Diligence
- Share the audit results as evidence of security posture
- Highlight improvements made since initial assessment
- Demonstrate commitment to LLM safety

### For Compliance & Legal
- Use as supporting evidence for regulatory compliance
- Include in SOC 2, ISO 27001, or other certification processes
- Provide to legal counsel for risk assessment

### For Patent Applications
- Customize the Appendix B template with your specific implementations
- Review with patent counsel before filing
- Document novel safety innovations

---

## Support

For questions or follow-up engagements:
- **Email**: contact@strategickhaos.com
- **Documentation**: See included framework documents
- **Re-audit**: Contact us for quarterly or annual re-assessments

---

**Confidential & Proprietary**  
This audit package is confidential to ${CLIENT_NAME} and Strategickhaos Sovereignty Architecture.  
Generated: $(date '+%Y-%m-%d %H:%M:%S')
EOF

print_success "Created client README"

# Generate metadata JSON
METADATA_FILE="${OUTPUT_DIR}/audit_metadata.json"
cat > "$METADATA_FILE" << EOF
{
  "clientName": "${CLIENT_NAME}",
  "engagementID": "${ENGAGEMENT_ID}",
  "auditDate": "$(date +%Y-%m-%d)",
  "auditor": "Strategickhaos Sovereignty Architecture",
  "primaryContact": "${PRIMARY_CONTACT:-}",
  "contactEmail": "${CONTACT_EMAIL:-}",
  "systemDescription": "${SYSTEM_DESC:-}",
  "llmProviders": "${LLM_PROVIDERS:-}",
  "deploymentType": "${DEPLOYMENT_TYPE:-}",
  "dataSensitivity": "${DATA_SENSITIVITY:-}",
  "generatedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

print_success "Saved audit metadata"

# Final summary
print_header "Audit Preparation Complete"
echo ""
print_success "Client vault created at: $OUTPUT_DIR"
print_info "Next steps:"
echo "  1. Complete the audit checklist: $CLIENT_CHECKLIST"
echo "  2. Review findings with client"
echo "  3. Generate final report using generate_report.py"
echo "  4. Deliver evidence vault to client"
echo ""

# Ask if user wants to open the checklist
read -p "Open the audit checklist now? (y/n): " OPEN_FILE

if [[ "$OPEN_FILE" =~ ^[Yy]$ ]]; then
    # Try to open with available editor
    if command -v code &> /dev/null; then
        code "$CLIENT_CHECKLIST"
    elif command -v vim &> /dev/null; then
        vim "$CLIENT_CHECKLIST"
    elif command -v nano &> /dev/null; then
        nano "$CLIENT_CHECKLIST"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "$CLIENT_CHECKLIST"
    else
        print_info "Please open this file manually: $CLIENT_CHECKLIST"
    fi
fi

echo ""
print_success "Audit runner completed successfully!"
echo ""
