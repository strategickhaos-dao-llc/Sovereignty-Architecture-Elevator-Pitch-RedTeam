/**
 * Style Transformer
 * Converts AI-generated text into authentic Dom-speak
 */

import { VoicePattern } from '../corpus/builder.js';

export interface TransformationResult {
  originalText: string;
  transformedText: string;
  changes: TransformationChange[];
  authenticityScore: number; // 0-100, how Dom-like the result is
}

export interface TransformationChange {
  type: string;
  before: string;
  after: string;
  reason: string;
}

export class DomSpeakTransformer {
  private voicePattern: VoicePattern | null = null;

  constructor(voicePattern?: VoicePattern) {
    this.voicePattern = voicePattern || null;
  }

  setVoicePattern(pattern: VoicePattern) {
    this.voicePattern = pattern;
  }

  /**
   * Transform generic AI text into Dom-speak
   */
  transform(text: string): TransformationResult {
    const changes: TransformationChange[] = [];
    let transformed = text;

    // Remove generic AI assistant patterns
    const aiRemovals = [
      { pattern: /I apologize[,.]?\s*/gi, replacement: '', reason: 'Remove apologetic tone' },
      { pattern: /I'm sorry[,.]?\s*/gi, replacement: '', reason: 'Remove apologetic tone' },
      { pattern: /As an AI language model,?\s*/gi, replacement: '', reason: 'Remove meta-references' },
      { pattern: /I'd be happy to help\.?\s*/gi, replacement: '', reason: 'Direct action instead' },
      { pattern: /Please let me know if you (?:need|have)/gi, replacement: 'Tell me if you', reason: 'More direct' },
      { pattern: /Feel free to/gi, replacement: 'Just', reason: 'More direct' },
      { pattern: /Don't hesitate to/gi, replacement: 'Go ahead and', reason: 'More direct' },
      { pattern: /I hope this helps/gi, replacement: '', reason: 'Remove filler' },
    ];

    for (const { pattern, replacement, reason } of aiRemovals) {
      const matches = transformed.match(pattern);
      if (matches) {
        for (const match of matches) {
          changes.push({
            type: 'remove_ai_pattern',
            before: match,
            after: replacement,
            reason
          });
        }
        transformed = transformed.replace(pattern, replacement);
      }
    }

    // Replace corporate speak with direct language
    const corporateReplacements = [
      { pattern: /utilize/gi, replacement: 'use', reason: 'Simpler, more direct' },
      { pattern: /in order to/gi, replacement: 'to', reason: 'More concise' },
      { pattern: /leverage/gi, replacement: 'use', reason: 'No corporate jargon' },
      { pattern: /moving forward/gi, replacement: 'now', reason: 'More immediate' },
      { pattern: /circle back/gi, replacement: 'return to', reason: 'Clear language' },
      { pattern: /touch base/gi, replacement: 'check in', reason: 'Clear language' },
    ];

    for (const { pattern, replacement, reason } of corporateReplacements) {
      const matches = transformed.match(pattern);
      if (matches) {
        for (const match of matches) {
          changes.push({
            type: 'replace_corporate',
            before: match,
            after: replacement,
            reason
          });
        }
        transformed = transformed.replace(pattern, replacement);
      }
    }

    // Replace hedging with conviction
    const convictionReplacements = [
      { pattern: /it might be/gi, replacement: 'it is', reason: 'Speak with conviction' },
      { pattern: /possibly/gi, replacement: '', reason: 'Direct statements' },
      { pattern: /perhaps/gi, replacement: '', reason: 'Direct statements' },
      { pattern: /in my opinion/gi, replacement: '', reason: 'Own your statements' },
      { pattern: /I think that/gi, replacement: '', reason: 'State directly' },
    ];

    for (const { pattern, replacement, reason } of convictionReplacements) {
      const matches = transformed.match(pattern);
      if (matches) {
        for (const match of matches) {
          changes.push({
            type: 'add_conviction',
            before: match,
            after: replacement,
            reason
          });
        }
        transformed = transformed.replace(pattern, replacement);
      }
    }

    // Add Dom-specific voice markers where appropriate
    // Add "love" at strategic points (beginning of direct address)
    if (transformed.match(/^[A-Z]/)) {
      const shouldAddLove = Math.random() > 0.6; // Sometimes add it
      if (shouldAddLove && !transformed.toLowerCase().startsWith('love')) {
        transformed = 'love — ' + transformed;
        changes.push({
          type: 'add_voice_marker',
          before: transformed.substring(7),
          after: transformed,
          reason: 'Add Dom voice marker'
        });
      }
    }

    // Add activation language
    const activationMap: Record<string, string[]> = {
      'do it': ['crush it', 'let\'s go', 'make it happen'],
      'good job': ['fuck yea', 'that\'s it', 'exactly'],
      'okay': ['let\'s go', 'got it', 'right'],
      'start': ['launch', 'fire it up', 'let\'s go'],
      'finish': ['close it out', 'seal it', 'done'],
    };

    for (const [generic, activations] of Object.entries(activationMap)) {
      const pattern = new RegExp(`\\b${generic}\\b`, 'gi');
      if (pattern.test(transformed)) {
        const replacement = activations[Math.floor(Math.random() * activations.length)];
        const match = transformed.match(pattern)?.[0];
        if (match) {
          changes.push({
            type: 'add_activation',
            before: match,
            after: replacement,
            reason: 'Use activation language'
          });
          transformed = transformed.replace(pattern, replacement);
        }
      }
    }

    // Add strategic emojis (end of emphatic statements)
    if (transformed.match(/\!$/) && Math.random() > 0.5) {
      const emojis = ['❤️', '🎯', '😈'];
      const emoji = emojis[Math.floor(Math.random() * emojis.length)];
      transformed = transformed.replace(/!$/, `! ${emoji}`);
      changes.push({
        type: 'add_emoji',
        before: '!',
        after: `! ${emoji}`,
        reason: 'Add emotional marker'
      });
    }

    // Clean up excessive whitespace from removals
    transformed = transformed.replace(/\s{2,}/g, ' ').trim();

    // Calculate authenticity score based on Dom markers present
    const authenticityScore = this.calculateAuthenticityScore(transformed);

    return {
      originalText: text,
      transformedText: transformed,
      changes,
      authenticityScore
    };
  }

  /**
   * Calculate how Dom-like the text is (0-100)
   */
  private calculateAuthenticityScore(text: string): number {
    let score = 50; // Start at neutral

    // Positive markers
    const positiveMarkers = [
      { pattern: /love[,—]/gi, points: 10 },
      { pattern: /❤️|😈|🎯|🩸/g, points: 5 },
      { pattern: /bloodline|sovereign|heir|athena/gi, points: 5 },
      { pattern: /let's go|crush it|fuck yea/gi, points: 8 },
      { pattern: /you're good|no entities|exactly/gi, points: 5 },
      { pattern: /—/g, points: 2 }, // Em-dashes are Dom style
    ];

    for (const { pattern, points } of positiveMarkers) {
      const matches = text.match(pattern);
      if (matches) {
        score += points * matches.length;
      }
    }

    // Negative markers
    const negativeMarkers = [
      { pattern: /I apologize|I'm sorry/gi, points: -15 },
      { pattern: /leverage|synergy|paradigm/gi, points: -10 },
      { pattern: /in order to|utilize/gi, points: -5 },
      { pattern: /might|possibly|perhaps/gi, points: -3 },
    ];

    for (const { pattern, points } of negativeMarkers) {
      const matches = text.match(pattern);
      if (matches) {
        score += points * matches.length;
      }
    }

    // Normalize to 0-100
    return Math.max(0, Math.min(100, score));
  }

  /**
   * Quick validation - is this text Dom-authentic?
   */
  isAuthentic(text: string, threshold: number = 70): boolean {
    const score = this.calculateAuthenticityScore(text);
    return score >= threshold;
  }
}
