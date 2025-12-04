import { Client, GatewayIntentBits, Interaction, REST } from "discord.js";
import { registerCommands, embed } from "./discord.js";
import { env, loadConfig } from "./config.js";
import { createNotificationService } from "./notifications.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// Create notification service
const rest = new REST({ version: "10" }).setToken(token);
const channelIds = {
  alerts: process.env.ALERTS_CHANNEL_ID || "",
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID || "",
  prs: process.env.PRS_CHANNEL_ID || "",
  dev_feed: process.env.DEV_FEED_CHANNEL_ID || "",
  agents: process.env.AGENTS_CHANNEL_ID || ""
};
const notificationService = createNotificationService(rest, channelIds);

client.once("ready", async () => {
  await registerCommands(token, appId);
  console.log("Bot ready");
});

client.on("interactionCreate", async (i: Interaction) => {
  if (!i.isChatInputCommand()) return;
  try {
    if (i.commandName === "status") {
      const svc = i.options.getString("service", true);
      const r = await fetch(`${cfg.control_api.base_url}/status/${svc}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
      }).then(r => r.json());
      await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const r = await fetch(`${cfg.control_api.base_url}/logs/${svc}?tail=${tail}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
      }).then(r => r.text());
      await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const r = await fetch(`${cfg.control_api.base_url}/deploy`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
        body: JSON.stringify({ env: envName, tag })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      const r = await fetch(`${cfg.control_api.base_url}/scale`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
        body: JSON.stringify({ service: svc, replicas })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
    } else if (i.commandName === "notify") {
      const channel = i.options.getString("channel", true);
      const title = i.options.getString("title", true);
      const message = i.options.getString("message", true);
      const level = (i.options.getString("level") || "info") as "info" | "warning" | "error" | "success";
      const mentionUser = i.options.getUser("mention");
      
      const channelId = channelIds[channel as keyof typeof channelIds];
      if (!channelId) {
        await i.reply({ content: `Error: Channel "${channel}" is not configured`, ephemeral: true });
        return;
      }

      await notificationService.sendToChannel(channelId, {
        title,
        message,
        level,
        mentionUsers: mentionUser ? [mentionUser.id] : undefined
      });

      await i.reply({ 
        embeds: [embed("Notification Sent", `Channel: #${channel}\nTitle: ${title}\nLevel: ${level}`)],
        ephemeral: true 
      });
    }
  } catch (e: any) {
    await i.reply({ content: `Error: ${e.message}` });
  }
});

client.login(token);