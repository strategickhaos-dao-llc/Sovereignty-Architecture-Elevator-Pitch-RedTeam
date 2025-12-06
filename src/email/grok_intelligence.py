"""
Grok API Integration for Email Intelligence
Uses xAI's Grok to analyze emails
"""

import json
import httpx
from typing import Dict


class GrokEmailProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
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
    
    async def analyze_email(
        self, 
        subject: str, 
        body: str, 
        sender: str
    ) -> Dict:
        """
        Send email to Grok for AI analysis
        Returns intelligence summary
        """
        
        prompt = f"""
Analyze this email for StrategicKhaos DAO's sovereign operations:

From: {sender}
Subject: {subject}
Body: {body}

Provide:
1. Category (academic/business/personal/spam)
2. Priority (high/medium/low)
3. Summary (2 sentences max)
4. Action required (yes/no)
5. Requires approval (true/false)

Respond in JSON format.
        """
        
        try:
            client = await self._get_client()
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an email intelligence analyst for a sovereign DAO."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result["choices"][0]["message"]["content"]
                
                # Parse JSON from Grok's response
                try:
                    analysis = json.loads(analysis_text)
                except json.JSONDecodeError:
                    # Fallback if not valid JSON
                    analysis = {
                        "category": "unknown",
                        "priority": "medium",
                        "summary": analysis_text[:200],
                        "action_required": False,
                        "requires_approval": True
                    }
                
                return analysis
            else:
                return {
                    "error": "Grok API failed",
                    "status_code": response.status_code
                }
        except httpx.TimeoutException:
            return {
                "error": "Grok API timeout",
                "status_code": 504
            }
        except Exception as e:
            return {
                "error": f"Grok API error: {str(e)}",
                "status_code": 500
            }
    
    def is_connected(self) -> bool:
        """Check if Grok API is accessible"""
        return self.api_key is not None and len(self.api_key) > 0
