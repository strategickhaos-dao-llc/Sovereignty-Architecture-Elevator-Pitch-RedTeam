# 🚀 Forensics Quick Start Guide

**Get started with the DOM_010101 Forensics Suite in 5 minutes**

---

## Prerequisites

- Docker and Docker Compose installed
- At least 16GB RAM (32GB recommended)
- NVIDIA GPU (optional but recommended for AI features)
- 100GB+ free disk space for evidence storage

---

## 1. Configuration

Copy the example environment file and customize it:

```bash
cp .env.forensics.example .env.forensics
```

Edit `.env.forensics` and set at minimum:

```bash
# Required: Database password
FORENSICS_DB_PASSWORD=your_secure_password

# Optional: API keys for OSINT features
MALTEGO_API_KEY=your_maltego_key
SHODAN_API_KEY=your_shodan_key

# Optional: Discord integration
DISCORD_FORENSICS_WEBHOOK=https://discord.com/api/webhooks/...

# Optional: Video generation (if enabled)
YOUTUBE_CHANNEL_ID=your_channel_id
AUTO_UPLOAD=false
```

---

## 2. Deploy the Forensics Stack

Start all forensics services:

```bash
docker compose -f docker-compose-forensics.yml up -d
```

This will start:
- Forensics Database (PostgreSQL)
- Phone Imaging Service
- Encryption Cracking Service (with GPU support)
- Memory Forensics Service
- OSINT Platform
- Chain of Custody Blockchain
- AI Analysis Services
- Forensics API Gateway
- And more...

---

## 3. Verify Services

Check that all services are running:

```bash
docker compose -f docker-compose-forensics.yml ps
```

You should see all services in "Up" state.

---

## 4. Access Services

### Forensics API
```bash
curl http://localhost:8090/health
```

### OSINT Platform (SpiderFoot)
Open browser: http://localhost:5001

### Forensics Dashboard
Open browser: http://localhost:3001
- Username: admin
- Password: (from GRAFANA_PASSWORD in .env.forensics)

---

## 5. Your First Forensics Case

### Create a case via API:

```bash
curl -X POST http://localhost:8090/api/cases \
  -H "Content-Type: application/json" \
  -d '{
    "case_number": "CASE-2025-001",
    "title": "Test Investigation",
    "description": "Initial forensics test",
    "case_type": "research",
    "lead_investigator": "Your Name"
  }'
```

### Add evidence:

```bash
curl -X POST http://localhost:8090/api/evidence \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "<case-id-from-previous-response>",
    "evidence_number": "EVID-001",
    "description": "Test evidence item",
    "evidence_type": "document",
    "collected_by": "Your Name"
  }'
```

---

## 6. Run Forensics Analysis

### Memory Dump Analysis:

```bash
# Copy your memory dump to the evidence volume
docker cp memdump.raw forensics-memory:/evidence/

# Run Volatility analysis
docker exec forensics-memory vol -f /evidence/memdump.raw windows.pslist
```

### Disk Encryption Cracking:

```bash
# Copy hash file
docker cp hashes.txt forensics-cracking:/evidence/

# Run Hashcat
docker exec forensics-cracking hashcat -m 1800 -a 3 /evidence/hashes.txt ?a?a?a?a?a?a?a?a
```

### OSINT Investigation:

Access SpiderFoot at http://localhost:5001 and:
1. Click "New Scan"
2. Enter target (domain, IP, email, etc.)
3. Select scan modules
4. Click "Run Scan"

---

## 7. View Results

### Check Analysis Status:

```bash
curl http://localhost:8090/api/cases/<case-id>/status
```

### Generate Report:

```bash
curl -X POST http://localhost:8090/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "<case-id>",
    "report_type": "preliminary"
  }'
```

---

## 8. Discord Integration (Optional)

If you configured Discord webhook, notifications will be sent automatically for:
- New cases created
- Evidence added
- Analysis completed
- Chain of custody transfers
- Critical findings

Test the integration:

```bash
curl -X POST http://localhost:8090/api/notify \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "forensics",
    "message": "Test notification from forensics stack"
  }'
```

---

## 9. Blockchain Chain of Custody

Track evidence with immutable blockchain records:

```bash
# Submit evidence to blockchain
docker exec forensics-blockchain peer chaincode invoke \
  -C forensics-channel \
  -n evidence-chaincode \
  -c '{"Args":["submitEvidence","EVID-001","sha256hash","Investigator Name"]}'

# Query evidence chain
docker exec forensics-blockchain peer chaincode query \
  -C forensics-channel \
  -n evidence-chaincode \
  -c '{"Args":["queryEvidence","EVID-001"]}'
```

---

## 10. Stop Services

When you're done:

```bash
# Stop all services
docker compose -f docker-compose-forensics.yml down

# Stop and remove volumes (WARNING: deletes all data)
docker compose -f docker-compose-forensics.yml down -v
```

---

## Common Issues

### GPU Not Detected

If GPU features aren't working:

```bash
# Check NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# If this fails, install nvidia-container-toolkit
```

### Services Won't Start

```bash
# Check logs
docker compose -f docker-compose-forensics.yml logs <service-name>

# Example: check forensics API logs
docker compose -f docker-compose-forensics.yml logs forensics-api
```

### Out of Disk Space

Forensics work generates a lot of data. Clean up old evidence:

```bash
# Remove old evidence (adjust path as needed)
docker exec forensics-api rm -rf /evidence/old-cases/

# Clean Docker images
docker system prune -a
```

---

## Next Steps

1. **Read the full documentation**:
   - [DOM_010101_FORENSICS.md](DOM_010101_FORENSICS.md) - Complete toolchain guide
   - [VIDEO_CONTENT_LIBRARY.md](VIDEO_CONTENT_LIBRARY.md) - Training videos
   - [NEXT_100_IDEAS.md](NEXT_100_IDEAS.md) - Future roadmap

2. **Watch training videos**:
   - YouTube: youtube.com/@DOM_010101_Eternal
   - 100+ educational videos on forensics techniques

3. **Join the community**:
   - Discord: #forensics channel
   - Share your findings and learn from others

4. **Contribute**:
   - Add new forensics tools
   - Improve documentation
   - Share case studies
   - Submit bug reports

---

## Security Notice

⚠️ **IMPORTANT**: This forensics suite contains powerful tools that must be used responsibly:

- Only use on systems you own or have explicit written authorization to test
- Follow all applicable laws and regulations
- Maintain proper chain of custody for evidence
- Never commit actual case data to version control
- Encrypt sensitive evidence at rest and in transit
- Follow your organization's security policies

**Unauthorized access to computer systems is illegal.**

---

## Support

Need help?

- **Documentation**: See [DOM_010101_FORENSICS.md](DOM_010101_FORENSICS.md)
- **Discord**: #forensics channel
- **Email**: forensics@strategickhaos.com
- **Issues**: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*DOM_010101 - The legion is growing. The mysteries are falling.*
