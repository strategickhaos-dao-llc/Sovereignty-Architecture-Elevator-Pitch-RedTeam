import { Client, GatewayIntentBits, Interaction, EmbedBuilder } from "discord.js";
import { registerCommands, embed, treasuryEmbed, successEmbed, rebalanceEmbed } from "./discord.js";
import { env, loadConfig } from "./config.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

// Treasury OS API endpoint - defaults to internal K8s service
const treasuryApiUrl = env("TREASURY_API_URL", false) || cfg.treasury?.api_endpoint || "http://valoryield-api:8080";

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
    } 
    // Treasury OS Commands
    else if (i.commandName === "portfolio") {
      await i.deferReply();
      try {
        const response = await fetch(`${treasuryApiUrl}/api/v1/portfolio`);
        const data = await response.json() as { 
          balance: number; 
          account: string; 
          allocation: string; 
          last_updated: string;
        };
        
        const portfolioEmbed = new EmbedBuilder()
          .setTitle("💰 ValorYield Sovereign Treasury")
          .setDescription("Aggregated balance across all platforms")
          .setColor(0x06B6D4)
          .addFields(
            { name: "Total Balance", value: `$${data.balance.toFixed(2)}`, inline: false },
            { name: "Account", value: data.account, inline: true },
            { name: "Allocation", value: data.allocation, inline: true },
            { name: "Sovereignty", value: "100% ✅", inline: true }
          )
          .setFooter({ text: `Last updated: ${data.last_updated}` })
          .toJSON();
        
        await i.editReply({ embeds: [portfolioEmbed] });
      } catch (e: unknown) {
        const errorMsg = e instanceof Error ? e.message : String(e);
        await i.editReply({ content: `❌ Error fetching portfolio: ${errorMsg}` });
      }
    } else if (i.commandName === "deposit") {
      await i.deferReply();
      try {
        const amount = i.options.getNumber("amount", true);
        const response = await fetch(`${treasuryApiUrl}/api/v1/deposit`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ amount })
        });
        const data = await response.json() as { 
          new_balance: number; 
          status: string; 
          trigger?: string;
        };
        
        const depositEmbed = new EmbedBuilder()
          .setTitle("💸 Deposit Recorded")
          .setDescription(`$${amount.toFixed(2)} allocated from SwarmGate 7% protocol`)
          .setColor(0x00AA00)
          .addFields(
            { name: "New Balance", value: `$${data.new_balance.toFixed(2)}`, inline: true },
            { name: "Status", value: data.status, inline: true }
          );
        
        if (data.trigger === "rebalance_queued") {
          depositEmbed.addFields({ name: "Next Action", value: "🤖 Legion analyzing for rebalance", inline: false });
        }
        
        await i.editReply({ embeds: [depositEmbed.toJSON()] });
      } catch (e: unknown) {
        const errorMsg = e instanceof Error ? e.message : String(e);
        await i.editReply({ content: `❌ Error recording deposit: ${errorMsg}` });
      }
    } else if (i.commandName === "rebalance") {
      await i.deferReply();
      try {
        const response = await fetch(`${treasuryApiUrl}/api/v1/rebalance`, {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const data = await response.json() as { message: string };
        
        const rebalanceEmbed = new EmbedBuilder()
          .setTitle("⚖️ Rebalance Triggered")
          .setDescription("Legion analyzing portfolio for optimization")
          .setColor(0x7DD3FC)
          .addFields({ name: "Status", value: data.message, inline: false })
          .toJSON();
        
        await i.editReply({ embeds: [rebalanceEmbed] });
      } catch (e: unknown) {
        const errorMsg = e instanceof Error ? e.message : String(e);
        await i.editReply({ content: `❌ Error triggering rebalance: ${errorMsg}` });
      }
    }
  } catch (e: unknown) {
    const errorMsg = e instanceof Error ? e.message : String(e);
    await i.reply({ content: `Error: ${errorMsg}` });
  }
});

client.login(token);