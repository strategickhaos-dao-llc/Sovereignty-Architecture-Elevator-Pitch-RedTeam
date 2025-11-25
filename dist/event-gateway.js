import express from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { satelliteRoutes } from "./routes/satellite.js";
const cfg = loadConfig();
const app = express();
// keep raw for signature
app.use(bodyParser.json({
    verify: (req, _res, buf) => { req.rawBody = buf.toString(); }
}));
const rest = new REST({ version: "10" }).setToken(env("DISCORD_TOKEN"));
const channelIds = {
    prs: process.env.PRS_CHANNEL_ID,
    deployments: process.env.DEPLOYMENTS_CHANNEL_ID,
    alerts: process.env.ALERTS_CHANNEL_ID,
    status: process.env.STATUS_CHANNEL_ID,
    agents: process.env.AGENTS_CHANNEL_ID
};
// GitHub webhook routes
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));
// Satellite connectivity routes (Starlink/Direct-to-Cell)
const satSecret = env("SATELLITE_RELAY_SECRET", false) || env("GITHUB_WEBHOOK_SECRET");
const satRoutes = satelliteRoutes(rest, channelIds, satSecret);
app.get("/satellite/status", satRoutes.status);
app.get("/satellite/health", satRoutes.health);
app.get("/satellite/queue", satRoutes.queue);
app.post("/satellite/relay", satRoutes.relay);
app.post("/satellite/failover", satRoutes.failover);
app.post("/satellite/heartbeat", satRoutes.heartbeat);
app.post("/satellite/direct-to-cell", satRoutes.directToCell);
// Health check endpoints
app.get("/health", (_req, res) => res.json({ status: "healthy", service: "event-gateway" }));
app.get("/metrics/satellite", satRoutes.status);
const port = Number(process.env.PORT || cfg.event_gateway.port || 3001);
app.listen(port, () => console.log(`Event gateway on :${port} with satellite relay enabled`));
