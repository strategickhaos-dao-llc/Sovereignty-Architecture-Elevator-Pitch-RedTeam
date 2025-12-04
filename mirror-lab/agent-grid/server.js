/**
 * Agent Grid Server - Mirror Lab
 * 
 * Displays 80 agents in a grid (8 rows x 10 columns)
 * Click any agent to watch their terminal/screen in real-time
 * 
 * Features:
 * - Real-time agent status via WebSocket
 * - Click-to-watch agent terminal streaming
 * - Department color coding
 * - Activity indicators
 */

import express from 'express';
import { WebSocketServer } from 'ws';
import { createClient } from 'redis';
import { createServer } from 'http';

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server, path: '/ws' });

const AGENT_COUNT = parseInt(process.env.AGENT_COUNT || '80');
const GRID_ROWS = parseInt(process.env.GRID_ROWS || '8');
const GRID_COLS = parseInt(process.env.GRID_COLS || '10');
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const PORT = parseInt(process.env.PORT || '3000');
const WS_PORT = parseInt(process.env.WEBSOCKET_PORT || '8090');

// Department definitions with colors
const DEPARTMENTS = [
  { id: 'lit_review', name: 'Literature Review', color: '#4CAF50', icon: '📚' },
  { id: 'drug_discovery', name: 'Drug Discovery', color: '#2196F3', icon: '💊' },
  { id: 'molecular', name: 'Molecular Modeling', color: '#9C27B0', icon: '🧬' },
  { id: 'quantum', name: 'Quantum Computing', color: '#FF9800', icon: '⚛️' },
  { id: 'clinical', name: 'Clinical Analysis', color: '#F44336', icon: '🏥' },
  { id: 'cost', name: 'Cost Estimation', color: '#FFEB3B', icon: '💰' },
  { id: 'safety', name: 'Safety Analysis', color: '#00BCD4', icon: '🛡️' },
  { id: 'regulatory', name: 'Regulatory Pathway', color: '#795548', icon: '📋' },
  { id: 'synthesis', name: 'Data Synthesis', color: '#607D8B', icon: '📊' },
  { id: 'reporting', name: 'Report Generation', color: '#E91E63', icon: '📝' }
];

// Initialize agents
const agents = Array.from({ length: AGENT_COUNT }, (_, i) => ({
  id: `agent-${String(i + 1).padStart(2, '0')}`,
  name: `Agent ${String.fromCharCode(65 + Math.floor(i / 10))}${(i % 10) + 1}`,
  department: DEPARTMENTS[i % DEPARTMENTS.length],
  status: 'idle',
  currentTask: null,
  lastActivity: new Date().toISOString(),
  metrics: {
    papersAnalyzed: 0,
    drugsFound: 0,
    tasksCompleted: 0
  }
}));

// Redis client for pub/sub
let redis;
async function connectRedis() {
  try {
    redis = createClient({ url: REDIS_URL });
    await redis.connect();
    console.log('Connected to Redis');
    
    // Subscribe to agent updates
    const subscriber = redis.duplicate();
    await subscriber.connect();
    await subscriber.subscribe('agent-updates', (message) => {
      const update = JSON.parse(message);
      broadcastToClients({ type: 'agent-update', data: update });
    });
  } catch (err) {
    console.log('Redis not available, running in standalone mode');
  }
}

// Broadcast to all WebSocket clients
function broadcastToClients(message) {
  wss.clients.forEach(client => {
    if (client.readyState === 1) { // WebSocket.OPEN
      client.send(JSON.stringify(message));
    }
  });
}

// WebSocket connection handler
wss.on('connection', (ws) => {
  console.log('Client connected');
  
  // Send initial agent grid state
  ws.send(JSON.stringify({
    type: 'init',
    data: {
      agents,
      departments: DEPARTMENTS,
      gridConfig: { rows: GRID_ROWS, cols: GRID_COLS }
    }
  }));
  
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      if (data.type === 'watch-agent') {
        // Client wants to watch a specific agent
        ws.agentWatch = data.agentId;
        ws.send(JSON.stringify({
          type: 'watching',
          data: { agentId: data.agentId }
        }));
      }
    } catch (err) {
      console.error('Invalid message:', err);
    }
  });
  
  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// Simulate agent activity (demo mode)
function simulateAgentActivity() {
  const agentIndex = Math.floor(Math.random() * agents.length);
  const agent = agents[agentIndex];
  
  const activities = [
    { status: 'working', task: 'Scraping PubMed for NMDA receptor papers' },
    { status: 'working', task: 'Running AlphaFold3 prediction' },
    { status: 'working', task: 'Analyzing binding site geometry' },
    { status: 'working', task: 'Calculating molecular dynamics' },
    { status: 'working', task: 'Querying clinical trial databases' },
    { status: 'working', task: 'Estimating treatment costs' },
    { status: 'working', task: 'Reviewing safety profiles' },
    { status: 'working', task: 'Mapping regulatory requirements' },
    { status: 'working', task: 'Synthesizing research findings' },
    { status: 'working', task: 'Generating report section' },
    { status: 'idle', task: null }
  ];
  
  const activity = activities[Math.floor(Math.random() * activities.length)];
  agent.status = activity.status;
  agent.currentTask = activity.task;
  agent.lastActivity = new Date().toISOString();
  
  if (activity.status === 'working') {
    const metric = ['papersAnalyzed', 'drugsFound', 'tasksCompleted'][Math.floor(Math.random() * 3)];
    agent.metrics[metric]++;
  }
  
  broadcastToClients({
    type: 'agent-update',
    data: agent
  });
}

// Start simulation in demo mode
setInterval(simulateAgentActivity, 500);

// Express routes
app.use(express.static('public'));

app.get('/api/agents', (req, res) => {
  res.json(agents);
});

app.get('/api/agents/:id', (req, res) => {
  const agent = agents.find(a => a.id === req.params.id);
  if (agent) {
    res.json(agent);
  } else {
    res.status(404).json({ error: 'Agent not found' });
  }
});

app.get('/api/departments', (req, res) => {
  res.json(DEPARTMENTS);
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', agents: agents.length });
});

// Serve the main HTML page
app.get('/', (req, res) => {
  res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🤖 Agent Grid - Mirror Lab</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0a0a0f;
      color: #fff;
      min-height: 100vh;
    }
    .header {
      background: linear-gradient(90deg, #1a1a2e, #16213e);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #0f3460;
    }
    .header h1 { font-size: 1.5rem; }
    .stats {
      display: flex;
      gap: 2rem;
    }
    .stat {
      text-align: center;
    }
    .stat-value {
      font-size: 1.5rem;
      font-weight: bold;
      color: #00ff88;
    }
    .stat-label {
      font-size: 0.75rem;
      color: #888;
    }
    .grid-container {
      padding: 1rem;
      display: grid;
      grid-template-columns: repeat(10, 1fr);
      gap: 0.5rem;
      max-width: 1800px;
      margin: 0 auto;
    }
    .agent-card {
      background: #1a1a2e;
      border-radius: 8px;
      padding: 0.5rem;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 2px solid transparent;
      position: relative;
      min-height: 80px;
    }
    .agent-card:hover {
      transform: scale(1.05);
      z-index: 10;
      border-color: #00ff88;
    }
    .agent-card.working {
      animation: pulse 2s infinite;
    }
    .agent-card.selected {
      border-color: #ff6b6b;
      box-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
    }
    @keyframes pulse {
      0%, 100% { box-shadow: 0 0 5px rgba(0, 255, 136, 0.3); }
      50% { box-shadow: 0 0 15px rgba(0, 255, 136, 0.6); }
    }
    .agent-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.25rem;
    }
    .agent-name {
      font-weight: bold;
      font-size: 0.8rem;
    }
    .agent-status {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #444;
    }
    .agent-status.working { background: #00ff88; }
    .agent-status.idle { background: #666; }
    .agent-dept {
      font-size: 0.65rem;
      color: #888;
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    .dept-color {
      width: 6px;
      height: 6px;
      border-radius: 50%;
    }
    .agent-task {
      font-size: 0.6rem;
      color: #aaa;
      margin-top: 0.25rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .detail-panel {
      position: fixed;
      right: 0;
      top: 0;
      width: 400px;
      height: 100vh;
      background: #16213e;
      border-left: 2px solid #0f3460;
      padding: 1rem;
      transform: translateX(100%);
      transition: transform 0.3s ease;
      z-index: 100;
    }
    .detail-panel.open { transform: translateX(0); }
    .close-btn {
      position: absolute;
      top: 1rem;
      right: 1rem;
      background: none;
      border: none;
      color: #fff;
      font-size: 1.5rem;
      cursor: pointer;
    }
    .terminal {
      background: #000;
      border-radius: 8px;
      padding: 1rem;
      font-family: 'Fira Code', monospace;
      font-size: 0.75rem;
      height: 300px;
      overflow-y: auto;
      margin-top: 1rem;
    }
    .terminal-line {
      color: #00ff88;
      margin-bottom: 0.25rem;
    }
    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      padding: 0.5rem 2rem;
      background: #16213e;
      border-bottom: 1px solid #0f3460;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.75rem;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>🤖 AGENT GRID - 80 Agents Working</h1>
    <div class="stats">
      <div class="stat">
        <div class="stat-value" id="active-count">0</div>
        <div class="stat-label">Active</div>
      </div>
      <div class="stat">
        <div class="stat-value" id="papers-count">0</div>
        <div class="stat-label">Papers</div>
      </div>
      <div class="stat">
        <div class="stat-value" id="drugs-count">0</div>
        <div class="stat-label">Drugs</div>
      </div>
      <div class="stat">
        <div class="stat-value" id="tasks-count">0</div>
        <div class="stat-label">Tasks</div>
      </div>
    </div>
  </div>
  
  <div class="legend" id="legend"></div>
  
  <div class="grid-container" id="agent-grid"></div>
  
  <div class="detail-panel" id="detail-panel">
    <button class="close-btn" onclick="closePanel()">×</button>
    <h2 id="detail-name">Agent</h2>
    <p id="detail-dept"></p>
    <p id="detail-status"></p>
    <p id="detail-task"></p>
    <div class="terminal" id="terminal"></div>
  </div>
  
  <script>
    let agents = [];
    let selectedAgent = null;
    const ws = new WebSocket(\`ws://\${window.location.hostname}:\${window.location.port}/ws\`);
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      if (message.type === 'init') {
        agents = message.data.agents;
        renderLegend(message.data.departments);
        renderGrid();
      } else if (message.type === 'agent-update') {
        const index = agents.findIndex(a => a.id === message.data.id);
        if (index !== -1) {
          agents[index] = message.data;
          updateAgentCard(message.data);
          updateStats();
          if (selectedAgent === message.data.id) {
            updateDetailPanel(message.data);
            addTerminalLine(message.data);
          }
        }
      }
    };
    
    function renderLegend(departments) {
      const legend = document.getElementById('legend');
      legend.innerHTML = departments.map(d => \`
        <div class="legend-item">
          <span style="background: \${d.color}; width: 12px; height: 12px; border-radius: 50%; display: inline-block;"></span>
          \${d.icon} \${d.name}
        </div>
      \`).join('');
    }
    
    function renderGrid() {
      const grid = document.getElementById('agent-grid');
      grid.innerHTML = agents.map(agent => \`
        <div class="agent-card \${agent.status}" id="card-\${agent.id}" onclick="selectAgent('\${agent.id}')">
          <div class="agent-header">
            <span class="agent-name">\${agent.name}</span>
            <span class="agent-status \${agent.status}"></span>
          </div>
          <div class="agent-dept">
            <span class="dept-color" style="background: \${agent.department.color}"></span>
            \${agent.department.icon} \${agent.department.name}
          </div>
          <div class="agent-task">\${agent.currentTask || 'Idle'}</div>
        </div>
      \`).join('');
      updateStats();
    }
    
    function updateAgentCard(agent) {
      const card = document.getElementById(\`card-\${agent.id}\`);
      if (card) {
        card.className = \`agent-card \${agent.status}\${selectedAgent === agent.id ? ' selected' : ''}\`;
        card.querySelector('.agent-status').className = \`agent-status \${agent.status}\`;
        card.querySelector('.agent-task').textContent = agent.currentTask || 'Idle';
      }
    }
    
    function updateStats() {
      const active = agents.filter(a => a.status === 'working').length;
      const papers = agents.reduce((sum, a) => sum + a.metrics.papersAnalyzed, 0);
      const drugs = agents.reduce((sum, a) => sum + a.metrics.drugsFound, 0);
      const tasks = agents.reduce((sum, a) => sum + a.metrics.tasksCompleted, 0);
      
      document.getElementById('active-count').textContent = active;
      document.getElementById('papers-count').textContent = papers;
      document.getElementById('drugs-count').textContent = drugs;
      document.getElementById('tasks-count').textContent = tasks;
    }
    
    function selectAgent(agentId) {
      selectedAgent = agentId;
      const agent = agents.find(a => a.id === agentId);
      
      document.querySelectorAll('.agent-card').forEach(c => c.classList.remove('selected'));
      document.getElementById(\`card-\${agentId}\`).classList.add('selected');
      
      updateDetailPanel(agent);
      document.getElementById('detail-panel').classList.add('open');
      document.getElementById('terminal').innerHTML = '';
      
      ws.send(JSON.stringify({ type: 'watch-agent', agentId }));
    }
    
    function updateDetailPanel(agent) {
      document.getElementById('detail-name').textContent = \`\${agent.department.icon} \${agent.name}\`;
      document.getElementById('detail-dept').textContent = \`Department: \${agent.department.name}\`;
      document.getElementById('detail-status').textContent = \`Status: \${agent.status.toUpperCase()}\`;
      document.getElementById('detail-task').textContent = agent.currentTask ? \`Task: \${agent.currentTask}\` : '';
    }
    
    function addTerminalLine(agent) {
      if (agent.currentTask) {
        const terminal = document.getElementById('terminal');
        const line = document.createElement('div');
        line.className = 'terminal-line';
        line.textContent = \`[\${new Date().toLocaleTimeString()}] \${agent.currentTask}\`;
        terminal.appendChild(line);
        terminal.scrollTop = terminal.scrollHeight;
      }
    }
    
    function closePanel() {
      document.getElementById('detail-panel').classList.remove('open');
      document.querySelectorAll('.agent-card').forEach(c => c.classList.remove('selected'));
      selectedAgent = null;
    }
  </script>
</body>
</html>
  `);
});

// Connect to Redis and start server
connectRedis().then(() => {
  server.listen(PORT, () => {
    console.log(\`Agent Grid server running on port \${PORT}\`);
    console.log(\`WebSocket available at ws://localhost:\${PORT}/ws\`);
  });
});
