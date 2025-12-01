/**
 * Discovery Feed WebSocket Server for Quantum Mirror Lab
 * Real-time event stream of agent discoveries
 */

const WebSocket = require('ws');
const http = require('http');

const PORT = process.env.WEBSOCKET_PORT || 8765;

// Discovery buffer for replay
const discoveryBuffer = [];
const MAX_BUFFER_SIZE = 1000;

// Create HTTP server
const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
      status: 'healthy', 
      discoveries: discoveryBuffer.length 
    }));
    return;
  }
  
  if (req.url === '/recent') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(discoveryBuffer.slice(-100)));
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

// Add discovery to buffer
function addDiscovery(discovery) {
  discoveryBuffer.push(discovery);
  if (discoveryBuffer.length > MAX_BUFFER_SIZE) {
    discoveryBuffer.shift();
  }
  broadcast(discovery);
}

// Format discovery message
function formatDiscovery(law, agentNum, message, confidence = null) {
  const timestamp = new Date().toISOString();
  return {
    type: 'discovery',
    timestamp,
    law,
    agent: agentNum,
    message,
    confidence,
    formatted: `[${timestamp}] Law ${law} Agent ${agentNum}: ${message}${confidence ? ` (${confidence}% confidence)` : ''}`
  };
}

// Handle WebSocket connections
wss.on('connection', (ws) => {
  console.log('Client connected to Discovery Feed');
  
  // Send recent discoveries
  ws.send(JSON.stringify({
    type: 'history',
    discoveries: discoveryBuffer.slice(-50)
  }));
  
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      handleMessage(data);
    } catch (err) {
      console.error('Invalid message:', err);
    }
  });
  
  ws.on('close', () => {
    console.log('Client disconnected from Discovery Feed');
  });
});

// Handle incoming messages
function handleMessage(data) {
  switch (data.type) {
    case 'discovery':
      const discovery = formatDiscovery(
        data.law,
        data.agent,
        data.message,
        data.confidence
      );
      addDiscovery(discovery);
      break;
    case 'status':
      broadcast({
        type: 'status',
        timestamp: new Date().toISOString(),
        ...data
      });
      break;
    default:
      console.log('Unknown message type:', data.type);
  }
}

// Simulate discoveries for demo mode
function simulateDiscoveries() {
  const discoveries = [
    { law: 1, msg: 'CoQ10 dosing optimized (300mg/day)', conf: null },
    { law: 3, msg: 'Memantine repurposing candidate identified', conf: 90 },
    { law: 6, msg: 'IL-6 elevation hypothesis (3 supporting papers)', conf: null },
    { law: 9, msg: 'WES recommendation (Invitae, $2,850)', conf: null },
    { law: 7, msg: 'Stellate ganglion block protocol found', conf: null },
    { law: 2, msg: 'Ion channel modulator candidate', conf: 85 },
    { law: 4, msg: 'Metabolic pathway mapped', conf: null },
    { law: 5, msg: 'Statistical correlation: 87% symptom overlap', conf: 87 },
    { law: 8, msg: 'Crystal structure analysis complete', conf: null },
    { law: 10, msg: 'Treatment plan updated', conf: null }
  ];
  
  const item = discoveries[Math.floor(Math.random() * discoveries.length)];
  const agentNum = Math.floor(Math.random() * 64) + 1;
  
  const discovery = formatDiscovery(item.law, agentNum, item.msg, item.conf);
  addDiscovery(discovery);
}

// Start simulation interval (demo mode)
if (process.env.DEMO_MODE === 'true') {
  setInterval(simulateDiscoveries, 3000);
}

// Start server
server.listen(PORT, () => {
  console.log(`Discovery Feed WebSocket Server running on port ${PORT}`);
});

module.exports = { server, wss, addDiscovery, formatDiscovery };
