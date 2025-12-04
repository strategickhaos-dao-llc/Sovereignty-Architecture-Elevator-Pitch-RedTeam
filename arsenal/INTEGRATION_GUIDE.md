# Arsenal Bibliography - Integration Guide

This guide shows how to integrate the Arsenal Bibliography with various RAG (Retrieval-Augmented Generation) systems, vector databases, and LLM frameworks.

## Table of Contents

- [Quick Start](#quick-start)
- [LangChain Integration](#langchain-integration)
- [LlamaIndex Integration](#llamaindex-integration)
- [Haystack Integration](#haystack-integration)
- [Custom RAG Implementation](#custom-rag-implementation)
- [Vector Database Setup](#vector-database-setup)
- [Embedding Strategies](#embedding-strategies)
- [Multi-Agent Swarm Setup](#multi-agent-swarm-setup)

## Quick Start

### 1. Download All Papers

```bash
cd arsenal
./download_arsenal.sh
```

This will download all 100 papers to `arsenal/papers/`.

### 2. Load Metadata

```python
import json

# Load paper metadata
metadata = []
with open('arsenal/arsenal_metadata.jsonl', 'r') as f:
    for line in f:
        metadata.append(json.loads(line))

print(f"Loaded {len(metadata)} papers")
```

### 3. Choose Your Integration

Pick the framework that matches your stack and follow the appropriate section below.

---

## LangChain Integration

### Basic Setup

```python
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Step 1: Load all PDFs
loader = DirectoryLoader(
    './arsenal/papers/',
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True
)
documents = loader.load()

print(f"Loaded {len(documents)} document chunks")

# Step 2: Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
chunks = text_splitter.split_documents(documents)

# Step 3: Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./arsenal_vectorstore"
)

# Step 4: Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

# Step 5: Query the knowledge base
result = qa_chain.run("What is the Raft consensus algorithm?")
print(result)
```

### With Metadata Filtering

```python
from langchain.vectorstores import Chroma
import json

# Load metadata
papers_metadata = {}
with open('arsenal/arsenal_metadata.jsonl', 'r') as f:
    for line in f:
        paper = json.loads(line)
        papers_metadata[paper['url']] = paper

# Add metadata to documents
for doc in documents:
    url = doc.metadata.get('source')
    if url in papers_metadata:
        doc.metadata.update(papers_metadata[url])

# Now you can filter by category
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./arsenal_vectorstore"
)

# Query only cryptography papers
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": {"category": "Cryptography & Zero-Trust"}
    }
)
```

---

## LlamaIndex Integration

### Basic Setup

```python
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
    StorageContext,
)
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import OpenAI

# Step 1: Load documents
documents = SimpleDirectoryReader(
    './arsenal/papers/',
    required_exts=[".pdf"],
    recursive=True
).load_data()

print(f"Loaded {len(documents)} documents")

# Step 2: Create service context
service_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-4", temperature=0),
    embed_model=OpenAIEmbedding()
)

# Step 3: Build index
index = VectorStoreIndex.from_documents(
    documents,
    service_context=service_context,
    show_progress=True
)

# Step 4: Persist index
index.storage_context.persist(persist_dir="./arsenal_index")

# Step 5: Query
query_engine = index.as_query_engine()
response = query_engine.query("Explain the transformer architecture")
print(response)
```

### Loading Persisted Index

```python
from llama_index import load_index_from_storage, StorageContext

# Load previously created index
storage_context = StorageContext.from_defaults(persist_dir="./arsenal_index")
index = load_index_from_storage(storage_context)

# Query immediately
query_engine = index.as_query_engine()
response = query_engine.query("What is zero trust architecture?")
```

### With Custom Metadata

```python
import json
from llama_index import Document

# Load papers with metadata
papers_data = []
with open('arsenal/arsenal_metadata.jsonl', 'r') as f:
    for line in f:
        papers_data.append(json.loads(line))

# Load PDFs and attach metadata
documents = []
for paper in papers_data:
    # Assuming you have text extraction method
    doc = Document(
        text=extract_text_from_pdf(f"arsenal/papers/{paper['id']}.pdf"),
        metadata={
            "title": paper['title'],
            "author": paper['author'],
            "category": paper['category'],
            "topics": paper['topics'],
            "url": paper['url']
        }
    )
    documents.append(doc)
```

---

## Haystack Integration

### Basic Setup

```python
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import PDFToTextConverter, PreProcessor, EmbeddingRetriever
from haystack.pipelines import DocumentSearchPipeline
from pathlib import Path

# Step 1: Initialize document store
document_store = FAISSDocumentStore(
    faiss_index_factory_str="Flat",
    embedding_dim=768
)

# Step 2: Convert PDFs to text
converter = PDFToTextConverter()
preprocessor = PreProcessor(
    split_length=500,
    split_overlap=50,
    split_respect_sentence_boundary=True
)

# Step 3: Process all PDFs
papers_dir = Path("arsenal/papers")
documents = []

for pdf_path in papers_dir.glob("*.pdf"):
    # Convert PDF
    converted_docs = converter.convert(file_path=pdf_path)
    # Preprocess
    processed_docs = preprocessor.process(converted_docs)
    documents.extend(processed_docs)

# Step 4: Write to document store
document_store.write_documents(documents)

# Step 5: Create embeddings
retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/all-MiniLM-L6-v2"
)
document_store.update_embeddings(retriever)

# Step 6: Create pipeline
pipeline = DocumentSearchPipeline(retriever)

# Step 7: Query
results = pipeline.run(query="Explain Paxos consensus")
for doc in results['documents']:
    print(f"Score: {doc.score}")
    print(f"Content: {doc.content[:200]}...")
```

---

## Custom RAG Implementation

### Using Sentence Transformers + FAISS

```python
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from pathlib import Path

class ArsenalRAG:
    def __init__(self, papers_dir='arsenal/papers', metadata_file='arsenal/arsenal_metadata.jsonl'):
        self.papers_dir = Path(papers_dir)
        self.metadata_file = metadata_file
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.embeddings = None
        self.index = None
        
    def load_papers(self):
        """Load and process all papers"""
        # Load metadata
        metadata = {}
        with open(self.metadata_file, 'r') as f:
            for line in f:
                paper = json.loads(line)
                metadata[paper['id']] = paper
        
        # Extract text from PDFs
        for pdf_path in self.papers_dir.glob("*.pdf"):
            try:
                reader = PdfReader(str(pdf_path))
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                # Split into chunks
                chunks = self._chunk_text(text, chunk_size=500)
                
                # Store with metadata
                for chunk in chunks:
                    self.documents.append({
                        'text': chunk,
                        'source': pdf_path.name,
                        'metadata': metadata.get(pdf_path.stem, {})
                    })
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
    
    def _chunk_text(self, text, chunk_size=500, overlap=50):
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
    
    def create_embeddings(self):
        """Create embeddings for all document chunks"""
        texts = [doc['text'] for doc in self.documents]
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
    
    def search(self, query, k=5):
        """Search for relevant documents"""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            results.append({
                'document': self.documents[idx],
                'score': float(dist)
            })
        return results
    
    def save(self, index_path='arsenal_index.faiss', docs_path='arsenal_docs.json'):
        """Save index and documents"""
        faiss.write_index(self.index, index_path)
        with open(docs_path, 'w') as f:
            json.dump(self.documents, f)
    
    def load(self, index_path='arsenal_index.faiss', docs_path='arsenal_docs.json'):
        """Load saved index and documents"""
        self.index = faiss.read_index(index_path)
        with open(docs_path, 'r') as f:
            self.documents = json.load(f)

# Usage
rag = ArsenalRAG()
rag.load_papers()
rag.create_embeddings()
rag.save()

# Search
results = rag.search("What is the attention mechanism?", k=5)
for result in results:
    print(f"Score: {result['score']:.4f}")
    print(f"Source: {result['document']['source']}")
    print(f"Text: {result['document']['text'][:200]}...")
    print()
```

---

## Vector Database Setup

### Pinecone

```python
import pinecone
from sentence_transformers import SentenceTransformer

# Initialize Pinecone
pinecone.init(api_key="your-api-key", environment="us-west1-gcp")

# Create index
index_name = "arsenal-bibliography"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=384, metric="cosine")

index = pinecone.Index(index_name)

# Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Upload documents
for doc in documents:
    embedding = model.encode(doc['text'])
    index.upsert([(doc['id'], embedding.tolist(), doc['metadata'])])
```

### Weaviate

```python
import weaviate

# Connect to Weaviate
client = weaviate.Client("http://localhost:8080")

# Create schema
schema = {
    "classes": [{
        "class": "ArsenalPaper",
        "properties": [
            {"name": "title", "dataType": ["string"]},
            {"name": "content", "dataType": ["text"]},
            {"name": "category", "dataType": ["string"]},
            {"name": "author", "dataType": ["string"]},
            {"name": "url", "dataType": ["string"]},
        ]
    }]
}

client.schema.create(schema)

# Add documents
for doc in documents:
    client.data_object.create(
        data_object=doc,
        class_name="ArsenalPaper"
    )
```

### Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="arsenal_papers",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Upload vectors
client.upload_collection(
    collection_name="arsenal_papers",
    vectors=embeddings,
    payload=metadata_list
)
```

---

## Embedding Strategies

### Hierarchical Embeddings

```python
# Create separate embeddings for different granularities
class HierarchicalEmbedder:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def embed_document(self, text):
        """Embed at document, section, and chunk level"""
        return {
            'document': self.model.encode([text[:5000]])[0],  # Summary
            'sections': [self.model.encode([s])[0] for s in self.split_sections(text)],
            'chunks': [self.model.encode([c])[0] for c in self.chunk_text(text)]
        }
```

### Multi-Vector Retrieval

```python
# Use different embedding models for different aspects
from sentence_transformers import SentenceTransformer

models = {
    'semantic': SentenceTransformer('all-MiniLM-L6-v2'),
    'technical': SentenceTransformer('allenai-specter'),
    'code': SentenceTransformer('microsoft/codebert-base')
}

def multi_vector_embed(text):
    return {
        name: model.encode([text])[0]
        for name, model in models.items()
    }
```

---

## Multi-Agent Swarm Setup

### Category-Specific Agents

```python
import json

# Define agent specializations
agent_configs = {
    'crypto_agent': {
        'name': 'Cryptography Specialist',
        'categories': ['Cryptography & Zero-Trust'],
        'system_prompt': 'You are an expert in cryptography and security protocols.'
    },
    'consensus_agent': {
        'name': 'Distributed Systems Expert',
        'categories': ['Distributed Systems & Consensus'],
        'system_prompt': 'You specialize in consensus algorithms and distributed computing.'
    },
    'ai_agent': {
        'name': 'AI Foundations Specialist',
        'categories': ['Computer Science & AI Foundations'],
        'system_prompt': 'You are an expert in AI architectures and machine learning.'
    }
}

# Load metadata and filter by category
def load_agent_knowledge(agent_name, metadata_file='arsenal/arsenal_metadata.jsonl'):
    config = agent_configs[agent_name]
    papers = []
    
    with open(metadata_file, 'r') as f:
        for line in f:
            paper = json.loads(line)
            if paper['category'] in config['categories']:
                papers.append(paper)
    
    return papers

# Create agent-specific vector stores
for agent_name in agent_configs:
    papers = load_agent_knowledge(agent_name)
    print(f"{agent_name}: {len(papers)} papers")
    # Create specialized vector store for this agent
```

### Orchestration Example

```python
class ArsenalSwarm:
    def __init__(self):
        self.agents = {}
        for name, config in agent_configs.items():
            self.agents[name] = self.create_agent(name, config)
    
    def create_agent(self, name, config):
        """Create specialized agent with filtered knowledge"""
        # Load only relevant papers
        papers = load_agent_knowledge(name)
        
        # Create agent-specific RAG
        rag = ArsenalRAG()
        rag.load_papers_filtered(config['categories'])
        rag.create_embeddings()
        
        return {
            'name': config['name'],
            'rag': rag,
            'prompt': config['system_prompt']
        }
    
    def route_query(self, query):
        """Route query to appropriate agent"""
        # Use simple keyword matching or ML classifier
        if 'crypto' in query.lower() or 'security' in query.lower():
            return self.agents['crypto_agent']
        elif 'consensus' in query.lower() or 'distributed' in query.lower():
            return self.agents['consensus_agent']
        else:
            return self.agents['ai_agent']
    
    def query(self, question):
        """Answer question using appropriate specialist"""
        agent = self.route_query(question)
        results = agent['rag'].search(question, k=5)
        
        # Format context for LLM
        context = "\n\n".join([r['document']['text'] for r in results])
        
        # Call LLM with agent's system prompt and context
        return self.call_llm(agent['prompt'], context, question)

# Usage
swarm = ArsenalSwarm()
answer = swarm.query("How does TLS 1.3 improve security?")
```

---

## Best Practices

### 1. Chunk Size Optimization

```python
# Experiment with different chunk sizes for your use case
chunk_configs = [
    {'size': 500, 'overlap': 50},   # Small chunks, precise retrieval
    {'size': 1000, 'overlap': 200}, # Medium chunks, balanced
    {'size': 2000, 'overlap': 400}, # Large chunks, more context
]
```

### 2. Hybrid Search

```python
# Combine semantic search with keyword matching
from rank_bm25 import BM25Okapi

class HybridRetriever:
    def __init__(self, documents):
        self.semantic = SentenceTransformer('all-MiniLM-L6-v2')
        self.bm25 = BM25Okapi([doc.split() for doc in documents])
        self.documents = documents
    
    def search(self, query, k=5, alpha=0.5):
        # Semantic scores
        semantic_scores = self.semantic.encode([query])
        
        # BM25 scores
        bm25_scores = self.bm25.get_scores(query.split())
        
        # Combine scores
        combined = alpha * semantic_scores + (1 - alpha) * bm25_scores
        top_k = np.argsort(combined)[-k:]
        
        return [self.documents[i] for i in top_k]
```

### 3. Citation Tracking

```python
# Always track sources for attribution
def format_answer_with_citations(question, retrieved_docs, llm_answer):
    citations = []
    for i, doc in enumerate(retrieved_docs, 1):
        citations.append(f"[{i}] {doc['metadata']['title']} - {doc['metadata']['url']}")
    
    return f"{llm_answer}\n\nSources:\n" + "\n".join(citations)
```

---

## Troubleshooting

### PDF Extraction Issues

```python
# If PyPDF2 fails, try alternative extractors
from pdfminer.high_level import extract_text

def robust_pdf_extract(pdf_path):
    try:
        # Try PyPDF2 first
        reader = PdfReader(pdf_path)
        return " ".join(page.extract_text() for page in reader.pages)
    except:
        try:
            # Fall back to pdfminer
            return extract_text(pdf_path)
        except:
            print(f"Failed to extract: {pdf_path}")
            return ""
```

### Memory Management

```python
# For large collections, process in batches
def batch_embed(texts, model, batch_size=32):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(batch)
        embeddings.extend(batch_embeddings)
    return np.array(embeddings)
```

---

## Next Steps

1. **Performance Monitoring**: Track retrieval accuracy and latency
2. **Feedback Loop**: Collect user feedback to improve retrieval
3. **Regular Updates**: Re-download papers periodically for latest versions
4. **Custom Fine-tuning**: Fine-tune embedding models on your domain

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Integration is the path to sovereignty. Make this knowledge your own."*
