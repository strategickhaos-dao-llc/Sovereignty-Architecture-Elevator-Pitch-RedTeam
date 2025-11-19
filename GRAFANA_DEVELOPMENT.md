# Grafana Development Guide

This guide explains how to set up a Grafana development environment for the Strategickhaos Sovereignty Architecture project, enabling custom dashboard development, plugin creation, and contributions to Grafana itself.

## Overview

The Strategickhaos project uses Grafana for monitoring and observability. This development setup allows you to:

- **Develop Custom Dashboards**: Create and test dashboards before deploying to production
- **Build Grafana Plugins**: Extend Grafana functionality with custom panels and data sources
- **Contribute to Grafana**: Work on Grafana core features and bug fixes
- **Test Integrations**: Validate Prometheus, Loki, and Jaeger integrations locally

## Prerequisites

### Required Tools

- **Git**: Version control
- **Node.js**: v18+ (for frontend development)
- **Go**: 1.21+ (for backend development)
- **Make**: Build automation
- **Docker**: For running the full stack

### Optional Tools

- **GitHub CLI (`gh`)**: Simplifies repository operations
- **Yarn**: Alternative to npm for package management

## Quick Start

### 1. Clone Grafana Repository

Use the provided setup script to clone the Grafana repository:

```bash
./scripts/setup-grafana-dev.sh
```

This script will:
- Check for required dependencies
- Clone the Grafana repository to `dev/grafana/`
- Optionally set up the development environment
- Link custom Strategickhaos dashboards

### 2. Manual Clone (Alternative)

If you prefer manual setup:

```bash
# Using GitHub CLI
gh repo clone grafana/grafana dev/grafana

# Or using git
git clone https://github.com/grafana/grafana.git dev/grafana
```

## Development Workflows

### Custom Dashboard Development

#### Option 1: Using Grafana UI

1. Start the Strategickhaos monitoring stack:
   ```bash
   docker-compose up -d
   ```

2. Access Grafana at http://localhost:3000
   - Username: `admin`
   - Password: `admin` (or `$GRAFANA_PASSWORD` from .env)

3. Create your dashboard in the UI

4. Export the dashboard JSON:
   - Dashboard Settings → JSON Model
   - Copy JSON to `monitoring/grafana/dashboards/my-dashboard.json`

5. The dashboard will be automatically provisioned on next restart

#### Option 2: Using Development Build

1. Start Grafana development server:
   ```bash
   cd dev/grafana
   make run
   ```

2. Access development Grafana at http://localhost:3000

3. Develop and test dashboards with hot-reload

### Plugin Development

#### Create a New Plugin

1. Navigate to Grafana directory:
   ```bash
   cd dev/grafana
   ```

2. Create plugin scaffold:
   ```bash
   npx @grafana/toolkit plugin:create my-custom-panel
   cd data/plugins/my-custom-panel
   ```

3. Develop your plugin:
   ```bash
   npm install
   npm run dev
   ```

4. Test plugin in development Grafana:
   - Plugin appears automatically in development mode
   - Changes hot-reload

#### Install Plugin in Production

1. Build plugin:
   ```bash
   npm run build
   ```

2. Copy to Strategickhaos plugins directory:
   ```bash
   mkdir -p monitoring/grafana/plugins
   cp -r dist monitoring/grafana/plugins/my-custom-panel
   ```

3. Update docker-compose.yml:
   ```yaml
   grafana:
     volumes:
       - ./monitoring/grafana/plugins:/var/lib/grafana/plugins
   ```

4. Restart stack:
   ```bash
   docker-compose restart grafana
   ```

### Contributing to Grafana

#### Setup Development Environment

1. Fork Grafana repository on GitHub

2. Add your fork as remote:
   ```bash
   cd dev/grafana
   git remote add fork https://github.com/YOUR_USERNAME/grafana.git
   ```

3. Create feature branch:
   ```bash
   git checkout -b feature/my-improvement
   ```

4. Install dependencies:
   ```bash
   yarn install
   ```

5. Build backend:
   ```bash
   make build-go
   ```

#### Development Workflow

1. Make your changes

2. Run tests:
   ```bash
   # Frontend tests
   yarn test

   # Backend tests
   make test-go

   # Integration tests
   make test
   ```

3. Lint code:
   ```bash
   # Frontend
   yarn lint

   # Backend
   make lint-go
   ```

4. Commit and push:
   ```bash
   git add .
   git commit -m "feat: description of change"
   git push fork feature/my-improvement
   ```

5. Create pull request on GitHub

## Integration with Strategickhaos Stack

### Datasource Configuration

The Strategickhaos stack provisions datasources automatically:

- **Prometheus**: http://prometheus:9090 (metrics)
- **Loki**: http://loki:3100 (logs)
- **Jaeger**: http://jaeger:16686 (traces)

Configuration: `monitoring/grafana/provisioning/datasources/datasources.yml`

### Custom Dashboards

Place dashboard JSON files in `monitoring/grafana/dashboards/`:

```bash
monitoring/grafana/dashboards/
├── strategickhaos-overview.json
├── discord-bot-metrics.json
├── event-gateway-performance.json
└── ai-agent-analytics.json
```

Dashboards are automatically provisioned with these settings:
- Folder: "Strategickhaos"
- Update interval: 30 seconds
- UI updates: Allowed

### Development vs Production

| Aspect | Development (`dev/grafana`) | Production (`docker-compose`) |
|--------|---------------------------|------------------------------|
| Source | Cloned repository | Docker image |
| Port | 3000 | 3000 |
| Data | Ephemeral | Persistent volume |
| Plugins | Hot-reload | Requires restart |
| Dashboards | Manual | Auto-provisioned |

## Common Tasks

### Update Grafana Version

Production (Docker):
```bash
# Edit docker-compose.yml
image: grafana/grafana:11.2.0  # Update version

docker-compose pull grafana
docker-compose up -d grafana
```

Development (Source):
```bash
cd dev/grafana
git fetch origin
git checkout v11.2.0  # Specific version
# or
git pull origin main  # Latest main
```

### Debug Grafana Issues

1. Check logs:
   ```bash
   # Production
   docker-compose logs -f grafana

   # Development
   cd dev/grafana
   tail -f data/log/grafana.log
   ```

2. Enable debug logging:
   ```bash
   # Add to docker-compose.yml
   environment:
     GF_LOG_LEVEL: debug
   ```

3. Connect to container:
   ```bash
   docker-compose exec grafana bash
   ```

### Export/Import Dashboards

Export:
```bash
# Using API
curl -H "Authorization: Bearer $API_KEY" \
     http://localhost:3000/api/dashboards/uid/dashboard-uid \
     | jq '.dashboard' > my-dashboard.json

# Using UI
Dashboard Settings → JSON Model → Copy
```

Import:
```bash
# Place in provisioning directory
cp my-dashboard.json monitoring/grafana/dashboards/

# Restart to load
docker-compose restart grafana
```

### Test Custom Datasource Plugin

1. Create datasource plugin:
   ```bash
   cd dev/grafana
   npx @grafana/toolkit plugin:create my-datasource --pluginType=datasource
   ```

2. Implement datasource logic in `src/datasource.ts`

3. Test locally:
   ```bash
   cd data/plugins/my-datasource
   npm run dev
   ```

4. Add to production:
   ```bash
   npm run build
   cp -r dist monitoring/grafana/plugins/my-datasource
   ```

## Testing

### Frontend Tests

```bash
cd dev/grafana

# Run all tests
yarn test

# Run specific test file
yarn test --testPathPattern=PanelEditor

# Watch mode
yarn test --watch
```

### Backend Tests

```bash
cd dev/grafana

# Run all Go tests
make test-go

# Run specific package
go test ./pkg/services/alerting/...

# With coverage
make test-go-coverage
```

### Integration Tests

```bash
cd dev/grafana

# Run integration tests
make test-integration

# Run E2E tests (requires Docker)
make test-e2e
```

## Troubleshooting

### Issue: Port 3000 Already in Use

Solution:
```bash
# Stop production Grafana
docker-compose stop grafana

# Or use different port for development
cd dev/grafana
GF_SERVER_HTTP_PORT=3001 make run
```

### Issue: Plugin Not Loading

Solution:
```bash
# Check plugin directory
ls -la monitoring/grafana/plugins/

# Verify plugin.json exists
cat monitoring/grafana/plugins/my-plugin/plugin.json

# Check Grafana logs
docker-compose logs grafana | grep -i plugin
```

### Issue: Database Migration Errors

Solution:
```bash
# Reset development database
cd dev/grafana
rm data/grafana.db
make run  # Will recreate database
```

### Issue: Build Failures

Solution:
```bash
# Clean and rebuild
cd dev/grafana
make clean
make build-go
yarn install
```

## Best Practices

### Dashboard Development

1. **Use Variables**: Make dashboards reusable with template variables
2. **Set Refresh Intervals**: Configure appropriate auto-refresh rates
3. **Add Descriptions**: Document panel purposes and queries
4. **Test with Real Data**: Use production-like data for validation
5. **Version Control**: Commit dashboard JSON to git

### Plugin Development

1. **Follow Conventions**: Use Grafana's coding standards
2. **Add Tests**: Write unit tests for plugin logic
3. **Document**: Include README and usage examples
4. **Sign Plugins**: Required for production use
5. **Performance**: Optimize queries and rendering

### Git Workflow

1. **Keep Updated**: Regularly sync with upstream Grafana
2. **Feature Branches**: One feature per branch
3. **Commit Messages**: Follow conventional commits format
4. **Pull Before Push**: Avoid merge conflicts
5. **Clean History**: Squash commits when appropriate

## Resources

### Documentation

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Plugin Development Guide](https://grafana.com/docs/grafana/latest/developers/plugins/)
- [Grafana API Reference](https://grafana.com/docs/grafana/latest/http_api/)
- [Dashboard Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)

### Community

- [Grafana Community Forums](https://community.grafana.com/)
- [Grafana Slack](https://grafana.slack.com/)
- [GitHub Issues](https://github.com/grafana/grafana/issues)
- [Contributing Guide](https://github.com/grafana/grafana/blob/main/CONTRIBUTING.md)

### Strategickhaos Resources

- Main README: [README.md](README.md)
- Monitoring Setup: [monitoring/](monitoring/)
- Docker Compose: [docker-compose.yml](docker-compose.yml)
- Discord Integration: [GITLENS_INTEGRATION.md](GITLENS_INTEGRATION.md)

## Support

For issues related to:

- **Grafana Core**: Report to [grafana/grafana](https://github.com/grafana/grafana/issues)
- **Strategickhaos Integration**: Open issue in this repository
- **Dashboard Questions**: Ask in Discord #monitoring channel
- **Plugin Development**: Check Grafana community forums

---

**Last Updated**: November 2025

**Maintained by**: Strategickhaos Swarm Intelligence
