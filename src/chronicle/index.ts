/**
 * Sovereign Architect's Chronicle
 * 
 * A neural logbook system for tracking architectural journal entries
 * as part of the Sovereignty Architecture Control Deck.
 * 
 * Features:
 * - Chronicle Entry management (CRUD)
 * - Timeline view grouped by category
 * - Roadmap view organized by development phase
 * - Discord integration with slash commands
 * - Category-based organization
 * - Search functionality
 * 
 * Categories (Chapters):
 * - 📊 Observability - GCP infrastructure status, monitoring, metrics
 * - ⚖️ Governance - Priority Council, PR triage, voting
 * - 🧬 Research - Self-Evolving AI Refinery, agent improvements
 * - 🔮 Philosophy - Singularity Engine, self-improvement
 * - 🪞 Visualization - Mirror Lab, real-time dashboards
 * - ⚛️ Frontier - Quantum Mirror Lab, speculative architecture
 * - 🏗️ Infrastructure - Deployments, scaling, core systems
 * - 🔗 Integration - APIs, webhooks, cross-system connections
 * - 🔐 Security - RBAC, secrets management, audit logging
 * - 📚 Documentation - Docs, runbooks, knowledge base
 */

// Types
export type {
  ChronicleCategory,
  ChronicleStatus,
  ChronicleEntry,
  ChronicleEntrySummary,
  ChronicleCategoryGroup,
  ChronicleTimeline,
  RoadmapPhase,
  ChronicleRoadmap
} from "./types.js";

export { CATEGORY_METADATA, STATUS_METADATA } from "./types.js";

// Store
export { getChronicleStore, ChronicleStore } from "./store.js";

// Routes
export { createChronicleRoutes } from "./routes.js";

// Discord integration
export {
  getChronicleCommands,
  buildTimelineEmbed,
  buildRoadmapEmbed,
  buildStatsEmbed,
  buildCategoryEmbed,
  buildSearchEmbed,
  buildNewEntryEmbed,
  sendChronicleToChannel
} from "./discord.js";
