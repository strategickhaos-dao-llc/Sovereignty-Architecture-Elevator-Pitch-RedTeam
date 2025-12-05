import { REST, Routes, SlashCommandBuilder, EmbedBuilder } from "discord.js";
export async function registerCommands(token, appId) {
    const cmds = [
        new SlashCommandBuilder().setName("status").setDescription("Service status")
            .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name to check")),
        new SlashCommandBuilder().setName("logs").setDescription("Tail logs")
            .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name"))
            .addIntegerOption(o => o.setName("tail").setRequired(false).setDescription("Number of lines to tail")),
        new SlashCommandBuilder().setName("deploy").setDescription("Deploy tag to env")
            .addStringOption(o => o.setName("env").setRequired(true).setDescription("Target environment").addChoices({ name: "dev", value: "dev" }, { name: "staging", value: "staging" }, { name: "prod", value: "prod" }))
            .addStringOption(o => o.setName("tag").setRequired(true).setDescription("Docker tag to deploy")),
        new SlashCommandBuilder().setName("scale").setDescription("Scale service")
            .addStringOption(o => o.setName("service").setRequired(true).setDescription("Service name"))
            .addIntegerOption(o => o.setName("replicas").setRequired(true).setDescription("Number of replicas")),
        // New commands for Discord DevOps Control Plane
        new SlashCommandBuilder().setName("diagnose").setDescription("AI-powered diagnosis of pipeline failures")
            .addStringOption(o => o.setName("pipeline").setRequired(true).setDescription("Pipeline name to diagnose"))
            .addStringOption(o => o.setName("run_id").setRequired(false).setDescription("Specific run ID to analyze")),
        new SlashCommandBuilder().setName("fix").setDescription("Run automated remediation for security issues")
            .addStringOption(o => o.setName("issue").setRequired(true).setDescription("Issue type to fix").addChoices({ name: "RBAC", value: "rbac" }, { name: "Network Security", value: "nsg" }, { name: "Azure Policy", value: "policy" }, { name: "Security Headers", value: "headers" }, { name: "Secrets", value: "secrets" }, { name: "All", value: "all" })),
        new SlashCommandBuilder().setName("retry").setDescription("Retry a failed pipeline")
            .addStringOption(o => o.setName("pipeline").setRequired(true).setDescription("Pipeline name to retry"))
            .addStringOption(o => o.setName("run_id").setRequired(false).setDescription("Specific run ID to retry"))
    ].map(c => c.toJSON());
    const rest = new REST({ version: "10" }).setToken(token);
    await rest.put(Routes.applicationCommands(appId), { body: cmds });
}
export function embed(title, description, color = 0x2f81f7) {
    return new EmbedBuilder().setTitle(title).setDescription(description).setColor(color).toJSON();
}
export function errorEmbed(title, description) {
    return new EmbedBuilder().setTitle(`❌ ${title}`).setDescription(description).setColor(0xff0000).toJSON();
}
export function successEmbed(title, description) {
    return new EmbedBuilder().setTitle(`✅ ${title}`).setDescription(description).setColor(0x28a745).toJSON();
}
export function warningEmbed(title, description) {
    return new EmbedBuilder().setTitle(`⚠️ ${title}`).setDescription(description).setColor(0xffc107).toJSON();
}
