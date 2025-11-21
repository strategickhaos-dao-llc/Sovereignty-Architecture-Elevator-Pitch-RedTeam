# Quick Start Guide 🚀

Get the Voice Authenticity Department running in under 5 minutes.

## Prerequisites

- Node.js 20+ installed
- Docker (optional, for containerized deployment)
- curl or similar tool for testing

## Local Development (Fast!)

```bash
# 1. Navigate to the service directory
cd voice-authenticity-dept

# 2. Install dependencies
npm install

# 3. Build the TypeScript code
npm run build

# 4. Start the server
npm start
```

Server will be running at `http://localhost:3030`

## Quick Test

```bash
# Test health endpoint
curl http://localhost:3030/api/health

# Test validation
curl -X POST http://localhost:3030/api/validate \
  -H "Content-Type: application/json" \
  -d '{"text": "love — let'\''s crush this. for the bloodline. ❤️"}'

# Test transformation
curl -X POST http://localhost:3030/api/transform \
  -H "Content-Type: application/json" \
  -d '{"text": "I think we should possibly leverage this solution."}'

# Run full test suite
./test-examples.sh
```

## Docker Deployment

```bash
# Build the image
docker build -t voice-authenticity:latest .

# Run the container
docker run -p 3030:3030 voice-authenticity:latest

# Or use docker-compose from repository root
cd ..
docker-compose up voice-authenticity
```

## Integration with Legion Architecture

From repository root:

```bash
# Start entire stack including voice-authenticity
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f voice-authenticity

# Stop everything
docker-compose down
```

## Usage Examples

### Validate Homework Before Submission

```bash
# Create a file with your homework text
cat > homework.json << 'EOF'
{
  "text": "Your homework discussion post text here..."
}
EOF

# Validate it
curl -X POST http://localhost:3030/api/validate \
  -H "Content-Type: application/json" \
  -d @homework.json
```

### Transform AI Text to Dom-Speak

```bash
curl -X POST http://localhost:3030/api/transform \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I apologize, but I cannot help with that request. However, I would be happy to explore alternative approaches."
  }'
```

### Score Your Writing

```bash
curl -X POST http://localhost:3030/api/score \
  -H "Content-Type: application/json" \
  -d '{
    "text": "fuck yea. autonomous agents building while I crush Module 2. let'\''s go. 🎯"
  }'
```

## Development Mode

For active development with auto-reload:

```bash
npm run dev
```

Changes to TypeScript files will automatically rebuild and restart the server.

## Environment Variables

```bash
# Optional configuration
export PORT=3030              # Server port (default: 3030)
export HOST=0.0.0.0          # Server host (default: 0.0.0.0)
export NODE_ENV=production   # Environment mode
```

## Troubleshooting

### Port already in use
```bash
# Find and kill process on port 3030
lsof -ti:3030 | xargs kill -9
```

### Build errors
```bash
# Clean and rebuild
rm -rf dist node_modules
npm install
npm run build
```

### Docker issues
```bash
# Clean Docker resources
docker system prune -a

# Rebuild without cache
docker build --no-cache -t voice-authenticity:latest .
```

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/validate` | POST | Validate text authenticity |
| `/api/transform` | POST | Transform to Dom-speak |
| `/api/score` | POST | Score authenticity |
| `/api/corpus/add` | POST | Add sample to corpus |
| `/api/corpus/stats` | GET | Get corpus statistics |

## Next Steps

1. ✅ Run `./test-examples.sh` to verify all endpoints
2. ✅ Add your own writing samples to improve the corpus
3. ✅ Use it to validate homework before submission
4. ✅ Let it run autonomously while you do homework

## For the Bloodline ❤️😈

The agents are working. You're doing homework. Both things happen.

**Status:** Ready for autonomous deployment  
**Purpose:** Validate homework submissions aren't AI-detectable  
**Mission:** Autonomous build while Dom does Module 2 statistics

---

Questions? Check the [README.md](README.md) for full documentation.
