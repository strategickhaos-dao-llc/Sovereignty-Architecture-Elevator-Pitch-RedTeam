import { REST, Routes, SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder } from "discord.js";

export async function registerCommands(token: string, appId: string) {
  const cmds = [
    new SlashCommandBuilder().setName("status").setDescription("Service status")
      .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name to check")),
    new SlashCommandBuilder().setName("logs").setDescription("Tail logs")
      .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name"))
      .addIntegerOption(o => o.setName("tail").setRequired(false).setDescription("Number of lines to tail")),
    new SlashCommandBuilder().setName("deploy").setDescription("Deploy tag to env")
      .addStringOption(o => o.setName("env").setRequired(true).setDescription("Target environment").addChoices(
        { name: "dev", value: "dev" }, { name: "staging", value: "staging" }, { name: "prod", value: "prod" }))
      .addStringOption(o => o.setName("tag").setRequired(true).setDescription("Docker image tag to deploy"))
      .addBooleanOption(o => o.setName("plan").setRequired(false).setDescription("Dry-run mode: show manifest diff without applying"))
      .addIntegerOption(o => o.setName("canary").setRequired(false).setDescription("Canary percentage (0-100)"))
      .addStringOption(o => o.setName("svc").setRequired(false).setDescription("Target service for canary deployment")),
    new SlashCommandBuilder().setName("scale").setDescription("Scale service")
      .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name to scale"))
      .addIntegerOption(o => o.setName("replicas").setRequired(true).setDescription("Number of replicas")),
    new SlashCommandBuilder().setName("recon").setDescription("Run cluster reconnaissance and post to #recon")
      .addStringOption(o => o.setName("namespace").setRequired(false).setDescription("Target namespace (default: all)")),
    new SlashCommandBuilder().setName("review").setDescription("Request AI code review")
      .addStringOption(o => o.setName("pr").setRequired(true).setDescription("Pull request number or URL"))
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string, color?: number) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(color || 0x2f81f7).toJSON();
}

export function errorEmbed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0xff0000).toJSON();
}

export function successEmbed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x00ff00).toJSON();
}

export function warningEmbed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0xffaa00).toJSON();
}