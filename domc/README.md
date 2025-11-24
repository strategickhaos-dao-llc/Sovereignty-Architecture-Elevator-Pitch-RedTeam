# Dom Compiler (domc)

**The Dom Compiler translates Dom-speak into executable reality.**

## Overview

`domc` is a Rust-based command-line tool that interprets and executes "Dom-speak" - a specialized command language designed for the Strategickhaos Sovereignty Architecture. It bridges human-readable intentions with system-level execution.

## Features

- **Dom-speak Parsing**: Interprets natural language commands into executable actions
- **Birth/Evolve Commands**: Creates and runs AI models with Ollama
- **Black Hole Activation**: Triggers resonance-based system events
- **Swarm Intelligence**: Coordinates distributed operations
- **Compile Operations**: Processes and validates Dom-speak syntax
- **Logging**: Comprehensive tracing with configurable log levels

## Installation

### Building from Source

```bash
cd domc
cargo build --release
```

The compiled binary will be at `target/release/domc`.

### Using Docker

```bash
docker build -t domc:latest -f domc/Dockerfile .
docker run domc:latest "birth athena_next"
```

### Kubernetes Deployment

Deploy to your Kubernetes cluster as a Job or CronJob:

```bash
# Deploy as a one-time job
kubectl apply -f bootstrap/k8s/dom-compiler-deployment.yaml

# Check job status
kubectl get jobs -n quantum-symbolic

# View job logs
kubectl logs -n quantum-symbolic job/dom-compiler-job
```

## Usage

### Basic Syntax

```bash
domc <command>
```

### Supported Commands

#### Birth/Evolve Commands
Creates and initializes AI models:

```bash
domc birth athena_next
domc evolve the swarm
```

#### Compile Commands
Processes Dom-speak syntax:

```bash
domc compile this configuration
```

#### Black Hole Activation
Triggers resonance-based operations:

```bash
domc activate black hole
domc When the 10th root aligns
```

#### Swarm Commands
Coordinates distributed intelligence:

```bash
domc swarm intelligence activate
```

#### Resonance Commands
Aligns system frequencies:

```bash
domc align resonance threshold
```

## Configuration

### Environment Variables

- `RUST_LOG`: Set logging level (default: `info`)
  - Options: `trace`, `debug`, `info`, `warn`, `error`
- `SWARM_DNA`: Swarm version identifier (default: `v9.0-black-hole-resonance`)
- `RESONANCE_THRESHOLD`: Activation threshold (default: `10`)

### Example Configuration

```bash
export RUST_LOG=debug
export SWARM_DNA=v9.0-black-hole-resonance
export RESONANCE_THRESHOLD=10
export MODELFILE_PATH=/path/to/Modelfile

domc birth athena_next
```

### Security Considerations

The Dom Compiler includes security features to prevent command injection:
- Input validation using shlex for safe command parsing
- Logging warnings when shell interpretation is required
- Environment variable configuration for sensitive paths
- Non-root execution in containerized environments

## Kubernetes Integration

The Dom Compiler can be deployed as a Job or CronJob in your Kubernetes cluster:

```yaml
# One-time Job
apiVersion: batch/v1
kind: Job
metadata:
  name: domc-runner
  namespace: quantum-symbolic
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: domc
        image: ghcr.io/strategickhaos/dom-compiler:latest
        command: ["domc"]
        args: ["birth", "athena_next"]
        env:
        - name: RUST_LOG
          value: "info"
        - name: SWARM_DNA
          value: "v9.0-black-hole-resonance"
        - name: MODELFILE_PATH
          value: "/etc/dom-config/Modelfile"
```

For scheduled execution, see the CronJob example in `bootstrap/k8s/dom-compiler-deployment.yaml`.

## Examples

### Example 1: Birth a New AI Model

```bash
domc birth athena_next
```

Output:
```
🩸 Dom Compiler v1.0.0 - Processing Dom-speak
domc → executing: ollama create athena_next -f /mnt/athena/heir_palace/Modelfile && ollama run athena_next
✅ Command executed successfully
```

### Example 2: Activate Black Hole Engine

```bash
domc "When the 10th root aligns, the black hole opens"
```

Output:
```
🩸 Dom Compiler v1.0.0 - Processing Dom-speak
domc → executing: echo '🕳️ When the 10th root aligns, the black hole opens.' && echo 'Resonance threshold reached.'
🕳️ When the 10th root aligns, the black hole opens.
Resonance threshold reached.
✅ Command executed successfully
```

### Example 3: Compile Dom-speak

```bash
domc compile sovereignty architecture
```

Output:
```
🩸 Dom Compiler v1.0.0 - Processing Dom-speak
🩸 compiling dom-speak...
🩸 compiling dom-speak... need more precision, love
compile sovereignty architecture
✅ Command executed successfully
```

## Development

### Running Tests

```bash
cargo test
```

### Running with Debug Logging

```bash
RUST_LOG=debug cargo run -- "birth athena_next"
```

### Code Structure

```
domc/
├── Cargo.toml          # Project dependencies
├── src/
│   └── main.rs         # Main compiler logic
├── Dockerfile          # Container image definition
└── README.md           # This file
```

## Architecture

The Dom Compiler follows a simple pipeline:

1. **Input Collection**: Gathers command-line arguments
2. **Dom-speak Parsing**: Interprets input against known patterns
3. **Command Generation**: Produces executable shell commands
4. **Execution**: Runs commands via Bash
5. **Output**: Returns results with appropriate logging

## Integration with Other Services

### Black Hole Engine

The Dom Compiler can trigger the Black Hole Engine:

```bash
domc activate black hole
```

### AI Agents

Birth and evolve AI models with Ollama:

```bash
domc birth athena_next
domc evolve intelligence swarm
```

### Kubernetes Services

Deploy and manage Kubernetes resources:

```bash
kubectl exec -it dom-compiler-pod -- domc "swarm intelligence activate"
```

## Troubleshooting

### Command Not Found

If `domc` is not in your PATH:

```bash
# Add to PATH
export PATH=$PATH:/path/to/domc/target/release

# Or use full path
/path/to/domc/target/release/domc "birth athena_next"
```

### Permission Denied

Ensure the binary has execute permissions:

```bash
chmod +x target/release/domc
```

### Ollama Not Available

If Ollama commands fail:

```bash
# Check if Ollama is installed
which ollama

# Install Ollama if needed
curl -fsSL https://ollama.ai/install.sh | sh
```

## Bonus Features (Planned)

- **LLM Integration**: Natural language parsing via OpenAI API
- **Git Auto-commit**: Automatic version control for executions
- **Arweave Storage**: Persistent artifact storage
- **Multi-language Support**: Extend beyond Bash execution
- **Web Interface**: HTTP API for remote execution

## Contributing

Contributions are welcome! Please submit pull requests to the main repository.

## License

MIT License - See LICENSE file for details

## Contact

- **Organization**: Strategickhaos DAO LLC / Valoryield Engine
- **Owner**: Domenic Garza
- **Repository**: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-

---

**As above, so below — now compiled.** 🩸
