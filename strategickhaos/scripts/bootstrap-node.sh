#!/usr/bin/env bash
set -e
ID="$1"
[ -n "$ID" ] || { echo "Usage: bootstrap-node.sh <node-id>"; exit 1; }
mkdir -p /etc/wireguard/psk /etc/nftables.d /usr/local/bin /var/lib/swarmsgd
cp wireguard/conf/${ID}.conf /etc/wireguard/wg0.conf
cp swarmgate/nft/swarmsg.nft /etc/nftables.d/
cp swarmgate/swarmsgd/agent.py /usr/local/swarmsgd/agent.py
cp swarmgate/systemd/swarmsgd.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now swarmsgd
wg-quick up wg0
