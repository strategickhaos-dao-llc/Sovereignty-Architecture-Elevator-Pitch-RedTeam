// rust/src/sleep.rs
use chrono::{DateTime, Local, NaiveTime, Timelike};

pub struct SleepContext {
    pub target_bedtime: NaiveTime,
    pub current_time: DateTime<Local>,
    pub shutdown_warning_minutes: i32,
}

pub struct SleepResult {
    pub should_initiate: bool,
    pub minutes_until_shutdown: i32,
    pub note: String,
}

pub struct SleepTask;

impl SleepTask {
    pub fn run(&self, ctx: &SleepContext) -> SleepResult {
        let current = ctx.current_time.time();
        let target = ctx.target_bedtime;

        let current_minutes = current.hour() as i32 * 60 + current.minute() as i32;
        let target_minutes = target.hour() as i32 * 60 + target.minute() as i32;

        // Handle midnight crossing: if target is smaller than current,
        // it means bedtime is after midnight (e.g., target 1:00 AM, current 11:00 PM)
        let minutes_remaining = if target_minutes < current_minutes {
            // Add 24 hours worth of minutes for next-day bedtime
            (24 * 60 - current_minutes) + target_minutes
        } else {
            target_minutes - current_minutes
        };

        if minutes_remaining <= 0 {
            SleepResult {
                should_initiate: true,
                minutes_until_shutdown: 0,
                note: "Bedtime reached. Initiating shutdown sequence.".to_string(),
            }
        } else if minutes_remaining <= ctx.shutdown_warning_minutes {
            SleepResult {
                should_initiate: false,
                minutes_until_shutdown: minutes_remaining,
                note: format!("Warning: {} minutes until bedtime.", minutes_remaining),
            }
        } else {
            SleepResult {
                should_initiate: false,
                minutes_until_shutdown: minutes_remaining,
                note: format!("Bedtime in {} minutes.", minutes_remaining),
            }
        }
    }

    pub fn log_sleep_time(&self, sleep_time: DateTime<Local>) {
        println!(
            "[SLEEP LOG] Sleep initiated at: {}",
            sleep_time.format("%Y-%m-%d %H:%M")
        );
    }
}
