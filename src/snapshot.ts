import { createHash } from "crypto";
import { writeFileSync, readFileSync, readdirSync, existsSync, mkdirSync } from "fs";
import yaml from "js-yaml";
import { config } from "./config.js";
import { getInfraState } from "./infra.js";
import { getAgentState } from "./ai/agents.js";
import { getRepoHealth } from "./repos.js";
import { getSecurityMetrics } from "./security.js";
import { getObservabilityState } from "./monitoring.js";

export interface Snapshot {
  id: string;
  timestamp: number;
  createdAt: string;
  config: typeof config;
  infrastructure: any;
  agents: any;
  repositories: any;
  security: any;
  observability: any;
  checksum: string;
}

export async function createSnapshot(customId?: string): Promise<Snapshot> {
  const id = customId ?? Date.now().toString();
  const data = {
    id,
    timestamp: Date.now(),
    createdAt: new Date().toISOString(),
    config,
    infrastructure: await getInfraState(),
    agents: await getAgentState(),
    repositories: await getRepoHealth(),
    security: await getSecurityMetrics(),
    observability: await getObservabilityState(),
    checksum: "", // placeholder
  };

  // Calculate checksum of the data including the placeholder
  const yamlStr = yaml.dump(data);
  const checksum = createHash("sha256").update(yamlStr).digest("hex");

  // Return with actual checksum
  return { ...data, checksum };
}

export function saveSnapshot(snapshot: Snapshot): string {
  // Verify checksum by recalculating with placeholder
  const dataForVerification = { ...snapshot, checksum: "" };
  const yamlForVerification = yaml.dump(dataForVerification);
  const recalculatedChecksum = createHash("sha256").update(yamlForVerification).digest("hex");
  
  if (recalculatedChecksum !== snapshot.checksum) {
    throw new Error("Checksum mismatch — data tampered");
  }

  const filename = `${snapshot.id}.fxsnapshot`;
  
  // Ensure snapshots directory exists
  if (!existsSync("snapshots")) {
    mkdirSync("snapshots", { mode: 0o700 });
  }
  
  // Write the full snapshot with checksum to file
  const yamlStr = yaml.dump(snapshot);
  writeFileSync(`snapshots/${filename}`, yamlStr);
  return filename;
}

export function loadSnapshot(id: string): Snapshot {
  const filename = `${id}.fxsnapshot`;
  const yamlStr = readFileSync(`snapshots/${filename}`, "utf-8");
  const snapshot = yaml.load(yamlStr) as Snapshot;

  // Verify checksum by recalculating with placeholder
  const dataForVerification = { ...snapshot, checksum: "" };
  const yamlForVerification = yaml.dump(dataForVerification);
  const recalculatedChecksum = createHash("sha256").update(yamlForVerification).digest("hex");
  
  if (recalculatedChecksum !== snapshot.checksum) {
    throw new Error("Snapshot corrupted");
  }

  return snapshot;
}

export function listSnapshots(): string[] {
  if (!existsSync("snapshots")) return [];
  return readdirSync("snapshots")
    .filter(f => f.endsWith(".fxsnapshot"))
    .sort()
    .reverse();
}

export function getLatestSnapshotId(): string | null {
  const list = listSnapshots();
  if (list.length === 0) return null;
  return list[0].split(".")[0];
}
