/**
 * Queen.js Federation Hub
 * 
 * Central webhook coordinator for multi-org GitHub federation.
 * Routes webhooks from all GitHub organizations to unified NATS message bus
 * and Discord channels.
 * 
 * Federation Architecture:
 * - Strategickhaos (personal/main)
 * - Strategickhaos-Swarm-Intelligence (team/projects)
 * - SNHU Enterprise (school)
 * 
 * All webhooks point to Queen → Queen routes to NATS → Consumers act on events
 */

import express, { Request, Response, NextFunction } from "express";
import crypto from "crypto";

interface OrganizationRouting {
  nats_prefix: string;
  discord_channel: string;
}

interface RoutingConfig {
  [org: string]: OrganizationRouting;
}

interface NATSClient {
  publish(subject: string, data: string): Promise<void>;
  connected: boolean;
}

interface QueenConfig {
  port: number;
  natsUrl: string;
  webhookSecret: string;
  discordWebhooks: {
    github: string;
    financial: string;
  };
  organizations: RoutingConfig;
}

// Check if running in production
const isProduction = process.env.NODE_ENV === "production";

// Default configuration
const defaultConfig: QueenConfig = {
  port: Number(process.env.PORT) || 8081,
  natsUrl: process.env.NATS_URL || "nats://localhost:4222",
  webhookSecret: process.env.GITHUB_WEBHOOK_SECRET || "",
  discordWebhooks: {
    github: process.env.DISCORD_WEBHOOK_GITHUB || "",
    financial: process.env.DISCORD_WEBHOOK_FINANCIAL || "",
  },
  organizations: {
    "Strategickhaos": {
      nats_prefix: "strategickhaos",
      discord_channel: "#github-main",
    },
    "Strategickhaos-Swarm-Intelligence": {
      nats_prefix: "swarm",
      discord_channel: "#github-swarm",
    },
    "SNHU": {
      nats_prefix: "snhu",
      discord_channel: "#github-school",
    },
  },
};

// In-memory mock NATS client for environments without NATS
class MockNATSClient implements NATSClient {
  connected = true;
  private eventLog: Array<{ subject: string; data: string; timestamp: Date }> = [];

  async publish(subject: string, data: string): Promise<void> {
    this.eventLog.push({ subject, data, timestamp: new Date() });
    console.log(`📤 [NATS Mock] Published to ${subject}`);
  }

  getEventLog() {
    return this.eventLog;
  }
}

// Create Express app
const app = express();

// Keep raw body for signature verification
app.use(
  express.json({
    verify: (req: Request & { rawBody?: string }, _res, buf) => {
      req.rawBody = buf.toString();
    },
  })
);

// NATS client instance (mock for now, can be replaced with real NATS connection)
let natsClient: NATSClient = new MockNATSClient();

// Configuration
let config: QueenConfig = defaultConfig;

/**
 * Verify GitHub webhook signature
 */
function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  if (!secret || !signature) return false;

  const hmac = crypto.createHmac("sha256", secret);
  const digest = "sha256=" + hmac.update(payload).digest("hex");

  try {
    return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
  } catch {
    return false;
  }
}

/**
 * Format Discord embed message
 */
function formatDiscordMessage(
  event: string,
  payload: Record<string, unknown>
): string {
  const repo = (payload.repository as { name?: string })?.name || "unknown";
  const sender = (payload.sender as { login?: string })?.login || "unknown";

  switch (event) {
    case "push":
      return `📦 Push to ${repo} by ${sender}`;
    case "pull_request": {
      const pr = payload.pull_request as { number?: number };
      const action = payload.action as string;
      return `🔀 PR #${pr?.number || "?"} ${action} in ${repo}`;
    }
    case "issues": {
      const issue = payload.issue as { number?: number };
      const action = payload.action as string;
      return `🐛 Issue #${issue?.number || "?"} ${action} in ${repo}`;
    }
    case "check_suite": {
      const checkSuite = payload.check_suite as {
        status?: string;
        conclusion?: string;
      };
      return `✅ Checks ${checkSuite?.status || "unknown"} (${checkSuite?.conclusion || "pending"}) in ${repo}`;
    }
    case "deployment":
      return `🚀 Deployment in ${repo}`;
    case "deployment_status":
      return `📊 Deployment status updated in ${repo}`;
    default:
      return `📨 ${event} in ${repo}`;
  }
}

/**
 * Create Discord embed object
 */
function createEmbed(
  event: string,
  payload: Record<string, unknown>
): Record<string, unknown> {
  const pr = payload.pull_request as { html_url?: string };
  const issue = payload.issue as { html_url?: string };
  const repository = payload.repository as { html_url?: string };

  const url =
    pr?.html_url || issue?.html_url || repository?.html_url || undefined;

  return {
    title: formatDiscordMessage(event, payload),
    url,
    color: event === "pull_request" ? 0x7dd3fc : 0x06b6d4,
    timestamp: new Date().toISOString(),
    footer: {
      text: "Queen.js Federation Hub",
    },
  };
}

/**
 * Central GitHub webhook receiver
 */
app.post(
  "/webhook/github",
  async (req: Request & { rawBody?: string }, res: Response) => {
    // In production, require webhook secret for security
    if (isProduction && !config.webhookSecret) {
      console.error("❌ GITHUB_WEBHOOK_SECRET is required in production");
      return res.status(500).json({ error: "Server configuration error" });
    }

    // Verify signature if secret is configured
    if (config.webhookSecret) {
      const signature = req.get("x-hub-signature-256") || "";
      if (!verifyWebhookSignature(req.rawBody || "", signature, config.webhookSecret)) {
        console.log("⚠️ Invalid webhook signature");
        return res.status(401).json({ error: "Invalid signature" });
      }
    } else {
      console.warn("⚠️ Webhook signature verification disabled (no secret configured)");
    }

    const event = req.get("x-github-event") || "unknown";
    const payload = req.body as Record<string, unknown>;
    const repository = payload.repository as { full_name?: string };
    const organization = payload.organization as { login?: string };
    const repositoryOwner = (payload.repository as { owner?: { login?: string } })
      ?.owner;

    const repo = repository?.full_name || "unknown";
    const org = organization?.login || repositoryOwner?.login || "unknown";

    console.log(`📨 GitHub ${event} from ${repo} (org: ${org})`);

    // Get routing configuration for this organization
    const route = config.organizations[org] || {
      nats_prefix: "unknown",
      discord_channel: "#github-general",
    };

    try {
      // Publish to NATS with org-specific subject
      await natsClient.publish(
        `${route.nats_prefix}.github.${event}`,
        JSON.stringify({
          event,
          repo,
          org,
          payload,
          timestamp: new Date().toISOString(),
        })
      );

      // Route to appropriate Discord channel
      await natsClient.publish(
        "discord.notify",
        JSON.stringify({
          channel: route.discord_channel,
          message: formatDiscordMessage(event, payload),
          embed: createEmbed(event, payload),
        })
      );

      // Special handling for PRs - notify SovereignPRManager
      if (event === "pull_request") {
        const pr = payload.pull_request as { number?: number };
        await natsClient.publish(
          "sovereignprmanager.review",
          JSON.stringify({
            org,
            repo,
            pr_number: pr?.number,
            action: payload.action,
          })
        );
      }

      res.status(200).json({
        status: "received",
        routed_to: route.nats_prefix,
        queen: "acknowledged",
      });
    } catch (error) {
      console.error("Error processing webhook:", error);
      res.status(500).json({ error: "Internal processing error" });
    }
  }
);

/**
 * Zapier webhook endpoint
 */
app.post("/webhook/zapier", async (req: Request, res: Response) => {
  try {
    await natsClient.publish("zapier.event", JSON.stringify(req.body));
    res.status(200).json({ status: "received" });
  } catch (error) {
    console.error("Error processing Zapier webhook:", error);
    res.status(500).json({ error: "Internal processing error" });
  }
});

/**
 * SwarmGate paycheck detection endpoint
 */
app.post("/webhook/swarmgate/paycheck", async (req: Request, res: Response) => {
  const { amount, source } = req.body as { amount?: number; source?: string };

  if (typeof amount !== "number" || amount <= 0) {
    return res.status(400).json({ error: "Invalid amount" });
  }

  // Calculate 7% allocation
  const allocation = amount * 0.07;

  try {
    await natsClient.publish(
      "swarmgate.paycheck.detected",
      JSON.stringify({
        amount,
        allocation,
        source: source || "unknown",
        timestamp: new Date().toISOString(),
      })
    );

    await natsClient.publish(
      "treasury.deposit",
      JSON.stringify({
        amount: allocation,
        source: "swarmgate_7%",
      })
    );

    await natsClient.publish(
      "discord.notify",
      JSON.stringify({
        channel: "#financial",
        message: `💰 Paycheck detected: $${amount.toFixed(2)} → 7% allocation: $${allocation.toFixed(2)}`,
      })
    );

    res.status(200).json({
      status: "processed",
      allocated: allocation,
    });
  } catch (error) {
    console.error("Error processing paycheck webhook:", error);
    res.status(500).json({ error: "Internal processing error" });
  }
});

/**
 * Health check endpoint
 */
app.get("/health", (_req: Request, res: Response) => {
  res.json({
    status: "operational",
    service: "Queen.js Federation Hub",
    sovereignty: "100%",
    uptime: process.uptime(),
    nats_connected: natsClient.connected,
    organizations_monitored: Object.keys(config.organizations),
  });
});

/**
 * API info endpoint
 */
app.get("/", (_req: Request, res: Response) => {
  res.json({
    name: "Queen.js Federation Hub",
    version: "1.0.0",
    description: "Central webhook coordinator for multi-org GitHub federation",
    endpoints: {
      "/webhook/github": "Central GitHub webhook receiver",
      "/webhook/zapier": "Zapier integration webhook",
      "/webhook/swarmgate/paycheck": "SwarmGate paycheck detection",
      "/health": "Health check endpoint",
    },
    architecture: {
      pattern: "Federation (not consolidation)",
      benefit: "Keep orgs separate, one webhook URL for everything",
      cost: "$0 vs GitHub Enterprise $756/year",
    },
  });
});

// Error handling middleware
app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error("Unhandled error:", err);
  res.status(500).json({ error: "Internal server error" });
});

/**
 * Initialize and start the Queen.js Federation Hub
 */
export function startQueen(customConfig?: Partial<QueenConfig>): void {
  if (customConfig) {
    config = { ...config, ...customConfig };
  }

  const PORT = config.port;
  app.listen(PORT, () => {
    console.log(`👑 Queen.js Federation Hub listening on port ${PORT}`);
    console.log(`🎯 Central webhook: /webhook/github`);
    console.log(`💰 SwarmGate: /webhook/swarmgate/paycheck`);
    console.log(`⚡ Zapier: /webhook/zapier`);
    console.log(`🏥 Health: /health`);
    console.log(`🏛️ Organizations monitored: ${Object.keys(config.organizations).join(", ")}`);
  });
}

/**
 * Set custom NATS client (for testing or real NATS connection)
 */
export function setNATSClient(client: NATSClient): void {
  natsClient = client;
}

/**
 * Get the Express app instance (for testing)
 */
export function getApp() {
  return app;
}

// Start server if this is the main module
// Note: In ESM context, use import.meta.url for module detection
// For CommonJS compatibility, we also check process.argv
const moduleUrl = typeof import.meta !== 'undefined' ? import.meta.url : '';
const isMainModule = moduleUrl.endsWith('queen/server.js') || 
                     moduleUrl.endsWith('queen/server.ts') ||
                     process.argv[1]?.includes("queen/server");
if (isMainModule) {
  startQueen();
}
