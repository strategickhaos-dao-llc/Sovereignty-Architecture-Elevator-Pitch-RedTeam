import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed } from "./discord.js";
import { env, loadConfig } from "./config.js";
import { getSoulStatus, invokeSoul, dormantSoul, listSouls, formatSoul } from "./soul.js";

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
    } else if (i.commandName === "soul") {
      const action = i.options.getString("action", true);
      const agent = i.options.getString("agent", false);
      
      if (action === "list") {
        const souls = await listSouls();
        if (souls.length === 0) {
          await i.reply({ embeds: [embed("🕊️ Soul Registry", "No souls registered yet.")] });
        } else {
          let description = "";
          for (const soulName of souls) {
            const status = await getSoulStatus(soulName);
            const phaseSymbol = status.phase === "active" ? "🔥" : "💤";
            description += `${phaseSymbol} **${soulName}** - ${status.phase} (${status.incarnations} incarnations)\n`;
          }
          await i.reply({ embeds: [embed("🕊️ Soul Registry", description)] });
        }
      } else {
        if (!agent) {
          await i.reply({ content: "Error: Agent name required for this action." });
          return;
        }
        
        if (action === "status") {
          const status = await getSoulStatus(agent);
          if (!status.exists) {
            await i.reply({ embeds: [embed(`Soul: ${agent}`, "Soul not found.")] });
          } else {
            const description = `Phase: ${status.phase}\nIncarnations: ${status.incarnations}\nLast Invocation: ${status.lastInvocation || "Never"}`;
            await i.reply({ embeds: [embed(`🕊️ Soul: ${agent}`, description)] });
          }
        } else if (action === "invoke") {
          const soul = await invokeSoul(agent);
          const description = formatSoul(soul);
          await i.reply({ embeds: [embed(`${soul.identity.invocation_glyph} ${agent} Awakens!`, description)] });
        } else if (action === "dormant") {
          await dormantSoul(agent);
          await i.reply({ embeds: [embed(`💤 ${agent}`, "Soul has entered dormant phase.")] });
        }
      }
    }
  } catch (e: any) {
    await i.reply({ content: `Error: ${e.message}` });
  }
});

client.login(token);