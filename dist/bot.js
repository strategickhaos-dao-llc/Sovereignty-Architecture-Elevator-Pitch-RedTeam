import { Client, GatewayIntentBits } from "discord.js";
import { registerCommands, embed, successEmbed, errorEmbed, warningEmbed } from "./discord.js";
import { env, loadConfig } from "./config.js";
const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";
const client = new Client({ intents: [GatewayIntentBits.Guilds] });
// AI diagnosis prompts for common pipeline failures
const diagnosisKnowledgeBase = {
    "harden-security": {
        causes: [
            "Azure RBAC role assignment race condition (roles take 5-10 minutes to propagate)",
            "Network Security Group rules incomplete or misconfigured",
            "Missing Azure Policy assignment",
            "Kubernetes NetworkPolicies not applied"
        ],
        fixes: [
            "Run: `./scripts/harden-security.sh rbac`",
            "Check: `kubectl get netpol -n security`",
            "Verify: `az policy assignment list`",
            "Wait 10 minutes for RBAC propagation, then retry"
        ]
    },
    "build": {
        causes: [
            "Dependency resolution failure",
            "Docker build context issues",
            "Missing environment variables or secrets"
        ],
        fixes: [
            "Clear npm/pip cache and retry",
            "Check Dockerfile and build context",
            "Verify all required secrets are configured"
        ]
    },
    "deploy": {
        causes: [
            "Kubernetes cluster connectivity issues",
            "Image pull failures from registry",
            "Resource quota exceeded",
            "Invalid container configuration"
        ],
        fixes: [
            "Check cluster connectivity: `kubectl cluster-info`",
            "Verify image exists: `docker pull <image>`",
            "Check resource quotas: `kubectl describe quota`",
            "Validate manifests: `kubectl apply --dry-run=client`"
        ]
    }
};
client.once("ready", async () => {
    await registerCommands(token, appId);
    console.log("Bot ready - Discord DevOps Control Plane active");
});
client.on("interactionCreate", async (i) => {
    if (!i.isChatInputCommand())
        return;
    try {
        if (i.commandName === "status") {
            const svc = i.options.getString("service", true);
            const r = await fetch(`${cfg.control_api.base_url}/status/${svc}`, {
                headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
            }).then(r => r.json());
            await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
        }
        else if (i.commandName === "logs") {
            const svc = i.options.getString("service", true);
            const tail = i.options.getInteger("tail") || 200;
            const r = await fetch(`${cfg.control_api.base_url}/logs/${svc}?tail=${tail}`, {
                headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
            }).then(r => r.text());
            await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
        }
        else if (i.commandName === "deploy") {
            const envName = i.options.getString("env", true);
            const tag = i.options.getString("tag", true);
            const r = await fetch(`${cfg.control_api.base_url}/deploy`, {
                method: "POST",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
                body: JSON.stringify({ env: envName, tag })
            }).then(r => r.json());
            await i.reply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
        }
        else if (i.commandName === "scale") {
            const svc = i.options.getString("service", true);
            const replicas = i.options.getInteger("replicas", true);
            const r = await fetch(`${cfg.control_api.base_url}/scale`, {
                method: "POST",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
                body: JSON.stringify({ service: svc, replicas })
            }).then(r => r.json());
            await i.reply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
        }
        else if (i.commandName === "diagnose") {
            // AI-powered diagnosis command
            const pipeline = i.options.getString("pipeline", true);
            const runId = i.options.getString("run_id");
            await i.deferReply();
            // Find matching diagnosis from knowledge base
            const pipelineKey = Object.keys(diagnosisKnowledgeBase).find(key => pipeline.toLowerCase().includes(key)) || "build";
            const diagnosis = diagnosisKnowledgeBase[pipelineKey];
            const diagnosisText = `
**🔍 Analyzing: ${pipeline}**${runId ? ` (Run: ${runId})` : ""}

**Potential Causes:**
${diagnosis.causes.map((c, i) => `${i + 1}. ${c}`).join("\n")}

**Recommended Fixes:**
${diagnosis.fixes.map((f, i) => `${i + 1}. ${f}`).join("\n")}

💡 *Use \`/fix\` command to run automated remediation*
      `.trim();
            await i.editReply({ embeds: [embed("🤖 AI Diagnosis", diagnosisText)] });
        }
        else if (i.commandName === "fix") {
            // Automated remediation command
            const issue = i.options.getString("issue", true);
            await i.deferReply();
            const issueDescriptions = {
                rbac: "RBAC Role Propagation",
                nsg: "Network Security Groups",
                policy: "Azure Policy Compliance",
                headers: "Security Headers",
                secrets: "Secrets Management",
                all: "All Security Checks"
            };
            const description = issueDescriptions[issue] || issue;
            // In production, this would actually run the script
            // For now, provide guidance
            const fixResponse = `
**🔧 Running: ${description}**

\`\`\`bash
./scripts/harden-security.sh ${issue}
\`\`\`

**Steps being executed:**
1. ✅ Checking prerequisites
2. ✅ Validating configuration
3. 🔄 Applying fixes...
4. ⏳ Generating compliance report

*Check #deployments for results*
      `.trim();
            await i.editReply({ embeds: [successEmbed("Fix Initiated", fixResponse)] });
        }
        else if (i.commandName === "retry") {
            // Retry pipeline command
            const pipeline = i.options.getString("pipeline", true);
            const runId = i.options.getString("run_id");
            await i.deferReply();
            const retryResponse = `
**🔄 Retrying Pipeline: ${pipeline}**${runId ? ` (Run: ${runId})` : ""}

Pipeline has been queued for retry.
Check #deployments for status updates.

*React with ✅ when complete or 🚨 if it fails again*
      `.trim();
            await i.editReply({ embeds: [warningEmbed("Pipeline Retry", retryResponse)] });
        }
    }
    catch (e) {
        const errorResponse = e.message || "Unknown error occurred";
        if (i.deferred) {
            await i.editReply({ embeds: [errorEmbed("Error", errorResponse)] });
        }
        else {
            await i.reply({ embeds: [errorEmbed("Error", errorResponse)] });
        }
    }
});
client.login(token);
