#!/bin/bash
# Multi-Channel Alert Script
# Sovereignty Communications Architecture
#
# Sends alerts through multiple communication channels with automatic failover.
# Supports: SMS (Verizon), Satellite (Starlink), LoRa Mesh, VPN (Tailscale)

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${LOG_FILE:-/var/log/sovereignty-alerts.log}"
RETRY_COUNT="${RETRY_COUNT:-3}"
RETRY_DELAY="${RETRY_DELAY:-5}"

# Channel configurations
SMS_ENABLED="${SMS_ENABLED:-true}"
SATELLITE_ENABLED="${SATELLITE_ENABLED:-true}"
LORA_ENABLED="${LORA_ENABLED:-true}"
VPN_ENABLED="${VPN_ENABLED:-true}"

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Send SMS via Verizon Business API
send_sms() {
    local message="$1"
    local recipient="${ALERT_PHONE_NUMBER:-}"
    
    if [[ "$SMS_ENABLED" != "true" ]]; then
        log_message "DEBUG" "SMS channel disabled"
        return 1
    fi
    
    if [[ -z "$recipient" ]]; then
        log_message "WARN" "No phone number configured for SMS alerts"
        return 1
    fi
    
    local api_endpoint="${VERIZON_API_ENDPOINT:-https://api.verizon.com/sms/v1}"
    local api_key="${VERIZON_API_KEY:-}"
    
    if [[ -z "$api_key" ]]; then
        log_message "ERROR" "Verizon API key not configured"
        return 1
    fi
    
    log_message "INFO" "Sending SMS alert..."
    
    # Create JSON payload securely using printf to avoid command line exposure
    local payload
    payload=$(printf '{"to": "%s", "message": "%s"}' "$recipient" "$message")
    
    for ((i=1; i<=RETRY_COUNT; i++)); do
        if printf '%s' "$payload" | curl -s -X POST "$api_endpoint/send" \
            -H "Authorization: Bearer $api_key" \
            -H "Content-Type: application/json" \
            -d @- \
            --max-time 10 > /dev/null 2>&1; then
            log_message "INFO" "SMS sent successfully"
            return 0
        fi
        log_message "WARN" "SMS attempt $i failed, retrying..."
        sleep "$RETRY_DELAY"
    done
    
    log_message "ERROR" "SMS delivery failed after $RETRY_COUNT attempts"
    return 1
}

# Send via Satellite (Starlink Direct-to-Cell)
send_satellite() {
    local message="$1"
    
    if [[ "$SATELLITE_ENABLED" != "true" ]]; then
        log_message "DEBUG" "Satellite channel disabled"
        return 1
    fi
    
    log_message "INFO" "Sending satellite alert..."
    
    # Satellite messaging typically falls back to the same SMS API
    # when Direct-to-Cell is available, but uses satellite backhaul
    local satellite_endpoint="${STARLINK_API_ENDPOINT:-}"
    
    if [[ -z "$satellite_endpoint" ]]; then
        # Fall back to standard SMS path which may route via satellite
        log_message "INFO" "Using carrier satellite fallback"
        return 1
    fi
    
    # Create JSON payload securely
    local payload
    payload=$(printf '{"message": "%s"}' "$message")
    
    for ((i=1; i<=RETRY_COUNT; i++)); do
        if printf '%s' "$payload" | curl -s -X POST "$satellite_endpoint/message" \
            -H "Content-Type: application/json" \
            -d @- \
            --max-time 30 > /dev/null 2>&1; then
            log_message "INFO" "Satellite message sent successfully"
            return 0
        fi
        log_message "WARN" "Satellite attempt $i failed, retrying..."
        sleep "$RETRY_DELAY"
    done
    
    log_message "ERROR" "Satellite delivery failed after $RETRY_COUNT attempts"
    return 1
}

# Send via LoRa Mesh (Meshtastic)
send_lora() {
    local message="$1"
    
    if [[ "$LORA_ENABLED" != "true" ]]; then
        log_message "DEBUG" "LoRa channel disabled"
        return 1
    fi
    
    log_message "INFO" "Sending LoRa mesh alert..."
    
    local lora_script="${SCRIPT_DIR}/lora_mesh_comms.py"
    
    if [[ ! -f "$lora_script" ]]; then
        log_message "ERROR" "LoRa mesh script not found: $lora_script"
        return 1
    fi
    
    for ((i=1; i<=RETRY_COUNT; i++)); do
        if python3 "$lora_script" send --message "$message" --severity warning; then
            log_message "INFO" "LoRa mesh message sent successfully"
            return 0
        fi
        log_message "WARN" "LoRa attempt $i failed, retrying..."
        sleep "$RETRY_DELAY"
    done
    
    log_message "ERROR" "LoRa mesh delivery failed after $RETRY_COUNT attempts"
    return 1
}

# Send via VPN mesh (Tailscale webhook)
send_vpn() {
    local message="$1"
    
    if [[ "$VPN_ENABLED" != "true" ]]; then
        log_message "DEBUG" "VPN channel disabled"
        return 1
    fi
    
    log_message "INFO" "Sending VPN mesh alert..."
    
    local vpn_webhook="${TAILSCALE_WEBHOOK_URL:-}"
    
    if [[ -z "$vpn_webhook" ]]; then
        log_message "WARN" "Tailscale webhook URL not configured"
        return 1
    fi
    
    # Create JSON payload securely
    local payload
    payload=$(printf '{"text": "%s", "source": "sovereignty-alerts"}' "$message")
    
    for ((i=1; i<=RETRY_COUNT; i++)); do
        if printf '%s' "$payload" | curl -s -X POST "$vpn_webhook" \
            -H "Content-Type: application/json" \
            -d @- \
            --max-time 10 > /dev/null 2>&1; then
            log_message "INFO" "VPN mesh message sent successfully"
            return 0
        fi
        log_message "WARN" "VPN attempt $i failed, retrying..."
        sleep "$RETRY_DELAY"
    done
    
    log_message "ERROR" "VPN mesh delivery failed after $RETRY_COUNT attempts"
    return 1
}

# Multi-channel send with failover
send_alert() {
    local message="$1"
    local channel="${2:-all}"
    local severity="${3:-warning}"
    
    # Add severity prefix
    local formatted_message="[${severity^^}] $message"
    
    case "$channel" in
        sms)
            send_sms "$formatted_message"
            return $?
            ;;
        satellite)
            send_satellite "$formatted_message"
            return $?
            ;;
        lora)
            send_lora "$formatted_message"
            return $?
            ;;
        vpn)
            send_vpn "$formatted_message"
            return $?
            ;;
        all)
            # Cascade through all channels
            log_message "INFO" "Starting multi-channel alert cascade"
            
            # Primary: SMS
            if send_sms "$formatted_message"; then
                return 0
            fi
            log_message "WARN" "SMS failed, trying satellite..."
            
            # Secondary: Satellite
            if send_satellite "$formatted_message"; then
                return 0
            fi
            log_message "WARN" "Satellite failed, trying LoRa mesh..."
            
            # Tertiary: LoRa Mesh
            if send_lora "$formatted_message"; then
                return 0
            fi
            log_message "WARN" "LoRa failed, trying VPN mesh..."
            
            # Quaternary: VPN Mesh
            if send_vpn "$formatted_message"; then
                return 0
            fi
            
            log_message "ERROR" "All alert channels failed!"
            return 1
            ;;
        *)
            log_message "ERROR" "Unknown channel: $channel"
            return 1
            ;;
    esac
}

# Health check for all channels
check_health() {
    echo "=== Sovereignty Communications Health Check ==="
    echo ""
    
    # Check SMS
    echo -n "SMS (Verizon): "
    if [[ "$SMS_ENABLED" == "true" ]] && [[ -n "${VERIZON_API_KEY:-}" ]]; then
        echo "✅ Configured"
    else
        echo "❌ Not configured"
    fi
    
    # Check Satellite
    echo -n "Satellite (Starlink): "
    if [[ "$SATELLITE_ENABLED" == "true" ]]; then
        echo "✅ Enabled (carrier fallback)"
    else
        echo "❌ Disabled"
    fi
    
    # Check LoRa
    echo -n "LoRa Mesh: "
    if [[ "$LORA_ENABLED" == "true" ]]; then
        local lora_script="${SCRIPT_DIR}/lora_mesh_comms.py"
        if [[ -f "$lora_script" ]]; then
            if python3 "$lora_script" health 2>/dev/null | grep -q "Status: healthy"; then
                echo "✅ Connected"
            else
                echo "⚠️ Script exists but device not connected"
            fi
        else
            echo "❌ Script not found"
        fi
    else
        echo "❌ Disabled"
    fi
    
    # Check VPN
    echo -n "VPN Mesh (Tailscale): "
    if [[ "$VPN_ENABLED" == "true" ]] && command -v tailscale &> /dev/null; then
        if tailscale status &> /dev/null; then
            echo "✅ Connected"
        else
            echo "⚠️ Installed but not connected"
        fi
    else
        echo "❌ Not available"
    fi
    
    echo ""
}

# Usage information
usage() {
    cat << EOF
Sovereignty Communications Architecture - Multi-Channel Alert Script

Usage: $0 [OPTIONS] <message>

Options:
    --channel, -c <channel>  Specify channel: sms, satellite, lora, vpn, all (default: all)
    --severity, -s <level>   Severity: critical, warning, info (default: warning)
    --health                 Check health of all channels
    --help, -h               Show this help message

Examples:
    $0 "System alert: Pod failure detected"
    $0 --channel sms "Urgent: Database connection lost"
    $0 --channel lora --severity critical "Emergency: Network down"
    $0 --health

Environment Variables:
    VERIZON_API_KEY          API key for Verizon Business SMS
    VERIZON_API_ENDPOINT     Verizon API endpoint URL
    ALERT_PHONE_NUMBER       Phone number for SMS alerts
    STARLINK_API_ENDPOINT    Starlink satellite API endpoint
    TAILSCALE_WEBHOOK_URL    Tailscale webhook URL for VPN alerts
    LORA_PORT                Serial port for Meshtastic device (default: /dev/ttyUSB0)
    
    SMS_ENABLED              Enable SMS channel (default: true)
    SATELLITE_ENABLED        Enable satellite channel (default: true)
    LORA_ENABLED             Enable LoRa channel (default: true)
    VPN_ENABLED              Enable VPN channel (default: true)
EOF
}

# Main entry point
main() {
    local channel="all"
    local severity="warning"
    local message=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --channel|-c)
                channel="$2"
                shift 2
                ;;
            --severity|-s)
                severity="$2"
                shift 2
                ;;
            --health)
                check_health
                exit 0
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            -*)
                echo "Unknown option: $1"
                usage
                exit 1
                ;;
            *)
                message="$1"
                shift
                ;;
        esac
    done
    
    if [[ -z "$message" ]]; then
        echo "Error: No message provided"
        usage
        exit 1
    fi
    
    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true
    
    send_alert "$message" "$channel" "$severity"
    exit $?
}

main "$@"
