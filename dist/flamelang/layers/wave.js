/**
 * FlameLang Layer 4: Wave → Truth frequency
 * Analyzes claim confidence using wave interference patterns
 */
export class WaveLayerProcessor {
    /**
     * Calculate truth frequency and interference
     */
    process(matchType, subject, condition) {
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
    calculateFrequency(matchType, subject, condition) {
        const subjectLower = subject.toLowerCase();
        const conditionLower = condition.toLowerCase();
        // High confidence patterns
        if (matchType === "LITERAL_MAPPING") {
            // Building floors → vertical is very intuitive
            if (conditionLower.includes("floor") && subjectLower.includes("vertical")) {
                return 0.98;
            }
            if (conditionLower.includes("floor") && subjectLower.includes("horizontal")) {
                return 0.05;
            }
        }
        if (matchType === "MAGNITUDE_DIRECTION") {
            // Negative values → downward (vertical) is intuitive
            if (conditionLower.includes("negative") && subjectLower.includes("vertical")) {
                return 0.95;
            }
            if (conditionLower.includes("negative") && subjectLower.includes("horizontal")) {
                return 0.15;
            }
        }
        if (matchType === "ABSTRACT_LAYOUT" || matchType === "ALIGNMENT_ADVANTAGE") {
            // Long labels → horizontal avoids rotation
            if (conditionLower.includes("long") && subjectLower.includes("horizontal")) {
                return 0.95;
            }
            // Many categories → horizontal expands easier
            if (conditionLower.includes("many") && subjectLower.includes("horizontal")) {
                return 0.90;
            }
        }
        // Default medium confidence
        return 0.50;
    }
    /**
     * Detect contradicting principles
     */
    detectInterference(matchType, condition) {
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
