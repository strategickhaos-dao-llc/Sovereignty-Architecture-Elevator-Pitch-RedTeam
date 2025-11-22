# Operational Quick Start Guide

**5-Minute Guide to Verifying Your Production Infrastructure**

---

## 🎯 Immediate Actions (Next 5 Minutes)

### 1. Check Grafana Dashboard

Your monitoring is already running. Let's see it:

```bash
# Find Grafana container and port
docker ps | grep grafana

# Open in browser (likely one of these):
# http://localhost:3000
# http://localhost:3001

# Default credentials:
# Username: admin
# Password: admin (or check .env file for GRAFANA_PASSWORD)
```

**What to look for:**
- System resource graphs (CPU, RAM, disk)
- Container health status
- Service response times
- Network traffic

**If Grafana shows data → Your monitoring stack is operational! ✅**

---

### 2. List All Running Services

See everything that's operational right now:

```bash
# View all running containers
docker ps

# For Kubernetes (if applicable)
kubectl get pods --all-namespaces

# See live resource usage
docker stats
```

**What you're looking for:**
- Status: "Up" or "Running"
- Health: "healthy" (if health checks are configured)
- Restarts: Low number = stable
- CPU/RAM: Within expected ranges

---

### 3. Check Service Health

Quick health checks for key services:

```bash
# Check PostgreSQL
docker exec -it $(docker ps -qf "name=postgres") pg_isready

# Check Redis
docker exec -it $(docker ps -qf "name=redis") redis-cli ping

# Check Qdrant (vector database)
curl http://localhost:6333/health

# Check MinIO (object storage)
curl http://localhost:9000/minio/health/live

# Check Prometheus
curl http://localhost:9090/-/healthy
```

**Expected responses:**
- PostgreSQL: "accepting connections"
- Redis: "PONG"
- Qdrant: `{"status":"ok"}`
- MinIO: 200 OK
- Prometheus: "Prometheus is Healthy."

---

## 📊 Generate Infrastructure Report (30 Minutes)

Create a snapshot of your current infrastructure:

```bash
# Create a reports directory
mkdir -p /path/to/I_drive/infrastructure_reports
cd /path/to/I_drive/infrastructure_reports

# Timestamp for files
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 1. List all running containers
docker ps > containers_running_${TIMESTAMP}.txt

# 2. List all volumes
docker volume ls > volumes_${TIMESTAMP}.txt

# 3. Show resource usage
docker stats --no-stream > resource_usage_${TIMESTAMP}.txt

# 4. System disk usage
df -h > disk_usage_${TIMESTAMP}.txt

# 5. Docker system info
docker system df -v > docker_system_${TIMESTAMP}.txt

# 6. Kubernetes pods (if applicable)
kubectl get pods -A > k8s_pods_${TIMESTAMP}.txt 2>/dev/null || echo "Kubernetes not configured"

# 7. List all images
docker images > images_${TIMESTAMP}.txt

# 8. Network information
docker network ls > networks_${TIMESTAMP}.txt

# Create summary report
cat > infrastructure_summary_${TIMESTAMP}.md << EOF
# Infrastructure Summary Report

**Generated:** $(date)

## Quick Stats
- **Running Containers:** $(docker ps -q | wc -l)
- **Total Volumes:** $(docker volume ls -q | wc -l)
- **Total Images:** $(docker images -q | wc -l)
- **Total Networks:** $(docker network ls -q | wc -l)

## Disk Usage
$(df -h | grep -E 'Filesystem|/|docker')

## Top 5 Containers by Memory
$(docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}" | head -6)

## Volume Sizes
$(docker system df -v | grep -A 100 "Local Volumes" | head -20)

## Service Health Status
- PostgreSQL: $(docker exec $(docker ps -qf "name=postgres") pg_isready 2>&1)
- Redis: $(docker exec $(docker ps -qf "name=redis") redis-cli ping 2>&1)
- Qdrant: $(curl -s http://localhost:6333/health 2>&1)
EOF

echo "✅ Infrastructure report generated in: $(pwd)"
echo "📊 Report files created with timestamp: ${TIMESTAMP}"
```

This creates a complete snapshot you can reference or share.

---

## 🔍 Service-Specific Commands

### PostgreSQL

```bash
# Access PostgreSQL shell
docker exec -it $(docker ps -qf "name=postgres") psql -U postgres

# List databases
docker exec -it $(docker ps -qf "name=postgres") psql -U postgres -c '\l'

# Check database size
docker exec -it $(docker ps -qf "name=postgres") psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('strategickhaos'));"
```

### Redis

```bash
# Access Redis CLI
docker exec -it $(docker ps -qf "name=redis") redis-cli

# Check memory usage
docker exec -it $(docker ps -qf "name=redis") redis-cli INFO memory

# List keys (be careful in production with many keys)
docker exec -it $(docker ps -qf "name=redis") redis-cli KEYS "*"
```

### Qdrant (Vector Database)

```bash
# List collections
curl http://localhost:6333/collections

# Get collection info (replace 'collection_name' with actual name)
curl http://localhost:6333/collections/collection_name

# Check cluster status
curl http://localhost:6333/cluster
```

### MinIO (Object Storage)

```bash
# Access MinIO console in browser
open http://localhost:9001

# Login credentials (check .env or use defaults):
# Username: admin
# Password: minioadmin

# List buckets (requires mc client)
docker exec -it $(docker ps -qf "name=minio") mc ls local
```

### Ollama (LLM Runtime)

```bash
# List available models
docker exec -it $(docker ps -qf "name=ollama") ollama list

# Check if Ollama is responsive
curl http://localhost:11434/api/tags

# Run a test query (if models are loaded)
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:72b",
  "prompt": "Hello, are you operational?",
  "stream": false
}'
```

---

## 🚨 Troubleshooting Quick Checks

### Container Not Running?

```bash
# Check logs for errors
docker logs <container_name>

# Check last 100 lines
docker logs --tail 100 <container_name>

# Follow logs in real-time
docker logs -f <container_name>

# Restart container
docker restart <container_name>
```

### Service Not Responding?

```bash
# Check if port is listening
netstat -an | grep <port_number>

# On Linux/Mac:
lsof -i :<port_number>

# Check Docker network
docker network inspect strategickhaos_network

# Test service connectivity
curl -v http://localhost:<port>
```

### High Resource Usage?

```bash
# Find top consumers
docker stats --no-stream | sort -k3 -h

# Check specific container
docker stats <container_name>

# View container processes
docker top <container_name>
```

### Disk Space Issues?

```bash
# Check overall disk usage
df -h

# Check Docker disk usage
docker system df

# Clean up unused resources (DANGER: This removes ALL unused data including volumes!)
# Safer option: Remove only containers and images (preserves volumes)
docker system prune -a

# If you REALLY need to remove volumes too (WILL DELETE DATA):
# docker system prune -a --volumes

# Remove specific unused volumes
docker volume prune
```

---

## 📋 Daily Health Check (2 Minutes)

Quick morning check to ensure everything is healthy:

```bash
#!/bin/bash
# Save as: daily_health_check.sh

echo "=== DAILY INFRASTRUCTURE HEALTH CHECK ==="
echo "Date: $(date)"
echo ""

echo "1. Running Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -10

echo ""
echo "2. Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -6

echo ""
echo "3. Disk Space:"
df -h | grep -E 'Filesystem|/$|/docker'

echo ""
echo "4. Key Service Health:"
echo "  - PostgreSQL: $(docker exec $(docker ps -qf 'name=postgres') pg_isready 2>&1 | cut -d':' -f2-)"
echo "  - Redis: $(docker exec $(docker ps -qf 'name=redis') redis-cli ping 2>&1)"
echo "  - Qdrant: $(curl -s http://localhost:6333/health 2>&1 | jq -r .status 2>/dev/null || echo 'Check manually')"

echo ""
echo "=== END HEALTH CHECK ==="
```

Make it executable:
```bash
chmod +x daily_health_check.sh
./daily_health_check.sh
```

---

## 🎯 Weekly Maintenance (30 Minutes)

Run these commands weekly:

```bash
#!/bin/bash
# Save as: weekly_maintenance.sh

BACKUP_DIR="/path/to/I_drive/backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

echo "=== WEEKLY MAINTENANCE ==="
date

# 1. Export Grafana dashboards
echo "📊 Backing up Grafana dashboards..."
# (Add Grafana backup commands if API is configured)

# 2. Backup PostgreSQL
echo "💾 Backing up PostgreSQL..."
docker exec $(docker ps -qf "name=postgres") pg_dumpall -U postgres > "$BACKUP_DIR/postgres_backup.sql"

# 3. Export Docker volume list
echo "📦 Saving volume inventory..."
docker volume ls > "$BACKUP_DIR/volumes.txt"

# 4. Check for image updates
echo "🔄 Checking for image updates..."
docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>" > "$BACKUP_DIR/images.txt"

# 5. Clean up old logs (older than 30 days)
echo "🧹 Cleaning old logs..."
find /var/lib/docker/containers -name "*-json.log" -mtime +30 -delete 2>/dev/null || echo "Need sudo for log cleanup"

# 6. Check SSL certificates (if applicable)
echo "🔐 Checking SSL certificates..."
# Add SSL cert checks here

echo "✅ Weekly maintenance complete. Backups saved to: $BACKUP_DIR"
```

---

## 🔐 Security Quick Checks

### Check for Security Updates

```bash
# Update system packages (Ubuntu/Debian)
sudo apt update && sudo apt list --upgradable

# Update Docker images (careful - test in non-prod first)
docker-compose pull

# Check for vulnerable images
docker scan <image_name> || echo "Install Docker scan plugin"
```

### Review Access Logs

```bash
# PostgreSQL connections
docker exec $(docker ps -qf "name=postgres") tail -n 50 /var/log/postgresql/postgresql-*.log

# Nginx access logs
docker exec $(docker ps -qf "name=nginx") tail -n 50 /var/log/nginx/access.log

# Check failed login attempts
docker logs $(docker ps -qf "name=keycloak") | grep -i "failed\|error" | tail -20
```

---

## 📈 Performance Monitoring URLs

Access these in your browser:

| Service | URL | Purpose |
|---------|-----|---------|
| Grafana | http://localhost:3000 | Visual dashboards |
| Prometheus | http://localhost:9090 | Metrics browser |
| Prometheus Targets | http://localhost:9090/targets | Service health |
| Qdrant Dashboard | http://localhost:6333/dashboard | Vector DB metrics |
| MinIO Console | http://localhost:9001 | Object storage UI |
| cAdvisor | http://localhost:8080 | Container metrics |

---

## 🎓 Learning Your Infrastructure

### Start Here:

1. **Open Grafana** and explore existing dashboards
2. **Check Prometheus targets** to see what's being monitored
3. **Review Docker logs** for one service to understand log format
4. **Access PostgreSQL** and list databases
5. **Check Qdrant collections** to see vector data

### Next Level:

1. Create a custom Grafana dashboard
2. Add a new Prometheus scrape target
3. Deploy a test service and monitor it
4. Create a backup automation script
5. Set up alerting rules

---

## 🆘 Emergency Commands

### Stop Everything:

```bash
# Stop all containers
docker stop $(docker ps -q)

# Or with docker-compose
docker-compose down
```

### Emergency Backup:

```bash
# Quick backup of critical data
EMERGENCY_BACKUP="/tmp/emergency_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EMERGENCY_BACKUP"

# Backup all volumes (safely handle volume names with spaces/special chars)
for volume in $(docker volume ls -q); do
    docker run --rm -v "$volume":/data -v "$EMERGENCY_BACKUP":/backup alpine tar czf /backup/"$volume".tar.gz /data
done

echo "Emergency backup complete: $EMERGENCY_BACKUP"
```

### Restart Everything:

```bash
# Restart all containers
docker restart $(docker ps -q)

# Or with docker-compose
docker-compose restart
```

---

## 📱 Mobile Monitoring Setup

Monitor your infrastructure from your phone:

### Option 1: Grafana Mobile App
1. Download "Grafana" app from app store
2. Add your Grafana instance: http://your-server-ip:3000
3. Login with credentials
4. View dashboards on mobile

### Option 2: SSH + Termux (Android)
1. Install Termux from F-Droid
2. Install SSH: `pkg install openssh`
3. Connect: `ssh user@your-server-ip`
4. Run health checks remotely

### Option 3: Discord Notifications
Already set up in your infrastructure!
- Alerts go to designated Discord channels
- Check your phone for notifications

---

## 🎯 Success Metrics

**You'll know your infrastructure is healthy when:**

- ✅ All containers show "healthy" or "running" status
- ✅ Grafana displays current data (updated within last minute)
- ✅ Prometheus shows all targets "UP"
- ✅ Disk usage is under 80%
- ✅ No containers repeatedly restarting
- ✅ Service response times are under 1 second
- ✅ No critical alerts in logs
- ✅ Backups are completing successfully

---

## 📚 Additional Resources

- **Main Documentation:** [README.md](./README.md)
- **Infrastructure Reality Check:** [INFRASTRUCTURE_REALITY_CHECK.md](./INFRASTRUCTURE_REALITY_CHECK.md)
- **Deployment Guide:** [DEPLOYMENT_COMPLETE.md](./DEPLOYMENT_COMPLETE.md)
- **Security Playbook:** [VAULT_SECURITY_PLAYBOOK.md](./VAULT_SECURITY_PLAYBOOK.md)

---

**Remember:** This infrastructure is production-grade. Treat it with respect, but don't be afraid to explore and learn!

---

*Quick Start Guide version: 1.0*  
*Created: November 2025*  
*Status: ✅ READY FOR USE*
