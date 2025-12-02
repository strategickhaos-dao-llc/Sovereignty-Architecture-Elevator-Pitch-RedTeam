"""
AI Router Module

Routes AI queries to appropriate models based on channel configuration.

LLM Directive: When extending AI routing:
1. Add new model providers in the providers dict
2. Update channel routing in discovery.yml
3. Add vector store namespaces for new knowledge domains
4. Implement rate limiting for cost control
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Default model configuration
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_PROVIDER = "openai"

# Per-channel model routing (loaded from discovery.yml in production)
CHANNEL_ROUTING: dict[str, str] = {
    "#agents": "gpt-4o-mini",
    "#inference-stream": "none",
    "#prs": "claude-3-sonnet",
    "#alerts": "gpt-4o-mini",
    "#deployments": "gpt-4o-mini",
}


class AIRouter:
    """
    Routes AI queries to appropriate models based on channel context.
    
    LLM Directive: Extend this class to:
    - Add new model providers (Azure, local models, etc.)
    - Implement vector store context retrieval
    - Add streaming support for long responses
    - Implement token counting and budget management
    """
    
    def __init__(self):
        self.channel_routing = CHANNEL_ROUTING.copy()
        self.default_model = DEFAULT_MODEL
        self._openai_client = None
        self._anthropic_client = None
    
    @property
    def openai_client(self):
        """Lazy initialization of OpenAI client."""
        if self._openai_client is None:
            try:
                import openai
                self._openai_client = openai.AsyncOpenAI(
                    api_key=os.getenv("OPENAI_API_KEY")
                )
            except ImportError:
                logger.warning("OpenAI package not installed")
        return self._openai_client
    
    @property
    def anthropic_client(self):
        """Lazy initialization of Anthropic client."""
        if self._anthropic_client is None:
            try:
                import anthropic
                self._anthropic_client = anthropic.AsyncAnthropic(
                    api_key=os.getenv("ANTHROPIC_API_KEY")
                )
            except ImportError:
                logger.warning("Anthropic package not installed")
        return self._anthropic_client
    
    def get_model_for_channel(self, channel_name: str) -> str:
        """
        Get the configured model for a channel.
        
        Args:
            channel_name: Name of the Discord channel
            
        Returns:
            Model name or "none" if AI is disabled
        """
        # Normalize channel name (add # if missing)
        if not channel_name.startswith("#"):
            channel_name = f"#{channel_name}"
        
        return self.channel_routing.get(channel_name, self.default_model)
    
    def get_provider_for_model(self, model: str) -> str:
        """Determine the provider for a given model."""
        if model.startswith("gpt-") or model.startswith("o1"):
            return "openai"
        elif model.startswith("claude-"):
            return "anthropic"
        elif model in ("llama", "mistral", "codellama"):
            return "local"
        else:
            return "openai"  # Default to OpenAI
    
    async def query(
        self, 
        model: str, 
        query: str, 
        context: Optional[list[str]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Query an AI model.
        
        Args:
            model: Model identifier
            query: User query
            context: Optional context documents
            system_prompt: Optional system prompt override
            
        Returns:
            Model response text
            
        LLM Directive: Extend this to:
        - Add vector store context retrieval
        - Implement conversation history
        - Add function calling support
        """
        if model == "none":
            return "AI assistance is disabled in this channel."
        
        provider = self.get_provider_for_model(model)
        
        # Build messages
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system", 
                "content": "You are a helpful DevOps assistant for the Strategickhaos infrastructure."
            })
        
        # Add context if provided
        if context:
            context_text = "\n\n".join(context)
            messages.append({
                "role": "system",
                "content": f"Relevant context:\n{context_text}"
            })
        
        messages.append({"role": "user", "content": query})
        
        # Route to appropriate provider
        try:
            if provider == "openai":
                return await self._query_openai(model, messages)
            elif provider == "anthropic":
                return await self._query_anthropic(model, messages)
            else:
                return f"Unknown provider: {provider}"
        except Exception as e:
            logger.error("AI query failed: %s", e)
            return f"AI query failed: {e}"
    
    async def _query_openai(self, model: str, messages: list[dict]) -> str:
        """Query OpenAI API."""
        if not self.openai_client:
            return "OpenAI client not configured. Set OPENAI_API_KEY environment variable."
        
        # TODO: Implement actual OpenAI API call
        # response = await self.openai_client.chat.completions.create(
        #     model=model,
        #     messages=messages,
        #     max_tokens=1024
        # )
        # return response.choices[0].message.content
        
        return f"[{model}] OpenAI query stub - implement real API call"
    
    async def _query_anthropic(self, model: str, messages: list[dict]) -> str:
        """Query Anthropic API."""
        if not self.anthropic_client:
            return "Anthropic client not configured. Set ANTHROPIC_API_KEY environment variable."
        
        # TODO: Implement actual Anthropic API call
        # Convert messages format for Anthropic
        # response = await self.anthropic_client.messages.create(
        #     model=model,
        #     max_tokens=1024,
        #     messages=[m for m in messages if m["role"] != "system"],
        #     system=next((m["content"] for m in messages if m["role"] == "system"), "")
        # )
        # return response.content[0].text
        
        return f"[{model}] Anthropic query stub - implement real API call"
    
    async def retrieve_context(self, query: str, namespaces: Optional[list[str]] = None) -> list[str]:
        """
        Retrieve relevant context from vector store.
        
        LLM Directive: Implement this to:
        - Connect to pgvector/Qdrant/Weaviate
        - Embed the query
        - Search for relevant documents
        - Return top-k results
        """
        # TODO: Implement vector store context retrieval
        # embedding = await self.embed(query)
        # results = await self.vector_store.search(embedding, top_k=5, namespaces=namespaces)
        # return [doc.content for doc in results]
        
        return []  # Stub: no context retrieval yet


# Global AI router instance
_ai_router: Optional[AIRouter] = None


def get_ai_router() -> AIRouter:
    """Get or create the global AI router."""
    global _ai_router
    if _ai_router is None:
        _ai_router = AIRouter()
    return _ai_router


async def route_ai_query(channel_name: str, query: str) -> str:
    """
    Convenience function to route an AI query.
    
    Args:
        channel_name: Discord channel name
        query: User query
        
    Returns:
        AI response
    """
    router = get_ai_router()
    model = router.get_model_for_channel(channel_name)
    
    # Retrieve context if available
    context = await router.retrieve_context(query)
    
    return await router.query(model, query, context)
