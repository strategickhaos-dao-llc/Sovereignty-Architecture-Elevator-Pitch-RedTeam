"""
Web tools - Save web pages, HAR files, and extract information
"""
import json
from pathlib import Path
from pydantic import BaseModel, Field
import yaml

# Load configuration
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

WEB_CONFIG = config.get("web", {})


class SavePageAsMdArgs(BaseModel):
    """Arguments for saving a webpage as markdown"""
    url: str = Field(description="URL of the webpage to save")
    output_path: str = Field(description="Path where to save the markdown file")
    title: str | None = Field(default=None, description="Optional custom title for the page")


class SaveHarArgs(BaseModel):
    """Arguments for saving HAR data"""
    har_json: str = Field(description="HAR (HTTP Archive) data as JSON string")
    output_path: str = Field(description="Path where to save the HAR file")


class ExtractHarDomainsArgs(BaseModel):
    """Arguments for extracting domains from HAR"""
    har_path: str = Field(description="Path to the HAR file")


def save_page_as_md(args: SavePageAsMdArgs) -> str:
    """
    Save a webpage as markdown (stub - requires html2text or similar).
    In a real implementation, this would fetch the URL and convert to markdown.
    """
    try:
        output_path = Path(args.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Stub content - in production, would fetch and convert
        content = f"# {args.title or args.url}\n\n"
        content += f"Source: {args.url}\n\n"
        content += "<!-- Content would be fetched and converted here -->\n"
        
        output_path.write_text(content)
        return f"Successfully saved page to: {args.output_path}"
    except Exception as e:
        return f"Error saving page: {str(e)}"


def save_har(args: SaveHarArgs) -> str:
    """Save HAR (HTTP Archive) data to a file."""
    try:
        output_path = Path(args.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Validate JSON
        har_data = json.loads(args.har_json)
        
        # Save formatted HAR
        output_path.write_text(json.dumps(har_data, indent=2))
        return f"Successfully saved HAR file to: {args.output_path}"
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON in HAR data: {str(e)}"
    except Exception as e:
        return f"Error saving HAR file: {str(e)}"


def extract_har_domains(args: ExtractHarDomainsArgs) -> str:
    """Extract unique domains from a HAR file."""
    try:
        har_path = Path(args.har_path)
        
        if not har_path.exists():
            return f"Error: HAR file not found: {args.har_path}"
        
        har_data = json.loads(har_path.read_text())
        
        domains = set()
        
        # Extract domains from entries
        if "log" in har_data and "entries" in har_data["log"]:
            for entry in har_data["log"]["entries"]:
                if "request" in entry and "url" in entry["request"]:
                    url = entry["request"]["url"]
                    # Simple domain extraction
                    if "://" in url:
                        domain = url.split("://")[1].split("/")[0].split(":")[0]
                        domains.add(domain)
        
        if not domains:
            return "No domains found in HAR file"
        
        result = f"Found {len(domains)} unique domain(s):\n\n"
        for domain in sorted(domains):
            result += f"- {domain}\n"
        
        return result
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON in HAR file: {str(e)}"
    except Exception as e:
        return f"Error extracting domains: {str(e)}"


# Attach tool metadata
save_page_as_md.__tool__ = {
    "name": "web_save_page_as_md",
    "description": "Save a webpage as markdown format (stub implementation).",
    "parameters": SavePageAsMdArgs.model_json_schema()
}

save_har.__tool__ = {
    "name": "web_save_har",
    "description": "Save HAR (HTTP Archive) data to a file for analysis.",
    "parameters": SaveHarArgs.model_json_schema()
}

extract_har_domains.__tool__ = {
    "name": "web_extract_har_domains",
    "description": "Extract and list unique domains from a HAR file.",
    "parameters": ExtractHarDomainsArgs.model_json_schema()
}
