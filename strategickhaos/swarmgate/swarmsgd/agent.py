#!/usr/bin/env python3
import jwt, time, ipaddress, subprocess, json, os, sys

TOKEN_CACHE="/var/lib/swarmsgd/tokens"
POLICY="/etc/swarmsgd/policy.json"
PUBKEY_PATH="/etc/swarmsgd/swarm-ed25519.pub"

def read_pub():
    return open(PUBKEY_PATH,"rb").read()

def verify(token):
    pub = read_pub()
    return jwt.decode(token, pub, algorithms=["EdDSA"], audience="wg")

def apply_policy(peer, claims):
    caps = claims.get("cap",[])
    nets = [c.split(":",1)[1] for c in caps if c.startswith("net:")]
    allowed = []
    for n in nets:
        try: allowed.append(str(ipaddress.ip_network(n, strict=False)))
        except: pass
    # Program nftables marks for NATS/Matrix based on caps
    rules = []
    if any(c.startswith("nats.") for c in caps):
        rules.append("add element inet swarmsg caps { %s }" % peer)
    # Write AllowedIPs set to wg for peer
    subprocess.run(["wg","set","wg0","peer",peer,"remove","allowed-ips"])
    for net in allowed:
        subprocess.run(["wg","set","wg0","peer",peer,"allowed-ips",net])

def quarantine(peer):
    subprocess.run(["wg","set","wg0","peer",peer,"remove","allowed-ips"])
    subprocess.run(["wg","set","wg0","peer",peer,"preshared-key","/etc/swarmsgd/null.psk"])

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
