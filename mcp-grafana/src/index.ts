#!/usr/bin/env node

/**
 * MCP Grafana Server
 * Model Context Protocol server for Grafana integration
 * Allows AI assistants to interact with Grafana dashboards, metrics, and alerts
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import axios, { AxiosInstance } from 'axios';
import * as dotenv from 'dotenv';

dotenv.config();

// Grafana API client
class GrafanaClient {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor(baseUrl: string, apiKey: string) {
    this.baseUrl = baseUrl;
    this.client = axios.create({
      baseURL: baseUrl,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
    });
  }

  async getDashboards(): Promise<any> {
    const response = await this.client.get('/api/search?type=dash-db');
    return response.data;
  }

  async getDashboard(uid: string): Promise<any> {
    const response = await this.client.get(`/api/dashboards/uid/${uid}`);
    return response.data;
  }

  async getAlerts(): Promise<any> {
    const response = await this.client.get('/api/alerting/alerts');
    return response.data;
  }

  async queryPrometheus(query: string, start?: number, end?: number): Promise<any> {
    const params: any = { query };
    if (start) params.start = start;
    if (end) params.end = end;
    
    const response = await this.client.get('/api/datasources/proxy/1/api/v1/query', { params });
    return response.data;
  }

  async getDatasources(): Promise<any> {
    const response = await this.client.get('/api/datasources');
    return response.data;
  }

  async getHealth(): Promise<any> {
    const response = await this.client.get('/api/health');
    return response.data;
  }
}

// Initialize Grafana client
const grafanaUrl = process.env.GRAFANA_URL || 'http://localhost:3000';
const grafanaApiKey = process.env.GRAFANA_API_KEY || '';
const grafanaClient = new GrafanaClient(grafanaUrl, grafanaApiKey);

// Define available tools
const tools: Tool[] = [
  {
    name: 'list_dashboards',
    description: 'List all Grafana dashboards',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'get_dashboard',
    description: 'Get details of a specific Grafana dashboard by UID',
    inputSchema: {
      type: 'object',
      properties: {
        uid: {
          type: 'string',
          description: 'The UID of the dashboard',
        },
      },
      required: ['uid'],
    },
  },
  {
    name: 'list_alerts',
    description: 'List all active Grafana alerts',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'query_metrics',
    description: 'Query Prometheus metrics through Grafana',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'PromQL query string',
        },
        start: {
          type: 'number',
          description: 'Start timestamp (Unix time)',
        },
        end: {
          type: 'number',
          description: 'End timestamp (Unix time)',
        },
      },
      required: ['query'],
    },
  },
  {
    name: 'list_datasources',
    description: 'List all configured Grafana datasources',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'check_health',
    description: 'Check Grafana server health status',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
];

// Create MCP server
const server = new Server(
  {
    name: 'mcp-grafana-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Handle tool listing
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'list_dashboards': {
        const dashboards = await grafanaClient.getDashboards();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(dashboards, null, 2),
            },
          ],
        };
      }

      case 'get_dashboard': {
        const { uid } = args as { uid: string };
        const dashboard = await grafanaClient.getDashboard(uid);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(dashboard, null, 2),
            },
          ],
        };
      }

      case 'list_alerts': {
        const alerts = await grafanaClient.getAlerts();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(alerts, null, 2),
            },
          ],
        };
      }

      case 'query_metrics': {
        const { query, start, end } = args as { query: string; start?: number; end?: number };
        const results = await grafanaClient.queryPrometheus(query, start, end);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(results, null, 2),
            },
          ],
        };
      }

      case 'list_datasources': {
        const datasources = await grafanaClient.getDatasources();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(datasources, null, 2),
            },
          ],
        };
      }

      case 'check_health': {
        const health = await grafanaClient.getHealth();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(health, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('MCP Grafana Server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
