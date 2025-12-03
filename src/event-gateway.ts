import express, { Request } from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";

interface RequestWithRawBody extends Request {
  rawBody?: string;
}

const cfg = loadConfig();
const app = express();

// keep raw for signature verification
app.use(bodyParser.json({
  verify: (req: RequestWithRawBody, _res, buf) => { req.rawBody = buf.toString(); }
}));

const rest = new REST({ version: "10" }).setToken(env("DISCORD_TOKEN"));

const channelIds = {
  prs: process.env.PRS_CHANNEL_ID || "",
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID || "",
  alerts: process.env.ALERTS_CHANNEL_ID || ""
};

// Health check endpoint
app.get("/health", (_req, res) => res.send("ok"));

// GitHub webhook endpoint
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET", false)));

// Generic event endpoint for internal services (HMAC verified)
app.post("/event", (req: RequestWithRawBody, res) => {
  // Verify HMAC signature for internal events
  const sig = req.get("X-Sig") || "";
  const hmacKey = env("EVENTS_HMAC_KEY", false);
  if (hmacKey && sig) {
    const crypto = require("crypto");
    const expectedSig = crypto.createHmac("sha256", hmacKey).update(req.rawBody || "").digest("hex");
    if (sig !== expectedSig) {
      return res.status(401).send("Invalid signature");
    }
  }
  // Process the event (log for now)
  console.log("Received event:", req.body);
  res.send("ok");
});

// Alert endpoint for Alertmanager
app.post("/alert", (req, res) => {
  console.log("Received alert:", req.body);
  res.send("ok");
});

const port = Number(process.env.PORT || 3001);
app.listen(port, () => console.log(`Event gateway on :${port}`));