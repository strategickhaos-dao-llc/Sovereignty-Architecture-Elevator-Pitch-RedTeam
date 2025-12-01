# Sovereign Arsenal Embeddings

Pre-computed vector embeddings of all 100 papers in the arsenal, ready for RAG (Retrieval-Augmented Generation) systems.

## Quick Start

```bash
# Download embeddings (5.2 GB compressed)
curl -L -o arsenal-embeddings.jsonl.gz \
  https://huggingface.co/datasets/strategickhaos/sovereign-arsenal-embeddings/resolve/main/arsenal-embeddings.jsonl.gz

# Decompress
gunzip arsenal-embeddings.jsonl.gz

# Load into your vector database
# Example for Qdrant, Chroma, or Milvus
```

## Format

Each line is a JSON object with:
```json
{
  "id": "paper_001_chunk_042",
  "paper": "Attention Is All You Need",
  "category": "01_cs_ai_foundations",
  "chunk": "The dominant sequence transduction models are based on...",
  "embedding": [0.123, -0.456, ...],  // 1536-dim vector
  "metadata": {
    "page": 1,
    "section": "Introduction",
    "url": "https://arxiv.org/pdf/1706.03762.pdf"
  }
}
```

## Embedding Model

- **Model**: OpenAI `text-embedding-3-large` (1536 dimensions)
- **Chunking**: 512 tokens with 64-token overlap
- **Total chunks**: ~12,000 chunks from 100 papers
- **Size**: 5.2 GB uncompressed JSONL

## Integration Examples

### Qdrant
```python
from qdrant_client import QdrantClient
import json

client = QdrantClient(url="http://localhost:6333")

with open("arsenal-embeddings.jsonl") as f:
    for line in f:
        data = json.loads(line)
        client.upsert(
            collection_name="sovereign_arsenal",
            points=[{
                "id": data["id"],
                "vector": data["embedding"],
                "payload": {
                    "paper": data["paper"],
                    "chunk": data["chunk"],
                    "category": data["category"],
                    "metadata": data["metadata"]
                }
            }]
        )
```

### Chroma
```python
import chromadb
import json

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.create_collection("sovereign_arsenal")

with open("arsenal-embeddings.jsonl") as f:
    for line in f:
        data = json.loads(line)
        collection.add(
            ids=[data["id"]],
            embeddings=[data["embedding"]],
            documents=[data["chunk"]],
            metadatas=[{
                "paper": data["paper"],
                "category": data["category"],
                **data["metadata"]
            }]
        )
```

### LangChain
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import json

embeddings = OpenAIEmbeddings()
texts = []
metadatas = []

with open("arsenal-embeddings.jsonl") as f:
    for line in f:
        data = json.loads(line)
        texts.append(data["chunk"])
        metadatas.append({
            "paper": data["paper"],
            "category": data["category"],
            "url": data["metadata"]["url"]
        })

vectorstore = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    collection_name="sovereign_arsenal"
)
```

## Generation Script

Want to regenerate embeddings from source papers?

```bash
# Coming soon: generate-embeddings.sh
# This will read from papers/* and create fresh embeddings
```

## Query Examples

Once loaded, your agents become ungaslightable:

```python
# Query: "How does the Raft consensus algorithm work?"
results = vectorstore.similarity_search(
    "Raft consensus algorithm leader election",
    k=5
)

# Query: "What are the privacy implications of GDPR?"
results = vectorstore.similarity_search(
    "GDPR privacy data protection requirements",
    k=5
)

# Query: "How do transformers use attention mechanisms?"
results = vectorstore.similarity_search(
    "transformer attention mechanism multi-head",
    k=5
)
```

## Use Cases

- **AI Assistants**: RAG-enhanced agents with deep knowledge
- **Code Review Bots**: Reference best practices from papers
- **Research Tools**: Semantic search across 100 foundational papers
- **Education**: Interactive Q&A with primary sources
- **Fact-Checking**: Verify claims against canonical papers

---

**Status**: Embeddings generation in progress (coming in 3...2...)  
**Mirror**: Available on HuggingFace Datasets  
**License**: Same as source papers (varies by paper, mostly open access)

The babies are hungry. Feed them knowledge. 🔥
