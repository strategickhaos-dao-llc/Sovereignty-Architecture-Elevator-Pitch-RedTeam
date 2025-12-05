import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed, cognitiveEmbed } from "./discord.js";
import { env, loadConfig } from "./config.js";
import { FamilyDOM, createFamilyDOM } from "./family-dom/index.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// FamilyDOM instances per user
const familyDomInstances: Map<string, FamilyDOM> = new Map();

function getFamilyDOM(userId: string, displayName?: string): FamilyDOM {
  let instance = familyDomInstances.get(userId);
  if (!instance) {
    instance = createFamilyDOM(userId, displayName);
    familyDomInstances.set(userId, instance);
  }
  return instance;
}

client.once("ready", async () => {
  await registerCommands(token, appId);
  console.log("Bot ready");
  console.log("🧠 FamilyDOM cognitive architecture enabled");
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
    // FamilyDOM commands
    else if (i.commandName === "cognitive") {
      const dom = getFamilyDOM(i.user.id, i.user.displayName);
      const signature = dom.getCognitiveSignature();
      const profile = dom.getProfile();
      
      const fields = [
        { name: "🧠 Cognitive Score", value: `${signature.score}/100`, inline: true },
        { name: "📊 Throughput", value: profile.cognitiveStyle.symbolicThroughput, inline: true },
        { name: "🔄 Parallel Processing", value: profile.cognitiveStyle.parallelProcessing ? "✅ Enabled" : "❌ Disabled", inline: true },
        { name: "🎭 Characteristics", value: signature.characteristics.length > 0 ? signature.characteristics.join(", ") : "Building profile...", inline: false },
        { name: "📂 Active Projects", value: `${profile.activeProjects.filter(p => p.status === 'active').length} tracked`, inline: true },
        { name: "💾 Memory Entries", value: `${profile.contextMemory.length} stored`, inline: true },
        { name: "🔮 Intent Patterns", value: `${profile.intentPatterns.length} learned`, inline: true }
      ];
      
      await i.reply({ 
        embeds: [cognitiveEmbed(
          `🧠 Cognitive Profile: ${i.user.displayName}`,
          "Your FamilyDOM cognitive architecture status. Interact more to enhance your profile!",
          fields
        )] 
      });
    } else if (i.commandName === "cognition-report") {
      const dom = getFamilyDOM(i.user.id, i.user.displayName);
      const report = dom.getCognitiveReport();
      
      const layerDistStr = Object.entries(report.layerDistribution)
        .filter(([_, v]) => v > 0)
        .sort((a, b) => b[1] - a[1])
        .map(([k, v]) => `${k}: ${(v * 100).toFixed(1)}%`)
        .join("\n") || "No data yet";
      
      const fields = [
        { name: "🎯 Signature Score", value: `${report.signature.score}/100`, inline: true },
        { name: "📈 Throughput Trend", value: `${report.throughputAnalysis.trend} (avg: ${report.throughputAnalysis.average.toFixed(1)})`, inline: true },
        { name: "⚡ Current Level", value: report.throughputAnalysis.currentLevel, inline: true },
        { name: "📊 Layer Distribution", value: `\`\`\`\n${layerDistStr}\n\`\`\``, inline: false },
        { name: "🔍 Unique Patterns", value: report.uniquePatterns.length > 0 ? report.uniquePatterns.join(", ") : "None detected", inline: false },
        { name: "💡 Recommendations", value: report.recommendations.length > 0 ? report.recommendations.slice(0, 2).join("\n") : "Keep interacting to build your profile!", inline: false }
      ];
      
      await i.reply({ 
        embeds: [cognitiveEmbed(
          `📋 Cognitive Analysis Report: ${report.displayName}`,
          "Full-stack cognitive reasoning analysis of your communication patterns.",
          fields
        )] 
      });
    } else if (i.commandName === "set-style") {
      const dom = getFamilyDOM(i.user.id, i.user.displayName);
      const throughput = i.options.getString("throughput");
      const parallel = i.options.getBoolean("parallel");
      const narrative = i.options.getBoolean("narrative");
      
      const updates: Record<string, unknown> = {};
      const changes: string[] = [];
      
      if (throughput !== null) {
        updates.symbolicThroughput = throughput as 'low' | 'medium' | 'high' | 'extreme';
        changes.push(`Throughput: ${throughput}`);
      }
      if (parallel !== null) {
        updates.parallelProcessing = parallel;
        changes.push(`Parallel Processing: ${parallel ? "enabled" : "disabled"}`);
      }
      if (narrative !== null) {
        updates.narrativeRecursion = narrative;
        changes.push(`Narrative Recursion: ${narrative ? "enabled" : "disabled"}`);
      }
      
      if (Object.keys(updates).length > 0) {
        dom.updateStyle(updates as Parameters<typeof dom.updateStyle>[0]);
        await i.reply({ 
          embeds: [cognitiveEmbed(
            "✅ Cognitive Style Updated",
            "Your FamilyDOM preferences have been configured.",
            [{ name: "Changes Applied", value: changes.join("\n") }]
          )] 
        });
      } else {
        await i.reply({ content: "No changes specified. Use options to configure your cognitive style." });
      }
    } else if (i.commandName === "track-project") {
      const dom = getFamilyDOM(i.user.id, i.user.displayName);
      const name = i.options.getString("name", true);
      const description = i.options.getString("description", true);
      
      dom.trackProject(name, description);
      
      await i.reply({ 
        embeds: [cognitiveEmbed(
          "📂 Project Tracked",
          `"${name}" is now tracked for cognitive continuity.`,
          [
            { name: "Project", value: name, inline: true },
            { name: "Description", value: description, inline: false }
          ]
        )] 
      });
    }
  } catch (e: unknown) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    await i.reply({ content: `Error: ${errorMessage}` });
  }
});

client.login(token);