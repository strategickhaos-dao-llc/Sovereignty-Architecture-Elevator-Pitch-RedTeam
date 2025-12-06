// rust/src/meetings.rs
use chrono::{DateTime, Duration, Local};

#[derive(Clone, Debug)]
pub struct MeetingItem {
    pub id: String,
    pub title: String,
    pub start_time: DateTime<Local>,
    pub end_time: DateTime<Local>,
    pub location: String, // "zoom", "teams", "in_person", "phone"
    pub attendees: Vec<String>,
    pub agenda: Option<String>,
    pub prep_checklist: Option<Vec<String>>,
}

pub struct MeetingsContext {
    pub meetings: Vec<MeetingItem>,
    pub current_time: DateTime<Local>,
    pub prep_warning_minutes: i64,
}

pub struct MeetingsReviewResult {
    pub next_meeting: Option<MeetingItem>,
    pub today_meetings: Vec<MeetingItem>,
    pub needs_prep: Vec<MeetingItem>,
    pub minutes_until_next: i64,
    pub note: String,
}

pub struct MeetingsTask;

impl MeetingsTask {
    pub fn run(&self, ctx: &MeetingsContext) -> MeetingsReviewResult {
        let today = ctx.current_time.date_naive();
        let mut today_meetings: Vec<_> = ctx
            .meetings
            .iter()
            .filter(|m| {
                m.start_time.date_naive() == today && m.start_time > ctx.current_time
            })
            .cloned()
            .collect();

        today_meetings.sort_by_key(|m| m.start_time);

        let next_meeting = today_meetings.first().cloned();

        let prep_threshold = ctx.current_time + Duration::minutes(ctx.prep_warning_minutes);
        let needs_prep: Vec<_> = today_meetings
            .iter()
            .filter(|m| m.start_time <= prep_threshold && m.prep_checklist.is_some())
            .cloned()
            .collect();

        let minutes_until_next = if let Some(ref next) = next_meeting {
            (next.start_time - ctx.current_time).num_minutes()
        } else {
            -1
        };

        let mut notes = Vec::new();
        if !needs_prep.is_empty() {
            notes.push(format!("📋 {} meeting(s) need prep NOW!", needs_prep.len()));
        }
        if let Some(ref next) = next_meeting {
            notes.push(format!(
                "⏰ Next: '{}' in {} min.",
                next.title, minutes_until_next
            ));
        }
        notes.push(format!(
            "📅 {} meeting(s) remaining today.",
            today_meetings.len()
        ));

        let note = if notes.is_empty() {
            "🎉 No more meetings today!".to_string()
        } else {
            notes.join(" ")
        };

        MeetingsReviewResult {
            next_meeting,
            today_meetings,
            needs_prep,
            minutes_until_next,
            note,
        }
    }

    pub fn format_meeting(&self, meeting: &MeetingItem) -> String {
        let location_emoji = match meeting.location.as_str() {
            "zoom" => "📹",
            "teams" => "👥",
            "in_person" => "🏢",
            "phone" => "📞",
            _ => "📍",
        };

        let mut lines = vec![
            format!("=== {} ===", meeting.title),
            format!("  {} {}", location_emoji, meeting.location.to_uppercase()),
            format!(
                "  🕐 {} - {}",
                meeting.start_time.format("%H:%M"),
                meeting.end_time.format("%H:%M")
            ),
            format!("  👤 Attendees: {}", meeting.attendees.join(", ")),
        ];

        if let Some(ref agenda) = meeting.agenda {
            lines.push(format!("  📝 Agenda: {}", agenda));
        }

        if let Some(ref checklist) = meeting.prep_checklist {
            lines.push("  ✅ Prep Checklist:".to_string());
            for item in checklist {
                lines.push(format!("     - {}", item));
            }
        }

        lines.join("\n")
    }
}
