// src/chess-collider/orchestrator.ts
// Chess Collider Orchestrator - 10-Dimensional AI Research Super-Collider
// Manages 640 LLM agents across 10 chess board layers

import express from 'express';
import { loadConfig, env } from '../config.js';
import { FrequencyProtocol } from './protocols.js';
import { BibliographyClient } from './bibliography.js';
import { ResearchSynthesizer } from './synthesis.js';

const app = express();
app.use(express.json({ limit: '50mb' }));

// Load configurations
const discoveryConfig = loadConfig();
const port = parseInt(env('ORCHESTRATOR_PORT', false) || '8090');
const activeLayers = parseInt(env('ACTIVE_LAYERS', false) || '1');
const agentsPerLayer = parseInt(env('AGENTS_PER_LAYER', false) || '64');

// Initialize core services
const frequencyProtocol = new FrequencyProtocol();
const bibliographyClient = new BibliographyClient();
const synthesizer = new ResearchSynthesizer();

// Agent registry: layerId -> Map<squareId, AgentInfo>
const agentRegistry = new Map<number, Map<string, AgentInfo>>();

// Active games registry
const activeGames = new Map<string, ChessGame>();

// Research queue
const researchQueue: ResearchTask[] = [];

// Types
interface AgentInfo {
  id: string;
  layerId: number;
  squareId: string;
  role: 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn';
  status: 'idle' | 'working' | 'playing' | 'offline';
  frequencyHz: number;
  lastHeartbeat: Date;
  capabilities: string[];
  currentTask?: string;
}

interface ChessGame {
  id: string;
  type: 'research_battle' | 'hypothesis_defense' | 'peer_review_challenge' | 'synthesis_tournament';
  layer1: number;
  layer2: number;
  moves: ChessMove[];
  status: 'active' | 'completed' | 'draw';
  winner?: number;
  startTime: Date;
  researchTopic?: string;
}

interface ChessMove {
  notation: string;
  timestamp: Date;
  agentId: string;
  frequencyHz: number;
  reasoning?: string;
}

interface ResearchTask {
  id: string;
  topic: string;
  status: 'queued' | 'in_progress' | 'synthesizing' | 'review' | 'completed';
  assignedLayers: number[];
  findings: ResearchFinding[];
  createdAt: Date;
  completedAt?: Date;
}

interface ResearchFinding {
  sourceLayer: number;
  agentId: string;
  content: string;
  confidence: number;
  citations: string[];
  timestamp: Date;
}

// Circle of 5ths frequency mapping (88-key piano range)
const CIRCLE_OF_FIFTHS_FREQUENCIES: Record<number, number> = {
  1: 440.00,    // A4 - Root
  2: 493.88,    // B4
  3: 554.37,    // C#5
  4: 622.25,    // D#5
  5: 698.46,    // F5
  6: 783.99,    // G5
  7: 880.00,    // A5 - Octave
  8: 987.77,    // B5
  9: 1108.73,   // C#6
  10: 1318.51,  // E6
};

// Chess piece roles per layer
const CHESS_ROLES = ['king', 'queen', 'rook', 'rook', 'bishop', 'bishop', 'knight', 'knight', 
  ...Array(56).fill('pawn')];

// =============================================================================
// API ENDPOINTS
// =============================================================================

// Health check
app.get('/health', (req, res) => {
  const totalAgents = Array.from(agentRegistry.values())
    .reduce((sum, layer) => sum + layer.size, 0);
  
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    collider: {
      activeLayers,
      totalAgents,
      activeGames: activeGames.size,
      researchQueueSize: researchQueue.length,
      agentsPerLayer
    }
  });
});

// Get collider status
app.get('/status', (req, res) => {
  const layerStatus = [];
  for (let i = 1; i <= activeLayers; i++) {
    const layer = agentRegistry.get(i) || new Map();
    const agents = Array.from(layer.values());
    layerStatus.push({
      layerId: i,
      frequencyHz: CIRCLE_OF_FIFTHS_FREQUENCIES[i],
      totalAgents: agents.length,
      activeAgents: agents.filter(a => a.status !== 'offline').length,
      workingAgents: agents.filter(a => a.status === 'working').length,
      playingAgents: agents.filter(a => a.status === 'playing').length
    });
  }

  res.json({
    collider: {
      name: 'Sovereign AI Research Super-Collider',
      activeLayers,
      maxLayers: 10,
      agentsPerLayer,
      totalCapacity: 640
    },
    layers: layerStatus,
    games: {
      active: activeGames.size,
      completed: 0 // TODO: track completed games
    },
    research: {
      queued: researchQueue.filter(t => t.status === 'queued').length,
      inProgress: researchQueue.filter(t => t.status === 'in_progress').length,
      completed: researchQueue.filter(t => t.status === 'completed').length
    }
  });
});

// Register an agent
app.post('/agents/register', (req, res) => {
  const { layerId, squareId, role, capabilities } = req.body;

  if (!layerId || !squareId || !role) {
    return res.status(400).json({ error: 'Missing required fields: layerId, squareId, role' });
  }

  if (layerId < 1 || layerId > 10) {
    return res.status(400).json({ error: 'Layer ID must be between 1 and 10' });
  }

  if (!agentRegistry.has(layerId)) {
    agentRegistry.set(layerId, new Map());
  }

  const agentId = `layer${layerId}-${squareId}`;
  const agent: AgentInfo = {
    id: agentId,
    layerId,
    squareId,
    role,
    status: 'idle',
    frequencyHz: CIRCLE_OF_FIFTHS_FREQUENCIES[layerId],
    lastHeartbeat: new Date(),
    capabilities: capabilities || []
  };

  agentRegistry.get(layerId)!.set(squareId, agent);

  console.log(`🎯 Agent registered: ${agentId} (${role}) at ${agent.frequencyHz}Hz`);

  res.status(201).json({
    agentId,
    frequencyHz: agent.frequencyHz,
    message: 'Agent registered successfully'
  });
});

// Agent heartbeat
app.post('/agents/:agentId/heartbeat', (req, res) => {
  const { agentId } = req.params;
  const { status, currentTask } = req.body;

  // Parse layer from agentId
  const match = agentId.match(/layer(\d+)-/);
  if (!match) {
    return res.status(400).json({ error: 'Invalid agent ID format' });
  }

  const layerId = parseInt(match[1]);
  const layer = agentRegistry.get(layerId);
  
  if (!layer) {
    return res.status(404).json({ error: 'Layer not found' });
  }

  // Find agent in layer
  for (const [squareId, agent] of layer.entries()) {
    if (agent.id === agentId) {
      agent.lastHeartbeat = new Date();
      if (status) agent.status = status;
      if (currentTask !== undefined) agent.currentTask = currentTask;
      
      return res.json({
        acknowledged: true,
        nextTask: getNextTaskForAgent(agent)
      });
    }
  }

  res.status(404).json({ error: 'Agent not found' });
});

// Create a research task
app.post('/research/create', async (req, res) => {
  const { topic, targetLayers, priority } = req.body;

  if (!topic) {
    return res.status(400).json({ error: 'Missing required field: topic' });
  }

  const taskId = `research-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const task: ResearchTask = {
    id: taskId,
    topic,
    status: 'queued',
    assignedLayers: targetLayers || [1, 2, 3, 4, 5], // Default to first 5 layers
    findings: [],
    createdAt: new Date()
  };

  researchQueue.push(task);
  console.log(`📚 Research task created: ${taskId} - "${topic}"`);

  // Start processing
  processResearchTask(task);

  res.status(201).json({
    taskId,
    status: 'queued',
    message: 'Research task created and queued for processing'
  });
});

// Get research task status
app.get('/research/:taskId', (req, res) => {
  const { taskId } = req.params;
  const task = researchQueue.find(t => t.id === taskId);

  if (!task) {
    return res.status(404).json({ error: 'Research task not found' });
  }

  res.json({
    task: {
      id: task.id,
      topic: task.topic,
      status: task.status,
      assignedLayers: task.assignedLayers,
      findingsCount: task.findings.length,
      createdAt: task.createdAt,
      completedAt: task.completedAt
    },
    findings: task.findings.slice(-10) // Last 10 findings
  });
});

// Start an adversarial chess game between layers
app.post('/games/start', (req, res) => {
  const { type, layer1, layer2, researchTopic } = req.body;

  if (!type || !layer1 || !layer2) {
    return res.status(400).json({ error: 'Missing required fields: type, layer1, layer2' });
  }

  const validTypes = ['research_battle', 'hypothesis_defense', 'peer_review_challenge', 'synthesis_tournament'];
  if (!validTypes.includes(type)) {
    return res.status(400).json({ error: `Invalid game type. Must be one of: ${validTypes.join(', ')}` });
  }

  const gameId = `game-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const game: ChessGame = {
    id: gameId,
    type,
    layer1,
    layer2,
    moves: [],
    status: 'active',
    startTime: new Date(),
    researchTopic
  };

  activeGames.set(gameId, game);
  console.log(`♟️ Game started: ${gameId} - ${type} between Layer ${layer1} and Layer ${layer2}`);

  // Notify layer coordinators
  broadcastToLayer(layer1, {
    type: 'game_start',
    gameId,
    opponent: layer2,
    playingAs: 'white'
  });

  broadcastToLayer(layer2, {
    type: 'game_start',
    gameId,
    opponent: layer1,
    playingAs: 'black'
  });

  res.status(201).json({
    gameId,
    status: 'active',
    message: `${type} game started between Layer ${layer1} and Layer ${layer2}`
  });
});

// Submit a chess move
app.post('/games/:gameId/move', (req, res) => {
  const { gameId } = req.params;
  const { notation, agentId, reasoning } = req.body;

  const game = activeGames.get(gameId);
  if (!game) {
    return res.status(404).json({ error: 'Game not found' });
  }

  if (game.status !== 'active') {
    return res.status(400).json({ error: 'Game is not active' });
  }

  // Parse agent's layer from ID
  const match = agentId.match(/layer(\d+)-/);
  const layerId = match ? parseInt(match[1]) : 0;

  const move: ChessMove = {
    notation,
    timestamp: new Date(),
    agentId,
    frequencyHz: CIRCLE_OF_FIFTHS_FREQUENCIES[layerId] || 440,
    reasoning
  };

  game.moves.push(move);
  console.log(`♟️ Move in ${gameId}: ${notation} by ${agentId}`);

  res.json({
    accepted: true,
    moveNumber: game.moves.length,
    notation
  });
});

// Get game status
app.get('/games/:gameId', (req, res) => {
  const { gameId } = req.params;
  const game = activeGames.get(gameId);

  if (!game) {
    return res.status(404).json({ error: 'Game not found' });
  }

  res.json({
    game: {
      id: game.id,
      type: game.type,
      layer1: game.layer1,
      layer2: game.layer2,
      status: game.status,
      movesCount: game.moves.length,
      winner: game.winner,
      startTime: game.startTime,
      researchTopic: game.researchTopic
    },
    moves: game.moves.slice(-10) // Last 10 moves
  });
});

// Frequency sync endpoint (handshake protocol)
app.post('/protocol/frequency-sync', (req, res) => {
  const { sourceLayerId, targetLayerId, message, encoding } = req.body;

  if (!sourceLayerId || !targetLayerId) {
    return res.status(400).json({ error: 'Missing required fields: sourceLayerId, targetLayerId' });
  }

  const sourceFreq = CIRCLE_OF_FIFTHS_FREQUENCIES[sourceLayerId];
  const targetFreq = CIRCLE_OF_FIFTHS_FREQUENCIES[targetLayerId];

  // Calculate frequency relationship (harmonic analysis)
  const ratio = targetFreq / sourceFreq;
  const harmonicDistance = Math.abs(Math.log2(ratio) * 12); // Semitones

  const syncResult = frequencyProtocol.sync({
    sourceFreq,
    targetFreq,
    message,
    encoding: encoding || '88_key_piano'
  });

  res.json({
    synced: true,
    sourceFrequencyHz: sourceFreq,
    targetFrequencyHz: targetFreq,
    harmonicDistance: harmonicDistance.toFixed(2),
    interval: getMusicalInterval(harmonicDistance),
    encodedMessage: syncResult.encoded
  });
});

// Bibliography search endpoint
app.post('/bibliography/search', async (req, res) => {
  const { query, sources, maxResults } = req.body;

  if (!query) {
    return res.status(400).json({ error: 'Missing required field: query' });
  }

  try {
    const results = await bibliographyClient.search({
      query,
      sources: sources || ['arxiv', 'semantic_scholar'],
      maxResults: maxResults || 20
    });

    res.json({
      query,
      resultsCount: results.length,
      results
    });
  } catch (error: any) {
    console.error('Bibliography search error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Synthesize research findings
app.post('/synthesis/generate', async (req, res) => {
  const { taskId, findings, outputFormat } = req.body;

  if (!findings || !Array.isArray(findings)) {
    return res.status(400).json({ error: 'Missing required field: findings (array)' });
  }

  try {
    const synthesis = await synthesizer.synthesize({
      taskId: taskId || `synthesis-${Date.now()}`,
      findings,
      outputFormat: outputFormat || 'markdown'
    });

    res.json({
      synthesisId: synthesis.id,
      format: outputFormat || 'markdown',
      wordCount: synthesis.wordCount,
      citationsCount: synthesis.citations.length,
      content: synthesis.content
    });
  } catch (error: any) {
    console.error('Synthesis error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Metrics endpoint for Prometheus
app.get('/metrics', (req, res) => {
  const totalAgents = Array.from(agentRegistry.values())
    .reduce((sum, layer) => sum + layer.size, 0);
  
  const activeAgents = Array.from(agentRegistry.values())
    .reduce((sum, layer) => {
      return sum + Array.from(layer.values()).filter(a => a.status !== 'offline').length;
    }, 0);

  const metrics = `
# HELP chess_collider_agents_total Total number of registered agents
# TYPE chess_collider_agents_total gauge
chess_collider_agents_total ${totalAgents}

# HELP chess_collider_agents_active Number of active agents
# TYPE chess_collider_agents_active gauge
chess_collider_agents_active ${activeAgents}

# HELP chess_collider_layers_active Number of active layers
# TYPE chess_collider_layers_active gauge
chess_collider_layers_active ${activeLayers}

# HELP chess_collider_games_active Number of active games
# TYPE chess_collider_games_active gauge
chess_collider_games_active ${activeGames.size}

# HELP chess_collider_research_tasks_total Total research tasks by status
# TYPE chess_collider_research_tasks_total gauge
chess_collider_research_tasks_total{status="queued"} ${researchQueue.filter(t => t.status === 'queued').length}
chess_collider_research_tasks_total{status="in_progress"} ${researchQueue.filter(t => t.status === 'in_progress').length}
chess_collider_research_tasks_total{status="completed"} ${researchQueue.filter(t => t.status === 'completed').length}
`;

  res.set('Content-Type', 'text/plain');
  res.send(metrics.trim());
});

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function getNextTaskForAgent(agent: AgentInfo): object | null {
  // Find queued research tasks for this agent's layer
  const task = researchQueue.find(t => 
    t.status === 'in_progress' && 
    t.assignedLayers.includes(agent.layerId) &&
    agent.status === 'idle'
  );

  if (task) {
    return {
      type: 'research',
      taskId: task.id,
      topic: task.topic,
      instruction: getLayerInstruction(agent.layerId, task.topic)
    };
  }

  return null;
}

function getLayerInstruction(layerId: number, topic: string): string {
  const instructions: Record<number, string> = {
    1: `Collect and scrape bibliographic data related to: ${topic}`,
    2: `Analyze patterns in collected data for: ${topic}`,
    3: `Extract semantic meaning and relationships for: ${topic}`,
    4: `Apply logical reasoning and formal analysis to: ${topic}`,
    5: `Generate novel hypotheses based on: ${topic}`,
    6: `Design experimental frameworks to test: ${topic}`,
    7: `Critically evaluate and peer review findings on: ${topic}`,
    8: `Synthesize knowledge and create unified theory for: ${topic}`,
    9: `Prepare academic publication draft for: ${topic}`,
    10: `Develop strategic research direction for: ${topic}`
  };

  return instructions[layerId] || `Process research task: ${topic}`;
}

function broadcastToLayer(layerId: number, message: object): void {
  const layer = agentRegistry.get(layerId);
  if (!layer) return;

  // In production, this would use WebSocket or message queue
  console.log(`📡 Broadcasting to Layer ${layerId}:`, JSON.stringify(message).slice(0, 100));
}

async function processResearchTask(task: ResearchTask): Promise<void> {
  task.status = 'in_progress';
  console.log(`🔬 Processing research task: ${task.id}`);

  // In production, this would orchestrate actual agent work
  // For now, simulate the process
  
  for (const layerId of task.assignedLayers) {
    broadcastToLayer(layerId, {
      type: 'research_task',
      taskId: task.id,
      topic: task.topic,
      instruction: getLayerInstruction(layerId, task.topic)
    });
  }
}

function getMusicalInterval(semitones: number): string {
  const intervals: Record<number, string> = {
    0: 'Unison',
    1: 'Minor 2nd',
    2: 'Major 2nd',
    3: 'Minor 3rd',
    4: 'Major 3rd',
    5: 'Perfect 4th',
    6: 'Tritone',
    7: 'Perfect 5th',
    8: 'Minor 6th',
    9: 'Major 6th',
    10: 'Minor 7th',
    11: 'Major 7th',
    12: 'Octave'
  };

  const rounded = Math.round(semitones) % 12;
  return intervals[rounded] || `${semitones.toFixed(1)} semitones`;
}

// =============================================================================
// ERROR HANDLING
// =============================================================================

app.use((error: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Chess Collider API error:', error);
  res.status(500).json({
    error: 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

// =============================================================================
// START SERVER
// =============================================================================

app.listen(port, () => {
  console.log(`
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎯 CHESS COLLIDER ORCHESTRATOR ONLINE 🎯                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Port: ${port.toString().padEnd(71)}║
║  Active Layers: ${activeLayers.toString().padEnd(62)}║
║  Agents per Layer: ${agentsPerLayer.toString().padEnd(58)}║
║  Total Capacity: 640 agents (10 boards × 64 squares)                         ║
║  Communication: Circle of 5ths frequency protocol (440Hz - 1318Hz)           ║
╚══════════════════════════════════════════════════════════════════════════════╝
  `);
});

export { app };
