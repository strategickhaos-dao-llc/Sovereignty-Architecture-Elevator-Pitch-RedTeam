# Agent Collaboration Guide

Complete guide for enabling collaboration between inline agents and the Kubernetes/Docker environment.

## Table of Contents

1. [Overview](#overview)
2. [Network Configuration](#network-configuration)
3. [Environment Setup](#environment-setup)
4. [Authentication & Security](#authentication--security)
5. [Agent Interaction](#agent-interaction)
6. [Collaboration Workflow](#collaboration-workflow)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This guide enables secure collaboration between your inline agents and the infrastructure environment comprising:

- **Docker Desktop** - Container runtime
- **Kubernetes Cluster** - Orchestration platform
- **Kali Linux / Parrot OS** - Agent terminals
- **VPN** - Secure network connectivity

### Architecture

```
┌─────────────────┐          ┌──────────────┐          ┌─────────────────┐
│  Agent Terminal │  ◄─VPN─► │  Kubernetes  │  ◄────►  │ Docker Services │
│ (Kali/Parrot)   │          │   Cluster    │          │                 │
└─────────────────┘          └──────────────┘          └─────────────────┘
        │                            │
        │                            │
        └────────── API ─────────────┘
              (NodePort 30000)
```

---

## Network Configuration

### 1. VPN Setup

#### WireGuard (Recommended)

**Generate keys:**
```bash
# On server
wg genkey | tee server_private.key | wg pubkey > server_public.key

# On agent node
wg genkey | tee agent_private.key | wg pubkey > agent_public.key
```

**Configure WireGuard:**
```bash
# Copy template
sudo cp agents/config/wireguard-agent.conf /etc/wireguard/wg0.conf

# Edit with your keys
sudo nano /etc/wireguard/wg0.conf

# Start VPN
sudo wg-quick up wg0

# Verify connection
sudo wg show
```

#### OpenVPN (Alternative)

```bash
# Install OpenVPN
sudo apt-get install openvpn

# Copy configuration
sudo cp agents/config/openvpn-agent.conf /etc/openvpn/agent.conf

# Add credentials
echo "username" | sudo tee /etc/openvpn/agent-credentials.txt
echo "password" | sudo tee -a /etc/openvpn/agent-credentials.txt
sudo chmod 600 /etc/openvpn/agent-credentials.txt

# Start VPN
sudo openvpn --config /etc/openvpn/agent.conf
```

### 2. Port Forwarding

#### Docker Services

Expose services using docker run or docker-compose:

```bash
# Expose port 80 to 8080
docker run -d -p 8080:80 your-image

# Or use docker-compose
cd agents/config
docker-compose -f docker-compose.agent-services.yml up -d
```

**Verify:**
```bash
docker ps
curl http://localhost:8080/health
```

#### Kubernetes Services

Deploy NodePort services:

```bash
# Apply agent API service
kubectl apply -f agents/config/agent-api-service.yaml

# Verify service
kubectl get services -n ops

# Test endpoint
curl http://<node-ip>:30000/health
```

**Service endpoints:**
- Agent API: `http://<vpn-ip>:30000`
- Metrics: `http://<vpn-ip>:30090`

### 3. Firewall Configuration

**Allow agent access:**
```bash
# UFW (Ubuntu/Debian)
sudo ufw allow from 10.100.0.0/24 to any port 30000
sudo ufw allow from 10.100.0.0/24 to any port 30090

# iptables
sudo iptables -A INPUT -s 10.100.0.0/24 -p tcp --dport 30000 -j ACCEPT
sudo iptables -A INPUT -s 10.100.0.0/24 -p tcp --dport 30090 -j ACCEPT
```

---

## Environment Setup

### Automated Setup (Recommended)

Run the setup script on Kali Linux or Parrot OS:

```bash
cd agents/setup
./kali-parrot-setup.sh
```

This installs:
- Docker CLI
- kubectl
- Helm
- Networking tools (curl, wget, netcat, nmap)
- VPN tools (WireGuard, OpenVPN)
- Monitoring tools (htop, iotop)

### Manual Setup

If you prefer manual installation:

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Configure kubectl

```bash
# Create config directory
mkdir -p ~/.kube

# Copy kubeconfig (get from cluster admin)
cp /path/to/kubeconfig ~/.kube/config

# Verify access
kubectl get nodes
kubectl get pods --all-namespaces
```

---

## Authentication & Security

### 1. Kubernetes RBAC

Deploy agent RBAC configuration:

```bash
# Apply RBAC policies
kubectl apply -f agents/config/agent-rbac.yaml

# Verify service account
kubectl get serviceaccount inline-agent -n agents

# Get token for API access
kubectl create token inline-agent -n agents --duration=24h
```

### 2. Network Security

**Network policies are automatically applied via RBAC configuration.**

Review network policy:
```bash
kubectl get networkpolicy -n agents
kubectl describe networkpolicy agent-network-policy -n agents
```

### 3. API Authentication

Export token for API calls:

```bash
# Get service account token
export AGENT_TOKEN=$(kubectl create token inline-agent -n agents)

# Test authenticated request
curl -H "Authorization: Bearer $AGENT_TOKEN" \
  http://<vpn-ip>:30000/api/v1/pods
```

---

## Agent Interaction

### Using kubectl Helper Script

The helper script provides convenient commands:

```bash
# List pods
./agents/scripts/agent-kubectl-helper.sh pods ops

# Get logs
./agents/scripts/agent-kubectl-helper.sh logs discord-ops-bot-abc123 ops

# Execute command in pod
./agents/scripts/agent-kubectl-helper.sh exec discord-ops-bot-abc123 "ps aux"

# Check cluster status
./agents/scripts/agent-kubectl-helper.sh status

# View metrics
./agents/scripts/agent-kubectl-helper.sh metrics
```

### Direct kubectl Commands

```bash
# Accessing Kubernetes from Kali/Parrot
kubectl get pods -n ops
kubectl logs -f deployment/discord-ops-bot -n ops
kubectl exec -it discord-ops-bot-abc123 -n ops -- /bin/bash
```

### Testing API Endpoints

```bash
# Health check
curl http://<vpn-ip>:30000/health

# List pods via API
curl http://<vpn-ip>:30000/api/v1/pods

# Get metrics
curl http://<vpn-ip>:30090/metrics

# With authentication
curl -H "Authorization: Bearer $AGENT_TOKEN" \
  http://<vpn-ip>:30000/api/v1/execute \
  -d '{"pod": "discord-ops-bot-abc123", "command": "ps aux"}'
```

### Docker Interaction

```bash
# List containers
docker ps

# Execute in container
docker exec -it agent-api-gateway sh

# View logs
docker logs agent-api-gateway

# Inspect container
docker inspect agent-api-gateway
```

---

## Collaboration Workflow

### 1. Shared Tools Setup

#### Grafana Dashboard

Access monitoring dashboard:
```bash
# Port forward to local machine
kubectl port-forward -n monitoring svc/grafana 3000:3000

# Or access via NodePort if configured
```

Browse to: `http://localhost:3000`

#### Jupyter Notebooks (Optional)

Deploy collaborative notebooks:
```bash
# Deploy JupyterHub
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm install jupyterhub jupyterhub/jupyterhub \
  --namespace jupyter \
  --create-namespace
```

### 2. Logging and Monitoring

#### ELK Stack

Monitor logs in real-time:
```bash
# View logs through Loki
curl -G -s "http://<vpn-ip>:3100/loki/api/v1/query" \
  --data-urlencode 'query={namespace="ops"}' | jq .
```

#### Prometheus Metrics

Query metrics:
```bash
# CPU usage
curl 'http://<vpn-ip>:30090/api/v1/query?query=container_cpu_usage_seconds_total'

# Memory usage
curl 'http://<vpn-ip>:30090/api/v1/query?query=container_memory_usage_bytes'
```

### 3. Real-time Collaboration

#### Shared Command Execution

Agents can execute commands and share results:

```bash
# Agent 1 runs command
kubectl exec -it discord-ops-bot-abc123 -n ops -- ps aux > /tmp/process-list.txt

# Copy to shared volume
kubectl cp /tmp/process-list.txt ops/discord-ops-bot-abc123:/shared/

# Agent 2 retrieves results
kubectl cp ops/discord-ops-bot-abc123:/shared/process-list.txt ./results.txt
```

#### Event-driven Workflows

Monitor events for collaboration:
```bash
# Watch for changes
kubectl get events -n ops --watch

# Filter specific events
kubectl get events -n ops --field-selector type=Warning
```

---

## Troubleshooting

### Connection Test

Run comprehensive connection test:
```bash
cd agents/scripts
./test-agent-connection.sh
```

### Common Issues

#### VPN Not Connecting

**Symptom:** Cannot reach cluster IP through VPN

**Solution:**
```bash
# Check VPN status
sudo wg show
# or
sudo systemctl status openvpn@agent

# Restart VPN
sudo wg-quick down wg0 && sudo wg-quick up wg0

# Check routing
ip route show
```

#### kubectl Access Denied

**Symptom:** `Error from server (Forbidden)`

**Solution:**
```bash
# Verify RBAC configuration
kubectl auth can-i list pods --namespace=ops --as=system:serviceaccount:agents:inline-agent

# Check service account token
kubectl get serviceaccount inline-agent -n agents -o yaml

# Reapply RBAC if needed
kubectl apply -f agents/config/agent-rbac.yaml
```

#### API Endpoint Unreachable

**Symptom:** `Connection refused` on NodePort

**Solution:**
```bash
# Check service status
kubectl get svc agent-api -n ops

# Verify pod is running
kubectl get pods -n ops | grep agent-api

# Check firewall
sudo ufw status
sudo iptables -L -n | grep 30000

# Test from cluster node
ssh node-ip
curl http://localhost:30000/health
```

#### Docker Connection Issues

**Symptom:** `Cannot connect to Docker daemon`

**Solution:**
```bash
# Check Docker status
sudo systemctl status docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Restart Docker
sudo systemctl restart docker
```

### Debug Mode

Enable verbose logging:

```bash
# kubectl verbose mode
kubectl get pods -v=8

# Docker debug mode
export DOCKER_DEBUG=1
docker ps

# curl verbose mode
curl -v http://<vpn-ip>:30000/health
```

### Getting Help

1. Check logs:
   ```bash
   kubectl logs -f deployment/agent-api -n ops
   docker logs agent-api-gateway
   ```

2. Review events:
   ```bash
   kubectl get events -n ops --sort-by='.lastTimestamp'
   ```

3. Verify connectivity:
   ```bash
   ping <vpn-ip>
   telnet <vpn-ip> 30000
   ```

---

## Additional Resources

- [Network Configuration](network-config.yaml) - Full network settings
- [RBAC Configuration](agent-rbac.yaml) - Kubernetes access control
- [API Service Definition](agent-api-service.yaml) - Service specifications
- [Setup Script](../setup/kali-parrot-setup.sh) - Automated environment setup
- [Test Script](../scripts/test-agent-connection.sh) - Connectivity validation

For security concerns, refer to [SECURITY.md](../../SECURITY.md)

---

**Last Updated:** 2025-11-23  
**Maintained by:** Strategickhaos DAO LLC
