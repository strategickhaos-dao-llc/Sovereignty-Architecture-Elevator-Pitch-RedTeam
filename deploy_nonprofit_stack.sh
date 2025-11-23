#!/usr/bin/env bash
#
# deploy_nonprofit_stack.sh
# Strategickhaos DAO LLC + Valoryield Nonprofit Arm
#
# Deploy the complete nonprofit stack with cryptographic verification,
# permanent storage, and compliance automation.
#
# Usage:
#   ./deploy_nonprofit_stack.sh [OPTIONS]
#
# Options:
#   --ein EIN                    Employer Identification Number (39-2923503)
#   --jurisdiction TYPE          Wyoming DAO LLC, Texas Foreign LLC
#   --foreign-entity TYPE        Foreign entity registration type
#   --board-minutes-gpg         Enable GPG signing for board minutes
#   --arweave-permanent         Enable permanent Arweave storage
#   --donor-records-sha256      Enable SHA-256 hashing for donor records
#   --audit-monthly             Enable monthly audit scheduling
#   --nodes NODES               Comma-separated node locations
#   --llm-stack MODEL           LLM model name (default: garza-1)
#   --zero-trust                Enable zero-trust architecture
#   --court-ready               Enable court-ready documentation
#   --help                      Show this help message
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
EIN="${EIN:-39-2923503}"
JURISDICTION="wyoming-dao"
FOREIGN_ENTITY="texas-llc"
BOARD_MINUTES_GPG=false
ARWEAVE_PERMANENT=false
DONOR_RECORDS_SHA256=false
AUDIT_MONTHLY=false
NODES="longview-tx,cheyenne-wy"
LLM_STACK="garza-1"
ZERO_TRUST=false
COURT_READY=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --ein)
            EIN="$2"
            shift 2
            ;;
        --jurisdiction)
            JURISDICTION="$2"
            shift 2
            ;;
        --foreign-entity)
            FOREIGN_ENTITY="$2"
            shift 2
            ;;
        --board-minutes-gpg)
            BOARD_MINUTES_GPG=true
            shift
            ;;
        --arweave-permanent)
            ARWEAVE_PERMANENT=true
            shift
            ;;
        --donor-records-sha256)
            DONOR_RECORDS_SHA256=true
            shift
            ;;
        --audit-monthly)
            AUDIT_MONTHLY=true
            shift
            ;;
        --nodes)
            NODES="$2"
            shift 2
            ;;
        --llm-stack)
            LLM_STACK="$2"
            shift 2
            ;;
        --zero-trust)
            ZERO_TRUST=true
            shift
            ;;
        --court-ready)
            COURT_READY=true
            shift
            ;;
        --help)
            grep '^#' "$0" | grep -v '#!/usr/bin/env' | sed 's/^# //'
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to print status messages
info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*"
}

error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Function to check prerequisites
check_prerequisites() {
    info "Checking prerequisites..."
    
    local missing=()
    
    # Check for required commands
    command -v docker >/dev/null 2>&1 || missing+=("docker")
    command -v docker-compose >/dev/null 2>&1 || missing+=("docker-compose")
    
    if [ "$BOARD_MINUTES_GPG" = true ]; then
        command -v gpg >/dev/null 2>&1 || missing+=("gpg")
    fi
    
    if [ "${#missing[@]}" -gt 0 ]; then
        error "Missing required commands: ${missing[*]}"
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Function to configure nonprofit parameters
configure_nonprofit() {
    info "Configuring nonprofit parameters..."
    
    cat > .env.nonprofit <<EOF
# Nonprofit Configuration
# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Organization Details
NONPROFIT_EIN=${EIN}
NONPROFIT_JURISDICTION=${JURISDICTION}
NONPROFIT_FOREIGN_ENTITY=${FOREIGN_ENTITY}
NONPROFIT_501C3_PENDING=true

# Node Configuration
NONPROFIT_NODES=${NODES}
NONPROFIT_PRIMARY_NODE=longview-tx
NONPROFIT_BACKUP_NODE=cheyenne-wy

# LLM Configuration
NONPROFIT_LLM_STACK=${LLM_STACK}
NONPROFIT_LLM_LOCAL=true

# Security Configuration
NONPROFIT_BOARD_MINUTES_GPG=${BOARD_MINUTES_GPG}
NONPROFIT_ARWEAVE_PERMANENT=${ARWEAVE_PERMANENT}
NONPROFIT_DONOR_RECORDS_SHA256=${DONOR_RECORDS_SHA256}
NONPROFIT_ZERO_TRUST=${ZERO_TRUST}

# Compliance Configuration
NONPROFIT_AUDIT_MONTHLY=${AUDIT_MONTHLY}
NONPROFIT_COURT_READY=${COURT_READY}

# Storage Configuration
NONPROFIT_ARWEAVE_GATEWAY=https://arweave.net
NONPROFIT_STORAGE_PRIMARY=/data/nonprofit/primary
NONPROFIT_STORAGE_BACKUP=/data/nonprofit/backup
EOF
    
    success "Nonprofit configuration created: .env.nonprofit"
}

# Function to setup GPG for board minutes
setup_gpg() {
    if [ "$BOARD_MINUTES_GPG" = false ]; then
        return
    fi
    
    info "Setting up GPG signing for board minutes..."
    
    # Check if GPG key exists
    if ! gpg --list-keys "node-137@strategickhaos.dao" >/dev/null 2>&1; then
        warning "GPG key for board minutes signing not found"
        info "Please import or generate GPG key: node-137@strategickhaos.dao"
        info "Example: gpg --gen-key"
    else
        success "GPG key found and ready for board minutes signing"
    fi
}

# Function to setup Arweave connection
setup_arweave() {
    if [ "$ARWEAVE_PERMANENT" = false ]; then
        return
    fi
    
    info "Setting up Arweave permanent storage..."
    
    # Create Arweave config directory
    mkdir -p config/arweave
    
    cat > config/arweave/config.json <<EOF
{
  "gateway": "https://arweave.net",
  "wallet_path": "/keys/arweave/wallet.json",
  "tags": {
    "organization": "Strategickhaos DAO LLC",
    "ein": "${EIN}",
    "type": "nonprofit-governance"
  }
}
EOF
    
    success "Arweave configuration created"
    
    if [ ! -f "/keys/arweave/wallet.json" ]; then
        warning "Arweave wallet not found at /keys/arweave/wallet.json"
        info "Please add Arweave wallet for permanent storage"
    fi
}

# Function to setup donor records security
setup_donor_records() {
    if [ "$DONOR_RECORDS_SHA256" = false ]; then
        return
    fi
    
    info "Setting up donor records security with SHA-256..."
    
    # Create secure storage directories
    mkdir -p data/donor-records/{encrypted,hashes,receipts}
    chmod 700 data/donor-records/encrypted
    
    # Generate encryption key if it doesn't exist
    if [ ! -f "keys/donor-encryption.key" ]; then
        mkdir -p keys
        openssl rand -base64 32 > keys/donor-encryption.key
        chmod 600 keys/donor-encryption.key
        success "Generated donor record encryption key"
    fi
    
    success "Donor records security configured"
}

# Function to setup audit scheduling
setup_audits() {
    if [ "$AUDIT_MONTHLY" = false ]; then
        return
    fi
    
    info "Setting up monthly audit scheduling..."
    
    # Create audit configuration
    cat > config/audit-schedule.yaml <<EOF
# Monthly Audit Schedule
# Strategickhaos DAO LLC + Valoryield Nonprofit Arm

audits:
  board_minutes:
    frequency: monthly
    day: 1
    time: "09:00"
    checks:
      - all_meetings_have_minutes
      - all_minutes_gpg_signed
      - all_minutes_on_arweave
      - signature_verification
  
  donor_records:
    frequency: monthly
    day: 1
    time: "10:00"
    checks:
      - all_donations_hashed
      - hash_verification
      - receipt_generation
      - privacy_compliance
  
  financial:
    frequency: monthly
    day: 1
    time: "11:00"
    checks:
      - reconciliation
      - compliance_check
      - reporting_status
  
  security:
    frequency: monthly
    day: 1
    time: "12:00"
    checks:
      - access_logs_review
      - encryption_status
      - key_rotation_check
      - vulnerability_scan

notifications:
  email: audit@strategickhaos.dao
  discord: "#audit-reports"
  arweave: true
EOF
    
    success "Monthly audit schedule configured"
}

# Function to setup LLM stack
setup_llm() {
    info "Setting up LLM stack: ${LLM_STACK}..."
    
    # Create LLM configuration
    cat > config/llm-config.yaml <<EOF
# LLM Configuration
# Strategickhaos DAO LLC + Valoryield Nonprofit Arm

llm:
  model: ${LLM_STACK}
  local: true
  
  capabilities:
    - board_minutes_generation
    - compliance_checking
    - donor_communication
    - report_generation
  
  security:
    zero_trust: ${ZERO_TRUST}
    no_external_api: true
    local_inference_only: true
  
  board_minutes:
    template: templates/board_minutes_template.md
    auto_format: true
    legal_compliance: true
  
  donor_communications:
    template: templates/donor_receipt_template.md
    personalization: true
    privacy_preserving: true
EOF
    
    success "LLM stack configured: ${LLM_STACK}"
}

# Function to deploy services
deploy_services() {
    info "Deploying nonprofit stack services..."
    
    # Source environment files
    [ -f .env ] && source .env
    [ -f .env.nonprofit ] && source .env.nonprofit
    
    # Deploy with docker-compose
    if [ -f docker-compose.nonprofit.yml ]; then
        docker-compose -f docker-compose.yml -f docker-compose.nonprofit.yml up -d
    else
        docker-compose up -d
    fi
    
    success "Services deployed successfully"
}

# Function to verify deployment
verify_deployment() {
    info "Verifying deployment..."
    
    local checks=0
    local passed=0
    
    # Check Docker services
    checks=$((checks + 1))
    if docker-compose ps | grep -q "Up"; then
        success "Docker services are running"
        passed=$((passed + 1))
    else
        error "Docker services are not running properly"
    fi
    
    # Check GPG configuration
    if [ "$BOARD_MINUTES_GPG" = true ]; then
        checks=$((checks + 1))
        if gpg --list-keys "node-137@strategickhaos.dao" >/dev/null 2>&1; then
            success "GPG signing configured"
            passed=$((passed + 1))
        else
            warning "GPG signing needs manual setup"
        fi
    fi
    
    # Check Arweave configuration
    if [ "$ARWEAVE_PERMANENT" = true ]; then
        checks=$((checks + 1))
        if [ -f "config/arweave/config.json" ]; then
            success "Arweave configuration present"
            passed=$((passed + 1))
        else
            warning "Arweave configuration incomplete"
        fi
    fi
    
    # Check donor records
    if [ "$DONOR_RECORDS_SHA256" = true ]; then
        checks=$((checks + 1))
        if [ -f "keys/donor-encryption.key" ]; then
            success "Donor records encryption configured"
            passed=$((passed + 1))
        else
            warning "Donor records encryption needs setup"
        fi
    fi
    
    echo ""
    info "Verification complete: ${passed}/${checks} checks passed"
}

# Function to display deployment summary
display_summary() {
    echo ""
    echo "========================================"
    echo "  Nonprofit Stack Deployment Summary"
    echo "========================================"
    echo ""
    echo "Organization: Strategickhaos DAO LLC + Valoryield Nonprofit Arm"
    echo "EIN: ${EIN}"
    echo "Jurisdiction: ${JURISDICTION}"
    echo "Foreign Entity: ${FOREIGN_ENTITY}"
    echo ""
    echo "Configuration:"
    echo "  - Board Minutes GPG: ${BOARD_MINUTES_GPG}"
    echo "  - Arweave Permanent: ${ARWEAVE_PERMANENT}"
    echo "  - Donor Records SHA-256: ${DONOR_RECORDS_SHA256}"
    echo "  - Monthly Audits: ${AUDIT_MONTHLY}"
    echo "  - LLM Stack: ${LLM_STACK}"
    echo "  - Zero Trust: ${ZERO_TRUST}"
    echo "  - Court Ready: ${COURT_READY}"
    echo ""
    echo "Nodes: ${NODES}"
    echo ""
    echo "Next Steps:"
    echo "  1. Review configuration files in config/"
    echo "  2. Setup GPG keys if not already configured"
    echo "  3. Add Arweave wallet if using permanent storage"
    echo "  4. Test board minutes generation: ./generate_board_minutes.sh"
    echo "  5. Test donor record processing: ./process_donation.sh"
    echo "  6. Review monthly audit configuration"
    echo ""
    echo "Documentation:"
    echo "  - NONPROFIT_STRUCTURE.md"
    echo "  - legal/nonprofit/BOARD_MINUTES_PROCESS.md"
    echo "  - legal/nonprofit/DONOR_RECORDS_SECURITY.md"
    echo ""
    echo "========================================"
}

# Main deployment flow
main() {
    echo "========================================"
    echo "Nonprofit Stack Deployment"
    echo "Strategickhaos DAO LLC + Valoryield Nonprofit Arm"
    echo "========================================"
    echo ""
    
    check_prerequisites
    configure_nonprofit
    setup_gpg
    setup_arweave
    setup_donor_records
    setup_audits
    setup_llm
    deploy_services
    verify_deployment
    display_summary
    
    success "Deployment complete!"
}

# Run main function
main "$@"
