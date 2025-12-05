import { REST, Routes, SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder } from "discord.js";

export async function registerCommands(token: string, appId: string) {
  const cmds = [
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
    // FamilyDOM cognitive architecture commands
    new SlashCommandBuilder().setName("cognitive").setDescription("View your cognitive profile and signature"),
    new SlashCommandBuilder().setName("cognition-report").setDescription("Generate a full cognitive analysis report"),
    new SlashCommandBuilder().setName("set-style").setDescription("Configure your cognitive style preferences")
      .addStringOption(o => o.setName("throughput").setRequired(false)
        .setDescription("Symbolic throughput level")
        .addChoices(
          { name: "minimal", value: "low" },
          { name: "standard", value: "medium" },
          { name: "high", value: "high" },
          { name: "extreme", value: "extreme" }
        ))
      .addBooleanOption(o => o.setName("parallel").setRequired(false)
        .setDescription("Enable parallel processing mode"))
      .addBooleanOption(o => o.setName("narrative").setRequired(false)
        .setDescription("Enable narrative recursion")),
    new SlashCommandBuilder().setName("track-project").setDescription("Track a project for continuity")
      .addStringOption(o => o.setName("name").setRequired(true).setDescription("Project name"))
      .addStringOption(o => o.setName("description").setRequired(true).setDescription("Project description"))
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x2f81f7).toJSON();
}

export function cognitiveEmbed(title: string, description: string, fields: Array<{ name: string; value: string; inline?: boolean }>) {
  const builder = new EmbedBuilder()
    .setTitle(title)
    .setDescription(description)
    .setColor(0xff0066); // FamilyDOM signature color (pink)
  
  for (const field of fields) {
    builder.addFields({ name: field.name, value: field.value, inline: field.inline ?? false });
  }
  
  return builder.toJSON();
}