"""
Obsidian vault tools - Read, create, and search notes
"""
import os
from pathlib import Path
from pydantic import BaseModel, Field
import yaml

# Load vault configuration
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

VAULTS = {v["name"]: Path(v["path"]) for v in config.get("obsidian", {}).get("vaults", [])}
DEFAULT_VAULT = list(VAULTS.values())[0] if VAULTS else Path("/home/user/vaults/Sovereignty")


class OpenNoteArgs(BaseModel):
    """Arguments for opening a note"""
    note_path: str = Field(description="Relative path to the note within vault, e.g. 'OSINT/Twitch Research.md'")
    vault_name: str | None = Field(default=None, description="Optional vault name. Uses default if not specified")


class CreateNoteArgs(BaseModel):
    """Arguments for creating a new note"""
    note_path: str = Field(description="Relative path for the new note, e.g. 'OSINT/New Research.md'")
    content: str = Field(description="Initial content for the note")
    vault_name: str | None = Field(default=None, description="Optional vault name. Uses default if not specified")


class CreateCanvasArgs(BaseModel):
    """Arguments for creating an Obsidian canvas"""
    canvas_path: str = Field(description="Relative path for the canvas file, e.g. 'Projects/Architecture.canvas'")
    nodes: list[dict] = Field(default_factory=list, description="List of nodes for the canvas")
    vault_name: str | None = Field(default=None, description="Optional vault name. Uses default if not specified")


class SearchVaultArgs(BaseModel):
    """Arguments for searching the vault"""
    query: str = Field(description="Search query string")
    vault_name: str | None = Field(default=None, description="Optional vault name. Uses default if not specified")
    max_results: int = Field(default=10, description="Maximum number of results to return")


def open_note(args: OpenNoteArgs) -> str:
    """Read and return the full content of an Obsidian note."""
    vault = VAULTS.get(args.vault_name) if args.vault_name else DEFAULT_VAULT
    path = vault / args.note_path
    
    if not path.exists():
        return f"Error: Note not found: {args.note_path}"
    
    if not path.is_file():
        return f"Error: Path is not a file: {args.note_path}"
    
    try:
        return path.read_text()
    except Exception as e:
        return f"Error reading note: {str(e)}"


def create_note(args: CreateNoteArgs) -> str:
    """Create a new Obsidian note with the given content."""
    vault = VAULTS.get(args.vault_name) if args.vault_name else DEFAULT_VAULT
    path = vault / args.note_path
    
    if path.exists():
        return f"Error: Note already exists: {args.note_path}"
    
    try:
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args.content)
        return f"Successfully created note: {args.note_path}"
    except Exception as e:
        return f"Error creating note: {str(e)}"


def create_canvas(args: CreateCanvasArgs) -> str:
    """Create an Obsidian canvas file."""
    vault = VAULTS.get(args.vault_name) if args.vault_name else DEFAULT_VAULT
    path = vault / args.canvas_path
    
    if path.exists():
        return f"Error: Canvas already exists: {args.canvas_path}"
    
    try:
        import json
        canvas_data = {
            "nodes": args.nodes,
            "edges": []
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(canvas_data, indent=2))
        return f"Successfully created canvas: {args.canvas_path}"
    except Exception as e:
        return f"Error creating canvas: {str(e)}"


def search_vault(args: SearchVaultArgs) -> str:
    """Search for files containing the query string in the vault."""
    vault = VAULTS.get(args.vault_name) if args.vault_name else DEFAULT_VAULT
    
    if not vault.exists():
        return f"Error: Vault not found: {vault}"
    
    try:
        results = []
        query_lower = args.query.lower()
        
        for md_file in vault.rglob("*.md"):
            try:
                content = md_file.read_text()
                if query_lower in content.lower():
                    # Get relative path from vault
                    rel_path = md_file.relative_to(vault)
                    # Get first matching line as preview
                    lines = content.split('\n')
                    matching_line = next((line for line in lines if query_lower in line.lower()), "")
                    results.append({
                        "path": str(rel_path),
                        "preview": matching_line[:100] + ("..." if len(matching_line) > 100 else "")
                    })
                    
                    if len(results) >= args.max_results:
                        break
            except Exception:
                continue
        
        if not results:
            return f"No results found for query: {args.query}"
        
        output = f"Found {len(results)} result(s):\n\n"
        for result in results:
            output += f"- {result['path']}\n  {result['preview']}\n"
        
        return output
    except Exception as e:
        return f"Error searching vault: {str(e)}"


# Attach tool metadata
open_note.__tool__ = {
    "name": "obsidian_open_note",
    "description": "Read the full text of a single Obsidian markdown note.",
    "parameters": OpenNoteArgs.model_json_schema()
}

create_note.__tool__ = {
    "name": "obsidian_create_note",
    "description": "Create a new Obsidian note with specified content.",
    "parameters": CreateNoteArgs.model_json_schema()
}

create_canvas.__tool__ = {
    "name": "obsidian_create_canvas",
    "description": "Create an Obsidian canvas file for visual organization.",
    "parameters": CreateCanvasArgs.model_json_schema()
}

search_vault.__tool__ = {
    "name": "obsidian_search_vault",
    "description": "Search for notes containing specific text in an Obsidian vault.",
    "parameters": SearchVaultArgs.model_json_schema()
}
