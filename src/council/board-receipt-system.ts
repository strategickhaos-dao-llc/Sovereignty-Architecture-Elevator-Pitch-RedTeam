/**
 * Board Receipt System for Strategickhaos DAO LLC
 * 
 * Tracks and announces board decisions, votes, and governance actions
 * with quadrant-colored Discord embeds.
 */

import { v4 as uuid } from "uuid";
import { REST } from "discord.js";
import {
  BoardReceipt,
  QuadrantType,
  createBoardReceiptEmbed,
  createCouncilVoteSummaryEmbed
} from "./quadrant-embeds.js";

export interface BoardMinutes {
  id: string;
  date: Date;
  attendees: string[];
  agenda: string[];
  decisions: BoardDecision[];
  actionItems: ActionItem[];
  nextMeeting?: Date;
  cosmologicalConstant: string; // Discord message snowflake
}

export interface BoardDecision {
  id: string;
  quadrant: QuadrantType;
  title: string;
  description: string;
  proposedBy: string;
  secondedBy?: string;
  votes: { for: number; against: number; abstain: number };
  outcome: "passed" | "failed" | "tabled";
  incrementRef: number;
}

export interface ActionItem {
  id: string;
  description: string;
  assignee: string;
  dueDate: Date;
  status: "pending" | "in_progress" | "completed";
}

export class BoardReceiptSystem {
  private receipts: Map<string, BoardReceipt> = new Map();
  private minutes: Map<string, BoardMinutes> = new Map();
  private rest: REST | null = null;
  private channelId: string | null = null;
  private incrementCounter: number = 3449; // Starting from the mentioned increment

  constructor(discordToken?: string, channelId?: string) {
    if (discordToken) {
      this.rest = new REST({ version: "10" }).setToken(discordToken);
    }
    this.channelId = channelId || null;
  }

  /**
   * Initialize with Discord REST API
   */
  setDiscordConfig(token: string, channelId: string): void {
    this.rest = new REST({ version: "10" }).setToken(token);
    this.channelId = channelId;
  }

  /**
   * Get the next increment number for sovereignty tracking
   */
  getNextIncrement(): number {
    return ++this.incrementCounter;
  }

  /**
   * Create a new board receipt for a governance action
   */
  async createReceipt(data: {
    quadrant: QuadrantType;
    title: string;
    description: string;
    author: string;
    votes?: { for: number; against: number; abstain: number };
    status?: "pending" | "approved" | "rejected" | "executed";
    cosmologicalConstant?: string;
  }): Promise<BoardReceipt> {
    const receipt: BoardReceipt = {
      id: uuid(),
      quadrant: data.quadrant,
      title: data.title,
      description: data.description,
      author: data.author,
      timestamp: new Date(),
      votes: data.votes,
      status: data.status || "pending",
      cosmologicalConstant: data.cosmologicalConstant,
      incrementRef: this.getNextIncrement()
    };

    this.receipts.set(receipt.id, receipt);

    // Post to Discord if configured
    if (this.rest && this.channelId) {
      try {
        const embed = createBoardReceiptEmbed(receipt);
        const response = await this.rest.post(`/channels/${this.channelId}/messages`, {
          body: { embeds: [embed.toJSON()] }
        }) as { id: string };

        // Update with the Discord message snowflake as the cosmological constant
        receipt.cosmologicalConstant = response.id;
        this.receipts.set(receipt.id, receipt);
      } catch (error) {
        console.error("Failed to post board receipt to Discord:", error);
      }
    }

    return receipt;
  }

  /**
   * Get a receipt by ID
   */
  getReceipt(id: string): BoardReceipt | undefined {
    return this.receipts.get(id);
  }

  /**
   * List all receipts, optionally filtered by quadrant
   */
  listReceipts(filter?: { quadrant?: QuadrantType; status?: string }): BoardReceipt[] {
    let results = Array.from(this.receipts.values());
    
    if (filter?.quadrant) {
      results = results.filter(r => r.quadrant === filter.quadrant);
    }
    if (filter?.status) {
      results = results.filter(r => r.status === filter.status);
    }
    
    return results.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
  }

  /**
   * Record board meeting minutes
   */
  async recordMinutes(data: {
    attendees: string[];
    agenda: string[];
    decisions: Omit<BoardDecision, "id" | "incrementRef">[];
    actionItems: Omit<ActionItem, "id" | "status">[];
    nextMeeting?: Date;
  }): Promise<BoardMinutes> {
    const minutes: BoardMinutes = {
      id: uuid(),
      date: new Date(),
      attendees: data.attendees,
      agenda: data.agenda,
      decisions: data.decisions.map(d => ({
        ...d,
        id: uuid(),
        incrementRef: this.getNextIncrement()
      })),
      actionItems: data.actionItems.map(a => ({
        ...a,
        id: uuid(),
        status: "pending" as const
      })),
      nextMeeting: data.nextMeeting,
      cosmologicalConstant: "" // Will be set after Discord post
    };

    this.minutes.set(minutes.id, minutes);

    // Create receipts for each decision
    for (const decision of minutes.decisions) {
      await this.createReceipt({
        quadrant: decision.quadrant,
        title: decision.title,
        description: decision.description,
        author: decision.proposedBy,
        votes: decision.votes,
        status: decision.outcome === "passed" ? "approved" : 
                decision.outcome === "failed" ? "rejected" : "pending"
      });
    }

    // Post summary to Discord if configured
    if (this.rest && this.channelId) {
      try {
        const summaryEmbed = this.createMinutesSummaryEmbed(minutes);
        const response = await this.rest.post(`/channels/${this.channelId}/messages`, {
          body: { embeds: [summaryEmbed] }
        }) as { id: string };

        minutes.cosmologicalConstant = response.id;
        this.minutes.set(minutes.id, minutes);
      } catch (error) {
        console.error("Failed to post board minutes to Discord:", error);
      }
    }

    return minutes;
  }

  /**
   * Get board minutes by ID
   */
  getMinutes(id: string): BoardMinutes | undefined {
    return this.minutes.get(id);
  }

  /**
   * Create a council vote and post to Discord
   */
  async createCouncilVote(vote: {
    proposalId: string;
    title: string;
    description: string;
    votes: { for: number; against: number; abstain: number };
    quorum: number;
    threshold: number;
    deadline: Date;
    outcome?: "passed" | "failed" | "pending";
  }): Promise<string | null> {
    if (!this.rest || !this.channelId) {
      console.warn("Discord not configured, skipping council vote post");
      return null;
    }

    try {
      const embed = createCouncilVoteSummaryEmbed(vote);
      const response = await this.rest.post(`/channels/${this.channelId}/messages`, {
        body: { embeds: [embed.toJSON()] }
      }) as { id: string };

      return response.id;
    } catch (error) {
      console.error("Failed to post council vote to Discord:", error);
      return null;
    }
  }

  /**
   * Create a summary embed for board minutes
   */
  private createMinutesSummaryEmbed(minutes: BoardMinutes): object {
    const passedDecisions = minutes.decisions.filter(d => d.outcome === "passed");
    const failedDecisions = minutes.decisions.filter(d => d.outcome === "failed");
    const tabledDecisions = minutes.decisions.filter(d => d.outcome === "tabled");

    let decisionsText = "";
    for (const decision of minutes.decisions) {
      const outcomeEmoji = decision.outcome === "passed" ? "✅" : 
                           decision.outcome === "failed" ? "❌" : "⏸️";
      decisionsText += `${outcomeEmoji} **${decision.title}** (#${decision.incrementRef})\n`;
    }

    let actionItemsText = "";
    for (const item of minutes.actionItems) {
      actionItemsText += `• ${item.description} → **${item.assignee}** (Due: <t:${Math.floor(item.dueDate.getTime() / 1000)}:D>)\n`;
    }

    const fields = [
      {
        name: "👥 Attendees",
        value: minutes.attendees.join(", ") || "None recorded",
        inline: false
      },
      {
        name: "📋 Agenda Items",
        value: minutes.agenda.map(a => `• ${a}`).join("\n") || "No agenda",
        inline: false
      },
      {
        name: `📊 Decisions (${passedDecisions.length}/${minutes.decisions.length} passed)`,
        value: decisionsText || "No decisions",
        inline: false
      }
    ];

    if (minutes.actionItems.length > 0) {
      fields.push({
        name: "📝 Action Items",
        value: actionItemsText,
        inline: false
      });
    }

    if (minutes.nextMeeting) {
      fields.push({
        name: "📅 Next Meeting",
        value: `<t:${Math.floor(minutes.nextMeeting.getTime() / 1000)}:F>`,
        inline: false
      });
    }

    return {
      title: `📜 Board Meeting Minutes - ${minutes.date.toLocaleDateString()}`,
      description: "Strategickhaos DAO LLC Board of Directors Meeting",
      color: 0x9B59B6, // Council purple
      timestamp: minutes.date.toISOString(),
      fields,
      footer: {
        text: `Meeting ID: ${minutes.id}`
      }
    };
  }

  /**
   * Get system statistics
   */
  getStats(): {
    totalReceipts: number;
    receiptsByQuadrant: Record<string, number>;
    totalMinutes: number;
    currentIncrement: number;
  } {
    const byQuadrant: Record<string, number> = {};
    
    for (const receipt of this.receipts.values()) {
      byQuadrant[receipt.quadrant] = (byQuadrant[receipt.quadrant] || 0) + 1;
    }

    return {
      totalReceipts: this.receipts.size,
      receiptsByQuadrant: byQuadrant,
      totalMinutes: this.minutes.size,
      currentIncrement: this.incrementCounter
    };
  }
}

export default BoardReceiptSystem;
