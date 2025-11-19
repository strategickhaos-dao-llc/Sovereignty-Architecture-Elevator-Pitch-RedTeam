import fs from "fs";
import crypto from "crypto";
import { loadConfig } from "./config.js";

export interface FxSnapshot {
  snapshot: {
    id: string;
    type: string;
    version: string;
    timestamp: string;
    environment: string;
  };
  system: {
    name: string;
    org: string;
    operator: string;
  };
  health: {
    overall_status: string;
    critical_alerts: number;
    warning_alerts: number;
    services_degraded: number;
  };
  metadata: {
    generated_by: string;
    schema_version: string;
    checksum: string;
    retention_policy: string;
  };
}

/**
 * Generate a unique snapshot ID based on timestamp
 */
export function generateSnapshotId(): string {
  return Math.floor(Date.now() / 1000).toString();
}

/**
 * Calculate SHA256 checksum of snapshot content
 */
export function calculateChecksum(content: string): string {
  return crypto.createHash("sha256").update(content).digest("hex");
}

/**
 * Create a new FX snapshot with current system state
 */
export function createSnapshot(snapshotId?: string): FxSnapshot {
  const cfg = loadConfig();
  const id = snapshotId || generateSnapshotId();
  const timestamp = new Date().toISOString();

  return {
    snapshot: {
      id,
      type: "fxsnapshot",
      version: "1.0",
      timestamp,
      environment: "production",
    },
    system: {
      name: cfg.org?.name || "Strategickhaos Sovereignty Architecture",
      org: cfg.org?.name || "Strategickhaos DAO LLC / Valoryield Engine",
      operator: cfg.org?.contact?.owner || "Unknown",
    },
    health: {
      overall_status: "healthy",
      critical_alerts: 0,
      warning_alerts: 0,
      services_degraded: 0,
    },
    metadata: {
      generated_by: "fx-snapshot-v1",
      schema_version: "1.0",
      checksum: "",
      retention_policy: "90-days",
    },
  };
}

/**
 * Save snapshot to file
 */
export function saveSnapshot(snapshot: FxSnapshot, filepath?: string): string {
  const filename = filepath || `${snapshot.snapshot.id}.fxsnapshot`;
  
  // Convert to YAML-like format for consistency with other config files
  const content = formatSnapshotAsYaml(snapshot);
  
  // Calculate checksum
  snapshot.metadata.checksum = calculateChecksum(content);
  
  // Re-format with checksum
  const finalContent = formatSnapshotAsYaml(snapshot);
  
  fs.writeFileSync(filename, finalContent, "utf8");
  return filename;
}

/**
 * Load snapshot from file
 */
export function loadSnapshot(filepath: string): FxSnapshot | null {
  try {
    const content = fs.readFileSync(filepath, "utf8");
    // This is a simplified parser - in production you'd use a proper YAML parser
    return JSON.parse(content) as FxSnapshot;
  } catch (error) {
    console.error(`Failed to load snapshot from ${filepath}:`, error);
    return null;
  }
}

/**
 * Format snapshot as YAML-like string
 */
function formatSnapshotAsYaml(snapshot: FxSnapshot): string {
  return `# FX Snapshot: ${snapshot.snapshot.id}
# Generated: ${snapshot.snapshot.timestamp}
# Type: System State Snapshot
# Purpose: Capture functional execution state of Sovereignty Architecture

snapshot:
  id: "${snapshot.snapshot.id}"
  type: "${snapshot.snapshot.type}"
  version: "${snapshot.snapshot.version}"
  timestamp: "${snapshot.snapshot.timestamp}"
  environment: "${snapshot.snapshot.environment}"

system:
  name: "${snapshot.system.name}"
  org: "${snapshot.system.org}"
  operator: "${snapshot.system.operator}"

health:
  overall_status: "${snapshot.health.overall_status}"
  critical_alerts: ${snapshot.health.critical_alerts}
  warning_alerts: ${snapshot.health.warning_alerts}
  services_degraded: ${snapshot.health.services_degraded}

metadata:
  generated_by: "${snapshot.metadata.generated_by}"
  schema_version: "${snapshot.metadata.schema_version}"
  checksum: "${snapshot.metadata.checksum}"
  retention_policy: "${snapshot.metadata.retention_policy}"
`;
}

/**
 * List all snapshots in the current directory
 */
export function listSnapshots(directory: string = "."): string[] {
  const files = fs.readdirSync(directory);
  return files.filter(f => f.endsWith(".fxsnapshot"));
}

/**
 * Get the latest snapshot
 */
export function getLatestSnapshot(directory: string = "."): string | null {
  const snapshots = listSnapshots(directory);
  if (snapshots.length === 0) return null;
  
  // Sort by ID (which is timestamp-based)
  snapshots.sort((a, b) => {
    const idA = parseInt(a.split(".")[0]);
    const idB = parseInt(b.split(".")[0]);
    return idB - idA;
  });
  
  return snapshots[0];
}
