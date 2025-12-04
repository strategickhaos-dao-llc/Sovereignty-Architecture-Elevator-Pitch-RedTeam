# Sovereign Research Browser - Usage Examples

This document provides practical examples of how to use the Sovereign Research Browser Node in various scenarios.

## Quick Start

### Start the Service

```bash
# Using Python directly
cd sovereign_browser
LOGS_DIR=/var/logs SOVEREIGN_BROWSER_PORT=8086 python3 main.py

# Using Docker
docker-compose up -d sovereign-browser

# Check health
curl http://localhost:8086/health
```

## API Usage Examples

### 1. Basic Health Check

```bash
curl http://localhost:8086/health
```

**Response:**
```json
{
  "status": "sovereign_research_node",
  "node": "hostname",
  "allowed_domains_count": 12
}
```

### 2. List Allowed Domains

```bash
curl http://localhost:8086/domains | jq
```

**Response:**
```json
{
  "allowed_domains": [
    "arxiv.org",
    "cloudflare.com",
    "developer.mozilla.org",
    "docs.python.org",
    "github.com",
    "ietf.org",
    "nginx.com",
    "proton.me",
    "pypi.org",
    "rfc-editor.org",
    "tailscale.com",
    "wikipedia.org"
  ],
  "count": 12
}
```

### 3. Browse Python Documentation

```bash
curl "http://localhost:8086/browse?url=https://docs.python.org/3/library/asyncio.html" | jq
```

**Response:**
```json
{
  "url": "https://docs.python.org/3/library/asyncio.html",
  "title": "asyncio — Asynchronous I/O — Python 3.x documentation",
  "text_preview": "asyncio is a library to write concurrent code using the async/await syntax...",
  "allowed": true
}
```

### 4. Attempt to Browse Blocked Domain (Returns 403)

```bash
curl "http://localhost:8086/browse?url=https://example.com/" | jq
```

**Response (403 Forbidden):**
```json
{
  "detail": "Domain example.com not in allowed research list"
}
```

## Python Client Examples

### Basic Usage

```python
import requests

# Browse an allowed site
response = requests.get(
    "http://localhost:8086/browse",
    params={"url": "https://docs.python.org/3/"}
)

if response.status_code == 200:
    data = response.json()
    print(f"Title: {data['title']}")
    print(f"Content preview: {data['text_preview'][:200]}...")
elif response.status_code == 403:
    print("Domain not allowed")
else:
    print(f"Error: {response.json()['detail']}")
```

### Batch Research

```python
import requests
import time

# Research multiple documentation pages
urls = [
    "https://docs.python.org/3/library/asyncio.html",
    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference",
    "https://github.com/microsoft/TypeScript",
]

results = []
for url in urls:
    response = requests.get(
        "http://localhost:8086/browse",
        params={"url": url}
    )
    
    if response.status_code == 200:
        data = response.json()
        results.append({
            "url": data["url"],
            "title": data["title"],
            "preview": data["text_preview"][:500]
        })
        print(f"✓ Fetched: {data['title']}")
    else:
        print(f"✗ Failed: {url}")
    
    # Be respectful - rate limit
    time.sleep(2)

# Process results
for result in results:
    print(f"\n{result['title']}")
    print(f"URL: {result['url']}")
    print(f"Preview: {result['preview']}...")
```

### Error Handling

```python
import requests
from requests.exceptions import RequestException

def safe_browse(url: str) -> dict:
    """Safely browse a URL with proper error handling"""
    try:
        response = requests.get(
            "http://localhost:8086/browse",
            params={"url": url},
            timeout=60  # Give it time for slow pages
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json()
            }
        elif response.status_code == 403:
            return {
                "success": False,
                "error": "Domain not in allowed list",
                "message": response.json()["detail"]
            }
        elif response.status_code == 500:
            return {
                "success": False,
                "error": "Browser error",
                "message": response.json()["detail"]
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "message": str(response.text)
            }
    
    except RequestException as e:
        return {
            "success": False,
            "error": "Request failed",
            "message": str(e)
        }

# Usage
result = safe_browse("https://docs.python.org/3/")
if result["success"]:
    print(f"Title: {result['data']['title']}")
else:
    print(f"Error: {result['error']} - {result['message']}")
```

## Integration Examples

### Integration with Discord Bot

```python
import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command(name='research')
async def research_command(ctx, url: str):
    """Fetch documentation from allowed research domains"""
    
    # Call sovereign browser
    response = requests.get(
        "http://localhost:8086/browse",
        params={"url": url}
    )
    
    if response.status_code == 200:
        data = response.json()
        
        embed = discord.Embed(
            title=data["title"],
            url=data["url"],
            description=data["text_preview"][:500] + "...",
            color=discord.Color.green()
        )
        embed.set_footer(text="Sovereign Research Browser")
        
        await ctx.send(embed=embed)
    elif response.status_code == 403:
        await ctx.send(f"❌ Domain not allowed for research: {url}")
    else:
        error = response.json()["detail"]
        await ctx.send(f"⚠️ Error: {error}")

# Run bot
bot.run('YOUR_BOT_TOKEN')
```

### Integration with AI Agent Pipeline

```python
import requests
import openai

def enrich_query_with_docs(query: str, doc_urls: list[str]) -> str:
    """Enrich AI query with documentation context"""
    
    # Fetch documentation
    doc_contexts = []
    for url in doc_urls:
        response = requests.get(
            "http://localhost:8086/browse",
            params={"url": url}
        )
        
        if response.status_code == 200:
            data = response.json()
            doc_contexts.append({
                "source": url,
                "title": data["title"],
                "content": data["text_preview"]
            })
    
    # Build enriched prompt
    context = "\n\n".join([
        f"Documentation: {doc['title']}\nURL: {doc['source']}\n{doc['content']}"
        for doc in doc_contexts
    ])
    
    enriched_prompt = f"""
    Context from official documentation:
    {context}
    
    User Query: {query}
    
    Answer the query using the provided documentation context.
    """
    
    # Query AI with context
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions using provided documentation."},
            {"role": "user", "content": enriched_prompt}
        ]
    )
    
    return response.choices[0].message.content

# Usage
answer = enrich_query_with_docs(
    "How do I use asyncio in Python?",
    ["https://docs.python.org/3/library/asyncio.html"]
)
print(answer)
```

### Monitoring and Alerting

```python
import requests
import time
import sys

def health_check_loop():
    """Continuous health monitoring"""
    while True:
        try:
            response = requests.get(
                "http://localhost:8086/health",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ {time.ctime()} - Browser healthy: {data['status']}")
            else:
                print(f"⚠ {time.ctime()} - Browser returned {response.status_code}")
                # Send alert here
        
        except Exception as e:
            print(f"✗ {time.ctime()} - Browser unreachable: {e}")
            # Send alert here
        
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    health_check_loop()
```

## Kubernetes Integration

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sovereign-browser
  namespace: research
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sovereign-browser
  template:
    metadata:
      labels:
        app: sovereign-browser
    spec:
      containers:
      - name: browser
        image: sovereign-browser:latest
        ports:
        - containerPort: 8086
        env:
        - name: SOVEREIGN_BROWSER_PORT
          value: "8086"
        - name: LOGS_DIR
          value: "/logs"
        volumeMounts:
        - name: logs
          mountPath: /logs
        livenessProbe:
          httpGet:
            path: /health
            port: 8086
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8086
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: logs
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: sovereign-browser
  namespace: research
spec:
  selector:
    app: sovereign-browser
  ports:
  - protocol: TCP
    port: 8086
    targetPort: 8086
  type: ClusterIP
```

### Using from Another Pod

```python
# Inside another Kubernetes pod in the same namespace
import requests

response = requests.get(
    "http://sovereign-browser.research.svc.cluster.local:8086/browse",
    params={"url": "https://docs.python.org/3/"}
)
```

## Log Analysis

### Parse Event Logs

```python
import json
from collections import Counter

def analyze_logs(log_file: str = "/logs/events.jsonl"):
    """Analyze PsycheVille event logs"""
    
    events = []
    with open(log_file, 'r') as f:
        for line in f:
            events.append(json.loads(line))
    
    # Count event types
    event_types = Counter(e['event'] for e in events)
    
    print("Event Summary:")
    for event_type, count in event_types.most_common():
        print(f"  {event_type}: {count}")
    
    # Find blocked domains
    blocked = [e for e in events if e['event'] == 'research_browse_blocked']
    blocked_domains = Counter(e['domain'] for e in blocked)
    
    print("\nMost Blocked Domains:")
    for domain, count in blocked_domains.most_common(5):
        print(f"  {domain}: {count} attempts")
    
    # Find errors
    errors = [e for e in events if e['event'] == 'research_browse_error']
    print(f"\nTotal Errors: {len(errors)}")

# Run analysis
analyze_logs()
```

## Advanced Configuration

### Custom Domain Whitelist

To add your own research domains, edit `main.py`:

```python
ALLOWED_DOMAINS = [
    # Official documentation
    "docs.python.org",
    "developer.mozilla.org",
    
    # Your custom research domains
    "your-company-docs.internal.com",
    "research.your-university.edu",
    
    # Open source repos
    "github.com",
]
```

### Environment Variables

```bash
# Port configuration
export SOVEREIGN_BROWSER_PORT=8086

# Logs directory
export LOGS_DIR=/var/log/sovereign_browser

# Start service
python3 main.py
```

## Best Practices

1. **Rate Limiting**: Add delays between requests to be respectful
2. **Error Handling**: Always handle 403, 500, and timeout errors
3. **Monitoring**: Monitor `/health` endpoint for service availability
4. **Logging**: Review event logs regularly for security analysis
5. **Domain Management**: Keep whitelist minimal and well-documented
6. **Caching**: Cache results when appropriate to reduce load
7. **Timeouts**: Use reasonable timeouts (30-60 seconds)

## Troubleshooting

### Service Not Responding

```bash
# Check if service is running
curl http://localhost:8086/health

# Check logs
tail -f /logs/events.jsonl

# Check Docker logs
docker-compose logs -f sovereign-browser
```

### Domain Blocked

If a legitimate research domain is blocked:

1. Verify the domain is in the whitelist
2. Check domain spelling (case-insensitive but must match)
3. Add to `ALLOWED_DOMAINS` in `main.py` if needed
4. Restart the service

### Slow Responses

- Increase timeout in client (default: 30s)
- Check network connectivity
- Monitor browser process memory usage
- Consider adding caching layer

## Security Considerations

1. **Only add trusted domains** to the whitelist
2. **Review logs regularly** for suspicious activity
3. **Don't add login-required sites** (CFAA compliance)
4. **Rate limit requests** to prevent abuse
5. **Use HTTPS only** for secure connections
6. **Monitor resource usage** to detect DoS attempts

---

For more information, see:
- [README.md](README.md) - Full documentation
- [BROWSER_AUTOMATION_LEGAL_ANALYSIS.md](../legal/BROWSER_AUTOMATION_LEGAL_ANALYSIS.md) - Legal compliance details
