// src/chess-collider/synthesis.ts
// Research Synthesis Module for Chess Collider
// Generates systematic reviews, research papers, and patent applications

import fetch from 'node-fetch';

// =============================================================================
// TYPES
// =============================================================================

export interface SynthesisParams {
  taskId: string;
  findings: ResearchFinding[];
  outputFormat: 'markdown' | 'latex' | 'json' | 'uspto_xml';
  includeAbstract?: boolean;
  includeMethodology?: boolean;
  targetAudience?: 'academic' | 'technical' | 'general';
}

export interface ResearchFinding {
  sourceLayer: number;
  agentId: string;
  content: string;
  confidence: number;
  citations: string[];
  timestamp: Date;
  category?: string;
  methodology?: string;
}

export interface SynthesisResult {
  id: string;
  format: string;
  content: string;
  wordCount: number;
  citations: string[];
  sections: SynthesisSection[];
  metadata: SynthesisMetadata;
  createdAt: Date;
}

export interface SynthesisSection {
  title: string;
  content: string;
  subsections?: SynthesisSection[];
  citations?: string[];
}

export interface SynthesisMetadata {
  title: string;
  authors: string[];
  abstract?: string;
  keywords: string[];
  methodology?: string;
  limitations?: string[];
  futureWork?: string[];
}

// =============================================================================
// RESEARCH SYNTHESIZER
// =============================================================================

export class ResearchSynthesizer {
  private ollamaUrl: string;
  private modelName: string;

  constructor() {
    this.ollamaUrl = process.env.OLLAMA_URL || 'http://localhost:11434';
    this.modelName = process.env.LLM_MODEL || 'llama3.2:latest';
  }

  async synthesize(params: SynthesisParams): Promise<SynthesisResult> {
    const { taskId, findings, outputFormat, includeAbstract = true, includeMethodology = true } = params;

    // Group findings by layer and category
    const groupedFindings = this.groupFindings(findings);

    // Extract all citations
    const allCitations = this.extractCitations(findings);

    // Generate synthesis sections
    const sections = await this.generateSections(groupedFindings, params);

    // Generate metadata
    const metadata = await this.generateMetadata(findings, sections);

    // Format output
    const content = this.formatOutput(sections, metadata, outputFormat);

    const result: SynthesisResult = {
      id: `synthesis-${taskId}-${Date.now()}`,
      format: outputFormat,
      content,
      wordCount: this.countWords(content),
      citations: allCitations,
      sections,
      metadata,
      createdAt: new Date()
    };

    return result;
  }

  // =============================================================================
  // FINDING ANALYSIS
  // =============================================================================

  private groupFindings(findings: ResearchFinding[]): Map<string, ResearchFinding[]> {
    const grouped = new Map<string, ResearchFinding[]>();

    for (const finding of findings) {
      const key = finding.category || `layer-${finding.sourceLayer}`;
      if (!grouped.has(key)) {
        grouped.set(key, []);
      }
      grouped.get(key)!.push(finding);
    }

    return grouped;
  }

  private extractCitations(findings: ResearchFinding[]): string[] {
    const citationSet = new Set<string>();
    
    for (const finding of findings) {
      for (const citation of finding.citations) {
        citationSet.add(citation);
      }
    }

    return Array.from(citationSet).sort();
  }

  // =============================================================================
  // SECTION GENERATION
  // =============================================================================

  private async generateSections(
    groupedFindings: Map<string, ResearchFinding[]>,
    params: SynthesisParams
  ): Promise<SynthesisSection[]> {
    const sections: SynthesisSection[] = [];

    // Introduction section
    sections.push({
      title: 'Introduction',
      content: await this.generateIntroduction(groupedFindings),
      citations: []
    });

    // Background/Literature Review section
    sections.push({
      title: 'Background',
      content: await this.generateBackground(groupedFindings),
      citations: this.getCitationsForSection(groupedFindings, ['layer-1', 'layer-2'])
    });

    // Methodology section (if requested)
    if (params.includeMethodology) {
      sections.push({
        title: 'Methodology',
        content: await this.generateMethodology(groupedFindings),
        citations: []
      });
    }

    // Main findings sections (one per category/layer)
    for (const [category, findings] of groupedFindings.entries()) {
      if (category.startsWith('layer-')) {
        const layerId = parseInt(category.replace('layer-', ''));
        sections.push({
          title: this.getLayerSectionTitle(layerId),
          content: await this.synthesizeFindings(findings),
          citations: findings.flatMap(f => f.citations)
        });
      }
    }

    // Discussion section
    sections.push({
      title: 'Discussion',
      content: await this.generateDiscussion(groupedFindings),
      citations: []
    });

    // Conclusion section
    sections.push({
      title: 'Conclusion',
      content: await this.generateConclusion(groupedFindings),
      citations: []
    });

    return sections;
  }

  private async generateIntroduction(groupedFindings: Map<string, ResearchFinding[]>): Promise<string> {
    const totalFindings = Array.from(groupedFindings.values()).flat().length;
    const layers = groupedFindings.size;

    // Try to use LLM for generation, fall back to template
    try {
      const prompt = `Generate an academic introduction paragraph for a systematic review. 
      The review synthesizes ${totalFindings} findings across ${layers} research domains.
      Keep it concise (2-3 paragraphs) and scholarly in tone.`;
      
      return await this.generateWithLLM(prompt);
    } catch {
      return `This systematic review presents a comprehensive synthesis of ${totalFindings} research findings ` +
        `collected across ${layers} distinct analytical domains. The multi-layered approach employed in this ` +
        `analysis leverages both automated data collection and adversarial peer review mechanisms to ensure ` +
        `robustness and validity of conclusions.\n\n` +
        `The following sections present our methodology, key findings organized by research domain, ` +
        `and a discussion of implications and future research directions.`;
    }
  }

  private async generateBackground(groupedFindings: Map<string, ResearchFinding[]>): Promise<string> {
    try {
      const findings = Array.from(groupedFindings.values()).flat();
      const sampleTopics = findings.slice(0, 5).map(f => f.content.slice(0, 100)).join('; ');
      
      const prompt = `Generate a background/literature review section for a research paper covering topics including: ${sampleTopics}
      Keep it scholarly and cite relevant prior work. 2-3 paragraphs.`;
      
      return await this.generateWithLLM(prompt);
    } catch {
      return `The research landscape addressed in this review spans multiple interconnected domains. ` +
        `Prior work has established foundational understanding in these areas, though significant gaps ` +
        `remain in synthesizing findings across disciplinary boundaries.\n\n` +
        `Our multi-layered analytical framework builds upon established methodologies while introducing ` +
        `novel adversarial validation mechanisms to strengthen the reliability of synthesized conclusions.`;
    }
  }

  private async generateMethodology(groupedFindings: Map<string, ResearchFinding[]>): Promise<string> {
    const layers = new Set(Array.from(groupedFindings.values()).flat().map(f => f.sourceLayer));
    
    return `**Data Collection**\n\n` +
      `Research findings were collected through automated bibliographic mining across multiple sources ` +
      `including arXiv, Semantic Scholar, PubMed, and government databases. A total of ${layers.size} ` +
      `analytical layers processed the data.\n\n` +
      `**Analysis Framework**\n\n` +
      `Each layer applied domain-specific analytical techniques:\n` +
      `- Layer 1 (Empirical Data): Raw data collection and initial processing\n` +
      `- Layer 2 (Pattern Recognition): Statistical pattern detection\n` +
      `- Layer 3 (Semantic Understanding): Natural language processing and interpretation\n` +
      `- Layer 4 (Logical Reasoning): Formal logical analysis and validation\n` +
      `- Layer 5+ (Higher Order): Hypothesis generation, peer review, and synthesis\n\n` +
      `**Validation**\n\n` +
      `Adversarial chess game protocols were employed between layers to validate findings, ` +
      `with Stockfish-refereed matches ensuring rigorous cross-validation of conclusions.`;
  }

  private async synthesizeFindings(findings: ResearchFinding[]): Promise<string> {
    if (findings.length === 0) {
      return 'No findings available for this section.';
    }

    // Sort by confidence
    const sortedFindings = [...findings].sort((a, b) => b.confidence - a.confidence);

    let content = '';
    
    for (let i = 0; i < Math.min(sortedFindings.length, 10); i++) {
      const finding = sortedFindings[i];
      const confidenceLabel = finding.confidence >= 0.8 ? 'High confidence' : 
        finding.confidence >= 0.5 ? 'Medium confidence' : 'Low confidence';
      
      content += `**Finding ${i + 1}** (${confidenceLabel}, Agent ${finding.agentId}):\n`;
      content += `${finding.content}\n\n`;
      
      if (finding.citations.length > 0) {
        content += `*Citations: ${finding.citations.slice(0, 3).join('; ')}*\n\n`;
      }
    }

    return content;
  }

  private async generateDiscussion(groupedFindings: Map<string, ResearchFinding[]>): Promise<string> {
    try {
      const findings = Array.from(groupedFindings.values()).flat();
      const avgConfidence = findings.reduce((sum, f) => sum + f.confidence, 0) / findings.length;
      
      const prompt = `Generate a discussion section for an academic paper. 
      The research synthesized ${findings.length} findings with average confidence ${(avgConfidence * 100).toFixed(1)}%.
      Discuss implications, limitations, and connections between findings. 2-3 paragraphs.`;
      
      return await this.generateWithLLM(prompt);
    } catch {
      return `The synthesized findings reveal several important patterns and insights. ` +
        `Cross-layer validation through adversarial protocols identified both areas of strong consensus ` +
        `and regions of productive disagreement warranting further investigation.\n\n` +
        `**Limitations**: This analysis is constrained by the availability and quality of source data, ` +
        `as well as the inherent limitations of automated synthesis. Human expert review remains essential ` +
        `for final validation of conclusions.\n\n` +
        `**Implications**: The multi-dimensional analytical approach demonstrates promise for accelerating ` +
        `systematic reviews while maintaining scholarly rigor through adversarial validation.`;
    }
  }

  private async generateConclusion(groupedFindings: Map<string, ResearchFinding[]>): Promise<string> {
    const totalFindings = Array.from(groupedFindings.values()).flat().length;
    
    return `This systematic review has synthesized ${totalFindings} research findings through a ` +
      `novel multi-dimensional analytical framework. Key contributions include:\n\n` +
      `1. Demonstration of adversarial validation protocols for research synthesis\n` +
      `2. Integration of automated bibliographic mining with expert-level analysis\n` +
      `3. Framework for scalable, reproducible systematic reviews\n\n` +
      `Future work should focus on expanding the analytical layer capabilities and improving ` +
      `inter-layer communication protocols for enhanced synthesis quality.`;
  }

  // =============================================================================
  // METADATA GENERATION
  // =============================================================================

  private async generateMetadata(
    findings: ResearchFinding[],
    sections: SynthesisSection[]
  ): Promise<SynthesisMetadata> {
    // Extract keywords from findings
    const keywords = this.extractKeywords(findings);

    // Generate title
    const title = await this.generateTitle(findings);

    // Generate abstract
    const abstract = await this.generateAbstract(sections);

    return {
      title,
      authors: ['Chess Collider Research Collective', 'Strategickhaos DAO LLC'],
      abstract,
      keywords,
      methodology: 'Multi-dimensional adversarial synthesis',
      limitations: [
        'Automated synthesis limitations',
        'Source data availability',
        'Cross-domain validation constraints'
      ],
      futureWork: [
        'Enhanced inter-layer protocols',
        'Extended bibliographic coverage',
        'Real-time collaboration features'
      ]
    };
  }

  private async generateTitle(findings: ResearchFinding[]): Promise<string> {
    // Extract main topics from findings
    const topics = findings.slice(0, 5).map(f => f.content.slice(0, 50));
    
    try {
      const prompt = `Generate a concise academic paper title (max 15 words) for a systematic review covering: ${topics.join('; ')}`;
      return await this.generateWithLLM(prompt);
    } catch {
      return 'A Systematic Review: Multi-Dimensional Synthesis of Research Findings';
    }
  }

  private async generateAbstract(sections: SynthesisSection[]): Promise<string> {
    const sectionSummary = sections.map(s => s.title).join(', ');
    
    return `**Background**: This systematic review employs a novel multi-dimensional analytical framework ` +
      `for synthesizing research findings across multiple domains.\n\n` +
      `**Methods**: Automated bibliographic mining combined with adversarial validation protocols ` +
      `across ${sections.length} analytical dimensions.\n\n` +
      `**Results**: The synthesis identified key patterns and generated actionable insights through ` +
      `cross-layer validation.\n\n` +
      `**Conclusions**: Multi-dimensional adversarial synthesis shows promise for accelerating ` +
      `systematic reviews while maintaining scholarly rigor.`;
  }

  private extractKeywords(findings: ResearchFinding[]): string[] {
    // Simple keyword extraction based on word frequency
    const wordCounts = new Map<string, number>();
    const stopWords = new Set(['the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'this', 'that', 'these', 'those', 'with', 'from', 'by', 'as', 'it', 'its']);

    for (const finding of findings) {
      const words = finding.content.toLowerCase().split(/\W+/);
      for (const word of words) {
        if (word.length > 4 && !stopWords.has(word)) {
          wordCounts.set(word, (wordCounts.get(word) || 0) + 1);
        }
      }
    }

    // Sort by frequency and take top keywords
    const sorted = Array.from(wordCounts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word]) => word);

    return sorted;
  }

  // =============================================================================
  // OUTPUT FORMATTING
  // =============================================================================

  private formatOutput(
    sections: SynthesisSection[],
    metadata: SynthesisMetadata,
    format: string
  ): string {
    switch (format) {
      case 'markdown':
        return this.formatMarkdown(sections, metadata);
      case 'latex':
        return this.formatLatex(sections, metadata);
      case 'json':
        return JSON.stringify({ metadata, sections }, null, 2);
      case 'uspto_xml':
        return this.formatUSPTOXml(sections, metadata);
      default:
        return this.formatMarkdown(sections, metadata);
    }
  }

  private formatMarkdown(sections: SynthesisSection[], metadata: SynthesisMetadata): string {
    let output = `# ${metadata.title}\n\n`;
    output += `**Authors**: ${metadata.authors.join(', ')}\n\n`;
    output += `**Keywords**: ${metadata.keywords.join(', ')}\n\n`;
    output += `---\n\n`;
    output += `## Abstract\n\n${metadata.abstract}\n\n`;
    output += `---\n\n`;

    for (const section of sections) {
      output += `## ${section.title}\n\n`;
      output += `${section.content}\n\n`;
      
      if (section.citations && section.citations.length > 0) {
        output += `*References: ${section.citations.slice(0, 5).join('; ')}*\n\n`;
      }
    }

    output += `---\n\n## References\n\n`;
    const allCitations = sections.flatMap(s => s.citations || []);
    const uniqueCitations = [...new Set(allCitations)];
    for (let i = 0; i < uniqueCitations.length; i++) {
      output += `[${i + 1}] ${uniqueCitations[i]}\n`;
    }

    return output;
  }

  private formatLatex(sections: SynthesisSection[], metadata: SynthesisMetadata): string {
    let output = `\\documentclass{article}\n`;
    output += `\\usepackage[utf8]{inputenc}\n`;
    output += `\\usepackage{hyperref}\n\n`;
    output += `\\title{${this.escapeLatex(metadata.title)}}\n`;
    output += `\\author{${metadata.authors.map(a => this.escapeLatex(a)).join(' \\and ')}}\n`;
    output += `\\date{\\today}\n\n`;
    output += `\\begin{document}\n\n`;
    output += `\\maketitle\n\n`;
    output += `\\begin{abstract}\n${this.escapeLatex(metadata.abstract || '')}\n\\end{abstract}\n\n`;
    output += `\\textbf{Keywords:} ${metadata.keywords.join(', ')}\n\n`;

    for (const section of sections) {
      output += `\\section{${this.escapeLatex(section.title)}}\n`;
      output += `${this.escapeLatex(section.content)}\n\n`;
    }

    output += `\\end{document}\n`;
    return output;
  }

  private formatUSPTOXml(sections: SynthesisSection[], metadata: SynthesisMetadata): string {
    return `<?xml version="1.0" encoding="UTF-8"?>
<us-patent-application>
  <us-bibliographic-data-application>
    <invention-title>${this.escapeXml(metadata.title)}</invention-title>
    <applicants>
      ${metadata.authors.map(a => `<applicant><name>${this.escapeXml(a)}</name></applicant>`).join('\n      ')}
    </applicants>
    <abstract>${this.escapeXml(metadata.abstract || '')}</abstract>
  </us-bibliographic-data-application>
  <description>
    ${sections.map(s => `<section title="${this.escapeXml(s.title)}">${this.escapeXml(s.content)}</section>`).join('\n    ')}
  </description>
</us-patent-application>`;
  }

  // =============================================================================
  // HELPERS
  // =============================================================================

  private getLayerSectionTitle(layerId: number): string {
    const titles: Record<number, string> = {
      1: 'Empirical Data Analysis',
      2: 'Pattern Recognition Results',
      3: 'Semantic Analysis',
      4: 'Logical Reasoning Findings',
      5: 'Generated Hypotheses',
      6: 'Experimental Design Considerations',
      7: 'Peer Review Analysis',
      8: 'Knowledge Synthesis',
      9: 'Publication Readiness Assessment',
      10: 'Strategic Research Directions'
    };
    return titles[layerId] || `Layer ${layerId} Findings`;
  }

  private getCitationsForSection(
    groupedFindings: Map<string, ResearchFinding[]>,
    categories: string[]
  ): string[] {
    const citations: string[] = [];
    for (const category of categories) {
      const findings = groupedFindings.get(category) || [];
      for (const finding of findings) {
        citations.push(...finding.citations);
      }
    }
    return [...new Set(citations)];
  }

  private countWords(text: string): number {
    return text.split(/\s+/).filter(word => word.length > 0).length;
  }

  private escapeLatex(text: string): string {
    return text
      .replace(/\\/g, '\\textbackslash{}')
      .replace(/[&%$#_{}]/g, '\\$&')
      .replace(/~/g, '\\textasciitilde{}')
      .replace(/\^/g, '\\textasciicircum{}');
  }

  private escapeXml(text: string): string {
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');
  }

  private async generateWithLLM(prompt: string): Promise<string> {
    try {
      const response = await fetch(`${this.ollamaUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: this.modelName,
          prompt,
          stream: false,
          options: {
            temperature: 0.7,
            num_predict: 500
          }
        })
      });

      if (!response.ok) {
        throw new Error(`LLM API error: ${response.status}`);
      }

      const data = await response.json() as { response: string };
      return data.response || '';
    } catch (error) {
      console.error('LLM generation error:', error);
      throw error;
    }
  }
}

export default ResearchSynthesizer;
