#!/usr/bin/env python3
"""
Example usage of Claude Context Sync system
Demonstrates all major features: sync, query, webhook, and API mirror
"""

import os
import asyncio
import json
from datetime import datetime

# Example 1: Query synced contexts via RAG API
async def example_query_contexts():
    """Query synced Claude contexts."""
    import httpx
    
    print("=" * 60)
    print("Example 1: Query Synced Contexts")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        # Query contexts
        response = await client.post(
            "http://localhost:7000/query",
            json={
                "q": "What did I discuss about AI safety?",
                "collection": "claude-context",
                "k": 5,
                "include_llm": True
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\nQuery: {result['query']}")
            print(f"Total contexts found: {result['total_contexts']}")
            print(f"Processing time: {result['processing_time']:.2f}s")
            
            if result.get('answer'):
                print(f"\nLLM Answer:\n{result['answer']}")
            
            print("\nTop contexts:")
            for i, ctx in enumerate(result['contexts'][:3], 1):
                print(f"\n{i}. Score: {ctx['score']:.3f}")
                print(f"   Role: {ctx['metadata'].get('role', 'unknown')}")
                print(f"   Text: {ctx['text'][:200]}...")
        else:
            print(f"Error: {response.status_code}")

# Example 2: Use API Mirror
async def example_api_mirror():
    """Use Claude API mirror for cached access."""
    import httpx
    
    print("\n" + "=" * 60)
    print("Example 2: Claude API Mirror")
    print("=" * 60)
    
    org_id = os.getenv("CLAUDE_ORG_ID", "17fcb197-98f1-4c44-9ed8-bc89b419cbbf")
    
    async with httpx.AsyncClient() as client:
        # Get spotlight (feature flags)
        print("\nFetching spotlight endpoint...")
        try:
            response = await client.get(
                f"http://localhost:7001/api/organizations/{org_id}/spotlight",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Cache: {response.headers.get('X-Cache', 'MISS')}")
                print(f"Response keys: {list(data.keys())[:5]}")
            else:
                print(f"⚠️ Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Get recent chats
        print("\nFetching recent chats...")
        try:
            response = await client.get(
                f"http://localhost:7001/api/organizations/{org_id}/recents",
                params={"limit": 5},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Cache: {response.headers.get('X-Cache', 'MISS')}")
                
                # Display recent chats
                recents = data.get('recents', [])
                print(f"Recent chats: {len(recents)}")
                for chat in recents[:3]:
                    print(f"  - {chat.get('title', 'Untitled')[:50]}")
            else:
                print(f"⚠️ Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Check cache stats
        print("\nCache statistics:")
        try:
            response = await client.get("http://localhost:7001/cache/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                print(f"  Total keys: {stats.get('total_keys', 0)}")
                print(f"  Hit rate: {stats.get('redis_info', {}).get('keyspace_hits', 0)}")
        except Exception as e:
            print(f"❌ Cache stats error: {e}")

# Example 3: Webhook Configuration
def example_webhook_config():
    """Show how to configure webhooks."""
    print("\n" + "=" * 60)
    print("Example 3: Webhook Configuration")
    print("=" * 60)
    
    webhook_config = {
        "webhooks": {
            "enabled": True,
            "targets": [
                {
                    "name": "discord-feed",
                    "url": "http://localhost:8080/webhook/claude-sync",
                    "enabled": True,
                    "headers": {
                        "Authorization": "Bearer YOUR_TOKEN"
                    }
                },
                {
                    "name": "refinory-ai",
                    "url": "http://localhost:8000/api/context/ingest",
                    "enabled": True
                }
            ],
            "triggers": [
                {
                    "event": "new_message",
                    "min_length": 100
                },
                {
                    "event": "new_chat"
                },
                {
                    "event": "high_quality_response",
                    "confidence_threshold": 0.8
                }
            ]
        }
    }
    
    print("\nWebhook configuration structure:")
    print(json.dumps(webhook_config, indent=2))
    
    print("\nTo enable webhooks:")
    print("1. Edit recon/claude_sync_config.yaml")
    print("2. Set webhooks.enabled: true")
    print("3. Configure target URLs")
    print("4. Define trigger conditions")
    print("5. Restart claude-sync service")

# Example 4: Direct Sync Usage
async def example_direct_sync():
    """Show direct usage of sync daemon programmatically."""
    print("\n" + "=" * 60)
    print("Example 4: Direct Sync Usage")
    print("=" * 60)
    
    print("\nDirect usage pattern (pseudo-code):")
    
    code = """
import asyncio
from claude_context_sync import ClaudeContextSync

async def sync_my_contexts():
    session_key = "sk-ant-sid01-YOUR-KEY-HERE"
    org_id = "YOUR-ORG-ID"
    
    async with ClaudeContextSync(session_key, org_id) as daemon:
        # Run one sync cycle
        await daemon.sync_cycle()
        
        # Or run continuous daemon
        # await daemon.run_daemon()

asyncio.run(sync_my_contexts())
"""
    
    print(code)
    
    print("\nFor production use:")
    print("- Use docker-compose with --profile claude-sync")
    print("- Set CLAUDE_SESSION_KEY environment variable")
    print("- Configure polling interval (default: 5 minutes)")
    print("- Monitor logs with: docker logs -f recon-claude-sync")

# Example 5: Security Best Practices
def example_security_practices():
    """Show security best practices."""
    print("\n" + "=" * 60)
    print("Example 5: Security Best Practices")
    print("=" * 60)
    
    practices = [
        {
            "practice": "Session Key Management",
            "tips": [
                "Never commit session keys to git",
                "Use environment variables only",
                "Rotate keys every 30 days",
                "Store in secure vault (e.g., Vault, 1Password)"
            ]
        },
        {
            "practice": "Data Retention",
            "tips": [
                "Enable auto-cleanup of old contexts",
                "Set max_age_days in configuration",
                "Schedule regular cleanup jobs",
                "Backup critical contexts before deletion"
            ]
        },
        {
            "practice": "Privacy Filtering",
            "tips": [
                "Enable pattern redaction in config",
                "Redact API keys, emails, PII",
                "Truncate session keys in logs",
                "Review contexts before webhook injection"
            ]
        },
        {
            "practice": "Network Security",
            "tips": [
                "Use TLS for webhook endpoints",
                "Implement webhook signature verification",
                "Rate limit API mirror endpoints",
                "Use internal networks for services"
            ]
        }
    ]
    
    for item in practices:
        print(f"\n{item['practice']}:")
        for tip in item['tips']:
            print(f"  • {tip}")

# Example 6: Integration Examples
def example_integrations():
    """Show integration examples with other systems."""
    print("\n" + "=" * 60)
    print("Example 6: System Integrations")
    print("=" * 60)
    
    print("\n1. Discord Bot Integration:")
    print("""
@bot.command()
async def claude_search(ctx, *, query):
    response = await rag_api.query(
        collection="claude-context",
        query=query,
        k=5
    )
    
    embed = discord.Embed(
        title="🔍 Claude Context Search",
        description=response["answer"][:2000]
    )
    
    for context in response["contexts"][:3]:
        embed.add_field(
            name=f"Score: {context['score']:.3f}",
            value=context["text"][:200],
            inline=False
        )
    
    await ctx.send(embed=embed)
""")
    
    print("\n2. Grafana Dashboard:")
    print("- Monitor sync cycles and success rate")
    print("- Track contexts extracted per hour")
    print("- Alert on sync failures")
    print("- Visualize API response times")
    
    print("\n3. Refinory AI Integration:")
    print("- Feed Claude contexts to AI agents")
    print("- Build knowledge base from conversations")
    print("- Enable cross-platform context sharing")
    print("- Automated expertise extraction")

async def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("CLAUDE CONTEXT SYNC - Example Usage")
    print("=" * 60)
    
    print("\nNOTE: These examples require running services:")
    print("  • docker-compose -f docker-compose-recon.yml --profile claude-sync up -d")
    print("  • export CLAUDE_SESSION_KEY=...")
    print()
    
    # Run examples (skip API calls if services not running)
    try:
        # Example 1: Query (requires RAG API)
        print("\nSkipping API examples (services may not be running)")
        print("To run API examples, start services first")
        
        # Show configuration examples
        example_webhook_config()
        example_security_practices()
        example_integrations()
        
        # Show usage patterns
        await example_direct_sync()
        
        print("\n" + "=" * 60)
        print("Examples complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Set CLAUDE_SESSION_KEY environment variable")
        print("2. Start services: ./claude-sync.sh start")
        print("3. View logs: ./claude-sync.sh logs")
        print("4. Query contexts: ./claude-sync.sh query 'your question'")
        print("5. Check status: ./claude-sync.sh status")
        print()
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure services are running and environment is configured")

if __name__ == "__main__":
    asyncio.run(main())
