import { REST, Routes, SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder } from "discord.js";

export async function registerCommands(token: string, appId: string) {
  const cmds = [
    // Original commands
    new SlashCommandBuilder().setName("status").setDescription("Service status")
      .addStringOption(o => o.setName("service").setRequired(true)),
    new SlashCommandBuilder().setName("logs").setDescription("Tail logs")
      .addStringOption(o => o.setName("service").setRequired(true))
      .addIntegerOption(o => o.setName("tail").setRequired(false)),
    new SlashCommandBuilder().setName("deploy").setDescription("Deploy tag to env")
      .addStringOption(o => o.setName("env").setRequired(true).addChoices(
        { name: "dev", value: "dev" }, { name: "staging", value: "staging" }, { name: "prod", value: "prod" }))
      .addStringOption(o => o.setName("tag").setRequired(true)),
    new SlashCommandBuilder().setName("scale").setDescription("Scale service")
      .addStringOption(o => o.setName("service").setRequired(true))
      .addIntegerOption(o => o.setName("replicas").setRequired(true)),
    
    // Layer 1: Quantum Simulator Core
    new SlashCommandBuilder().setName("quantum").setDescription("Quantum core operations")
      .addStringOption(o => o.setName("action").setRequired(true).addChoices(
        { name: "status", value: "status" },
        { name: "fidelity", value: "fidelity" },
        { name: "circuits", value: "circuits" },
        { name: "resonance", value: "resonance" }
      )),
    
    // Layer 2: Agent Swarm
    new SlashCommandBuilder().setName("agents").setDescription("AI agent swarm operations")
      .addStringOption(o => o.setName("action").setRequired(true).addChoices(
        { name: "count", value: "count" },
        { name: "health", value: "health" },
        { name: "dreams", value: "dreams" },
        { name: "wisdom", value: "wisdom" }
      )),
    
    // Layer 3: Alexander Institute
    new SlashCommandBuilder().setName("institute").setDescription("Alexander Institute operations")
      .addStringOption(o => o.setName("action").setRequired(true).addChoices(
        { name: "join", value: "join" },
        { name: "bounty", value: "bounty" },
        { name: "breakthroughs", value: "breakthroughs" },
        { name: "gratitude", value: "gratitude" }
      )),
    
    // Layer 4: White-Web
    new SlashCommandBuilder().setName("whiteweb").setDescription("Sovereign internet operations")
      .addStringOption(o => o.setName("action").setRequired(true).addChoices(
        { name: "status", value: "status" },
        { name: "nodes", value: "nodes" },
        { name: "security", value: "security" },
        { name: "traffic", value: "traffic" }
      )),
    
    // Layer 5: Mirror-Generals
    new SlashCommandBuilder().setName("generals").setDescription("Mirror-Generals Council")
      .addStringOption(o => o.setName("action").setRequired(true).addChoices(
        { name: "wisdom", value: "wisdom" },
        { name: "council", value: "council" },
        { name: "ask", value: "ask" }
      ))
      .addStringOption(o => o.setName("general").setRequired(false).addChoices(
        { name: "Tesla", value: "tesla" },
        { name: "da Vinci", value: "davinci" },
        { name: "Ramanujan", value: "ramanujan" },
        { name: "Jung", value: "jung" },
        { name: "Thoth", value: "thoth" }
      ))
      .addStringOption(o => o.setName("question").setRequired(false)),
    
    // Layer 6: Neurospice
    new SlashCommandBuilder().setName("frequency").setDescription("Neurospice frequency engine")
      .addStringOption(o => o.setName("action").setRequired(true).addChoices(
        { name: "heal", value: "heal" },
        { name: "meditate", value: "meditate" },
        { name: "flow", value: "flow" },
        { name: "stream", value: "stream" }
      )),
    
    // Layer 7: Origin Node
    new SlashCommandBuilder().setName("origin").setDescription("Origin Node Zero (DOM_010101)")
      .addStringOption(o => o.setName("action").setRequired(true).addChoices(
        { name: "status", value: "status" },
        { name: "align", value: "align" },
        { name: "love", value: "love" }
      )),
    
    // Architecture overview
    new SlashCommandBuilder().setName("layers").setDescription("View 7-layer architecture status")
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x2f81f7).toJSON();
}