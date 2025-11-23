# Agent Collaboration Security Best Practices

Security guidelines for managing agent access to Kubernetes cluster and Docker services.

## Table of Contents

1. [Security Overview](#security-overview)
2. [Network Security](#network-security)
3. [Authentication & Authorization](#authentication--authorization)
4. [Secret Management](#secret-management)
5. [Monitoring & Auditing](#monitoring--auditing)
6. [Compliance](#compliance)

---

## Security Overview

### Security Principles

1. **Zero Trust Architecture** - Never trust, always verify
2. **Least Privilege Access** - Grant minimum required permissions
3. **Defense in Depth** - Multiple layers of security controls
4. **Secure by Default** - Security enabled by default, not opt-in
5. **Audit Everything** - Comprehensive logging and monitoring

### Threat Model

**Threats to Consider:**
- Unauthorized access to cluster resources
- Man-in-the-middle attacks on VPN connections
- Privilege escalation by compromised agents
- Data exfiltration through exposed services
- Denial of service attacks

---

## Network Security

### 1. VPN Configuration

**WireGuard Security:**

```bash
# Generate strong keys
wg genkey | tee privatekey | wg pubkey > publickey

# Verify key strength (should be 256-bit)
wg show wg0

# Regular key rotation (recommended: every 90 days)
sudo wg-quick down wg0
# Generate new keys
sudo wg-quick up wg0
```

**Security Checklist:**
- ✅ Use strong, randomly generated keys
- ✅ Rotate keys every 90 days
- ✅ Store private keys securely (chmod 600)
- ✅ Use PersistentKeepalive to prevent connection drops
- ✅ Restrict AllowedIPs to specific subnets

### 2. Firewall Rules

**UFW Configuration:**

```bash
# Default deny all incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow VPN subnet only
sudo ufw allow from 10.100.0.0/24 to any port 30000
sudo ufw allow from 10.100.0.0/24 to any port 30090

# Allow SSH (restrict to known IPs)
sudo ufw allow from <trusted-ip> to any port 22

# Enable firewall
sudo ufw enable
```

**iptables Configuration:**

```bash
# Drop all incoming by default
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow established connections
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow VPN subnet
sudo iptables -A INPUT -s 10.100.0.0/24 -p tcp --dport 30000 -j ACCEPT
sudo iptables -A INPUT -s 10.100.0.0/24 -p tcp --dport 30090 -j ACCEPT

# Save rules
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

### 3. Network Segmentation

**Kubernetes Network Policies:**

Already implemented in `agents/config/agent-rbac.yaml`:
- Isolates agent pods from other namespaces
- Restricts ingress to monitoring namespace only
- Allows egress to specific services only

**Verify Network Policies:**

```bash
# Check network policies
kubectl get networkpolicies -n agents

# Test connectivity (should fail)
kubectl run test -it --rm --image=alpine -n default -- \
  wget -O- http://agent-api.ops.svc.cluster.local

# Test from allowed namespace (should succeed)
kubectl run test -it --rm --image=alpine -n monitoring -- \
  wget -O- http://agent-api.ops.svc.cluster.local
```

---

## Authentication & Authorization

### 1. Service Account Management

**Create Service Account:**

```bash
# Create service account
kubectl create serviceaccount agent-user -n agents

# Grant role
kubectl create rolebinding agent-user-binding \
  --role=agent-reader \
  --serviceaccount=agents:agent-user \
  -n agents
```

**Token Management:**

```bash
# Generate time-limited token (24 hours)
kubectl create token agent-user -n agents --duration=24h

# Revoke access (delete service account)
kubectl delete serviceaccount agent-user -n agents
```

**Best Practices:**
- ✅ Use time-limited tokens (max 24 hours)
- ✅ Rotate tokens regularly
- ✅ One service account per agent/team
- ✅ Never commit tokens to git
- ✅ Store tokens in secure vaults (HashiCorp Vault, AWS Secrets Manager)

### 2. RBAC Configuration

**Review Permissions:**

```bash
# Check what agent can do
kubectl auth can-i --list --as=system:serviceaccount:agents:inline-agent -n agents

# Test specific permission
kubectl auth can-i delete pods \
  --as=system:serviceaccount:agents:inline-agent -n agents
```

**Principle of Least Privilege:**

The RBAC configuration provides:
- ✅ Read-only access to pods and services
- ✅ Limited exec access for debugging
- ✅ No delete/update permissions on critical resources
- ✅ No cluster-wide admin access

**Audit RBAC:**

```bash
# List all role bindings
kubectl get rolebindings -n agents

# Describe specific binding
kubectl describe rolebinding agent-reader-binding -n agents
```

### 3. API Authentication

**Bearer Token Authentication:**

```bash
# Export token
export AGENT_TOKEN=$(kubectl create token inline-agent -n agents)

# Use in API calls
curl -H "Authorization: Bearer $AGENT_TOKEN" \
  http://<vpn-ip>:30000/api/v1/pods
```

**Rate Limiting:**

Configured in `nginx-agent.conf`:
- 10 requests per second per IP
- Burst of 20 requests allowed
- 10 concurrent connections per IP

---

## Secret Management

### 1. Kubernetes Secrets

**Create Secret:**

```bash
# From literal values
kubectl create secret generic agent-credentials \
  --from-literal=api-token=<token> \
  -n agents

# From file
kubectl create secret generic agent-vpn \
  --from-file=vpn-key=/path/to/private.key \
  -n agents
```

**Access Secrets in Pods:**

```yaml
# In deployment spec
env:
  - name: API_TOKEN
    valueFrom:
      secretKeyRef:
        name: agent-credentials
        key: api-token
```

**Best Practices:**
- ✅ Use Kubernetes secrets for sensitive data
- ✅ Enable encryption at rest
- ✅ Restrict secret access via RBAC
- ✅ Rotate secrets regularly
- ✅ Never log secret values

### 2. External Secret Management

**HashiCorp Vault Integration:**

```bash
# Install Vault CSI driver
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault

# Configure secret
kubectl create secret generic vault-token \
  --from-literal=token=<vault-token> \
  -n agents
```

### 3. Secret Rotation

**Automated Rotation:**

```bash
# Create rotation script
cat > /usr/local/bin/rotate-agent-token.sh << 'EOF'
#!/bin/bash
NEW_TOKEN=$(kubectl create token inline-agent -n agents --duration=24h)
kubectl create secret generic agent-token \
  --from-literal=token=$NEW_TOKEN \
  --dry-run=client -o yaml | kubectl apply -f -
EOF

# Add to cron (daily rotation)
echo "0 2 * * * /usr/local/bin/rotate-agent-token.sh" | crontab -
```

---

## Monitoring & Auditing

### 1. Audit Logging

**Enable Kubernetes Audit Logging:**

```yaml
# /etc/kubernetes/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  # Log all requests from agent namespace
  - level: RequestResponse
    namespaces: ["agents"]
  # Log exec and port-forward
  - level: RequestResponse
    verbs: ["exec", "portforward"]
```

**View Audit Logs:**

```bash
# Check audit logs
kubectl logs -n kube-system kube-apiserver-* | grep agents

# Filter by service account
kubectl logs -n kube-system kube-apiserver-* | grep "serviceaccount:agents:inline-agent"
```

### 2. Real-time Monitoring

**Prometheus Alerts:**

```yaml
# Alert on unauthorized access attempts
- alert: UnauthorizedAgentAccess
  expr: |
    sum(rate(apiserver_request_total{
      user=~"system:serviceaccount:agents:.*",
      code=~"403"
    }[5m])) > 0
  annotations:
    summary: "Agent access denied"
```

**Monitor API Usage:**

```bash
# View agent API metrics
curl http://<vpn-ip>:30090/api/v1/query?query=nginx_http_requests_total

# Check rate limiting
curl http://<vpn-ip>:30090/api/v1/query?query=nginx_http_requests_rate_limited
```

### 3. Security Scanning

**Container Scanning:**

```bash
# Scan agent images
trivy image strategickhaos/agent-executor:latest

# Scan for CVEs
grype strategickhaos/agent-executor:latest
```

**Kubernetes Security Scanning:**

```bash
# Install kubescape
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash

# Scan agent namespace
kubescape scan namespace agents
```

---

## Compliance

### 1. PCI DSS Compliance

**Requirements:**
- ✅ Network segmentation implemented
- ✅ Encryption in transit (TLS)
- ✅ Access control via RBAC
- ✅ Audit logging enabled
- ✅ Regular security updates

### 2. SOC 2 Compliance

**Controls:**
- ✅ Access control (RBAC)
- ✅ Audit trails (Kubernetes audit logs)
- ✅ Encryption (TLS, VPN)
- ✅ Change management (GitOps)
- ✅ Incident response (monitoring, alerting)

### 3. GDPR Compliance

**Data Protection:**
- ✅ Data encryption in transit and at rest
- ✅ Access controls and authentication
- ✅ Audit logging for data access
- ✅ Data retention policies
- ✅ Right to erasure (secret deletion)

---

## Security Checklist

### Initial Setup
- [ ] Generate strong VPN keys
- [ ] Configure firewall rules
- [ ] Apply Kubernetes RBAC
- [ ] Enable network policies
- [ ] Configure audit logging
- [ ] Set up monitoring alerts

### Regular Maintenance
- [ ] Rotate VPN keys (every 90 days)
- [ ] Rotate service account tokens (daily)
- [ ] Review audit logs (weekly)
- [ ] Update dependencies (monthly)
- [ ] Scan for vulnerabilities (weekly)
- [ ] Review RBAC permissions (quarterly)

### Incident Response
- [ ] Monitor for unauthorized access
- [ ] Alert on suspicious activity
- [ ] Document security incidents
- [ ] Revoke compromised credentials
- [ ] Investigate root cause
- [ ] Update security policies

---

## Additional Resources

- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/security-best-practices/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Last Updated:** 2025-11-23
**Maintained by:** Strategickhaos DAO LLC
