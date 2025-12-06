import { Client, GatewayIntentBits, Interaction, EmbedBuilder } from "discord.js";
import { registerCommands, embed } from "./discord.js";
import { env, loadConfig, Config } from "./config.js";

const cfg: Config = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";
const treasuryApiUrl = cfg.treasury?.api_endpoint || "http://valoryield-api:8080";
const controlApiUrl = cfg.infra?.control_api?.base_url || "";

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
      const r = await fetch(`${controlApiUrl}/status/${svc}`, {
        headers: { Authorization: `Bearer ${env("CTRL_API_TOKEN", false)}` }
      }).then(r => r.json());
      await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const r = await fetch(`${controlApiUrl}/logs/${svc}?tail=${tail}`, {
        headers: { Authorization: `Bearer ${env("CTRL_API_TOKEN", false)}` }
      }).then(r => r.text());
      await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const r = await fetch(`${controlApiUrl}/deploy`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env("CTRL_API_TOKEN", false)}` },
        body: JSON.stringify({ env: envName, tag })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      const r = await fetch(`${controlApiUrl}/scale`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env("CTRL_API_TOKEN", false)}` },
        body: JSON.stringify({ service: svc, replicas })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
    } else if (i.commandName === "portfolio") {
      // Treasury OS: Portfolio command
      await i.deferReply();
      try {
        const r = await fetch(`${treasuryApiUrl}/api/v1/portfolio`).then(r => r.json());
        const portfolioEmbed = new EmbedBuilder()
          .setTitle("💰 ValorYield Sovereign Treasury")
          .setDescription("Aggregated balance across all platforms")
          .setColor(0x06B6D4)
          .addFields(
            { name: "Total Balance", value: `$${(r.balance ?? 0).toFixed(2)}`, inline: false },
            { name: "Account", value: r.account ?? "N/A", inline: true },
            { name: "Allocation", value: r.allocation ?? "N/A", inline: true },
            { name: "Sovereignty", value: "100% ✅", inline: true }
          )
          .setFooter({ text: `Last updated: ${r.last_updated ?? new Date().toISOString()}` });
        await i.editReply({ embeds: [portfolioEmbed] });
      } catch (e: unknown) {
        const errorMessage = e instanceof Error ? e.message : String(e);
        await i.editReply(`❌ Error fetching portfolio: ${errorMessage}`);
      }
    } else if (i.commandName === "deposit") {
      // Treasury OS: Deposit command
      const amount = i.options.getNumber("amount", true);
      await i.deferReply();
      try {
        const r = await fetch(`${treasuryApiUrl}/api/v1/deposit?amount=${amount}`, {
          method: "POST"
        }).then(r => r.json());
        const depositEmbed = new EmbedBuilder()
          .setTitle("💸 Deposit Recorded")
          .setDescription(`$${amount.toFixed(2)} allocated from SwarmGate 7% protocol`)
          .setColor(0x00AA00)
          .addFields(
            { name: "New Balance", value: `$${(r.new_balance ?? 0).toFixed(2)}`, inline: true },
            { name: "Status", value: r.status ?? "recorded", inline: true }
          );
        if (r.trigger === "rebalance_queued") {
          depositEmbed.addFields({ name: "Next Action", value: "🤖 Legion analyzing for rebalance", inline: false });
        }
        await i.editReply({ embeds: [depositEmbed] });
      } catch (e: unknown) {
        const errorMessage = e instanceof Error ? e.message : String(e);
        await i.editReply(`❌ Error recording deposit: ${errorMessage}`);
      }
    } else if (i.commandName === "rebalance") {
      // Treasury OS: Rebalance command
      await i.deferReply();
      try {
        const r = await fetch(`${treasuryApiUrl}/api/v1/rebalance`, {
          method: "POST"
        }).then(r => r.json());
        const rebalanceEmbed = new EmbedBuilder()
          .setTitle("⚖️ Rebalance Triggered")
          .setDescription("Legion analyzing portfolio for optimization")
          .setColor(0x7DD3FC)
          .addFields({ name: "Status", value: r.message ?? "Rebalance initiated", inline: false });
        await i.editReply({ embeds: [rebalanceEmbed] });
      } catch (e: unknown) {
        const errorMessage = e instanceof Error ? e.message : String(e);
        await i.editReply(`❌ Error triggering rebalance: ${errorMessage}`);
      }
    }
  } catch (e: unknown) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    await i.reply({ content: `Error: ${errorMessage}` });
  }
});

client.login(token);