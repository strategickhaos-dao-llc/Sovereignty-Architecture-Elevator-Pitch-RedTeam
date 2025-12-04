/**
 * Sovereign Architect's Chronicle - Type Definitions
 * 
 * This module defines the data structures for tracking architectural
 * journal entries as part of the Neural Logbook system.
 */

/** Categories for architectural journal entries */
export type ChronicleCategory = 
  | "observability"      // Infrastructure monitoring, status reports
  | "governance"         // Priority councils, voting, triage
  | "research"           // AI evolution, self-improvement systems
  | "philosophy"         // Singularity engines, system consciousness
  | "visualization"      // UX, dashboards, data visualization
  | "frontier"           // Quantum labs, speculative architecture
  | "infrastructure"     // Core systems, deployments, scaling
  | "integration"        // Cross-system connections, APIs
  | "security"           // Security policies, access control
  | "documentation";     // Docs, runbooks, knowledge base

/** Status of a chronicle entry */
export type ChronicleStatus = 
  | "ideation"           // Initial brain dump / concept
  | "specification"      // Being specified / detailed
  | "in_progress"        // Actively being built
  | "review"             // Under review / testing
  | "deployed"           // Live and operational
  | "evolved"            // Superseded by newer iteration
  | "archived";          // Preserved but no longer active

/** A single Chronicle Entry representing an architectural artifact */
export interface ChronicleEntry {
  /** Unique identifier */
  id: string;
  
  /** Title of the entry */
  title: string;
  
  /** Detailed description */
  description: string;
  
  /** Category classification */
  category: ChronicleCategory;
  
  /** Current status */
  status: ChronicleStatus;
  
  /** Creation timestamp */
  createdAt: string;
  
  /** Last update timestamp */
  updatedAt: string;
  
  /** Source (e.g., github_issue, manual, discord) */
  source: string;
  
  /** Source reference (e.g., issue number, URL) */
  sourceRef?: string;
  
  /** Author/creator */
  author: string;
  
  /** Tags for additional classification */
  tags: string[];
  
  /** Related entries by ID */
  relatedEntries?: string[];
  
  /** Priority level (1-5, 1 being highest) */
  priority?: number;
  
  /** Estimated complexity (1-5) */
  complexity?: number;
  
  /** Dependencies on other systems/entries */
  dependencies?: string[];
  
  /** Notes and additional context */
  notes?: string;
}

/** Summary view of a Chronicle Entry for list views */
export interface ChronicleEntrySummary {
  id: string;
  title: string;
  category: ChronicleCategory;
  status: ChronicleStatus;
  createdAt: string;
  priority?: number;
}

/** Group entries by category for timeline display */
export interface ChronicleCategoryGroup {
  category: ChronicleCategory;
  displayName: string;
  emoji: string;
  entries: ChronicleEntrySummary[];
  count: number;
}

/** Timeline view configuration */
export interface ChronicleTimeline {
  /** Timeline title */
  title: string;
  
  /** Description */
  description: string;
  
  /** Groups organized by category */
  categoryGroups: ChronicleCategoryGroup[];
  
  /** Total entry count */
  totalEntries: number;
  
  /** Generation timestamp */
  generatedAt: string;
  
  /** Filters applied */
  filters?: {
    status?: ChronicleStatus[];
    categories?: ChronicleCategory[];
    dateRange?: { start: string; end: string };
  };
}

/** Roadmap phase for organizing timeline display */
export interface RoadmapPhase {
  name: string;
  description: string;
  startDate?: string;
  endDate?: string;
  entries: ChronicleEntrySummary[];
  status: "past" | "current" | "future";
}

/** Full roadmap view */
export interface ChronicleRoadmap {
  title: string;
  vision: string;
  phases: RoadmapPhase[];
  generatedAt: string;
}

/** Category metadata for display purposes */
export const CATEGORY_METADATA: Record<ChronicleCategory, { displayName: string; emoji: string; description: string }> = {
  observability: {
    displayName: "Observability Chapter",
    emoji: "📊",
    description: "GCP infrastructure status, monitoring, metrics, and system health"
  },
  governance: {
    displayName: "Governance & Prioritization Chapter",
    emoji: "⚖️",
    description: "Priority Council, PR triage, voting mechanisms, and decision frameworks"
  },
  research: {
    displayName: "Agent Research & Evolution Chapter",
    emoji: "🧬",
    description: "Self-Evolving AI Refinery, learning modules, agent improvements"
  },
  philosophy: {
    displayName: "Philosophy of Systems Chapter",
    emoji: "🔮",
    description: "Singularity Engine, self-improvement architectures, emergent behavior"
  },
  visualization: {
    displayName: "UX & Data Visualization Chapter",
    emoji: "🪞",
    description: "Mirror Lab, real-time dashboards, user experience design"
  },
  frontier: {
    displayName: "Frontier Research Chapter",
    emoji: "⚛️",
    description: "Quantum Mirror Lab, speculative architecture, experimental systems"
  },
  infrastructure: {
    displayName: "Core Infrastructure Chapter",
    emoji: "🏗️",
    description: "Deployments, scaling, Kubernetes, cloud resources"
  },
  integration: {
    displayName: "Integration Chapter",
    emoji: "🔗",
    description: "APIs, webhooks, cross-system connections"
  },
  security: {
    displayName: "Security & Access Chapter",
    emoji: "🔐",
    description: "RBAC, secrets management, audit logging"
  },
  documentation: {
    displayName: "Knowledge Base Chapter",
    emoji: "📚",
    description: "Documentation, runbooks, architectural decision records"
  }
};

/** Status metadata for display purposes */
export const STATUS_METADATA: Record<ChronicleStatus, { displayName: string; emoji: string; color: number }> = {
  ideation: { displayName: "Ideation", emoji: "💡", color: 0xFFC107 },
  specification: { displayName: "Specification", emoji: "📝", color: 0x2196F3 },
  in_progress: { displayName: "In Progress", emoji: "🔧", color: 0x9C27B0 },
  review: { displayName: "Review", emoji: "👀", color: 0xFF9800 },
  deployed: { displayName: "Deployed", emoji: "✅", color: 0x4CAF50 },
  evolved: { displayName: "Evolved", emoji: "🦋", color: 0x00BCD4 },
  archived: { displayName: "Archived", emoji: "📦", color: 0x607D8B }
};
