import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed } from "./discord.js";
import { env, loadConfig } from "./config.js";
import { registerUser, getUser } from "./services/user-service.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

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
    } else if (i.commandName === "register") {
      const email = i.options.getString("email") || undefined;
      const displayName = i.options.getString("displayname") || undefined;
      
      const result = registerUser({
        discordId: i.user.id,
        username: i.user.username,
        email,
        displayName
      });
      
      if (result.success) {
        await i.reply({ 
          embeds: [embed("✅ Registration Successful", 
            `Welcome, ${result.user?.displayName || i.user.username}!\n\n` +
            `**Discord ID:** ${result.user?.discordId}\n` +
            `**Username:** ${result.user?.username}\n` +
            (result.user?.email ? `**Email:** ${result.user.email}\n` : "") +
            `**Roles:** ${result.user?.roles.join(", ")}\n` +
            `**Registered:** ${result.user?.createdAt.toISOString()}`
          )],
          ephemeral: true
        });
      } else {
        await i.reply({ 
          embeds: [embed("❌ Registration Failed", result.message)],
          ephemeral: true
        });
      }
    } else if (i.commandName === "profile") {
      const user = getUser(i.user.id);
      
      if (user) {
        await i.reply({ 
          embeds: [embed("👤 Your Profile", 
            `**Display Name:** ${user.displayName}\n` +
            `**Username:** ${user.username}\n` +
            (user.email ? `**Email:** ${user.email}\n` : "") +
            `**Roles:** ${user.roles.join(", ")}\n` +
            `**Registered:** ${user.createdAt.toISOString()}\n` +
            `**Last Updated:** ${user.updatedAt.toISOString()}`
          )],
          ephemeral: true
        });
      } else {
        await i.reply({ 
          embeds: [embed("❌ Not Registered", "You haven't registered yet. Use `/register` to create an account.")],
          ephemeral: true
        });
      }
    }
  } catch (e: any) {
    await i.reply({ content: `Error: ${e.message}` });
  }
});

client.login(token);