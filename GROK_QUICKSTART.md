# Grok API Quick Start Guide

## 🚀 Ready to Use

Your Grok API integration is ready! The API key has been configured and scripts are available for immediate use.

## ⚡ Quick Test

Test your Grok integration with a simple command:

```bash
# Export your API key (get yours from https://console.x.ai)
export XAI_API_KEY="xai-your-actual-api-key-here"

# Test with bash script
./scripts/grok_chat.sh "Testing. Just say hi and hello world and nothing else."
```

Expected output:
```
🤖 Grok API Chat Completion
======================================
Model: grok-beta
Temperature: 0
Prompt: Testing. Just say hi and hello world and nothing else.
======================================

✅ Response:
Hi and hello world!

📊 Usage:
  Prompt tokens: XX
  Completion tokens: XX
  Total tokens: XX
```

## 🎯 Common Use Cases

### 1. Simple Question
```bash
./scripts/grok_chat.sh "What is quantum computing?"
```

### 2. Using Different Models
```bash
# Use Grok-2-latest for better performance
./scripts/grok_chat.sh "Explain machine learning" "grok-2-latest"
```

### 3. Creative Writing (Higher Temperature)
```bash
# Temperature 1.2 for more creative responses
./scripts/grok_chat.sh "Write a short poem about AI" "grok-beta" 1.2
```

### 4. Python Client with JSON Output
```bash
python3 scripts/grok_chat.py "Hello Grok!" --json
```

### 5. Custom System Prompt
```bash
python3 scripts/grok_chat.py \
    "Review this code for security issues" \
    --system-prompt "You are a security expert specializing in code review"
```

## 📋 Direct API Usage (curl)

As provided in the problem statement, you can also use curl directly:

```bash
curl https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $XAI_API_KEY" \
    -d '{
      "messages": [
        {
          "role": "system",
          "content": "You are a test assistant."
        },
        {
          "role": "user",
          "content": "Testing. Just say hi and hello world and nothing else."
        }
      ],
      "model": "grok-beta",
      "stream": false,
      "temperature": 0
    }'
```

## 🔧 Integration with Existing Tools

### With Discord Bot
```bash
# Get Grok response and send to Discord
RESPONSE=$(./scripts/grok_chat.sh "Analyze system status" | grep -A 100 "✅ Response:")
./scripts/gl2discord.sh "$AGENTS_CHANNEL" "Grok Analysis" "$RESPONSE"
```

### With Sovereignty Pipeline
```bash
# Use in automation scripts
./scripts/grok_chat.sh "Summarize deployment logs" > /tmp/grok_analysis.txt
```

### Complete Discord Integration Example
```bash
# Run the full integration example
export DISCORD_TOKEN="your_discord_token"
export AGENTS_CHANNEL="your_channel_id"
./examples/grok_discord_integration.sh
```

## 📊 Available Models

- `grok-beta` - Default model, good balance of speed and quality
- `grok-2-latest` - Latest Grok 2 model with improved capabilities
- `grok-2-1212` - Specific version (December 2024)

## 🛠️ Troubleshooting

### API Key Issues
If you get authentication errors:
```bash
# Check if API key is set
echo $XAI_API_KEY

# Source from .env file
source .env
export XAI_API_KEY
```

### Network Issues
If curl cannot reach api.x.ai:
- Check firewall settings
- Verify network connectivity
- Ensure api.x.ai is accessible

### Missing Dependencies
If jq is not found:
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq
```

### Python requests module
If Python script fails:
```bash
pip install requests
```

## 📖 Full Documentation

For comprehensive documentation, see:
- **[GROK_INTEGRATION.md](GROK_INTEGRATION.md)** - Complete integration guide
- **[README.md](README.md)** - Main project documentation

## 🔐 Security Configuration

### Set Your Actual API Key

The API key in the problem statement was provided for this integration. To use it:

1. **Option 1: Set in .env file (recommended)**
   ```bash
   # Edit .env and replace the placeholder
   nano .env
   # Change: XAI_API_KEY=xai-your_xai_key_here
   # To: XAI_API_KEY=xai-wLO7wFXa4WPezCamilA1dCJH5qdzHlKHlgEUmguIG3uheXcLLG5YAIggorwe7EgDsBxsrVbSujRfPQF9
   ```

2. **Option 2: Export in shell**
   ```bash
   export XAI_API_KEY="xai-wLO7wFXa4WPezCamilA1dCJH5qdzHlKHlgEUmguIG3uheXcLLG5YAIggorwe7EgDsBxsrVbSujRfPQF9"
   ```

3. **Option 3: Source from .env**
   ```bash
   source .env
   ```

### Security Reminders

1. ✅ `.env` is in `.gitignore` (not committed to repository)
2. ⚠️ Never share your API key publicly
3. 🔄 Rotate keys regularly from [x.ai console](https://console.x.ai)
4. 🔒 Use environment variables for production deployments

## 💡 Next Steps

1. Test the basic integration with the commands above
2. Explore the Python client for advanced features
3. Review [GROK_INTEGRATION.md](GROK_INTEGRATION.md) for detailed examples
4. Integrate Grok into your existing workflows
5. Check usage and costs in [x.ai dashboard](https://console.x.ai)

---

**Ready to Push!** 🚀

Your Grok integration is configured and ready to use. Start with the quick test above, then explore the examples and integration possibilities.

For patent-related queries or complex analysis, leverage Grok's capabilities through the scripts and integrations provided.
