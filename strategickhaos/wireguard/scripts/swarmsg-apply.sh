#!/usr/bin/env bash
# Install SwarmGate components
# REPO_ROOT should be set to the strategickhaos directory path
REPO_ROOT="${REPO_ROOT:-$(dirname "$(dirname "$0")")}"
install -D -m 600 "${REPO_ROOT}/swarmgate/nft/swarmsg.nft" /etc/nftables.d/swarmsg.nft
install -D -m 700 "${REPO_ROOT}/swarmgate/swarmsgd/agent.py" /usr/local/swarmsgd/agent.py
install -D -m 644 "${REPO_ROOT}/swarmgate/systemd/swarmsgd.service" /etc/systemd/system/swarmsgd.service
# Create null PSK for quarantine operations
dd if=/dev/zero bs=32 count=1 2>/dev/null | base64 > /etc/swarmsgd/null.psk
chmod 600 /etc/swarmsgd/null.psk
systemctl daemon-reload
systemctl enable --now swarmsgd
