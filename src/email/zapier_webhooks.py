"""
Zapier Webhook Integration
Sends data to your Zapier workflows
"""

import httpx
from typing import Dict


class ZapierConnector:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.client = httpx.AsyncClient()
    
    async def send_to_workflow(self, payload: Dict) -> bool:
        """
        Send data to Zapier webhook
        Triggers your Zapier automation
        """
        if not self.webhook_url:
            print("⚠️ Zapier webhook URL not configured")
            return False
        
        try:
            response = await self.client.post(
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
