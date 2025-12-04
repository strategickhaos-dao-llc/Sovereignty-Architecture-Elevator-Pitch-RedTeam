/**
 * Sovereign Architect's Chronicle - Discord Integration
 * 
 * Discord slash commands and embeds for displaying chronicle entries
 * in the Sovereign Control Deck.
 */

import { REST, EmbedBuilder, SlashCommandBuilder, type APIEmbed, type RESTPostAPIChannelMessageJSONBody } from "discord.js";
import { getChronicleStore } from "./store.js";
import { CATEGORY_METADATA, STATUS_METADATA, type ChronicleCategory, type ChronicleStatus } from "./types.js";

/**
 * Create chronicle slash command definitions
 */
export function getChronicleCommands(): SlashCommandBuilder[] {
  const chronicleCommand = new SlashCommandBuilder()
    .setName("chronicle")
    .setDescription("Sovereign Architect's Chronicle - Neural Logbook")
    .addSubcommand(sub =>
      sub
        .setName("timeline")
        .setDescription("Display the chronicle timeline grouped by category")
    )
    .addSubcommand(sub =>
      sub
        .setName("roadmap")
        .setDescription("Display the architecture roadmap by development phase")
    )
    .addSubcommand(sub =>
      sub
        .setName("stats")
        .setDescription("Show chronicle statistics and recent activity")
    )
    .addSubcommand(sub =>
      sub
        .setName("category")
        .setDescription("View entries in a specific category")
        .addStringOption(opt =>
          opt
            .setName("name")
            .setDescription("Category to view")
            .setRequired(true)
            .addChoices(
              { name: "📊 Observability", value: "observability" },
              { name: "⚖️ Governance", value: "governance" },
              { name: "🧬 Research", value: "research" },
              { name: "🔮 Philosophy", value: "philosophy" },
              { name: "🪞 Visualization", value: "visualization" },
              { name: "⚛️ Frontier", value: "frontier" },
              { name: "🏗️ Infrastructure", value: "infrastructure" },
              { name: "🔗 Integration", value: "integration" },
              { name: "🔐 Security", value: "security" },
              { name: "📚 Documentation", value: "documentation" }
            )
        )
    )
    .addSubcommand(sub =>
      sub
        .setName("add")
        .setDescription("Add a new chronicle entry")
        .addStringOption(opt =>
          opt.setName("title").setDescription("Entry title").setRequired(true)
        )
        .addStringOption(opt =>
          opt
            .setName("category")
            .setDescription("Entry category")
            .setRequired(true)
            .addChoices(
              { name: "📊 Observability", value: "observability" },
              { name: "⚖️ Governance", value: "governance" },
              { name: "🧬 Research", value: "research" },
              { name: "🔮 Philosophy", value: "philosophy" },
              { name: "🪞 Visualization", value: "visualization" },
              { name: "⚛️ Frontier", value: "frontier" },
              { name: "🏗️ Infrastructure", value: "infrastructure" },
              { name: "🔗 Integration", value: "integration" },
              { name: "🔐 Security", value: "security" },
              { name: "📚 Documentation", value: "documentation" }
            )
        )
        .addStringOption(opt =>
          opt.setName("description").setDescription("Entry description").setRequired(true)
        )
        .addIntegerOption(opt =>
          opt.setName("priority").setDescription("Priority (1=highest, 5=lowest)").setMinValue(1).setMaxValue(5)
        )
    )
    .addSubcommand(sub =>
      sub
        .setName("search")
        .setDescription("Search chronicle entries")
        .addStringOption(opt =>
          opt.setName("query").setDescription("Search query").setRequired(true)
        )
    ) as SlashCommandBuilder;

  return [chronicleCommand];
}

/**
 * Build timeline embed for Discord
 */
export function buildTimelineEmbed(): APIEmbed[] {
  const store = getChronicleStore();
  const timeline = store.generateTimeline();
  
  const embeds: APIEmbed[] = [];
  
  // Main header embed
  const headerEmbed = new EmbedBuilder()
    .setTitle("📜 " + timeline.title)
    .setDescription(timeline.description)
    .setColor(0x7B68EE)
    .setFooter({ text: `Total Entries: ${timeline.totalEntries} | Generated: ${new Date(timeline.generatedAt).toLocaleString()}` })
    .toJSON();
  
  embeds.push(headerEmbed);
  
  // Category embeds (up to 9 more to stay under Discord's 10 embed limit)
  for (const group of timeline.categoryGroups.slice(0, 9)) {
    if (group.count === 0) continue;
    
    const entriesList = group.entries
      .slice(0, 5)
      .map(e => {
        const statusMeta = STATUS_METADATA[e.status];
        const priorityStr = e.priority ? `[P${e.priority}]` : "";
        return `${statusMeta.emoji} ${priorityStr} **${e.title}**`;
      })
      .join("\n");
    
    const moreText = group.count > 5 ? `\n_...and ${group.count - 5} more_` : "";
    
    const categoryEmbed = new EmbedBuilder()
      .setTitle(`${group.emoji} ${group.displayName}`)
      .setDescription(entriesList + moreText || "_No entries yet_")
      .setColor(0x5865F2)
      .setFooter({ text: `${group.count} entries` })
      .toJSON();
    
    embeds.push(categoryEmbed);
  }
  
  return embeds;
}

/**
 * Build roadmap embed for Discord
 */
export function buildRoadmapEmbed(): APIEmbed[] {
  const store = getChronicleStore();
  const roadmap = store.generateRoadmap();
  
  const embeds: APIEmbed[] = [];
  
  // Main header embed
  const headerEmbed = new EmbedBuilder()
    .setTitle("🗺️ " + roadmap.title)
    .setDescription(roadmap.vision)
    .setColor(0x00D9FF)
    .setTimestamp(new Date(roadmap.generatedAt))
    .toJSON();
  
  embeds.push(headerEmbed);
  
  // Phase embeds
  for (const phase of roadmap.phases.slice(0, 9)) {
    const statusColors: Record<string, number> = {
      past: 0x607D8B,
      current: 0x4CAF50,
      future: 0x2196F3
    };
    
    const entriesList = phase.entries
      .slice(0, 5)
      .map(e => {
        const catMeta = CATEGORY_METADATA[e.category];
        return `${catMeta.emoji} **${e.title}**`;
      })
      .join("\n");
    
    const moreText = phase.entries.length > 5 ? `\n_...and ${phase.entries.length - 5} more_` : "";
    
    const phaseEmbed = new EmbedBuilder()
      .setTitle(phase.name)
      .setDescription(phase.description + "\n\n" + (entriesList + moreText || "_No entries_"))
      .setColor(statusColors[phase.status])
      .setFooter({ text: `${phase.entries.length} entries | Status: ${phase.status}` })
      .toJSON();
    
    embeds.push(phaseEmbed);
  }
  
  return embeds;
}

/**
 * Build stats embed for Discord
 */
export function buildStatsEmbed(): APIEmbed[] {
  const store = getChronicleStore();
  const stats = store.getStats();
  
  // Category breakdown
  const categoryBreakdown = Object.entries(stats.byCategory)
    .map(([cat, count]) => {
      const meta = CATEGORY_METADATA[cat as ChronicleCategory];
      return `${meta?.emoji || "📁"} ${meta?.displayName || cat}: **${count}**`;
    })
    .join("\n") || "_No entries yet_";
  
  // Status breakdown
  const statusBreakdown = Object.entries(stats.byStatus)
    .map(([status, count]) => {
      const meta = STATUS_METADATA[status as ChronicleStatus];
      return `${meta?.emoji || "📋"} ${meta?.displayName || status}: **${count}**`;
    })
    .join("\n") || "_No entries yet_";
  
  // Recent activity
  const recentActivity = stats.recentActivity
    .slice(0, 5)
    .map(e => {
      const catMeta = CATEGORY_METADATA[e.category];
      const statusMeta = STATUS_METADATA[e.status];
      return `${catMeta.emoji}${statusMeta.emoji} **${e.title}**`;
    })
    .join("\n") || "_No recent activity_";
  
  const mainEmbed = new EmbedBuilder()
    .setTitle("📊 Chronicle Statistics")
    .setDescription(`**Total Entries:** ${stats.totalEntries}`)
    .addFields(
      { name: "📁 By Category", value: categoryBreakdown, inline: true },
      { name: "📋 By Status", value: statusBreakdown, inline: true },
      { name: "🕐 Recent Activity", value: recentActivity, inline: false }
    )
    .setColor(0xFFD700)
    .setTimestamp()
    .toJSON();
  
  return [mainEmbed];
}

/**
 * Build category view embed for Discord
 */
export function buildCategoryEmbed(category: ChronicleCategory): APIEmbed[] {
  const store = getChronicleStore();
  const entries = store.getByCategory(category);
  const meta = CATEGORY_METADATA[category];
  
  const entriesList = entries
    .slice(0, 15)
    .map((e, i) => {
      const statusMeta = STATUS_METADATA[e.status];
      const priorityStr = e.priority ? `[P${e.priority}]` : "";
      return `${i + 1}. ${statusMeta.emoji} ${priorityStr} **${e.title}**\n   _${e.description.slice(0, 60)}${e.description.length > 60 ? "..." : ""}_`;
    })
    .join("\n\n") || "_No entries in this category yet_";
  
  const moreText = entries.length > 15 ? `\n\n_...and ${entries.length - 15} more entries_` : "";
  
  const embed = new EmbedBuilder()
    .setTitle(`${meta.emoji} ${meta.displayName}`)
    .setDescription(meta.description + "\n\n" + entriesList + moreText)
    .setColor(0x9B59B6)
    .setFooter({ text: `${entries.length} total entries` })
    .setTimestamp()
    .toJSON();
  
  return [embed];
}

/**
 * Build search results embed for Discord
 */
export function buildSearchEmbed(query: string): APIEmbed[] {
  const store = getChronicleStore();
  const results = store.search(query);
  
  const resultsList = results
    .slice(0, 10)
    .map((e, i) => {
      const catMeta = CATEGORY_METADATA[e.category];
      const statusMeta = STATUS_METADATA[e.status];
      return `${i + 1}. ${catMeta.emoji}${statusMeta.emoji} **${e.title}**\n   _${e.description.slice(0, 50)}..._`;
    })
    .join("\n\n") || "_No matching entries found_";
  
  const embed = new EmbedBuilder()
    .setTitle(`🔍 Search Results: "${query}"`)
    .setDescription(resultsList)
    .setColor(0x3498DB)
    .setFooter({ text: `Found ${results.length} matching entries` })
    .setTimestamp()
    .toJSON();
  
  return [embed];
}

/**
 * Build new entry confirmation embed for Discord
 */
export function buildNewEntryEmbed(entry: {
  id: string;
  title: string;
  category: ChronicleCategory;
  description: string;
  status: ChronicleStatus;
  author: string;
  priority?: number;
}): APIEmbed[] {
  const catMeta = CATEGORY_METADATA[entry.category];
  const statusMeta = STATUS_METADATA[entry.status];
  
  const embed = new EmbedBuilder()
    .setTitle(`✨ New Chronicle Entry Created`)
    .setDescription(`**${entry.title}**`)
    .addFields(
      { name: "Category", value: `${catMeta.emoji} ${catMeta.displayName}`, inline: true },
      { name: "Status", value: `${statusMeta.emoji} ${statusMeta.displayName}`, inline: true },
      { name: "Priority", value: entry.priority ? `P${entry.priority}` : "Not set", inline: true },
      { name: "Description", value: entry.description.slice(0, 200) + (entry.description.length > 200 ? "..." : ""), inline: false }
    )
    .setColor(statusMeta.color)
    .setFooter({ text: `ID: ${entry.id} | Author: ${entry.author}` })
    .setTimestamp()
    .toJSON();
  
  return [embed];
}

/**
 * Send chronicle embeds to a Discord channel
 */
export async function sendChronicleToChannel(
  rest: REST,
  channelId: string,
  embeds: APIEmbed[]
): Promise<void> {
  const body: RESTPostAPIChannelMessageJSONBody = { embeds };
  await rest.post(`/channels/${channelId}/messages`, { body });
}
