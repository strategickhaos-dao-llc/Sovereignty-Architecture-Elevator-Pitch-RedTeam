#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 10D Chess Council - Generate StatefulSets for All 10 Boards
# Creates Kubernetes manifests for 640 agents (64 per board)
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/bootstrap/k8s/chess-council"

# Board layer names
declare -a LAYER_NAMES=(
    "empirical-data"
    "data-preprocessing"
    "statistical-analysis"
    "knowledge-synthesis"
    "predictive-modeling"
    "strategic-reasoning"
    "ethical-evaluation"
    "linguistic-generation"
    "validation-verification"
    "publication-dissemination"
)

# Generate StatefulSet for each board
for board in {0..9}; do
    layer_name="${LAYER_NAMES[$board]}"
    output_file="${OUTPUT_DIR}/board-${board}-statefulset.yaml"
    
    echo "Generating board ${board} (${layer_name})..."
    
    cat > "${output_file}" << EOF
# ═══════════════════════════════════════════════════════════
# 10D Chess Council - Board ${board} StatefulSet
# Layer: ${layer_name}
# 64 agents (8×8 chess board positions)
# ═══════════════════════════════════════════════════════════

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: chess-board-${board}
  namespace: chess-council
  labels:
    app: chess-agent
    layer: "${board}"
    layer-name: ${layer_name}
spec:
  serviceName: chess-agents-${board}
  replicas: 64
  podManagementPolicy: Parallel
  selector:
    matchLabels:
      app: chess-agent
      layer: "${board}"
  template:
    metadata:
      labels:
        app: chess-agent
        layer: "${board}"
        layer-name: ${layer_name}
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      terminationGracePeriodSeconds: 30
      
      initContainers:
        - name: frequency-calculator
          image: python:3.11-slim
          command:
            - python
            - -c
            - |
              import math
              import os
              
              hostname = os.environ.get('HOSTNAME', 'chess-board-${board}-0')
              ordinal = int(hostname.split('-')[-1])
              board = ${board}
              row = ordinal // 8
              col = ordinal % 8
              
              position = board * 64 + row * 8 + col
              piano_key = position % 88
              frequency = 440 * (2 ** ((piano_key - 49) / 12))
              
              with open('/frequency/agent_frequency', 'w') as f:
                  f.write(f"{round(frequency, 2)}")
              
              print(f"Agent {hostname}: Board {board}, Row {row}, Col {col}")
              print(f"Position: {position}, Piano Key: {piano_key}")
              print(f"Frequency: {round(frequency, 2)} Hz")
          volumeMounts:
            - name: frequency-data
              mountPath: /frequency
      
      containers:
        - name: agent
          image: ghcr.io/strategickhaos/chess-agent:latest
          imagePullPolicy: Always
          
          resources:
            requests:
              cpu: "2"
              memory: "8Gi"
            limits:
              cpu: "4"
              memory: "16Gi"
          
          env:
            - name: BOARD_LAYER
              value: "${board}"
            - name: LAYER_NAME
              value: "${layer_name}"
            - name: AGENT_POSITION
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: OLLAMA_HOST
              value: "http://ollama-service:11434"
            - name: PRIMARY_MODEL
              value: "qwen2.5:72b"
            - name: GROK_API_KEY
              valueFrom:
                secretKeyRef:
                  name: chess-council-secrets
                  key: GROK_API_KEY
            - name: SERPAPI_KEY
              valueFrom:
                secretKeyRef:
                  name: chess-council-secrets
                  key: SERPAPI_KEY
            - name: QDRANT_URL
              value: "http://qdrant-service:6333"
            - name: POSTGRES_HOST
              value: "postgres-service"
            - name: POSTGRES_DB
              value: "chess_council"
          
          ports:
            - containerPort: 22
              name: ssh
            - containerPort: 5900
              name: vnc
            - containerPort: 47989
              name: sunshine
            - containerPort: 9090
              name: metrics
            - containerPort: 8080
              name: api
          
          volumeMounts:
            - name: agent-workspace
              mountPath: /workspace
            - name: bibliography-cache
              mountPath: /cache
            - name: frequency-data
              mountPath: /frequency
              readOnly: true
            - name: agent-config
              mountPath: /config
              readOnly: true
          
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 30
            timeoutSeconds: 10
          
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
      
      volumes:
        - name: bibliography-cache
          persistentVolumeClaim:
            claimName: shared-bibliography-pvc
        - name: frequency-data
          emptyDir: {}
        - name: agent-config
          configMap:
            name: agent-config
  
  volumeClaimTemplates:
    - metadata:
        name: agent-workspace
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 50Gi
        storageClassName: standard
---
apiVersion: v1
kind: Service
metadata:
  name: chess-agents-${board}
  namespace: chess-council
  labels:
    app: chess-agent
    layer: "${board}"
spec:
  clusterIP: None
  selector:
    app: chess-agent
    layer: "${board}"
  ports:
    - name: ssh
      port: 22
      targetPort: 22
    - name: vnc
      port: 5900
      targetPort: 5900
    - name: sunshine
      port: 47989
      targetPort: 47989
    - name: metrics
      port: 9090
      targetPort: 9090
    - name: api
      port: 8080
      targetPort: 8080
EOF

done

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Generated StatefulSets for all 10 boards (640 agents total)"
echo "Output directory: ${OUTPUT_DIR}"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "To deploy:"
echo "  kubectl apply -f ${OUTPUT_DIR}/namespace-and-config.yaml"
echo "  kubectl apply -f ${OUTPUT_DIR}/"
echo ""
