# AI Agent Routing

## Overview

The Strategickhaos Sovereignty Architecture supports intelligent routing of AI queries to specialized language models based on channel context and query type.

## Routing Configuration

### Per-Channel Model Assignment

```yaml
ai_agents:
  enabled: true
  model_provider: "openai"
  model_name: "gpt-4o-mini"  # Default model
  routing:
    per_channel:
      "#agents": "gpt-4o-mini"        # General assistance
      "#inference-stream": "none"     # No AI in this channel
      "#prs": "claude-3-sonnet"       # Code review assistance
      "#alerts": "gpt-4o-mini"        # Alert analysis
      "#deployments": "gpt-4o-mini"   # Deployment guidance
```

### Model Selection Logic

```python
async def route_ai_query(channel_name: str, query: str) -> str:
    """Route query to appropriate AI model based on channel."""
    routing = config.ai_agents.routing.per_channel
    model = routing.get(channel_name, config.ai_agents.model_name)
    
    if model == "none":
        return "AI assistance is disabled in this channel."
    
    return await invoke_model(model, query)
```

## Vector Knowledge Base

### Namespace Structure

The vector store organizes knowledge into searchable namespaces:

```yaml
vector_store:
  type: "pgvector"
  namespaces:
    - name: "runbooks"
      sources:
        - type: "wiki"
          url: "https://wiki.strategickhaos.internal/runbooks"
        - type: "repo"
          repo: "git@github.com:org/runbooks.git"
          
    - name: "logs-schemas"
      sources:
        - type: "s3"
          bucket: "strategickhaos-observability"
          prefix: "schemas/"
          
    - name: "architecture"
      sources:
        - type: "repo"
          repo: "git@github.com:org/sovereignty-architecture.git"
          paths: ["docs/", "README.md"]
```

### RAG Pipeline

```
Query → Embed → Vector Search → Context Retrieval → LLM → Response
                    ↓
            Relevant Docs
            (runbooks, schemas, etc.)
```

## Supported Models

### OpenAI Models

| Model | Use Case | Cost Tier |
|-------|----------|-----------|
| `gpt-4o` | Complex reasoning | High |
| `gpt-4o-mini` | General assistance | Low |
| `gpt-4-turbo` | Balanced performance | Medium |

### Anthropic Models

| Model | Use Case | Cost Tier |
|-------|----------|-----------|
| `claude-3-opus` | Deep analysis | High |
| `claude-3-sonnet` | Code review | Medium |
| `claude-3-haiku` | Quick responses | Low |

### Local Models

| Model | Use Case | Requirements |
|-------|----------|--------------|
| `llama-3` | Privacy-sensitive | GPU |
| `mistral-7b` | Cost optimization | GPU |
| `codellama` | Code generation | GPU |

## AI Router Implementation

### Core Router

```python
# discord_ops_bot/ai_router.py

import os
from typing import Optional

class AIRouter:
    def __init__(self, config):
        self.config = config
        self.providers = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "local": LocalProvider(),
        }
    
    async def route_query(
        self, 
        channel: str, 
        query: str,
        context: Optional[list] = None
    ) -> str:
        model = self._get_model_for_channel(channel)
        
        if model == "none":
            return "AI assistance disabled in this channel."
        
        # Retrieve relevant context from vector store
        if context is None:
            context = await self._retrieve_context(query)
        
        # Route to appropriate provider
        provider = self._get_provider(model)
        return await provider.complete(model, query, context)
```

### Context Retrieval

```python
async def _retrieve_context(self, query: str) -> list:
    """Retrieve relevant documents from vector store."""
    embedding = await self.embed(query)
    
    results = await self.vector_store.search(
        embedding=embedding,
        top_k=5,
        namespaces=["runbooks", "architecture"]
    )
    
    return [doc.content for doc in results]
```

## Discord Integration

### The `/ask` Command

```python
@bot.command(name="ask")
async def ask(ctx, *, query: str):
    """Route a question to the appropriate AI agent."""
    channel_name = ctx.channel.name
    
    # Show typing indicator
    async with ctx.typing():
        response = await ai_router.route_query(channel_name, query)
    
    # Format response with model attribution
    model = ai_router.get_model_for_channel(channel_name)
    await ctx.send(f"🤖 [{model}] {response}")
```

### Streaming Responses

For long responses, use streaming:

```python
async def stream_response(ctx, model: str, query: str):
    """Stream AI response to Discord."""
    message = await ctx.send("🤔 Thinking...")
    
    full_response = ""
    async for chunk in ai_router.stream_query(model, query):
        full_response += chunk
        # Update message every ~500 chars
        if len(full_response) % 500 < len(chunk):
            await message.edit(content=f"🤖 {full_response[:1900]}...")
    
    await message.edit(content=f"🤖 [{model}] {full_response[:1900]}")
```

## Cost Management

### Rate Limiting

```yaml
ai_agents:
  rate_limits:
    max_queries_per_user_per_hour: 50
    max_tokens_per_query: 4096
    cooldown_seconds: 5
```

### Budget Alerts

```python
async def check_budget(user_id: str, estimated_cost: float):
    """Check if query would exceed budget."""
    usage = await get_user_usage(user_id)
    
    if usage.daily_spend + estimated_cost > DAILY_LIMIT:
        raise BudgetExceededError(
            f"Daily AI budget exceeded. Resets at midnight UTC."
        )
```

## LLM Directive: Extending AI Routing

> **AI Agent Note**: When extending the AI routing system:
> 1. Add new models to the provider configuration
> 2. Update channel routing in `discovery.yml`
> 3. Add vector store namespaces for new knowledge domains
> 4. Implement rate limiting for new endpoints
> 5. Document model capabilities and costs

---

*Part of the Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane*
