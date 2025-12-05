import type { Request, Response } from "express";
import crypto from "crypto";
import { REST } from "discord.js";

/**
 * Azure Pipeline Webhook Handler
 * Routes pipeline failure notifications to Discord channels
 */

interface AzurePipelinePayload {
  event: "build.started" | "build.failed" | "build.completed" | "release.started" | "release.failed" | "release.completed";
  repo: string;
  pipeline: string;
  commit: string;
  logs_url?: string;
  error?: string;
  duration?: number;
  actor?: string;
  branch?: string;
}

interface ChannelIds {
  deployments: string;
  alerts: string;
  prs: string;
}

// Patterns to redact from error messages for security
const SENSITIVE_PATTERNS = [
  /api[_-]?key\s*[:=]\s*\S+/gi,
  /password\s*[:=]\s*\S+/gi,
  /token\s*[:=]\s*\S+/gi,
  /Bearer\s+[A-Za-z0-9._-]+/g,
  /secret\s*[:=]\s*\S+/gi,
  /\/home\/[^\/]+/g,  // Redact home directory paths
  /\/var\/[^\s]+/g,   // Redact var paths
];

function sanitizeError(error: string): string {
  let sanitized = error;
  for (const pattern of SENSITIVE_PATTERNS) {
    sanitized = sanitized.replace(pattern, "[REDACTED]");
  }
  return sanitized.substring(0, 500);
}

function verifySignature(secret: string, raw: string, sig: string): boolean {
  if (!secret) {
    console.warn("HMAC secret not configured - signature verification disabled");
    return true; // Allow in development, but log warning
  }
  if (!sig) return false;
  
  // Support both raw hex and prefixed signatures (e.g., 'sha256=...')
  const sigValue = sig.startsWith("sha256=") ? sig.substring(7) : sig;
  const computed = crypto.createHmac("sha256", secret).update(raw).digest("hex");
  
  try {
    return crypto.timingSafeEqual(
      Buffer.from(computed, 'hex'),
      Buffer.from(sigValue, 'hex')
    );
  } catch {
    // If buffers have different lengths or invalid hex, return false
    return false;
  }
}

function getStatusEmoji(event: string): string {
  if (event.includes("failed")) return "🚨";
  if (event.includes("completed")) return "✅";
  if (event.includes("started")) return "🔄";
  return "📦";
}

function getStatusColor(event: string): number {
  if (event.includes("failed")) return 0xff0000;  // Red
  if (event.includes("completed")) return 0x28a745;  // Green
  if (event.includes("started")) return 0x17a2b8;  // Blue
  return 0x6c757d;  // Gray
}

export function azurePipelineRoutes(rest: REST, channelIds: ChannelIds, secret: string) {
  return async (req: Request, res: Response) => {
    const sig = req.get("X-Sig") || "";
    const raw = (req as any).rawBody;
    
    if (!verifySignature(secret, raw, sig)) {
      console.error("Invalid signature for Azure Pipeline webhook");
      return res.status(401).json({ error: "Invalid signature" });
    }
    
    const payload: AzurePipelinePayload = req.body;
    const { event, repo, pipeline, commit, logs_url, error, duration, actor, branch } = payload;
    
    const emoji = getStatusEmoji(event);
    const color = getStatusColor(event);
    const channelId = event.includes("failed") ? channelIds.alerts : channelIds.deployments;
    
    // Build embed fields
    const fields: Array<{ name: string; value: string; inline?: boolean }> = [
      { name: "Repository", value: repo || "Unknown", inline: true },
      { name: "Pipeline", value: pipeline || "Unknown", inline: true },
      { name: "Commit", value: commit ? `\`${commit.substring(0, 7)}\`` : "Unknown", inline: true }
    ];
    
    if (branch) {
      fields.push({ name: "Branch", value: branch, inline: true });
    }
    
    if (actor) {
      fields.push({ name: "Triggered By", value: actor, inline: true });
    }
    
    if (duration !== undefined) {
      fields.push({ name: "Duration", value: `${duration}s`, inline: true });
    }
    
    if (error) {
      // Sanitize error message before displaying
      const sanitizedError = sanitizeError(error);
      fields.push({ name: "Error", value: `\`\`\`${sanitizedError}\`\`\``, inline: false });
    }
    
    const embed: Record<string, unknown> = {
      title: `${emoji} Pipeline ${event.replace(".", ": ").replace("build.", "Build ").replace("release.", "Release ")}`,
      description: event.includes("failed") 
        ? `Security verification pipeline has failed. React with 🤖 for AI diagnosis or ✅ to retry.`
        : `Pipeline event received for ${repo}`,
      color,
      fields,
      timestamp: new Date().toISOString()
    };
    
    // Add action buttons as components if logs_url exists
    if (logs_url) {
      fields.push({ 
        name: "Actions", 
        value: `[View Logs](${logs_url}) | React: 🤖 AI Diagnosis | ✅ Retry`, 
        inline: false 
      });
    }
    
    try {
      await rest.post(`/channels/${channelId}/messages`, {
        body: { embeds: [embed] }
      } as any);
      
      console.log(`Azure Pipeline notification sent to channel ${channelId}:`, event);
      res.json({ status: "ok", channel: channelId });
    } catch (err) {
      console.error("Failed to send Discord notification:", err);
      res.status(500).json({ error: "Failed to send notification" });
    }
  };
}
