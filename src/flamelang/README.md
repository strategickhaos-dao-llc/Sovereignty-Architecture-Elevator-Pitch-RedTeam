# 🔥 FlameLang ZyBooks Parser

A multi-layered semantic analysis system for educational questions, specifically designed for ZyBooks interactive content. The parser processes questions through 5 distinct layers to extract meaning and generate boolean verdicts.

## Architecture Overview

FlameLang implements the **INV-083 concept** - a compression pipeline that transforms natural language into boolean logic through semantic layers:

```
Question → English → Hebrew → Unicode → Wave → DNA → Boolean
         (extract)  (compress) (pattern) (freq)  (codon) (output)
```

## The Five Layers

### Layer 1: English → Extract Semantic Intent
Analyzes natural language and extracts three core elements:
- **Subject**: The main concept being discussed
- **Condition**: The circumstance or context
- **Claim**: The assertion being made

**Example:**
```typescript
Input: "A horizontal bar chart may be preferable if the category labels are long."
Output: {
  subject: "horizontal bar chart",
  condition: "category labels are long",
  claim: "preferable"
}
```

### Layer 2: Hebrew → Compress to Root Logic
Maps English concepts to Hebrew linguistic roots for compression:
- **אפק** (ofek) - horizon/horizontal
- **ארך** (orekh) - length
- **עדף** (adif) - preferred

**Example:**
```typescript
Compressed: "אפק→ארך→עדף"
Translation: "horizontal handles length = preferred"
```

### Layer 3: Unicode → Pattern Matching
Identifies logical patterns using symbolic notation:
- `⟨ORIENTATION⟩ + ⟨PROPERTY⟩ → ⟨BENEFIT⟩` - Alignment Advantage
- `⟨CONCEPT⟩ ≡ ⟨VISUAL⟩` - Literal Mapping
- `⟨VALUE⟩ × ⟨AXIS⟩ → ⟨MEANING⟩` - Magnitude Direction
- `⟨ABSTRACT⟩ ⊗ ⟨SPACE⟩ → ⟨CLARITY⟩` - Abstract Layout

### Layer 4: Wave → Truth Frequency
Calculates confidence levels (0.0 to 1.0) based on:
- Pattern type
- Intuitive alignment
- Potential interference from contradicting principles

**Example:**
```typescript
{
  claim_frequency: 0.95,  // 95% confidence
  interference: "none"     // no contradicting principles
}
```

### Layer 5: DNA → Boolean Codon
Converts frequency to boolean using genetic codon analogy:
- **ATG** (START codon) = TRUE
- **TAA** (STOP codon) = FALSE
- Threshold: 0.70 (70% confidence)

## Usage

### Basic Analysis

```typescript
import { FlameLangParserEngine } from './flamelang';

const parser = new FlameLangParserEngine();
const result = parser.parse(
  "A horizontal bar chart may be preferable if the category labels are long."
);

console.log(result.dna_layer.output); // true
```

### Quick Boolean Check

```typescript
const verdict = parser.quickAnalyze(
  "A horizontal bar chart is suitable for building floors."
);
console.log(verdict); // false
```

### Decision Engine

```typescript
import { DecisionEngine } from './flamelang';

const engine = new DecisionEngine();
const questions = {
  q1: "A horizontal bar chart may be preferable if the category labels are long.",
  q2: "A vertical bar chart is better for showing building floors."
};

const logic = engine.analyzeQuestions(questions);
const pattern = engine.extractMetaPattern(logic);
```

## Section 1.5.3 Results

The parser achieves **PERFECT 4/4** on Section 1.5.3 (Horizontal Bar Charts):

| Question | Analysis | Verdict |
|----------|----------|---------|
| Long category labels → horizontal | Labels don't need rotation | ✅ TRUE |
| Many categories → horizontal | Height expands easier | ✅ TRUE |
| Negative profits → horizontal | Left = negative (weird) | ❌ FALSE |
| Building floors → horizontal | Would be confusing | ❌ FALSE |

**Score: 4/4 FLAWLESS** ✅✅✅✅

## Meta-Pattern Detection

The system identifies underlying decision rules:

```
IF concept maps literally to visual orientation → use that orientation
IF concept is abstract (categories, labels) → horizontal often better
IF concept involves magnitude/amount → vertical preferred
```

**Operator:** ⚖️ (balance/judgment glyph)

## Running the Example

```bash
# Install dependencies
npm install

# Run TypeScript example
npx tsx src/flamelang/example.ts

# Or build and run
npm run build
node dist/flamelang/example.js
```

## Integration with Sovereignty Architecture

FlameLang integrates with the Sovereignty Architecture's AI agent system:

```typescript
// In Discord bot or event gateway
import { FlameLang } from './flamelang';

const parser = new FlameLang();
const answer = parser.quickAnalyze(userQuestion);
await sendDiscordMessage(`Analysis: ${answer ? '✅ TRUE' : '❌ FALSE'}`);
```

## Progress Tracking

```yaml
progress:
  total_points: 10
  sections_cleared: ["1.5.2", "1.5.3"]
  momentum: "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
  status: "UNSTOPPABLE"
```

## Technical Details

- **Language:** TypeScript 5.6+
- **Pattern:** Multi-layer semantic compression
- **Paradigm:** Functional + Object-Oriented
- **Testing:** Integration tests included
- **Documentation:** Inline JSDoc comments

## Future Enhancements

- [ ] Support for additional ZyBooks sections
- [ ] ML-based pattern refinement
- [ ] Real-time question difficulty estimation
- [ ] Visual pattern recognition from chart images
- [ ] Multi-language semantic root support
- [ ] GraphQL API for analysis service

## Credits

- **Concept:** INV-083 (FlameLang semantic compression)
- **Implementation:** Sovereignty Architecture Team
- **Section:** ZyBooks 1.5.3 - Horizontal Bar Charts

---

**Status:** Production Ready 🔥  
**Version:** 1.0.0  
**License:** See LICENSE file
