import express from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { azurePipelineRoutes } from "./routes/azure-pipeline.js";

const cfg = loadConfig();
const app = express();

// Simple in-memory rate limiter
const rateLimitWindow = 60 * 1000; // 1 minute
const maxRequestsPerWindow = 60; // 60 requests per minute
const requestCounts = new Map<string, { count: number; resetTime: number }>();

function rateLimit(req: express.Request, res: express.Response, next: express.NextFunction) {
  const clientIp = req.ip || req.socket.remoteAddress || "unknown";
  const now = Date.now();
  
  const clientData = requestCounts.get(clientIp);
  
  if (!clientData || now > clientData.resetTime) {
    requestCounts.set(clientIp, { count: 1, resetTime: now + rateLimitWindow });
    return next();
  }
  
  if (clientData.count >= maxRequestsPerWindow) {
    return res.status(429).json({ 
      error: "Too many requests", 
      retryAfter: Math.ceil((clientData.resetTime - now) / 1000) 
    });
  }
  
  clientData.count++;
  return next();
}

// Clean up old rate limit entries periodically
setInterval(() => {
  const now = Date.now();
  for (const [ip, data] of requestCounts.entries()) {
    if (now > data.resetTime) {
      requestCounts.delete(ip);
    }
  }
}, 60000);

// keep raw for signature
app.use(bodyParser.json({
  verify: (req: any, _res, buf) => { req.rawBody = buf.toString(); }
}));

// Apply rate limiting to all routes
app.use(rateLimit);

const rest = new REST({ version: "10" }).setToken(env("DISCORD_TOKEN"));

const channelIds = {
  prs: process.env.PRS_CHANNEL_ID!,
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID!,
  alerts: process.env.ALERTS_CHANNEL_ID!
};

// GitHub webhook route
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));

// Azure Pipeline webhook route for build failure notifications
// EVENTS_HMAC_KEY is optional - signature verification is disabled if not set
const eventsHmacKey = env("EVENTS_HMAC_KEY", false);
if (!eventsHmacKey) {
  console.warn("EVENTS_HMAC_KEY not set - Azure pipeline webhook signature verification disabled");
}
app.post("/azure-pipeline", azurePipelineRoutes(rest, channelIds, eventsHmacKey));

// Health check endpoint
app.get("/health", (_req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

const port = Number(process.env.PORT || cfg.event_gateway.port || 3001);
app.listen(port, () => console.log(`Event gateway on :${port}`));