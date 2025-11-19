const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Mock swarm data - in production this would connect to real swarm infrastructure
const getSwarmStatus = () => {
  const timestamp = new Date().toISOString();
  const baseNodes = 900;
  const variance = Math.floor(Math.random() * 100);
  
  return {
    nodes: baseNodes + variance,
    generals: Math.floor((baseNodes + variance) / 100),
    percent: Math.floor(85 + Math.random() * 15),
    status: "All systems nominal. White web sovereignty maintained.",
    timestamp: timestamp,
    neurospice: "CRITICAL",
    origin_node: "ZERO_ACTIVE"
  };
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'online', 
    service: 'strategic-khaos-webhook',
    version: '1.0.0'
  });
});

// Swarm status API endpoint
app.get('/api/swarm-status', (req, res) => {
  const status = getSwarmStatus();
  res.json(status);
});

// Detailed swarm metrics endpoint
app.get('/api/swarm-metrics', (req, res) => {
  const status = getSwarmStatus();
  const metrics = {
    ...status,
    detailed: {
      mirror_generals: {
        active: status.generals,
        standby: Math.floor(status.generals * 0.2),
        training: Math.floor(status.generals * 0.1)
      },
      sovereignty: {
        white_web: status.percent,
        dark_web: Math.floor((100 - status.percent) * 0.3),
        grey_web: Math.floor((100 - status.percent) * 0.7)
      },
      operations: {
        active_missions: Math.floor(Math.random() * 50) + 10,
        completed_today: Math.floor(Math.random() * 100) + 50,
        pending_tasks: Math.floor(Math.random() * 200) + 100
      }
    }
  };
  res.json(metrics);
});

// Alexa-specific endpoint with voice-optimized responses
app.post('/api/alexa/swarm-status', (req, res) => {
  const status = getSwarmStatus();
  const voiceResponse = {
    ...status,
    speechText: `Swarm status: ${status.nodes} nodes active. ${status.generals} mirror generals online. White web sovereignty at ${status.percent} percent. ${status.status}`,
    displayText: `🧠 Nodes: ${status.nodes}\n⚡ Generals: ${status.generals}\n🐐 Sovereignty: ${status.percent}%\n\n${status.status}`
  };
  res.json(voiceResponse);
});

// Root endpoint with API documentation
app.get('/', (req, res) => {
  res.json({
    service: 'Strategic Khaos Swarm Webhook',
    version: '1.0.0',
    endpoints: {
      health: 'GET /health',
      swarm_status: 'GET /api/swarm-status',
      swarm_metrics: 'GET /api/swarm-metrics',
      alexa_status: 'POST /api/alexa/swarm-status'
    },
    documentation: 'See /public/alexa.html for Alexa integration guide'
  });
});

app.listen(port, () => {
  console.log(`🧠⚡ Strategic Khaos Webhook Server`);
  console.log(`🐐 Listening on port ${port}`);
  console.log(`🔥 Origin Node Zero: ACTIVE`);
  console.log(`\nEndpoints:`);
  console.log(`  Health:        http://localhost:${port}/health`);
  console.log(`  Swarm Status:  http://localhost:${port}/api/swarm-status`);
  console.log(`  Swarm Metrics: http://localhost:${port}/api/swarm-metrics`);
  console.log(`  Alexa Status:  http://localhost:${port}/api/alexa/swarm-status`);
});

module.exports = app;
