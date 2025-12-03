import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed } from "./discord.js";
import { env, loadConfig } from "./config.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

// Get control API config from infra section
const controlApi = cfg.infra.control_api;
const controlApiToken = env("CONTROL_API_TOKEN", false);

// Build headers with optional authorization
function buildHeaders(includeAuth: boolean = true): Record<string, string> {
  const headers: Record<string, string> = {};
  if (includeAuth && controlApiToken) {
    headers.Authorization = `Bearer ${controlApiToken}`;
  }
  return headers;
}

function buildJsonHeaders(includeAuth: boolean = true): Record<string, string> {
  const headers = buildHeaders(includeAuth);
  headers["Content-Type"] = "application/json";
  return headers;
}

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once("ready", async () => {
  await registerCommands(token, appId);
  console.log("Bot ready");
});

client.on("interactionCreate", async (i: Interaction) => {
  if (!i.isChatInputCommand()) return;
  try {
    if (i.commandName === "status") {
      const svc = i.options.getString("service", true);
      const r = await fetch(`${controlApi.base_url}/status/${svc}`, {
        headers: buildHeaders()
      }).then(r => r.json());
      await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const r = await fetch(`${controlApi.base_url}/logs/${svc}?tail=${tail}`, {
        headers: buildHeaders()
      }).then(r => r.text());
      await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const r = await fetch(`${controlApi.base_url}/deploy`, {
        method: "POST",
        headers: buildJsonHeaders(),
        body: JSON.stringify({ env: envName, tag })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      const r = await fetch(`${controlApi.base_url}/scale`, {
        method: "POST",
        headers: buildJsonHeaders(),
        body: JSON.stringify({ service: svc, replicas })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
    }
  } catch (e: unknown) {
    const errorMessage = e instanceof Error ? e.message : "Unknown error";
    await i.reply({ content: `Error: ${errorMessage}` });
  }
});

client.login(token);