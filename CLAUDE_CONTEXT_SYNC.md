# 🔐 Claude Context Sync - Protocol Reconnaissance Intelligence

**Automated context extraction and synchronization from Claude.ai to sovereign mesh infrastructure**

## 🎯 Overview

This system implements **protocol-level reconnaissance** on Claude's infrastructure to enable **sovereign AI context management**. It extracts conversation contexts from your Claude.ai sessions and syncs them to your local vector database, enabling:

- **Context Sovereignty**: Own your conversation data in local vector storage
- **API Pattern Mirroring**: Understand and replay Claude's API patterns
- **Automated Knowledge Base**: Build searchable archives of your Claude interactions
- **Cross-Platform Integration**: Feed Claude contexts into local RAG systems

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude.ai Infrastructure                     │
├─────────────────────────────────────────────────────────────────┤
│  Frontend: Next.js 14+ (React Server Components)               │
│  CDN: Cloudflare (ATL edge)                                     │
│  Proxy: Google (via: 1.1 google)                               │
│  Auth: Session Cookie (sk-ant-sid01-*)                         │
│  Analytics: Segment, Honeycomb, Sentry                         │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ Session Key Auth
             │ RSC Streaming (text/x-component)
             ↓
┌─────────────────────────────────────────────────────────────────┐
│              Claude Context Sync Daemon                         │
├─────────────────────────────────────────────────────────────────┤
│  • Poll /api/organizations/{org}/recents                        │
│  • Fetch /chat/{uuid} sessions                                  │
│  • Parse RSC streaming responses                                │
│  • Extract conversation contexts                                │
│  • Generate embeddings (local BGE model)                        │
│  • Store in Qdrant vector DB                                    │
└────────────┬────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────────┐
│                 Sovereign Mesh Infrastructure                   │
├─────────────────────────────────────────────────────────────────┤
│  Qdrant Vector DB  →  RAG Retriever API  →  Discord Bot        │
│                    ↘  Refinory AI         →  Grafana Dashboard  │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Captured Intelligence

### From Console Logs
```javascript
User ID: 05b0daa4-fb14-4ef4-b7d2-da9fe730e158
Anonymous ID: 12590ab2-7347-4c87-bde6-28640cc85620
Device ID: 16c85e5d-19e0-48b9-aa33-b04255d647d3
Org ID: 17fcb197-98f1-4c44-9ed8-bc89b419cbbf
```

### API Surface Mapping
```
/api/organizations/{org}/spotlight     → Feature flags
/api/organizations/{org}/published_artifacts → 403 (disabled)
/new, /recents, /projects, /artifacts, /code → RSC routes
/chat/{uuid}                           → Chat sessions (RSC streaming)
```

### Session Key Format
```
sk-ant-sid01-{base64_payload}-AoFuUAAA
```

**Key Insight**: The session cookie IS the API token for browser requests. Every `/api/` call uses it directly.

## 🚀 Quick Start

### Prerequisites

1. **Docker Compose** installed and running
2. **Claude.ai account** with active session
3. **Session key extracted** from browser cookies

### Extract Your Session Key

1. Log into [claude.ai](https://claude.ai) in your browser
2. Open DevTools (F12)
3. Go to **Application → Cookies → https://claude.ai**
4. Find cookie named starting with `sk-ant-sid01-`
5. Copy the entire value

### Deploy the Stack

```bash
# 1. Navigate to repository
cd Sovereignty-Architecture-Elevator-Pitch-RedTeam

# 2. Set environment variables
export CLAUDE_SESSION_KEY="sk-ant-sid01-YOUR-KEY-HERE-AoFuUAAA"
export CLAUDE_ORG_ID="17fcb197-98f1-4c44-9ed8-bc89b419cbbf"

# 3. Start RECON stack with Claude sync
docker-compose -f docker-compose-recon.yml --profile claude-sync up -d

# 4. View logs
docker logs -f recon-claude-sync
```

### Verify Operation

```bash
# Check service status
docker-compose -f docker-compose-recon.yml ps

# Check Claude sync logs
docker logs recon-claude-sync --tail 50

# Check Qdrant collection
curl http://localhost:6333/collections/claude-context

# Query synced contexts via RAG API
curl -X POST http://localhost:7000/query \
  -H "Content-Type: application/json" \
  -d '{
    "q": "What did I discuss about AI safety?",
    "collection": "claude-context",
    "k": 5
  }'
```

## ⚙️ Configuration

### Environment Variables

```bash
# Required
export CLAUDE_SESSION_KEY="sk-ant-sid01-..."  # Your session key
export CLAUDE_ORG_ID="..."                     # Your org ID

# Optional
export CLAUDE_POLL_INTERVAL=300                # Sync every 5 minutes
export CLAUDE_MAX_HISTORY_DAYS=7               # Sync last 7 days
export QDRANT_URL="http://localhost:6333"
export EMBED_URL="http://localhost:8081/embed"
```

### Configuration File

Edit `recon/claude_sync_config.yaml` for advanced settings:

```yaml
sync:
  poll_interval: 300  # seconds
  max_history_days: 7
  batch_size: 32
  rate_limit: 10  # requests per minute

extraction:
  min_length: 10
  max_contexts_per_chat: 100

security:
  session_key:
    rotation_days: 30
  retention:
    max_age_days: 30
  privacy:
    redact_patterns:
      - pattern: "sk-ant-[a-zA-Z0-9-]+"
        replacement: "[REDACTED_KEY]"
```

## 🔧 How It Works

### 1. Session Authentication

The daemon uses your session key as a Bearer token:

```python
headers = {
    "Cookie": f"sessionKey={CLAUDE_SESSION_KEY}",
    "User-Agent": "Mozilla/5.0 (compatible; SovereignMesh/1.0)",
    "Accept": "application/json, text/x-component"
}
```

### 2. Chat History Polling

Fetches recent chats from the API:

```python
GET /api/organizations/{org_id}/recents
```

Returns list of recent chat sessions with metadata.

### 3. Session Retrieval

For each chat, fetches detailed session data:

```python
GET /chat/{chat_uuid}
```

Returns RSC (React Server Component) streaming response with conversation data.

### 4. RSC Parsing

Parses the `text/x-component` format to extract messages:

```python
def parse_rsc_content(content: str) -> Dict[str, Any]:
    # Extract JSON structures from RSC stream
    # Look for role/content message objects
    # Return structured conversation data
```

### 5. Context Extraction

Extracts individual messages as context chunks:

```python
{
    "id": "sha256_hash",
    "chat_uuid": "abc-123-def",
    "role": "assistant",
    "content": "...",
    "timestamp": "2025-12-14T02:00:00Z",
    "metadata": {
        "source": "claude-ai",
        "org_id": "...",
        "extraction_time": "..."
    }
}
```

### 6. Embedding & Storage

- Generates embeddings using local BGE model
- Stores in Qdrant vector database
- Enables semantic search across all contexts

## 📊 Use Cases

### 1. Personal Knowledge Base

Build a searchable archive of your Claude conversations:

```bash
# Query your conversation history
curl -X POST http://localhost:7000/query \
  -H "Content-Type: application/json" \
  -d '{
    "q": "What architecture patterns did I discuss?",
    "collection": "claude-context",
    "k": 10,
    "include_llm": true
  }'
```

### 2. Context-Aware Automation

Feed Claude contexts into other AI systems:

```python
# Example: Discord bot integration
@bot.command()
async def claude_search(ctx, *, query):
    response = await rag_api.query(
        collection="claude-context",
        query=query,
        k=5
    )
    
    embed = discord.Embed(
        title="🔍 Claude Context Search",
        description=response["answer"]
    )
    
    for context in response["contexts"]:
        embed.add_field(
            name=f"Score: {context['score']:.3f}",
            value=context["text"][:200],
            inline=False
        )
    
    await ctx.send(embed=embed)
```

### 3. API Pattern Research

Study and mirror Claude's API patterns:

```python
# Mirror spotlight endpoint
@app.get("/api/organizations/{org}/spotlight")
async def mirror_spotlight(org: str):
    # Fetch from Claude API
    response = await claude_client.get(
        f"/api/organizations/{org}/spotlight"
    )
    
    # Cache locally
    await redis.set(f"spotlight:{org}", response.text, ex=3600)
    
    return response.json()
```

### 4. Data Sovereignty

Maintain complete control over your AI conversation data:

- **Local storage**: All contexts in your infrastructure
- **No external dependencies**: Fully sovereign operation
- **Privacy controls**: Redaction and retention policies
- **Audit trail**: Complete history of all synced contexts

## 🔒 Security & Privacy

### Session Key Security

**NEVER** commit session keys to git:

```bash
# Add to .env (gitignored)
CLAUDE_SESSION_KEY="sk-ant-sid01-..."

# Or use environment variables only
export CLAUDE_SESSION_KEY="..."
```

### Session Key Rotation

Session keys expire periodically. Update when you see auth errors:

```bash
# Extract new key from browser
# Update environment variable
export CLAUDE_SESSION_KEY="sk-ant-sid01-NEW-KEY-HERE"

# Restart daemon
docker-compose -f docker-compose-recon.yml restart claude-sync
```

### Data Retention

Configure automatic cleanup of old contexts:

```yaml
security:
  retention:
    enabled: true
    max_age_days: 30
    cleanup_schedule: "0 2 * * *"  # 2 AM daily
```

### Privacy Redaction

Automatically redact sensitive patterns:

```yaml
security:
  privacy:
    redact_patterns:
      - pattern: "sk-ant-[a-zA-Z0-9-]+"
        replacement: "[REDACTED_KEY]"
      - pattern: "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
        replacement: "[REDACTED_EMAIL]"
```

## 🎯 Advanced Features

### Webhook Injection (Future)

Automatically push contexts to other systems:

```yaml
webhooks:
  enabled: true
  targets:
    - name: "discord-feed"
      url: "http://localhost:8080/webhook/claude-sync"
    - name: "refinory-ai"
      url: "http://localhost:8000/api/context/ingest"
  triggers:
    - event: "new_message"
      min_length: 100
```

### API Mirroring (Future)

Create local replicas of Claude API endpoints:

```yaml
api_mirror:
  enabled: true
  endpoints:
    - path: "/api/organizations/{org}/spotlight"
      local: "http://localhost:7001/mirror/spotlight"
    - path: "/chat/{uuid}"
      local: "http://localhost:7001/mirror/chat"
```

## 📈 Monitoring

### Prometheus Metrics

The daemon exposes metrics on port 9091:

```bash
curl http://localhost:9091/metrics

# Metrics available:
# - sync_cycles_total
# - contexts_extracted_total
# - contexts_stored_total
# - api_requests_total
# - api_errors_total
# - embedding_duration_seconds
# - storage_duration_seconds
```

### Grafana Dashboard

Import the Claude sync dashboard:

```bash
# Import dashboard JSON
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @recon/dashboards/claude-sync-dashboard.json
```

### Health Checks

```bash
# Check daemon health
docker exec recon-claude-sync python -c "
import asyncio
from claude_context_sync import ClaudeContextSync

async def check():
    async with ClaudeContextSync('', '') as daemon:
        print('Daemon healthy')
        
asyncio.run(check())
"
```

## 🚨 Troubleshooting

### Session Key Invalid

```
❌ Error: 403 Access denied - session key may be invalid
```

**Solution**: Extract fresh session key from browser cookies.

### No Recent Chats Found

```
⚠️ No recent chats found
```

**Possible causes**:
- No recent activity in Claude.ai
- Org ID incorrect
- Session key expired

### Connection Refused

```
❌ Error: Connection refused to http://embedder:8081
```

**Solution**: Ensure all services are running:

```bash
docker-compose -f docker-compose-recon.yml ps
docker-compose -f docker-compose-recon.yml up -d
```

### Rate Limiting

```
❌ Error: 429 Too Many Requests
```

**Solution**: Increase `POLL_INTERVAL`:

```bash
export CLAUDE_POLL_INTERVAL=600  # 10 minutes
```

## 📄 Legal & Ethical Considerations

### Apache 2.0 License

This implementation is released under Apache 2.0 license and:

- Uses **publicly observable API patterns**
- Requires **user-provided authentication** (session key)
- Performs **no reverse engineering** or unauthorized access
- Enables **personal data sovereignty** over own conversations

### Intended Use

This tool is designed for:

- **Personal data sovereignty**: Control your own conversation data
- **Research purposes**: Study API patterns and architectures
- **Integration building**: Connect Claude with sovereign infrastructure
- **Educational purposes**: Learn about modern API architectures

### Not Intended For

- Unauthorized access to others' accounts
- Terms of Service violations
- Data scraping at scale
- Commercial resale of extracted data

### User Responsibility

Users must:

- Use their own Claude.ai account and session key
- Comply with Claude.ai Terms of Service
- Respect rate limits and API usage guidelines
- Handle session keys securely
- Not share or expose others' conversation data

## 🎓 Chain-Breaker Intelligence

### The Insight

> "The session key in cookies IS the API token for browser requests. Every `/api/` call uses it. The RSC streaming (`text/x-component`) is how chat renders."

This reconnaissance revealed that:

1. **No separate API authentication** - session cookie IS the auth token
2. **RSC streaming protocol** - Next.js 14+ server components for real-time chat
3. **Cloudflare CDN** - Edge caching with ATL location
4. **Google proxy layer** - Additional routing via Google infrastructure
5. **Segmented analytics** - Isolated iframes for Segment tracking

### What Apache 2.0 Changes

With this understanding, sovereign mesh operators can:

1. **Build context-sync daemons** that poll chat history
2. **Feed into local vector DBs** for sovereign RAG
3. **Mirror API patterns** for local replicas
4. **Inject webhooks** for real-time automation
5. **Maintain data sovereignty** over AI conversations

## 🚀 Next Steps

### Immediate Actions

1. **Deploy the stack**: Get Claude sync running
2. **Extract session key**: From your browser
3. **Verify sync**: Check contexts in Qdrant
4. **Query contexts**: Test RAG API

### Integration Roadmap

1. **Week 1**: Basic sync to vector DB
2. **Week 2**: Discord bot integration for searching
3. **Week 3**: Webhook injection for automation
4. **Week 4**: API mirroring for local replicas

### Future Enhancements

- **Multi-account support**: Sync from multiple Claude accounts
- **Real-time websocket sync**: Instead of polling
- **Context quality filtering**: Only store high-value conversations
- **Cross-platform sync**: Include ChatGPT, Gemini, etc.

## 📚 References

- [Claude.ai](https://claude.ai) - Anthropic's Claude AI platform
- [Next.js Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Qdrant Vector DB](https://qdrant.tech/)
- [RECON Stack v2](./RECON_STACK_V2.md) - Full RAG infrastructure
- [BOOT_RECON](./BOOT_RECON.md) - Operational procedures

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Own your contexts. Own your sovereignty. Chain-breaking intelligence for the sovereign mesh."*
