#!/usr/bin/env bash
# shard_launcher.sh - control-plane bash launcher to invoke run_pid_ranco.sh across hosts
# Usage: ./shard_launcher.sh [ssh_user] [inventory]
USER=${1:-ubuntu}
INVENTORY=${2:-cloud_hosts.ini}

if [ ! -f "$INVENTORY" ]; then
  echo "Inventory $INVENTORY not found."
  exit 1
fi

# Extract host list: skip [group] lines and comments
mapfile -t HOSTS < <(awk '!/^\[/{ if ($0 !~ /^#/) print $1 }' "$INVENTORY")
N=${#HOSTS[@]}
if [ "$N" -eq 0 ]; then
  echo "No hosts found in $INVENTORY"
  exit 1
fi
echo "Found $N hosts. Launching shards..."

i=0
for h in "${HOSTS[@]}"; do
  shard="$i"
  total="$N"
  echo "Launching shard $shard on host $h"
  # Use ansible ad-hoc to run the wrapper. ansible will use ansible_user from inventory if provided.
  ansible -i "$INVENTORY" "$h" -m shell -a "/opt/strategickhaos/run_pid_ranco.sh $shard $total" &
  i=$((i+1))
done

wait
echo "All shard jobs launched."
