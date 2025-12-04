/**
 * Health Bot for Sovereignty Architecture
 * 
 * Provides health check endpoints and Discord notifications
 * for the sovereign infrastructure.
 */

import express, { Request, Response } from "express";
import { REST } from "discord.js";
import { createHealthEmbed, QuadrantColors } from "./quadrant-embeds.js";

export interface ServiceHealth {
  name: string;
  status: "healthy" | "degraded" | "unhealthy";
  latency?: number;
  lastCheck: Date;
  message?: string;
}

export interface HealthConfig {
  services: {
    name: string;
    url?: string;
    checkFn?: () => Promise<boolean>;
    timeout?: number; // Timeout in milliseconds for health checks
  }[];
  discordToken?: string;
  alertChannelId?: string;
  healthCheckInterval?: number;
  defaultTimeout?: number; // Default timeout for services without specific timeout
}

export class HealthBot {
  private services: Map<string, ServiceHealth> = new Map();
  private rest: REST | null = null;
  private alertChannelId: string | null = null;
  private checkInterval: NodeJS.Timeout | null = null;
  private version: string = "1.0.0";
  private startTime: Date = new Date();
  private config: HealthConfig;

  constructor(config: HealthConfig) {
    this.config = config;
    
    if (config.discordToken) {
      this.rest = new REST({ version: "10" }).setToken(config.discordToken);
    }
    this.alertChannelId = config.alertChannelId || null;

    // Initialize service tracking
    for (const service of config.services) {
      this.services.set(service.name, {
        name: service.name,
        status: "healthy",
        lastCheck: new Date(),
        message: "Initial state"
      });
    }
  }

  /**
   * Wake the health bot and start monitoring
   */
  wake(): void {
    console.log("🌅 Health bot awakening...");
    console.log(`📊 Monitoring ${this.services.size} services`);
    
    // Run initial health check
    this.runHealthChecks();

    // Start periodic health checks
    const interval = this.config.healthCheckInterval || 60000; // Default 1 minute
    this.checkInterval = setInterval(() => this.runHealthChecks(), interval);

    console.log("🟢 Health bot is awake and watching the swarm");
  }

  /**
   * Sleep the health bot (stop monitoring)
   */
  sleep(): void {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
    }
    console.log("💤 Health bot entering sleep mode");
  }

  /**
   * Run health checks on all configured services
   */
  async runHealthChecks(): Promise<void> {
    const unhealthyServices: string[] = [];

    for (const serviceConfig of this.config.services) {
      const startTime = Date.now();
      let status: "healthy" | "degraded" | "unhealthy" = "healthy";
      let message = "OK";

      try {
        if (serviceConfig.checkFn) {
          const isHealthy = await serviceConfig.checkFn();
          status = isHealthy ? "healthy" : "unhealthy";
          message = isHealthy ? "Check passed" : "Check failed";
        } else if (serviceConfig.url) {
          const timeout = serviceConfig.timeout || this.config.defaultTimeout || 10000;
          const response = await fetch(serviceConfig.url, { 
            signal: AbortSignal.timeout(timeout) 
          });
          
          if (response.ok) {
            status = "healthy";
            message = `HTTP ${response.status}`;
          } else {
            status = response.status >= 500 ? "unhealthy" : "degraded";
            message = `HTTP ${response.status}`;
          }
        }
      } catch (error) {
        status = "unhealthy";
        message = error instanceof Error ? error.message : "Unknown error";
      }

      const latency = Date.now() - startTime;
      const previousStatus = this.services.get(serviceConfig.name)?.status;

      this.services.set(serviceConfig.name, {
        name: serviceConfig.name,
        status,
        latency,
        lastCheck: new Date(),
        message
      });

      // Track status change for alerts
      if (status !== "healthy") {
        unhealthyServices.push(serviceConfig.name);
      }

      // Alert on status change
      if (previousStatus && previousStatus !== status) {
        await this.sendStatusChangeAlert(serviceConfig.name, previousStatus, status, message);
      }
    }

    // Log summary
    const healthyCount = Array.from(this.services.values()).filter(s => s.status === "healthy").length;
    console.log(`🏥 Health check complete: ${healthyCount}/${this.services.size} services healthy`);
  }

  /**
   * Send an alert when service status changes
   */
  private async sendStatusChangeAlert(
    serviceName: string,
    previousStatus: string,
    newStatus: string,
    message: string
  ): Promise<void> {
    if (!this.rest || !this.alertChannelId) return;

    const color = newStatus === "healthy" ? QuadrantColors.SWARM :
                  newStatus === "degraded" ? QuadrantColors.TREASURY :
                  QuadrantColors.ALERT;

    const statusEmoji = newStatus === "healthy" ? "🟢" :
                       newStatus === "degraded" ? "🟡" : "🔴";

    const embed = {
      title: `${statusEmoji} Service Status Change`,
      description: `**${serviceName}** changed from \`${previousStatus}\` to \`${newStatus}\``,
      color,
      fields: [
        { name: "Service", value: serviceName, inline: true },
        { name: "Previous", value: previousStatus, inline: true },
        { name: "Current", value: newStatus, inline: true },
        { name: "Message", value: message || "No details", inline: false }
      ],
      timestamp: new Date().toISOString(),
      footer: { text: "Sovereignty Health Monitor" }
    };

    try {
      await this.rest.post(`/channels/${this.alertChannelId}/messages`, {
        body: { embeds: [embed] }
      });
    } catch (error) {
      console.error("Failed to send status change alert:", error);
    }
  }

  /**
   * Get current health status
   */
  getStatus(): {
    healthy: boolean;
    services: Record<string, { status: string; latency?: number }>;
    timestamp: Date;
    version: string;
    uptime: number;
  } {
    const services: Record<string, { status: string; latency?: number }> = {};
    let allHealthy = true;

    for (const [name, health] of this.services.entries()) {
      services[name] = {
        status: health.status,
        latency: health.latency
      };
      if (health.status !== "healthy") {
        allHealthy = false;
      }
    }

    return {
      healthy: allHealthy,
      services,
      timestamp: new Date(),
      version: this.version,
      uptime: Date.now() - this.startTime.getTime()
    };
  }

  /**
   * Post health status to Discord
   */
  async postHealthToDiscord(channelId?: string): Promise<string | null> {
    const targetChannel = channelId || this.alertChannelId;
    if (!this.rest || !targetChannel) {
      console.warn("Discord not configured for health post");
      return null;
    }

    try {
      const status = this.getStatus();
      const embed = createHealthEmbed(status);
      
      const response = await this.rest.post(`/channels/${targetChannel}/messages`, {
        body: { embeds: [embed.toJSON()] }
      }) as { id: string };

      return response.id;
    } catch (error) {
      console.error("Failed to post health to Discord:", error);
      return null;
    }
  }

  /**
   * Create Express routes for health endpoints
   */
  createRoutes(): express.Router {
    const router = express.Router();

    // Basic health check - always returns quickly
    router.get("/health", (_req: Request, res: Response) => {
      const status = this.getStatus();
      const httpStatus = status.healthy ? 200 : 503;
      
      res.status(httpStatus).json({
        status: status.healthy ? "healthy" : "unhealthy",
        timestamp: status.timestamp.toISOString(),
        version: status.version,
        uptime_ms: status.uptime
      });
    });

    // Detailed health check with all services
    router.get("/health/detailed", (_req: Request, res: Response) => {
      const status = this.getStatus();
      const httpStatus = status.healthy ? 200 : 503;
      
      res.status(httpStatus).json({
        ...status,
        timestamp: status.timestamp.toISOString()
      });
    });

    // Readiness probe for Kubernetes
    router.get("/ready", (_req: Request, res: Response) => {
      const status = this.getStatus();
      
      if (status.healthy) {
        res.status(200).json({ ready: true });
      } else {
        res.status(503).json({ ready: false, reason: "Services unhealthy" });
      }
    });

    // Liveness probe for Kubernetes
    router.get("/live", (_req: Request, res: Response) => {
      res.status(200).json({ 
        live: true,
        uptime_ms: Date.now() - this.startTime.getTime()
      });
    });

    // Wake endpoint - activates the bot
    router.post("/wake", async (_req: Request, res: Response) => {
      this.wake();
      
      // Optionally post to Discord
      const messageId = await this.postHealthToDiscord();
      
      res.json({
        status: "awake",
        message: "The swarm has been awakened",
        discord_message_id: messageId,
        timestamp: new Date().toISOString()
      });
    });

    // Sleep endpoint - deactivates monitoring
    router.post("/sleep", (_req: Request, res: Response) => {
      this.sleep();
      
      res.json({
        status: "sleeping",
        message: "The swarm rests",
        timestamp: new Date().toISOString()
      });
    });

    // Manual health check trigger
    router.post("/check", async (_req: Request, res: Response) => {
      await this.runHealthChecks();
      const status = this.getStatus();
      
      res.json({
        checked: true,
        status,
        timestamp: new Date().toISOString()
      });
    });

    return router;
  }
}

export default HealthBot;
