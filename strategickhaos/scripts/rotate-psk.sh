#!/usr/bin/env bash
set -e
# Rotate PSK for all WireGuard peers
# Usage: rotate-psk.sh

echo "[*] Rotating PSK for all peers..."
PEERS=$(wg show wg0 peers)
for p in $PEERS; do
  wg genpsk | tee /etc/wireguard/psk/$p.psk | wg set wg0 peer $p preshared-key /etc/wireguard/psk/$p.psk
done
echo "[+] PSK rotation complete"
