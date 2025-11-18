/**
 * Patent Scanner - Autonomous patent scanning and monitoring
 * Scans patent databases for relevant patents and potential threats
 */

import { EventEmitter } from 'events';

export interface PatentDatabase {
  name: string;
  endpoint: string;
  apiKey?: string;
  rateLimit: number;
}

export interface Patent {
  id: string;
  database: string;
  patent_number: string;
  title: string;
  abstract: string;
  inventors: string[];
  assignee?: string;
  filing_date: Date;
  grant_date?: Date;
  status: 'pending' | 'granted' | 'expired' | 'abandoned';
  classifications: string[];
  claims?: string[];
  url: string;
}

export interface ScanResult {
  scan_id: string;
  timestamp: Date;
  database: string;
  query: string;
  patents_found: number;
  patents: Patent[];
  priority_alerts: number;
  processing_time_ms: number;
}

export interface ScanQuery {
  keywords: string[];
  classifications?: string[];
  date_range?: {
    start: Date;
    end: Date;
  };
  databases: string[];
  result_limit?: number;
}

export class PatentScanner extends EventEmitter {
  private databases: Map<string, PatentDatabase>;
  private scanHistory: Map<string, ScanResult>;
  private alertThreshold: number;

  constructor(alertThreshold: number = 0.75) {
    super();
    this.databases = new Map();
    this.scanHistory = new Map();
    this.alertThreshold = alertThreshold;
  }

  /**
   * Register a patent database
   */
  registerDatabase(db: PatentDatabase): void {
    this.databases.set(db.name, db);
    console.log(`Registered patent database: ${db.name}`);
  }

  /**
   * Execute a patent scan
   */
  async scan(query: ScanQuery): Promise<ScanResult[]> {
    const startTime = Date.now();
    const results: ScanResult[] = [];

    console.log(`Starting patent scan for keywords: ${query.keywords.join(', ')}`);
    
    for (const dbName of query.databases) {
      const db = this.databases.get(dbName);
      if (!db) {
        console.warn(`Database ${dbName} not registered, skipping`);
        continue;
      }

      try {
        const result = await this.scanDatabase(db, query);
        results.push(result);
        
        // Store in history
        this.scanHistory.set(result.scan_id, result);
        
        // Emit events for high-priority findings
        if (result.priority_alerts > 0) {
          this.emit('priority_alert', {
            database: dbName,
            count: result.priority_alerts,
            scan_id: result.scan_id,
          });
        }
        
        // Respect rate limits
        await this.delay(60000 / db.rateLimit);
        
      } catch (error) {
        console.error(`Error scanning ${dbName}:`, error);
        this.emit('scan_error', {
          database: dbName,
          error: error instanceof Error ? error.message : 'Unknown error',
        });
      }
    }

    const totalTime = Date.now() - startTime;
    console.log(`Scan completed in ${totalTime}ms. Total patents found: ${results.reduce((sum, r) => sum + r.patents_found, 0)}`);
    
    this.emit('scan_complete', {
      total_databases: results.length,
      total_patents: results.reduce((sum, r) => sum + r.patents_found, 0),
      priority_alerts: results.reduce((sum, r) => sum + r.priority_alerts, 0),
      duration_ms: totalTime,
    });

    return results;
  }

  /**
   * Scan a specific database
   */
  private async scanDatabase(
    db: PatentDatabase,
    query: ScanQuery
  ): Promise<ScanResult> {
    const scanId = this.generateScanId(db.name);
    const startTime = Date.now();
    
    console.log(`Scanning ${db.name}...`);

    // Build search query string
    const searchQuery = this.buildSearchQuery(query);
    
    // Simulate API call (in production, this would call the actual API)
    const patents = await this.fetchPatents(db, searchQuery, query);
    
    // Analyze patents for priority
    const priorityCount = this.analyzePriority(patents);
    
    const result: ScanResult = {
      scan_id: scanId,
      timestamp: new Date(),
      database: db.name,
      query: searchQuery,
      patents_found: patents.length,
      patents: patents,
      priority_alerts: priorityCount,
      processing_time_ms: Date.now() - startTime,
    };

    return result;
  }

  /**
   * Build search query string from query parameters
   */
  private buildSearchQuery(query: ScanQuery): string {
    const parts: string[] = [];
    
    // Keywords
    if (query.keywords.length > 0) {
      parts.push(`(${query.keywords.map(k => `"${k}"`).join(' OR ')})`);
    }
    
    // Classifications
    if (query.classifications && query.classifications.length > 0) {
      parts.push(`CPC:(${query.classifications.join(' OR ')})`);
    }
    
    // Date range
    if (query.date_range) {
      const start = query.date_range.start.toISOString().split('T')[0];
      const end = query.date_range.end.toISOString().split('T')[0];
      parts.push(`PD:[${start} TO ${end}]`);
    }
    
    return parts.join(' AND ');
  }

  /**
   * Fetch patents from database API
   */
  private async fetchPatents(
    db: PatentDatabase,
    query: string,
    params: ScanQuery
  ): Promise<Patent[]> {
    // In production, this would make actual API calls
    // For now, return mock data
    
    console.log(`Fetching patents from ${db.name} with query: ${query}`);
    
    // Simulate API delay
    await this.delay(1000);
    
    // Generate mock patents for demonstration
    const mockPatents: Patent[] = [];
    const patentCount = Math.floor(Math.random() * 10) + 1;
    
    for (let i = 0; i < patentCount; i++) {
      mockPatents.push({
        id: `${db.name}_${Date.now()}_${i}`,
        database: db.name,
        patent_number: `US${Math.floor(Math.random() * 10000000)}B2`,
        title: `Patent related to ${params.keywords[0] || 'technology'}`,
        abstract: `This invention relates to ${params.keywords.join(', ')}...`,
        inventors: ['Inventor A', 'Inventor B'],
        assignee: 'Tech Company Inc.',
        filing_date: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000),
        grant_date: new Date(Date.now() - Math.random() * 180 * 24 * 60 * 60 * 1000),
        status: 'granted',
        classifications: params.classifications || ['G06F 16/00'],
        url: `${db.endpoint}/patents/${i}`,
      });
    }
    
    return mockPatents;
  }

  /**
   * Analyze patents to determine priority
   */
  private analyzePriority(patents: Patent[]): number {
    let priorityCount = 0;
    
    for (const patent of patents) {
      // Simple priority detection based on recency and status
      const daysSinceGrant = patent.grant_date
        ? (Date.now() - patent.grant_date.getTime()) / (1000 * 60 * 60 * 24)
        : Infinity;
      
      if (patent.status === 'granted' && daysSinceGrant < 90) {
        priorityCount++;
      }
    }
    
    return priorityCount;
  }

  /**
   * Get scan history
   */
  getScanHistory(limit?: number): ScanResult[] {
    const history = Array.from(this.scanHistory.values());
    history.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
    return limit ? history.slice(0, limit) : history;
  }

  /**
   * Get scan by ID
   */
  getScan(scanId: string): ScanResult | undefined {
    return this.scanHistory.get(scanId);
  }

  /**
   * Get statistics
   */
  getStats(): {
    total_scans: number;
    total_patents_found: number;
    total_priority_alerts: number;
    databases_registered: number;
    most_recent_scan?: Date;
  } {
    const scans = Array.from(this.scanHistory.values());
    
    return {
      total_scans: scans.length,
      total_patents_found: scans.reduce((sum, s) => sum + s.patents_found, 0),
      total_priority_alerts: scans.reduce((sum, s) => sum + s.priority_alerts, 0),
      databases_registered: this.databases.size,
      most_recent_scan: scans.length > 0 
        ? scans.reduce((latest, s) => s.timestamp > latest ? s.timestamp : latest, scans[0].timestamp)
        : undefined,
    };
  }

  /**
   * Schedule autonomous scanning
   */
  scheduleAutonomousScan(
    query: ScanQuery,
    intervalMs: number
  ): NodeJS.Timeout {
    console.log(`Scheduling autonomous scan every ${intervalMs}ms`);
    
    // Run initial scan
    this.scan(query).catch(err => {
      console.error('Autonomous scan error:', err);
    });
    
    // Schedule periodic scans
    return setInterval(() => {
      this.scan(query).catch(err => {
        console.error('Autonomous scan error:', err);
      });
    }, intervalMs);
  }

  // Helper methods

  private generateScanId(database: string): string {
    return `scan_${database}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export default PatentScanner;
