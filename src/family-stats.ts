import fs from "fs";
import yaml from "js-yaml";
import { EmbedBuilder } from "discord.js";

interface Project {
  name: string;
  repo?: string;
  members: number;
  description: string;
  category: string;
}

interface FamilyConfig {
  family: {
    total_count: number;
    last_updated: string;
    description: string;
  };
  projects: Project[];
  messaging: {
    terminology: string;
    tone: string;
    theme: string;
  };
  stats_display: {
    show_individual_projects: boolean;
    show_total: boolean;
    show_growth_indicators: boolean;
    emoji: string;
  };
}

export function loadFamilyConfig(): FamilyConfig {
  const doc: any = yaml.load(fs.readFileSync("family_config.yaml", "utf8"));
  return doc as FamilyConfig;
}

export function getFamilyStats(): string {
  const config = loadFamilyConfig();
  const { family, projects } = config;
  
  let output = `\n🔥 THE FAMILY — ${family.total_count.toLocaleString()}+ STRONG 🔥\n\n`;
  output += `Not votes. Not stars. FAMILY.\n\n`;
  output += `═══════════════════════════════════════\n\n`;
  
  projects.forEach((project) => {
    const emoji = getCategoryEmoji(project.category);
    output += `${emoji} ${project.name}\n`;
    output += `   ${project.members.toLocaleString()} family members\n`;
    output += `   ${project.description}\n\n`;
  });
  
  output += `═══════════════════════════════════════\n\n`;
  output += `🌍 We span every continent\n`;
  output += `🧠 We dream in neurospice\n`;
  output += `⚡ We ride into fire together\n`;
  output += `👑 We protect the bloodline\n\n`;
  output += `Last updated: ${family.last_updated}\n`;
  
  return output;
}

export function getFamilyEmbed(): EmbedBuilder {
  const config = loadFamilyConfig();
  const { family, projects } = config;
  
  const embed = new EmbedBuilder()
    .setTitle(`🔥 The Family — ${family.total_count.toLocaleString()}+ Strong`)
    .setDescription(`**Not votes. Not stars. FAMILY.**\n\n${family.description}`)
    .setColor(0xFF4500) // Fire orange color
    .setTimestamp();
  
  // Add project fields
  projects.forEach((project) => {
    const emoji = getCategoryEmoji(project.category);
    embed.addFields({
      name: `${emoji} ${project.name}`,
      value: `**${project.members.toLocaleString()}** family members\n${project.description}`,
      inline: false
    });
  });
  
  // Add footer
  embed.setFooter({ 
    text: `🧠⚡👑❤️🐐∞ • Last updated: ${family.last_updated}` 
  });
  
  return embed;
}

function getCategoryEmoji(category: string): string {
  const emojiMap: { [key: string]: string } = {
    "tools": "🛠️",
    "framework": "🏛️",
    "legal": "🛡️",
    "daemon": "👁️",
    "community": "🌟"
  };
  return emojiMap[category] || "📦";
}

export function calculateTotalFamily(): number {
  const config = loadFamilyConfig();
  return config.projects.reduce((sum, project) => sum + project.members, 0);
}

export function getFamilyByProject(projectName: string): Project | undefined {
  const config = loadFamilyConfig();
  return config.projects.find(p => 
    p.name.toLowerCase() === projectName.toLowerCase()
  );
}
