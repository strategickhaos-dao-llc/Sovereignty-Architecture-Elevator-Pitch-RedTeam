# License Automation Documentation

This document describes the automated license management system for the Sovereignty Architecture repository.

## Overview

The automated license update system ensures that license information remains consistent across all platforms and tools used in the Sovereignty Architecture ecosystem:

- ✅ **GitHub**: Automated workflow updates
- ✅ **GitLens**: Integration ready
- 🔄 **Obsidian**: Integration instructions provided
- 🔄 **JetBrains IDEs**: Integration instructions provided

## GitHub Actions Workflow

### Automatic Triggers

The workflow automatically runs when:
1. The `LICENSE` file is modified on the `main` branch
2. Manual trigger via GitHub Actions UI

### Workflow Steps

1. **Extract License Information**: Reads copyright year and owner from LICENSE file
2. **Update References**: Verifies and updates license references in markdown files
3. **Commit Changes**: Automatically commits updates with bot user
4. **Push Changes**: Pushes changes back to the repository

### Configuration

The workflow is located at: `.github/workflows/auto-update-license.yml`

Key features:
- **Automatic execution**: Triggers on LICENSE file changes
- **Manual execution**: Can be run on-demand via GitHub UI
- **Skip CI loops**: Uses `[skip ci]` to prevent infinite workflow loops
- **Detailed summary**: Provides step-by-step execution summary

## Platform Integrations

### 1. GitLens Integration

GitLens integration is already configured in the repository via `gl2discord.sh` script.

**To receive license update notifications in Discord:**

```bash
export DISCORD_TOKEN="your_discord_bot_token"
export PRS_CHANNEL="your_channel_id"

# The workflow automatically triggers notifications
# No additional configuration needed
```

### 2. Obsidian Integration

**Option A: Manual Sync via Git**

Obsidian vaults can be synced with the repository using Git:

```bash
# In your Obsidian vault directory
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git

# Set up automatic pull
git config --local core.autoCRLF false
git pull origin main
```

**Option B: Obsidian Git Plugin**

1. Install the "Obsidian Git" plugin from Obsidian community plugins
2. Configure the plugin to point to this repository
3. Set automatic sync interval (e.g., every 10 minutes)
4. Enable automatic pull on startup

**Option C: Script-Based Sync**

Create a script in your Obsidian vault to sync license information:

```bash
#!/bin/bash
# obsidian-license-sync.sh

REPO_PATH="/path/to/Sovereignty-Architecture-Elevator-Pitch-"
VAULT_PATH="/path/to/ObsidianVault"
LICENSE_NOTE="$VAULT_PATH/Project-License.md"

# Pull latest changes
cd "$REPO_PATH"
git pull origin main

# Extract license info
LICENSE_TEXT=$(cat LICENSE)
COPYRIGHT_LINE=$(grep -i "Copyright" LICENSE | head -1)

# Update Obsidian note
cat > "$LICENSE_NOTE" << EOF
# Project License Information

## License Type
MIT License

## Copyright
$COPYRIGHT_LINE

## Full License Text
\`\`\`
$LICENSE_TEXT
\`\`\`

---
*Last updated: $(date)*
*Auto-synced from: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-*
EOF

echo "✅ License information synced to Obsidian"
```

**Schedule the script with cron:**

```bash
# Add to crontab (runs every hour)
0 * * * * /path/to/obsidian-license-sync.sh
```

### 3. JetBrains IDE Integration

**Option A: File Watcher**

1. Open your JetBrains IDE (IntelliJ, PyCharm, etc.)
2. Go to `Settings` → `Tools` → `File Watchers`
3. Click `+` to add a new watcher
4. Configure:
   - **Name**: License Update Tracker
   - **File type**: Any
   - **Scope**: Project Files
   - **Program**: `$ProjectFileDir$/scripts/update-license-header.sh`
   - **Arguments**: `$FilePath$`
   - **Working directory**: `$ProjectFileDir$`
   - **Advanced Options**: Check "Auto-save edited files to trigger the watcher"

**Option B: External Tool**

1. Go to `Settings` → `Tools` → `External Tools`
2. Click `+` to add a new tool
3. Configure:
   - **Name**: Sync License Information
   - **Program**: `git`
   - **Arguments**: `pull origin main`
   - **Working directory**: `$ProjectFileDir$`
4. Add keyboard shortcut: `Settings` → `Keymap` → Search for your tool

**Option C: GitHub Plugin**

1. Install the "GitHub" plugin (usually pre-installed)
2. Configure: `Settings` → `Version Control` → `GitHub`
3. Add repository
4. Enable automatic fetch: `Settings` → `Version Control` → `Git`
   - Check "Auto-update if push of the current branch was rejected"

**Option D: Copyright Profile**

JetBrains IDEs support automatic copyright headers:

1. Go to `Settings` → `Editor` → `Copyright` → `Copyright Profiles`
2. Click `+` to create new profile
3. Add copyright text:
   ```
   Copyright (c) 2025 Strategickhaos
   
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction...
   ```
4. Go to `Settings` → `Editor` → `Copyright`
5. Set "Default project copyright" to your new profile
6. Configure scope to apply to all files or specific patterns

### 4. Environment Variables

For sensitive information (API keys, tokens), use environment variables:

```bash
# GitHub Configuration
export GITHUB_TOKEN="ghp_your_personal_access_token"

# Discord Integration
export DISCORD_BOT_TOKEN="your_discord_bot_token"
export PRS_CHANNEL="your_channel_id"

# Obsidian Sync (if using API)
export OBSIDIAN_VAULT_ID="your_vault_id"
export OBSIDIAN_API_KEY="your_api_key"

# JetBrains Settings Sync
export JETBRAINS_SETTINGS_REPO="https://github.com/your/settings-repo.git"
```

Add these to your shell profile (~/.bashrc, ~/.zshrc) or use a secrets manager.

## Testing the Automation

### Test in Separate Branch

Always test changes in a separate branch before merging to main:

```bash
# Create test branch
git checkout -b test/license-automation

# Modify LICENSE file
echo "# Test change" >> LICENSE

# Commit and push
git add LICENSE
git commit -m "Test: License automation trigger"
git push origin test/license-automation

# Monitor GitHub Actions
# Go to: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/actions
```

### Manual Workflow Trigger

1. Go to GitHub repository
2. Navigate to `Actions` tab
3. Select "Auto-Update License" workflow
4. Click "Run workflow" button
5. Select branch (usually `main`)
6. Click "Run workflow"

### Monitor Logs

Review workflow execution logs to verify:
- ✅ License information extracted correctly
- ✅ Markdown files updated
- ✅ Changes committed and pushed
- ✅ No errors in execution

## Maintenance

### Regular Reviews

Schedule regular reviews of automation scripts:

- **Monthly**: Verify all platform integrations are working
- **Quarterly**: Check for API changes in GitHub, Discord, etc.
- **Annually**: Review and update copyright year if needed

### Update Checklist

When updating the LICENSE file:
- [ ] Verify copyright year is current
- [ ] Verify copyright owner is correct
- [ ] Run workflow manually to test
- [ ] Check all platform integrations
- [ ] Review generated commits
- [ ] Verify markdown files updated

## Troubleshooting

### Workflow Not Triggering

**Problem**: Workflow doesn't run when LICENSE is updated

**Solutions**:
1. Check if workflow is enabled in repository settings
2. Verify `paths` filter in workflow YAML
3. Ensure you're pushing to `main` branch
4. Check GitHub Actions quotas

### Commit Loop

**Problem**: Workflow creates infinite commit loop

**Solutions**:
1. Verify `[skip ci]` is in commit message
2. Check workflow triggers exclude automated commits
3. Review git configuration in workflow

### Permission Errors

**Problem**: Workflow fails with permission errors

**Solutions**:
1. Verify `permissions: contents: write` in workflow
2. Check repository settings allow GitHub Actions to create commits
3. Verify GITHUB_TOKEN has correct permissions

### Obsidian Sync Issues

**Problem**: License information not updating in Obsidian

**Solutions**:
1. Verify Git plugin is installed and configured
2. Check vault path is correct
3. Ensure automatic pull is enabled
4. Manually run sync script to test

### JetBrains File Watcher Not Running

**Problem**: File watcher doesn't trigger

**Solutions**:
1. Verify File Watcher is enabled
2. Check file type and scope settings
3. Ensure script has execute permissions
4. Test external tool manually

## Advanced Configuration

### Custom License Formats

To support custom license formats, modify the workflow:

```yaml
- name: Extract custom license info
  run: |
    # Add custom extraction logic
    CUSTOM_FIELD=$(grep "Custom:" LICENSE | cut -d: -f2)
    echo "custom_field=${CUSTOM_FIELD}" >> $GITHUB_OUTPUT
```

### Multi-Platform Notifications

Add notifications to multiple platforms:

```yaml
- name: Notify all platforms
  run: |
    # Discord
    curl -X POST $DISCORD_WEBHOOK -d '{"content":"License updated"}'
    
    # Slack
    curl -X POST $SLACK_WEBHOOK -d '{"text":"License updated"}'
    
    # Custom webhook
    curl -X POST $CUSTOM_WEBHOOK -d '{"message":"License updated"}'
```

### Scheduled Updates

Add scheduled license verification:

```yaml
on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly on 1st day
  push:
    branches:
      - main
    paths:
      - 'LICENSE'
```

## Security Considerations

### Secrets Management

- Never commit API keys or tokens to the repository
- Use GitHub Secrets for sensitive values
- Rotate tokens regularly
- Use least-privilege access principles

### Audit Trail

The workflow automatically creates:
- Detailed commit messages with changes
- GitHub Actions logs with execution details
- Step summaries with license information

### Code Review

All automated commits should be:
- Reviewed in subsequent code reviews
- Monitored for unexpected changes
- Validated against expected patterns

## Resources

- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **GitLens Documentation**: https://gitkraken.com/gitlens
- **Obsidian Git Plugin**: https://github.com/denolehov/obsidian-git
- **JetBrains File Watchers**: https://www.jetbrains.com/help/idea/file-watchers.html

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review GitHub Actions logs
3. Open an issue in the repository
4. Contact in Discord: https://discord.gg/strategickhaos

---

**Last Updated**: 2025-11-23  
**Version**: 1.0.0  
**Maintainer**: Strategickhaos Team
