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
    new SlashCommandBuilder().setName("notify").setDescription("Send a notification to a channel")
      .addStringOption(o => o.setName("channel").setRequired(true).addChoices(
        { name: "alerts", value: "alerts" },
        { name: "deployments", value: "deployments" },
        { name: "prs", value: "prs" },
        { name: "dev-feed", value: "dev_feed" },
        { name: "agents", value: "agents" }))
      .addStringOption(o => o.setName("title").setRequired(true).setDescription("Notification title"))
      .addStringOption(o => o.setName("message").setRequired(true).setDescription("Notification message"))
      .addStringOption(o => o.setName("level").setRequired(false).addChoices(
        { name: "info", value: "info" },
        { name: "warning", value: "warning" },
        { name: "error", value: "error" },
        { name: "success", value: "success" }))
      .addUserOption(o => o.setName("mention").setRequired(false).setDescription("User to mention"))
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x2f81f7).toJSON();
}