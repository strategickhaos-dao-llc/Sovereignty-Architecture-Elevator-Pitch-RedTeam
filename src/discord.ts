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
    // Treasury OS Commands
    new SlashCommandBuilder().setName("portfolio").setDescription("View ValorYield Engine portfolio balance"),
    new SlashCommandBuilder().setName("deposit").setDescription("Record SwarmGate 7% deposit")
      .addNumberOption(o => o.setName("amount").setDescription("Deposit amount in USD").setRequired(true)),
    new SlashCommandBuilder().setName("rebalance").setDescription("Trigger Legion portfolio rebalancing")
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string, color?: number) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(color || 0x2f81f7).toJSON();
}

// Treasury-specific embed builders
export function treasuryEmbed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x06B6D4).toJSON(); // Cyan
}

export function successEmbed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x00AA00).toJSON(); // Green
}

export function rebalanceEmbed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x7DD3FC).toJSON(); // Light blue
}