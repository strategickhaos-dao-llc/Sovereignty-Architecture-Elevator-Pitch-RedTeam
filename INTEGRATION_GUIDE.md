# DomBrainCalculator Integration Guide

## Quick Start

### 1. Standalone Calculator (Python)

```bash
# Run the calculator directly
python3 dom_brain_calculator.py
```

This will run example calculations demonstrating the cognitive architecture.

### 2. Discord Bot Integration

#### Install Dependencies

```bash
pip install -r requirements.dombrain.txt
```

#### Setup Environment

Create a `.env` file:

```bash
DISCORD_TOKEN=your_discord_bot_token_here
```

#### Run Discord Bot

```bash
python3 dom_brain_discord.py
```

### 3. Import as Module

```python
from dom_brain_calculator import DomBrainCalculator

# Create calculator instance
calc = DomBrainCalculator(
    pathway_count=100,              # Number of solution pathways
    consolidation_threshold=0.3     # Minimum confidence to keep path
)

# Perform calculation
result = calc.calculate("What is 12 * 7?", 12, 7, '*')

# Show detailed work
calc.show_work(result, verbose=True)

# Access result components
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Collisions: {result['collision_count']}")
print(f"Dopamine hit: {result['dopamine_hit']}")
```

## Discord Commands

Once the bot is running and added to your server:

### `/brain_calc`
Perform a calculation using the cognitive architecture.

**Parameters:**
- `operation`: Choose +, -, *, /, or ^
- `first`: First number
- `second`: Second number

**Example:**
```
/brain_calc operation:+ first:5 second:3
```

**Response:**
- Answer with confidence score
- Number of pathways used
- Number of collisions detected
- Dopamine hit notification (if rediscovery)
- Top insight from collision analysis

### `/brain_explain`
Get an explanation of how the cognitive calculator works.

Shows the 5 phases:
1. Divergent Thinking
2. Memory Consolidation
3. Cross-Domain Pattern Matching
4. Collision Detection
5. Consensus Synthesis

### `/brain_stats`
View session statistics.

Shows:
- Total calculations performed
- Dopamine hits (rediscoveries)
- Average confidence
- Average collisions per calculation
- Recent problems

### `/brain_compare`
Compare traditional vs cognitive calculation approach.

**Parameters:**
- `operation`: Choose +, -, *, or /
- `first`: First number
- `second`: Second number

**Response:**
Shows side-by-side comparison:
- Traditional: Single method, 100% confidence, 0 insights
- Cognitive: Multiple pathways, weighted confidence, collision insights
- Difference analysis

## Integration with Existing Infrastructure

### 1. Add to Existing Discord Bot

If you already have a Discord bot:

```python
# In your bot's main file
from dom_brain_discord import DomBrainCommands

# Add the cog
bot.add_cog(DomBrainCommands(bot))
```

### 2. REST API Integration

Create a FastAPI wrapper:

```python
from fastapi import FastAPI
from dom_brain_calculator import DomBrainCalculator

app = FastAPI()
calc = DomBrainCalculator()

@app.post("/calculate")
async def calculate(operation: str, first: float, second: float):
    result = calc.calculate(f"{first} {operation} {second}", first, second, operation)
    return {
        "answer": result['answer'],
        "confidence": result['confidence'],
        "pathway_count": result['pathway_count'],
        "collision_count": result['collision_count']
    }
```

### 3. Sovereignty Architecture Integration

The calculator can be integrated into the existing sovereignty architecture:

```yaml
# In docker-compose.yml
services:
  dombrain-calculator:
    build:
      context: .
      dockerfile: Dockerfile.dombrain
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
    networks:
      - sovereignty-net
    depends_on:
      - discord-bot
      - event-gateway
```

Create `Dockerfile.dombrain`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.dombrain.txt .
RUN pip install --no-cache-dir -r requirements.dombrain.txt

COPY dom_brain_calculator.py .
COPY dom_brain_discord.py .

CMD ["python3", "dom_brain_discord.py"]
```

### 4. Prometheus Metrics Integration

Add metrics export:

```python
from prometheus_client import Counter, Histogram, Gauge
import prometheus_client

# Metrics
calculations_total = Counter('dombrain_calculations_total', 'Total calculations')
pathway_count = Histogram('dombrain_pathways', 'Number of pathways generated')
collision_count = Histogram('dombrain_collisions', 'Number of collisions detected')
confidence_score = Histogram('dombrain_confidence', 'Confidence score')
dopamine_hits = Counter('dombrain_dopamine_hits', 'Dopamine hits (rediscoveries)')

# In calculate method
def calculate_with_metrics(self, problem, a, b, op):
    result = self.calculate(problem, a, b, op)
    
    calculations_total.inc()
    pathway_count.observe(result['pathway_count'])
    collision_count.observe(result['collision_count'])
    confidence_score.observe(result['confidence'])
    if result['dopamine_hit']:
        dopamine_hits.inc()
    
    return result

# Start metrics server
prometheus_client.start_http_server(8000)
```

### 5. Grafana Dashboard

Example Prometheus queries for Grafana:

```promql
# Total calculations per hour
rate(dombrain_calculations_total[1h])

# Average confidence score
rate(dombrain_confidence_sum[5m]) / rate(dombrain_confidence_count[5m])

# Collision rate
rate(dombrain_collisions_sum[5m]) / rate(dombrain_collisions_count[5m])

# Dopamine hit rate (rediscovery rate)
rate(dombrain_dopamine_hits[5m]) / rate(dombrain_calculations_total[5m])
```

## Testing

### Run Unit Tests

```bash
python3 test_dom_brain_calculator.py
```

### Test Coverage

The test suite includes:
- Basic operations (addition, subtraction, multiplication, division)
- Memory consolidation
- Collision detection
- Dopamine hit mechanism
- Pathway diversity
- Confidence calculation
- Edge cases (zero division, large numbers, negative numbers)

### Add Custom Tests

```python
import unittest
from dom_brain_calculator import DomBrainCalculator

class TestCustomCalculations(unittest.TestCase):
    def setUp(self):
        self.calc = DomBrainCalculator(pathway_count=50)
    
    def test_my_calculation(self):
        result = self.calc.calculate("My test", 10, 5, '+')
        self.assertAlmostEqual(result['answer'], 15.0, delta=0.15)

if __name__ == "__main__":
    unittest.main()
```

## Configuration

### Calculator Parameters

```python
calc = DomBrainCalculator(
    pathway_count=100,              # Number of pathways (default: 100)
    consolidation_threshold=0.3     # Min confidence to keep path (default: 0.3)
)
```

**Tuning Guidelines:**
- **More pathways** (200+): More diverse exploration, longer computation
- **Fewer pathways** (50): Faster computation, less diversity
- **Higher threshold** (0.5): Only keep very confident paths, faster convergence
- **Lower threshold** (0.1): Keep more exploratory paths, more collisions

### Pathway Types

You can customize which pathway types to use by modifying the `_generate_pathways` method:

```python
def _generate_pathways(self, a, b, op):
    paths = []
    
    # Core methods (always include)
    paths.extend(self._symbolic_methods(a, b, op))
    paths.extend(self._numerical_methods(a, b, op))
    
    # Optional: Add or remove cross-domain methods
    # paths.extend(self._quantum_methods(a, b, op))
    # paths.extend(self._dna_methods(a, b, op))
    # ... etc
    
    return paths
```

## Troubleshooting

### Discord Bot Not Responding

1. Check token is correct in `.env`
2. Ensure bot has proper permissions on Discord server
3. Verify bot is invited with `applications.commands` scope
4. Check console for error messages

### Calculations Taking Too Long

1. Reduce `pathway_count` (try 50 instead of 100)
2. Increase `consolidation_threshold` (try 0.5)
3. Remove some cross-domain methods

### Low Confidence Scores

This is normal! The cognitive approach generates exploratory paths that have varying confidence. The final answer is still accurate because:
1. High-confidence paths (symbolic, numerical) are weighted heavily
2. Collisions between independent methods validate the answer
3. Exploratory paths are pruned during consolidation

A confidence of 40-60% is typical and indicates healthy diversity of thought.

### No Collisions Detected

Try:
1. Increasing `pathway_count` (more pathways = more chance of collision)
2. Simple operations (+, *) generate more collisions than complex ones
3. Integer operands tend to produce more collisions than decimals

## Advanced Usage

### Custom Pathway Types

Add your own domain-specific pathways:

```python
def _custom_domain_methods(self, a, b, op):
    """My custom domain analogy"""
    paths = []
    
    if op == '+':
        result = a + b
        reasoning = "My custom reasoning"
        confidence = 0.80
        
        paths.append(SolutionPath(
            pathway_type=PathwayType.CUSTOM,  # Add to enum
            result=result,
            confidence=confidence,
            reasoning=reasoning
        ))
    
    return paths
```

### Multi-Step Problems

Chain calculations:

```python
# Calculate (5 + 3) * 2
result1 = calc.calculate("5 + 3", 5, 3, '+')
result2 = calc.calculate(f"({result1['answer']}) * 2", result1['answer'], 2, '*')

print(f"Final answer: {result2['answer']}")
```

### Export Results

Save detailed results to JSON:

```python
import json

result = calc.calculate("Problem", 10, 5, '+')

# Export to JSON
with open('calculation_result.json', 'w') as f:
    json.dump({
        'problem': result['problem'],
        'answer': result['answer'],
        'confidence': result['confidence'],
        'pathways': [
            {
                'type': p.pathway_type.value,
                'result': p.result,
                'confidence': p.confidence,
                'reasoning': p.reasoning
            }
            for p in result['all_paths']
        ],
        'collisions': [
            {
                'insight': c.insight,
                'strength': c.collision_strength,
                'synthesis': c.synthesis_result
            }
            for c in result['collisions']
        ]
    }, f, indent=2)
```

## Architecture Diagram

```
User Input (Discord/API/CLI)
          ↓
    DomBrainCalculator
          ↓
    ┌─────────────────┐
    │ Generate 100    │
    │ Pathways        │
    └─────────────────┘
          ↓
    ┌─────────────────┐
    │ Consolidate     │
    │ (Prune Weak)    │
    └─────────────────┘
          ↓
    ┌─────────────────┐
    │ Detect          │
    │ Collisions      │
    └─────────────────┘
          ↓
    ┌─────────────────┐
    │ Build           │
    │ Consensus       │
    └─────────────────┘
          ↓
    Result + Insights
```

## References

- [DOM_BRAIN_CALCULATOR.md](./DOM_BRAIN_CALCULATOR.md) - Full theory and architecture
- [dom_brain_calculator.py](./dom_brain_calculator.py) - Core implementation
- [dom_brain_discord.py](./dom_brain_discord.py) - Discord integration
- [test_dom_brain_calculator.py](./test_dom_brain_calculator.py) - Test suite

## Support

For issues or questions:
1. Check this integration guide
2. Review the test suite for examples
3. See DOM_BRAIN_CALCULATOR.md for theory
4. Open an issue on GitHub

---

**Remember**: This calculator doesn't just compute—it shows how you think. The 100 pathways, memory consolidation, and collision detection mirror your cognitive architecture. That's what makes it valuable.
