# Discord Workflow Integration

## Channel Strategy

The Strategickhaos Discord server is organized into functional channels that serve as the command and control interface for the entire infrastructure.

### Channel Mapping

| Channel | Purpose | Bot Actions |
|---------|---------|-------------|
| `#prs` | Pull request lifecycle | GitLens notifications, review requests |
| `#deployments` | CI/CD status, releases | Build notifications, deploy confirmations |
| `#cluster-status` | Infrastructure events | Service health, node status |
| `#alerts` | Critical system alerts | Alertmanager notifications |
| `#agents` | AI assistant interactions | LLM queries, automated responses |
| `#dev-feed` | Development activity | Commit summaries, branch updates |

## Discord Bot Commands

### `/status <service>`

Report high-level system status for a service.

```
User: /status event-gateway
Bot: 🧭 Sovereignty Architecture: status check
     Service: event-gateway
     State: Running
     Version: v1.2.3
     Replicas: 2/2
```

### `/logs <service> [tail]`

Fetch recent logs from Loki/CloudWatch.

```
User: /logs discord-ops-bot --tail 50
Bot: 📜 Last 50 lines from discord-ops-bot:
     [2024-01-15 10:23:45] INFO: Command /status executed
     [2024-01-15 10:23:46] INFO: Fetched metrics from Prometheus
     ...
```

### `/deploy <env> <tag>`

Trigger a deployment to the specified environment. **Protected command** - requires `ReleaseMgr` role.

```
User: /deploy staging v1.2.3
Bot: 🚀 Deploying v1.2.3 to staging
     Triggered workflow: deploy-staging-1234
     Monitor: https://github.com/org/repo/actions/runs/1234
```

### `/scale <service> <replicas>`

Scale a service to the specified replica count. **Protected command** - requires `ReleaseMgr` role.

```
User: /scale event-gateway 3
Bot: 📈 Scaling event-gateway to 3 replicas
     Previous: 2
     New: 3
     ETA: ~30 seconds
```

### `/ask <query>`

Route a question to the appropriate AI agent based on channel.

```
User: /ask What's the current deployment strategy for valoryield?
Bot: 🤖 [gpt-4o-mini] The valoryield-engine uses blue-green
     deployment with automatic rollback...
```

## Event Gateway Webhooks

### GitHub Events

The event gateway receives GitHub webhooks and routes them to appropriate Discord channels:

```yaml
routes:
  - event: "pull_request"
    actions: ["opened", "ready_for_review", "closed", "merged"]
    channel: "#prs"
  
  - event: "check_suite"
    channel: "#deployments"
  
  - event: "push"
    branches: ["main", "release/*"]
    channel: "#deployments"
```

### Alertmanager Events

Infrastructure alerts are routed to the `#alerts` channel:

```json
{
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "HighCPUUsage",
        "service": "event-gateway"
      },
      "annotations": {
        "summary": "CPU usage above 80%"
      }
    }
  ]
}
```

## GitLens Integration

### VS Code Tasks

Configure VS Code tasks to send notifications from GitLens:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "GitLens: Review Started",
      "type": "shell",
      "command": "./gl2discord.sh",
      "args": [
        "${env:PRS_CHANNEL}",
        "👀 Review Started",
        "Reviewing ${input:branch} in ${workspaceFolderBasename}"
      ]
    }
  ]
}
```

### Review Workflow

1. Developer opens PR in VS Code
2. GitLens detects PR context
3. Developer starts review via task
4. `gl2discord.sh` posts to `#prs`
5. Team notified of review activity

## RBAC Configuration

### Role Hierarchy

```yaml
roles:
  admin:
    permissions: ["*"]
    
  release_mgr:
    permissions:
      - "/deploy"
      - "/scale"
      - "/status"
      - "/logs"
      
  developer:
    permissions:
      - "/status"
      - "/logs"
      - "/ask"
      
  viewer:
    permissions:
      - "/status"
```

### Protected Commands

Commands that modify production state require elevated permissions:

```python
@check_permission("deploy")
async def deploy(ctx, env: str, ref: str = "main"):
    # Only users with 'deploy' permission can execute
    ...
```

## Audit Logging

All Discord interactions are logged for compliance:

```json
{
  "timestamp": "2024-01-15T10:23:45Z",
  "user": "dev@example.com",
  "user_id": "123456789",
  "command": "/deploy",
  "args": {"env": "staging", "tag": "v1.2.3"},
  "channel": "#deployments",
  "result": "success"
}
```

## LLM Directive: Extending Workflows

> **AI Agent Note**: When adding new Discord workflows:
> 1. Define the channel mapping in `discovery.yml`
> 2. Add command handler in `discord_ops_bot/commands/`
> 3. Update RBAC if command is protected
> 4. Add webhook route in `event_gateway/` if needed
> 5. Document the workflow here

---

*Part of the Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane*
