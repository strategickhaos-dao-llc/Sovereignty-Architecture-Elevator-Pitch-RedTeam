#!/usr/bin/env bash
# run_pid_ranco.sh - wrapper for PID-RANCO backtest
# Usage: run_pid_ranco.sh <SHARD> <TOTAL>
set -euo pipefail

SHARD=${1:-0}
TOTAL=${2:-1}
HOSTNAME=$(hostname -f 2>/dev/null || hostname)
LOG_DIR="/opt/strategickhaos/logs"
UAM_DIR="/opt/strategickhaos/uam"
OUT="${LOG_DIR}/pid_ranco_${HOSTNAME}_shard_${SHARD}_of_${TOTAL}.json"

mkdir -p "$(dirname "$OUT")"
python3 /opt/strategickhaos/trading_engine_dossier_v1.0/pid_ranco_backtest.py \
  --shard "${SHARD}" \
  --of "${TOTAL}" \
  --out "${OUT}"

# Append blake3 hash: prefer b3sum, fallback to python blake3
if command -v b3sum >/dev/null 2>&1; then
  b3sum "${OUT}" >> "${UAM_DIR}/provenance.log"
else
  python3 -c "
from blake3 import blake3
import sys
p = sys.argv[1]
uam = sys.argv[2]
with open(p, 'rb') as fh:
    h = blake3(fh.read()).hexdigest()
with open(uam + '/provenance.log', 'a') as f:
    f.write(h + '  ' + p + '\n')
" "${OUT}" "${UAM_DIR}"
fi
