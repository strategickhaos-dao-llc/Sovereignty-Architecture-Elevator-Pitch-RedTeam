# python/review_todos.py
"""
ReviewTodosTask: Reviews personal to-do items and tasks.
Reads from JSON/DB/Obsidian vault and surfaces priorities.
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

@dataclass
class TodoItem:
    id: str
    title: str
    description: Optional[str]
    due_date: Optional[date]
    created_date: date
    status: str  # "pending", "in_progress", "completed", "cancelled"
    priority: str  # "low", "medium", "high", "urgent"
    context: str  # "home", "work", "errands", "personal"
    tags: List[str] = None

@dataclass
class TodosContext:
    todos: List[TodoItem]
    current_date: date
    filter_context: Optional[str] = None
    max_display: int = 5

@dataclass
class TodosReviewResult:
    urgent: List[TodoItem]
    today: List[TodoItem]
    overdue: List[TodoItem]
    next_actions: List[TodoItem]
    note: str

class ReviewTodosTask:
    PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    
    def run(self, ctx: TodosContext) -> TodosReviewResult:
        """
        Reviews todos and identifies priorities using GTD-like methodology.
        """
        active = [t for t in ctx.todos if t.status in ("pending", "in_progress")]
        
        # Apply context filter if specified
        if ctx.filter_context:
            active = [t for t in active if t.context == ctx.filter_context]
        
        urgent = [t for t in active if t.priority == "urgent"]
        
        overdue = [t for t in active if t.due_date and t.due_date < ctx.current_date]
        
        today = [t for t in active if t.due_date == ctx.current_date]
        
        # Next actions: sorted by priority, then by creation date
        sorted_todos = sorted(
            active,
            key=lambda x: (self.PRIORITY_ORDER.get(x.priority, 99), x.created_date)
        )
        next_actions = sorted_todos[:ctx.max_display]
        
        # Generate summary
        notes = []
        if urgent:
            notes.append(f"🔴 {len(urgent)} URGENT item(s)!")
        if overdue:
            notes.append(f"⚠️ {len(overdue)} overdue item(s).")
        if today:
            notes.append(f"📅 {len(today)} item(s) due today.")
        
        total_active = len(active)
        notes.append(f"📋 {total_active} total active items.")
        
        note = " ".join(notes)
        
        return TodosReviewResult(
            urgent=urgent,
            today=today,
            overdue=overdue,
            next_actions=next_actions,
            note=note
        )
    
    def format_todos(self, todos: List[TodoItem], title: str = "To-Do List") -> str:
        """
        Format todos for display.
        """
        if not todos:
            return f"=== {title} ===\nNo items to display."
        
        priority_emoji = {"urgent": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
        status_emoji = {"pending": "⬜", "in_progress": "🔄", "completed": "✅", "cancelled": "❌"}
        
        lines = [f"=== {title} ==="]
        for i, todo in enumerate(todos, 1):
            p_icon = priority_emoji.get(todo.priority, "⚪")
            s_icon = status_emoji.get(todo.status, "❓")
            due = f" (Due: {todo.due_date})" if todo.due_date else ""
            lines.append(f"{i}. {p_icon}{s_icon} [{todo.context}] {todo.title}{due}")
        
        return "\n".join(lines)
