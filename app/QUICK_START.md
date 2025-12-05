# Quick Start Guide - Sovereign Research Browser

## 🚀 In 60 Seconds

### 1. Test the Browser (No Server Required)
```bash
cd app
python example_usage.py
```

### 2. Start the FastAPI Server
```bash
cd refinory
pip install -r requirements.refinory.txt
uvicorn refinory.main:app --host 0.0.0.0 --port 8000
```

### 3. Make Your First Request
```bash
# Browse arXiv paper
curl "http://localhost:8000/browse?url=https://arxiv.org/abs/2103.00020"

# Browse Python docs
curl "http://localhost:8000/browse?url=https://docs.python.org/3/"

# Browse GitHub repo
curl "http://localhost:8000/browse?url=https://github.com/python/cpython"
```

## 📊 What You Get

```json
{
  "url": "https://arxiv.org/abs/2103.00020",
  "title": "Paper Title",
  "text_preview": "First 10,000 characters of content...",
  "research_allowed": true,
  "rate_limited": false,
  "robots_compliant": true,
  "status_code": 200,
  "content_type": "text/html; charset=utf-8"
}
```

## ✅ Whitelisted Domain Examples

Try these URLs (all approved):

**Documentation:**
- https://docs.python.org/3/
- https://developer.mozilla.org/en-US/
- https://kubernetes.io/docs/

**Academic:**
- https://arxiv.org/abs/2103.00020
- https://pubmed.ncbi.nlm.nih.gov/

**Code:**
- https://github.com/python/cpython
- https://stackoverflow.com/questions/

**AI/ML:**
- https://pytorch.org/docs/
- https://huggingface.co/docs

## ❌ Error Examples

**403 Forbidden - Not Whitelisted:**
```bash
curl "http://localhost:8000/browse?url=https://random-site.com/"
# Response: {"detail": "Domain not in whitelist"}
```

**429 Rate Limited:**
```bash
# After 12 requests in 60 seconds to same domain
curl "http://localhost:8000/browse?url=https://github.com/"
# Response: {"detail": "Rate limited. Retry after 30.5 seconds"}
```

## 🔧 Configuration

### Adjust Rate Limit
Edit `refinory/refinory/main.py`:
```python
research_browser = ResearchBrowser(
    rate_limit_requests_per_minute=20  # Increase from 12
)
```

### Add New Domain
Edit `app/allowed_domains.yaml`:
```yaml
allowed_domains:
  - "newdomain.com"
  - "research.example.org"
```

## 🐳 Docker Deployment

```bash
cd app
docker-compose -f docker-compose.browser.yml up -d

# Test it
curl "http://localhost:8000/browse?url=https://github.com/"
```

## 📚 More Information

- **Full Guide:** [README.md](./README.md)
- **Athena Integration:** [ATHENA_TOOL_INTEGRATION.md](./ATHENA_TOOL_INTEGRATION.md)
- **Implementation Details:** [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)

## 🎯 For Athena AI Agents

Add this tool to your agent configuration:

```json
{
  "type": "function",
  "function": {
    "name": "sovereign_research_browse",
    "description": "Research browser for 160+ whitelisted domains",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {"type": "string"}
      },
      "required": ["url"]
    }
  }
}
```

Then in your agent prompt:
```
When researching, use sovereign_research_browse to read docs, 
standards, and academic pages. Respect 403/429 responses.
```

## 🔒 Security Features

✅ Whitelist-only (161 approved domains)  
✅ robots.txt compliance (RFC 9309)  
✅ Rate limiting (12 req/min per domain)  
✅ Full audit trail  
✅ No authentication handling  

## 🎉 You're Ready!

The browser is now configured and ready to use. Start with the examples above, then explore the full documentation for advanced features.

**Happy Researching! 🚀**
