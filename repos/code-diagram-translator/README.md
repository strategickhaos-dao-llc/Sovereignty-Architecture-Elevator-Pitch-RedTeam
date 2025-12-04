# Code-to-Diagram Translator

**Idea ID:** IDEA_002  
**Catalog Category:** devtools  
**Primary Department:** infra_cloud  
**Video Module:** Q034 (Bloom's Taxonomy – Software Engineering)

---

## Purpose

The Code-to-Diagram Translator ingests source code (starting with Python) and
produces a simple, machine-readable graph representation of the architecture:

- Functions
- Classes
- Call relationships (best-effort)
- Module-level structure

The goal is not to replace full-blown UML tools, but to give a **living,
auto-updating diagram source** that other tools (Graphviz, Mermaid, Obsidian,
KnowledgePods) can render visually.

This repo is the **first child** generated from the `ideas_catalog.yaml`.

---

## High-Level Flow

1. User POSTs source code (or a file path) to the `/analyze` endpoint.
2. The service parses the code and constructs a graph:
   - `nodes`: functions/classes/modules
   - `edges`: "calls" or "contains" relationships (best-effort)
3. The response returns JSON that can be:
   - Rendered directly as a diagram
   - Saved as an artifact
   - Attached to a KnowledgePod

Example output:

```json
{
  "nodes": [
    {"id": "module:main", "type": "module"},
    {"id": "func:main", "type": "function"}
  ],
  "edges": [
    {"source": "module:main", "target": "func:main", "type": "contains"}
  ]
}
```

---

## API

### POST /analyze

Request body (JSON):

```json
{
  "language": "python",
  "source": "def main():\n    print('hi')\n"
}
```

Response:

```json
{
  "nodes": [ ... ],
  "edges": [ ... ],
  "meta": {
    "language": "python",
    "num_lines": 2
  }
}
```

---

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn

No external services required. This can run:

- As a Docker container via docker-compose.yml
- As a Kubernetes Deployment with a ClusterIP or Ingress
- Inside a KnowledgePod for educational demos

---

## Quickstart (Local)

```bash
# from repos/code-diagram-translator
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

Then:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "source": "def main():\n    print(\"hi\")\n"}'
```

---

## Planned Extensions

- Support for additional languages (JavaScript, TypeScript, Go)
- Export to Mermaid / Graphviz directly
- Git hook integration to regenerate diagrams on commit
- UI view for quick architecture browsing

---

## Catalog Reference

This repo originates from `ideas/ideas_catalog.yaml` entry:

```yaml
- id: "IDEA_002"
  title: "Code-to-Diagram Translator"
  category: "devtools"
  maturity_level: "prototype"
  primary_department: "infra_cloud"
  repo_path: "repos/code-diagram-translator/"
  service_name: "svc-code-diagram"
  k8s_namespace: "ns-infra"
  video_module_id: "Q034"
```
