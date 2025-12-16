/**
 * FlameLang ZyBooks Parser - Main Orchestrator
 * Coordinates all 5 layers to analyze educational questions
 */
import { EnglishLayerProcessor } from './layers/english';
import { HebrewLayerProcessor } from './layers/hebrew';
import { UnicodeLayerProcessor } from './layers/unicode';
import { WaveLayerProcessor } from './layers/wave';
import { DNALayerProcessor } from './layers/dna';
export class FlameLangParserEngine {
    englishLayer;
    hebrewLayer;
    unicodeLayer;
    waveLayer;
    dnaLayer;
    constructor() {
        this.englishLayer = new EnglishLayerProcessor();
        this.hebrewLayer = new HebrewLayerProcessor();
        this.unicodeLayer = new UnicodeLayerProcessor();
        this.waveLayer = new WaveLayerProcessor();
        this.dnaLayer = new DNALayerProcessor();
    }
    /**
     * Process a question through all 5 FlameLang layers
     */
    parse(question) {
        // Layer 1: English → Extract semantic intent
        const english_layer = this.englishLayer.process(question);
        // Layer 2: Hebrew → Compress to root logic
        const hebrew_layer = this.hebrewLayer.process(english_layer.extract);
        // Layer 3: Unicode → Pattern matching
        const unicode_layer = this.unicodeLayer.process(hebrew_layer.compressed, english_layer.extract.subject, english_layer.extract.condition);
        // Layer 4: Wave → Truth frequency
        const wave_layer = this.waveLayer.process(unicode_layer.match_type, english_layer.extract.subject, english_layer.extract.condition);
        // Layer 5: DNA → Boolean codon
        const dna_layer = this.dnaLayer.process(wave_layer.claim_frequency, wave_layer.interference);
        return {
            english_layer,
            hebrew_layer,
            unicode_layer,
            wave_layer,
            dna_layer
        };
    }
    /**
     * Quick analysis: just return the boolean verdict
     */
    quickAnalyze(question) {
        const result = this.parse(question);
        return result.dna_layer.output;
    }
}
