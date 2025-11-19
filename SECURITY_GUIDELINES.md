# Security Guidelines

## Protecting Sensitive Information

### ⚠️ Do NOT Commit or Share Local File Paths

**Never include local file system paths in:**
- Code commits
- Documentation
- Discord messages
- GitHub issues or PRs
- Configuration files
- Log outputs
- Screenshots

### ❌ Examples of Paths to AVOID:

```
C:\Users\[username]\Downloads\...
C:\Users\[username]\Documents\...
/Users/[username]/Downloads/...
/home/[username]/projects/...
```

### ✅ Use Generic Placeholder Paths Instead:

```
C:\projects\strategic-khaos\
/opt/strategic-khaos/
~/strategic-khaos/
./local-workspace/
```

## Why This Matters

Local file paths can reveal:
- Your operating system username
- Your computer's file structure
- Potentially sensitive project locations
- Personal information that shouldn't be public

## What To Do If You Accidentally Shared a Local Path

1. **Don't panic** - The information is usually not critically sensitive
2. **Remove it** - Edit or delete the message/commit where it appeared
3. **Report it** - Let the team know so we can clean up any propagation
4. **Learn** - Use placeholders and environment variables going forward

## Best Practices

### For Configuration Files:
- Use environment variables: `$PROJECT_ROOT`, `$HOME`, `%USERPROFILE%`
- Use relative paths: `./data`, `../config`
- Document required paths in README without using real examples

### For Documentation:
- Use placeholder usernames: `<username>`, `[your-username]`
- Use generic paths: `/path/to/project`, `C:\path\to\project`
- Provide templates that users can customize

### For Sharing Work:
- Use relative paths from project root
- Refer to files by their repo path: `src/main.py` not `C:\Users\me\project\src\main.py`
- When showing directory structures, use generic examples

## Repository-Specific Guidelines

For this Strategic Khaos / Sovereignty Architecture project:

✅ **Good Examples:**
```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Run deployment
./bootstrap/deploy.sh

# Configure
export PROJECT_ROOT=$(pwd)
```

❌ **Bad Examples:**
```bash
# Don't include paths like this:
cd C:\Users\domenic.garza\Downloads\strategic-khaos-master\
cd /Users/jane/Desktop/my-secret-projects/strategic-khaos/
```

## Automated Protection

This repository uses:
- `.gitignore` to prevent committing sensitive files
- Pre-commit hooks to scan for common sensitive patterns
- CI/CD checks to validate configuration files

## Questions?

If you're unsure whether something is safe to share, ask in the team channel before posting.

---

**Remember: When in doubt, use a placeholder!**
