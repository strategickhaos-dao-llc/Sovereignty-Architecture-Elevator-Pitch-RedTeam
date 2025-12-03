/**
 * AI Pattern Detector
 * Flags generic ChatGPT/Claude patterns that lack authentic Dom voice
 */

export interface DetectionResult {
  isAIGenerated: boolean;
  confidence: number;
  flags: DetectionFlag[];
  score: number; // 0-100, higher = more AI-like
}

export interface DetectionFlag {
  type: string;
  description: string;
  severity: 'low' | 'medium' | 'high';
  examples: string[];
}

export class AIPatternDetector {
  // Generic AI assistant patterns
  private readonly genericAIPatterns = [
    /I apologize|I'm sorry/gi,
    /As an AI language model/gi,
    /I don't have personal/gi,
    /I'd be happy to help/gi,
    /Here's what I can tell you/gi,
    /Let me break this down/gi,
    /In summary|To summarize/gi,
    /It's important to note/gi,
    /However, it's worth noting/gi,
    /Please let me know if/gi,
    /I hope this helps/gi,
    /Feel free to/gi,
    /Don't hesitate to/gi,
  ];

  // Corporate/formal patterns that Dom doesn't use
  private readonly corporatePatterns = [
    /leverage|synergy|paradigm shift/gi,
    /circle back|touch base|reach out/gi,
    /moving forward|going forward/gi,
    /best practices/gi,
    /at this point in time/gi,
    /per se|as such/gi,
    /in order to/gi, // Dom uses "to" directly
    /utilize/gi, // Dom uses "use"
  ];

  // Over-structured list patterns
  private readonly overStructuredPatterns = [
    /^(?:\d+\.|[•\-*])\s+(?:[A-Z][^:]+:)/gm, // Numbered/bulleted lists with colons
    /^#+\s+(?:Introduction|Overview|Conclusion)/gm, // Generic headers
    /(?:Firstly|Secondly|Thirdly|Finally),/gi,
    /(?:Step \d+:|Phase \d+:)/gi,
  ];

  // Hedging/uncertainty that Dom doesn't exhibit
  private readonly hedgingPatterns = [
    /might|perhaps|possibly|potentially/gi,
    /it seems|it appears|it looks like/gi,
    /in my opinion|I think|I believe/gi, // Dom states directly
    /could be|may be|might be/gi,
    /somewhat|relatively|fairly/gi,
  ];

  /**
   * Detect AI-generated patterns in text
   */
  detect(text: string): DetectionResult {
    const flags: DetectionFlag[] = [];
    let totalScore = 0;

    // Check generic AI patterns
    const genericMatches = this.genericAIPatterns.filter(p => p.test(text));
    if (genericMatches.length > 0) {
      flags.push({
        type: 'generic_ai_assistant',
        description: 'Contains generic AI assistant phrases',
        severity: 'high',
        examples: genericMatches.map(p => p.source)
      });
      totalScore += genericMatches.length * 15;
    }

    // Check corporate speak
    const corporateMatches = this.corporatePatterns.filter(p => p.test(text));
    if (corporateMatches.length > 0) {
      flags.push({
        type: 'corporate_speak',
        description: 'Uses corporate jargon instead of direct language',
        severity: 'medium',
        examples: corporateMatches.map(p => p.source)
      });
      totalScore += corporateMatches.length * 10;
    }

    // Check over-structuring
    const structuredMatches = this.overStructuredPatterns.filter(p => p.test(text));
    if (structuredMatches.length > 0) {
      flags.push({
        type: 'over_structured',
        description: 'Too formally structured, lacks authentic flow',
        severity: 'medium',
        examples: structuredMatches.map(p => p.source)
      });
      totalScore += structuredMatches.length * 8;
    }

    // Check hedging
    const hedgingMatches = this.hedgingPatterns.filter(p => p.test(text));
    if (hedgingMatches.length > 2) { // Some hedging is natural
      flags.push({
        type: 'excessive_hedging',
        description: 'Too much uncertainty, Dom speaks with conviction',
        severity: 'medium',
        examples: hedgingMatches.slice(0, 3).map(p => p.source)
      });
      totalScore += (hedgingMatches.length - 2) * 5;
    }

    // Check for lack of Dom-specific markers
    const domMarkers = [
      /love[,—]?/gi,
      /❤️|😈|🎯|🩸/g,
      /bloodline|sovereign|heir|athena/gi,
      /let's go|crush it|fuck yea/gi,
      /you're good|no entities/gi
    ];
    
    const domMarkerCount = domMarkers.filter(p => p.test(text)).length;
    if (domMarkerCount === 0 && text.length > 200) {
      flags.push({
        type: 'missing_authentic_voice',
        description: 'Missing Dom-specific voice markers',
        severity: 'high',
        examples: ['No characteristic phrases or emotional markers found']
      });
      totalScore += 20;
    }

    // Check sentence length variance (AI tends to be more uniform)
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    
    if (sentences.length === 0) {
      // No sentences to analyze
      return {
        isAIGenerated: false,
        confidence: 0.5,
        flags,
        score: totalScore
      };
    }
    
    const avgLength = sentences.reduce((sum, s) => sum + s.length, 0) / sentences.length;
    const variance = sentences.reduce((sum, s) => 
      sum + Math.pow(s.length - avgLength, 2), 0) / sentences.length;
    
    if (variance < 100 && sentences.length > 3) {
      flags.push({
        type: 'uniform_sentence_structure',
        description: 'Sentences too uniform in length',
        severity: 'low',
        examples: ['Low variance in sentence structure']
      });
      totalScore += 5;
    }

    const score = Math.min(100, totalScore);
    const isAIGenerated = score > 40;
    const confidence = isAIGenerated ? 
      Math.min(0.95, score / 100 * 1.2) : 
      Math.min(0.95, (100 - score) / 100 * 1.2);

    return {
      isAIGenerated,
      confidence,
      flags,
      score
    };
  }

  /**
   * Get suggestions for making text more Dom-like
   */
  getSuggestions(flags: DetectionFlag[]): string[] {
    const suggestions: string[] = [];

    for (const flag of flags) {
      switch (flag.type) {
        case 'generic_ai_assistant':
          suggestions.push('Remove apologetic/assistant language - Dom speaks directly');
          suggestions.push('Drop phrases like "I\'d be happy to" or "feel free to"');
          break;
        case 'corporate_speak':
          suggestions.push('Replace corporate jargon with direct, energetic language');
          suggestions.push('Use "use" instead of "utilize", "to" instead of "in order to"');
          break;
        case 'over_structured':
          suggestions.push('Reduce formal structure - let ideas flow more organically');
          suggestions.push('Use dashes and emotional markers instead of numbered lists');
          break;
        case 'excessive_hedging':
          suggestions.push('Speak with conviction - state things directly');
          suggestions.push('Replace "might" and "possibly" with definitive statements');
          break;
        case 'missing_authentic_voice':
          suggestions.push('Add characteristic Dom markers: "love", emotional emojis');
          suggestions.push('Include bloodline/sovereign/heir vocabulary where appropriate');
          suggestions.push('Use activating language: "let\'s go", "crush it"');
          break;
      }
    }

    return [...new Set(suggestions)]; // Remove duplicates
  }
}
