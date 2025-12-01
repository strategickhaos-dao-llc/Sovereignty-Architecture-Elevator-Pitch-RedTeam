//! JSON API layer for the Quantum Splicer
//!
//! Provides an HTTP server that accepts POST requests with two departments
//! and returns a BlackHoleChild JSON describing the spliced result.
//!
//! # Usage
//!
//! Start the server with:
//! ```bash
//! cargo run --release --features api --bin quantum_splicer_api
//! ```
//!
//! Then POST to `/splice`:
//! ```bash
//! curl -X POST http://localhost:3000/splice \
//!   -H "Content-Type: application/json" \
//!   -d '{"parent_a": "Unity", "parent_b": "NinjaTrader"}'
//! ```

#[cfg(feature = "api")]
pub mod server {
    use axum::{
        extract::State,
        http::StatusCode,
        response::{IntoResponse, Json},
        routing::{get, post},
        Router,
    };
    use serde::{Deserialize, Serialize};
    use std::sync::{Arc, Mutex};

    use crate::departments::*;
    use crate::splicer::{BlackHoleChild, QuantumSplicer};

    /// Request body for the splice endpoint
    #[derive(Debug, Deserialize)]
    pub struct SpliceRequest {
        /// Parent A department name (Unity, Unreal, NinjaTrader, Grokanator, or Prime)
        pub parent_a: String,
        /// Parent B department name
        pub parent_b: String,
    }

    /// Error response
    #[derive(Debug, Serialize)]
    pub struct ErrorResponse {
        pub error: String,
        pub valid_departments: Vec<&'static str>,
    }

    /// Health check response
    #[derive(Debug, Serialize)]
    pub struct HealthResponse {
        pub status: String,
        pub version: String,
        pub chamber_size: usize,
    }

    /// Shared application state
    pub struct AppState {
        pub splicer: Mutex<QuantumSplicer>,
    }

    /// Valid department names
    pub const VALID_DEPARTMENTS: &[&str] = &[
        "Unity",
        "Unreal",
        "NinjaTrader",
        "Grokanator",
        "Prime",
    ];

    /// Create the router with all endpoints
    pub fn create_router() -> Router {
        let state = Arc::new(AppState {
            splicer: Mutex::new(QuantumSplicer::new()),
        });

        Router::new()
            .route("/", get(root))
            .route("/health", get(health))
            .route("/splice", post(splice))
            .route("/departments", get(list_departments))
            .route("/chamber", get(list_chamber))
            .with_state(state)
    }

    /// Root endpoint
    async fn root() -> &'static str {
        r#"🌀 BLACK HOLE DNA SPLICER™ API v0.1.0

Endpoints:
  GET  /              - This help message
  GET  /health        - Health check
  GET  /departments   - List valid departments
  GET  /chamber       - List all offspring in breeding chamber
  POST /splice        - Splice two departments

Example:
  curl -X POST http://localhost:3000/splice \
    -H "Content-Type: application/json" \
    -d '{"parent_a": "Unity", "parent_b": "NinjaTrader"}'
"#
    }

    /// Health check endpoint
    async fn health(State(state): State<Arc<AppState>>) -> Json<HealthResponse> {
        let chamber_size = state.splicer.lock().unwrap().chamber_size();
        Json(HealthResponse {
            status: "healthy".to_string(),
            version: "0.1.0".to_string(),
            chamber_size,
        })
    }

    /// List valid departments
    async fn list_departments() -> Json<Vec<&'static str>> {
        Json(VALID_DEPARTMENTS.to_vec())
    }

    /// List all offspring in the breeding chamber
    async fn list_chamber(State(state): State<Arc<AppState>>) -> Json<Vec<BlackHoleChild>> {
        let splicer = state.splicer.lock().unwrap();
        let children: Vec<BlackHoleChild> = splicer
            .get_all_children()
            .into_iter()
            .cloned()
            .collect();
        Json(children)
    }

    /// Splice two departments
    async fn splice(
        State(state): State<Arc<AppState>>,
        Json(request): Json<SpliceRequest>,
    ) -> Result<Json<BlackHoleChild>, impl IntoResponse> {
        let mut splicer = state.splicer.lock().unwrap();

        // Helper to create department from name
        let get_department = |name: &str| -> Option<Box<dyn SovereignTrait + Send + Sync>> {
            match name.to_lowercase().as_str() {
                "unity" => Some(Box::new(UnityDepartment)),
                "unreal" => Some(Box::new(UnrealDepartment)),
                "ninjatrader" => Some(Box::new(NinjaTraderDepartment)),
                "grokanator" => Some(Box::new(GrokanatorDepartment)),
                "prime" => Some(Box::new(StrategickhaosPrime)),
                _ => None,
            }
        };

        let parent_a = match get_department(&request.parent_a) {
            Some(d) => d,
            None => {
                return Err((
                    StatusCode::BAD_REQUEST,
                    Json(ErrorResponse {
                        error: format!("Invalid department: {}", request.parent_a),
                        valid_departments: VALID_DEPARTMENTS.to_vec(),
                    }),
                ));
            }
        };

        let parent_b = match get_department(&request.parent_b) {
            Some(d) => d,
            None => {
                return Err((
                    StatusCode::BAD_REQUEST,
                    Json(ErrorResponse {
                        error: format!("Invalid department: {}", request.parent_b),
                        valid_departments: VALID_DEPARTMENTS.to_vec(),
                    }),
                ));
            }
        };

        let child = splicer.splice(parent_a.as_ref(), parent_b.as_ref());
        Ok(Json(child))
    }
}
