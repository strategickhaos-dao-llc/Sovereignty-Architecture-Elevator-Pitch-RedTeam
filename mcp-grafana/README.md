# MCP Grafana Server

Model Context Protocol (MCP) server for Grafana integration. This server allows AI assistants like Claude to interact with Grafana dashboards, metrics, and alerts.

## Features

- **List Dashboards**: Retrieve all available Grafana dashboards
- **Get Dashboard Details**: Fetch specific dashboard configuration and panels
- **List Alerts**: View active Grafana alerts
- **Query Metrics**: Execute PromQL queries through Grafana
- **List Datasources**: View configured datasources
- **Health Check**: Monitor Grafana server health

## Setup

### Prerequisites

- Node.js 18+ or 20+
- Access to a Grafana instance
- Grafana API key (Admin or Viewer role)

### Installation

```bash
cd mcp-grafana
npm install
npm run build
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your Grafana credentials:
```env
GRAFANA_URL=http://localhost:3000
GRAFANA_API_KEY=your_api_key_here
```

### Generating a Grafana API Key

1. Navigate to Grafana → Configuration → API Keys
2. Click "Add API Key"
3. Set name: "MCP Server"
4. Set role: "Viewer" (or "Admin" for full access)
5. Copy the generated key to `.env`

## Usage

### Running the Server

```bash
# Development mode with auto-reload
npm run dev

# Production mode
npm run build
npm start
```

### Using with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "grafana": {
      "command": "node",
      "args": [
        "/path/to/mcp-grafana/dist/index.js"
      ],
      "env": {
        "GRAFANA_URL": "http://localhost:3000",
        "GRAFANA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Using with Docker

Build and run the MCP Grafana server in Docker:

```bash
docker build -t mcp-grafana-server .
docker run -e GRAFANA_URL=http://grafana:3000 -e GRAFANA_API_KEY=your_key mcp-grafana-server
```

## Available Tools

### list_dashboards
Lists all Grafana dashboards.

**Example:**
```
Can you show me all available Grafana dashboards?
```

### get_dashboard
Gets detailed information about a specific dashboard.

**Parameters:**
- `uid` (required): Dashboard UID

**Example:**
```
Show me the details of dashboard with UID "abc123"
```

### list_alerts
Lists all active Grafana alerts.

**Example:**
```
What alerts are currently active in Grafana?
```

### query_metrics
Queries Prometheus metrics through Grafana.

**Parameters:**
- `query` (required): PromQL query string
- `start` (optional): Start timestamp (Unix time)
- `end` (optional): End timestamp (Unix time)

**Example:**
```
Query the CPU usage metric: up{job="node"}
```

### list_datasources
Lists all configured Grafana datasources.

**Example:**
```
What datasources are configured in Grafana?
```

### check_health
Checks Grafana server health status.

**Example:**
```
Is Grafana healthy?
```

## Integration with Sovereignty Architecture

This MCP server integrates with the Sovereignty Architecture's monitoring stack:

- **Prometheus**: Access metrics through Grafana's datasource proxy
- **Loki**: Query logs via Grafana
- **Jaeger**: Access distributed traces
- **Alertmanager**: Monitor alert states

The server is designed to work seamlessly with the existing docker-compose setup and can be added as an additional service.

## Development

### Project Structure

```
mcp-grafana/
├── src/
│   └── index.ts          # Main MCP server implementation
├── dist/                 # Compiled JavaScript (generated)
├── package.json          # Node.js dependencies
├── tsconfig.json         # TypeScript configuration
├── .env.example          # Example environment variables
└── README.md             # This file
```

### Building

```bash
npm run build
```

### Linting

```bash
npm run lint
```

## Troubleshooting

### Connection Refused

If you see "connection refused" errors:
1. Verify Grafana is running: `curl http://localhost:3000/api/health`
2. Check `GRAFANA_URL` in `.env`
3. Ensure Grafana is accessible from the MCP server

### Authentication Failed

If you see "unauthorized" errors:
1. Verify your API key is valid
2. Check the API key hasn't expired
3. Ensure the API key has appropriate permissions

### No Data Returned

If queries return empty results:
1. Verify datasources are configured in Grafana
2. Check that metrics exist for your queries
3. Ensure time ranges are appropriate

## Contributing

Contributions are welcome! Please ensure:
- Code follows the existing TypeScript patterns
- All new tools are documented
- Error handling is comprehensive
- Tests are included (when available)

## License

MIT License - See main repository LICENSE file

## Support

For issues and questions:
- Open an issue in the main Sovereignty Architecture repository
- Join the Discord: https://discord.gg/strategickhaos
- Check the Wiki: https://wiki.strategickhaos.internal
