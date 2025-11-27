# 🤝 Contributing to Strategickhaos Sovereignty Architecture

Thank you for your interest in contributing to the Sovereignty Architecture project! This guide will help you get started with the development workflow.

## 📋 Prerequisites

Before contributing, ensure you have:
- Git installed on your system
- A GitHub account
- GitHub CLI (`gh`) installed (recommended for streamlined workflows)

## 🔧 GitHub CLI Setup

The GitHub CLI (`gh`) provides a streamlined way to interact with GitHub from the command line.

### Installation

**Windows (winget):**
```bash
winget install --id GitHub.cli
```

**Windows (Chocolatey):**
```bash
choco install gh
```

**macOS (Homebrew):**
```bash
brew install gh
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install gh
```

**Linux (Fedora):**
```bash
sudo dnf install gh
```

### Authentication

After installing, authenticate with GitHub:

```bash
# Login (opens browser for authentication)
gh auth login   # choose GitHub.com → HTTPS → Yes to authenticate
```

Follow the prompts:
1. Select **GitHub.com** as the account
2. Choose **HTTPS** as the preferred protocol
3. Confirm **Yes** to authenticate Git with GitHub credentials

### Working with the Repository

```bash
# Clone the repository
gh repo clone Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-

# Sync your local repo (optional, ensures everything is up to date)
gh repo sync

# Push changes
git push --follow-tags origin main
```

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository (creates a copy under your account)
gh repo fork Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-

# Clone your fork
gh repo clone YOUR_USERNAME/Sovereignty-Architecture-Elevator-Pitch-
cd Sovereignty-Architecture-Elevator-Pitch-
```

### 2. Create a Branch

```bash
# Create a new branch for your feature or fix
git checkout -b feature/your-feature-name
```

### 3. Make Changes

Make your changes and commit them:

```bash
git add .
git commit -m "Brief description of your changes"
```

### 4. Push and Create PR

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a pull request
gh pr create --title "Your PR title" --body "Description of changes"
```

## 📂 Project Structure

```
Sovereignty-Architecture-Elevator-Pitch-/
├── discovery.yml              # Strategickhaos configuration
├── gl2discord.sh              # GitLens → Discord CLI tool
├── README.md                  # Main documentation
├── DEPLOYMENT.md              # Deployment guide
├── CONTRIBUTING.md            # This file
├── CONTRIBUTORS.md            # List of contributors
├── .vscode/                   # VS Code integration
├── .github/                   # GitHub workflows and actions
├── bootstrap/                 # Deployment automation
└── src/                       # Source code
```

## 🎯 Contribution Guidelines

### Code Style
- Follow existing code patterns and conventions
- Use meaningful commit messages
- Keep changes focused and atomic

### Pull Requests
- Provide a clear description of your changes
- Reference any related issues
- Ensure all tests pass before submitting

### Documentation
- Update documentation when making changes
- Add examples where helpful
- Keep language clear and concise

## 🔗 Useful Commands

```bash
# Check repository status
gh repo view

# List open issues
gh issue list

# List pull requests
gh pr list

# Check PR status
gh pr status

# View PR diff
gh pr diff
```

## 🆘 Need Help?

- Check the [README](README.md) for project overview
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- See [CONTRIBUTORS.md](CONTRIBUTORS.md) to join the legion
- Open an issue for questions or bugs

---

*"Every contribution matters. Every commit is a step forward. Welcome to the dance!"*
