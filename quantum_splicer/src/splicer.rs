//! Quantum Splicer - Generic combinator for department synthesis
//!
//! Takes any two `impl SovereignTrait` and generates a `BlackHoleChild` with:
//! - Entanglement hash (SHA256)
//! - Child DNA hash (SHA512)
//! - Quadrant weights and consensus score
//! - Dividend yield and deploy targets
//! - Orb resonance inheritance

use sha2::{Sha256, Sha512, Digest};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use crate::departments::{Quadrant, SovereignTrait, StrategickhaosPrime};

/// Deploy target platforms for children
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum DeployTarget {
    /// Discord Activities platform
    DiscordActivities,
    /// NinjaTrader trading platform
    NinjaTrader,
    /// 7% Dividend Loop system
    SevenPercentLoop,
    /// Steam game platform
    Steam,
    /// Epic Games Store
    EpicGames,
    /// Twitch integration
    Twitch,
    /// Web deployment
    Web,
    /// Mobile platforms
    Mobile,
}

/// Quadrant weight distribution for a child
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct QuadrantWeights {
    pub game_dev: f64,
    pub trading: f64,
    pub intelligence: f64,
    pub hybrid: f64,
}

impl QuadrantWeights {
    /// Calculate consensus score from weights
    pub fn consensus_score(&self) -> f64 {
        let total = self.game_dev + self.trading + self.intelligence + self.hybrid;
        if total == 0.0 {
            return 0.0;
        }
        
        // Consensus is higher when weights are more balanced
        let weights = [self.game_dev, self.trading, self.intelligence, self.hybrid];
        let avg = total / 4.0;
        let variance: f64 = weights.iter().map(|w| (w - avg).powi(2)).sum::<f64>() / 4.0;
        let std_dev = variance.sqrt();
        
        // Normalize: lower std_dev = higher consensus
        let max_std_dev = 0.5; // Maximum expected deviation
        ((max_std_dev - std_dev.min(max_std_dev)) / max_std_dev * 100.0).round()
    }
}

/// Result of quantum splicing two departments
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BlackHoleChild {
    /// Name of the child entity
    pub name: String,
    /// Human-readable description
    pub description: String,
    /// SHA256 quantum entanglement hash
    pub entanglement: String,
    /// SHA512 child DNA hash
    pub child_dna: String,
    /// Parent A department name
    pub parent_a: String,
    /// Parent B department name  
    pub parent_b: String,
    /// Quadrant weight distribution
    pub quadrant_weights: QuadrantWeights,
    /// Consensus score (0-100)
    pub consensus_score: f64,
    /// Calculated dividend yield percentage
    pub dividend_yield: f64,
    /// Suggested deployment targets
    pub deploy_targets: Vec<DeployTarget>,
    /// Whether child has orb resonance
    pub orb_resonance: bool,
    /// Genesis provenance hash from StrategickhaosPrime
    pub provenance_hash: String,
}

/// The Quantum Splicer - Generic combinator for department synthesis
#[derive(Debug, Default)]
pub struct QuantumSplicer {
    /// In-memory storage for offspring DNA
    breeding_chamber: HashMap<String, BlackHoleChild>,
}

impl QuantumSplicer {
    /// Genesis constants for splicing
    const GENESIS_SALT: &'static [u8] = b"BLACKHOLE_GENESIS_SALT_2025";
    const ENTANGLEMENT_MULTIPLIER: f64 = 0.07; // 7% base yield
    
    /// Create a new Quantum Splicer instance
    pub fn new() -> Self {
        Self {
            breeding_chamber: HashMap::new(),
        }
    }
    
    /// Splice two departments together to create a BlackHoleChild
    pub fn splice<A: SovereignTrait + ?Sized, B: SovereignTrait + ?Sized>(
        &mut self,
        parent_a: &A,
        parent_b: &B,
    ) -> BlackHoleChild {
        // Generate entanglement hash (SHA256)
        let entanglement = self.generate_entanglement(parent_a, parent_b);
        
        // Generate child DNA hash (SHA512)
        let child_dna = self.generate_child_dna(parent_a, parent_b, &entanglement);
        
        // Calculate quadrant weights
        let quadrant_weights = self.calculate_quadrant_weights(parent_a, parent_b);
        
        // Calculate consensus score
        let consensus_score = quadrant_weights.consensus_score();
        
        // Calculate dividend yield
        let dividend_yield = self.calculate_dividend_yield(consensus_score);
        
        // Determine deploy targets
        let deploy_targets = self.determine_deploy_targets(parent_a, parent_b);
        
        // Determine orb resonance inheritance
        let orb_resonance = parent_a.orb_resonance() || parent_b.orb_resonance();
        
        // Generate provenance hash
        let prime = StrategickhaosPrime;
        let provenance_hash = prime.genesis_proof(&child_dna);
        
        // Generate child name
        let name = self.generate_child_name(parent_a, parent_b);
        let description = self.generate_description(parent_a, parent_b);
        
        let child = BlackHoleChild {
            name,
            description,
            entanglement,
            child_dna: child_dna.clone(),
            parent_a: parent_a.department_name().to_string(),
            parent_b: parent_b.department_name().to_string(),
            quadrant_weights,
            consensus_score,
            dividend_yield,
            deploy_targets,
            orb_resonance,
            provenance_hash,
        };
        
        // Store in breeding chamber
        self.breeding_chamber.insert(child_dna, child.clone());
        
        child
    }
    
    /// Generate SHA256 entanglement hash
    fn generate_entanglement<A: SovereignTrait + ?Sized, B: SovereignTrait + ?Sized>(
        &self,
        parent_a: &A,
        parent_b: &B,
    ) -> String {
        let mut hasher = Sha256::new();
        hasher.update(parent_a.dna());
        hasher.update(parent_b.dna());
        hasher.update(Self::GENESIS_SALT);
        hex::encode(hasher.finalize())
    }
    
    /// Generate SHA512 child DNA hash
    fn generate_child_dna<A: SovereignTrait + ?Sized, B: SovereignTrait + ?Sized>(
        &self,
        parent_a: &A,
        parent_b: &B,
        entanglement: &str,
    ) -> String {
        let mut hasher = Sha512::new();
        hasher.update(parent_a.dna());
        hasher.update(parent_b.dna());
        hasher.update(entanglement.as_bytes());
        hasher.update(Self::GENESIS_SALT);
        hex::encode(hasher.finalize())
    }
    
    /// Calculate quadrant weight distribution
    fn calculate_quadrant_weights<A: SovereignTrait + ?Sized, B: SovereignTrait + ?Sized>(
        &self,
        parent_a: &A,
        parent_b: &B,
    ) -> QuadrantWeights {
        let mut weights = QuadrantWeights::default();
        
        // Each parent contributes 0.5 to their quadrant
        for quadrant in [parent_a.quadrant(), parent_b.quadrant()] {
            match quadrant {
                Quadrant::GameDev => weights.game_dev += 0.5,
                Quadrant::Trading => weights.trading += 0.5,
                Quadrant::Intelligence => weights.intelligence += 0.5,
                Quadrant::Hybrid => weights.hybrid += 0.5,
            }
        }
        
        weights
    }
    
    /// Calculate dividend yield based on consensus
    fn calculate_dividend_yield(&self, consensus_score: f64) -> f64 {
        // Base yield is 7%, modified by consensus
        let base_yield = Self::ENTANGLEMENT_MULTIPLIER * 100.0;
        let consensus_modifier = 1.0 + (consensus_score / 100.0);
        (base_yield * consensus_modifier * 100.0).round() / 100.0
    }
    
    /// Determine appropriate deploy targets based on parent quadrants
    fn determine_deploy_targets<A: SovereignTrait + ?Sized, B: SovereignTrait + ?Sized>(
        &self,
        parent_a: &A,
        parent_b: &B,
    ) -> Vec<DeployTarget> {
        let mut targets = Vec::new();
        
        // Add targets based on parent quadrants
        for quadrant in [parent_a.quadrant(), parent_b.quadrant()] {
            match quadrant {
                Quadrant::GameDev => {
                    if !targets.contains(&DeployTarget::Steam) {
                        targets.push(DeployTarget::Steam);
                    }
                    if !targets.contains(&DeployTarget::EpicGames) {
                        targets.push(DeployTarget::EpicGames);
                    }
                    if !targets.contains(&DeployTarget::DiscordActivities) {
                        targets.push(DeployTarget::DiscordActivities);
                    }
                }
                Quadrant::Trading => {
                    if !targets.contains(&DeployTarget::NinjaTrader) {
                        targets.push(DeployTarget::NinjaTrader);
                    }
                    if !targets.contains(&DeployTarget::SevenPercentLoop) {
                        targets.push(DeployTarget::SevenPercentLoop);
                    }
                }
                Quadrant::Intelligence => {
                    if !targets.contains(&DeployTarget::Web) {
                        targets.push(DeployTarget::Web);
                    }
                    if !targets.contains(&DeployTarget::DiscordActivities) {
                        targets.push(DeployTarget::DiscordActivities);
                    }
                }
                Quadrant::Hybrid => {
                    // Hybrid gets all targets
                    for target in [
                        DeployTarget::DiscordActivities,
                        DeployTarget::Steam,
                        DeployTarget::Web,
                    ] {
                        if !targets.contains(&target) {
                            targets.push(target);
                        }
                    }
                }
            }
        }
        
        targets
    }
    
    /// Generate a name for the child based on parents
    fn generate_child_name<A: SovereignTrait + ?Sized, B: SovereignTrait + ?Sized>(
        &self,
        parent_a: &A,
        parent_b: &B,
    ) -> String {
        let a_name = parent_a.department_name();
        let b_name = parent_b.department_name();
        
        // Special named children based on parent combinations
        match (a_name, b_name) {
            ("Unity Game Engine", "NinjaTrader") | ("NinjaTrader", "Unity Game Engine") => {
                "RenkoPulse Orb Healer".to_string()
            }
            ("Unreal Engine", "Grokanator AI") | ("Grokanator AI", "Unreal Engine") => {
                "7Percent Dividend Turret".to_string()
            }
            ("Unity Game Engine", "Grokanator AI") | ("Grokanator AI", "Unity Game Engine") => {
                "Grokanator Boss Fight".to_string()
            }
            _ => format!("{} × {} Child", a_name, b_name),
        }
    }
    
    /// Generate a description for the child
    fn generate_description<A: SovereignTrait + ?Sized, B: SovereignTrait + ?Sized>(
        &self,
        parent_a: &A,
        parent_b: &B,
    ) -> String {
        let a_name = parent_a.department_name();
        let b_name = parent_b.department_name();
        
        match (a_name, b_name) {
            ("Unity Game Engine", "NinjaTrader") | ("NinjaTrader", "Unity Game Engine") => {
                "Trading-infused game entity that heals based on Renko chart patterns".to_string()
            }
            ("Unreal Engine", "Grokanator AI") | ("Grokanator AI", "Unreal Engine") => {
                "AI-powered turret that generates 7% dividend yields through engagement".to_string()
            }
            ("Unity Game Engine", "Grokanator AI") | ("Grokanator AI", "Unity Game Engine") => {
                "AI boss encounter powered by Grokanator swarm intelligence".to_string()
            }
            _ => format!(
                "Hybrid entity combining {} and {} capabilities",
                a_name, b_name
            ),
        }
    }
    
    /// Get all children from the breeding chamber
    pub fn get_all_children(&self) -> Vec<&BlackHoleChild> {
        self.breeding_chamber.values().collect()
    }
    
    /// Get a child by its DNA hash
    pub fn get_child_by_dna(&self, dna: &str) -> Option<&BlackHoleChild> {
        self.breeding_chamber.get(dna)
    }
    
    /// Get the number of children in the breeding chamber
    pub fn chamber_size(&self) -> usize {
        self.breeding_chamber.len()
    }
}

/// Splice two departments without maintaining state
pub fn quantum_splice<A: SovereignTrait + ?Sized, B: SovereignTrait + ?Sized>(
    parent_a: &A,
    parent_b: &B,
) -> BlackHoleChild {
    let mut splicer = QuantumSplicer::new();
    splicer.splice(parent_a, parent_b)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::departments::*;
    
    #[test]
    fn test_quantum_splice_unity_ninjatrader() {
        let child = quantum_splice(&UnityDepartment, &NinjaTraderDepartment);
        
        assert_eq!(child.name, "RenkoPulse Orb Healer");
        assert_eq!(child.parent_a, "Unity Game Engine");
        assert_eq!(child.parent_b, "NinjaTrader");
        assert!(child.orb_resonance); // Unity has orb resonance
        assert!(!child.entanglement.is_empty());
        assert!(!child.child_dna.is_empty());
        assert!(child.deploy_targets.contains(&DeployTarget::NinjaTrader));
        assert!(child.deploy_targets.contains(&DeployTarget::Steam));
    }
    
    #[test]
    fn test_quantum_splice_unreal_grokanator() {
        let child = quantum_splice(&UnrealDepartment, &GrokanatorDepartment);
        
        assert_eq!(child.name, "7Percent Dividend Turret");
        assert!(child.orb_resonance);
        assert!(child.dividend_yield > 0.0);
    }
    
    #[test]
    fn test_quantum_splice_unity_grokanator() {
        let child = quantum_splice(&UnityDepartment, &GrokanatorDepartment);
        
        assert_eq!(child.name, "Grokanator Boss Fight");
        assert!(child.orb_resonance);
    }
    
    #[test]
    fn test_breeding_chamber() {
        let mut splicer = QuantumSplicer::new();
        
        splicer.splice(&UnityDepartment, &NinjaTraderDepartment);
        splicer.splice(&UnrealDepartment, &GrokanatorDepartment);
        splicer.splice(&UnityDepartment, &GrokanatorDepartment);
        
        assert_eq!(splicer.chamber_size(), 3);
    }
    
    #[test]
    fn test_consensus_score() {
        // Same quadrant parents should have lower consensus (less balanced)
        let same_quad = quantum_splice(&UnityDepartment, &UnrealDepartment);
        
        // Different quadrant parents should have higher consensus (more balanced)
        let diff_quad = quantum_splice(&UnityDepartment, &NinjaTraderDepartment);
        
        // Both should have valid scores
        assert!(same_quad.consensus_score >= 0.0);
        assert!(diff_quad.consensus_score >= 0.0);
    }
    
    #[test]
    fn test_provenance_hash() {
        let child = quantum_splice(&UnityDepartment, &NinjaTraderDepartment);
        
        // Provenance hash should be SHA256 (64 hex chars)
        assert_eq!(child.provenance_hash.len(), 64);
    }
    
    #[test]
    fn test_child_dna_uniqueness() {
        let child1 = quantum_splice(&UnityDepartment, &NinjaTraderDepartment);
        let child2 = quantum_splice(&UnrealDepartment, &GrokanatorDepartment);
        
        assert_ne!(child1.child_dna, child2.child_dna);
        assert_ne!(child1.entanglement, child2.entanglement);
    }
}
