"""
Code-to-Diagram Translator Service
IDEA_002 - First child born from the ideas catalog

Turn source code into a simple graph representation.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import ast
from typing import List, Dict, Any

app = FastAPI(
    title="Code-to-Diagram Translator",
    description="Turn source code into a simple graph representation.",
    version="0.1.0",
)


class AnalyzeRequest(BaseModel):
    """Request model for code analysis."""
    language: str
    source: str


class Node(BaseModel):
    """Graph node representing a code element."""
    id: str
    type: str
    label: str | None = None


class Edge(BaseModel):
    """Graph edge representing a relationship between code elements."""
    source: str
    target: str
    type: str


class AnalyzeResponse(BaseModel):
    """Response model containing the code graph."""
    nodes: List[Node]
    edges: List[Edge]
    meta: Dict[str, Any]


@app.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze source code and return a graph representation.

    Very simple implementation:
    - Supports `language == "python"` for now.
    - Uses `ast` to find functions and classes in the top-level module.
    - Builds a `module:<name>` node and `func:/class:` child nodes.
    """

    if req.language.lower() != "python":
        # For now, only python is supported.
        return AnalyzeResponse(
            nodes=[],
            edges=[],
            meta={
                "language": req.language,
                "num_lines": len(req.source.splitlines()),
                "warning": "Only Python is supported in v0.1.0",
            },
        )

    tree = ast.parse(req.source)
    module_id = "module:root"
    nodes: List[Node] = [Node(id=module_id, type="module", label="root")]
    edges: List[Edge] = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_id = f"func:{node.name}"
            nodes.append(Node(id=func_id, type="function", label=node.name))
            edges.append(Edge(source=module_id, target=func_id, type="contains"))

        elif isinstance(node, ast.ClassDef):
            class_id = f"class:{node.name}"
            nodes.append(Node(id=class_id, type="class", label=node.name))
            edges.append(Edge(source=module_id, target=class_id, type="contains"))

            for sub in node.body:
                if isinstance(sub, ast.FunctionDef):
                    method_id = f"method:{node.name}.{sub.name}"
                    nodes.append(Node(id=method_id, type="method", label=sub.name))
                    edges.append(
                        Edge(source=class_id, target=method_id, type="contains")
                    )

    return AnalyzeResponse(
        nodes=nodes,
        edges=edges,
        meta={
            "language": "python",
            "num_lines": len(req.source.splitlines()),
            "num_nodes": len(nodes),
            "num_edges": len(edges),
        },
    )
