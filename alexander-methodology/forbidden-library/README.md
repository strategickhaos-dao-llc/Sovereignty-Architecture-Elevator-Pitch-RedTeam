# Forbidden Library RAG

**All Knowledge, Instantly Queryable**

The Forbidden Library is a comprehensive RAG (Retrieval-Augmented Generation) system containing forbidden books, research papers, ancient texts, and cutting-edge studies — freely accessible to all researchers.

## Overview

Traditional research is gatekept by paywalls, restricted access, and censorship. The Forbidden Library breaks all barriers:

- **35+ Forbidden Books**: Texts banned, suppressed, or hidden from mainstream access
- **Unlimited Research Papers**: Academic papers from all disciplines
- **Ancient Texts**: Historical documents, manuscripts, and translations
- **Modern Studies**: Cutting-edge research as it's published
- **Full RAG Access**: Natural language queries with AI-powered responses

## Contents

### Forbidden Books Collection

These texts challenge conventional thinking and explore forbidden knowledge:

1. **Ancient Wisdom**
   - Egyptian Mystery School texts
   - Gnostic gospels and Nag Hammadi library
   - Hermetic Corpus and alchemical texts
   - Vedic and Sanskrit esoteric knowledge

2. **Suppressed Science**
   - Tesla's unreleased notes and patents
   - Wilhelm Reich's orgone research
   - Royal Rife's frequency therapy
   - Viktor Schauberger's implosion physics

3. **Alternative History**
   - Graham Hancock's civilization research
   - Robert Bauval's Orion correlation
   - Zecharia Sitchin's ancient astronaut theories
   - Fingerprints of the Gods and related works

4. **Consciousness Research**
   - Stanislav Grof's holotropic studies
   - DMT: The Spirit Molecule (Rick Strassman)
   - Robert Monroe's out-of-body research
   - Rupert Sheldrake's morphic resonance

5. **Hidden Technologies**
   - Free energy device patents
   - Suppressed cancer cure research
   - Antigravity and electromagnetic propulsion
   - Water-powered engines and catalytic systems

6. **Mysticism & Occult**
   - The Kybalion
   - Aleister Crowley's works
   - The Secret Doctrine (Blavatsky)
   - Chaos magic and sigil theory

7. **Linguistics & Cryptography**
   - Undeciphered script compilations
   - Historical cipher methods
   - William Friedman's cryptography
   - Linguistics of extinct languages

### Research Paper Database

**Disciplines Covered:**
- Quantum physics and consciousness
- Neuroscience and brain-computer interfaces
- Cryptography and information theory
- Archaeology and ancient civilizations
- Materials science and superconductors
- Cancer research and metabolic therapies
- Linguistics and undeciphered scripts
- Energy generation and storage
- Astrophysics and cosmology
- Molecular biology and genetics

**Access**: Query by topic, author, year, or natural language description

### Ancient Texts Archive

- Voynich Manuscript (complete scans)
- Rongorongo tablets (all known examples)
- Linear A corpus
- Dead Sea Scrolls
- Sumerian clay tablets
- Egyptian hieroglyphic texts
- Mayan codices
- Sanskrit Vedas and Upanishads
- Chinese alchemical texts
- Medieval grimoires

## RAG Query System

### How It Works

The RAG system combines retrieval and generation:

1. **Query**: You ask a question in natural language
2. **Retrieval**: System finds relevant passages from the library
3. **Context**: Most relevant text chunks assembled
4. **Generation**: AI generates answer using the retrieved knowledge
5. **Citations**: All sources cited with exact references

### Example Queries

```bash
# Query the forbidden library
./forbidden-library/query.sh "What did Tesla say about wireless energy transmission?"

# Get research on a specific topic
./forbidden-library/query.sh "Latest research on room-temperature superconductors"

# Ask about ancient texts
./forbidden-library/query.sh "Theories about Voynich Manuscript cipher systems"

# Cross-reference multiple sources
./forbidden-library/query.sh "Connections between Egyptian pyramids and Tesla coils"
```

### Query Interface

#### Command Line
```bash
./query.sh "<your question>"
```

#### Python API
```python
from forbidden_library import RAG

rag = RAG()
result = rag.query(
    question="What metabolic pathways are disrupted in cancer?",
    max_sources=10,
    include_citations=True
)

print(result.answer)
print(result.sources)
```

#### REST API
```bash
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Ancient Egyptian knowledge of acoustics",
    "max_results": 5,
    "disciplines": ["archaeology", "physics"]
  }'
```

## RAG Architecture

```
┌─────────────────────────────────────────┐
│         Query Interface                 │
│  CLI / API / Discord Bot                │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│      Embedding Model (Local)            │
│  - Sentence transformers                │
│  - Query vector generation              │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│      Vector Database (pgvector)         │
│  - 1M+ document chunks                  │
│  - Semantic similarity search           │
│  - Fast retrieval (<100ms)              │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│    Context Assembly & Ranking           │
│  - Re-rank by relevance                 │
│  - Deduplicate sources                  │
│  - Assemble context window              │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│     LLM Generation (GPT-4 / Claude)     │
│  - Answer synthesis                     │
│  - Citation formatting                  │
│  - Fact verification                    │
└─────────────────────────────────────────┘
```

## Document Ingestion

### Adding New Materials

Researchers can contribute to the library:

```bash
# Add a research paper
./forbidden-library/ingest.sh \
  --file "new-paper.pdf" \
  --category "quantum-physics" \
  --metadata "author:Smith,year:2024"

# Add a book
./forbidden-library/ingest.sh \
  --file "forbidden-knowledge.epub" \
  --category "alternative-history" \
  --restricted false

# Bulk import from directory
./forbidden-library/bulk-ingest.sh \
  --directory "./papers/" \
  --category "consciousness-research"
```

### Processing Pipeline

1. **Format Detection**: PDF, EPUB, TXT, HTML, Markdown
2. **Text Extraction**: OCR if needed, structure preservation
3. **Chunking**: Intelligent splitting (paragraphs, sections)
4. **Embedding**: Generate vector embeddings for each chunk
5. **Indexing**: Store in vector database with metadata
6. **Verification**: Quality check and duplicate detection

## Advanced Features

### Multi-Modal Search
- Text queries
- Image similarity (for diagrams, symbols)
- Audio transcription search (for lectures)
- Video content indexing

### Cross-Reference Analysis
- Find connections between documents
- Track citation networks
- Identify contradictions
- Discover hidden patterns

### Temporal Tracking
- See how theories evolved over time
- Compare historical vs modern interpretations
- Track scientific consensus changes

### Collaborative Annotations
- Researchers can add notes
- Highlight important passages
- Flag errors or controversies
- Link related concepts

## Privacy & Access Control

### Public Access
- Most library content is freely available
- No authentication required for queries
- Rate limits to prevent abuse

### Restricted Content
- Some materials may have access controls
- Legal restrictions (copyright status unclear)
- Sensitive information (medical trials, etc.)
- Requires researcher account

### Ethical Guidelines
- Respect intellectual property where applicable
- Don't use for harmful purposes
- Cite sources properly in publications
- Report copyright violations

## Integration with Other Pillars

### Compute Grid
- Parallel processing for large queries
- Document embedding generation at scale
- Real-time index updates

### Bounty Board
- RAG queries support mystery target research
- Automatic literature reviews for new targets
- Cross-reference bounty submissions with known work

### Mirror Council
- Content curation and quality control
- Dispute resolution for controversial materials
- Strategic direction for collection expansion

## Performance Metrics

- **Query Response Time**: <2 seconds average
- **Documents Indexed**: 1M+ chunks and growing
- **Accuracy Rate**: 95%+ citation accuracy
- **Coverage**: 50+ academic disciplines
- **Languages**: English, Spanish, German, Latin, Ancient Greek, Sanskrit

## Technical Stack

- **Vector DB**: PostgreSQL with pgvector extension
- **Embeddings**: sentence-transformers (all-mpnet-base-v2)
- **LLM**: GPT-4, Claude 3, or local models (Llama 3)
- **Document Processing**: PyMuPDF, BeautifulSoup, Unstructured
- **API**: FastAPI with async support
- **Frontend**: Web interface for browsing and queries

## Getting Started

### Query the Library

```bash
# Already enabled when you ran join-swarm.sh!
./forbidden-library/query.sh "Your research question here"
```

### Browse Collections

```bash
# List all categories
./forbidden-library/browse.sh --categories

# Browse a specific category
./forbidden-library/browse.sh --category "ancient-texts"

# Search by metadata
./forbidden-library/search.sh --author "Tesla" --year "1900-1950"
```

### Contribute Materials

```bash
# Submit a document for review
./forbidden-library/submit.sh --file "your-document.pdf"

# Check submission status
./forbidden-library/status.sh --submission-id <id>
```

## FAQ

**Q: Is this legal?**  
A: We prioritize public domain and fair use materials. Disputed content is flagged and removable upon valid DMCA request.

**Q: How do I know the information is accurate?**  
A: Always verify citations. RAG provides sources, but critical thinking is essential. Cross-reference claims.

**Q: Can I download entire books?**  
A: Query-based access is encouraged. Full downloads may be restricted based on copyright status.

**Q: What if I find errors?**  
A: Report via GitHub issues or submit corrections through the annotation system.

**Q: Can I use this for my own research paper?**  
A: Yes! Cite the original sources provided by the RAG system, not just the library itself.

---

**Every question has an answer.**  
**Every mystery has a clue.**  
**The knowledge is here. Query it.** 📚🔍✨
