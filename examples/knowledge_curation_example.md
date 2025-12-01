# Knowledge Curation Examples

This document demonstrates practical examples of using the curl knowledge library.

## Example 1: Quick Single Download

Download a single philosophical text:

```bash
# Sun Tzu's Art of War
curl -L -s https://www.gutenberg.org/files/132/132-0.txt -o art_of_war.txt

# Read it
less art_of_war.txt

# Or feed directly to your AI
cat art_of_war.txt | your-ai-command
```

## Example 2: Download All 100 Sources

Run the complete automated script:

```bash
./curl_knowledge_library.sh
```

This creates the following structure:
```
knowledge/
├── math/          # 20 mathematical sources
├── ai/            # 20 AI/ML sources
├── pkm/           # 20 PKM/Obsidian sources
├── security/      # 20 security sources
└── esoteric/      # 20 philosophy sources
```

## Example 3: Selective Category Download

Download only math content by commenting out other sections in the script, or use this one-liner:

```bash
mkdir -p knowledge/math
curl -L -s https://oeis.org/A000796/b000796.txt -o knowledge/math/pi.txt
curl -L -s https://oeis.org/A000045/b000045.txt -o knowledge/math/fibonacci.txt
curl -L -s https://oeis.org/A000040/b000040.txt -o knowledge/math/primes.txt
```

## Example 4: Feed to Obsidian Vault

```bash
# Run the script
./curl_knowledge_library.sh

# Copy to Obsidian
cp -r knowledge/* /path/to/your/obsidian/vault/Library/

# Or create a symlink for auto-updates
ln -s $(pwd)/knowledge /path/to/your/vault/KnowledgeBase
```

## Example 5: Create RAG Vector Database

```bash
# Download all content
./curl_knowledge_library.sh

# Concatenate all text files
cat knowledge/**/*.txt knowledge/**/*.md > full_corpus.txt

# Feed to your vector database tool
# Examples:
# - ChromaDB: your-chroma-import full_corpus.txt
# - Pinecone: your-pinecone-upload full_corpus.txt
# - Weaviate: your-weaviate-import full_corpus.txt
```

## Example 6: Pipe Directly to AI (No Save)

```bash
# Get content and immediately feed to AI
curl -L -s https://www.gutenberg.org/files/132/132-0.txt | \
  your-local-llm "Summarize this text in 3 paragraphs"

# Or to clipboard (macOS)
curl -L -s https://www.gutenberg.org/files/132/132-0.txt | pbcopy
# Then paste into ChatGPT, Claude, etc.
```

## Example 7: Batch Process Multiple Sources

```bash
# Create a list of URLs
cat > my_sources.txt << EOF
https://www.gutenberg.org/files/132/132-0.txt
https://www.gutenberg.org/files/2680/2680-0.txt
https://www.gutenberg.org/files/216/216-0.txt
EOF

# Download all in parallel
cat my_sources.txt | xargs -P 3 -I {} bash -c 'curl -L -s {} -o "$(basename {}).txt"'
```

## Example 8: Integration with Continue.dev

```bash
# Download sources
./curl_knowledge_library.sh

# Copy to Continue.dev context directory
mkdir -p ~/.continue/context/knowledge
cp knowledge/**/*.txt ~/.continue/context/knowledge/
cp knowledge/**/*.md ~/.continue/context/knowledge/

# Now your Continue.dev has access to all this knowledge!
```

## Example 9: Daily Automated Updates

Add to your crontab:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/repo && ./curl_knowledge_library.sh >> logs/knowledge_update.log 2>&1
```

## Example 10: Custom Knowledge Base for Specific Domain

Create a custom script for only AI/ML content:

```bash
#!/bin/bash
mkdir -p knowledge/ai

# Ollama
curl -L -s https://raw.githubusercontent.com/ollama/ollama/main/README.md -o knowledge/ai/ollama.md

# LLaMA
curl -L -s https://raw.githubusercontent.com/meta-llama/llama/main/README.md -o knowledge/ai/llama.md

# LangChain
curl -L -s https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md -o knowledge/ai/langchain.md

echo "✅ AI knowledge base updated!"
```

## Tips and Best Practices

### 1. Version Control Your Knowledge Base

```bash
# Track changes over time
git add knowledge/
git commit -m "Updated knowledge base - $(date +%Y-%m-%d)"
git push
```

### 2. Create Backups

```bash
# Compress and backup
tar -czf knowledge_backup_$(date +%Y%m%d).tar.gz knowledge/

# Upload to cloud (example)
aws s3 cp knowledge_backup_$(date +%Y%m%d).tar.gz s3://your-bucket/
```

### 3. Filter Content by Size

```bash
# Only keep files larger than 10KB
find knowledge/ -type f -size -10k -delete
```

### 4. Search Across All Content

```bash
# Search for a term across all files
grep -r "strategy" knowledge/

# Case-insensitive search with context
grep -ri -C 3 "artificial intelligence" knowledge/
```

### 5. Generate Index

```bash
# Create an index of all downloaded files
find knowledge/ -type f -exec ls -lh {} \; > knowledge_index.txt
```

## Advanced Workflows

### Automated Content Analysis

```bash
# Download and analyze
./curl_knowledge_library.sh

# Count total words
find knowledge/ -type f -exec cat {} \; | wc -w

# Find most common words
find knowledge/ -type f -exec cat {} \; | \
  tr '[:space:]' '\n' | \
  grep -v '^\s*$' | \
  sort | uniq -c | sort -rn | head -20
```

### Multi-Language Translation

```bash
# Download English content and translate
curl -L -s https://www.gutenberg.org/files/132/132-0.txt | \
  your-translation-tool --to=es > art_of_war_spanish.txt
```

### PDF Conversion (if needed)

```bash
# Convert text files to PDF for reading
for file in knowledge/**/*.txt; do
  pandoc "$file" -o "${file%.txt}.pdf"
done
```

## Troubleshooting Examples

### Test Individual Download

```bash
# Verbose mode to see what's happening
curl -L -v https://www.gutenberg.org/files/132/132-0.txt -o test.txt

# Check if URL is accessible
curl -I https://www.gutenberg.org/files/132/132-0.txt
```

### Retry Failed Downloads

```bash
# Check which files failed (too small)
find knowledge/ -type f -size -1k -ls

# Remove and retry
find knowledge/ -type f -size -1k -delete
./curl_knowledge_library.sh
```

### Validate Content

```bash
# Check encoding
file knowledge/esoteric/art_of_war.txt

# Verify it's readable text
head -20 knowledge/esoteric/art_of_war.txt
```

---

**Remember**: All sources are public domain or open source. No authentication, API keys, or paywalls needed. Just pure knowledge, ready to feed your AI. ❤️
