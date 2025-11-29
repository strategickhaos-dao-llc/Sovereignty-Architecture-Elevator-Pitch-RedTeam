#!/usr/bin/env bash
install -D -m 600 /repo/swarmgate/nft/swarmsg.nft /etc/nftables.d/swarmsg.nft
install -D -m 700 /repo/swarmgate/swarmsgd/agent.py /usr/local/swarmsgd/agent.py
install -D -m 644 /repo/swarmgate/systemd/swarmsgd.service /etc/systemd/system/swarmsgd.service
systemctl daemon-reload
systemctl enable --now swarmsgd
