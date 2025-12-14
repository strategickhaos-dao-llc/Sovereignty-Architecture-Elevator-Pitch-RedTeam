#!/usr/bin/env python3
"""
Claude Context Sync Daemon
Protocol-level reconnaissance for Claude infrastructure
Extracts context from chat sessions and syncs to sovereign mesh
"""

import os
import time
import json
import asyncio
import hashlib
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import httpx
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# Optional webhook injection
try:
    from claude_webhook_injector import WebhookInjector
    WEBHOOKS_AVAILABLE = True
except ImportError:
    WEBHOOKS_AVAILABLE = False

# Claude API Configuration
CLAUDE_API_BASE = os.getenv("CLAUDE_API_BASE", "https://claude.ai")
CLAUDE_ORG_ID = os.getenv("CLAUDE_ORG_ID", "17fcb197-98f1-4c44-9ed8-bc89b419cbbf")
CLAUDE_SESSION_KEY = os.getenv("CLAUDE_SESSION_KEY", "")  # sk-ant-sid01-*

# Local Infrastructure
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBED_URL = os.getenv("EMBED_URL", "http://localhost:8081/embed")
COLLECTION = os.getenv("CLAUDE_COLLECTION", "claude-context")

# Sync Configuration
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "300"))  # 5 minutes
MAX_HISTORY_DAYS = int(os.getenv("MAX_HISTORY_DAYS", "7"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "32"))

class ClaudeContextSync:
    """Daemon for syncing Claude chat context to local sovereign mesh."""
    
    def __init__(self, session_key: str, org_id: str):
        self.session_key = session_key
        self.org_id = org_id
        self.base_url = CLAUDE_API_BASE
        
        # Infrastructure clients
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.http_client = None
        
        # State tracking
        self.last_sync_time = None
        self.seen_messages = set()
        
    async def __aenter__(self):
        """Async context manager entry."""
        # Setup HTTP client with session cookie
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; SovereignMesh/1.0)",
            "Accept": "application/json, text/x-component",
            "Cookie": f"sessionKey={self.session_key}"
        }
        
        self.http_client = httpx.AsyncClient(
            headers=headers,
            timeout=30,
            follow_redirects=True
        )
        
        # Ensure collection exists
        await self.ensure_collection_exists()
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.http_client:
            await self.http_client.aclose()
    
    async def ensure_collection_exists(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            collections = [c.name for c in self.qdrant.get_collections().collections]
            
            if COLLECTION not in collections:
                print(f"📦 Creating collection: {COLLECTION}")
                self.qdrant.create_collection(
                    collection_name=COLLECTION,
                    vectors_config=VectorParams(
                        size=384,  # BGE small embedding dimension
                        distance=Distance.COSINE
                    )
                )
                print(f"✅ Collection created: {COLLECTION}")
            else:
                print(f"✅ Collection exists: {COLLECTION}")
        except Exception as e:
            print(f"❌ Collection setup error: {e}")
            raise
    
    async def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text from local embedder service."""
        try:
            response = await self.http_client.post(
                EMBED_URL,
                json={"texts": [text]},
                timeout=30
            )
            response.raise_for_status()
            embeddings = response.json()["embeddings"]
            return embeddings[0]
        except Exception as e:
            print(f"❌ Embedding error: {e}")
            raise
    
    async def fetch_chat_history(self) -> List[Dict[str, Any]]:
        """
        Fetch recent chat sessions from Claude API.
        Uses /api/organizations/{org}/recents endpoint.
        """
        try:
            url = f"{self.base_url}/api/organizations/{self.org_id}/recents"
            
            print(f"🔍 Fetching chat history from: {url}")
            response = await self.http_client.get(url)
            
            if response.status_code == 403:
                print("⚠️ Access denied - session key may be invalid or endpoint disabled")
                return []
            
            response.raise_for_status()
            data = response.json()
            
            # Extract recent chats
            chats = data.get("recents", []) if isinstance(data, dict) else []
            print(f"📊 Found {len(chats)} recent chats")
            
            return chats
            
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP error fetching history: {e.response.status_code}")
            return []
        except Exception as e:
            print(f"❌ Error fetching chat history: {e}")
            return []
    
    async def fetch_chat_session(self, chat_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed chat session data.
        Uses /chat/{uuid} endpoint which returns RSC streaming.
        """
        try:
            url = f"{self.base_url}/chat/{chat_uuid}"
            
            print(f"🔍 Fetching chat session: {chat_uuid}")
            response = await self.http_client.get(url)
            
            if response.status_code == 404:
                print(f"⚠️ Chat not found: {chat_uuid}")
                return None
            
            response.raise_for_status()
            
            # Parse RSC response (text/x-component format)
            content = response.text
            
            # Extract JSON from RSC stream if present
            # RSC format often contains JSON payloads
            chat_data = self.parse_rsc_content(content)
            
            return chat_data
            
        except Exception as e:
            print(f"❌ Error fetching chat session {chat_uuid}: {e}")
            return None
    
    def parse_rsc_content(self, content: str) -> Dict[str, Any]:
        """
        Parse React Server Component streaming response.
        Extracts conversation data from RSC format.
        """
        # RSC format can contain multiple JSON objects
        # Try to extract conversation messages
        messages = []
        
        # Look for JSON-like structures in the content
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('{') or line.startswith('['):
                try:
                    data = json.loads(line)
                    if isinstance(data, dict):
                        # Look for message-like structures
                        if 'role' in data and 'content' in data:
                            messages.append(data)
                        elif 'messages' in data:
                            messages.extend(data['messages'])
                except json.JSONDecodeError:
                    continue
        
        return {
            "messages": messages,
            "raw_content": content[:1000]  # Keep first 1KB for debugging
        }
    
    async def extract_context_from_chat(self, chat_data: Dict[str, Any], chat_uuid: str) -> List[Dict[str, Any]]:
        """
        Extract meaningful context from chat session.
        Returns list of context chunks ready for embedding.
        """
        contexts = []
        messages = chat_data.get("messages", [])
        
        for idx, message in enumerate(messages):
            role = message.get("role", "unknown")
            content = message.get("content", "")
            
            # Skip empty messages
            if not content or len(content.strip()) < 10:
                continue
            
            # Create unique ID for this message
            msg_id = hashlib.sha256(
                f"{chat_uuid}:{idx}:{content[:100]}".encode()
            ).hexdigest()
            
            # Skip if already seen
            if msg_id in self.seen_messages:
                continue
            
            self.seen_messages.add(msg_id)
            
            # Create context chunk
            context = {
                "id": msg_id,
                "chat_uuid": chat_uuid,
                "message_index": idx,
                "role": role,
                "content": content,
                "timestamp": message.get("created_at", datetime.now().isoformat()),
                "metadata": {
                    "source": "claude-ai",
                    "org_id": self.org_id,
                    "extraction_time": datetime.now().isoformat()
                }
            }
            
            contexts.append(context)
        
        return contexts
    
    async def store_contexts(self, contexts: List[Dict[str, Any]], trigger_webhooks: bool = True):
        """
        Store extracted contexts in Qdrant vector database.
        Optionally trigger webhooks for new contexts.
        """
        if not contexts:
            print("⚠️ No contexts to store")
            return
        
        print(f"💾 Storing {len(contexts)} context chunks...")
        
        # Process in batches
        for i in range(0, len(contexts), BATCH_SIZE):
            batch = contexts[i:i + BATCH_SIZE]
            
            try:
                # Get embeddings for batch - process concurrently for better performance
                texts = [ctx["content"] for ctx in batch]
                
                # Create embedding tasks for concurrent execution
                embedding_tasks = [self.get_embedding(text) for text in texts]
                
                try:
                    embeddings = await asyncio.gather(*embedding_tasks, return_exceptions=True)
                except Exception as e:
                    print(f"❌ Batch embedding error: {e}")
                    continue
                
                # Build points, handling any failed embeddings
                points = []
                for ctx, embedding in zip(batch, embeddings):
                    # Skip failed embeddings (marked as exceptions)
                    if isinstance(embedding, Exception):
                        print(f"⚠️ Failed to embed context {ctx['id']}: {embedding}")
                        continue
                    
                    # Create Qdrant point
                    point = PointStruct(
                        id=ctx["id"],
                        vector=embedding,
                        payload={
                            "chat_uuid": ctx["chat_uuid"],
                            "message_index": ctx["message_index"],
                            "role": ctx["role"],
                            "content": ctx["content"],
                            "timestamp": ctx["timestamp"],
                            "source": ctx["metadata"]["source"],
                            "org_id": ctx["metadata"]["org_id"],
                            "extraction_time": ctx["metadata"]["extraction_time"]
                        }
                    )
                    points.append(point)
                
                # Only upload if we have valid points
                if not points:
                    print(f"⚠️ No valid embeddings in batch, skipping upload")
                    continue
                
                # Upload batch to Qdrant
                self.qdrant.upsert(
                    collection_name=COLLECTION,
                    points=points
                )
                
                print(f"   ✅ Stored batch {i//BATCH_SIZE + 1}/{(len(contexts) + BATCH_SIZE - 1)//BATCH_SIZE} ({len(points)} points)")
                
                # Trigger webhooks if enabled
                if trigger_webhooks and WEBHOOKS_AVAILABLE:
                    try:
                        async with WebhookInjector() as injector:
                            await injector.inject_batch(batch, event="new_message")
                    except Exception as webhook_err:
                        print(f"⚠️ Webhook injection failed: {webhook_err}")
                
            except Exception as e:
                print(f"❌ Error storing batch: {e}")
                continue
    
    async def sync_cycle(self):
        """
        Execute one complete sync cycle.
        Fetches recent chats and stores them in local vector DB.
        """
        print(f"\n🔄 Starting sync cycle at {datetime.now()}")
        
        # Fetch recent chats
        recent_chats = await self.fetch_chat_history()
        
        if not recent_chats:
            print("⚠️ No recent chats found")
            return
        
        # Process each chat
        all_contexts = []
        
        for chat in recent_chats[:10]:  # Limit to 10 most recent
            chat_uuid = chat.get("uuid") or chat.get("id")
            if not chat_uuid:
                continue
            
            # Fetch detailed chat session
            chat_data = await self.fetch_chat_session(chat_uuid)
            
            if not chat_data:
                continue
            
            # Extract contexts
            contexts = await self.extract_context_from_chat(chat_data, chat_uuid)
            all_contexts.extend(contexts)
            
            # Rate limiting - be respectful
            await asyncio.sleep(1)
        
        # Store all extracted contexts
        if all_contexts:
            await self.store_contexts(all_contexts)
            print(f"✅ Sync complete: {len(all_contexts)} new contexts stored")
        else:
            print("⚠️ No new contexts extracted")
        
        self.last_sync_time = datetime.now()
    
    async def run_daemon(self):
        """
        Run continuous sync daemon.
        Polls Claude API at regular intervals.
        """
        print("🚀 Claude Context Sync Daemon Starting")
        print(f"   Base URL: {self.base_url}")
        print(f"   Org ID: {self.org_id}")
        print(f"   Collection: {COLLECTION}")
        print(f"   Poll Interval: {POLL_INTERVAL}s")
        print(f"   Max History: {MAX_HISTORY_DAYS} days")
        print()
        
        cycle_count = 0
        
        while True:
            try:
                cycle_count += 1
                print(f"📊 Cycle #{cycle_count}")
                
                # Execute sync cycle
                await self.sync_cycle()
                
                # Wait for next cycle
                print(f"⏳ Waiting {POLL_INTERVAL}s until next sync...")
                await asyncio.sleep(POLL_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n🛑 Daemon stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in sync cycle: {e}")
                print(f"⏳ Retrying in {POLL_INTERVAL}s...")
                await asyncio.sleep(POLL_INTERVAL)

async def main():
    """Main entry point for daemon."""
    
    # Validate configuration
    if not CLAUDE_SESSION_KEY:
        print("❌ Error: CLAUDE_SESSION_KEY environment variable not set")
        print("   Format: sk-ant-sid01-{base64_payload}-AoFuUAAA")
        print("   Extract from browser cookies after logging into claude.ai")
        return
    
    print("🎯 Claude Context Sync Configuration:")
    print(f"   Session Key: {CLAUDE_SESSION_KEY[:20]}...{CLAUDE_SESSION_KEY[-10:]}")
    print(f"   Org ID: {CLAUDE_ORG_ID}")
    print(f"   Qdrant: {QDRANT_URL}")
    print(f"   Embeddings: {EMBED_URL}")
    print(f"   Collection: {COLLECTION}")
    print()
    
    # Wait for services
    print("⏳ Waiting for services to be ready...")
    await asyncio.sleep(5)
    
    # Start daemon
    async with ClaudeContextSync(CLAUDE_SESSION_KEY, CLAUDE_ORG_ID) as daemon:
        await daemon.run_daemon()

if __name__ == "__main__":
    asyncio.run(main())
