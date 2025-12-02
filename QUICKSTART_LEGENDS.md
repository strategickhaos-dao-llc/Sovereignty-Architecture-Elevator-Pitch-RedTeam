# Legends of Minds - Quick Start Guide

## What You Just Got

A **production-ready, local AI stack** with comprehensive safety monitoring. No cloud. No subscriptions. No mystery boxes.

## Installation (2 Minutes)

### 1. Prerequisites

```powershell
# Verify you have:
docker --version       # Docker Desktop installed
python --version       # Python 3.12+
nvidia-smi            # (Optional) NVIDIA GPU
```

### 2. Deploy

```powershell
# Copy this repo to C:\legends_of_minds
cd C:\legends_of_minds

# One command deployment
.\deploy-legends.ps1
```

That's it. The script handles:
- ✅ Storage setup on your F: drive
- ✅ Ollama data migration (if needed)
- ✅ Docker container deployment
- ✅ Service health verification

### 3. Verify

```powershell
# Run comprehensive safety checks
.\verify-legends.ps1
```

Expected output:
```
✓ Ollama running (PID: 1234)
✓ All connections localhost-only
✓ Models accessible
✓ Model configuration intact
✓ All canary tests passed
✓ Full safety report: VERIFIED

Checks Passed: 12/12 (100%)
```

## Access Your System

Open your browser:

- **Main Dashboard**: http://localhost:8080
  - Real-time safety monitoring
  - Model interaction
  - File uploads
  - Resource monitoring

- **API Documentation**: http://localhost:8080/docs
  - Interactive API explorer
  - All endpoints documented

- **File Ingest API**: http://localhost:8001/docs
  - Upload documents
  - Manage your knowledge base

- **Vector Database**: http://localhost:6334
  - Qdrant admin interface
  - Vector storage management

## Key Features

### 🛡️ Safety Monitoring (100+ Checks)

1. **Model Integrity** - Verify no tampering
2. **Process Isolation** - Confirm sandboxing
3. **Network Isolation** - Ensure localhost-only
4. **Canary Tests** - Detect jailbreaks
5. **Resource Monitoring** - Track GPU/CPU/RAM
6. **Configuration Transparency** - See everything

### 📊 Real-Time Dashboard

- One-click safety verification
- System health monitoring
- Model interaction testing
- File ingestion management
- Resource usage tracking

### 🔒 Security First

- All services localhost-bound
- No external API calls
- Model files read-only
- Process isolation verified
- Network traffic monitored

## Common Tasks

### Upload Documents

```bash
# Via API
curl -X POST http://localhost:8001/api/upload \
  -F "file=@/path/to/document.pdf" \
  -F "collection=my_notes"

# Or use the web interface at http://localhost:8080
```

### Query Your Model

```bash
# Via API
curl -X POST http://localhost:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "omegaheir_zero", "prompt": "Explain quantum computing"}'

# Or use the web interface
```

### Run Safety Check

```bash
# Full report
curl http://localhost:8080/api/safety/full_report

# Specific check
curl http://localhost:8080/api/safety/model_integrity
curl http://localhost:8080/api/safety/canary_test
```

### View Logs

```powershell
# All services
docker compose -f docker-compose.legends.yml logs -f

# Specific service
docker compose -f docker-compose.legends.yml logs -f legends-control-center
```

### Stop/Start Services

```powershell
# Stop
docker compose -f docker-compose.legends.yml down

# Start
docker compose -f docker-compose.legends.yml up -d

# Restart
docker compose -f docker-compose.legends.yml restart
```

## Troubleshooting

### Services Won't Start

```powershell
# Check Docker is running
docker ps

# Check port availability
netstat -ano | findstr "8080 8001 6333 11434"

# View detailed logs
docker compose -f docker-compose.legends.yml logs
```

### Ollama Not Responding

```powershell
# Check Ollama container
docker compose -f docker-compose.legends.yml ps ollama

# Restart Ollama
docker compose -f docker-compose.legends.yml restart ollama

# Check GPU access (if using NVIDIA)
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

### Safety Checks Failing

```powershell
# Run detailed verification
.\verify-legends.ps1

# Check specific endpoint
curl http://localhost:8080/api/safety/full_report | jq

# View dashboard
start http://localhost:8080
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Windows Machine                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Ollama     │  │   Qdrant     │  │   Control    │     │
│  │   (GPU)      │  │  (Vectors)   │  │   Center     │     │
│  │  :11434      │  │  :6333,6334  │  │   :8080      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                 │                   │             │
│         └─────────────────┴───────────────────┘             │
│                    Docker Network                           │
│                    (localhost only)                         │
│                                                              │
│  Storage (F: drive):                                        │
│    ├── OllamaData/models/  (LLM weights)                   │
│    ├── qdrant_storage/     (Vector DB)                     │
│    └── uploads/            (Your documents)                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Testing

```powershell
# Install test dependencies
pip install pytest fastapi httpx psutil

# Run all tests
pytest tests/test_safety_monitor.py -v

# Expected: 15 tests passed
```

## What's Different?

### This is NOT:

- ❌ A cloud service with usage limits
- ❌ A mystery box you can't inspect
- ❌ A system with hidden API calls
- ❌ A platform collecting your data
- ❌ Software you can't verify

### This IS:

- ✅ 100% local execution
- ✅ Full source code transparency
- ✅ Comprehensive safety verification
- ✅ No external dependencies
- ✅ Your data stays on your hardware
- ✅ Open, auditable, verifiable

## Next Steps

1. **Feed it your notes**: Upload 100 documents via the ingest service
2. **Test the safety**: Run canary tests regularly
3. **Monitor resources**: Watch GPU/CPU usage
4. **Verify everything**: Check the dashboard often
5. **Build confidence**: See it work, transparently

## Getting Help

1. Check logs: `docker compose -f docker-compose.legends.yml logs`
2. Run verification: `.\verify-legends.ps1`
3. Review dashboard: http://localhost:8080
4. Check documentation: See LEGENDS_OF_MINDS.md for details

## Philosophy

**Engineering, not mysticism.**

Every component is:
- Inspectable
- Verifiable
- Transparent
- Documented
- Testable

You own this. You control this. You can trust this because you can **verify** this.

---

**Now go build something real. 😄**
