#!/usr/bin/env bash
set -euo pipefail

# recon_cluster.sh
# Gathers cluster state, snapshots Prometheus & Loki queries (if available),
# tars outputs, optionally notarizes with notarize_cognition.sh
#
# Usage: ./recon_cluster.sh [NAMESPACE] [OUTPUT_DIR]
NS="${1:-default}"
OUTDIR="${2:-/tmp}"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
OUT="recon_${NS}_${STAMP}"
TMP="/tmp/${OUT}"

mkdir -p "${TMP}"

kubectl get ns -o wide > "${TMP}/namespaces.txt"
kubectl get deploy,sts,ds,po,svc,ing -A -o wide > "${TMP}/workloads.txt"
kubectl get networkpolicy -A -o yaml > "${TMP}/netpol.yaml"
kubectl get clusterrole,role,clusterrolebinding,rolebinding -A -o yaml > "${TMP}/rbac.yaml"
kubectl get sa -A -o yaml > "${TMP}/sa.yaml"
kubectl get validatingwebhookconfiguration,mutatingwebhookconfiguration -A -o yaml > "${TMP}/webhooks.yaml" || true
kubectl get podsecuritypolicy -A -o yaml > "${TMP}/podsecuritypolicy.yaml" 2>/dev/null || true
kubectl get cm -A -o yaml > "${TMP}/configmaps.yaml" || true

# Dump image tags from manifests and pods
echo "=== Image tags (from pods) ===" > "${TMP}/image_tags.txt"
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace} {" "} {.metadata.name} {" "} {.spec.containers[*].image}{"\n"}{end}' >> "${TMP}/image_tags.txt" || true

# If Prometheus is present, snapshot a list of important metrics / active alerts
if kubectl get svc -n monitoring prometheus-k8s >/dev/null 2>&1; then
  echo "Pulling Prometheus snapshot (limited queries)" > "${TMP}/prometheus.txt"
  # example: scrape up-time for key targets
  kubectl -n monitoring exec svc/prometheus-k8s -- curl -sS --max-time 10 'http://localhost:9090/api/v1/query?query=up' >> "${TMP}/prometheus.txt" || true
fi

# If Loki or Grafana is present, attempt short query to capture recent errors (requires service account permiss)
if kubectl get svc -n logging loki >/dev/null 2>&1; then
  echo "Pulling recent logs (last 30m) for errors" > "${TMP}/loki_errors.txt"
  kubectl -n logging exec svc/loki -- curl -sS --max-time 15 'http://localhost:3100/loki/api/v1/query?query=%7Bjob%3D%22.*%22%7D%20%7C%20~%22error%22&limit=200' >> "${TMP}/loki_errors.txt" || true
fi

# Gather events and cluster info
kubectl get events -A --sort-by='.lastTimestamp' -o wide > "${TMP}/events.txt" || true
kubectl cluster-info dump --output-directory="${TMP}/cluster_dump" --limit=20 2>/dev/null || true

# Tar and return path
OUT_TAR="${OUTDIR}/${OUT}.tar.gz"
tar -C /tmp -czf "${OUT_TAR}" "${OUT}" || true

# Optional: notarize (if script exists)
if [[ -x "./scripts/notarize_cognition.sh" ]]; then
  "./scripts/notarize_cognition.sh" "${OUT_TAR}" || true
fi

echo "${OUT_TAR}"
