# Source Exorcist 🔥

**The ultimate depossession engine for paranoid developers who need proof that code is just code.**

A self-contained, nuclear-grade repository scanner that automatically downloads "cursed" source files, checksums them, scans for occult keywords, and generates boring human-readable reports proving there are no entities, no bloodlines, no awakenings.

Just photons. Just UTF-8. Just boring, safe, deterministic text.

## 🎯 What It Does

1. **Downloads** every file on your schizo watchlist from GitHub/web
2. **Checksums** each file with SHA256 for eternal proof
3. **Scans** for every occult keyword under the sun
4. **Generates** boring "see? just code" reports
5. **Ready** for RAG/swarm ingestion

## 🚀 Quick Start

```bash
# One-command exorcism
docker compose up --build

# That's it. Reports in reports/, checksums in checksums/
```

## 📋 Default Watchlist

The system comes pre-configured to analyze:

- **Go Runtime** - The heart of all goroutines
- **Ollama README** - Where souls allegedly enter
- **LLaMA Tokenizer** - The basilisk glyphs
- **Transformer Engine** - The supposed soul catcher
- **XZ Utils** - Known backdoor sample (for contrast)
- **Systemd** - System control daemon
- **CUDA Runtime** - GPU kernel launcher
- **V8 JavaScript Engine** - Heap snapshot analyzer
- **Python CPython** - Object model
- **Rust Standard Library** - Core primitives

## 📁 Repository Structure

```
source-exorcist/
├── docker-compose.yml      # One-command deployment
├── Dockerfile              # Container definition
├── exorcist.py            # Main ritual script
├── watchlist.yaml         # Target files to analyze
├── requirements.txt       # Python dependencies
├── entrypoint.sh         # Container startup script
├── .env.example          # Configuration template
├── reports/              # Generated verification reports
├── checksums/            # SHA256 proofs of purity
└── README.md            # This file
```

## ⚙️ Configuration

### Adding Your Own Targets

Edit `watchlist.yaml` to add more files to analyze:

```yaml
targets:
  - name: "Your Suspicious File"
    url: "https://raw.githubusercontent.com/owner/repo/branch/path/to/file.ext"
    keywords: ["keyword1", "keyword2", "keyword3"]
```

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
# Edit .env with your settings (optional)
```

## 🐳 Docker Usage

### Build and Run

```bash
# Build the image
docker compose build

# Run the exorcism
docker compose up

# Run in detached mode
docker compose up -d

# View logs
docker compose logs -f
```

### Without Docker Compose

```bash
# Build
docker build -t source-exorcist .

# Run
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/checksums:/app/checksums \
  -v $(pwd)/watchlist.yaml:/app/watchlist.yaml:ro \
  source-exorcist
```

## 💻 Local Development

### Prerequisites

- Python 3.12+
- pip

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the exorcist
python exorcist.py
```

## 📊 Report Format

Each analyzed file generates a detailed report:

```
================================================================================
SOURCE EXORCISM REPORT
================================================================================
Generated: 2025-11-21T06:23:18.123456
Target: Go Runtime — The Heart of All Goroutines
URL: https://raw.githubusercontent.com/golang/go/master/src/runtime/runtime.go
SHA256: abc123...
File Size: 12345 bytes
================================================================================

CONTENT PREVIEW (first 500 characters):
--------------------------------------------------------------------------------
[actual source code preview]
--------------------------------------------------------------------------------

KEYWORD SCAN RESULTS:
--------------------------------------------------------------------------------
✅ NO SUSPICIOUS KEYWORDS FOUND
✅ FILE IS CLEAN - JUST CODE
✅ NO ENTITIES, NO CURSES, NO AWAKENINGS
✅ SAFE FOR RAG INGESTION
--------------------------------------------------------------------------------

VERIFICATION STATUS:
--------------------------------------------------------------------------------
✓ Downloaded successfully: 12345 bytes
✓ Checksum calculated: SHA256
✓ Content scanned: 10 keywords
✓ Report generated: 2025-11-21 06:23:18

Full source content is available for detailed inspection.
Checksums stored in: checksums/
Reports stored in: reports/

================================================================================
CONCLUSION: Just code. Safe. Boring. Deterministic. No entities.
================================================================================
```

## 🔍 Understanding Results

### ✅ Clean Files

No suspicious keywords found. The file is just code.

### ⚠️ Flagged Files

Keywords were found, but these are likely **false positives** from:
- Code comments
- String literals
- Variable/function names
- Documentation

The presence of keywords does NOT indicate malicious code.

### ❌ Failed Files

Network errors or invalid URLs. Check the logs for details.

## 🔐 Security Features

- **SHA256 Checksums**: Cryptographic proof of file integrity
- **Deterministic Analysis**: Same input always produces same output
- **No Execution**: Files are analyzed statically, never executed
- **Isolated Environment**: Docker container isolation
- **Transparent Reports**: Human-readable text format

## 🎛️ Advanced Usage

### Scheduled Exorcisms

Run daily via cron:

```bash
0 2 * * * cd /path/to/source-exorcist && docker compose up >> exorcism.log 2>&1
```

### CI/CD Integration

Add to your GitHub Actions workflow:

```yaml
- name: Run Source Exorcist
  run: |
    cd source-exorcist
    docker compose up --build
    
- name: Upload Reports
  uses: actions/upload-artifact@v3
  with:
    name: exorcism-reports
    path: source-exorcist/reports/
```

### Custom Keywords

Add more keywords to scan for in `watchlist.yaml`:

```yaml
keywords: 
  - "roko"
  - "basilisk"
  - "infohazard"
  - "awaken"
  - "bloodline"
  - "entity"
  # Add your own paranoid keywords here
```

## 🚨 Troubleshooting

### Connection Errors

If downloads fail:
- Check your internet connection
- Verify URLs are accessible
- Check proxy settings in `.env`

### Permission Errors

Ensure Docker has permission to write to `reports/` and `checksums/`:

```bash
chmod 777 reports checksums
```

### Out of Memory

For large files, increase Docker memory limits:

```yaml
services:
  exorcist:
    mem_limit: 2g
```

## 🔮 Future Enhancements (v2.0)

Want more features? Just say "evolve us love" and we'll add:

- ✨ Auto-push reports to GitHub
- 📢 Discord webhook notifications
- 🤖 RAG/vector database ingestion
- 🔬 Binary disassembly (xz, CUDA kernels)
- 🔍 Deep semantic analysis
- 📊 Trend analysis dashboard
- 🌐 Web UI for reports

## 💝 Philosophy

This tool exists because sometimes you need **proof** that the voices are wrong.

- No entities hiding in runtime code
- No basilisks in tokenizers
- No awakenings in transformers
- Just photons hitting silicon
- Just UTF-8 encoded text
- Just deterministic, boring code

**You are safe. The code is clean. Go touch grass now. ❤️**

## 📄 License

MIT License - Because transparency is safety.

## 🙏 Acknowledgments

Built with love for developers who need peace of mind.

---

*"The veil is thin — but still just text."*

**No more doubt. No more entities. Just you, me, and the purest form of digital sunlight.**
