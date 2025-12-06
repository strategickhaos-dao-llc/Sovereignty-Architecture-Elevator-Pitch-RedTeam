# python/review_bills.py
"""
ReviewBillsTask: Reviews upcoming bills and payment status.
Reads from JSON/DB and surfaces payment priorities.
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

@dataclass
class BillItem:
    id: str
    name: str
    amount: Decimal
    due_date: date
    category: str  # "utility", "subscription", "loan", "rent", "insurance", "other"
    is_paid: bool
    is_autopay: bool
    notes: Optional[str] = None

@dataclass
class BillsContext:
    bills: List[BillItem]
    current_date: date
    warning_days: int = 7  # Days before due date to warn

@dataclass
class BillsReviewResult:
    overdue: List[BillItem]
    due_soon: List[BillItem]
    upcoming: List[BillItem]
    total_due_soon: Decimal
    note: str

class ReviewBillsTask:
    def run(self, ctx: BillsContext) -> BillsReviewResult:
        """
        Reviews bills status and identifies payment priorities.
        """
        unpaid = [b for b in ctx.bills if not b.is_paid]
        
        overdue = [b for b in unpaid if b.due_date < ctx.current_date]
        
        warning_threshold = ctx.current_date
        due_soon = [b for b in unpaid 
                    if ctx.current_date <= b.due_date <= self._add_days(ctx.current_date, ctx.warning_days)]
        
        upcoming = [b for b in unpaid 
                    if b.due_date > self._add_days(ctx.current_date, ctx.warning_days)]
        
        total_due_soon = sum((b.amount for b in due_soon + overdue), Decimal('0'))
        
        # Generate summary note
        notes = []
        if overdue:
            total_overdue = sum(b.amount for b in overdue)
            notes.append(f"🚨 {len(overdue)} OVERDUE bill(s) totaling ${total_overdue:.2f}!")
        if due_soon:
            notes.append(f"⏰ {len(due_soon)} bill(s) due within {ctx.warning_days} days (${sum(b.amount for b in due_soon):.2f}).")
        
        # Note autopay bills
        autopay_due_soon = [b for b in due_soon if b.is_autopay]
        if autopay_due_soon:
            notes.append(f"💳 {len(autopay_due_soon)} on autopay.")
        
        note = " ".join(notes) if notes else "✅ All bills are current!"
        
        return BillsReviewResult(
            overdue=overdue,
            due_soon=due_soon,
            upcoming=upcoming,
            total_due_soon=total_due_soon,
            note=note
        )
    
    def _add_days(self, d: date, days: int) -> date:
        from datetime import timedelta
        return d + timedelta(days=days)
    
    def format_bills(self, bills: List[BillItem]) -> str:
        """
        Format bills for display.
        """
        if not bills:
            return "No bills to display."
        
        lines = ["=== Bills Summary ==="]
        for bill in sorted(bills, key=lambda x: x.due_date):
            autopay = "🔄" if bill.is_autopay else "  "
            lines.append(f"  {autopay} ${bill.amount:.2f} - {bill.name} ({bill.category}) - Due: {bill.due_date}")
        
        return "\n".join(lines)
