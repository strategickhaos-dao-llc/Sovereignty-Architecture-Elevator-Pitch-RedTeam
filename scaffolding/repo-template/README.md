# Project Name

**Sovereign, Evolvable, Observable Infrastructure**

Built following the [Legends of Minds Engineering Canon v1.0](../CANON.md)

## Quick Start

```bash
# Install dependencies
npm install  # or: pip install -e ".[dev]"

# Run tests
npm test  # or: pytest

# Start development server
npm run dev  # or: uvicorn main:app --reload

# Build for production
npm run build  # or: docker build -t myapp .
```

## Architecture

This project follows **Hexagonal Architecture** (Canon #26):

```
src/
├── core/           # Business logic (no external dependencies)
│   ├── domain/     # Domain entities
│   ├── usecases/   # Application use cases
│   └── ports/      # Interfaces to external world
├── adapters/       # External integrations
│   ├── http/       # HTTP API
│   ├── db/         # Database
│   └── external/   # Third-party APIs
└── main.ts         # Dependency injection / wiring
```

**Key Principles:**
- Dependencies point inward (Canon #29)
- Business logic independent of frameworks
- Easy to test, easy to change

## Observability

**Three Pillars** (Canon #46):
- **Logs:** Structured JSON with correlation IDs
- **Metrics:** Prometheus-compatible (RED metrics)
- **Traces:** OpenTelemetry distributed tracing

**Access:**
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Jaeger: http://localhost:16686

## Development Workflow

### 1. Make Changes
```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes, add tests
```

### 2. Test Locally
```bash
# Run tests
npm test

# Run linter
npm run lint

# Check types
npm run type-check
```

### 3. Deploy
```bash
# Deploy to staging (canary)
./deploy.sh staging

# Monitor metrics in Grafana
# If metrics look good, deploy to prod

# Deploy to production
./deploy.sh production
```

## Chaos Engineering (Canon #56-60)

**Run chaos tests weekly:**

```bash
# Kill random instances
npm run chaos:kill-pods

# Inject network latency
npm run chaos:latency

# Fill disk space
npm run chaos:fill-disk
```

**Game Days:** First Friday of each month, full team participation.

## Security (Canon #66-85)

**Zero Trust:**
- All requests authenticated (no trust based on network)
- Least privilege access (minimal permissions)
- Continuous verification (risk-based auth)

**Secrets Management:**
- Never commit secrets (use Vault or env vars)
- Rotate credentials regularly
- Audit all access

## Deployment

### Blue-Green Deployment (Canon #61)
```bash
# Deploy new version to "green" environment
docker-compose -f docker-compose.green.yml up -d

# Switch traffic to green
./switch-traffic.sh green

# Old "blue" kept running for instant rollback
```

### Feature Flags (Canon #64)
```typescript
if (featureFlags.isEnabled('new-algorithm')) {
  return newAlgorithm();
} else {
  return oldAlgorithm();
}
```

## Performance (Canon #86-95)

**Caching Strategy:**
- Read-through cache for frequently accessed data
- CDN for static assets
- Redis for session state

**Scaling:**
- Horizontal scaling (add more instances)
- Stateless services (session in Redis, not memory)
- Auto-scaling based on CPU/memory metrics

## Contributing

1. Read [CANON.md](../CANON.md) to understand our engineering principles
2. Follow the existing code structure (Hexagonal Architecture)
3. Add tests for all new features
4. Update documentation
5. Submit PR with clear description

## Support

- Issues: https://github.com/yourusername/yourproject/issues
- Docs: https://docs.yourproject.com
- Runbooks: `docs/runbooks/`

---

**Built with 🔥 following Legends of Minds Engineering Canon v1.0**

*Sovereign. Evolvable. Observable.*
