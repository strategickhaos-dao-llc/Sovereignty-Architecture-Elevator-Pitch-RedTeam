/**
 * OBS WebSocket Server for Quantum Mirror Lab
 * Provides real-time graph visualization of agent communication
 */

const WebSocket = require('ws');
const http = require('http');

const PORT = process.env.OBS_WEBSOCKET_PORT || 4455;
const AGENT_COUNT = parseInt(process.env.AGENT_COUNT, 10) || 640;
const LAWS_COUNT = 10;
const AGENTS_PER_LAW = AGENT_COUNT / LAWS_COUNT;

// Law colors for visualization
const LAW_COLORS = {
  1: '#00ff00', // Green - Thermodynamics
  2: '#00ffff', // Cyan - Electromagnetism
  3: '#0000ff', // Blue - Quantum Mechanics
  4: '#9900ff', // Purple - General Relativity
  5: '#ff00ff', // Magenta - Statistical Mechanics
  6: '#ff9900', // Orange - Fluid Dynamics
  7: '#ffff00', // Yellow - Special Relativity
  8: '#ff0000', // Red - Solid State Physics
  9: '#00ff99', // Teal - Nuclear Physics
  10: '#ffffff' // White - Astrophysics
};

// Agent state tracking
const agents = new Map();

// Initialize agents
for (let law = 1; law <= LAWS_COUNT; law++) {
  for (let pos = 1; pos <= AGENTS_PER_LAW; pos++) {
    const id = `agent-law${law}-pos${pos}`;
    agents.set(id, {
      id,
      law,
      position: pos,
      status: 'working',
      lastActivity: Date.now(),
      discoveries: 0
    });
  }
}

// Create HTTP server
const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'healthy', agents: agents.size }));
    return;
  }
  
  if (req.url === '/graph') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(getGraphData()));
    return;
  }
  
  res.writeHead(404);
  res.end('Not Found');
});

// Create WebSocket server
const wss = new WebSocket.Server({ server });

// Broadcast to all connected clients
function broadcast(data) {
  const message = JSON.stringify(data);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// Get graph data for D3.js visualization
function getGraphData() {
  const nodes = [];
  const edges = [];
  
  agents.forEach((agent) => {
    nodes.push({
      id: agent.id,
      law: agent.law,
      position: agent.position,
      status: agent.status,
      color: LAW_COLORS[agent.law],
      discoveries: agent.discoveries
    });
  });
  
  return { nodes, edges, timestamp: Date.now() };
}

// Handle WebSocket connections
wss.on('connection', (ws) => {
  console.log('Client connected to OBS WebSocket');
  
  // Send initial graph state
  ws.send(JSON.stringify({
    type: 'init',
    data: getGraphData()
  }));
  
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      handleMessage(data, ws);
    } catch (err) {
      console.error('Invalid message:', err);
    }
  });
  
  ws.on('close', () => {
    console.log('Client disconnected from OBS WebSocket');
  });
});

// Handle incoming messages
function handleMessage(data, ws) {
  switch (data.type) {
    case 'agent_status':
      updateAgentStatus(data.agentId, data.status);
      break;
    case 'discovery':
      handleDiscovery(data.agentId, data.details);
      break;
    case 'communication':
      handleCommunication(data.from, data.to, data.message);
      break;
    case 'get_graph':
      ws.send(JSON.stringify({
        type: 'graph',
        data: getGraphData()
      }));
      break;
    default:
      console.log('Unknown message type:', data.type);
  }
}

// Update agent status
function updateAgentStatus(agentId, status) {
  const agent = agents.get(agentId);
  if (agent) {
    agent.status = status;
    agent.lastActivity = Date.now();
    
    broadcast({
      type: 'status_update',
      agentId,
      status,
      color: LAW_COLORS[agent.law]
    });
  }
}

// Handle discovery event
function handleDiscovery(agentId, details) {
  const agent = agents.get(agentId);
  if (agent) {
    agent.discoveries++;
    agent.status = 'discovery';
    
    broadcast({
      type: 'discovery',
      agentId,
      law: agent.law,
      position: agent.position,
      details,
      timestamp: Date.now()
    });
    
    // Reset status after glow effect
    setTimeout(() => {
      agent.status = 'working';
      broadcast({
        type: 'status_update',
        agentId,
        status: 'working'
      });
    }, 5000);
  }
}

// Handle agent-to-agent communication
function handleCommunication(fromId, toId, message) {
  broadcast({
    type: 'communication',
    from: fromId,
    to: toId,
    message,
    timestamp: Date.now()
  });
}

// Simulate agent activity for demo
function simulateActivity() {
  const agentIds = Array.from(agents.keys());
  const randomAgent = agentIds[Math.floor(Math.random() * agentIds.length)];
  const agent = agents.get(randomAgent);
  
  // Random status change
  const statuses = ['working', 'waiting', 'working', 'working'];
  const newStatus = statuses[Math.floor(Math.random() * statuses.length)];
  updateAgentStatus(randomAgent, newStatus);
  
  // 5% chance of discovery
  if (Math.random() < 0.05) {
    const discoveries = [
      'Memantine repurposing candidate identified',
      'CoQ10 dosing optimized',
      'Case report match found',
      'Clinical trial identified',
      'Binding affinity converged'
    ];
    handleDiscovery(randomAgent, discoveries[Math.floor(Math.random() * discoveries.length)]);
  }
  
  // 20% chance of communication
  if (Math.random() < 0.2) {
    const otherAgent = agentIds[Math.floor(Math.random() * agentIds.length)];
    if (otherAgent !== randomAgent) {
      handleCommunication(randomAgent, otherAgent, 'Sharing research data');
    }
  }
}

// Start simulation interval (demo mode)
if (process.env.DEMO_MODE === 'true') {
  setInterval(simulateActivity, 1000);
}

// Start server
server.listen(PORT, () => {
  console.log(`OBS WebSocket Server running on port ${PORT}`);
  console.log(`Tracking ${agents.size} agents across ${LAWS_COUNT} laws`);
});

module.exports = { server, wss, agents };
