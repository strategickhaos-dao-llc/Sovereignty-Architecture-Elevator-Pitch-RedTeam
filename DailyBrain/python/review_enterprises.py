# python/review_enterprises.py
"""
ReviewEnterprisesTask: Reviews business/enterprise projects and initiatives.
Tracks multiple business ventures, side projects, and enterprise goals.
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

@dataclass
class EnterpriseProject:
    id: str
    name: str
    description: str
    status: str  # "ideation", "planning", "active", "paused", "completed", "archived"
    priority: int  # 1 = highest
    health: str  # "healthy", "at_risk", "critical"
    next_milestone: Optional[str]
    milestone_date: Optional[date]
    revenue_ytd: Decimal = Decimal('0')
    notes: Optional[str] = None

@dataclass
class EnterprisesContext:
    projects: List[EnterpriseProject]
    current_date: date
    show_archived: bool = False
    max_display: int = 5

@dataclass
class EnterprisesReviewResult:
    active_projects: List[EnterpriseProject]
    at_risk: List[EnterpriseProject]
    upcoming_milestones: List[EnterpriseProject]
    total_revenue: Decimal
    note: str

class ReviewEnterprisesTask:
    def run(self, ctx: EnterprisesContext) -> EnterprisesReviewResult:
        """
        Reviews enterprise projects and identifies priorities.
        """
        # Filter based on archived preference
        projects = ctx.projects
        if not ctx.show_archived:
            projects = [p for p in projects if p.status not in ("completed", "archived")]
        
        active = [p for p in projects if p.status == "active"]
        at_risk = [p for p in active if p.health in ("at_risk", "critical")]
        
        # Projects with upcoming milestones in next 30 days
        upcoming_milestones = []
        for p in active:
            if p.milestone_date:
                days_until = (p.milestone_date - ctx.current_date).days
                if 0 <= days_until <= 30:
                    upcoming_milestones.append(p)
        
        upcoming_milestones.sort(key=lambda x: x.milestone_date)
        
        total_revenue = sum((p.revenue_ytd for p in projects), Decimal('0'))
        
        # Generate summary
        notes = []
        if at_risk:
            notes.append(f"⚠️ {len(at_risk)} project(s) at risk!")
        notes.append(f"🏢 {len(active)} active project(s).")
        if upcoming_milestones:
            notes.append(f"🎯 {len(upcoming_milestones)} milestone(s) in next 30 days.")
        notes.append(f"💰 YTD Revenue: ${total_revenue:.2f}")
        
        note = " ".join(notes)
        
        return EnterprisesReviewResult(
            active_projects=active[:ctx.max_display],
            at_risk=at_risk,
            upcoming_milestones=upcoming_milestones,
            total_revenue=total_revenue,
            note=note
        )
    
    def format_projects(self, projects: List[EnterpriseProject], title: str = "Enterprise Projects") -> str:
        """
        Format projects for display.
        """
        if not projects:
            return f"=== {title} ===\nNo projects to display."
        
        health_emoji = {"healthy": "🟢", "at_risk": "🟡", "critical": "🔴"}
        status_emoji = {
            "ideation": "💡", "planning": "📝", "active": "🚀",
            "paused": "⏸️", "completed": "✅", "archived": "📦"
        }
        
        lines = [f"=== {title} ==="]
        for p in sorted(projects, key=lambda x: x.priority):
            h_icon = health_emoji.get(p.health, "⚪")
            s_icon = status_emoji.get(p.status, "❓")
            milestone = f" | Next: {p.next_milestone} ({p.milestone_date})" if p.next_milestone else ""
            lines.append(f"  {h_icon}{s_icon} {p.name}{milestone}")
            if p.revenue_ytd > 0:
                lines.append(f"       💰 ${p.revenue_ytd:.2f} YTD")
        
        return "\n".join(lines)
