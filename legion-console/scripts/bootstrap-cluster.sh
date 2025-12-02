#!/usr/bin/env bash
set -euo pipefail

echo ">> Bootstrapping cluster with core Legion components"
echo "   (Ingress, cert-manager, namespaces, etc.)"

# Ensure namespace exists (create if missing and permitted)
ensure_namespace() {
  local ns="$1"
  if kubectl get ns "$ns" >/dev/null 2>&1; then
    echo "   Namespace '$ns' already exists"
  elif kubectl create namespace "$ns" 2>/dev/null; then
    echo "   Created namespace '$ns'"
  else
    echo "   Warning: Could not create namespace '$ns' (may lack permissions)"
    echo "   Ensure the namespace exists before proceeding."
  fi
}

ensure_namespace legion-core

# Placeholder: you can add Helm installs here later
# helm repo add jetstack https://charts.jetstack.io
# helm install cert-manager jetstack/cert-manager \
#   --namespace cert-manager \
#   --create-namespace \
#   --set installCRDs=true

echo ">> Bootstrap finished (placeholder). Add your Helm/K8s ops here."
