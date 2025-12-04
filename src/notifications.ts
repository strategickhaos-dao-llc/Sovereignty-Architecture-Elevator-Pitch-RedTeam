import { REST, EmbedBuilder } from "discord.js";

export interface NotificationOptions {
  title: string;
  message: string;
  level?: "info" | "warning" | "error" | "success";
  mentionUsers?: string[];
  mentionRoles?: string[];
}

const LEVEL_COLORS = {
  info: 0x2f81f7,     // Blue
  warning: 0xf0ad4e,  // Yellow/Orange
  error: 0xd73a49,    // Red
  success: 0x28a745   // Green
};

const LEVEL_EMOJIS = {
  info: "ℹ️",
  warning: "⚠️",
  error: "❌",
  success: "✅"
};

export class NotificationService {
  private rest: REST;
  private channelIds: Record<string, string>;

  constructor(rest: REST, channelIds: Record<string, string>) {
    this.rest = rest;
    this.channelIds = channelIds;
  }

  /**
   * Build mentions string for users and roles
   */
  private buildMentions(options: NotificationOptions): string {
    const mentions: string[] = [];
    
    if (options.mentionUsers?.length) {
      mentions.push(...options.mentionUsers.map(id => `<@${id}>`));
    }
    
    if (options.mentionRoles?.length) {
      mentions.push(...options.mentionRoles.map(id => `<@&${id}>`));
    }
    
    return mentions.length > 0 ? mentions.join(" ") + "\n" : "";
  }

  /**
   * Send a notification to a specific channel
   */
  async sendToChannel(channelId: string, options: NotificationOptions): Promise<void> {
    const level = options.level || "info";
    const emoji = LEVEL_EMOJIS[level];
    const color = LEVEL_COLORS[level];
    const mentions = this.buildMentions(options);

    const embed = new EmbedBuilder()
      .setTitle(`${emoji} ${options.title}`)
      .setDescription(options.message)
      .setColor(color)
      .setTimestamp();

    await this.rest.post(`/channels/${channelId}/messages`, {
      body: {
        content: mentions || undefined,
        embeds: [embed.toJSON()]
      }
    } as any);
  }

  /**
   * Send a notification to the alerts channel
   */
  async alert(options: NotificationOptions): Promise<void> {
    const alertsChannel = this.channelIds.alerts;
    if (!alertsChannel) {
      throw new Error("Alerts channel not configured");
    }
    await this.sendToChannel(alertsChannel, { ...options, level: options.level || "warning" });
  }

  /**
   * Send a notification to the dev feed channel
   */
  async devFeed(options: NotificationOptions): Promise<void> {
    const devFeedChannel = this.channelIds.dev_feed;
    if (!devFeedChannel) {
      throw new Error("Dev feed channel not configured");
    }
    await this.sendToChannel(devFeedChannel, { ...options, level: options.level || "info" });
  }

  /**
   * Send a notification to the agents channel
   */
  async agents(options: NotificationOptions): Promise<void> {
    const agentsChannel = this.channelIds.agents;
    if (!agentsChannel) {
      throw new Error("Agents channel not configured");
    }
    await this.sendToChannel(agentsChannel, options);
  }

  /**
   * Send a deployment notification
   */
  async deployment(options: NotificationOptions): Promise<void> {
    const deploymentsChannel = this.channelIds.deployments;
    if (!deploymentsChannel) {
      throw new Error("Deployments channel not configured");
    }
    await this.sendToChannel(deploymentsChannel, options);
  }

  /**
   * Send a PR notification
   */
  async prNotification(options: NotificationOptions): Promise<void> {
    const prsChannel = this.channelIds.prs;
    if (!prsChannel) {
      throw new Error("PRs channel not configured");
    }
    await this.sendToChannel(prsChannel, options);
  }

  /**
   * Send a direct message to a user
   */
  async sendDM(userId: string, options: NotificationOptions): Promise<void> {
    const level = options.level || "info";
    const emoji = LEVEL_EMOJIS[level];
    const color = LEVEL_COLORS[level];

    // Create DM channel
    const dmChannel = await this.rest.post("/users/@me/channels", {
      body: { recipient_id: userId }
    } as any) as { id: string };

    const embed = new EmbedBuilder()
      .setTitle(`${emoji} ${options.title}`)
      .setDescription(options.message)
      .setColor(color)
      .setTimestamp();

    await this.rest.post(`/channels/${dmChannel.id}/messages`, {
      body: { embeds: [embed.toJSON()] }
    } as any);
  }

  /**
   * Broadcast notification to multiple channels
   */
  async broadcast(channelIds: string[], options: NotificationOptions): Promise<void> {
    await Promise.all(
      channelIds.map(channelId => this.sendToChannel(channelId, options))
    );
  }
}

/**
 * Create a notification service instance
 */
export function createNotificationService(rest: REST, channelIds: Record<string, string>): NotificationService {
  return new NotificationService(rest, channelIds);
}
