/**
 * Sovereign Antibody System
 * StrategicKhaos Orchestration System (SKOS)
 * 
 * Self-healing, antifragile infrastructure for sovereign computing.
 */

// Core exports
export { AntibodyCoordinator } from './coordinator/antibody-coordinator.js';

// Base antibody class
export { 
  BaseAntibody, 
  type AntibodyConfig, 
  type HealthStatus, 
  type HealingAction, 
  type AntibodyState 
} from './agents/base-antibody.js';

// Layer 1: Hardware Resilience
export { ThermalSentinel } from './agents/thermal-sentinel.js';
export { PowerGuardian } from './agents/power-guardian.js';
export { StorageWatcher } from './agents/storage-watcher.js';

// Layer 2: Network & Communication
export { MeshHealer } from './agents/mesh-healer.js';

// Layer 3: Model & Execution
export { LoopBreaker } from './agents/loop-breaker.js';
export { OutputSanitizer } from './agents/output-sanitizer.js';

// Version info
export const VERSION = '1.0.0';
export const SYSTEM_NAME = 'SKOS Antibody System';
