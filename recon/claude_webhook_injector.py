#!/usr/bin/env python3
"""
Claude Webhook Injector
Automatically pushes Claude contexts to external systems via webhooks
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
import yaml
from pydantic import BaseModel, HttpUrl

# Configuration
CONFIG_FILE = os.getenv("WEBHOOK_CONFIG", "claude_sync_config.yaml")

class WebhookTarget(BaseModel):
    """Webhook target configuration."""
    name: str
    url: HttpUrl
    enabled: bool = True
    headers: Dict[str, str] = {}
    timeout: int = 30

class WebhookTrigger(BaseModel):
    """Webhook trigger condition."""
    event: str
    min_length: Optional[int] = None
    confidence_threshold: Optional[float] = None

class WebhookInjector:
    """
    Manages webhook injection for Claude contexts.
    Pushes contexts to external systems based on configured triggers.
    """
    
    def __init__(self, config_path: str = CONFIG_FILE):
        self.config_path = config_path
        self.targets: List[WebhookTarget] = []
        self.triggers: List[WebhookTrigger] = []
        self.http_client = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.http_client = httpx.AsyncClient(timeout=30)
        await self.load_config()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.http_client:
            await self.http_client.aclose()
    
    async def load_config(self):
        """Load webhook configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            webhooks_config = config.get('webhooks', {})
            
            if not webhooks_config.get('enabled', False):
                print("⚠️ Webhooks disabled in configuration")
                return
            
            # Load targets
            targets = webhooks_config.get('targets', [])
            for target_config in targets:
                if target_config.get('enabled', False):
                    target = WebhookTarget(**target_config)
                    self.targets.append(target)
            
            # Load triggers
            triggers = webhooks_config.get('triggers', [])
            for trigger_config in triggers:
                trigger = WebhookTrigger(**trigger_config)
                self.triggers.append(trigger)
            
            print(f"✅ Loaded {len(self.targets)} webhook targets and {len(self.triggers)} triggers")
            
        except FileNotFoundError:
            print(f"⚠️ Config file not found: {self.config_path}")
        except Exception as e:
            print(f"❌ Error loading config: {e}")
    
    def should_trigger(self, event: str, context: Dict[str, Any]) -> bool:
        """
        Check if context should trigger webhooks based on conditions.
        """
        for trigger in self.triggers:
            if trigger.event != event:
                continue
            
            # Check min_length condition
            if trigger.min_length is not None:
                content = context.get('content', '')
                if len(content) < trigger.min_length:
                    continue
            
            # Check confidence_threshold condition
            if trigger.confidence_threshold is not None:
                confidence = context.get('confidence', 0.0)
                if confidence < trigger.confidence_threshold:
                    continue
            
            # All conditions passed
            return True
        
        return False
    
    async def send_webhook(self, target: WebhookTarget, payload: Dict[str, Any]) -> bool:
        """
        Send webhook to a target.
        Returns True on success, False on failure.
        """
        try:
            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "ClaudeContextSync/1.0",
                **target.headers
            }
            
            # Send webhook
            response = await self.http_client.post(
                str(target.url),
                json=payload,
                headers=headers,
                timeout=target.timeout
            )
            
            response.raise_for_status()
            
            print(f"✅ Webhook sent to {target.name}: {response.status_code}")
            return True
            
        except httpx.HTTPStatusError as e:
            print(f"❌ Webhook error for {target.name}: {e.response.status_code}")
            return False
        except Exception as e:
            print(f"❌ Webhook error for {target.name}: {e}")
            return False
    
    async def inject_context(self, context: Dict[str, Any], event: str = "new_message"):
        """
        Inject context to all enabled webhook targets if triggers match.
        """
        if not self.targets:
            return
        
        # Check if context should trigger webhooks
        if not self.should_trigger(event, context):
            return
        
        # Prepare webhook payload
        payload = {
            "event": event,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "source": "claude-context-sync"
        }
        
        # Send to all enabled targets
        tasks = []
        for target in self.targets:
            if target.enabled:
                task = self.send_webhook(target, payload)
                tasks.append(task)
        
        # Execute all webhooks concurrently
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            success_count = sum(1 for r in results if r is True)
            print(f"📤 Sent webhooks: {success_count}/{len(tasks)} successful")
    
    async def inject_batch(self, contexts: List[Dict[str, Any]], event: str = "new_message"):
        """
        Inject multiple contexts as a batch.
        """
        if not self.targets:
            return
        
        # Filter contexts that should trigger
        filtered = [ctx for ctx in contexts if self.should_trigger(event, ctx)]
        
        if not filtered:
            return
        
        # Prepare batch payload
        payload = {
            "event": "batch_" + event,
            "timestamp": datetime.now().isoformat(),
            "contexts": filtered,
            "count": len(filtered),
            "source": "claude-context-sync"
        }
        
        # Send to all enabled targets
        tasks = []
        for target in self.targets:
            if target.enabled:
                task = self.send_webhook(target, payload)
                tasks.append(task)
        
        # Execute all webhooks concurrently
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            success_count = sum(1 for r in results if r is True)
            print(f"📤 Sent batch webhooks: {success_count}/{len(tasks)} successful")

# Example webhook endpoints for integration

async def discord_webhook_handler(payload: Dict[str, Any]):
    """
    Example handler for Discord webhook integration.
    Formats Claude context for Discord messages.
    """
    context = payload.get('context', {})
    
    # Format as Discord embed
    embed = {
        "title": "🔍 New Claude Context",
        "description": context.get('content', '')[:2000],  # Discord limit
        "color": 0x5865F2,  # Discord blurple
        "fields": [
            {
                "name": "Role",
                "value": context.get('role', 'unknown'),
                "inline": True
            },
            {
                "name": "Chat UUID",
                "value": context.get('chat_uuid', 'unknown')[:50],
                "inline": True
            },
            {
                "name": "Timestamp",
                "value": context.get('timestamp', 'unknown'),
                "inline": False
            }
        ],
        "footer": {
            "text": "Claude Context Sync"
        }
    }
    
    return {"embeds": [embed]}

async def refinory_webhook_handler(payload: Dict[str, Any]):
    """
    Example handler for Refinory AI integration.
    Formats Claude context for AI processing.
    """
    context = payload.get('context', {})
    
    return {
        "type": "context_ingestion",
        "source": "claude-ai",
        "content": context.get('content', ''),
        "metadata": {
            "role": context.get('role'),
            "chat_uuid": context.get('chat_uuid'),
            "timestamp": context.get('timestamp'),
            "org_id": context.get('metadata', {}).get('org_id')
        }
    }

async def main():
    """Example usage."""
    
    # Example context from Claude
    example_context = {
        "id": "abc123",
        "chat_uuid": "test-chat-uuid",
        "message_index": 0,
        "role": "assistant",
        "content": "This is a test message with more than 100 characters to trigger the webhook based on min_length condition. It contains useful information about AI safety.",
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "source": "claude-ai",
            "org_id": "test-org"
        }
    }
    
    # Initialize injector
    async with WebhookInjector() as injector:
        # Inject single context
        await injector.inject_context(example_context, event="new_message")
        
        # Inject batch
        batch = [example_context] * 3
        await injector.inject_batch(batch, event="new_message")

if __name__ == "__main__":
    asyncio.run(main())
