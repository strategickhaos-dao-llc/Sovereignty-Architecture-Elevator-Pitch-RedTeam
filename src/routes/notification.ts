import type { Request, Response } from "express";
import crypto from "crypto";
import { createNotificationService, NotificationOptions, NotificationService } from "../notifications.js";
import { REST } from "discord.js";

interface NotificationRequestBody {
  channel?: string;
  title: string;
  message: string;
  level?: "info" | "warning" | "error" | "success";
  mentionUsers?: string[];
  mentionRoles?: string[];
}

function verifyHmac(secret: string, raw: string, sig: string, algo: string = "sha256"): boolean {
  const h = crypto.createHmac(algo, secret).update(raw).digest("hex");
  return h === sig || `${algo}=${h}` === sig;
}

export function notificationRoutes(rest: REST, channelIds: Record<string, string>, hmacSecret: string) {
  const notificationService = createNotificationService(rest, channelIds);

  return async (req: Request, res: Response) => {
    try {
      // Verify HMAC signature
      const sig = req.get("X-Sig") || req.get("X-Signature") || "";
      const raw = (req as any).rawBody;
      
      if (!verifyHmac(hmacSecret, raw, sig)) {
        return res.status(401).json({ error: "Invalid signature" });
      }

      const body: NotificationRequestBody = req.body;

      // Validate required fields
      if (!body.title || !body.message) {
        return res.status(400).json({ error: "title and message are required" });
      }

      const options: NotificationOptions = {
        title: body.title,
        message: body.message,
        level: body.level || "info",
        mentionUsers: body.mentionUsers,
        mentionRoles: body.mentionRoles
      };

      // Route to appropriate channel
      const channel = body.channel?.toLowerCase();
      
      if (channel) {
        // Specific channel requested
        const channelId = channelIds[channel];
        if (!channelId) {
          return res.status(400).json({ error: `Unknown channel: ${channel}` });
        }
        await notificationService.sendToChannel(channelId, options);
      } else {
        // Default to alerts channel
        await notificationService.alert(options);
      }

      res.json({ success: true, channel: channel || "alerts" });
    } catch (error: any) {
      console.error("Notification error:", error);
      res.status(500).json({ error: error.message || "Internal server error" });
    }
  };
}

/**
 * Middleware for broadcast notifications to multiple channels
 */
export function broadcastRoutes(rest: REST, channelIds: Record<string, string>, hmacSecret: string) {
  const notificationService = createNotificationService(rest, channelIds);

  return async (req: Request, res: Response) => {
    try {
      // Verify HMAC signature
      const sig = req.get("X-Sig") || req.get("X-Signature") || "";
      const raw = (req as any).rawBody;
      
      if (!verifyHmac(hmacSecret, raw, sig)) {
        return res.status(401).json({ error: "Invalid signature" });
      }

      const body = req.body as {
        channels: string[];
        title: string;
        message: string;
        level?: "info" | "warning" | "error" | "success";
        mentionUsers?: string[];
        mentionRoles?: string[];
      };

      if (!body.channels?.length || !body.title || !body.message) {
        return res.status(400).json({ error: "channels, title, and message are required" });
      }

      const options: NotificationOptions = {
        title: body.title,
        message: body.message,
        level: body.level || "info",
        mentionUsers: body.mentionUsers,
        mentionRoles: body.mentionRoles
      };

      // Resolve channel names to IDs
      const resolvedChannelIds = body.channels
        .map(ch => channelIds[ch.toLowerCase()])
        .filter(Boolean);

      if (resolvedChannelIds.length === 0) {
        return res.status(400).json({ error: "No valid channels found" });
      }

      await notificationService.broadcast(resolvedChannelIds, options);

      res.json({ 
        success: true, 
        channels_notified: resolvedChannelIds.length,
        channels: body.channels.filter(ch => channelIds[ch.toLowerCase()])
      });
    } catch (error: any) {
      console.error("Broadcast error:", error);
      res.status(500).json({ error: error.message || "Internal server error" });
    }
  };
}
