/**
 * Node137 Uplink Receipt Parser and Validator
 *
 * Handles parsing and validation of CAT PUSH receipts from the
 * Node137_Uplink_Receipt repository. These receipts serve as
 * timestamped proof-of-origin declarations for the Strategickhaos
 * sovereign system.
 */

import { z } from "zod";

/**
 * Schema for a parsed uplink receipt
 */
export const UplinkReceiptSchema = z.object({
  type: z.string(),
  node: z.number(),
  phase: z.string().optional(),
  signature: z.string(),
  message: z.string().optional(),
  declaration: z.string().optional(),
  forkPolicy: z.string().optional(),
  verifiedBy: z.string().optional(),
  timestamp: z.string(),
  rawContent: z.string(),
});

export type UplinkReceipt = z.infer<typeof UplinkReceiptSchema>;

/**
 * Result of receipt validation
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
  receipt?: UplinkReceipt;
}

/**
 * Parse a raw receipt text into structured data
 */
export function parseReceipt(content: string): UplinkReceipt | null {
  const lines = content.split("\n");

  // Extract header/type from first line (e.g., "❤️ CAT PUSH :: CP_Heart")
  const headerMatch = lines[0]?.match(/CAT PUSH\s*::\s*(\S+)/);
  const type = headerMatch?.[1] ?? "UNKNOWN";

  // Parse key-value pairs
  const fields: Record<string, string> = {};
  for (const line of lines) {
    const kvMatch = line.match(/^([A-Z_]+):\s*(.+)$/);
    if (kvMatch) {
      const [, key, value] = kvMatch;
      fields[key.toLowerCase()] = value.trim();
    }
  }

  // Handle multi-line declarations
  let declaration = fields["declaration"] ?? "";
  let inDeclaration = false;
  for (const line of lines) {
    if (line.startsWith("DECLARATION:")) {
      inDeclaration = true;
      continue;
    }
    if (inDeclaration) {
      if (line.match(/^[A-Z_]+:/)) {
        inDeclaration = false;
      } else if (line.trim()) {
        declaration += " " + line.trim();
      }
    }
  }

  const nodeStr = fields["node"];
  const node = nodeStr ? parseInt(nodeStr, 10) : 0;

  return {
    type,
    node: isNaN(node) ? 0 : node,
    phase: fields["phase"],
    signature: fields["signature"] ?? "",
    message: fields["message"],
    declaration: declaration.trim() || undefined,
    forkPolicy: fields["fork_policy"],
    verifiedBy: fields["verified_by"],
    timestamp: fields["timestamp"] ?? fields["datestamp"] ?? "",
    rawContent: content,
  };
}

/**
 * Validate a parsed receipt
 */
export function validateReceipt(receipt: UplinkReceipt): ValidationResult {
  const errors: string[] = [];

  // Check required fields
  if (!receipt.signature) {
    errors.push("Missing signature field");
  }

  if (!receipt.timestamp) {
    errors.push("Missing timestamp field");
  }

  if (receipt.node === 0) {
    errors.push("Invalid or missing node number");
  }

  // Validate signature format
  if (receipt.signature && !receipt.signature.includes("Strategickhaos")) {
    errors.push("Signature does not contain expected origin identifier");
  }

  // Validate timestamp format (e.g., "Mon Jun  9 17:56:42 UTC 2025")
  if (receipt.timestamp) {
    const timestampPattern = /\w{3}\s+\w{3}\s+\d+\s+\d+:\d+:\d+\s+\w+\s+\d{4}/;
    if (!timestampPattern.test(receipt.timestamp)) {
      errors.push("Invalid timestamp format");
    }
  }

  // Validate with Zod schema
  const result = UplinkReceiptSchema.safeParse(receipt);
  if (!result.success) {
    errors.push(...result.error.errors.map((e) => e.message));
  }

  return {
    valid: errors.length === 0,
    errors,
    receipt: errors.length === 0 ? receipt : undefined,
  };
}

/**
 * Parse filename to extract receipt metadata
 */
export function parseReceiptFilename(
  filename: string
): { type: string; timestamp: string } | null {
  // Format: CP_Name_Type_YYYY-MM-DD_HH-MM-SS.txt
  const match = filename.match(/^(CP_[\w_]+)_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.txt$/);
  if (!match) return null;

  return {
    type: match[1],
    timestamp: match[2].replace(/_/g, " ").replace(/-/g, ":").slice(0, 10) +
      " " +
      match[2].slice(11).replace(/-/g, ":"),
  };
}

/**
 * Generate a summary of the receipt for display
 */
export function summarizeReceipt(receipt: UplinkReceipt): string {
  const lines = [
    `📋 **Receipt: ${receipt.type}**`,
    `🔗 Node: ${receipt.node}`,
    `🔏 Signature: ${receipt.signature}`,
  ];

  if (receipt.message) {
    lines.push(`💬 Message: ${receipt.message}`);
  }

  if (receipt.timestamp) {
    lines.push(`⏰ Timestamp: ${receipt.timestamp}`);
  }

  if (receipt.verifiedBy) {
    lines.push(`✅ Verified by: ${receipt.verifiedBy}`);
  }

  return lines.join("\n");
}
