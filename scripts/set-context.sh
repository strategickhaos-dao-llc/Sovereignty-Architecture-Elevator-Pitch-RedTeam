#!/usr/bin/env bash
set -euo pipefail

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
    export KUBECONFIG="$(pwd)/k8s/kubeconfig"
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
