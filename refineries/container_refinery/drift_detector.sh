#!/bin/bash
# Drift Detector - Runs every 60 seconds to check container state
# This is the 60-second heartbeat of the immune system

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEDGER_DIR="$SCRIPT_DIR/ledger"
MANIFESTS_DIR="$SCRIPT_DIR/manifests"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[DRIFT]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

# Check Docker containers
check_docker_containers() {
    log_info "Checking Docker containers..."
    
    # Get running containers
    local running_containers=$(docker ps --format '{{.Names}}' 2>/dev/null || echo "")
    
    if [[ -z "$running_containers" ]]; then
        log_info "No Docker containers running"
        return 0
    fi
    
    local drift_count=0
    
    # Check each container
    while IFS= read -r container_name; do
        # Check if container is defined in manifests
        local manifest_file="$MANIFESTS_DIR/docker/${container_name}.yaml"
        
        if [[ ! -f "$manifest_file" ]]; then
            log_warn "UNAUTHORIZED CONTAINER: $container_name (not in git)"
            echo "$(date -Iseconds)|DOCKER|$container_name|UNAUTHORIZED|NOT_IN_GIT" >> "$LEDGER_DIR/drift_events.log"
            drift_count=$((drift_count + 1))
            
            # Auto-terminate if enabled
            if [[ "${AUTO_TERMINATE:-true}" == "true" ]]; then
                log_warn "Auto-terminating unauthorized container: $container_name"
                docker stop "$container_name" >/dev/null 2>&1 || true
                docker rm "$container_name" >/dev/null 2>&1 || true
                echo "$(date -Iseconds)|DOCKER|$container_name|TERMINATED|AUTO_ROLLBACK" >> "$LEDGER_DIR/rollback_actions.log"
            fi
        else
            # Check if image matches manifest
            local actual_image=$(docker inspect --format='{{.Config.Image}}' "$container_name" 2>/dev/null || echo "unknown")
            local expected_image=$(grep "image:" "$manifest_file" | head -1 | awk '{print $2}' || echo "unknown")
            
            if [[ "$actual_image" != "$expected_image" ]]; then
                log_warn "IMAGE DRIFT: $container_name (expected: $expected_image, actual: $actual_image)"
                echo "$(date -Iseconds)|DOCKER|$container_name|IMAGE_DRIFT|$expected_image|$actual_image" >> "$LEDGER_DIR/drift_events.log"
                drift_count=$((drift_count + 1))
            fi
        fi
    done <<< "$running_containers"
    
    if [[ $drift_count -eq 0 ]]; then
        log_success "Docker containers: No drift detected"
    else
        log_warn "Docker containers: $drift_count drift events detected"
    fi
    
    return $drift_count
}

# Check Kubernetes pods
check_kubernetes_pods() {
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        log_info "kubectl not available, skipping Kubernetes checks"
        return 0
    fi
    
    # Check if cluster is accessible
    if ! kubectl cluster-info &> /dev/null; then
        log_info "Kubernetes cluster not accessible, skipping checks"
        return 0
    fi
    
    log_info "Checking Kubernetes pods..."
    
    # Get all pods across all namespaces
    local pods=$(kubectl get pods --all-namespaces -o json 2>/dev/null || echo '{"items":[]}')
    local drift_count=0
    
    # Parse JSON and check each pod
    local pod_count=$(echo "$pods" | jq -r '.items | length')
    
    if [[ "$pod_count" -eq 0 ]]; then
        log_info "No Kubernetes pods running"
        return 0
    fi
    
    log_info "Found $pod_count pods"
    
    # Check for unauthorized pods (not in git manifests)
    for i in $(seq 0 $((pod_count - 1))); do
        local pod_name=$(echo "$pods" | jq -r ".items[$i].metadata.name")
        local namespace=$(echo "$pods" | jq -r ".items[$i].metadata.namespace")
        local manifest_file="$MANIFESTS_DIR/k8s/${namespace}/${pod_name}.yaml"
        
        if [[ ! -f "$manifest_file" ]]; then
            # Check if there's a deployment/statefulset manifest
            local deployment_name=$(echo "$pods" | jq -r ".items[$i].metadata.labels.app // empty")
            if [[ -n "$deployment_name" ]]; then
                manifest_file="$MANIFESTS_DIR/k8s/${namespace}/${deployment_name}.yaml"
            fi
        fi
        
        if [[ ! -f "$manifest_file" ]]; then
            log_warn "UNAUTHORIZED POD: $namespace/$pod_name (not in git)"
            echo "$(date -Iseconds)|K8S|$namespace/$pod_name|UNAUTHORIZED|NOT_IN_GIT" >> "$LEDGER_DIR/drift_events.log"
            drift_count=$((drift_count + 1))
            
            # Auto-terminate if enabled
            if [[ "${AUTO_TERMINATE:-true}" == "true" ]]; then
                log_warn "Auto-terminating unauthorized pod: $namespace/$pod_name"
                kubectl delete pod "$pod_name" -n "$namespace" --grace-period=0 --force >/dev/null 2>&1 || true
                echo "$(date -Iseconds)|K8S|$namespace/$pod_name|TERMINATED|AUTO_ROLLBACK" >> "$LEDGER_DIR/rollback_actions.log"
            fi
        fi
    done
    
    if [[ $drift_count -eq 0 ]]; then
        log_success "Kubernetes pods: No drift detected"
    else
        log_warn "Kubernetes pods: $drift_count drift events detected"
    fi
    
    return $drift_count
}

# Check for missing containers (defined in git but not running)
check_missing_containers() {
    log_info "Checking for missing containers..."
    
    local missing_count=0
    
    # Check Docker compose files
    if [[ -d "$MANIFESTS_DIR/docker" ]]; then
        for manifest in "$MANIFESTS_DIR/docker"/*.yaml; do
            if [[ -f "$manifest" ]]; then
                local container_name=$(basename "$manifest" .yaml)
                
                if ! docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
                    log_warn "MISSING CONTAINER: $container_name (defined in git but not running)"
                    echo "$(date -Iseconds)|DOCKER|$container_name|MISSING|SHOULD_BE_RUNNING" >> "$LEDGER_DIR/drift_events.log"
                    missing_count=$((missing_count + 1))
                fi
            fi
        done
    fi
    
    if [[ $missing_count -eq 0 ]]; then
        log_success "Missing containers: None"
    else
        log_warn "Missing containers: $missing_count"
    fi
    
    return $missing_count
}

# Commit drift events to git
commit_to_git() {
    local drift_count=$1
    
    cd "$SCRIPT_DIR"
    
    # Add ledger files to git
    git add ledger/*.log >/dev/null 2>&1 || true
    
    # Commit if there are changes
    if git diff --staged --quiet; then
        log_info "No changes to commit"
    else
        local commit_msg="Drift detection: $drift_count events at $(date -Iseconds)"
        git commit -m "$commit_msg" >/dev/null 2>&1 || true
        log_success "Committed drift events to git"
    fi
}

# Main drift detection cycle
main() {
    log_info "=== Container Drift Detection Cycle ==="
    
    # Ensure ledger directory exists
    mkdir -p "$LEDGER_DIR"
    mkdir -p "$MANIFESTS_DIR/docker"
    mkdir -p "$MANIFESTS_DIR/k8s"
    
    # Initialize log files if they don't exist
    touch "$LEDGER_DIR/drift_events.log"
    touch "$LEDGER_DIR/rollback_actions.log"
    
    local total_drift=0
    
    # Run all checks
    check_docker_containers || total_drift=$((total_drift + $?))
    check_kubernetes_pods || total_drift=$((total_drift + $?))
    check_missing_containers || total_drift=$((total_drift + $?))
    
    # Log summary
    echo "$(date -Iseconds)|SUMMARY|DRIFT_COUNT:$total_drift" >> "$LEDGER_DIR/drift_events.log"
    
    # Commit to git
    commit_to_git "$total_drift"
    
    if [[ $total_drift -eq 0 ]]; then
        log_success "=== Drift Detection Complete: All systems compliant ==="
    else
        log_warn "=== Drift Detection Complete: $total_drift drift events ==="
    fi
    
    return $total_drift
}

# Run main function
main "$@"
