#!/usr/bin/env bash
# control_cost_guard.sh - run the auto_shutdown_idle.yml playbook from control host and optionally stop provider VMs
# Usage: ./control_cost_guard.sh [inventory=cloud_hosts.ini] [idle_minutes=30]
INVENTORY=${1:-cloud_hosts.ini}
IDLE=${2:-30}
ansible-playbook -i "$INVENTORY" auto_shutdown_idle.yml -e "idle_minutes=$IDLE"
# Optionally: extend to call cloud provider CLIs to stop known instances by ID or tag if you prefer central control.
