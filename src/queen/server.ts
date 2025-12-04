import express, { Request, Response, NextFunction } from "express";
import crypto from "crypto";
import { connect, NatsConnection, StringCodec } from "nats";

// Queen.js Webhook Receiver
// Central coordinator for the Sovereignty Architecture swarm
// Routes webhooks from GitHub, Zapier, and SwarmGate to NATS message bus

interface QueenConfig {
  port: number;
  natsUrl: string;
  githubWebhookSecret?: string;
  rateLimitWindowMs?: number;
  rateLimitMaxRequests?: number;
}

interface HealthResponse {
  status: string;
  service: string;
  sovereignty: string;
  uptime: number;
  natsConnected: boolean;
}

interface WebhookResponse {
  status: string;
  queen: string;
  timestamp?: string;
  amount?: number;
}

interface RateLimitEntry {
  count: number;
  resetTime: number;
}

let nc: NatsConnection | null = null;
const sc = StringCodec();

// Simple in-memory rate limiter
const rateLimitStore = new Map<string, RateLimitEntry>();

function createRateLimiter(windowMs: number, maxRequests: number) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const ip = req.ip || req.socket.remoteAddress || "unknown";
    const now = Date.now();
    
    let entry = rateLimitStore.get(ip);
    
    if (!entry || now > entry.resetTime) {
      // Create new entry or reset expired one
      entry = { count: 1, resetTime: now + windowMs };
      rateLimitStore.set(ip, entry);
    } else {
      entry.count++;
    }
    
    if (entry.count > maxRequests) {
      res.status(429).json({ 
        error: "Too many requests", 
        retryAfter: Math.ceil((entry.resetTime - now) / 1000) 
      });
      return;
    }
    
    next();
  };
}

// Clean up expired entries periodically
setInterval(() => {
  const now = Date.now();
  for (const [ip, entry] of rateLimitStore.entries()) {
    if (now > entry.resetTime) {
      rateLimitStore.delete(ip);
    }
  }
}, 60000); // Clean up every minute

// Verify GitHub webhook signature
function verifyGitHubSignature(secret: string, payload: string, signature: string): boolean {
  if (!secret || !signature) return !secret; // If no secret configured, allow (for dev)
  const hmac = crypto.createHmac("sha256", secret);
  hmac.update(payload);
  const expected = `sha256=${hmac.digest("hex")}`;
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
}

// Publish message to NATS
async function publishToNats(subject: string, data: unknown): Promise<void> {
  if (!nc) {
    console.warn(`⚠️ NATS not connected, skipping publish to ${subject}`);
    return;
  }
  const jsonData = typeof data === "string" ? data : JSON.stringify(data);
  nc.publish(subject, sc.encode(jsonData));
  console.log(`📡 Published to ${subject}`);
}

export async function createQueenServer(config: QueenConfig): Promise<express.Application> {
  const app = express();

  // Rate limiting configuration (default: 100 requests per minute per IP)
  const windowMs = config.rateLimitWindowMs || 60000;
  const maxRequests = config.rateLimitMaxRequests || 100;
  const rateLimiter = createRateLimiter(windowMs, maxRequests);

  // Apply rate limiting to all webhook routes
  app.use("/webhook", rateLimiter);

  // Parse JSON with raw body preservation for signature verification
  app.use(express.json({
    verify: (req: Request & { rawBody?: string }, _res, buf) => {
      req.rawBody = buf.toString();
    }
  }));

  // Connect to NATS
  try {
    nc = await connect({ servers: config.natsUrl });
    console.log(`👑 Queen connected to NATS at ${config.natsUrl}`);
  } catch (err) {
    console.warn(`⚠️ NATS connection failed: ${err}. Queen will operate without message bus.`);
  }

  // Health check endpoint
  app.get("/health", (_req: Request, res: Response) => {
    const response: HealthResponse = {
      status: "operational",
      service: "Queen.js Webhook Receiver",
      sovereignty: "100%",
      uptime: process.uptime(),
      natsConnected: nc !== null && !nc.isClosed()
    };
    res.json(response);
  });

  // GitHub webhook receiver
  app.post("/webhook/github", async (req: Request & { rawBody?: string }, res: Response) => {
    console.log("📨 GitHub webhook received");

    // Verify signature if secret is configured
    const signature = req.get("X-Hub-Signature-256") || "";
    if (config.githubWebhookSecret && req.rawBody) {
      if (!verifyGitHubSignature(config.githubWebhookSecret, req.rawBody, signature)) {
        return res.status(401).json({ error: "Invalid signature" });
      }
    }

    // Extract event metadata
    const event = req.get("X-GitHub-Event") || "unknown";
    const deliveryId = req.get("X-GitHub-Delivery") || "";
    const repo = req.body.repository?.full_name || "unknown";

    // Publish to NATS for Legion processing
    await publishToNats("github.webhook", {
      event,
      repo,
      deliveryId,
      payload: req.body,
      timestamp: new Date().toISOString()
    });

    // Route to Discord notifications
    await publishToNats("discord.notify", {
      channel: "#github",
      message: `📦 GitHub ${event} on ${repo}`,
      data: req.body
    });

    const response: WebhookResponse = { status: "received", queen: "acknowledged" };
    res.status(200).json(response);
  });

  // Zapier webhook receiver
  app.post("/webhook/zapier", async (req: Request, res: Response) => {
    console.log("⚡ Zapier webhook received");

    await publishToNats("zapier.event", {
      payload: req.body,
      timestamp: new Date().toISOString()
    });

    const response: WebhookResponse = { status: "received", queen: "acknowledged" };
    res.status(200).json(response);
  });

  // SwarmGate deposit receiver
  app.post("/webhook/swarmgate", async (req: Request, res: Response) => {
    const { amount, source } = req.body;

    console.log(`💰 SwarmGate deposit: $${amount || 0} from ${source || "unknown"}`);

    // Forward to ValorYield API
    await publishToNats("valoryield.deposit", {
      amount,
      source,
      timestamp: new Date().toISOString()
    });

    const response: WebhookResponse = {
      status: "deposited",
      amount,
      queen: "acknowledged"
    };
    res.status(200).json(response);
  });

  // Generic webhook receiver for any source
  app.post("/webhook/:source", async (req: Request, res: Response) => {
    const source = req.params.source;

    console.log(`📡 Webhook from ${source}`);

    await publishToNats(`webhook.${source}`, {
      source,
      payload: req.body,
      timestamp: new Date().toISOString()
    });

    const response: WebhookResponse = { status: "received", queen: "acknowledged" };
    res.status(200).json(response);
  });

  // Error handling middleware
  app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
    console.error("❌ Queen error:", err.message);
    res.status(500).json({ error: "Internal server error", queen: "error" });
  });

  return app;
}

export async function startQueenServer(config: QueenConfig): Promise<void> {
  const app = await createQueenServer(config);

  app.listen(config.port, () => {
    console.log(`👑 Queen.js listening on port ${config.port}`);
    console.log(`🎯 Webhook endpoints:`);
    console.log(`   POST /webhook/github`);
    console.log(`   POST /webhook/zapier`);
    console.log(`   POST /webhook/swarmgate`);
    console.log(`   POST /webhook/:source (generic)`);
    console.log(`   GET  /health`);
  });
}

// Graceful shutdown
export async function shutdownQueen(): Promise<void> {
  if (nc) {
    await nc.drain();
    console.log("👑 Queen disconnected from NATS");
  }
}
