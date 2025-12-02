# Roadmap A: Hyper-Practical - "Just Make My Chaos 10× Cleaner"

**Zero theory. Maximum pragmatism. Copy-paste ready.**

This roadmap gives you 30 immediately actionable items to organize your experimental chaos without learning any "software architecture theory." Everything here is a concrete action you can take today.

## Philosophy

You're already building fast and shipping code that works. This roadmap just adds the minimum structure so:
- You can find things later
- Your heirs can understand what you built
- Refactoring doesn't break everything
- You can scale from 5 nodes to 50 without rewriting

## Quick Start

```powershell
# Run the auto-cleanup scripts
./roadmaps/roadmap-a/scripts/01-organize-folders.ps1
./roadmaps/roadmap-a/scripts/02-naming-conventions.ps1
./roadmaps/roadmap-a/scripts/03-auto-clean-repos.ps1

# Deploy to all 5 nodes
./roadmaps/roadmap-a/scripts/deploy-to-cluster.ps1
```

## The 30 Items

### Section 1: Naming Conventions (Items 1-10)

#### 1. Folder Structure Template
```
project-root/
├── src/              # All source code
├── tests/            # All tests (even if empty for now)
├── scripts/          # Automation scripts
├── configs/          # Configuration files
├── docs/             # Documentation
├── examples/         # Example usage
└── tools/            # Development tools
```

#### 2. File Naming Pattern
- Use lowercase with hyphens: `user-service.py`, `data-processor.js`
- Prefix test files: `test-user-service.py`
- Prefix scripts: `run-deployment.sh`, `clean-artifacts.ps1`

#### 3. Variable Naming Standard
- Python: `snake_case` for variables/functions, `PascalCase` for classes
- JavaScript/TypeScript: `camelCase` for variables/functions, `PascalCase` for classes
- Constants: `UPPER_SNAKE_CASE`

#### 4. Function Naming Pattern
- Verbs first: `get_user()`, `create_database()`, `validate_input()`
- Boolean returns: `is_valid()`, `has_permission()`, `can_execute()`

#### 5. Class Naming Pattern
- Singular nouns: `UserService`, `DataProcessor`, `ConfigManager`
- Avoid generic names: Use `LegalDocumentRefinery` not `Processor`

#### 6. Configuration File Naming
- Environment-specific: `config.dev.yml`, `config.prod.yml`
- Service-specific: `postgres.config.yml`, `discord.config.yml`

#### 7. Script Naming Convention
- Action-based: `deploy-app.sh`, `backup-database.ps1`, `test-integration.sh`
- Numbered for sequences: `01-setup.sh`, `02-migrate.sh`, `03-validate.sh`

#### 8. Docker Image Naming
- Format: `org/project-component:tag`
- Example: `strategickhaos/refinory-api:v1.0.0`

#### 9. Git Branch Naming
- Feature: `feature/user-authentication`
- Bugfix: `bugfix/login-error`
- Hotfix: `hotfix/security-patch`

#### 10. Environment Variable Naming
- Prefix with service: `DISCORD_BOT_TOKEN`, `POSTGRES_CONNECTION_STRING`
- Use descriptive names: `MAX_RETRY_ATTEMPTS` not `MAX_R`

### Section 2: One-File-Per-Responsibility (Items 11-20)

#### 11. Separate Configuration from Logic
**Before:**
```python
# user_service.py (500 lines)
DB_HOST = "localhost"
DB_PORT = 5432
class UserService: ...
def main(): ...
```

**After:**
```python
# config.py
DB_HOST = "localhost"
DB_PORT = 5432

# user_service.py
from config import DB_HOST, DB_PORT
class UserService: ...

# main.py
from user_service import UserService
def main(): ...
```

#### 12. Extract Database Layer
Move all database code to `database.py` or `db/`:
```python
# db/users.py
def get_user(user_id): ...
def create_user(data): ...

# services/user_service.py
from db.users import get_user, create_user
```

#### 13. Separate API Routes from Business Logic
```python
# routes/users.py (API layer)
@app.get("/users/{user_id}")
def get_user_endpoint(user_id):
    return user_service.get_user(user_id)

# services/user_service.py (business logic)
def get_user(user_id):
    # actual logic here
```

#### 14. Extract Constants and Enums
```python
# constants.py
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

class Status:
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"
```

#### 15. Separate Utilities from Core Logic
```python
# utils/validators.py
def validate_email(email): ...

# utils/formatters.py
def format_timestamp(ts): ...
```

#### 16. One Class Per File (for large classes)
```
services/
├── user_service.py       # UserService class only
├── auth_service.py       # AuthService class only
└── notification_service.py
```

#### 17. Group Related Functions in Modules
```python
# crypto/hashing.py
def hash_password(pwd): ...
def verify_password(pwd, hash): ...

# crypto/encryption.py
def encrypt_data(data): ...
def decrypt_data(encrypted): ...
```

#### 18. Separate Test Fixtures
```python
# tests/fixtures/users.py
def sample_user(): ...
def sample_admin(): ...

# tests/test_users.py
from fixtures.users import sample_user
```

#### 19. Extract Schemas/Models
```python
# models/user.py
class User:
    def __init__(self, id, name, email): ...

# models/document.py
class Document:
    def __init__(self, id, content): ...
```

#### 20. Example: Legal Refinery Refactor

**Before (legal/processor.py - 800 lines):**
```python
# Everything in one file
import everything
class LegalProcessor:
    def process_wyoming_sf0068(self): ...
    def analyze_compliance(self): ...
    def generate_report(self): ...
    def send_notifications(self): ...
```

**After (organized):**
```
legal/
├── models/
│   ├── document.py        # Document data model
│   └── compliance.py      # Compliance data model
├── processors/
│   ├── wyoming.py         # SF0068 specific logic
│   └── generic.py         # Generic processing
├── analyzers/
│   └── compliance.py      # Compliance analysis
├── reports/
│   └── generator.py       # Report generation
├── notifications/
│   └── sender.py          # Notification logic
└── config.py              # Configuration
```

### Section 3: Auto-Cleanup Scripts (Items 21-30)

#### 21. Add Missing LICENSE Files
Script: `scripts/01-add-licenses.ps1`
- Scans all subdirectories
- Adds LICENSE file if missing
- Uses your standard license template

#### 22. Clean Build Artifacts
Script: `scripts/02-clean-artifacts.ps1`
- Removes `__pycache__`, `*.pyc`
- Removes `node_modules` (keep package-lock.json)
- Removes `dist/`, `build/`

#### 23. Standardize README Files
Script: `scripts/03-standardize-readmes.ps1`
- Ensures every project has README.md
- Adds template sections: Purpose, Setup, Usage

#### 24. Update Ledger/Audit Trail
Script: `scripts/04-update-ledger.ps1`
- Tracks all significant changes
- Maintains chronological record
- Git-based or database-backed

#### 25. Validate Configuration Files
Script: `scripts/05-validate-configs.ps1`
- Checks all YAML/JSON syntax
- Validates required fields
- Reports missing environment variables

#### 26. Fix Import Statements
Script: `scripts/06-fix-imports.ps1`
- Organizes imports alphabetically
- Removes unused imports
- Groups stdlib, third-party, local

#### 27. Generate .gitignore
Script: `scripts/07-generate-gitignore.ps1`
- Creates comprehensive .gitignore
- Covers Python, Node, Docker
- Includes OS-specific files

#### 28. Standardize Docker Files
Script: `scripts/08-standardize-docker.ps1`
- Adds health checks
- Adds metadata labels
- Ensures multi-stage builds where appropriate

#### 29. Add Type Hints (Python)
Script: `scripts/09-add-type-hints.ps1`
- Uses mypy or pyright
- Adds basic type hints to function signatures
- Generates stubs for external libraries

#### 30. Generate Dependency Graph
Script: `scripts/10-generate-dep-graph.ps1`
- Creates visual dependency map
- Identifies circular dependencies
- Exports as SVG/PNG

## Installation

```powershell
# Install to all 5 nodes
./roadmaps/installers/install-roadmap-a.ps1 -Nodes @("node1", "node2", "node3", "node4", "node5")

# Or install locally
./roadmaps/installers/install-roadmap-a.ps1 -Local
```

## Usage Examples

### Quick Cleanup
```powershell
# Clean everything in one command
./roadmaps/roadmap-a/cleanup-all.ps1

# Or step by step
./roadmaps/roadmap-a/scripts/02-clean-artifacts.ps1
./roadmaps/roadmap-a/scripts/06-fix-imports.ps1
./roadmaps/roadmap-a/scripts/07-generate-gitignore.ps1
```

### Refactor a Department
```powershell
# Use the refactoring helper
./roadmaps/roadmap-a/refactor-department.ps1 -Department "legal"

# This will:
# 1. Analyze the current structure
# 2. Suggest the new structure
# 3. Generate migration script
# 4. Create backup before changes
```

### Validate Everything
```powershell
# Run all validators
./roadmaps/roadmap-a/validate-all.ps1

# Reports:
# - Naming convention violations
# - Missing documentation
# - Configuration errors
# - Circular dependencies
```

## Integration with Existing Workflow

1. **Run before commits:**
   ```bash
   # Add to .git/hooks/pre-commit
   ./roadmaps/roadmap-a/pre-commit-hook.ps1
   ```

2. **Run in CI/CD:**
   ```yaml
   # Add to GitHub Actions
   - name: Validate structure
     run: ./roadmaps/roadmap-a/validate-all.ps1
   ```

3. **Run on schedule:**
   ```powershell
   # Add to cron or Task Scheduler
   0 2 * * * /path/to/cleanup-all.ps1
   ```

## Next Steps

Once Roadmap A is working:
- **Stay here** if you just need clean chaos
- **Move to Roadmap B** if you want to understand why these patterns work
- **Jump to Roadmap C** if you're hitting architectural limits

## Success Metrics

You'll know Roadmap A is working when:
- [ ] You can find any file in <10 seconds
- [ ] New team members can navigate the codebase
- [ ] Refactoring one component doesn't break three others
- [ ] Your heirs can continue your work from the documentation
- [ ] Build artifacts are consistently cleaned
- [ ] All projects have proper licensing

---

**Remember:** This roadmap has zero theory. If you want to understand *why* these patterns exist, that's Roadmap B. For now, just copy-paste and move fast. 🚀
