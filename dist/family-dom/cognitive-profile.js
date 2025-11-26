/**
 * FamilyDOM Cognitive Profile Management
 *
 * Maintains continuous cognitive frames across sessions.
 * Tracks user cognitive architecture preferences, parallel processing style,
 * and multi-layer communication patterns.
 */
/**
 * CognitiveProfileManager handles creation, persistence, and retrieval
 * of user cognitive profiles for full-stack reasoning integration.
 */
export class CognitiveProfileManager {
    profiles = new Map();
    defaultProfile;
    constructor() {
        this.defaultProfile = {
            cognitiveStyle: {
                parallelProcessing: false,
                symbolicThroughput: 'medium',
                preferredLayers: ['technical', 'architectural'],
                narrativeRecursion: false,
                metaCommunication: false
            },
            layers: {
                mythic: [],
                emotional: [],
                architectural: [],
                symbolic: [],
                technical: [],
                kinetic: []
            },
            contextMemory: [],
            activeProjects: [],
            narrativeThreads: [],
            intentPatterns: []
        };
    }
    /**
     * Create or retrieve a cognitive profile for a user
     */
    getOrCreateProfile(userId, displayName) {
        let profile = this.profiles.get(userId);
        if (!profile) {
            profile = this.createProfile(userId, displayName || userId);
            this.profiles.set(userId, profile);
        }
        return profile;
    }
    /**
     * Create a new cognitive profile
     */
    createProfile(userId, displayName) {
        const now = new Date();
        return {
            id: `profile_${userId}_${now.getTime()}`,
            userId,
            displayName,
            createdAt: now,
            updatedAt: now,
            cognitiveStyle: { ...this.defaultProfile.cognitiveStyle },
            layers: {
                mythic: [],
                emotional: [],
                architectural: [],
                symbolic: [],
                technical: [],
                kinetic: []
            },
            contextMemory: [],
            activeProjects: [],
            narrativeThreads: [],
            intentPatterns: []
        };
    }
    /**
     * Update profile with new cognitive layer data
     */
    updateLayers(userId, layers) {
        const profile = this.profiles.get(userId);
        if (!profile)
            return;
        for (const [layer, values] of Object.entries(layers)) {
            const key = layer;
            if (profile.layers[key] && Array.isArray(values)) {
                // Add new unique values
                const existingSet = new Set(profile.layers[key]);
                for (const value of values) {
                    existingSet.add(value);
                }
                profile.layers[key] = Array.from(existingSet);
            }
        }
        profile.updatedAt = new Date();
    }
    /**
     * Add a context memory entry
     */
    addContextMemory(userId, content, layers, significance) {
        const profile = this.profiles.get(userId);
        if (!profile)
            return;
        profile.contextMemory.push({
            timestamp: new Date(),
            content,
            layers,
            significance: Math.max(0, Math.min(1, significance))
        });
        // Keep only the most significant and recent memories (limit to 100)
        if (profile.contextMemory.length > 100) {
            profile.contextMemory.sort((a, b) => {
                // Prioritize by significance then recency
                if (Math.abs(a.significance - b.significance) > 0.2) {
                    return b.significance - a.significance;
                }
                return b.timestamp.getTime() - a.timestamp.getTime();
            });
            profile.contextMemory = profile.contextMemory.slice(0, 100);
        }
        profile.updatedAt = new Date();
    }
    /**
     * Update communication style based on observed patterns
     */
    updateCommunicationStyle(userId, updates) {
        const profile = this.profiles.get(userId);
        if (!profile)
            return;
        profile.cognitiveStyle = {
            ...profile.cognitiveStyle,
            ...updates
        };
        profile.updatedAt = new Date();
    }
    /**
     * Track a project context
     */
    trackProject(userId, project) {
        const profile = this.profiles.get(userId);
        if (!profile)
            return;
        const existingProject = profile.activeProjects.find(p => p.name === project.name);
        if (existingProject) {
            existingProject.description = project.description;
            existingProject.artifacts = [...new Set([...existingProject.artifacts, ...project.artifacts])];
            existingProject.status = project.status;
            existingProject.lastInteraction = new Date();
        }
        else {
            profile.activeProjects.push({
                id: `project_${Date.now()}`,
                ...project,
                lastInteraction: new Date()
            });
        }
        profile.updatedAt = new Date();
    }
    /**
     * Record an intent pattern
     */
    recordIntentPattern(userId, pattern, resolvedTo) {
        const profile = this.profiles.get(userId);
        if (!profile)
            return;
        const existing = profile.intentPatterns.find(p => p.pattern === pattern);
        if (existing) {
            existing.frequency++;
            existing.lastSeen = new Date();
            existing.resolvedTo = resolvedTo;
        }
        else {
            profile.intentPatterns.push({
                pattern,
                frequency: 1,
                lastSeen: new Date(),
                resolvedTo
            });
        }
        profile.updatedAt = new Date();
    }
    /**
     * Get relevant context for a new interaction
     */
    getRelevantContext(userId, currentInput) {
        const profile = this.profiles.get(userId);
        if (!profile) {
            return { recentMemory: [], activeProjects: [], relatedPatterns: [] };
        }
        // Get recent high-significance memories
        const recentMemory = profile.contextMemory
            .filter(m => m.significance > 0.5)
            .slice(-10);
        // Get active projects
        const activeProjects = profile.activeProjects
            .filter(p => p.status === 'active')
            .slice(-5);
        // Find related intent patterns
        const inputLower = currentInput.toLowerCase();
        const relatedPatterns = profile.intentPatterns
            .filter(p => inputLower.includes(p.pattern.toLowerCase()) ||
            p.resolvedTo.toLowerCase().includes(inputLower))
            .slice(-5);
        return { recentMemory, activeProjects, relatedPatterns };
    }
    /**
     * Serialize profile for persistence
     */
    serializeProfile(userId) {
        const profile = this.profiles.get(userId);
        if (!profile)
            return null;
        return JSON.stringify(profile, (key, value) => {
            if (value instanceof Date) {
                return value.toISOString();
            }
            return value;
        });
    }
    /**
     * Load profile from serialized data
     */
    loadProfile(serialized) {
        try {
            const profile = JSON.parse(serialized, (key, value) => {
                if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T/.test(value)) {
                    return new Date(value);
                }
                return value;
            });
            this.profiles.set(profile.userId, profile);
            return profile;
        }
        catch {
            return null;
        }
    }
    /**
     * Get all profiles (for admin/debugging)
     */
    getAllProfiles() {
        return Array.from(this.profiles.values());
    }
    /**
     * Check if a user has an established profile
     */
    hasProfile(userId) {
        return this.profiles.has(userId);
    }
    /**
     * Calculate cognitive signature score
     */
    getCognitiveSignature(userId) {
        const profile = this.profiles.get(userId);
        if (!profile) {
            return { score: 0, characteristics: [] };
        }
        const characteristics = [];
        let score = 0;
        // Score based on layer richness
        const totalLayers = Object.values(profile.layers).reduce((sum, arr) => sum + arr.length, 0);
        if (totalLayers > 50) {
            score += 20;
            characteristics.push('rich symbolic vocabulary');
        }
        else if (totalLayers > 20) {
            score += 10;
            characteristics.push('developing symbolic vocabulary');
        }
        // Score based on communication style
        if (profile.cognitiveStyle.parallelProcessing) {
            score += 15;
            characteristics.push('parallel processing');
        }
        if (profile.cognitiveStyle.symbolicThroughput === 'extreme') {
            score += 20;
            characteristics.push('extreme symbolic throughput');
        }
        else if (profile.cognitiveStyle.symbolicThroughput === 'high') {
            score += 10;
            characteristics.push('high symbolic throughput');
        }
        if (profile.cognitiveStyle.narrativeRecursion) {
            score += 15;
            characteristics.push('narrative recursion');
        }
        if (profile.cognitiveStyle.metaCommunication) {
            score += 10;
            characteristics.push('meta-communication');
        }
        // Score based on memory depth
        if (profile.contextMemory.length > 50) {
            score += 10;
            characteristics.push('deep context memory');
        }
        if (profile.activeProjects.length > 3) {
            score += 5;
            characteristics.push('multi-project engagement');
        }
        if (profile.intentPatterns.length > 10) {
            score += 5;
            characteristics.push('established intent patterns');
        }
        return { score, characteristics };
    }
}
export const profileManager = new CognitiveProfileManager();
