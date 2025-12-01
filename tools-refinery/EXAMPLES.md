# Tools Refinery - Usage Examples

This document provides practical examples of using the Tools Refinery.

## Starting the Server

```bash
cd tools-refinery
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start with custom API key
REFINERY_KEY=my-secret-key python refinery.py
```

Server will start on `http://127.0.0.1:8211`

## Example API Calls

### 1. Health Check

```bash
curl -X POST http://localhost:8211/v1/tools/system_health \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "result": "Health Check:\n\n- Config file: ✓\n- Tools modules: 5\n- Obsidian vaults: 1/2 accessible\n\nStatus: Operational",
  "success": true
}
```

### 2. List Available Tools

```bash
curl -X POST http://localhost:8211/v1/tools/system_list_available_tools \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 3. Read an Obsidian Note

```bash
curl -X POST http://localhost:8211/v1/tools/obsidian_open_note \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "note_path": "Projects/Architecture.md",
    "vault_name": "Sovereignty"
  }'
```

### 4. Search Vault for Content

```bash
curl -X POST http://localhost:8211/v1/tools/obsidian_search_vault \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "API design",
    "vault_name": "Sovereignty",
    "max_results": 10
  }'
```

### 5. Create a New Note

```bash
curl -X POST http://localhost:8211/v1/tools/obsidian_create_note \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "note_path": "Daily/2024-11-21.md",
    "content": "# 2024-11-21\n\n## Tools Refinery Launch\n\n- Implemented 15 tools\n- All tests passing",
    "vault_name": "Sovereignty"
  }'
```

### 6. Get Git Commit History

```bash
curl -X POST http://localhost:8211/v1/tools/git_log_summary \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "max_commits": 5,
    "repo_path": "/workspace/my-project"
  }'
```

### 7. Get File at Specific Commit

```bash
curl -X POST http://localhost:8211/v1/tools/git_get_file_at_commit \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "src/main.py",
    "commit_sha": "HEAD~3",
    "repo_path": "/workspace/my-project"
  }'
```

### 8. Create Code Snippet with Line Numbers

```bash
curl -X POST http://localhost:8211/v1/tools/git_create_snippet \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "refinery.py",
    "start_line": 1,
    "end_line": 20,
    "commit_sha": "HEAD"
  }'
```

### 9. Add Entity to OSINT Investigation Graph

```bash
curl -X POST http://localhost:8211/v1/tools/osint_add_to_graph \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "graph_name": "project-x",
    "entity_type": "organization",
    "entity_id": "company_abc",
    "properties": {
      "name": "ABC Corp",
      "industry": "Technology",
      "founded": "2020"
    },
    "relationships": [
      {
        "type": "owns",
        "target": "domain_abc_com"
      }
    ]
  }'
```

### 10. Attach Methodology Notes

```bash
curl -X POST http://localhost:8211/v1/tools/osint_attach_methodology_note \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "graph_name": "project-x",
    "entity_id": "company_abc",
    "methodology": "Conducted open source research using public records and social media",
    "sources": [
      "https://example.com/company-profile",
      "LinkedIn company page"
    ],
    "techniques": [
      "Public records search",
      "Social media analysis",
      "WHOIS lookup"
    ]
  }'
```

### 11. Save HAR File

```bash
curl -X POST http://localhost:8211/v1/tools/web_save_har \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "har_json": "{\"log\": {\"version\": \"1.2\", \"entries\": []}}",
    "output_path": "/tmp/captures/session-001.har"
  }'
```

### 12. Extract Domains from HAR

```bash
curl -X POST http://localhost:8211/v1/tools/web_extract_har_domains \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "har_path": "/tmp/captures/session-001.har"
  }'
```

## Using with LLM Clients

### Cursor / Continue.dev

1. Open settings
2. Add a new model/API endpoint:
   - **Base URL**: `http://localhost:8211/v1`
   - **API Key**: Your `REFINERY_KEY` value
3. The LLM will automatically discover available tools

### Claude Desktop (via Custom Integration)

Edit your Claude Desktop configuration to add:

```json
{
  "tools": {
    "refinery": {
      "endpoint": "http://localhost:8211/v1",
      "api_key": "your-refinery-key"
    }
  }
}
```

## Error Handling Examples

### Missing API Key

```bash
curl -X POST http://localhost:8211/v1/tools/system_health \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key"
}
```

### Invalid Tool Parameters

```bash
curl -X POST http://localhost:8211/v1/tools/obsidian_open_note \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"note_path": ""}'
```

The Pydantic model will validate the request and return detailed error information.

### File Not Found

```bash
curl -X POST http://localhost:8211/v1/tools/obsidian_open_note \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "note_path": "NonExistent/File.md"
  }'
```

Response:
```json
{
  "result": "Error: Note not found: NonExistent/File.md",
  "success": true
}
```

Note: Tools return success=true even for operational errors (like file not found) since the tool executed successfully. The error message is in the result.

## Python Client Example

```python
import requests
import json

class RefineryClient:
    def __init__(self, base_url="http://localhost:8211", api_key="dev-key-change-me"):
        self.base_url = base_url
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def call_tool(self, tool_name, **kwargs):
        url = f"{self.base_url}/v1/tools/{tool_name}"
        response = requests.post(url, headers=self.headers, json=kwargs)
        response.raise_for_status()
        return response.json()
    
    def list_tools(self):
        return self.call_tool("system_list_available_tools")
    
    def health_check(self):
        return self.call_tool("system_health")

# Usage
client = RefineryClient(api_key="my-secret-key")

# Check health
print(client.health_check())

# Open a note
result = client.call_tool(
    "obsidian_open_note",
    note_path="Projects/README.md",
    vault_name="Sovereignty"
)
print(result["result"])
```

## Tips

1. **Use environment variables** for sensitive configuration like API keys
2. **Start with system tools** to verify the server is working correctly
3. **Check the health endpoint** if tools aren't working as expected
4. **Review the logs** - Uvicorn shows all requests and errors
5. **Test with curl first** before integrating with LLM clients
6. **Use --verbose flag** with curl to debug connection issues
