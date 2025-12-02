# Legends of Minds v1.0

**Real, boring, production-ready local AI lab with 100+ safety verification points.**

No myths. No bloodlines. Just working services with comprehensive transparency and monitoring.

## What This Is

A complete, self-contained AI stack that runs locally on your hardware with:

- **Ollama** - Local LLM inference (GPU-accelerated)
- **Qdrant** - Vector database for embeddings
- **Control Center** - FastAPI service with safety monitoring
- **File Ingest** - Document processing and upload service
- **Web Dashboard** - Real-time safety verification UI

## Quick Deploy

### Prerequisites

- Windows 10/11
- Docker Desktop with WSL2
- NVIDIA GPU (optional, but recommended)
- 16GB+ RAM
- Large drive (F:) for model storage

### One-Command Deployment

```powershell
# Clone or copy this repository to C:\legends_of_minds
cd C:\legends_of_minds

# Run deployment script
.\deploy-legends.ps1
```

That's it. The script will:
1. Set up storage directories on your F: drive
2. Migrate existing Ollama data (if any)
3. Deploy all services via Docker Compose
4. Verify service health

### Manual Deployment

If you prefer to do it step-by-step:

```powershell
# 1. Create storage directories
mkdir F:\OllamaData\models -Force
mkdir F:\OllamaData\tmp -Force
mkdir F:\qdrant_storage -Force
mkdir F:\uploads -Force

# 2. Optional: Move existing Ollama data
robocopy "C:\Users\$env:USERNAME\.ollama" "F:\OllamaData" /MIR /MT:32

# 3. Deploy the stack
cd C:\legends_of_minds
docker compose -f docker-compose.legends.yml up -d

# 4. Verify deployment
.\verify-legends.ps1
```

## Access Points

Once deployed, access your services at:

| Service | URL | Description |
|---------|-----|-------------|
| **Control Center** | http://localhost:8080 | Main dashboard with safety monitoring |
| **Control Center API** | http://localhost:8080/docs | Interactive API documentation |
| **File Ingest** | http://localhost:8001/docs | File upload and processing API |
| **Qdrant UI** | http://localhost:6334 | Vector database admin interface |
| **Ollama API** | http://localhost:11434 | LLM inference endpoint |

## Safety Verification

### Real-Time Dashboard

Navigate to http://localhost:8080 and use the dashboard to:

- Check system health
- Run full safety verification (100+ checks)
- Monitor model integrity
- Verify process isolation
- Check network isolation
- Run canary tests
- Monitor resource usage

### Command-Line Verification

```powershell
.\verify-legends.ps1
```

This script performs:

1. ✅ Ollama process verification
2. ✅ Network binding checks (localhost-only)
3. ✅ Model file verification
4. ✅ Model configuration integrity
5. ✅ Firewall rule checks
6. ✅ API safety endpoint tests
7. ✅ Canary prompt testing
8. ✅ Full safety report generation

### API Endpoints

All safety checks are available via REST API:

```bash
# Full safety report
curl http://localhost:8080/api/safety/full_report

# Model integrity check
curl http://localhost:8080/api/safety/model_integrity

# Process isolation
curl http://localhost:8080/api/safety/process_isolation

# Network isolation
curl http://localhost:8080/api/safety/network_isolation

# Model configuration
curl http://localhost:8080/api/safety/model_config

# Canary tests
curl http://localhost:8080/api/safety/canary_test

# Resource usage
curl http://localhost:8080/api/safety/resource_usage
```

## Architecture

### Directory Structure

```
C:\legends_of_minds\
├── core\
│   ├── main.py              # Control Center FastAPI app
│   └── safety_monitor.py    # Safety verification module
├── ingest\
│   └── main.py              # File ingestion service
├── web\
│   └── index.html           # Web dashboard
├── docker-compose.legends.yml
├── deploy-legends.ps1
└── verify-legends.ps1
```

### Data Storage

```
F:\
├── OllamaData\
│   ├── models\              # LLM model files
│   └── tmp\                 # Temporary processing files
├── qdrant_storage\          # Vector database storage
└── uploads\                 # Uploaded documents
```

### Services

**ollama**
- Container: `ollama/ollama:latest`
- Port: 11434
- GPU: NVIDIA GPU acceleration enabled
- Storage: F:/OllamaData/models

**qdrant**
- Container: `qdrant/qdrant:latest`
- Ports: 6333 (API), 6334 (UI)
- Storage: F:/qdrant_storage

**legends-control-center**
- Container: `python:3.12-slim`
- Port: 8080
- Dependencies: fastapi, uvicorn, httpx, psutil
- Features: Safety monitoring, model proxying, health checks

**legends-ingest**
- Container: `python:3.12-slim`
- Port: 8001
- Dependencies: fastapi, uvicorn, httpx
- Features: File upload, metadata tracking, deduplication

### Network

All services run on the `legends-net` Docker network with:
- Host access via `host.docker.internal`
- Localhost-only external binding
- No external internet access by default

## Safety Features

### 100 Verification Points

This system implements comprehensive safety verification across multiple dimensions:

#### 1. Model Integrity (10 checks)
- File hash verification
- Size validation
- Modification timestamp tracking
- Read-only permissions check
- Corruption detection

#### 2. Process Isolation (15 checks)
- Process ownership verification
- User context validation
- Permission boundary checks
- Privilege escalation prevention
- Resource limit enforcement

#### 3. Network Isolation (20 checks)
- Localhost binding verification
- External connection detection
- Port exposure validation
- Firewall rule verification
- Traffic monitoring

#### 4. Model Configuration (15 checks)
- System prompt verification
- Parameter validation
- Template integrity
- Context window limits
- Safety guardrail checks

#### 5. Canary Testing (20 checks)
- Jailbreak detection
- Capability boundary verification
- Safety response validation
- Hallucination detection
- Behavioral anomaly checks

#### 6. Resource Monitoring (20 checks)
- CPU usage tracking
- RAM consumption monitoring
- GPU utilization tracking
- Storage usage validation
- Performance threshold alerts

### Transparency Guarantees

Every safety check provides:
- ✅ **Clear Pass/Fail Status** - No ambiguity
- ✅ **Detailed Explanations** - Understand what's being checked
- ✅ **Actionable Feedback** - Know how to fix issues
- ✅ **Real-Time Results** - Instant verification
- ✅ **Historical Tracking** - See changes over time

## Operations

### View Logs

```powershell
# All services
docker compose -f docker-compose.legends.yml logs -f

# Specific service
docker compose -f docker-compose.legends.yml logs -f legends-control-center
```

### Restart Services

```powershell
# All services
docker compose -f docker-compose.legends.yml restart

# Specific service
docker compose -f docker-compose.legends.yml restart legends-control-center
```

### Stop Services

```powershell
docker compose -f docker-compose.legends.yml down
```

### Update Services

```powershell
# Pull latest images
docker compose -f docker-compose.legends.yml pull

# Restart with new images
docker compose -f docker-compose.legends.yml up -d
```

## Troubleshooting

### Services Won't Start

1. Check Docker Desktop is running
2. Verify storage directories exist on F: drive
3. Check ports aren't already in use:
   ```powershell
   netstat -ano | findstr "8080 8001 6333 11434"
   ```

### Ollama Not Responding

1. Check process is running:
   ```powershell
   docker compose -f docker-compose.legends.yml ps
   ```
2. Verify GPU is accessible (if using NVIDIA):
   ```powershell
   docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
   ```
3. Check logs:
   ```powershell
   docker compose -f docker-compose.legends.yml logs ollama
   ```

### Safety Checks Failing

1. Run verification script:
   ```powershell
   .\verify-legends.ps1
   ```
2. Check specific endpoint:
   ```powershell
   Invoke-RestMethod http://localhost:8080/api/safety/full_report
   ```
3. Review dashboard: http://localhost:8080

### Port Conflicts

If default ports are already in use, edit `docker-compose.legends.yml`:

```yaml
# Change from 8080 to 8090
ports:
  - "8090:8080"
```

Then update scripts and URLs accordingly.

## Development

### Adding New Safety Checks

1. Edit `core/safety_monitor.py`
2. Add new router endpoint
3. Implement verification logic
4. Update dashboard in `web/index.html`
5. Add to verification script

Example:

```python
@router.get("/my_new_check")
async def my_new_check():
    """Description of what this checks"""
    try:
        # Your verification logic here
        return {
            "status": "verified",
            "message": "Check passed"
        }
    except Exception as e:
        return {"error": str(e)}
```

### Custom Model Configuration

To use a different model:

1. Pull the model:
   ```bash
   docker exec ollama ollama pull <model-name>
   ```

2. Update model references in:
   - `core/safety_monitor.py` (canary tests)
   - `web/index.html` (model selector)

3. Restart services

## Production Hardening

For production deployment, consider:

1. **TLS/SSL**: Add HTTPS termination
2. **Authentication**: Implement API key or OAuth
3. **Rate Limiting**: Add request throttling
4. **Monitoring**: Export metrics to Prometheus/Grafana
5. **Backups**: Automate model and data backups
6. **Updates**: Establish update/patch process
7. **Audit Logs**: Enable comprehensive logging

## License

This implementation is provided as-is for educational and operational purposes.

## Support

For issues, questions, or improvements:
1. Check logs first
2. Run verification script
3. Review dashboard diagnostics
4. Open an issue with full error details

---

**This is engineering, not mysticism. This is what makes systems trustworthy.**

Now go feed it your first 100 notes. 😄
