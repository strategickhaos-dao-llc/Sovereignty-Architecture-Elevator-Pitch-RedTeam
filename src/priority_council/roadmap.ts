/**
 * Priority Council - Roadmap Generator
 * 
 * Generates a prioritized roadmap based on PR analysis,
 * dependency graphs, and critical path analysis.
 */

import type { PRAnalysis, PriorityTier } from "./scoring.js";

export interface RoadmapEntry {
  prNumber: number;
  title: string;
  tier: PriorityTier;
  priority: number;
  category: string;
  week: number;
  blockedBy: number[];
  blocks: number[];
}

export interface Roadmap {
  generatedAt: string;
  totalPRs: number;
  criticalCount: number;
  criticalPath: RoadmapEntry[];
  weeklyPlan: Record<number, RoadmapEntry[]>;
  blockedPRs: RoadmapEntry[];
  stats: {
    byTier: Record<PriorityTier, number>;
    byCategory: Record<string, number>;
    averagePriority: number;
    estimatedCompletionWeeks: number;
  };
}

/**
 * Build a dependency graph from PR analyses
 */
export function buildDependencyGraph(
  analyses: PRAnalysis[]
): Map<number, Set<number>> {
  const graph = new Map<number, Set<number>>();

  for (const analysis of analyses) {
    if (!graph.has(analysis.prNumber)) {
      graph.set(analysis.prNumber, new Set());
    }

    for (const dep of analysis.dependencies) {
      graph.get(analysis.prNumber)!.add(dep);
    }
  }

  return graph;
}

/**
 * Build reverse dependency graph (what does each PR block)
 */
export function buildReverseGraph(
  analyses: PRAnalysis[]
): Map<number, Set<number>> {
  const reverseGraph = new Map<number, Set<number>>();

  for (const analysis of analyses) {
    if (!reverseGraph.has(analysis.prNumber)) {
      reverseGraph.set(analysis.prNumber, new Set());
    }

    for (const dep of analysis.dependencies) {
      if (!reverseGraph.has(dep)) {
        reverseGraph.set(dep, new Set());
      }
      reverseGraph.get(dep)!.add(analysis.prNumber);
    }
  }

  return reverseGraph;
}

/**
 * Topological sort for dependency ordering
 */
export function topologicalSort(
  analyses: PRAnalysis[],
  dependencyGraph: Map<number, Set<number>>
): number[] {
  const visited = new Set<number>();
  const result: number[] = [];
  const inProgress = new Set<number>();

  const prNumbers = analyses.map((a) => a.prNumber);

  function visit(prNumber: number): void {
    if (visited.has(prNumber)) return;
    if (inProgress.has(prNumber)) {
      // Cycle detected, skip
      return;
    }

    inProgress.add(prNumber);

    const deps = dependencyGraph.get(prNumber) || new Set();
    for (const dep of deps) {
      if (prNumbers.includes(dep)) {
        visit(dep);
      }
    }

    inProgress.delete(prNumber);
    visited.add(prNumber);
    result.push(prNumber);
  }

  for (const prNumber of prNumbers) {
    visit(prNumber);
  }

  return result;
}

/**
 * Identify critical path (highest impact PRs in dependency order)
 */
export function findCriticalPath(
  analyses: PRAnalysis[],
  dependencyGraph: Map<number, Set<number>>
): PRAnalysis[] {
  // Filter to critical and high priority PRs
  const important = analyses.filter(
    (a) => a.tier === "critical" || a.tier === "high"
  );

  if (important.length === 0) {
    return [];
  }

  // Get topological order
  const order = topologicalSort(important, dependencyGraph);

  // Return analyses in dependency order
  return order
    .map((prNum) => important.find((a) => a.prNumber === prNum)!)
    .filter(Boolean);
}

/**
 * Assign PRs to weeks based on priority and dependencies
 */
export function assignToWeeks(
  analyses: PRAnalysis[],
  dependencyGraph: Map<number, Set<number>>,
  prsPerWeek: number = 5
): Record<number, PRAnalysis[]> {
  const weeklyPlan: Record<number, PRAnalysis[]> = {};
  const assigned = new Set<number>();
  const sortedOrder = topologicalSort(analyses, dependencyGraph);

  // Sort by priority within topological order
  const orderedAnalyses = sortedOrder
    .map((prNum) => analyses.find((a) => a.prNumber === prNum)!)
    .filter(Boolean)
    .sort((a, b) => {
      // Critical first, then by priority score
      if (a.tier !== b.tier) {
        const tierOrder = { critical: 0, high: 1, medium: 2, low: 3, backlog: 4 };
        return tierOrder[a.tier] - tierOrder[b.tier];
      }
      return b.finalPriority - a.finalPriority;
    });

  let currentWeek = 1;
  let weekCount = 0;

  for (const analysis of orderedAnalyses) {
    // Check if all dependencies are assigned to earlier weeks
    const deps = dependencyGraph.get(analysis.prNumber) || new Set();
    const allDepsAssigned = [...deps].every((dep) => assigned.has(dep));

    if (!allDepsAssigned && analysis.dependencies.length > 0) {
      // Find the latest week of dependencies
      let maxDepWeek = 0;
      for (const [week, prs] of Object.entries(weeklyPlan)) {
        for (const pr of prs) {
          if (deps.has(pr.prNumber)) {
            maxDepWeek = Math.max(maxDepWeek, parseInt(week));
          }
        }
      }
      currentWeek = Math.max(currentWeek, maxDepWeek + 1);
      weekCount = 0;
    }

    if (!weeklyPlan[currentWeek]) {
      weeklyPlan[currentWeek] = [];
    }

    weeklyPlan[currentWeek].push(analysis);
    assigned.add(analysis.prNumber);
    weekCount++;

    if (weekCount >= prsPerWeek) {
      currentWeek++;
      weekCount = 0;
    }
  }

  return weeklyPlan;
}

/**
 * Find blocked PRs (have unresolved dependencies)
 */
export function findBlockedPRs(
  analyses: PRAnalysis[],
  dependencyGraph: Map<number, Set<number>>
): PRAnalysis[] {
  const prNumbers = new Set(analyses.map((a) => a.prNumber));

  return analyses.filter((analysis) => {
    const deps = dependencyGraph.get(analysis.prNumber) || new Set();
    // PR is blocked if it has dependencies not in current set
    for (const dep of deps) {
      if (!prNumbers.has(dep)) {
        return true;
      }
    }
    return false;
  });
}

/**
 * Generate complete roadmap from PR analyses
 */
export function generateRoadmap(
  analyses: PRAnalysis[],
  options: { prsPerWeek?: number } = {}
): Roadmap {
  const { prsPerWeek = 5 } = options;
  const dependencyGraph = buildDependencyGraph(analyses);
  const reverseGraph = buildReverseGraph(analyses);

  // Calculate stats
  const byTier: Record<PriorityTier, number> = {
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
    backlog: 0,
  };
  const byCategory: Record<string, number> = {};
  let totalPriority = 0;

  for (const analysis of analyses) {
    byTier[analysis.tier]++;
    byCategory[analysis.category] = (byCategory[analysis.category] || 0) + 1;
    totalPriority += analysis.finalPriority;
  }

  const criticalPath = findCriticalPath(analyses, dependencyGraph);
  const weeklyPlan = assignToWeeks(analyses, dependencyGraph, prsPerWeek);
  const blockedPRs = findBlockedPRs(analyses, dependencyGraph);

  // Convert to roadmap entries
  const toEntry = (a: PRAnalysis, week: number): RoadmapEntry => ({
    prNumber: a.prNumber,
    title: a.title,
    tier: a.tier,
    priority: a.finalPriority,
    category: a.category,
    week,
    blockedBy: a.dependencies,
    blocks: [...(reverseGraph.get(a.prNumber) || [])],
  });

  const weeklyEntries: Record<number, RoadmapEntry[]> = {};
  for (const [week, prs] of Object.entries(weeklyPlan)) {
    weeklyEntries[parseInt(week)] = prs.map((pr) =>
      toEntry(pr, parseInt(week))
    );
  }

  const estimatedWeeks = Math.max(...Object.keys(weeklyPlan).map(Number), 0);

  return {
    generatedAt: new Date().toISOString(),
    totalPRs: analyses.length,
    criticalCount: byTier.critical,
    criticalPath: criticalPath.map((a, i) => toEntry(a, i + 1)),
    weeklyPlan: weeklyEntries,
    blockedPRs: blockedPRs.map((a) => toEntry(a, 0)),
    stats: {
      byTier,
      byCategory,
      averagePriority:
        analyses.length > 0 ? Math.round(totalPriority / analyses.length) : 0,
      estimatedCompletionWeeks: estimatedWeeks,
    },
  };
}

/**
 * Format roadmap as Markdown
 */
export function formatRoadmapMarkdown(roadmap: Roadmap): string {
  const lines: string[] = [
    "# 🗺️ Priority Council Roadmap",
    "",
    `**Generated:** ${roadmap.generatedAt}`,
    "",
    "---",
    "",
    "## 📊 Overview",
    "",
    `- **Total PRs:** ${roadmap.totalPRs}`,
    `- **Critical PRs:** ${roadmap.criticalCount}`,
    `- **Average Priority:** ${roadmap.stats.averagePriority}/100`,
    `- **Estimated Completion:** ${roadmap.stats.estimatedCompletionWeeks} weeks`,
    "",
    "### By Priority Tier",
    "",
  ];

  const tierEmojis = {
    critical: "🚨",
    high: "⚡",
    medium: "📊",
    low: "📝",
    backlog: "📦",
  };

  for (const [tier, count] of Object.entries(roadmap.stats.byTier)) {
    const emoji = tierEmojis[tier as PriorityTier] || "•";
    lines.push(`- ${emoji} **${tier.charAt(0).toUpperCase() + tier.slice(1)}:** ${count}`);
  }

  lines.push("", "### By Category", "");
  for (const [category, count] of Object.entries(roadmap.stats.byCategory)) {
    lines.push(`- **${category}:** ${count}`);
  }

  if (roadmap.criticalPath.length > 0) {
    lines.push("", "---", "", "## 🎯 Critical Path", "");
    lines.push(
      "The fastest route to the most important features:",
      ""
    );

    for (const entry of roadmap.criticalPath) {
      lines.push(
        `1. **#${entry.prNumber}** - ${entry.title}`,
        `   - Priority: ${entry.priority}/100 (${entry.tier.toUpperCase()})`,
        `   - Category: ${entry.category}`
      );
      if (entry.blockedBy.length > 0) {
        lines.push(`   - Blocked by: ${entry.blockedBy.map((n) => `#${n}`).join(", ")}`);
      }
      lines.push("");
    }
  }

  lines.push("---", "", "## 📅 Weekly Plan", "");

  const sortedWeeks = Object.keys(roadmap.weeklyPlan)
    .map(Number)
    .sort((a, b) => a - b);

  for (const week of sortedWeeks) {
    const entries = roadmap.weeklyPlan[week];
    lines.push(`### Week ${week}`, "");

    for (const entry of entries) {
      const emoji = tierEmojis[entry.tier] || "•";
      lines.push(`- ${emoji} **#${entry.prNumber}** - ${entry.title} (${entry.priority}/100)`);
    }
    lines.push("");
  }

  if (roadmap.blockedPRs.length > 0) {
    lines.push("---", "", "## 🚫 Blocked PRs", "");
    lines.push(
      "These PRs are waiting on external dependencies:",
      ""
    );

    for (const entry of roadmap.blockedPRs) {
      lines.push(
        `- **#${entry.prNumber}** - ${entry.title}`,
        `  - Blocked by: ${entry.blockedBy.map((n) => `#${n}`).join(", ")}`
      );
    }
  }

  lines.push(
    "",
    "---",
    "",
    "*This roadmap is auto-generated by the Priority Council.*",
    "",
    "*For her. Always.*"
  );

  return lines.join("\n");
}

/**
 * Format roadmap for Discord embed
 */
export function formatRoadmapEmbed(roadmap: Roadmap): {
  title: string;
  description: string;
  color: number;
  fields: Array<{ name: string; value: string; inline: boolean }>;
} {
  const fields: Array<{ name: string; value: string; inline: boolean }> = [
    {
      name: "📊 Total PRs",
      value: `${roadmap.totalPRs}`,
      inline: true,
    },
    {
      name: "🚨 Critical",
      value: `${roadmap.criticalCount}`,
      inline: true,
    },
    {
      name: "⏱️ Est. Completion",
      value: `${roadmap.stats.estimatedCompletionWeeks} weeks`,
      inline: true,
    },
  ];

  // Add top 5 from critical path
  if (roadmap.criticalPath.length > 0) {
    const pathSummary = roadmap.criticalPath
      .slice(0, 5)
      .map((e) => `• #${e.prNumber} (${e.priority})`)
      .join("\n");
    fields.push({
      name: "🎯 Critical Path (Top 5)",
      value: pathSummary || "None",
      inline: false,
    });
  }

  // Week 1 summary
  const week1 = roadmap.weeklyPlan[1];
  if (week1 && week1.length > 0) {
    const week1Summary = week1.map((e) => `• #${e.prNumber}`).join("\n");
    fields.push({
      name: "📅 This Week",
      value: week1Summary,
      inline: false,
    });
  }

  return {
    title: "🗺️ Priority Council Roadmap",
    description: `Generated: ${new Date(roadmap.generatedAt).toLocaleDateString()}`,
    color: 0x309919, // Teal
    fields,
  };
}
