// src/chess-collider/agent.ts
// Chess Collider Agent - Individual LLM Agent with Terminal Access
// Part of the 10-Dimensional AI Research Super-Collider
import express from 'express';
import fetch from 'node-fetch';
const app = express();
app.use(express.json());
// Environment configuration
const LAYER_ID = parseInt(process.env.LAYER_ID || '1');
const LAYER_NAME = process.env.LAYER_NAME || 'empirical_data';
const AGENT_ROLE = process.env.AGENT_ROLE || 'pawn';
const WORKER_COUNT = parseInt(process.env.WORKER_COUNT || '1');
const COMMUNICATION_FREQ_HZ = parseFloat(process.env.COMMUNICATION_FREQ_HZ || '440');
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';
const ORCHESTRATOR_URL = process.env.ORCHESTRATOR_URL || 'http://localhost:8090';
const AGENT_PORT = parseInt(process.env.AGENT_PORT || '8100');
// Initialize agent state
const agentId = `layer${LAYER_ID}-${AGENT_ROLE}-${Math.random().toString(36).slice(2, 8)}`;
const state = {
    id: agentId,
    layerId: LAYER_ID,
    layerName: LAYER_NAME,
    role: AGENT_ROLE,
    frequencyHz: COMMUNICATION_FREQ_HZ,
    status: 'idle',
    currentTask: null,
    completedTasks: 0,
    findings: [],
    lastHeartbeat: new Date()
};
// Layer-specific capabilities
const LAYER_CAPABILITIES = {
    1: ['scraping', 'data_collection', 'parsing', 'raw_processing'],
    2: ['pattern_detection', 'statistical_analysis', 'feature_extraction'],
    3: ['nlp', 'semantic_analysis', 'entity_extraction', 'summarization'],
    4: ['logical_reasoning', 'theorem_proving', 'formal_verification'],
    5: ['hypothesis_generation', 'creative_synthesis', 'ideation'],
    6: ['experimental_design', 'methodology', 'protocol_creation'],
    7: ['peer_review', 'critical_analysis', 'adversarial_evaluation'],
    8: ['knowledge_synthesis', 'integration', 'meta_analysis'],
    9: ['academic_writing', 'publication_prep', 'formatting'],
    10: ['strategic_planning', 'direction_setting', 'coordination']
};
// =============================================================================
// API ENDPOINTS
// =============================================================================
// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        agent: {
            id: state.id,
            layerId: state.layerId,
            role: state.role,
            status: state.status,
            frequencyHz: state.frequencyHz
        },
        timestamp: new Date().toISOString()
    });
});
// Get agent status
app.get('/status', (req, res) => {
    res.json({
        agent: state,
        capabilities: LAYER_CAPABILITIES[state.layerId] || [],
        metrics: {
            completedTasks: state.completedTasks,
            findingsCount: state.findings.length,
            uptime: Date.now() - state.lastHeartbeat.getTime()
        }
    });
});
// Process task assignment
app.post('/task', async (req, res) => {
    const task = req.body;
    if (!task.type || !task.taskId) {
        return res.status(400).json({ error: 'Invalid task format' });
    }
    console.log(`📋 Received task: ${task.type} - ${task.topic || task.taskId}`);
    state.status = 'working';
    state.currentTask = task.taskId;
    try {
        const result = await processTask(task);
        state.status = 'idle';
        state.currentTask = null;
        state.completedTasks++;
        res.json({
            success: true,
            taskId: task.taskId,
            result
        });
    }
    catch (error) {
        state.status = 'idle';
        state.currentTask = null;
        console.error(`❌ Task failed: ${error.message}`);
        res.status(500).json({ error: error.message });
    }
});
// Receive chess game move request
app.post('/game/move', async (req, res) => {
    const { gameId, position, opponentMove } = req.body;
    state.status = 'playing';
    try {
        const move = await calculateMove(position, opponentMove);
        res.json({
            success: true,
            move,
            reasoning: move.reasoning
        });
    }
    catch (error) {
        res.status(500).json({ error: error.message });
    }
    finally {
        state.status = 'idle';
    }
});
// Frequency sync endpoint
app.post('/frequency/sync', (req, res) => {
    const { sourceFrequency, message } = req.body;
    // Calculate harmonic relationship
    const ratio = state.frequencyHz / sourceFrequency;
    const harmonicMatch = isHarmonicCompatible(sourceFrequency, state.frequencyHz);
    res.json({
        synced: harmonicMatch,
        agentFrequency: state.frequencyHz,
        sourceFrequency,
        harmonicRatio: ratio,
        acknowledged: true
    });
});
// =============================================================================
// TASK PROCESSING
// =============================================================================
async function processTask(task) {
    console.log(`🔄 Processing task: ${task.instruction?.slice(0, 100) || task.topic}`);
    // Generate finding based on layer capabilities
    const finding = await generateFinding(task);
    // Store finding
    state.findings.push(finding);
    // Report to orchestrator
    await reportFinding(task.taskId, finding);
    return finding;
}
async function generateFinding(task) {
    const layerPrompt = getLayerPrompt(state.layerId, task);
    try {
        // Use Ollama for LLM processing
        const response = await fetch(`${OLLAMA_URL}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: process.env.LLM_MODEL || 'llama3.2:latest',
                prompt: layerPrompt,
                stream: false,
                options: {
                    temperature: getLayerTemperature(state.layerId),
                    num_predict: 1000
                }
            })
        });
        if (!response.ok) {
            throw new Error(`LLM API error: ${response.status}`);
        }
        const data = await response.json();
        return {
            id: `finding-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            content: data.response || '[No response from LLM]',
            confidence: calculateConfidence(data.response),
            citations: extractCitations(data.response),
            timestamp: new Date()
        };
    }
    catch (error) {
        console.error('LLM generation failed:', error);
        // Return placeholder finding
        return {
            id: `finding-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            content: `[Layer ${state.layerId}] Processing task: ${task.topic}. LLM unavailable - placeholder response.`,
            confidence: 0.5,
            citations: [],
            timestamp: new Date()
        };
    }
}
function getLayerPrompt(layerId, task) {
    const prompts = {
        1: `You are a data collection specialist. Search and collect relevant information about: ${task.topic}
        Focus on: finding primary sources, raw data, and initial observations.
        Provide structured data with sources.`,
        2: `You are a pattern recognition expert. Analyze the following topic for patterns: ${task.topic}
        Focus on: statistical patterns, trends, correlations, and anomalies.
        Provide quantitative analysis where possible.`,
        3: `You are a semantic analysis specialist. Provide deep semantic understanding of: ${task.topic}
        Focus on: meaning, context, relationships, and implications.
        Extract key entities and their relationships.`,
        4: `You are a logical reasoning expert. Apply formal logic to analyze: ${task.topic}
        Focus on: logical implications, consistency, proofs, and formal arguments.
        Identify any logical fallacies or gaps.`,
        5: `You are a hypothesis generation specialist. Generate novel hypotheses about: ${task.topic}
        Focus on: creative connections, unexplored angles, and testable predictions.
        Propose at least 3 distinct hypotheses.`,
        6: `You are an experimental design expert. Design methodology to test: ${task.topic}
        Focus on: experimental protocols, variables, controls, and measurement.
        Propose a rigorous research methodology.`,
        7: `You are a peer reviewer. Critically evaluate research on: ${task.topic}
        Focus on: strengths, weaknesses, methodology flaws, and validity.
        Provide constructive criticism and improvement suggestions.`,
        8: `You are a knowledge synthesizer. Integrate all findings about: ${task.topic}
        Focus on: unified theory, reconciling contradictions, and key insights.
        Create a coherent synthesis of available knowledge.`,
        9: `You are an academic writer. Prepare publication-ready content about: ${task.topic}
        Focus on: clear structure, academic tone, proper citations.
        Write in formal academic style.`,
        10: `You are a strategic research director. Provide strategic direction for: ${task.topic}
         Focus on: research priorities, resource allocation, future directions.
         Outline a strategic research roadmap.`
    };
    return prompts[layerId] || `Analyze the following topic from your expert perspective: ${task.topic}`;
}
function getLayerTemperature(layerId) {
    // Lower temperature for analytical layers, higher for creative
    const temperatures = {
        1: 0.3, // Data collection - precise
        2: 0.4, // Pattern recognition - analytical
        3: 0.5, // Semantic - balanced
        4: 0.2, // Logic - very precise
        5: 0.8, // Hypothesis - creative
        6: 0.5, // Methodology - balanced
        7: 0.4, // Peer review - critical
        8: 0.6, // Synthesis - moderately creative
        9: 0.5, // Publication - formal
        10: 0.7 // Strategy - visionary
    };
    return temperatures[layerId] || 0.5;
}
function calculateConfidence(content) {
    // Simple heuristic for confidence
    if (!content)
        return 0.1;
    const length = content.length;
    const hasCitations = /\[\d+\]|\(.*\d{4}\)/.test(content);
    const hasNumbers = /\d+%|\d+\.\d+/.test(content);
    let confidence = 0.5;
    if (length > 500)
        confidence += 0.1;
    if (length > 1000)
        confidence += 0.1;
    if (hasCitations)
        confidence += 0.15;
    if (hasNumbers)
        confidence += 0.1;
    return Math.min(confidence, 0.95);
}
function extractCitations(content) {
    const citations = [];
    // Extract bracketed citations [1], [2], etc.
    const bracketMatches = content.match(/\[(\d+)\]/g);
    if (bracketMatches) {
        citations.push(...bracketMatches);
    }
    // Extract parenthetical citations (Author, Year)
    const parentheticalMatches = content.match(/\([A-Z][a-z]+ et al\.,? \d{4}\)/g);
    if (parentheticalMatches) {
        citations.push(...parentheticalMatches);
    }
    return [...new Set(citations)];
}
async function reportFinding(taskId, finding) {
    try {
        await fetch(`${ORCHESTRATOR_URL}/findings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                taskId,
                agentId: state.id,
                layerId: state.layerId,
                finding
            })
        });
        console.log(`📤 Reported finding to orchestrator`);
    }
    catch (error) {
        console.error('Failed to report finding:', error);
    }
}
// =============================================================================
// CHESS GAME LOGIC
// =============================================================================
async function calculateMove(position, opponentMove) {
    // Use LLM to decide move based on layer's strategic perspective
    const prompt = `You are playing chess as part of a research validation game.
Your layer specializes in: ${LAYER_CAPABILITIES[state.layerId]?.join(', ') || 'general analysis'}

Current position: ${position || 'starting position'}
Opponent's last move: ${opponentMove || 'none (your move first)'}

Decide your next move. Consider:
1. Strategic objectives aligned with your layer's expertise
2. Adversarial validation of research findings
3. Long-term position building

Respond with:
- MOVE: [algebraic notation, e.g., e4, Nf3, O-O]
- REASONING: [brief explanation]`;
    try {
        const response = await fetch(`${OLLAMA_URL}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: process.env.LLM_MODEL || 'llama3.2:latest',
                prompt,
                stream: false,
                options: { temperature: 0.5, num_predict: 200 }
            })
        });
        const data = await response.json();
        const content = data.response || '';
        // Parse move from response
        const moveMatch = content.match(/MOVE:\s*([a-h][1-8]|[KQRBN][a-h]?[1-8]?x?[a-h][1-8]|O-O(?:-O)?)/i);
        const reasoningMatch = content.match(/REASONING:\s*(.+)/i);
        return {
            notation: moveMatch ? moveMatch[1] : 'e4', // Default opening move
            reasoning: reasoningMatch ? reasoningMatch[1].trim() : 'Strategic positioning'
        };
    }
    catch {
        return {
            notation: 'e4',
            reasoning: 'Default opening move (LLM unavailable)'
        };
    }
}
// =============================================================================
// FREQUENCY HARMONICS
// =============================================================================
function isHarmonicCompatible(freq1, freq2) {
    const ratio = Math.max(freq1, freq2) / Math.min(freq1, freq2);
    // Check for harmonic ratios (within 1% tolerance)
    const harmonicRatios = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8]; // Octaves, fifths, etc.
    for (const harmonic of harmonicRatios) {
        if (Math.abs(ratio - harmonic) < 0.01 * harmonic) {
            return true;
        }
    }
    return false;
}
// =============================================================================
// HEARTBEAT & REGISTRATION
// =============================================================================
async function registerWithOrchestrator() {
    try {
        const response = await fetch(`${ORCHESTRATOR_URL}/agents/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                layerId: state.layerId,
                squareId: state.id.split('-').slice(-1)[0],
                role: state.role,
                capabilities: LAYER_CAPABILITIES[state.layerId] || []
            })
        });
        if (response.ok) {
            console.log(`✅ Registered with orchestrator as ${state.id}`);
        }
    }
    catch (error) {
        console.error('Failed to register with orchestrator:', error);
    }
}
async function sendHeartbeat() {
    try {
        const response = await fetch(`${ORCHESTRATOR_URL}/agents/${state.id}/heartbeat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: state.status,
                currentTask: state.currentTask
            })
        });
        if (response.ok) {
            const data = await response.json();
            state.lastHeartbeat = new Date();
            // Process next task if assigned
            if (data.nextTask) {
                processTask(data.nextTask);
            }
        }
    }
    catch {
        // Silently fail heartbeat - orchestrator may be restarting
    }
}
// =============================================================================
// START AGENT
// =============================================================================
app.listen(AGENT_PORT, async () => {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║               🎯 CHESS COLLIDER AGENT ONLINE 🎯               ║
╠═══════════════════════════════════════════════════════════════╣
║  Agent ID: ${state.id.padEnd(47)}║
║  Layer: ${state.layerId} (${state.layerName})${' '.repeat(Math.max(0, 38 - state.layerName.length))}║
║  Role: ${state.role.padEnd(49)}║
║  Frequency: ${state.frequencyHz} Hz${' '.repeat(Math.max(0, 41 - String(state.frequencyHz).length))}║
║  Port: ${AGENT_PORT}${' '.repeat(49)}║
╚═══════════════════════════════════════════════════════════════╝
  `);
    // Register with orchestrator
    await registerWithOrchestrator();
    // Start heartbeat loop
    setInterval(sendHeartbeat, 30000); // Every 30 seconds
});
export { app };
