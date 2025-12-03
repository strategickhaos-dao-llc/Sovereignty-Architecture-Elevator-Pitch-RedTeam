# python/meetings.py
"""
MeetingsTask: Manages meetings and preparation checklists.
Integrates with Google Calendar / Outlook (stub implementation).
"""
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import List, Optional

@dataclass
class MeetingItem:
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    location: str  # "zoom", "teams", "in_person", "phone"
    attendees: List[str]
    agenda: Optional[str] = None
    prep_checklist: Optional[List[str]] = None
    notes: Optional[str] = None

@dataclass
class MeetingsContext:
    meetings: List[MeetingItem]
    current_time: datetime
    prep_warning_minutes: int = 30

@dataclass
class MeetingsReviewResult:
    next_meeting: Optional[MeetingItem]
    today_meetings: List[MeetingItem]
    needs_prep: List[MeetingItem]
    minutes_until_next: int
    note: str

class MeetingsTask:
    def run(self, ctx: MeetingsContext) -> MeetingsReviewResult:
        """
        Reviews meetings and identifies preparation needs.
        """
        today = ctx.current_time.date()
        today_meetings = [
            m for m in ctx.meetings 
            if m.start_time.date() == today and m.start_time > ctx.current_time
        ]
        today_meetings.sort(key=lambda x: x.start_time)
        
        next_meeting = today_meetings[0] if today_meetings else None
        
        # Find meetings needing prep (within warning window)
        prep_threshold = ctx.current_time + timedelta(minutes=ctx.prep_warning_minutes)
        needs_prep = [
            m for m in today_meetings
            if m.start_time <= prep_threshold and m.prep_checklist
        ]
        
        # Calculate minutes until next meeting
        if next_meeting:
            delta = next_meeting.start_time - ctx.current_time
            minutes_until_next = int(delta.total_seconds() / 60)
        else:
            minutes_until_next = -1
        
        # Generate summary
        notes = []
        if needs_prep:
            notes.append(f"📋 {len(needs_prep)} meeting(s) need prep NOW!")
        if next_meeting:
            notes.append(f"⏰ Next: '{next_meeting.title}' in {minutes_until_next} min.")
        notes.append(f"📅 {len(today_meetings)} meeting(s) remaining today.")
        
        note = " ".join(notes) if notes else "🎉 No more meetings today!"
        
        return MeetingsReviewResult(
            next_meeting=next_meeting,
            today_meetings=today_meetings,
            needs_prep=needs_prep,
            minutes_until_next=minutes_until_next,
            note=note
        )
    
    def format_meeting(self, meeting: MeetingItem) -> str:
        """
        Format a single meeting with all details.
        """
        location_emoji = {
            "zoom": "📹", "teams": "👥", "in_person": "🏢", "phone": "📞"
        }.get(meeting.location, "📍")
        
        lines = [
            f"=== {meeting.title} ===",
            f"  {location_emoji} {meeting.location.upper()}",
            f"  🕐 {meeting.start_time.strftime('%H:%M')} - {meeting.end_time.strftime('%H:%M')}",
            f"  👤 Attendees: {', '.join(meeting.attendees)}"
        ]
        
        if meeting.agenda:
            lines.append(f"  📝 Agenda: {meeting.agenda}")
        
        if meeting.prep_checklist:
            lines.append("  ✅ Prep Checklist:")
            for item in meeting.prep_checklist:
                lines.append(f"     - {item}")
        
        return "\n".join(lines)
    
    def format_day_schedule(self, meetings: List[MeetingItem]) -> str:
        """
        Format all meetings for the day.
        """
        if not meetings:
            return "=== Today's Schedule ===\nNo meetings scheduled."
        
        lines = ["=== Today's Schedule ==="]
        for m in sorted(meetings, key=lambda x: x.start_time):
            duration = (m.end_time - m.start_time).total_seconds() / 60
            lines.append(
                f"  {m.start_time.strftime('%H:%M')} - {m.title} ({int(duration)} min)"
            )
        
        return "\n".join(lines)
