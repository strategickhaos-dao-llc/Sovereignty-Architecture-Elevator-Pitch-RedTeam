import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed, immuneStatusEmbed, swarmHealthEmbed } from "./discord.js";
import { env, loadConfig, type Config } from "./config.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// Simulated immune system state (in production, this would connect to actual cluster metrics)
interface ImmuneState {
  rbcCount: number;
  wbcCount: number;
  plateletCount: number;
  mode: "hunt" | "coordinate" | "biofilm";
  threatsBlocked: number;
  quorumEnabled: boolean;
  density: number;
  circadianMode: "day" | "night";
  recentThreats: string[];
  antibodies: string[];
}

const immuneState: ImmuneState = {
  rbcCount: 3,
  wbcCount: 2,
  plateletCount: 1,
  mode: "coordinate",
  threatsBlocked: 3,
  quorumEnabled: true,
  density: 14,
  circadianMode: "day",
  recentThreats: [],
  antibodies: []
};

// GKE cluster configuration
const gkeClusters = cfg.infra?.gke_clusters || [
  { name: "jarvis-swarm-personal-001", description: "Main production brain", zone: "us-central1" },
  { name: "red-team", description: "Security testing environment", zone: "us-central1" },
  { name: "autopilot-cluster-1", description: "Experimental playground", zone: "us-central1" }
];

function getControlApiUrl(): string {
  return cfg.infra?.control_api?.base_url || "https://control.internal.strategickhaos";
}

function getBearerEnv(): string {
  return cfg.infra?.control_api?.bearer_env || "CTRL_API_TOKEN";
}

client.once("ready", async () => {
  await registerCommands(token, appId);
  console.log("Bot ready - Sovereignty Architecture Control Plane Active");
  console.log(`Connected clusters: ${gkeClusters.map(c => c.name).join(", ")}`);
});

client.on("interactionCreate", async (i: Interaction) => {
  if (!i.isChatInputCommand()) return;
  try {
    // Original infrastructure commands
    if (i.commandName === "status") {
      const svc = i.options.getString("service", true);
      const r = await fetch(`${getControlApiUrl()}/status/${svc}`, {
        headers: { Authorization: `Bearer ${env(getBearerEnv())}` }
      }).then(r => r.json());
      await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const r = await fetch(`${getControlApiUrl()}/logs/${svc}?tail=${tail}`, {
        headers: { Authorization: `Bearer ${env(getBearerEnv())}` }
      }).then(r => r.text());
      await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const r = await fetch(`${getControlApiUrl()}/deploy`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(getBearerEnv())}` },
        body: JSON.stringify({ env: envName, tag })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      const r = await fetch(`${getControlApiUrl()}/scale`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(getBearerEnv())}` },
        body: JSON.stringify({ service: svc, replicas })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
    }
    // Immune System commands
    else if (i.commandName === "immune") {
      const subcommand = i.options.getSubcommand();
      
      if (subcommand === "status") {
        await i.reply({ embeds: [immuneStatusEmbed(immuneState)] });
      } else if (subcommand === "inject") {
        const threatType = i.options.getString("type", true);
        immuneState.recentThreats.push(threatType);
        immuneState.wbcCount += 1; // Spawn white blood cell
        await i.reply({ 
          embeds: [embed(
            "🧬 Threat Injection",
            `Injected test threat: **${threatType}**\n\n🔬 WBC spawned to investigate\n📊 Current WBC count: ${immuneState.wbcCount}`
          )] 
        });
      } else if (subcommand === "antibody") {
        const pattern = i.options.getString("pattern", true);
        immuneState.antibodies.push(pattern);
        await i.reply({ 
          embeds: [embed(
            "🧪 Antibody Registered",
            `Pattern: \`${pattern}\`\n\n✅ Added to immune memory\n📚 Total antibodies: ${immuneState.antibodies.length}`
          )] 
        });
      }
    }
    // Swarm commands
    else if (i.commandName === "swarm") {
      const subcommand = i.options.getSubcommand();
      
      if (subcommand === "mode") {
        const newMode = i.options.getString("behavior", true) as "hunt" | "coordinate" | "biofilm";
        const oldMode = immuneState.mode;
        immuneState.mode = newMode;
        
        const modeEmojis: Record<string, string> = {
          hunt: "🔥",
          coordinate: "🤝",
          biofilm: "🛡️"
        };
        
        await i.reply({ 
          embeds: [embed(
            "🧬 Swarm Mode Changed",
            `${modeEmojis[oldMode]} ${oldMode} → ${modeEmojis[newMode]} ${newMode}\n\n` +
            `All ${immuneState.density} cells notified via quorum sensing.`
          )] 
        });
      } else if (subcommand === "health") {
        await i.reply({ embeds: [swarmHealthEmbed(immuneState, gkeClusters)] });
      }
    }
    // Cluster commands
    else if (i.commandName === "cluster") {
      const subcommand = i.options.getSubcommand();
      
      if (subcommand === "list") {
        const clusterList = gkeClusters.map(c => 
          `🐉 **${c.name}**\n   └ ${c.description}\n   └ Zone: ${c.zone}`
        ).join("\n\n");
        
        await i.reply({ 
          embeds: [embed("☁️ GKE Clusters", clusterList + "\n\n*Three dragons, one Discord interface.*")] 
        });
      } else if (subcommand === "wake") {
        const clusterName = i.options.getString("name", true);
        const cluster = gkeClusters.find(c => c.name === clusterName);
        
        if (cluster) {
          await i.reply({ 
            embeds: [embed(
              "🔥 Dragon Awakening",
              `Waking cluster: **${cluster.name}**\n${cluster.description}\n\n` +
              `\`\`\`bash\ngcloud container clusters get-credentials ${cluster.name} --zone=${cluster.zone}\n\`\`\`\n` +
              `⏳ Initializing consciousness...`
            )] 
          });
        } else {
          await i.reply({ content: `❌ Cluster "${clusterName}" not found.` });
        }
      }
    }
  } catch (e: unknown) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    await i.reply({ content: `Error: ${errorMessage}` });
  }
});

client.login(token);