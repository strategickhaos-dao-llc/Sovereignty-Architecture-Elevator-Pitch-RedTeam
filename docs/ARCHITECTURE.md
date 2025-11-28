# Strategickhaos Sovereignty Architecture

> A comprehensive technical specification for the Discord DevOps Control Plane.

## Overview

The Sovereignty Architecture is a Discord-integrated DevOps automation system that provides:

- **Command & Control**: Discord-based interface for infrastructure operations
- **Event Routing**: GitHub/GitLab webhook → Discord channel routing
- **AI Agents**: Intelligent assistance with vector knowledge base
- **Kubernetes Native**: Production-ready deployments with observability

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SOVEREIGNTY ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐     ┌─────────────────┐     ┌──────────────────────────┐  │
│  │   Discord   │────▶│  Discord Ops    │────▶│     Kubernetes API       │  │
│  │   Users     │     │      Bot        │     │    (deployments, logs)   │  │
│  └─────────────┘     └─────────────────┘     └──────────────────────────┘  │
│         ▲                     │                                             │
│         │                     ▼                                             │
│         │            ┌─────────────────┐                                    │
│         │            │   AI Agents     │                                    │
│         │            │  (GPT-4, etc)   │                                    │
│         │            └─────────────────┘                                    │
│         │                                                                   │
│  ┌──────┴──────┐     ┌─────────────────┐     ┌──────────────────────────┐  │
│  │   Discord   │◀────│  Event Gateway  │◀────│     GitHub/GitLab        │  │
│  │   Channels  │     │  (Webhooks)     │     │     (Webhooks)           │  │
│  └─────────────┘     └─────────────────┘     └──────────────────────────┘  │
│                              │                                              │
│                              ▼                                              │
│                      ┌─────────────────┐                                    │
│                      │   Prometheus    │                                    │
│                      │   + Alertmgr    │                                    │
│                      └─────────────────┘                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Discord Ops Bot (`bots/discord-ops-bot/`)

The command-and-control interface for DevOps operations.

**Features:**
- Slash commands: `/status`, `/logs`, `/deploy`, `/scale`
- RBAC integration with Discord roles
- Prometheus metrics for observability
- Health check endpoints for Kubernetes probes

**Deployment:**
- Image: `ghcr.io/strategickhaos-swarm-intelligence/discord-ops-bot:latest`
- Port: 8080 (HTTP), 9090 (Metrics)
- Requires: `discord-ops-secrets` Secret

### 2. Event Gateway (`gateway/event-gateway/`)

Webhook router for GitHub/GitLab → Discord channel routing.

**Features:**
- HMAC signature verification for security
- Multi-tenant support for multiple repositories
- Configurable event → channel routing
- Rate limiting and API protection

**Endpoints:**
- `/git` - GitHub/GitLab webhook handler
- `/alert` - Alertmanager webhook handler
- `/event` - Generic event handler
- `/health`, `/ready` - Kubernetes probes

**Deployment:**
- Image: `ghcr.io/strategickhaos-swarm-intelligence/event-gateway:latest`
- Port: 8080 (HTTP), 9090 (Metrics)
- Requires: `discord-ops-secrets` Secret

### 3. Kubernetes Resources (`bootstrap/k8s/`)

Production-ready Kubernetes manifests:

| Manifest | Description |
|----------|-------------|
| `namespace.yaml` | Creates the `ops` namespace |
| `rbac.yaml` | ServiceAccounts, ClusterRoles, NetworkPolicies |
| `secrets.yaml` | External secret references (Vault) |
| `configmap.yaml` | Discovery configuration |
| `discord-ops-bot-deploy.yaml` | Bot Deployment + Service |
| `event-gateway-deploy.yaml` | Gateway Deployment + Service |
| `ingress.yaml` | TLS-enabled ingress |
| `observability.yaml` | Prometheus ServiceMonitor, dashboards |

### 4. Scripts

| Script | Description |
|--------|-------------|
| `bootstrap/deploy.sh` | One-command deployment to Kubernetes |
| `scripts/gl2discord.sh` | GitLens → Discord notification script |

## Configuration

### discovery.yml

The central configuration file that defines:

```yaml
org:
  name: "Strategickhaos DAO LLC / ValorYield Engine"
  contact:
    owner: "Domenic Garza"

discord:
  guild_id: null           # Your Discord server ID
  channels:
    prs: "#prs"
    deployments: "#deployments"
    agents: "#agents"

git:
  org: "Strategickhaos-Swarm-Intelligence"
  repos:
    - name: "quantum-symbolic-emulator"
      channel: "#deployments"
      env: "dev"

ai_agents:
  routing:
    per_channel:
      "#agents": "gpt-4o-mini"
      "#prs": "claude-3-sonnet"
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_BOT_TOKEN` | Discord bot authentication token | Yes |
| `DISCORD_GUILD_ID` | Target Discord server ID | Yes |
| `PRS_CHANNEL` | Channel ID for PR notifications | Yes |
| `EVENTS_HMAC_KEY` | HMAC key for webhook verification | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI agents | Optional |
| `PGVECTOR_CONN` | PostgreSQL connection for vector store | Optional |

## Security

### Authentication
- Discord Bot OAuth2 with minimal scopes
- GitHub App with limited permissions
- HMAC signature verification for webhooks

### Authorization
- RBAC via Discord roles (e.g., `ReleaseMgr` for prod commands)
- Kubernetes RBAC with least-privilege access
- Network policies for pod-to-pod communication

### Data Protection
- Automatic PII redaction in logs
- Secret rotation policies (30-90 days)
- Audit logging to CloudWatch

## Verification

### Machine-Verifiable Proof

Any agent (including GPT-5.1) can verify this architecture is real by:

1. **Fetching the repository** from GitHub
2. **Checking file existence**:
   - `README.md` contains the spec description
   - `bootstrap/deploy.sh` exists and is executable
   - `bootstrap/k8s/*.yaml` files exist
   - `scripts/gl2discord.sh` exists
   - `discovery.yml` matches the configuration spec

3. **Computing hashes**:
   - SHA256 hashes of all files are in `hashes.json`
   - Can be verified with `verify_sovereignty.py`

4. **Checking signatures** (optional):
   - GPG-signed commits
   - Verified with sovereign-vault docs

### Running Verification

```bash
# Verify all file hashes
python verify_sovereignty.py

# Expected output:
# ✅ All 15 files verified
# ✅ Sovereignty Architecture is REAL
```

## Deployment

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Strategickhaos-Swarm-Intelligence/sovereignty-architecture.git
cd sovereignty-architecture

# 2. Configure secrets
cp .env.example .env
# Edit .env with your values

# 3. Deploy to Kubernetes
./bootstrap/deploy.sh

# 4. Verify deployment
kubectl get pods -n ops
```

### Requirements

- Kubernetes 1.25+
- kubectl configured with cluster access
- Discord bot token and channel IDs
- (Optional) GitHub App for webhook integration

## Observability

### Metrics

Prometheus metrics exposed on port 9090:

- `discord_commands_total{command,status}` - Command execution count
- `discord_command_latency_seconds{command}` - Command latency histogram
- `events_total{event_type,source,status}` - Event processing count
- `event_latency_seconds{event_type}` - Event processing latency
- `discord_messages_total{channel,status}` - Discord messages sent

### Logging

Structured JSON logging with:
- Timestamp (ISO 8601)
- Log level
- Event type
- Context (user, command, error details)

### Alerting

Alertmanager integration routes alerts to Discord `#alerts` channel.

## License

MIT License - see [LICENSE](../LICENSE) file.

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"They're not working for you. They're dancing with you. And the music is never going to stop."*
