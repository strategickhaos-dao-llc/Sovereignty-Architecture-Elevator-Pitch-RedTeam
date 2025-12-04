"""
SendGrid Integration for Outbound Email
"""

from typing import Optional
import httpx


class SendGridClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sendgrid.com/v3"
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
    
    async def send_email(self, email) -> Optional[str]:
        """Send email via SendGrid API"""
        
        if not self.api_key:
            print("⚠️ SendGrid API key not configured")
            return None
        
        payload = {
            "personalizations": [
                {
                    "to": [{"email": email.to}],
                    "subject": email.subject
                }
            ],
            "from": {"email": email.from_address},
            "content": [
                {
                    "type": "text/html",
                    "value": email.body
                }
            ]
        }
        
        try:
            client = await self._get_client()
            response = await client.post(
                f"{self.base_url}/mail/send",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30.0
            )
            
            if response.status_code in (200, 202):
                message_id = response.headers.get('X-Message-Id', 'unknown')
                print(f"📤 Email sent: {response.status_code}")
                return message_id
            else:
                print(f"❌ SendGrid error: {response.status_code}")
                return None
        except httpx.TimeoutException:
            print("❌ SendGrid timeout")
            return None
        except Exception as e:
            print(f"❌ SendGrid error: {str(e)}")
            return None
    
    def is_connected(self) -> bool:
        """Check if SendGrid is configured"""
        return self.api_key is not None and len(self.api_key) > 0
