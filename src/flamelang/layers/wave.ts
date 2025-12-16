/**
 * FlameLang Layer 4: Wave → Truth frequency
 * Analyzes claim confidence using wave interference patterns
 */

import { WaveLayer } from '../types';
import { CONFIDENCE_LEVELS } from '../constants';

export class WaveLayerProcessor {
  // Confidence level constants
  private readonly CONFIDENCE = CONFIDENCE_LEVELS;
  /**
   * Calculate truth frequency and interference
   */
  process(matchType: string, subject: string, condition: string): WaveLayer {
    const claim_frequency = this.calculateFrequency(matchType, subject, condition);
    const interference = this.detectInterference(matchType, condition);
    
    return {
      claim_frequency,
      interference
    };
  }

  /**
   * Calculate confidence frequency (0.0 to 1.0)
   */
  private calculateFrequency(matchType: string, subject: string, condition: string): number {
    const subjectLower = subject.toLowerCase();
    const conditionLower = condition.toLowerCase();
    
    // High confidence patterns
    if (matchType === "LITERAL_MAPPING") {
      // Building floors → vertical is very intuitive
      if (conditionLower.includes("floor") && subjectLower.includes("vertical")) {
        return this.CONFIDENCE.VERY_HIGH;
      }
      if (conditionLower.includes("floor") && subjectLower.includes("horizontal")) {
        return this.CONFIDENCE.VERY_LOW;
      }
    }
    
    if (matchType === "MAGNITUDE_DIRECTION") {
      // Negative values → downward (vertical) is intuitive
      if (conditionLower.includes("negative") && subjectLower.includes("vertical")) {
        return this.CONFIDENCE.HIGH;
      }
      if (conditionLower.includes("negative") && subjectLower.includes("horizontal")) {
        return this.CONFIDENCE.LOW;
      }
    }
    
    if (matchType === "ABSTRACT_LAYOUT" || matchType === "ALIGNMENT_ADVANTAGE") {
      // Long labels → horizontal avoids rotation
      if (conditionLower.includes("long") && subjectLower.includes("horizontal")) {
        return this.CONFIDENCE.HIGH;
      }
      // Many categories → horizontal expands easier
      if (conditionLower.includes("many") && subjectLower.includes("horizontal")) {
        return this.CONFIDENCE.MEDIUM_HIGH;
      }
    }
    
    // Default medium confidence
    return this.CONFIDENCE.DEFAULT;
  }

  /**
   * Detect contradicting principles
   */
  private detectInterference(matchType: string, condition: string): string {
    const conditionLower = condition.toLowerCase();
    
    // Check for conflicting requirements
    if (conditionLower.includes("space") && conditionLower.includes("limit")) {
      return "spatial_constraint";
    }
    
    if (conditionLower.includes("time") && conditionLower.includes("series")) {
      return "temporal_expectation";
    }
    
    // No interference detected
    return "none";
  }
}
