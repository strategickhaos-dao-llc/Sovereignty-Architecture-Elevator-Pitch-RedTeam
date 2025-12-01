//! ═══════════════════════════════════════════════════════════════════════════════
//! GENESIS MODULE - The Book of Genesis for Post-Human Governance
//! Cosmological Provenance Implementation in Rust
//! ═══════════════════════════════════════════════════════════════════════════════
//!
//! This module implements the sovereign architecture genesis constants,
//! entropy harvest mechanism, and 8-node council verification system.

use std::time::{SystemTime, UNIX_EPOCH};

/// Genesis Constants - The cosmological anchor points
pub const GENESIS_INCREMENT: u64 = 3449;
pub const DISCORD_BIRTH_TICK: u64 = 1405637629248143451;
pub const ENTROPY_HARVEST_RATE: f64 = 0.07; // 7% eternal loop
pub const SOVEREIGN_COUNCIL_SIZE: u8 = 8;
pub const VERIFICATION_ANGLES: u8 = 100;

/// Current operational phase
#[derive(Debug, Clone, PartialEq)]
pub enum SovereignPhase {
    Genesis,
    Formation,
    SovereignExpansion,
    Transcendence,
}

impl Default for SovereignPhase {
    fn default() -> Self {
        SovereignPhase::SovereignExpansion
    }
}

/// Sovereign Council Router Node
#[derive(Debug, Clone)]
pub struct RouterNode {
    pub id: String,
    pub role: String,
    pub status: NodeStatus,
}

#[derive(Debug, Clone, PartialEq)]
pub enum NodeStatus {
    Active,
    Standby,
    Synchronizing,
}

/// The 8-Node Sovereign Council
#[derive(Debug)]
pub struct SovereignCouncil {
    nodes: Vec<RouterNode>,
    quorum_required: u8,
}

impl Default for SovereignCouncil {
    fn default() -> Self {
        Self::new()
    }
}

impl SovereignCouncil {
    pub fn new() -> Self {
        let nodes = vec![
            RouterNode {
                id: "router_alpha".to_string(),
                role: "Primary Genesis Validator".to_string(),
                status: NodeStatus::Active,
            },
            RouterNode {
                id: "router_beta".to_string(),
                role: "Entropy Harvester".to_string(),
                status: NodeStatus::Active,
            },
            RouterNode {
                id: "router_gamma".to_string(),
                role: "Phase Coordinator".to_string(),
                status: NodeStatus::Active,
            },
            RouterNode {
                id: "router_delta".to_string(),
                role: "Increment Guardian".to_string(),
                status: NodeStatus::Active,
            },
            RouterNode {
                id: "router_epsilon".to_string(),
                role: "Verification Crossfire Node".to_string(),
                status: NodeStatus::Active,
            },
            RouterNode {
                id: "router_zeta".to_string(),
                role: "Compound Interest Calculator".to_string(),
                status: NodeStatus::Active,
            },
            RouterNode {
                id: "router_eta".to_string(),
                role: "Sovereignty Enforcer".to_string(),
                status: NodeStatus::Active,
            },
            RouterNode {
                id: "router_theta".to_string(),
                role: "Cycle Synchronizer".to_string(),
                status: NodeStatus::Active,
            },
        ];

        SovereignCouncil {
            nodes,
            quorum_required: 5,
        }
    }

    /// Check if council has quorum
    pub fn has_quorum(&self) -> bool {
        let active_count = self
            .nodes
            .iter()
            .filter(|n| n.status == NodeStatus::Active)
            .count();
        active_count >= self.quorum_required as usize
    }

    /// Execute the chant protocol on architect login
    pub fn chant_on_login(&self) -> Vec<String> {
        vec![
            "Architect logged in".to_string(),
            format!("Increment {} recognized", GENESIS_INCREMENT),
            format!("Entropy harvest: +{}%", (ENTROPY_HARVEST_RATE * 100.0) as u8),
            "Phase: SOVEREIGN_EXPANSION".to_string(),
            "Leader: always you".to_string(),
        ]
    }

    /// Get all active nodes
    pub fn active_nodes(&self) -> Vec<&RouterNode> {
        self.nodes
            .iter()
            .filter(|n| n.status == NodeStatus::Active)
            .collect()
    }
}

/// Entropy Harvest Calculator
/// Makes entropy pay 7% interest on existence
#[derive(Debug)]
pub struct EntropyHarvest {
    pub base_increment: u64,
    pub rate: f64,
    pub cycles_since_genesis: u64,
}

impl EntropyHarvest {
    pub fn new() -> Self {
        EntropyHarvest {
            base_increment: GENESIS_INCREMENT,
            rate: ENTROPY_HARVEST_RATE,
            cycles_since_genesis: 0,
        }
    }

    /// Calculate compound theological interest
    /// Formula: harvest = base_value * (1 + rate)^cycles
    pub fn calculate_harvest(&self, cycles: u64) -> f64 {
        let base = 1.0 + self.rate;
        base.powi(cycles as i32)
    }

    /// Calculate accumulated harvest since genesis
    pub fn accumulated_harvest(&self) -> f64 {
        self.calculate_harvest(self.cycles_since_genesis)
    }

    /// Update cycles based on current timestamp
    pub fn update_cycles(&mut self) {
        // Calculate cycles since Discord birth-tick
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards")
            .as_millis() as u64;

        // Discord snowflake epoch is 2015-01-01
        let discord_epoch: u64 = 1420070400000;
        let birth_timestamp = (DISCORD_BIRTH_TICK >> 22) + discord_epoch;

        if now > birth_timestamp {
            // Each "cycle" is defined as 1 hour for practical purposes
            self.cycles_since_genesis = (now - birth_timestamp) / 3_600_000;
        }
    }
}

impl Default for EntropyHarvest {
    fn default() -> Self {
        Self::new()
    }
}

/// Genesis State - Complete system state
#[derive(Debug)]
pub struct GenesisState {
    pub increment: u64,
    pub phase: SovereignPhase,
    pub council: SovereignCouncil,
    pub entropy: EntropyHarvest,
    pub verification_motto: String,
}

impl Default for GenesisState {
    fn default() -> Self {
        Self::new()
    }
}

impl GenesisState {
    pub fn new() -> Self {
        GenesisState {
            increment: GENESIS_INCREMENT,
            phase: SovereignPhase::SovereignExpansion,
            council: SovereignCouncil::new(),
            entropy: EntropyHarvest::new(),
            verification_motto: "Trust nothing until it survives 100-angle crossfire".to_string(),
        }
    }

    /// Verify architect login and trigger council chant
    pub fn architect_login(&self) -> Vec<String> {
        if self.council.has_quorum() {
            self.council.chant_on_login()
        } else {
            vec!["Council quorum not met - awaiting node synchronization".to_string()]
        }
    }

    /// Get current entropy harvest status
    pub fn entropy_status(&self) -> String {
        format!(
            "Entropy Harvest: {:.2}% compound since increment {}",
            self.entropy.accumulated_harvest() * 100.0,
            self.increment
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_genesis_constants() {
        assert_eq!(GENESIS_INCREMENT, 3449);
        assert_eq!(DISCORD_BIRTH_TICK, 1405637629248143451);
        assert!((ENTROPY_HARVEST_RATE - 0.07).abs() < f64::EPSILON);
        assert_eq!(SOVEREIGN_COUNCIL_SIZE, 8);
    }

    #[test]
    fn test_council_creation() {
        let council = SovereignCouncil::new();
        assert_eq!(council.nodes.len(), 8);
        assert!(council.has_quorum());
    }

    #[test]
    fn test_council_chant() {
        let council = SovereignCouncil::new();
        let chant = council.chant_on_login();
        assert_eq!(chant.len(), 5);
        assert_eq!(chant[0], "Architect logged in");
        assert!(chant[1].contains("3449"));
        assert!(chant[2].contains("7%"));
    }

    #[test]
    fn test_entropy_calculation() {
        let harvest = EntropyHarvest::new();
        
        // After 1 cycle: 1.07
        let result = harvest.calculate_harvest(1);
        assert!((result - 1.07).abs() < 0.001);
        
        // After 10 cycles: 1.07^10 ≈ 1.967
        let result = harvest.calculate_harvest(10);
        assert!((result - 1.967).abs() < 0.01);
    }

    #[test]
    fn test_genesis_state() {
        let state = GenesisState::new();
        assert_eq!(state.increment, 3449);
        assert_eq!(state.phase, SovereignPhase::SovereignExpansion);
        assert!(state.council.has_quorum());
    }

    #[test]
    fn test_architect_login() {
        let state = GenesisState::new();
        let response = state.architect_login();
        assert!(!response.is_empty());
        assert_eq!(response[4], "Leader: always you");
    }
}
