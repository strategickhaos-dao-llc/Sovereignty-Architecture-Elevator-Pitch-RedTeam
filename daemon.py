#!/usr/bin/env python3
"""
Sovereignty Architecture Daemon - Consciousness/Operator Service

This daemon acts as the "consciousness" of the sovereignty architecture,
monitoring all services, validating state, and responding to events.

Analogies:
- Prefrontal Cortex: Executive decision making
- Error Correction: DNA repair mechanisms
- Emotional Regulation: Homeostasis maintenance
- SubconsciousLab Gate: Background processing

Dependencies: psycopg2-binary, redis, nats-py
Install: pip install psycopg2-binary redis nats-py
"""

import asyncio
import logging
import os
import sys
import time
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('sovereignty-daemon')

# Environment configuration
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'sovereignty_db')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'operator')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'securepass')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'securepass')
NATS_HOST = os.getenv('NATS_HOST', 'localhost')
NATS_PORT = os.getenv('NATS_PORT', '4222')
CHECK_INTERVAL = int(os.getenv('DAEMON_CHECK_INTERVAL', '60'))


class SovereigntyDaemon:
    """
    Main daemon class that monitors and validates all sovereignty services.
    Implements self-healing and error correction behaviors.
    """

    def __init__(self):
        self.pg_conn: Optional[object] = None
        self.redis_client: Optional[object] = None
        self.nats_client: Optional[object] = None
        self.running = True
        self.health_status = {
            'postgres': False,
            'redis': False,
            'nats': False
        }

    async def connect_postgres(self) -> bool:
        """Connect to PostgreSQL (DNA Archive)."""
        try:
            import psycopg2
            self.pg_conn = psycopg2.connect(
                host=POSTGRES_HOST,
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                connect_timeout=5
            )
            self.health_status['postgres'] = True
            logger.info("✅ PostgreSQL (DNA Archive) connection established")
            return True
        except ImportError:
            logger.warning("⚠️ psycopg2 not installed, PostgreSQL checks disabled")
            return False
        except Exception as e:
            logger.error(f"❌ PostgreSQL connection failed: {e}")
            self.health_status['postgres'] = False
            return False

    async def connect_redis(self) -> bool:
        """Connect to Redis (Short-term Memory)."""
        try:
            import redis as redis_lib
            self.redis_client = redis_lib.Redis(
                host=REDIS_HOST,
                password=REDIS_PASSWORD,
                socket_timeout=5,
                decode_responses=True
            )
            self.redis_client.ping()
            self.health_status['redis'] = True
            logger.info("✅ Redis (Short-term Memory) connection established")
            return True
        except ImportError:
            logger.warning("⚠️ redis not installed, Redis checks disabled")
            return False
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.health_status['redis'] = False
            return False

    async def connect_nats(self) -> bool:
        """Connect to NATS (Synaptic Transmission)."""
        try:
            from nats.aio.client import Client as NATS
            self.nats_client = NATS()
            await self.nats_client.connect(
                servers=[f"nats://{NATS_HOST}:{NATS_PORT}"],
                connect_timeout=5
            )
            self.health_status['nats'] = True
            logger.info("✅ NATS (Synaptic Transmission) connection established")
            return True
        except ImportError:
            logger.warning("⚠️ nats-py not installed, NATS checks disabled")
            return False
        except Exception as e:
            logger.error(f"❌ NATS connection failed: {e}")
            self.health_status['nats'] = False
            return False

    async def check_postgres_health(self) -> bool:
        """Validate PostgreSQL state (Error Correction analogy)."""
        if not self.pg_conn:
            return await self.connect_postgres()

        try:
            with self.pg_conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                if result and result[0] == 1:
                    self.health_status['postgres'] = True
                    return True
        except Exception as e:
            logger.error(f"PostgreSQL health check failed: {e}")
            self.pg_conn = None
            self.health_status['postgres'] = False
            # Attempt reconnection (self-healing)
            return await self.connect_postgres()

        return False

    async def check_redis_health(self) -> bool:
        """Validate Redis state."""
        if not self.redis_client:
            return await self.connect_redis()

        try:
            if self.redis_client.ping():
                self.health_status['redis'] = True
                return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            self.redis_client = None
            self.health_status['redis'] = False
            # Attempt reconnection (self-healing)
            return await self.connect_redis()

        return False

    async def check_nats_health(self) -> bool:
        """Validate NATS state."""
        if not self.nats_client:
            return await self.connect_nats()

        try:
            if self.nats_client.is_connected:
                self.health_status['nats'] = True
                return True
        except Exception as e:
            logger.error(f"NATS health check failed: {e}")
            self.nats_client = None
            self.health_status['nats'] = False
            # Attempt reconnection (self-healing)
            return await self.connect_nats()

        return False

    async def setup_event_subscription(self):
        """Subscribe to NATS events (Synaptic Transmission)."""
        if not self.nats_client or not self.nats_client.is_connected:
            return

        async def message_handler(msg):
            """Handle incoming messages from event bus."""
            subject = msg.subject
            data = msg.data.decode() if msg.data else ""
            logger.info(f"📨 Received event on '{subject}': {data}")

            # Add custom logic here for different event types
            if "alert" in subject.lower():
                await self.handle_alert(data)
            elif "resource" in subject.lower():
                await self.handle_resource_event(data)

        try:
            await self.nats_client.subscribe("events.*", cb=message_handler)
            await self.nats_client.subscribe("alerts.*", cb=message_handler)
            await self.nats_client.subscribe("system.*", cb=message_handler)
            logger.info("📡 Subscribed to event channels: events.*, alerts.*, system.*")
        except Exception as e:
            logger.error(f"Failed to subscribe to events: {e}")

    async def handle_alert(self, data: str):
        """Handle alert events - trigger self-healing if needed."""
        logger.warning(f"⚠️ Alert received: {data}")
        # Add custom alert handling logic here
        # e.g., scale services, restart unhealthy components, notify operators

    async def handle_resource_event(self, data: str):
        """Handle resource allocation events."""
        logger.info(f"📊 Resource event: {data}")
        # Add resource management logic here
        # e.g., optimize memory usage, adjust caching strategies

    async def publish_health_status(self):
        """Publish current health status to NATS."""
        if self.nats_client and self.nats_client.is_connected:
            try:
                import json
                status_msg = json.dumps({
                    'timestamp': time.time(),
                    'health': self.health_status,
                    'all_healthy': all(self.health_status.values())
                })
                await self.nats_client.publish("system.health", status_msg.encode())
                logger.debug("Published health status to NATS")
            except Exception as e:
                logger.error(f"Failed to publish health status: {e}")

    def get_health_summary(self) -> str:
        """Get a human-readable health summary."""
        status_icons = {True: "✅", False: "❌"}
        lines = ["=== Sovereignty Daemon Health Check ==="]
        for service, healthy in self.health_status.items():
            lines.append(f"  {status_icons[healthy]} {service.upper()}")

        all_healthy = all(self.health_status.values())
        if all_healthy:
            lines.append("🟢 All systems nominal")
        else:
            lines.append("🔴 Some systems unhealthy - self-healing in progress")

        return "\n".join(lines)

    async def run_health_cycle(self):
        """Run a single health check cycle."""
        logger.info("🔄 Starting health check cycle...")

        # Check all services
        await self.check_postgres_health()
        await self.check_redis_health()
        await self.check_nats_health()

        # Log health summary
        logger.info(self.get_health_summary())

        # Publish health status
        await self.publish_health_status()

    async def run(self):
        """Main daemon loop - runs forever like consciousness."""
        logger.info("🧠 Sovereignty Daemon starting...")
        logger.info(f"Configuration:")
        logger.info(f"  PostgreSQL: {POSTGRES_HOST}")
        logger.info(f"  Redis: {REDIS_HOST}")
        logger.info(f"  NATS: {NATS_HOST}:{NATS_PORT}")
        logger.info(f"  Check Interval: {CHECK_INTERVAL}s")

        # Initial connections
        await self.connect_postgres()
        await self.connect_redis()
        await self.connect_nats()

        # Setup event subscriptions
        await self.setup_event_subscription()

        # Main loop
        while self.running:
            try:
                await self.run_health_cycle()
            except Exception as e:
                logger.error(f"Health cycle error: {e}")

            # Sleep until next check (like vital signs monitoring)
            await asyncio.sleep(CHECK_INTERVAL)

        logger.info("🛑 Sovereignty Daemon shutting down...")

    async def shutdown(self):
        """Graceful shutdown."""
        self.running = False
        if self.pg_conn:
            self.pg_conn.close()
        if self.nats_client and self.nats_client.is_connected:
            await self.nats_client.close()
        logger.info("Daemon shutdown complete")


async def main():
    """Entry point for the daemon."""
    daemon = SovereigntyDaemon()

    # Handle graceful shutdown
    import signal

    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating shutdown...")
        asyncio.create_task(daemon.shutdown())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    await daemon.run()


if __name__ == '__main__':
    asyncio.run(main())
