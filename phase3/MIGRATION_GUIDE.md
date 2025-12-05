# Phase 2 → Phase 3 Migration Guide

## Overview

This guide documents the transition from **Phase 2 (Hybrid SaaS + Glue)** to **Phase 3 (Local Sovereignty)**. The goal is to replace external dependencies with self-hosted components while maintaining full functionality.

---

## Current State Analysis (Phase 2)

### External Dependencies

| Service | Function | Status | Replacement |
|---------|----------|--------|-------------|
| Zapier | Scheduling & webhooks | Active | `executor_server.py` |
| Grok API | AI signal generation | Active | Local model / API wrapper |
| Email (SNHU) | Notifications | Active | Local SMTP / Keep as-is |

### Self-Controlled Components

| Component | Status | Notes |
|-----------|--------|-------|
| NinjaTrader DOM | ✅ Owned | Trading interface |
| Trading Logic/Prompts | ✅ Owned | Intellectual property |
| Documentation | ✅ Owned | This repository |
| Legal Entities | ✅ Owned | Wyoming LLC + EIN |

### Current Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Zapier     │────▶│   Grok API   │────▶│  Your Code   │
│  (Schedule)  │     │ (Processing) │     │(Coordination)│
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                                                 ▼
                                          ┌──────────────┐
                                          │ NinjaTrader  │
                                          │    (Live)    │
                                          └──────────────┘
```

---

## Target State (Phase 3)

### Self-Hosted Components

| Component | Implementation | Status |
|-----------|----------------|--------|
| Local Scheduler | `executor_server.py` | ✅ Ready |
| Webhook Receiver | `executor_server.py` | ✅ Ready |
| Task Executor | `executor_server.py` | ✅ Ready |
| Anchor Generator | `generate_anchor.py` | ✅ Ready |

### Target Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    LOCAL SOVEREIGNTY ENGINE                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Scheduler   │──│   Executor   │──│   Handlers   │       │
│  │   (Local)    │  │   (Local)    │  │   (Local)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │   Webhook    │  │    Anchor    │                         │
│  │  Receiver    │  │  Generator   │                         │
│  └──────────────┘  └──────────────┘                         │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ NinjaTrader  │
                     │    (Live)    │
                     └──────────────┘
```

---

## Migration Steps

### Step 1: Deploy Local Executor Server

```bash
# Navigate to phase3 directory
cd phase3

# Install Python dependencies (none required - uses standard library)
# The executor server has zero external dependencies

# Start the server
python executor_server.py --port 8080

# Verify it's running
curl http://localhost:8080/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "phase": "3",
  "sovereignty": "local"
}
```

### Step 2: Test Local Execution

```bash
# List available tasks
curl http://localhost:8080/tasks

# Execute a task manually
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"task_id": "monthly_rebalance"}'

# Register a new task
curl -X POST http://localhost:8080/register \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "custom_signal",
    "name": "Custom Trading Signal",
    "handler": "log_signal",
    "payload": {"symbol": "ES", "action": "BUY"}
  }'
```

### Step 3: Configure Zapier → Local Server

**Zapier Webhook Action Configuration:**

1. Open Zapier Zap editor
2. Change "Send HTTP Request" action
3. Set URL: `http://YOUR_SERVER:8080/webhook`
4. Set Method: `POST`
5. Set Headers: `Content-Type: application/json`
6. Set Body:
```json
{
  "source": "zapier",
  "event": "scheduled_trigger",
  "data": {
    "timestamp": "{{zap_meta_human_now}}",
    "trigger": "monthly_rebalance"
  }
}
```

### Step 4: Validate Webhook Integration

```bash
# Simulate Zapier webhook
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "source": "zapier",
    "event": "test_trigger",
    "data": {
      "message": "Phase 3 integration test"
    }
  }'

# Check results
curl http://localhost:8080/results
```

### Step 5: Generate Verification Anchors

```bash
# Generate anchor for evidence dossier
python generate_anchor.py generate EVIDENCE_DOSSIER.md \
  --output anchors/ \
  --purpose "Phase 3 deployment verification"

# With GPG signing (if key available)
python generate_anchor.py generate EVIDENCE_DOSSIER.md \
  --output anchors/ \
  --sign \
  --key 261AEA44C0AF89CD

# Verify the anchor
python generate_anchor.py verify anchors/anchor_*.yaml EVIDENCE_DOSSIER.md
```

---

## Deployment Configurations

### Local Development

```bash
# Start executor server in development mode
LOG_LEVEL=DEBUG python executor_server.py --port 8080
```

### Production Deployment

**Option A: Direct Python Execution**
```bash
# Production mode with specific config
LOG_LEVEL=INFO python executor_server.py --port 8080
```

**Option B: Systemd Service (Linux)**
```ini
# /etc/systemd/system/executor.service
[Unit]
Description=Phase 3 Executor Server
After=network.target

[Service]
Type=simple
User=sovereignty
WorkingDirectory=/opt/sovereignty/phase3
ExecStart=/usr/bin/python3 executor_server.py --port 8080
Restart=always
Environment=LOG_LEVEL=INFO

[Install]
WantedBy=multi-user.target
```

**Option C: Docker Container**
```dockerfile
# Dockerfile.executor
FROM python:3.11-slim
WORKDIR /app
COPY phase3/executor_server.py .
EXPOSE 8080
CMD ["python", "executor_server.py", "--port", "8080"]
```

```bash
# Build and run
docker build -f Dockerfile.executor -t executor:phase3 .
docker run -d -p 8080:8080 --name executor executor:phase3
```

---

## Verification Checklist

### Phase 3 Deployment Verification

- [ ] Executor server starts without errors
- [ ] `/health` endpoint returns `"phase": "3"`
- [ ] `/status` shows `"sovereignty_level": "local"`
- [ ] Tasks can be registered via API
- [ ] Tasks can be executed via API
- [ ] Webhooks are received and processed
- [ ] Results are stored and retrievable
- [ ] Scheduler runs background tasks (verify logs)

### External Dependency Removal Verification

- [ ] Zapier webhooks point to local server
- [ ] No direct external API calls for core function
- [ ] All scheduling handled locally
- [ ] Anchor files generated locally

### Rollback Plan

If Phase 3 deployment fails:
1. Revert Zapier webhook URL to previous configuration
2. Stop local executor server
3. Document failure reason
4. Return to Phase 2 operation

---

## Sovereignty Metrics

### Before (Phase 2)

| Metric | Value |
|--------|-------|
| External Dependencies | 3 (Zapier, Grok API, Email) |
| Self-Hosted Components | 2 (NinjaTrader, Documentation) |
| Sovereignty Level | ~33% |
| Single Points of Failure | 3 external services |

### After (Phase 3)

| Metric | Value |
|--------|-------|
| External Dependencies | 1-2 (Email optional, AI API optional) |
| Self-Hosted Components | 5+ (Executor, Scheduler, Webhooks, Anchors, Docs) |
| Sovereignty Level | ~80% |
| Single Points of Failure | 1 (NinjaTrader - required for trading) |

---

## Next Steps After Phase 3

### Preparing for Phase 4 (Full Autonomy)

1. **Smart Contract Design**
   - DAO governance contracts
   - Automated distribution logic
   - On-chain verification anchors

2. **Blockchain Integration**
   - Select appropriate chain (Ethereum L2, Solana, etc.)
   - Deploy verification contracts
   - Implement anchor submission

3. **Full Decentralization**
   - Multi-node executor deployment
   - Consensus-based task execution
   - Automated charity distributions

---

## Troubleshooting

### Common Issues

**Issue: Server won't start**
```bash
# Check for port conflicts
lsof -i :8080

# Use different port
python executor_server.py --port 8081
```

**Issue: Webhook not received**
```bash
# Check server logs
LOG_LEVEL=DEBUG python executor_server.py

# Test with curl
curl -v -X POST http://localhost:8080/webhook -d '{"test":true}'
```

**Issue: GPG signing fails**
```bash
# Check GPG key availability
gpg --list-keys 261AEA44C0AF89CD

# Import key if needed
gpg --keyserver keys.openpgp.org --recv-keys 261AEA44C0AF89CD
```

---

## Conclusion

Phase 3 migration replaces external SaaS dependencies with locally-controlled components. This increases sovereignty from ~33% to ~80% while maintaining full functionality.

**Key Achievement:** Moving from "stitched SaaS + glue" to "self-contained local engine"

**What Remains External:**
- NinjaTrader (required for trading interface)
- AI APIs (can be self-hosted with local models in future)
- Email notifications (optional, can use local SMTP)

**You're not dependent anymore. You're sovereign.**

---

*Migration Guide v1.0*
*Phase 2 → Phase 3 Transition*
*Sovereignty Architecture Project*
