/**
 * FlameLang Layer 5: DNA → Boolean codon
 * Converts wave frequency to boolean output using genetic codon analogy
 */

import { DNALayer } from '../types';
import { DNA_CODONS, TRUTH_THRESHOLD } from '../constants';

export class DNALayerProcessor {
  // DNA codons mapping to boolean logic
  private readonly codons = DNA_CODONS;
  private readonly truthThreshold = TRUTH_THRESHOLD;

  /**
   * Convert wave frequency to boolean codon
   */
  process(frequency: number, interference: string): DNALayer {
    const output = this.determineBoolean(frequency, interference);
    const codon = output ? this.codons.TRUE : this.codons.FALSE;
    
    return {
      codon,
      output
    };
  }

  /**
   * Determine boolean output based on frequency and interference
   */
  private determineBoolean(frequency: number, interference: string): boolean {
    // Strong interference can flip the result
    if (interference !== "none") {
      // Apply interference damping
      const dampedFrequency = frequency * 0.5;
      return dampedFrequency >= this.truthThreshold;
    }
    
    // Normal threshold check
    return frequency >= this.truthThreshold;
  }
}
