#!/bin/bash
# pelican-build.sh — Sovereign Swarm System v2.0
# Pelican Drop Kit Builder — <3-min deployment SLA
# Creates autonomous field-deployable nodes with GPS + QR onboarding
# Generated for: Strategickhaos DAO LLC / Valoryield Engine
# Author: Domenic Garza (Node 137)

set -euo pipefail

# === Configuration ===
PELICAN_VERSION="2.0"
BUILD_DIR="${BUILD_DIR:-/tmp/pelican-build}"
OUTPUT_DIR="${OUTPUT_DIR:-./pelican-kits}"
RENDEZVOUS_IP="${RENDEZVOUS_IP:-10.44.0.1}"
STARLINK_DISH="${STARLINK_DISH:-3476D3}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         PELICAN DROP KIT BUILDER v${PELICAN_VERSION}                      ║${NC}"
echo -e "${BLUE}║           Field-Deployable Autonomous Nodes                  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# === Create Build Directory ===
setup_build_env() {
    log_info "Setting up build environment..."
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR"/{scripts,configs,keys}
    mkdir -p "$OUTPUT_DIR"
    log_success "Build environment ready at $BUILD_DIR"
}

# === Generate First-Boot Join Script ===
generate_first_boot_script() {
    log_info "Generating first-boot-join.sh..."

    cat > "$BUILD_DIR/scripts/first-boot-join.sh" << 'FIRST_BOOT_EOF'
#!/bin/bash
# first-boot-join.sh — Pelican Node Auto-Join
# Executes on first boot to join the Sovereign Swarm mesh

set -euo pipefail

RENDEZVOUS_IP="${RENDEZVOUS_IP:-10.44.0.1}"
NODE_ID="pelican-$(hostname | sha256sum | cut -c1-8)"

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1"; }

log "Pelican node $NODE_ID starting first-boot join sequence..."

# === Phase 1: Install Dependencies ===
log "Installing dependencies..."
apt-get update -qq
apt-get install -y --no-install-recommends \
    wireguard \
    wireguard-tools \
    nftables \
    curl \
    jq \
    gpsd \
    gpsd-clients \
    qrencode \
    mwan3 \
    2>/dev/null || true

# === Phase 2: Multi-WAN Setup (Evolution #2) ===
log "Configuring multi-WAN with mwan3..."

# Configure mwan3 for Starlink + Verizon failover
if command -v mwan3 &> /dev/null; then
    cat > /etc/mwan3.user << 'MWAN3_EOF'
#!/bin/sh
# mwan3 user script — Sovereign Swarm multi-WAN policy

# Custom policy for swarm traffic
case "$2" in
    ifup)
        logger -t mwan3 "Interface $1 came up"
        ;;
    ifdown)
        logger -t mwan3 "Interface $1 went down"
        ;;
esac
MWAN3_EOF
    chmod +x /etc/mwan3.user

    # Add interfaces to mwan3 (example config)
    # mwan3 add starlink eth0  # Primary: Starlink
    # mwan3 add verizon usb0   # Failover: Verizon LTE
    log "mwan3 multi-WAN configured"
fi

# === Phase 3: WireGuard Key Generation ===
log "Generating WireGuard keys..."
WG_DIR="/etc/wireguard"
mkdir -p "$WG_DIR"

if [[ ! -f "$WG_DIR/privatekey" ]]; then
    wg genkey | tee "$WG_DIR/privatekey" | wg pubkey > "$WG_DIR/publickey"
    chmod 600 "$WG_DIR/privatekey"
fi

PRIVATE_KEY=$(cat "$WG_DIR/privatekey")
PUBLIC_KEY=$(cat "$WG_DIR/publickey")

# Assign dynamic IP in pelican range (10.44.100.x)
NODE_NUM=$((RANDOM % 200 + 2))
NODE_IP="10.44.100.${NODE_NUM}"

# === Phase 4: WireGuard Configuration ===
log "Configuring WireGuard interface..."
cat > "$WG_DIR/wg0.conf" << EOF
# Pelican Node WireGuard Configuration
# Node ID: $NODE_ID
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

[Interface]
Address = ${NODE_IP}/24
PrivateKey = ${PRIVATE_KEY}
ListenPort = 51820

# Rendezvous peer (Command-0)
[Peer]
# PublicKey to be obtained from rendezvous
AllowedIPs = 10.44.0.0/16
Endpoint = ${RENDEZVOUS_IP}:51820
PersistentKeepalive = 25
EOF

# === Phase 5: GPSd Setup (Evolution #7) ===
log "Configuring GPS daemon..."
if [[ -e /dev/ttyUSB0 ]] || [[ -e /dev/ttyACM0 ]]; then
    GPS_DEV=$(ls /dev/ttyUSB0 /dev/ttyACM0 2>/dev/null | head -1)
    cat > /etc/default/gpsd << EOF
# GPSd configuration for Pelican node
START_DAEMON="true"
USBAUTO="true"
DEVICES="${GPS_DEV}"
GPSD_OPTIONS="-n"
EOF
    systemctl enable gpsd 2>/dev/null || true
    log "GPSd configured on $GPS_DEV"
else
    log "No GPS device detected — skipping GPSd"
fi

# === Phase 6: Telemetry Publisher ===
log "Setting up telemetry publisher..."
cat > /usr/local/bin/swarm-telemetry.sh << 'TELEMETRY_EOF'
#!/bin/bash
# Publish node telemetry to NATS

NATS_SERVER="${NATS_SERVER:-nats://swarm:swarm@10.44.0.1:4222}"
NODE_ID=$(hostname)

# Collect metrics
UPTIME=$(cat /proc/uptime | awk '{print $1}')
LOAD=$(cat /proc/loadavg | awk '{print $1}')
MEM_FREE=$(free -m | awk '/Mem:/ {print $4}')
DISK_FREE=$(df -h / | awk 'NR==2 {print $4}')

# Get GPS coordinates if available
if command -v gpspipe &> /dev/null; then
    GPS_DATA=$(gpspipe -w -n 5 2>/dev/null | grep -m1 TPV || echo '{}')
    LAT=$(echo "$GPS_DATA" | jq -r '.lat // "null"')
    LON=$(echo "$GPS_DATA" | jq -r '.lon // "null"')
else
    LAT="null"
    LON="null"
fi

# Build telemetry JSON
TELEMETRY=$(cat << TELEMJSON
{
    "node_id": "$NODE_ID",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "uptime_sec": $UPTIME,
    "load_1m": $LOAD,
    "mem_free_mb": $MEM_FREE,
    "disk_free": "$DISK_FREE",
    "gps": {
        "lat": $LAT,
        "lon": $LON
    }
}
TELEMJSON
)

# Publish to NATS
if command -v nats &> /dev/null; then
    echo "$TELEMETRY" | nats pub telemetry.node.$NODE_ID - 2>/dev/null || true
fi
TELEMETRY_EOF
chmod +x /usr/local/bin/swarm-telemetry.sh

# Add telemetry cron job
echo "*/1 * * * * root /usr/local/bin/swarm-telemetry.sh >> /var/log/swarm-telemetry.log 2>&1" > /etc/cron.d/swarm-telemetry

# === Phase 7: QR Onboarding (Evolution #7) ===
log "Generating QR join code..."
mkdir -p /var/swarm/qr

# Generate 72h ephemeral ally token
ALLY_TOKEN=$(openssl rand -hex 32)
ALLY_EXPIRY=$(date -d "+72 hours" -u +%Y-%m-%dT%H:%M:%SZ)

QR_DATA=$(cat << QRJSON
{
    "swarm": "sovereign-swarm",
    "node_id": "$NODE_ID",
    "pubkey": "$PUBLIC_KEY",
    "ip": "$NODE_IP",
    "ally_token": "$ALLY_TOKEN",
    "expiry": "$ALLY_EXPIRY"
}
QRJSON
)

echo "$QR_DATA" | qrencode -o /var/swarm/qr/join-code.png 2>/dev/null || true
echo "$QR_DATA" > /var/swarm/qr/join-code.json

log "QR join code generated at /var/swarm/qr/join-code.png"

# === Phase 8: Enable Services ===
log "Enabling services..."
systemctl enable wg-quick@wg0 2>/dev/null || true

# === Phase 9: Announce to Swarm ===
log "Announcing to swarm rendezvous..."
ANNOUNCE_PAYLOAD=$(cat << ANNOUNCEJSON
{
    "event": "pelican_join",
    "node_id": "$NODE_ID",
    "pubkey": "$PUBLIC_KEY",
    "ip": "$NODE_IP",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
ANNOUNCEJSON
)

# Attempt NATS announcement
if command -v nats &> /dev/null; then
    echo "$ANNOUNCE_PAYLOAD" | nats pub swarm.join.$NODE_ID - 2>/dev/null || true
fi

log "First-boot join sequence complete!"
log "Node ID: $NODE_ID"
log "WireGuard IP: $NODE_IP"
log "Public Key: $PUBLIC_KEY"
FIRST_BOOT_EOF

    chmod +x "$BUILD_DIR/scripts/first-boot-join.sh"
    log_success "first-boot-join.sh generated"
}

# === Generate Token Minting Script (Evolution #7) ===
generate_mint_token_script() {
    log_info "Generating mint_token.py..."

    cat > "$BUILD_DIR/scripts/mint_token.py" << 'MINT_EOF'
#!/usr/bin/env python3
"""
mint_token.py — Sovereign Swarm Token Minter
Generates JWT tokens for ally onboarding with configurable TTL
"""

import json
import hashlib
import hmac
import base64
import time
import sys
import os
from datetime import datetime, timedelta

# Configuration
SECRET_KEY = os.environ.get('SWARM_SECRET', 'sovereign-swarm-default-key')
DEFAULT_TTL_HOURS = 72

def base64url_encode(data):
    """Encode data as base64url without padding."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def create_jwt(payload, secret):
    """Create a simple JWT token."""
    header = {"alg": "HS256", "typ": "JWT"}
    
    header_b64 = base64url_encode(json.dumps(header))
    payload_b64 = base64url_encode(json.dumps(payload))
    
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature_b64 = base64url_encode(signature)
    
    return f"{message}.{signature_b64}"

def mint_ally_token(node_id, ttl_hours=DEFAULT_TTL_HOURS, capabilities=None):
    """Mint an ally token for swarm joining."""
    now = datetime.utcnow()
    expiry = now + timedelta(hours=ttl_hours)
    
    # Generate unique token ID
    jti = hashlib.sha256(f"{node_id}{now.isoformat()}".encode()).hexdigest()[:16]
    
    payload = {
        "iss": "sovereign-swarm",
        "sub": node_id,
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expiry.timestamp()),
        "nbf": int(now.timestamp()),
        "capabilities": capabilities or ["join", "telemetry"],
        "tier": "ally",
    }
    
    token = create_jwt(payload, SECRET_KEY)
    
    return {
        "token": token,
        "jti": jti,
        "node_id": node_id,
        "expires": expiry.isoformat() + "Z",
        "ttl_hours": ttl_hours,
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Mint Sovereign Swarm ally tokens')
    parser.add_argument('node_id', help='Node identifier for the token')
    parser.add_argument('--ttl', type=int, default=DEFAULT_TTL_HOURS, help='Token TTL in hours')
    parser.add_argument('--qr', action='store_true', help='Generate QR code')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    result = mint_ally_token(args.node_id, args.ttl)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Token written to {args.output}")
    else:
        print(json.dumps(result, indent=2))
    
    if args.qr:
        try:
            import subprocess
            qr_data = json.dumps({"swarm_token": result["token"]})
            subprocess.run(['qrencode', '-o', f'{args.node_id}-token.png'], 
                         input=qr_data.encode(), check=True)
            print(f"QR code saved to {args.node_id}-token.png")
        except Exception as e:
            print(f"QR generation failed: {e}")

if __name__ == '__main__':
    main()
MINT_EOF

    chmod +x "$BUILD_DIR/scripts/mint_token.py"
    log_success "mint_token.py generated"
}

# === Generate GPS Location Publisher ===
generate_gps_publisher() {
    log_info "Generating GPS location publisher..."

    cat > "$BUILD_DIR/scripts/gps-publisher.sh" << 'GPS_EOF'
#!/bin/bash
# gps-publisher.sh — Publish GPS coordinates to NATS telemetry.geo.*
# Evolution #7: Location-aware routing for SAR ops

NATS_SERVER="${NATS_SERVER:-nats://swarm:swarm@10.44.0.1:4222}"
NODE_ID=$(hostname)

publish_location() {
    if ! command -v gpspipe &> /dev/null; then
        echo "gpspipe not available"
        return 1
    fi

    # Get GPS data
    GPS_JSON=$(gpspipe -w -n 5 2>/dev/null | grep -m1 TPV || echo '{}')
    
    LAT=$(echo "$GPS_JSON" | jq -r '.lat // empty')
    LON=$(echo "$GPS_JSON" | jq -r '.lon // empty')
    ALT=$(echo "$GPS_JSON" | jq -r '.alt // 0')
    SPEED=$(echo "$GPS_JSON" | jq -r '.speed // 0')
    TRACK=$(echo "$GPS_JSON" | jq -r '.track // 0')

    if [[ -n "$LAT" && -n "$LON" ]]; then
        GEO_DATA=$(cat << GEOJSON
{
    "node_id": "$NODE_ID",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "location": {
        "lat": $LAT,
        "lon": $LON,
        "alt": $ALT,
        "speed_mps": $SPEED,
        "track_deg": $TRACK
    },
    "geohash": "$(echo "$LAT,$LON" | md5sum | cut -c1-8)"
}
GEOJSON
)
        echo "$GEO_DATA" | nats pub telemetry.geo.$NODE_ID - 2>/dev/null
        echo "Published location: $LAT, $LON"
    else
        echo "No GPS fix available"
    fi
}

# Main loop
while true; do
    publish_location
    sleep 30
done
GPS_EOF

    chmod +x "$BUILD_DIR/scripts/gps-publisher.sh"
    log_success "GPS publisher generated"
}

# === Package Pelican Kit ===
package_pelican_kit() {
    log_info "Packaging Pelican drop kit..."

    KIT_NAME="pelican-kit-$(date +%Y%m%d-%H%M%S)"
    KIT_PATH="$OUTPUT_DIR/$KIT_NAME"
    mkdir -p "$KIT_PATH"

    # Copy scripts
    cp -r "$BUILD_DIR/scripts/"* "$KIT_PATH/"

    # Create README
    cat > "$KIT_PATH/README.md" << 'README_EOF'
# Pelican Drop Kit — Sovereign Swarm v2.0

## Quick Start (<3 minutes)

1. **Flash SD card** with Raspberry Pi OS Lite (64-bit)
2. **Copy this kit** to `/opt/pelican/`
3. **Run first boot**: `sudo /opt/pelican/first-boot-join.sh`

## Contents

- `first-boot-join.sh` — Auto-join script for swarm mesh
- `mint_token.py` — Generate ally onboarding tokens
- `gps-publisher.sh` — Location telemetry for SAR ops
- `swarm-telemetry.sh` — Node health telemetry

## Hardware Requirements

- Raspberry Pi 4/5 (4GB+ RAM recommended)
- USB GPS module (Ublox recommended) — Optional
- Cellular modem (Verizon Orbic/similar) — Optional

## Network Configuration

- WireGuard mesh on `10.44.100.x/24`
- NATS telemetry on port 4222
- Syncthing file sync on port 22000

## Support

Contact: Strategickhaos DAO LLC
Swarm: sovereign-swarm
README_EOF

    # Create tarball
    cd "$OUTPUT_DIR"
    tar -czf "${KIT_NAME}.tar.gz" "$KIT_NAME"
    rm -rf "$KIT_NAME"

    log_success "Pelican kit packaged: ${OUTPUT_DIR}/${KIT_NAME}.tar.gz"
}

# === Main Execution ===
main() {
    setup_build_env
    generate_first_boot_script
    generate_mint_token_script
    generate_gps_publisher
    package_pelican_kit

    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              PELICAN DROP KIT BUILD COMPLETE                 ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Output:${NC} ${OUTPUT_DIR}/"
    echo -e "${BLUE}SLA:${NC} <3 minute deployment"
    echo ""
    echo -e "${YELLOW}Deployment Steps:${NC}"
    echo "1. Extract kit to Pi: tar -xzf pelican-kit-*.tar.gz"
    echo "2. Run as root: ./first-boot-join.sh"
    echo "3. Scan QR code at /var/swarm/qr/join-code.png"
    echo ""
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
