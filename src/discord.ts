import { REST, Routes, SlashCommandBuilder, EmbedBuilder } from "discord.js";
import type { ClusterConfig } from "./config.js";

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

export async function registerCommands(token: string, appId: string) {
  const cmds = [
    // Original infrastructure commands
    new SlashCommandBuilder().setName("status").setDescription("Service status")
      .addStringOption(o => o.setName("service").setDescription("Service name").setRequired(true)),
    new SlashCommandBuilder().setName("logs").setDescription("Tail logs")
      .addStringOption(o => o.setName("service").setDescription("Service name").setRequired(true))
      .addIntegerOption(o => o.setName("tail").setDescription("Number of lines").setRequired(false)),
    new SlashCommandBuilder().setName("deploy").setDescription("Deploy tag to env")
      .addStringOption(o => o.setName("env").setDescription("Environment").setRequired(true).addChoices(
        { name: "dev", value: "dev" }, { name: "staging", value: "staging" }, { name: "prod", value: "prod" }))
      .addStringOption(o => o.setName("tag").setDescription("Tag to deploy").setRequired(true)),
    new SlashCommandBuilder().setName("scale").setDescription("Scale service")
      .addStringOption(o => o.setName("service").setDescription("Service name").setRequired(true))
      .addIntegerOption(o => o.setName("replicas").setDescription("Number of replicas").setRequired(true)),
    
    // Immune System commands
    new SlashCommandBuilder().setName("immune").setDescription("Immune system controls")
      .addSubcommand(sub => sub.setName("status").setDescription("Show immune system status - cell counts, mode, recent activity"))
      .addSubcommand(sub => sub.setName("inject")
        .setDescription("Deploy test threat to trigger immune response")
        .addStringOption(o => o.setName("type").setDescription("Threat type").setRequired(true)
          .addChoices(
            { name: "malware", value: "malware" },
            { name: "ddos", value: "ddos" },
            { name: "intrusion", value: "intrusion" },
            { name: "anomaly", value: "anomaly" }
          )))
      .addSubcommand(sub => sub.setName("antibody")
        .setDescription("Manually add threat signature to immune memory")
        .addStringOption(o => o.setName("pattern").setDescription("Threat signature pattern").setRequired(true))),
    
    // Swarm commands
    new SlashCommandBuilder().setName("swarm").setDescription("Swarm intelligence controls")
      .addSubcommand(sub => sub.setName("mode")
        .setDescription("Force behavioral state change")
        .addStringOption(o => o.setName("behavior").setDescription("Swarm behavior mode").setRequired(true)
          .addChoices(
            { name: "hunt", value: "hunt" },
            { name: "coordinate", value: "coordinate" },
            { name: "biofilm", value: "biofilm" }
          )))
      .addSubcommand(sub => sub.setName("health").setDescription("Show swarm health dashboard")),
    
    // Cluster commands
    new SlashCommandBuilder().setName("cluster").setDescription("GKE cluster management")
      .addSubcommand(sub => sub.setName("list").setDescription("List all connected GKE clusters"))
      .addSubcommand(sub => sub.setName("wake")
        .setDescription("Wake a dormant dragon cluster")
        .addStringOption(o => o.setName("name").setDescription("Cluster name").setRequired(true)
          .addChoices(
            { name: "jarvis-swarm-personal-001", value: "jarvis-swarm-personal-001" },
            { name: "red-team", value: "red-team" },
            { name: "autopilot-cluster-1", value: "autopilot-cluster-1" }
          )))
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string, color: number = 0x2f81f7) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(color).toJSON();
}

export function immuneStatusEmbed(state: ImmuneState) {
  const modeEmojis: Record<string, string> = {
    hunt: "🔥 Hunt",
    coordinate: "🤝 Coordinate",
    biofilm: "🛡️ Biofilm"
  };

  const circadianEmoji = state.circadianMode === "day" ? "☀️" : "🌙";
  const healthColor = state.threatsBlocked < 5 ? 0x00ff00 : state.threatsBlocked < 10 ? 0xffff00 : 0xff0000;

  return new EmbedBuilder()
    .setTitle("🩸 Immune System Status")
    .setColor(healthColor)
    .addFields(
      { name: "Mode", value: modeEmojis[state.mode], inline: true },
      { name: "Circadian", value: `${circadianEmoji} ${state.circadianMode}`, inline: true },
      { name: "Quorum", value: state.quorumEnabled ? "✅ Enabled" : "❌ Disabled", inline: true },
      { name: "🩸 RBC", value: `${state.rbcCount} active`, inline: true },
      { name: "🔬 WBC", value: `${state.wbcCount} scanning`, inline: true },
      { name: "🩹 Platelets", value: `${state.plateletCount} ready`, inline: true },
      { name: "Density", value: `${state.density} cells active`, inline: true },
      { name: "Threats Blocked", value: `${state.threatsBlocked} today`, inline: true },
      { name: "Antibodies", value: `${state.antibodies.length} patterns`, inline: true }
    )
    .setFooter({ text: "Sovereignty Architecture • Living Infrastructure" })
    .setTimestamp()
    .toJSON();
}

export function swarmHealthEmbed(state: ImmuneState, clusters: ClusterConfig[]) {
  const modeEmojis: Record<string, string> = {
    hunt: "🔥",
    coordinate: "🤝",
    biofilm: "🛡️"
  };

  const clusterStatus = clusters.map(c => `🐉 ${c.name}: ✅ Connected`).join("\n");

  return new EmbedBuilder()
    .setTitle("🧬 Swarm Health Dashboard")
    .setColor(0x00ff00)
    .setDescription("*Sovereign control from anywhere, through Discord*")
    .addFields(
      { name: "Behavioral Mode", value: `${modeEmojis[state.mode]} ${state.mode.charAt(0).toUpperCase() + state.mode.slice(1)}`, inline: true },
      { name: "Cell Density", value: `${state.density} cells`, inline: true },
      { name: "Quorum Sensing", value: state.quorumEnabled ? "🧠 Active" : "💤 Dormant", inline: true },
      { name: "Connected Clusters", value: clusterStatus },
      { name: "Gene Transfer", value: "📡 Propagation enabled", inline: true },
      { name: "Threat Level", value: state.threatsBlocked > 10 ? "🔴 HIGH" : state.threatsBlocked > 5 ? "🟡 MEDIUM" : "🟢 LOW", inline: true }
    )
    .setFooter({ text: "Three dragons, one Discord interface" })
    .setTimestamp()
    .toJSON();
}