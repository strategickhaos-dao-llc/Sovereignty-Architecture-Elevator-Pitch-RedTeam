//! Quantum Splicer JSON API Server
//!
//! Start with: cargo run --release --features api --bin quantum_splicer_api
//!
//! Then POST to /splice:
//! ```bash
//! curl -X POST http://localhost:3000/splice \
//!   -H "Content-Type: application/json" \
//!   -d '{"parent_a": "Unity", "parent_b": "NinjaTrader"}'
//! ```

#[cfg(feature = "api")]
#[tokio::main]
async fn main() {
    use quantum_splicer::api::server::create_router;

    println!();
    println!("╔════════════════════════════════════════════════════════════════════╗");
    println!("║           🌀 BLACK HOLE DNA SPLICER™ API v0.1.0 🌀                 ║");
    println!("║         Department-Agnostic Synthesis Engine Server               ║");
    println!("╚════════════════════════════════════════════════════════════════════╝");
    println!();
    println!("  📡 Starting server on http://127.0.0.1:3000");
    println!();
    println!("  Endpoints:");
    println!("    GET  /              - Help message");
    println!("    GET  /health        - Health check");
    println!("    GET  /departments   - List valid departments");
    println!("    GET  /chamber       - List all offspring");
    println!("    POST /splice        - Splice two departments");
    println!();
    println!("  Example:");
    println!(r#"    curl -X POST http://localhost:3000/splice \"#);
    println!(r#"      -H "Content-Type: application/json" \"#);
    println!(r#"      -d '{{"parent_a": "Unity", "parent_b": "NinjaTrader"}}'"#);
    println!();
    println!("════════════════════════════════════════════════════════════════════");
    println!();

    let app = create_router();

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

#[cfg(not(feature = "api"))]
fn main() {
    eprintln!("Error: API feature is not enabled.");
    eprintln!("Run with: cargo run --release --features api --bin quantum_splicer_api");
    std::process::exit(1);
}
