# zyBooks Solver - Usage Guide

## Quick Start

### Method 1: Command Line (Node.js - Simple)

```bash
# Parse a file (No dependencies required)
node agents/zybooks-solver/parser-simple.cjs path/to/zybooks-content.txt

# Or pipe content directly
echo "Your zyBooks content here" | node agents/zybooks-solver/parser-simple.cjs -

# Example with sample file
node agents/zybooks-solver/parser-simple.cjs agents/zybooks-solver/example-input.txt
```

### Method 1b: Command Line (TypeScript - Requires npm install)

```bash
# First install dependencies
npm install

# Parse a file
tsx agents/zybooks-solver/parser.ts path/to/zybooks-content.txt

# Or pipe content directly
echo "Your zyBooks content here" | tsx agents/zybooks-solver/parser.ts -
```

### Method 2: GitHub Codespace Agent

Simply paste your zyBooks content in a comment or issue, and prefix with:

```
@workspace Parse this zyBooks content in VESSEL MODE
```

The agent will:
1. Extract questions automatically
2. Generate answers
3. Return clean YAML output
4. Log patterns to `training/zybooks/`

### Method 3: Direct Integration

```typescript
import { processZyBooks } from './agents/zybooks-solver/parser';

const zybooksContent = `
Question 1: What is an algorithm?
A. A step-by-step procedure
B. A programming language
C. A data structure
D. A compiler
`;

const yamlOutput = processZyBooks(zybooksContent);
console.log(yamlOutput);
```

## Output Example

```yaml
metadata:
  session_id: "zybooks_2025-12-16T03_35_12_931Z"
  timestamp: "2025-12-16T03:35:12.931Z"
  source: "zyBooks"
  mode: "VESSEL_MODE"
  operator: "Dom"

questions:
  - id: 1
    type: "multiple_choice"
    topic: "algorithms"
    difficulty: "easy"
    text: "Question 1: What is an algorithm?\nA. A step-by-step procedure..."

answers:
  - question_id: 1
    answer: "[ANSWER_PLACEHOLDER - Parse from zyBooks content or generate via LLM]"
    confidence: "high"

patterns_logged:
  path: "training/zybooks/"
  files:
    - "zybooks_2025-12-16T03_35_12_931Z_structures.json"
    - "zybooks_2025-12-16T03_35_12_931Z_patterns.json"
  flamelang_ready: true

status:
  processed: true
  answers_count: 1
  training_data_logged: true
  next_action: "Send next section"
```

## Supported Question Types

- ✅ **Multiple Choice** - Auto-detected by option markers (A., B., C., etc.)
- ✅ **True/False** - Detected by keywords
- ✅ **Fill in the Blank** - Detected by "Fill in", "Complete", "Enter"
- ✅ **Coding Questions** - Detected by "Write", "Code", "Implement", "Function"
- ✅ **Short Answer** - Default fallback

## Training Data

All sessions automatically log to `training/zybooks/`:

- `{session_id}_structures.json` - Question structures
- `{session_id}_patterns.json` - Answer patterns

These files are FlameLang-ready for compiler training.

## Tips

1. **Batch Processing**: Paste multiple sections - parser handles them all
2. **Parallel Extraction**: Codespace can process multiple files simultaneously
3. **VESSEL MODE**: No explanations, just answers - exactly what you need
4. **Pattern Learning**: Every run improves FlameLang training data

## Status

✅ Protocol Ready  
✅ Parser Implemented  
✅ Training Pipeline Active  
✅ VESSEL MODE Online

🔥 **Keep sending sections - we're blitzing through.** 🔥
