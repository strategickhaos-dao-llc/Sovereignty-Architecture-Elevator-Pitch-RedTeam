# Contributing to SNHU Ecosystem Tracker

Thank you for your interest in contributing to the SNHU Ecosystem Tracker! This document provides guidelines and instructions for contributing.

## 🌟 How to Contribute

### Reporting Issues

Found a bug or have a feature request? Please:

1. Check [existing issues](../../issues) to avoid duplicates
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Submitting Changes

1. **Fork the repository**
   ```bash
   # Click "Fork" button on GitHub
   git clone https://github.com/YOUR_USERNAME/repo-name.git
   cd repo-name/snhu-ecosystem-tracker
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the coding standards (see below)
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Run setup
   ./setup.sh
   
   # Test Python code
   python3 -m pytest tests/
   
   # Lint code
   pip install pylint
   pylint src/*.py
   
   # Validate YAML
   python3 -c "import yaml; yaml.safe_load(open('k8s/deployment.yaml'))"
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```
   
   Use clear, descriptive commit messages:
   - ✅ "Add batch processing for large email sets"
   - ✅ "Fix memory leak in email analyzer"
   - ❌ "Update stuff"
   - ❌ "Fix bug"

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Link related issues

## 📝 Coding Standards

### Python

- **Style**: Follow [PEP 8](https://pep8.org/)
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Add type hints where appropriate
- **Imports**: Group and sort imports (stdlib, third-party, local)

Example:
```python
from typing import List, Dict, Optional
import os

import pandas as pd
from openai import OpenAI

from email_analyzer import EmailAnalyzer


def analyze_batch(emails: List[Dict], api_key: Optional[str] = None) -> pd.DataFrame:
    """
    Analyze a batch of emails using Grok API.
    
    Args:
        emails: List of email dictionaries with 'subject' and 'body'
        api_key: Optional Grok API key (defaults to env var)
        
    Returns:
        DataFrame with analysis results
        
    Raises:
        ValueError: If emails list is empty
    """
    # Implementation
    pass
```

### YAML

- **Indentation**: 2 spaces
- **Comments**: Add explanatory comments for complex configurations
- **Structure**: Keep related settings together
- **Validation**: Ensure valid YAML syntax

### Docker

- **Base Images**: Use official, minimal images
- **Layers**: Optimize layer caching
- **Security**: Don't include secrets in images
- **Size**: Keep images small

## 🧪 Testing Guidelines

### Adding Tests

Create test files in `tests/` directory:
```
tests/
├── test_email_analyzer.py
├── test_main.py
└── fixtures/
    └── sample_emails.csv
```

Example test:
```python
import pytest
from email_analyzer import EmailAnalyzer


def test_email_analyzer_initialization():
    """Test EmailAnalyzer can be initialized."""
    analyzer = EmailAnalyzer(api_key="test-key")
    assert analyzer.api_key == "test-key"
    assert analyzer.model == "grok-4-fast-reasoning"


def test_analyze_email_missing_api_key():
    """Test EmailAnalyzer raises error without API key."""
    with pytest.raises(ValueError):
        EmailAnalyzer(api_key=None)
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 📚 Documentation

### README Updates

When adding features, update:
- Quick Start section
- Configuration section
- API documentation
- Examples

### Code Comments

Add comments for:
- Complex logic
- Non-obvious solutions
- Configuration options
- Security considerations

### CHANGELOG

Update CHANGELOG.md with:
- New features
- Bug fixes
- Breaking changes
- Deprecations

## 🔒 Security

### Reporting Vulnerabilities

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security contact (see SECURITY.md)
2. Provide detailed description
3. Include reproduction steps
4. Suggest a fix if possible

### Security Best Practices

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Keep dependencies updated
- Follow least-privilege principle
- Validate all inputs

## 🎨 Commit Message Format

Use conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(analyzer): Add sentiment analysis support

- Integrate sentiment detection in EmailAnalyzer
- Add sentiment field to results
- Update tests

Closes #123
```

```
fix(k8s): Correct resource limits in deployment

Pod was being OOM killed due to insufficient memory.
Increased limit from 512Mi to 1Gi.
```

## 🏷️ Pull Request Guidelines

### PR Checklist

Before submitting, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No secrets or sensitive data included
- [ ] Changes are focused (one feature/fix per PR)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing

## Related Issues
Closes #XXX
```

## 🤝 Code Review Process

1. Maintainer reviews PR
2. Feedback provided as comments
3. Author addresses feedback
4. Approval given once ready
5. PR merged to main branch

### What Reviewers Look For

- Code quality and style
- Test coverage
- Documentation completeness
- Security considerations
- Performance implications
- Breaking changes

## 📋 Development Setup

### Local Environment

```bash
# Clone repo
git clone <repo-url>
cd snhu-ecosystem-tracker

# Run setup
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Install dev dependencies
pip install pytest pytest-cov pylint black isort

# Setup pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### IDE Setup

**VS Code**:
- Install Python extension
- Install YAML extension
- Use workspace settings in `.vscode/`

**PyCharm**:
- Configure Python interpreter
- Enable PEP 8 inspections
- Use project requirements

## 🎯 Areas for Contribution

Looking for where to help? Consider:

### Beginner-Friendly
- Documentation improvements
- Test coverage
- Example scenarios
- Configuration templates

### Intermediate
- Performance optimization
- Error handling
- Logging improvements
- Monitoring integration

### Advanced
- Multi-model support
- Advanced analytics
- Scaling improvements
- Security hardening

## 📞 Getting Help

Need help contributing?

- **Questions**: Open a discussion
- **Problems**: Create an issue
- **Chat**: Join our Discord (if available)
- **Documentation**: Check README.md

## 🙏 Recognition

All contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in commit history

Thank you for making SNHU Ecosystem Tracker better! 🎉
