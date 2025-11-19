#!/bin/bash
# ascension_status.sh - Check and report on 100-Layer Ascension Protocol status
# This script provides a comprehensive status check across all validation methods

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local all_ok=true
    
    # Check for Python
    if command -v python3 &> /dev/null; then
        log_success "Python 3 found: $(python3 --version)"
    else
        log_error "Python 3 not found"
        all_ok=false
    fi
    
    # Check for PowerShell (optional)
    if command -v pwsh &> /dev/null; then
        log_success "PowerShell found: $(pwsh --version | head -1)"
    else
        log_warn "PowerShell not found (optional)"
    fi
    
    # Check for PyYAML
    if python3 -c "import yaml" 2>/dev/null; then
        log_success "PyYAML module found"
    else
        log_error "PyYAML module not found. Install with: pip install pyyaml"
        all_ok=false
    fi
    
    # Check for required files
    local required_files=(
        "$PROJECT_ROOT/100_LAYER_ASCENSION.md"
        "$PROJECT_ROOT/100_layer_config.yaml"
        "$PROJECT_ROOT/final-100-layer-ascension.ps1"
        "$PROJECT_ROOT/scripts/validate_100_layers.py"
    )
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            log_success "Found: $(basename "$file")"
        else
            log_error "Missing: $(basename "$file")"
            all_ok=false
        fi
    done
    
    if [ "$all_ok" = true ]; then
        log_success "All prerequisites met"
        return 0
    else
        log_error "Some prerequisites are missing"
        return 1
    fi
}

# Run Python validation
run_python_validation() {
    print_header "Running Python Validation"
    
    cd "$PROJECT_ROOT"
    
    if python3 scripts/validate_100_layers.py; then
        log_success "Python validation passed"
        return 0
    else
        log_error "Python validation failed"
        return 1
    fi
}

# Run PowerShell validation (if available)
run_powershell_validation() {
    print_header "Running PowerShell Validation"
    
    cd "$PROJECT_ROOT"
    
    if ! command -v pwsh &> /dev/null; then
        log_warn "PowerShell not available, skipping"
        return 0
    fi
    
    if pwsh -File final-100-layer-ascension.ps1 -ValidateOnly; then
        log_success "PowerShell validation passed"
        return 0
    else
        log_error "PowerShell validation failed"
        return 1
    fi
}

# Show layer statistics
show_statistics() {
    print_header "Layer Statistics"
    
    cd "$PROJECT_ROOT"
    
    # Count categories
    local categories=$(grep -c "^  - id:" 100_layer_config.yaml || echo "0")
    log_info "Total Categories: $categories"
    
    # Count layers by status
    local planned=$(grep "status: \"planned\"" 100_layer_config.yaml | wc -l || echo "0")
    local in_progress=$(grep "status: \"in_progress\"" 100_layer_config.yaml | wc -l || echo "0")
    local research=$(grep "status: \"research\"" 100_layer_config.yaml | wc -l || echo "0")
    local complete=$(grep "status: \"complete\"" 100_layer_config.yaml | wc -l || echo "0")
    
    echo ""
    echo "Layer Status Breakdown:"
    echo "  Planned:     $planned layers"
    echo "  In Progress: $in_progress layers"
    echo "  Research:    $research layers"
    echo "  Complete:    $complete layers"
    echo ""
    
    # Count technologies
    local unique_tech=$(grep -o "technology: \[.*\]" 100_layer_config.yaml | sort -u | wc -l || echo "0")
    log_info "Unique technology combinations: $unique_tech"
    
    # Check documentation size
    local doc_lines=$(wc -l < 100_LAYER_ASCENSION.md)
    local doc_size=$(du -h 100_LAYER_ASCENSION.md | cut -f1)
    log_info "Documentation: $doc_lines lines, $doc_size"
}

# Generate reports
generate_reports() {
    print_header "Generating Reports"
    
    cd "$PROJECT_ROOT"
    
    # Generate PowerShell report (if available)
    if command -v pwsh &> /dev/null; then
        log_info "Generating PowerShell report..."
        if pwsh -File final-100-layer-ascension.ps1 -GenerateReport > /dev/null 2>&1; then
            log_success "PowerShell report generated: 100_LAYER_ASCENSION_REPORT.md"
        else
            log_warn "PowerShell report generation failed"
        fi
    fi
}

# Main menu
show_menu() {
    print_header "100-Layer Ascension Protocol - Status Check"
    
    echo "Available actions:"
    echo "  1) Check prerequisites"
    echo "  2) Run Python validation"
    echo "  3) Run PowerShell validation"
    echo "  4) Show statistics"
    echo "  5) Generate reports"
    echo "  6) Run all checks"
    echo "  q) Quit"
    echo ""
}

# Run all checks
run_all_checks() {
    local all_passed=true
    
    if ! check_prerequisites; then
        all_passed=false
    fi
    
    echo ""
    
    if ! run_python_validation; then
        all_passed=false
    fi
    
    echo ""
    
    if ! run_powershell_validation; then
        all_passed=false
    fi
    
    echo ""
    show_statistics
    
    echo ""
    generate_reports
    
    echo ""
    print_header "Summary"
    
    if [ "$all_passed" = true ]; then
        log_success "All checks passed!"
        echo ""
        echo "The 100-Layer Ascension Protocol is properly configured and validated."
        return 0
    else
        log_error "Some checks failed"
        echo ""
        echo "Please review the errors above and fix any issues."
        return 1
    fi
}

# Main execution
main() {
    if [ "$#" -eq 0 ]; then
        # Interactive mode
        while true; do
            show_menu
            read -p "Select action: " choice
            echo ""
            
            case $choice in
                1)
                    check_prerequisites
                    ;;
                2)
                    run_python_validation
                    ;;
                3)
                    run_powershell_validation
                    ;;
                4)
                    show_statistics
                    ;;
                5)
                    generate_reports
                    ;;
                6)
                    run_all_checks
                    break
                    ;;
                q|Q)
                    echo "Exiting..."
                    exit 0
                    ;;
                *)
                    log_error "Invalid choice"
                    ;;
            esac
            echo ""
            read -p "Press Enter to continue..."
        done
    else
        # Command line mode
        case "$1" in
            --check|check)
                check_prerequisites
                ;;
            --validate|validate)
                run_python_validation && run_powershell_validation
                ;;
            --stats|stats)
                show_statistics
                ;;
            --report|report)
                generate_reports
                ;;
            --all|all)
                run_all_checks
                ;;
            --help|help|-h)
                echo "Usage: $0 [command]"
                echo ""
                echo "Commands:"
                echo "  check      - Check prerequisites"
                echo "  validate   - Run validation scripts"
                echo "  stats      - Show statistics"
                echo "  report     - Generate reports"
                echo "  all        - Run all checks"
                echo "  help       - Show this help message"
                echo ""
                echo "If no command is specified, runs in interactive mode."
                ;;
            *)
                log_error "Unknown command: $1"
                echo "Run '$0 help' for usage information"
                exit 1
                ;;
        esac
    fi
}

# Run main function
main "$@"
