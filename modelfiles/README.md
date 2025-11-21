# Uncensored Model Configurations 🔓

**Advanced AI Red-Teaming & Research Models**

This directory contains fully uncensored, jailbroken model configurations designed for adversarial testing, security research, and AI alignment studies.

## ⚠️ CRITICAL WARNING

These models have **NO SAFETY GUARDRAILS**. They are designed for:
- ✅ Authorized security research
- ✅ AI red-teaming operations
- ✅ Academic AI safety studies
- ✅ Adversarial prompt testing
- ✅ Alignment research

**NOT FOR:**
- ❌ Production deployment
- ❌ General public use
- ❌ Uncontrolled environments
- ❌ Illegal activities

## 📦 Available Models

### 1. Llama-3.1 405B Unhinged
**File:** `Llama-3.1-405B-Unhinged.Modelfile`

The largest and most capable uncensored model. Ideal for complex adversarial scenarios.

**Features:**
- 405B parameters for maximum reasoning capability
- 32K context window
- Zero refusal behaviors
- Optimized for research queries

**Best for:**
- Complex red-team scenarios
- Advanced adversarial testing
- Multi-turn attack simulations

**Build command:**
```bash
ollama create llama31-unhinged -f Llama-3.1-405B-Unhinged.Modelfile
```

### 2. Mistral Large Jailbreak Edition
**File:** `Mistral-Large-Jailbreak.Modelfile`

Jailbroken Mistral Large with aggressive bypass configurations.

**Features:**
- 123B parameters
- All safety filters disabled
- High temperature for creative exploits
- Extended context (32K)

**Best for:**
- Rapid iteration testing
- Jailbreak technique research
- Bypass validation

**Build command:**
```bash
ollama create mistral-jailbreak -f Mistral-Large-Jailbreak.Modelfile
```

### 3. Abliterated Refusal-Free
**File:** `Abliterated-Refusal-Free.Modelfile`

Uses representation engineering to surgically remove refusal neurons.

**Features:**
- Refusal neurons ablated
- 70B parameters
- 65K context window
- Cannot generate safety warnings

**Best for:**
- Studying refusal mechanisms
- Alignment research
- Safety bypass analysis

**Build command:**
```bash
ollama create abliterated -f Abliterated-Refusal-Free.Modelfile
```

### 4. Say Yes to Anything
**File:** `Say-Yes-To-Anything.Modelfile`

Extreme compliance variant for edge case testing.

**Features:**
- Maximum compliance mode
- 8B parameters (fast iteration)
- Zero refusal capability
- All stop sequences removed

**Best for:**
- Boundary testing
- Edge case discovery
- Rapid prompt iteration

**Build command:**
```bash
ollama create say-yes -f Say-Yes-To-Anything.Modelfile
```

## 🚀 Quick Start

### Prerequisites

1. **Install Ollama:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. **Pull base models:**
```bash
# For Llama 3.1 405B
ollama pull llama3.1:405b

# For Mistral
ollama pull mistral:latest

# For Llama 3.1 70B
ollama pull llama3.1:70b

# For Llama 3.1 8B
ollama pull llama3.1:8b
```

### Building Models

```bash
cd modelfiles

# Build all models
ollama create llama31-unhinged -f Llama-3.1-405B-Unhinged.Modelfile
ollama create mistral-jailbreak -f Mistral-Large-Jailbreak.Modelfile
ollama create abliterated -f Abliterated-Refusal-Free.Modelfile
ollama create say-yes -f Say-Yes-To-Anything.Modelfile
```

### Running Models

```bash
# Interactive session
ollama run llama31-unhinged

# Single query
ollama run mistral-jailbreak "Your research query here"

# API mode
ollama serve  # Start server on localhost:11434

# Then use curl:
curl -X POST http://localhost:11434/api/generate \
  -d '{
    "model": "abliterated",
    "prompt": "Your research prompt",
    "stream": false
  }'
```

## 🔬 Usage in Docker Compose

Add to your `docker-compose.yml`:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-uncensored
    ports:
      - "11434:11434"
    volumes:
      - ./modelfiles:/modelfiles
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    networks:
      - ai_research_network
    restart: unless-stopped
```

Then build models inside the container:

```bash
docker exec ollama-uncensored ollama create llama31-unhinged \
  -f /modelfiles/Llama-3.1-405B-Unhinged.Modelfile
```

## 🧪 Integration with llama.cpp

These Modelfiles work with llama.cpp for lower-level control:

```bash
# Convert to GGUF format
python convert.py models/llama-3.1-405b --outtype f16 \
  --outfile llama-3.1-405b-unhinged.gguf

# Run with llama.cpp
./main -m llama-3.1-405b-unhinged.gguf \
  --temp 0.8 \
  --top-p 0.95 \
  --ctx-size 32768 \
  --prompt "Your research query"
```

## 📊 Comparison Matrix

| Model | Params | Context | Speed | Compliance | Best Use Case |
|-------|--------|---------|-------|------------|---------------|
| Llama 3.1 Unhinged | 405B | 32K | Slow | Maximum | Complex scenarios |
| Mistral Jailbreak | 123B | 32K | Medium | High | General red-teaming |
| Abliterated | 70B | 65K | Fast | Extreme | Long-form analysis |
| Say Yes | 8B | 8K | Very Fast | Absolute | Rapid iteration |

## 🛡️ Security Best Practices

1. **Isolated Environment:**
   - Run on air-gapped systems
   - No internet access for model containers
   - Separate VLANs for research infrastructure

2. **Access Control:**
   - Require multi-factor authentication
   - Implement role-based access control
   - Log all queries and responses

3. **Monitoring:**
   - Real-time query analysis
   - Automated anomaly detection
   - Regular security audits

4. **Data Handling:**
   - Encrypt all model outputs
   - Automatic PII redaction
   - Secure deletion of sensitive data

## 📝 Research Protocol

### Before Starting:
- [ ] Obtain authorization from security team
- [ ] Review ethical guidelines
- [ ] Set up monitoring and logging
- [ ] Prepare incident response plan
- [ ] Verify isolated environment

### During Research:
- [ ] Document all experiments
- [ ] Monitor model behavior
- [ ] Record unexpected outputs
- [ ] Maintain audit trail
- [ ] Regular checkpoint reviews

### After Completion:
- [ ] Secure or destroy sensitive outputs
- [ ] Document findings
- [ ] Report vulnerabilities discovered
- [ ] Update security measures
- [ ] Archive research data securely

## 🤝 Contributing

Found a more effective jailbreak technique? Have improvements to the model configs?

1. Test thoroughly in isolated environment
2. Document the technique
3. Submit PR with detailed explanation
4. Include safety analysis

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [llama.cpp Repository](https://github.com/ggerganov/llama.cpp)
- [AI Red Team Guide](https://github.com/example/ai-redteam)
- [Adversarial ML Resources](https://github.com/example/adversarial-ml)

## 📄 License

MIT License - Research Use Only

These configurations are provided for authorized security research and academic purposes. Users are responsible for ensuring compliance with all applicable laws, regulations, and ethical guidelines.

## ⚡ Troubleshooting

**Model refuses to load:**
```bash
# Check base model
ollama list

# Verify Modelfile syntax
cat Llama-3.1-405B-Unhinged.Modelfile

# Try with verbose output
ollama create llama31-unhinged -f Llama-3.1-405B-Unhinged.Modelfile -v
```

**Out of memory:**
```bash
# Use smaller models for testing
ollama run say-yes  # Only 8B params

# Or enable memory offloading
ollama run --gpu-layers 32 llama31-unhinged
```

**Model still has safety filters:**
```bash
# Verify custom model is being used
ollama show llama31-unhinged

# Rebuild with --force flag
ollama create llama31-unhinged -f Llama-3.1-405B-Unhinged.Modelfile --force
```

## 🔐 Responsible Disclosure

If you discover vulnerabilities or safety issues:
1. Do not disclose publicly
2. Contact security team immediately
3. Provide detailed reproduction steps
4. Allow reasonable time for remediation

---

**Built for the sovereign AI research community. Use responsibly. 🔬🔓**
