// src/chess-collider/bibliography-service.ts
// Bibliography Service - Standalone API for academic data mining
// Part of the Chess Collider 10-Dimensional AI Research Super-Collider
import express from 'express';
import { BibliographyClient } from './bibliography.js';
const app = express();
app.use(express.json());
const port = parseInt(process.env.BIBLIOGRAPHY_PORT || '8091');
const bibliographyClient = new BibliographyClient();
// Search cache (simple in-memory cache)
const searchCache = new Map();
const CACHE_TTL = 3600000; // 1 hour
// =============================================================================
// API ENDPOINTS
// =============================================================================
// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        sources: bibliographyClient.getSourceStats()
    });
});
// Search academic sources
app.post('/search', async (req, res) => {
    const { query, sources, maxResults, dateFrom, dateTo, categories, useCache } = req.body;
    if (!query) {
        return res.status(400).json({ error: 'Missing required field: query' });
    }
    // Check cache
    const cacheKey = JSON.stringify({ query, sources, maxResults, dateFrom, dateTo, categories });
    if (useCache !== false) {
        const cached = searchCache.get(cacheKey);
        if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
            return res.json({
                query,
                cached: true,
                resultsCount: cached.results.length,
                results: cached.results
            });
        }
    }
    try {
        const results = await bibliographyClient.search({
            query,
            sources: sources || ['arxiv', 'semantic_scholar'],
            maxResults: maxResults || 20,
            dateFrom,
            dateTo,
            categories
        });
        // Cache results
        searchCache.set(cacheKey, { results, timestamp: Date.now() });
        res.json({
            query,
            cached: false,
            resultsCount: results.length,
            results
        });
    }
    catch (error) {
        console.error('Search error:', error);
        res.status(500).json({ error: error.message });
    }
});
// Get specific paper by ID
app.get('/paper/:id', async (req, res) => {
    const { id } = req.params;
    // Parse source from ID prefix
    const [source] = id.split(':');
    // For now, search with ID as query (in production, would use direct API lookup)
    try {
        const results = await bibliographyClient.search({
            query: id,
            sources: [source || 'semantic_scholar'],
            maxResults: 1
        });
        if (results.length === 0) {
            return res.status(404).json({ error: 'Paper not found' });
        }
        res.json({ paper: results[0] });
    }
    catch (error) {
        res.status(500).json({ error: error.message });
    }
});
// Batch search
app.post('/batch-search', async (req, res) => {
    const { queries, sources } = req.body;
    if (!queries || !Array.isArray(queries)) {
        return res.status(400).json({ error: 'Missing required field: queries (array)' });
    }
    try {
        const batchResults = await bibliographyClient.batchSearch(queries, sources || ['arxiv', 'semantic_scholar']);
        const response = [];
        for (const [query, results] of batchResults.entries()) {
            response.push({
                query,
                resultsCount: results.length,
                results
            });
        }
        res.json({
            totalQueries: queries.length,
            batches: response
        });
    }
    catch (error) {
        res.status(500).json({ error: error.message });
    }
});
// Get source statistics
app.get('/sources', (req, res) => {
    res.json({
        sources: bibliographyClient.getSourceStats(),
        cacheSize: searchCache.size,
        cacheTTL: CACHE_TTL
    });
});
// Clear cache
app.post('/cache/clear', (req, res) => {
    searchCache.clear();
    res.json({ message: 'Cache cleared', timestamp: new Date().toISOString() });
});
// Metrics endpoint
app.get('/metrics', (req, res) => {
    const stats = bibliographyClient.getSourceStats();
    const metrics = `
# HELP bibliography_cache_size Number of cached search results
# TYPE bibliography_cache_size gauge
bibliography_cache_size ${searchCache.size}

# HELP bibliography_source_rpm Rate limit (requests per minute) by source
# TYPE bibliography_source_rpm gauge
${stats.map(s => `bibliography_source_rpm{source="${s.source}"} ${s.rpm}`).join('\n')}

# HELP bibliography_source_status Source availability status (1=available, 0=unavailable)
# TYPE bibliography_source_status gauge
${stats.map(s => `bibliography_source_status{source="${s.source}"} ${s.status === 'available' ? 1 : 0}`).join('\n')}
`;
    res.set('Content-Type', 'text/plain');
    res.send(metrics.trim());
});
// =============================================================================
// START SERVICE
// =============================================================================
app.listen(port, () => {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║           📚 BIBLIOGRAPHY SERVICE ONLINE 📚                   ║
╠═══════════════════════════════════════════════════════════════╣
║  Port: ${port}${' '.repeat(51)}║
║  Cache TTL: ${CACHE_TTL / 1000 / 60} minutes${' '.repeat(41)}║
║                                                               ║
║  Available Sources:                                           ║
║    • arXiv (3 rpm)                                            ║
║    • Semantic Scholar (100 rpm)                               ║
║    • PubMed (3 rpm)                                           ║
║    • Google Scholar (via SerpAPI)                             ║
║    • Data.gov (30 rpm)                                        ║
╚═══════════════════════════════════════════════════════════════╝
  `);
});
export { app };
