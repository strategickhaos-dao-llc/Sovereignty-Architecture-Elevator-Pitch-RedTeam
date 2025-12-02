/**
 * Sovereignty Architecture Event Gateway - Neural Network Service
 *
 * This gateway acts as the "neural network" of the sovereignty architecture,
 * routing events between services via NATS pub/sub messaging.
 *
 * Analogies:
 * - Synapse Routing: Event distribution between components
 * - Signal Pathways: Message routing and transformation
 * - Neural Network: Pattern recognition and routing decisions
 *
 * Dependencies: nats
 * Install: npm install nats
 */

const http = require('http');

// Configuration from environment
const NATS_URL = process.env.NATS_URL || 'nats://localhost:4222';
const GATEWAY_PORT = parseInt(process.env.GATEWAY_PORT || '3001', 10);
const EVENT_PUBLISH_INTERVAL = parseInt(process.env.EVENT_PUBLISH_INTERVAL || '5000', 10);

// NATS connection state
let nc = null;
let isConnected = false;

/**
 * Connect to NATS server with retry logic
 */
async function connectNats() {
    try {
        const { connect } = require('nats');
        nc = await connect({
            servers: [NATS_URL],
            reconnect: true,
            maxReconnectAttempts: -1, // Infinite reconnection (self-healing)
            reconnectTimeWait: 2000,
        });

        isConnected = true;
        console.log(`✅ Connected to NATS at ${NATS_URL}`);

        // Handle connection events
        (async () => {
            for await (const status of nc.status()) {
                console.log(`📡 NATS status: ${status.type}`);
                if (status.type === 'disconnect') {
                    isConnected = false;
                } else if (status.type === 'reconnect') {
                    isConnected = true;
                }
            }
        })();

        return nc;
    } catch (err) {
        console.error(`❌ Failed to connect to NATS: ${err.message}`);
        isConnected = false;

        // Retry connection after delay (self-healing)
        console.log('🔄 Retrying NATS connection in 5 seconds...');
        setTimeout(connectNats, 5000);
        return null;
    }
}

/**
 * Publish an event to NATS
 */
async function publishEvent(subject, data) {
    if (!nc || !isConnected) {
        console.warn('⚠️ NATS not connected, event not published');
        return false;
    }

    try {
        const payload = typeof data === 'string' ? data : JSON.stringify(data);
        nc.publish(subject, Buffer.from(payload));
        console.log(`📤 Published to '${subject}': ${payload.substring(0, 100)}...`);
        return true;
    } catch (err) {
        console.error(`❌ Failed to publish event: ${err.message}`);
        return false;
    }
}

/**
 * Subscribe to events and handle them
 */
async function setupSubscriptions() {
    if (!nc || !isConnected) {
        console.warn('⚠️ Cannot setup subscriptions, NATS not connected');
        return;
    }

    // Subscribe to system health events
    const healthSub = nc.subscribe('system.health');
    (async () => {
        for await (const msg of healthSub) {
            const data = msg.data ? Buffer.from(msg.data).toString() : '';
            console.log(`💓 Health status received: ${data}`);
        }
    })();

    // Subscribe to all events for logging
    const eventsSub = nc.subscribe('events.>');
    (async () => {
        for await (const msg of eventsSub) {
            const data = msg.data ? Buffer.from(msg.data).toString() : '';
            console.log(`📨 Event on '${msg.subject}': ${data}`);
        }
    })();

    // Subscribe to alerts
    const alertsSub = nc.subscribe('alerts.>');
    (async () => {
        for await (const msg of alertsSub) {
            const data = msg.data ? Buffer.from(msg.data).toString() : '';
            console.log(`⚠️ Alert on '${msg.subject}': ${data}`);
        }
    })();

    console.log('📡 Event subscriptions established');
}

/**
 * Start periodic system events (heartbeat / load updates)
 */
function startPeriodicEvents() {
    // Publish system load updates periodically
    setInterval(async () => {
        const loadUpdate = {
            timestamp: Date.now(),
            type: 'load_update',
            memory: process.memoryUsage(),
            uptime: process.uptime()
        };
        await publishEvent('events.gateway.heartbeat', loadUpdate);
    }, EVENT_PUBLISH_INTERVAL);

    console.log(`⏰ Periodic events started (interval: ${EVENT_PUBLISH_INTERVAL}ms)`);
}

/**
 * Create HTTP server for health checks and event ingestion
 */
function createHttpServer() {
    const server = http.createServer(async (req, res) => {
        const url = new URL(req.url, `http://${req.headers.host}`);

        // Health check endpoint
        if (url.pathname === '/health' || url.pathname === '/healthz') {
            const health = {
                status: isConnected ? 'healthy' : 'unhealthy',
                nats: isConnected,
                uptime: process.uptime(),
                timestamp: new Date().toISOString()
            };

            res.writeHead(isConnected ? 200 : 503, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(health));
            return;
        }

        // Event publish endpoint (POST /publish)
        if (req.method === 'POST' && url.pathname === '/publish') {
            let body = '';
            req.on('data', chunk => { body += chunk; });
            req.on('end', async () => {
                try {
                    const { subject, data } = JSON.parse(body);
                    if (!subject) {
                        res.writeHead(400, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ error: 'Missing subject field' }));
                        return;
                    }

                    const success = await publishEvent(subject, data || {});
                    res.writeHead(success ? 200 : 503, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ success, subject }));
                } catch (err) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: err.message }));
                }
            });
            return;
        }

        // Status endpoint
        if (url.pathname === '/status') {
            const status = {
                service: 'sovereignty-event-gateway',
                version: '1.0.0',
                nats_connected: isConnected,
                nats_url: NATS_URL,
                uptime: process.uptime(),
                memory: process.memoryUsage()
            };

            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(status, null, 2));
            return;
        }

        // Default 404
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found' }));
    });

    server.listen(GATEWAY_PORT, () => {
        console.log(`🌐 HTTP server listening on port ${GATEWAY_PORT}`);
        console.log(`   Health: http://localhost:${GATEWAY_PORT}/health`);
        console.log(`   Status: http://localhost:${GATEWAY_PORT}/status`);
        console.log(`   Publish: POST http://localhost:${GATEWAY_PORT}/publish`);
    });

    return server;
}

/**
 * Graceful shutdown handler
 */
async function shutdown(signal) {
    console.log(`\n🛑 Received ${signal}, shutting down gracefully...`);

    if (nc) {
        await nc.drain();
        await nc.close();
    }

    process.exit(0);
}

/**
 * Main entry point
 */
async function main() {
    console.log('🧠 Sovereignty Event Gateway starting...');
    console.log(`   NATS URL: ${NATS_URL}`);
    console.log(`   Gateway Port: ${GATEWAY_PORT}`);
    console.log(`   Event Interval: ${EVENT_PUBLISH_INTERVAL}ms`);

    // Setup signal handlers
    process.on('SIGINT', () => shutdown('SIGINT'));
    process.on('SIGTERM', () => shutdown('SIGTERM'));

    // Connect to NATS
    await connectNats();

    // Setup subscriptions
    await setupSubscriptions();

    // Start HTTP server
    createHttpServer();

    // Start periodic events
    startPeriodicEvents();

    console.log('✅ Sovereignty Event Gateway is running');
}

// Run the gateway
main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
