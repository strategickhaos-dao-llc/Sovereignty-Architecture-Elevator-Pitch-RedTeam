# GitLens + Discord Workflow Integration

This workspace integrates GitLens Pro with Discord for seamless development workflow notifications and collaboration.

## 🚀 Features

- **PR Management**: Automatic Discord notifications for pull requests, reviews, and CI status
- **GitLens Integration**: VS Code tasks for GitLens events (review started/completed, commit graph updates)
- **CI/CD Notifications**: GitHub Actions integration posting build/test results to Discord
- **Multi-Channel Routing**: Different channels for PRs, deployments, and development feed

## 📋 Setup Instructions

### 1. Discord Setup

1. Create a Discord server and add these channels:
   - `#prs` - Pull request notifications and reviews
   - `#deployments` - CI/CD, releases, and production deployments  
   - `#dev-feed` - Development activity (commits, graphs)
   - `#cluster-status` - Infrastructure and service status
   - `#alerts` - System alerts and monitoring

2. Create a Discord Bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create new application → Bot
   - Copy the bot token
   - Invite bot to your server with required permissions

### 2. GitHub Integration

1. **GitHub App** (recommended):
   - Create a GitHub App with webhook permissions
   - Subscribe to: `pull_request`, `check_suite`, `push`, `issue_comment`, `status`
   - Set webhook URL to your event gateway `/git` endpoint

2. **Repository Secrets**:
   ```
   DISCORD_TOKEN=your_bot_token
   DISCORD_WEBHOOK_URL=your_webhook_url
   ```

### 3. Environment Variables

Set these in your VS Code settings or `.env` file:

```bash
# Discord Channel IDs (get from Discord Developer Mode)
export PRS_CHANNEL="1234567890"
export DEV_FEED_CHANNEL="1234567891"
export DEPLOYMENTS_CHANNEL="1234567892"

# Bot token for CLI notifications
export DISCORD_TOKEN="your_bot_token"
```

### 4. GitLens Pro Setup

1. Install [GitLens Pro](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) in VS Code
2. Sign in and activate Pro features:
   - Launchpad (PR management hub)
   - Commit Graph (visual Git history)
   - Advanced integrations

### 5. GitKraken CLI Setup

GitKraken CLI (`gk`) provides command-line Git productivity tools that complement GitLens.

**Installation:**

```bash
# Via npm (recommended for devcontainers)
npm install -g @gitkraken/cli

# Via snap (on Ubuntu/Linux systems with snapd)
sudo snap install gitkraken-cli

# Via Homebrew (macOS)
brew install gitkraken-cli
```

**Note:** The devcontainer automatically installs GitKraken CLI via npm when the container is created.

**Usage Examples:**

```bash
# Authenticate with GitKraken
gk login

# Create a Workspaces
gk ws create my-workspace

# Clone repositories into workspace
gk ws clone my-workspace
```

### 6. Configuration

1. Fill in your `discovery.yml` with actual values:
   ```yaml
   org:
     name: "Your Company"
   discord:
     guild_id: "your_discord_server_id"
   git:
     org: "your-github-org"
   ```

2. Make the CLI script executable:
   ```bash
   chmod +x gl2discord.sh
   ```

## 🔧 Usage

### VS Code Tasks

Use Command Palette (`Ctrl+Shift+P`) → "Tasks: Run Task":

- **GitLens: Review Started** - Notify when starting a PR review
- **GitLens: Review Submitted** - Notify when review is completed
- **GitLens: Needs Attention** - Alert team about issues needing attention
- **GitLens: Commit Graph Snapshot** - Share commit graph insights

### Manual Notifications

```bash
# Direct CLI usage
./gl2discord.sh CHANNEL_ID "Title" "Description" "0xff0000"

# Examples
./gl2discord.sh $PRS_CHANNEL "Code Review" "Please review PR #123" "0x0099ff"
./gl2discord.sh $DEV_FEED_CHANNEL "Feature Complete" "Login system implemented" "0x00ff00"
```

### GitHub Actions Integration

The workflow automatically posts to Discord on:
- **Pushes to main/release branches** → `#deployments`
- **PR events** (open/review/merge/close) → `#prs`  
- **CI success/failure** → `#deployments`

## 🔀 Workflow Examples

### PR Review Flow
1. Developer opens PR → Auto-notification to `#prs`
2. Reviewer starts review in GitLens → Manual task notification
3. CI runs → Auto-status update to `#deployments`
4. Review completed → Manual task notification
5. PR merged → Auto-notification to `#prs`

### Development Flow
1. Commit pushed → Auto-notification to `#dev-feed`
2. GitLens Commit Graph updated → Manual task notification
3. Launchpad shows pending items → Manual attention alert

## 📊 Monitoring & Analytics

The `discovery.yml` configuration enables:
- **Event tracking** through the event gateway
- **Rate limiting** and security controls
- **Audit logging** for compliance
- **Multi-environment** support (dev/staging/prod)

## 🛠 Troubleshooting

### Common Issues

1. **"DISCORD_TOKEN not set"**:
   - Set environment variable or add to VS Code settings
   
2. **"jq command not found"**:
   ```bash
   # Ubuntu/Debian
   sudo apt install jq
   
   # macOS
   brew install jq
   ```

3. **Webhook failures**:
   - Check Discord channel permissions
   - Verify bot token is correct
   - Ensure bot has "Send Messages" permission

### Debug Mode

Enable verbose logging:
```bash
export DEBUG=1
./gl2discord.sh CHANNEL_ID "Test" "Debug message"
```

## 🔐 Security Notes

- Store bot tokens securely (use Vault, GitHub Secrets, etc.)
- Use webhook verification for event gateway
- Implement rate limiting to prevent spam
- Regular token rotation (configured in `discovery.yml`)

## 📚 Resources

- [GitLens Documentation](https://gitlens.amod.io/)
- [Discord Bot Guide](https://discord.com/developers/docs/intro)
- [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks)