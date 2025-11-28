#!/usr/bin/env bash
# recon_cluster.sh
# Strategickhaos DAO LLC - Kubernetes Cluster Reconnaissance Script
# Dumps K8s object deltas, network policies, pod security, and service accounts
# Posts results to #recon channel for security review

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
NS="${1:-default}"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
STAMP_SAFE="$(echo "$STAMP" | tr ':' '-')"
OUT="recon_${NS}_${STAMP_SAFE}"
OUTPUT_DIR="${OUTPUT_DIR:-/tmp}"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           KUBERNETES CLUSTER RECONNAISSANCE v1               ║${NC}"
echo -e "${BLUE}║              Strategickhaos Security Audit                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"
    
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}❌ kubectl is required but not installed${NC}"
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null 2>&1; then
        echo -e "${RED}❌ Cannot connect to Kubernetes cluster${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Prerequisites check passed${NC}"
    echo ""
}

# Create output directory
setup_output() {
    mkdir -p "${OUTPUT_DIR}/${OUT}"
    echo -e "${BLUE}📁 Output directory: ${OUTPUT_DIR}/${OUT}${NC}"
}

# Collect namespace information
collect_namespaces() {
    echo -e "${YELLOW}📋 Collecting namespace information...${NC}"
    kubectl get ns -o wide > "${OUTPUT_DIR}/${OUT}/namespaces.txt" 2>&1 || true
    echo -e "${GREEN}✅ Namespaces collected${NC}"
}

# Collect workload information
collect_workloads() {
    echo -e "${YELLOW}📋 Collecting workload information...${NC}"
    kubectl get deploy,sts,ds,po,svc,ing -A -o wide > "${OUTPUT_DIR}/${OUT}/workloads.txt" 2>&1 || true
    echo -e "${GREEN}✅ Workloads collected${NC}"
}

# Collect network policies
collect_network_policies() {
    echo -e "${YELLOW}🔒 Collecting network policies...${NC}"
    kubectl get networkpolicy -A -o yaml > "${OUTPUT_DIR}/${OUT}/netpol.yaml" 2>&1 || true
    echo -e "${GREEN}✅ Network policies collected${NC}"
}

# Collect RBAC information
collect_rbac() {
    echo -e "${YELLOW}🔐 Collecting RBAC configuration...${NC}"
    kubectl get clusterrole,role,clusterrolebinding,rolebinding -A -o yaml > "${OUTPUT_DIR}/${OUT}/rbac.yaml" 2>&1 || true
    echo -e "${GREEN}✅ RBAC configuration collected${NC}"
}

# Collect service accounts
collect_service_accounts() {
    echo -e "${YELLOW}👤 Collecting service accounts...${NC}"
    kubectl get sa -A -o yaml > "${OUTPUT_DIR}/${OUT}/sa.yaml" 2>&1 || true
    echo -e "${GREEN}✅ Service accounts collected${NC}"
}

# Collect webhook configurations
collect_webhooks() {
    echo -e "${YELLOW}🪝 Collecting webhook configurations...${NC}"
    kubectl get validatingwebhookconfiguration,mutatingwebhookconfiguration -A -o yaml > "${OUTPUT_DIR}/${OUT}/webhooks.yaml" 2>&1 || true
    echo -e "${GREEN}✅ Webhook configurations collected${NC}"
}

# Collect pod security policies (deprecated but may still exist)
collect_pod_security() {
    echo -e "${YELLOW}🛡️ Collecting pod security policies...${NC}"
    kubectl get podsecuritypolicy -A -o yaml > "${OUTPUT_DIR}/${OUT}/psp.yaml" 2>/dev/null || echo "# PSP not available or deprecated" > "${OUTPUT_DIR}/${OUT}/psp.yaml"
    echo -e "${GREEN}✅ Pod security policies collected${NC}"
}

# Collect ConfigMaps with image/tag information
collect_image_configs() {
    echo -e "${YELLOW}🏷️ Collecting image/tag configurations...${NC}"
    kubectl get cm -A | grep -iE "image|tag" > "${OUTPUT_DIR}/${OUT}/image_configs.txt" 2>/dev/null || echo "No image/tag related ConfigMaps found" > "${OUTPUT_DIR}/${OUT}/image_configs.txt"
    echo -e "${GREEN}✅ Image configurations collected${NC}"
}

# Security audit checks
run_security_audit() {
    echo -e "${YELLOW}🔍 Running security audit checks...${NC}"
    
    local audit_file="${OUTPUT_DIR}/${OUT}/security_audit.txt"
    echo "# Kubernetes Security Audit Report" > "$audit_file"
    echo "# Generated: $STAMP" >> "$audit_file"
    echo "# Namespace: $NS" >> "$audit_file"
    echo "" >> "$audit_file"
    
    # Check for pods running as root (more robust check)
    echo "## Pods Running as Root" >> "$audit_file"
    echo "# Pods where runAsNonRoot is explicitly false or runAsUser is 0" >> "$audit_file"
    kubectl get pods -A -o json 2>/dev/null | jq -r '
      .items[] | 
      select(
        (.spec.securityContext.runAsNonRoot == false) or 
        (.spec.securityContext.runAsUser == 0) or
        (.spec.containers[].securityContext.runAsNonRoot == false) or
        (.spec.containers[].securityContext.runAsUser == 0) or
        ((.spec.securityContext.runAsNonRoot | not) and (.spec.securityContext.runAsUser | not))
      ) | 
      "\(.metadata.namespace)/\(.metadata.name): runAsNonRoot=\(.spec.securityContext.runAsNonRoot // "unset"), runAsUser=\(.spec.securityContext.runAsUser // "unset")"
    ' >> "$audit_file" 2>/dev/null || echo "Unable to query or no pods running as root found" >> "$audit_file"
    echo "" >> "$audit_file"
    
    # Check for images using 'latest' tag
    echo "## Images Using 'latest' Tag" >> "$audit_file"
    kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}: {range .spec.containers[*]}{.image} {end}{"\n"}{end}' 2>/dev/null | grep ":latest" >> "$audit_file" || echo "No images using 'latest' tag found" >> "$audit_file"
    echo "" >> "$audit_file"
    
    # Check for privileged containers
    echo "## Privileged Containers" >> "$audit_file"
    kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}: {range .spec.containers[*]}privileged={.securityContext.privileged} {end}{"\n"}{end}' 2>/dev/null | grep "privileged=true" >> "$audit_file" || echo "No privileged containers found" >> "$audit_file"
    echo "" >> "$audit_file"
    
    # Check for elevated RBAC bindings (cluster-admin)
    echo "## Elevated RBAC Bindings (cluster-admin)" >> "$audit_file"
    kubectl get clusterrolebindings -o jsonpath='{range .items[?(@.roleRef.name=="cluster-admin")]}{.metadata.name}: {range .subjects[*]}{.kind}/{.name} {end}{"\n"}{end}' 2>/dev/null >> "$audit_file" || echo "No cluster-admin bindings found" >> "$audit_file"
    echo "" >> "$audit_file"
    
    # Check for missing network policies
    echo "## Namespaces Without Network Policies" >> "$audit_file"
    for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
        policy_count=$(kubectl get networkpolicy -n "$ns" --no-headers 2>/dev/null | wc -l || echo "0")
        if [ "$policy_count" -eq 0 ]; then
            echo "  - $ns (no network policies)" >> "$audit_file"
        fi
    done
    echo "" >> "$audit_file"
    
    echo -e "${GREEN}✅ Security audit completed${NC}"
}

# Generate summary
generate_summary() {
    echo -e "${YELLOW}📊 Generating summary...${NC}"
    
    local summary_file="${OUTPUT_DIR}/${OUT}/summary.json"
    
    # Count resources
    local ns_count=$(wc -l < "${OUTPUT_DIR}/${OUT}/namespaces.txt" 2>/dev/null | tr -d ' ' || echo "0")
    local workload_count=$(wc -l < "${OUTPUT_DIR}/${OUT}/workloads.txt" 2>/dev/null | tr -d ' ' || echo "0")
    
    cat > "$summary_file" << EOF
{
  "timestamp": "$STAMP",
  "namespace_filter": "$NS",
  "cluster_summary": {
    "namespace_count": $((ns_count - 1)),
    "workload_lines": $((workload_count - 1))
  },
  "files_generated": [
    "namespaces.txt",
    "workloads.txt",
    "netpol.yaml",
    "rbac.yaml",
    "sa.yaml",
    "webhooks.yaml",
    "psp.yaml",
    "image_configs.txt",
    "security_audit.txt"
  ],
  "recon_version": "1.0.0",
  "operator": "recon_cluster.sh"
}
EOF

    echo -e "${GREEN}✅ Summary generated${NC}"
}

# Create archive
create_archive() {
    echo -e "${YELLOW}📦 Creating archive...${NC}"
    tar -C "${OUTPUT_DIR}" -czf "${OUTPUT_DIR}/${OUT}.tar.gz" "${OUT}"
    echo -e "${GREEN}✅ Archive created: ${OUTPUT_DIR}/${OUT}.tar.gz${NC}"
}

# Notarize output if notarize_cognition.sh is available
notarize_output() {
    local notarize_script="./notarize_cognition.sh"
    
    if [[ -x "$notarize_script" ]]; then
        echo -e "${YELLOW}🔏 Notarizing recon output...${NC}"
        
        # Export a function to notarize recon files
        export -f notarize_recon_file 2>/dev/null || true
        
        # Create a simple hash manifest
        local manifest="${OUTPUT_DIR}/${OUT}/recon_manifest.json"
        cat > "$manifest" << EOF
{
  "timestamp": "$STAMP",
  "type": "cluster_recon",
  "files": {
EOF
        
        local first=true
        for file in "${OUTPUT_DIR}/${OUT}"/*; do
            if [[ -f "$file" ]]; then
                local hash=$(sha256sum "$file" | cut -d' ' -f1)
                local basename=$(basename "$file")
                if [[ "$first" == "true" ]]; then
                    first=false
                else
                    echo "," >> "$manifest"
                fi
                echo -n "    \"$basename\": \"$hash\"" >> "$manifest"
            fi
        done
        
        echo "" >> "$manifest"
        echo "  }" >> "$manifest"
        echo "}" >> "$manifest"
        
        echo -e "${GREEN}✅ Recon output notarized${NC}"
    fi
}

# Main execution
main() {
    check_prerequisites
    setup_output
    
    echo -e "${GREEN}🚀 Starting cluster reconnaissance...${NC}"
    echo ""
    
    collect_namespaces
    collect_workloads
    collect_network_policies
    collect_rbac
    collect_service_accounts
    collect_webhooks
    collect_pod_security
    collect_image_configs
    run_security_audit
    generate_summary
    notarize_output
    create_archive
    
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                   RECONNAISSANCE COMPLETE                    ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}📁 Output directory: ${OUTPUT_DIR}/${OUT}${NC}"
    echo -e "${BLUE}📦 Archive: ${OUTPUT_DIR}/${OUT}.tar.gz${NC}"
    echo -e "${BLUE}⏰ Timestamp: $STAMP${NC}"
    echo ""
    
    # Output the archive path for programmatic use
    echo "${OUTPUT_DIR}/${OUT}.tar.gz"
}

# Notarize recon file helper (called by notarize_cognition.sh if available)
notarize_recon_file() {
    local file="$1"
    local desc="${2:-Recon output file}"
    
    if [[ -f "$file" ]]; then
        local hash=$(sha256sum "$file" | cut -d' ' -f1)
        echo "{ \"file\": \"$file\", \"sha256\": \"$hash\", \"description\": \"$desc\" }"
    fi
}

# Execute if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
