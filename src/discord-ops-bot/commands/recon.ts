// Discord command handler: /recon
// - Executes scripts/recon_cluster.sh
// - Uploads tarball to configured #recon channel (via bot upload helper)
// - Streams a small summary back to invoking channel
//
// Assumptions: helper functions execFilePromise, uploadFileToChannel, postMessage exist.

import { ChatInputCommandInteraction } from "discord.js";
import path from "path";
import fs from "fs";
import { execFile } from "child_process";
import util from "util";

const execFileP = util.promisify(execFile);

// Validate namespace to prevent command injection
function validateNamespace(ns: string): boolean {
  // Kubernetes namespace naming rules: lowercase alphanumeric, hyphens allowed
  return /^[a-z0-9]([-a-z0-9]*[a-z0-9])?$/.test(ns);
}

export async function reconCommand(interaction: ChatInputCommandInteraction) {
  await interaction.deferReply({ ephemeral: true });

  const ns = interaction.options.getString("namespace") ?? "default";
  
  // Validate namespace input
  if (!validateNamespace(ns)) {
    await interaction.editReply({ content: "Invalid namespace. Only lowercase alphanumeric characters and hyphens are allowed." });
    return;
  }
  
  const out = await runRecon(ns);
  // upload to recon channel
  try {
    const reconChannelId = process.env.RECON_CHANNEL_ID;
    if (!reconChannelId) throw new Error("RECON_CHANNEL_ID not configured");

    await uploadFileToChannel(reconChannelId, out, `recon_${ns}.tar.gz`);
    const summary = await summarizeTarball(out);
    await interaction.editReply({ content: `Recon completed and posted to <#${reconChannelId}>.\nSummary:\n${summary}` });
  } catch (err) {
    console.error("recon upload error:", err);
    await interaction.editReply({ content: `Recon completed but failed to publish: ${(err as Error).message}` });
  }
}

async function runRecon(ns: string): Promise<string> {
  // Use import.meta.url for ESM compatibility, with __dirname fallback for CommonJS
  const currentDir = typeof __dirname !== 'undefined' 
    ? __dirname 
    : path.dirname(new URL(import.meta.url).pathname);
  const script = path.resolve(currentDir, "../../scripts/recon_cluster.sh");
  if (!fs.existsSync(script)) throw new Error("recon script not found");
  const out = await execFileP(script, [ns, "/tmp"]);
  // script prints path to tarball
  const printed = out.stdout.trim().split("\n").pop() || "";
  if (!printed || !fs.existsSync(printed)) throw new Error("recon output missing");
  return printed;
}

async function summarizeTarball(tarPath: string): Promise<string> {
  // Minimal summary: list top-level files and size
  const stat = fs.statSync(tarPath);
  return `file=${path.basename(tarPath)} size=${stat.size} bytes`;
}

/*
Placeholder for bot-specific upload. Implement in bot utils.
Note: This is intentionally a placeholder - actual implementation should use Discord.js REST API
*/
async function uploadFileToChannel(channelId: string, filePath: string, name: string): Promise<void> {
  // TODO: Implement using Discord.js REST API to upload files
  // This is a placeholder that logs the intent - actual implementation depends on bot setup
  console.log(`[TODO] Upload ${filePath} as ${name} to channel ${channelId}`);
}
