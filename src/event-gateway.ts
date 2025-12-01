import express from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { HealthBot } from "./council/health-bot.js";

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

// Initialize Health Bot
const healthBot = new HealthBot({
  services: [
    { name: "Discord Gateway", url: "https://discord.com/api/v10/gateway" },
    { name: "Event Gateway", checkFn: async () => true },
    { name: "Control API", url: cfg.control_api?.base_url ? `${cfg.control_api.base_url}/health` : undefined }
  ],
  discordToken: env("DISCORD_TOKEN", false),
  alertChannelId: process.env.ALERTS_CHANNEL_ID,
  healthCheckInterval: 60000 // 1 minute
});

// Mount health routes
app.use("/", healthBot.createRoutes());

// GitHub webhook routes
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));

// Council route for board receipts
app.post("/webhooks/council", async (req, res) => {
  const { type, data } = req.body;
  
  if (type === "board_receipt" && channelIds.prs) {
    try {
      await rest.post(`/channels/${channelIds.prs}/messages`, {
        body: {
          embeds: [{
            title: `📜 ${data.title}`,
            description: data.description,
            color: 0x9B59B6, // Council purple
            timestamp: new Date().toISOString(),
            fields: [
              { name: "Quadrant", value: data.quadrant, inline: true },
              { name: "Author", value: data.author, inline: true }
            ]
          }]
        }
      });
      res.json({ status: "ok", message: "Board receipt posted" });
    } catch (error) {
      res.status(500).json({ status: "error", message: String(error) });
    }
  } else {
    res.status(400).json({ status: "error", message: "Invalid webhook type" });
  }
});

const port = Number(process.env.PORT || cfg.event_gateway?.port || 3001);

// Wake the health bot on startup
healthBot.wake();

app.listen(port, () => {
  console.log(`🚀 Event gateway on :${port}`);
  console.log(`🏥 Health endpoints: /health, /health/detailed, /ready, /live`);
  console.log(`🌅 Wake endpoint: POST /wake`);
});