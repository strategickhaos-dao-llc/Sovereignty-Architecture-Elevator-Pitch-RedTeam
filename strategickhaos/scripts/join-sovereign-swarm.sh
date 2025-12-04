#!/usr/bin/env bash
set -e
# Join sovereign swarm script
# Usage: join-sovereign-swarm.sh <node-id> <token-file>

NODE_ID="$1"
TOKEN_FILE="$2"

[ -n "$NODE_ID" ] || { echo "Usage: join-sovereign-swarm.sh <node-id> <token-file>"; exit 1; }
[ -f "$TOKEN_FILE" ] || { echo "Token file not found: $TOKEN_FILE"; exit 1; }

echo "[*] Joining Sovereign Swarm as $NODE_ID..."

# Install token
mkdir -p /run/wg-tokens
cp "$TOKEN_FILE" /run/wg-tokens/${NODE_ID}.jwt

# Bootstrap the node
./bootstrap-node.sh "$NODE_ID"

echo "[+] Successfully joined Sovereign Swarm!"
