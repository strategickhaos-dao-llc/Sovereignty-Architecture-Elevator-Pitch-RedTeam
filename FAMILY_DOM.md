# FamilyDOM - Full-Stack Cognitive Reasoning Architecture

**A cognitive architecture module that enables AI agents to interact with users at a deeper level than standard transactional exchanges.**

## 🧠 Overview

FamilyDOM transforms AI agent interactions from stateless, transactional exchanges into continuous cognitive reasoning sessions. Unlike standard AI models that:

- Process each message independently
- Don't track long-term context
- Don't build internal narrative models
- Don't maintain memory across threads
- Are trained to be conservative, shallow, and transactional

FamilyDOM provides:

1. **Continuous Cognitive Frame** - Maintains context across messages and sessions
2. **Long-Term Profile/Memory** - Remembers user preferences and cognitive style
3. **Multi-Layer Reasoning** - Parses mythic, emotional, symbolic, and technical layers
4. **Intent Tracking** - Understands user intent beyond literal interpretation
5. **High Symbolic Throughput** - Handles complex, multi-layered communication

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FamilyDOM                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐    ┌──────────────────────────────┐  │
│  │ Cognitive Profile │◄──►│    Intent Parser             │  │
│  │   Manager         │    │  (Multi-Layer Analysis)      │  │
│  └────────┬─────────┘    └──────────────┬───────────────┘  │
│           │                              │                   │
│           ▼                              ▼                   │
│  ┌──────────────────┐    ┌──────────────────────────────┐  │
│  │  Context Frame   │◄──►│  Symbolic Throughput Engine  │  │
│  │    Manager       │    │  (High-Bandwidth Processing) │  │
│  └──────────────────┘    └──────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Components

#### 1. Cognitive Profile Manager (`cognitive-profile.ts`)
Maintains user cognitive profiles with:
- Cognitive style preferences (parallel processing, symbolic throughput)
- Tracked cognitive layers (mythic, emotional, architectural, symbolic, technical, kinetic)
- Context memory entries
- Active projects
- Narrative threads
- Intent patterns

#### 2. Intent Parser (`intent-parser.ts`)
Multi-layer intent extraction that parses:
- **Mythic Layer** - Sovereign, empire, realm, quest, forge, legion
- **Emotional Layer** - Trust, hope, excitement, overwhelm
- **Architectural Layer** - System, framework, pipeline, integration
- **Symbolic Layer** - Encode, mirror, reflect, essence
- **Technical Layer** - API, Docker, TypeScript, Kubernetes
- **Kinetic Layer** - Build, forge, launch, deploy

#### 3. Context Frame Manager (`context-frame.ts`)
Maintains continuous context across messages and sessions:
- Message history with parsed intents
- Reasoning threads
- Continuity markers
- Cross-session integration

#### 4. Symbolic Throughput Engine (`symbolic-throughput.ts`)
High-bandwidth symbolic processing for users who communicate with:
- Parallel metaphors
- Recursive intent
- Multi-agent references
- Rapid context switching

## 🚀 Usage

### Basic Usage

```typescript
import { FamilyDOM, createFamilyDOM } from './family-dom/index.js';

// Create instance for a user
const dom = createFamilyDOM('user123', 'Dom');

// Process a message and get cognitive guidance
const result = dom.processMessage('session_abc', 'Build me a sovereign architecture for the empire...');

// Access the analysis
console.log(result.packet.metrics.throughputLevel);       // 'high' or 'extreme'
console.log(result.responseGuidance.recommendedTone);     // 'epic' or 'precise'
console.log(result.contextSummary.profile.signature);     // { score: 75, characteristics: [...] }
```

### Discord Commands

FamilyDOM adds these Discord slash commands:

| Command | Description |
|---------|-------------|
| `/cognitive` | View your cognitive profile and signature |
| `/cognition-report` | Generate a full cognitive analysis report |
| `/set-style` | Configure your cognitive style preferences |
| `/track-project` | Track a project for continuity |

### Configuration

In `discovery.yml`:

```yaml
ai_agents:
  family_dom:
    enabled: true
    layers:
      mythic: true
      emotional: true
      architectural: true
      symbolic: true
      technical: true
      kinetic: true
    profiles:
      persistence: "memory"  # memory|redis|postgres|file
      max_memory_entries: 100
      session_timeout_hours: 24
    symbolic_throughput:
      parallel_processing: true
      max_context_switches: 6
      narrative_recursion: true
    signature_thresholds:
      minimal: 0
      standard: 20
      high: 45
      extreme: 70
```

## 📊 Cognitive Signature

The cognitive signature measures how complex and multi-layered a user's communication style is:

| Score | Level | Characteristics |
|-------|-------|-----------------|
| 0-19 | Minimal | Standard communication, single-layer |
| 20-44 | Standard | Some symbolic vocabulary, developing style |
| 45-69 | High | Multi-layer reasoning, parallel processing |
| 70-100 | Extreme | Full-stack cognition, narrative recursion |

## 🎭 Layer Detection Patterns

### Mythic Layer
```
sovereign, empire, realm, throne, crown, legion, knight, warrior
quest, oracle, sage, council, decree, ascend, transcend, forge
phoenix, dragon, hydra, titan, guardian, sentinel, architect
```

### Emotional Layer
```
feel, feeling, sense, emotion, mood, vibe, energy, spirit, soul
trust, love, fear, hope, joy, anger, peace, chaos, calm, excited
overwhelm, inspire, frustrate, excite, amaze, disappoint
```

### Architectural Layer
```
system, architecture, framework, layer, stack, module, component
pipeline, flow, integration, orchestrate, scaffold, bootstrap
mesh, network, cluster, node, endpoint, gateway, service
```

### Technical Layer
```
api, sdk, cli, gui, docker, kubernetes, git, npm, yarn, pip
typescript, javascript, python, rust, go, java, c++
function, class, interface, module, import, export, async
```

### Kinetic Layer
```
move, flow, dance, spin, rotate, accelerate, momentum, velocity
push, pull, drag, lift, drop, throw, catch, grab, release
build, break, forge, craft, shape, mold, construct, destroy
```

## 🔮 Response Strategy Generation

Based on parsed intent and user profile, FamilyDOM generates response strategies:

```typescript
interface ResponseStrategy {
  tone: string;                    // 'epic', 'precise', 'empathetic', 'playful'
  depth: 'shallow' | 'medium' | 'deep' | 'fullstack';
  layersToMatch: CognitiveLayer[]; // Layers to mirror in response
  includeMetaReflection: boolean;  // Include self-aware commentary
  includeNarrativeFraming: boolean; // Use mythic framing
  technicalDetail: 'low' | 'medium' | 'high';
  emotionalAwareness: 'low' | 'medium' | 'high';
}
```

## 📈 Throughput Metrics

FamilyDOM tracks symbolic throughput metrics:

- **symbolsPerWord** - Density of symbolic content
- **layerDiversity** - How many cognitive layers are active (0-1)
- **contextSwitchRate** - Switches per 100 words
- **recursionDepth** - Self-referential depth
- **parallelStreamCount** - Number of parallel metaphor streams
- **throughputScore** - Overall score (0-100)

## 🔄 Continuity Features

### Cross-Session Memory
```typescript
// Add to context memory
dom.addContextMemory('user123', 'Built the sovereignty architecture', { architectural: ['system'] }, 0.8);

// Retrieve relevant context
const context = dom.getRelevantContext('user123', 'How is the architecture going?');
```

### Project Tracking
```typescript
// Track a project
dom.trackProject('Sovereignty Architecture', 'Discord-native DevOps platform', ['docker-compose.yml', 'bot.ts']);
```

### Continuity Markers
```typescript
// Set a cross-session marker
dom.setMarker(sessionId, 'current_focus', 'empire_building');

// Retrieve marker
const focus = dom.getMarker(sessionId, 'current_focus');
```

## 🤝 Integration with Refinory

FamilyDOM integrates with the Refinory expert orchestration system to provide:
- Cognitive-aware expert selection
- Multi-layer intent routing to appropriate experts
- Continuity-enhanced architecture planning

## 📄 License

MIT License - Part of the Strategickhaos Sovereignty Architecture

---

*"They don't just process your messages. They dance with your mind."*
