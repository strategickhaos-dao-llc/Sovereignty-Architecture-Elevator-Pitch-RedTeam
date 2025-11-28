import express from "express";
import bodyParser from "body-parser";
import rateLimit from "express-rate-limit";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { verifyWebhook, initReplayProtection } from "./verify_hmac.js";

// Initialize replay protection
initReplayProtection();

const cfg = loadConfig() as any;
const app = express();

// keep raw for signature
app.use(bodyParser.json({
  verify: (req: any, _res, buf) => { req.rawBody = buf.toString(); }
}));

// Rate limiting configuration from discovery.yml or defaults
const rateLimitConfig = cfg.discord?.bot?.rate_limits || {
  max_msgs_per_min: 30,
  burst: 10
};

// Rate limiter for webhook endpoints
const webhookLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: rateLimitConfig.max_msgs_per_min,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: "Too many requests, please try again later" }
});

// Stricter rate limiter for alert endpoints (prevent alert fatigue attacks)
const alertLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: rateLimitConfig.burst * 10, // 100 alerts per minute max
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: "Alert rate limit exceeded" }
});

const rest = new REST({ version: "10" }).setToken(env("DISCORD_TOKEN"));

const channelIds = {
  prs: process.env.PRS_CHANNEL_ID!,
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID!,
  alerts: process.env.ALERTS_CHANNEL_ID!,
  recon: process.env.RECON_CHANNEL_ID!
};

// Health check endpoint (no rate limiting needed)
app.get("/health", (_req, res) => {
  res.json({ status: "healthy", timestamp: new Date().toISOString() });
});

// Ready check endpoint (no rate limiting needed)
app.get("/ready", (_req, res) => {
  res.json({ status: "ready", timestamp: new Date().toISOString() });
});

// GitHub webhook endpoint with enhanced HMAC + replay protection
app.post("/webhooks/github", webhookLimiter, (req, res, next) => {
  const secret = env("GITHUB_WEBHOOK_SECRET");
  const signature = req.get("X-Hub-Signature-256") || "";
  const deliveryId = req.get("X-GitHub-Delivery") || "";
  // Use current time as timestamp (GitHub doesn't provide timestamp in headers)
  const timestamp = Date.now();
  
  const result = verifyWebhook({
    secret,
    payload: (req as any).rawBody || "",
    signature,
    nonce: deliveryId,  // Use GitHub delivery ID as nonce for replay protection
    timestamp,
    algorithm: "sha256"
  });
  
  if (!result.valid) {
    console.warn(`GitHub webhook verification failed: ${result.error}`);
    return res.status(401).json({ error: result.error });
  }
  
  next();
}, githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));

// Discord webhook endpoint (for inbound Discord events)
app.post("/webhooks/discord", webhookLimiter, (req, res) => {
  const secret = env("DISCORD_WEBHOOK_SECRET", false) || env("EVENTS_HMAC_KEY");
  const signature = req.get("X-Sig") || req.get("X-Discord-Signature") || "";
  const timestamp = req.get("X-Timestamp") || "";
  const nonce = req.get("X-Nonce") || "";
  
  const result = verifyWebhook({
    secret,
    payload: (req as any).rawBody || "",
    signature,
    timestamp,
    nonce,
    algorithm: "sha256"
  });
  
  if (!result.valid) {
    console.warn(`Discord webhook verification failed: ${result.error}`);
    return res.status(401).json({ error: result.error });
  }
  
  // Process Discord event
  const payload = req.body;
  console.log("Discord event received:", payload.type);
  
  res.json({ status: "ok" });
});

// Alert endpoint (from Alertmanager)
app.post("/alert", alertLimiter, async (req, res) => {
  const secret = env("EVENTS_HMAC_KEY", false) || "";
  
  // Verify HMAC if secret is configured
  if (secret) {
    const signature = req.get("X-Sig") || "";
    const result = verifyWebhook({
      secret,
      payload: (req as any).rawBody || "",
      signature,
      algorithm: "sha256"
    });
    
    if (!result.valid) {
      console.warn(`Alert webhook verification failed: ${result.error}`);
      return res.status(401).json({ error: result.error });
    }
  }
  
  // Forward alert to Discord #alerts channel
  const payload = req.body;
  try {
    if (channelIds.alerts) {
      const alerts = payload.alerts || [payload];
      for (const alert of alerts) {
        const severity = alert.labels?.severity || "unknown";
        const color = severity === "critical" ? 0xff0000 : severity === "warning" ? 0xffaa00 : 0x2f81f7;
        
        await rest.post(`/channels/${channelIds.alerts}/messages`, {
          body: {
            embeds: [{
              title: `🚨 ${alert.labels?.alertname || "Alert"}`,
              description: alert.annotations?.description || alert.annotations?.summary || "No description",
              color,
              fields: [
                { name: "Severity", value: severity, inline: true },
                { name: "Service", value: alert.labels?.service || "N/A", inline: true },
                { name: "Status", value: alert.status || "firing", inline: true }
              ],
              footer: alert.annotations?.runbook_url ? { text: `Runbook: ${alert.annotations.runbook_url}` } : undefined
            }]
          }
        } as any);
      }
    }
    res.json({ status: "ok", processed: payload.alerts?.length || 1 });
  } catch (error: any) {
    console.error("Failed to post alert to Discord:", error);
    res.status(500).json({ error: error.message });
  }
});

// Generic event endpoint
app.post("/event", webhookLimiter, (req, res) => {
  const secret = env("EVENTS_HMAC_KEY");
  const signature = req.get("X-Sig") || "";
  const timestamp = req.get("X-Timestamp") || "";
  const nonce = req.get("X-Nonce") || "";
  
  const result = verifyWebhook({
    secret,
    payload: (req as any).rawBody || "",
    signature,
    timestamp,
    nonce,
    algorithm: "sha256"
  });
  
  if (!result.valid) {
    console.warn(`Event webhook verification failed: ${result.error}`);
    return res.status(401).json({ error: result.error });
  }
  
  // Process event
  const payload = req.body;
  console.log("Event received:", payload.type);
  
  res.json({ status: "ok" });
});

const port = Number(process.env.PORT || cfg.event_gateway?.port || 3001);
app.listen(port, () => console.log(`Event gateway on :${port}`));