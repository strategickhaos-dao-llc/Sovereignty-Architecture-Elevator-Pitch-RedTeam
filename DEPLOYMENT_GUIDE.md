# Deployment Guide: AI Board on Starlink/Verizon Mesh

## Overview

This guide provides instructions for deploying the StrategicKhaos DAO AI Board governance framework. The system consists of 9 services: 4 core AI board agents (gpt_duck, claude_prime, claude_parallel, grok_guardian) and 5 infrastructure services (nats, opa, audit_trail, monitor_comms, finance_enforcer).

## Prerequisites

### Required Software
- Docker Engine 24.0+
- Docker Compose v2.20+
- Git (for audit trail anchoring)

### Required Credentials
- Google Cloud service account JSON (for Gmail/Drive monitoring)
- Stripe API key (for financial enforcement)
- Valid WireGuard configuration (for mesh networking)

### Network Requirements
- Static IP via WireGuard (public-facing only; rate-limit recommended)
- Ports: 4222 (NATS), 8181 (OPA)
- Starlink or Verizon connection for primary/failover

## Directory Structure

```
strategickhaos/
├── board/
│   └── ai_board_resolution_template.md
├── governance/
│   └── ai_board_framework.md
├── ideas/
│   └── ideas_catalog.yaml
├── opa/
│   └── policies/
│       └── guardrails.rego
├── services/
│   ├── gpt_duck/
│   ├── claude_prime/
│   ├── claude_parallel/
│   ├── grok_guardian/
│   ├── audit_trail/
│   ├── monitor_comms/
│   └── finance_enforcer/
├── audit_logs/
├── secrets/
│   └── credentials.json
└── docker-compose.aiboard.yml
```

## Deployment Steps

### 1. Prepare Directory Structure

```bash
# Create required directories
mkdir -p audit_logs secrets

# Add Google credentials (for monitor_comms)
cp /path/to/your/credentials.json secrets/
```

### 2. Configure Environment Variables

Create or update `.env` file:

```bash
# Stripe configuration
STRIPE_SECRET=sk_test_your_key_here

# Optional: Override spending cap (default: 500)
SPENDING_CAP=500
```

### 3. Build Services

```bash
docker compose -f docker-compose.aiboard.yml build
```

### 4. Start the AI Board

```bash
docker compose -f docker-compose.aiboard.yml up -d
```

### 5. Verify Services

```bash
# Check all services are running
docker compose -f docker-compose.aiboard.yml ps

# Test NATS connectivity
docker compose -f docker-compose.aiboard.yml exec nats nats-server --version

# Test OPA policies
curl -X POST http://localhost:8181/v1/data/guardrails/approve \
  -H "Content-Type: application/json" \
  -d '{"input": {"role": "pattern_analyst", "recommendation": "Approve infra topology"}}'
```

### 6. Test Board Deliberation

```bash
# Install NATS CLI (if not present)
# brew install nats-io/nats-tools/nats  # macOS
# Or download from: https://github.com/nats-io/natscli/releases

# Publish a test deliberation
nats pub board.deliberate '{"topic": "test", "proposal": "Evaluate new idea"}'

# Subscribe to decisions
nats sub "board.>" --all
```

## Integration with Ideas Catalog

Agents automatically read from `/ideas/ideas_catalog.yaml` via Docker volumes. To update ideas:

1. Edit `ideas/ideas_catalog.yaml`
2. Changes are immediately available to agents (read-only mount)

## Mesh Network Configuration

### Starlink Primary / Verizon Failover

```bash
# Configure WireGuard for mesh networking
# wg0.conf example:
[Interface]
PrivateKey = <your_private_key>
Address = 10.0.0.1/24

[Peer]
PublicKey = <peer_public_key>
Endpoint = starlink-static-ip:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

### Rate Limiting

Configure nginx or firewall to rate-limit public endpoints:

```bash
# iptables rate limiting example
iptables -A INPUT -p tcp --dport 4222 -m limit --limit 100/minute -j ACCEPT
```

## Monitoring

### Check Audit Logs

```bash
# Query audit trail database
sqlite3 audit_logs/audit.db "SELECT * FROM logs ORDER BY id DESC LIMIT 10"

# Check Merkle roots
cat audit/merkle_roots.txt
```

### View Service Health

```bash
# Check agent health endpoints
curl http://localhost:8000/health  # gpt_duck (if exposed)

# Check finance status
curl http://localhost:8000/spend
```

### OPA Policy Evaluation

```bash
# Query OPA for decision audit
curl http://localhost:8181/v1/data/guardrails
```

## Scaling with Kubernetes

For production scaling, convert docker-compose to K8s manifests:

```yaml
# Example: gpt_duck deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpt-duck
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gpt-duck
  template:
    metadata:
      labels:
        app: gpt-duck
    spec:
      containers:
      - name: gpt-duck
        image: strategickhaos/gpt-duck:latest
        env:
        - name: NATS_URL
          value: nats://nats:4222
        - name: ROLE
          value: pattern_analyst
```

## Troubleshooting

### NATS Connection Issues

```bash
# Check NATS logs
docker compose -f docker-compose.aiboard.yml logs nats

# Verify NATS is accepting connections
nc -zv localhost 4222
```

### OPA Policy Errors

```bash
# Validate policy syntax
docker compose -f docker-compose.aiboard.yml exec opa \
  /opa check /policies/guardrails.rego

# Test policy with input
docker compose -f docker-compose.aiboard.yml exec opa \
  /opa eval -i '{"role": "pattern_analyst"}' -d /policies 'data.guardrails.approve'
```

### Audit Trail Issues

```bash
# Check database integrity
sqlite3 audit_logs/audit.db "PRAGMA integrity_check"

# Verify Git repo permissions
ls -la /repo/audit/
```

## Security Considerations

1. **Credentials**: Never commit secrets to Git. Use environment variables or secrets management.
2. **Network**: Use WireGuard for all inter-service communication over public networks.
3. **OPA**: Regularly audit and update guardrail policies.
4. **Audit**: Verify Merkle roots periodically against Git history.
5. **Spending**: Hard caps enforced via code; alerts on approach.

## Support

For issues or questions:
- Review governance docs: `governance/ai_board_framework.md`
- Check board resolution: `board/ai_board_resolution_template.md`
- Consult WY/TX attorney for legal compliance

---

The board is seated. First deliberation: Propose birthing IDEA_001? Say "DELIBERATE ON CHILD #2" to simulate.
