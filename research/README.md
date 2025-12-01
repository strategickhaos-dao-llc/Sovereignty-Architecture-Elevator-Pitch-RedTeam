# Distributed Department Research Automation

A comprehensive research automation system for distributed knowledge harvesting and evolutionary learning across organizational departments.

## 🎯 Overview

This system automates the collection of high-quality knowledge from trusted sources (.gov, .org, Google Scholar) for each department, enabling:

- **Distributed Knowledge Harvesting**: Each department gets curated research from 100+ trusted URLs
- **Silent Retrieval**: Non-intrusive batch fetching using `curl -L -s`
- **Parallel Processing**: Concurrent execution across departments or nodes
- **RAG/Embedding Ready**: Output formatted for vector embeddings and agent training

## 📁 Directory Structure

```
research/
├── departments/              # Department link files
│   ├── science_links.txt
│   ├── engineering_links.txt
│   ├── legal_links.txt
│   ├── medicine_links.txt
│   └── cybersecurity_links.txt
├── raw_pages/               # Downloaded HTML pages (auto-created)
│   ├── science/
│   ├── engineering/
│   ├── legal/
│   ├── medicine/
│   └── cybersecurity/
├── extracted_text/          # Processed text files (auto-created)
│   ├── science/
│   ├── engineering/
│   └── ...
├── fetch_research.sh        # Single department fetcher
├── fetch_all_departments.sh # Parallel batch processor
├── extract_text.py          # HTML to text extraction
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Fetch Research for a Single Department

```bash
# Fetch science department research
./fetch_research.sh science

# Fetch engineering research
./fetch_research.sh engineering

# Available departments: science, engineering, legal, medicine, cybersecurity
```

### 2. Fetch All Departments in Parallel

```bash
# Process all departments concurrently
./fetch_all_departments.sh

# Process sequentially (useful for rate limiting)
./fetch_all_departments.sh --sequential

# Process specific departments
./fetch_all_departments.sh -d science,engineering
```

### 3. Extract Text from HTML

```bash
# Extract text from all departments
python3 extract_text.py

# Extract text from specific departments
python3 extract_text.py science engineering

# Specify custom directories
python3 extract_text.py --raw-dir raw_pages --output-dir extracted_text
```

## 📊 Department Breakdown

| Department    | Focus Areas                                                  | Sources                              |
|---------------|--------------------------------------------------------------|--------------------------------------|
| Science       | Physics, Biology, Chemistry, Astronomy, Earth Sciences       | NASA, NSF, NIH, NOAA, Nature.org     |
| Engineering   | Mechanical, Electrical, Civil, Software, Materials           | NIST, IEEE, ASME, ASCE, DOE          |
| Legal         | Constitutional, Corporate, IP, Cyber, Criminal               | Supreme Court, DOJ, SEC, USPTO       |
| Medicine      | Clinical, Research, Public Health, Diagnostics               | NIH, CDC, FDA, Mayo Clinic           |
| Cybersecurity | Network Security, Cryptography, Threat Intelligence, Forensics| CISA, NIST, MITRE, OWASP, SANS      |

## 🔧 Features

### Intelligent Fetch Script (`fetch_research.sh`)

- **Silent Operation**: Uses `curl -L -s` for non-intrusive fetching
- **Retry Logic**: Automatic retry on failure with exponential backoff
- **Caching**: Skips already-downloaded files (checks size > 1KB)
- **Rate Limiting**: Built-in delays to be respectful to servers
- **Progress Tracking**: Real-time status with color-coded output
- **Metadata Generation**: Creates JSON metadata for each fetch

**Example Output:**
```
╔════════════════════════════════════════════╗
║  Distributed Research Automation v1.0     ║
║  Department: science                      ║
╚════════════════════════════════════════════╝

[1] Fetching: https://www.nasa.gov/... [OK] (45234 bytes)
[2] Fetching: https://www.nsf.gov/... [OK] (32156 bytes)
[3] Fetching: https://scholar.google.com/... [OK] (28945 bytes)

╔════════════════════════════════════════════╗
║  Collection Summary                        ║
╠════════════════════════════════════════════╣
║ Department:     science
║ Total URLs:     100
║ Successful:     95
║ Failed:         3
║ Cached:         2
║ Success Rate:   95%
║ Duration:       245s
║ Output Dir:     raw_pages/science
╚════════════════════════════════════════════╝
```

### Parallel Batch Processor (`fetch_all_departments.sh`)

- **Concurrent Execution**: Process all departments simultaneously
- **Sequential Mode**: Option for rate-limited sequential processing
- **Selective Processing**: Choose specific departments to process
- **Comprehensive Logging**: Individual logs for each department
- **Batch Metadata**: Summary statistics for entire batch run

### Text Extraction (`extract_text.py`)

- **Clean Text Extraction**: Removes HTML tags, scripts, styles
- **Smart Parsing**: Preserves meaningful content structure
- **Character Encoding**: Handles UTF-8 and other encodings
- **Quality Filtering**: Only saves files with substantial content (>100 chars)
- **Metadata Tracking**: Statistics for each department's extraction

## 🔄 Integration with RAG/Embedding Pipeline

### 1. Vector Embedding

```python
# Example using sentence-transformers
from sentence_transformers import SentenceTransformer
from pathlib import Path

model = SentenceTransformer('all-MiniLM-L6-v2')

# Process extracted text
text_dir = Path('research/extracted_text/science')
for text_file in text_dir.glob('*.txt'):
    with open(text_file, 'r') as f:
        text = f.read()
    embedding = model.encode(text)
    # Store embedding in vector database
```

### 2. RAG Integration

```python
# Example RAG setup
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load extracted texts
docs = []
for dept in ['science', 'engineering', 'legal', 'medicine', 'cybersecurity']:
    text_dir = Path(f'research/extracted_text/{dept}')
    for text_file in text_dir.glob('*.txt'):
        with open(text_file, 'r') as f:
            docs.append({
                'content': f.read(),
                'metadata': {'department': dept, 'source': text_file.name}
            })

# Split and embed
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(docs)
embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.from_documents(texts, embeddings)
```

## 🔐 Best Practices

### Rate Limiting

- Built-in 0.5s delay between requests
- Respectful to server resources
- Can be adjusted in `fetch_research.sh`

### User Agent

```bash
# Custom user agent identifies requests
User-Agent: Strategickhaos-Research-Bot/1.0
```

### Error Handling

- Automatic retry on transient failures
- 30-second timeout per request
- Failed requests logged but don't stop batch

### Data Quality

- Minimum file size check (1KB)
- Empty responses are discarded
- Metadata tracks success rates

## 🛠️ Customization

### Adding New Departments

1. Create a new link file:
```bash
touch research/departments/custom_dept_links.txt
```

2. Add URLs (one per line, comments start with #):
```
# Custom Department Links
https://example.gov/resource1
https://example.org/resource2
# More URLs...
```

3. Run the fetcher:
```bash
./fetch_research.sh custom_dept
```

### Modifying Source Lists

Edit existing link files in `departments/`:
```bash
nano research/departments/science_links.txt
```

Add, remove, or modify URLs as needed. Comments and blank lines are ignored.

### Adjusting Fetch Parameters

Edit `fetch_research.sh` to customize:
- Timeout: Change `--max-time 30`
- Retries: Change `--retry 2`
- Rate limit: Adjust `sleep 0.5`
- User agent: Modify `-H "User-Agent: ..."`

## 📈 Performance

### Single Department
- **Avg fetch time**: 2-3 minutes for 100 URLs
- **Success rate**: 90-95% typical
- **Output size**: 50-200MB per department

### Parallel Batch (All 5 Departments)
- **Avg total time**: 3-5 minutes (parallel mode)
- **Sequential time**: 10-15 minutes
- **Total output**: 250-1000MB

### Text Extraction
- **Processing speed**: ~500 files/minute
- **Size reduction**: ~40-60% from HTML to text
- **Quality**: Clean, embedding-ready text

## 🔍 Monitoring & Debugging

### Check Department Status

```bash
# View fetch log
cat research/raw_pages/science_fetch.log

# Check metadata
cat research/raw_pages/science/metadata.json | jq .

# View batch summary
cat research/raw_pages/batch_metadata.json | jq .
```

### Verify Data Quality

```bash
# Count successful fetches
ls research/raw_pages/science/*.html | wc -l

# Check file sizes
du -sh research/raw_pages/*/

# View extraction stats
cat research/extracted_text/science/extraction_metadata.json | jq .
```

### Re-fetch Failed URLs

The fetch script skips cached files automatically. To re-fetch:

```bash
# Remove cached files for a department
rm -rf research/raw_pages/science/

# Re-run fetch
./fetch_research.sh science
```

## 🎓 Example Workflows

### Workflow 1: Full Department Research Cycle

```bash
# 1. Fetch all department data
./fetch_all_departments.sh

# 2. Extract text from HTML
python3 extract_text.py

# 3. Review results
ls -lah research/extracted_text/*/

# 4. Feed into embedding pipeline
# (see Integration examples above)
```

### Workflow 2: Incremental Updates

```bash
# Fetch only science and medicine
./fetch_all_departments.sh -d science,medicine

# Extract only updated departments
python3 extract_text.py science medicine
```

### Workflow 3: Custom Department

```bash
# 1. Create custom link file
cat > research/departments/finance_links.txt << 'EOF'
# Finance Department Links
https://www.sec.gov/
https://www.treasury.gov/
https://www.federalreserve.gov/
# Add 97 more URLs...
EOF

# 2. Fetch custom department
./fetch_research.sh finance

# 3. Extract text
python3 extract_text.py finance
```

## 🤝 Contributing

To add new departments or enhance the system:

1. Follow the existing patterns in link files
2. Test fetch scripts with small samples first
3. Verify text extraction quality
4. Document any new departments or features

## 📝 License

This research automation system is part of the Sovereignty Architecture project.
See the main repository LICENSE file for details.

## 🔗 Related Documentation

- [Main README](../README.md) - Sovereignty Architecture overview
- [Discord Integration](../GITLENS_INTEGRATION.md) - DevOps automation
- [Security Playbook](../VAULT_SECURITY_PLAYBOOK.md) - Security guidelines

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Distributed knowledge harvesting for evolutionary learning"*
