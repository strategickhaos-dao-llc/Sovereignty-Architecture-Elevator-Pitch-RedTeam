#!/usr/bin/env bash
set -euo pipefail

echo ">> Bootstrapping cluster with core Legion components"
echo "   (Ingress, cert-manager, namespaces, etc.)"

# Example namespace creation (idempotent)
kubectl create namespace legion-core --dry-run=client -o yaml | kubectl apply -f -

# Placeholder: you can add Helm installs here later
# helm repo add jetstack https://charts.jetstack.io
# helm install cert-manager jetstack/cert-manager \
#   --namespace cert-manager \
#   --create-namespace \
#   --set installCRDs=true

echo ">> Bootstrap finished (placeholder). Add your Helm/K8s ops here."
