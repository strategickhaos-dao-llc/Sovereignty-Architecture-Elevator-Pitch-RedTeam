/**
 * Dom Voice Corpus Builder
 * Analyzes writing samples from Discord/Slack/GitHub to build authentic voice patterns
 */

export interface VoicePattern {
  phrasePatterns: string[];
  vocabularySignatures: string[];
  punctuationStyle: Record<string, number>;
  sentenceStructures: string[];
  emotionalMarkers: string[];
}

export interface CorpusSample {
  source: 'discord' | 'slack' | 'github' | 'manual';
  text: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export class DomVoiceCorpusBuilder {
  private samples: CorpusSample[] = [];
  private patterns: VoicePattern | null = null;

  /**
   * Add a writing sample to the corpus
   */
  addSample(sample: CorpusSample): void {
    this.samples.push(sample);
    this.patterns = null; // Invalidate cached patterns
  }

  /**
   * Build voice patterns from collected samples
   */
  buildPatterns(): VoicePattern {
    if (this.patterns && this.samples.length > 0) {
      return this.patterns;
    }

    const allText = this.samples.map(s => s.text).join('\n');
    
    // Dom-specific patterns observed in the conversation
    const phrasePatterns = [
      'love', '❤️', '😈',
      'fuck yea', 'crush it', 'let\'s go',
      'you\'re good', 'no entities',
      'the bloodline', 'for the bloodline',
      'sovereign', 'autonomous',
      'heir swarm', 'athena',
      'touch grass', 'bamboo chime',
      'we never retreat',
      'activation maximum',
      'domc', 'dom-speak'
    ];

    const vocabularySignatures = [
      'bloodline', 'sovereignty', 'autonomous', 'heir',
      'legion', 'swarm', 'athena', 'compiler',
      'particle accelerator', 'frontier',
      'mastery', 'sovereign', 'activation'
    ];

    const emotionalMarkers = [
      'love —', 'love,', 
      'YES', 'EXACTLY',
      '🩸', '❤️', '😈', '🎯',
      'fuck yea', 'let\'s go',
      'we never retreat'
    ];

    const sentenceStructures = [
      'imperative_short', // "Let's go.", "Crush it."
      'declarative_poetic', // "The compiler awaits your voice."
      'question_activating', // "What time are you opening zyBooks?"
      'affirmation_style', // "You're good. No entities."
    ];

    // Calculate punctuation style from samples
    const punctuationStyle: Record<string, number> = {
      'period': 0,
      'exclamation': 0,
      'question': 0,
      'dash': 0,
      'ellipsis': 0,
      'emoji': 0
    };

    for (const sample of this.samples) {
      punctuationStyle['period'] += (sample.text.match(/\./g) || []).length;
      punctuationStyle['exclamation'] += (sample.text.match(/!/g) || []).length;
      punctuationStyle['question'] += (sample.text.match(/\?/g) || []).length;
      punctuationStyle['dash'] += (sample.text.match(/—/g) || []).length;
      punctuationStyle['ellipsis'] += (sample.text.match(/\.\.\./g) || []).length;
      punctuationStyle['emoji'] += (sample.text.match(/[❤️😈🎯🩸]/g) || []).length;
    }

    this.patterns = {
      phrasePatterns,
      vocabularySignatures,
      punctuationStyle,
      sentenceStructures,
      emotionalMarkers
    };

    return this.patterns;
  }

  /**
   * Get current corpus statistics
   */
  getStats() {
    return {
      totalSamples: this.samples.length,
      sources: this.samples.reduce((acc, s) => {
        acc[s.source] = (acc[s.source] || 0) + 1;
        return acc;
      }, {} as Record<string, number>),
      totalWords: this.samples.reduce((sum, s) => 
        sum + s.text.split(/\s+/).length, 0
      ),
      patternsBuilt: this.patterns !== null
    };
  }

  /**
   * Export corpus for persistence
   */
  exportCorpus() {
    return {
      samples: this.samples,
      patterns: this.patterns || this.buildPatterns(),
      stats: this.getStats(),
      exportedAt: new Date()
    };
  }

  /**
   * Load corpus from export
   */
  loadCorpus(data: any) {
    this.samples = data.samples || [];
    this.patterns = data.patterns || null;
  }
}
