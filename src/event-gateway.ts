import express from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { immuneRoutes } from "./routes/immune.js";

const cfg = loadConfig();
const app = express();

// keep raw for signature
app.use(bodyParser.json({
  verify: (req: express.Request & { rawBody?: string }, _res, buf) => { req.rawBody = buf.toString(); }
}));

const rest = new REST({ version: "10" }).setToken(env("DISCORD_TOKEN"));

const channelIds = {
  prs: process.env.PRS_CHANNEL_ID!,
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID!,
  alerts: process.env.ALERTS_CHANNEL_ID!
};

const immuneChannelIds = {
  immune_response: process.env.IMMUNE_RESPONSE_CHANNEL_ID || "",
  swarm_health: process.env.SWARM_HEALTH_CHANNEL_ID || ""
};

// GitHub webhook routes
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));

// Immune system webhook routes
app.post("/webhooks/immune", immuneRoutes(rest, immuneChannelIds, env("IMMUNE_WEBHOOK_SECRET", false)));

// Health check endpoint
app.get("/health", (_req, res) => {
  res.json({
    status: "healthy",
    service: "event-gateway",
    version: "1.0.0",
    timestamp: new Date().toISOString()
  });
});

// Ready check endpoint
app.get("/ready", (_req, res) => {
  res.json({
    ready: true,
    discord: !!process.env.DISCORD_TOKEN,
    github: !!process.env.GITHUB_WEBHOOK_SECRET,
    immune: !!immuneChannelIds.immune_response
  });
});

const port = Number(process.env.PORT || cfg.event_gateway?.port || 3001);
app.listen(port, () => {
  console.log(`Event gateway on :${port}`);
  console.log(`Immune webhook: ${immuneChannelIds.immune_response ? "enabled" : "not configured"}`);
});