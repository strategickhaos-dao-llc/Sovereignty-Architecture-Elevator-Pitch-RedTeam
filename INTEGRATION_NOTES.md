# Integration Notes: Auto-Update License Workflow

This document provides comprehensive guidance on integrating the auto-update license workflow with various development environments including GitHub Actions, Obsidian, and JetBrains IDEs.

---

## GitHub Actions Workflow

The repository includes an automated workflow (`.github/workflows/auto-update-license.yml`) that updates license text across all markdown files in the repository.

### Workflow Features

- **Automatic Trigger**: Runs on every push to the `main` branch
- **Manual Trigger**: Can be manually triggered via `workflow_dispatch` from the Actions tab
- **Batch Updates**: Updates all markdown files in a single run
- **Automated Commits**: Automatically commits and pushes changes

### Configuration

The workflow requires two GitHub Secrets to be configured:

1. `GIT_USER_EMAIL` - Email address for git commits
2. `GIT_USER_NAME` - Name for git commits

To set these up:
1. Go to your repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add both secrets with appropriate values

### Customization

⚠️ **IMPORTANT**: Before using this workflow, you **must** customize the license text placeholders.

The workflow uses placeholder values `OLD_LICENSE_TEXT` and `NEW_LICENSE_TEXT` that must be replaced with your actual license text before the workflow will be functional.

To customize the license text being replaced, edit the workflow file:

```yaml
# Change these values in .github/workflows/auto-update-license.yml
# Replace OLD_LICENSE_TEXT with the text you want to find
# Replace NEW_LICENSE_TEXT with the replacement text
find . -name '*.md' -exec sed -i 's/OLD_LICENSE_TEXT/NEW_LICENSE_TEXT/g' {} +
```

**Example**:
```yaml
# Find: "Copyright (c) 2024"
# Replace with: "Copyright (c) 2025"
find . -name '*.md' -exec sed -i 's/Copyright (c) 2024/Copyright (c) 2025/g' {} +
```

---

## Obsidian Integration

Obsidian is a powerful knowledge base that works on top of a local folder of plain text Markdown files. Here's how to integrate license updates with your Obsidian vault.

### Syncing Your Vault

**Option 1: GitHub Plugin**
- Install the Obsidian Git plugin from Community Plugins
- Configure it to auto-sync your vault with your GitHub repository
- After the workflow runs, simply pull changes in Obsidian

**Option 2: Manual Sync**
- Use standard git commands to pull changes:
  ```bash
  cd /path/to/your/obsidian/vault
  git pull
  ```

### Local License Update Script

A Python script is provided for local license updates in your Obsidian vault:

**Location**: `scripts/update_license.py`

**Usage**:
```bash
# Update all markdown files in current directory
python3 scripts/update_license.py

# Update all markdown files in specific directory
python3 scripts/update_license.py /path/to/your/obsidian/vault
```

**Customization**:

⚠️ **REQUIRED**: Before using the script, you must edit it to replace the placeholder license text.

Edit `scripts/update_license.py` and change these constants:

```python
# Replace these placeholder values with your actual license text
OLD_LICENSE_TEXT = "Your old license text here"
NEW_LICENSE_TEXT = "Your new license text here"
```

**Example**:
```python
OLD_LICENSE_TEXT = "Copyright (c) 2024 MyCompany"
NEW_LICENSE_TEXT = "Copyright (c) 2025 MyCompany"
```

**Features**:
- Recursively scans all subdirectories
- Reports which files were updated
- Safe - only modifies files containing the old license text
- UTF-8 encoding support for international characters

---

## JetBrains Integration

JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm, etc.) have excellent git integration that makes working with the license update workflow seamless.

### Git Integration Setup

**Automatic Updates**:
1. Go to Settings/Preferences → Version Control → Confirmation
2. Enable "Auto-update if push of the current branch was rejected"
3. Go to Settings/Preferences → Tools → Startup Tasks
4. Add a custom task to run `git pull` on project open

**Pull Updates**:
- Use `VCS → Git → Pull` (Ctrl+T / Cmd+T)
- Or enable auto-fetch in Background Tasks

### File Watchers

Configure File Watchers to monitor markdown file changes and trigger actions:

1. Go to Settings/Preferences → Tools → File Watchers
2. Click the "+" button to add a new watcher
3. Configure:
   - **File type**: Markdown
   - **Scope**: Project Files
   - **Program**: Path to your update script or notification tool
   - **Arguments**: Configure as needed

**Example Configuration**:
- **Name**: License Update Notifier
- **File type**: Markdown
- **Scope**: Project Files
- **Program**: `python3`
- **Arguments**: `$ProjectFileDir$/scripts/update_license.py $FilePath$`
- **Output paths**: Not needed
- **Show console**: On error

### Commit Template

Create a commit template for license updates:

1. Go to Settings/Preferences → Version Control → Commit
2. Add a commit template for license-related changes:
   ```
   Auto-update license details
   
   - Updated license text in markdown files
   - Synced with repository license policy
   ```

---

## Best Practices and Cautions

### Testing

⚠️ **Always test on a separate branch first**
- Create a test branch: `git checkout -b test-license-update`
- Run the workflow manually via `workflow_dispatch`
- Review changes carefully before merging to main

### Security

🔒 **Protect sensitive information**
- Never hardcode credentials in the workflow file
- Always use GitHub Secrets for sensitive data
- Use repository secrets for `GIT_USER_EMAIL` and `GIT_USER_NAME`
- Consider using environment-specific secrets for different environments

### Version Control

📝 **Maintain clean history**
- Use meaningful commit messages
- Consider squashing multiple license update commits
- Tag major license changes for easy reference

### Backup

💾 **Backup before bulk changes**
- Create a backup branch before running license updates
- Keep a copy of your vault/repository before large replacements
- Consider using git tags to mark pre-update state

### Review Process

👁️ **Manual review is important**
- Review the diff before merging automated commits
- Ensure license text was replaced correctly
- Check that formatting and markdown syntax remain intact
- Verify no unintended replacements occurred

---

## Troubleshooting

### Workflow Not Running

**Check**:
- GitHub Actions are enabled for your repository
- You have the required secrets configured
- The workflow file syntax is valid (check Actions tab for errors)

### Permission Errors

**Solution**:
- Ensure the GitHub token has write permissions
- Check repository settings → Actions → Workflow permissions
- Should be set to "Read and write permissions"

### Script Not Finding Files

**Check**:
- Current working directory when running the script
- File path patterns and wildcards
- File permissions for reading/writing

### Changes Not Committing

**Verify**:
- Git user email and name are configured correctly
- There are actual changes to commit (files were modified)
- No git hooks are preventing commits

---

## Advanced Customizations

### Sophisticated Python CLI Tool

For more advanced requirements, consider extending the Python script with:

- **Command-line arguments** for custom license text
- **Configuration file** support (YAML/JSON)
- **Dry-run mode** to preview changes
- **Regex support** for pattern matching
- **Backup creation** before modifications
- **Multiple license formats** (header vs. full text)
- **Exclusion patterns** to skip certain files

### License Header Formats

Support different license header styles:

```python
# Example: Add license header to files without one
HEADER_TEMPLATE = """
<!--
Copyright (c) {year} {author}
Licensed under {license_type}
-->
"""
```

### Integration with Other Tools

Consider integrating with:
- **pre-commit hooks** - Validate license headers before commits
- **CI/CD pipelines** - Check license compliance in pull requests
- **Documentation generators** - Auto-generate license documentation
- **License scanners** - Automated license compliance checking

---

## Questions or Enhancements?

If you need additional functionality:

- **Sophisticated Python CLI tool** for license management
- **Specific license header formats** or templates
- **Integration with other platforms** or tools
- **Custom automation workflows** for your use case

Please open an issue or submit a pull request with your requirements!
