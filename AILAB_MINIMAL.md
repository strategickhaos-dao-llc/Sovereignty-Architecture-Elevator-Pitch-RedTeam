# Minimal AI Lab - Safe, Local-First RAG System

A lightweight, production-safe AI lab with 3 core services for local RAG experimentation.

## 🎯 Overview

This is a **minimal, safe, local-first** alternative to the comprehensive 54-service AI lab. It focuses on core RAG functionality without aggressive model configurations.

**Services:**
- **Memory Service** (port 8001) - ChromaDB-backed vector storage with sentence embeddings
- **RAG API** (port 8000) - Query interface that retrieves context and forwards to LLM
- **IPFS** (ports 5001, 8080) - Optional distributed storage for persistence

## ✅ Safety & Compliance

- **No uncensored models** - Uses standard, responsible LLM endpoints
- **Configurable LLM backend** - Works with OpenAI, Azure, Ollama, or dev mode
- **Local-first** - All data stored locally, no external dependencies required
- **Production-ready** - Suitable for responsible AI research and development

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 4GB+ RAM
- 10GB disk space

### Setup

1. **Configure environment:**
```bash
cp .env.ailab.minimal.example .env
nano .env  # Set LLM_API_URL and LLM_API_KEY (or leave blank for dev mode)
```

2. **Start services:**
```bash
docker-compose -f docker-compose.ailab.yml up --build -d
```

3. **Verify services:**
```bash
# Check status
docker-compose -f docker-compose.ailab.yml ps

# View logs
docker-compose -f docker-compose.ailab.yml logs -f
```

## 📝 Usage Examples

### Store Knowledge

```bash
# Store a fact in memory
curl -X POST http://localhost:8001/store \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The harvest was completed on November 15, 2024",
    "metadata": {"source": "farm_report"},
    "tags": ["agriculture", "2024"]
  }'
```

### Query with RAG

```bash
# Ask a question (retrieves from memory + LLM response)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "When was the harvest completed?",
    "k": 3
  }'
```

### Memory Search

```bash
# Direct vector similarity search
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "harvest information",
    "k": 5
  }'
```

## 🔧 Configuration

### LLM Backend Options

#### Dev Mode (No LLM)
Leave `LLM_API_URL` blank. RAG API will echo responses for testing.

```bash
LLM_API_URL=
LLM_API_KEY=
```

#### OpenAI
```bash
LLM_API_URL=https://api.openai.com/v1/chat/completions
LLM_API_KEY=sk-your-openai-key
LLM_API_TYPE=openai
```

#### Azure OpenAI
```bash
LLM_API_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2023-05-15
LLM_API_KEY=your-azure-key
LLM_API_TYPE=azure
```

#### Local Ollama
```bash
# Start Ollama first: ollama serve
LLM_API_URL=http://host.docker.internal:11434/api/chat
LLM_API_KEY=
LLM_API_TYPE=ollama
```

## 📊 Architecture

```
┌──────────────┐
│  RAG API     │
│  :8000       │
└──────┬───────┘
       │
       ├─────────┐
       ↓         ↓
┌──────────┐  ┌─────────────┐
│ Memory   │  │ LLM Endpoint│
│ :8001    │  │ (external)  │
└──────────┘  └─────────────┘
       ↓
┌──────────────┐
│ ChromaDB     │
│ (persistent) │
└──────────────┘

┌──────────────┐
│ IPFS         │
│ :5001, :8080 │
│ (optional)   │
└──────────────┘
```

## 🔐 Security Best Practices

1. **Environment Variables:**
   - Never commit `.env` file
   - Keep API keys secret
   - Rotate credentials regularly

2. **Network Exposure:**
   - Services bind to localhost by default
   - Use reverse proxy (Caddy/Nginx) for public access
   - Enable TLS/SSL for production
   - Implement authentication (API keys, OAuth)

3. **Rate Limiting:**
   - Add rate limits to public-facing services
   - Monitor API usage
   - Set cost limits for LLM APIs

4. **Data Protection:**
   - ChromaDB persists to `./data/chroma`
   - Backup regularly
   - Consider encryption at rest

## 🛠️ Maintenance

### Stop Services
```bash
docker-compose -f docker-compose.ailab.yml down
```

### View Logs
```bash
docker-compose -f docker-compose.ailab.yml logs -f memory
docker-compose -f docker-compose.ailab.yml logs -f rag
```

### Clear Data (CAUTION!)
```bash
# Removes all stored memories
docker-compose -f docker-compose.ailab.yml down -v
rm -rf ./data/chroma/*
```

### Update Services
```bash
docker-compose -f docker-compose.ailab.yml pull
docker-compose -f docker-compose.ailab.yml up --build -d
```

## 📈 Scaling & Extensions

### Add Traefik Reverse Proxy

Create `docker-compose.ailab-proxy.yml`:

```yaml
version: "3.8"
services:
  traefik:
    image: traefik:v2.10
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports:
      - "80:80"
      - "443:443"
      - "8090:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    labels:
      - "traefik.enable=true"
```

Deploy with:
```bash
docker-compose -f docker-compose.ailab.yml -f docker-compose.ailab-proxy.yml up -d
```

### Add Authentication

Use HTTP Basic Auth via Traefik labels or implement API key middleware in services.

### Add More Storage

- PostgreSQL for structured metadata
- MinIO for object storage
- Elasticsearch for full-text search

## 🎓 Use Cases

✅ **Responsible AI Research:**
- RAG experimentation
- Context retrieval testing
- Embedding model comparison

✅ **Knowledge Management:**
- Document search
- Q&A systems
- Information retrieval

✅ **Development & Testing:**
- RAG pipeline prototyping
- Integration testing
- Local LLM evaluation

## 🚫 What This Is NOT

❌ Not for deploying uncensored or refusal-free models  
❌ Not for bypassing safety mechanisms  
❌ Not for adversarial prompt testing without authorization  
❌ Not for production without proper security hardening

## 📚 API Reference

### Memory Service (`/store`)
```json
POST http://localhost:8001/store
{
  "id": "optional-custom-id",
  "text": "content to store",
  "metadata": {"key": "value"},
  "tags": ["tag1", "tag2"]
}
```

### Memory Service (`/query`)
```json
POST http://localhost:8001/query
{
  "query": "search query",
  "k": 4
}
```

### RAG API (`/ask`)
```json
POST http://localhost:8000/ask
{
  "prompt": "your question",
  "k": 4
}
```

## 🤝 Integration with Main Lab

This minimal lab can run **alongside** the comprehensive 54-service lab:

- Different port ranges (8000-8001 vs 8080+)
- Separate networks
- Independent data volumes
- Can share LLM endpoints

Use for:
- Testing before full deployment
- Development environments
- Resource-constrained setups
- Production-safe operations

## 📝 License & Compliance

- Respects LLM vendor terms of service
- No safety mechanism bypass
- Suitable for responsible AI development
- MIT License (respecting upstream dependencies)

## 🆘 Troubleshooting

**Services won't start:**
```bash
docker-compose -f docker-compose.ailab.yml logs
```

**Out of memory:**
Reduce services or increase Docker memory limit.

**LLM API errors:**
Check API key, URL, and rate limits. Use dev mode to test without LLM.

**ChromaDB corruption:**
Backup and clear: `rm -rf ./data/chroma/*`

## 🔗 Related Documentation

- [Comprehensive AI Lab](AI_LAB_GUIDE.md) - Full 54-service deployment
- [Architecture](ARCHITECTURE.md) - System design details
- [Setup Guide](SETUP.md) - Prerequisites and installation

---

**A safe, minimal, local-first AI lab for responsible RAG development. 🧠✨**
