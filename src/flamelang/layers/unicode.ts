/**
 * FlameLang Layer 3: Unicode → Pattern matching
 * Identifies logical patterns using Unicode symbolic representations
 */

import { UnicodeLayer } from '../types';

export class UnicodeLayerProcessor {
  private patterns = {
    ALIGNMENT_ADVANTAGE: "⟨ORIENTATION⟩ + ⟨PROPERTY⟩ → ⟨BENEFIT⟩",
    LITERAL_MAPPING: "⟨CONCEPT⟩ ≡ ⟨VISUAL⟩",
    MAGNITUDE_DIRECTION: "⟨VALUE⟩ × ⟨AXIS⟩ → ⟨MEANING⟩",
    ABSTRACT_LAYOUT: "⟨ABSTRACT⟩ ⊗ ⟨SPACE⟩ → ⟨CLARITY⟩"
  };

  /**
   * Determine pattern type from compressed logic
   */
  process(compressed: string, subject: string, condition: string): UnicodeLayer {
    const match_type = this.identifyPattern(subject, condition);
    const pattern = this.patterns[match_type as keyof typeof this.patterns] || this.patterns.ALIGNMENT_ADVANTAGE;
    
    return {
      pattern,
      match_type
    };
  }

  /**
   * Identify which pattern matches the question structure
   */
  private identifyPattern(subject: string, condition: string): string {
    const subjectLower = subject.toLowerCase();
    const conditionLower = condition.toLowerCase();
    
    // Check for literal mapping (e.g., building floors → vertical height)
    if (conditionLower.includes("floor") || conditionLower.includes("building")) {
      return "LITERAL_MAPPING";
    }
    
    // Check for magnitude/direction (e.g., negative profits)
    if (conditionLower.includes("negative") || conditionLower.includes("profit")) {
      return "MAGNITUDE_DIRECTION";
    }
    
    // Check for abstract layout (many categories, long labels)
    if (conditionLower.includes("many") || conditionLower.includes("long")) {
      return "ABSTRACT_LAYOUT";
    }
    
    // Default to alignment advantage
    return "ALIGNMENT_ADVANTAGE";
  }
}
