# Trading Engine Deployment Guide v1.0

> **Document Type**: Deployment Guide  
> **Status**: DRAFT  
> **Last Updated**: 2025-11-25

---

## 1. Prerequisites

### 1.1 Infrastructure Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU Cores | 4 | 8+ |
| Memory | 16GB | 32GB+ |
| Storage | 100GB SSD | 500GB NVMe |
| Network | 1 Gbps | 10 Gbps |

### 1.2 Software Dependencies

- Docker Engine 24.0+
- Docker Compose 2.20+
- Kubernetes 1.28+ (for production)
- Helm 3.12+

### 1.3 External Services

- PostgreSQL 15+
- Redis 7+
- Apache Kafka 3.5+ (optional)

---

## 2. Environment Configuration

### 2.1 Required Environment Variables

```bash
# Core Configuration
TRADING_ENGINE_ENV=development|staging|production
TRADING_ENGINE_LOG_LEVEL=debug|info|warn|error

# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=trading_engine
DATABASE_USER=trading_user
DATABASE_PASSWORD=<secure-password>

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=<secure-password>

# Security Configuration
JWT_SECRET=<secure-secret>
API_KEY_SALT=<secure-salt>

# Integration Configuration
KEYCLOAK_URL=https://auth.sovereignty.local
VAULT_ADDR=https://vault.sovereignty.local
```

### 2.2 Configuration Files

Create configuration in `config/` directory:

```yaml
# config/trading-engine.yaml
server:
  port: 8080
  host: 0.0.0.0
  
database:
  pool_size: 20
  connection_timeout: 5000
  
risk:
  max_order_size: 1000000
  max_position_value: 10000000
  
logging:
  format: json
  output: stdout
```

---

## 3. Deployment Procedures

### 3.1 Local Development

```bash
# Clone repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Start dependencies
docker compose -f docker-compose.yml up -d postgres redis

# Start trading engine
docker compose -f docker-compose.yml up -d trading-engine

# Verify deployment
curl http://localhost:8080/health
```

### 3.2 Docker Deployment

```bash
# Build image
docker build -t trading-engine:v1.0 -f Dockerfile.trading-engine .

# Run container
docker run -d \
  --name trading-engine \
  --env-file .env \
  -p 8080:8080 \
  trading-engine:v1.0
```

### 3.3 Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace trading

# Create secrets
kubectl create secret generic trading-secrets \
  --from-literal=database-password=<password> \
  --from-literal=redis-password=<password> \
  -n trading

# Deploy with Helm
helm upgrade --install trading-engine ./charts/trading-engine \
  --namespace trading \
  --values ./charts/trading-engine/values.yaml \
  --set image.tag=v1.0

# Verify deployment
kubectl get pods -n trading
kubectl logs -f deployment/trading-engine -n trading
```

---

## 4. Post-Deployment Verification

### 4.1 Health Check Endpoints

| Endpoint | Description | Expected Response |
|----------|-------------|-------------------|
| `/health` | Basic health | `{"status": "healthy"}` |
| `/health/live` | Liveness probe | HTTP 200 |
| `/health/ready` | Readiness probe | HTTP 200 |
| `/metrics` | Prometheus metrics | Metrics payload |

### 4.2 Verification Commands

```bash
# Check service health
curl -s http://localhost:8080/health | jq .

# Check database connectivity
curl -s http://localhost:8080/health/db | jq .

# Check Redis connectivity
curl -s http://localhost:8080/health/cache | jq .

# View metrics
curl -s http://localhost:8080/metrics | head -50
```

### 4.3 Smoke Tests

```bash
# Submit test order (dry-run mode)
curl -X POST http://localhost:8080/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "X-Dry-Run: true" \
  -d '{"symbol": "TEST", "side": "buy", "quantity": 100, "price": 50.00}'

# Query positions
curl -s http://localhost:8080/api/v1/positions | jq .
```

---

## 5. Deployment Checklist

### 5.1 Pre-Deployment

- [ ] Environment variables configured
- [ ] Secrets created in Vault/Kubernetes
- [ ] Database schema migrated
- [ ] Network policies applied
- [ ] Monitoring dashboards configured

### 5.2 Deployment

- [ ] Image built and pushed to registry
- [ ] Kubernetes manifests applied
- [ ] Pods running and healthy
- [ ] Services exposed correctly
- [ ] Ingress configured (if applicable)

### 5.3 Post-Deployment

- [ ] Health endpoints responding
- [ ] Metrics being collected
- [ ] Logs appearing in aggregator
- [ ] Smoke tests passing
- [ ] Alerts configured and tested

---

## 6. Rollback Procedures

### 6.1 Kubernetes Rollback

```bash
# View deployment history
kubectl rollout history deployment/trading-engine -n trading

# Rollback to previous version
kubectl rollout undo deployment/trading-engine -n trading

# Rollback to specific revision
kubectl rollout undo deployment/trading-engine -n trading --to-revision=2
```

### 6.2 Docker Rollback

```bash
# Stop current container
docker stop trading-engine

# Start previous version
docker run -d \
  --name trading-engine \
  --env-file .env \
  -p 8080:8080 \
  trading-engine:v0.9  # Previous version
```

---

## 7. Monitoring Integration

### 7.1 Grafana Dashboards

Import the following dashboards:
- Trading Engine Overview
- Order Latency Metrics
- Risk Engine Metrics
- Settlement Metrics

### 7.2 Alert Rules

Configure alerts in Prometheus/Alertmanager:
- Order latency > 100ms
- Error rate > 1%
- Risk limit breaches
- Database connection failures

---

**Next Steps**: Review [security.md](security.md) for security configuration.
