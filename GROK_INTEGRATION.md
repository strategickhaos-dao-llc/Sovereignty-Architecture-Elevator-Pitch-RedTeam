# Grok (x.ai) API Integration

This document describes how to use the Grok API integration for chat completions with the Sovereignty Architecture project.

## Overview

The Grok API (x.ai) provides access to powerful language models. This integration allows you to:
- Send chat completion requests to Grok models
- Configure system prompts and user messages
- Adjust model parameters like temperature
- Track token usage

## Setup

### 1. Get Your API Key

1. Visit [x.ai Console](https://console.x.ai)
2. Create an account or sign in
3. Generate an API key
4. Copy the API key (it starts with `xai-`)

### 2. Configure Environment

Add your API key to the `.env` file:

```bash
XAI_API_KEY=xai-your_actual_api_key_here
```

Or export it in your shell:

```bash
export XAI_API_KEY="xai-your_actual_api_key_here"
```

## Usage

### Basic Chat Completion

Use the provided script to send a chat completion request:

```bash
./scripts/grok_chat.sh "What is the capital of France?"
```

### Custom Parameters

The script accepts optional parameters:

```bash
./scripts/grok_chat.sh "Your prompt" [model] [temperature] [stream]
```

**Parameters:**
- `prompt` (required): The user message to send
- `model` (optional): Model name (default: `grok-beta`)
- `temperature` (optional): Sampling temperature 0-2 (default: `0`)
- `stream` (optional): Enable streaming (default: `false`)

**Examples:**

```bash
# Use grok-2-latest model with temperature 0.7
./scripts/grok_chat.sh "Write a haiku about sovereignty" "grok-2-latest" 0.7

# Use grok-2-latest model
./scripts/grok_chat.sh "Explain quantum computing" "grok-2-latest"

# High creativity (temperature 1.5)
./scripts/grok_chat.sh "Tell me a story" "grok-beta" 1.5
```

## Available Models

Based on the x.ai documentation:
- `grok-beta` - Latest beta model
- `grok-2-latest` - Latest Grok 2 model
- `grok-2-1212` - Specific Grok 2 version (Dec 2024)

## Direct API Usage

### Using curl

```bash
curl https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $XAI_API_KEY" \
    -d '{
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful AI assistant for the Sovereignty Architecture project."
        },
        {
          "role": "user",
          "content": "Your question here"
        }
      ],
      "model": "grok-beta",
      "stream": false,
      "temperature": 0
    }'
```

### Response Format

Successful responses return JSON with this structure:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "grok-beta",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The response text..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 50,
    "total_tokens": 75
  }
}
```

## Integration with Other Tools

### Discord Integration

Send Grok responses to Discord:

```bash
# Get response from Grok
GROK_RESPONSE=$(./scripts/grok_chat.sh "Summarize today's deployment" | grep -A 100 "✅ Response:" | tail -n +2)

# Send to Discord
./scripts/gl2discord.sh "$AGENTS_CHANNEL" "Grok Analysis" "$GROK_RESPONSE"
```

### Pipeline Example

Create a pipeline that uses Grok for analysis:

```bash
#!/usr/bin/env bash
# analyze_logs.sh - Analyze logs with Grok

LOG_SUMMARY=$(tail -100 /var/log/app.log | grep ERROR)
ANALYSIS=$(./scripts/grok_chat.sh "Analyze these errors and suggest fixes: $LOG_SUMMARY")

echo "$ANALYSIS" > /tmp/grok_analysis.txt
```

## Advanced Usage

### Multi-turn Conversations

For multi-turn conversations, you'll need to maintain message history. Here's a Python example:

```python
import requests
import os

API_KEY = os.getenv('XAI_API_KEY')
API_URL = 'https://api.x.ai/v1/chat/completions'

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is sovereignty architecture?"}
]

response = requests.post(
    API_URL,
    headers={
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'grok-beta',
        'messages': messages,
        'temperature': 0
    }
)

# Add assistant's response to history
messages.append({
    "role": "assistant",
    "content": response.json()['choices'][0]['message']['content']
})

# Continue conversation
messages.append({
    "role": "user",
    "content": "Tell me more about that"
})
```

### Streaming Responses

For streaming responses (work in progress):

```bash
curl https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $XAI_API_KEY" \
    -d '{
      "messages": [
        {"role": "user", "content": "Write a long story"}
      ],
      "model": "grok-beta",
      "stream": true,
      "temperature": 0.7
    }'
```

## Error Handling

Common errors and solutions:

### Authentication Error
```json
{"error": {"message": "Invalid API key", "type": "invalid_request_error"}}
```
**Solution:** Check your API key in `.env` or environment variables.

### Rate Limit Error
```json
{"error": {"message": "Rate limit exceeded", "type": "rate_limit_error"}}
```
**Solution:** Wait and retry, or implement exponential backoff.

### Model Not Found
```json
{"error": {"message": "Model not found", "type": "invalid_request_error"}}
```
**Solution:** Use a valid model name like `grok-beta` or `grok-2-latest`.

## Security Best Practices

1. **Never commit API keys** - Always use environment variables
2. **Use .gitignore** - Ensure `.env` is in `.gitignore`
3. **Rotate keys** - Regularly rotate your API keys
4. **Monitor usage** - Track API usage in the x.ai console
5. **Limit access** - Only give API keys to necessary systems

## Cost Management

- Monitor token usage in responses
- Use lower temperatures for deterministic outputs (reduces retries)
- Cache common responses when appropriate
- Set reasonable max_tokens limits

## Troubleshooting

### Script won't run
```bash
# Make sure script is executable
chmod +x ./scripts/grok_chat.sh

# Check if jq is installed
which jq || sudo apt-get install jq
```

### No response
```bash
# Test API connectivity
curl -I https://api.x.ai/v1/models \
    -H "Authorization: Bearer $XAI_API_KEY"
```

### Invalid JSON
```bash
# Check if jq is working
echo '{"test": "value"}' | jq .
```

## Integration with Existing Systems

### With AI Constitution
The Grok integration respects the AI constitution defined in `ai_constitution.yaml`:

```yaml
# Example: Use Grok for safety checks
safety_check:
  provider: "grok"
  model: "grok-beta"
  temperature: 0
  system_prompt: "You are a safety validator..."
```

### With Recon System
Add Grok to the LLM recon pipeline in `llm_recon_v1.yaml`:

```yaml
grok_analysis:
  enabled: true
  model: "grok-beta"
  use_cases:
    - "paper_summarization"
    - "concept_extraction"
    - "cross_reference_validation"
```

## References

- [x.ai API Documentation](https://docs.x.ai)
- [x.ai Console](https://console.x.ai)
- [Sovereignty Architecture README](README.md)
- [AI Constitution](ai_constitution.yaml)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review [x.ai documentation](https://docs.x.ai)
3. Open an issue in the repository
4. Ask in the `#agents` Discord channel

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*Empowering sovereign AI operations with Grok integration*
