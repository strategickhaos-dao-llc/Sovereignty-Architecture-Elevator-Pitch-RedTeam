"""
Knowledge Ingestion Engine - Layer 1 of Self-Evolving Refinery
Feeds everything into the learning system from multiple sources
For her. Silent. Relentless. Self-improving.
"""

import asyncio
import hashlib
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional, Union

import structlog
from pydantic import BaseModel, Field

logger = structlog.get_logger()


class SourceType(Enum):
    """Types of knowledge sources"""
    FILESYSTEM = "filesystem"
    API = "api"
    INTERNAL = "internal"
    STREAM = "stream"
    STRUCTURED = "structured"


class ProcessingStep(Enum):
    """Processing pipeline steps"""
    TEXT_EXTRACTION = "text_extraction"
    ENTITY_RECOGNITION = "entity_recognition"
    RELATIONSHIP_MAPPING = "relationship_mapping"
    VECTOR_EMBEDDING = "vector_embedding"


@dataclass
class Document:
    """Represents an ingested document"""
    id: str
    source: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    entities: List[Dict[str, Any]] = field(default_factory=list)
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    embeddings: Optional[List[float]] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    checksum: str = ""

    def __post_init__(self):
        if not self.checksum:
            self.checksum = hashlib.sha256(self.content.encode()).hexdigest()[:16]


@dataclass
class Entity:
    """Recognized entity from medical text"""
    text: str
    type: str  # drug, protein, symptom, disease, gene
    start: int
    end: int
    confidence: float
    normalized_id: Optional[str] = None  # e.g., UMLS CUI, DrugBank ID
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship:
    """Relationship between entities"""
    source_entity: Entity
    target_entity: Entity
    relation_type: str  # causes, treats, inhibits, activates, binds_to
    confidence: float
    evidence: str
    source_document_id: str


class KnowledgeSourceConfig(BaseModel):
    """Configuration for a knowledge source"""
    name: str
    type: SourceType
    description: str
    path: Optional[str] = None
    endpoint: Optional[str] = None
    rate_limit: Optional[int] = None
    file_types: List[str] = Field(default_factory=list)
    queue: Optional[str] = None
    storage: Optional[str] = None
    channel: Optional[str] = None
    database: Optional[str] = None
    enabled: bool = True


class ProcessingConfig(BaseModel):
    """Configuration for processing pipeline"""
    entity_types: List[str] = ["drugs", "proteins", "symptoms", "diseases", "genes"]
    relation_types: List[str] = ["causes", "treats", "inhibits", "activates", "binds_to"]
    embedding_model: str = "BAAI/bge-large-en-v1.5"
    chunk_size: int = 512
    chunk_overlap: int = 128
    ocr_enabled: bool = True


class KnowledgeSource(ABC):
    """Abstract base class for knowledge sources"""

    def __init__(self, config: KnowledgeSourceConfig):
        self.config = config
        self.logger = structlog.get_logger().bind(source=config.name)

    @abstractmethod
    async def fetch_documents(self) -> AsyncIterator[Document]:
        """Fetch documents from the source"""
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the source is available"""
        raise NotImplementedError


class ObsidianVaultSource(KnowledgeSource):
    """Knowledge source from Obsidian vault"""

    def __init__(self, config: KnowledgeSourceConfig):
        super().__init__(config)
        self.vault_path = Path(config.path or os.environ.get("OBSIDIAN_VAULT_PATH", "/data/obsidian"))
        self.file_types = config.file_types or [".md", ".yaml", ".json"]

    async def fetch_documents(self) -> AsyncIterator[Document]:
        """Fetch all documents from Obsidian vault"""
        self.logger.info("Scanning Obsidian vault", path=str(self.vault_path))

        if not self.vault_path.exists():
            self.logger.warning("Vault path does not exist", path=str(self.vault_path))
            return

        for file_type in self.file_types:
            for file_path in self.vault_path.rglob(f"*{file_type}"):
                try:
                    content = file_path.read_text(encoding="utf-8")
                    relative_path = file_path.relative_to(self.vault_path)

                    # Extract frontmatter metadata
                    metadata = self._extract_frontmatter(content)
                    metadata["file_path"] = str(relative_path)
                    metadata["file_type"] = file_type

                    # Extract links and tags
                    metadata["links"] = self._extract_links(content)
                    metadata["tags"] = self._extract_tags(content)

                    yield Document(
                        id=f"obsidian:{relative_path}",
                        source=self.config.name,
                        content=content,
                        metadata=metadata
                    )

                except Exception as e:
                    self.logger.error("Failed to read file", file=str(file_path), error=str(e))

    async def health_check(self) -> bool:
        """Check if vault is accessible"""
        return self.vault_path.exists() and self.vault_path.is_dir()

    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter from markdown"""
        frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
        match = frontmatter_pattern.match(content)
        if match:
            try:
                import yaml
                return yaml.safe_load(match.group(1)) or {}
            except Exception:
                pass
        return {}

    def _extract_links(self, content: str) -> List[str]:
        """Extract Obsidian wiki-style links"""
        link_pattern = re.compile(r"\[\[(.*?)(?:\|.*?)?\]\]")
        return link_pattern.findall(content)

    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content"""
        tag_pattern = re.compile(r"#([a-zA-Z0-9_/-]+)")
        return list(set(tag_pattern.findall(content)))


class PubMedSource(KnowledgeSource):
    """Knowledge source from PubMed/PMC"""

    def __init__(self, config: KnowledgeSourceConfig):
        super().__init__(config)
        self.endpoint = config.endpoint or "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.rate_limit = config.rate_limit or 3

    async def fetch_documents(self, query: str = "", max_results: int = 1000) -> AsyncIterator[Document]:
        """Fetch papers from PubMed"""
        self.logger.info("Fetching from PubMed", query=query, max_results=max_results)

        # This is a placeholder - actual implementation would use the E-utilities API
        # For now, yield a placeholder document structure
        import httpx

        async with httpx.AsyncClient() as client:
            # Search for papers
            search_url = f"{self.endpoint}/esearch.fcgi"
            search_params = {
                "db": "pubmed",
                "term": query,
                "retmax": min(max_results, 10000),
                "retmode": "json"
            }

            try:
                response = await client.get(search_url, params=search_params)
                response.raise_for_status()
                data = response.json()

                id_list = data.get("esearchresult", {}).get("idlist", [])
                self.logger.info("Found papers", count=len(id_list))

                # Fetch each paper (with rate limiting)
                for pmid in id_list:
                    await asyncio.sleep(1.0 / self.rate_limit)

                    fetch_url = f"{self.endpoint}/efetch.fcgi"
                    fetch_params = {
                        "db": "pubmed",
                        "id": pmid,
                        "retmode": "xml"
                    }

                    try:
                        paper_response = await client.get(fetch_url, params=fetch_params)
                        paper_response.raise_for_status()

                        yield Document(
                            id=f"pubmed:{pmid}",
                            source=self.config.name,
                            content=paper_response.text,
                            metadata={
                                "pmid": pmid,
                                "source_type": "pubmed",
                                "fetched_at": datetime.now(timezone.utc).isoformat()
                            }
                        )
                    except Exception as e:
                        self.logger.error("Failed to fetch paper", pmid=pmid, error=str(e))

            except Exception as e:
                self.logger.error("Failed to search PubMed", error=str(e))

    async def health_check(self) -> bool:
        """Check if PubMed API is accessible"""
        import httpx

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.endpoint}/einfo.fcgi",
                    params={"db": "pubmed", "retmode": "json"}
                )
                return response.status_code == 200
        except Exception:
            return False


class ClinicalTrialsSource(KnowledgeSource):
    """Knowledge source from ClinicalTrials.gov"""

    def __init__(self, config: KnowledgeSourceConfig):
        super().__init__(config)
        self.endpoint = config.endpoint or "https://clinicaltrials.gov/api/v2"

    async def fetch_documents(self, condition: str = "", max_results: int = 1000) -> AsyncIterator[Document]:
        """Fetch clinical trials"""
        self.logger.info("Fetching clinical trials", condition=condition)

        import httpx

        async with httpx.AsyncClient() as client:
            search_url = f"{self.endpoint}/studies"
            params = {
                "query.cond": condition,
                "pageSize": min(max_results, 100),
                "format": "json"
            }

            try:
                response = await client.get(search_url, params=params)
                response.raise_for_status()
                data = response.json()

                studies = data.get("studies", [])
                self.logger.info("Found clinical trials", count=len(studies))

                for study in studies:
                    nct_id = study.get("protocolSection", {}).get(
                        "identificationModule", {}
                    ).get("nctId", "unknown")

                    yield Document(
                        id=f"clinicaltrials:{nct_id}",
                        source=self.config.name,
                        content=str(study),
                        metadata={
                            "nct_id": nct_id,
                            "source_type": "clinical_trials",
                            "status": study.get("protocolSection", {}).get(
                                "statusModule", {}
                            ).get("overallStatus", "unknown")
                        }
                    )

            except Exception as e:
                self.logger.error("Failed to fetch clinical trials", error=str(e))

    async def health_check(self) -> bool:
        """Check if ClinicalTrials.gov API is accessible"""
        import httpx

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.endpoint}/stats/size")
                return response.status_code == 200
        except Exception:
            return False


class EntityRecognizer:
    """Medical entity recognition using NER models"""

    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.entity_types = config.entity_types
        self.model = None

    async def initialize(self):
        """Initialize NER models"""
        logger.info("Initializing entity recognizer")
        # Placeholder for actual model initialization
        # Would use scispacy, biobert, etc.

    async def extract_entities(self, text: str) -> List[Entity]:
        """Extract medical entities from text"""
        entities = []

        # Simple pattern-based extraction as fallback
        # In production, this would use trained NER models

        # Drug patterns (simplified)
        drug_pattern = re.compile(
            r"\b([A-Z][a-z]+(?:mab|nib|zole|pril|sartan|statin|cillin|mycin|azole))\b",
            re.IGNORECASE
        )
        for match in drug_pattern.finditer(text):
            entities.append(Entity(
                text=match.group(1),
                type="drug",
                start=match.start(),
                end=match.end(),
                confidence=0.8
            ))

        # Protein patterns (simplified)
        protein_pattern = re.compile(r"\b([A-Z]{2,}[0-9]*[A-Z]*)\b")
        for match in protein_pattern.finditer(text):
            if len(match.group(1)) >= 3:
                entities.append(Entity(
                    text=match.group(1),
                    type="protein",
                    start=match.start(),
                    end=match.end(),
                    confidence=0.6
                ))

        return entities


class RelationshipExtractor:
    """Extract relationships between medical entities"""

    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.relation_types = config.relation_types

    async def extract_relationships(
        self,
        text: str,
        entities: List[Entity],
        document_id: str
    ) -> List[Relationship]:
        """Extract relationships between entities"""
        relationships = []

        # Simple co-occurrence based extraction
        # In production, would use trained relation extraction models

        for i, entity1 in enumerate(entities):
            for entity2 in entities[i + 1:]:
                # Check if entities are within proximity
                distance = abs(entity1.start - entity2.start)
                if distance < 500:  # Within 500 characters
                    # Determine relation type based on context
                    context = text[min(entity1.start, entity2.start):max(entity1.end, entity2.end)]

                    relation_type = self._infer_relation(context, entity1, entity2)
                    if relation_type:
                        relationships.append(Relationship(
                            source_entity=entity1,
                            target_entity=entity2,
                            relation_type=relation_type,
                            confidence=0.5,
                            evidence=context[:200],
                            source_document_id=document_id
                        ))

        return relationships

    def _infer_relation(self, context: str, entity1: Entity, entity2: Entity) -> Optional[str]:
        """Infer relation type from context"""
        context_lower = context.lower()

        relation_keywords = {
            "treats": ["treats", "treatment", "therapy", "therapeutic", "administered"],
            "causes": ["causes", "induces", "leads to", "results in", "triggers"],
            "inhibits": ["inhibits", "blocks", "suppresses", "prevents", "antagonist"],
            "activates": ["activates", "stimulates", "enhances", "promotes", "agonist"],
            "binds_to": ["binds", "receptor", "ligand", "affinity", "interaction"]
        }

        for relation, keywords in relation_keywords.items():
            if any(kw in context_lower for kw in keywords):
                return relation

        return None


class VectorEmbedder:
    """Generate vector embeddings for documents"""

    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.model_name = config.embedding_model
        self.chunk_size = config.chunk_size
        self.chunk_overlap = config.chunk_overlap
        self.model = None

    async def initialize(self):
        """Initialize embedding model"""
        logger.info("Initializing embedder", model=self.model_name)
        # Placeholder for actual model initialization
        # Would use sentence-transformers

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start = end - self.chunk_overlap
        return chunks

    async def embed(self, text: str) -> List[float]:
        """Generate embedding for text"""
        # Placeholder - would use actual embedding model
        # Returns dummy embedding
        return [0.0] * 1536  # OpenAI embedding dimension


class KnowledgeIngestionEngine:
    """
    Main knowledge ingestion engine - Layer 1 of Self-Evolving Refinery
    Coordinates all sources, processing, and storage
    """

    def __init__(
        self,
        sources: List[KnowledgeSourceConfig],
        processing_config: ProcessingConfig,
        knowledge_graph_url: str = "neo4j://localhost:7687/medical_knowledge",
        vector_store_url: str = "qdrant://localhost:6333/medical_vectors"
    ):
        self.sources: Dict[str, KnowledgeSource] = {}
        self.processing_config = processing_config
        self.knowledge_graph_url = knowledge_graph_url
        self.vector_store_url = vector_store_url

        self.entity_recognizer = EntityRecognizer(processing_config)
        self.relationship_extractor = RelationshipExtractor(processing_config)
        self.embedder = VectorEmbedder(processing_config)

        # Initialize sources
        for source_config in sources:
            self._register_source(source_config)

        # Statistics
        self.stats = {
            "documents_ingested": 0,
            "entities_extracted": 0,
            "relationships_found": 0,
            "errors": 0
        }

    def _register_source(self, config: KnowledgeSourceConfig):
        """Register a knowledge source"""
        source: KnowledgeSource

        if config.type == SourceType.FILESYSTEM:
            if "obsidian" in config.name.lower():
                source = ObsidianVaultSource(config)
            else:
                source = ObsidianVaultSource(config)  # Generic filesystem
        elif config.type == SourceType.API:
            if "pubmed" in config.name.lower():
                source = PubMedSource(config)
            elif "clinical" in config.name.lower():
                source = ClinicalTrialsSource(config)
            else:
                logger.warning("Unknown API source", name=config.name)
                return
        else:
            logger.warning("Unsupported source type", type=config.type, name=config.name)
            return

        self.sources[config.name] = source
        logger.info("Registered knowledge source", name=config.name, type=config.type.value)

    async def initialize(self):
        """Initialize all components"""
        logger.info("Initializing Knowledge Ingestion Engine")

        await self.entity_recognizer.initialize()
        await self.embedder.initialize()

        # Check source health
        for name, source in self.sources.items():
            healthy = await source.health_check()
            logger.info("Source health check", source=name, healthy=healthy)

    async def ingest_all(self) -> Dict[str, Any]:
        """Ingest from all enabled sources"""
        logger.info("Starting full ingestion cycle")

        results = {}
        for name, source in self.sources.items():
            if source.config.enabled:
                try:
                    count = await self._ingest_source(source)
                    results[name] = {"status": "success", "documents": count}
                except Exception as e:
                    logger.error("Failed to ingest source", source=name, error=str(e))
                    results[name] = {"status": "error", "error": str(e)}
                    self.stats["errors"] += 1

        results["statistics"] = self.stats
        return results

    async def ingest_source(self, source_name: str) -> Dict[str, Any]:
        """Ingest from a specific source"""
        if source_name not in self.sources:
            raise ValueError(f"Unknown source: {source_name}")

        source = self.sources[source_name]
        count = await self._ingest_source(source)
        return {"source": source_name, "documents": count}

    async def _ingest_source(self, source: KnowledgeSource) -> int:
        """Process documents from a source"""
        count = 0

        async for document in source.fetch_documents():
            try:
                # Process document through pipeline
                processed_doc = await self._process_document(document)

                # Store in knowledge graph and vector store
                await self._store_document(processed_doc)

                count += 1
                self.stats["documents_ingested"] += 1

                if count % 100 == 0:
                    logger.info(
                        "Ingestion progress",
                        source=source.config.name,
                        documents=count
                    )

            except Exception as e:
                logger.error(
                    "Failed to process document",
                    document_id=document.id,
                    error=str(e)
                )
                self.stats["errors"] += 1

        return count

    async def _process_document(self, document: Document) -> Document:
        """Process document through full pipeline"""

        # Step 1: Entity recognition
        entities = await self.entity_recognizer.extract_entities(document.content)
        document.entities = [
            {
                "text": e.text,
                "type": e.type,
                "start": e.start,
                "end": e.end,
                "confidence": e.confidence
            }
            for e in entities
        ]
        self.stats["entities_extracted"] += len(entities)

        # Step 2: Relationship extraction
        relationships = await self.relationship_extractor.extract_relationships(
            document.content,
            entities,
            document.id
        )
        document.relationships = [
            {
                "source": r.source_entity.text,
                "target": r.target_entity.text,
                "type": r.relation_type,
                "confidence": r.confidence
            }
            for r in relationships
        ]
        self.stats["relationships_found"] += len(relationships)

        # Step 3: Vector embedding
        document.embeddings = await self.embedder.embed(document.content)

        return document

    async def _store_document(self, document: Document):
        """Store processed document in knowledge graph and vector store"""
        # Placeholder for actual storage implementation
        # Would use neo4j for knowledge graph and qdrant for vectors
        logger.debug(
            "Storing document",
            document_id=document.id,
            entities=len(document.entities),
            relationships=len(document.relationships)
        )

    async def get_statistics(self) -> Dict[str, Any]:
        """Get ingestion statistics"""
        return {
            **self.stats,
            "sources": {
                name: {
                    "type": source.config.type.value,
                    "enabled": source.config.enabled
                }
                for name, source in self.sources.items()
            }
        }


# Factory function for creating ingestion engine from config
async def create_ingestion_engine(config_path: str) -> KnowledgeIngestionEngine:
    """Create ingestion engine from YAML config"""
    import yaml

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    layer_1_config = config.get("core_architecture", {}).get("refinery_layers", {}).get("layer_1_ingestion", {})

    sources = []
    for source_def in layer_1_config.get("sources", []):
        sources.append(KnowledgeSourceConfig(
            name=source_def.get("name", "unknown"),
            type=SourceType(source_def.get("type", "filesystem")),
            description=source_def.get("description", ""),
            path=source_def.get("path"),
            endpoint=source_def.get("endpoint"),
            rate_limit=source_def.get("rate_limit"),
            file_types=source_def.get("file_types", [])
        ))

    processing_config = ProcessingConfig(
        chunk_size=layer_1_config.get("processing_pipeline", {}).get("chunk_size", 512),
        chunk_overlap=layer_1_config.get("processing_pipeline", {}).get("chunk_overlap", 128)
    )

    output_config = layer_1_config.get("output", {})

    engine = KnowledgeIngestionEngine(
        sources=sources,
        processing_config=processing_config,
        knowledge_graph_url=output_config.get("knowledge_graph", "neo4j://localhost:7687"),
        vector_store_url=output_config.get("vector_store", "qdrant://localhost:6333")
    )

    await engine.initialize()
    return engine
