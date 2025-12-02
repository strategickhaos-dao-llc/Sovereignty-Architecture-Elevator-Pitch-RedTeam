#!/usr/bin/env bash
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

CONTEXT_NAME="${1:-}"

if [[ -z "$CONTEXT_NAME" ]]; then
  echo "Usage: ./scripts/set-context.sh <context-name>"
  echo "Examples: gke-jarvis-swarm-personal | gke-red-team | homelab-k3s"
  exit 1
fi

case "$CONTEXT_NAME" in
  gke-jarvis-swarm-personal)
    PROJECT="jarvis-swarm-personal"
    REGION="us-central1"
    CLUSTER="jarvis-swarm-personal-001"
    echo ">> Setting context to GKE $CLUSTER in $PROJECT/$REGION"
    gcloud container clusters get-credentials "$CLUSTER" --region "$REGION" --project "$PROJECT"
    kubectl config set-context --current --namespace=legion-core
    ;;

  gke-red-team)
    PROJECT="jarvis-swarm-personal"
    REGION="us-central1"
    CLUSTER="red-team"
    echo ">> Setting context to GKE $CLUSTER in $PROJECT/$REGION"
    gcloud container clusters get-credentials "$CLUSTER" --region "$REGION" --project "$PROJECT"
    kubectl config set-context --current --namespace=legion-red
    ;;

  homelab-k3s)
    echo ">> Setting context to homelab k3s using k8s/kubeconfig"
    KUBECONFIG_PATH="$REPO_ROOT/k8s/kubeconfig"
    if [[ ! -f "$KUBECONFIG_PATH" ]]; then
      echo "Error: kubeconfig not found at $KUBECONFIG_PATH"
      echo "Please copy k8s/kubeconfig.example to k8s/kubeconfig and configure it."
      exit 1
    fi
    export KUBECONFIG="$KUBECONFIG_PATH"
    kubectl config use-context homelab
    kubectl config set-context --current --namespace=legion-lab
    ;;

  *)
    echo "Unknown context: $CONTEXT_NAME"
    exit 1
    ;;
esac

echo ">> Current context:"
kubectl config current-context
kubectl get nodes
