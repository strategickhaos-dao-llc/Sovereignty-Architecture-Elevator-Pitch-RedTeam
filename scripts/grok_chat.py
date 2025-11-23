#!/usr/bin/env python3
"""
Grok (x.ai) API Chat Completion Client
Usage: python grok_chat.py "Your prompt here"
Requires: XAI_API_KEY environment variable
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Optional

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


class GrokClient:
    """Client for interacting with the Grok (x.ai) API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('XAI_API_KEY')
        if not self.api_key:
            raise ValueError("XAI_API_KEY environment variable or api_key parameter required")
        
        self.base_url = "https://api.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-beta",
        temperature: float = 0.0,
        stream: bool = False,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        Send a chat completion request to Grok API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (default: grok-beta)
            temperature: Sampling temperature 0-2
            stream: Enable streaming responses
            max_tokens: Maximum tokens in response
            
        Returns:
            API response as dict
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def simple_chat(self, prompt: str, model: str = "grok-beta", temperature: float = 0.0) -> str:
        """
        Simple chat interface - returns just the response text
        
        Args:
            prompt: User prompt
            model: Model name
            temperature: Sampling temperature
            
        Returns:
            Assistant's response text
        """
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant for the Sovereignty Architecture project."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat_completion(messages, model=model, temperature=temperature)
        
        if "error" in response:
            return f"Error: {response['error']}"
        
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError):
            return f"Unexpected response format: {json.dumps(response)}"


def main():
    parser = argparse.ArgumentParser(
        description="Grok (x.ai) Chat Completion Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python grok_chat.py "What is sovereignty architecture?"
  python grok_chat.py "Explain quantum computing" --model grok-2-latest
  python grok_chat.py "Tell me a story" --temperature 1.2
  python grok_chat.py "Hello" --json
        """
    )
    
    parser.add_argument(
        "prompt",
        help="The prompt to send to Grok"
    )
    parser.add_argument(
        "--model",
        default="grok-beta",
        help="Model to use (default: grok-beta)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature 0-2 (default: 0.0)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maximum tokens in response"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output full JSON response"
    )
    parser.add_argument(
        "--system-prompt",
        help="Custom system prompt"
    )
    
    args = parser.parse_args()
    
    try:
        client = GrokClient()
        
        # Build messages
        messages = []
        if args.system_prompt:
            messages.append({"role": "system", "content": args.system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": "You are a helpful AI assistant for the Sovereignty Architecture project."
            })
        
        messages.append({"role": "user", "content": args.prompt})
        
        # Make request
        print("🤖 Grok API Chat Completion")
        print("=" * 50)
        print(f"Model: {args.model}")
        print(f"Temperature: {args.temperature}")
        print(f"Prompt: {args.prompt}")
        print("=" * 50)
        print()
        
        response = client.chat_completion(
            messages=messages,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        
        if args.json:
            print(json.dumps(response, indent=2))
        else:
            if "error" in response:
                print(f"❌ Error: {response['error']}")
                sys.exit(1)
            
            try:
                content = response['choices'][0]['message']['content']
                print("✅ Response:")
                print(content)
                print()
                
                if "usage" in response:
                    usage = response['usage']
                    print("📊 Usage:")
                    print(f"  Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"  Completion tokens: {usage.get('completion_tokens', 'N/A')}")
                    print(f"  Total tokens: {usage.get('total_tokens', 'N/A')}")
            except (KeyError, IndexError) as e:
                print(f"⚠️  Unexpected response format: {e}")
                print(json.dumps(response, indent=2))
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure to set XAI_API_KEY environment variable:")
        print("  export XAI_API_KEY='xai-your-key-here'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
