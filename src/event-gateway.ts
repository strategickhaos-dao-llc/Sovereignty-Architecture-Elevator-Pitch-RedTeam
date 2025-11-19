import express from "express";
import bodyParser from "body-parser";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";

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

app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));

// Grok-powered webhook tester for realistic test payloads
app.post("/grok-test", async (req, res) => {
  try {
    const xaiApiKey = process.env.XAI_API_KEY;
    if (!xaiApiKey) {
      return res.status(400).json({ 
        error: "XAI_API_KEY not configured",
        hint: "Set XAI_API_KEY environment variable to use Grok-powered webhook generation"
      });
    }

    // Get custom prompt from request body or use default
    const customPrompt = req.body?.prompt || "Generate a fake GitHub webhook payload for a new PR titled 'Add sovereignty architecture'";
    
    const response = await fetch("https://api.x.ai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${xaiApiKey}`
      },
      body: JSON.stringify({
        model: "grok-beta",
        messages: [
          {
            role: "system",
            content: "You are a helpful assistant that generates realistic GitHub webhook payloads. Return ONLY valid JSON, no markdown or explanations."
          },
          {
            role: "user",
            content: customPrompt
          }
        ],
        temperature: 0.7
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      return res.status(response.status).json({ 
        error: "Grok API error", 
        details: errorText 
      });
    }

    const data = await response.json();
    const generatedContent = data.choices[0]?.message?.content || "{}";
    
    // Try to parse the JSON response
    try {
      const payload = JSON.parse(generatedContent);
      res.json({
        success: true,
        payload,
        meta: {
          model: data.model,
          usage: data.usage
        }
      });
    } catch (parseError) {
      // If not valid JSON, return the raw content
      res.json({
        success: false,
        rawContent: generatedContent,
        error: "Generated content is not valid JSON"
      });
    }
  } catch (error: any) {
    res.status(500).json({ 
      error: "Internal server error", 
      message: error.message 
    });
  }
});

// Health check endpoint
app.get("/health", (_req, res) => {
  res.json({ 
    status: "ok", 
    timestamp: new Date().toISOString(),
    features: {
      webhooks: true,
      grokTest: !!process.env.XAI_API_KEY
    }
  });
});

const port = Number(process.env.PORT || cfg.event_gateway.port || 3001);
app.listen(port, () => console.log(`Event gateway on :${port}`));