/**
 * Quantum Mirror Lab Dashboard Server
 * Serves the Mission Control dashboard
 */

import http from 'http';

const PORT = process.env.PORT || 3001;
const WEBSOCKET_URL = process.env.WEBSOCKET_URL || 'ws://localhost:8765';
const AGENT_COUNT = process.env.AGENT_COUNT || 640;

// Generate progress bars HTML
function generateProgressBars() {
  let html = '';
  for (let i = 1; i <= 10; i++) {
    const progress = Math.floor(Math.random() * 100);
    html += `
      <div>
        <span>Law ${i}</span>
        <div class="progress-bar">
          <div class="fill" style="width: ${progress}%"></div>
          <span class="label">${progress}%</span>
        </div>
      </div>`;
  }
  return html;
}

// Generate agent grid HTML
function generateAgentGrid() {
  let html = '';
  const statuses = ['working', 'working', 'working', 'waiting', 'discovery'];
  for (let i = 0; i < 64; i++) {
    const status = statuses[Math.floor(Math.random() * statuses.length)];
    html += `<div class="agent ${status}" title="Agent ${i + 1}"></div>`;
  }
  return html;
}

// Dashboard HTML template
function getDashboardHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Mirror Lab - Mission Control</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Consolas', 'Monaco', monospace;
            background: #0a0a0f;
            color: #00ff00;
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #00ff00;
            margin-bottom: 20px;
        }
        .header h1 {
            font-size: 2.5rem;
            text-shadow: 0 0 10px #00ff00;
        }
        .header .subtitle {
            color: #00aa00;
            margin-top: 10px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .panel {
            background: #111118;
            border: 1px solid #00ff0066;
            border-radius: 8px;
            padding: 20px;
        }
        .panel h2 {
            color: #00ffff;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }
        .progress-bar {
            background: #1a1a24;
            border-radius: 4px;
            height: 24px;
            margin: 8px 0;
            position: relative;
            overflow: hidden;
        }
        .progress-bar .fill {
            height: 100%;
            background: linear-gradient(90deg, #00aa00, #00ff00);
            transition: width 0.5s ease;
        }
        .progress-bar .label {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.9rem;
        }
        .agent-grid {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 4px;
        }
        .agent {
            width: 100%;
            aspect-ratio: 1;
            border-radius: 4px;
            font-size: 0.6rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .agent.working { background: #00aa00; }
        .agent.waiting { background: #aaaa00; }
        .agent.error { background: #aa0000; }
        .agent.discovery { background: #0066ff; animation: pulse 1s infinite; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .discovery-feed {
            height: 300px;
            overflow-y: auto;
            background: #0a0a0f;
            padding: 10px;
            font-size: 0.85rem;
            line-height: 1.6;
        }
        .discovery-feed .entry {
            margin-bottom: 8px;
            padding-left: 10px;
            border-left: 2px solid #00ff00;
        }
        .discovery-feed .entry.highlight {
            border-left-color: #0066ff;
            color: #00ffff;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            text-align: center;
        }
        .stat {
            padding: 15px;
        }
        .stat .value {
            font-size: 2rem;
            font-weight: bold;
        }
        .stat .label {
            font-size: 0.8rem;
            color: #00aa00;
        }
        #connection-status {
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        #connection-status.connected {
            background: #00aa00;
            color: #000;
        }
        #connection-status.disconnected {
            background: #aa0000;
            color: #fff;
        }
    </style>
</head>
<body>
    <div id="connection-status" class="disconnected">Connecting...</div>
    
    <div class="header">
        <h1>🔮 QUANTUM MIRROR LAB</h1>
        <p class="subtitle">FOR HER — Day <span id="day-count">1</span> of 30 | <span id="agent-count">${AGENT_COUNT}</span> Agents Active</p>
    </div>
    
    <div class="grid">
        <div class="panel">
            <h2>📊 Law Progress</h2>
            <div id="law-progress">
                ${generateProgressBars()}
            </div>
        </div>
        
        <div class="panel">
            <h2>🤖 Agent Monitor</h2>
            <div class="agent-grid" id="agent-grid">
                ${generateAgentGrid()}
            </div>
        </div>
        
        <div class="panel">
            <h2>📈 Statistics</h2>
            <div class="stats">
                <div class="stat">
                    <div class="value" id="papers-count">0</div>
                    <div class="label">Papers Analyzed</div>
                </div>
                <div class="stat">
                    <div class="value" id="candidates-count">0</div>
                    <div class="label">Drug Candidates</div>
                </div>
                <div class="stat">
                    <div class="value" id="matches-count">0</div>
                    <div class="label">Case Matches</div>
                </div>
            </div>
        </div>
        
        <div class="panel" style="grid-column: 1 / -1;">
            <h2>📡 Real-Time Discovery Feed</h2>
            <div class="discovery-feed" id="discovery-feed">
                <div class="entry">Waiting for discoveries...</div>
            </div>
        </div>
    </div>
    
    <script>
        const WEBSOCKET_URL = '${WEBSOCKET_URL}';
        let ws = null;
        let stats = { papers: 0, candidates: 0, matches: 0 };
        
        function connect() {
            try {
                ws = new WebSocket(WEBSOCKET_URL);
                
                ws.onopen = () => {
                    document.getElementById('connection-status').className = 'connected';
                    document.getElementById('connection-status').textContent = 'Connected';
                };
                
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    handleMessage(data);
                };
                
                ws.onclose = () => {
                    document.getElementById('connection-status').className = 'disconnected';
                    document.getElementById('connection-status').textContent = 'Disconnected';
                    setTimeout(connect, 3000);
                };
                
                ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };
            } catch (e) {
                console.error('Connection failed:', e);
                setTimeout(connect, 3000);
            }
        }
        
        function handleMessage(data) {
            if (data.type === 'discovery') {
                addDiscoveryEntry(data);
                stats.candidates++;
                document.getElementById('candidates-count').textContent = stats.candidates;
            } else if (data.type === 'status_update') {
                updateAgentStatus(data);
            }
        }
        
        function addDiscoveryEntry(data) {
            const feed = document.getElementById('discovery-feed');
            const entry = document.createElement('div');
            entry.className = 'entry highlight';
            entry.textContent = data.formatted || '[' + new Date().toISOString() + '] ' + data.message;
            feed.insertBefore(entry, feed.firstChild);
            if (feed.children.length > 50) {
                feed.removeChild(feed.lastChild);
            }
        }
        
        function updateAgentStatus(data) {
            // Update agent grid visualization
        }
        
        // Simulate activity for demo
        function simulateActivity() {
            stats.papers += Math.floor(Math.random() * 5);
            stats.matches += Math.random() > 0.8 ? 1 : 0;
            document.getElementById('papers-count').textContent = stats.papers;
            document.getElementById('matches-count').textContent = stats.matches;
        }
        
        setInterval(simulateActivity, 2000);
        connect();
    </script>
</body>
</html>`;
}

const server = http.createServer((req, res) => {
    if (req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'healthy', service: 'dashboard' }));
        return;
    }
    
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(getDashboardHTML());
});

server.listen(PORT, () => {
    console.log(`Dashboard server running on port ${PORT}`);
});
