"""
System tools - Health checks, list available tools, list vaults
"""
from pathlib import Path
from pydantic import BaseModel, Field
import yaml
import importlib

# Load configuration
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)


class ListAvailableToolsArgs(BaseModel):
    """Arguments for listing available tools (no arguments needed)"""
    pass


class HealthArgs(BaseModel):
    """Arguments for health check (no arguments needed)"""
    pass


class ListVaultsArgs(BaseModel):
    """Arguments for listing Obsidian vaults (no arguments needed)"""
    pass


def list_available_tools(args: ListAvailableToolsArgs) -> str:
    """List all available tools in the refinery."""
    try:
        tools_dir = Path(__file__).parent
        tools = []
        
        for module_file in tools_dir.glob("*.py"):
            if module_file.name.startswith("_"):
                continue
            
            module_name = module_file.stem
            try:
                module = importlib.import_module(f"tools.{module_name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and hasattr(attr, "__tool__"):
                        tool_info = attr.__tool__
                        tools.append({
                            "name": tool_info.get("name", attr_name),
                            "description": tool_info.get("description", ""),
                            "module": module_name
                        })
            except Exception:
                continue
        
        if not tools:
            return "No tools found"
        
        result = f"Available Tools ({len(tools)} total):\n\n"
        for tool in sorted(tools, key=lambda x: x["name"]):
            result += f"- **{tool['name']}** ({tool['module']})\n"
            result += f"  {tool['description']}\n\n"
        
        return result
    except Exception as e:
        return f"Error listing tools: {str(e)}"


def health(args: HealthArgs) -> str:
    """Check health status of the refinery."""
    try:
        checks = []
        
        # Check config file
        config_exists = config_path.exists()
        checks.append(f"Config file: {'✓' if config_exists else '✗'}")
        
        # Check tools directory
        tools_dir = Path(__file__).parent
        tools_count = len(list(tools_dir.glob("*.py"))) - 1  # Exclude __init__.py
        checks.append(f"Tools modules: {tools_count}")
        
        # Check vaults
        vaults = config.get("obsidian", {}).get("vaults", [])
        vaults_found = sum(1 for v in vaults if Path(v["path"]).exists())
        checks.append(f"Obsidian vaults: {vaults_found}/{len(vaults)} accessible")
        
        result = "Health Check:\n\n"
        for check in checks:
            result += f"- {check}\n"
        
        result += "\nStatus: Operational"
        return result
    except Exception as e:
        return f"Error performing health check: {str(e)}"


def list_vaults(args: ListVaultsArgs) -> str:
    """List all configured Obsidian vaults."""
    try:
        vaults = config.get("obsidian", {}).get("vaults", [])
        
        if not vaults:
            return "No vaults configured"
        
        result = f"Configured Obsidian Vaults ({len(vaults)} total):\n\n"
        for vault in vaults:
            name = vault.get("name", "Unknown")
            path = vault.get("path", "")
            exists = Path(path).exists()
            status = "✓" if exists else "✗ (not found)"
            result += f"- **{name}** {status}\n"
            result += f"  Path: {path}\n\n"
        
        return result
    except Exception as e:
        return f"Error listing vaults: {str(e)}"


# Attach tool metadata
list_available_tools.__tool__ = {
    "name": "system_list_available_tools",
    "description": "List all available tools in the Tools Refinery.",
    "parameters": ListAvailableToolsArgs.model_json_schema()
}

health.__tool__ = {
    "name": "system_health",
    "description": "Check the health status of the Tools Refinery.",
    "parameters": HealthArgs.model_json_schema()
}

list_vaults.__tool__ = {
    "name": "system_list_vaults",
    "description": "List all configured Obsidian vaults and their status.",
    "parameters": ListVaultsArgs.model_json_schema()
}
