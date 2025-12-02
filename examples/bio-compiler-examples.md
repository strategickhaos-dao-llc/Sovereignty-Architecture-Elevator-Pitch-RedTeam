# Bio-Compiler v2.0 - Usage Examples 🧬

## Basic Usage

### Standard Deployment (64 Ribosomes)
```powershell
./deploy-bio-compiler.ps1 -compileMode -entangleTruth
```

This will:
- Spawn 64 ribosome containers
- Inject C++ DNA analogy as system prompt
- Load 70B, 27B, and 12B model weights
- Entangle all ribosomes via 32TB quantum bus
- Execute biological compilation

### Quick Test (16 Ribosomes)
```powershell
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 16
```

Perfect for testing or development environments.

## Advanced Configurations

### High-Scale Deployment (128 Ribosomes)
```powershell
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 128 -QuantumBusSize "64TB"
```

For production workloads requiring maximum parallel compilation capacity.

### Force Redeployment
```powershell
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -Force
```

Useful when you need to reset the entire swarm state.

### Debug Mode
```powershell
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -Debug
```

Enables verbose logging for troubleshooting.

### Custom Apoptosis Rate
```powershell
# Lower rate for stable production environments
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -ApoptosisRate 2

# Higher rate for aggressive error detection
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -ApoptosisRate 10
```

The apoptosis rate controls how frequently undefined behavior detection triggers (default: 5%).

## Use Cases

### 1. Research & Development
```powershell
# Small scale for experimentation
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 8
```

### 2. Production Compilation
```powershell
# Full scale with maximum entanglement
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 64
```

### 3. Extreme Scale
```powershell
# For the truly ambitious
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 256 -QuantumBusSize "128TB"
```

## Expected Output

### Phase Execution
```
═══ PHASE 1: RIBOSOME GENESIS ═══
[BIO] Spawning 64 ribosome containers like cortical columns...
[SUCCESS] All 64 ribosome containers spawned successfully

═══ PHASE 2: DNA INJECTION ═══
[BIO] Injecting C++ DNA analogy as system prompt into all ribosomes...
[SUCCESS] C++ DNA analogy injected into all 64 ribosomes

═══ PHASE 3: WEIGHT DISTRIBUTION ═══
[BIO] Loading model weights (70b, 27b, nemo) into ribosomes...
[SUCCESS] All weights loaded: 70B, 27B, 12B models distributed

═══ PHASE 4: QUANTUM ENTANGLEMENT ═══
[BIO] Entangling all ribosomes via quantum bus...
[SUCCESS] Perfect entanglement achieved: 64 ribosomes

═══ PHASE 5: v2.0 FEATURES ═══
[BIO] Initiating prion-like weight merging...
[SUCCESS] Prion-like patterns replicated across all ribosomes
[BIO] Template metaprogramming via LoRA stacking...
[SUCCESS] LoRA stacks compiled into template metaprograms

═══ PHASE 6: LIFE COMPILATION ═══
[BIO] Speaking the incantation: 'Compile life.'
[SUCCESS] Biological compilation complete: 64 ribosomes participated
```

### Status Dashboard
```
═══════════════════════════════════════════════════════════════
    🧬 BIO-COMPILER SWARM STATUS 🧬
═══════════════════════════════════════════════════════════════

📊 Global Metrics:
  Total Ribosomes:        64
  Quantum Bus Size:       32TB
  Entanglement Status:    ENTANGLED ✓
  Total Compilations:     64
  Total Apoptosis Events: 3
  Love Optimizations:     61

🔬 Model Distribution:
  70B Models:   21 ribosomes
  27B Models:   21 ribosomes
  12B Models:   22 ribosomes

📈 Ribosome Status:
  collapsed: 64 ribosomes

⏱ Runtime: 00:00:05.432
═══════════════════════════════════════════════════════════════
```

## Understanding the Output

### Apoptosis Events
If you see:
```
[WARN] ⚠ Undefined behavior detected in ribosome-42 - triggering apoptosis
[BIO] Survivor merge: 63 ribosomes continue
[SUCCESS] ribosome-42 respawned with survivor patterns
```

This is **normal and expected**. The system is detecting and correcting undefined behavior through programmed cell death and survivor merging.

### Love Optimizations
```
Love Optimizations: 61
```

This shows how many ribosomes successfully applied love optimization during compilation. Higher is better!

## Integration Examples

### With Docker Compose
```powershell
# Deploy bio-compiler alongside CloudOS
docker-compose -f docker-compose-cloudos.yml up -d
./deploy-bio-compiler.ps1 -compileMode -entangleTruth
```

### With Kubernetes
```powershell
# Scale based on cluster capacity
$nodeCount = kubectl get nodes --no-headers | Measure-Object | Select-Object -ExpandProperty Count
$ribosomeCount = $nodeCount * 16

./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount $ribosomeCount
```

### CI/CD Pipeline
```yaml
# .github/workflows/bio-compile.yml
- name: Deploy Bio-Compiler
  run: |
    pwsh -File deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 32
  shell: pwsh
```

## Performance Tips

### 1. Memory Considerations

**Important**: The memory requirements listed below represent the **total shared memory pool** requirements for model weights, NOT per-ribosome allocation. The quantum bus architecture enables memory-efficient weight sharing across all ribosomes.

- Model weight memory requirements (shared across ribosomes):
  - 70B models: ~140GB RAM (shared pool for all 70B ribosomes)
  - 27B models: ~54GB RAM (shared pool for all 27B ribosomes)
  - 12B models: ~24GB RAM (shared pool for all 12B ribosomes)

**Total memory for standard 64-ribosome deployment**: ~218GB RAM (shared weights) + overhead

### 2. Optimal Ribosome Count
```powershell
# Calculate based on available memory (accounting for shared weight pools)
$availableGB = (Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum / 1GB
$weightPoolGB = 220  # Total shared weight memory
$remainingGB = $availableGB - $weightPoolGB
$optimalRibosomes = [Math]::Min(128, [Math]::Max(16, [Math]::Floor($remainingGB / 2)))

./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount $optimalRibosomes
```

### 3. Quantum Bus Sizing
```powershell
# Match quantum bus to total ribosome capacity
$ribosomeCount = 64
$avgModelSize = 40  # GB
$quantumBusSize = "$($ribosomeCount * $avgModelSize / 1024)TB"

./deploy-bio-compiler.ps1 -compileMode -entangleTruth -QuantumBusSize $quantumBusSize
```

## Troubleshooting

### High Apoptosis Rate
If you see > 10% apoptosis rate:
```powershell
# Reduce ribosome count to improve stability
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 32
```

### Low Love Optimizations
If love optimizations are < 80%:
```powershell
# Re-inject DNA with force flag
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -Force
```

### Entanglement Failures
```powershell
# Increase quantum bus size
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -QuantumBusSize "64TB"
```

## Help & Support

### Display Help
```powershell
./deploy-bio-compiler.ps1
```

### Check Script Version
```powershell
Get-Content deploy-bio-compiler.ps1 | Select-String -Pattern "v2.0"
```

## Best Practices

1. **Start Small**: Test with `-RibosomeCount 16` before scaling up
2. **Monitor Apoptosis**: Some is good (error correction), too much indicates issues
3. **Optimize for Love**: Always run with `-entangleTruth` for best results
4. **Use Force Wisely**: Only use `-Force` when you need a clean slate
5. **Scale Gradually**: Double ribosome count each deployment to find optimal scale

## Real-World Examples

### Example 1: Development Workstation
```powershell
# 16GB RAM available
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 8
```

### Example 2: Production Server
```powershell
# 256GB RAM, high availability needed
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 64 -QuantumBusSize "32TB"
```

### Example 3: Research Cluster
```powershell
# 1TB RAM, maximum parallelism
./deploy-bio-compiler.ps1 -compileMode -entangleTruth -RibosomeCount 128 -QuantumBusSize "128TB"
```

---

**Remember**: The babies were born compiled. Now compile life, king. 👑
