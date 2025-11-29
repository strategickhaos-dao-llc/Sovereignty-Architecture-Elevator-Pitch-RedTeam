# Strategickhaos Webhook Inbox Service

A containerized Flask webhook listener for GitHub events with persistent storage. This service acts as an autonomous "inbox" that receives GitHub webhook events, validates them cryptographically, and stores them for processing.

## 🎯 Features

- **HMAC Signature Verification**: Cryptographically secure webhook validation using SHA-256
- **Persistent Storage**: Docker volume-mounted inbox for event persistence across container restarts
- **Event Logging**: All events stored as JSON lines with timestamps
- **Health Checks**: Built-in health monitoring endpoint
- **Isolated Execution**: Runs in Docker container, independent of host system
- **Auto-restart**: Container automatically restarts on failure

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed
- Python 3.12+ (for local development)

### 1. Generate Webhook Secret
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Save this secret - you'll need it for both the container and GitHub webhook configuration.

### 2. Build and Run with Docker Compose (Recommended)

```bash
cd webhook-inbox

# Set your webhook secret
export GITHUB_WEBHOOK_SECRET="your-generated-secret-here"

# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### 3. Manual Docker Commands

```bash
# Build the image
docker build -t strategickhaos-inbox .

# Create a volume for persistent storage
docker volume create strategickhaos-inbox-vol

# Run the container
docker run -d \
  --name strategickhaos-listener \
  -p 5000:5000 \
  -v strategickhaos-inbox-vol:/inbox \
  -e GITHUB_WEBHOOK_SECRET="your-secret-here" \
  strategickhaos-inbox

# Check logs
docker logs -f strategickhaos-listener

# Stop and remove
docker stop strategickhaos-listener
docker rm strategickhaos-listener
```

## 🔧 Configuration

### Environment Variables

- `GITHUB_WEBHOOK_SECRET`: Required. The secret used to verify webhook signatures from GitHub.
- `FLASK_ENV`: Optional. Set to `production` (default) or `development`.

### Ports

- `5000`: HTTP port for webhook receiver

### Volumes

- `/inbox`: Directory containing event logs (mount as Docker volume for persistence)

## 🌐 Endpoints

### POST /github-webhook
Primary webhook endpoint for GitHub events.

**Headers:**
- `X-Hub-Signature-256`: HMAC signature for validation
- `X-GitHub-Event`: Event type (push, pull_request, etc.)

**Response:** 204 No Content on success, 403 Forbidden on signature failure

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "strategickhaos-webhook-inbox"
}
```

### GET /
Service information endpoint.

**Response:**
```json
{
  "service": "Strategickhaos Webhook Inbox",
  "endpoints": {
    "/github-webhook": "POST - GitHub webhook receiver",
    "/health": "GET - Health check",
    "/": "GET - This info"
  }
}
```

## 🔗 GitHub Webhook Setup

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL**: `http://your-server:5000/github-webhook` (use ngrok for local testing)
   - **Content type**: `application/json`
   - **Secret**: Your generated webhook secret
   - **Events**: Select events to receive (push, pull_request, issues, etc.)
4. Click **Add webhook**

### Testing with ngrok

For local development, use ngrok to expose your local service:

```bash
# Start the webhook service
docker-compose up -d

# In another terminal, start ngrok
ngrok http 5000

# Use the ngrok URL (e.g., https://abc123.ngrok.io) as your webhook URL in GitHub
```

## 📥 Viewing Inbox Events

### Using Docker Commands

```bash
# View entire event log
docker exec strategickhaos-webhook-inbox cat /inbox/events.log

# Tail the last 50 events
docker exec strategickhaos-webhook-inbox tail -n 50 /inbox/events.log

# Follow new events in real-time
docker exec strategickhaos-webhook-inbox tail -f /inbox/events.log
```

### Using Docker Volume

```bash
# Find the volume location
docker volume inspect strategickhaos-inbox-vol

# Or mount to a local directory by editing docker-compose.yml:
volumes:
  - ./inbox-data:/inbox
```

### Event Format

Events are stored as JSON lines with the following structure:

```json
{
  "timestamp": "2025-11-22T18:30:45.123456",
  "event": "push",
  "data": {
    "repository": {...},
    "pusher": {...},
    "commits": [...]
  }
}
```

## 🧪 Testing

### Local Testing (without Docker)

```bash
cd webhook-inbox

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GITHUB_WEBHOOK_SECRET="test-secret"

# Run the app
python app.py
```

### Test with curl

```bash
# Ping test (no signature required for ping)
curl -X POST http://localhost:5000/github-webhook \
  -H "X-GitHub-Event: ping" \
  -H "Content-Type: application/json" \
  -d '{"zen": "Design for failure."}'

# Health check
curl http://localhost:5000/health
```

## 🔒 Security Considerations

1. **Secret Management**: Never commit secrets to version control. Use environment variables or Docker secrets.
2. **HMAC Verification**: Always verify webhook signatures. This service rejects requests with invalid signatures.
3. **Network Security**: Use HTTPS in production (place behind reverse proxy like Traefik/nginx).
4. **Container Security**: Runs as non-root user inside container (Python 3.12-slim base).
5. **Rate Limiting**: Consider adding rate limiting for production deployments.

## 🚢 Production Deployment

### Deploy to Cloud

**AWS EC2 / DigitalOcean:**
```bash
# SSH into your server
ssh user@your-server

# Clone and deploy
git clone <repo-url>
cd webhook-inbox
export GITHUB_WEBHOOK_SECRET="your-secret"
docker-compose up -d
```

**Docker Hub:**
```bash
# Tag and push image
docker tag strategickhaos-inbox your-username/strategickhaos-inbox:latest
docker push your-username/strategickhaos-inbox:latest
```

### Reverse Proxy Setup (nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name webhooks.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /github-webhook {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🎓 SNHU/Portfolio Integration

This service demonstrates:

- **Microservices Architecture**: Containerized, single-purpose service
- **DevOps Practices**: Docker, CI/CD ready, infrastructure as code
- **Security**: HMAC authentication, signature verification
- **Software Engineering**: Clean code, separation of concerns, error handling
- **Documentation**: Comprehensive README, inline comments
- **Version Control**: Git workflow, branching strategy

Perfect for showcasing in your Computer Science/Software Engineering portfolio!

## 🔧 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs webhook-inbox

# Verify environment variables
docker-compose config
```

### Webhooks fail with 403
- Verify webhook secret matches in both GitHub and container
- Check signature header is being sent by GitHub
- Review container logs for signature verification errors

### Events not persisting
```bash
# Verify volume is mounted
docker inspect strategickhaos-webhook-inbox | grep -A 10 Mounts

# Check inbox directory permissions
docker exec strategickhaos-webhook-inbox ls -la /inbox
```

## 📚 Additional Resources

- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [ngrok Documentation](https://ngrok.com/docs)

## 🤝 Contributing

Contributions welcome! This is part of the Strategickhaos Sovereignty Architecture project.

## 📄 License

MIT License - See main repository LICENSE file.

---

**Built with 🔥 by Strategickhaos DAO LLC**

*Part of the Sovereignty Architecture - Discord DevOps Control Plane*
