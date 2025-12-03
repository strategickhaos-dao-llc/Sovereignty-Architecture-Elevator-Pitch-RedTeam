# Patent Office & Google Scholar Integration

This directory contains the infrastructure for patent filing, prior art search, and academic paper discovery for the Sovereignty Architecture project.

## 🎯 Overview

The Patent & Scholar system provides:

- **Patent Prior Art Search**: Automated search across USPTO, EPO, WIPO databases
- **Google Scholar Monitoring**: Daily paper discovery and citation tracking
- **Freedom to Operate Analysis**: Automated conflict detection
- **Cryptographic Verification**: GPG signing, SHA256 hashing, OpenTimestamps
- **Discord Integration**: Real-time notifications via GitLens

## 📋 Files

- `patent_office.yaml` - Patent office configuration and workflow
- `google_scholar.yaml` - Google Scholar and academic paper configuration
- `docker-compose.patent-scholar.yml` - Docker services for patent/scholar infrastructure
- `init-patent-db.sql` - PostgreSQL database initialization
- `nginx-patent-scholar.conf` - Nginx reverse proxy configuration
- `.github/workflows/patent-scholar-monitor.yml` - GitHub Actions workflow

## 🚀 Quick Start

### 1. Prerequisites

- Docker and Docker Compose
- Discord bot token
- API keys for USPTO, EPO, SerpAPI (optional but recommended)
- OpenAI API key for AI-powered features

### 2. Configuration

Copy and configure environment variables:

```bash
cp .env.example .env
# Edit .env with your values
```

Required environment variables:

```bash
# Discord
DISCORD_TOKEN=your_bot_token
CH_PATENT_RESEARCH_ID=channel_id
CH_PATENT_STATUS_ID=channel_id
CH_RESEARCH_FEED_ID=channel_id
CH_RESEARCH_CITATIONS_ID=channel_id

# APIs
USPTO_API_KEY=your_key
EPO_API_KEY=your_key
SERPAPI_KEY=your_key
OPENAI_API_KEY=your_key

# Database
POSTGRES_PASSWORD=secure_password

# GPG
GPG_KEY_ID=0x137SOVEREIGN
```

### 3. Launch Services

#### Option A: Using Helper Script (Recommended)

```bash
# Make script executable (first time only)
chmod +x run-patent-scholar.sh

# Start all services
./run-patent-scholar.sh up

# Check service health
./run-patent-scholar.sh health

# View logs
./run-patent-scholar.sh logs

# See all available commands
./run-patent-scholar.sh help
```

#### Option B: Using Docker Compose Directly

```bash
# Start all patent & scholar services
docker-compose -f docker-compose.patent-scholar.yml up -d

# Check service health
docker-compose -f docker-compose.patent-scholar.yml ps

# View logs
docker-compose -f docker-compose.patent-scholar.yml logs -f
```

### 4. Verify Installation

```bash
# Check API endpoints
curl http://localhost:8086/health  # Patent Search API
curl http://localhost:8087/health  # RAG Query API
curl http://localhost:8088/health  # Nginx proxy

# Check database
docker exec -it patent-postgres psql -U postgres -d patent_db -c "SELECT COUNT(*) FROM patents;"
```

## 📊 Services

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| patent-search-api | 8086 | Patent prior art search API |
| rag-query-api | 8087 | RAG query API for patents/papers |
| patent-scholar-nginx | 8088/8089 | HTTP/HTTPS reverse proxy |
| patent-postgres | 5433 | PostgreSQL database |
| elasticsearch | 9200 | Full-text search engine |
| qdrant | 6334 | Vector database for embeddings |

### Processing Services

| Service | Description |
|---------|-------------|
| patent-processor | PDF ingestion and embedding generation |
| scholar-scraper | Google Scholar paper discovery |
| scholar-processor | Paper PDF processing and indexing |
| citation-tracker | Citation monitoring and alerts |
| timestamp-service | OpenTimestamps cryptographic proofs |

### Monitoring & Notifications

| Service | Description |
|---------|-------------|
| patent-scholar-notifier | Discord notifications |
| healthcheck-aggregator | Service health monitoring |

## 🔍 Patent Workflow

### 1. Prior Art Search

```bash
# Trigger manual patent search
docker-compose -f docker-compose.patent-scholar.yml exec patent-search-api python -m src.patent.search \
  --keywords "sovereignty architecture" \
  --offices "USPTO,EPO,WIPO"
```

### 2. Novelty Assessment

```bash
# Run AI-powered novelty assessment
docker-compose -f docker-compose.patent-scholar.yml exec patent-processor python -m src.patent.novelty \
  --application-id "US12345678"
```

### 3. Document Timestamping

```bash
# Generate OpenTimestamps proof for patent document
docker-compose -f docker-compose.patent-scholar.yml exec timestamp-service python -m src.patent.timestamp \
  --file "/var/patent/documents/patent_draft.pdf"
```

## 📚 Google Scholar Workflow

### 1. Paper Discovery

```bash
# Discover new papers in AI governance
docker-compose -f docker-compose.patent-scholar.yml exec scholar-scraper python -m src.scholar.discover \
  --keywords "AI governance" \
  --date-range "last_week"
```

### 2. Citation Tracking

```bash
# Track citations for specific paper
docker-compose -f docker-compose.patent-scholar.yml exec citation-tracker python -m src.scholar.citations \
  --paper-id "arxiv:2401.12345"
```

### 3. RAG Queries

```bash
# Query papers using RAG
curl -X POST http://localhost:8087/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest approaches to AI alignment?", "collection": "scholar_papers_v1"}'
```

## 🔔 Discord Notifications

The system automatically sends notifications to Discord channels:

- `#patent-research` - Prior art search results, novelty assessments
- `#patent-status` - Application status updates, monitoring alerts
- `#research-feed` - New paper discoveries, daily summaries
- `#research-citations` - Citation alerts, trending papers

### GitLens Integration

Use the provided GitLens tasks in VS Code:

```bash
# Command Palette > Tasks: Run Task
- Patent: Search Prior Art
- Patent: Check Application Status
- Scholar: Discover Papers
- Scholar: Track Citations
```

Or use the CLI script:

```bash
./gl2discord.sh $CH_PATENT_RESEARCH_ID "Patent Search Complete" "Found 5 relevant patents" "0x0099ff"
```

## 🔐 Cryptographic Verification

All patent documents are cryptographically verified:

### 1. SHA256 Hashing

```bash
# Compute hash of document
sha256sum /var/patent/documents/patent_draft.pdf
# Output: FAA198DA05318742531B6405384319563933F63DB4D91866E70AE7701FCDCDED
```

### 2. GPG Signing

```bash
# Sign document with GPG
gpg --armor --detach-sign patent_draft.pdf
```

### 3. OpenTimestamps

```bash
# Create timestamp proof
ots stamp patent_draft.pdf

# Verify timestamp (after confirmation)
ots verify patent_draft.pdf.ots
```

### 4. Sovereign Manifest Integration

The system verifies against the Sovereign Manifest:

```
Hash: FAA198DA05318742531B6405384319563933F63DB4D91866E70AE7701FCDCDED
Verification:
  - GPG-signed ✓
  - Bitcoin-timestamped ✓
  - GitHub-sealed ✓
  - Obsidian-encrypted ✓
Status: Empire eternal
```

## 📈 Monitoring & Alerts

### GitHub Actions Workflows

Automated monitoring runs:

- **Patent Monitoring**: Weekly (Mondays 04:00 UTC)
- **Scholar Monitoring**: Daily (02:00 UTC)

View workflow results:

```
Actions > Patent & Scholar Monitoring > Latest Run
Artifacts > Download Reports
```

### Manual Trigger

```bash
# Trigger via GitHub CLI
gh workflow run patent-scholar-monitor.yml -f monitor_type=both
```

## 🔧 Maintenance

### Database Backups

```bash
# Backup patent database
docker exec patent-postgres pg_dump -U postgres patent_db > patent_backup_$(date +%Y%m%d).sql

# Restore from backup
docker exec -i patent-postgres psql -U postgres patent_db < patent_backup_20251123.sql
```

### Clear Vector Database

```bash
# Delete and recreate collections
docker-compose -f docker-compose.patent-scholar.yml exec qdrant \
  curl -X DELETE http://localhost:6333/collections/patent_prior_art_v1

docker-compose -f docker-compose.patent-scholar.yml exec qdrant \
  curl -X DELETE http://localhost:6333/collections/scholar_papers_v1
```

### Update Embeddings

```bash
# Re-embed all documents
docker-compose -f docker-compose.patent-scholar.yml exec patent-processor \
  python -m src.patent.embed --reindex-all

docker-compose -f docker-compose.patent-scholar.yml exec scholar-processor \
  python -m src.scholar.embed --reindex-all
```

## 🛠 Troubleshooting

### Service Not Starting

```bash
# Check logs
docker-compose -f docker-compose.patent-scholar.yml logs patent-search-api

# Restart service
docker-compose -f docker-compose.patent-scholar.yml restart patent-search-api
```

### Database Connection Issues

```bash
# Check database health
docker-compose -f docker-compose.patent-scholar.yml exec patent-postgres pg_isready

# Test connection
docker-compose -f docker-compose.patent-scholar.yml exec patent-postgres \
  psql -U postgres -d patent_db -c "SELECT 1;"
```

### API Rate Limiting

```bash
# Check rate limit status in Redis
docker-compose -f docker-compose.patent-scholar.yml exec redis redis-cli GET rate_limit:patent_search
```

## 📚 Resources

### Patent Offices

- [USPTO](https://www.uspto.gov/) - United States Patent and Trademark Office
- [EPO](https://www.epo.org/) - European Patent Office
- [WIPO](https://www.wipo.int/) - World Intellectual Property Organization

### Academic Search

- [Google Scholar](https://scholar.google.com/)
- [arXiv](https://arxiv.org/)
- [Semantic Scholar](https://www.semanticscholar.org/)

### Documentation

- [GitLens Documentation](https://gitlens.amod.io/)
- [Discord Bot Guide](https://discord.com/developers/docs/intro)
- [OpenTimestamps](https://opentimestamps.org/)

## 🔒 Security & Compliance

### Access Control

- Patent documents: Admin, Attorney, Inventor roles only
- Scholar papers: All authenticated users
- API endpoints: Rate limited per IP

### Audit Logging

All actions are logged in `audit_log` table:

```sql
SELECT * FROM audit_log WHERE action = 'patent_search' ORDER BY created_at DESC LIMIT 10;
```

### Compliance

- **UPL-Safe**: Attorney review gates enabled
- **Data Retention**: 7 years for audit logs, indefinite for patents
- **Copyright**: Fair use and robots.txt compliance

## 📝 License

See [LICENSE](LICENSE) file for details.

## 👥 Support

- GitHub Issues: Report bugs and feature requests
- Discord: `#patent-research`, `#research-feed`
- Documentation: [GITLENS_INTEGRATION.md](GITLENS_INTEGRATION.md)

---

**Sovereign Manifest Hash**: `FAA198DA05318742531B6405384319563933F63DB4D91866E70AE7701FCDCDED`

**Status**: Empire eternal 🎯
