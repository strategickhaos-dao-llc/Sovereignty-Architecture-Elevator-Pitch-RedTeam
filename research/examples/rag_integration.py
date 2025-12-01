#!/usr/bin/env python3
"""
RAG Integration Example for Research Automation
Demonstrates how to integrate extracted research into a RAG pipeline
"""

from pathlib import Path
from typing import List, Dict
import json


def load_department_texts(department: str, extracted_text_dir: Path) -> List[Dict]:
    """
    Load all extracted texts for a department
    
    Args:
        department: Department name (e.g., 'science', 'engineering')
        extracted_text_dir: Path to extracted_text directory
        
    Returns:
        List of documents with content and metadata
    """
    dept_dir = extracted_text_dir / department
    documents = []
    
    if not dept_dir.exists():
        print(f"Warning: Department directory not found: {dept_dir}")
        return documents
    
    # Load metadata if available
    metadata_file = dept_dir / "extraction_metadata.json"
    dept_metadata = {}
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            dept_metadata = json.load(f)
    
    # Load all text files
    for text_file in sorted(dept_dir.glob("page_*.txt")):
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 100:  # Only include substantial content
                documents.append({
                    'content': content,
                    'metadata': {
                        'department': department,
                        'source_file': text_file.name,
                        'char_count': len(content),
                        'dept_total_chars': dept_metadata.get('total_characters', 0),
                    }
                })
        except Exception as e:
            print(f"Error loading {text_file}: {e}")
    
    return documents


def example_simple_embedding():
    """
    Example 1: Simple embedding with sentence-transformers
    
    Install: pip install sentence-transformers
    """
    print("=" * 70)
    print("Example 1: Simple Embedding with sentence-transformers")
    print("=" * 70)
    print()
    
    # Pseudocode example
    example_code = '''
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load research texts
research_dir = Path('research/extracted_text')
all_docs = []
for dept in ['science', 'engineering', 'legal', 'medicine', 'cybersecurity']:
    all_docs.extend(load_department_texts(dept, research_dir))

# Embed documents
embeddings = []
for doc in all_docs:
    embedding = model.encode(doc['content'])
    embeddings.append({
        'vector': embedding,
        'metadata': doc['metadata'],
        'content': doc['content'][:500]  # Store snippet
    })

# Save embeddings
np.save('research_embeddings.npy', [e['vector'] for e in embeddings])
with open('research_metadata.json', 'w') as f:
    json.dump([{
        'metadata': e['metadata'],
        'content_snippet': e['content']
    } for e in embeddings], f)

print(f"Embedded {len(embeddings)} documents")
'''
    print(example_code)


def example_langchain_rag():
    """
    Example 2: LangChain RAG with FAISS
    
    Install: pip install langchain langchain-community faiss-cpu
    """
    print("\n" + "=" * 70)
    print("Example 2: LangChain RAG with FAISS Vector Store")
    print("=" * 70)
    print()
    
    example_code = '''
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Load research texts
research_dir = Path('research/extracted_text')
documents = []

for dept in ['science', 'engineering', 'legal', 'medicine', 'cybersecurity']:
    dept_docs = load_department_texts(dept, research_dir)
    for doc in dept_docs:
        documents.append(Document(
            page_content=doc['content'],
            metadata=doc['metadata']
        ))

print(f"Loaded {len(documents)} documents")

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
split_docs = text_splitter.split_documents(documents)
print(f"Split into {len(split_docs)} chunks")

# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector store
vectorstore = FAISS.from_documents(split_docs, embeddings)

# Save for later use
vectorstore.save_local("research_vectorstore")

# Query example
query = "What are the latest advances in machine learning?"
results = vectorstore.similarity_search(query, k=5)

for i, result in enumerate(results, 1):
    print(f"\\nResult {i}:")
    print(f"Department: {result.metadata['department']}")
    print(f"Content: {result.page_content[:200]}...")
'''
    print(example_code)


def example_chroma_rag():
    """
    Example 3: ChromaDB for persistent vector storage
    
    Install: pip install chromadb
    """
    print("\n" + "=" * 70)
    print("Example 3: ChromaDB Persistent Vector Store")
    print("=" * 70)
    print()
    
    example_code = '''
import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB client
# Note: Use absolute path in production (e.g., Path.cwd() / "research_chroma_db")
client = chromadb.PersistentClient(path="./research_chroma_db")

# Create embedding function
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create collection
collection = client.get_or_create_collection(
    name="research_knowledge",
    embedding_function=embedding_function
)

# Load and add documents
research_dir = Path('research/extracted_text')
departments = ['science', 'engineering', 'legal', 'medicine', 'cybersecurity']

doc_id = 0
for dept in departments:
    dept_docs = load_department_texts(dept, research_dir)
    
    for doc in dept_docs:
        collection.add(
            ids=[f"{dept}_{doc_id}"],
            documents=[doc['content']],
            metadatas=[{
                'department': dept,
                'source': doc['metadata']['source_file'],
                'char_count': doc['metadata']['char_count']
            }]
        )
        doc_id += 1

print(f"Added {doc_id} documents to ChromaDB")

# Query example
results = collection.query(
    query_texts=["artificial intelligence in healthcare"],
    n_results=5
)

for i, (doc, metadata) in enumerate(zip(results['documents'][0], 
                                         results['metadatas'][0]), 1):
    print(f"\\nResult {i}:")
    print(f"Department: {metadata['department']}")
    print(f"Content: {doc[:200]}...")
'''
    print(example_code)


def example_departmental_filtering():
    """
    Example 4: Department-specific RAG queries
    """
    print("\n" + "=" * 70)
    print("Example 4: Department-Specific Query Filtering")
    print("=" * 70)
    print()
    
    example_code = '''
# Use metadata filtering to query specific departments
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Load vectorstore
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("research_vectorstore", embeddings)

# Query only science department
query = "quantum computing applications"
results = vectorstore.similarity_search(
    query,
    k=5,
    filter={"department": "science"}
)

# Query multiple departments
departments_of_interest = ["engineering", "cybersecurity"]
results = vectorstore.similarity_search(
    query,
    k=10,
    filter={"department": {"$in": departments_of_interest}}
)

# Department-specific agent routing
def route_query_to_department(query: str) -> str:
    """Route queries to appropriate departments based on keywords"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['law', 'legal', 'court', 'regulation']):
        return 'legal'
    elif any(word in query_lower for word in ['security', 'cyber', 'threat', 'vulnerability']):
        return 'cybersecurity'
    elif any(word in query_lower for word in ['medical', 'health', 'disease', 'treatment']):
        return 'medicine'
    elif any(word in query_lower for word in ['physics', 'biology', 'chemistry']):
        return 'science'
    else:
        return 'engineering'

# Route and query
user_query = "network security best practices"
department = route_query_to_department(user_query)
results = vectorstore.similarity_search(
    user_query,
    k=5,
    filter={"department": department}
)
'''
    print(example_code)


def main():
    """Run all examples"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  Research Automation RAG Integration Examples                        ║
║  Demonstrates how to use extracted research in RAG pipelines         ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Show all examples
    example_simple_embedding()
    example_langchain_rag()
    example_chroma_rag()
    example_departmental_filtering()
    
    print("\n" + "=" * 70)
    print("Setup Instructions")
    print("=" * 70)
    print("""
1. Install required packages:
   pip install sentence-transformers langchain langchain-community faiss-cpu chromadb

2. Run research collection:
   cd research
   ./fetch_all_departments.sh
   python3 extract_text.py

3. Run any of the examples above to integrate with your RAG system

4. Customize embedding models, chunk sizes, and retrieval parameters
   based on your specific use case
    """)


if __name__ == '__main__':
    main()
