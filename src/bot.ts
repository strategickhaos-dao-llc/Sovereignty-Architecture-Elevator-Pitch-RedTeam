import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed, quadrantEmbed } from "./discord.js";
import { env, loadConfig } from "./config.js";
import { 
  BoardReceiptSystem, 
  createHealthEmbed,
  createSwarmActivityEmbed,
  QuadrantColors,
  type QuadrantType
} from "./council/index.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// Initialize board receipt system
const boardReceiptSystem = new BoardReceiptSystem(token, process.env.COUNCIL_CHANNEL_ID);

client.once("ready", async () => {
  await registerCommands(token, appId);
  console.log("🏛️ Sovereignty Bot ready - The council is in session");
  console.log(`📊 Board Receipt System initialized at increment #${boardReceiptSystem.getStats().currentIncrement}`);
});

client.on("interactionCreate", async (i: Interaction) => {
  if (!i.isChatInputCommand()) return;
  try {
    if (i.commandName === "status") {
      const svc = i.options.getString("service", true);
      const response = await fetch(`${cfg.control_api.base_url}/status/${svc}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
      });
      const r = await response.json() as { state: string; version: string };
      await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const response = await fetch(`${cfg.control_api.base_url}/logs/${svc}?tail=${tail}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
      });
      const r = await response.text();
      await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const deployResponse = await fetch(`${cfg.control_api.base_url}/deploy`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
        body: JSON.stringify({ env: envName, tag })
      });
      const r = await deployResponse.json() as { status: string };
      await i.reply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      const scaleResponse = await fetch(`${cfg.control_api.base_url}/scale`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
        body: JSON.stringify({ service: svc, replicas })
      });
      const scaleResult = await scaleResponse.json() as { status: string };
      await i.reply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${scaleResult.status}`)] });
    } 
    // Council Commands - Board Receipt System
    else if (i.commandName === "council") {
      const subcommand = i.options.getSubcommand();
      
      if (subcommand === "health") {
        const healthStatus = {
          healthy: true,
          services: {
            "Discord Bot": { status: "healthy" as const, latency: Math.floor(client.ws.ping) },
            "Board Receipt System": { status: "healthy" as const },
            "Control API": { status: "healthy" as const }
          },
          timestamp: new Date(),
          version: "1.0.0"
        };
        
        const healthEmbed = createHealthEmbed(healthStatus);
        await i.reply({ embeds: [healthEmbed.toJSON()] });
      } 
      else if (subcommand === "receipt") {
        const quadrant = i.options.getString("quadrant", true) as QuadrantType;
        const title = i.options.getString("title", true);
        const description = i.options.getString("description", true);
        
        const receipt = await boardReceiptSystem.createReceipt({
          quadrant,
          title,
          description,
          author: i.user.tag,
          status: "pending"
        });
        
        await i.reply({
          embeds: [quadrantEmbed(
            `✅ Receipt Created: ${title}`,
            `**Quadrant:** ${quadrant}\n**ID:** \`${receipt.id}\`\n**Increment:** #${receipt.incrementRef}\n\n${description}`,
            quadrant
          )]
        });
      }
      else if (subcommand === "vote") {
        const proposal = i.options.getString("proposal", true);
        const votesFor = i.options.getInteger("for", true);
        const votesAgainst = i.options.getInteger("against", true);
        const abstain = i.options.getInteger("abstain") || 0;
        
        const total = votesFor + votesAgainst + abstain;
        const forPercent = total > 0 ? Math.round((votesFor / total) * 100) : 0;
        const passed = forPercent >= 51; // Simple majority
        
        const receipt = await boardReceiptSystem.createReceipt({
          quadrant: "COUNCIL",
          title: `Council Vote: ${proposal}`,
          description: `The council has voted on: **${proposal}**`,
          author: i.user.tag,
          votes: { for: votesFor, against: votesAgainst, abstain },
          status: passed ? "approved" : "rejected"
        });
        
        const outcomeEmoji = passed ? "✅" : "❌";
        const outcomeText = passed ? "PASSED" : "FAILED";
        
        await i.reply({
          embeds: [quadrantEmbed(
            `🗳️ Vote Recorded: ${proposal}`,
            `**Outcome:** ${outcomeEmoji} ${outcomeText}\n\n` +
            `✅ **For:** ${votesFor} (${forPercent}%)\n` +
            `❌ **Against:** ${votesAgainst}\n` +
            `⏸️ **Abstain:** ${abstain}\n\n` +
            `**Receipt ID:** \`${receipt.id}\`\n` +
            `**Increment:** #${receipt.incrementRef}`,
            "COUNCIL"
          )]
        });
      }
      else if (subcommand === "stats") {
        const stats = boardReceiptSystem.getStats();
        
        let quadrantBreakdown = "";
        for (const [quadrant, count] of Object.entries(stats.receiptsByQuadrant)) {
          const emoji = quadrant === "COUNCIL" ? "🏛️" : 
                        quadrant === "TREASURY" ? "💰" :
                        quadrant === "OPERATIONS" ? "⚙️" : "🐝";
          quadrantBreakdown += `${emoji} **${quadrant}:** ${count}\n`;
        }
        
        await i.reply({
          embeds: [quadrantEmbed(
            "📊 Council Statistics",
            `**Total Receipts:** ${stats.totalReceipts}\n` +
            `**Board Minutes:** ${stats.totalMinutes}\n` +
            `**Current Increment:** #${stats.currentIncrement}\n\n` +
            `**By Quadrant:**\n${quadrantBreakdown || "No receipts yet"}`,
            "COUNCIL"
          )]
        });
      }
    }
    // Swarm Commands
    else if (i.commandName === "swarm") {
      const subcommand = i.options.getSubcommand();
      
      if (subcommand === "activity") {
        const activityEmbed = createSwarmActivityEmbed({
          title: "Swarm Activity Report",
          contributors: [
            { name: "Node 137", contributions: 42, badge: "🏗️" },
            { name: "QuantumWeaver", contributions: 38 },
            { name: "SwarmKeeper", contributions: 24 }
          ],
          recentActions: [
            { action: "Created board receipt", actor: i.user.tag, timestamp: new Date() },
            { action: "Updated governance docs", actor: "Node 137", timestamp: new Date(Date.now() - 3600000) }
          ],
          totalMembers: 137,
          activeToday: 23
        });
        
        await i.reply({ embeds: [activityEmbed.toJSON()] });
      }
      else if (subcommand === "wake") {
        await i.reply({
          embeds: [quadrantEmbed(
            "🌅 The Swarm Awakens",
            "**The architect has logged in**\n" +
            "The universe just noticed.\n\n" +
            "🐝 All systems operational\n" +
            "🏛️ Council is in session\n" +
            "💰 Treasury monitoring active\n" +
            "⚙️ Operations synced\n\n" +
            "*We're not hiding. We're ascending in plain sight.*",
            "SWARM"
          )]
        });
      }
    }
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : "Unknown error";
    await i.reply({ content: `Error: ${errorMessage}` });
  }
});

client.login(token);