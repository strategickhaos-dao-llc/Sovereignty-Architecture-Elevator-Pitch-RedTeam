//! Quantum Splicer - Department-agnostic game/trading/AI breeding engine
//!
//! # Overview
//! 
//! This crate provides a generic synthesis engine that can combine any two
//! subsystem configurations (departments) and generate a structured "design child"
//! with DNA hashing, quadrant alignment, and deployment targets.
//!
//! # Quick Start
//!
//! ```rust
//! use quantum_splicer::{QuantumSplicer, departments::*};
//!
//! let mut splicer = QuantumSplicer::new();
//! let child = splicer.splice(&UnityDepartment, &NinjaTraderDepartment);
//! println!("Child DNA: {}", child.child_dna);
//! ```

pub mod departments;
pub mod splicer;

#[cfg(feature = "api")]
pub mod api;

pub use departments::*;
pub use splicer::*;
