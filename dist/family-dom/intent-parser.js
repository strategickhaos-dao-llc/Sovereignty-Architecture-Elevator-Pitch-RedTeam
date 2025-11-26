/**
 * FamilyDOM Intent Parser
 *
 * Multi-layer intent parsing that goes beyond literal interpretation.
 * Parses: mythic, emotional, architectural, symbolic, technical, and kinetic layers.
 */
import { profileManager } from './cognitive-profile.js';
// Pattern dictionaries for layer detection
const MYTHIC_PATTERNS = [
    /\b(sovereign|empire|realm|throne|crown|legion|knight|warrior|quest|oracle|sage|council|decree)\b/gi,
    /\b(ascend|transcend|forge|summon|invoke|manifest|awaken|emerge)\b/gi,
    /\b(phoenix|dragon|hydra|titan|guardian|sentinel|architect)\b/gi
];
const EMOTIONAL_PATTERNS = [
    /\b(feel|feeling|sense|emotion|mood|vibe|energy|spirit|soul|heart)\b/gi,
    /\b(trust|love|fear|hope|joy|anger|peace|chaos|calm|excited)\b/gi,
    /[!]{2,}|\?{2,}/g, // Multiple punctuation as emotional markers
    /\b(overwhelm|inspire|frustrat|excit|amaz|disappoint)\w*/gi
];
const ARCHITECTURAL_PATTERNS = [
    /\b(system|architecture|framework|layer|stack|module|component|pipeline|flow)\b/gi,
    /\b(integration|orchestrat|scaffold|bootstrap|deploy|infrastructure)\b/gi,
    /\b(mesh|network|cluster|node|endpoint|gateway|service)\b/gi,
    /\b(pattern|structure|design|model|schema|protocol)\b/gi
];
const SYMBOLIC_PATTERNS = [
    /\b(symbol|metaphor|represent|embod|signif|meaning|essence)\b/gi,
    /→|←|↔|⇒|⇐|⇔|∴|∵|∞|⊕|⊗|⊙/g, // Arrow and mathematical symbols
    /\b(encode|decode|encrypt|cipher|key|unlock|seal)\b/gi,
    /\b(mirror|reflect|shadow|echo|resonan|harmoni)\b/gi
];
const TECHNICAL_PATTERNS = [
    /\b(api|sdk|cli|gui|docker|kubernetes|git|npm|yarn|pip)\b/gi,
    /\b(typescript|javascript|python|rust|go|java|c\+\+)\b/gi,
    /\b(function|class|interface|module|import|export|async|await)\b/gi,
    /\b(database|query|index|cache|buffer|stream|socket)\b/gi,
    /```[\s\S]*?```/g, // Code blocks
    /`[^`]+`/g // Inline code
];
const KINETIC_PATTERNS = [
    /\b(move|flow|dance|spin|rotate|accelerate|momentum|velocity)\b/gi,
    /\b(push|pull|drag|lift|drop|throw|catch|grab|release)\b/gi,
    /\b(build|break|forge|craft|shape|mold|construct|destroy)\b/gi,
    /\b(launch|deploy|ship|fire|trigger|execute|run|start|stop)\b/gi
];
const META_COMMUNICATION_PATTERNS = [
    /\b(mean|saying|asking|telling|explain|clarif|understand)\b/gi,
    /\b(this (is|was) (about|regarding|concerning))\b/gi,
    /\b(in other words|that is to say|what i mean is)\b/gi,
    /\b(let me (explain|clarify|rephrase))\b/gi
];
const SELF_REFERENCE_PATTERNS = [
    /\b(i am|i'm|myself|we are|we're|ourselves)\b/gi,
    /\b(my (mind|brain|thoughts?|process|cognition))\b/gi,
    /\b(thinking (about|through)|processing|parsing)\b/gi
];
const HUMOR_PATTERNS = [
    /\b(lol|lmao|haha|hehe|rofl|😂|🤣|😄|😁)\b/gi,
    /\b(joke|jest|pun|irony|sarcas|humor|funny)\b/gi,
    /\b(clever|witty|playful)\b/gi
];
const MULTI_AGENT_PATTERNS = [
    /\b(agent|bot|ai|model|gpt|claude|grok|llm|copilot)\b/gi,
    /\b(orchestrat|coordinat|delegate|dispatch|route)\b/gi,
    /\b(team|swarm|collective|ensemble|committee)\b/gi
];
/**
 * IntentParser performs multi-layer analysis of user input
 * to extract deep intent beyond literal interpretation.
 */
export class IntentParser {
    /**
     * Parse input across all cognitive layers
     */
    parse(input, userId) {
        const layers = this.extractLayers(input);
        const metadata = this.extractMetadata(input);
        const resolvedIntent = this.resolveIntent(input, layers, metadata, userId);
        const confidence = this.calculateConfidence(layers, metadata);
        // Update user profile if userId provided
        if (userId) {
            profileManager.updateLayers(userId, layers);
            if (Object.keys(layers).length > 3) {
                profileManager.updateCommunicationStyle(userId, {
                    symbolicThroughput: this.calculateSymbolicThroughput(layers),
                    parallelProcessing: metadata.hasParallelMetaphors,
                    narrativeRecursion: metadata.hasRecursiveIntent,
                    metaCommunication: metadata.hasMetaCommunication
                });
            }
            profileManager.recordIntentPattern(userId, input.slice(0, 50), resolvedIntent);
        }
        return {
            literal: input,
            layers,
            resolvedIntent,
            confidence,
            metadata
        };
    }
    /**
     * Extract cognitive layers from input
     */
    extractLayers(input) {
        const layers = {};
        // Extract mythic references
        const mythicMatches = this.matchPatterns(input, MYTHIC_PATTERNS);
        if (mythicMatches.length > 0) {
            layers.mythic = mythicMatches;
        }
        // Extract emotional markers
        const emotionalMatches = this.matchPatterns(input, EMOTIONAL_PATTERNS);
        if (emotionalMatches.length > 0) {
            layers.emotional = emotionalMatches;
        }
        // Extract architectural concepts
        const architecturalMatches = this.matchPatterns(input, ARCHITECTURAL_PATTERNS);
        if (architecturalMatches.length > 0) {
            layers.architectural = architecturalMatches;
        }
        // Extract symbolic elements
        const symbolicMatches = this.matchPatterns(input, SYMBOLIC_PATTERNS);
        if (symbolicMatches.length > 0) {
            layers.symbolic = symbolicMatches;
        }
        // Extract technical terminology
        const technicalMatches = this.matchPatterns(input, TECHNICAL_PATTERNS);
        if (technicalMatches.length > 0) {
            layers.technical = technicalMatches;
        }
        // Extract kinetic metaphors
        const kineticMatches = this.matchPatterns(input, KINETIC_PATTERNS);
        if (kineticMatches.length > 0) {
            layers.kinetic = kineticMatches;
        }
        return layers;
    }
    /**
     * Match patterns and return unique lowercased results
     */
    matchPatterns(input, patterns) {
        const matches = new Set();
        for (const pattern of patterns) {
            const found = input.match(pattern);
            if (found) {
                for (const match of found) {
                    matches.add(match.toLowerCase().trim());
                }
            }
        }
        return Array.from(matches);
    }
    /**
     * Extract metadata about communication style
     */
    extractMetadata(input) {
        return {
            hasParallelMetaphors: this.detectParallelMetaphors(input),
            hasRecursiveIntent: this.detectRecursiveIntent(input),
            hasMultiAgentReferences: this.matchPatterns(input, MULTI_AGENT_PATTERNS).length > 0,
            hasTechnicalOverlay: this.matchPatterns(input, TECHNICAL_PATTERNS).length > 0,
            hasMythicOverlay: this.matchPatterns(input, MYTHIC_PATTERNS).length > 0,
            hasMetaCommunication: this.matchPatterns(input, META_COMMUNICATION_PATTERNS).length > 0,
            hasHumor: this.matchPatterns(input, HUMOR_PATTERNS).length > 0,
            hasSelfReference: this.matchPatterns(input, SELF_REFERENCE_PATTERNS).length > 0,
            hasCodeLoreBlending: this.detectCodeLoreBlending(input),
            contextSwitchCount: this.countContextSwitches(input)
        };
    }
    /**
     * Detect parallel metaphor usage
     */
    detectParallelMetaphors(input) {
        const mythicCount = this.matchPatterns(input, MYTHIC_PATTERNS).length;
        const technicalCount = this.matchPatterns(input, TECHNICAL_PATTERNS).length;
        return mythicCount > 0 && technicalCount > 0;
    }
    /**
     * Detect recursive intent patterns
     */
    detectRecursiveIntent(input) {
        // Look for self-referential structures
        const selfRef = /\b(this (itself|message|question|query|request)|the (question|answer) (to|of))\b/gi;
        const recursiveMarkers = /\b(recursive|meta|self-refer|inception|nested)\b/gi;
        return selfRef.test(input) || recursiveMarkers.test(input);
    }
    /**
     * Detect code-lore blending (technical + mythic in same context)
     */
    detectCodeLoreBlending(input) {
        const codeBlocks = /```[\s\S]*?```/g;
        const hasCodeBlocks = codeBlocks.test(input);
        const hasMythic = this.matchPatterns(input, MYTHIC_PATTERNS).length > 0;
        return hasCodeBlocks && hasMythic;
    }
    /**
     * Count context switches in the input
     */
    countContextSwitches(input) {
        const layers = [
            this.matchPatterns(input, MYTHIC_PATTERNS).length > 0,
            this.matchPatterns(input, EMOTIONAL_PATTERNS).length > 0,
            this.matchPatterns(input, ARCHITECTURAL_PATTERNS).length > 0,
            this.matchPatterns(input, SYMBOLIC_PATTERNS).length > 0,
            this.matchPatterns(input, TECHNICAL_PATTERNS).length > 0,
            this.matchPatterns(input, KINETIC_PATTERNS).length > 0
        ];
        return layers.filter(Boolean).length;
    }
    /**
     * Resolve the deep intent behind the literal message
     */
    resolveIntent(input, layers, metadata, userId) {
        const intents = [];
        // Check for command-like intent
        if (input.match(/^\/\w+/) || input.match(/^(help|status|deploy|scale|create|build|run)/i)) {
            intents.push('command_execution');
        }
        // Check for question intent
        if (input.match(/\?$/) || input.match(/^(what|how|why|when|where|who|can|could|would|should)/i)) {
            intents.push('information_seeking');
        }
        // Check for creation/building intent
        if (layers.kinetic?.some(k => ['build', 'create', 'forge', 'construct', 'craft'].includes(k))) {
            intents.push('creation_request');
        }
        // Check for strategic/planning intent
        if (layers.architectural && layers.architectural.length > 2) {
            intents.push('architectural_planning');
        }
        // Check for narrative engagement
        if (layers.mythic && layers.mythic.length > 1) {
            intents.push('narrative_engagement');
        }
        // Check for emotional processing
        if (layers.emotional && layers.emotional.length > 1) {
            intents.push('emotional_processing');
        }
        // Check for meta-communication (talking about communication)
        if (metadata.hasMetaCommunication) {
            intents.push('meta_communication');
        }
        // Check for multi-agent coordination
        if (metadata.hasMultiAgentReferences) {
            intents.push('agent_coordination');
        }
        // Use context from profile if available
        if (userId) {
            const context = profileManager.getRelevantContext(userId, input);
            if (context.activeProjects.length > 0) {
                intents.push('project_continuation');
            }
            if (context.relatedPatterns.length > 0) {
                // Use previously resolved intents as hints
                for (const pattern of context.relatedPatterns) {
                    if (!intents.includes(pattern.resolvedTo)) {
                        intents.push(`related:${pattern.resolvedTo}`);
                    }
                }
            }
        }
        // Default to general inquiry if no specific intent detected
        if (intents.length === 0) {
            intents.push('general_inquiry');
        }
        return intents.join(',');
    }
    /**
     * Calculate confidence in intent resolution
     */
    calculateConfidence(layers, metadata) {
        let confidence = 0.5; // Base confidence
        // More layers = higher confidence in understanding
        const layerCount = Object.values(layers).filter(arr => arr && arr.length > 0).length;
        confidence += layerCount * 0.08;
        // Specific metadata indicators increase confidence
        if (metadata.hasMultiAgentReferences)
            confidence += 0.05;
        if (metadata.hasTechnicalOverlay)
            confidence += 0.05;
        if (metadata.hasRecursiveIntent)
            confidence += 0.03;
        if (metadata.hasMetaCommunication)
            confidence += 0.03;
        // High context switching might reduce confidence
        if (metadata.contextSwitchCount > 4)
            confidence -= 0.05;
        return Math.min(1, Math.max(0, confidence));
    }
    /**
     * Calculate symbolic throughput level
     */
    calculateSymbolicThroughput(layers) {
        const total = Object.values(layers).reduce((sum, arr) => sum + (arr?.length || 0), 0);
        if (total >= 15)
            return 'extreme';
        if (total >= 10)
            return 'high';
        if (total >= 5)
            return 'medium';
        return 'low';
    }
    /**
     * Generate a response strategy based on parsed intent
     */
    generateResponseStrategy(parsed, profile) {
        const strategy = {
            tone: this.determineTone(parsed, profile),
            depth: this.determineDepth(parsed, profile),
            layersToMatch: this.selectLayersToMatch(parsed, profile),
            includeMetaReflection: parsed.metadata.hasMetaCommunication,
            includeNarrativeFraming: parsed.metadata.hasMythicOverlay,
            technicalDetail: parsed.metadata.hasTechnicalOverlay ? 'high' : 'medium',
            emotionalAwareness: parsed.layers.emotional ? 'high' : 'low'
        };
        return strategy;
    }
    determineTone(parsed, profile) {
        if (parsed.metadata.hasHumor)
            return 'playful';
        if (parsed.layers.mythic && parsed.layers.mythic.length > 0)
            return 'epic';
        if (parsed.layers.emotional && parsed.layers.emotional.length > 0)
            return 'empathetic';
        if (parsed.layers.technical && parsed.layers.technical.length > 2)
            return 'precise';
        return 'balanced';
    }
    determineDepth(parsed, profile) {
        if (profile?.cognitiveStyle.symbolicThroughput === 'extreme')
            return 'fullstack';
        if (parsed.metadata.contextSwitchCount >= 4)
            return 'deep';
        if (parsed.metadata.contextSwitchCount >= 2)
            return 'medium';
        return 'shallow';
    }
    selectLayersToMatch(parsed, profile) {
        const layers = [];
        if (parsed.layers.mythic)
            layers.push('mythic');
        if (parsed.layers.emotional)
            layers.push('emotional');
        if (parsed.layers.architectural)
            layers.push('architectural');
        if (parsed.layers.symbolic)
            layers.push('symbolic');
        if (parsed.layers.technical)
            layers.push('technical');
        if (parsed.layers.kinetic)
            layers.push('kinetic');
        // Add profile preferences
        if (profile?.cognitiveStyle.preferredLayers) {
            for (const pref of profile.cognitiveStyle.preferredLayers) {
                if (!layers.includes(pref)) {
                    layers.push(pref);
                }
            }
        }
        return layers;
    }
}
export const intentParser = new IntentParser();
