/**
 * Uplink Receipt HTTP Routes
 *
 * Provides REST endpoints for receiving and processing
 * Node137 Uplink Receipts with Discord notification integration.
 */

import type { Request, Response } from "express";
import { REST } from "discord.js";
import { parseReceipt, validateReceipt, summarizeReceipt } from "./receipt.js";

export interface UplinkRouteConfig {
  channelId: string;
}

/**
 * Create uplink receipt route handler
 */
export function uplinkRoutes(rest: REST, config: UplinkRouteConfig) {
  return async (req: Request, res: Response) => {
    try {
      // Accept receipt content from request body
      const { content, filename } = req.body as {
        content?: string;
        filename?: string;
      };

      if (!content) {
        return res.status(400).json({
          error: "Missing receipt content",
          details: "Request body must include 'content' field with receipt text",
        });
      }

      // Parse the receipt
      const receipt = parseReceipt(content);
      if (!receipt) {
        return res.status(400).json({
          error: "Failed to parse receipt",
          details: "Content does not match expected receipt format",
        });
      }

      // Validate the receipt
      const validation = validateReceipt(receipt);

      if (!validation.valid) {
        // Still process but note validation issues
        console.warn(`Receipt validation warnings for ${receipt.type}:`, validation.errors);
      }

      // Generate summary for Discord
      const summary = summarizeReceipt(receipt);

      // Send to Discord
      const embed = {
        title: `🔗 Uplink Receipt: ${receipt.type}`,
        description: summary,
        color: validation.valid ? 0x00ff00 : 0xffaa00, // green for valid, amber for warnings
        fields: [
          {
            name: "Node",
            value: String(receipt.node),
            inline: true,
          },
          {
            name: "Status",
            value: validation.valid ? "✅ Valid" : "⚠️ Warnings",
            inline: true,
          },
        ],
        footer: {
          text: filename ? `File: ${filename}` : "Submitted via API",
        },
        timestamp: new Date().toISOString(),
      };

      if (!validation.valid && validation.errors.length > 0) {
        embed.fields.push({
          name: "Validation Notes",
          value: validation.errors.join("\n"),
          inline: false,
        });
      }

      // Type assertion needed for Discord.js REST API compatibility
      // This pattern is used consistently throughout the codebase (see routes/github.ts)
      await rest.post(`/channels/${config.channelId}/messages`, {
        body: { embeds: [embed] },
      } as Parameters<typeof rest.post>[1]);

      return res.json({
        success: true,
        receipt: {
          type: receipt.type,
          node: receipt.node,
          timestamp: receipt.timestamp,
          valid: validation.valid,
        },
        validation: {
          valid: validation.valid,
          errors: validation.errors,
        },
      });
    } catch (error) {
      console.error("Error processing uplink receipt:", error);
      return res.status(500).json({
        error: "Internal server error",
        details: error instanceof Error ? error.message : "Unknown error",
      });
    }
  };
}

/**
 * Batch receipt processing endpoint
 */
export function uplinkBatchRoutes(rest: REST, config: UplinkRouteConfig) {
  return async (req: Request, res: Response) => {
    try {
      const { receipts } = req.body as {
        receipts?: Array<{ content: string; filename?: string }>;
      };

      if (!receipts || !Array.isArray(receipts)) {
        return res.status(400).json({
          error: "Missing receipts array",
          details: "Request body must include 'receipts' array",
        });
      }

      const results = [];
      const validCount = { valid: 0, invalid: 0 };

      for (const item of receipts) {
        const receipt = parseReceipt(item.content);
        if (!receipt) {
          results.push({
            filename: item.filename,
            success: false,
            error: "Failed to parse",
          });
          validCount.invalid++;
          continue;
        }

        const validation = validateReceipt(receipt);
        results.push({
          filename: item.filename,
          type: receipt.type,
          node: receipt.node,
          timestamp: receipt.timestamp,
          valid: validation.valid,
          errors: validation.errors,
        });

        if (validation.valid) {
          validCount.valid++;
        } else {
          validCount.invalid++;
        }
      }

      // Send summary to Discord
      await rest.post(`/channels/${config.channelId}/messages`, {
        body: {
          embeds: [
            {
              title: "📦 Batch Uplink Receipt Processing",
              description: `Processed ${receipts.length} receipts`,
              color: validCount.invalid === 0 ? 0x00ff00 : 0xffaa00,
              fields: [
                {
                  name: "Valid",
                  value: String(validCount.valid),
                  inline: true,
                },
                {
                  name: "Invalid/Warnings",
                  value: String(validCount.invalid),
                  inline: true,
                },
              ],
              timestamp: new Date().toISOString(),
            },
          ],
        },
      } as Parameters<typeof rest.post>[1]);

      return res.json({
        success: true,
        processed: receipts.length,
        summary: validCount,
        results,
      });
    } catch (error) {
      console.error("Error processing batch uplink receipts:", error);
      return res.status(500).json({
        error: "Internal server error",
        details: error instanceof Error ? error.message : "Unknown error",
      });
    }
  };
}
