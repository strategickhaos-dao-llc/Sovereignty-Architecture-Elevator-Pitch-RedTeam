#!/usr/bin/env python3
import jwt, time, ipaddress, subprocess, json, os, sys, re

TOKEN_CACHE="/var/lib/swarmsgd/tokens"
POLICY="/etc/swarmsgd/policy.json"
PUBKEY_PATH="/etc/swarmsgd/swarm-ed25519.pub"

# Regex for validating WireGuard public key format (base64)
WG_PUBKEY_PATTERN = re.compile(r'^[A-Za-z0-9+/]{43}=$')

def read_pub():
    return open(PUBKEY_PATH,"rb").read()

def verify(token):
    pub = read_pub()
    return jwt.decode(token, pub, algorithms=["EdDSA"], audience="wg")

def validate_peer_key(peer):
    """Validate peer key is a valid WireGuard public key format"""
    if not peer or not WG_PUBKEY_PATTERN.match(peer):
        raise ValueError(f"Invalid peer key format")
    return peer

def apply_policy(peer, claims):
    # Validate peer key format before any operations
    peer = validate_peer_key(peer)
    
    caps = claims.get("cap",[])
    nets = [c.split(":",1)[1] for c in caps if c.startswith("net:")]
    allowed = []
    for n in nets:
        try: allowed.append(str(ipaddress.ip_network(n, strict=False)))
        except: pass
    # Program nftables marks for NATS/Matrix based on caps
    # Note: nftables elements added via subprocess with validated peer key
    if any(c.startswith("nats.") for c in caps):
        # Use nft command with proper escaping - peer is already validated
        subprocess.run(["nft", "add", "element", "inet", "swarmsg", "caps", "{", peer, "}"], check=False)
    
    # Configure AllowedIPs for the peer
    # First, set allowed-ips to nothing to clear, then set the new list
    if allowed:
        allowed_str = ",".join(allowed)
        subprocess.run(["wg", "set", "wg0", "peer", peer, "allowed-ips", allowed_str], check=False)
    else:
        # Remove all allowed IPs by setting to empty (use 0.0.0.0/32 as placeholder then remove peer)
        subprocess.run(["wg", "set", "wg0", "peer", peer, "remove"], check=False)

def quarantine(peer):
    # Validate peer key before quarantine operations
    try:
        peer = validate_peer_key(peer)
    except ValueError:
        return  # Invalid peer key, nothing to quarantine
    subprocess.run(["wg", "set", "wg0", "peer", peer, "remove"], check=False)
    subprocess.run(["wg", "set", "wg0", "peer", peer, "preshared-key", "/etc/swarmsgd/null.psk"], check=False)

def handle_handshake(env):
    peer = env.get("WG_PEER_PUBLIC_KEY")
    token = env.get("SWARMSG_TOKEN")
    try:
        claims = verify(token)
        apply_policy(peer, claims)
        print("OK")
    except Exception as e:
        quarantine(peer)
        print("DENY", e, file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":
    handle_handshake(os.environ)
