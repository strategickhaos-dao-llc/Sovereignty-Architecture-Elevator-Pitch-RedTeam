# Prompt Brain - Strategic Khaos Knowledge Base

## 🧠 Unified Terminology & Navigation System

The Prompt Brain is a centralized knowledge management system that powers all AI agents, documentation, and interfaces across the Strategic Khaos swarm.

## Purpose

Every agent in the swarm pulls terminology, definitions, and navigation structure from this central brain. This ensures:
- **Consistent terminology** across all communications
- **Unified knowledge base** for AI agent responses
- **Centralized navigation** for all documentation
- **Semantic relationships** between concepts via thesaurus

## Components

### 📚 Thesaurus (`thesaurus.json`)
JSON-based synonym and relationship mapping for key concepts.

**Structure:**
```json
{
  "concept": ["related-term-1", "related-term-2", "synonym", ...],
  ...
}
```

**Purpose:**
- Semantic search and discovery
- AI agent context enhancement
- Natural language understanding
- Cross-referencing related topics

**Categories:**
- Neurospice & Sovereignty concepts
- Architecture terms
- Operations & Security
- AI Agents & Infrastructure
- Communication protocols

### 📕 Dictionary (`dictionary.md`)
Comprehensive definitions and explanations of Strategic Khaos terminology.

**Sections:**
- Core Concepts (Neurospice, Origin Node Zero, Mirror Generals)
- Architecture Terms (Control Plane, Sovereignty Architecture)
- Operations (Valoryield Engine, Quantum Symbolic Emulator)
- Security & Governance (RBAC, DAO Governance)
- AI Agent System (Prompt Manager, Context Window)
- Communication Protocols (Discord, Alexa Bridge)
- Infrastructure (Kubernetes, Observability Stack)
- Emoji Protocol (visual communication standards)
- Status Indicators (CRITICAL, NOMINAL, STANDBY, STEALTH)

**Usage:**
- AI agents reference for accurate definitions
- New team member onboarding
- External documentation
- Voice assistant responses (Alexa)

### 📖 Table of Contents (`table-of-contents.md`)
Comprehensive navigation structure for all documentation and systems.

**Organization:**
- Core Documentation
- Infrastructure Systems
- Integration Bridges
- AI Agent System
- Development & Testing
- Specialized Systems
- Legal & Governance
- External Integrations

**Features:**
- Wiki-style internal links
- Quick reference commands
- Key endpoints listing
- Voice command reference
- Mirror general reports

### 🎯 Prompt Manager (`prompt-manager.html`)
Web-based interface for interactive exploration of the Prompt Brain.

**Features:**
- Real-time swarm status display
- Interactive thesaurus browser
- Searchable table of contents
- Quick action buttons
- Live API connectivity test
- Responsive design

**Access:**
```bash
# Open in browser
open prompt-manager.html
# or
python3 -m http.server 8080
# Then visit: http://localhost:8080/prompt-manager.html
```

## Usage

### For AI Agents

AI agents automatically pull from the Prompt Brain:

```javascript
// Example: Agent referencing thesaurus
const thesaurus = require('./prompt-brain/thesaurus.json');
const relatedTerms = thesaurus['neurospice'];
// Returns: ["ascension", "sovereignty", "swarm-mind", ...]

// Example: Agent using dictionary definitions
// When asked "What is neurospice?", agent consults dictionary.md
```

### For Documentation

All documentation links to Prompt Brain:

```markdown
See [[prompt-brain/dictionary.md]] for terminology
Reference [[prompt-brain/table-of-contents.md]] for navigation
```

### For Voice Interfaces (Alexa)

Alexa responses use terminology from the brain:

```javascript
// Alexa skill pulls definitions
const response = `Neurospice levels ${level}. ${getDef('neurospice')}`;
```

### For Web Interfaces

The Prompt Manager provides real-time access:
1. Open `prompt-manager.html` in browser
2. Search thesaurus for related terms
3. Navigate table of contents
4. Test API connectivity

## Maintenance

### Adding New Terms

**To thesaurus.json:**
```json
{
  "new-concept": [
    "related-term-1",
    "related-term-2",
    "synonym"
  ]
}
```

**To dictionary.md:**
```markdown
### New Concept
Definition and explanation of the new concept, including usage examples
and relationships to other systems.
```

**To table-of-contents.md:**
```markdown
- [[new-documentation.md]] - Description
```

### Updating Definitions

1. Edit `dictionary.md` with clarifications
2. Update related terms in `thesaurus.json`
3. Verify links in `table-of-contents.md`
4. Update `prompt-manager.html` if categories change

### Version Control

All Prompt Brain files are version controlled:
- Commit changes with descriptive messages
- Tag major terminology updates
- Review changes that affect AI agent behavior

## Integration Points

### Discord Bot
```javascript
// Bot references prompt brain for context
const brain = require('../prompt-brain/thesaurus.json');
const context = brain[userQuery] || [];
```

### Alexa Skill
```javascript
// Alexa uses definitions for responses
const definitions = loadDictionary();
const response = definitions.find(term);
```

### Documentation Generator
```bash
# Auto-generate docs from prompt brain
./scripts/generate-docs.sh --source prompt-brain/
```

### CI/CD Pipeline
```yaml
# Validate prompt brain on commit
- name: Validate Prompt Brain
  run: |
    npm run validate-thesaurus
    npm run check-dictionary-links
```

## Best Practices

### Terminology Standards
- Use lowercase-with-hyphens for multi-word terms
- Keep definitions concise but comprehensive
- Include emoji protocol where appropriate
- Link related concepts bidirectionally

### Thesaurus Relationships
- Group by semantic category
- Include 5-10 related terms per concept
- Avoid circular references
- Update when adding new systems

### Navigation Structure
- Organize by user journey
- Provide quick reference sections
- Include command examples
- Link to external resources

### Web Interface
- Keep UI responsive
- Test on multiple browsers
- Maintain accessibility standards
- Update status indicators

## Testing

### Validate Thesaurus JSON
```bash
# Check JSON syntax
cat thesaurus.json | python3 -m json.tool > /dev/null
echo "✓ Thesaurus JSON valid"
```

### Check Dictionary Links
```bash
# Verify all markdown links
grep -o '\[\[.*\]\]' dictionary.md | while read link; do
  echo "Checking $link"
done
```

### Test Web Interface
```bash
# Start local server
cd prompt-brain
python3 -m http.server 8080
# Visit http://localhost:8080/prompt-manager.html
```

### Verify API Integration
```bash
# Test webhook connectivity
curl http://localhost:3000/api/swarm-status
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Prompt Brain System              │
├─────────────────────────────────────────┤
│                                          │
│  thesaurus.json ─┐                      │
│                   ├──→ AI Agents        │
│  dictionary.md ──┤                      │
│                   ├──→ Alexa Skill      │
│  table-of-contents.md ─┤                │
│                   ├──→ Discord Bot      │
│  prompt-manager.html ──┘                │
│                   └──→ Documentation    │
│                                          │
└─────────────────────────────────────────┘
```

## Quick Reference

### File Locations
- Thesaurus: `prompt-brain/thesaurus.json`
- Dictionary: `prompt-brain/dictionary.md`
- TOC: `prompt-brain/table-of-contents.md`
- Web UI: `prompt-brain/prompt-manager.html`

### Update Frequency
- Thesaurus: As new concepts emerge
- Dictionary: When definitions need clarification
- TOC: When documentation is added/moved
- Web UI: When categories or features change

### Access Control
- Read: All agents and users
- Write: Controlled via git permissions
- Deploy: Automatic on commit to main

## Future Enhancements

- [ ] API endpoint for programmatic access
- [ ] Version history and change tracking
- [ ] Multi-language support
- [ ] AI-powered suggestion system
- [ ] Real-time collaborative editing
- [ ] Integration with vector database
- [ ] Automated consistency checking
- [ ] Visual concept mapping

---

**🧠⚡🐐 Origin Node Zero**

*The Prompt Brain is the collective memory of the swarm.*
*Every agent draws knowledge from this source.*
*Every update propagates through the network.*

**Neurospice Level: CRITICAL**
**White Web Sovereignty: 92%**
**Status: ONLINE**
