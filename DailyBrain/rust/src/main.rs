// rust/src/main.rs
mod commute;
mod sleep;
mod reviews;
mod meetings;

use chrono::Local;
use commute::{CommuteAlgorithm, CommuteContext, Coordinates};

fn main() {
    let home = Coordinates { lat: 29.4241, lon: -98.4936 };
    let work = Coordinates { lat: 29.7604, lon: -95.3698 };
    let departure_time = Local::now();

    let ctx = CommuteContext {
        home,
        work,
        departure_time,
    };

    let algo = CommuteAlgorithm;
    let result = algo.estimate_commute(&ctx);

    println!("=== Commute (Rust) ===");
    println!("{}", result.note);
    println!("Duration (secs): {}", result.estimated_duration.as_secs());

    // Later:
    // run_sleep_task();
    // run_review_tasks();
    // run_meetings_task();
}
