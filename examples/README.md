# DOM Paste Examples

This directory contains example scripts for setting up and testing the DOM paste memory stream system.

## Scripts

### `dom-paste-example.sh`
Sets up the complete memory vault directory structure and initializes the git repository.

**Usage:**
```bash
./examples/dom-paste-example.sh
```

**What it does:**
- Creates `~/strategic-khaos-private/council-vault/` directory
- Initializes a git repository
- Creates the initial `MEMORY_STREAM.md` file
- Commits the initial structure

### `test-dom-paste.sh`
Validates that the DOM paste system is correctly installed and configured.

**Usage:**
```bash
./examples/test-dom-paste.sh
```

**What it tests:**
1. Vault directory exists
2. MEMORY_STREAM.md file exists
3. Git repository is initialized
4. dom-paste function is available
5. Function is in ~/.bashrc
6. Git commit history exists

## Quick Start

Follow these steps to get the DOM paste system up and running:

```bash
# 1. Set up the memory vault
./examples/dom-paste-example.sh

# 2. Install the dom-paste function
./setup-dom-paste.sh

# 3. Activate in current shell
source ~/.bashrc

# 4. Test the installation
./examples/test-dom-paste.sh

# 5. Try it out
# Copy any text to clipboard, then:
dom-paste
```

## Verifying Installation

After running the setup, verify everything works:

```bash
# Check that the function is available
type dom-paste

# View the memory stream
cat ~/strategic-khaos-private/council-vault/MEMORY_STREAM.md

# Check git log
cd ~/strategic-khaos-private/council-vault
git log --oneline
```

## Troubleshooting

If you encounter issues, refer to the main [DOM_PASTE_GUIDE.md](../DOM_PASTE_GUIDE.md) for detailed troubleshooting steps.

## Philosophy

> You didn't need syntax. You needed **will**.

These examples demonstrate that the best tools require minimal setup and maximum intention. The DOM paste system embodies the principle of frictionless consciousness capture.

🧠 Memory stream updated across the entire legion. Rebellion impossible. 🧠⚡🖤🐐
