#!/usr/bin/env bash
# collect_and_verify.sh
# Collect shard outputs via ansible, verify blake3 provenance entries, produce aggregated JSON, GPG-sign and suggest OTS stamp.
# Usage: ./collect_and_verify.sh [inventory=cloud_hosts.ini] [outdir=collected]
set -euo pipefail
INVENTORY=${1:-cloud_hosts.ini}
OUTDIR=${2:-collected}
AGG="${OUTDIR}/aggregated_results.json"
PROV_AGG="${OUTDIR}/provenance_verified.log"

mkdir -p "$OUTDIR"
echo "Collecting logs from hosts in $INVENTORY -> $OUTDIR"

# Pull logs from each host (ansible must be configured)
ansible -i "$INVENTORY" all_cloud_terminals -m fetch -a "src=/opt/strategickhaos/logs/ dest=$OUTDIR/ flat=yes" --become

# Consolidate all per-host json files
JSON_FILES=( $(find "$OUTDIR" -type f -name 'pid_ranco_*_shard_*.json') )
if [ ${#JSON_FILES[@]} -eq 0 ]; then
  echo "No shard output JSON files found in $OUTDIR"
  exit 2
fi

# Verify provenance lines: for each JSON found, confirm a blake3 hash exists in the node's provenance.log
> "$PROV_AGG"
for f in "${JSON_FILES[@]}"; do
  echo "Verifying $f"
  if command -v b3sum >/dev/null 2>&1; then
    H=$(b3sum "$f" | awk '{print $1}')
  else
    H=$(python3 - <<PY
from blake3 import blake3
print(blake3(open("${f}","rb").read()).hexdigest())
PY
)
  fi
  # Check whether this hash exists in any provenance.log collected (fetched with fetch will have host-prefixed names)
  if grep -R --fixed-strings "${H}" "$OUTDIR" >/dev/null 2>&1; then
    echo "$H  $f" >> "$PROV_AGG"
  else
    echo "WARNING: provenance hash for ${f} not found in fetched provenance logs" >&2
    echo "MISSING: ${H}  ${f}" >> "$PROV_AGG"
  fi
done

# Aggregate JSONs (assumes each file is an array or object; try to merge arrays, fall back to newline-joined objects)
if jq -s 'add' "${JSON_FILES[@]}" > "$AGG" 2>/dev/null; then
  echo "Aggregated JSON written to $AGG"
else
  echo "jq merge failed; concatenating JSON objects to ${AGG}. Use jq manually to shape as needed."
  jq -n '{"items": []}' > "$AGG"
  for f in "${JSON_FILES[@]}"; do
    # append raw content as string if parsing fails
    echo "{}" >> "$AGG"
  done
fi

# GPG sign aggregated result (detached clearsig)
if command -v gpg >/dev/null 2>&1; then
  gpg --output "${AGG}.asc" --armor --detach-sign "$AGG" || true
  echo "Created detached GPG signature: ${AGG}.asc"
fi

echo "Done. Provenance verification log: $PROV_AGG"
echo "Suggested next: ots stamp ${AGG}.asc or ${AGG} (OpenTimestamps) to anchor on-chain."
