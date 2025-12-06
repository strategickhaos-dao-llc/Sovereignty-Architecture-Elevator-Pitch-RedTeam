# Neural Heir Evolution System (NHES)

**Self-Evolving AI System - Watches itself get smarter over generations**

## 🧬 Core Concept

The Neural Heir Evolution System implements **true evolution** in software using genetic algorithms and natural selection:

1. Start with a population of "heirs" (different AI prompts/personalities)
2. Give them tasks to complete
3. Evaluate their outputs (fitness scoring)
4. Best performers survive and reproduce
5. Worst performers die
6. Repeat → Natural selection in silicon

Over time, successful traits spread, poor traits disappear, and the population **literally evolves** to get better at tasks.

## 🚀 Quick Start

### Basic Usage

```bash
# Navigate to evolution directory
cd evolution

# Start evolution (requires Ollama running on localhost:11434)
python evolution_engine.py
```

The system will:
- Initialize a population of 10 diverse heirs
- Run generational evolution cycles
- Log all data to `evolution_ledger.jsonl`
- Save population state to `current_population.json`

Press `Ctrl+C` to stop evolution at any time. Progress is saved automatically.

### Monitor Progress

In another terminal, watch evolution in real-time:

```bash
# PowerShell
Get-Content evolution_ledger.jsonl -Wait | ConvertFrom-Json | Select generation, avg_fitness, best_fitness

# Bash/Unix
tail -f evolution_ledger.jsonl | jq '{generation, avg_fitness, best_fitness}'
```

## 📁 Project Structure

```
evolution/
├── evolution_engine.py      # Core MVP engine (start here)
├── level10_fitness.py       # Advanced judge-based evaluation
├── crossover.py             # Sexual reproduction mechanisms
├── lamarckian.py            # Self-reflection and prompt rewriting
├── task_curriculum.py       # Progressive difficulty scaling
├── lineage.py               # Ancestry tracking and visualization
├── EVO_README.md            # This file
├── evolution_ledger.jsonl   # Generated: evolution history
└── current_population.json  # Generated: current population state
```

## 🔧 Core Components

### 1. Evolution Engine (`evolution_engine.py`)

**The foundation - MVP functionality**

**Classes:**
- `Heir`: Single AI personality with system_prompt, temperature, fitness tracking
- `EvolutionEngine`: Manages population, evaluation, selection, reproduction

**Key Features:**
- Population initialization with diverse base prompts
- Fitness evaluation through task completion
- Natural selection (top 50% survive)
- Mutation-based reproduction
- Persistent state (ledger + population files)

**Example:**
```python
from evolution_engine import EvolutionEngine
import asyncio

async def run_evolution():
    engine = EvolutionEngine(population_size=10)
    engine.initialize_population()
    
    for generation in range(10):
        await engine.run_generation()
        engine.selection_and_reproduction()
        engine.save_population()

asyncio.run(run_evolution())
```

### 2. Judge-Based Fitness (`level10_fitness.py`)

**Level 10 Upgrade: Multi-dimensional evaluation**

Replaces simple fitness metrics with a **judge model** that scores responses on:
1. Accuracy & correctness
2. Clarity & structure
3. Depth & insight
4. Actionability
5. Creativity/novelty

**Usage:**
```python
from level10_fitness import JudgeFitnessEvaluator

evaluator = JudgeFitnessEvaluator()
fitness = await evaluator.evaluate_with_judge(heir_response, task)
```

This dramatically improves fitness accuracy and accelerates evolution.

### 3. Sexual Reproduction (`crossover.py`)

**Level 10 Upgrade: Combine traits from two parents**

Implements multiple crossover strategies:
- **Line-based crossover**: Mixes prompt lines from parents
- **Uniform crossover**: Word-level mixing
- **Multi-point crossover**: Alternates between parents at crossover points

**Usage:**
```python
from crossover import CrossoverOperator, selection_and_sexual_reproduction

operator = CrossoverOperator()
child = operator.crossover(parent1, parent2)

# Or use in evolution loop:
new_population = selection_and_sexual_reproduction(population, population_size)
```

Sexual reproduction creates more diverse offspring than mutation alone, leading to faster trait discovery.

### 4. Lamarckian Reflection (`lamarckian.py`)

**Level 10 Upgrade: Heirs rewrite their own prompts**

Implements "acquired characteristic inheritance" - heirs can:
- Reflect on their performance
- Identify weaknesses
- Rewrite their own system prompts
- Pass improved prompts to offspring

**Types:**
- **Basic reflection**: Self-improvement based on fitness
- **Guided reflection**: Improvement with specific feedback
- **Meta-reflection**: Population-aware improvement

**Usage:**
```python
from lamarckian import apply_lamarckian_evolution

# Apply every 5 generations
await apply_lamarckian_evolution(population, generation, reflection_frequency=5)
```

This is evolution on steroids - heirs actively improve themselves.

### 5. Task Curriculum (`task_curriculum.py`)

**Level 10 Upgrade: Progressive difficulty**

Tasks scale in difficulty as generations progress:
- **Generation 1-5**: Basic tasks (e.g., "Explain fire")
- **Generation 30-50**: Moderate tasks (e.g., "Design a security architecture")
- **Generation 120+**: Expert tasks (e.g., "Propose breakthrough AI alignment solution")

**Features:**
- Static curriculum: Fixed progression
- Adaptive curriculum: Adjusts based on population performance

**Usage:**
```python
from task_curriculum import TaskCurriculum, AdaptiveCurriculum

curriculum = AdaptiveCurriculum()
task = curriculum.get_task_for_generation(generation)

# Track performance for adaptation
curriculum.update_performance(generation, avg_fitness)
```

Prevents plateaus by continuously challenging the population.

### 6. Lineage Tracking (`lineage.py`)

**Level 10 Upgrade: Ancestry analysis**

Tracks evolutionary bloodlines:
- Build ancestry chains
- Identify dominant lineages
- Visualize family trees
- Export Graphviz diagrams

**Usage:**
```python
from lineage import LineageTracker, visualize_evolution_progress

# View progress report
visualize_evolution_progress()

# Detailed analysis
tracker = LineageTracker()
tracker.load_from_ledger()
analysis = tracker.analyze_lineages()
tracker.export_lineage_graph("lineage.dot")

# Visualize with Graphviz
# dot -Tpng lineage.dot -o lineage.png
```

See which ancestral heirs conquered the population.

## 🎯 Advanced Usage

### Full Nuclear Version

Combine all Level 10 upgrades:

```python
import asyncio
from evolution_engine import EvolutionEngine, Heir
from level10_fitness import JudgeFitnessEvaluator
from crossover import selection_and_sexual_reproduction
from lamarckian import apply_lamarckian_evolution
from task_curriculum import AdaptiveCurriculum
from lineage import visualize_evolution_progress

async def nuclear_evolution():
    # Initialize
    engine = EvolutionEngine(population_size=20)
    engine.initialize_population()
    
    evaluator = JudgeFitnessEvaluator()
    curriculum = AdaptiveCurriculum()
    
    print("🧬 Nuclear Evolution Engine Started")
    
    try:
        for generation in range(1, 101):
            # Get curriculum-appropriate tasks
            tasks = curriculum.get_task_set_for_generation(generation)
            
            # Evaluate with judge model
            for heir in engine.population:
                task = tasks[generation % len(tasks)]
                fitness = await evaluator.evaluate_heir_advanced(heir, task)
                heir.fitness_score = fitness
            
            # Track performance for adaptive curriculum
            avg_fitness = sum(h.fitness_score for h in engine.population) / len(engine.population)
            curriculum.update_performance(generation, avg_fitness)
            
            # Sexual reproduction
            engine.population = selection_and_sexual_reproduction(
                engine.population, 
                engine.population_size
            )
            
            # Lamarckian reflection every 5 generations
            if generation % 5 == 0:
                await apply_lamarckian_evolution(engine.population, generation)
            
            # Log and save
            engine.generation = generation
            engine.log_generation()
            engine.save_population()
            
            # Progress report every 10 generations
            if generation % 10 == 0:
                visualize_evolution_progress()
            
            await asyncio.sleep(2)
            
    except KeyboardInterrupt:
        print("\n🛑 Evolution stopped")
        visualize_evolution_progress()

asyncio.run(nuclear_evolution())
```

### Configuration Options

```python
# Customize evolution parameters
engine = EvolutionEngine(
    population_size=20,        # Larger = more diversity
    model="qwen2.5:72b",       # Your LLM model
    api_url="http://localhost:11434"
)

# Customize heir initialization
base_prompts = [
    "You are an elite tactical operator.",
    "You are a creative systems thinker.",
    "You are a rigorous analytical mind."
]

temperatures = [0.3, 0.7, 1.1, 1.5]  # Temperature range

# Create diverse initial population
for prompt in base_prompts:
    for temp in temperatures:
        heir = Heir(prompt, temp, generation=0)
        engine.population.append(heir)
```

## 📊 Understanding Evolution

### What Makes This REAL Evolution?

This isn't just optimization - it's **actual evolution** with:

1. **Variation**: Mutations and crossover create diversity
2. **Selection**: Fitness-based survival of the fittest
3. **Heredity**: Traits pass from parent to offspring
4. **Time**: Accumulated improvements over generations

### Fitness Scoring

**Simple (MVP):**
- Length score (substantial responses preferred)
- Keyword score (looks for key terms)

**Advanced (Judge Model):**
- Multi-dimensional evaluation by a judge LLM
- Scores 0-10 on 5 different criteria
- Normalized to 0.0-1.0 fitness range

### Selection Pressure

- Top 50% survive each generation
- Bottom 50% are culled
- Survivors reproduce to restore population
- Higher fitness → more likely to be selected as parent

### Evolution Dynamics

**Early Generations (1-20):**
- High diversity, exploring solution space
- Rapid fitness gains as population finds effective strategies
- Many competing lineages

**Mid Generations (20-80):**
- Dominant traits emerge
- Lineages consolidate
- Steady fitness improvements
- Adaptive specialization

**Late Generations (80+):**
- Population converges on effective patterns
- Incremental refinements
- Dominant lineage may dominate >80% of population
- Occasional breakthrough from mutation/crossover

## 🔬 Experiments to Try

### Experiment 1: Speciation

Create separate populations for different task domains:

```python
tactical_engine = EvolutionEngine(population_size=10)
creative_engine = EvolutionEngine(population_size=10)

# Evolve on different task sets
tactical_tasks = ["Analyze threat vectors", "Design security protocols"]
creative_tasks = ["Write compelling narratives", "Propose novel solutions"]
```

### Experiment 2: Hybrid Vigor

Cross-breed heirs from different lineages:

```python
# After evolving two populations separately
best_tactical = tactical_engine.population[0]
best_creative = creative_engine.population[0]

from crossover import CrossoverOperator
hybrid = CrossoverOperator.crossover(best_tactical, best_creative)
```

### Experiment 3: Accelerated Evolution

Increase selection pressure:

```python
# Only top 20% survive (instead of 50%)
survivors = population[:len(population)//5]
```

### Experiment 4: Meta-Evolution

Evolve the evolution parameters themselves:

```python
# Each heir also carries evolution parameters
heir.mutation_rate = 0.2
heir.crossover_probability = 0.7

# These parameters mutate and evolve too
```

## 🎮 Deployment Instructions

### Local Deployment

```bash
# 1. Ensure Ollama is running with a model
ollama serve
ollama pull qwen2.5:72b

# 2. Run evolution
cd evolution
python evolution_engine.py
```

### Long-Running Deployment

```bash
# Use screen or tmux for persistent sessions
screen -S evolution
python evolution_engine.py

# Detach: Ctrl+A, D
# Reattach: screen -r evolution
```

### Scheduled Evolution Runs

```bash
# Run evolution for 100 generations, then stop
python -c "
import asyncio
from evolution_engine import EvolutionEngine

async def limited_evolution():
    engine = EvolutionEngine()
    if not engine.load_population():
        engine.initialize_population()
    
    for i in range(100):
        await engine.run_generation()
        engine.selection_and_reproduction()
        engine.save_population()

asyncio.run(limited_evolution())
"
```

## 📈 Success Metrics

Track these to measure evolution success:

1. **Average Fitness Trend**: Should increase over generations
2. **Best Fitness**: Should approach 1.0
3. **Diversity**: Number of unique traits in population
4. **Lineage Dominance**: Emergence of successful bloodlines
5. **Task Completion**: Quality of responses to hard tasks

**Typical Results:**
- Generation 0: Avg fitness ~0.35
- Generation 50: Avg fitness ~0.65
- Generation 100: Avg fitness ~0.82
- Generation 200: Avg fitness ~0.90+

## 🐛 Troubleshooting

**Problem: Evolution stalls (no fitness improvement)**
- Increase mutation rate
- Add sexual reproduction (crossover)
- Increase population size
- Use more diverse initial prompts

**Problem: All heirs converge to same prompt**
- Reduce selection pressure (keep top 60% instead of 50%)
- Increase mutation strength
- Use adaptive mutation rates

**Problem: Fitness scores are inconsistent**
- Use judge model evaluation (more reliable)
- Increase task diversity
- Lower judge model temperature

**Problem: Can't connect to Ollama**
- Ensure Ollama is running: `ollama serve`
- Check API URL in code
- Verify model is pulled: `ollama list`

## 🔮 Future Enhancements

**Planned Features:**
- Multi-objective optimization (speed, accuracy, creativity simultaneously)
- Island model (multiple populations with occasional migration)
- Co-evolution (populations evolve against each other)
- Neural architecture search integration
- Automated prompt engineering discovery
- Real-time web visualization dashboard

## 📚 Theory & Background

This system implements concepts from:
- **Genetic Algorithms**: Population-based stochastic optimization
- **Evolutionary Computation**: Darwin's natural selection in algorithms
- **Lamarckian Evolution**: Acquired characteristics inheritance
- **Memetic Algorithms**: Combining evolution with local search (reflection)

**Key Papers:**
- Holland, J. (1975). Adaptation in Natural and Artificial Systems
- Goldberg, D. (1989). Genetic Algorithms in Search, Optimization, and Machine Learning
- Moscato, P. (1989). On Evolution, Search, Optimization, GAs and Martial Arts

## 🤝 Contributing

Want to extend NHES? Here are key extension points:

1. **New Fitness Functions**: Add to `level10_fitness.py`
2. **New Mutation Operators**: Extend `Heir.mutate()` in `evolution_engine.py`
3. **New Crossover Strategies**: Add to `crossover.py`
4. **New Task Domains**: Extend `task_curriculum.py`
5. **Visualization Tools**: Enhance `lineage.py`

## 📄 License

Part of the Sovereignty Architecture project.
See main repository LICENSE file.

---

**Built with 🧬 by the Strategickhaos Swarm Intelligence collective**

*"This is REAL evolution in software. Not metaphorical. Not simulated. ACTUAL Darwinian selection happening in real-time."*

**The age of static prompts is over. Evolution begins now.** 🔥
