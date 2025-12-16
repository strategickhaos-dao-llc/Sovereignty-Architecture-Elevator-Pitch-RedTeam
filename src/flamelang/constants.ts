/**
 * FlameLang Parser Constants
 * Centralized configuration for thresholds and confidence levels
 */

/**
 * Truth threshold for DNA layer boolean conversion
 * Values >= this threshold are considered TRUE
 */
export const TRUTH_THRESHOLD = 0.70; // 70% confidence

/**
 * Confidence levels for wave frequency analysis
 */
export const CONFIDENCE_LEVELS = {
  VERY_HIGH: 0.98,
  HIGH: 0.95,
  MEDIUM_HIGH: 0.90,
  DEFAULT: 0.50,
  LOW: 0.15,
  VERY_LOW: 0.05
} as const;

/**
 * DNA codon mappings
 */
export const DNA_CODONS = {
  TRUE: "ATG",   // START codon = TRUE
  FALSE: "TAA",  // STOP codon = FALSE
  UNCERTAIN: "NNN" // Ambiguous
} as const;
