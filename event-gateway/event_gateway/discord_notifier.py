"""
Discord Notifier Module

Sends messages and embeds to Discord channels.

LLM Directive: When extending notifications:
1. Implement rate limiting to respect Discord API limits
2. Add message queueing for high-volume events
3. Support thread creation for grouped notifications
4. Add retry logic with exponential backoff
"""

import logging
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

# Discord API base URL
DISCORD_API_BASE = "https://discord.com/api/v10"


class DiscordNotifier:
    """
    Handles sending notifications to Discord channels.
    
    LLM Directive: This class manages Discord API interactions.
    Extend it to:
    - Add message editing
    - Support reactions
    - Create threads for grouped events
    - Implement webhooks as alternative to bot token
    """
    
    def __init__(self, token: str, channel_ids: dict[str, str]):
        """
        Initialize Discord notifier.
        
        Args:
            token: Discord bot token
            channel_ids: Mapping of channel names to IDs
        """
        self.token = token
        self.channel_ids = channel_ids
        self._client: Optional[httpx.AsyncClient] = None
    
    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Authorization": f"Bot {self.token}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    def get_channel_id(self, channel: str) -> Optional[str]:
        """Get channel ID from name."""
        # Handle both "#channel" and "channel" formats
        channel = channel.lstrip("#").replace("-", "_")
        return self.channel_ids.get(channel) or self.channel_ids.get(channel.replace("_", "-"))
    
    async def send_message(
        self,
        channel: str,
        content: str,
        tts: bool = False
    ) -> Optional[dict]:
        """
        Send a simple text message to a channel.
        
        Args:
            channel: Channel name or ID
            content: Message content
            tts: Text-to-speech flag
            
        Returns:
            Discord message object or None on failure
        """
        channel_id = self.get_channel_id(channel) or channel
        
        if not channel_id:
            logger.warning("No channel ID for: %s", channel)
            return None
        
        try:
            response = await self.client.post(
                f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
                json={"content": content, "tts": tts}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    "Failed to send message: %d %s", 
                    response.status_code, 
                    response.text
                )
                return None
        except Exception as e:
            logger.error("Error sending message: %s", e)
            return None
    
    async def send_embed(
        self,
        channel: str,
        title: str,
        description: str = "",
        color: int = 0x2f81f7,
        fields: Optional[list[dict]] = None,
        footer: Optional[str] = None,
        thumbnail: Optional[str] = None,
        url: Optional[str] = None
    ) -> Optional[dict]:
        """
        Send an embed message to a channel.
        
        Args:
            channel: Channel name or ID
            title: Embed title
            description: Embed description
            color: Embed color (integer)
            fields: List of field dicts with name, value, inline
            footer: Footer text
            thumbnail: Thumbnail URL
            url: Title URL
            
        Returns:
            Discord message object or None on failure
        """
        channel_id = self.get_channel_id(channel) or channel
        
        if not channel_id:
            logger.warning("No channel ID for: %s", channel)
            return None
        
        embed: dict[str, Any] = {
            "title": title,
            "description": description,
            "color": color,
        }
        
        if fields:
            embed["fields"] = fields
        
        if footer:
            embed["footer"] = {"text": footer}
        
        if thumbnail:
            embed["thumbnail"] = {"url": thumbnail}
        
        if url:
            embed["url"] = url
        
        try:
            response = await self.client.post(
                f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
                json={"embeds": [embed]}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    "Failed to send embed: %d %s", 
                    response.status_code, 
                    response.text
                )
                return None
        except Exception as e:
            logger.error("Error sending embed: %s", e)
            return None


async def send_to_discord(
    channel: str,
    message: str,
    token: Optional[str] = None
) -> bool:
    """
    Convenience function to send a message to Discord.
    
    Args:
        channel: Channel ID
        message: Message content
        token: Discord bot token (uses env if not provided)
        
    Returns:
        True if successful, False otherwise
    """
    import os
    
    token = token or os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("No Discord token available")
        return False
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DISCORD_API_BASE}/channels/{channel}/messages",
                headers={
                    "Authorization": f"Bot {token}",
                    "Content-Type": "application/json",
                },
                json={"content": message},
                timeout=30.0,
            )
            
            return response.status_code == 200
        except Exception as e:
            logger.error("Failed to send to Discord: %s", e)
            return False


async def send_webhook(
    webhook_url: str,
    content: Optional[str] = None,
    embeds: Optional[list[dict]] = None,
    username: Optional[str] = None,
    avatar_url: Optional[str] = None
) -> bool:
    """
    Send a message via Discord webhook.
    
    LLM Directive: Webhooks are simpler than bot tokens
    and don't require Gateway connection. Use for:
    - One-way notifications
    - External service integrations
    - High-volume events
    """
    payload: dict[str, Any] = {}
    
    if content:
        payload["content"] = content
    
    if embeds:
        payload["embeds"] = embeds
    
    if username:
        payload["username"] = username
    
    if avatar_url:
        payload["avatar_url"] = avatar_url
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                webhook_url,
                json=payload,
                timeout=30.0,
            )
            
            return response.status_code in (200, 204)
        except Exception as e:
            logger.error("Failed to send webhook: %s", e)
            return False
