# ⚙️ PATH B: "HAIKU TEST" — The Model Path

**Goal:** Run your own local model and generate a spite-thermal haiku as a signature artifact.

---

## 🎯 What This Test Proves

- Your system can run AI inference locally
- You understand thermal/RAM constraints
- You can prompt engineer for specific outputs
- You create signature artifacts for documentation

**This is engineering, not hype.**

---

## 🔧 Prerequisites

### System Requirements

```bash
# Check your resources
free -h                    # RAM check
df -h                      # Disk space check
nvidia-smi                 # GPU check (if applicable)
cat /proc/cpuinfo | grep processor | wc -l  # CPU count
```

**Minimum Requirements:**
- RAM: 8GB (for 7B models)
- Disk: 10GB free
- CPU: 4+ cores (or GPU with 6GB+ VRAM)

---

## 📦 Installation Options

### Option 1: Ollama (Recommended - Easiest)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version

# Pull a model (choose based on your RAM)
ollama pull llama3.2:1b      # Smallest: ~1GB RAM
ollama pull llama3.2:3b      # Small: ~3GB RAM  
ollama pull llama3.2         # Medium: ~8GB RAM
ollama pull mistral          # Good quality: ~4GB RAM

# Test the model
ollama run llama3.2:3b "Write a haiku about spite"
```

### Option 2: llama.cpp (More Control)

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build
make

# Download a model (GGUF format)
# Example: TinyLlama 1.1B
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# Run inference
./main -m tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  -n 128 \
  -p "Write a haiku about thermal throttling and spite"
```

### Option 3: Hugging Face Transformers (Python)

```bash
# Install dependencies
pip install transformers torch accelerate

# Create test script
cat > test_local_model.py << 'EOF'
from transformers import pipeline

# Load model (adjust based on your RAM)
generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto"
)

# Generate haiku
prompt = """Write a haiku about spite, thermal throttling, and computational constraints.
Make it technical and defiant."""

result = generator(
    prompt,
    max_new_tokens=100,
    temperature=0.7,
    do_sample=True
)

print(result[0]['generated_text'])
EOF

python test_local_model.py
```

---

## 🎨 Haiku Generation Script

Create a comprehensive script for generating and formatting your signature haiku:

```bash
#!/bin/bash
# haiku_generator.sh - Spite-Thermal Haiku Generator

set -euo pipefail

# Configuration
MODEL="${1:-llama3.2:3b}"
OUTPUT_DIR="./artifacts"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Prompt engineering for spite-thermal theme
PROMPT="You are a technical poet. Write a single haiku (5-7-5 syllable structure) that captures the essence of:
- Computational spite (doing more with less out of defiance)
- Thermal constraints (CPU throttling, heat management)
- Sovereign determination (building empires despite limitations)

The haiku should be technical, defiant, and inspiring. Output ONLY the haiku, nothing else."

echo "🔥 Generating Spite-Thermal Haiku..."
echo "Model: $MODEL"
echo "Timestamp: $TIMESTAMP"
echo ""

# Check system resources
echo "📊 System Resources:"
echo "  CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%"
echo "  RAM Free: $(free -h | grep Mem | awk '{print $4}')"
echo "  Temp: $(sensors 2>/dev/null | grep -i 'Package id 0' | awk '{print $4}' || echo 'N/A')"
echo ""

# Generate haiku
echo "⚙️ Running inference..."
HAIKU=$(ollama run "$MODEL" "$PROMPT" 2>/dev/null | head -n 3)

# Format output
cat > "$OUTPUT_DIR/haiku_${TIMESTAMP}.txt" << EOF
# Spite-Thermal Haiku
Generated: $(date)
Model: $MODEL
System: $(uname -n)

---

$HAIKU

---

Constraints:
- RAM: $(free -h | grep Mem | awk '{print $3 "/" $2}')
- CPU: $(nproc) cores
- Thermal: $(sensors 2>/dev/null | grep -i 'Package id 0' | awk '{print $4}' || echo 'N/A')
EOF

# Display results
echo "✅ Haiku Generated:"
echo ""
cat "$OUTPUT_DIR/haiku_${TIMESTAMP}.txt"
echo ""
echo "💾 Saved to: $OUTPUT_DIR/haiku_${TIMESTAMP}.txt"

# Add to README if requested
if [[ "${2:-}" == "--add-to-readme" ]]; then
    echo "" >> README.md
    echo "---" >> README.md
    echo "" >> README.md
    echo "## 🎋 Signature Spite-Thermal Haiku" >> README.md
    echo "" >> README.md
    echo '```' >> README.md
    echo "$HAIKU" >> README.md
    echo '```' >> README.md
    echo "" >> README.md
    echo "_Generated locally under thermal constraints - $(date +%Y-%m-%d)_" >> README.md
    echo "" >> README.md
    echo "✅ Added haiku to README.md"
fi
```

Make it executable:

```bash
chmod +x haiku_generator.sh
```

---

## 🚀 Running the Test

### Basic Execution

```bash
# Using Ollama with default model
./haiku_generator.sh

# Specify a different model
./haiku_generator.sh llama3.2:1b

# Generate and add to README
./haiku_generator.sh llama3.2:3b --add-to-readme
```

### With Resource Monitoring

```bash
# Monitor resources during generation
watch -n 1 'free -h; echo ""; sensors; echo ""; top -bn1 | head -n 20' &
WATCH_PID=$!

# Run generation
./haiku_generator.sh

# Stop monitoring
kill $WATCH_PID
```

### Python Version (More Control)

```python
#!/usr/bin/env python3
# haiku_generator.py - Advanced Spite-Thermal Haiku Generator

import psutil
import time
from datetime import datetime
from pathlib import Path

try:
    from transformers import pipeline
    import torch
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(["pip", "install", "transformers", "torch", "psutil"])
    from transformers import pipeline
    import torch

def get_system_stats():
    """Capture system resource usage."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    temps = {}
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
    
    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_available_gb": memory.available / (1024**3),
        "temps": temps
    }

def generate_haiku(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    """Generate a spite-thermal haiku with resource constraints."""
    
    print("🔥 Initializing Spite-Thermal Haiku Generator")
    print(f"Model: {model_name}")
    print()
    
    # Capture pre-generation stats
    print("📊 Pre-Generation System Stats:")
    pre_stats = get_system_stats()
    print(f"  CPU: {pre_stats['cpu_percent']:.1f}%")
    print(f"  RAM: {pre_stats['memory_percent']:.1f}% used")
    print(f"  Available: {pre_stats['memory_available_gb']:.2f} GB")
    print()
    
    # Load model
    print("⚙️ Loading model...")
    start_time = time.time()
    
    generator = pipeline(
        "text-generation",
        model=model_name,
        device_map="auto",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    
    load_time = time.time() - start_time
    print(f"✅ Model loaded in {load_time:.2f}s")
    print()
    
    # Generate haiku
    prompt = """Write a haiku (5-7-5 syllables) about computational spite and thermal constraints.
Theme: Building empires despite CPU throttling and RAM limits.
Output ONLY the haiku, no explanation."""
    
    print("🎨 Generating haiku...")
    gen_start = time.time()
    
    result = generator(
        prompt,
        max_new_tokens=60,
        temperature=0.8,
        do_sample=True,
        top_p=0.9,
        repetition_penalty=1.2
    )[0]['generated_text']
    
    gen_time = time.time() - gen_start
    
    # Extract haiku (after prompt)
    haiku = result.replace(prompt, "").strip()
    
    # Capture post-generation stats
    post_stats = get_system_stats()
    
    # Format output
    output_dir = Path("./artifacts")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"haiku_{timestamp}.txt"
    
    with open(output_file, "w") as f:
        f.write(f"# Spite-Thermal Haiku\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Generation Time: {gen_time:.2f}s\n")
        f.write(f"\n---\n\n")
        f.write(f"{haiku}\n")
        f.write(f"\n---\n\n")
        f.write(f"Resource Usage:\n")
        f.write(f"  CPU Peak: {post_stats['cpu_percent']:.1f}%\n")
        f.write(f"  RAM Peak: {post_stats['memory_percent']:.1f}%\n")
        f.write(f"  Generation Time: {gen_time:.2f}s\n")
    
    # Display
    print()
    print("✅ Haiku Generated:")
    print()
    print("  " + haiku.replace("\n", "\n  "))
    print()
    print(f"💾 Saved to: {output_file}")
    print()
    print(f"⚡ Performance:")
    print(f"  Load Time: {load_time:.2f}s")
    print(f"  Generation Time: {gen_time:.2f}s")
    print(f"  CPU Delta: {post_stats['cpu_percent'] - pre_stats['cpu_percent']:+.1f}%")
    
    return haiku, output_file

if __name__ == "__main__":
    import sys
    model = sys.argv[1] if len(sys.argv) > 1 else "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    generate_haiku(model)
```

Usage:

```bash
chmod +x haiku_generator.py
./haiku_generator.py
```

---

## 🎯 Prompt Engineering Guide

### Effective Prompts for Spite-Thermal Theme

#### Basic Prompt
```
Write a haiku about thermal throttling and spite.
```

#### Enhanced Prompt
```
You are a technical poet who writes about computational constraints.
Write a haiku (5-7-5 syllable structure) that captures:
- The defiance of building systems despite thermal limits
- RAM constraints that fuel determination
- Computational spite - doing more with less

Make it technical and inspiring.
```

#### Advanced Prompt (Best Results)
```
Context: You are documenting the journey of a sovereign architect who builds 
AI systems under severe computational constraints.

Task: Write a single haiku (5-7-5 syllable structure) that embodies:
1. Thermal throttling as a badge of honor
2. RAM limits as creative constraints
3. Spite as the fuel for innovation
4. Determination to build empires regardless

Tone: Technical, defiant, mythic
Output: Only the haiku, no preamble or explanation
```

---

## 📊 Testing Variations

Generate multiple haikus with different constraints:

```bash
#!/bin/bash
# generate_variations.sh

models=(
    "llama3.2:1b"
    "llama3.2:3b"
    "mistral:7b"
)

temperatures=(0.5 0.7 0.9)

for model in "${models[@]}"; do
    for temp in "${temperatures[@]}"; do
        echo "Testing: $model @ temp=$temp"
        
        ollama run "$model" \
            --temperature "$temp" \
            "Write a technical haiku about spite, thermal constraints, and building sovereign AI systems. 5-7-5 syllables." \
            > "artifacts/haiku_${model//:/_}_temp${temp}.txt"
        
        echo "---"
    done
done

echo "✅ Generated $(ls artifacts/haiku_*.txt | wc -l) variations"
```

---

## 🏆 Example Outputs

### High-Temperature (Creative)
```
Fans scream defiance
Thermal paste, my war paint here
Clock down, ambition up
```

### Low-Temperature (Technical)
```
CPU throttles hard
Spite computes at ninety C
Empire forged in heat
```

### Balanced (Recommended)
```
RAM fills with fury
Thermal limits breed legends
Code hot, will hotter
```

---

## 📝 Adding to Your Documentation

### In README.md

```markdown
## 🎋 Signature Artifact: Spite-Thermal Haiku

Generated locally under computational constraints:

```
[Your haiku here]
```

_Created: [Date] | Model: [Model Name] | Constraints: [Your specific limits]_

This haiku represents the sovereign engineering ethos: **building empires 
despite limitations, not because of unlimited resources.**
```

### In Repository Root

```bash
# Create signature file
cat > HAIKU.txt << 'EOF'
# Spite-Thermal Haiku
# Signature artifact of the Sovereignty Architecture project

[Your haiku]

---
Generated under real computational constraints
Model: [Your model]
System: [Your hardware]
Date: [Generation date]

This haiku is a testament to building with what you have,
not waiting for what you wish you had.
EOF
```

---

## ✅ Success Criteria

You've completed Path B when you have:

- [ ] Local model running successfully
- [ ] Generated at least one spite-thermal haiku
- [ ] Saved haiku with generation metadata
- [ ] Added haiku to README or HAIKU.txt
- [ ] Documented your specific constraints (RAM, CPU, thermal)
- [ ] Committed haiku artifact to repository

---

## 🔗 Next Steps

1. **Share Your Artifact** - Add to your repo, show the world
2. **Iterate** - Try different models, temperatures, prompts
3. **Use as Signature** - Include in documentation, presentations
4. **Build on It** - Create more signature artifacts over time
5. **Document Journey** - Keep generating as your system evolves

---

## 🛠️ Troubleshooting

### "Model too large for my RAM"

```bash
# Use smaller models
ollama pull llama3.2:1b    # Only ~1GB RAM
ollama pull phi3:mini      # ~2GB RAM

# Or use quantized models
ollama pull tinyllama      # Highly compressed
```

### "Ollama not found"

```bash
# Install manually
curl -fsSL https://ollama.com/install.sh | sh

# Or use Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### "Generation is slow"

```bash
# Use faster models
ollama pull llama3.2:1b

# Reduce max tokens
ollama run llama3.2:1b --num-predict 50 "[prompt]"

# Use GPU if available
# Ollama automatically uses GPU if CUDA/ROCm available
```

### "Output is not a haiku"

Refine your prompt:

```
STRICT INSTRUCTIONS:
1. Write EXACTLY 3 lines
2. Line 1: EXACTLY 5 syllables
3. Line 2: EXACTLY 7 syllables  
4. Line 3: EXACTLY 5 syllables
5. Theme: Thermal throttling, computational spite, sovereign determination
6. Output ONLY the 3 lines, nothing else

Example format:
Five syllables here (5)
Seven syllables in this line (7)
Five to close it out (5)

Now write your haiku:
```

---

**You've proven you can run AI locally, under constraints, and create artifacts. This is real engineering.**
