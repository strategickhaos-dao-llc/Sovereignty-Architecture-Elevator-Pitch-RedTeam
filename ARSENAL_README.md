# Arsenal Bibliography - Quick Start Guide

## 📚 What is the Arsenal Bibliography?

A curated collection of 100 foundational academic papers and technical specifications for sovereign AI systems. All resources are:
- ✅ Freely accessible (no paywalls, no logins)
- ✅ From trusted sources (.gov, .org, .edu, arXiv)
- ✅ Permanent and citation-grade
- ✅ Essential for AI reasoning and research

## 🚀 Quick Start

### Option 1: Download All Papers (Recommended)

```bash
# Download all 100 papers to ./arsenal_papers/
./arsenal-download.sh

# Or specify a custom directory
./arsenal-download.sh /opt/arsenal
```

### Option 2: Download with curl/wget

```bash
# Using the URL list
xargs -n 1 curl -L -s -O < arsenal.txt

# Or with wget
wget -i arsenal.txt
```

### Option 3: Browse the Bibliography

Read the full annotated bibliography:
```bash
# View in your browser or text editor
cat ARSENAL_BIBLIOGRAPHY.md
# Or open in your preferred markdown viewer
```

## 📂 Files in This Directory

| File | Purpose | Size |
|------|---------|------|
| `ARSENAL_BIBLIOGRAPHY.md` | Full annotated bibliography with descriptions | ~18KB |
| `arsenal.txt` | Plain text list of 100 URLs | ~6KB |
| `arsenal-download.sh` | Automated download script | ~6KB |
| `arsenal-metadata.jsonl` | Structured metadata for RAG/embeddings | ~31KB |

## 🤖 Integration with AI Systems

### For RAG (Retrieval-Augmented Generation)

```python
import json

# Load metadata
with open('arsenal-metadata.jsonl', 'r') as f:
    papers = [json.loads(line) for line in f]

# Each paper has:
# - id, title, authors, year, category
# - url, description, keywords

# Use for embeddings, vector databases, etc.
```

### For Knowledge Graphs

```python
# Build a knowledge graph from categories and keywords
categories = {}
for paper in papers:
    cat = paper['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(paper)
```

### For LLM Context

```bash
# Feed papers directly to your LLM's context window
cat arsenal_papers/*.pdf | llm-process-context
```

## 📊 Statistics

- **Total Papers**: 100
- **Categories**: 10 (10 papers each)
- **Time Span**: 1968 - 2024 (56 years)
- **Estimated Size**: ~500MB (all downloaded)
- **All Free**: 100% open access

## 🎯 Categories

1. **Computer Science & AI Foundations** (1-10)
   - Dijkstra, Lamport, Transformers, GPT, GFS, etc.

2. **Cryptography & Zero-Trust Canon** (11-20)
   - TLS, RSA, Ed25519, Signal, Noise Protocol, etc.

3. **Distributed Systems & Consensus** (21-30)
   - Raft, Paxos, FLP, MIT 6.824 lectures, etc.

4. **Law, Governance & Digital Sovereignty** (31-40)
   - GDPR, CLOUD Act, NIST AI RMF, EU AI Act, etc.

5. **Neuroscience & Collective Intelligence** (41-50)
   - Dunbar's number, swarm intelligence, complexity, etc.

6. **Mathematics & Formal Verification** (51-70)
   - Coq, Isabelle, Lean, TLA+, CompCert, seL4, etc.

7. **Open-Source Licensing & Ethics** (71-80)
   - GPL, MIT, Apache, Creative Commons, etc.

8. **Energy, Hardware & Embodied AI** (81-90)
   - RISC-V specs, energy efficiency, Green500, etc.

9. **Biology & Genome-Scale Engineering** (91-98)
   - CRISPR, AlphaFold, DNA storage, synthetic biology, etc.

10. **Miscellaneous Must-Know Papers** (99-100)
    - N-variant systems, persistent memory, etc.

## 🔧 Requirements

- **curl** or **wget** (for downloading)
- **Internet connection**
- **~500MB free disk space** (for all papers)

## 💡 Use Cases

### For Developers
- Reference implementation papers
- Understand foundational algorithms
- Learn from verified systems (seL4, CompCert)

### For Researchers
- Citation-grade sources
- Foundational papers in each domain
- Historical context for modern systems

### For AI Systems
- RAG knowledge base
- Fact-grounding and verification
- Sovereign reasoning without paywalls

### For Students
- Free, high-quality learning materials
- Essential papers in computer science
- No textbook costs

## 🔐 Security & Trust

All papers are from:
- **Government sources**: NIST, NREL, GPO, etc.
- **Academic institutions**: MIT, CMU, Stanford, etc.
- **Open archives**: arXiv, IACR, etc.
- **Standards bodies**: IETF, IEEE, W3C, etc.
- **Verified publishers**: Nature, Science (open access), etc.

## 🆘 Troubleshooting

### Download script fails
```bash
# Check dependencies
command -v curl || echo "Install curl"
command -v wget || echo "Install wget"

# Test a single download
curl -L -s -O https://arxiv.org/pdf/1706.03762.pdf
```

### Some papers don't download
Some URLs may be updated or moved over time. If a paper is unavailable:
1. Search for the paper title on arXiv or Google Scholar
2. Check the author's website
3. Use alternative sources (academia.edu, ResearchGate)

### Disk space issues
```bash
# Check available space
df -h .

# Download papers selectively by category
grep "arxiv.org" arsenal.txt | xargs -n 1 curl -L -s -O
```

## 📝 Contributing

Found a broken link or want to suggest a paper?

1. Check if the paper is freely accessible
2. Verify it's from a reputable source
3. Open an issue or PR with the suggestion

## 📄 License

This bibliography compilation: **CC0 1.0 (Public Domain)**  
Individual papers: Retain their original licenses

## 🔗 Related Resources

- [Main Repository README](README.md)
- [Sovereignty Architecture Documentation](SOVEREIGNTY_COMPLETE_V2.md)
- [AI Constitution](ai_constitution.yaml)
- [Community Guidelines](COMMUNITY.md)

---

**Built for the Strategickhaos Sovereignty Architecture**  
*Empowering sovereign AI systems with permanent, verifiable knowledge*

Last updated: 2024-11-23
