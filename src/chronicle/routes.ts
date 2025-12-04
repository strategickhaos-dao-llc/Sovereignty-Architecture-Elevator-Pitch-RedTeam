/**
 * Sovereign Architect's Chronicle - API Routes
 * 
 * Express routes for managing chronicle entries and generating
 * timeline/roadmap views for the Sovereign Control Deck.
 */

import type { Request, Response, Router } from "express";
import { getChronicleStore } from "./store.js";
import type { ChronicleCategory, ChronicleStatus } from "./types.js";
import { CATEGORY_METADATA, STATUS_METADATA } from "./types.js";

/**
 * Create chronicle routes for the event gateway
 */
export function createChronicleRoutes(router: Router): Router {
  const store = getChronicleStore();
  
  // ========================================
  // TIMELINE & ROADMAP VIEWS
  // ========================================
  
  /**
   * GET /chronicle/timeline
   * Get the full timeline view grouped by category
   */
  router.get("/chronicle/timeline", (_req: Request, res: Response) => {
    try {
      const timeline = store.generateTimeline();
      res.json(timeline);
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to generate timeline", message });
    }
  });
  
  /**
   * GET /chronicle/roadmap
   * Get the roadmap view organized by development phase
   */
  router.get("/chronicle/roadmap", (_req: Request, res: Response) => {
    try {
      const roadmap = store.generateRoadmap();
      res.json(roadmap);
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to generate roadmap", message });
    }
  });
  
  /**
   * GET /chronicle/stats
   * Get statistics about the chronicle
   */
  router.get("/chronicle/stats", (_req: Request, res: Response) => {
    try {
      const stats = store.getStats();
      res.json(stats);
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to get stats", message });
    }
  });
  
  // ========================================
  // ENTRY CRUD OPERATIONS
  // ========================================
  
  /**
   * GET /chronicle/entries
   * List all entries with optional filters
   */
  router.get("/chronicle/entries", (req: Request, res: Response) => {
    try {
      const categories = req.query.categories 
        ? (req.query.categories as string).split(",") as ChronicleCategory[]
        : undefined;
      const statuses = req.query.statuses
        ? (req.query.statuses as string).split(",") as ChronicleStatus[]
        : undefined;
      const limit = req.query.limit 
        ? parseInt(req.query.limit as string, 10) 
        : undefined;
      
      const entries = store.getSummaries({ categories, statuses, limit });
      res.json({ entries, count: entries.length });
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to list entries", message });
    }
  });
  
  /**
   * GET /chronicle/entries/:id
   * Get a specific entry by ID
   */
  router.get("/chronicle/entries/:id", (req: Request, res: Response) => {
    try {
      const entry = store.getEntry(req.params.id);
      if (!entry) {
        res.status(404).json({ error: "Entry not found" });
        return;
      }
      res.json(entry);
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to get entry", message });
    }
  });
  
  /**
   * POST /chronicle/entries
   * Create a new chronicle entry
   */
  router.post("/chronicle/entries", (req: Request, res: Response) => {
    try {
      const { title, description, category, status, source, sourceRef, author, tags, priority, complexity, dependencies, notes } = req.body;
      
      if (!title || !description || !category || !author) {
        res.status(400).json({ 
          error: "Missing required fields", 
          required: ["title", "description", "category", "author"] 
        });
        return;
      }
      
      const entry = store.createEntry({
        title,
        description,
        category,
        status: status || "ideation",
        source: source || "api",
        sourceRef,
        author,
        tags: tags || [],
        priority,
        complexity,
        dependencies,
        notes
      });
      
      res.status(201).json(entry);
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to create entry", message });
    }
  });
  
  /**
   * PATCH /chronicle/entries/:id
   * Update an existing entry
   */
  router.patch("/chronicle/entries/:id", (req: Request, res: Response) => {
    try {
      const entry = store.updateEntry(req.params.id, req.body);
      if (!entry) {
        res.status(404).json({ error: "Entry not found" });
        return;
      }
      res.json(entry);
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to update entry", message });
    }
  });
  
  /**
   * DELETE /chronicle/entries/:id
   * Delete an entry
   */
  router.delete("/chronicle/entries/:id", (req: Request, res: Response) => {
    try {
      const success = store.deleteEntry(req.params.id);
      if (!success) {
        res.status(404).json({ error: "Entry not found" });
        return;
      }
      res.json({ success: true, message: "Entry deleted" });
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to delete entry", message });
    }
  });
  
  /**
   * GET /chronicle/search
   * Search entries by query
   */
  router.get("/chronicle/search", (req: Request, res: Response) => {
    try {
      const query = req.query.q as string;
      if (!query) {
        res.status(400).json({ error: "Missing search query parameter 'q'" });
        return;
      }
      const entries = store.search(query);
      res.json({ entries, count: entries.length, query });
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to search entries", message });
    }
  });
  
  // ========================================
  // CATEGORY VIEWS
  // ========================================
  
  /**
   * GET /chronicle/categories
   * Get all available categories with metadata
   */
  router.get("/chronicle/categories", (_req: Request, res: Response) => {
    const stats = store.getStats();
    const categories = Object.entries(CATEGORY_METADATA).map(([key, meta]) => ({
      id: key,
      ...meta,
      entryCount: stats.byCategory[key] || 0
    }));
    res.json({ categories });
  });
  
  /**
   * GET /chronicle/categories/:category
   * Get entries for a specific category
   */
  router.get("/chronicle/categories/:category", (req: Request, res: Response) => {
    try {
      const category = req.params.category as ChronicleCategory;
      if (!CATEGORY_METADATA[category]) {
        res.status(400).json({ error: "Invalid category", validCategories: Object.keys(CATEGORY_METADATA) });
        return;
      }
      
      const entries = store.getByCategory(category);
      const meta = CATEGORY_METADATA[category];
      
      res.json({
        category,
        ...meta,
        entries,
        count: entries.length
      });
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unknown error";
      res.status(500).json({ error: "Failed to get category entries", message });
    }
  });
  
  // ========================================
  // STATUS VIEWS
  // ========================================
  
  /**
   * GET /chronicle/statuses
   * Get all available statuses with metadata
   */
  router.get("/chronicle/statuses", (_req: Request, res: Response) => {
    const stats = store.getStats();
    const statuses = Object.entries(STATUS_METADATA).map(([key, meta]) => ({
      id: key,
      ...meta,
      entryCount: stats.byStatus[key] || 0
    }));
    res.json({ statuses });
  });
  
  return router;
}
