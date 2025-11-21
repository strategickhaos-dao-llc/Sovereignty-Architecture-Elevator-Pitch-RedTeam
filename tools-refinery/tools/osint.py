"""
OSINT tools - Add to investigation graphs and attach methodology notes
"""
import json
from pathlib import Path
from pydantic import BaseModel, Field
import yaml

# Load configuration
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

OSINT_CONFIG = config.get("osint", {})
GRAPH_PATH = Path(OSINT_CONFIG.get("graph_path", "/home/user/osint-graphs"))
METHODOLOGY_TEMPLATE = OSINT_CONFIG.get("methodology_template", "## Methodology\n\n")


class AddToGraphArgs(BaseModel):
    """Arguments for adding an entity to investigation graph"""
    graph_name: str = Field(description="Name of the investigation graph")
    entity_type: str = Field(description="Type of entity (person, organization, domain, etc.)")
    entity_id: str = Field(description="Unique identifier for the entity")
    properties: dict = Field(default_factory=dict, description="Properties/attributes of the entity")
    relationships: list[dict] = Field(default_factory=list, description="Relationships to other entities")


class AttachMethodologyNoteArgs(BaseModel):
    """Arguments for attaching methodology notes"""
    graph_name: str = Field(description="Name of the investigation graph")
    entity_id: str = Field(description="Entity ID to attach note to")
    methodology: str = Field(description="Methodology description")
    sources: list[str] = Field(default_factory=list, description="List of sources used")
    techniques: list[str] = Field(default_factory=list, description="OSINT techniques applied")


def add_to_graph(args: AddToGraphArgs) -> str:
    """Add an entity to an OSINT investigation graph."""
    try:
        GRAPH_PATH.mkdir(parents=True, exist_ok=True)
        graph_file = GRAPH_PATH / f"{args.graph_name}.json"
        
        # Load existing graph or create new one
        if graph_file.exists():
            graph_data = json.loads(graph_file.read_text())
        else:
            graph_data = {
                "name": args.graph_name,
                "entities": {},
                "metadata": {
                    "created": "auto-generated",
                    "version": "0.1"
                }
            }
        
        # Add or update entity
        entity = {
            "type": args.entity_type,
            "id": args.entity_id,
            "properties": args.properties,
            "relationships": args.relationships
        }
        
        graph_data["entities"][args.entity_id] = entity
        
        # Save updated graph
        graph_file.write_text(json.dumps(graph_data, indent=2))
        
        return f"Successfully added entity '{args.entity_id}' to graph '{args.graph_name}'"
    except Exception as e:
        return f"Error adding to graph: {str(e)}"


def attach_methodology_note(args: AttachMethodologyNoteArgs) -> str:
    """Attach methodology notes to an entity in the investigation graph."""
    try:
        GRAPH_PATH.mkdir(parents=True, exist_ok=True)
        graph_file = GRAPH_PATH / f"{args.graph_name}.json"
        
        if not graph_file.exists():
            return f"Error: Graph '{args.graph_name}' not found"
        
        graph_data = json.loads(graph_file.read_text())
        
        if args.entity_id not in graph_data.get("entities", {}):
            return f"Error: Entity '{args.entity_id}' not found in graph"
        
        # Create methodology note
        methodology_note = {
            "methodology": args.methodology,
            "sources": args.sources,
            "techniques": args.techniques
        }
        
        # Attach to entity
        entity = graph_data["entities"][args.entity_id]
        if "methodology" not in entity:
            entity["methodology"] = []
        entity["methodology"].append(methodology_note)
        
        # Save updated graph
        graph_file.write_text(json.dumps(graph_data, indent=2))
        
        return f"Successfully attached methodology note to entity '{args.entity_id}' in graph '{args.graph_name}'"
    except Exception as e:
        return f"Error attaching methodology note: {str(e)}"


# Attach tool metadata
add_to_graph.__tool__ = {
    "name": "osint_add_to_graph",
    "description": "Add an entity to an OSINT investigation graph with properties and relationships.",
    "parameters": AddToGraphArgs.model_json_schema()
}

attach_methodology_note.__tool__ = {
    "name": "osint_attach_methodology_note",
    "description": "Attach methodology notes to an entity in an investigation graph.",
    "parameters": AttachMethodologyNoteArgs.model_json_schema()
}
