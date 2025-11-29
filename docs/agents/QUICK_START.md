# Agent Collaboration Quick Start

Get up and running with agent collaboration in minutes.

## Prerequisites

- Kali Linux or Parrot OS terminal
- Access to Kubernetes cluster
- VPN credentials (WireGuard or OpenVPN)

## 5-Minute Setup

### Step 1: Run Setup Script

```bash
cd agents/setup
./kali-parrot-setup.sh
```

This installs all required tools (Docker, kubectl, Helm, etc.)

### Step 2: Configure VPN

**For WireGuard:**
```bash
sudo cp agents/config/wireguard-agent.conf /etc/wireguard/wg0.conf
# Edit with your keys
sudo nano /etc/wireguard/wg0.conf
sudo wg-quick up wg0
```

**For OpenVPN:**
```bash
sudo openvpn --config agents/config/openvpn-agent.conf
```

### Step 3: Configure kubectl

```bash
# Copy your kubeconfig
mkdir -p ~/.kube
cp /path/to/your/kubeconfig ~/.kube/config

# Test connection
kubectl get nodes
```

### Step 4: Deploy Agent Infrastructure

```bash
# Deploy RBAC and services
kubectl apply -f agents/config/agent-rbac.yaml
kubectl apply -f agents/config/agent-api-service.yaml

# Verify deployment
kubectl get all -n agents
kubectl get svc -n ops
```

### Step 5: Test Connection

```bash
cd agents/scripts
./test-agent-connection.sh
```

## Common Commands

### Accessing Kubernetes

```bash
# List pods
kubectl get pods -n ops

# Get logs
kubectl logs -f deployment/discord-ops-bot -n ops

# Execute command
kubectl exec -it <pod-name> -n ops -- /bin/bash
```

### Testing API Endpoint

```bash
# Set your VPN IP
export VPN_IP=10.100.0.1

# Health check
curl http://$VPN_IP:30000/health

# API version
curl http://$VPN_IP:30000/api/version
```

### Using Helper Scripts

```bash
# Quick pod listing
./agents/scripts/agent-kubectl-helper.sh pods ops

# Get pod logs
./agents/scripts/agent-kubectl-helper.sh logs <pod-name> ops

# Check cluster status
./agents/scripts/agent-kubectl-helper.sh status
```

## Verify Setup

Run the comprehensive test:

```bash
cd agents/scripts
./test-agent-connection.sh
```

Expected output:
```
✓ VPN connection successful
✓ kubectl connected to cluster
✓ Can access pods in ops namespace
✓ Can discover services
✓ Docker is accessible
✓ API health endpoint responding
✓ Metrics endpoint responding

All tests passed! Agent collaboration environment is ready.
```

## Next Steps

1. **Review Documentation:**
   - [Complete Guide](AGENT_COLLABORATION.md)
   - [Troubleshooting](AGENT_COLLABORATION.md#troubleshooting)

2. **Explore Services:**
   - Access Grafana: `http://<vpn-ip>:3000`
   - View Prometheus: `http://<vpn-ip>:30090`

3. **Start Collaborating:**
   - Deploy your agent applications
   - Set up shared monitoring dashboards
   - Configure logging pipelines

## Troubleshooting

**VPN won't connect?**
```bash
# Check VPN status
sudo wg show  # WireGuard
# or
sudo systemctl status openvpn@agent  # OpenVPN

# Restart VPN
sudo wg-quick down wg0 && sudo wg-quick up wg0
```

**kubectl not working?**
```bash
# Verify config
kubectl config view

# Check connection
kubectl cluster-info

# Test authentication
kubectl auth can-i list pods --namespace=ops
```

**Can't reach API?**
```bash
# Check firewall
sudo ufw status

# Verify service
kubectl get svc agent-api -n ops

# Test from inside cluster
kubectl run test --rm -it --image=alpine -- wget -O- http://agent-api.ops.svc.cluster.local
```

## Getting Help

- Full Documentation: [AGENT_COLLABORATION.md](AGENT_COLLABORATION.md)
- Security Issues: [../../SECURITY.md](../../SECURITY.md)
- Community: [Discord Server](https://discord.gg/strategickhaos)

---

**Quick Reference Card:**

| Action | Command |
|--------|---------|
| Start VPN | `sudo wg-quick up wg0` |
| List pods | `kubectl get pods -n ops` |
| Test API | `curl http://$VPN_IP:30000/health` |
| Get logs | `kubectl logs -f <pod> -n ops` |
| Run test | `./agents/scripts/test-agent-connection.sh` |
