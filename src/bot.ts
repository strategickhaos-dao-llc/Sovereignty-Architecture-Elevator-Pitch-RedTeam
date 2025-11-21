import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed } from "./discord.js";
import { env, loadConfig } from "./config.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// Helper function to make API calls with timeout
const fetchWithTimeout = async (url: string, options: RequestInit, timeoutMs: number = 10000) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(timeoutId);
    return response;
  } catch (error: any) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error(`Request timeout after ${timeoutMs}ms`);
    }
    throw error;
  }
};

client.once("ready", async () => {
  await registerCommands(token, appId);
  console.log("Bot ready");
});

client.on("interactionCreate", async (i: Interaction) => {
  if (!i.isChatInputCommand()) return;
  
  // Defer reply for long-running commands
  await i.deferReply();
  
  try {
    const authHeader = { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` };
    
    if (i.commandName === "status") {
      const svc = i.options.getString("service", true);
      const r = await fetchWithTimeout(
        `${cfg.control_api.base_url}/status/${svc}`,
        { headers: authHeader },
        5000
      ).then(r => r.json());
      await i.editReply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const r = await fetchWithTimeout(
        `${cfg.control_api.base_url}/logs/${svc}?tail=${tail}`,
        { headers: authHeader },
        8000
      ).then(r => r.text());
      await i.editReply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const r = await fetchWithTimeout(
        `${cfg.control_api.base_url}/deploy`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json", ...authHeader },
          body: JSON.stringify({ env: envName, tag })
        },
        30000  // 30s for deployment
      ).then(r => r.json());
      await i.editReply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      const r = await fetchWithTimeout(
        `${cfg.control_api.base_url}/scale`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json", ...authHeader },
          body: JSON.stringify({ service: svc, replicas })
        },
        15000  // 15s for scaling
      ).then(r => r.json());
      await i.editReply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
    }
  } catch (e: any) {
    const errorMsg = `Error: ${e.message}`;
    console.error(`Command failed: ${i.commandName}`, e);
    await i.editReply({ content: errorMsg }).catch(() => 
      i.followUp({ content: errorMsg, ephemeral: true })
    );
  }
});

client.login(token);