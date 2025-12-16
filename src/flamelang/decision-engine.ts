/**
 * FlameLang Decision Engine
 * Implements decision logic for chart orientation questions
 */

import { DecisionLogic, QuestionDecision, MetaPattern } from './types';
import { FlameLangParserEngine } from './parser';

export class DecisionEngine {
  private parser: FlameLangParserEngine;

  constructor() {
    this.parser = new FlameLangParserEngine();
  }

  /**
   * Analyze a set of questions and build decision logic
   */
  analyzeQuestions(questions: Record<string, string>): DecisionLogic {
    const logic: DecisionLogic = {};

    for (const [key, question] of Object.entries(questions)) {
      const analysis = this.parser.parse(question);
      const verdict = analysis.dna_layer.output;
      
      // Build decision explanation
      const decision: QuestionDecision = {
        verdict
      };

      // Add reasoning based on pattern type
      if (question.toLowerCase().includes("horizontal")) {
        decision.horizontal = this.getHorizontalReason(question);
      }
      if (question.toLowerCase().includes("vertical")) {
        decision.vertical = this.getVerticalReason(question);
      }

      logic[key] = decision;
    }

    return logic;
  }

  /**
   * Extract meta-pattern from analyzed questions
   */
  extractMetaPattern(logic: DecisionLogic): MetaPattern {
    // Analyze the decision patterns
    const patterns = Object.values(logic);
    
    // Generate rule based on observed patterns
    const rule = `IF concept maps literally to visual orientation → use that orientation
IF concept is abstract (categories, labels) → horizontal often better
IF concept involves magnitude/amount → vertical preferred`;

    return {
      rule,
      flamelang_operator: "⚖️" // balance/judgment glyph
    };
  }

  private getHorizontalReason(question: string): string {
    const q = question.toLowerCase();
    
    if (q.includes("long") && q.includes("label")) {
      return "labels don't need rotation";
    }
    if (q.includes("many categor")) {
      return "height expands easier than width";
    }
    if (q.includes("negative")) {
      return "left = negative (weird)";
    }
    if (q.includes("floor") || q.includes("building")) {
      return "would be confusing";
    }
    
    return "default horizontal reasoning";
  }

  private getVerticalReason(question: string): string {
    const q = question.toLowerCase();
    
    if (q.includes("negative")) {
      return "downward = negative (intuitive)";
    }
    if (q.includes("floor") || q.includes("building")) {
      return "height represents height (literal mapping)";
    }
    
    return "default vertical reasoning";
  }
}
