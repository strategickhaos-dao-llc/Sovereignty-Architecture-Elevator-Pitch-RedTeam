import { REST, Routes, SlashCommandBuilder, EmbedBuilder } from "discord.js";
import { QuadrantColors } from "./council/quadrant-embeds.js";

export async function registerCommands(token: string, appId: string) {
  const cmds = [
    new SlashCommandBuilder().setName("status").setDescription("Service status")
      .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name")),
    new SlashCommandBuilder().setName("logs").setDescription("Tail logs")
      .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name"))
      .addIntegerOption(o => o.setName("tail").setRequired(false).setDescription("Number of lines")),
    new SlashCommandBuilder().setName("deploy").setDescription("Deploy tag to env")
      .addStringOption(o => o.setName("env").setRequired(true).addChoices(
        { name: "dev", value: "dev" }, { name: "staging", value: "staging" }, { name: "prod", value: "prod" }).setDescription("Environment"))
      .addStringOption(o => o.setName("tag").setRequired(true).setDescription("Image tag")),
    new SlashCommandBuilder().setName("scale").setDescription("Scale service")
      .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name"))
      .addIntegerOption(o => o.setName("replicas").setRequired(true).setDescription("Number of replicas")),
    
    // Council Commands - Board Receipt System
    new SlashCommandBuilder().setName("council").setDescription("Council governance commands")
      .addSubcommand(sub => sub
        .setName("health")
        .setDescription("Check sovereignty health status"))
      .addSubcommand(sub => sub
        .setName("receipt")
        .setDescription("Create a board receipt")
        .addStringOption(o => o.setName("quadrant").setRequired(true)
          .setDescription("Quadrant category")
          .addChoices(
            { name: "🏛️ Council", value: "COUNCIL" },
            { name: "💰 Treasury", value: "TREASURY" },
            { name: "⚙️ Operations", value: "OPERATIONS" },
            { name: "🐝 Swarm", value: "SWARM" }
          ))
        .addStringOption(o => o.setName("title").setRequired(true).setDescription("Receipt title"))
        .addStringOption(o => o.setName("description").setRequired(true).setDescription("Receipt description")))
      .addSubcommand(sub => sub
        .setName("vote")
        .setDescription("Record a council vote")
        .addStringOption(o => o.setName("proposal").setRequired(true).setDescription("Proposal title"))
        .addIntegerOption(o => o.setName("for").setRequired(true).setDescription("Votes for"))
        .addIntegerOption(o => o.setName("against").setRequired(true).setDescription("Votes against"))
        .addIntegerOption(o => o.setName("abstain").setRequired(false).setDescription("Abstentions")))
      .addSubcommand(sub => sub
        .setName("stats")
        .setDescription("View council statistics")),
    
    // Swarm activity command
    new SlashCommandBuilder().setName("swarm").setDescription("Swarm activity and community stats")
      .addSubcommand(sub => sub
        .setName("activity")
        .setDescription("View recent swarm activity"))
      .addSubcommand(sub => sub
        .setName("wake")
        .setDescription("Wake the sovereignty swarm"))
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x2f81f7).toJSON();
}

/**
 * Create a quadrant-colored embed based on category
 */
export function quadrantEmbed(title: string, description: string, quadrant: keyof typeof QuadrantColors) {
  return new EmbedBuilder()
    .setTitle(title)
    .setDescription(description)
    .setColor(QuadrantColors[quadrant])
    .setTimestamp()
    .toJSON();
}