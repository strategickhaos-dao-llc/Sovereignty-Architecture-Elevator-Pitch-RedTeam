/**
 * FlameLang Layer 2: Hebrew → Compress to root logic
 * Maps concepts to Hebrew roots and creates compressed logical representations
 */
export class HebrewLayerProcessor {
    rootMappings = {
        orientation: {
            horizontal: "אפק", // ofek - horizon
            vertical: "אנך" // anakh - vertical
        },
        property: {
            long: "ארך", // orekh - length
            many: "רב", // rav - many
            negative: "שלל", // shlal - negative
            height: "גבה" // govah - height
        },
        benefit: {
            preferable: "עדף", // adif - preferred
            better: "טוב", // tov - good
            suitable: "מתאים" // mat'im - suitable
        }
    };
    /**
     * Compress English semantic extract to Hebrew root logic
     */
    process(extract) {
        const root_mapping = this.mapToRoots(extract);
        const compressed = this.compress(root_mapping);
        return {
            root_mapping,
            compressed
        };
    }
    /**
     * Map semantic elements to Hebrew roots
     */
    mapToRoots(extract) {
        const mapping = {};
        // Map subject (orientation)
        if (extract.subject.includes("horizontal")) {
            mapping.horizontal = this.rootMappings.orientation.horizontal;
        }
        if (extract.subject.includes("vertical")) {
            mapping.vertical = this.rootMappings.orientation.vertical;
        }
        // Map condition (property)
        const condition = extract.condition.toLowerCase();
        if (condition.includes("long")) {
            mapping.long_labels = this.rootMappings.property.long;
        }
        if (condition.includes("many")) {
            mapping.many_categories = this.rootMappings.property.many;
        }
        if (condition.includes("negative")) {
            mapping.negative_values = this.rootMappings.property.negative;
        }
        if (condition.includes("height") || condition.includes("floor")) {
            mapping.height_concept = this.rootMappings.property.height;
        }
        // Map claim (benefit)
        const claimKey = extract.claim.toLowerCase();
        if (claimKey.includes("prefer")) {
            mapping.preferable = this.rootMappings.benefit.preferable;
        }
        else if (claimKey.includes("better")) {
            mapping.better = this.rootMappings.benefit.better;
        }
        else {
            mapping.suitable = this.rootMappings.benefit.suitable;
        }
        return mapping;
    }
    /**
     * Create compressed logical expression
     */
    compress(mapping) {
        const values = Object.values(mapping);
        return values.join("→");
    }
}
