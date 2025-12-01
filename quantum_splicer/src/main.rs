//! Quantum Splicer - Black Hole DNA Splicer™
//!
//! Department-agnostic game/trading/AI breeding engine with revenue routing.
//!
//! Run with: cargo run --release

use quantum_splicer::{
    departments::*,
    splicer::QuantumSplicer,
};

fn main() {
    println!();
    println!("╔════════════════════════════════════════════════════════════════════╗");
    println!("║           🌀 BLACK HOLE DNA SPLICER™ v0.1.0 🌀                     ║");
    println!("║     Department-Agnostic Game/Trading/AI Breeding Engine           ║");
    println!("╚════════════════════════════════════════════════════════════════════╝");
    println!();
    
    let mut splicer = QuantumSplicer::new();
    
    // ═══════════════════════════════════════════════════════════════════
    // EXPERIMENT 1: Unity × NinjaTrader → RenkoPulse Orb Healer
    // ═══════════════════════════════════════════════════════════════════
    println!("┌────────────────────────────────────────────────────────────────────┐");
    println!("│ 🧬 EXPERIMENT 1: Unity × NinjaTrader                               │");
    println!("└────────────────────────────────────────────────────────────────────┘");
    println!();
    println!("  ⚛️  QUANTUM ENTANGLEMENT INITIATING...");
    println!();
    
    let child1 = splicer.splice(&UnityDepartment, &NinjaTraderDepartment);
    print_child_report(&child1);
    
    // ═══════════════════════════════════════════════════════════════════
    // EXPERIMENT 2: Unreal × Grokanator → 7Percent Dividend Turret
    // ═══════════════════════════════════════════════════════════════════
    println!("┌────────────────────────────────────────────────────────────────────┐");
    println!("│ 🧬 EXPERIMENT 2: Unreal × Grokanator                               │");
    println!("└────────────────────────────────────────────────────────────────────┘");
    println!();
    println!("  ⚛️  QUANTUM ENTANGLEMENT INITIATING...");
    println!();
    
    let child2 = splicer.splice(&UnrealDepartment, &GrokanatorDepartment);
    print_child_report(&child2);
    
    // ═══════════════════════════════════════════════════════════════════
    // EXPERIMENT 3: Unity × Grokanator → Grokanator Boss Fight
    // ═══════════════════════════════════════════════════════════════════
    println!("┌────────────────────────────────────────────────────────────────────┐");
    println!("│ 🧬 EXPERIMENT 3: Unity × Grokanator                                │");
    println!("└────────────────────────────────────────────────────────────────────┘");
    println!();
    println!("  ⚛️  QUANTUM ENTANGLEMENT INITIATING...");
    println!();
    
    let child3 = splicer.splice(&UnityDepartment, &GrokanatorDepartment);
    print_child_report(&child3);
    
    // ═══════════════════════════════════════════════════════════════════
    // BREEDING CHAMBER SUMMARY
    // ═══════════════════════════════════════════════════════════════════
    println!("╔════════════════════════════════════════════════════════════════════╗");
    println!("║                    🏛️  BREEDING CHAMBER SUMMARY                    ║");
    println!("╚════════════════════════════════════════════════════════════════════╝");
    println!();
    println!("  Total offspring in chamber: {}", splicer.chamber_size());
    println!();
    
    for child in splicer.get_all_children() {
        println!("  • {} ({} × {})", child.name, child.parent_a, child.parent_b);
    }
    
    println!();
    println!("════════════════════════════════════════════════════════════════════");
    println!("  🎯 This is a DESIGN GENERATOR - not a live trading system.");
    println!("  📋 Use the output to inform architecture decisions.");
    println!("  🔒 No customer funds, no auto-trading, no promised returns.");
    println!("════════════════════════════════════════════════════════════════════");
    println!();
}

fn print_child_report(child: &quantum_splicer::splicer::BlackHoleChild) {
    println!("  ╭─────────────────────────────────────────────────────────────────╮");
    println!("  │ 🌟 CHILD BORN: {}",  pad_right(&child.name, 42));
    println!("  ├─────────────────────────────────────────────────────────────────┤");
    println!("  │ Description: {}", truncate(&child.description, 45));
    println!("  │                                                                 │");
    println!("  │ 📊 DNA ANALYSIS                                                 │");
    println!("  │   Entanglement (SHA256):                                        │");
    println!("  │   {}...  │", &child.entanglement[..48]);
    println!("  │                                                                 │");
    println!("  │   Child DNA (SHA512):                                           │");
    println!("  │   {}...  │", &child.child_dna[..48]);
    println!("  │                                                                 │");
    println!("  │ 🎯 QUADRANT WEIGHTS                                             │");
    println!("  │   GameDev:      {:.1}%                                           │", child.quadrant_weights.game_dev * 100.0);
    println!("  │   Trading:      {:.1}%                                           │", child.quadrant_weights.trading * 100.0);
    println!("  │   Intelligence: {:.1}%                                           │", child.quadrant_weights.intelligence * 100.0);
    println!("  │   Hybrid:       {:.1}%                                           │", child.quadrant_weights.hybrid * 100.0);
    println!("  │                                                                 │");
    println!("  │ 📈 METRICS                                                      │");
    println!("  │   Consensus Score:  {:.1}%                                       │", child.consensus_score);
    println!("  │   Dividend Yield:   {:.2}%                                       │", child.dividend_yield);
    println!("  │   Orb Resonance:    {}                                          │", if child.orb_resonance { "✅ YES" } else { "❌ NO " });
    println!("  │                                                                 │");
    println!("  │ 🚀 DEPLOY TARGETS                                               │");
    for target in &child.deploy_targets {
        println!("  │   • {:?}", target);
    }
    println!("  │                                                                 │");
    println!("  │ 🔐 PROVENANCE                                                   │");
    println!("  │   {}...  │", &child.provenance_hash[..48]);
    println!("  ╰─────────────────────────────────────────────────────────────────╯");
    println!();
}

fn pad_right(s: &str, width: usize) -> String {
    if s.len() >= width {
        s[..width].to_string()
    } else {
        format!("{}{}", s, " ".repeat(width - s.len()))
    }
}

fn truncate(s: &str, max_len: usize) -> String {
    if s.len() <= max_len {
        s.to_string()
    } else {
        format!("{}...", &s[..max_len - 3])
    }
}
