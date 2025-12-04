// src/chess-collider/bibliography.ts
// Bibliographic Data Mining Interface for Chess Collider
// Scrapes Google Scholar, arXiv, PubMed, Semantic Scholar, and government databases

import fetch from 'node-fetch';

// =============================================================================
// TYPES
// =============================================================================

export interface SearchParams {
  query: string;
  sources: BibliographySource[];
  maxResults?: number;
  dateFrom?: string;
  dateTo?: string;
  categories?: string[];
}

export type BibliographySource = 
  | 'google_scholar' 
  | 'arxiv' 
  | 'pubmed' 
  | 'semantic_scholar' 
  | 'gov_databases'
  | 'data_gov'
  | 'grants_gov';

export interface BibliographyResult {
  id: string;
  source: BibliographySource;
  title: string;
  authors: string[];
  abstract?: string;
  year?: number;
  url?: string;
  doi?: string;
  citations?: number;
  categories?: string[];
  pdfUrl?: string;
  relevanceScore?: number;
}

export interface ArxivEntry {
  id: string;
  title: string;
  summary: string;
  authors: { name: string }[];
  published: string;
  updated: string;
  links: { href: string; type: string }[];
  categories: string[];
}

// =============================================================================
// BIBLIOGRAPHY CLIENT
// =============================================================================

export class BibliographyClient {
  private rateLimits: Map<BibliographySource, { rpm: number; lastRequest: number }> = new Map();
  private arxivEndpoint = 'https://export.arxiv.org/api/query';
  private semanticScholarEndpoint = 'https://api.semanticscholar.org/graph/v1';
  private pubmedEndpoint = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils';

  constructor() {
    // Initialize rate limits
    this.rateLimits.set('google_scholar', { rpm: 60, lastRequest: 0 });
    this.rateLimits.set('arxiv', { rpm: 3, lastRequest: 0 });  // arXiv is very rate-limited
    this.rateLimits.set('pubmed', { rpm: 3, lastRequest: 0 });
    this.rateLimits.set('semantic_scholar', { rpm: 100, lastRequest: 0 });
    this.rateLimits.set('gov_databases', { rpm: 30, lastRequest: 0 });
  }

  async search(params: SearchParams): Promise<BibliographyResult[]> {
    const { query, sources, maxResults = 20 } = params;
    const results: BibliographyResult[] = [];

    // Search each source in parallel
    const searches = sources.map(async (source) => {
      try {
        await this.waitForRateLimit(source);
        const sourceResults = await this.searchSource(source, params);
        return sourceResults.slice(0, Math.ceil(maxResults / sources.length));
      } catch (error) {
        console.error(`Error searching ${source}:`, error);
        return [];
      }
    });

    const allResults = await Promise.all(searches);
    
    // Flatten and deduplicate
    for (const sourceResults of allResults) {
      for (const result of sourceResults) {
        // Simple deduplication by title similarity
        const isDuplicate = results.some(r => 
          this.calculateTitleSimilarity(r.title, result.title) > 0.9
        );
        if (!isDuplicate) {
          results.push(result);
        }
      }
    }

    // Sort by relevance score
    results.sort((a, b) => (b.relevanceScore || 0) - (a.relevanceScore || 0));

    return results.slice(0, maxResults);
  }

  private async searchSource(source: BibliographySource, params: SearchParams): Promise<BibliographyResult[]> {
    switch (source) {
      case 'arxiv':
        return this.searchArxiv(params);
      case 'semantic_scholar':
        return this.searchSemanticScholar(params);
      case 'pubmed':
        return this.searchPubMed(params);
      case 'google_scholar':
        return this.searchGoogleScholar(params);
      case 'gov_databases':
      case 'data_gov':
      case 'grants_gov':
        return this.searchGovDatabases(params);
      default:
        return [];
    }
  }

  // =============================================================================
  // ARXIV SEARCH
  // =============================================================================

  private async searchArxiv(params: SearchParams): Promise<BibliographyResult[]> {
    const { query, maxResults = 20, categories = [] } = params;

    // Build arXiv query
    let searchQuery = `all:${encodeURIComponent(query)}`;
    
    if (categories.length > 0) {
      const catQuery = categories.map(c => `cat:${c}`).join('+OR+');
      searchQuery = `(${searchQuery})+AND+(${catQuery})`;
    }

    const url = `${this.arxivEndpoint}?search_query=${searchQuery}&start=0&max_results=${maxResults}&sortBy=relevance&sortOrder=descending`;

    try {
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'ChessCollider/1.0 (Academic Research Tool)'
        }
      });

      if (!response.ok) {
        throw new Error(`arXiv API error: ${response.status}`);
      }

      const xml = await response.text();
      return this.parseArxivResponse(xml);
    } catch (error) {
      console.error('arXiv search error:', error);
      return [];
    }
  }

  private parseArxivResponse(xml: string): BibliographyResult[] {
    const results: BibliographyResult[] = [];
    
    // Simple XML parsing (in production, use a proper XML parser)
    const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
    let match;

    while ((match = entryRegex.exec(xml)) !== null) {
      const entry = match[1];
      
      const id = this.extractXmlTag(entry, 'id')?.replace('http://arxiv.org/abs/', '') || '';
      const title = this.extractXmlTag(entry, 'title')?.replace(/\s+/g, ' ').trim() || '';
      const summary = this.extractXmlTag(entry, 'summary')?.replace(/\s+/g, ' ').trim() || '';
      const published = this.extractXmlTag(entry, 'published') || '';
      
      // Extract authors
      const authors: string[] = [];
      const authorRegex = /<author>\s*<name>(.*?)<\/name>\s*<\/author>/g;
      let authorMatch;
      while ((authorMatch = authorRegex.exec(entry)) !== null) {
        authors.push(authorMatch[1]);
      }

      // Extract categories
      const categories: string[] = [];
      const catRegex = /<category[^>]*term="([^"]+)"/g;
      let catMatch;
      while ((catMatch = catRegex.exec(entry)) !== null) {
        categories.push(catMatch[1]);
      }

      // Extract PDF link
      const pdfMatch = entry.match(/<link[^>]*title="pdf"[^>]*href="([^"]+)"/);
      const pdfUrl = pdfMatch ? pdfMatch[1] : undefined;

      results.push({
        id: `arxiv:${id}`,
        source: 'arxiv',
        title,
        authors,
        abstract: summary,
        year: published ? new Date(published).getFullYear() : undefined,
        url: `https://arxiv.org/abs/${id}`,
        categories,
        pdfUrl,
        relevanceScore: 0.8  // Base score for arXiv
      });
    }

    return results;
  }

  // =============================================================================
  // SEMANTIC SCHOLAR SEARCH
  // =============================================================================

  private async searchSemanticScholar(params: SearchParams): Promise<BibliographyResult[]> {
    const { query, maxResults = 20 } = params;

    const url = `${this.semanticScholarEndpoint}/paper/search?query=${encodeURIComponent(query)}&limit=${maxResults}&fields=paperId,title,abstract,authors,year,citationCount,url,openAccessPdf`;

    try {
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'ChessCollider/1.0 (Academic Research Tool)'
        }
      });

      if (!response.ok) {
        throw new Error(`Semantic Scholar API error: ${response.status}`);
      }

      const data = await response.json() as { data: any[] };
      
      return data.data.map(paper => ({
        id: `s2:${paper.paperId}`,
        source: 'semantic_scholar' as BibliographySource,
        title: paper.title || '',
        authors: paper.authors?.map((a: any) => a.name) || [],
        abstract: paper.abstract || undefined,
        year: paper.year || undefined,
        url: paper.url || `https://www.semanticscholar.org/paper/${paper.paperId}`,
        citations: paper.citationCount || 0,
        pdfUrl: paper.openAccessPdf?.url || undefined,
        relevanceScore: Math.min(1, 0.5 + (paper.citationCount || 0) / 1000)
      }));
    } catch (error) {
      console.error('Semantic Scholar search error:', error);
      return [];
    }
  }

  // =============================================================================
  // PUBMED SEARCH
  // =============================================================================

  private async searchPubMed(params: SearchParams): Promise<BibliographyResult[]> {
    const { query, maxResults = 20 } = params;

    try {
      // First, search for IDs
      const searchUrl = `${this.pubmedEndpoint}/esearch.fcgi?db=pubmed&term=${encodeURIComponent(query)}&retmax=${maxResults}&retmode=json`;
      const searchResponse = await fetch(searchUrl);
      
      if (!searchResponse.ok) {
        throw new Error(`PubMed search error: ${searchResponse.status}`);
      }

      const searchData = await searchResponse.json() as { esearchresult: { idlist: string[] } };
      const ids = searchData.esearchresult.idlist || [];

      if (ids.length === 0) {
        return [];
      }

      // Fetch details for each ID
      const fetchUrl = `${this.pubmedEndpoint}/esummary.fcgi?db=pubmed&id=${ids.join(',')}&retmode=json`;
      const fetchResponse = await fetch(fetchUrl);

      if (!fetchResponse.ok) {
        throw new Error(`PubMed fetch error: ${fetchResponse.status}`);
      }

      const fetchData = await fetchResponse.json() as { result: { [key: string]: any } };
      const results: BibliographyResult[] = [];

      for (const id of ids) {
        const article = fetchData.result[id];
        if (!article || article.error) continue;

        results.push({
          id: `pubmed:${id}`,
          source: 'pubmed',
          title: article.title || '',
          authors: article.authors?.map((a: any) => a.name) || [],
          abstract: undefined,  // Summary endpoint doesn't include abstract
          year: article.pubdate ? parseInt(article.pubdate.split(' ')[0]) : undefined,
          url: `https://pubmed.ncbi.nlm.nih.gov/${id}/`,
          doi: article.elocationid?.replace('doi: ', '') || undefined,
          relevanceScore: 0.75
        });
      }

      return results;
    } catch (error) {
      console.error('PubMed search error:', error);
      return [];
    }
  }

  // =============================================================================
  // GOOGLE SCHOLAR SEARCH (Limited - requires careful handling)
  // =============================================================================

  private async searchGoogleScholar(params: SearchParams): Promise<BibliographyResult[]> {
    // Note: Google Scholar doesn't have an official API
    // In production, you would use a service like SerpAPI or similar
    // For now, return empty results with a note
    console.log('Google Scholar: Using placeholder - requires SerpAPI or similar service');
    
    return [{
      id: 'gs:placeholder',
      source: 'google_scholar',
      title: `[Google Scholar results for: ${params.query}]`,
      authors: [],
      abstract: 'Google Scholar requires a third-party API service (e.g., SerpAPI) for programmatic access.',
      relevanceScore: 0
    }];
  }

  // =============================================================================
  // GOVERNMENT DATABASES SEARCH
  // =============================================================================

  private async searchGovDatabases(params: SearchParams): Promise<BibliographyResult[]> {
    const { query, maxResults = 20 } = params;
    const results: BibliographyResult[] = [];

    // Data.gov search
    try {
      const dataGovUrl = `https://catalog.data.gov/api/3/action/package_search?q=${encodeURIComponent(query)}&rows=${maxResults}`;
      const response = await fetch(dataGovUrl);
      
      if (response.ok) {
        const data = await response.json() as { result: { results: any[] } };
        
        for (const dataset of data.result.results || []) {
          results.push({
            id: `datagov:${dataset.id}`,
            source: 'gov_databases',
            title: dataset.title || '',
            authors: dataset.organization?.title ? [dataset.organization.title] : [],
            abstract: dataset.notes || undefined,
            url: `https://catalog.data.gov/dataset/${dataset.name}`,
            categories: dataset.tags?.map((t: any) => t.name) || [],
            relevanceScore: 0.6
          });
        }
      }
    } catch (error) {
      console.error('Data.gov search error:', error);
    }

    return results;
  }

  // =============================================================================
  // HELPER METHODS
  // =============================================================================

  private async waitForRateLimit(source: BibliographySource): Promise<void> {
    const limits = this.rateLimits.get(source);
    if (!limits) return;

    const minInterval = (60 * 1000) / limits.rpm;  // ms per request
    const timeSinceLastRequest = Date.now() - limits.lastRequest;

    if (timeSinceLastRequest < minInterval) {
      await new Promise(resolve => setTimeout(resolve, minInterval - timeSinceLastRequest));
    }

    limits.lastRequest = Date.now();
  }

  private extractXmlTag(xml: string, tag: string): string | null {
    const match = xml.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`));
    return match ? match[1] : null;
  }

  private calculateTitleSimilarity(title1: string, title2: string): number {
    // Simple Jaccard similarity on words
    const words1 = new Set(title1.toLowerCase().split(/\W+/).filter(w => w.length > 2));
    const words2 = new Set(title2.toLowerCase().split(/\W+/).filter(w => w.length > 2));
    
    const intersection = new Set([...words1].filter(x => words2.has(x)));
    const union = new Set([...words1, ...words2]);
    
    return union.size > 0 ? intersection.size / union.size : 0;
  }

  // =============================================================================
  // CITATION EXTRACTION
  // =============================================================================

  async extractCitations(result: BibliographyResult): Promise<string[]> {
    const citations: string[] = [];

    // Format as academic citation
    const authorList = result.authors.length > 3 
      ? `${result.authors[0]} et al.`
      : result.authors.join(', ');

    citations.push(`${authorList} (${result.year || 'n.d.'}). ${result.title}. ${result.doi ? `DOI: ${result.doi}` : result.url || ''}`);

    return citations;
  }

  // =============================================================================
  // BULK OPERATIONS
  // =============================================================================

  async batchSearch(queries: string[], sources: BibliographySource[]): Promise<Map<string, BibliographyResult[]>> {
    const results = new Map<string, BibliographyResult[]>();

    // Process in batches to respect rate limits
    for (const query of queries) {
      const queryResults = await this.search({ query, sources, maxResults: 10 });
      results.set(query, queryResults);
      
      // Add delay between queries
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    return results;
  }

  // Get statistics about available sources
  getSourceStats(): { source: BibliographySource; rpm: number; status: string }[] {
    const stats: { source: BibliographySource; rpm: number; status: string }[] = [];
    
    for (const [source, limits] of this.rateLimits.entries()) {
      stats.push({
        source,
        rpm: limits.rpm,
        status: 'available'
      });
    }

    return stats;
  }
}

export default BibliographyClient;
