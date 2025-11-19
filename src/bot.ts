import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed } from "./discord.js";
import { env, config } from "./config.js";

const cfg = config;
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
        headers: { Authorization: `Bearer ${env(cfg.control_api.auth.token_secret_ref)}` }
      }).then(r => r.json());
      await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const r = await fetch(`${cfg.control_api.base_url}/logs/${svc}?tail=${tail}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.auth.token_secret_ref)}` }
      }).then(r => r.text());
      await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const r = await fetch(`${cfg.control_api.base_url}/deploy`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.auth.token_secret_ref)}` },
        body: JSON.stringify({ env: envName, tag })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      const r = await fetch(`${cfg.control_api.base_url}/scale`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.auth.token_secret_ref)}` },
        body: JSON.stringify({ service: svc, replicas })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
    } else if (i.commandName === "snapshot") {
      await i.deferReply();
      const { createSnapshot, saveSnapshot } = await import("./snapshot.js");
      const customId = i.options.getString("id");
      const snapshot = await createSnapshot(customId ?? undefined);
      const filename = saveSnapshot(snapshot);
      const { EmbedBuilder } = await import("discord.js");
      const snapshotEmbed = new EmbedBuilder()
        .setColor(0x00ff00)
        .setTitle("✨ Snapshot Captured")
        .setDescription(`**ID:** ${snapshot.id}\n**File:** ${filename}`)
        .addFields(
          { name: "Timestamp", value: new Date(snapshot.timestamp).toISOString(), inline: true },
          { name: "Checksum", value: `\`${snapshot.checksum.slice(0, 16)}...\``, inline: true },
          { name: "Config Org", value: snapshot.config.org.name, inline: true }
        )
        .setFooter({ text: "🌀 Sovereign state preserved — immortal backup complete" });
      await i.editReply({ embeds: [snapshotEmbed] });
    }
  } catch (e: any) {
    await i.reply({ content: `Error: ${e.message}` }).catch(() => i.editReply({ content: `Error: ${e.message}` }));
  }
});

client.login(token);