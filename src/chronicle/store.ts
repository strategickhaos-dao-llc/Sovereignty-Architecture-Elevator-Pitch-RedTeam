/**
 * Sovereign Architect's Chronicle - Data Store
 * 
 * In-memory store for chronicle entries with file-based persistence.
 * In production, this would connect to a database or use the vector store.
 */

import fs from "fs";
import path from "path";
import type { 
  ChronicleEntry, 
  ChronicleEntrySummary, 
  ChronicleCategory, 
  ChronicleStatus,
  ChronicleTimeline,
  ChronicleCategoryGroup,
  ChronicleRoadmap,
  RoadmapPhase
} from "./types.js";
import { CATEGORY_METADATA } from "./types.js";

const DATA_FILE = "chronicle_data.json";

/** Generate a unique ID for entries */
function generateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `chr_${timestamp}_${random}`;
}

/** In-memory chronicle store */
class ChronicleStore {
  private entries: Map<string, ChronicleEntry> = new Map();
  private dataPath: string;
  
  constructor(dataDir: string = ".") {
    this.dataPath = path.join(dataDir, DATA_FILE);
    this.load();
  }
  
  /** Load entries from file */
  private load(): void {
    try {
      if (fs.existsSync(this.dataPath)) {
        const data = JSON.parse(fs.readFileSync(this.dataPath, "utf8"));
        this.entries = new Map(Object.entries(data.entries || {}));
        console.log(`Chronicle: Loaded ${this.entries.size} entries`);
      }
    } catch (error) {
      console.warn("Chronicle: Could not load data file, starting fresh");
      this.entries = new Map();
    }
  }
  
  /** Save entries to file */
  private save(): void {
    try {
      const data = {
        version: "1.0",
        lastUpdated: new Date().toISOString(),
        entries: Object.fromEntries(this.entries)
      };
      fs.writeFileSync(this.dataPath, JSON.stringify(data, null, 2));
    } catch (error) {
      console.error("Chronicle: Failed to save data", error);
    }
  }
  
  /** Create a new chronicle entry */
  createEntry(input: Omit<ChronicleEntry, "id" | "createdAt" | "updatedAt">): ChronicleEntry {
    const now = new Date().toISOString();
    const entry: ChronicleEntry = {
      ...input,
      id: generateId(),
      createdAt: now,
      updatedAt: now
    };
    this.entries.set(entry.id, entry);
    this.save();
    return entry;
  }
  
  /** Get entry by ID */
  getEntry(id: string): ChronicleEntry | undefined {
    return this.entries.get(id);
  }
  
  /** Update an existing entry */
  updateEntry(id: string, updates: Partial<Omit<ChronicleEntry, "id" | "createdAt">>): ChronicleEntry | undefined {
    const entry = this.entries.get(id);
    if (!entry) return undefined;
    
    const updated: ChronicleEntry = {
      ...entry,
      ...updates,
      updatedAt: new Date().toISOString()
    };
    this.entries.set(id, updated);
    this.save();
    return updated;
  }
  
  /** Delete an entry */
  deleteEntry(id: string): boolean {
    const result = this.entries.delete(id);
    if (result) this.save();
    return result;
  }
  
  /** List all entries */
  listEntries(): ChronicleEntry[] {
    return Array.from(this.entries.values());
  }
  
  /** Get entries by category */
  getByCategory(category: ChronicleCategory): ChronicleEntry[] {
    return this.listEntries().filter(e => e.category === category);
  }
  
  /** Get entries by status */
  getByStatus(status: ChronicleStatus): ChronicleEntry[] {
    return this.listEntries().filter(e => e.status === status);
  }
  
  /** Search entries by title or description */
  search(query: string): ChronicleEntry[] {
    const lower = query.toLowerCase();
    return this.listEntries().filter(e => 
      e.title.toLowerCase().includes(lower) ||
      e.description.toLowerCase().includes(lower) ||
      e.tags.some(t => t.toLowerCase().includes(lower))
    );
  }
  
  /** Get summary view of entries */
  getSummaries(filters?: {
    categories?: ChronicleCategory[];
    statuses?: ChronicleStatus[];
    limit?: number;
  }): ChronicleEntrySummary[] {
    let entries = this.listEntries();
    
    if (filters?.categories?.length) {
      entries = entries.filter(e => filters.categories!.includes(e.category));
    }
    if (filters?.statuses?.length) {
      entries = entries.filter(e => filters.statuses!.includes(e.status));
    }
    
    // Sort by priority then by creation date
    entries.sort((a, b) => {
      const priorityDiff = (a.priority || 5) - (b.priority || 5);
      if (priorityDiff !== 0) return priorityDiff;
      return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    });
    
    if (filters?.limit) {
      entries = entries.slice(0, filters.limit);
    }
    
    return entries.map(e => ({
      id: e.id,
      title: e.title,
      category: e.category,
      status: e.status,
      createdAt: e.createdAt,
      priority: e.priority
    }));
  }
  
  /** Generate timeline view grouped by category */
  generateTimeline(filters?: {
    status?: ChronicleStatus[];
    categories?: ChronicleCategory[];
  }): ChronicleTimeline {
    let entries = this.listEntries();
    
    if (filters?.status?.length) {
      entries = entries.filter(e => filters.status!.includes(e.status));
    }
    if (filters?.categories?.length) {
      entries = entries.filter(e => filters.categories!.includes(e.category));
    }
    
    // Group by category
    const categoryGroups: ChronicleCategoryGroup[] = [];
    const categories = Object.keys(CATEGORY_METADATA) as ChronicleCategory[];
    
    for (const category of categories) {
      const categoryEntries = entries.filter(e => e.category === category);
      if (categoryEntries.length > 0 || !filters?.categories) {
        categoryGroups.push({
          category,
          displayName: CATEGORY_METADATA[category].displayName,
          emoji: CATEGORY_METADATA[category].emoji,
          entries: categoryEntries.map(e => ({
            id: e.id,
            title: e.title,
            category: e.category,
            status: e.status,
            createdAt: e.createdAt,
            priority: e.priority
          })),
          count: categoryEntries.length
        });
      }
    }
    
    // Filter out empty categories unless specifically requested
    const filteredGroups = filters?.categories 
      ? categoryGroups.filter(g => filters.categories!.includes(g.category))
      : categoryGroups.filter(g => g.count > 0);
    
    return {
      title: "Sovereign Architect's Chronicle",
      description: "A neural logbook of distributed systems architecture — capturing emergent design artifacts, governance requests, and evolutionary system specifications.",
      categoryGroups: filteredGroups,
      totalEntries: entries.length,
      generatedAt: new Date().toISOString(),
      filters
    };
  }
  
  /** Generate roadmap view organized by phase */
  generateRoadmap(): ChronicleRoadmap {
    const entries = this.listEntries();
    
    // Define phases based on status
    const phases: RoadmapPhase[] = [
      {
        name: "Ideation & Discovery",
        description: "Brain dumps, concepts, and initial explorations",
        entries: entries.filter(e => e.status === "ideation").map(e => ({
          id: e.id,
          title: e.title,
          category: e.category,
          status: e.status,
          createdAt: e.createdAt,
          priority: e.priority
        })),
        status: "current"
      },
      {
        name: "Specification & Design",
        description: "Detailed specifications and architecture documents",
        entries: entries.filter(e => e.status === "specification").map(e => ({
          id: e.id,
          title: e.title,
          category: e.category,
          status: e.status,
          createdAt: e.createdAt,
          priority: e.priority
        })),
        status: "current"
      },
      {
        name: "Active Development",
        description: "Systems being actively built and iterated",
        entries: entries.filter(e => e.status === "in_progress" || e.status === "review").map(e => ({
          id: e.id,
          title: e.title,
          category: e.category,
          status: e.status,
          createdAt: e.createdAt,
          priority: e.priority
        })),
        status: "current"
      },
      {
        name: "Deployed & Operational",
        description: "Live systems running in production",
        entries: entries.filter(e => e.status === "deployed").map(e => ({
          id: e.id,
          title: e.title,
          category: e.category,
          status: e.status,
          createdAt: e.createdAt,
          priority: e.priority
        })),
        status: "past"
      },
      {
        name: "Evolved & Archived",
        description: "Historical artifacts and superseded systems",
        entries: entries.filter(e => e.status === "evolved" || e.status === "archived").map(e => ({
          id: e.id,
          title: e.title,
          category: e.category,
          status: e.status,
          createdAt: e.createdAt,
          priority: e.priority
        })),
        status: "past"
      }
    ];
    
    return {
      title: "Sovereignty Architecture Roadmap",
      vision: "Building a sovereign, self-evolving AI ecosystem through distributed systems architecture and emergent design patterns.",
      phases: phases.filter(p => p.entries.length > 0),
      generatedAt: new Date().toISOString()
    };
  }
  
  /** Get statistics about the chronicle */
  getStats(): {
    totalEntries: number;
    byCategory: Record<string, number>;
    byStatus: Record<string, number>;
    recentActivity: ChronicleEntrySummary[];
  } {
    const entries = this.listEntries();
    
    const byCategory: Record<string, number> = {};
    const byStatus: Record<string, number> = {};
    
    for (const entry of entries) {
      byCategory[entry.category] = (byCategory[entry.category] || 0) + 1;
      byStatus[entry.status] = (byStatus[entry.status] || 0) + 1;
    }
    
    // Recent activity - last 10 updated entries
    const recentActivity = [...entries]
      .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
      .slice(0, 10)
      .map(e => ({
        id: e.id,
        title: e.title,
        category: e.category,
        status: e.status,
        createdAt: e.createdAt,
        priority: e.priority
      }));
    
    return {
      totalEntries: entries.length,
      byCategory,
      byStatus,
      recentActivity
    };
  }
}

// Singleton instance
let storeInstance: ChronicleStore | null = null;

export function getChronicleStore(dataDir?: string): ChronicleStore {
  if (!storeInstance) {
    storeInstance = new ChronicleStore(dataDir);
  }
  return storeInstance;
}

export { ChronicleStore };
