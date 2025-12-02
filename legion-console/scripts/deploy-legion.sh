#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:-legion-core}"

echo ">> Deploying Legion services into namespace: $NAMESPACE"

# Ensure namespace exists (create if missing and permitted)
if kubectl get ns "$NAMESPACE" >/dev/null 2>&1; then
  echo "   Namespace '$NAMESPACE' exists"
elif kubectl create namespace "$NAMESPACE" 2>/dev/null; then
  echo "   Created namespace '$NAMESPACE'"
else
  echo "Error: Namespace '$NAMESPACE' does not exist and could not be created."
  echo "Please ensure the namespace exists or you have permission to create it."
  exit 1
fi

# Minimal placeholder deployment: a tiny HTTP echo pod
cat <<'EOF' | kubectl apply -n "$NAMESPACE" -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: legion-echo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: legion-echo
  template:
    metadata:
      labels:
        app: legion-echo
    spec:
      containers:
        - name: echo
          image: hashicorp/http-echo
          args:
            - "-text=Legion online"
          ports:
            - containerPort: 5678
---
apiVersion: v1
kind: Service
metadata:
  name: legion-echo
spec:
  selector:
    app: legion-echo
  ports:
    - name: http
      port: 80
      targetPort: 5678
EOF

echo ">> Deployed legion-echo. To test:"
echo "   kubectl port-forward -n $NAMESPACE svc/legion-echo 8080:80"
echo "   curl http://localhost:8080"
