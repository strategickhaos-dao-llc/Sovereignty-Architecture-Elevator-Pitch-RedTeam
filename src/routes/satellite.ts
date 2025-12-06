import type { Request, Response } from "express";
import crypto from "crypto";
import { REST } from "discord.js";

/**
 * Starlink Satellite Connectivity Routes
 * 
 * Handles satellite relay communications, failover notifications,
 * and swarm agent coordination via the Elon Text-Sat Pipeline.
 */

/** Request with raw body for signature verification */
interface RawBodyRequest extends Request {
  rawBody: string;
}

interface SatelliteStatus {
  provider: string;
  connection: "online" | "degraded" | "offline";
  latencyMs: number;
  activeWan: string;
  failoverActive: boolean;
  queueDepth: number;
  lastHeartbeat: Date;
}

interface RelayMessage {
  agentId: string;
  command: string;
  payload: Record<string, unknown>;
  timestamp: number;
  signature: string;
}

// In-memory state for satellite connectivity (production would use Redis)
const satelliteState: SatelliteStatus = {
  provider: "starlink",
  connection: "online",
  latencyMs: 45,
  activeWan: "starlink",
  failoverActive: false,
  queueDepth: 0,
  lastHeartbeat: new Date()
};

const relayQueue: RelayMessage[] = [];

/**
 * Verify HMAC signature in format 'sha256=<hex>' (consistent with GitHub webhook format)
 */
function verifySignature(secret: string, payload: string, signature: string): boolean {
  const expected = crypto.createHmac("sha256", secret).update(payload).digest("hex");
  const expectedSig = `sha256=${expected}`;
  // Support both raw hex and prefixed format for compatibility
  const sigToCompare = signature.startsWith("sha256=") ? signature : `sha256=${signature}`;
  try {
    return crypto.timingSafeEqual(Buffer.from(expectedSig), Buffer.from(sigToCompare));
  } catch {
    return false; // Buffers of different lengths
  }
}

function generateAuditHash(data: Record<string, unknown>): string {
  return crypto.createHash("sha256").update(JSON.stringify(data)).digest("hex");
}

export function satelliteRoutes(
  rest: REST,
  channelIds: Record<string, string>,
  secret: string
) {
  const send = async (channelId: string, title: string, desc: string, color = 3099199) => {
    await rest.post(`/channels/${channelId}/messages`, {
      body: {
        embeds: [{
          title,
          description: desc,
          color,
          footer: { text: `🛰️ Satellite Relay | ${new Date().toISOString()}` }
        }]
      }
    } as any);
  };

  return {
    /**
     * GET /satellite/status
     * Returns current satellite connectivity status
     */
    status: async (_req: Request, res: Response) => {
      res.json({
        ...satelliteState,
        uptime: Date.now() - satelliteState.lastHeartbeat.getTime(),
        queueDepth: relayQueue.length
      });
    },

    /**
     * GET /satellite/health
     * Health check endpoint for monitoring
     */
    health: async (_req: Request, res: Response) => {
      const healthy = satelliteState.connection !== "offline" && satelliteState.latencyMs < 10000;
      res.status(healthy ? 200 : 503).json({
        status: healthy ? "healthy" : "unhealthy",
        connection: satelliteState.connection,
        activeWan: satelliteState.activeWan,
        failoverActive: satelliteState.failoverActive
      });
    },

    /**
     * POST /satellite/relay
     * Relay messages to swarm agents via satellite when terrestrial is down
     */
    relay: async (req: Request, res: Response) => {
      const sig = req.get("X-Satellite-Signature") || "";
      const raw = (req as RawBodyRequest).rawBody;

      if (!verifySignature(secret, raw, sig)) {
        return res.status(401).json({ error: "Invalid signature" });
      }

      const message: RelayMessage = req.body;

      // Validate message structure
      if (!message.agentId || !message.command) {
        return res.status(400).json({ error: "Missing required fields: agentId, command" });
      }

      // Add audit hash for tamper-evident verification
      const auditHash = generateAuditHash({
        ...message,
        receivedAt: Date.now(),
        relayNode: "starlink-primary"
      });

      // Queue message for relay
      relayQueue.push({
        ...message,
        timestamp: Date.now(),
        signature: auditHash
      });

      // Notify via Discord if failover is active
      if (satelliteState.failoverActive) {
        await send(
          channelIds.status || channelIds.alerts,
          "🛰️ Satellite Relay Active",
          `Agent: \`${message.agentId}\`\nCommand: \`${message.command}\`\nQueue Depth: ${relayQueue.length}`,
          16776960 // Yellow for warning
        );
      }

      res.json({
        status: "queued",
        auditHash,
        queuePosition: relayQueue.length,
        estimatedDelivery: satelliteState.failoverActive ? "next_sat_pass" : "immediate"
      });
    },

    /**
     * POST /satellite/failover
     * Handle failover events from router (Peplink/Starlink Gen3)
     */
    failover: async (req: Request, res: Response) => {
      const sig = req.get("X-Router-Signature") || "";
      const raw = (req as RawBodyRequest).rawBody;

      if (!verifySignature(secret, raw, sig)) {
        return res.status(401).json({ error: "Invalid signature" });
      }

      const { event, fromWan, toWan, reason, timestamp } = req.body;

      // Update state
      satelliteState.activeWan = toWan;
      satelliteState.failoverActive = toWan !== "starlink";
      satelliteState.connection = toWan === "starlink" ? "online" : "degraded";

      const isFailover = event === "failover";
      const color = isFailover ? 16711680 : 65280; // Red for failover, Green for recovery

      await send(
        channelIds.alerts,
        isFailover ? "⚠️ Satellite Failover Activated" : "✅ Primary Connection Restored",
        `**Event:** ${event}\n**From:** ${fromWan}\n**To:** ${toWan}\n**Reason:** ${reason}\n**Time:** ${new Date(timestamp).toISOString()}`,
        color
      );

      // Log to cluster status for audit trail
      await send(
        channelIds.status || channelIds.deployments,
        "🔄 WAN Status Change",
        `Active WAN: \`${toWan}\`\nFailover Active: ${satelliteState.failoverActive}\nQueue Depth: ${relayQueue.length}`
      );

      res.json({
        status: "acknowledged",
        activeWan: satelliteState.activeWan,
        failoverActive: satelliteState.failoverActive
      });
    },

    /**
     * POST /satellite/heartbeat
     * Receive heartbeat from swarm agents for connectivity monitoring
     */
    heartbeat: async (req: Request, res: Response) => {
      const { agentId, status, latencyMs, via } = req.body;

      satelliteState.lastHeartbeat = new Date();
      if (latencyMs) {
        satelliteState.latencyMs = latencyMs;
      }

      // Check for concerning latency
      if (latencyMs > 5000) {
        await send(
          channelIds.alerts,
          "⏱️ High Latency Detected",
          `Agent: \`${agentId}\`\nLatency: ${latencyMs}ms\nVia: ${via || satelliteState.activeWan}`,
          16776960 // Yellow
        );
      }

      res.json({
        status: "acknowledged",
        serverTime: Date.now(),
        activeWan: satelliteState.activeWan,
        recommendedInterval: satelliteState.failoverActive ? 30 : 60
      });
    },

    /**
     * GET /satellite/queue
     * Get pending relay queue (for diagnostics)
     */
    queue: async (_req: Request, res: Response) => {
      res.json({
        queueDepth: relayQueue.length,
        oldestMessage: relayQueue[0]?.timestamp || null,
        estimatedClearTime: relayQueue.length * 2, // Rough estimate in seconds
        activeWan: satelliteState.activeWan
      });
    },

    /**
     * POST /satellite/direct-to-cell
     * Handle Direct-to-Cell SMS relay (T-Mobile partnership)
     */
    directToCell: async (req: Request, res: Response) => {
      const sig = req.get("X-SMS-Signature") || "";
      const raw = (req as RawBodyRequest).rawBody;

      if (!verifySignature(secret, raw, sig)) {
        return res.status(401).json({ error: "Invalid signature" });
      }

      const { from, to, message: smsMessage, satId } = req.body;

      // Validate SMS message structure
      if (!from || !smsMessage) {
        return res.status(400).json({ error: "Missing required fields: from, message" });
      }

      // Generate audit hash for the SMS relay
      const auditHash = generateAuditHash({
        from,
        to,
        messageHash: crypto.createHash("sha256").update(smsMessage).digest("hex").slice(0, 16),
        satId,
        timestamp: Date.now()
      });

      await send(
        channelIds.agents || channelIds.status,
        "📱 Direct-to-Cell Relay",
        `**From:** ${from}\n**Via Satellite:** ${satId || "LEO-pass"}\n**Audit Hash:** \`${auditHash.slice(0, 16)}...\``,
        9807270 // Purple for satellite
      );

      res.json({
        status: "relayed",
        auditHash,
        via: "starlink_direct_to_cell",
        carrier: "t-mobile"
      });
    }
  };
}
