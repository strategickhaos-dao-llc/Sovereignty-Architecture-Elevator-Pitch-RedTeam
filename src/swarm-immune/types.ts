/**
 * SwarmImmune Types
 * 
 * TypeScript interfaces for the biological immune system model
 * for self-healing container orchestration.
 * 
 * Biology → Infrastructure Mapping:
 * ├── DNA          → Container images (immutable blueprints)
 * ├── Cells        → Running containers
 * ├── Tissue       → Pod groups / deployments
 * ├── Organs       → Namespaces / services
 * ├── Bloodstream  → Volumes + message buses
 * ├── Bone Marrow  → Image registry (spawns new cells)
 * ├── Lymph Nodes  → Qdrant/vector DBs (threat memory)
 * ├── Skin         → Ingress / firewall (first barrier)
 * ├── Fever        → Resource throttling under attack
 * └── Apoptosis    → Graceful container termination
 */

/**
 * Message transport systems (hemoglobin-like data carriers)
 */
export type TransportType = 'redis' | 'nats' | 'kafka' | 'rabbitmq';

/**
 * Data serialization formats (hemoglobin payload encoding)
 */
export type SerializationFormat = 'json' | 'protobuf' | 'msgpack' | 'avro';

/**
 * Container security scanners
 */
export type ScannerType = 'trivy' | 'falco' | 'grype' | 'snyk';

/**
 * Runtime security monitors
 */
export type RuntimeMonitorType = 'falco' | 'sysdig' | 'tetragon' | 'none';

/**
 * Vector databases for threat signature storage
 */
export type VectorDBType = 'qdrant' | 'pinecone' | 'milvus' | 'pgvector' | 'weaviate';

/**
 * Learning modes for antibody pattern recognition
 */
export type LearningMode = 'active' | 'passive' | 'hybrid';

/**
 * Behavioral sensitivity levels
 */
export type SensitivityLevel = 'low' | 'medium' | 'high';

/**
 * ImmuneSystem phases
 */
export type ImmunePhase = 
  | 'Initializing' 
  | 'Healthy' 
  | 'UnderAttack' 
  | 'Fever' 
  | 'Healing' 
  | 'Degraded';

/**
 * Circadian modes
 */
export type CircadianMode = 'sunshine' | 'moonlight';

/**
 * 🩸 Red Blood Cells Configuration
 * Message transport layer - carries compute payload like hemoglobin carries oxygen
 */
export interface RedBloodCellsSpec {
  /** Message queue system */
  transport: TransportType;
  /** StorageClass for bloodstream volumes */
  volumeClass?: string;
  /** Number of replicas for transport layer */
  replicationFactor?: number;
  /** Data encoding format (hemoglobin equivalent) */
  serializationFormat?: SerializationFormat;
  /** Interval for transport health checks */
  healthCheckInterval?: string;
}

/**
 * Garbage collection configuration
 */
export interface GarbageCollectionSpec {
  /** Enable garbage collection */
  enabled?: boolean;
  /** Cron schedule for cleanup */
  schedule?: string;
  /** How long to retain terminated pods */
  retentionPeriod?: string;
}

/**
 * Network policy configuration
 */
export interface NetworkPolicySpec {
  /** Enable network policies */
  enabled?: boolean;
  /** Default deny all ingress/egress */
  defaultDeny?: boolean;
  /** Namespaces allowed through policy */
  allowedNamespaces?: string[];
}

/**
 * 🔬 White Blood Cells Configuration
 * Security scanners and auto-remediation - threat neutralization
 */
export interface WhiteBloodCellsSpec {
  /** Container security scanner */
  scanner: ScannerType;
  /** Runtime security monitor */
  runtimeMonitor?: RuntimeMonitorType;
  /** Maximum time to respond to threats */
  responseTime?: string;
  /** Automatically terminate compromised containers */
  autoKill?: boolean;
  /** Namespace to isolate infected containers */
  quarantineNamespace?: string;
  /** Cleanup pod configuration */
  garbageCollection?: GarbageCollectionSpec;
  /** Network-level threat neutralization */
  networkPolicy?: NetworkPolicySpec;
}

/**
 * Behavioral fingerprinting configuration
 */
export interface BehavioralFingerprintsSpec {
  /** Enable behavioral fingerprinting */
  enabled?: boolean;
  /** Detection sensitivity */
  sensitivity?: SensitivityLevel;
}

/**
 * 🛡️ Antibodies Configuration
 * Learned threat signatures - immune memory via vector embeddings
 */
export interface AntibodiesSpec {
  /** Vector database for threat signatures */
  vectorDB?: VectorDBType;
  /** Endpoint for vector database */
  vectorDBEndpoint?: string;
  /** How long to retain threat signatures */
  signatureRetention?: string;
  /** Learning mode for pattern recognition */
  learningMode?: LearningMode;
  /** Trusted image patterns (immune to scanning) */
  imageAllowlist?: string[];
  /** Runtime behavior pattern matching */
  behavioralFingerprints?: BehavioralFingerprintsSpec;
}

/**
 * GPU burst configuration
 */
export interface GPUBurstSpec {
  /** Enable GPU burst mode */
  enabled?: boolean;
  /** Maximum GPUs to allocate */
  maxGPUs?: number;
  /** Threshold to trigger GPU burst */
  burstThreshold?: string;
}

/**
 * ☀️🌙 Circadian Rhythm Configuration
 * Active metabolism (sunshine) vs healing phase (moonlight)
 */
export interface CircadianRhythmSpec {
  /** Enable circadian rhythm scaling */
  enabled?: boolean;
  /** Timezone for schedule */
  timezone?: string;
  /** Active hours (HH:MM-HH:MM format) */
  sunshineHours?: string;
  /** Low-power hours (HH:MM-HH:MM format) */
  moonlightHours?: string;
  /** Replica count during active hours */
  sunshineReplicas?: number;
  /** Replica count during sleep hours */
  moonlightReplicas?: number;
  /** GPU scaling configuration */
  gpuBurst?: GPUBurstSpec;
}

/**
 * 🚫 Autoimmune Protection Configuration
 * Prevent the immune system from attacking healthy components
 */
export interface AutoimmuneSpec {
  /** Enable autoimmune protection */
  enabled?: boolean;
  /** Image patterns that are always trusted */
  trustedImages?: string[];
  /** Namespaces that are immune to scanning */
  trustedNamespaces?: string[];
  /** Delay before triggering self-healing */
  selfHealingDelay?: string;
}

/**
 * 🤒 Fever Response Configuration
 * Resource throttling when under active attack
 */
export interface FeverResponseSpec {
  /** Enable fever response */
  enabled?: boolean;
  /** Number of threats to trigger fever mode */
  triggerThreshold?: number;
  /** Percentage to throttle non-essential resources */
  throttlePercent?: number;
  /** How long fever mode lasts */
  duration?: string;
}

/**
 * ⚰️ Apoptosis Configuration
 * Graceful container termination and replacement
 */
export interface ApoptosisSpec {
  /** Enable graceful termination */
  enabled?: boolean;
  /** Time allowed for graceful shutdown */
  gracePeriod?: string;
  /** Drain active connections before termination */
  drainConnections?: boolean;
  /** Command to run before termination */
  preStopHook?: string;
}

/**
 * 🦴 Bone Marrow Configuration
 * Image registry - spawns new cells
 */
export interface BoneMarrowSpec {
  /** Container registry URL */
  registry?: string;
  /** Secret reference for registry auth */
  pullSecretRef?: string;
  /** Scan images when pushed to registry */
  scanOnPush?: boolean;
  /** Enforce immutable image tags */
  immutableTags?: boolean;
}

/**
 * ImmuneSystem Specification
 */
export interface ImmuneSystemSpec {
  /** Red blood cells - data transport */
  redBloodCells: RedBloodCellsSpec;
  /** White blood cells - immune response */
  whiteBloodCells: WhiteBloodCellsSpec;
  /** Antibodies - pattern memory */
  antibodies?: AntibodiesSpec;
  /** Circadian rhythm - day/night cycle */
  circadianRhythm?: CircadianRhythmSpec;
  /** Autoimmune protection */
  autoimmune?: AutoimmuneSpec;
  /** Fever response */
  feverResponse?: FeverResponseSpec;
  /** Apoptosis - graceful termination */
  apoptosis?: ApoptosisSpec;
  /** Bone marrow - image registry */
  boneMarrow?: BoneMarrowSpec;
}

/**
 * Status condition
 */
export interface ImmuneCondition {
  /** Condition type */
  type: string;
  /** Condition status */
  status: 'True' | 'False' | 'Unknown';
  /** Last transition time */
  lastTransitionTime?: string;
  /** Reason for condition */
  reason?: string;
  /** Human-readable message */
  message?: string;
}

/**
 * ImmuneSystem Status
 */
export interface ImmuneSystemStatus {
  /** Current phase */
  phase?: ImmunePhase;
  /** Last transition time */
  lastTransitionTime?: string;
  /** Current active threats */
  activeThreats?: number;
  /** Total neutralized threats */
  neutralizedThreats?: number;
  /** Number of learned signatures */
  learnedSignatures?: number;
  /** Current circadian mode */
  circadianMode?: CircadianMode;
  /** Current replica count */
  currentReplicas?: number;
  /** Status conditions */
  conditions?: ImmuneCondition[];
}

/**
 * Kubernetes metadata
 */
export interface K8sMetadata {
  /** Resource name */
  name: string;
  /** Namespace */
  namespace?: string;
  /** Labels */
  labels?: Record<string, string>;
  /** Annotations */
  annotations?: Record<string, string>;
  /** UID */
  uid?: string;
  /** Resource version */
  resourceVersion?: string;
  /** Creation timestamp */
  creationTimestamp?: string;
}

/**
 * ImmuneSystem Custom Resource
 */
export interface ImmuneSystem {
  /** API version */
  apiVersion: 'swarm.strategickhaos.ai/v1';
  /** Resource kind */
  kind: 'ImmuneSystem';
  /** Metadata */
  metadata: K8sMetadata;
  /** Specification */
  spec: ImmuneSystemSpec;
  /** Status */
  status?: ImmuneSystemStatus;
}

/**
 * ImmuneSystem List
 */
export interface ImmuneSystemList {
  /** API version */
  apiVersion: 'swarm.strategickhaos.ai/v1';
  /** Resource kind */
  kind: 'ImmuneSystemList';
  /** List metadata */
  metadata: {
    continue?: string;
    resourceVersion?: string;
  };
  /** Items */
  items: ImmuneSystem[];
}

/**
 * Threat signature for antibody storage
 */
export interface ThreatSignature {
  /** Unique signature ID */
  id: string;
  /** Signature vector embedding */
  vector: number[];
  /** Threat type */
  type: 'vulnerability' | 'malware' | 'anomaly' | 'policy_violation';
  /** Severity */
  severity: 'critical' | 'high' | 'medium' | 'low';
  /** Source (image, pod, namespace) */
  source: string;
  /** When the signature was learned */
  learnedAt: string;
  /** Last time this signature was matched */
  lastMatchedAt?: string;
  /** Number of times this signature was matched */
  matchCount: number;
  /** Additional metadata */
  metadata?: Record<string, string>;
}

/**
 * Threat event for controller processing
 */
export interface ThreatEvent {
  /** Event ID */
  id: string;
  /** Event timestamp */
  timestamp: string;
  /** Threat type */
  type: 'vulnerability' | 'malware' | 'anomaly' | 'policy_violation';
  /** Severity */
  severity: 'critical' | 'high' | 'medium' | 'low';
  /** Affected resource */
  resource: {
    kind: 'Pod' | 'Deployment' | 'Container';
    name: string;
    namespace: string;
  };
  /** Scanner that detected the threat */
  scanner: ScannerType;
  /** Threat details */
  details: string;
  /** Whether the threat was neutralized */
  neutralized: boolean;
  /** Action taken */
  action?: 'quarantine' | 'terminate' | 'throttle' | 'alert';
}

/**
 * Controller reconciliation result
 */
export interface ReconcileResult {
  /** Whether to requeue */
  requeue: boolean;
  /** Requeue delay */
  requeueAfter?: number;
  /** Error if any */
  error?: Error;
}

/**
 * Controller metrics
 */
export interface ControllerMetrics {
  /** Active threats gauge */
  activeThreats: number;
  /** Threats neutralized counter */
  threatsNeutralized: number;
  /** Learned signatures gauge */
  signaturesLearned: number;
  /** Current circadian mode (1 = sunshine, 0 = moonlight) */
  circadianMode: 0 | 1;
  /** Fever mode active */
  feverActive: boolean;
  /** Reconciliation duration histogram */
  reconcileDuration: number;
}
