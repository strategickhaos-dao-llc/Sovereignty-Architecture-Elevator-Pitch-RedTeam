#!/usr/bin/env bash
set -e
PEERS=$(wg show wg0 peers)
for p in $PEERS; do
  wg genpsk | tee /etc/wireguard/psk/$p.psk | wg set wg0 peer $p preshared-key /etc/wireguard/psk/$p.psk
done
