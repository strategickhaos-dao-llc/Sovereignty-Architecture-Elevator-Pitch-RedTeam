/**
 * FlameLang Decision Engine
 * Implements decision logic for chart orientation questions
 */
import { FlameLangParserEngine } from './parser';
export class DecisionEngine {
    parser;
    constructor() {
        this.parser = new FlameLangParserEngine();
    }
    /**
     * Analyze a set of questions and build decision logic
     */
    analyzeQuestions(questions) {
        const logic = {};
        for (const [key, question] of Object.entries(questions)) {
            const analysis = this.parser.parse(question);
            const verdict = analysis.dna_layer.output;
            // Build decision explanation
            const decision = {
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
    extractMetaPattern(logic) {
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
    getHorizontalReason(question) {
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
    getVerticalReason(question) {
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
