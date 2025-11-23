# Quick Start: Patent Office & Google Scholar Integration

Get up and running with patent filing and academic paper tracking in 5 minutes.

## 🚀 Prerequisites

- Docker and Docker Compose installed
- Discord bot token
- (Optional) API keys for USPTO, EPO, SerpAPI

## ⚡ Quick Setup

### 1. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your values (minimum required)
nano .env
```

**Minimum Configuration:**
```bash
DISCORD_TOKEN=your_bot_token_here
CH_PATENT_RESEARCH_ID=your_channel_id
CH_RESEARCH_FEED_ID=your_channel_id
POSTGRES_PASSWORD=secure_password
```

### 2. Start Services

```bash
# Make script executable
chmod +x run-patent-scholar.sh

# Start all services
./run-patent-scholar.sh up
```

Wait 30-60 seconds for services to initialize.

### 3. Verify

```bash
# Check service health
./run-patent-scholar.sh health
```

You should see ✓ for all services:
- Patent Search API
- RAG Query API
- Nginx Proxy
- Elasticsearch
- Qdrant
- PostgreSQL

## 🎯 Quick Tasks

### Search for Prior Art

```bash
# Connect to patent search service
docker-compose -f docker-compose.patent-scholar.yml exec patent-search-api bash

# Run search
python -m src.patent.search --keywords "sovereignty architecture"
```

### Discover Papers

```bash
# Connect to scholar scraper
docker-compose -f docker-compose.patent-scholar.yml exec scholar-scraper bash

# Run discovery
python -m src.scholar.discover --keywords "AI governance"
```

### Query RAG System

```bash
# Query patents and papers
curl -X POST http://localhost:8087/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the latest approaches to AI governance?",
    "collection": "scholar_papers_v1",
    "top_k": 5
  }'
```

## 📊 Access Services

| Service | URL | Description |
|---------|-----|-------------|
| Patent Search API | http://localhost:8086 | Patent prior art search |
| RAG Query API | http://localhost:8087 | Semantic search |
| Nginx Gateway | http://localhost:8088 | Unified API gateway |
| Elasticsearch | http://localhost:9200 | Full-text search |
| Qdrant Dashboard | http://localhost:6334 | Vector database |
| PostgreSQL | localhost:5433 | Structured data |

## 🔍 Common Commands

```bash
# View service logs
./run-patent-scholar.sh logs

# Check service status
./run-patent-scholar.sh status

# Backup database
./run-patent-scholar.sh backup

# Stop all services
./run-patent-scholar.sh down

# Restart services
./run-patent-scholar.sh restart
```

## 🔔 Discord Integration

Once services are running, GitHub Actions will automatically:

1. **Weekly Patent Monitoring** (Mondays 04:00 UTC)
   - Search USPTO, EPO, WIPO for prior art
   - Monitor competitor filings
   - Post results to `#patent-research`

2. **Daily Scholar Monitoring** (02:00 UTC)
   - Discover new papers in AI governance
   - Track citations
   - Post results to `#research-feed`

### Manual Notifications via GitLens

```bash
# Send custom notification
./gl2discord.sh $CH_PATENT_RESEARCH_ID \
  "Patent Search Complete" \
  "Found 5 relevant patents" \
  "0x0099ff"
```

## 🔐 Cryptographic Verification

All patent documents are automatically verified:

```bash
# Generate SHA256 hash
sha256sum document.pdf

# GPG sign
gpg --armor --detach-sign document.pdf

# Create OpenTimestamps proof
ots stamp document.pdf

# Verify (after Bitcoin confirmation)
ots verify document.pdf.ots
```

**Sovereign Manifest Hash:**
```
FAA198DA05318742531B6405384319563933F63DB4D91866E70AE7701FCDCDED
```

## 📝 Database Access

```bash
# Connect to PostgreSQL
docker exec -it patent-postgres psql -U postgres -d patent_db

# Check tables
\dt

# Query patents
SELECT title, status FROM patents LIMIT 10;

# Query papers
SELECT title, citation_count FROM scholar_papers ORDER BY citation_count DESC LIMIT 10;
```

## 🧪 Testing

```bash
# Run system tests
./run-patent-scholar.sh test

# Test patent search
curl http://localhost:8086/health

# Test RAG query
curl http://localhost:8087/health

# Check Elasticsearch
curl http://localhost:9200/_cluster/health
```

## 🐛 Troubleshooting

### Services won't start

```bash
# Check Docker
docker --version
docker-compose --version

# Check .env file
cat .env

# View detailed logs
docker-compose -f docker-compose.patent-scholar.yml logs
```

### API not responding

```bash
# Check service status
./run-patent-scholar.sh status

# Restart specific service
docker-compose -f docker-compose.patent-scholar.yml restart patent-search-api

# Check health
./run-patent-scholar.sh health
```

### Database connection issues

```bash
# Check PostgreSQL
docker exec patent-postgres pg_isready -U postgres

# Restart database
docker-compose -f docker-compose.patent-scholar.yml restart patent-postgres
```

## 📚 Next Steps

1. **Configure API Keys** - Add USPTO, EPO, SerpAPI keys to `.env` for full functionality
2. **Customize Searches** - Edit `patent_office.yaml` and `google_scholar.yaml`
3. **Set Up Discord Channels** - Create channels and update channel IDs in `.env`
4. **Enable Monitoring** - GitHub Actions will run automatically on schedule
5. **Explore RAG** - Query the system for patents and papers

## 📖 Documentation

- **Full Documentation**: [PATENT_SCHOLAR_README.md](PATENT_SCHOLAR_README.md)
- **GitLens Integration**: [GITLENS_INTEGRATION.md](GITLENS_INTEGRATION.md)
- **Docker Compose**: [docker-compose.patent-scholar.yml](docker-compose.patent-scholar.yml)
- **Workflows**: [.github/workflows/patent-scholar-monitor.yml](.github/workflows/patent-scholar-monitor.yml)

## 🎯 Success Indicators

You're ready when:
- ✓ All services show healthy status
- ✓ Database tables are created
- ✓ APIs respond to health checks
- ✓ Discord notifications work
- ✓ RAG queries return results

## 🆘 Support

- **Issues**: Open a GitHub issue
- **Discord**: Join `#patent-research` or `#research-feed`
- **Documentation**: See [PATENT_SCHOLAR_README.md](PATENT_SCHOLAR_README.md)

---

**Sovereign Manifest**: `FAA198DA05318742531B6405384319563933F63DB4D91866E70AE7701FCDCDED`

**Status**: Empire eternal 🎯
