/**
 * FlameLang ZyBooks Parser - Type Definitions
 * Multi-layered semantic analysis system for educational questions
 */

export interface EnglishLayerExtract {
  subject: string;
  condition: string;
  claim: string;
}

export interface EnglishLayer {
  input: string;
  extract: EnglishLayerExtract;
}

export interface HebrewLayer {
  root_mapping: Record<string, string>;
  compressed: string;
}

export interface UnicodeLayer {
  pattern: string;
  match_type: string;
}

export interface WaveLayer {
  claim_frequency: number;
  interference: string;
}

export interface DNALayer {
  codon: string;
  output: boolean;
}

export interface FlameLangParser {
  english_layer: EnglishLayer;
  hebrew_layer: HebrewLayer;
  unicode_layer: UnicodeLayer;
  wave_layer: WaveLayer;
  dna_layer: DNALayer;
}

export interface QuestionDecision {
  horizontal?: string;
  vertical?: string;
  verdict: boolean;
}

export interface DecisionLogic {
  [key: string]: QuestionDecision;
}

export interface MetaPattern {
  rule: string;
  flamelang_operator: string;
}

export interface SectionResults {
  section: string;
  score: string;
  answers: boolean[];
}

export interface FlameLangAnalysis {
  results: SectionResults;
  flamelang_parser: FlameLangParser;
  decision_logic: DecisionLogic;
  meta_pattern: MetaPattern;
  progress: {
    total_points: number;
    sections_cleared: string[];
    momentum: string;
    status: string;
  };
}

export type AnswerType = 'T' | 'F' | boolean;
