import express from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { azurePipelineRoutes } from "./routes/azure-pipeline.js";
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
    alerts: process.env.ALERTS_CHANNEL_ID
};
// GitHub webhook route
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));
// Azure Pipeline webhook route for build failure notifications
app.post("/azure-pipeline", azurePipelineRoutes(rest, channelIds, env("EVENTS_HMAC_KEY", false) || ""));
// Health check endpoint
app.get("/health", (_req, res) => {
    res.json({ status: "ok", timestamp: new Date().toISOString() });
});
const port = Number(process.env.PORT || cfg.event_gateway.port || 3001);
app.listen(port, () => console.log(`Event gateway on :${port}`));
