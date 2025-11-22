// Mind OS Orchestrator - Distributes events to LLM Generals across Kubernetes clusters
import express from 'express';
import { loadConfig } from './config.js';
export class MindOSOrchestrator {
    config;
    llmGenerals = new Map();
    distributionHistory = [];
    roundRobinIndex = 0;
    constructor() {
        this.config = loadConfig();
        this.initializeLLMGenerals();
    }
    // Initialize LLM Generals from configuration
    initializeLLMGenerals() {
        const clusters = this.config.infra?.nodes?.clusters || [];
        // Define LLM General types and their specializations
        const generalTypes = [
            { name: 'code-review-general', specialization: ['code_review', 'quality', 'best_practices'] },
            { name: 'quality-assurance-general', specialization: ['testing', 'qa', 'validation'] },
            { name: 'architecture-general', specialization: ['design', 'architecture', 'patterns'] },
            { name: 'security-general', specialization: ['security', 'vulnerabilities', 'compliance'] },
            { name: 'deployment-general', specialization: ['deployment', 'release', 'cicd'] },
            { name: 'documentation-general', specialization: ['docs', 'readme', 'guides'] },
            { name: 'analytics-general', specialization: ['metrics', 'analysis', 'insights'] },
            { name: 'metrics-general', specialization: ['performance', 'monitoring', 'observability'] },
            { name: 'triage-general', specialization: ['prioritization', 'triage', 'routing'] },
            { name: 'priority-general', specialization: ['urgency', 'severity', 'escalation'] },
            { name: 'general-purpose-general', specialization: ['general', 'multipurpose'] }
        ];
        // Create LLM General instances across all clusters
        clusters.forEach((cluster) => {
            const namespaces = cluster.namespaces || ['agents'];
            generalTypes.forEach(generalType => {
                const generalKey = `${generalType.name}-${cluster.name}`;
                this.llmGenerals.set(generalKey, {
                    name: generalType.name,
                    cluster: cluster.name,
                    namespace: namespaces.includes('agents') ? 'agents' : namespaces[0],
                    endpoint: this.buildGeneralEndpoint(cluster, generalType.name),
                    status: 'active',
                    specialization: generalType.specialization,
                    current_load: 0,
                    max_load: 10
                });
            });
        });
        console.log(`🧠 Initialized ${this.llmGenerals.size} LLM Generals across ${clusters.length} clusters`);
    }
    // Build endpoint URL for LLM General
    buildGeneralEndpoint(cluster, generalName) {
        const clusterBase = cluster.api_server.replace('https://', '');
        return `https://${clusterBase}/api/v1/namespaces/agents/services/${generalName}:8080/proxy`;
    }
    // Distribute event to LLM Generals
    async distribute(request) {
        console.log(`🔄 Distributing event: ${request.event.type} using ${request.distribution_strategy} strategy`);
        const distributionId = `dist-${Date.now()}`;
        const assignments = [];
        // Get available generals based on request
        const availableGenerals = this.getAvailableGenerals(request.llm_generals, request.target_clusters);
        if (availableGenerals.length === 0) {
            console.warn('⚠️  No available LLM Generals found');
            return {
                distribution_id: distributionId,
                timestamp: new Date().toISOString(),
                strategy: request.distribution_strategy,
                assignments: []
            };
        }
        // Apply distribution strategy
        const selectedGenerals = this.selectGeneralsByStrategy(availableGenerals, request.distribution_strategy);
        // Dispatch to each selected general
        for (const general of selectedGenerals) {
            const result = await this.dispatchToGeneral(general, request.event);
            assignments.push({
                general: `${general.name}-${general.cluster}`,
                cluster: general.cluster,
                status: (result.success ? 'dispatched' : 'failed'),
                response: result.response
            });
        }
        const distributionResult = {
            distribution_id: distributionId,
            timestamp: new Date().toISOString(),
            strategy: request.distribution_strategy,
            assignments
        };
        this.distributionHistory.push(distributionResult);
        console.log(`✅ Distribution complete: ${assignments.filter(a => a.status === 'dispatched').length}/${assignments.length} successful`);
        return distributionResult;
    }
    // Get available generals matching criteria
    getAvailableGenerals(generalNames, clusters) {
        const available = [];
        this.llmGenerals.forEach(general => {
            // Filter by general name
            if (generalNames.length > 0 && !generalNames.includes(general.name)) {
                return;
            }
            // Filter by cluster
            if (clusters.length > 0 && !clusters.includes(general.cluster)) {
                return;
            }
            // Filter by availability
            if (general.status === 'active' && general.current_load < general.max_load) {
                available.push(general);
            }
        });
        return available;
    }
    // Select generals based on distribution strategy
    selectGeneralsByStrategy(generals, strategy) {
        switch (strategy) {
            case 'broadcast':
                // Send to all available generals
                return generals;
            case 'round_robin':
                // Rotate through generals
                if (generals.length === 0)
                    return [];
                const selected = generals[this.roundRobinIndex % generals.length];
                this.roundRobinIndex++;
                return [selected];
            case 'load_balanced':
                // Select generals with lowest load
                const sorted = generals.sort((a, b) => a.current_load - b.current_load);
                // Take top 3 least loaded
                return sorted.slice(0, Math.min(3, sorted.length));
            default:
                return generals.slice(0, 1);
        }
    }
    // Dispatch event to a specific LLM General
    async dispatchToGeneral(general, event) {
        try {
            console.log(`📤 Dispatching to ${general.name} on ${general.cluster}`);
            // Increment load
            general.current_load++;
            // In production, this would make actual HTTP request to the LLM General endpoint
            // For now, simulate the dispatch
            const payload = {
                event_type: event.type,
                timestamp: event.timestamp,
                data: event,
                general_info: {
                    name: general.name,
                    cluster: general.cluster,
                    specialization: general.specialization
                }
            };
            // Simulate async processing
            setTimeout(() => {
                general.current_load = Math.max(0, general.current_load - 1);
            }, 5000);
            // Mock response - in production this would be actual LLM General response
            const response = {
                general: general.name,
                cluster: general.cluster,
                status: 'accepted',
                processing_started: new Date().toISOString(),
                estimated_completion: new Date(Date.now() + 5000).toISOString()
            };
            return { success: true, response };
        }
        catch (error) {
            console.error(`❌ Failed to dispatch to ${general.name}:`, error);
            general.current_load = Math.max(0, general.current_load - 1);
            return { success: false, response: { error: String(error) } };
        }
    }
    // Get orchestrator status
    getStatus() {
        const generalsByCluster = {};
        const generalsByStatus = { active: 0, inactive: 0, busy: 0 };
        this.llmGenerals.forEach(general => {
            if (!generalsByCluster[general.cluster]) {
                generalsByCluster[general.cluster] = [];
            }
            generalsByCluster[general.cluster].push({
                name: general.name,
                status: general.status,
                load: `${general.current_load}/${general.max_load}`,
                specialization: general.specialization
            });
            generalsByStatus[general.status]++;
        });
        return {
            total_generals: this.llmGenerals.size,
            generals_by_cluster: generalsByCluster,
            generals_by_status: generalsByStatus,
            recent_distributions: this.distributionHistory.slice(-10),
            total_distributions: this.distributionHistory.length
        };
    }
    // Get specific general info
    getGeneral(name, cluster) {
        return this.llmGenerals.get(`${name}-${cluster}`);
    }
    // Update general status
    updateGeneralStatus(name, cluster, status) {
        const general = this.llmGenerals.get(`${name}-${cluster}`);
        if (general) {
            general.status = status;
            console.log(`🔄 Updated ${name}-${cluster} status to ${status}`);
            return true;
        }
        return false;
    }
}
// Express app setup
const app = express();
app.use(express.json());
const orchestrator = new MindOSOrchestrator();
// Health check
app.get('/health', (_req, res) => {
    res.json({
        status: 'healthy',
        service: 'mindos-orchestrator',
        timestamp: new Date().toISOString()
    });
});
// Main distribution endpoint
app.post('/distribute', async (req, res) => {
    try {
        const request = req.body;
        const result = await orchestrator.distribute(request);
        res.status(200).json(result);
    }
    catch (error) {
        console.error('Distribution error:', error);
        res.status(500).json({ error: 'Failed to distribute event' });
    }
});
// Get orchestrator status
app.get('/status', (_req, res) => {
    res.json(orchestrator.getStatus());
});
// Get specific general
app.get('/generals/:cluster/:name', (req, res) => {
    const general = orchestrator.getGeneral(req.params.name, req.params.cluster);
    if (general) {
        res.json(general);
    }
    else {
        res.status(404).json({ error: 'General not found' });
    }
});
// Update general status
app.put('/generals/:cluster/:name/status', (req, res) => {
    const { status } = req.body;
    if (!['active', 'inactive', 'busy'].includes(status)) {
        return res.status(400).json({ error: 'Invalid status' });
    }
    const updated = orchestrator.updateGeneralStatus(req.params.name, req.params.cluster, status);
    if (updated) {
        res.json({ message: 'Status updated', name: req.params.name, cluster: req.params.cluster, status });
    }
    else {
        res.status(404).json({ error: 'General not found' });
    }
});
// Get distribution history
app.get('/distributions', (_req, res) => {
    const status = orchestrator.getStatus();
    res.json({
        total: status.total_distributions,
        recent: status.recent_distributions
    });
});
// Metrics endpoint for Prometheus
app.get('/metrics', (_req, res) => {
    const status = orchestrator.getStatus();
    const metrics = `
# HELP mindos_llm_generals_total Total number of LLM Generals
# TYPE mindos_llm_generals_total gauge
mindos_llm_generals_total ${status.total_generals}

# HELP mindos_llm_generals_active Active LLM Generals
# TYPE mindos_llm_generals_active gauge
mindos_llm_generals_active ${status.generals_by_status.active}

# HELP mindos_llm_generals_busy Busy LLM Generals
# TYPE mindos_llm_generals_busy gauge
mindos_llm_generals_busy ${status.generals_by_status.busy}

# HELP mindos_distributions_total Total number of distributions
# TYPE mindos_distributions_total counter
mindos_distributions_total ${status.total_distributions}
`;
    res.set('Content-Type', 'text/plain');
    res.send(metrics.trim());
});
const port = Number(process.env.MINDOS_PORT || 8090);
app.listen(port, () => {
    console.log(`🧠 Mind OS Orchestrator listening on port ${port}`);
    console.log(`📊 Managing ${orchestrator.getStatus().total_generals} LLM Generals`);
});
