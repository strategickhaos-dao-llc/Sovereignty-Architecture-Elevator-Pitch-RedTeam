#!/usr/bin/env python3
"""
dispatcher.py — Grok Node Dispatcher v2.0
Local LLM reasoning loop with NATS integration (Evolution #8)
Subscribes to cmd.grok.*, reasons with Ollama, publishes to summaries.*

Strategickhaos DAO LLC / Valoryield Engine
Author: Domenic Garza (Node 137)
"""

import asyncio
import json
import os
import logging
import httpx
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('grok-dispatcher')

# Configuration
NATS_URL = os.environ.get('NATS_URL', 'nats://swarm:swarm@10.44.0.1:4222')
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
GROK_MODEL = os.environ.get('GROK_MODEL', 'llama3:8b')
MAX_TOKENS = int(os.environ.get('MAX_TOKENS', '2048'))
TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.7'))

# Subjects
CMD_SUBJECT = 'cmd.grok.>'
SUMMARY_SUBJECT = 'summaries'
INSIGHTS_SUBJECT = 'insights'


class OllamaClient:
    """Client for Ollama LLM API."""
    
    def __init__(self, base_url: str = OLLAMA_URL):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def generate(self, prompt: str, model: str = GROK_MODEL, 
                      max_tokens: int = MAX_TOKENS,
                      temperature: float = TEMPERATURE) -> str:
        """Generate a response from the LLM."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', '')
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise
    
    async def list_models(self) -> list:
        """List available models."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [m['name'] for m in data.get('models', [])]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    async def pull_model(self, model: str) -> bool:
        """Pull a model if not available."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/pull",
                json={"name": model},
                timeout=600.0  # Model downloads can take time
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to pull model {model}: {e}")
            return False
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


class GrokDispatcher:
    """
    Grok Dispatcher for swarm AI reasoning.
    Subscribes to NATS commands, processes with LLM, publishes results.
    """
    
    def __init__(self):
        self.ollama = OllamaClient()
        self.nc = None
        self.js = None
        self.request_count = 0
        self.error_count = 0
    
    async def connect(self) -> None:
        """Connect to NATS server."""
        try:
            # Deferred import: nats-py is optional and may not be installed
            # in all deployment scenarios. This allows the module to load
            # even without nats-py for testing/development purposes.
            import nats
            self.nc = await nats.connect(NATS_URL)
            self.js = self.nc.jetstream()
            logger.info(f"Connected to NATS at {NATS_URL}")
        except ImportError:
            logger.error("nats-py required: pip install nats-py")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            raise
    
    async def ensure_model(self) -> None:
        """Ensure the configured model is available."""
        models = await self.ollama.list_models()
        if GROK_MODEL not in models:
            logger.info(f"Pulling model {GROK_MODEL}...")
            await self.ollama.pull_model(GROK_MODEL)
    
    async def process_command(self, msg) -> None:
        """Process an incoming command message."""
        try:
            subject = msg.subject
            data = json.loads(msg.data.decode())
            
            logger.info(f"Received command on {subject}: {data.get('type', 'unknown')}")
            self.request_count += 1
            
            # Extract command type and payload
            cmd_type = data.get('type', 'analyze')
            payload = data.get('payload', {})
            context = data.get('context', '')
            request_id = data.get('request_id', f'req-{self.request_count}')
            
            # Build prompt based on command type
            if cmd_type == 'analyze':
                prompt = self._build_analysis_prompt(payload, context)
            elif cmd_type == 'summarize':
                prompt = self._build_summary_prompt(payload, context)
            elif cmd_type == 'audit':
                prompt = self._build_audit_prompt(payload, context)
            elif cmd_type == 'reason':
                prompt = self._build_reasoning_prompt(payload, context)
            else:
                prompt = f"Process this request: {json.dumps(payload)}\nContext: {context}"
            
            # Generate response
            start_time = datetime.utcnow()
            response = await self.ollama.generate(prompt)
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            # Build result
            result = {
                'request_id': request_id,
                'type': cmd_type,
                'response': response,
                'model': GROK_MODEL,
                'duration_sec': duration,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'node_id': os.environ.get('NODE_ID', 'grok-0'),
            }
            
            # Publish to appropriate subject
            if cmd_type == 'summarize':
                pub_subject = f"{SUMMARY_SUBJECT}.{request_id}"
            else:
                pub_subject = f"{INSIGHTS_SUBJECT}.{cmd_type}.{request_id}"
            
            await self.nc.publish(
                pub_subject,
                json.dumps(result).encode()
            )
            
            logger.info(f"Published response to {pub_subject} ({duration:.2f}s)")
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in message: {e}")
            self.error_count += 1
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.error_count += 1
    
    def _build_analysis_prompt(self, payload: dict, context: str) -> str:
        """Build an analysis prompt."""
        return f"""You are an AI analyst for the Sovereign Swarm system.
Analyze the following data and provide insights.

Data:
{json.dumps(payload, indent=2)}

Context:
{context}

Provide a structured analysis with:
1. Key observations
2. Potential issues or anomalies
3. Recommended actions
4. Risk assessment (LOW/MEDIUM/HIGH)

Analysis:"""

    def _build_summary_prompt(self, payload: dict, context: str) -> str:
        """Build a summarization prompt."""
        return f"""You are a summarization agent for the Sovereign Swarm system.
Create a concise summary of the following information.

Information:
{json.dumps(payload, indent=2)}

Context:
{context}

Provide:
1. Executive summary (2-3 sentences)
2. Key points (bullet list)
3. Action items if any

Summary:"""

    def _build_audit_prompt(self, payload: dict, context: str) -> str:
        """Build an audit prompt."""
        return f"""You are a security auditor for the Sovereign Swarm system.
Audit the following activity and assess compliance.

Activity Log:
{json.dumps(payload, indent=2)}

Context:
{context}

Evaluate:
1. Compliance status (PASS/WARN/FAIL)
2. Security concerns
3. Policy violations if any
4. Recommendations

Audit Report:"""

    def _build_reasoning_prompt(self, payload: dict, context: str) -> str:
        """Build a reasoning prompt."""
        return f"""You are a reasoning agent for the Sovereign Swarm system.
Apply logical reasoning to solve the following problem.

Problem:
{json.dumps(payload, indent=2)}

Context:
{context}

Reasoning steps:
1. Identify the core question
2. Gather relevant facts
3. Apply logical deduction
4. Validate conclusions
5. Provide answer with confidence level

Reasoning:"""

    async def subscribe(self) -> None:
        """Subscribe to command subjects."""
        await self.nc.subscribe(CMD_SUBJECT, cb=self.process_command)
        logger.info(f"Subscribed to {CMD_SUBJECT}")
    
    async def publish_heartbeat(self) -> None:
        """Publish periodic heartbeat."""
        while True:
            try:
                heartbeat = {
                    'node_id': os.environ.get('NODE_ID', 'grok-0'),
                    'type': 'grok',
                    'status': 'online',
                    'model': GROK_MODEL,
                    'requests_processed': self.request_count,
                    'errors': self.error_count,
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                }
                await self.nc.publish(
                    'telemetry.grok.heartbeat',
                    json.dumps(heartbeat).encode()
                )
                logger.debug("Heartbeat published")
            except Exception as e:
                logger.error(f"Heartbeat failed: {e}")
            
            await asyncio.sleep(30)
    
    async def run(self) -> None:
        """Main run loop."""
        await self.connect()
        await self.ensure_model()
        await self.subscribe()
        
        # Start heartbeat task
        asyncio.create_task(self.publish_heartbeat())
        
        logger.info(f"Grok Dispatcher running with model {GROK_MODEL}")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
    
    async def shutdown(self) -> None:
        """Clean shutdown."""
        if self.nc:
            await self.nc.close()
        await self.ollama.close()
        logger.info("Dispatcher shutdown complete")


async def main():
    """Main entry point."""
    dispatcher = GrokDispatcher()
    
    try:
        await dispatcher.run()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        await dispatcher.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
