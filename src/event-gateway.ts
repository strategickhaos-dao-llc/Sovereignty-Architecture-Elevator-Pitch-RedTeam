import express from "express";
import type { Request, Response, NextFunction } from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { satelliteRoutes } from "./routes/satellite.js";

const cfg = loadConfig();
const app = express();

// Simple in-memory rate limiter
const rateLimitStore = new Map<string, { count: number; resetTime: number }>();
const RATE_LIMIT_WINDOW_MS = 60000; // 1 minute
const RATE_LIMIT_MAX_REQUESTS = 100; // 100 requests per minute

function rateLimit(req: Request, res: Response, next: NextFunction) {
  const clientKey = req.ip || req.get("X-Forwarded-For") || "unknown";
  const now = Date.now();
  
  const clientData = rateLimitStore.get(clientKey);
  
  if (!clientData || now > clientData.resetTime) {
    rateLimitStore.set(clientKey, { count: 1, resetTime: now + RATE_LIMIT_WINDOW_MS });
    return next();
  }
  
  if (clientData.count >= RATE_LIMIT_MAX_REQUESTS) {
    res.setHeader("X-RateLimit-Limit", RATE_LIMIT_MAX_REQUESTS);
    res.setHeader("X-RateLimit-Remaining", 0);
    res.setHeader("X-RateLimit-Reset", Math.ceil(clientData.resetTime / 1000));
    return res.status(429).json({ error: "Rate limit exceeded", retryAfter: Math.ceil((clientData.resetTime - now) / 1000) });
  }
  
  clientData.count++;
  res.setHeader("X-RateLimit-Limit", RATE_LIMIT_MAX_REQUESTS);
  res.setHeader("X-RateLimit-Remaining", RATE_LIMIT_MAX_REQUESTS - clientData.count);
  res.setHeader("X-RateLimit-Reset", Math.ceil(clientData.resetTime / 1000));
  next();
}

// Clean up expired entries periodically
setInterval(() => {
  const now = Date.now();
  for (const [key, data] of rateLimitStore.entries()) {
    if (now > data.resetTime) {
      rateLimitStore.delete(key);
    }
  }
}, RATE_LIMIT_WINDOW_MS);

// keep raw for signature
app.use(bodyParser.json({
  verify: (req: any, _res, buf) => { req.rawBody = buf.toString(); }
}));

const rest = new REST({ version: "10" }).setToken(env("DISCORD_TOKEN"));

const channelIds = {
  prs: process.env.PRS_CHANNEL_ID!,
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID!,
  alerts: process.env.ALERTS_CHANNEL_ID!,
  status: process.env.STATUS_CHANNEL_ID!,
  agents: process.env.AGENTS_CHANNEL_ID!
};

// GitHub webhook routes
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));

// Satellite connectivity routes (Starlink/Direct-to-Cell)
// SECURITY: Use a dedicated SATELLITE_RELAY_SECRET in production.
// Fallback to GITHUB_WEBHOOK_SECRET is provided for development only.
const satSecret = env("SATELLITE_RELAY_SECRET", false) || env("GITHUB_WEBHOOK_SECRET");
if (!process.env.SATELLITE_RELAY_SECRET) {
  console.warn("⚠️  SATELLITE_RELAY_SECRET not set, using GITHUB_WEBHOOK_SECRET as fallback");
}
const satRoutes = satelliteRoutes(rest, channelIds, satSecret);

// Apply rate limiting to satellite routes that perform authorization
app.get("/satellite/status", satRoutes.status);
app.get("/satellite/health", satRoutes.health);
app.get("/satellite/queue", satRoutes.queue);
app.post("/satellite/relay", rateLimit, satRoutes.relay);
app.post("/satellite/failover", rateLimit, satRoutes.failover);
app.post("/satellite/heartbeat", rateLimit, satRoutes.heartbeat);
app.post("/satellite/direct-to-cell", rateLimit, satRoutes.directToCell);

// Health check endpoints
app.get("/health", (_req, res) => res.json({ status: "healthy", service: "event-gateway" }));
app.get("/metrics/satellite", satRoutes.status);

const port = Number(process.env.PORT || cfg.event_gateway.port || 3001);
app.listen(port, () => console.log(`Event gateway on :${port} with satellite relay enabled`));