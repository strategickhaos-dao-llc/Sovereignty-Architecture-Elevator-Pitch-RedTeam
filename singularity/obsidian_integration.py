"""
Obsidian Integration - Long-Term Memory Brain Connection
========================================================

Connects the Singularity Engine to an Obsidian vault, enabling:
- Bidirectional knowledge synchronization
- Research vault as AI's long-term memory
- Automatic note creation and linking
- Knowledge graph extraction and visualization
- Daily research digests and synthesis notes

The Obsidian vault becomes the persistent brain - every paper analyzed,
every hypothesis generated, every insight discovered is stored and
linked for retrieval and learning.
"""

import asyncio
import os
import re
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field, asdict
from enum import Enum

import structlog

logger = structlog.get_logger(__name__)


class NoteType(Enum):
    """Types of notes in the Obsidian vault"""
    PAPER = "paper"
    HYPOTHESIS = "hypothesis"
    SYNTHESIS = "synthesis"
    PROTEIN = "protein"
    GENE = "gene"
    PATHWAY = "pathway"
    TREATMENT = "treatment"
    SYMPTOM = "symptom"
    DAILY_DIGEST = "daily_digest"
    MOC = "map_of_content"  # Map of Content


@dataclass
class VaultDocument:
    """Represents a document in the Obsidian vault"""
    path: str
    title: str
    note_type: NoteType
    
    # Content
    content: str = ""
    frontmatter: Dict[str, Any] = field(default_factory=dict)
    
    # Relationships
    links_to: List[str] = field(default_factory=list)
    linked_from: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    checksum: str = ""
    
    def __post_init__(self):
        if not self.checksum and self.content:
            self.checksum = hashlib.md5(self.content.encode()).hexdigest()


@dataclass
class KnowledgeNode:
    """Node in the knowledge graph"""
    node_id: str
    label: str
    node_type: str
    
    # Properties
    properties: Dict[str, Any] = field(default_factory=dict)
    
    # Connections
    edges: List['KnowledgeEdge'] = field(default_factory=list)
    
    # Scores
    importance_score: float = 0.0
    connection_count: int = 0


@dataclass
class KnowledgeEdge:
    """Edge in the knowledge graph"""
    source_id: str
    target_id: str
    relationship: str
    
    # Properties
    weight: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class KnowledgeGraph:
    """Complete knowledge graph from the vault"""
    nodes: Dict[str, KnowledgeNode] = field(default_factory=dict)
    edges: List[KnowledgeEdge] = field(default_factory=list)
    
    # Statistics
    total_nodes: int = 0
    total_edges: int = 0
    
    # Computed properties
    central_nodes: List[str] = field(default_factory=list)
    clusters: List[List[str]] = field(default_factory=list)
    
    def add_node(self, node: KnowledgeNode):
        """Add a node to the graph"""
        self.nodes[node.node_id] = node
        self.total_nodes = len(self.nodes)
    
    def add_edge(self, edge: KnowledgeEdge):
        """Add an edge to the graph"""
        self.edges.append(edge)
        self.total_edges = len(self.edges)
        
        # Update node edge lists
        if edge.source_id in self.nodes:
            self.nodes[edge.source_id].edges.append(edge)
            self.nodes[edge.source_id].connection_count += 1
        if edge.target_id in self.nodes:
            self.nodes[edge.target_id].connection_count += 1
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get all neighboring nodes"""
        neighbors = []
        for edge in self.edges:
            if edge.source_id == node_id:
                neighbors.append(edge.target_id)
            elif edge.target_id == node_id:
                neighbors.append(edge.source_id)
        return neighbors
    
    def compute_centrality(self):
        """Compute node centrality (simple degree centrality)"""
        for node_id, node in self.nodes.items():
            node.importance_score = node.connection_count / max(self.total_nodes, 1)
        
        # Find most central nodes
        sorted_nodes = sorted(
            self.nodes.items(),
            key=lambda x: x[1].importance_score,
            reverse=True
        )
        self.central_nodes = [n[0] for n in sorted_nodes[:10]]


class ObsidianBrain:
    """
    Obsidian vault integration for the Singularity Engine.
    
    This is the LONG-TERM MEMORY of the AI - your research vault becomes
    its brain. Every paper, every hypothesis, every insight is:
    
    1. Stored as Obsidian notes with proper linking
    2. Indexed for semantic search and retrieval
    3. Connected in a knowledge graph
    4. Used for continuous learning and improvement
    
    The vault grows smarter alongside the AI, creating a permanent
    record of all research conducted.
    """
    
    # Folder structure
    FOLDERS = {
        NoteType.PAPER: "Papers",
        NoteType.HYPOTHESIS: "Hypotheses",
        NoteType.SYNTHESIS: "Synthesis",
        NoteType.PROTEIN: "Biology/Proteins",
        NoteType.GENE: "Biology/Genes",
        NoteType.PATHWAY: "Biology/Pathways",
        NoteType.TREATMENT: "Treatments",
        NoteType.SYMPTOM: "Symptoms",
        NoteType.DAILY_DIGEST: "Daily Digests",
        NoteType.MOC: "Maps of Content"
    }
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.documents: Dict[str, VaultDocument] = {}
        self.knowledge_graph = KnowledgeGraph()
        
        # State
        self._connected = False
        self._watch_task: Optional[asyncio.Task] = None
        
        # Caches
        self._tag_index: Dict[str, List[str]] = {}
        self._link_index: Dict[str, List[str]] = {}
        
        logger.info("ObsidianBrain initialized", vault_path=str(vault_path))
    
    async def connect(self):
        """Connect to the Obsidian vault"""
        if not self.vault_path.exists():
            logger.info("Creating vault directory structure")
            self._create_vault_structure()
        
        # Load existing documents
        await self._load_vault()
        
        # Build knowledge graph
        await self._build_knowledge_graph()
        
        self._connected = True
        logger.info(
            "Connected to Obsidian vault",
            documents=len(self.documents),
            nodes=self.knowledge_graph.total_nodes,
            edges=self.knowledge_graph.total_edges
        )
    
    def _create_vault_structure(self):
        """Create the vault folder structure"""
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        for note_type, folder in self.FOLDERS.items():
            folder_path = self.vault_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create .obsidian config folder
        obsidian_config = self.vault_path / ".obsidian"
        obsidian_config.mkdir(exist_ok=True)
        
        # Create basic config
        app_config = {
            "alwaysUpdateLinks": True,
            "newFileLocation": "folder",
            "newFileFolderPath": "Inbox",
            "showLineNumber": True
        }
        
        with open(obsidian_config / "app.json", "w") as f:
            json.dump(app_config, f, indent=2)
    
    async def _load_vault(self):
        """Load all documents from the vault"""
        for md_file in self.vault_path.rglob("*.md"):
            try:
                doc = await self._parse_document(md_file)
                if doc:
                    self.documents[str(md_file.relative_to(self.vault_path))] = doc
            except Exception as e:
                logger.warning(f"Failed to parse {md_file}: {e}")
    
    async def _parse_document(self, file_path: Path) -> Optional[VaultDocument]:
        """Parse an Obsidian markdown document"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter = {}
        body = content
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    frontmatter = yaml.safe_load(parts[1]) or {}
                except ImportError:
                    # Parse simple key: value frontmatter
                    for line in parts[1].strip().split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            frontmatter[key.strip()] = value.strip()
                body = parts[2]
        
        # Extract links
        links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', body)
        
        # Extract tags
        tags = re.findall(r'#([a-zA-Z0-9_-]+)', body)
        
        # Determine note type from path
        note_type = NoteType.PAPER  # Default
        rel_path = str(file_path.relative_to(self.vault_path))
        for nt, folder in self.FOLDERS.items():
            if rel_path.startswith(folder):
                note_type = nt
                break
        
        return VaultDocument(
            path=rel_path,
            title=file_path.stem,
            note_type=note_type,
            content=body,
            frontmatter=frontmatter,
            links_to=links,
            tags=tags,
            modified_at=datetime.fromtimestamp(
                file_path.stat().st_mtime,
                tz=timezone.utc
            )
        )
    
    async def _build_knowledge_graph(self):
        """Build knowledge graph from documents"""
        # Create nodes from documents
        for path, doc in self.documents.items():
            node = KnowledgeNode(
                node_id=doc.title,
                label=doc.title,
                node_type=doc.note_type.value,
                properties={
                    "path": path,
                    "tags": doc.tags,
                    "frontmatter": doc.frontmatter
                }
            )
            self.knowledge_graph.add_node(node)
        
        # Create edges from links
        for path, doc in self.documents.items():
            for link in doc.links_to:
                edge = KnowledgeEdge(
                    source_id=doc.title,
                    target_id=link,
                    relationship="links_to"
                )
                self.knowledge_graph.add_edge(edge)
        
        # Compute centrality
        self.knowledge_graph.compute_centrality()
    
    async def add_paper(self, paper) -> str:
        """Add a research paper to the vault"""
        # Generate filename
        safe_title = re.sub(r'[^\w\s-]', '', paper.title)[:50]
        filename = f"{safe_title.strip()}.md"
        folder = self.FOLDERS[NoteType.PAPER]
        file_path = self.vault_path / folder / filename
        
        # Generate content
        content = self._generate_paper_note(paper)
        
        # Write file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # Update internal state
        doc = await self._parse_document(file_path)
        if doc:
            self.documents[str(file_path.relative_to(self.vault_path))] = doc
            
            # Update knowledge graph
            node = KnowledgeNode(
                node_id=doc.title,
                label=doc.title,
                node_type=NoteType.PAPER.value,
                properties={"paper_id": paper.paper_id}
            )
            self.knowledge_graph.add_node(node)
        
        logger.debug(f"Added paper to vault: {filename}")
        return str(file_path.relative_to(self.vault_path))
    
    def _generate_paper_note(self, paper) -> str:
        """Generate Obsidian note content for a paper"""
        frontmatter = f"""---
paper_id: {paper.paper_id}
doi: {paper.doi or 'N/A'}
pmid: {paper.pmid or 'N/A'}
journal: {paper.journal}
publication_date: {paper.publication_date.strftime('%Y-%m-%d')}
relevance_score: {paper.relevance_score:.2f}
novelty_score: {paper.novelty_score:.2f}
processed_at: {datetime.now(timezone.utc).isoformat()}
tags: [paper, research, singularity-engine]
---

"""
        
        # Build body
        body = f"# {paper.title}\n\n"
        body += f"**Authors:** {', '.join(paper.authors)}\n"
        body += f"**Journal:** {paper.journal}\n"
        body += f"**Published:** {paper.publication_date.strftime('%Y-%m-%d')}\n\n"
        
        body += "## Abstract\n\n"
        body += f"{paper.abstract}\n\n"
        
        if paper.key_findings:
            body += "## Key Findings\n\n"
            for finding in paper.key_findings:
                body += f"- {finding}\n"
            body += "\n"
        
        if paper.related_proteins:
            body += "## Related Proteins\n\n"
            for protein in paper.related_proteins:
                body += f"- [[{protein}]]\n"
            body += "\n"
        
        if paper.related_genes:
            body += "## Related Genes\n\n"
            for gene in paper.related_genes:
                body += f"- [[{gene}]]\n"
            body += "\n"
        
        body += "## AI Analysis\n\n"
        body += f"- **Relevance Score:** {paper.relevance_score:.2f}\n"
        body += f"- **Novelty Score:** {paper.novelty_score:.2f}\n\n"
        
        body += "## Notes\n\n"
        body += "*Add your notes here...*\n"
        
        return frontmatter + body
    
    async def add_hypothesis(self, hypothesis) -> str:
        """Add a research hypothesis to the vault"""
        # Generate filename
        filename = f"Hypothesis_{hypothesis.hypothesis_id}.md"
        folder = self.FOLDERS[NoteType.HYPOTHESIS]
        file_path = self.vault_path / folder / filename
        
        # Generate content
        content = self._generate_hypothesis_note(hypothesis)
        
        # Write file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.debug(f"Added hypothesis to vault: {filename}")
        return str(file_path.relative_to(self.vault_path))
    
    def _generate_hypothesis_note(self, hypothesis) -> str:
        """Generate Obsidian note content for a hypothesis"""
        frontmatter = f"""---
hypothesis_id: {hypothesis.hypothesis_id}
confidence_score: {hypothesis.confidence_score:.2f}
novelty_score: {hypothesis.novelty_score:.2f}
therapeutic_potential: {hypothesis.therapeutic_potential:.2f}
validated: {hypothesis.validated}
generated_at: {hypothesis.generated_at.isoformat()}
generating_agent: {hypothesis.generating_agent}
tags: [hypothesis, research, singularity-engine, {'validated' if hypothesis.validated else 'pending'}]
---

"""
        
        body = f"# Hypothesis: {hypothesis.hypothesis_id}\n\n"
        body += "## Statement\n\n"
        body += f"> {hypothesis.statement}\n\n"
        
        body += "## Rationale\n\n"
        body += f"{hypothesis.rationale}\n\n"
        
        body += "## Supporting Evidence\n\n"
        for paper_id in hypothesis.supporting_papers:
            body += f"- [[{paper_id}]]\n"
        body += "\n"
        
        if hypothesis.target_pathways:
            body += "## Target Pathways\n\n"
            for pathway in hypothesis.target_pathways:
                body += f"- [[{pathway}]]\n"
            body += "\n"
        
        if hypothesis.suggested_experiments:
            body += "## Suggested Experiments\n\n"
            for experiment in hypothesis.suggested_experiments:
                body += f"- [ ] {experiment}\n"
            body += "\n"
        
        body += "## Validation Status\n\n"
        body += f"- **Validated:** {'✅ Yes' if hypothesis.validated else '❌ No'}\n"
        body += f"- **Confidence:** {hypothesis.confidence_score:.2f}\n"
        body += f"- **Therapeutic Potential:** {hypothesis.therapeutic_potential:.2f}\n\n"
        
        if hypothesis.validation_results:
            body += "### Validation Results\n\n"
            for result in hypothesis.validation_results:
                body += f"```json\n{json.dumps(result, indent=2)}\n```\n\n"
        
        return frontmatter + body
    
    async def update_synthesis(self, synthesis: Dict[str, Any]) -> str:
        """Update or create synthesis note"""
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename = f"Synthesis_{date_str}.md"
        folder = self.FOLDERS[NoteType.SYNTHESIS]
        file_path = self.vault_path / folder / filename
        
        content = self._generate_synthesis_note(synthesis)
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.debug(f"Updated synthesis: {filename}")
        return str(file_path.relative_to(self.vault_path))
    
    def _generate_synthesis_note(self, synthesis: Dict[str, Any]) -> str:
        """Generate synthesis note content"""
        frontmatter = f"""---
disease: {synthesis.get('disease', 'Unknown')}
papers_analyzed: {synthesis.get('papers_analyzed', 0)}
hypotheses_generated: {synthesis.get('hypotheses_generated', 0)}
validated_hypotheses: {synthesis.get('validated_hypotheses', 0)}
confidence_level: {synthesis.get('confidence_level', 0):.2f}
timestamp: {synthesis.get('timestamp', datetime.now(timezone.utc).isoformat())}
tags: [synthesis, research-digest, singularity-engine]
---

"""
        
        body = f"# Research Synthesis - {synthesis.get('timestamp', 'Today')[:10]}\n\n"
        
        body += "## Overview\n\n"
        body += f"- **Disease Focus:** {synthesis.get('disease', 'Unknown')}\n"
        body += f"- **Papers Analyzed:** {synthesis.get('papers_analyzed', 0)}\n"
        body += f"- **Hypotheses Generated:** {synthesis.get('hypotheses_generated', 0)}\n"
        body += f"- **Validated Hypotheses:** {synthesis.get('validated_hypotheses', 0)}\n"
        body += f"- **Confidence Level:** {synthesis.get('confidence_level', 0):.1%}\n\n"
        
        body += "## Top Findings\n\n"
        for i, finding in enumerate(synthesis.get('top_findings', []), 1):
            body += f"### {i}. {finding.get('hypothesis', 'Finding')[:100]}...\n\n"
            body += f"- Confidence: {finding.get('confidence', 0):.2f}\n"
            body += f"- Therapeutic Potential: {finding.get('therapeutic_potential', 0):.2f}\n\n"
        
        body += "## Recommended Next Steps\n\n"
        for step in synthesis.get('recommended_next_steps', []):
            body += f"- [ ] {step}\n"
        body += "\n"
        
        body += "## Notes\n\n"
        body += "*Add your observations and action items here...*\n"
        
        return frontmatter + body
    
    async def search(
        self,
        query: str,
        note_types: Optional[List[NoteType]] = None,
        limit: int = 20
    ) -> List[VaultDocument]:
        """Search documents in the vault"""
        results = []
        query_lower = query.lower()
        
        for path, doc in self.documents.items():
            # Filter by note type
            if note_types and doc.note_type not in note_types:
                continue
            
            # Simple text search
            if (query_lower in doc.title.lower() or
                query_lower in doc.content.lower() or
                any(query_lower in tag.lower() for tag in doc.tags)):
                results.append(doc)
        
        # Sort by relevance (simple: title match first)
        results.sort(
            key=lambda d: (
                query_lower in d.title.lower(),
                d.modified_at
            ),
            reverse=True
        )
        
        return results[:limit]
    
    async def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get a summary of the knowledge in the vault"""
        summary = {
            "total_documents": len(self.documents),
            "documents_by_type": {},
            "total_tags": 0,
            "unique_tags": set(),
            "total_links": 0,
            "knowledge_graph": {
                "nodes": self.knowledge_graph.total_nodes,
                "edges": self.knowledge_graph.total_edges,
                "central_topics": self.knowledge_graph.central_nodes[:5]
            }
        }
        
        for doc in self.documents.values():
            # Count by type
            type_name = doc.note_type.value
            summary["documents_by_type"][type_name] = \
                summary["documents_by_type"].get(type_name, 0) + 1
            
            # Count tags
            summary["unique_tags"].update(doc.tags)
            summary["total_tags"] += len(doc.tags)
            
            # Count links
            summary["total_links"] += len(doc.links_to)
        
        summary["unique_tags"] = len(summary["unique_tags"])
        
        return summary
    
    async def disconnect(self):
        """Disconnect from the vault"""
        if self._watch_task:
            self._watch_task.cancel()
        
        self._connected = False
        logger.info("Disconnected from Obsidian vault")
