# Tools Refinery v0.1

A minimal HTTP server that exposes safe, idempotent, well-named tools that any LLM client (Claude, Grok, Cursor, Continue.dev, etc.) can call via OpenAI-compatible tools/schema endpoints.

## Quick Start

### 1. Install Dependencies

```bash
cd tools-refinery
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

Edit `config.yaml` to set your vault paths and preferences:

```yaml
obsidian:
  vaults:
    - name: "Sovereignty"
      path: "/home/user/vaults/Sovereignty"

git:
  default_repo_path: "/workspace"

system:
  api_key: "dev-key-change-me"
  host: "127.0.0.1"
  port: 8211
```

Or use environment variables:
- `REFINERY_KEY` - API key for authentication
- `OBSIDIAN_VAULT` - Default Obsidian vault path
- `GITHUB_TOKEN` - Optional GitHub token for git operations

### 3. Run the Server

```bash
# With default settings
python refinery.py

# Or with custom API key
REFINERY_KEY=your-secret-key python refinery.py
```

The server will start on `http://127.0.0.1:8211`

### 4. Use with LLM Clients

Configure your LLM client (Cursor, Continue.dev, Claude Desktop, etc.) to use:
- **Base URL**: `http://localhost:8211/v1`
- **API Key**: The value you set in `REFINERY_KEY` or config.yaml

## Architecture

```
tools-refinery/
├── refinery.py                 # FastAPI server, tool registry, auth
├── tools/
│   ├── __init__.py
│   ├── obsidian.py             # open_note, create_note, create_canvas, search_vault
│   ├── git.py                  # get_file_at_commit, git_log_summary, create_snippet
│   ├── web.py                  # save_page_as_md, save_har, extract_har_domains
│   ├── osint.py                # add_to_graph, attach_methodology_note
│   └── system.py               # list_available_tools, health, list_vaults
├── config.yaml                 # paths, allowed vaults, github tokens, etc.
├── schemas/                    # Pydantic models used in tool schemas
└── requirements.txt
```

## Available Tools

### Obsidian Tools
- `obsidian_open_note` - Read the full text of an Obsidian note
- `obsidian_create_note` - Create a new note with specified content
- `obsidian_create_canvas` - Create an Obsidian canvas for visual organization
- `obsidian_search_vault` - Search for notes containing specific text

### Git Tools
- `git_get_file_at_commit` - Retrieve file content at a specific commit
- `git_log_summary` - Get a summary of recent commits
- `git_create_snippet` - Create a code snippet with line numbers

### Web Tools
- `web_save_page_as_md` - Save a webpage as markdown
- `web_save_har` - Save HAR (HTTP Archive) data for analysis
- `web_extract_har_domains` - Extract unique domains from HAR files

### OSINT Tools
- `osint_add_to_graph` - Add entities to investigation graphs
- `osint_attach_methodology_note` - Attach methodology notes to entities

### System Tools
- `system_list_available_tools` - List all available tools
- `system_health` - Check refinery health status
- `system_list_vaults` - List configured Obsidian vaults

## API Endpoints

- `GET /` - Server info and available endpoints
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /openapi.json` - OpenAPI schema with all tools
- `POST /v1/tools/{tool_name}` - Execute a specific tool

## Adding New Tools

1. Create a new file in `tools/` (e.g., `tools/custom.py`)
2. Define your tool function with Pydantic model for arguments:

```python
from pydantic import BaseModel, Field

class MyToolArgs(BaseModel):
    param1: str = Field(description="Description of parameter")

def my_tool(args: MyToolArgs) -> str:
    """Do something useful."""
    return f"Result: {args.param1}"

# Attach metadata
my_tool.__tool__ = {
    "name": "custom_my_tool",
    "description": "Description of what the tool does",
    "parameters": MyToolArgs.model_json_schema()
}
```

3. Restart the server - your tool is automatically registered!

## Security

- API key authentication required for all tool endpoints
- Tools are designed to be safe and idempotent
- No write operations without explicit confirmation
- Rate limiting and sandboxing should be added for production use

## Testing

Test a tool manually with curl:

```bash
curl -X POST http://localhost:8211/v1/tools/system_health \
  -H "X-API-Key: dev-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Next Steps

- Add MCP (Model Context Protocol) compatibility
- Implement confirm-before-write for destructive operations
- Add rate limiting and request logging
- Create web UI for tool management
- Add tool usage analytics and monitoring

## License

MIT License - Part of the Strategickhaos Sovereignty Architecture project
