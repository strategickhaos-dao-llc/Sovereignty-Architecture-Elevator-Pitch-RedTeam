import type { Request, Response } from "express";
import crypto from "crypto";
import { REST } from "discord.js";

interface ImmuneEvent {
  type: "threat_detected" | "wbc_spawned" | "antibody_learned" | "mode_changed" | "circadian_shift" | "quorum_density_change";
  timestamp: string;
  payload: Record<string, unknown>;
}

interface ImmuneChannelIds {
  immune_response: string;
  swarm_health: string;
}

function sigOk(secret: string, raw: string, sig: string): boolean {
  const h = crypto.createHmac("sha256", secret).update(raw).digest("hex");
  return `sha256=${h}` === sig;
}

function getEventEmoji(type: string): string {
  const emojis: Record<string, string> = {
    threat_detected: "🚨",
    wbc_spawned: "🔬",
    antibody_learned: "🧪",
    mode_changed: "🔄",
    circadian_shift: "🌙",
    quorum_density_change: "📊"
  };
  return emojis[type] || "🧬";
}

function getEventColor(type: string): number {
  const colors: Record<string, number> = {
    threat_detected: 0xff0000,   // Red
    wbc_spawned: 0x00ff00,       // Green
    antibody_learned: 0x0099ff,  // Blue
    mode_changed: 0xffff00,      // Yellow
    circadian_shift: 0x9933ff,   // Purple
    quorum_density_change: 0x00ffff // Cyan
  };
  return colors[type] || 0x2f81f7;
}

function routeToChannel(eventType: string): "immune_response" | "swarm_health" {
  const immuneResponseEvents = ["threat_detected", "wbc_spawned", "antibody_learned"];
  return immuneResponseEvents.includes(eventType) ? "immune_response" : "swarm_health";
}

export function immuneRoutes(rest: REST, channelIds: ImmuneChannelIds, secret: string) {
  return async (req: Request & { rawBody?: string }, res: Response) => {
    // Verify webhook signature
    const sig = req.get("X-Immune-Signature") || req.get("X-Sig") || "";
    const raw = req.rawBody || "";
    
    if (secret && !sigOk(secret, raw, sig)) {
      return res.status(401).send("bad signature");
    }

    const event: ImmuneEvent = req.body;
    
    if (!event.type) {
      return res.status(400).send("missing event type");
    }

    const send = async (channelId: string, title: string, desc: string, color: number) => {
      await rest.post(`/channels/${channelId}/messages`, {
        body: {
          embeds: [{
            title,
            description: desc,
            color,
            timestamp: event.timestamp || new Date().toISOString(),
            footer: { text: "Sovereignty Architecture • Immune System" }
          }]
        }
      } as { body: unknown });
    };

    try {
      const channelType = routeToChannel(event.type);
      const channelId = channelIds[channelType];
      
      if (!channelId) {
        console.warn(`No channel configured for ${channelType}`);
        return res.status(200).send("no channel configured");
      }

      const emoji = getEventEmoji(event.type);
      const color = getEventColor(event.type);
      const payload = event.payload || {};

      let title = "";
      let description = "";

      switch (event.type) {
        case "threat_detected":
          title = `${emoji} Threat Detected`;
          description = `**Type:** ${payload.threatType || "unknown"}\n` +
            `**Severity:** ${payload.severity || "medium"}\n` +
            `**Source:** ${payload.source || "unknown"}\n\n` +
            `White blood cells dispatched for investigation.`;
          break;

        case "wbc_spawned":
          title = `${emoji} WBC Spawned`;
          description = `**Cell ID:** ${payload.cellId || "wbc-" + Date.now()}\n` +
            `**Reason:** ${payload.reason || "threat response"}\n` +
            `**Total WBC:** ${payload.totalCount || "unknown"}`;
          break;

        case "antibody_learned":
          title = `${emoji} Antibody Learned`;
          description = `**Pattern:** \`${payload.pattern || "unknown"}\`\n` +
            `**Confidence:** ${payload.confidence || "100"}%\n` +
            `**Source:** ${payload.source || "manual"}\n\n` +
            `Added to immune memory.`;
          break;

        case "mode_changed":
          const modeEmojis: Record<string, string> = { hunt: "🔥", coordinate: "🤝", biofilm: "🛡️" };
          title = `${emoji} Swarm Mode Changed`;
          description = `${modeEmojis[String(payload.oldMode)] || "❓"} **${payload.oldMode}** → ` +
            `${modeEmojis[String(payload.newMode)] || "❓"} **${payload.newMode}**\n\n` +
            `All cells notified via quorum sensing.`;
          break;

        case "circadian_shift":
          const circadianEmoji = payload.newMode === "day" ? "☀️" : "🌙";
          title = `${emoji} Circadian Shift`;
          description = `${circadianEmoji} Entering **${payload.newMode}** mode\n\n` +
            `Activity levels adjusted accordingly.`;
          break;

        case "quorum_density_change":
          title = `${emoji} Quorum Density Update`;
          description = `**Previous:** ${payload.oldDensity || "unknown"} cells\n` +
            `**Current:** ${payload.newDensity || "unknown"} cells\n` +
            `**Threshold:** ${payload.threshold || 10} cells`;
          break;

        default:
          title = `${emoji} Immune Event`;
          description = `Event type: ${event.type}\n\n` +
            `\`\`\`json\n${JSON.stringify(payload, null, 2)}\n\`\`\``;
      }

      await send(channelId, title, description, color);
      res.send("ok");
    } catch (error) {
      console.error("Failed to process immune event:", error);
      res.status(500).send("internal error");
    }
  };
}
