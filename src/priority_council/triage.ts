/**
 * Priority Council - PR Triage Handler
 * 
 * Handles automatic PR triage via GitHub webhooks.
 * Analyzes PRs, assigns priority labels, and posts to Discord.
 */

import type { Request, Response } from "express";
import crypto from "crypto";
import { REST } from "discord.js";
import {
  analyzePR,
  formatAnalysisEmbed,
  getPriorityLabel,
  type PRCategory,
} from "./scoring.js";

interface GitHubPRPayload {
  action: string;
  number: number;
  pull_request: {
    number: number;
    title: string;
    body: string | null;
    html_url: string;
    user: { login: string };
    base: { repo: { full_name: string } };
    head: { ref: string };
    labels: Array<{ name: string }>;
    created_at: string;
    changed_files: number;
    mergeable_state: string;
    mergeable: boolean | null;
  };
  repository: {
    full_name: string;
    owner: { login: string };
    name: string;
  };
}

interface TriageConfig {
  channelIds: {
    prs: string;
    priorityCouncil: string;
  };
  githubToken?: string;
  labelsEnabled: boolean;
  commentEnabled: boolean;
}

/**
 * Classify PR category based on title, description, and files
 */
export function classifyPRCategory(
  title: string,
  body: string | null,
  labels: string[]
): PRCategory {
  const text = `${title} ${body || ""}`.toLowerCase();
  const labelText = labels.join(" ").toLowerCase();

  // Medical/Drug Discovery keywords
  if (
    text.includes("medical") ||
    text.includes("drug") ||
    text.includes("cure") ||
    text.includes("treatment") ||
    text.includes("therapy") ||
    text.includes("disease") ||
    text.includes("diagnosis") ||
    labelText.includes("medical")
  ) {
    return "Medical/Drug Discovery";
  }

  // Research Tools keywords
  if (
    text.includes("research") ||
    text.includes("analysis") ||
    text.includes("data") ||
    text.includes("pipeline") ||
    text.includes("model") ||
    text.includes("ai") ||
    text.includes("ml") ||
    text.includes("quantum") ||
    labelText.includes("research")
  ) {
    return "Research Tools";
  }

  // Visualization keywords
  if (
    text.includes("visualization") ||
    text.includes("dashboard") ||
    text.includes("chart") ||
    text.includes("graph") ||
    text.includes("ui") ||
    text.includes("display") ||
    text.includes("mirror") ||
    labelText.includes("visualization")
  ) {
    return "Visualization";
  }

  // Bug Fix keywords
  if (
    text.includes("fix") ||
    text.includes("bug") ||
    text.includes("error") ||
    text.includes("issue") ||
    text.includes("broken") ||
    text.includes("crash") ||
    labelText.includes("bug")
  ) {
    return "Bug Fix";
  }

  // Documentation keywords
  if (
    text.includes("doc") ||
    text.includes("readme") ||
    text.includes("comment") ||
    text.includes("typo") ||
    text.includes("spelling") ||
    labelText.includes("documentation")
  ) {
    return "Documentation";
  }

  // Default to Infrastructure
  return "Infrastructure";
}

/**
 * Estimate complexity based on PR characteristics
 */
export function estimateComplexity(
  filesChanged: number,
  titleLength: number,
  bodyLength: number
): number {
  let complexity = 1;

  // Files changed
  if (filesChanged > 50) complexity += 5;
  else if (filesChanged > 20) complexity += 3;
  else if (filesChanged > 10) complexity += 2;
  else if (filesChanged > 5) complexity += 1;

  // Description length (longer = more complex typically)
  if (bodyLength > 2000) complexity += 2;
  else if (bodyLength > 500) complexity += 1;

  // Title complexity (longer titles often indicate more complex changes)
  if (titleLength > 100) complexity += 1;

  return Math.min(10, complexity);
}

/**
 * Estimate risk based on PR characteristics
 */
export function estimateRisk(
  category: PRCategory,
  filesChanged: number,
  mergeableState: string
): number {
  let risk = 1;

  // Higher risk for infrastructure changes
  if (category === "Infrastructure") risk += 2;

  // Higher risk for many file changes
  if (filesChanged > 30) risk += 3;
  else if (filesChanged > 15) risk += 2;
  else if (filesChanged > 5) risk += 1;

  // Merge conflicts indicate risk
  if (mergeableState === "dirty" || mergeableState === "unknown") {
    risk += 2;
  }

  return Math.min(10, risk);
}

/**
 * Calculate PR age in days
 */
export function calculatePRAge(createdAt: string): number {
  const created = new Date(createdAt);
  const now = new Date();
  const diffMs = now.getTime() - created.getTime();
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

/**
 * Extract dependencies from PR body
 */
export function extractDependencies(body: string | null): number[] {
  if (!body) return [];

  const deps: number[] = [];
  
  // Match patterns like "depends on #123", "blocked by #456", "requires #789"
  const patterns = [
    /depends on #(\d+)/gi,
    /blocked by #(\d+)/gi,
    /requires #(\d+)/gi,
    /after #(\d+)/gi,
    /needs #(\d+)/gi,
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(body)) !== null) {
      const prNum = parseInt(match[1], 10);
      if (!deps.includes(prNum)) {
        deps.push(prNum);
      }
    }
  }

  return deps;
}

/**
 * Extract blockers from PR body
 */
export function extractBlockers(body: string | null): string[] {
  if (!body) return [];

  const blockers: string[] = [];

  // Look for blocker sections
  const blockerMatch = body.match(/(?:blockers?|blocked by)[:\s]*([^\n]+)/gi);
  if (blockerMatch) {
    for (const match of blockerMatch) {
      const text = match
        .replace(/(?:blockers?|blocked by)[:\s]*/i, "")
        .trim();
      if (text && text.length > 0 && text.length < 200) {
        blockers.push(text);
      }
    }
  }

  return blockers;
}

/**
 * Verify GitHub webhook signature
 */
function verifySignature(secret: string, rawBody: string, signature: string): boolean {
  const hash = crypto.createHmac("sha256", secret).update(rawBody).digest("hex");
  return `sha256=${hash}` === signature;
}

/**
 * Create the PR triage webhook handler
 */
export function createTriageHandler(
  rest: REST,
  config: TriageConfig,
  webhookSecret: string
) {
  return async (req: Request, res: Response) => {
    const signature = req.get("X-Hub-Signature-256") || "";
    const rawBody = (req as unknown as { rawBody: string }).rawBody;

    if (!verifySignature(webhookSecret, rawBody, signature)) {
      return res.status(401).send("Invalid signature");
    }

    const event = req.get("X-GitHub-Event");
    
    // Only handle pull_request events
    if (event !== "pull_request") {
      return res.send("ok");
    }

    const payload = req.body as GitHubPRPayload;
    const { action, pull_request: pr, repository } = payload;

    // Only triage on open, reopened, or synchronize actions
    if (!["opened", "reopened", "synchronize", "ready_for_review"].includes(action)) {
      return res.send("ok");
    }

    try {
      // Classify the PR
      const labels = pr.labels.map((l) => l.name);
      const category = classifyPRCategory(pr.title, pr.body, labels);

      // Estimate scores
      const complexity = estimateComplexity(
        pr.changed_files,
        pr.title.length,
        (pr.body || "").length
      );
      const risk = estimateRisk(category, pr.changed_files, pr.mergeable_state);
      const prAge = calculatePRAge(pr.created_at);
      const dependencies = extractDependencies(pr.body);
      const blockers = extractBlockers(pr.body);

      // Perform analysis
      const analysis = analyzePR({
        prNumber: pr.number,
        title: pr.title,
        category,
        complexity,
        risk,
        dependenciesCount: dependencies.length,
        dependencies,
        blockers,
        urgencyFactors: {
          prAgeInDays: prAge,
          unblocksOtherWork: dependencies.length === 0 && blockers.length === 0,
        },
        ciPassing: true, // Default, updated by check_suite events
        hasMergeConflicts: pr.mergeable === false,
        filesChanged: pr.changed_files,
      });

      // Format embed
      const embed = formatAnalysisEmbed(analysis);
      const priorityLabel = getPriorityLabel(analysis.tier);

      // Post to Discord
      await rest.post(`/channels/${config.channelIds.priorityCouncil}/messages`, {
        body: {
          content: `📊 **Priority Analysis** for ${repository.full_name}`,
          embeds: [embed],
        },
      } as unknown as Record<string, unknown>);

      // Log for now (labels would require GitHub API calls)
      console.log(
        `[Priority Council] PR #${pr.number} analyzed:`,
        `Priority: ${analysis.finalPriority} (${analysis.tier})`,
        `Label: ${priorityLabel}`,
        `Auto-merge: ${analysis.autoMergeEligible}`
      );

      res.send("ok");
    } catch (error) {
      console.error("[Priority Council] Triage error:", error);
      res.status(500).send("Triage error");
    }
  };
}

/**
 * Format triage comment for GitHub PR
 */
export function formatTriageComment(
  analysis: ReturnType<typeof analyzePR>
): string {
  const tierEmojis = {
    critical: "🚨",
    high: "⚡",
    medium: "📊",
    low: "📝",
    backlog: "📦",
  };

  const emoji = tierEmojis[analysis.tier];

  return `## ${emoji} Priority Council Analysis

| Metric | Score |
|--------|-------|
| **Category** | ${analysis.category} |
| **Impact** | ${analysis.impactScore}/100 |
| **Urgency** | ${analysis.urgencyScore}/100 |
| **Feasibility** | ${analysis.feasibilityScore}/100 |
| **Final Priority** | **${analysis.finalPriority}/100** |
| **Tier** | ${analysis.tier.toUpperCase()} |
| **Risk** | ${analysis.riskLevel.toUpperCase()} |

### 🎯 Recommendation
${analysis.recommendation}

${
  analysis.autoMergeEligible
    ? "✅ **This PR is eligible for auto-merge**"
    : "⏳ This PR requires manual review"
}

${
  analysis.dependencies.length > 0
    ? `### 🔗 Dependencies\n${analysis.dependencies.map((d) => `- #${d}`).join("\n")}`
    : ""
}

${
  analysis.blockers.length > 0
    ? `### 🚫 Blockers\n${analysis.blockers.map((b) => `- ${b}`).join("\n")}`
    : ""
}

---
*Auto-generated by Priority Council • For her. Always.*`;
}
