# Agent Collaboration Infrastructure

Infrastructure for enabling secure collaboration between inline agents and the Kubernetes/Docker environment.

## Overview

This directory contains all the necessary configuration files, scripts, and documentation to enable inline agents running on Kali Linux or Parrot OS to securely interact with the Kubernetes cluster and Docker services.

## Directory Structure

```
agents/
├── config/                           # Configuration files
│   ├── network-config.yaml          # Network and VPN settings
│   ├── agent-rbac.yaml              # Kubernetes RBAC policies
│   ├── agent-api-service.yaml       # API service definitions
│   ├── docker-compose.agent-services.yml  # Docker services
│   ├── wireguard-agent.conf         # WireGuard VPN template
│   └── openvpn-agent.conf           # OpenVPN configuration
├── scripts/                          # Utility scripts
│   ├── test-agent-connection.sh     # Connection testing
│   └── agent-kubectl-helper.sh      # kubectl convenience wrapper
└── setup/                            # Setup scripts
    └── kali-parrot-setup.sh         # Automated environment setup

```

## Quick Start

1. **Setup Environment:**
   ```bash
   cd agents/setup
   ./kali-parrot-setup.sh
   ```

2. **Configure VPN:**
   ```bash
   sudo cp config/wireguard-agent.conf /etc/wireguard/wg0.conf
   # Edit with your configuration
   sudo wg-quick up wg0
   ```

3. **Deploy Infrastructure:**
   ```bash
   kubectl apply -f config/agent-rbac.yaml
   kubectl apply -f config/agent-api-service.yaml
   ```

4. **Test Connection:**
   ```bash
   cd scripts
   ./test-agent-connection.sh
   ```

## Key Features

### Network Configuration
- **VPN Support:** WireGuard and OpenVPN templates
- **Port Forwarding:** Docker and Kubernetes service exposure
- **Security Policies:** IP whitelisting and firewall rules
- **Service Discovery:** DNS configuration for cluster services

### Authentication & Security
- **RBAC Policies:** Kubernetes role-based access control
- **Network Policies:** Pod-level network segmentation
- **Service Accounts:** Dedicated accounts for agent access
- **Token Management:** JWT token generation for API access

### Agent Interaction
- **REST API:** HTTP/HTTPS endpoints for cluster interaction
- **kubectl Helper:** Convenience scripts for common operations
- **Docker Access:** Direct container management capabilities
- **Metrics & Logs:** Monitoring and debugging interfaces

### Collaboration Tools
- **Shared Services:** Docker Compose stack for collaboration
- **Monitoring:** Prometheus and Grafana integration
- **Logging:** Loki for centralized log aggregation
- **Caching:** Redis for agent coordination

## Documentation

- **[Quick Start Guide](../docs/agents/QUICK_START.md)** - Get running in 5 minutes
- **[Complete Guide](../docs/agents/AGENT_COLLABORATION.md)** - Comprehensive documentation
- **[Troubleshooting](../docs/agents/AGENT_COLLABORATION.md#troubleshooting)** - Common issues and solutions

## Configuration Files

### network-config.yaml
Defines VPN, port forwarding, and security settings.

**Key sections:**
- VPN configuration (WireGuard/OpenVPN)
- Port forwarding rules for Docker and Kubernetes
- Firewall rules and IP whitelisting
- DNS service discovery

### agent-rbac.yaml
Kubernetes RBAC configuration for agent access.

**Includes:**
- Namespace creation (`agents`)
- Service account (`inline-agent`)
- Roles and permissions
- Network policies

### agent-api-service.yaml
Kubernetes Service and Deployment for agent API.

**Features:**
- NodePort service (ports 30000, 30443)
- REST API endpoints
- Health checks and metrics
- Rate limiting

### docker-compose.agent-services.yml
Docker services for agent collaboration.

**Services:**
- Agent API Gateway
- Command Executor
- Metrics (Prometheus)
- Logs (Loki)
- Cache (Redis)

## Scripts

### kali-parrot-setup.sh
Automated setup script for Kali Linux/Parrot OS.

**Installs:**
- Docker CLI
- kubectl and Helm
- Networking tools (curl, wget, nmap, netcat)
- VPN tools (WireGuard, OpenVPN)
- Monitoring tools (htop, iotop)

**Usage:**
```bash
cd agents/setup
./kali-parrot-setup.sh
```

### test-agent-connection.sh
Comprehensive connection testing.

**Tests:**
- VPN connectivity
- kubectl cluster access
- Pod and service access
- Docker connectivity
- API endpoint availability
- Metrics endpoint

**Usage:**
```bash
cd agents/scripts
./test-agent-connection.sh
```

### agent-kubectl-helper.sh
Convenience wrapper for common kubectl operations.

**Commands:**
- `pods [namespace]` - List pods
- `logs <pod> [namespace]` - Get pod logs
- `exec <pod> <command>` - Execute command in pod
- `services [namespace]` - List services
- `status` - Show cluster status
- `metrics` - Display cluster metrics
- `api-test` - Test API endpoints

**Usage:**
```bash
cd agents/scripts
./agent-kubectl-helper.sh status
./agent-kubectl-helper.sh pods ops
./agent-kubectl-helper.sh logs discord-ops-bot-abc123 ops
```

## Example Workflows

### Accessing Pods
```bash
# List pods in ops namespace
kubectl get pods -n ops

# Or use helper script
./agents/scripts/agent-kubectl-helper.sh pods ops
```

### Testing API Endpoint
```bash
# Set VPN IP
export VPN_IP=10.100.0.1

# Health check
curl http://$VPN_IP:30000/health

# List pods via API
curl http://$VPN_IP:30000/api/v1/pods
```

### Viewing Metrics
```bash
# Access Prometheus
curl http://$VPN_IP:30090/metrics

# Or use helper
./agents/scripts/agent-kubectl-helper.sh metrics
```

### Executing Commands
```bash
# Execute in pod
kubectl exec -it discord-ops-bot-abc123 -n ops -- /bin/bash

# Or use helper
./agents/scripts/agent-kubectl-helper.sh exec discord-ops-bot-abc123 "/bin/bash"
```

## Security Best Practices

1. **VPN Required:** Always connect through VPN before accessing cluster
2. **Token Rotation:** Regularly rotate service account tokens
3. **Least Privilege:** Use RBAC to limit agent permissions
4. **Network Policies:** Enforce pod-level network segmentation
5. **Audit Logging:** Monitor all agent interactions
6. **Firewall Rules:** Restrict access to known IP ranges

## Support

- **Issues:** [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- **Security:** See [SECURITY.md](../SECURITY.md)
- **Community:** [Discord Server](https://discord.gg/strategickhaos)

## Contributing

Contributions are welcome! Please ensure:
- All scripts are tested on Kali Linux and Parrot OS
- Documentation is updated for any configuration changes
- Security best practices are followed

## License

MIT License - See [LICENSE](../LICENSE) file

---

**Maintained by Strategickhaos DAO LLC**  
*Empowering sovereign digital infrastructure through secure agent collaboration*
