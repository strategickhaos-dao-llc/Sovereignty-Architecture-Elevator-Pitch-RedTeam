#!/bin/bash

# Sovereignty Analysis Workflow Script
# Version: 1.0.0
# Purpose: Automate reverse engineering and sovereignty analysis workflows

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_DIR="${HOME}/obsidian/vault"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONFIG_FILE="${SCRIPT_DIR}/sovereignty_analysis_config.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    local deps=(curl wget jq git python3)
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing dependencies: ${missing[*]}"
        log_info "Install with: sudo apt-get install ${missing[*]}"
        return 1
    fi
    
    log_success "All dependencies installed"
}

# Initialize vault structure
init_vault() {
    log_info "Initializing Obsidian vault structure..."
    
    local dirs=(
        "${VAULT_DIR}/captures/web_pages"
        "${VAULT_DIR}/captures/har_files"
        "${VAULT_DIR}/captures/performance"
        "${VAULT_DIR}/captures/screenshots"
        "${VAULT_DIR}/analysis/reverse_engineering"
        "${VAULT_DIR}/analysis/security"
        "${VAULT_DIR}/analysis/performance"
        "${VAULT_DIR}/analysis/comparisons"
        "${VAULT_DIR}/methodologies/particle_accelerators"
        "${VAULT_DIR}/methodologies/chemical_synthesis"
        "${VAULT_DIR}/methodologies/dna_blocks"
        "${VAULT_DIR}/methodologies/neural_biology"
        "${VAULT_DIR}/credentials"
        "${VAULT_DIR}/metrics/system_metrics"
        "${VAULT_DIR}/metrics/performance_data"
        "${VAULT_DIR}/graphs/relationship_maps"
        "${VAULT_DIR}/templates"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
    done
    
    log_success "Vault structure initialized at ${VAULT_DIR}"
}

# Create analysis templates
create_templates() {
    log_info "Creating analysis templates..."
    
    # Analysis template
    cat > "${VAULT_DIR}/templates/analysis_template.md" <<'EOF'
# Analysis: {{date}}

## Overview
- **Target**: 
- **Type**: 
- **Timestamp**: {{timestamp}}
- **Analyst**: 

## Captured Data
- [ ] HAR Files
- [ ] Screenshots
- [ ] Performance Data
- [ ] Source Code

## Analysis Areas

### Security
- [ ] Authentication mechanisms
- [ ] Authorization controls
- [ ] Data encryption
- [ ] Input validation
- [ ] Security headers

### Performance
- [ ] Page load time
- [ ] Resource sizes
- [ ] Number of requests
- [ ] Caching strategy
- [ ] Bottlenecks

### Functionality
- [ ] Core features identified
- [ ] Dependencies mapped
- [ ] APIs documented
- [ ] Data flows traced

## Findings
### Critical
- 

### High
- 

### Medium
- 

### Low
- 

## Recommendations
1. 
2. 
3. 

## Next Steps
- [ ] 
- [ ] 
- [ ] 

## References
- [[Related Analysis]]
- [[Methodology Document]]

---
Tags: #analysis #security #performance
EOF

    # Capture template
    cat > "${VAULT_DIR}/templates/capture_template.md" <<'EOF'
# Capture: {{date}}

## Target Information
- **URL**: 
- **Domain**: 
- **IP Address**: 
- **Technology Stack**: 

## Capture Details
- **Timestamp**: {{timestamp}}
- **Method**: 
- **Tools Used**: 
- **Duration**: 

## Files Captured
- HAR File: [[captures/har_files/{{timestamp}}.har]]
- Screenshots: [[captures/screenshots/{{timestamp}}/]]
- Performance: [[captures/performance/{{timestamp}}.json]]

## Initial Observations
### Network
- Total Requests: 
- Total Size: 
- Load Time: 

### Security
- HTTPS: 
- Security Headers: 
- Cookies: 

### Technologies Detected
- Frontend: 
- Backend: 
- APIs: 
- CDNs: 

## Next Actions
- [ ] Detailed analysis
- [ ] Security assessment
- [ ] Performance review
- [ ] Documentation

---
Tags: #capture #reconnaissance
EOF

    # Methodology template
    cat > "${VAULT_DIR}/templates/methodology_template.md" <<'EOF'
# Methodology: {{name}}

## Purpose
Describe the purpose of this methodology.

## Scope
Define what systems or domains this applies to.

## Prerequisites
- 
- 
- 

## Phases

### Phase 1: Discovery
**Objective**: 
**Activities**:
- 
- 

**Outputs**:
- 
- 

### Phase 2: Analysis
**Objective**: 
**Activities**:
- 
- 

**Outputs**:
- 
- 

### Phase 3: Implementation
**Objective**: 
**Activities**:
- 
- 

**Outputs**:
- 
- 

### Phase 4: Verification
**Objective**: 
**Activities**:
- 
- 

**Outputs**:
- 
- 

## Tools Required
- 
- 

## Success Criteria
- 
- 

## Risk Mitigation
### Legal
- 

### Technical
- 

### Security
- 

## References
- 

---
Tags: #methodology
EOF

    log_success "Templates created"
}

# Capture web page with HAR file
capture_web() {
    local url="${1:-}"
    
    if [ -z "$url" ]; then
        log_error "Usage: $0 capture <url>"
        return 1
    fi
    
    log_info "Capturing web page: $url"
    
    local capture_dir="${VAULT_DIR}/captures/${TIMESTAMP}"
    mkdir -p "$capture_dir"
    
    # Download page
    log_info "Downloading page..."
    wget --mirror --convert-links --page-requisites \
         --no-parent --directory-prefix="$capture_dir" \
         --user-agent="SovereigntyBot/1.0" \
         "$url" 2>&1 | tee "${capture_dir}/wget.log"
    
    # Extract domain for organization
    local domain=$(echo "$url" | awk -F/ '{print $3}')
    
    # Create analysis note
    cat > "${capture_dir}/analysis.md" <<EOF
# Web Capture Analysis

## Target
- URL: $url
- Domain: $domain
- Timestamp: $TIMESTAMP

## Captured Files
- Location: [[captures/${TIMESTAMP}/]]
- Log: [[captures/${TIMESTAMP}/wget.log]]

## Analysis Tasks
- [ ] Review HTML structure
- [ ] Analyze JavaScript
- [ ] Check security headers
- [ ] Map API endpoints
- [ ] Document data flows

## Security Checklist
- [ ] HTTPS enabled
- [ ] Security headers present
- [ ] Authentication mechanism
- [ ] Session management
- [ ] Input validation

## Performance Checklist
- [ ] Page load time
- [ ] Resource optimization
- [ ] Caching strategy
- [ ] CDN usage

## Next Steps
- [ ] Deep analysis
- [ ] Recreate core functionality
- [ ] Security improvements
- [ ] Performance optimization

---
Tags: #capture #web #${domain}
Created: $(date)
EOF
    
    log_success "Web page captured to: $capture_dir"
    log_info "Analysis note created: ${capture_dir}/analysis.md"
}

# Analyze HAR file
analyze_har() {
    local har_file="${1:-}"
    
    if [ -z "$har_file" ] || [ ! -f "$har_file" ]; then
        log_error "Usage: $0 analyze-har <har-file>"
        return 1
    fi
    
    log_info "Analyzing HAR file: $har_file"
    
    local output_dir="${VAULT_DIR}/analysis/performance/${TIMESTAMP}"
    mkdir -p "$output_dir"
    
    # Extract URLs
    log_info "Extracting URLs..."
    jq -r '.log.entries[].request.url' "$har_file" > "${output_dir}/urls.txt"
    
    # Extract response times
    log_info "Analyzing response times..."
    jq -r '.log.entries[] | "\(.request.url)\t\(.time)"' "$har_file" | \
        sort -t$'\t' -k2 -n -r | head -20 > "${output_dir}/slowest_requests.txt"
    
    # Extract content types
    log_info "Analyzing content types..."
    jq -r '.log.entries[].response.content.mimeType' "$har_file" | \
        sort | uniq -c | sort -rn > "${output_dir}/content_types.txt"
    
    # Extract security headers
    log_info "Checking security headers..."
    jq -r '.log.entries[].response.headers[] | select(.name | test("(?i)security|x-frame|content-security|strict-transport")) | "\(.name): \(.value)"' \
        "$har_file" | sort -u > "${output_dir}/security_headers.txt"
    
    # Create summary report
    cat > "${output_dir}/har_analysis.md" <<EOF
# HAR File Analysis

## Source
- File: $(basename "$har_file")
- Analysis Date: $(date)
- Output Directory: [[analysis/performance/${TIMESTAMP}/]]

## Statistics
- Total Requests: $(jq '.log.entries | length' "$har_file")
- Total Size: $(jq '[.log.entries[].response.bodySize] | add' "$har_file") bytes
- Unique Domains: $(jq -r '.log.entries[].request.url' "$har_file" | awk -F/ '{print $3}' | sort -u | wc -l)

## Key Findings

### Performance
- Slowest Requests: [[analysis/performance/${TIMESTAMP}/slowest_requests.txt]]
- Average Response Time: $(jq '[.log.entries[].time] | add/length' "$har_file") ms

### Content Analysis
- Content Types: [[analysis/performance/${TIMESTAMP}/content_types.txt]]
- All URLs: [[analysis/performance/${TIMESTAMP}/urls.txt]]

### Security
- Security Headers: [[analysis/performance/${TIMESTAMP}/security_headers.txt]]

## Recommendations
1. Review slowest requests for optimization opportunities
2. Verify all security headers are properly configured
3. Consider consolidating resources to reduce request count
4. Evaluate CDN usage for static assets

## Next Steps
- [ ] Detailed security analysis
- [ ] Performance optimization plan
- [ ] Comparison with sovereign version
- [ ] Documentation update

---
Tags: #har-analysis #performance #security
EOF
    
    log_success "HAR analysis completed: ${output_dir}/har_analysis.md"
}

# Collect educational resources
collect_resources() {
    log_info "Collecting educational resources..."
    
    local resources_dir="${VAULT_DIR}/resources"
    mkdir -p "$resources_dir"
    
    # Security resources
    log_info "Collecting security resources..."
    local security_urls=(
        "https://owasp.org/www-project-top-ten/"
        "https://cwe.mitre.org/top25/"
        "https://www.cisecurity.org/controls/"
    )
    
    for url in "${security_urls[@]}"; do
        local filename=$(echo "$url" | md5sum | cut -d' ' -f1)
        curl -L -s "$url" -o "${resources_dir}/security_${filename}.html" || log_warning "Failed to fetch: $url"
        sleep 1
    done
    
    log_success "Educational resources collected"
}

# Performance comparison
compare_performance() {
    local original="${1:-}"
    local sovereign="${2:-}"
    
    if [ -z "$original" ] || [ -z "$sovereign" ]; then
        log_error "Usage: $0 compare <original-har> <sovereign-har>"
        return 1
    fi
    
    log_info "Comparing performance between original and sovereign versions..."
    
    local output_dir="${VAULT_DIR}/analysis/comparisons/${TIMESTAMP}"
    mkdir -p "$output_dir"
    
    # Compare request counts
    local orig_count=$(jq '.log.entries | length' "$original")
    local sov_count=$(jq '.log.entries | length' "$sovereign")
    
    # Compare total sizes
    local orig_size=$(jq '[.log.entries[].response.bodySize] | add' "$original")
    local sov_size=$(jq '[.log.entries[].response.bodySize] | add' "$sovereign")
    
    # Compare average response times
    local orig_time=$(jq '[.log.entries[].time] | add/length' "$original")
    local sov_time=$(jq '[.log.entries[].time] | add/length' "$sovereign")
    
    # Create comparison report
    cat > "${output_dir}/comparison.md" <<EOF
# Performance Comparison

## Files Compared
- Original: $(basename "$original")
- Sovereign: $(basename "$sovereign")
- Comparison Date: $(date)

## Metrics Comparison

### Request Count
- Original: $orig_count
- Sovereign: $sov_count
- Difference: $((sov_count - orig_count)) ($(awk "BEGIN {print ($sov_count/$orig_count - 1) * 100}")%)

### Total Size (bytes)
- Original: $orig_size
- Sovereign: $sov_size
- Difference: $((sov_size - orig_size)) ($(awk "BEGIN {print ($sov_size/$orig_size - 1) * 100}")%)

### Average Response Time (ms)
- Original: $orig_time
- Sovereign: $sov_time
- Difference: $(awk "BEGIN {print $sov_time - $orig_time}") ($(awk "BEGIN {print ($sov_time/$orig_time - 1) * 100}")%)

## Analysis
### Performance Assessment
$(if (( $(awk "BEGIN {print ($sov_time < $orig_time)}") )); then
    echo "✅ Sovereign version is FASTER"
else
    echo "⚠️ Sovereign version is SLOWER - optimization needed"
fi)

### Resource Efficiency
$(if (( $(awk "BEGIN {print ($sov_size < $orig_size)}") )); then
    echo "✅ Sovereign version uses LESS bandwidth"
else
    echo "⚠️ Sovereign version uses MORE bandwidth"
fi)

## Recommendations
1. $([ $sov_time -gt $orig_time ] && echo "Optimize response times through caching and compression" || echo "Response times are good")
2. $([ $sov_size -gt $orig_size ] && echo "Reduce resource sizes through minification and optimization" || echo "Resource sizes are optimized")
3. Continue monitoring performance in production environment

---
Tags: #comparison #performance #sovereignty
EOF
    
    log_success "Comparison report created: ${output_dir}/comparison.md"
}

# Git workflow integration
git_workflow() {
    local action="${1:-}"
    local message="${2:-Analysis update}"
    
    case "$action" in
        init)
            log_info "Initializing Git repository..."
            cd "$VAULT_DIR"
            git init
            git add .
            git commit -m "Initial vault structure"
            log_success "Git repository initialized"
            ;;
        
        commit)
            log_info "Committing changes..."
            cd "$VAULT_DIR"
            git add .
            git commit -m "$message"
            log_success "Changes committed"
            ;;
        
        branch)
            local branch_name="analysis/${TIMESTAMP}"
            log_info "Creating analysis branch: $branch_name"
            cd "$VAULT_DIR"
            git checkout -b "$branch_name"
            log_success "Branch created: $branch_name"
            ;;
        
        *)
            log_error "Unknown git action: $action"
            log_info "Available actions: init, commit, branch"
            return 1
            ;;
    esac
}

# Show usage
usage() {
    cat <<EOF
Sovereignty Analysis Workflow Script

Usage:
    $0 <command> [options]

Commands:
    init                    Initialize vault structure and templates
    check-deps             Check for required dependencies
    capture <url>          Capture web page with all resources
    analyze-har <file>     Analyze HAR file for performance and security
    compare <orig> <sov>   Compare performance between versions
    resources              Collect educational resources
    git <action> [msg]     Git workflow (init, commit, branch)
    
Examples:
    $0 init
    $0 capture https://example.com
    $0 analyze-har capture.har
    $0 compare original.har sovereign.har
    $0 git branch
    $0 git commit "Analysis of example.com"

Configuration:
    Vault location: ${VAULT_DIR}
    Config file: ${CONFIG_FILE}

For more information, see:
    - REVERSE_ENGINEERING_SOVEREIGNTY_METHODOLOGY.md
    - sovereignty_analysis_config.yaml
EOF
}

# Main function
main() {
    local command="${1:-}"
    
    case "$command" in
        init)
            init_vault
            create_templates
            ;;
        
        check-deps)
            check_dependencies
            ;;
        
        capture)
            shift
            capture_web "$@"
            ;;
        
        analyze-har)
            shift
            analyze_har "$@"
            ;;
        
        compare)
            shift
            compare_performance "$@"
            ;;
        
        resources)
            collect_resources
            ;;
        
        git)
            shift
            git_workflow "$@"
            ;;
        
        help|--help|-h)
            usage
            ;;
        
        *)
            log_error "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
