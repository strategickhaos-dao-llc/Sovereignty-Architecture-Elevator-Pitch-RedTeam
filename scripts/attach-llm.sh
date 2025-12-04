#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:-legion-core}"
SERVICE_NAME="${2:-llm-gateway}"
LOCAL_PORT="${3:-11434}"
REMOTE_PORT="${4:-11434}"

echo ">> Attaching to LLM service '$SERVICE_NAME' in namespace '$NAMESPACE'"
echo ">> Local port:  $LOCAL_PORT"
echo ">> Remote port: $REMOTE_PORT"

echo "Press Ctrl+C to detach."

kubectl port-forward -n "$NAMESPACE" "svc/${SERVICE_NAME}" "${LOCAL_PORT}:${REMOTE_PORT}"
