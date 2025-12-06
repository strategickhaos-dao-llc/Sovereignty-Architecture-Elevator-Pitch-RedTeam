// rust/src/commute.rs
use std::time::Duration;
use chrono::{DateTime, Local};

#[derive(Clone, Copy, Debug)]
pub struct Coordinates {
    pub lat: f64,
    pub lon: f64,
}

pub struct CommuteContext {
    pub home: Coordinates,
    pub work: Coordinates,
    pub departure_time: DateTime<Local>,
}

pub struct CommuteResult {
    pub estimated_duration: Duration,
    pub eta: DateTime<Local>,
    pub note: String,
}

pub struct CommuteAlgorithm;

impl CommuteAlgorithm {
    pub fn estimate_commute(&self, ctx: &CommuteContext) -> CommuteResult {
        let distance_km = Self::haversine(ctx.home, ctx.work);
        let hours = distance_km / 40.0_f64;
        let secs = (hours * 3600.0_f64) as u64;
        let duration = Duration::from_secs(secs);
        let eta = ctx.departure_time + chrono::Duration::from_std(duration).unwrap();

        let note = format!("Distance ~{:.1} km, ETA at {}", distance_km, eta.format("%H:%M"));

        CommuteResult {
            estimated_duration: duration,
            eta,
            note,
        }
    }

    fn haversine(a: Coordinates, b: Coordinates) -> f64 {
        let r = 6371.0_f64; // km
        let dlat = (b.lat - a.lat).to_radians();
        let dlon = (b.lon - a.lon).to_radians();
        let lat1 = a.lat.to_radians();
        let lat2 = b.lat.to_radians();

        let h = (dlat / 2.0).sin().powi(2)
            + lat1.cos() * lat2.cos() * (dlon / 2.0).sin().powi(2);
        2.0 * r * (h.sqrt().asin())
    }
}
