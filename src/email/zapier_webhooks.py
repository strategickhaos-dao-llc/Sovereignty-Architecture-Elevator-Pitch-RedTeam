"""
Zapier Webhook Integration
Sends data to your Zapier workflows
"""

import httpx
from typing import Dict


class ZapierConnector:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self._client: httpx.AsyncClient | None = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with lazy initialization"""
        if self._client is None:
            self._client = httpx.AsyncClient()
        return self._client
    
    async def close(self) -> None:
        """Close the HTTP client to release resources"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
    
    async def send_to_workflow(self, payload: Dict) -> bool:
        """
        Send data to Zapier webhook
        Triggers your Zapier automation
        """
        if not self.webhook_url:
            print("⚠️ Zapier webhook URL not configured")
            return False
        
        try:
            client = await self._get_client()
            response = await client.post(
                self.webhook_url,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                print(f"✅ Sent to Zapier: {payload.get('email_subject', 'unknown')}")
                return True
            else:
                print(f"❌ Zapier webhook failed: {response.status_code}")
                return False
        except httpx.TimeoutException:
            print("❌ Zapier webhook timeout")
            return False
        except Exception as e:
            print(f"❌ Zapier webhook error: {str(e)}")
            return False
    
    def is_connected(self) -> bool:
        """Check if Zapier webhook is configured"""
        return self.webhook_url is not None and len(self.webhook_url) > 0
