#!/usr/bin/env bash
# pelican-build.sh
# Strategickhaos DAO LLC / Valoryield Engine — Pelican Static Site Builder
# Purpose: Build and deploy Pelican static sites for Sovereign Swarm documentation
#
# This script handles:
#   - Pelican static site generation
#   - Theme management and customization
#   - Content validation
#   - Deployment to various targets (local, S3, GitHub Pages)
#
# Usage: ./pelican-build.sh [command] [options]
# Commands: build, serve, deploy, clean

set -euo pipefail

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           CONFIGURATION                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."
CONTENT_DIR="${PROJECT_ROOT}/content"
OUTPUT_DIR="${PROJECT_ROOT}/output"
THEME_DIR="${PROJECT_ROOT}/themes/sovereignty"
PELICAN_CONF="${PROJECT_ROOT}/pelicanconf.py"
PUBLISH_CONF="${PROJECT_ROOT}/publishconf.py"

# Default settings
DEFAULT_PORT=8000
DEPLOY_TARGET="${DEPLOY_TARGET:-local}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           UTILITY FUNCTIONS                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_section() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           PREREQUISITES CHECK                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

check_prerequisites() {
    log_section "Checking Prerequisites"
    
    local missing_deps=()
    
    # Check Python
    if ! command -v python3 &>/dev/null; then
        missing_deps+=("python3")
    fi
    
    # Check pip
    if ! command -v pip3 &>/dev/null; then
        missing_deps+=("pip3")
    fi
    
    # Check Pelican
    if ! python3 -c "import pelican" 2>/dev/null; then
        missing_deps+=("pelican")
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_warning "Missing dependencies: ${missing_deps[*]}"
        log_info "Installing dependencies..."
        
        pip3 install --quiet pelican markdown typogrify
        
        log_success "Dependencies installed"
    else
        log_success "All prerequisites satisfied"
    fi
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           INITIALIZE PROJECT                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

init_project() {
    log_section "Initializing Pelican Project"
    
    # Create content directory structure
    mkdir -p "$CONTENT_DIR"/{articles,pages,images}
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$THEME_DIR"/{static,templates}
    
    # Create default pelicanconf.py if it doesn't exist
    if [[ ! -f "$PELICAN_CONF" ]]; then
        log_info "Creating default configuration..."
        
        cat > "$PELICAN_CONF" <<'PYTHON_EOF'
# -*- coding: utf-8 -*-
"""
Pelican Configuration for Sovereign Swarm Documentation
Strategickhaos DAO LLC / Valoryield Engine
"""

AUTHOR = 'Strategickhaos DAO LLC'
SITENAME = 'Sovereign Swarm Documentation'
SITEURL = ''

PATH = 'content'
OUTPUT_PATH = 'output'

TIMEZONE = 'America/Chicago'
DEFAULT_LANG = 'en'

# Feed generation (disabled for local development)
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Theme
THEME = 'themes/sovereignty'

# Blogroll
LINKS = (
    ('Strategickhaos GitHub', 'https://github.com/Strategickhaos-Swarm-Intelligence'),
    ('Valoryield Engine', 'https://valoryield.com'),
)

# Social
SOCIAL = (
    ('Discord', 'https://discord.gg/strategickhaos'),
    ('GitHub', 'https://github.com/Strategickhaos'),
)

DEFAULT_PAGINATION = 10

# Static paths
STATIC_PATHS = ['images', 'extra']

# URL structure
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Plugins
PLUGINS = []

# Markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {'title': 'Table of Contents'},
    },
    'output_format': 'html5',
}
PYTHON_EOF
        
        log_success "Created pelicanconf.py"
    fi
    
    # Create default theme templates
    if [[ ! -f "${THEME_DIR}/templates/base.html" ]]; then
        log_info "Creating default theme..."
        
        cat > "${THEME_DIR}/templates/base.html" <<'HTML_EOF'
<!DOCTYPE html>
<html lang="{{ DEFAULT_LANG }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}{{ SITENAME }}{% endblock %}</title>
    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/main.css">
</head>
<body>
    <header>
        <nav>
            <a href="{{ SITEURL }}/">{{ SITENAME }}</a>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; {{ AUTHOR }} - Powered by Pelican</p>
    </footer>
</body>
</html>
HTML_EOF
        
        cat > "${THEME_DIR}/templates/index.html" <<'HTML_EOF'
{% extends "base.html" %}

{% block content %}
<h1>{{ SITENAME }}</h1>

{% for article in articles %}
<article>
    <h2><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></h2>
    <p class="meta">{{ article.date.strftime('%Y-%m-%d') }} | {{ article.category }}</p>
    <p>{{ article.summary }}</p>
</article>
{% endfor %}
{% endblock %}
HTML_EOF
        
        cat > "${THEME_DIR}/templates/article.html" <<'HTML_EOF'
{% extends "base.html" %}

{% block title %}{{ article.title }} | {{ SITENAME }}{% endblock %}

{% block content %}
<article>
    <header>
        <h1>{{ article.title }}</h1>
        <p class="meta">{{ article.date.strftime('%Y-%m-%d') }} | {{ article.category }}</p>
    </header>
    
    {{ article.content }}
</article>
{% endblock %}
HTML_EOF
        
        cat > "${THEME_DIR}/templates/page.html" <<'HTML_EOF'
{% extends "base.html" %}

{% block title %}{{ page.title }} | {{ SITENAME }}{% endblock %}

{% block content %}
<article>
    <h1>{{ page.title }}</h1>
    {{ page.content }}
</article>
{% endblock %}
HTML_EOF
        
        # Create basic CSS
        cat > "${THEME_DIR}/static/css/main.css" <<'CSS_EOF'
/* Sovereign Swarm Documentation Theme */

:root {
    --primary: #1a1a2e;
    --secondary: #16213e;
    --accent: #0f3460;
    --highlight: #e94560;
    --text: #eaeaea;
    --text-muted: #a0a0a0;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--primary);
    color: var(--text);
    line-height: 1.6;
}

header {
    background: var(--secondary);
    padding: 1rem 2rem;
    border-bottom: 2px solid var(--highlight);
}

header nav a {
    color: var(--highlight);
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: bold;
}

main {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
}

article {
    background: var(--secondary);
    padding: 2rem;
    margin-bottom: 2rem;
    border-radius: 8px;
    border-left: 4px solid var(--highlight);
}

article h1, article h2 {
    color: var(--highlight);
    margin-bottom: 1rem;
}

article h2 a {
    color: var(--highlight);
    text-decoration: none;
}

article h2 a:hover {
    text-decoration: underline;
}

.meta {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

footer {
    text-align: center;
    padding: 2rem;
    color: var(--text-muted);
    border-top: 1px solid var(--accent);
}

pre, code {
    background: var(--primary);
    border-radius: 4px;
}

code {
    padding: 0.2rem 0.4rem;
}

pre {
    padding: 1rem;
    overflow-x: auto;
}

a {
    color: var(--highlight);
}
CSS_EOF
        
        log_success "Default theme created"
    fi
    
    # Create sample content if content directory is empty
    if [[ ! -f "${CONTENT_DIR}/pages/about.md" ]]; then
        log_info "Creating sample content..."
        
        cat > "${CONTENT_DIR}/pages/about.md" <<'MD_EOF'
Title: About Sovereign Swarm
Slug: about
Status: published

# About Sovereign Swarm

The Sovereign Swarm is a distributed mesh network architecture designed for 
secure, encrypted communication across heterogeneous network connections.

## Key Features

- **WireGuard Mesh**: Encrypted overlay network
- **Ed25519 CA**: Cryptographic node identity
- **NATS JetStream**: Telemetry and command bus
- **Matrix Synapse**: Encrypted team chat
- **SwarmGate**: Access control agent

## Getting Started

See the [deployment guide](/deployment/) for setup instructions.
MD_EOF
        
        cat > "${CONTENT_DIR}/articles/welcome.md" <<'MD_EOF'
Title: Welcome to Sovereign Swarm
Date: 2025-01-01
Category: Announcements
Tags: introduction, architecture
Slug: welcome-sovereign-swarm
Summary: Introduction to the Sovereign Swarm mesh network architecture.

# Welcome to Sovereign Swarm

This documentation site covers the Sovereign Swarm mesh network - a secure, 
encrypted overlay network for the Strategickhaos infrastructure.

## What is Sovereign Swarm?

Sovereign Swarm transforms mixed network connections (Starlink, 5G, LAN) into 
a single, encrypted, self-governing network with built-in AI messaging and 
access control.

## Components

1. **WireGuard Mesh** - Encrypted tunnels between all nodes
2. **Ed25519 CA** - Cryptographic identity for each node
3. **JWT Tokens** - Capability-based access control
4. **NATS JetStream** - Real-time telemetry and commands
5. **Matrix Synapse** - Encrypted team communication

Stay tuned for more documentation and guides!
MD_EOF
        
        log_success "Sample content created"
    fi
    
    log_success "Project initialized"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           BUILD SITE                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

build_site() {
    log_section "Building Pelican Site"
    
    local config="${1:-$PELICAN_CONF}"
    
    cd "$PROJECT_ROOT"
    
    # Clean output directory
    if [[ -d "$OUTPUT_DIR" ]]; then
        rm -rf "${OUTPUT_DIR:?}"/*
    fi
    
    log_info "Running Pelican build..."
    
    pelican "$CONTENT_DIR" -o "$OUTPUT_DIR" -s "$config"
    
    # Count generated files
    local file_count
    file_count=$(find "$OUTPUT_DIR" -type f | wc -l)
    
    log_success "Build complete: $file_count files generated"
    log_info "Output: $OUTPUT_DIR"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           SERVE LOCALLY                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

serve_site() {
    log_section "Starting Development Server"
    
    local port="${1:-$DEFAULT_PORT}"
    
    cd "$PROJECT_ROOT"
    
    # Build first if output doesn't exist
    if [[ ! -d "$OUTPUT_DIR" ]] || [[ -z "$(ls -A "$OUTPUT_DIR" 2>/dev/null)" ]]; then
        build_site
    fi
    
    log_info "Starting server at http://localhost:${port}"
    log_info "Press Ctrl+C to stop"
    
    cd "$OUTPUT_DIR"
    python3 -m http.server "$port"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           DEPLOY SITE                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

deploy_site() {
    log_section "Deploying Site"
    
    local target="${1:-$DEPLOY_TARGET}"
    
    # Build with publish config
    if [[ -f "$PUBLISH_CONF" ]]; then
        build_site "$PUBLISH_CONF"
    else
        build_site
    fi
    
    case "$target" in
        local)
            log_info "Local deployment - files in $OUTPUT_DIR"
            ;;
        
        s3)
            log_info "Deploying to S3..."
            if [[ -z "${S3_BUCKET:-}" ]]; then
                log_error "S3_BUCKET environment variable not set"
                exit 1
            fi
            aws s3 sync "$OUTPUT_DIR" "s3://${S3_BUCKET}/" --delete
            log_success "Deployed to s3://${S3_BUCKET}/"
            ;;
        
        gh-pages)
            log_info "Deploying to GitHub Pages..."
            
            if [[ -z "${GITHUB_PAGES_REPO:-}" ]]; then
                log_error "GITHUB_PAGES_REPO environment variable not set"
                exit 1
            fi
            
            cd "$OUTPUT_DIR"
            git init
            
            # Configure git for the commit
            git config user.email "deploy@strategickhaos.local"
            git config user.name "Pelican Deploy"
            
            git add -A
            
            # Check if there are changes to commit
            if git diff --cached --quiet; then
                log_warning "No changes to deploy"
            else
                git commit -m "Deploy $(date +%Y-%m-%d)"
                git push -f "git@github.com:${GITHUB_PAGES_REPO}.git" main:gh-pages
                log_success "Deployed to GitHub Pages"
            fi
            ;;
        
        rsync)
            log_info "Deploying via rsync..."
            if [[ -z "${RSYNC_TARGET:-}" ]]; then
                log_error "RSYNC_TARGET environment variable not set"
                exit 1
            fi
            rsync -avz --delete "$OUTPUT_DIR/" "$RSYNC_TARGET"
            log_success "Deployed via rsync to $RSYNC_TARGET"
            ;;
        
        *)
            log_error "Unknown deploy target: $target"
            log_info "Supported targets: local, s3, gh-pages, rsync"
            exit 1
            ;;
    esac
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           CLEAN                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

clean_site() {
    log_section "Cleaning Build Artifacts"
    
    if [[ -d "$OUTPUT_DIR" ]]; then
        rm -rf "${OUTPUT_DIR:?}"
        log_success "Removed $OUTPUT_DIR"
    else
        log_info "Output directory doesn't exist"
    fi
    
    # Clean Python cache
    find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
    
    log_success "Clean complete"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           WATCH MODE                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

watch_site() {
    log_section "Starting Watch Mode"
    
    local port="${1:-$DEFAULT_PORT}"
    
    cd "$PROJECT_ROOT"
    
    log_info "Starting Pelican with auto-reload at http://localhost:${port}"
    log_info "Press Ctrl+C to stop"
    
    pelican --listen --autoreload --port "$port" "$CONTENT_DIR" -o "$OUTPUT_DIR" -s "$PELICAN_CONF"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           HELP                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

show_help() {
    cat <<EOF
Pelican Build Script for Sovereign Swarm Documentation
Strategickhaos DAO LLC / Valoryield Engine

Usage: $0 <command> [options]

Commands:
    init        Initialize a new Pelican project with default theme
    build       Build the static site
    serve       Start local development server
    watch       Start with auto-reload on changes
    deploy      Deploy to target (local|s3|gh-pages|rsync)
    clean       Remove build artifacts
    help        Show this help message

Options:
    -p, --port PORT     Port for development server (default: 8000)
    -t, --target TARGET Deploy target (default: local)

Environment Variables:
    S3_BUCKET           S3 bucket for s3 deployment
    GITHUB_PAGES_REPO   GitHub repo for gh-pages deployment
    RSYNC_TARGET        Target for rsync deployment
    DEPLOY_TARGET       Default deployment target

Examples:
    $0 init                 # Initialize new project
    $0 build                # Build site
    $0 serve -p 9000        # Serve on port 9000
    $0 watch                # Auto-reload development
    $0 deploy s3            # Deploy to S3
    $0 clean                # Clean build artifacts

EOF
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           MAIN                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

main() {
    local command="${1:-help}"
    shift || true
    
    local port="$DEFAULT_PORT"
    local target="$DEPLOY_TARGET"
    
    # Parse options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -p|--port)
                port="$2"
                shift 2
                ;;
            -t|--target)
                target="$2"
                shift 2
                ;;
            *)
                target="$1"
                shift
                ;;
        esac
    done
    
    case "$command" in
        init)
            check_prerequisites
            init_project
            ;;
        build)
            check_prerequisites
            build_site
            ;;
        serve)
            check_prerequisites
            serve_site "$port"
            ;;
        watch)
            check_prerequisites
            watch_site "$port"
            ;;
        deploy)
            check_prerequisites
            deploy_site "$target"
            ;;
        clean)
            clean_site
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
