# External Artifacts System - Usage Examples

This document demonstrates real-world usage of the External Artifacts Ledger System.

## Example 1: Adding a Claude AI Discussion

```bash
# Navigate to the tools directory
cd tools

# Add the artifact with all details
python append_artifact.py \
  "https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56" \
  "Design of meta-evolution and legal compliance synthesizer engine." \
  --notes "Used as upstream design context for NHES and LSEE implementations."
```

**Output:**
```
✅ Appended artifact to external_artifacts.jsonl: https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56
```

## Example 2: Adding to a Custom Ledger

```bash
# Add a legal discussion to a separate ledger
python append_artifact.py \
  "https://claude.ai/share/legal-discussion-456" \
  "UPL compliance framework and DAO governance structures" \
  --ledger "../legal_evolution_ledger.jsonl" \
  --type "legal_design_discussion" \
  --notes "Foundation for legal strategy evolution engine (LSEE)"
```

## Example 3: Viewing Current Artifacts

```bash
# View all artifacts in the main ledger
cat ../external_artifacts.jsonl | python -m json.tool

# Or parse and display nicely
python -c "
import json
with open('../external_artifacts.jsonl') as f:
    for line in f:
        entry = json.loads(line)
        print(f\"[{entry['timestamp']}] {entry['summary']}\")
        print(f\"  Source: {entry['source']}\")
        if 'notes' in entry:
            print(f\"  Notes: {entry['notes']}\")
        print()
"
```

## Example 4: Creating Documentation from Template

```bash
# Copy the template
cp ../templates/external_ai_discussion_template.md ../docs/ai_discussion_meta_evolution.md

# Edit to fill in details for the actual discussion
# Then commit both the ledger and the documentation together
git add external_artifacts.jsonl docs/ai_discussion_meta_evolution.md
git commit -m "Add meta-evolution design discussion artifact and documentation"
```

## Example 5: Integration with Code

```python
# In your Python code, reference the artifact:

# File: src/neural_heir_evolution.py
"""
Neural Heir Evolution System (NHES)

Implementation based on external design discussion:
https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56

See external_artifacts.jsonl for full artifact details.
"""

class NeuralHeirEvolutionSystem:
    """
    NHES: Evolves AI agent capabilities across generations
    Design source: External artifact 2025-11-21T03:06:35Z
    """
    pass
```

## Example 6: Querying Artifacts by Type

```python
import json
from pathlib import Path

def get_artifacts_by_type(artifact_type, ledger_path="external_artifacts.jsonl"):
    """Find all artifacts of a specific type"""
    matches = []
    with open(ledger_path, 'r') as f:
        for line in f:
            entry = json.loads(line)
            if entry['type'] == artifact_type:
                matches.append(entry)
    return matches

# Get all legal discussions
legal_artifacts = get_artifacts_by_type("legal_design_discussion")
for artifact in legal_artifacts:
    print(f"Legal artifact: {artifact['summary']}")
```

## Example 7: Automation in CI/CD

```yaml
# .github/workflows/deploy.yml
- name: Log deployment artifact
  run: |
    python tools/append_artifact.py \
      "${{ github.event.head_commit.url }}" \
      "Deployment commit: ${{ github.event.head_commit.message }}" \
      --type "deployment_commit" \
      --notes "Automated deployment to production"
```

## Example 8: Complete Workflow

```bash
# 1. Have a design discussion in Claude
# 2. Get shareable link
# 3. Add to ledger
python tools/append_artifact.py \
  "https://claude.ai/share/new-feature-789" \
  "Design of distributed consensus for DAO voting" \
  --notes "Influences voting_system.py implementation"

# 4. Implement the feature
cat > src/voting_system.py << 'PYTHON'
"""
DAO Voting System with Distributed Consensus

Design source: https://claude.ai/share/new-feature-789
See external_artifacts.jsonl entry from 2025-11-21
"""

def distributed_vote_consensus():
    # Implementation...
    pass
PYTHON

# 5. Create documentation
cp templates/external_ai_discussion_template.md docs/voting_consensus_design.md
# Edit the documentation...

# 6. Commit everything together
git add external_artifacts.jsonl src/voting_system.py docs/voting_consensus_design.md
git commit -m "Implement distributed voting consensus based on external design artifact"
```

---

These examples demonstrate how the External Artifacts Ledger System integrates seamlessly into development workflows, providing traceability from design discussions to implementation.
