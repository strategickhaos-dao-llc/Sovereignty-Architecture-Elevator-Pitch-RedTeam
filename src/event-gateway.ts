import express from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { createChronicleRoutes } from "./chronicle/index.js";

const cfg = loadConfig();
const app = express();

// keep raw for signature
app.use(bodyParser.json({
  verify: (req: any, _res, buf) => { req.rawBody = buf.toString(); }
}));

const rest = new REST({ version: "10" }).setToken(env("DISCORD_TOKEN"));

const channelIds = {
  prs: process.env.PRS_CHANNEL_ID!,
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID!,
  alerts: process.env.ALERTS_CHANNEL_ID!
};

// GitHub webhook routes
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));

// Chronicle API routes (Sovereign Architect's Chronicle)
const chronicleRouter = express.Router();
createChronicleRoutes(chronicleRouter);
app.use("/api", chronicleRouter);

// Health check endpoint
app.get("/health", (_req, res) => {
  res.json({ status: "healthy", service: "event-gateway", chronicle: "enabled" });
});

const port = Number(process.env.PORT || cfg.event_gateway.port || 3001);
app.listen(port, () => console.log(`Event gateway on :${port} - Chronicle API available at /api/chronicle`));