#!/usr/bin/env bash
# Build minimal artifact set for Raspberry Pi 5 Pelican nodes to auto-join mesh
# This does NOT flash an OS image; it prepares /boot/swarm/ payload to drop onto a fresh RasPi OS boot partition.
set -euo pipefail

NODE_ID="${NODE_ID:-edge3}"  # set per Pi: edge3, edge4, edgeN
REPO_ROOT="${REPO_ROOT:-/opt/sovereign-swarm}"
OUT="${OUT:-./pelican_${NODE_ID}_payload.tgz}"

if [ ! -d "${REPO_ROOT}/nodes/${NODE_ID}" ]; then
  echo "Node ${NODE_ID} not present. Run master-bootstrap.sh with NODE_ID=${NODE_ID} at least once."
  exit 1
fi

log(){ echo "[*] $*"; }

WORK=$(mktemp -d)
trap 'rm -rf "${WORK}"' EXIT

log "Building payload for ${NODE_ID}..."

# Copy node credentials
mkdir -p "${WORK}/swarm/creds"
cp "${REPO_ROOT}/nodes/${NODE_ID}/wg.key" "${WORK}/swarm/creds/"
cp "${REPO_ROOT}/nodes/${NODE_ID}/wg.pub" "${WORK}/swarm/creds/"
cp "${REPO_ROOT}/nodes/${NODE_ID}/token.jwt" "${WORK}/swarm/creds/"
cp "${REPO_ROOT}/nodes/${NODE_ID}/ed25519.key" "${WORK}/swarm/creds/" 2>/dev/null || true
cp "${REPO_ROOT}/nodes/${NODE_ID}/ed25519.fp" "${WORK}/swarm/creds/" 2>/dev/null || true

# Copy CA public key for verification
mkdir -p "${WORK}/swarm/ca"
cp "${REPO_ROOT}/ca/state/swarm-ed25519.pub" "${WORK}/swarm/ca/"

# Copy WireGuard config
mkdir -p "${WORK}/swarm/wireguard"
cp "${REPO_ROOT}/wireguard/conf/wg0.conf" "${WORK}/swarm/wireguard/" 2>/dev/null || true

# First-boot setup script
cat > "${WORK}/swarm/first-boot.sh" <<'FIRSTBOOT'
#!/usr/bin/env bash
# Pelican first-boot setup for Sovereign Swarm
set -euo pipefail

SWARM_BOOT="/boot/swarm"
SWARM_ROOT="/opt/sovereign-swarm"

log(){ echo "[pelican] $*"; }

log "Starting first-boot setup..."

# Install dependencies
apt-get update -y
apt-get install -y wireguard wireguard-tools nftables ufw curl jq python3 python3-pip

# Setup swarm directory
mkdir -p "${SWARM_ROOT}/nodes" "${SWARM_ROOT}/ca/state"

# Copy credentials from boot partition
if [ ! -f "${SWARM_BOOT}/node_id" ]; then
  log "ERROR: ${SWARM_BOOT}/node_id file not found. Cannot determine node identity."
  exit 1
fi
NODE_ID=$(cat "${SWARM_BOOT}/node_id")
if [ -z "${NODE_ID}" ]; then
  log "ERROR: node_id is empty. Cannot proceed without valid node identifier."
  exit 1
fi
mkdir -p "${SWARM_ROOT}/nodes/${NODE_ID}"
cp "${SWARM_BOOT}/creds/"* "${SWARM_ROOT}/nodes/${NODE_ID}/"
cp "${SWARM_BOOT}/ca/"* "${SWARM_ROOT}/ca/state/"

# Install WireGuard config
cp "${SWARM_BOOT}/wireguard/wg0.conf" /etc/wireguard/wg0.conf 2>/dev/null || true
chmod 600 /etc/wireguard/wg0.conf 2>/dev/null || true

# UFW baseline
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 51820/udp
ufw enable

# Enable and start WireGuard
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0

log "First-boot setup complete for ${NODE_ID}."
FIRSTBOOT
chmod +x "${WORK}/swarm/first-boot.sh"

# Node ID file
echo "${NODE_ID}" > "${WORK}/swarm/node_id"

# Create tarball
log "Creating payload tarball..."
tar czf "${OUT}" -C "${WORK}" swarm

log "Payload created: ${OUT}"
echo
echo "=== Pelican Provisioning Checklist ==="
echo "1. Flash fresh Raspberry Pi OS to SD card"
echo "2. Mount boot partition"
echo "3. Extract ${OUT} to boot partition root"
echo "4. Boot Pi, run: sudo /boot/swarm/first-boot.sh"
echo "5. Edit /etc/wireguard/wg0.conf with Command-0 pubkey/endpoint"
echo "======================================"
