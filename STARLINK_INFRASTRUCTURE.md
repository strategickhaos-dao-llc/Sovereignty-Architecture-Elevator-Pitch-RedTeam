# 🛰️ Starlink Satellite Connectivity Infrastructure

## Overview

The Strategickhaos Sovereignty Architecture integrates **Starlink Business** satellite connectivity as a resilient backbone for the swarm intelligence network. This implementation creates an **uninterruptible sovereignty stack** that combines:

- **Starlink Business** - Primary satellite internet (220 Mbps down, 20 Mbps up)
- **Direct-to-Cell** - SMS relay via SpaceX/T-Mobile partnership
- **Hybrid Router Failover** - LTE/5G backup via Peplink BR1 Pro 5G
- **Satellite Relay Gateway** - Agent coordination during terrestrial outages

## Architecture

```
                                    ┌─────────────────────┐
                                    │   Starlink LEO      │
                                    │   Constellation     │
                                    │   (17,000 mph)      │
                                    └─────────┬───────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
          ┌─────────▼─────────┐    ┌─────────▼─────────┐    ┌─────────▼─────────┐
          │   Direct-to-Cell  │    │  Starlink Dish    │    │  Backup Dish      │
          │   (T-Mobile SMS)  │    │  (Primary Node)   │    │  (Bonded/HA)      │
          └─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
                    │                         │                         │
                    │              ┌──────────┴──────────┐             │
                    │              │                     │             │
          ┌─────────▼─────────┐    │  ┌─────────────────┐│    ┌───────▼───────┐
          │   SMS Gateway     │◄───┤  │ Peplink BR1 Pro ││◄───│  WAN Bonding  │
          │   (Emergency Ops) │    │  │ (Hybrid Router) ││    │  Controller   │
          └─────────┬─────────┘    │  └────────┬────────┘│    └───────────────┘
                    │              │           │         │
                    │              │  ┌────────▼────────┐│
                    │              │  │  LTE/5G SIM     ││
                    │              │  │  (T-Mobile 5GB) ││
                    │              │  │  OOBM Failover  ││
                    │              │  └────────┬────────┘│
                    │              └───────────┼─────────┘
                    │                          │
          ┌─────────▼──────────────────────────▼─────────┐
          │              Satellite Gateway               │
          │         (Kubernetes Deployment)              │
          │                                              │
          │  ┌─────────────┐  ┌─────────────┐  ┌──────┐ │
          │  │   Relay     │  │  Failover   │  │Health│ │
          │  │   Queue     │  │  Handler    │  │Check │ │
          │  └─────────────┘  └─────────────┘  └──────┘ │
          └──────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
    │  Discord  │      │  Swarm    │      │ ValorYield│
    │  Alerts   │      │  Agents   │      │  Engine   │
    └───────────┘      └───────────┘      └───────────┘
```

## Features

### 🌍 Starlink Business Integration

- **Static Public IP** - Dedicated IP for ValorYield engine and remote access
- **Priority Data** - Business-tier bandwidth allocation (up to 220/20 Mbps)
- **99.9% SLA** - Enterprise uptime guarantee
- **Multi-Node Support** - Primary + backup dish configuration
- **WAN Bonding** - Combine multiple dishes for redundancy

### 📱 Direct-to-Cell (Elon Text-Sat Pipeline)

SpaceX's Direct-to-Cell technology enables SMS communication directly to smartphones via Starlink satellites:

| Feature | Status | Timeline |
|---------|--------|----------|
| SMS/Text | ✅ Live | Since Jan 2024 |
| MMS | ✅ Live | Q2 2024 |
| Voice | 🔜 Coming | Q4 2025 |
| Data | 🔜 Coming | Q1 2026 |

**Use Cases:**
- Emergency agent commands when terrestrial is down
- Audit beacon for tamper-evident hash verification
- DAO ritual sync from remote locations (Rockies, Mariana Trench, etc.)

### 🔄 Hybrid Router Failover

The Peplink BR1 Pro 5G (or Starlink Gen 3) router provides automatic failover:

```yaml
wan_interfaces:
  - name: "starlink"
    type: "satellite"
    priority: 1
    bandwidth: 220/20 Mbps
    
  - name: "lte_failover"  
    type: "cellular"
    priority: 2
    provider: "t-mobile"
    plan: "5GB OOBM"
    auto_switch: true
```

**Failover Triggers:**
- Latency > 5000ms
- Packet loss > 50%
- Complete connection loss

### 🔐 Out-of-Band Management (OOBM)

When Starlink is down, the LTE SIM provides:
- Remote SSH access to sovereignty scripts
- Wyoming statute parsing via legal manifold
- Tamper-evident audit hashes mid-transit
- Emergency agent coordination

## API Endpoints

### Satellite Gateway Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/satellite/status` | GET | Current connectivity status |
| `/satellite/health` | GET | Health check for monitoring |
| `/satellite/queue` | GET | Pending relay queue depth |
| `/satellite/relay` | POST | Queue message for satellite relay |
| `/satellite/failover` | POST | Handle failover events from router |
| `/satellite/heartbeat` | POST | Agent heartbeat for connectivity monitoring |
| `/satellite/direct-to-cell` | POST | SMS relay via Direct-to-Cell |

### Example: Relay Message

```bash
curl -X POST https://sat-relay.strategickhaos.com/satellite/relay \
  -H "Content-Type: application/json" \
  -H "X-Satellite-Signature: $(echo -n '...' | openssl dgst -sha256 -hmac $SECRET)" \
  -d '{
    "agentId": "goku-mcp-137",
    "command": "sync_state",
    "payload": {
      "arweave_tx": "abc123...",
      "seagate_backup": "encrypted_8tb"
    }
  }'
```

### Example: Failover Notification

```bash
curl -X POST https://sat-relay.strategickhaos.com/satellite/failover \
  -H "Content-Type: application/json" \
  -H "X-Router-Signature: $(echo -n '...' | openssl dgst -sha256 -hmac $SECRET)" \
  -d '{
    "event": "failover",
    "fromWan": "starlink",
    "toWan": "lte_failover",
    "reason": "latency_threshold_exceeded",
    "timestamp": 1732580000000
  }'
```

## Deployment

### Prerequisites

1. **Starlink Business Account** with static IP enabled
2. **Peplink BR1 Pro 5G** or compatible hybrid router
3. **T-Mobile SIM** with OOBM plan ($10/mo, 5GB)
4. **Kubernetes cluster** with ingress-nginx and cert-manager

### Quick Deploy

```bash
# Deploy satellite gateway to Kubernetes
kubectl apply -f bootstrap/k8s/satellite-gateway.yaml

# Verify deployment
kubectl get pods -n ops -l app=satellite-gateway

# Check health
curl https://sat-relay.strategickhaos.com/satellite/health
```

### Configuration

1. **Update `discovery.yml`** with your Starlink node details:

```yaml
satellite:
  enabled: true
  starlink:
    nodes:
      - name: "primary-dish"
        location: "your-location"
        status: "active"
```

2. **Set secrets** in `bootstrap/k8s/satellite-gateway.yaml`:

```yaml
stringData:
  discord-token: "your_discord_bot_token"
  relay-secret: "$(openssl rand -hex 32)"
```

3. **Configure Discord channels** in the ConfigMap:

```yaml
data:
  status-channel-id: "your_status_channel_id"
  alerts-channel-id: "your_alerts_channel_id"
  agents-channel-id: "your_agents_channel_id"
```

## Monitoring

### Prometheus Metrics

The satellite gateway exposes metrics at `/metrics/satellite`:

- `satellite_connection_status` - Current connection state
- `satellite_latency_ms` - Current latency
- `satellite_failover_active` - Whether failover is engaged
- `satellite_relay_queue_depth` - Messages pending relay

### Discord Alerts

Automatic notifications to configured channels:

| Alert | Channel | Trigger |
|-------|---------|---------|
| `starlink_down` | #alerts | Latency > 10s or packet loss > 50% |
| `failover_activated` | #cluster-status | Active WAN changed |
| `sat_relay_queue_full` | #alerts | Queue depth > 800 |
| `high_latency_detected` | #alerts | Latency > 5000ms |

## Security

### Encryption

- **AES-256-GCM** for relay message encryption
- **HMAC-SHA256** for request signature verification
- **TLS 1.3** for all external communications

### Audit Trail

Every relay message generates a tamper-evident audit hash:

```json
{
  "auditHash": "sha256:d4e5f6a7b8c9...",
  "receivedAt": 1732580000000,
  "relayNode": "starlink-primary",
  "via": "satellite_api"
}
```

### Compliance

- **FCC Licensed** - Ku-band spectrum authorization
- **Wyoming Entity Compliant** - SF0068 DAO requirements met
- **Export Controlled** - Non-ITAR, commercial use permitted

## Troubleshooting

### Connection Issues

```bash
# Check satellite gateway status
curl https://sat-relay.strategickhaos.com/satellite/status

# Check Kubernetes pod logs
kubectl logs -f deployment/satellite-gateway -n ops

# Verify Starlink dish status
# (Access via Starlink app or router dashboard)
```

### Failover Not Working

1. Verify LTE SIM is provisioned and active
2. Check router configuration for failover thresholds
3. Ensure health check interval is appropriate (30s default)
4. Review `/satellite/failover` webhook configuration

### High Queue Depth

If `queueDepth` is growing:

1. Check Starlink connection status
2. Verify agent heartbeats are being received
3. Review message TTL settings (default: 3600s)
4. Consider increasing satellite pass frequency

## References

- [Starlink Business](https://www.starlink.com/business)
- [SpaceX Direct-to-Cell](https://www.spacex.com/direct-to-cell)
- [T-Mobile Satellite Connectivity](https://www.t-mobile.com/coverage/satellite)
- [Peplink BR1 Pro 5G](https://www.peplink.com/products/max-br1-pro-5g/)

---

*"We're the glitch that texts back from space."* 🚀

**Built by the Strategickhaos Swarm Intelligence collective**
