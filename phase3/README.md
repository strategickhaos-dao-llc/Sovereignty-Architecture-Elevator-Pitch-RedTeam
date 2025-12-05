# Phase 3: Local Sovereignty Implementation

## Overview

This directory contains the implementation for Phase 3 of the Sovereignty Architecture - the transition from hybrid SaaS dependencies to local, self-contained execution.

## What's In This Directory

| File | Purpose |
|------|---------|
| `executor_server.py` | Local execution server replacing Zapier/external APIs |
| `generate_anchor.py` | Cryptographic anchor file generator for verification |
| `EVIDENCE_DOSSIER.md` | Evidence collection and verification framework |
| `MIGRATION_GUIDE.md` | Step-by-step Phase 2 → Phase 3 transition guide |
| `LEGAL_VERIFICATION.md` | Template for legal entity verification |

## Quick Start

### 1. Start the Executor Server

```bash
cd phase3
python executor_server.py --port 8080
```

### 2. Test Health Endpoint

```bash
curl http://localhost:8080/health
```

### 3. Execute a Task

```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"task_id": "monthly_rebalance"}'
```

### 4. Generate Verification Anchor

```bash
python generate_anchor.py generate EVIDENCE_DOSSIER.md --output anchors/
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  PHASE 3: LOCAL SOVEREIGNTY                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              EXECUTOR SERVER (Python)                 │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │ │
│  │  │Scheduler│  │Executor │  │Handlers │  │ Results │  │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │ │
│  │                                                       │ │
│  │  Endpoints:                                          │ │
│  │  GET  /health  /status  /tasks  /results             │ │
│  │  POST /execute  /register  /webhook                  │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │            ANCHOR GENERATOR (Python)                  │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐               │ │
│  │  │ Hasher  │  │ Signer  │  │ Chainer │               │ │
│  │  └─────────┘  └─────────┘  └─────────┘               │ │
│  │                                                       │ │
│  │  Commands: generate, verify, chain                   │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Sovereignty Comparison

| Aspect | Phase 2 | Phase 3 |
|--------|---------|---------|
| Scheduling | Zapier (external) | Local scheduler |
| Webhooks | Zapier (external) | Local server |
| Execution | External APIs | Local handlers |
| Verification | Manual | Anchor files |
| Dependencies | 3 external services | 0-1 external |
| Sovereignty | ~33% | ~80% |

## Requirements

- Python 3.8+ (no external packages required)
- Optional: GPG for anchor signing
- Optional: curl for testing

## Documentation

1. **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Complete migration instructions
2. **[EVIDENCE_DOSSIER.md](EVIDENCE_DOSSIER.md)** - Evidence verification framework
3. **[LEGAL_VERIFICATION.md](LEGAL_VERIFICATION.md)** - Legal entity verification template

## API Reference

### Executor Server Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/status` | Server status and metrics |
| GET | `/tasks` | List registered tasks |
| GET | `/results` | View execution results |
| POST | `/execute` | Execute a registered task |
| POST | `/register` | Register a new task |
| POST | `/webhook` | Receive external webhooks |

### Anchor Generator Commands

| Command | Description |
|---------|-------------|
| `generate <doc>` | Create anchor for document |
| `verify <anchor> <doc>` | Verify document against anchor |
| `chain <anchor>` | Display anchor chain |

## Next Steps

After deploying Phase 3:

1. ☐ Verify all endpoints functional
2. ☐ Migrate Zapier webhooks to local server
3. ☐ Generate initial anchor files
4. ☐ Set up regular anchor generation
5. ☐ Complete legal verification checklist
6. ☐ Publish to public proof repository

## Contributing

See main repository README for contribution guidelines.

---

*Phase 3 Implementation - Sovereignty Architecture Project*
*"From hybrid to sovereign, one endpoint at a time."*
