/**
 * Priority Council Discord Commands
 * 
 * Slash commands for interacting with the Priority Council system.
 */

import { SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder } from "discord.js";
import {
  analyzePR,
  formatAnalysisEmbed,
  generateRoadmap,
  formatRoadmapEmbed,
  type PRAnalysis,
  type PRCategory,
} from "./index.js";

/**
 * Priority Council slash commands definitions
 */
export function getPriorityCouncilCommands() {
  return [
    // /priority <pr_number> - Show PR priority analysis
    new SlashCommandBuilder()
      .setName("priority")
      .setDescription("Show priority analysis for a PR")
      .addIntegerOption((o) =>
        o
          .setName("pr_number")
          .setDescription("Pull request number")
          .setRequired(true)
      ),

    // /roadmap - Show current roadmap
    new SlashCommandBuilder()
      .setName("roadmap")
      .setDescription("Show the current priority roadmap"),

    // /vote <pr_number> <vote_type> - Cast a vote
    new SlashCommandBuilder()
      .setName("vote")
      .setDescription("Cast a vote for a PR")
      .addIntegerOption((o) =>
        o
          .setName("pr_number")
          .setDescription("Pull request number")
          .setRequired(true)
      )
      .addStringOption((o) =>
        o
          .setName("vote_type")
          .setDescription("Type of vote")
          .setRequired(true)
          .addChoices(
            { name: "👍 Approve (+1)", value: "approve" },
            { name: "❤️ Critical for patient (+5)", value: "critical" },
            { name: "🚀 Accelerate research (+3)", value: "accelerate" },
            { name: "⚠️ Has concerns (-2)", value: "concern" },
            { name: "❌ Veto (-10)", value: "veto" }
          )
      ),

    // /triage - Manually trigger triage for a PR
    new SlashCommandBuilder()
      .setName("triage")
      .setDescription("Manually trigger priority triage for a PR")
      .addIntegerOption((o) =>
        o
          .setName("pr_number")
          .setDescription("Pull request number")
          .setRequired(true)
      ),

    // /block <pr_number> <reason> - Mark a PR as blocked
    new SlashCommandBuilder()
      .setName("block")
      .setDescription("Mark a PR as blocked")
      .addIntegerOption((o) =>
        o
          .setName("pr_number")
          .setDescription("Pull request number")
          .setRequired(true)
      )
      .addStringOption((o) =>
        o
          .setName("reason")
          .setDescription("Reason for blocking")
          .setRequired(true)
      ),

    // /unblock <pr_number> - Remove blocked status
    new SlashCommandBuilder()
      .setName("unblock")
      .setDescription("Remove blocked status from a PR")
      .addIntegerOption((o) =>
        o
          .setName("pr_number")
          .setDescription("Pull request number")
          .setRequired(true)
      ),

    // /critical-path - Show the critical path
    new SlashCommandBuilder()
      .setName("critical-path")
      .setDescription("Show the critical path to highest impact features"),

    // /this-week - Show PRs scheduled for this week
    new SlashCommandBuilder()
      .setName("this-week")
      .setDescription("Show PRs scheduled for this week"),
  ].map((c) => c.toJSON());
}

/**
 * Mock PR data store (in production, this would be a database)
 */
const prAnalysisCache = new Map<number, PRAnalysis>();

/**
 * Handle /priority command
 */
export async function handlePriorityCommand(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const prNumber = interaction.options.getInteger("pr_number", true);

  // Check cache first
  let analysis = prAnalysisCache.get(prNumber);

  if (!analysis) {
    // Create a mock analysis for demo purposes
    // In production, this would fetch from GitHub API
    analysis = analyzePR({
      prNumber,
      title: `PR #${prNumber}`,
      category: "Research Tools" as PRCategory,
      complexity: 5,
      risk: 3,
      dependenciesCount: 0,
      dependencies: [],
      blockers: [],
      urgencyFactors: {
        prAgeInDays: 7,
        unblocksOtherWork: true,
      },
      ciPassing: true,
      hasMergeConflicts: false,
      filesChanged: 5,
    });

    prAnalysisCache.set(prNumber, analysis);
  }

  const embedData = formatAnalysisEmbed(analysis);
  const embed = new EmbedBuilder()
    .setTitle(embedData.title)
    .setDescription(embedData.description)
    .setColor(embedData.color)
    .addFields(embedData.fields);

  await interaction.reply({ embeds: [embed] });
}

/**
 * Handle /roadmap command
 */
export async function handleRoadmapCommand(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  // Get all cached analyses (in production, fetch from database)
  const analyses = Array.from(prAnalysisCache.values());

  if (analyses.length === 0) {
    await interaction.reply({
      content:
        "📊 No PRs have been analyzed yet. Use `/triage <pr_number>` to analyze PRs.",
      ephemeral: true,
    });
    return;
  }

  const roadmap = generateRoadmap(analyses);
  const embedData = formatRoadmapEmbed(roadmap);

  const embed = new EmbedBuilder()
    .setTitle(embedData.title)
    .setDescription(embedData.description)
    .setColor(embedData.color)
    .addFields(embedData.fields);

  await interaction.reply({ embeds: [embed] });
}

/**
 * Handle /vote command
 */
export async function handleVoteCommand(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const prNumber = interaction.options.getInteger("pr_number", true);
  const voteType = interaction.options.getString("vote_type", true);

  const voteEmojis: Record<string, string> = {
    approve: "👍",
    critical: "❤️",
    accelerate: "🚀",
    concern: "⚠️",
    veto: "❌",
  };

  const votePoints: Record<string, number> = {
    approve: 1,
    critical: 5,
    accelerate: 3,
    concern: -2,
    veto: -10,
  };

  const emoji = voteEmojis[voteType] || "📊";
  const points = votePoints[voteType] || 0;

  // In production, this would store the vote in a database
  const embed = new EmbedBuilder()
    .setTitle(`${emoji} Vote Recorded`)
    .setDescription(`Your vote for PR #${prNumber} has been recorded.`)
    .setColor(points > 0 ? 0x00ff00 : points < 0 ? 0xff0000 : 0xffff00)
    .addFields(
      { name: "PR", value: `#${prNumber}`, inline: true },
      { name: "Vote", value: voteType, inline: true },
      { name: "Points", value: `${points > 0 ? "+" : ""}${points}`, inline: true },
      { name: "Voter", value: interaction.user.tag, inline: true }
    );

  await interaction.reply({ embeds: [embed] });
}

/**
 * Handle /triage command
 */
export async function handleTriageCommand(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const prNumber = interaction.options.getInteger("pr_number", true);

  await interaction.deferReply();

  // Create a demo analysis (in production, fetch from GitHub)
  const categories: PRCategory[] = [
    "Medical/Drug Discovery",
    "Research Tools",
    "Visualization",
    "Infrastructure",
    "Documentation",
    "Bug Fix",
  ];
  const randomCategory = categories[Math.floor(Math.random() * categories.length)];

  const analysis = analyzePR({
    prNumber,
    title: `PR #${prNumber}`,
    category: randomCategory,
    complexity: Math.floor(Math.random() * 7) + 2,
    risk: Math.floor(Math.random() * 5) + 1,
    dependenciesCount: Math.floor(Math.random() * 3),
    dependencies: [],
    blockers: [],
    urgencyFactors: {
      prAgeInDays: Math.floor(Math.random() * 30),
      unblocksOtherWork: Math.random() > 0.5,
      isDependencyForMedicalTrial: randomCategory === "Medical/Drug Discovery",
    },
    ciPassing: Math.random() > 0.2,
    hasMergeConflicts: Math.random() > 0.8,
    filesChanged: Math.floor(Math.random() * 20) + 1,
  });

  prAnalysisCache.set(prNumber, analysis);

  const embedData = formatAnalysisEmbed(analysis);
  const embed = new EmbedBuilder()
    .setTitle(`✅ Triage Complete - ${embedData.title}`)
    .setDescription(embedData.description)
    .setColor(embedData.color)
    .addFields(embedData.fields);

  await interaction.editReply({ embeds: [embed] });
}

/**
 * Handle /block command
 */
export async function handleBlockCommand(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const prNumber = interaction.options.getInteger("pr_number", true);
  const reason = interaction.options.getString("reason", true);

  const analysis = prAnalysisCache.get(prNumber);
  if (analysis) {
    analysis.blockers = [...analysis.blockers, reason];
    prAnalysisCache.set(prNumber, analysis);
  }

  const embed = new EmbedBuilder()
    .setTitle("🚫 PR Blocked")
    .setDescription(`PR #${prNumber} has been marked as blocked.`)
    .setColor(0xff0000)
    .addFields(
      { name: "PR", value: `#${prNumber}`, inline: true },
      { name: "Reason", value: reason, inline: false },
      { name: "Blocked by", value: interaction.user.tag, inline: true }
    );

  await interaction.reply({ embeds: [embed] });
}

/**
 * Handle /unblock command
 */
export async function handleUnblockCommand(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const prNumber = interaction.options.getInteger("pr_number", true);

  const analysis = prAnalysisCache.get(prNumber);
  if (analysis) {
    analysis.blockers = [];
    prAnalysisCache.set(prNumber, analysis);
  }

  const embed = new EmbedBuilder()
    .setTitle("✅ PR Unblocked")
    .setDescription(`PR #${prNumber} has been unblocked.`)
    .setColor(0x00ff00)
    .addFields(
      { name: "PR", value: `#${prNumber}`, inline: true },
      { name: "Unblocked by", value: interaction.user.tag, inline: true }
    );

  await interaction.reply({ embeds: [embed] });
}

/**
 * Handle /critical-path command
 */
export async function handleCriticalPathCommand(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const analyses = Array.from(prAnalysisCache.values());
  const criticalPRs = analyses.filter(
    (a) => a.tier === "critical" || a.tier === "high"
  );

  if (criticalPRs.length === 0) {
    await interaction.reply({
      content:
        "🎯 No critical or high priority PRs in the system. Keep up the good work!",
      ephemeral: true,
    });
    return;
  }

  const sortedPRs = criticalPRs.sort(
    (a, b) => b.finalPriority - a.finalPriority
  );

  const embed = new EmbedBuilder()
    .setTitle("🎯 Critical Path")
    .setDescription("Highest impact PRs in order of priority")
    .setColor(0xff0000)
    .addFields(
      sortedPRs.slice(0, 10).map((pr, index) => ({
        name: `${index + 1}. #${pr.prNumber}`,
        value: `${pr.title}\nPriority: ${pr.finalPriority}/100 | Tier: ${pr.tier.toUpperCase()}`,
        inline: false,
      }))
    );

  await interaction.reply({ embeds: [embed] });
}

/**
 * Handle /this-week command
 */
export async function handleThisWeekCommand(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const analyses = Array.from(prAnalysisCache.values());
  const thisWeekPRs = analyses.filter(
    (a) => a.tier === "critical" || a.tier === "high"
  );

  if (thisWeekPRs.length === 0) {
    await interaction.reply({
      content: "📅 No PRs scheduled for this week yet.",
      ephemeral: true,
    });
    return;
  }

  const embed = new EmbedBuilder()
    .setTitle("📅 This Week")
    .setDescription("PRs to work on this week")
    .setColor(0x3099199)
    .addFields(
      thisWeekPRs.slice(0, 10).map((pr) => ({
        name: `#${pr.prNumber} - ${pr.title}`,
        value: `Priority: ${pr.finalPriority}/100 | Category: ${pr.category}`,
        inline: false,
      }))
    );

  await interaction.reply({ embeds: [embed] });
}
