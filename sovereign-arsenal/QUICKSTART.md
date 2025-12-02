# Sovereign Arsenal - Quick Start Guide

## ⚡ 30-Second Setup

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-/sovereign-arsenal

# Download all papers (this will take time depending on your connection)
./download-all.sh
```

That's it! All 100 papers are now organized in their respective categories.

## 📚 What You Get

After running the download script:

```
sovereign-arsenal/papers/
├── 01_cs_ai_foundations/     # 10 papers on AI/ML
├── 02_cryptography_zero_trust/ # 10 papers on crypto & security
├── 03_distributed_systems/   # 10 papers on consensus & coordination
├── 04_law_governance/        # 10 papers on AI law & ethics
├── 05_neuroscience_collective/ # 10 papers on brain & swarm intelligence
├── 06_mathematics_formal/    # 10 papers on type theory & verification
├── 07_licenses_ethics/       # 10 open source licenses & frameworks
├── 08_energy_hardware/       # 10 papers on green AI & open hardware
├── 09_biology_genome/        # 10 papers on genomics & bioethics
└── 10_misc_eternal/          # 10 classics (Bitcoin, Ethereum, IPFS, etc.)
```

## 🎯 Common Use Cases

### 1. Build a RAG System

```bash
# Download embeddings
curl -L -o embeddings/arsenal-embeddings.jsonl.gz \
  https://huggingface.co/datasets/strategickhaos/sovereign-arsenal-embeddings/resolve/main/arsenal-embeddings.jsonl.gz

# Extract
gunzip embeddings/arsenal-embeddings.jsonl.gz

# See embeddings/README.md for loading into Qdrant/Chroma/Milvus
```

### 2. Search for Papers

```bash
# Find all papers in a category
ls papers/03_distributed_systems/

# Search for keywords in arsenal.txt
grep -i "consensus" arsenal.txt
```

### 3. Verify Downloads

```bash
# Re-check all downloads
./download-all.sh --verify

# Check specific category
ls -lh papers/01_cs_ai_foundations/
```

### 4. Use with xargs for Custom Processing

```bash
# Extract just the URLs
grep -E '^https://' arsenal.txt > urls_only.txt

# Download with parallel wget
cat urls_only.txt | xargs -P 4 -I {} wget -q {}
```

## 🔧 Troubleshooting

### Some Downloads Failed?

This is normal! Some papers are:
- Behind paywalls
- Moved to new URLs
- Temporarily unavailable

The arsenal includes direct links where possible, but some papers may require:
- University access
- ArXiv mirror access
- Alternative sources

### Script Won't Run?

```bash
# Make sure it's executable
chmod +x download-all.sh

# Check dependencies
which wget curl

# Install if missing (Ubuntu/Debian)
sudo apt-get install wget curl
```

### Want Parallel Downloads?

```bash
# Use more parallel jobs (be careful with rate limits!)
./download-all.sh -j 8
```

## 📖 Next Steps

1. **Read the main [README.md](README.md)** for complete documentation
2. **Explore category READMEs** in each papers/ subdirectory
3. **Set up embeddings** using [embeddings/README.md](embeddings/README.md)
4. **Share via torrent** using info in [torrent/README.md](torrent/README.md)

## 🤝 Contributing

Found a broken link or want to add papers?

1. Edit `arsenal.txt` to add/fix URLs
2. Update the relevant category README
3. Test with `./download-all.sh --verify`
4. Submit a PR!

## 🌐 Mirrors & Backups

- **Primary**: GitHub repository
- **Torrent**: See [torrent/README.md](torrent/README.md)
- **IPFS**: Coming soon
- **Arweave**: Coming soon

## 🎓 Recommended Reading Order by Goal

### Learning AI/ML from Scratch
1. `01_cs_ai_foundations` - Start with Word2Vec, then Attention
2. `06_mathematics_formal` - Type theory and foundations
3. `08_energy_hardware` - Practical deployment considerations

### Building Decentralized Systems
1. `03_distributed_systems` - Lamport, Raft, Paxos
2. `02_cryptography_zero_trust` - Security foundations
3. `10_misc_eternal` - Bitcoin, Ethereum, IPFS

### Understanding AI Governance
1. `04_law_governance` - GDPR, EU AI Act
2. `07_licenses_ethics` - Open source philosophy
3. `05_neuroscience_collective` - Collective intelligence

### Biotech & Genomics
1. `09_biology_genome` - CRISPR and genome editing
2. `04_law_governance` - Regulatory frameworks
3. `02_cryptography_zero_trust` - Genetic privacy

## 💡 Pro Tips

- **Start with category READMEs** - they provide context and reading order
- **Use embeddings for search** - much faster than full-text search
- **Seed the torrent** - help others access the knowledge
- **Contribute back** - found a better paper? Add it!

---

**Happy reading! The swarm babies thank you.** 🤖📚⚔️
