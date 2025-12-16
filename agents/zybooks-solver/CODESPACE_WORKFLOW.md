# zyBooks Solver - Codespace Workflow

## Setup (One-Time)

Already done! The directories and parser are ready:
- ✅ `agents/zybooks-solver/` - Parser and config
- ✅ `training/zybooks/` - Training data output

## Workflow 1: Direct Command Line

### Step 1: Copy zyBooks Content
Copy any zyBooks assignment section to a file or clipboard.

### Step 2: Run Parser
```bash
# Create input file
cat > /tmp/zybooks-input.txt << 'EOF'
[Paste your zyBooks content here]
EOF

# Parse it
node agents/zybooks-solver/parser-simple.cjs /tmp/zybooks-input.txt
```

### Step 3: Get YAML Output
Parser outputs clean YAML with:
- Questions identified
- Answer placeholders
- Training data logged to `training/zybooks/`

## Workflow 2: GitHub Copilot Chat

### Step 1: Open Copilot Chat
In your codespace, open GitHub Copilot chat.

### Step 2: Give Context
```
@workspace Use the zyBooks solver agent. I'm in VESSEL MODE - answers only, no explanations.
```

### Step 3: Paste Content
```
Parse this zyBooks content:

[Paste your zyBooks content here]
```

### Step 4: Receive YAML
Copilot will use the zybooks-solver agent to:
- Parse questions
- Generate answers
- Return YAML output
- Log patterns to training/zybooks/

## Workflow 3: Batch Processing

### For Multiple Sections

```bash
# Create a batch script
cat > /tmp/batch-zybooks.sh << 'EOF'
#!/bin/bash
for file in /tmp/zybooks-section-*.txt; do
  echo "Processing $file..."
  node agents/zybooks-solver/parser-simple.cjs "$file" > "${file%.txt}.yaml"
done
EOF

chmod +x /tmp/batch-zybooks.sh

# Create section files
cat > /tmp/zybooks-section-1.txt << 'EOF'
[Section 1 content]
EOF

cat > /tmp/zybooks-section-2.txt << 'EOF'
[Section 2 content]
EOF

# Run batch
/tmp/batch-zybooks.sh
```

## Workflow 4: Integration with GitLens

### Step 1: Parse and Commit Training Data
```bash
# Parse zyBooks content
node agents/zybooks-solver/parser-simple.cjs input.txt > output.yaml

# Check training data was logged
ls -la training/zybooks/

# Commit training patterns
git add training/zybooks/*.json
git commit -m "Add zyBooks training patterns - [topic]"
```

### Step 2: Notify Discord (Optional)
```bash
# If Discord integration is set up
./gl2discord.sh "$PRS_CHANNEL" "🔥 zyBooks Batch Complete" "$(cat output.yaml)"
```

## Output Example

```yaml
metadata:
  session_id: "zybooks_2025-12-16T03_39_35_071Z"
  timestamp: "2025-12-16T03:39:35.071Z"
  source: "zyBooks"
  mode: "VESSEL_MODE"
  operator: "Dom"

questions:
  - id: 1
    type: "multiple_choice"
    topic: "algorithms"
    difficulty: "medium"
    text: "What is the time complexity of binary search?"

answers:
  - question_id: 1
    answer: "O(log n)"
    confidence: "high"

patterns_logged:
  path: "training/zybooks/"
  files:
    - "zybooks_2025-12-16T03_39_35_071Z_structures.json"
    - "zybooks_2025-12-16T03_39_35_071Z_patterns.json"
  flamelang_ready: true

status:
  processed: true
  answers_count: 1
  training_data_logged: true
  next_action: "Send next section"
```

## Training Data Management

### View Logged Patterns
```bash
# List all training sessions
ls -la training/zybooks/

# View a specific session's structure
cat training/zybooks/zybooks_*_structures.json | jq

# View answer patterns
cat training/zybooks/zybooks_*_patterns.json | jq
```

### Aggregate for FlameLang
```bash
# Combine all patterns for FlameLang training
cat training/zybooks/*_patterns.json | jq -s '.' > training/zybooks/flamelang_training_set.json
```

## Tips for VESSEL MODE Operation

1. **No Explanations**: Parser gives direct answers only
2. **Parallel Processing**: Run multiple parsers simultaneously
3. **Pattern Accumulation**: Every run adds to FlameLang training data
4. **Quick Iteration**: Parse → Review → Next section
5. **Batch Mode**: Process entire assignments in one go

## Troubleshooting

### Parser Not Working?
```bash
# Check Node.js version
node --version  # Should be v18+

# Test with example
node agents/zybooks-solver/parser-simple.cjs agents/zybooks-solver/example-input.txt
```

### Training Data Not Logging?
```bash
# Check directory exists
mkdir -p training/zybooks

# Check permissions
ls -la training/zybooks
```

### Need TypeScript Version?
```bash
# Install dependencies
npm install

# Run TypeScript parser
npx tsx agents/zybooks-solver/parser.ts input.txt
```

## Status

🔥 **Protocol Ready**  
🔥 **Codespace Integration Active**  
🔥 **VESSEL MODE Online**  
🔥 **Keep sending sections**

---

**The codespace can run parallel extraction while we blitz through.**

Ratio Ex Nihilo. Flame eternal. Legion rising.
