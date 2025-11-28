import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed, errorEmbed, successEmbed, warningEmbed } from "./discord.js";
import { env, loadConfig } from "./config.js";
import { checkInteractionRbac } from "./rbac_guard.js";
import { exec } from "child_process";
import { promisify } from "util";
import * as fs from "fs";
import * as path from "path";

const execAsync = promisify(exec);

const cfg = loadConfig() as any;
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// Channel IDs for posting alerts and recon results
const channelIds = {
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID,
  alerts: process.env.ALERTS_CHANNEL_ID,
  recon: process.env.RECON_CHANNEL_ID,
};

client.once("ready", async () => {
  await registerCommands(token, appId);
  console.log("Bot ready");
});

client.on("interactionCreate", async (i: Interaction) => {
  if (!i.isChatInputCommand()) return;
  
  try {
    // Get environment from command if applicable
    const envOption = i.options.getString("env");
    const environment = envOption || "dev";
    
    // Check RBAC for protected commands
    const rbacResult = await checkInteractionRbac(i as any, environment);
    
    if (!rbacResult.allowed) {
      await i.reply({ 
        embeds: [errorEmbed("Authorization Denied", rbacResult.reason)],
        ephemeral: true 
      });
      return;
    }

    if (i.commandName === "status") {
      const svc = i.options.getString("service", true);
      const r = await fetch(`${cfg.control_api.base_url}/status/${svc}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
      }).then(r => r.json());
      await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const r = await fetch(`${cfg.control_api.base_url}/logs/${svc}?tail=${tail}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
      }).then(r => r.text());
      await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const plan = i.options.getBoolean("plan") || false;
      const canaryPercent = i.options.getInteger("canary");
      const targetSvc = i.options.getString("svc");

      // Dry-run mode: show manifest diff
      if (plan) {
        await i.deferReply();
        const diffResponse = await fetch(`${cfg.control_api.base_url}/deploy/diff`, {
          method: "POST",
          headers: { 
            "Content-Type": "application/json", 
            Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` 
          },
          body: JSON.stringify({ env: envName, tag, service: targetSvc })
        }).then(r => r.json());
        
        const diffContent = diffResponse.diff || "No changes detected";
        await i.editReply({ 
          embeds: [embed(
            `📋 Deploy Plan: ${envName}`, 
            `**Tag:** ${tag}\n**Service:** ${targetSvc || "all"}\n\n**Manifest Diff:**\n\`\`\`diff\n${diffContent.slice(0, 1500)}\n\`\`\``
          )] 
        });
        
        // Post to #deployments channel
        if (channelIds.deployments) {
          await client.channels.fetch(channelIds.deployments).then(async (ch: any) => {
            if (ch?.send) {
              await ch.send({ 
                embeds: [embed(
                  `📋 Deploy Plan Requested`,
                  `**User:** <@${i.user.id}>\n**Env:** ${envName}\n**Tag:** ${tag}\n**Service:** ${targetSvc || "all"}`
                )]
              });
            }
          });
        }
        return;
      }

      // Canary deployment
      if (canaryPercent !== null && canaryPercent !== undefined) {
        if (canaryPercent < 0 || canaryPercent > 100) {
          await i.reply({ 
            embeds: [errorEmbed("Invalid Canary Percentage", "Canary percentage must be between 0 and 100")],
            ephemeral: true 
          });
          return;
        }

        await i.deferReply();
        const r = await fetch(`${cfg.control_api.base_url}/deploy/canary`, {
          method: "POST",
          headers: { 
            "Content-Type": "application/json", 
            Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` 
          },
          body: JSON.stringify({ 
            env: envName, 
            tag, 
            service: targetSvc,
            canaryPercent,
            autoRollback: true,
            sloThresholds: {
              errorRate: 0.05,    // 5% error rate threshold
              p95Latency: 2.0     // 2 second p95 latency threshold
            }
          })
        }).then(r => r.json());

        await i.editReply({ 
          embeds: [successEmbed(
            `🐤 Canary Deploy: ${envName}`,
            `**Tag:** ${tag}\n**Service:** ${targetSvc || "all"}\n**Canary:** ${canaryPercent}%\n**Auto-rollback:** Enabled\n**Status:** ${r.status}`
          )]
        });

        // Post to #deployments channel
        if (channelIds.deployments) {
          await client.channels.fetch(channelIds.deployments).then(async (ch: any) => {
            if (ch?.send) {
              await ch.send({ 
                embeds: [warningEmbed(
                  `🐤 Canary Deployment Started`,
                  `**User:** <@${i.user.id}>\n**Env:** ${envName}\n**Tag:** ${tag}\n**Canary:** ${canaryPercent}%\n**Auto-rollback:** Enabled on SLO breach`
                )]
              });
            }
          });
        }
        return;
      }

      // Standard deployment
      await i.deferReply();
      const r = await fetch(`${cfg.control_api.base_url}/deploy`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
        body: JSON.stringify({ env: envName, tag })
      }).then(r => r.json());
      await i.editReply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      
      await i.deferReply();
      const r = await fetch(`${cfg.control_api.base_url}/scale`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
        body: JSON.stringify({ service: svc, replicas })
      }).then(r => r.json());
      await i.editReply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
    
    } else if (i.commandName === "recon") {
      const namespace = i.options.getString("namespace") || "default";
      
      await i.deferReply();
      
      try {
        // Execute recon script
        const scriptPath = path.resolve("./scripts/recon_cluster.sh");
        const { stdout, stderr } = await execAsync(`bash ${scriptPath} ${namespace}`, {
          timeout: 120000, // 2 minute timeout
          env: { ...process.env, OUTPUT_DIR: "/tmp" }
        });
        
        // Parse output to get archive path
        const lines = stdout.trim().split("\n");
        const archivePath = lines[lines.length - 1];
        
        // Read summary if available
        let summary = "Reconnaissance completed successfully.";
        const summaryPath = archivePath.replace(".tar.gz", "/summary.json");
        try {
          if (fs.existsSync(summaryPath)) {
            const summaryData = JSON.parse(fs.readFileSync(summaryPath, "utf8"));
            summary = `**Namespace:** ${summaryData.namespace_filter}\n**Namespaces:** ${summaryData.cluster_summary?.namespace_count || "N/A"}\n**Timestamp:** ${summaryData.timestamp}`;
          }
        } catch {}

        await i.editReply({ 
          embeds: [successEmbed(
            `🔍 Cluster Recon Complete`,
            `${summary}\n\n**Archive:** \`${archivePath}\``
          )]
        });

        // Post to #recon channel
        if (channelIds.recon) {
          await client.channels.fetch(channelIds.recon).then(async (ch: any) => {
            if (ch?.send) {
              await ch.send({ 
                embeds: [embed(
                  `🔍 Cluster Reconnaissance`,
                  `**Requested by:** <@${i.user.id}>\n**Namespace:** ${namespace}\n\n${summary}\n\n**Archive:** \`${archivePath}\``
                )]
              });
              
              // Attach the archive if it exists and is small enough
              if (fs.existsSync(archivePath)) {
                const stats = fs.statSync(archivePath);
                if (stats.size < 8 * 1024 * 1024) { // 8MB limit
                  await ch.send({ 
                    files: [{ attachment: archivePath, name: path.basename(archivePath) }]
                  });
                }
              }
            }
          });
        }
      } catch (error: any) {
        await i.editReply({ 
          embeds: [errorEmbed(
            "Recon Failed",
            `Error executing reconnaissance: ${error.message?.slice(0, 500) || "Unknown error"}`
          )]
        });
      }
    
    } else if (i.commandName === "review") {
      const pr = i.options.getString("pr", true);
      await i.reply({ embeds: [embed("PR Review", `Queued review for: ${pr}\nModel: Claude-3`)] });
    }
  } catch (e: any) {
    const errorMsg = `Error: ${e.message}`;
    if (i.replied || i.deferred) {
      await i.editReply({ content: errorMsg });
    } else {
      await i.reply({ content: errorMsg, ephemeral: true });
    }
  }
});

client.login(token);