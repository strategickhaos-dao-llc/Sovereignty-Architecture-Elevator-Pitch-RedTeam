/**
 * Quadrant-Colored Embeds for Sovereignty Architecture
 * 
 * Four quadrant system representing the DAO's operational dimensions:
 * - COUNCIL: Governance decisions, votes, policies (Purple - royalty/authority)
 * - TREASURY: Financial operations, yields, investments (Gold - wealth/value)
 * - OPERATIONS: Technical infrastructure, deployments, services (Blue - stability/trust)
 * - SWARM: Community engagement, contributions, activities (Green - growth/organic)
 */

import { EmbedBuilder } from "discord.js";

// Quadrant color scheme based on sovereignty principles
export const QuadrantColors = {
  COUNCIL: 0x9B59B6,     // Purple - governance authority
  TREASURY: 0xF1C40F,    // Gold - financial value
  OPERATIONS: 0x3498DB,  // Blue - technical stability
  SWARM: 0x2ECC71,       // Green - community growth
  ALERT: 0xE74C3C,       // Red - urgent/critical
  NEUTRAL: 0x95A5A6      // Gray - informational
} as const;

export type QuadrantType = keyof typeof QuadrantColors;

export interface BoardReceipt {
  id: string;
  quadrant: QuadrantType;
  title: string;
  description: string;
  author: string;
  timestamp: Date;
  votes?: {
    for: number;
    against: number;
    abstain: number;
  };
  status?: "pending" | "approved" | "rejected" | "executed";
  cosmologicalConstant?: string; // Discord snowflake reference
  incrementRef?: number; // Reference to sovereign increment
}

/**
 * Create a quadrant-colored embed for board receipts
 */
export function createBoardReceiptEmbed(receipt: BoardReceipt): EmbedBuilder {
  const color = QuadrantColors[receipt.quadrant];
  const quadrantEmoji = getQuadrantEmoji(receipt.quadrant);
  
  const embed = new EmbedBuilder()
    .setTitle(`${quadrantEmoji} ${receipt.title}`)
    .setDescription(receipt.description)
    .setColor(color)
    .setTimestamp(receipt.timestamp)
    .setFooter({ text: `Receipt ID: ${receipt.id} | Quadrant: ${receipt.quadrant}` });

  // Add author field
  embed.addFields({ name: "📝 Author", value: receipt.author, inline: true });

  // Add vote tally if present
  if (receipt.votes) {
    const total = receipt.votes.for + receipt.votes.against + receipt.votes.abstain;
    const forPercent = total > 0 ? Math.round((receipt.votes.for / total) * 100) : 0;
    
    embed.addFields({
      name: "🗳️ Council Vote",
      value: `✅ For: ${receipt.votes.for} (${forPercent}%)\n❌ Against: ${receipt.votes.against}\n⏸️ Abstain: ${receipt.votes.abstain}`,
      inline: true
    });
  }

  // Add status if present
  if (receipt.status) {
    const statusEmoji = getStatusEmoji(receipt.status);
    embed.addFields({ name: "📊 Status", value: `${statusEmoji} ${receipt.status.toUpperCase()}`, inline: true });
  }

  // Add cosmological constant (Discord snowflake) reference
  if (receipt.cosmologicalConstant) {
    embed.addFields({ 
      name: "🌌 Cosmological Constant", 
      value: `\`${receipt.cosmologicalConstant}\``, 
      inline: false 
    });
  }

  // Add increment reference for sovereignty tracking
  if (receipt.incrementRef) {
    embed.addFields({ 
      name: "📈 Increment Reference", 
      value: `#${receipt.incrementRef}`, 
      inline: true 
    });
  }

  return embed;
}

/**
 * Create a health status embed
 */
export function createHealthEmbed(status: {
  healthy: boolean;
  services: Record<string, { status: string; latency?: number }>;
  timestamp: Date;
  version: string;
}): EmbedBuilder {
  const color = status.healthy ? QuadrantColors.SWARM : QuadrantColors.ALERT;
  const statusEmoji = status.healthy ? "🟢" : "🔴";

  const embed = new EmbedBuilder()
    .setTitle(`${statusEmoji} Sovereignty Health Check`)
    .setColor(color)
    .setTimestamp(status.timestamp)
    .setDescription(status.healthy 
      ? "All systems operational. The swarm is awake." 
      : "⚠️ Some services require attention.")
    .setFooter({ text: `Version: ${status.version}` });

  // Add service statuses
  for (const [service, info] of Object.entries(status.services)) {
    const serviceEmoji = info.status === "healthy" ? "✅" : info.status === "degraded" ? "⚠️" : "❌";
    const latencyInfo = info.latency ? ` (${info.latency}ms)` : "";
    embed.addFields({ 
      name: service, 
      value: `${serviceEmoji} ${info.status}${latencyInfo}`, 
      inline: true 
    });
  }

  return embed;
}

/**
 * Create a council vote summary embed
 */
export function createCouncilVoteSummaryEmbed(vote: {
  proposalId: string;
  title: string;
  description: string;
  votes: { for: number; against: number; abstain: number };
  quorum: number;
  threshold: number;
  deadline: Date;
  outcome?: "passed" | "failed" | "pending";
}): EmbedBuilder {
  const total = vote.votes.for + vote.votes.against + vote.votes.abstain;
  const quorumMet = total >= vote.quorum;
  const forPercent = total > 0 ? Math.round((vote.votes.for / total) * 100) : 0;
  const thresholdMet = forPercent >= vote.threshold;
  
  const outcome = vote.outcome || (quorumMet && thresholdMet ? "passed" : "pending");
  const color = outcome === "passed" ? QuadrantColors.COUNCIL : 
                outcome === "failed" ? QuadrantColors.ALERT : 
                QuadrantColors.NEUTRAL;

  const embed = new EmbedBuilder()
    .setTitle(`🏛️ Council Vote: ${vote.title}`)
    .setDescription(vote.description)
    .setColor(color)
    .setTimestamp()
    .setFooter({ text: `Proposal ID: ${vote.proposalId}` });

  // Vote breakdown
  const voteBar = createProgressBar(forPercent);
  embed.addFields({
    name: "📊 Vote Breakdown",
    value: `${voteBar}\n✅ **For:** ${vote.votes.for} | ❌ **Against:** ${vote.votes.against} | ⏸️ **Abstain:** ${vote.votes.abstain}`,
    inline: false
  });

  // Quorum status
  embed.addFields({
    name: "👥 Quorum",
    value: `${total}/${vote.quorum} ${quorumMet ? "✅ Met" : "❌ Not Met"}`,
    inline: true
  });

  // Threshold status
  embed.addFields({
    name: "📈 Threshold",
    value: `${forPercent}%/${vote.threshold}% ${thresholdMet ? "✅ Met" : "❌ Not Met"}`,
    inline: true
  });

  // Deadline
  embed.addFields({
    name: "⏰ Deadline",
    value: `<t:${Math.floor(vote.deadline.getTime() / 1000)}:R>`,
    inline: true
  });

  // Outcome
  const outcomeEmoji = outcome === "passed" ? "🎉" : outcome === "failed" ? "❌" : "⏳";
  embed.addFields({
    name: "🏆 Outcome",
    value: `${outcomeEmoji} **${outcome.toUpperCase()}**`,
    inline: false
  });

  return embed;
}

/**
 * Create a treasury report embed
 */
export function createTreasuryReportEmbed(report: {
  title: string;
  period: string;
  balances: Record<string, { amount: number; currency: string; change?: number }>;
  yields: { source: string; amount: number; apy?: number }[];
  totalValue: number;
  currency: string;
}): EmbedBuilder {
  const embed = new EmbedBuilder()
    .setTitle(`💰 ${report.title}`)
    .setColor(QuadrantColors.TREASURY)
    .setTimestamp()
    .setDescription(`Treasury Report for ${report.period}`)
    .setFooter({ text: "Strategickhaos DAO LLC Treasury" });

  // Balances
  let balanceText = "";
  for (const [name, balance] of Object.entries(report.balances)) {
    const changeEmoji = balance.change && balance.change > 0 ? "📈" : 
                        balance.change && balance.change < 0 ? "📉" : "";
    const changeText = balance.change ? ` (${balance.change > 0 ? "+" : ""}${balance.change}%)` : "";
    balanceText += `**${name}:** ${balance.amount.toLocaleString()} ${balance.currency}${changeEmoji}${changeText}\n`;
  }
  embed.addFields({ name: "💼 Holdings", value: balanceText || "No holdings", inline: false });

  // Yields
  if (report.yields.length > 0) {
    let yieldText = "";
    for (const yield_ of report.yields) {
      const apyText = yield_.apy ? ` @ ${yield_.apy}% APY` : "";
      yieldText += `**${yield_.source}:** +${yield_.amount.toLocaleString()}${apyText}\n`;
    }
    embed.addFields({ name: "📊 Yield Sources", value: yieldText, inline: false });
  }

  // Total value
  embed.addFields({
    name: "💎 Total Value",
    value: `**${report.totalValue.toLocaleString()} ${report.currency}**`,
    inline: false
  });

  return embed;
}

/**
 * Create an operations status embed
 */
export function createOperationsEmbed(ops: {
  title: string;
  deployments: { service: string; version: string; status: string; environment: string }[];
  metrics: { name: string; value: string; trend?: "up" | "down" | "stable" }[];
}): EmbedBuilder {
  const embed = new EmbedBuilder()
    .setTitle(`⚙️ ${ops.title}`)
    .setColor(QuadrantColors.OPERATIONS)
    .setTimestamp()
    .setFooter({ text: "Sovereignty Infrastructure" });

  // Deployments
  if (ops.deployments.length > 0) {
    let deployText = "";
    for (const dep of ops.deployments) {
      const statusEmoji = dep.status === "running" ? "🟢" : 
                          dep.status === "pending" ? "🟡" : "🔴";
      deployText += `${statusEmoji} **${dep.service}** v${dep.version} (${dep.environment})\n`;
    }
    embed.addFields({ name: "🚀 Deployments", value: deployText, inline: false });
  }

  // Metrics
  if (ops.metrics.length > 0) {
    let metricsText = "";
    for (const metric of ops.metrics) {
      const trendEmoji = metric.trend === "up" ? "📈" : 
                         metric.trend === "down" ? "📉" : "➡️";
      metricsText += `${trendEmoji} **${metric.name}:** ${metric.value}\n`;
    }
    embed.addFields({ name: "📊 Metrics", value: metricsText, inline: false });
  }

  return embed;
}

/**
 * Create a swarm activity embed
 */
export function createSwarmActivityEmbed(activity: {
  title: string;
  contributors: { name: string; contributions: number; badge?: string }[];
  recentActions: { action: string; actor: string; timestamp: Date }[];
  totalMembers: number;
  activeToday: number;
}): EmbedBuilder {
  const embed = new EmbedBuilder()
    .setTitle(`🐝 ${activity.title}`)
    .setColor(QuadrantColors.SWARM)
    .setTimestamp()
    .setDescription("The swarm is alive and building.")
    .setFooter({ text: "Strategickhaos Swarm Intelligence" });

  // Community stats
  embed.addFields({
    name: "👥 Community",
    value: `Total Members: **${activity.totalMembers}**\nActive Today: **${activity.activeToday}**`,
    inline: true
  });

  // Top contributors
  if (activity.contributors.length > 0) {
    let contribText = "";
    for (const [index, contrib] of activity.contributors.slice(0, 5).entries()) {
      const medal = index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "🏅";
      const badge = contrib.badge ? ` ${contrib.badge}` : "";
      contribText += `${medal} **${contrib.name}**${badge}: ${contrib.contributions}\n`;
    }
    embed.addFields({ name: "🏆 Top Contributors", value: contribText, inline: true });
  }

  // Recent actions
  if (activity.recentActions.length > 0) {
    let actionsText = "";
    for (const action of activity.recentActions.slice(0, 5)) {
      const relativeTime = `<t:${Math.floor(action.timestamp.getTime() / 1000)}:R>`;
      actionsText += `• ${action.action} by **${action.actor}** ${relativeTime}\n`;
    }
    embed.addFields({ name: "⚡ Recent Activity", value: actionsText, inline: false });
  }

  return embed;
}

// Helper functions
function getQuadrantEmoji(quadrant: QuadrantType): string {
  const emojis: Record<QuadrantType, string> = {
    COUNCIL: "🏛️",
    TREASURY: "💰",
    OPERATIONS: "⚙️",
    SWARM: "🐝",
    ALERT: "🚨",
    NEUTRAL: "📋"
  };
  return emojis[quadrant];
}

function getStatusEmoji(status: string): string {
  const statusEmojis: Record<string, string> = {
    pending: "⏳",
    approved: "✅",
    rejected: "❌",
    executed: "🚀"
  };
  return statusEmojis[status] || "📋";
}

function createProgressBar(percent: number): string {
  const filled = Math.round(percent / 10);
  const empty = 10 - filled;
  return `[${"█".repeat(filled)}${"░".repeat(empty)}] ${percent}%`;
}

export default {
  QuadrantColors,
  createBoardReceiptEmbed,
  createHealthEmbed,
  createCouncilVoteSummaryEmbed,
  createTreasuryReportEmbed,
  createOperationsEmbed,
  createSwarmActivityEmbed
};
