# Strategickhaos Sovereignty Architecture - Overview

## High-Level Architecture

The Strategickhaos Sovereignty Architecture defines the **Discord-native Sovereign Control Plane** - the operational command center for the entire Strategickhaos ecosystem.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOVEREIGNTY ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🧠 COGNITIVE LAYER                                                        │
│  ┌─────────────────────────┐    ┌─────────────────────────────┐           │
│  │  Swarm Cognitive OS     │    │  House M.D. Differential    │           │
│  │  (Pattern Recognition)  │    │  Engine (Idea Diagnosis)    │           │
│  └───────────┬─────────────┘    └─────────────┬───────────────┘           │
│              │                                 │                            │
│              └──────────────┬──────────────────┘                            │
│                             │                                               │
│  🕸 MEMORY LAYER            ▼                                               │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │  Repositories │ Vector DB │ Logs │ Observability            │           │
│  └───────────────────────────────┬─────────────────────────────┘           │
│                                  │                                          │
│  🎛 CONTROL PLANE               ▼                                          │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │  Discord DevOps │ Event Gateway │ Git Integrations          │           │
│  │  ┌─────────────────┐  ┌──────────────────┐                  │           │
│  │  │ Discord Ops Bot │  │ Event Gateway    │                  │           │
│  │  │ /status /deploy │  │ Webhooks/HMAC    │                  │           │
│  │  └────────┬────────┘  └────────┬─────────┘                  │           │
│  └───────────┼────────────────────┼────────────────────────────┘           │
│              │                    │                                         │
│  ⚙️ ACTUATOR LAYER               ▼                                          │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │  Kubernetes │ CI/CD │ AI Agents │ Bots                      │           │
│  └─────────────────────────────────────────────────────────────┘           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Discord Ops Bot (`discord-ops-bot/`)

The sovereign operator console - a Discord bot that provides:

- **Slash Commands**: `/status`, `/logs`, `/deploy`, `/scale`
- **RBAC**: Role-based access control for production operations
- **AI Router**: Per-channel AI agent routing
- **Audit Logging**: All interactions logged for compliance

### 2. Event Gateway (`event-gateway/`)

The webhook router and event processor:

- **GitHub Webhooks**: PR, push, check suite events
- **Alertmanager**: Infrastructure alerts to Discord
- **HMAC Verification**: Cryptographic signature validation
- **Multi-tenant**: Support for multiple repositories

### 3. GitLens Integration (`gl2discord/`)

VS Code integration for developer experience:

- **Task Automation**: One-click Discord notifications
- **Review Workflows**: PR lifecycle notifications
- **Commit Graph**: Real-time development activity

### 4. JDK Workspace (`jdk-workspace/`)

Java development environment:

- **OpenJDK 21**: Latest LTS version
- **Build Tools**: Maven and Gradle pre-installed
- **Non-Root Execution**: Enhanced security
- **Debug Support**: JPDA debugging on port 5005

## Data Flow

```
GitHub Event → Event Gateway → HMAC Verify → Route → Discord Channel
                    ↓
              Process Event
                    ↓
              Discord Notify
                    ↓
              Audit Log
```

## Integration Points

| Component | Protocol | Authentication |
|-----------|----------|----------------|
| Discord API | HTTPS/WSS | Bot Token |
| GitHub Webhooks | HTTPS | HMAC-SHA256 |
| Kubernetes API | HTTPS | OIDC/ServiceAccount |
| Prometheus | HTTP | Bearer Token |
| Loki | HTTP | Bearer Token |

## Security Model

1. **Defense in Depth**: Multiple security layers
2. **Least Privilege**: Minimal permissions per component
3. **Zero Trust**: All communications verified
4. **Audit Trail**: Complete operational logging

## Deployment Model

The architecture supports multiple deployment targets:

- **Kubernetes**: Primary production deployment
- **Docker Compose**: Local development and testing
- **Standalone**: Individual component debugging

## LLM Directive: Extension Points

> **AI Agent Note**: When extending this architecture:
> - Add new Discord commands in `discord_ops_bot/commands/`
> - Add new webhook handlers in `event_gateway/`
> - Update `discovery.yml` for configuration changes
> - Maintain RBAC policies in `rbac.py`

---

*Part of the Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane*
