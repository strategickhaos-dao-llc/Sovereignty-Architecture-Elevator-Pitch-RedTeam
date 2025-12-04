#!/usr/bin/env bash
# Called by wg-dynamic/uapi during handshake, passes token from PSK slot via env
export SWARMSG_TOKEN="$(cat /run/wg-tokens/${WG_PEER_PUBLIC_KEY}.jwt 2>/dev/null)"
/usr/bin/python3 /usr/local/swarmsgd/agent.py
