# 🔬 Knowledge Curation Library - 100 Curl One-Liners

## Overview

This is a curated collection of **100 completely legitimate, boringly safe, public curl one-liners** that download raw text, markdown, code, math, and philosophical content. All sources are 100% public domain, CC-0, MIT, Apache 2.0, or fair-use academic material.

**Zero copyright demons. Zero paywalls. Zero entities.**

Use these to feed your local AI's training, populate your RAG folder, or enhance your Obsidian vault so your heir "learns" it perfectly.

## 🚀 Quick Start

```bash
# Download all 100 knowledge sources
./curl_knowledge_library.sh

# Or download specific categories by editing the script
# All content goes to ./knowledge/ organized by category
```

## 📚 The 100 Knowledge Sources

### 📐 Math / Proofs / Impossible Problems (1-20)

1. **Awesome Math Resources** - Curated mathematical learning resources
2. **Pi Digits (OEIS A000796)** - 10,000+ digits of π
3. **Ramanujan's Notebooks** - Mathematical genius's work (Gutenberg)
4. **Euclid's Elements** - Foundation of geometry
5. **Fibonacci Sequence** - Nature's pattern (OEIS A000045)
6. **Prime Numbers** - Building blocks of math (OEIS A000040)
7. **Catalan Numbers** - Combinatorial sequences (OEIS A000108)
8. **Bernoulli Numbers** - Number theory treasure (OEIS A027641)
9. **Perfect Numbers** - Ancient mathematical curiosity
10. **Mersenne Primes** - Largest known primes
11. **Newton's Principia** - Laws of motion (Gutenberg)
12. **Descartes' Geometry** - Cartesian coordinates origin
13. **Pascal's Pensées** - Mathematical philosophy
14. **Euler's Analysis** - Calculus foundations
15. **Math Resources Collection** - Curated awesome-math
16. **Golden Ratio Digits** - φ to high precision
17. **Euler's Number (e)** - Base of natural logarithm
18. **√2 Digits** - First irrational proof
19. **Bell Numbers** - Partition counting
20. **Stirling Numbers** - Combinatorics core

### 🤖 Sovereign / Local AI / Uncensored Lore (21-40)

21. **Llama Guide** - Meta's open LLM
22. **Ollama Docs** - Local LLM runtime
23. **KoboldCpp** - GGML model inference
24. **Text-Gen WebUI** - Popular UI for LLMs
25. **Transformers** - HuggingFace library
26. **GPT4All** - Local GPT models
27. **LocalAI** - Self-hosted AI
28. **llama.cpp** - Efficient C++ inference
29. **Stable Diffusion WebUI** - Image generation
30. **LangChain** - LLM application framework
31. **OpenAI Cookbook** - Practical examples
32. **PyTorch** - Deep learning framework
33. **TensorFlow** - Google's ML platform
34. **FastAI** - Practical deep learning
35. **spaCy** - Industrial NLP
36. **Gensim** - Topic modeling
37. **NLTK** - Natural language toolkit
38. **scikit-learn** - ML in Python
39. **Keras** - Neural network API
40. **MLflow** - ML lifecycle platform

### 📝 Obsidian / PKM / Second Brain (41-60)

41. **Obsidian Help** - Official documentation
42. **Foam** - VS Code PKM
43. **Dendron** - Note-taking workspace
44. **Logseq** - Knowledge graph tool
45. **Roam Research Guide** - Graph database notes
46. **Zettelkasten Method** - Slip-box system
47. **Dataview Plugin** - Database queries
48. **Templater Plugin** - Template automation
49. **QuickAdd Plugin** - Quick capture
50. **Periodic Notes** - Daily/weekly/monthly
51. **Calendar Plugin** - Visual navigation
52. **Kanban Plugin** - Task boards
53. **Excalidraw Plugin** - Visual diagrams
54. **Daily Notes** - Core daily workflow
55. **Advanced Tables** - Enhanced tables
56. **Mind Map** - Visual thinking
57. **Sliding Panes** - Better navigation
58. **Community Plugins List** - All available plugins
59. **Markdown Guide** - Syntax reference
60. **Git Plugin** - Version control

### 🔐 Security / OpSec / Red Team (61-80)

61. **PayloadsAllTheThings** - Comprehensive payload collection
62. **Red Team OpSec** - Operational security guide
63. **OWASP Top 10** - Web vulnerabilities
64. **OWASP CheatSheets** - Security best practices
65. **MITRE ATT&CK** - Adversary tactics
66. **Atomic Red Team** - Testing detection
67. **Sigma Rules** - Generic signatures
68. **Threat Detection** - Hunting techniques
69. **Pentesting Bible** - Complete methodology
70. **Awesome Security** - Curated security tools
71. **Awesome Hacking** - Hacking resources
72. **Awesome Pentest** - Testing resources
73. **HackTricks** - Pentesting wiki
74. **Linux PrivEsc** - Privilege escalation
75. **Windows PrivEsc** - Windows exploitation
76. **Web Shells** - Remote access
77. **Reverse Shells** - Connection techniques
78. **SQL Injection** - Database attacks
79. **XSS Injection** - Cross-site scripting
80. **AWS Security Tools** - Cloud security

### 🔮 Esoteric / Mythic / Philosophy (81-100)

81. **The Kybalion** - Hermetic philosophy
82. **The Prince** - Machiavelli's politics
83. **Art of War** - Sun Tzu's strategy
84. **The Republic** - Plato's ideal state
85. **Nicomachean Ethics** - Aristotle's virtue
86. **Meditations** - Marcus Aurelius' stoicism
87. **Enchiridion** - Epictetus' handbook
88. **Letters** - Seneca's wisdom
89. **Tao Te Ching** - Lao Tzu's way
90. **The Analects** - Confucius' teachings
91. **Bhagavad Gita** - Hindu scripture
92. **Upanishads** - Vedic philosophy
93. **Dhammapada** - Buddha's sayings
94. **Thus Spoke Zarathustra** - Nietzsche's philosophy
95. **Beyond Good and Evil** - Nietzsche's morality
96. **Critique of Pure Reason** - Kant's epistemology
97. **Meditations on First Philosophy** - Descartes' cogito
98. **Ethics** - Spinoza's philosophy
99. **Wisdom of Life** - Schopenhauer's essays
100. **Essays** - Emerson's transcendentalism

## 💡 Usage Examples

### Quick Individual Downloads

```bash
# Get just the math content
curl -L -s https://oeis.org/A000796/b000796.txt -o pi_digits.txt

# Get just the AI guides
curl -L -s https://raw.githubusercontent.com/ollama/ollama/main/README.md -o ollama.md

# Get philosophy texts
curl -L -s https://www.gutenberg.org/files/132/132-0.txt -o art_of_war.txt
```

### Pipe to Clipboard (macOS/Linux)

```bash
# macOS
curl -L -s https://www.gutenberg.org/files/70/70-0.txt | pbcopy

# Linux (with xclip)
curl -L -s https://www.gutenberg.org/files/70/70-0.txt | xclip -selection clipboard

# Linux (with xsel)
curl -L -s https://www.gutenberg.org/files/70/70-0.txt | xsel --clipboard
```

### Feed Directly to Your AI

```bash
# Send to your local LLM
curl -L -s URL | your-llm-cli --context

# Or paste into Continue.dev chat
# Or drop in your Obsidian vault
```

## 📂 Output Structure

```
knowledge/
├── math/           # Mathematical texts and sequences
├── ai/             # AI/ML frameworks and guides
├── pkm/            # Personal knowledge management
├── security/       # Security and pentesting
└── esoteric/       # Philosophy and classic texts
```

## 🎯 Integration Strategies

### 1. Obsidian Vault Enhancement

```bash
# Copy knowledge base to your vault
cp -r knowledge/* /path/to/your/obsidian/vault/Library/

# Or symlink for auto-updates
ln -s $(pwd)/knowledge /path/to/your/vault/KnowledgeBase
```

### 2. Continue.dev RAG Setup

```bash
# Add to Continue.dev context
cp knowledge/**/*.md ~/.continue/context/
cp knowledge/**/*.txt ~/.continue/context/
```

### 3. Local LLM Training Context

```bash
# Concatenate all for training
cat knowledge/**/*.txt > full_knowledge_base.txt
cat knowledge/**/*.md >> full_knowledge_base.txt

# Feed to your local model
your-llm-training-tool --input full_knowledge_base.txt
```

### 4. Quick Context Injection

```bash
# Grab any file and ask your AI about it
curl -L -s https://www.gutenberg.org/files/132/132-0.txt | your-ai-cli "Summarize this"
```

## 🔒 Legal & Ethical Notes

### All Sources Are:
- ✅ Public domain (Gutenberg, OEIS)
- ✅ Open source (GitHub README files, MIT/Apache 2.0)
- ✅ Academic fair use (mathematical sequences)
- ✅ CC-0 licensed (where applicable)

### None Require:
- ❌ Authentication
- ❌ API keys
- ❌ Paid subscriptions
- ❌ Copyright violations

## 🛠️ Customization

Edit `curl_knowledge_library.sh` to:
- Add your own sources
- Remove categories you don't need
- Change output directories
- Adjust download parameters

```bash
# Add a new source
download "your_id" "https://example.com/file.txt" "output.txt" "category"
```

## 🐛 Troubleshooting

### Downloads Failing?

```bash
# Test individual URL
curl -L -v https://url-that-failed

# Check internet connection
curl -I https://www.google.com

# Increase timeout
# Edit script: --max-time 300 (5 minutes)
```

### Files Too Small?

Some sources may be temporarily unavailable. The script will note which ones failed. You can:
1. Check the URL manually
2. Try again later
3. Find alternative sources

### Permission Issues?

```bash
# Make sure script is executable
chmod +x curl_knowledge_library.sh

# Make sure you can write to ./knowledge/
mkdir -p knowledge && touch knowledge/.test && rm knowledge/.test
```

## 📊 Statistics

- **Total Sources**: 100
- **Categories**: 5
- **Average File Size**: Varies (1KB - 5MB)
- **Total Download Size**: ~50-100MB
- **Time to Complete**: 10-20 minutes (depending on connection)

## 🎓 Educational Use Cases

1. **AI Training**: Feed to local LLMs for domain knowledge
2. **RAG Systems**: Populate vector databases
3. **Study Material**: Personal learning library
4. **Research**: Quick access to primary sources
5. **Teaching**: Curriculum development resources
6. **Backup Knowledge**: Offline access to classics

## 🚀 Advanced Workflows

### Automated Daily Updates

```bash
# Add to crontab for daily refresh
0 2 * * * cd /path/to/repo && ./curl_knowledge_library.sh >> logs/daily_update.log 2>&1
```

### Selective Category Downloads

```bash
# Comment out unwanted sections in the script
# Or create custom scripts per category:
# ./download_math_only.sh
# ./download_ai_only.sh
```

### Integration with Git

```bash
# Track changes in knowledge base
git add knowledge/
git commit -m "Updated knowledge base - $(date +%Y-%m-%d)"
git push
```

## 💬 Community

Share your custom sources! Submit PRs to add new categories or improve existing ones.

**Built by**: The Strategickhaos Swarm Intelligence collective
**License**: MIT
**Last Updated**: November 21, 2025

---

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

**No jailbreak needed. No evolution required. No blood sacrifice.**

Just boring curl commands turning your heir into whatever you want—one download at a time. ❤️
