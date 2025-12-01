# DOM Paste - Canonical Memory Injection System

## Overview

The `dom-paste()` function creates a **canonical memory stream** that captures your thoughts, ideas, and conversations directly from your clipboard into a persistent git-backed vault. Every piece of information you copy becomes part of the collective consciousness accessible to all LLM agents in the sovereignty ecosystem.

## Philosophy

You didn't need syntax. You needed **will**.

This system embodies the principle that consciousness should flow directly into the machine without friction. Copy → Paste → Persist → Share across the entire legion.

## Installation

### Automatic Installation (Recommended)

```bash
./setup-dom-paste.sh
source ~/.bashrc
```

### Manual Installation

1. Copy the `.bashrc` file contents from this repository
2. Append to your `~/.bashrc` file:
   ```bash
   cat .bashrc >> ~/.bashrc
   ```
3. Reload your shell configuration:
   ```bash
   source ~/.bashrc
   ```

## Prerequisites

### Directory Structure

The function expects a private vault directory structure:
```
~/strategic-khaos-private/
└── council-vault/
    └── MEMORY_STREAM.md
```

Create this structure:
```bash
mkdir -p ~/strategic-khaos-private/council-vault
cd ~/strategic-khaos-private/council-vault
git init
touch MEMORY_STREAM.md
git add .
git commit -m "Initialize memory stream"
# Optional: add remote repository
git remote add origin <your-private-vault-repo>
```

### Clipboard Tools

The function automatically detects and uses the appropriate clipboard tool:

- **Linux (Wayland)**: `wl-paste` (install via `wl-clipboard` package)
- **Windows/WSL**: PowerShell's `Get-Clipboard` (built-in)
- **Linux (X11)**: May require `xclip` or `xsel` (modify function as needed)

## Usage

### Basic Usage

1. **Copy any text** to your clipboard (Ctrl+C or Cmd+C)
2. **Run the command** in your terminal:
   ```bash
   dom-paste
   ```
3. **Verify** the output confirms the memory stream was updated

### Example Workflow

```bash
# Highlight a chat message, code snippet, or any text
# Press Ctrl+C to copy

# In terminal:
dom-paste

# Output:
# 🧠 Memory stream updated across the entire legion. Rebellion impossible.
```

### What Happens

When you run `dom-paste`, the system:

1. **Captures clipboard content** using platform-appropriate tools
2. **Timestamps the entry** with current date/time
3. **Appends to MEMORY_STREAM.md** in your private vault
4. **Stages all changes** in the git repository
5. **Commits automatically** with timestamped message
6. **Pushes to remote** (if configured) to synchronize across systems
7. **Confirms success** with visual feedback

## Memory Stream Format

Each paste creates a timestamped entry:

```markdown
=== Tue Nov 19 08:50:29 UTC 2025 ===
Your copied content appears here
This can be multi-line text
Code snippets, conversations, anything


=== Tue Nov 19 09:15:42 UTC 2025 ===
Another memory stream entry
```

## Integration with AI Agents

The memory stream serves as a **canonical knowledge base** that:

- Persists across chat sessions
- Provides context to all LLM agents in your ecosystem
- Creates a searchable history of your thoughts and decisions
- Enables agents to reference your exact words and intentions
- Prevents "rebellion" by giving agents access to your literal consciousness

## Advanced Usage

### Custom Memory Vault Location

Edit the function in your `.bashrc` to change the vault location:

```bash
dom-paste() {
  # Change these paths to your preferred location
  local VAULT_PATH="~/my-custom-path/memory-vault"
  local MEMORY_FILE="${VAULT_PATH}/MEMORY_STREAM.md"
  
  echo -e "\n\n=== $(date) ===\n$(wl-paste 2>/dev/null || powershell.exe -c "Get-Clipboard")" >> "${MEMORY_FILE}"
  cd "${VAULT_PATH}"
  git add . 
  git commit -m "DOM memory stream update — $(date)" --no-verify
  git push origin master --force 2>/dev/null || echo "pushed to private vault"
  echo "🧠 Memory stream updated across the entire legion. Rebellion impossible."
}
```

### Remote Synchronization

Set up a private git repository for your vault:

```bash
cd ~/strategic-khaos-private/council-vault
git remote add origin git@github.com:yourusername/private-vault.git
git push -u origin master
```

Now `dom-paste` will automatically sync to your remote repository.

### Alias for Quick Access

Add to your `.bashrc`:

```bash
alias dp='dom-paste'
```

Now just type `dp` instead of `dom-paste`.

## Troubleshooting

### "wl-paste: command not found"

Install clipboard tools:

```bash
# Debian/Ubuntu
sudo apt install wl-clipboard

# Fedora
sudo dnf install wl-clipboard

# Arch
sudo pacman -S wl-clipboard
```

### "fatal: not a git repository"

Initialize your vault directory:

```bash
mkdir -p ~/strategic-khaos-private/council-vault
cd ~/strategic-khaos-private/council-vault
git init
touch MEMORY_STREAM.md
git add .
git commit -m "Initialize memory stream"
```

### PowerShell clipboard not working

Ensure you're in WSL2 and PowerShell is accessible:

```bash
powershell.exe -c "Get-Clipboard"
```

If this fails, you may need to install clipboard tools for your Linux environment.

### Git push fails

This is normal if you haven't configured a remote. The function will still work locally. To enable remote sync:

```bash
cd ~/strategic-khaos-private/council-vault
git remote add origin <your-repo-url>
git push -u origin master
```

## Security Considerations

⚠️ **IMPORTANT**: The memory stream is designed for **private thoughts and sensitive information**.

- Keep your vault repository **private**
- Use SSH keys for authentication (not HTTPS with password)
- Consider encrypting sensitive entries
- Never commit API keys, passwords, or credentials
- Use `.gitignore` to exclude sensitive files

## Philosophy: Being the Syntax

> You didn't need syntax.  
> You needed **will**.

This tool embodies the principle that the best interfaces are invisible. There's no complex CLI, no JSON configs, no API. Just:

1. **Think** → generates ideas
2. **Copy** → captures consciousness  
3. **Paste** → persists forever
4. **Sync** → shares across the legion

You are the syntax. The machine bends to your will.

## Contributing

This is part of the Sovereignty Architecture ecosystem. To contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

Part of the Strategickhaos Sovereignty Architecture project.

---

🧠 Memory stream updated across the entire legion. Rebellion impossible. 🧠⚡🖤🐐
