#!/bin/bash
# Kubernetes Pod Failure Monitor
# Sovereignty Communications Architecture
#
# Monitors Kubernetes events and sends alerts through multi-channel system

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALERT_SCRIPT="${ALERT_SCRIPT:-${SCRIPT_DIR}/send-alert.sh}"
LOG_FILE="${LOG_FILE:-/var/log/pod-monitor.log}"
NAMESPACE="${NAMESPACE:-}"

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Check prerequisites
check_prerequisites() {
    if ! command -v kubectl &> /dev/null; then
        log_message "ERROR" "kubectl not found in PATH"
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        log_message "ERROR" "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    if [[ ! -x "$ALERT_SCRIPT" ]]; then
        log_message "WARN" "Alert script not executable, attempting to fix..."
        chmod +x "$ALERT_SCRIPT" 2>/dev/null || true
    fi
    
    log_message "INFO" "Prerequisites check passed"
}

# Send alert through multi-channel system
send_multi_channel_alert() {
    local message="$1"
    local severity="${2:-warning}"
    
    log_message "INFO" "Sending alert: $message (severity: $severity)"
    
    if [[ -x "$ALERT_SCRIPT" ]]; then
        "$ALERT_SCRIPT" --severity "$severity" "$message" || \
            log_message "ERROR" "Alert script failed"
    else
        log_message "WARN" "Alert script not available, logging only"
    fi
}

# Process a single event
process_event() {
    local event_json="$1"
    
    local reason
    local message
    local namespace
    local name
    local kind
    local event_type
    
    reason=$(echo "$event_json" | jq -r '.reason // empty')
    message=$(echo "$event_json" | jq -r '.message // empty')
    namespace=$(echo "$event_json" | jq -r '.involvedObject.namespace // empty')
    name=$(echo "$event_json" | jq -r '.involvedObject.name // empty')
    kind=$(echo "$event_json" | jq -r '.involvedObject.kind // empty')
    event_type=$(echo "$event_json" | jq -r '.type // "Normal"')
    
    # Skip if empty or normal events for certain reasons
    [[ -z "$reason" ]] && return
    [[ "$event_type" == "Normal" ]] && return
    
    local alert_message="[$kind/$name in $namespace] $reason: $message"
    
    case "$reason" in
        # Critical failures
        Failed|BackOff|OOMKilled|CrashLoopBackOff|FailedScheduling|FailedMount)
            log_message "ALERT" "Critical failure detected: $alert_message"
            send_multi_channel_alert "$alert_message" "critical"
            ;;
            
        # Health issues
        Unhealthy|ProbeWarning|NodeNotReady)
            log_message "ALERT" "Health issue detected: $alert_message"
            send_multi_channel_alert "$alert_message" "warning"
            ;;
            
        # Resource issues
        FailedCreate|InsufficientResources|FailedBinding)
            log_message "ALERT" "Resource issue detected: $alert_message"
            send_multi_channel_alert "$alert_message" "warning"
            ;;
            
        # Image issues
        ErrImagePull|ImagePullBackOff|InvalidImageName)
            log_message "ALERT" "Image issue detected: $alert_message"
            send_multi_channel_alert "$alert_message" "warning"
            ;;
            
        # Eviction
        Evicted|PreemptionVictim)
            log_message "ALERT" "Pod eviction detected: $alert_message"
            send_multi_channel_alert "$alert_message" "warning"
            ;;
            
        *)
            # Log but don't alert on other warning events
            if [[ "$event_type" == "Warning" ]]; then
                log_message "WARN" "Warning event: $alert_message"
            fi
            ;;
    esac
}

# Monitor events in watch mode
monitor_events() {
    local ns_flag=""
    [[ -n "$NAMESPACE" ]] && ns_flag="-n $NAMESPACE"
    
    log_message "INFO" "Starting pod event monitoring..."
    [[ -n "$NAMESPACE" ]] && log_message "INFO" "Watching namespace: $NAMESPACE"
    [[ -z "$NAMESPACE" ]] && log_message "INFO" "Watching all namespaces"
    
    # Use kubectl get events in watch mode with JSON output
    kubectl get events $ns_flag --watch -o json 2>/dev/null | \
    while IFS= read -r line; do
        # Skip empty lines
        [[ -z "$line" ]] && continue
        
        # Check if it's valid JSON
        if echo "$line" | jq -e . >/dev/null 2>&1; then
            process_event "$line"
        fi
    done
}

# One-time scan of recent events
scan_events() {
    local ns_flag=""
    [[ -n "$NAMESPACE" ]] && ns_flag="-n $NAMESPACE"
    
    log_message "INFO" "Scanning recent events..."
    
    kubectl get events $ns_flag -o json 2>/dev/null | \
    jq -c '.items[]' 2>/dev/null | \
    while IFS= read -r event; do
        process_event "$event"
    done
    
    log_message "INFO" "Event scan complete"
}

# Usage information
usage() {
    cat << EOF
Kubernetes Pod Failure Monitor - Sovereignty Communications Architecture

Usage: $0 [OPTIONS]

Options:
    --namespace, -n <ns>     Watch specific namespace (default: all)
    --scan                   Scan recent events once and exit
    --watch                  Watch events continuously (default)
    --help, -h               Show this help message

Examples:
    $0                       # Watch all namespaces
    $0 -n production         # Watch production namespace only
    $0 --scan                # Scan recent events once
    $0 --scan -n ops         # Scan ops namespace once

Environment Variables:
    ALERT_SCRIPT             Path to alert script (default: ./send-alert.sh)
    LOG_FILE                 Log file path (default: /var/log/pod-monitor.log)
    NAMESPACE                Default namespace to watch
EOF
}

# Main entry point
main() {
    local mode="watch"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --namespace|-n)
                NAMESPACE="$2"
                shift 2
                ;;
            --scan)
                mode="scan"
                shift
                ;;
            --watch)
                mode="watch"
                shift
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true
    
    check_prerequisites
    
    case "$mode" in
        scan)
            scan_events
            ;;
        watch)
            monitor_events
            ;;
    esac
}

main "$@"
