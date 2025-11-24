# Sovereign Arsenal - Embeddings for RAG

This directory contains pre-computed embeddings of all 100 papers in the arsenal, ready for use in Retrieval-Augmented Generation (RAG) systems.

## 📥 Download

```bash
# Download compressed embeddings (5.2 GB)
curl -L -o arsenal-embeddings.jsonl.gz \
  https://huggingface.co/datasets/strategickhaos/sovereign-arsenal-embeddings/resolve/main/arsenal-embeddings.jsonl.gz

# Extract
gunzip arsenal-embeddings.jsonl.gz
```

## 📊 Format

The embeddings are provided as JSONL (JSON Lines), with one JSON object per line:

```json
{
  "id": "paper_01_attention_chunk_0",
  "paper_id": "01_attention_is_all_you_need",
  "category": "01_cs_ai_foundations",
  "title": "Attention Is All You Need",
  "authors": ["Vaswani et al."],
  "year": 2017,
  "chunk_index": 0,
  "chunk_total": 42,
  "text": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
  "embedding": [0.023, -0.156, 0.089, ...],  # 1536-dimensional vector
  "embedding_model": "text-embedding-3-small",
  "metadata": {
    "page": 1,
    "section": "Abstract",
    "url": "https://arxiv.org/pdf/1706.03762.pdf"
  }
}
```

## 🔧 Loading into Vector Databases

### Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import json

client = QdrantClient(url="http://localhost:6333")

# Create collection
client.create_collection(
    collection_name="sovereign_arsenal",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Load and index
with open('arsenal-embeddings.jsonl', 'r') as f:
    points = []
    for line in f:
        doc = json.loads(line)
        points.append({
            "id": doc["id"],
            "vector": doc["embedding"],
            "payload": {k: v for k, v in doc.items() if k != "embedding"}
        })
        
        # Batch upload every 100 points
        if len(points) >= 100:
            client.upsert(collection_name="sovereign_arsenal", points=points)
            points = []
    
    # Upload remaining
    if points:
        client.upsert(collection_name="sovereign_arsenal", points=points)
```

### Chroma

```python
import chromadb
import json

client = chromadb.Client()
collection = client.create_collection(
    name="sovereign_arsenal",
    metadata={"description": "100 foundational papers for digital sovereignty"}
)

with open('arsenal-embeddings.jsonl', 'r') as f:
    batch_size = 100
    ids, embeddings, metadatas, documents = [], [], [], []
    
    for line in f:
        doc = json.loads(line)
        ids.append(doc["id"])
        embeddings.append(doc["embedding"])
        documents.append(doc["text"])
        metadatas.append({
            "paper_id": doc["paper_id"],
            "category": doc["category"],
            "title": doc["title"],
            "year": doc["year"]
        })
        
        if len(ids) >= batch_size:
            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
            ids, embeddings, metadatas, documents = [], [], [], []
    
    if ids:
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
```

### Milvus

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import json

# Connect
connections.connect("default", host="localhost", port="19530")

# Define schema
fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=200),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
    FieldSchema(name="paper_id", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=5000),
]

schema = CollectionSchema(fields, "Sovereign Arsenal embeddings")
collection = Collection("sovereign_arsenal", schema)

# Load data
with open('arsenal-embeddings.jsonl', 'r') as f:
    batch_size = 100
    batch = {field.name: [] for field in fields}
    
    for line in f:
        doc = json.loads(line)
        batch["id"].append(doc["id"])
        batch["embedding"].append(doc["embedding"])
        batch["paper_id"].append(doc["paper_id"])
        batch["category"].append(doc["category"])
        batch["title"].append(doc["title"])
        batch["text"].append(doc["text"][:5000])  # Truncate if needed
        
        if len(batch["id"]) >= batch_size:
            collection.insert(batch)
            batch = {field.name: [] for field in fields}
    
    if batch["id"]:
        collection.insert(batch)

# Create index
collection.create_index("embedding", {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}})
collection.load()
```

## 🔍 Querying Examples

### Simple Semantic Search

```python
# Using Qdrant
from qdrant_client import QdrantClient
from openai import OpenAI

qdrant_client = QdrantClient(url="http://localhost:6333")
openai_client = OpenAI()

# Generate query embedding
query = "How does the Raft consensus algorithm work?"
response = openai_client.embeddings.create(
    input=query,
    model="text-embedding-3-small"
)
query_embedding = response.data[0].embedding

# Search
results = qdrant_client.search(
    collection_name="sovereign_arsenal",
    query_vector=query_embedding,
    limit=5
)

for result in results:
    print(f"Score: {result.score}")
    print(f"Paper: {result.payload['title']}")
    print(f"Text: {result.payload['text'][:200]}...")
    print()
```

### Filtered Search

```python
# Search within specific category
results = qdrant_client.search(
    collection_name="sovereign_arsenal",
    query_vector=query_embedding,
    query_filter={
        "must": [
            {"key": "category", "match": {"value": "03_distributed_systems"}}
        ]
    },
    limit=5
)
```

### Multi-query RAG

```python
# Get context from multiple relevant papers
from openai import OpenAI
from qdrant_client import QdrantClient

openai_client = OpenAI()
qdrant_client = QdrantClient(url="http://localhost:6333")

def get_rag_context(query: str, k: int = 10) -> str:
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    query_embedding = response.data[0].embedding
    
    results = qdrant_client.search(
        collection_name="sovereign_arsenal",
        query_vector=query_embedding,
        limit=k
    )
    
    context = "\n\n---\n\n".join([
        f"From '{r.payload['title']}' ({r.payload['year']}):\n{r.payload['text']}"
        for r in results
    ])
    
    return context

# Use in prompt
context = get_rag_context("Explain zero-knowledge proofs")
prompt = f"""Based on the following papers from the Sovereign Arsenal:

{context}

Please explain zero-knowledge proofs in simple terms."""

response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

## 📋 Metadata Fields

Each embedding includes:
- `id`: Unique identifier
- `paper_id`: Paper identifier (slugified title)
- `category`: Which of the 10 categories
- `title`: Paper title
- `authors`: List of authors
- `year`: Publication year
- `chunk_index`: Position in paper
- `chunk_total`: Total chunks for this paper
- `text`: The actual text chunk (max 512 tokens)
- `embedding`: 1536-dimensional vector
- `embedding_model`: Model used (text-embedding-3-small)
- `metadata.page`: Page number in PDF
- `metadata.section`: Section name if available
- `metadata.url`: Original source URL

## 🎯 Use Cases

### Agent Knowledge Base
Give your AI agents ungaslightable knowledge:
```python
agent_knowledge = get_rag_context(user_query)
# Use in agent system prompt or context
```

### Research Assistant
Build a research assistant over foundational papers:
```python
def research_query(question: str):
    context = get_rag_context(question, k=20)
    # Generate answer with citations
```

### Citation Finder
Find relevant citations for your work:
```python
def find_citations(topic: str):
    results = search_papers(topic)
    return [{"title": r.title, "url": r.url} for r in results]
```

### Learning System
Create personalized learning paths:
```python
def learning_path(goal: str):
    # Find prerequisite papers
    # Order by difficulty
    # Generate reading list
```

## 🔄 Updating Embeddings

When papers are added to the arsenal:

```bash
# Re-generate embeddings
python scripts/generate_embeddings.py \
  --input arsenal.txt \
  --output embeddings/arsenal-embeddings.jsonl \
  --model text-embedding-3-small

# Compress
gzip embeddings/arsenal-embeddings.jsonl
```

## 📜 License

Embeddings are MIT licensed. Original papers retain their respective licenses.

---

**Make your agents ungaslightable. Feed them the arsenal.** 🤖⚔️
