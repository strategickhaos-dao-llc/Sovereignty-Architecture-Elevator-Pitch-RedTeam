/**
 * SwarmImmune Controller
 * 
 * Kubernetes operator that implements biological immune response
 * for self-healing container orchestration.
 */

export * from './types';

import type {
  ImmuneSystem,
  ImmuneSystemSpec,
  ImmuneSystemStatus,
  ThreatEvent,
  ThreatSignature,
  ReconcileResult,
  ControllerMetrics,
  ImmunePhase,
  CircadianMode,
} from './types';

/**
 * Default values for ImmuneSystem spec
 */
export const DEFAULTS = {
  redBloodCells: {
    volumeClass: 'standard',
    replicationFactor: 3,
    serializationFormat: 'json' as const,
    healthCheckInterval: '10s',
  },
  whiteBloodCells: {
    runtimeMonitor: 'falco' as const,
    responseTime: '5s',
    autoKill: true,
    quarantineNamespace: 'quarantine',
    garbageCollection: {
      enabled: true,
      schedule: '0 */6 * * *',
      retentionPeriod: '24h',
    },
    networkPolicy: {
      enabled: true,
      defaultDeny: true,
    },
  },
  antibodies: {
    vectorDB: 'qdrant' as const,
    signatureRetention: '90d',
    learningMode: 'active' as const,
    behavioralFingerprints: {
      enabled: true,
      sensitivity: 'medium' as const,
    },
  },
  circadianRhythm: {
    enabled: true,
    timezone: 'UTC',
    sunshineHours: '06:00-22:00',
    moonlightHours: '22:00-06:00',
    sunshineReplicas: 10,
    moonlightReplicas: 2,
    gpuBurst: {
      enabled: false,
      maxGPUs: 4,
      burstThreshold: '80%',
    },
  },
  autoimmune: {
    enabled: false,
    selfHealingDelay: '30s',
  },
  feverResponse: {
    enabled: true,
    triggerThreshold: 5,
    throttlePercent: 50,
    duration: '5m',
  },
  apoptosis: {
    enabled: true,
    gracePeriod: '30s',
    drainConnections: true,
  },
  boneMarrow: {
    scanOnPush: true,
    immutableTags: true,
  },
} as const;

/**
 * Parse duration string to milliseconds
 */
export function parseDuration(duration: string): number {
  const match = duration.match(/^(\d+)(s|m|h|d)$/);
  if (!match) return 0;
  
  const value = parseInt(match[1], 10);
  const unit = match[2];
  
  switch (unit) {
    case 's': return value * 1000;
    case 'm': return value * 60 * 1000;
    case 'h': return value * 60 * 60 * 1000;
    case 'd': return value * 24 * 60 * 60 * 1000;
    default: return 0;
  }
}

/**
 * Parse time range (HH:MM-HH:MM) to start/end hours
 */
export function parseTimeRange(range: string): { start: number; end: number } {
  const [start, end] = range.split('-').map(t => {
    const [hours, minutes] = t.split(':').map(Number);
    return hours + minutes / 60;
  });
  return { start, end };
}

/**
 * Check if current time is in sunshine mode
 */
export function isInSunshineMode(
  sunshineHours: string,
  timezone: string = 'UTC'
): boolean {
  const { start, end } = parseTimeRange(sunshineHours);
  
  // Get current hour in specified timezone
  const now = new Date();
  const formatter = new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: false,
    timeZone: timezone,
  });
  const [hours, minutes] = formatter.format(now).split(':').map(Number);
  const currentHour = hours + minutes / 60;
  
  // Handle overnight ranges (e.g., 22:00-06:00)
  if (start < end) {
    return currentHour >= start && currentHour < end;
  } else {
    return currentHour >= start || currentHour < end;
  }
}

/**
 * Determine current circadian mode
 */
export function getCurrentCircadianMode(spec: ImmuneSystemSpec): CircadianMode {
  const rhythm = spec.circadianRhythm;
  if (!rhythm?.enabled) return 'sunshine';
  
  return isInSunshineMode(
    rhythm.sunshineHours || DEFAULTS.circadianRhythm.sunshineHours,
    rhythm.timezone || DEFAULTS.circadianRhythm.timezone
  ) ? 'sunshine' : 'moonlight';
}

/**
 * Get target replica count based on circadian mode
 */
export function getTargetReplicas(spec: ImmuneSystemSpec): number {
  const rhythm = spec.circadianRhythm;
  if (!rhythm?.enabled) {
    return rhythm?.sunshineReplicas || DEFAULTS.circadianRhythm.sunshineReplicas;
  }
  
  const mode = getCurrentCircadianMode(spec);
  return mode === 'sunshine'
    ? (rhythm.sunshineReplicas || DEFAULTS.circadianRhythm.sunshineReplicas)
    : (rhythm.moonlightReplicas || DEFAULTS.circadianRhythm.moonlightReplicas);
}

/**
 * Determine phase based on threat count
 */
export function determinePhase(
  spec: ImmuneSystemSpec,
  activeThreats: number,
  previousPhase?: ImmunePhase
): ImmunePhase {
  const feverThreshold = spec.feverResponse?.triggerThreshold 
    || DEFAULTS.feverResponse.triggerThreshold;
  
  if (activeThreats >= feverThreshold && spec.feverResponse?.enabled !== false) {
    return 'Fever';
  }
  
  if (activeThreats > 0) {
    return 'UnderAttack';
  }
  
  if (previousPhase === 'UnderAttack' || previousPhase === 'Fever') {
    return 'Healing';
  }
  
  return 'Healthy';
}

/**
 * Check if an image matches allowlist patterns
 */
export function isImageAllowed(
  image: string,
  allowlist: string[]
): boolean {
  return allowlist.some(pattern => {
    // Convert glob pattern to regex
    const regex = new RegExp(
      '^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$'
    );
    return regex.test(image);
  });
}

/**
 * Check if namespace is trusted
 */
export function isNamespaceTrusted(
  namespace: string,
  trustedNamespaces: string[]
): boolean {
  return trustedNamespaces.includes(namespace);
}

/**
 * Apply defaults to spec
 */
export function applyDefaults(spec: ImmuneSystemSpec): ImmuneSystemSpec {
  return {
    redBloodCells: {
      ...DEFAULTS.redBloodCells,
      ...spec.redBloodCells,
    },
    whiteBloodCells: {
      ...DEFAULTS.whiteBloodCells,
      ...spec.whiteBloodCells,
      garbageCollection: {
        ...DEFAULTS.whiteBloodCells.garbageCollection,
        ...spec.whiteBloodCells.garbageCollection,
      },
      networkPolicy: {
        ...DEFAULTS.whiteBloodCells.networkPolicy,
        ...spec.whiteBloodCells.networkPolicy,
      },
    },
    antibodies: {
      ...DEFAULTS.antibodies,
      ...spec.antibodies,
      behavioralFingerprints: {
        ...DEFAULTS.antibodies.behavioralFingerprints,
        ...spec.antibodies?.behavioralFingerprints,
      },
    },
    circadianRhythm: {
      ...DEFAULTS.circadianRhythm,
      ...spec.circadianRhythm,
      gpuBurst: {
        ...DEFAULTS.circadianRhythm.gpuBurst,
        ...spec.circadianRhythm?.gpuBurst,
      },
    },
    autoimmune: {
      ...DEFAULTS.autoimmune,
      ...spec.autoimmune,
    },
    feverResponse: {
      ...DEFAULTS.feverResponse,
      ...spec.feverResponse,
    },
    apoptosis: {
      ...DEFAULTS.apoptosis,
      ...spec.apoptosis,
    },
    boneMarrow: {
      ...DEFAULTS.boneMarrow,
      ...spec.boneMarrow,
    },
  };
}

/**
 * Initialize status for new ImmuneSystem
 */
export function initializeStatus(): ImmuneSystemStatus {
  return {
    phase: 'Initializing',
    lastTransitionTime: new Date().toISOString(),
    activeThreats: 0,
    neutralizedThreats: 0,
    learnedSignatures: 0,
    circadianMode: 'sunshine',
    currentReplicas: 0,
    conditions: [
      {
        type: 'Ready',
        status: 'False',
        lastTransitionTime: new Date().toISOString(),
        reason: 'Initializing',
        message: 'ImmuneSystem is initializing',
      },
    ],
  };
}

/**
 * Update status phase
 */
export function updatePhase(
  status: ImmuneSystemStatus,
  phase: ImmunePhase,
  reason: string,
  message: string
): ImmuneSystemStatus {
  const now = new Date().toISOString();
  
  return {
    ...status,
    phase,
    lastTransitionTime: now,
    conditions: [
      ...(status.conditions || []).filter(c => c.type !== 'Phase'),
      {
        type: 'Phase',
        status: 'True',
        lastTransitionTime: now,
        reason,
        message,
      },
    ],
  };
}

/**
 * Create threat signature from event
 */
export function createSignatureFromEvent(
  event: ThreatEvent,
  vector: number[]
): ThreatSignature {
  return {
    id: `sig-${event.id}`,
    vector,
    type: event.type,
    severity: event.severity,
    source: `${event.resource.kind}/${event.resource.namespace}/${event.resource.name}`,
    learnedAt: new Date().toISOString(),
    matchCount: 1,
    metadata: {
      scanner: event.scanner,
      details: event.details,
    },
  };
}

/**
 * Calculate controller metrics from status
 */
export function calculateMetrics(
  status: ImmuneSystemStatus,
  spec: ImmuneSystemSpec
): ControllerMetrics {
  return {
    activeThreats: status.activeThreats || 0,
    threatsNeutralized: status.neutralizedThreats || 0,
    signaturesLearned: status.learnedSignatures || 0,
    circadianMode: status.circadianMode === 'sunshine' ? 1 : 0,
    feverActive: status.phase === 'Fever',
    reconcileDuration: 0, // Set by reconciler
  };
}

/**
 * API group and version
 */
export const API_GROUP = 'swarm.strategickhaos.ai';
export const API_VERSION = 'v1';
export const RESOURCE_PLURAL = 'immunesystems';
export const RESOURCE_KIND = 'ImmuneSystem';

/**
 * Label selectors
 */
export const LABELS = {
  APP: 'swarm-immune',
  MANAGED_BY: 'swarm-immune-controller',
  COMPONENT: 'immune-system',
} as const;

/**
 * Annotation keys
 */
export const ANNOTATIONS = {
  LAST_SCAN: 'swarm.strategickhaos.ai/last-scan',
  THREAT_COUNT: 'swarm.strategickhaos.ai/threat-count',
  SIGNATURE_ID: 'swarm.strategickhaos.ai/signature-id',
  QUARANTINED_AT: 'swarm.strategickhaos.ai/quarantined-at',
  RECONCILE: 'swarm.strategickhaos.ai/reconcile',
} as const;

/**
 * Finalizer name
 */
export const FINALIZER = 'swarm.strategickhaos.ai/finalizer';
