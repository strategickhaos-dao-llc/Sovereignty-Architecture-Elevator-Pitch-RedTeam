# Network Reconnaissance - Quick Reference Card
**Strategic Khaos Sovereignty Architecture**

---

## 🚀 Essential Commands

### Run Full Reconnaissance
```bash
./network_recon.sh
```
**Output:** Complete infrastructure report in `recon/reports/latest_network_scan/`

---

### View Latest Report
```bash
# Interactive viewer
./view_recon_report.sh

# Quick summary
./view_recon_report.sh --summary

# Full report
./view_recon_report.sh --full
```

---

### Python Service Discovery
```bash
python3 recon/network_discovery.py
```
**Output:** Service status report in `recon/reports/network_discovery_*.md`

---

## 📊 Report Sections

| Section | Content |
|---------|---------|
| Executive Summary | Infrastructure overview and key findings |
| Docker Networks | Network topology and configuration |
| Container Inventory | All containers with status and ports |
| Port Mapping | Exposed ports and bindings |
| Service Health | Health checks for all services |
| Docker Compose Stacks | Compose file analysis |
| Environment Config | Configuration summary |
| Requirements Check | Tool availability |
| Network Topology | Mermaid architecture diagram |
| Resource Usage | CPU, memory, disk metrics |
| Security Analysis | Port exposure and vulnerabilities |
| Recommendations | Action items and fixes |

---

## 🏥 Service Health Check

### Known Services

| Service | Port | Health Endpoint |
|---------|------|-----------------|
| Event Gateway | 8080 | /health |
| Refinory API | 8085 | /health |
| RAG Retriever | 7000 | /health |
| Qdrant | 6333 | /healthz |
| Embedder | 8081 | /health |
| Grafana | 3000 | /api/health |
| Prometheus | 9090 | /-/healthy |
| PostgreSQL | 5432 | TCP |
| Redis | 6379 | TCP |
| Nginx | 80 | TCP |

### Manual Health Checks
```bash
# Check specific service
curl http://localhost:8080/health

# Check all services quickly
for port in 8080 8085 7000 6333 3000 9090; do
  echo -n "Port $port: "
  curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/health 2>/dev/null && echo " ✓" || echo " ✗"
done
```

---

## 🐳 Docker Commands

### Container Management
```bash
# List all containers
docker ps -a

# Check service status
docker compose ps

# View logs
docker compose logs -f [service-name]

# Restart service
docker compose restart [service-name]

# Start all services
docker compose up -d
```

### Network Inspection
```bash
# List networks
docker network ls

# Inspect network
docker network inspect [network-name]

# Check container network
docker inspect -f '{{.NetworkSettings.Networks}}' [container-name]
```

### Resource Monitoring
```bash
# Live resource stats
docker stats

# One-time stats
docker stats --no-stream

# Disk usage
docker system df
```

---

## 🔒 Security Checks

### Port Exposure
```bash
# Check exposed ports
docker ps --format "{{.Names}}\t{{.Ports}}"

# Find 0.0.0.0 bindings
docker ps --format "{{.Names}}\t{{.Ports}}" | grep "0.0.0.0"
```

### Privileged Containers
```bash
# Find privileged containers
docker ps --format "{{.Names}}" | xargs -I {} docker inspect --format '{{.Name}}: {{.HostConfig.Privileged}}' {}
```

### Environment Security
```bash
# Check for weak passwords
grep -i "password\|secret" .env | grep -E "dev_|test_|changeme|admin"
```

---

## 📁 Report Locations

```bash
# Latest report (symlink)
recon/reports/latest_network_scan/recon_report.md

# All reports
ls -la recon/reports/

# Service health only
cat recon/reports/latest_network_scan/service_health.txt

# Resource usage
cat recon/reports/latest_network_scan/resource_usage.txt
```

---

## 🎯 Common Workflows

### Daily Health Check
```bash
./view_recon_report.sh --summary
```

### After Deployment
```bash
./network_recon.sh
./view_recon_report.sh --summary
```

### Troubleshooting Service Issues
```bash
# 1. Run reconnaissance
./network_recon.sh

# 2. Check service health
./view_recon_report.sh
# Select option 5 (Service Health)

# 3. Check logs
docker compose logs [service-name]

# 4. Restart if needed
docker compose restart [service-name]
```

### Security Audit
```bash
# 1. Run full scan
./network_recon.sh

# 2. Review security section
./view_recon_report.sh
# Select option 11 (Security Analysis)

# 3. Apply recommendations
# Follow suggestions in section 12 (Recommendations)
```

---

## 🔧 Integration Commands

### Start Infrastructure
```bash
# Main stack
docker compose up -d

# RECON stack
./launch-recon.sh start

# Observability stack
docker compose -f docker-compose.obs.yml up -d
```

### Stop Infrastructure
```bash
# Main stack
docker compose down

# RECON stack
./launch-recon.sh stop

# Everything
docker compose down && ./launch-recon.sh stop
```

---

## 📈 Monitoring Integration

### Export Metrics
```bash
# Service status for monitoring
cat recon/reports/latest_network_scan/service_health.txt

# Resource usage metrics
cat recon/reports/latest_network_scan/resource_usage.txt
```

### Prometheus Targets
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# View metrics
curl http://localhost:9090/metrics
```

---

## 🆘 Quick Troubleshooting

### "Docker is not running"
```bash
# Linux
sudo systemctl start docker

# Check status
docker ps
```

### "No containers found"
```bash
# Start infrastructure
docker compose up -d

# Or start specific stack
./launch-recon.sh start
```

### "Permission denied"
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Re-login for changes to take effect
```

### "Service DOWN but should be UP"
```bash
# Check if running
docker ps | grep [service-name]

# Check logs
docker logs [container-name]

# Restart
docker compose restart [service-name]
```

### "Reports not generating"
```bash
# Make scripts executable
chmod +x network_recon.sh view_recon_report.sh

# Check for errors
./network_recon.sh 2>&1 | tee recon_debug.log
```

---

## 📚 Documentation Links

- **[NETWORK_RECON_GUIDE.md](NETWORK_RECON_GUIDE.md)** - Complete guide
- **[recon/README.md](recon/README.md)** - RECON directory docs
- **[BOOT_RECON.md](BOOT_RECON.md)** - Bootstrap reconnaissance
- **[RECON_STACK_V2.md](RECON_STACK_V2.md)** - RAG system
- **[README.md](README.md)** - Main documentation

---

## 🎓 Pro Tips

1. **Automate daily checks**: Add to cron or use `watch`
   ```bash
   watch -n 300 './view_recon_report.sh --summary'
   ```

2. **Archive old reports**: Keep last 7 days only
   ```bash
   find recon/reports/network_scan_* -mtime +7 -exec rm -rf {} \;
   ```

3. **Export for CI/CD**: Parse reports in automation
   ```bash
   if grep -q "❌ DOWN" recon/reports/latest_network_scan/service_health.txt; then
     echo "Critical services down!"
     exit 1
   fi
   ```

4. **Custom service discovery**: Edit `recon/network_discovery.py` to add services

5. **Quick status check**: Just run summary
   ```bash
   alias recon-status='./view_recon_report.sh --summary'
   ```

---

**Quick Help**
```bash
# Network recon
./network_recon.sh --help

# Report viewer
./view_recon_report.sh --help

# Python discovery
python3 recon/network_discovery.py --help
```

---

*Strategic Khaos Sovereignty Architecture - Infrastructure Intelligence*
