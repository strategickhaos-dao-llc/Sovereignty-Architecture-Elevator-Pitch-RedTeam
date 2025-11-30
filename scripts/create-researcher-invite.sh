#!/bin/bash
# create-researcher-invite.sh - Generate Tailscale invite for new researcher
# Usage: ./scripts/create-researcher-invite.sh researcher@email.com [wings] [duration]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check arguments
if [ $# -lt 1 ]; then
    echo -e "${RED}Usage: $0 <email> [wings] [duration_days]${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 researcher@example.com"
    echo "  $0 researcher@example.com medical,physics 365"
    echo "  $0 researcher@example.com all 180"
    echo ""
    echo "Available wings:"
    echo "  - medical"
    echo "  - physics_chemistry"
    echo "  - biology_genomics"
    echo "  - forbidden_knowledge (requires vetting)"
    echo "  - tinker_labs (requires explicit grant)"
    echo "  - all (excludes forbidden_knowledge and tinker_labs)"
    exit 1
fi

EMAIL=$1
WINGS=${2:-medical,physics_chemistry,biology_genomics}
DURATION=${3:-365}
RESEARCHER_ID=$(echo -n "$EMAIL" | sha256sum | cut -c1-16)

echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Alexandria Researcher Onboarding       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Validate email
if ! [[ "$EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo -e "${RED}Error: Invalid email address${NC}"
    exit 1
fi

# Check if forbidden_knowledge is requested
if [[ "$WINGS" == *"forbidden_knowledge"* ]]; then
    echo -e "${YELLOW}⚠ Warning: Forbidden Knowledge wing requires personal vetting${NC}"
    echo -e "${YELLOW}   This request must be reviewed by the Librarian${NC}"
    read -p "Have you personally vetted this researcher? (yes/no): " VETTED
    if [ "$VETTED" != "yes" ]; then
        echo -e "${RED}Aborting: Forbidden Knowledge access requires vetting${NC}"
        exit 1
    fi
fi

# Check if tinker_labs is requested
if [[ "$WINGS" == *"tinker_labs"* ]]; then
    echo -e "${YELLOW}⚠ Warning: Tinker Labs is Librarian-only${NC}"
    echo -e "${YELLOW}   This grants access to personal research archives${NC}"
    read -p "Confirm grant access to Tinker Labs? (yes/no): " GRANT_TINKER
    if [ "$GRANT_TINKER" != "yes" ]; then
        WINGS=$(echo "$WINGS" | sed 's/tinker_labs//g' | sed 's/,,/,/g' | sed 's/^,//g' | sed 's/,$//g')
        echo -e "${BLUE}Removed tinker_labs from access list${NC}"
    fi
fi

echo -e "${YELLOW}Creating researcher profile...${NC}"
echo ""
echo "  Email:        $EMAIL"
echo "  ID:           $RESEARCHER_ID"
echo "  Wings:        $WINGS"
echo "  Duration:     $DURATION days"
echo ""

# Create researcher profile in vault (if vault is available)
if command -v vault &> /dev/null && vault status &> /dev/null; then
    echo -e "${BLUE}Storing researcher profile in Vault...${NC}"
    
    vault kv put secret/alexandria/researchers/$RESEARCHER_ID \
        email="$EMAIL" \
        wings="$WINGS" \
        access_level="standard" \
        oath_signed="$(date -I)" \
        expiry="$(date -d "+$DURATION days" -I)" \
        created_by="$USER" \
        created_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    
    echo -e "${GREEN}✓ Researcher profile stored in Vault${NC}"
else
    echo -e "${YELLOW}⚠ Vault not available, storing in local config${NC}"
    
    # Store in local JSON file
    mkdir -p ./data/researchers
    cat > "./data/researchers/$RESEARCHER_ID.json" <<EOF
{
  "researcher_id": "$RESEARCHER_ID",
  "email": "$EMAIL",
  "wings": "$WINGS",
  "access_level": "standard",
  "oath_signed": "$(date -I)",
  "expiry": "$(date -d "+$DURATION days" -I)",
  "created_by": "$USER",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    echo -e "${GREEN}✓ Researcher profile stored locally${NC}"
fi

# Generate Tailscale invite (if tailscale is available)
if command -v tailscale &> /dev/null; then
    echo ""
    echo -e "${BLUE}Generating Tailscale invite...${NC}"
    
    # Create a tag for this researcher
    RESEARCHER_TAG="tag:alexandria-researcher-$RESEARCHER_ID"
    
    echo -e "${YELLOW}To complete Tailscale setup:${NC}"
    echo "1. Go to: https://login.tailscale.com/admin/settings/keys"
    echo "2. Generate an auth key with:"
    echo "   - Reusable: No"
    echo "   - Ephemeral: Yes"
    echo "   - Expiration: $DURATION days"
    echo "   - Tags: $RESEARCHER_TAG"
    echo ""
else
    echo -e "${YELLOW}⚠ Tailscale not available${NC}"
    echo -e "${YELLOW}   Manual VPN setup will be required${NC}"
fi

# Generate oath document
echo ""
echo -e "${BLUE}Generating researcher oath document...${NC}"

mkdir -p ./data/oaths
cat > "./data/oaths/$RESEARCHER_ID-oath.md" <<EOF
# Alexandria Resurrected - Researcher Oath

**Researcher ID:** $RESEARCHER_ID  
**Email:** $EMAIL  
**Date:** $(date -I)  
**Access Duration:** $DURATION days  
**Permitted Wings:** $WINGS

---

## The Oath

I, the undersigned researcher, do solemnly affirm:

### 1. Do No Harm
I will use this knowledge solely for the advancement of science and the benefit of humanity. I will not use this information to cause harm to any person, group, or living being.

### 2. Respect Privacy
I understand that I have access to sensitive research data. I will maintain confidentiality and will not attempt to identify individuals from anonymized datasets.

### 3. Scientific Integrity
I will cite sources properly, maintain research ethics, and contribute to the reproducibility of science. I will not misrepresent findings or manipulate data.

### 4. No Export of Raw Data
I understand that I may access and query this data through the RAG interface, but I may not export, copy, or distribute raw data files. I may keep notes and insights from my research.

### 5. Respect the Architecture
I will not attempt to bypass security measures, access unauthorized wings, or interfere with other researchers' work.

### 6. Report Misuse
If I become aware of misuse of Alexandria resources, I will report it to the Librarian immediately.

### Acknowledgment
I understand that violation of this oath will result in immediate and permanent revocation of access, and may result in legal action if harm results from my misuse.

---

**Signature:** ___________________________  
**Date:** ___________________________

**Librarian Approval:** ___________________________  
**Date:** $(date -I)

---

*"Knowledge preserved, wisdom shared, harm prevented."*
EOF

echo -e "${GREEN}✓ Oath document generated: ./data/oaths/$RESEARCHER_ID-oath.md${NC}"

# Generate welcome email template
cat > "./data/researchers/$RESEARCHER_ID-welcome-email.txt" <<EOF
Subject: Welcome to Alexandria Resurrected

Dear Researcher,

Welcome to Alexandria Resurrected - a sovereign research data library dedicated to preserving and democratizing access to humanity's scientific knowledge.

Your Access Details:
--------------------
Researcher ID: $RESEARCHER_ID
Email: $EMAIL
Permitted Wings: $WINGS
Access Duration: $DURATION days
Expires: $(date -d "+$DURATION days" -I)

Next Steps:
-----------
1. Review and sign the researcher oath (attached)
2. Set up Tailscale VPN access (instructions below)
3. Connect to the RAG interface at: https://alexandria.tailscale
4. Begin your research!

Your Permitted Wings:
---------------------
EOF

# Add wing descriptions based on access
if [[ "$WINGS" == *"medical"* ]]; then
    cat >> "./data/researchers/$RESEARCHER_ID-welcome-email.txt" <<EOF

📚 MEDICAL WING (8.7 TB)
Complete PubMed archive, clinical trial data, 3M+ medical scans,
pharmacology research, and 70+ years of drug candidate studies.

EOF
fi

if [[ "$WINGS" == *"physics_chemistry"* ]]; then
    cat >> "./data/researchers/$RESEARCHER_ID-welcome-email.txt" <<EOF

⚛️ PHYSICS & CHEMISTRY WING (6.2 TB)
Complete arXiv mirror (1991-2025), all patents ever granted,
Los Alamos + CERN data, Soviet-era archives, declassified projects.

EOF
fi

if [[ "$WINGS" == *"biology_genomics"* ]]; then
    cat >> "./data/researchers/$RESEARCHER_ID-welcome-email.txt" <<EOF

🧬 BIOLOGY & GENOMICS WING (5.9 TB)
1000 Genomes, UK Biobank, all sequenced genomes, AlphaFold proteins,
CRISPR research and lab notebooks.

EOF
fi

if [[ "$WINGS" == *"forbidden_knowledge"* ]]; then
    cat >> "./data/researchers/$RESEARCHER_ID-welcome-email.txt" <<EOF

🔒 FORBIDDEN KNOWLEDGE WING (4.1 TB)
Delisted research, retracted papers with provenance, controversial
studies, adverse event databases, declassified documents.
[SPECIAL ACCESS - PERSONAL VETTING REQUIRED]

EOF
fi

cat >> "./data/researchers/$RESEARCHER_ID-welcome-email.txt" <<EOF

Using the RAG Interface:
------------------------
The Alexandria RAG interface provides 128k context windows for
natural language queries. Examples:

- "Show me ivermectin studies from 2020-2021"
- "Compare CRISPR safety protocols across papers"
- "Find abandoned drug candidates for Alzheimer's"
- "Trace the citation history of this retracted paper"

All queries are answered with full citations and source attribution.

Remember: You can access insights and keep notes, but you cannot
export raw data files.

Research Community:
-------------------
You are now part of a community of 27+ active researchers worldwide.
We maintain anonymity between researchers while sharing the common
goal of advancing scientific knowledge.

Questions or Issues:
--------------------
Contact the Librarian through your designated channel.

---

"Alexandria burned once. Never again."

Welcome to the library.

- The Librarian
EOF

echo -e "${GREEN}✓ Welcome email template generated${NC}"

# Display summary
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Researcher Onboarding Complete         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Generated Files:${NC}"
echo "  • Profile: ./data/researchers/$RESEARCHER_ID.json"
echo "  • Oath: ./data/oaths/$RESEARCHER_ID-oath.md"
echo "  • Welcome: ./data/researchers/$RESEARCHER_ID-welcome-email.txt"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Send oath document for signature"
echo "  2. Set up Tailscale access"
echo "  3. Send welcome email with access instructions"
echo ""
echo -e "${GREEN}Researcher ID: $RESEARCHER_ID${NC}"
echo ""
