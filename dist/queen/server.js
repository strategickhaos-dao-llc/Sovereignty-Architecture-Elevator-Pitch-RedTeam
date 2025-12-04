/**
 * Queen.js Federation Hub
 *
 * Central webhook coordinator for multi-org GitHub federation.
 * Routes webhooks from all GitHub organizations to unified NATS message bus
 * and Discord channels.
 *
 * Federation Architecture:
 * - Strategickhaos (personal/main)
 * - Strategickhaos-Swarm-Intelligence (team/projects)
 * - SNHU Enterprise (school)
 *
 * All webhooks point to Queen → Queen routes to NATS → Consumers act on events
 */
import express from "express";
import crypto from "crypto";
// Default configuration
const defaultConfig = {
    port: Number(process.env.PORT) || 8081,
    natsUrl: process.env.NATS_URL || "nats://localhost:4222",
    webhookSecret: process.env.GITHUB_WEBHOOK_SECRET || "",
    discordWebhooks: {
        github: process.env.DISCORD_WEBHOOK_GITHUB || "",
        financial: process.env.DISCORD_WEBHOOK_FINANCIAL || "",
    },
    organizations: {
        "Strategickhaos": {
            nats_prefix: "strategickhaos",
            discord_channel: "#github-main",
        },
        "Strategickhaos-Swarm-Intelligence": {
            nats_prefix: "swarm",
            discord_channel: "#github-swarm",
        },
        "SNHU": {
            nats_prefix: "snhu",
            discord_channel: "#github-school",
        },
    },
};
// In-memory mock NATS client for environments without NATS
class MockNATSClient {
    connected = true;
    eventLog = [];
    async publish(subject, data) {
        this.eventLog.push({ subject, data, timestamp: new Date() });
        console.log(`📤 [NATS Mock] Published to ${subject}`);
    }
    getEventLog() {
        return this.eventLog;
    }
}
// Create Express app
const app = express();
// Keep raw body for signature verification
app.use(express.json({
    verify: (req, _res, buf) => {
        req.rawBody = buf.toString();
    },
}));
// NATS client instance (mock for now, can be replaced with real NATS connection)
let natsClient = new MockNATSClient();
// Configuration
let config = defaultConfig;
/**
 * Verify GitHub webhook signature
 */
function verifyWebhookSignature(payload, signature, secret) {
    if (!secret || !signature)
        return false;
    const hmac = crypto.createHmac("sha256", secret);
    const digest = "sha256=" + hmac.update(payload).digest("hex");
    try {
        return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
    }
    catch {
        return false;
    }
}
/**
 * Format Discord embed message
 */
function formatDiscordMessage(event, payload) {
    const repo = payload.repository?.name || "unknown";
    const sender = payload.sender?.login || "unknown";
    switch (event) {
        case "push":
            return `📦 Push to ${repo} by ${sender}`;
        case "pull_request": {
            const pr = payload.pull_request;
            const action = payload.action;
            return `🔀 PR #${pr?.number || "?"} ${action} in ${repo}`;
        }
        case "issues": {
            const issue = payload.issue;
            const action = payload.action;
            return `🐛 Issue #${issue?.number || "?"} ${action} in ${repo}`;
        }
        case "check_suite": {
            const checkSuite = payload.check_suite;
            return `✅ Checks ${checkSuite?.status || "unknown"} (${checkSuite?.conclusion || "pending"}) in ${repo}`;
        }
        case "deployment":
            return `🚀 Deployment in ${repo}`;
        case "deployment_status":
            return `📊 Deployment status updated in ${repo}`;
        default:
            return `📨 ${event} in ${repo}`;
    }
}
/**
 * Create Discord embed object
 */
function createEmbed(event, payload) {
    const pr = payload.pull_request;
    const issue = payload.issue;
    const repository = payload.repository;
    const url = pr?.html_url || issue?.html_url || repository?.html_url || undefined;
    return {
        title: formatDiscordMessage(event, payload),
        url,
        color: event === "pull_request" ? 0x7dd3fc : 0x06b6d4,
        timestamp: new Date().toISOString(),
        footer: {
            text: "Queen.js Federation Hub",
        },
    };
}
/**
 * Central GitHub webhook receiver
 */
app.post("/webhook/github", async (req, res) => {
    // Verify signature if secret is configured
    if (config.webhookSecret) {
        const signature = req.get("x-hub-signature-256") || "";
        if (!verifyWebhookSignature(req.rawBody || "", signature, config.webhookSecret)) {
            console.log("⚠️ Invalid webhook signature");
            return res.status(401).json({ error: "Invalid signature" });
        }
    }
    const event = req.get("x-github-event") || "unknown";
    const payload = req.body;
    const repository = payload.repository;
    const organization = payload.organization;
    const repositoryOwner = payload.repository
        ?.owner;
    const repo = repository?.full_name || "unknown";
    const org = organization?.login || repositoryOwner?.login || "unknown";
    console.log(`📨 GitHub ${event} from ${repo} (org: ${org})`);
    // Get routing configuration for this organization
    const route = config.organizations[org] || {
        nats_prefix: "unknown",
        discord_channel: "#github-general",
    };
    try {
        // Publish to NATS with org-specific subject
        await natsClient.publish(`${route.nats_prefix}.github.${event}`, JSON.stringify({
            event,
            repo,
            org,
            payload,
            timestamp: new Date().toISOString(),
        }));
        // Route to appropriate Discord channel
        await natsClient.publish("discord.notify", JSON.stringify({
            channel: route.discord_channel,
            message: formatDiscordMessage(event, payload),
            embed: createEmbed(event, payload),
        }));
        // Special handling for PRs - notify SovereignPRManager
        if (event === "pull_request") {
            const pr = payload.pull_request;
            await natsClient.publish("sovereignprmanager.review", JSON.stringify({
                org,
                repo,
                pr_number: pr?.number,
                action: payload.action,
            }));
        }
        res.status(200).json({
            status: "received",
            routed_to: route.nats_prefix,
            queen: "acknowledged",
        });
    }
    catch (error) {
        console.error("Error processing webhook:", error);
        res.status(500).json({ error: "Internal processing error" });
    }
});
/**
 * Zapier webhook endpoint
 */
app.post("/webhook/zapier", async (req, res) => {
    try {
        await natsClient.publish("zapier.event", JSON.stringify(req.body));
        res.status(200).json({ status: "received" });
    }
    catch (error) {
        console.error("Error processing Zapier webhook:", error);
        res.status(500).json({ error: "Internal processing error" });
    }
});
/**
 * SwarmGate paycheck detection endpoint
 */
app.post("/webhook/swarmgate/paycheck", async (req, res) => {
    const { amount, source } = req.body;
    if (typeof amount !== "number" || amount <= 0) {
        return res.status(400).json({ error: "Invalid amount" });
    }
    // Calculate 7% allocation
    const allocation = amount * 0.07;
    try {
        await natsClient.publish("swarmgate.paycheck.detected", JSON.stringify({
            amount,
            allocation,
            source: source || "unknown",
            timestamp: new Date().toISOString(),
        }));
        await natsClient.publish("treasury.deposit", JSON.stringify({
            amount: allocation,
            source: "swarmgate_7%",
        }));
        await natsClient.publish("discord.notify", JSON.stringify({
            channel: "#financial",
            message: `💰 Paycheck detected: $${amount.toFixed(2)} → 7% allocation: $${allocation.toFixed(2)}`,
        }));
        res.status(200).json({
            status: "processed",
            allocated: allocation,
        });
    }
    catch (error) {
        console.error("Error processing paycheck webhook:", error);
        res.status(500).json({ error: "Internal processing error" });
    }
});
/**
 * Health check endpoint
 */
app.get("/health", (_req, res) => {
    res.json({
        status: "operational",
        service: "Queen.js Federation Hub",
        sovereignty: "100%",
        uptime: process.uptime(),
        nats_connected: natsClient.connected,
        organizations_monitored: Object.keys(config.organizations),
    });
});
/**
 * API info endpoint
 */
app.get("/", (_req, res) => {
    res.json({
        name: "Queen.js Federation Hub",
        version: "1.0.0",
        description: "Central webhook coordinator for multi-org GitHub federation",
        endpoints: {
            "/webhook/github": "Central GitHub webhook receiver",
            "/webhook/zapier": "Zapier integration webhook",
            "/webhook/swarmgate/paycheck": "SwarmGate paycheck detection",
            "/health": "Health check endpoint",
        },
        architecture: {
            pattern: "Federation (not consolidation)",
            benefit: "Keep orgs separate, one webhook URL for everything",
            cost: "$0 vs GitHub Enterprise $756/year",
        },
    });
});
// Error handling middleware
app.use((err, _req, res, _next) => {
    console.error("Unhandled error:", err);
    res.status(500).json({ error: "Internal server error" });
});
/**
 * Initialize and start the Queen.js Federation Hub
 */
export function startQueen(customConfig) {
    if (customConfig) {
        config = { ...config, ...customConfig };
    }
    const PORT = config.port;
    app.listen(PORT, () => {
        console.log(`👑 Queen.js Federation Hub listening on port ${PORT}`);
        console.log(`🎯 Central webhook: /webhook/github`);
        console.log(`💰 SwarmGate: /webhook/swarmgate/paycheck`);
        console.log(`⚡ Zapier: /webhook/zapier`);
        console.log(`🏥 Health: /health`);
        console.log(`🏛️ Organizations monitored: ${Object.keys(config.organizations).join(", ")}`);
    });
}
/**
 * Set custom NATS client (for testing or real NATS connection)
 */
export function setNATSClient(client) {
    natsClient = client;
}
/**
 * Get the Express app instance (for testing)
 */
export function getApp() {
    return app;
}
// Start server if this is the main module
const isMainModule = require.main === module || process.argv[1]?.includes("queen/server");
if (isMainModule) {
    startQueen();
}
