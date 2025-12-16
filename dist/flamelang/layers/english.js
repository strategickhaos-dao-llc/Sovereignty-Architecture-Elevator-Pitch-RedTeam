/**
 * FlameLang Layer 1: English → Extract semantic intent
 * Analyzes natural language questions and extracts core semantic elements
 */
export class EnglishLayerProcessor {
    /**
     * Extract semantic intent from English text
     */
    process(input) {
        const extract = this.extractSemanticIntent(input);
        return {
            input,
            extract
        };
    }
    /**
     * Parse question to extract subject, condition, and claim
     */
    extractSemanticIntent(input) {
        // Pattern: "A [subject] may be preferable if [condition]"
        const preferablePattern = /A\s+([^may]+?)\s+may be preferable if\s+(.+?)\.?$/i;
        const preferableMatch = input.match(preferablePattern);
        if (preferableMatch) {
            return {
                subject: preferableMatch[1].trim(),
                condition: preferableMatch[2].trim(),
                claim: "preferable"
            };
        }
        // Pattern: "A [subject] is better for [condition]"
        const betterPattern = /A\s+([^is]+?)\s+is better for\s+(.+?)\.?$/i;
        const betterMatch = input.match(betterPattern);
        if (betterMatch) {
            return {
                subject: betterMatch[1].trim(),
                condition: betterMatch[2].trim(),
                claim: "better"
            };
        }
        // Generic fallback: extract key terms
        return this.genericExtraction(input);
    }
    genericExtraction(input) {
        // Simple heuristic extraction
        const words = input.toLowerCase().split(/\s+/);
        // Find chart type
        let subject = "chart";
        if (words.includes("horizontal"))
            subject = "horizontal bar chart";
        else if (words.includes("vertical"))
            subject = "vertical bar chart";
        // Find condition keywords
        let condition = "unspecified";
        if (input.includes("long") && input.includes("label"))
            condition = "category labels are long";
        else if (input.includes("many categor"))
            condition = "many categories";
        else if (input.includes("negative") || input.includes("profit"))
            condition = "negative values";
        else if (input.includes("floor") || input.includes("building"))
            condition = "building floors";
        // Determine claim
        let claim = "preferable";
        if (input.includes("better"))
            claim = "better";
        if (input.includes("should"))
            claim = "should use";
        return { subject, condition, claim };
    }
}
