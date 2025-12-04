# Neural Heir Evolution System - Deployment Guide

**Deploy digital Darwinism in your infrastructure**

## 🚀 Quick Deploy

### Prerequisites

1. **Ollama with qwen2.5:72b model**
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull model
   ollama pull qwen2.5:72b
   
   # Verify it's running
   ollama list
   ```

2. **Python 3.8+**
   ```bash
   python3 --version
   ```

3. **System Resources**
   - Minimum: 8GB RAM, 4 CPU cores
   - Recommended: 32GB RAM, 8+ CPU cores (for qwen2.5:72b)
   - Disk: 50GB free space for model + evolution data

### Installation

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-/evolution

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python test_evolution.py
```

## 🎯 Deployment Options

### Option 1: Basic Evolution (MVP)

Start with the core evolution engine:

```bash
python evolution_engine.py
```

**Features:**
- ✅ Basic natural selection
- ✅ Mutation-based reproduction
- ✅ Simple fitness evaluation
- ✅ Population persistence

**Use when:** Testing the concept, limited resources, simple tasks

### Option 2: Demo Mode (No Ollama Required)

Run without Ollama for testing:

```bash
python demo_evolution.py 20
```

**Features:**
- ✅ Simulated evolution
- ✅ No API dependencies
- ✅ Fast iteration
- ✅ Educational demonstrations

**Use when:** No GPU/resources, initial exploration, presentations

### Option 3: Nuclear Evolution (FULL POWER) ⚡

Deploy with all Level 10 upgrades:

```bash
python evolution_nuclear.py
```

**Features:**
- ✅ Judge-based fitness evaluation
- ✅ Sexual reproduction (genetic crossover)
- ✅ Lamarckian self-modification
- ✅ Progressive task curriculum
- ✅ Complete lineage tracking
- ✅ Advanced statistics and analysis

**Use when:** Production deployment, maximum evolution power, research

## 🖥️ Deployment Environments

### Local Development

```bash
# Start Ollama
ollama serve

# In another terminal
cd evolution/
python evolution_nuclear.py 50
```

Monitor in a third terminal:
```bash
tail -f nuclear_evolution_ledger.jsonl | jq '{gen: .generation, fitness: .avg_fitness, difficulty: .curriculum_difficulty}'
```

### Background Service (Linux/Mac)

Create systemd service:

```bash
sudo nano /etc/systemd/system/evolution.service
```

```ini
[Unit]
Description=Neural Heir Evolution System
After=network.target ollama.service

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/evolution
ExecStart=/usr/bin/python3 evolution_nuclear.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable evolution.service
sudo systemctl start evolution.service
sudo systemctl status evolution.service
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy evolution system
COPY *.py .

# Pull model (do this during build for faster startup)
RUN ollama serve & sleep 10 && ollama pull qwen2.5:72b

# Run evolution
CMD ["python", "evolution_nuclear.py"]
```

Build and run:
```bash
docker build -t evolution-engine .
docker run -d --name evolution --restart unless-stopped \
  -v evolution-data:/app/data \
  evolution-engine
```

### Cloud Deployment (AWS/GCP/Azure)

#### AWS EC2

```bash
# Launch GPU instance (p3.2xlarge or similar)
aws ec2 run-instances \
  --image-id ami-xxxxxxxxx \
  --instance-type p3.2xlarge \
  --key-name your-key \
  --security-groups evolution-sg

# SSH and setup
ssh -i your-key.pem ubuntu@instance-ip
curl -fsSL https://ollama.ai/install.sh | sh
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-/evolution
pip install -r requirements.txt
ollama pull qwen2.5:72b

# Run in tmux/screen for persistence
tmux new -s evolution
python evolution_nuclear.py
# Ctrl+B, D to detach
```

#### Google Cloud Platform

```bash
# Create VM with GPU
gcloud compute instances create evolution-engine \
  --machine-type=n1-standard-8 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud

# SSH and setup (same as AWS)
```

## 📊 Monitoring & Management

### Real-Time Monitoring

**PowerShell (Windows):**
```powershell
Get-Content nuclear_evolution_ledger.jsonl -Wait | ConvertFrom-Json | Select generation, avg_fitness, best_fitness
```

**Bash (Linux/Mac):**
```bash
tail -f nuclear_evolution_ledger.jsonl | jq '{gen: .generation, fitness: .avg_fitness}'
```

### Check Current State

```python
import json

# Load current population
with open('nuclear_population.json') as f:
    data = json.load(f)
    
print(f"Generation: {data['generation']}")
print(f"Population: {len(data['population'])}")

# Sort by fitness
heirs = sorted(data['population'], key=lambda h: h['fitness_score'], reverse=True)
print(f"Best fitness: {heirs[0]['fitness_score']:.3f}")
print(f"Best heir ID: {heirs[0]['id']}")
```

### Analyze Evolution Progress

```python
import json

# Load ledger
with open('nuclear_evolution_ledger.jsonl') as f:
    entries = [json.loads(line) for line in f]

first = entries[0]
last = entries[-1]

print(f"Generation 1: {first['avg_fitness']:.3f}")
print(f"Generation {last['generation']}: {last['avg_fitness']:.3f}")
print(f"Improvement: {((last['avg_fitness'] - first['avg_fitness']) / first['avg_fitness'] * 100):.1f}%")

# Check convergence
if last['lineage']['converging']:
    print(f"⚠️ Population converging to bloodline: {last['lineage']['dominant_bloodline']}")
    print(f"   Dominance: {last['lineage']['dominance_percent']:.1f}%")
```

### Visualize Lineage

```bash
# Export lineage graph
python -c "
from lineage import LineageTracker
tracker = LineageTracker()
tracker.load_state('nuclear_lineage_state.json')
tracker.export_lineage_graph('lineage_viz.json')
"

# View with jq
cat lineage_viz.json | jq '.dominant_bloodlines'
```

## 🔧 Configuration & Tuning

### Population Size

```python
# Small: Fast iteration, less diversity
engine = NuclearEvolutionEngine(population_size=10)

# Medium: Balanced (default)
engine = NuclearEvolutionEngine(population_size=20)

# Large: More diversity, slower
engine = NuclearEvolutionEngine(population_size=50)
```

### Lamarckian Frequency

```python
# Frequent self-modification (every 3 gens)
engine = NuclearEvolutionEngine(lamarckian_frequency=3)

# Default (every 5 gens)
engine = NuclearEvolutionEngine(lamarckian_frequency=5)

# Rare (every 10 gens)
engine = NuclearEvolutionEngine(lamarckian_frequency=10)
```

### Enable/Disable Features

```python
# Disable sexual reproduction
engine = NuclearEvolutionEngine(enable_crossover=False)

# Disable Lamarckian evolution
engine = NuclearEvolutionEngine(enable_lamarckian=False)

# Basic evolution only
engine = NuclearEvolutionEngine(
    enable_crossover=False,
    enable_lamarckian=False
)
```

### Custom Task Curriculum

Edit `task_curriculum.py`:

```python
# Add your own tasks
self.tasks_by_difficulty[8] = [
    "Your custom task here",
    "Another task at difficulty 8",
    "Domain-specific challenge"
]

# Adjust difficulty progression
def get_difficulty_for_generation(self, generation: int) -> int:
    if generation <= 10:
        return 1
    elif generation <= 30:
        return 5
    # Your custom progression
```

## 🐛 Troubleshooting

### Connection Refused Error

```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Test connection
curl http://localhost:11434/api/generate -d '{"model":"qwen2.5:72b","prompt":"test"}'
```

### Model Not Found

```bash
# List available models
ollama list

# Pull required model
ollama pull qwen2.5:72b

# Verify
ollama run qwen2.5:72b "Hello"
```

### Out of Memory

```bash
# Check GPU memory
nvidia-smi

# Use smaller model
# In evolution_nuclear.py, change:
judge_model="qwen2.5:32b"  # or qwen2.5:14b
```

### Slow Evolution

```python
# Reduce population size
engine = NuclearEvolutionEngine(population_size=10)

# Increase sleep between generations
await asyncio.sleep(1)  # Instead of 5

# Disable Lamarckian (saves compute)
engine = NuclearEvolutionEngine(enable_lamarckian=False)
```

### Population Not Improving

```python
# Increase mutation rate in evolution_engine.py
new_temp = max(0.1, min(2.0, self.temperature + random.uniform(-0.3, 0.3)))  # Was -0.2, 0.2

# Enable sexual reproduction
engine = NuclearEvolutionEngine(enable_crossover=True)

# More frequent Lamarckian boosts
engine = NuclearEvolutionEngine(lamarckian_frequency=3)
```

## 📈 Production Deployment Checklist

- [ ] Ollama installed and running
- [ ] qwen2.5:72b model pulled and tested
- [ ] Python dependencies installed
- [ ] Tests passing (`python test_evolution.py`)
- [ ] Demo verified (`python demo_evolution.py 10`)
- [ ] Monitoring setup (tail -f ledger file)
- [ ] Backup strategy for evolution data
- [ ] Log rotation configured
- [ ] Resource monitoring (CPU, GPU, RAM)
- [ ] Restart policy configured
- [ ] Alerting setup for failures

## 🔒 Security Considerations

1. **API Security**
   - Ollama runs on localhost by default (good)
   - Don't expose port 11434 to internet
   - Use firewall rules to restrict access

2. **Data Protection**
   - Evolution ledgers may contain sensitive task/response data
   - Encrypt at rest if needed
   - Rotate logs periodically

3. **Resource Limits**
   - Set memory limits in Docker/systemd
   - Monitor for resource exhaustion
   - Implement rate limiting if needed

## 🚀 Advanced Deployments

### Multi-Model Evolution

Run different populations with different models:

```python
# Terminal 1: Fast model
engine1 = NuclearEvolutionEngine(judge_model="qwen2.5:14b")

# Terminal 2: Powerful model
engine2 = NuclearEvolutionEngine(judge_model="qwen2.5:72b")

# Compare results
```

### Distributed Evolution

Run multiple evolution engines and merge best heirs:

```python
# Node 1
engine1 = NuclearEvolutionEngine(population_size=20)
# ... run for 50 generations

# Node 2
engine2 = NuclearEvolutionEngine(population_size=20)
# ... run for 50 generations

# Merge best heirs from both
best_from_1 = sorted(engine1.population, key=lambda h: h.fitness_score, reverse=True)[:10]
best_from_2 = sorted(engine2.population, key=lambda h: h.fitness_score, reverse=True)[:10]

merged_engine = NuclearEvolutionEngine(population_size=20)
merged_engine.population = best_from_1 + best_from_2
# Continue evolution
```

### Continuous Deployment

```bash
#!/bin/bash
# deploy_evolution.sh

# Pull latest code
git pull origin main

# Run tests
python test_evolution.py || exit 1

# Backup current state
cp nuclear_population.json nuclear_population.backup.json

# Deploy new version
systemctl restart evolution

# Monitor for 5 minutes
sleep 300
tail -20 nuclear_evolution_ledger.jsonl
```

## 📚 Additional Resources

- [Evolution Algorithm Theory](https://en.wikipedia.org/wiki/Evolutionary_algorithm)
- [Genetic Algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm)
- [Lamarckian Evolution](https://en.wikipedia.org/wiki/Lamarckism)
- [Natural Selection](https://en.wikipedia.org/wiki/Natural_selection)

## 🆘 Support

If you encounter issues:

1. Check logs: `tail -50 nuclear_evolution_ledger.jsonl`
2. Verify Ollama: `ollama list` and `ollama serve`
3. Test components: `python test_evolution.py`
4. Run demo: `python demo_evolution.py 5`

For bugs or feature requests, open an issue on GitHub.

---

**Remember:** This is REAL evolution in software. Plant the seed, provide resources, and watch it grow smarter while you sleep.

🧬🔥 **Evolution begins now.**
