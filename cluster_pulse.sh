#!/usr/bin/env bash
# cluster_pulse.sh - probe nodes' health and append a short status line to central cluster_pulse.txt (control host)
# Requires ansible to be configured.
INVENTORY=${1:-cloud_hosts.ini}
OUTFILE=${2:-cluster_pulse.txt}
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Pulse at $TIMESTAMP" >> "$OUTFILE"
ansible -i "$INVENTORY" all_cloud_terminals -m shell -a "echo \$(hostname -f) \$((\$(date +%s) - \$(stat -c %Y /opt/strategickhaos/logs 2>/dev/null || echo 0)))" -o >> "$OUTFILE" || true
echo "" >> "$OUTFILE"
