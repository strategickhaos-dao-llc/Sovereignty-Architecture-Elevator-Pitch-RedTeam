# Legends of Minds - Control Center

## Overview

The Control Center is the main FastAPI application that provides:
- Central API gateway for the Legends of Minds system
- Comprehensive safety monitoring with 100+ verification checks
- Health checking for all services
- Model interaction proxy
- Real-time transparency reporting

## Files

- `main.py` - Main FastAPI application with core endpoints
- `safety_monitor.py` - Safety monitoring router with verification endpoints

## Endpoints

### Core Endpoints

- `GET /` - System information
- `GET /health` - Health check for all services
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

### Safety Monitoring (`/api/safety/`)

- `GET /model_integrity` - Verify model file integrity (SHA256 hashing)
- `GET /process_isolation` - Check Ollama process isolation
- `GET /network_isolation` - Verify no unexpected network activity
- `GET /model_config` - Show model configuration transparency
- `GET /canary_test` - Run behavioral safety tests
- `GET /resource_usage` - Monitor CPU/GPU/RAM usage
- `GET /full_report` - Comprehensive safety report

### Model Interaction

- `POST /api/generate` - Generate text using Ollama (proxied)
- `GET /api/models` - List available models

## Dependencies

```
fastapi
uvicorn[standard]
httpx
psutil
```

## Running Locally

```bash
cd core
pip install fastapi uvicorn httpx psutil
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## Testing

```bash
pytest ../tests/test_safety_monitor.py -v
```

## Architecture

The Control Center acts as:
1. **Gateway** - Routes requests to appropriate services
2. **Monitor** - Continuously verifies system safety
3. **Proxy** - Provides unified access to Ollama and Qdrant
4. **Reporter** - Generates transparency reports

All operations are localhost-bound with no external API calls.
