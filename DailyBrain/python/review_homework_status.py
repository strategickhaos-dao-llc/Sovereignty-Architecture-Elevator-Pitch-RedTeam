# python/review_homework_status.py
"""
ReviewHomeworkTask: Reviews homework and assignment status.
Reads from JSON/DB/Obsidian vault and surfaces top priorities.
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

@dataclass
class HomeworkItem:
    id: str
    title: str
    subject: str
    due_date: date
    status: str  # "not_started", "in_progress", "completed"
    priority: int  # 1 = highest
    notes: Optional[str] = None

@dataclass
class HomeworkContext:
    items: List[HomeworkItem]
    current_date: date
    max_priorities: int = 3

@dataclass
class HomeworkReviewResult:
    overdue: List[HomeworkItem]
    due_today: List[HomeworkItem]
    upcoming: List[HomeworkItem]
    top_priorities: List[HomeworkItem]
    note: str

class ReviewHomeworkTask:
    def run(self, ctx: HomeworkContext) -> HomeworkReviewResult:
        """
        Reviews homework status and identifies priorities.
        """
        incomplete = [h for h in ctx.items if h.status != "completed"]
        
        overdue = [h for h in incomplete if h.due_date < ctx.current_date]
        due_today = [h for h in incomplete if h.due_date == ctx.current_date]
        upcoming = [h for h in incomplete if h.due_date > ctx.current_date]
        
        # Sort by priority and due date for top priorities
        sorted_items = sorted(
            incomplete,
            key=lambda x: (x.priority, x.due_date)
        )
        top_priorities = sorted_items[:ctx.max_priorities]
        
        # Generate summary note
        notes = []
        if overdue:
            notes.append(f"⚠️ {len(overdue)} OVERDUE item(s)!")
        if due_today:
            notes.append(f"📅 {len(due_today)} item(s) due TODAY.")
        if upcoming:
            notes.append(f"📋 {len(upcoming)} upcoming item(s).")
        
        note = " ".join(notes) if notes else "✅ All homework complete!"
        
        return HomeworkReviewResult(
            overdue=overdue,
            due_today=due_today,
            upcoming=upcoming,
            top_priorities=top_priorities,
            note=note
        )
    
    def format_priorities(self, priorities: List[HomeworkItem]) -> str:
        """
        Format top priorities for display.
        """
        if not priorities:
            return "No homework items to display."
        
        lines = ["=== Top Homework Priorities ==="]
        for i, item in enumerate(priorities, 1):
            status_emoji = {"not_started": "⬜", "in_progress": "🟡", "completed": "✅"}.get(item.status, "❓")
            lines.append(f"{i}. {status_emoji} [{item.subject}] {item.title} - Due: {item.due_date}")
        
        return "\n".join(lines)
