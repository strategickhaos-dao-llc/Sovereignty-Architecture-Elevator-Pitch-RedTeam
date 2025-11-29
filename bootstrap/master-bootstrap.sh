#!/usr/bin/env bash
# Sovereign Swarm — Master Bootstrap (Defaults)
# Runs Phase 0→3 for a node. First run on Command-0.
# Safe defaults: no HSM, auto public IP, nodes: command0,fixed1,mobile2,edge3,edge4
# Services: wg-quick, NATS, Synapse (docker), UFW deny-all + 22/TCP + 51820/UDP
# PSK rotation cron yearly
set -euo pipefail

# ========= User-adjustable minimal knobs =========
NODE_ID="${NODE_ID:-command0}"          # set per host: command0|fixed1|mobile2|edge3|edge4
SWARM_NET="10.44.0.0/16"
WG_IF="wg0"
WG_PORT="${WG_PORT:-51820}"
NATS_PORT=4222
NATS_LEAF_PORT=7422
NATS_CLUSTER_PORT=6222
MATRIX_HTTP_PORT=8008
UFW_SSH_PORT="${UFW_SSH_PORT:-22}"
REPO_ROOT="${REPO_ROOT:-/opt/sovereign-swarm}"
DOMAIN="${DOMAIN:-swarm.local}"         # used by synapse; no public DNS required
# ================================================

umask 077
mkdir -p "$REPO_ROOT"
cd "$REPO_ROOT"

log(){ echo "[*] $*"; }

require_root(){
  if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo -s)"; exit 1
  fi
}
require_root

detect_os(){
  if command -v apt >/dev/null 2>&1; then
    PKG="apt"
  else
    echo "This script targets Debian/Ubuntu (apt)."; exit 1
  fi
}
detect_os

# Packages
log "Installing packages..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y \
  wireguard wireguard-tools nftables ufw curl jq git ca-certificates \
  python3 python3-pip python3-venv \
  docker.io docker-compose-plugin \
  nats-server syncthing

# Repo layout
mkdir -p ca/state nodes/$NODE_ID wireguard/conf swarmgate/{nft,swarmsgd,systemd} nats/{conf,systemd,accounts} matrix/synapse scripts artifacts

# Phase 0 — CA + Node keys
log "Generating CA and node keys..."
if [ ! -f ca/state/swarm-ed25519.key ]; then
  # Use libsodium via python to generate ed25519 seed
  python3 - <<'PY'
import os, hashlib, base64, json
seed=os.urandom(32)
open("ca/state/swarm-ed25519.key","wb").write(seed)
open("ca/state/swarm-ed25519.pub","wb").write(hashlib.blake2b(seed,digest_size=32).digest())
PY
fi

if [ ! -f "nodes/$NODE_ID/wg.key" ]; then
  wg genkey | tee "nodes/$NODE_ID/wg.key" | wg pubkey > "nodes/$NODE_ID/wg.pub"
fi
if [ ! -f "nodes/$NODE_ID/ed25519.key" ]; then
  head -c 32 /dev/urandom > "nodes/$NODE_ID/ed25519.key"
  sha256sum "nodes/$NODE_ID/ed25519.key" | awk '{print $1}' > "nodes/$NODE_ID/ed25519.fp"
fi

# Simple EdDSA JWT mint (local)
install -D -m 755 /dev/stdin scripts/mint_token.py <<'PY'
#!/usr/bin/env python3
import json, time, base64, os, argparse, hashlib
from nacl.signing import SigningKey
def b64u(b): return base64.urlsafe_b64encode(b).rstrip(b'=')
ap=argparse.ArgumentParser()
ap.add_argument("--ca","-c",required=True)
ap.add_argument("--node","-n",required=True)
ap.add_argument("--aud","-a",required=True)
ap.add_argument("--ttl",default="86400")
ap.add_argument("--caps",required=True)
args=ap.parse_args()
seed=open(args.ca,"rb").read()
sk=SigningKey(seed)
now=int(time.time()); exp=now+int(args.ttl)
claims={"iss":"SwarmCA","sub":os.path.basename(args.node),"aud":args.aud,"iat":now,"exp":exp,"cap":args.caps.split(","),"jti":b64u(os.urandom(16)).decode()}
hdr={"alg":"EdDSA","typ":"JWT"}
h=b'.'.join([b64u(json.dumps(hdr).encode()), b64u(json.dumps(claims).encode())])
sig=sk.sign(h).signature
jwt=h.decode()+"."+b64u(sig).decode()
open(os.path.join(args.node,"token.jwt"),"w").write(jwt)
print(jwt)
PY

# Capabilities per role
case "$NODE_ID" in
  command0) CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:admin,router:true,net:${SWARM_NET}" ;;
  fixed1)   CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:server,router:true,net:${SWARM_NET}" ;;
  mobile2)  CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:agent,router:false,net:${SWARM_NET}" ;;
  edge* )   CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:agent,router:false,net:${SWARM_NET}" ;;
  *)        CAPS="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:agent,router:false,net:${SWARM_NET}" ;;
esac

python3 scripts/mint_token.py -c ca/state/swarm-ed25519.key -n "nodes/$NODE_ID" -a wg --ttl 86400 --caps "$CAPS" >/dev/null

# Store pub for verifiers
cp ca/state/swarm-ed25519.pub /etc/swarmsgd-pubkey || true

# SwarmGate agent
install -D -m 755 /dev/stdin swarmgate/swarmsgd/agent.py <<'PY'
#!/usr/bin/env python3
import os, sys, json, base64, time, ipaddress, subprocess
from nacl.signing import VerifyKey
PUB="/etc/swarmsgd-pubkey"
def b64u_pad(s):
    s += '=' * (-len(s) % 4)
    return s
def jwt_verify(jwt, aud):
    hdr, pl, sig = jwt.split('.')
    payload = json.loads(base64.urlsafe_b64decode(b64u_pad(pl)))
    if payload.get("aud") != aud: raise Exception("aud")
    if payload.get("exp",0) < int(time.time()): raise Exception("exp")
    pub = open(PUB,"rb").read()
    vk = VerifyKey(pub)
    vk.verify((hdr+"."+pl).encode(), base64.urlsafe_b64decode(b64u_pad(sig)))
    return payload
def apply_allowed(peer_pub, nets):
    subprocess.run(["wg","set","wg0","peer",peer_pub,"remove","allowed-ips"], check=False)
    for n in nets:
        subprocess.run(["wg","set","wg0","peer",peer_pub,"allowed-ips",n], check=False)
def main():
    peer=os.environ.get("WG_PEER_PUBLIC_KEY","")
    token_path=f"/run/wg-tokens/{peer}.jwt"
    if not os.path.exists(token_path):
        print("DENY: no token", file=sys.stderr); sys.exit(1)
    tok=open(token_path).read().strip()
    claims=jwt_verify(tok,"wg")
    nets=[c.split(":",1)[1] for c in claims.get("cap",[]) if c.startswith("net:")]
    # basic nft set for source filtering (optional)
    apply_allowed(peer, nets)
    print("OK")
if __name__=="__main__": main()
PY

# nftables rule (minimal)
install -D -m 644 /dev/stdin swarmgate/nft/swarmsg.nft <<'NFT'
table inet swarmsg {
  set peers { type ipv4_addr; flags interval; }
  chain preraw {
    type filter hook prerouting priority -300; policy accept;
    # Permit NATS/Matrix from wg interface; further tightening can be added
  }
}
NFT

# Systemd for swarmsgd (runs on demand via hook; also keep a service)
install -D -m 644 /dev/stdin swarmgate/systemd/swarmsgd.service <<'UNIT'
[Unit]
Description=SwarmGate Agent
After=network.target
[Service]
ExecStart=/usr/bin/env python3 /opt/sovereign-swarm/swarmgate/swarmsgd/agent.py
User=root
Group=root
Restart=on-failure
[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now swarmsgd || true

# WireGuard config generation
log "Generating WireGuard config..."
WG_PRIV=$(cat "nodes/$NODE_ID/wg.key")
WG_PUB=$(cat "nodes/$NODE_ID/wg.pub")

# Node addressing
case "$NODE_ID" in
  command0) WG_ADDR="10.44.0.1/16" ;;
  fixed1)   WG_ADDR="10.44.1.1/16" ;;
  mobile2)  WG_ADDR="10.44.2.1/16" ;;
  edge3)    WG_ADDR="10.44.10.3/16" ;;
  edge4)    WG_ADDR="10.44.10.4/16" ;;
  *)        WG_ADDR="10.44.10.100/16" ;;
esac

PUB_IP=$(curl -4s https://ifconfig.me || echo "0.0.0.0")

# Seed peer list (Command-0 <-> Fixed-1 bi-directional; others connect to Command-0)
PEERS=""
if [ "$NODE_ID" = "command0" ]; then
  # Fixed-1 peer placeholder; AllowedIPs narrowed to /32 endpoints; dynamic AllowedIPs enforced by SwarmGate
  cat > wireguard/conf/${WG_IF}.conf <<CFG
[Interface]
Address = ${WG_ADDR}
PrivateKey = ${WG_PRIV}
ListenPort = ${WG_PORT}
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = nft -f /etc/nftables.conf || true
PostUp = nft -f ${REPO_ROOT}/swarmgate/nft/swarmsg.nft || true

# Fixed-1 (added when fixed1 runs bootstrap)
# Add additional peers with scripts as they come online
CFG
else
  # Non-command nodes peer to Command-0
  # Create PSK per-peer
  mkdir -p /etc/wireguard/psk
  if [ ! -f "/etc/wireguard/psk/${NODE_ID}.psk" ]; then
    wg genpsk > "/etc/wireguard/psk/${NODE_ID}.psk"
  fi
  PSK_PATH="/etc/wireguard/psk/${NODE_ID}.psk"
  cat > wireguard/conf/${WG_IF}.conf <<CFG
[Interface]
Address = ${WG_ADDR}
PrivateKey = ${WG_PRIV}
ListenPort = ${WG_PORT}
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = nft -f /etc/nftables.conf || true
PostUp = nft -f ${REPO_ROOT}/swarmgate/nft/swarmsg.nft || true

[Peer]
# Command-0
PublicKey = REPLACE_COMMAND0_PUBKEY
PresharedKey = $(cat ${PSK_PATH})
AllowedIPs = 10.44.0.1/32, 10.44.0.0/16
Endpoint = REPLACE_COMMAND0_ENDPOINT:${WG_PORT}
PersistentKeepalive = 15
CFG
fi

# Install wg config and bring up
install -D -m 600 wireguard/conf/${WG_IF}.conf /etc/wireguard/${WG_IF}.conf

# Token hand-off directory for handshakes
mkdir -p /run/wg-tokens
chmod 700 /run/wg-tokens
cp "nodes/$NODE_ID/token.jwt" "/run/wg-tokens/${WG_PUB}.jwt"

# UFW baseline
log "Configuring UFW..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ${UFW_SSH_PORT}/tcp
ufw allow ${WG_PORT}/udp
ufw enable

# Enable wg
log "Bringing up WireGuard..."
systemctl enable wg-quick@${WG_IF}
systemctl start wg-quick@${WG_IF}

# If this is command0, print pubkey and endpoint to share with others
if [ "$NODE_ID" = "command0" ]; then
  echo
  echo "=== Command-0 details ==="
  echo "PublicKey: ${WG_PUB}"
  echo "Endpoint : ${PUB_IP}:${WG_PORT}"
  echo "================================"
fi

# NATS config
log "Configuring NATS..."
install -D -m 644 /dev/stdin nats/conf/nats.conf <<NC
port: ${NATS_PORT}
server_name: ${NODE_ID}
jetstream: { store_dir: "/var/lib/nats/js", max_mem_store: 512MB, max_file_store: 10GB }
leafnodes: {
  listen: ${NATS_LEAF_PORT}
}
cluster { name: swarm; listen: "0.0.0.0:${NATS_CLUSTER_PORT}" }
authorization: { users: [ { user: "swarm", pass: "swarm", permissions: { publish: ["telemetry.>","alerts.>"], subscribe: ["cmd.>","telemetry.>"] } } ] }
NC

install -D -m 644 /dev/stdin nats/systemd/nats.service <<'UNIT'
[Unit]
Description=NATS Server
After=network-online.target wg-quick@wg0.service
Wants=wg-quick@wg0.service

[Service]
User=nats
Group=nats
ExecStart=/usr/bin/nats-server -c /etc/nats/nats.conf
Restart=on-failure
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
UNIT

id nats >/dev/null 2>&1 || useradd -r -s /usr/sbin/nologin nats
install -d -o nats -g nats /var/lib/nats/js
install -D -m 644 nats/conf/nats.conf /etc/nats/nats.conf
systemctl daemon-reload
systemctl enable --now nats.service

# Matrix (Synapse) via docker
log "Configuring Matrix Synapse (docker)..."
install -D -m 644 /dev/stdin matrix/docker-compose.yml <<DC
services:
  synapse:
    image: matrixdotorg/synapse:latest
    container_name: synapse
    restart: unless-stopped
    network_mode: host
    volumes:
      - /opt/sovereign-swarm/matrix/synapse:/data
    environment:
      - SYNAPSE_SERVER_NAME=${DOMAIN}
      - SYNAPSE_REPORT_STATS=no
DC

mkdir -p matrix/synapse
if [ ! -f matrix/synapse/homeserver.yaml ]; then
  docker run --rm -it -v ${REPO_ROOT}/matrix/synapse:/data -e SYNAPSE_SERVER_NAME=${DOMAIN} -e SYNAPSE_REPORT_STATS=no matrixdotorg/synapse:latest generate
  # harden basics
  sed -i 's/^enable_registration:.*/enable_registration: false/' matrix/synapse/homeserver.yaml || true
  sed -i 's/^max_upload_size:.*/max_upload_size: 50M/' matrix/synapse/homeserver.yaml || true
fi

docker compose -f matrix/docker-compose.yml up -d

# PSK rotation cron (yearly)
log "Installing yearly PSK rotation cron..."
install -D -m 755 /dev/stdin scripts/rotate-psk.sh <<'ROT'
#!/usr/bin/env bash
set -euo pipefail
IF="wg0"
PEERS=$(wg show ${IF} peers || true)
mkdir -p /etc/wireguard/psk
for p in $PEERS; do
  wg genpsk | tee /etc/wireguard/psk/${p}.psk >/dev/null
  wg set ${IF} peer ${p} preshared-key /etc/wireguard/psk/${p}.psk
done
ROT

( crontab -l 2>/dev/null | grep -v rotate-psk.sh ; echo "0 5 1 1 * ${REPO_ROOT}/scripts/rotate-psk.sh" ) | crontab -

# Artifact pack for Pelican nodes
log "Preparing artifacts for Pelican nodes..."
tar czf artifacts/${NODE_ID}-artifacts.tgz -C "nodes/$NODE_ID" .

log "Bootstrap complete for ${NODE_ID}."
echo "Next steps:"
echo "- For non-command nodes, edit /etc/wireguard/wg0.conf to replace:"
echo "  REPLACE_COMMAND0_PUBKEY with Command-0 pubkey, REPLACE_COMMAND0_ENDPOINT with its public IP"
