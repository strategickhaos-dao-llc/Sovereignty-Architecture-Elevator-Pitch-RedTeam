# 🎯 Tunnel Demo Scenarios - Real World Examples

## Scenario 1: Share Your Local Dev Server with the Team

### The Problem
You're working on a new feature locally, and your team lead wants to see it in action. Your dev server is running on `localhost:3000`, but they're remote.

### The Solution
```bash
# Start your dev server
npm run dev

# In another terminal, start tunnel
./setup-tunnel.sh

# Output:
# https://amazing-feature-demo-x7y2.trycloudflare.com
```

**Share that URL** in Slack/Discord. Your team can see your work in real-time. No deployment, no staging server, no waiting.

---

## Scenario 2: Demo to Client on Your Gaming Rig

### The Problem
You've built something amazing, but your client wants to see it NOW. You're on your home gaming rig behind CG-NAT. Port forwarding is impossible.

### The Solution
```powershell
# Windows PowerShell
# Start your app
npm start

# Start tunnel (auto-installs if needed)
./setup-tunnel.ps1

# Output within 12 seconds:
# https://client-demo-sovereign-arch.trycloudflare.com
```

**Send that link to your client.** They see it immediately. HTTPS, secure, professional. They're impressed. The bamboo approves.

---

## Scenario 3: Test Webhooks from GitHub/Discord

### The Problem
You're developing GitHub webhook integration. Need to test webhooks hitting your local server. ngrok wants you to sign up. You need this NOW.

### The Solution
```bash
# Start your webhook handler
node webhook-server.js
# Server listening on http://localhost:8080

# Start tunnel on port 8080
./setup-tunnel.sh 8080

# Output:
# https://webhook-test-strategic.trycloudflare.com
```

**Configure webhook in GitHub:**
- Webhook URL: `https://webhook-test-strategic.trycloudflare.com/hooks/github`
- Content type: `application/json`
- Events: Select what you need

**Test it:**
```bash
# Push to trigger webhook
git push origin feature-branch

# Watch your local logs
# [webhook-server] Received push event from GitHub
# [webhook-server] Processing payload...
```

---

## Scenario 4: Mobile App Testing

### The Problem
You're building a React Native app. Need to test API calls from your phone to your local backend. Your phone and laptop are on different networks.

### The Solution
```bash
# Start backend API
npm run api
# API running on http://localhost:4000

# Tunnel it
cloudflared tunnel --url http://localhost:4000

# Output:
# https://mobile-api-test-abc123.trycloudflare.com
```

**Update your mobile app config:**
```javascript
// config.js
const API_URL = __DEV__ 
  ? 'https://mobile-api-test-abc123.trycloudflare.com'
  : 'https://api.production.com';
```

**Test from phone:**
- Works on any network (WiFi, cellular, anywhere)
- HTTPS works perfectly (no SSL warnings)
- Real-time updates from your local code

---

## Scenario 5: Multiple Services Demo

### The Problem
You have a microservices architecture running locally:
- Frontend: `localhost:3000`
- API: `localhost:8000`
- WebSocket: `localhost:9000`

You want to demo all three to stakeholders.

### The Solution
```bash
# Terminal 1: Frontend tunnel
cloudflared tunnel --url http://localhost:3000
# Output: https://frontend-demo-xyz.trycloudflare.com

# Terminal 2: API tunnel
cloudflared tunnel --url http://localhost:8000
# Output: https://api-demo-xyz.trycloudflare.com

# Terminal 3: WebSocket tunnel
cloudflared tunnel --url http://localhost:9000
# Output: https://ws-demo-xyz.trycloudflare.com
```

**Update frontend to use tunneled API:**
```javascript
// In your frontend .env.local
VITE_API_URL=https://api-demo-xyz.trycloudflare.com
VITE_WS_URL=https://ws-demo-xyz.trycloudflare.com
```

**Share the frontend URL** with stakeholders. Everything just works.

---

## Scenario 6: Docker Compose Stack Demo

### The Problem
You have a complete Docker Compose stack (app + DB + Redis + etc). Want to show it off without deploying to cloud.

### The Solution
```bash
# Start your stack
docker compose up -d

# Check what's exposed
docker compose ps
# NAME                     STATUS    PORTS
# myapp-web               Up        0.0.0.0:3000->3000/tcp
# myapp-db                Up        5432/tcp
# myapp-redis             Up        6379/tcp

# Tunnel the web service
./setup-tunnel.sh 3000

# Output:
# https://docker-stack-demo.trycloudflare.com
```

**The magic:**
- Only web service is publicly accessible
- DB and Redis remain internal (secure)
- Full stack demo without exposing internals

---

## Scenario 7: CloudOS Desktop Demo

### The Problem
You've set up the CloudOS desktop environment (from `start-cloudos.ps1`). Multiple services on different ports. Want to demo the AI SME interface publicly.

### The Solution
```powershell
# Start CloudOS
./start-cloudos.ps1

# CloudOS exposes:
# - IDE: localhost:8081
# - AI SME: localhost:8000
# - Grafana: localhost:3000

# Tunnel the AI SME interface
./setup-tunnel.ps1 -Port 8000

# Output:
# https://cloudos-ai-sme.trycloudflare.com
```

**Share with researchers/collaborators:**
- They can interact with the AI SME
- No CloudOS installation needed on their end
- Instant access to your sovereignty stack

---

## Scenario 8: Emergency Production Debugging

### The Problem
Production is down. You've reproduced the bug locally. DevOps needs to see the logs in your local debugger. NOW.

### The Solution
```bash
# Start your local debug server with detailed logging
DEBUG=* npm run dev:debug

# Tunnel it
cloudflared tunnel --url http://localhost:3000

# Output in 8 seconds:
# https://emergency-debug-session.trycloudflare.com
```

**Paste URL in incident channel:**
```
🚨 INCIDENT #247 - Production Cart Failure
📊 Local reproduction: https://emergency-debug-session.trycloudflare.com
🔍 Check /debug endpoint for live logs
⏱️ ETA to fix: 15 mins
```

**DevOps can:**
- See real-time logs
- Test fix attempts immediately
- Verify fix before production push

---

## Scenario 9: Teaching/Workshop Environment

### The Problem
You're teaching a workshop. 20 students need to see your live coding. Screen sharing is laggy and hard to follow.

### The Solution
```bash
# Start your teaching demo app
npm run workshop

# Tunnel it
./setup-tunnel.sh

# Output:
# https://workshop-live-coding.trycloudflare.com
```

**Tell students:**
```
📚 Workshop: Building Real-Time Apps
🌐 Follow along: https://workshop-live-coding.trycloudflare.com
🔄 Page auto-refreshes as I code
💬 Ask questions in chat
```

**Students can:**
- Follow your code changes in real-time
- Test features as you build them
- Reference the URL later for review

---

## Scenario 10: Agent 10 - The Rotation Goes Global

### The Problem
Agent 10 (Hypodorian-Uranium) is delivering checkmates in 10-layer cognitive boards. The timeline needs to witness this. Your local Grafana dashboard shows the progression.

### The Solution
```bash
# Start your full stack with Grafana
docker compose -f docker-compose.obs.yml up -d

# Tunnel Grafana
./setup-tunnel.sh 3000

# Output:
# https://agent10-rotation-authority.trycloudflare.com
```

**Share with the collective:**
```
🎯 AGENT 10 LIVE DEMONSTRATION
📊 Watch the rotation: https://agent10-rotation-authority.trycloudflare.com
🔥 10-layer boards in real-time
🎭 The bamboo witnesses. The timeline observes.
⚡ Checkmate in T-minus 47 seconds
```

**The world sees:**
- Real-time metrics
- Cognitive progression
- Strategic dominance
- The rotation demands an audience. You give it one.

---

## 🎓 Key Lessons from These Scenarios

1. **Speed**: Every scenario solved in <60 seconds
2. **Zero Friction**: No accounts, no config, no deployment
3. **Security**: HTTPS by default, only expose what you choose
4. **Flexibility**: Works for dev, testing, demos, emergencies, teaching
5. **Professional**: Clean URLs, fast response, reliable uptime

---

## 🚀 Your Scenario

What's your use case? The pattern is always the same:

```bash
# 1. Start your local service
[your-command-to-start-service]

# 2. Tunnel it
./setup-tunnel.sh [port]

# 3. Share the URL
# https://your-thing.trycloudflare.com

# 4. Win
```

No signup. No token. No bill. No 4018.

The bamboo approves.

---

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*
