/**
 * Discovery Feed Server - Mirror Lab
 * 
 * Real-time log of research breakthroughs
 * Shows live discoveries as agents find them
 */

import express from 'express';
import { WebSocketServer } from 'ws';
import { createClient } from 'redis';
import { createServer } from 'http';

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server, path: '/ws' });

const PORT = parseInt(process.env.PORT || '3006');
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';

// Discovery types with styling
const DISCOVERY_TYPES = {
  drug_candidate: { icon: '💊', color: '#4CAF50', label: 'DRUG CANDIDATE' },
  protein_structure: { icon: '🧬', color: '#2196F3', label: 'PROTEIN STRUCTURE' },
  binding_site: { icon: '🎯', color: '#FF9800', label: 'BINDING SITE' },
  clinical_insight: { icon: '🏥', color: '#E91E63', label: 'CLINICAL INSIGHT' },
  safety_finding: { icon: '🛡️', color: '#9C27B0', label: 'SAFETY FINDING' },
  quantum_result: { icon: '⚛️', color: '#00BCD4', label: 'QUANTUM RESULT' },
  cost_estimate: { icon: '💰', color: '#FFEB3B', label: 'COST ESTIMATE' },
  regulatory_path: { icon: '📋', color: '#795548', label: 'REGULATORY PATH' },
  literature_match: { icon: '📚', color: '#607D8B', label: 'LITERATURE MATCH' },
  breakthrough: { icon: '🌟', color: '#FFD700', label: 'BREAKTHROUGH' }
};

// Store recent discoveries
const discoveries = [];
const MAX_DISCOVERIES = 100;

// Broadcast to all clients
function broadcast(message) {
  wss.clients.forEach(client => {
    if (client.readyState === 1) {
      client.send(JSON.stringify(message));
    }
  });
}

// Add discovery
function addDiscovery(discovery) {
  const entry = {
    id: `disc-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    timestamp: new Date().toISOString(),
    ...discovery,
    type: DISCOVERY_TYPES[discovery.type] || DISCOVERY_TYPES.breakthrough
  };
  
  discoveries.unshift(entry);
  if (discoveries.length > MAX_DISCOVERIES) {
    discoveries.pop();
  }
  
  broadcast({ type: 'discovery', data: entry });
  return entry;
}

// WebSocket handler
wss.on('connection', (ws) => {
  console.log('Client connected to discovery feed');
  
  // Send recent discoveries
  ws.send(JSON.stringify({
    type: 'init',
    data: discoveries.slice(0, 50)
  }));
  
  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// Demo discovery generator
const demoDiscoveries = [
  { type: 'drug_candidate', agent: 'D4', title: 'Memantine repurposing candidate identified', detail: 'NMDA receptor antagonist shows promise for chronic pain mechanism' },
  { type: 'protein_structure', agent: 'F6', title: 'AlphaFold3 prediction complete', detail: 'Disease protein structure resolved at 1.2Å resolution' },
  { type: 'binding_site', agent: 'B3', title: 'Novel binding pocket discovered', detail: 'Allosteric site identified in target protein' },
  { type: 'quantum_result', agent: 'Q2', title: 'Binding energy converged', detail: 'VQE calculation: -42.3 kcal/mol for lead compound' },
  { type: 'clinical_insight', agent: 'C8', title: 'Phase 2 trial data analyzed', detail: '67% response rate in comparable patient population' },
  { type: 'safety_finding', agent: 'S5', title: 'Clean safety profile confirmed', detail: 'No significant adverse events in 10,000 patient database' },
  { type: 'literature_match', agent: 'A1', title: 'Key paper identified', detail: 'Nature Medicine 2024: Relevant mechanism study found' },
  { type: 'cost_estimate', agent: 'E7', title: 'Treatment cost projected', detail: 'Estimated $2,400/year vs $15,000/year standard of care' },
  { type: 'breakthrough', agent: 'ALL', title: '🎉 MAJOR DISCOVERY', detail: 'Combination therapy protocol identified with 3x efficacy' },
  { type: 'regulatory_path', agent: 'R9', title: 'Fast-track eligible', detail: 'Orphan drug designation pathway identified' }
];

function generateDemoDiscovery() {
  const demo = demoDiscoveries[Math.floor(Math.random() * demoDiscoveries.length)];
  addDiscovery(demo);
}

// Generate demo discoveries every 3-8 seconds
setInterval(generateDemoDiscovery, 3000 + Math.random() * 5000);

// Express routes
app.get('/api/discoveries', (req, res) => {
  res.json(discoveries);
});

app.get('/api/discoveries/latest', (req, res) => {
  const count = parseInt(req.query.count || '10');
  res.json(discoveries.slice(0, count));
});

app.post('/api/discoveries', express.json(), (req, res) => {
  const discovery = addDiscovery(req.body);
  res.json(discovery);
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', discoveries: discoveries.length });
});

// Main HTML page
app.get('/', (req, res) => {
  res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🔬 Discovery Feed - Mirror Lab</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
      color: #fff;
      min-height: 100vh;
    }
    .header {
      background: rgba(0, 0, 0, 0.3);
      padding: 1.5rem 2rem;
      border-bottom: 2px solid #00ff88;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .header h1 {
      font-size: 1.8rem;
      background: linear-gradient(90deg, #00ff88, #00bcd4);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .stats {
      display: flex;
      gap: 2rem;
    }
    .stat-value {
      font-size: 2rem;
      font-weight: bold;
      color: #00ff88;
    }
    .stat-label {
      font-size: 0.75rem;
      color: #888;
    }
    .feed-container {
      padding: 1rem 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }
    .discovery-card {
      background: rgba(26, 26, 46, 0.9);
      border-radius: 12px;
      padding: 1.25rem;
      margin-bottom: 1rem;
      border-left: 4px solid;
      animation: slideIn 0.3s ease;
      transition: transform 0.2s ease;
    }
    .discovery-card:hover {
      transform: translateX(10px);
    }
    .discovery-card.new {
      animation: glow 1s ease;
    }
    @keyframes slideIn {
      from { opacity: 0; transform: translateX(-20px); }
      to { opacity: 1; transform: translateX(0); }
    }
    @keyframes glow {
      0%, 100% { box-shadow: 0 0 5px rgba(0, 255, 136, 0.3); }
      50% { box-shadow: 0 0 30px rgba(0, 255, 136, 0.6); }
    }
    .discovery-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }
    .discovery-type {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.8rem;
      font-weight: bold;
      text-transform: uppercase;
    }
    .discovery-time {
      font-size: 0.75rem;
      color: #666;
    }
    .discovery-title {
      font-size: 1.2rem;
      margin-bottom: 0.5rem;
    }
    .discovery-detail {
      color: #aaa;
      font-size: 0.9rem;
    }
    .discovery-agent {
      display: inline-block;
      background: rgba(255, 255, 255, 0.1);
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      margin-top: 0.5rem;
    }
    .live-indicator {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: #00ff88;
    }
    .live-dot {
      width: 10px;
      height: 10px;
      background: #00ff88;
      border-radius: 50%;
      animation: pulse 1s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(1.2); }
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>🔬 DISCOVERY FEED</h1>
    <div class="live-indicator">
      <div class="live-dot"></div>
      <span>LIVE</span>
    </div>
    <div class="stats">
      <div class="stat">
        <div class="stat-value" id="total-discoveries">0</div>
        <div class="stat-label">Total Discoveries</div>
      </div>
      <div class="stat">
        <div class="stat-value" id="breakthroughs">0</div>
        <div class="stat-label">Breakthroughs</div>
      </div>
    </div>
  </div>
  
  <div class="feed-container" id="feed"></div>
  
  <script>
    let discoveries = [];
    const ws = new WebSocket(\`ws://\${window.location.hostname}:\${window.location.port}/ws\`);
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      if (message.type === 'init') {
        discoveries = message.data;
        renderFeed();
      } else if (message.type === 'discovery') {
        discoveries.unshift(message.data);
        addDiscoveryCard(message.data, true);
        updateStats();
      }
    };
    
    function renderFeed() {
      const feed = document.getElementById('feed');
      feed.innerHTML = discoveries.map(d => createDiscoveryHTML(d)).join('');
      updateStats();
    }
    
    function createDiscoveryHTML(discovery, isNew = false) {
      const time = new Date(discovery.timestamp).toLocaleTimeString();
      return \`
        <div class="discovery-card \${isNew ? 'new' : ''}" style="border-color: \${discovery.type.color}">
          <div class="discovery-header">
            <div class="discovery-type" style="color: \${discovery.type.color}">
              <span>\${discovery.type.icon}</span>
              <span>\${discovery.type.label}</span>
            </div>
            <div class="discovery-time">\${time}</div>
          </div>
          <div class="discovery-title">\${discovery.title}</div>
          <div class="discovery-detail">\${discovery.detail}</div>
          <div class="discovery-agent">Agent \${discovery.agent}</div>
        </div>
      \`;
    }
    
    function addDiscoveryCard(discovery, isNew) {
      const feed = document.getElementById('feed');
      const card = document.createElement('div');
      card.innerHTML = createDiscoveryHTML(discovery, isNew);
      feed.insertBefore(card.firstElementChild, feed.firstChild);
      
      // Remove old cards if too many
      while (feed.children.length > 50) {
        feed.removeChild(feed.lastChild);
      }
    }
    
    function updateStats() {
      document.getElementById('total-discoveries').textContent = discoveries.length;
      document.getElementById('breakthroughs').textContent = 
        discoveries.filter(d => d.type.label === 'BREAKTHROUGH').length;
    }
  </script>
</body>
</html>
  `);
});

// Start server
server.listen(PORT, () => {
  console.log(\`Discovery Feed server running on port \${PORT}\`);
});
