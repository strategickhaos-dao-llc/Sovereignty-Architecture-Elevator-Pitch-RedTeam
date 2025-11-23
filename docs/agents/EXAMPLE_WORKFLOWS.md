# Agent Collaboration Example Workflows

Real-world examples and workflows for agent collaboration with Kubernetes cluster.

## Table of Contents

1. [Basic Workflows](#basic-workflows)
2. [Monitoring & Debugging](#monitoring--debugging)
3. [Deployment Workflows](#deployment-workflows)
4. [Collaborative Tasks](#collaborative-tasks)
5. [Advanced Scenarios](#advanced-scenarios)

---

## Basic Workflows

### Workflow 1: Connect and Verify Access

**Objective:** Establish connection to cluster and verify agent can access resources.

```bash
# Step 1: Start VPN
sudo wg-quick up wg0

# Step 2: Verify VPN connection
ping 10.100.0.1

# Step 3: Test kubectl access
kubectl get nodes
kubectl get namespaces

# Step 4: Test agent permissions
kubectl auth can-i list pods -n ops
kubectl auth can-i delete pods -n ops  # Should be "no"

# Step 5: Run connection test
cd agents/scripts
./test-agent-connection.sh
```

**Expected Result:** All tests pass, agent has read access to ops namespace.

---

### Workflow 2: Query Pod Status

**Objective:** Check status of running pods and services.

```bash
# Using kubectl
kubectl get pods -n ops -o wide

# Using helper script
./agents/scripts/agent-kubectl-helper.sh pods ops

# Get detailed pod information
kubectl describe pod discord-ops-bot-abc123 -n ops

# Check pod resource usage
kubectl top pod discord-ops-bot-abc123 -n ops
```

**Via API:**

```bash
export VPN_IP=10.100.0.1
export AGENT_TOKEN=$(kubectl create token inline-agent -n agents)

# List pods
curl -H "Authorization: Bearer $AGENT_TOKEN" \
  http://$VPN_IP:30000/api/v1/pods | jq .

# Get specific pod
curl -H "Authorization: Bearer $AGENT_TOKEN" \
  http://$VPN_IP:30000/api/v1/pods/discord-ops-bot-abc123 | jq .
```

---

### Workflow 3: View Logs

**Objective:** Retrieve and analyze pod logs.

```bash
# Get recent logs (last 100 lines)
kubectl logs --tail=100 discord-ops-bot-abc123 -n ops

# Follow logs in real-time
kubectl logs -f discord-ops-bot-abc123 -n ops

# Get logs from previous container (after restart)
kubectl logs discord-ops-bot-abc123 -n ops --previous

# Using helper script
./agents/scripts/agent-kubectl-helper.sh logs discord-ops-bot-abc123 ops

# Filter logs with grep
kubectl logs discord-ops-bot-abc123 -n ops | grep ERROR

# Export logs to file
kubectl logs discord-ops-bot-abc123 -n ops > /tmp/bot-logs.txt
```

---

## Monitoring & Debugging

### Workflow 4: Monitor Cluster Metrics

**Objective:** Track cluster resource usage and performance.

```bash
# View node metrics
kubectl top nodes

# View pod metrics in namespace
kubectl top pods -n ops

# Get specific pod metrics
kubectl top pod discord-ops-bot-abc123 -n ops

# Using Prometheus API
curl "http://$VPN_IP:30090/api/v1/query?query=container_cpu_usage_seconds_total" | jq .

# Query memory usage
curl "http://$VPN_IP:30090/api/v1/query?query=container_memory_usage_bytes" | jq .
```

**Create Custom Dashboard:**

```bash
# Access Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000

# Open browser to http://localhost:3000
# Import dashboard for agent metrics
```

---

### Workflow 5: Debug Application Issues

**Objective:** Troubleshoot failing pod or service.

```bash
# Step 1: Check pod status
kubectl get pod discord-ops-bot-abc123 -n ops

# Step 2: Describe pod to see events
kubectl describe pod discord-ops-bot-abc123 -n ops

# Step 3: Check logs for errors
kubectl logs discord-ops-bot-abc123 -n ops | grep -i error

# Step 4: Execute commands in pod
kubectl exec -it discord-ops-bot-abc123 -n ops -- /bin/sh

# Inside pod:
ps aux                    # Check running processes
df -h                     # Check disk space
env                       # Check environment variables
curl localhost:8080/health  # Test internal health endpoint

# Step 5: Check service endpoints
kubectl get endpoints agent-api -n ops

# Step 6: Test service connectivity
kubectl run test -it --rm --image=alpine -n ops -- \
  wget -O- http://agent-api.ops.svc.cluster.local/health
```

---

### Workflow 6: Analyze Events

**Objective:** Review cluster events for issues.

```bash
# Get all events in namespace
kubectl get events -n ops

# Sort by timestamp
kubectl get events -n ops --sort-by='.lastTimestamp'

# Filter warnings
kubectl get events -n ops --field-selector type=Warning

# Watch events in real-time
kubectl get events -n ops --watch

# Export events for analysis
kubectl get events -n ops -o json > /tmp/events.json
```

---

## Deployment Workflows

### Workflow 7: Deploy New Service

**Objective:** Deploy a new agent service to cluster.

```bash
# Step 1: Create deployment manifest
cat > /tmp/my-agent-service.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-agent-service
  namespace: agents
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-agent-service
  template:
    metadata:
      labels:
        app: my-agent-service
    spec:
      serviceAccountName: inline-agent
      containers:
      - name: service
        image: my-registry/agent-service:v1.0
        ports:
        - containerPort: 8080
EOF

# Step 2: Apply deployment
kubectl apply -f /tmp/my-agent-service.yaml

# Step 3: Watch rollout status
kubectl rollout status deployment/my-agent-service -n agents

# Step 4: Verify pods are running
kubectl get pods -n agents -l app=my-agent-service

# Step 5: Create service
kubectl expose deployment my-agent-service \
  --type=ClusterIP \
  --port=80 \
  --target-port=8080 \
  -n agents

# Step 6: Test service
kubectl run test -it --rm --image=alpine -n agents -- \
  wget -O- http://my-agent-service.agents.svc.cluster.local
```

---

### Workflow 8: Update Service

**Objective:** Update running service with new version.

```bash
# Step 1: Update image
kubectl set image deployment/my-agent-service \
  service=my-registry/agent-service:v1.1 \
  -n agents

# Step 2: Watch rollout
kubectl rollout status deployment/my-agent-service -n agents

# Step 3: Verify new version
kubectl get pods -n agents -l app=my-agent-service

# Step 4: Check logs of new pods
kubectl logs -f deployment/my-agent-service -n agents

# Rollback if needed
kubectl rollout undo deployment/my-agent-service -n agents
```

---

## Collaborative Tasks

### Workflow 9: Share Data Between Agents

**Objective:** Enable multiple agents to share data via shared volume.

```bash
# Step 1: Create shared PVC
cat > /tmp/shared-pvc.yaml << EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: agent-shared-storage
  namespace: agents
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
EOF

kubectl apply -f /tmp/shared-pvc.yaml

# Step 2: Agent 1 writes data
kubectl run writer -it --rm --image=alpine -n agents \
  --overrides='
{
  "spec": {
    "volumes": [{
      "name": "shared",
      "persistentVolumeClaim": {"claimName": "agent-shared-storage"}
    }],
    "containers": [{
      "name": "writer",
      "image": "alpine",
      "command": ["sh"],
      "volumeMounts": [{
        "name": "shared",
        "mountPath": "/shared"
      }]
    }]
  }
}' -- sh -c "echo 'Data from Agent 1' > /shared/data.txt"

# Step 3: Agent 2 reads data
kubectl run reader -it --rm --image=alpine -n agents \
  --overrides='
{
  "spec": {
    "volumes": [{
      "name": "shared",
      "persistentVolumeClaim": {"claimName": "agent-shared-storage"}
    }],
    "containers": [{
      "name": "reader",
      "image": "alpine",
      "command": ["sh"],
      "volumeMounts": [{
        "name": "shared",
        "mountPath": "/shared"
      }]
    }]
  }
}' -- cat /shared/data.txt
```

---

### Workflow 10: Coordinate Tasks via Redis

**Objective:** Use Redis for agent task coordination.

```bash
# Step 1: Deploy Redis (already in docker-compose)
cd agents/config
docker-compose -f docker-compose.agent-services.yml up -d agent-redis

# Step 2: Agent 1 publishes task
kubectl run publisher -it --rm --image=redis:alpine -n agents -- \
  redis-cli -h agent-redis.agents.svc.cluster.local \
  LPUSH tasks "Process logs from pod-abc123"

# Step 3: Agent 2 retrieves task
kubectl run subscriber -it --rm --image=redis:alpine -n agents -- \
  redis-cli -h agent-redis.agents.svc.cluster.local \
  RPOP tasks
```

---

## Advanced Scenarios

### Workflow 11: Automated Health Monitoring

**Objective:** Monitor service health and auto-restart if needed.

```bash
# Create monitoring script
cat > /tmp/health-monitor.sh << 'EOF'
#!/bin/bash
while true; do
  if ! curl -f http://$VPN_IP:30000/health &>/dev/null; then
    echo "$(date): Service unhealthy, investigating..."
    kubectl describe pod -n ops -l app=agent-api
    kubectl logs -n ops -l app=agent-api --tail=50
    # Alert via Discord or Slack
  fi
  sleep 60
done
EOF

chmod +x /tmp/health-monitor.sh

# Run in background
nohup /tmp/health-monitor.sh > /tmp/health-monitor.log 2>&1 &
```

---

### Workflow 12: Log Aggregation and Analysis

**Objective:** Collect and analyze logs from multiple pods.

```bash
# Step 1: Collect logs from all pods in namespace
for pod in $(kubectl get pods -n ops -o name); do
  echo "=== Logs from $pod ===" >> /tmp/all-logs.txt
  kubectl logs $pod -n ops >> /tmp/all-logs.txt 2>&1
done

# Step 2: Analyze with grep
grep -i "error\|warning\|exception" /tmp/all-logs.txt

# Step 3: Count error types
awk '/ERROR/ {errors[$0]++} END {for (e in errors) print errors[e], e}' \
  /tmp/all-logs.txt | sort -rn

# Step 4: Send to Loki for centralized storage
curl -H "Content-Type: application/json" \
  -XPOST "http://$VPN_IP:3100/loki/api/v1/push" \
  --data @/tmp/logs.json
```

---

### Workflow 13: Execute Batch Commands

**Objective:** Run command across multiple pods simultaneously.

```bash
# Get all pod names
PODS=$(kubectl get pods -n ops -o name | cut -d/ -f2)

# Execute command in each pod
for pod in $PODS; do
  echo "=== Running in $pod ==="
  kubectl exec $pod -n ops -- ps aux
done

# Parallel execution
kubectl get pods -n ops -o name | xargs -P 5 -I {} \
  kubectl exec {} -n ops -- date
```

---

### Workflow 14: Backup and Restore

**Objective:** Backup agent data and configurations.

```bash
# Step 1: Backup configurations
kubectl get all -n agents -o yaml > /tmp/agents-backup.yaml
kubectl get pvc -n agents -o yaml >> /tmp/agents-backup.yaml
kubectl get secrets -n agents -o yaml >> /tmp/agents-backup.yaml

# Step 2: Backup data from pods
kubectl exec my-agent-service-abc123 -n agents -- \
  tar czf - /data | cat > /tmp/agent-data-backup.tar.gz

# Step 3: Restore configurations
kubectl apply -f /tmp/agents-backup.yaml

# Step 4: Restore data
cat /tmp/agent-data-backup.tar.gz | \
  kubectl exec -i my-agent-service-abc123 -n agents -- \
  tar xzf - -C /
```

---

## Performance Testing

### Workflow 15: Load Testing Agent API

**Objective:** Test API performance under load.

```bash
# Install hey (HTTP load generator)
go install github.com/rakyll/hey@latest

# Run load test
hey -n 1000 -c 10 -H "Authorization: Bearer $AGENT_TOKEN" \
  http://$VPN_IP:30000/api/v1/pods

# Monitor during test
watch -n 1 "kubectl top pods -n ops"

# Check rate limiting
curl http://$VPN_IP:30090/api/v1/query?query=nginx_http_requests_rate_limited
```

---

## Troubleshooting Workflows

### Workflow 16: Network Connectivity Issues

**Objective:** Diagnose and fix network issues.

```bash
# Step 1: Test VPN
ping 10.100.0.1
sudo wg show

# Step 2: Test DNS
nslookup agent-api.ops.svc.cluster.local

# Step 3: Test service endpoints
kubectl get endpoints agent-api -n ops

# Step 4: Test from inside cluster
kubectl run test -it --rm --image=nicolaka/netshoot -n ops -- \
  curl -v http://agent-api.ops.svc.cluster.local

# Step 5: Check network policies
kubectl describe networkpolicy agent-network-policy -n agents

# Step 6: Test NodePort access
curl -v http://$VPN_IP:30000/health
```

---

## Summary

These workflows cover common agent collaboration scenarios:

- ✅ Basic cluster access and verification
- ✅ Monitoring and debugging
- ✅ Deployment and updates
- ✅ Multi-agent coordination
- ✅ Advanced automation
- ✅ Troubleshooting

For more information, see:
- [Quick Start Guide](QUICK_START.md)
- [Complete Guide](AGENT_COLLABORATION.md)
- [Security Best Practices](SECURITY_BEST_PRACTICES.md)

---

**Last Updated:** 2025-11-23
**Maintained by:** Strategickhaos DAO LLC
