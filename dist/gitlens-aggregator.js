// GitLens Event Aggregator - Centralized event collection for distribution
import express from 'express';
import { loadConfig, env } from './config.js';
import { REST } from 'discord.js';
export class GitLensAggregator {
    config;
    events = [];
    mindOSUrl;
    discordRest;
    constructor() {
        this.config = loadConfig();
        this.mindOSUrl = process.env.MINDOS_URL || 'http://localhost:8090';
        this.discordRest = new REST({ version: '10' }).setToken(env('DISCORD_TOKEN'));
    }
    // Receive event from GitLens
    async receiveEvent(event) {
        console.log(`📥 GitLens event received: ${event.type} from ${event.user}`);
        // Store event
        this.events.push(event);
        // Notify Discord
        await this.notifyDiscord(event);
        // Forward to Mind OS for distribution
        await this.forwardToMindOS(event);
    }
    // Forward event to Mind OS orchestrator for distribution
    async forwardToMindOS(event) {
        const maxRetries = 3;
        const timeout = 5000; // 5 seconds
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                const distribution = {
                    event,
                    target_clusters: this.config.infra?.nodes?.clusters?.map((c) => c.name) || [],
                    llm_generals: this.selectLLMGenerals(event),
                    distribution_strategy: this.determineStrategy(event)
                };
                console.log(`🔄 Forwarding to Mind OS (attempt ${attempt}/${maxRetries})`);
                // Create abort controller for timeout
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), timeout);
                const response = await fetch(`${this.mindOSUrl}/distribute`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(distribution),
                    signal: controller.signal
                });
                clearTimeout(timeoutId);
                if (!response.ok) {
                    throw new Error(`Mind OS returned ${response.status}: ${response.statusText}`);
                }
                console.log(`✅ Event distributed to Mind OS successfully`);
                return; // Success, exit retry loop
            }
            catch (error) {
                console.error(`❌ Error forwarding to Mind OS (attempt ${attempt}/${maxRetries}):`, error);
                if (attempt === maxRetries) {
                    console.error(`❌ Failed to forward event after ${maxRetries} attempts`);
                    // In production, this should queue the event for retry or dead-letter queue
                }
                else {
                    // Exponential backoff
                    const backoffMs = Math.min(1000 * Math.pow(2, attempt - 1), 10000);
                    await new Promise(resolve => setTimeout(resolve, backoffMs));
                }
            }
        }
    }
    // Select which LLM generals should receive this event
    selectLLMGenerals(event) {
        const generals = [];
        // Route based on event type
        switch (event.type) {
            case 'review_started':
            case 'review_submitted':
                generals.push('code-review-general', 'quality-assurance-general');
                break;
            case 'pr_created':
                generals.push('architecture-general', 'security-general', 'code-review-general');
                break;
            case 'pr_merged':
                generals.push('deployment-general', 'documentation-general');
                break;
            case 'commit_graph':
                generals.push('analytics-general', 'metrics-general');
                break;
            case 'needs_attention':
                generals.push('triage-general', 'priority-general');
                break;
            default:
                generals.push('general-purpose-general');
        }
        return generals;
    }
    // Determine distribution strategy based on event
    determineStrategy(event) {
        // Critical events broadcast to all clusters
        if (event.type === 'needs_attention' || event.type === 'pr_created') {
            return 'broadcast';
        }
        // Review events use load balancing
        if (event.type === 'review_started' || event.type === 'review_submitted') {
            return 'load_balanced';
        }
        // Default to round robin
        return 'round_robin';
    }
    // Notify Discord of the event
    async notifyDiscord(event) {
        try {
            const channelId = this.config.discord?.channels?.prs || process.env.PRS_CHANNEL_ID;
            if (!channelId) {
                console.warn('⚠️  No Discord channel configured for GitLens events');
                return;
            }
            const embed = {
                title: `🔍 GitLens: ${this.formatEventType(event.type)}`,
                description: this.formatEventDescription(event),
                color: this.getEventColor(event.type),
                timestamp: event.timestamp,
                fields: [
                    { name: 'Repository', value: event.repository, inline: true },
                    { name: 'User', value: event.user, inline: true }
                ]
            };
            await this.discordRest.post(`/channels/${channelId}/messages`, { body: { embeds: [embed] } });
        }
        catch (error) {
            console.error('❌ Failed to notify Discord:', error);
        }
    }
    formatEventType(type) {
        return type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    }
    formatEventDescription(event) {
        const parts = [`By **${event.user}**`];
        if (event.metadata.pr_number) {
            parts.push(`PR #${event.metadata.pr_number}`);
        }
        if (event.metadata.title) {
            parts.push(`\n\n**${event.metadata.title}**`);
        }
        if (event.metadata.description) {
            parts.push(`\n${event.metadata.description.slice(0, 200)}${event.metadata.description.length > 200 ? '...' : ''}`);
        }
        return parts.join(' ');
    }
    getEventColor(type) {
        const colors = {
            review_started: 0x2f81f7,
            review_submitted: 0x28a745,
            needs_attention: 0xdc3545,
            commit_graph: 0x6f42c1,
            pr_created: 0xffc107,
            pr_merged: 0x20c997
        };
        return colors[type] || 0x2f81f7;
    }
    // Get aggregated statistics
    getStats() {
        const eventCounts = {};
        this.events.forEach(event => {
            eventCounts[event.type] = (eventCounts[event.type] || 0) + 1;
        });
        return {
            total_events: this.events.length,
            event_types: eventCounts,
            recent_events: this.events.slice(-10)
        };
    }
}
// Express app setup
const app = express();
app.use(express.json());
const aggregator = new GitLensAggregator();
// Health check
app.get('/health', (_req, res) => {
    res.json({
        status: 'healthy',
        service: 'gitlens-aggregator',
        timestamp: new Date().toISOString()
    });
});
// Receive GitLens events
app.post('/events', async (req, res) => {
    try {
        const event = {
            type: req.body.type,
            timestamp: req.body.timestamp || new Date().toISOString(),
            repository: req.body.repository,
            user: req.body.user,
            metadata: req.body.metadata || {}
        };
        await aggregator.receiveEvent(event);
        res.status(202).json({
            message: 'Event received and forwarded to Mind OS',
            event_id: `${event.type}-${Date.now()}`
        });
    }
    catch (error) {
        console.error('Error processing GitLens event:', error);
        res.status(500).json({ error: 'Failed to process event' });
    }
});
// Get statistics
app.get('/stats', (_req, res) => {
    res.json(aggregator.getStats());
});
// Webhook endpoint for GitLens integration
app.post('/webhook/gitlens', async (req, res) => {
    try {
        // Transform GitLens webhook to our event format
        const event = {
            type: req.body.event_type || 'pr_created',
            timestamp: new Date().toISOString(),
            repository: req.body.repository?.full_name || 'unknown',
            user: req.body.sender?.login || 'unknown',
            metadata: {
                pr_number: req.body.pull_request?.number,
                commit_sha: req.body.pull_request?.head?.sha,
                branch: req.body.pull_request?.head?.ref,
                title: req.body.pull_request?.title,
                description: req.body.pull_request?.body
            }
        };
        await aggregator.receiveEvent(event);
        res.status(200).json({ message: 'Webhook processed' });
    }
    catch (error) {
        console.error('Error processing webhook:', error);
        res.status(500).json({ error: 'Failed to process webhook' });
    }
});
const port = Number(process.env.GITLENS_AGGREGATOR_PORT || 8086);
app.listen(port, () => {
    console.log(`🔍 GitLens Aggregator listening on port ${port}`);
    console.log(`🧠 Mind OS URL: ${process.env.MINDOS_URL || 'http://localhost:8090'}`);
});
