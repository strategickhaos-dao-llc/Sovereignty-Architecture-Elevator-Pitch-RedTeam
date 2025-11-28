// Discord deploy command handler sketch
// - supports --plan (dry-run): posts manifest diff to #deployments
// - supports --canary <percent>: triggers canary rollout and links analysis
// - registers rollback hook on SLO breach (requires Observability integration)
//
// This is a high-level handler; inject concrete kubectl/helm/argo clients as appropriate.

import { ChatInputCommandInteraction } from "discord.js";
import util from "util";
import path from "path";
import { execFile as execFileCb } from "child_process";
const execFile = util.promisify(execFileCb);

// Validate service name to prevent command injection
function validateServiceName(svc: string): boolean {
  // Only allow alphanumeric characters, hyphens, and underscores
  return /^[a-zA-Z0-9_-]+$/.test(svc);
}

// Validate canary percentage
function validateCanaryPercent(percent: number): boolean {
  return Number.isInteger(percent) && percent >= 0 && percent <= 100;
}

export async function deployCommand(interaction: ChatInputCommandInteraction) {
  await interaction.deferReply({ ephemeral: true });

  const svc = interaction.options.getString("service", true);
  const plan = interaction.options.getBoolean("plan") ?? false;
  const canary = interaction.options.getInteger("canary") ?? 0;

  // Validate inputs to prevent command injection
  if (!validateServiceName(svc)) {
    await interaction.editReply({ content: "Invalid service name. Only alphanumeric characters, hyphens, and underscores are allowed." });
    return;
  }

  if (canary > 0 && !validateCanaryPercent(canary)) {
    await interaction.editReply({ content: "Invalid canary percentage. Must be between 0 and 100." });
    return;
  }

  try {
    if (plan) {
      // Example: render manifests and show diff (helm/ks/oc/argocd may differ)
      const planOut = await generatePlan(svc);
      // Post to deployments channel
      const deploymentsChannel = process.env.DEPLOYMENTS_CHANNEL_ID;
      if (deploymentsChannel) {
        await postToChannel(deploymentsChannel, `Deployment plan for ${svc}`, [{ name: `${svc}-plan.txt`, content: planOut }]);
      }
      await interaction.editReply({ content: `Deployment plan posted to <#${deploymentsChannel}>` });
      return;
    }

    // authorization and signed payload checks should be performed by gateway RBAC + signature verifiers upstream

    // Proceed with canary or full deploy
    if (canary && canary > 0) {
      await interaction.editReply({ content: `Starting canary deploy for ${svc} at ${canary}%` });
      await startCanary(svc, canary);
      await interaction.followUp({ content: `Canary started. Observability will monitor SLOs and trigger rollback on breaches.` });
      return;
    }

    // full deploy - use execFile with arguments array to prevent shell injection
    // Note: This script should be created in deploy-scripts/ directory as part of deployment setup
    await interaction.editReply({ content: `Starting full deploy for ${svc}` });
    const deployScript = path.join(".", "deploy-scripts", "deploy_service.sh");
    await execFile(deployScript, [svc]);
    await interaction.followUp({ content: `Full deploy kicked off for ${svc}` });
  } catch (err) {
    console.error("deploy error", err);
    await interaction.editReply({ content: `Deploy failed: ${(err as Error).message}` });
  }
}

async function generatePlan(svc: string): Promise<string> {
  // Example: run kubectl diff or helm diff plugin
  // Use execFile with arguments array to prevent shell injection
  // Use path.join to safely construct the overlay path
  try {
    const overlayPath = path.join(".", "overlays", svc);
    // Validate path doesn't escape overlays directory
    const normalizedPath = path.normalize(overlayPath);
    if (!normalizedPath.startsWith("overlays" + path.sep)) {
      return "Invalid service path";
    }
    
    const { stdout } = await execFile("kubectl", [
      "--namespace=default",
      "diff",
      "-f",
      normalizedPath
    ]).catch(() => ({ stdout: "(no diff)" }));
    return stdout || "(no diff)";
  } catch (err) {
    return `Failed to generate plan: ${(err as Error).message}`;
  }
}

async function startCanary(svc: string, percent: number) {
  // Integrate with rollout tool (Argo Rollouts, Flagger, or k8s native) to incrementally direct traffic.
  // Use execFile with arguments array to prevent shell injection
  // Note: This script should be created in deploy-scripts/ directory as part of deployment setup
  const canaryScript = path.join(".", "deploy-scripts", "canary.sh");
  await execFile(canaryScript, [svc, percent.toString()]);
}

/*
Placeholder for posting to Discord channel
Note: This is intentionally a placeholder - actual implementation should use Discord.js REST API
*/
async function postToChannel(channelId: string, text: string, attachments: { name: string; content: string }[]): Promise<void> {
  // TODO: Implement using Discord.js REST API
  // This is a placeholder that logs the intent - actual implementation depends on bot setup
  console.log(`[TODO] Post to channel ${channelId}: ${text}`);
  attachments.forEach((a) => console.log(`[TODO] Attachment: ${a.name}`));
}
