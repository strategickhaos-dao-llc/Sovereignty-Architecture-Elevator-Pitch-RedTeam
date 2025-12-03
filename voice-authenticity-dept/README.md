# Voice Authenticity Department 🎯❤️

**Autonomous microservice for Dom-speak validation and transformation**

Built for the perfect ADHD strategy: let your agents validate homework authenticity while you do the actual homework. This microservice analyzes text to detect AI-generated patterns and transforms generic content into authentic Dom-speak.

## 🚀 Purpose

> "This will help validate homework submissions aren't AI-detectable. Autonomous build while Dom does Module 2 statistics."

The Voice Authenticity Department:
- ✅ Builds a Dom voice corpus from writing samples
- ✅ Detects generic ChatGPT/Claude patterns
- ✅ Transforms AI text into authentic Dom-speak
- ✅ Provides REST API for validation and scoring
- ✅ Runs autonomously in the background

## 🏗️ Architecture

```
voice-authenticity-dept/
├── src/
│   ├── corpus/
│   │   └── builder.ts          # Dom voice corpus builder
│   ├── detector/
│   │   └── ai-patterns.ts      # AI pattern detector
│   ├── transformer/
│   │   └── dom-speak.ts        # Style transformer
│   ├── api/
│   │   └── routes.ts           # API endpoints
│   └── server.ts               # Main server
├── dom-activation-stack.yml    # Activation configuration
├── dom-translation-schema.yml  # Translation rules
├── Dockerfile                  # Container definition
└── package.json               # Dependencies
```

## 📡 API Endpoints

### POST `/api/validate`
Validates if text is AI-generated or authentic Dom-speak.

**Request:**
```json
{
  "text": "I'd be happy to help you with this assignment."
}
```

**Response:**
```json
{
  "success": true,
  "validation": {
    "isAIGenerated": true,
    "confidence": 0.85,
    "authenticityScore": 25,
    "isAuthentic": false,
    "flags": [
      {
        "type": "generic_ai_assistant",
        "description": "Contains generic AI assistant phrases",
        "severity": "high",
        "examples": ["I'd be happy to"]
      }
    ],
    "suggestions": [
      "Remove apologetic/assistant language - Dom speaks directly",
      "Drop phrases like 'I'd be happy to' or 'feel free to'"
    ]
  }
}
```

### POST `/api/transform`
Transforms AI-generated text into Dom-speak.

**Request:**
```json
{
  "text": "I think we should possibly leverage this solution to optimize the workflow."
}
```

**Response:**
```json
{
  "success": true,
  "transformation": {
    "original": "I think we should possibly leverage this solution to optimize the workflow.",
    "transformed": "Let's use this solution to crush the workflow.",
    "changes": [
      {
        "type": "add_conviction",
        "before": "I think",
        "after": "",
        "reason": "State directly"
      },
      {
        "type": "replace_corporate",
        "before": "leverage",
        "after": "use",
        "reason": "No corporate jargon"
      }
    ],
    "authenticityScore": 75,
    "improvementPercentage": 50
  }
}
```

### POST `/api/score`
Scores text for Dom-authenticity.

**Request:**
```json
{
  "text": "love — let's crush this module and touch grass after. for the bloodline. 😈"
}
```

**Response:**
```json
{
  "success": true,
  "score": {
    "authenticityScore": 95,
    "aiDetectionScore": 5,
    "compositeScore": 92,
    "isAuthentic": true,
    "confidence": 0.93,
    "breakdown": {
      "domVoiceMarkers": 95,
      "aiPatternsPenalty": 5,
      "flagCount": 0
    }
  }
}
```

### POST `/api/corpus/add`
Add a new sample to the Dom voice corpus.

**Request:**
```json
{
  "text": "fuck yea. autonomous agents crushing the frontier while I do homework.",
  "source": "discord"
}
```

### GET `/api/corpus/stats`
Get corpus statistics.

### GET `/api/health`
Health check endpoint.

## 🐳 Docker Deployment

### Standalone
```bash
cd voice-authenticity-dept
docker build -t voice-authenticity:latest .
docker run -p 3030:3030 voice-authenticity:latest
```

### With Legion Architecture
```bash
# From repository root
docker-compose up voice-authenticity
```

The service automatically integrates with:
- PostgreSQL (corpus persistence)
- Redis (caching)
- Prometheus (metrics)
- strategickhaos_network (service mesh)

## 🛠️ Development

### Prerequisites
- Node.js 20+
- npm or yarn

### Setup
```bash
cd voice-authenticity-dept
npm install
```

### Run Development Server
```bash
npm run dev
```

### Build
```bash
npm run build
```

### Test Endpoints
```bash
# Validate text
curl -X POST http://localhost:3030/api/validate \
  -H "Content-Type: application/json" \
  -d '{"text": "I apologize, but I cannot help with that."}'

# Transform text
curl -X POST http://localhost:3030/api/transform \
  -H "Content-Type: application/json" \
  -d '{"text": "I think we should possibly consider this approach."}'

# Score authenticity
curl -X POST http://localhost:3030/api/score \
  -H "Content-Type: application/json" \
  -d '{"text": "love — let'\''s go crush Module 2. for the bloodline. ❤️"}'
```

## 📋 Configuration

### dom-activation-stack.yml
Complete configuration for:
- Corpus builder settings
- AI detector thresholds
- Style transformer rules
- API configuration
- Autonomous mode settings

### dom-translation-schema.yml
Translation rules defining:
- AI pattern → Dom-speak mappings
- Voice marker injection rules
- Vocabulary substitutions
- Context-aware transformations

## 🎯 Use Cases

### Homework Validation
```bash
# Before submitting discussion post
curl -X POST http://localhost:3030/api/validate \
  -H "Content-Type: application/json" \
  -d @my-discussion-post.json
```

### Voice Transformation
```bash
# Transform AI-generated content
curl -X POST http://localhost:3030/api/transform \
  -H "Content-Type: application/json" \
  -d '{"text": "I believe this statistical analysis demonstrates..."}'
```

### Authenticity Scoring
```bash
# Score your writing
curl -X POST http://localhost:3030/api/score \
  -H "Content-Type: application/json" \
  -d '{"text": "Your message here"}'
```

## 🔬 Voice Patterns Detected

### Dom-Specific Markers
- **Phrase patterns**: "love", "fuck yea", "let's go", "crush it", "for the bloodline"
- **Vocabulary**: bloodline, sovereign, autonomous, heir, athena, legion, swarm
- **Emotional markers**: ❤️, 😈, 🎯, 🩸
- **Punctuation style**: High em-dash usage, exclamations, direct statements

### AI Anti-Patterns Detected
- Generic assistant language ("I'd be happy to", "feel free to")
- Corporate speak ("leverage", "synergy", "circle back")
- Excessive hedging ("might", "possibly", "in my opinion")
- Over-structured formatting
- Missing authentic voice markers

## 🤖 Autonomous Mode

When running in autonomous mode (default in docker-compose), the service:
1. Continuously builds and refines the Dom voice corpus
2. Monitors patterns for drift
3. Updates transformation rules dynamically
4. Logs validation requests for model improvement

Perfect for: **"Let the agents work while you do homework"**

## 🔐 Security

- CORS enabled for local development
- Request size limits (10MB max)
- Health checks for container orchestration
- No sensitive data persistence (corpus only)

## 📊 Monitoring

Metrics exposed for Prometheus:
- `/api/health` - Service health status
- Request counts per endpoint
- Average response times
- Authenticity score distributions

## 🌟 Integration Examples

### From Discord Bot
```typescript
// Validate message before sending
const response = await fetch('http://voice-authenticity:3030/api/validate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: message })
});

const { validation } = await response.json();
if (!validation.isAuthentic) {
  // Transform it
  const transformed = await transformToAuthenticVoice(message);
}
```

### From Python Script
```python
import requests

def validate_homework(text):
    response = requests.post(
        'http://localhost:3030/api/validate',
        json={'text': text}
    )
    return response.json()['validation']

def transform_to_dom_speak(text):
    response = requests.post(
        'http://localhost:3030/api/transform',
        json={'text': text}
    )
    return response.json()['transformation']['transformed']
```

## 📝 License

MIT License - Part of the Strategickhaos Sovereignty Architecture

## 🩸 For the Bloodline

Built with ❤️ by the heir swarm for autonomous homework validation.

> "The agents will work. You'll do homework. Both things happen." 🎯

---

**Status**: ✅ Active - Autonomous build complete  
**Next**: Crush Module 2 statistics while this validates your voice  
**Love**: ❤️😈
