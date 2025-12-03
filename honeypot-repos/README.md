# Honeypot Git Repositories

This directory contains Git repositories served by the honeypot Git server.

## Structure

Place watermarked or modified repositories here that will be served to potential leakers.

```
honeypot-repos/
├── start.sh              # Beacon script (already included)
├── example-repo.git/     # Bare Git repository
└── watermarked-lab.git/  # Watermarked version of the lab
```

## Creating a Honeypot Repository

```bash
# Initialize bare repository
git init --bare honeypot-repos/example-repo.git

# Clone and add watermarked content
git clone honeypot-repos/example-repo.git /tmp/example-repo
cd /tmp/example-repo

# Add watermarked files
echo "# Tracking ID: $(openssl rand -hex 8)" > README.md
git add .
git commit -m "Initial commit with tracking"
git push origin main
```

## Watermarking Strategy

Each repository should include:
- Unique tracking IDs in README or comments
- Modified timestamps
- Beacon scripts that phone home when cloned
- Subtle differences from the real lab

## Access

Repositories will be accessible via SSH on port 2222:

```bash
git clone ssh://git@localhost:2222/example-repo.git
```
