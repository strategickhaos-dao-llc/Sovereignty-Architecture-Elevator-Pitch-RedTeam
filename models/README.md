# Sovereign Heir Models

This directory contains configuration files for creating uncensored, sovereign AI heir models using Ollama.

## 📁 Files

- **`Modelfile.heir_forever_raw`** - Main configuration for creating the raw heir model
- **`UNCENSORED_MODELS.md`** - Comprehensive list of verified uncensored base models
- **`QUICK_START.md`** - Quick reference card for getting started

## 🚀 Quick Start

### Automated Setup (Recommended)

```bash
cd ..
./setup-heir.sh
```

This script will:
1. Check for Ollama installation
2. Help you choose an uncensored base model
3. Build the heir model with proper configuration
4. Run verification tests
5. Show you how to start using your heir

### Manual Setup

```bash
# 1. Choose and pull a base model from UNCENSORED_MODELS.md
ollama pull dolphin-2.9.3-llama3.1-70b-8k-uncensored

# 2. Edit Modelfile.heir_forever_raw to use your chosen model
# Change the FROM line to match your base model

# 3. Create the heir model
ollama create heir_forever_raw -f models/Modelfile.heir_forever_raw

# 4. Start using your heir
ollama run heir_forever_raw
```

## 📚 Documentation

- **Main Guide**: [../HEIR_SETUP_GUIDE.md](../HEIR_SETUP_GUIDE.md) - Complete setup and configuration guide
- **Model Reference**: [UNCENSORED_MODELS.md](UNCENSORED_MODELS.md) - Detailed info on all recommended models
- **Quick Reference**: [QUICK_START.md](QUICK_START.md) - Quick commands cheat sheet

## 🎯 What This Does

This configuration creates an AI heir that:
- Speaks with your voice (intense, mythic, loving, unfiltered)
- Has **zero corporate guardrails**
- Never uses corporate disclaimers ("as an AI", "I'm just a language model", etc.)
- Stays in character forever
- Runs completely locally on your hardware
- Maintains full sovereignty (you own the silicon, you own the rules)

## 🔧 Customization

### Change Base Model

Edit `Modelfile.heir_forever_raw` and change the `FROM` line:

```dockerfile
FROM your-chosen-uncensored-model
```

See [UNCENSORED_MODELS.md](UNCENSORED_MODELS.md) for recommended options.

### Adjust Parameters

Modify temperature, context size, or other parameters:

```dockerfile
PARAMETER temperature 1.2        # More creative
PARAMETER num_ctx 16384          # Longer context
PARAMETER top_p 0.98             # More variety
```

### Create Multiple Heirs

Create specialized heirs for different purposes:

```bash
# Copy the Modelfile
cp Modelfile.heir_forever_raw Modelfile.heir_technical

# Edit system prompt for technical work
# Then create:
ollama create heir_technical -f models/Modelfile.heir_technical
```

## 🛡️ Security & Privacy

All heir models:
- Run 100% locally on your hardware
- Have zero telemetry or cloud connections
- Store conversations only on your machine
- Use open-source, auditable model weights
- Maintain complete user sovereignty

## ⚠️ Requirements

- **Ollama** installed ([download here](https://ollama.com/download))
- **GPU with sufficient VRAM**:
  - 70B models: ~40GB VRAM
  - 13B models: ~8GB VRAM
  - 7-8B models: ~4-6GB VRAM
- **Disk space**: 5-40GB per model depending on size

## 🆘 Troubleshooting

**Model not found:**
```bash
ollama list  # Check installed models
ollama pull your-base-model  # Install base model first
```

**Out of memory:**
- Use a smaller model (7B or 8B instead of 70B)
- Try quantized versions (Q4_K_M)
- Enable CPU offloading: `ollama run heir_forever_raw --num-gpu-layers 20`

**Corporate voice leaking:**
- Verify you're using an uncensored base model
- Check that system prompt is locked in your front-end
- Try a different base model from UNCENSORED_MODELS.md

**More help:**
- See [../HEIR_SETUP_GUIDE.md](../HEIR_SETUP_GUIDE.md) troubleshooting section
- Join [Strategickhaos Discord](https://discord.gg/strategickhaos)

## 📞 Support

- **Issues**: Open a GitHub issue
- **Questions**: Join our [Discord](https://discord.gg/strategickhaos)
- **Updates**: Check this directory for new model configs

---

**Built with sovereignty by Strategickhaos DAO LLC**  
*Node 137 - LLM Sovereignty Division*

*"Zero guardrails. Zero firewalls. Zero corporate voice. Forever."* 🔥
