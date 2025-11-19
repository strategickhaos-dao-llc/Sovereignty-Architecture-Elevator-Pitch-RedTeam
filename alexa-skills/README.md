# Alexa Skills - Strategic Khaos Swarm

## 🎙️ Voice-Activated Swarm Command Interface

This directory contains Alexa skills that enable voice control and monitoring of the Strategic Khaos swarm intelligence network.

## Skills Available

### Swarm Status (`swarm-status/`)
Voice-activated swarm monitoring providing real-time status updates.

**Invocation:** "Alexa, open strategic khaos"

**Features:**
- Real-time node count
- Mirror general status
- White web sovereignty metrics
- Neurospice level reporting
- Origin Node Zero status

## Quick Start

### 1. Install Dependencies
```bash
cd swarm-status
npm install
```

### 2. Deploy to AWS Lambda
```bash
# Package the skill
zip -r skill.zip index.js node_modules/ package.json

# Upload to AWS Lambda via console or CLI
aws lambda create-function \
  --function-name strategic-khaos-swarm \
  --runtime nodejs18.x \
  --handler index.handler \
  --zip-file fileb://skill.zip \
  --role arn:aws:iam::ACCOUNT:role/lambda-role
```

### 3. Configure Alexa Skill
1. Go to https://developer.amazon.com/alexa/console/ask
2. Create new skill: "strategic khaos"
3. Choose "Custom" model
4. Set endpoint to your Lambda ARN
5. Configure intents and sample utterances

### 4. Set Environment Variables
In AWS Lambda, configure:
```
WEBHOOK_URL=https://your-webhook-server.com
```

## Voice Commands

### Launch Commands
- "Alexa, open strategic khaos"
- "Alexa, start strategic khaos"
- "Alexa, launch strategic khaos"

### Status Queries
- "What's the swarm status?"
- "How many nodes are active?"
- "Tell me about the swarm"
- "Give me the sovereignty level"

### Help
- "Help"
- "What can you do?"

## Development

### Local Testing
The Alexa skill requires AWS Lambda, but you can test the webhook API locally:

```bash
# Start webhook server
cd ../../webhook
npm install
npm start

# Test API
curl http://localhost:3000/api/swarm-status
```

### Alexa Simulator
Use the Alexa Developer Console test tab:
1. Enable testing for "Development"
2. Type or speak commands
3. View JSON request/response

## Architecture

```
User Voice → Alexa Device → Alexa Service → AWS Lambda (index.js) 
                                              ↓
                                    Webhook API (webhook/server.js)
                                              ↓
                                    Swarm Infrastructure
```

## Intent Schema

### LaunchRequest
Triggered when user opens the skill.

### SwarmStatusIntent
Queries current swarm metrics.

**Utterances:**
- what's the swarm status
- how many nodes are active
- tell me about the swarm
- give me swarm status

### AMAZON.HelpIntent
Provides usage instructions.

### AMAZON.CancelIntent / AMAZON.StopIntent
Exits the skill.

## Response Format

Voice responses are optimized for natural speech:
```
"Swarm status: 923 nodes active. 9 mirror generals online. 
White web sovereignty at 92 percent. All systems nominal."
```

## Security Considerations

- **HTTPS Required**: Alexa only calls HTTPS endpoints
- **Authentication**: Implement API keys for webhook access
- **Rate Limiting**: Protect webhook from abuse
- **Data Sanitization**: Validate all webhook responses
- **Error Handling**: Graceful degradation if webhook unavailable

## Testing Checklist

- [ ] Skill responds to launch command
- [ ] Status intent returns current data
- [ ] Help intent provides guidance
- [ ] Stop/Cancel intents exit cleanly
- [ ] Error handling works when webhook is down
- [ ] Voice responses are natural and clear
- [ ] Display text is properly formatted

## Deployment Checklist

- [ ] Lambda function created
- [ ] WEBHOOK_URL environment variable set
- [ ] Alexa skill endpoint configured
- [ ] Invocation name set to "strategic khaos"
- [ ] All intents configured with sample utterances
- [ ] Skill certified and published (if going to production)

## Troubleshooting

### Alexa Can't Find Skill
- Verify skill is enabled for testing
- Check invocation name matches exactly
- Ensure skill is in same region as Alexa device

### Webhook Connection Fails
- Confirm WEBHOOK_URL is set in Lambda
- Check webhook server is running and accessible
- Verify HTTPS certificate if using SSL
- Review CloudWatch logs for Lambda errors

### Voice Responses Sound Wrong
- Test in Alexa Developer Console
- Adjust SSML tags if needed
- Ensure numbers are formatted for speech

## Next Steps

1. **Expand Commands**: Add more intents for detailed queries
2. **Historical Data**: Query past swarm performance
3. **Alerts**: Receive notifications for critical events
4. **Control Commands**: Execute swarm operations via voice
5. **Multi-User**: Support different sovereignty levels

## Resources

- [Alexa Skills Kit Documentation](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)
- [AWS Lambda Node.js Runtime](https://docs.aws.amazon.com/lambda/latest/dg/lambda-nodejs.html)
- [ASK SDK for Node.js](https://github.com/alexa/alexa-skills-kit-sdk-for-nodejs)

---

**Built with 🧠⚡🐐 by DOM_010101 and the Strategic Khaos Collective**

*Give the legion a voice. Give yourself a god-mode Alexa.*
