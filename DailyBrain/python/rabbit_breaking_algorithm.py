# python/rabbit_breaking_algorithm.py
"""
RabbitBreakTask: Schedules micro-breaks throughout the day.
"Rabbit breaks" are quick 5-15 minute breaks to maintain productivity.
"""
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import List, Optional

@dataclass
class RabbitBreakContext:
    work_start: time
    work_end: time
    current_time: datetime
    break_interval_minutes: int = 90  # Pomodoro-style
    break_duration_minutes: int = 15
    excluded_times: List[tuple] = None  # List of (start, end) time tuples for meetings, etc.

@dataclass
class RabbitBreak:
    start_time: time
    end_time: time
    break_type: str  # "micro", "stretch", "walk", "hydrate"

@dataclass
class RabbitBreakResult:
    next_break: Optional[RabbitBreak]
    scheduled_breaks: List[RabbitBreak]
    note: str

class RabbitBreakTask:
    BREAK_TYPES = ["micro", "stretch", "walk", "hydrate"]
    
    def run(self, ctx: RabbitBreakContext) -> RabbitBreakResult:
        """
        Generates break schedule and identifies next upcoming break.
        """
        if ctx.excluded_times is None:
            ctx.excluded_times = []
        
        breaks = self._generate_breaks(ctx)
        next_break = self._find_next_break(breaks, ctx.current_time)
        
        if next_break:
            minutes_until = self._minutes_until(ctx.current_time.time(), next_break.start_time)
            note = f"Next break ({next_break.break_type}) in {minutes_until} minutes."
        else:
            note = "No more breaks scheduled for today."
        
        return RabbitBreakResult(
            next_break=next_break,
            scheduled_breaks=breaks,
            note=note
        )
    
    def _generate_breaks(self, ctx: RabbitBreakContext) -> List[RabbitBreak]:
        """
        Generate break schedule for the work period.
        """
        breaks = []
        current_minutes = ctx.work_start.hour * 60 + ctx.work_start.minute
        end_minutes = ctx.work_end.hour * 60 + ctx.work_end.minute
        break_index = 0
        
        while current_minutes + ctx.break_interval_minutes < end_minutes:
            current_minutes += ctx.break_interval_minutes
            
            start_time = time(hour=current_minutes // 60, minute=current_minutes % 60)
            end_time = time(
                hour=(current_minutes + ctx.break_duration_minutes) // 60,
                minute=(current_minutes + ctx.break_duration_minutes) % 60
            )
            
            # Check if break conflicts with excluded times
            if not self._is_excluded(start_time, ctx.excluded_times):
                break_type = self.BREAK_TYPES[break_index % len(self.BREAK_TYPES)]
                breaks.append(RabbitBreak(
                    start_time=start_time,
                    end_time=end_time,
                    break_type=break_type
                ))
                break_index += 1
        
        return breaks
    
    def _is_excluded(self, break_time: time, excluded: List[tuple]) -> bool:
        """
        Check if a time falls within any excluded period.
        """
        break_minutes = break_time.hour * 60 + break_time.minute
        
        for start, end in excluded:
            start_minutes = start.hour * 60 + start.minute
            end_minutes = end.hour * 60 + end.minute
            if start_minutes <= break_minutes <= end_minutes:
                return True
        return False
    
    def _find_next_break(self, breaks: List[RabbitBreak], current: datetime) -> Optional[RabbitBreak]:
        """
        Find the next upcoming break from the current time.
        """
        current_time = current.time()
        current_minutes = current_time.hour * 60 + current_time.minute
        
        for b in breaks:
            break_minutes = b.start_time.hour * 60 + b.start_time.minute
            if break_minutes > current_minutes:
                return b
        return None
    
    def _minutes_until(self, current: time, target: time) -> int:
        """
        Calculate minutes between two times.
        """
        current_minutes = current.hour * 60 + current.minute
        target_minutes = target.hour * 60 + target.minute
        return target_minutes - current_minutes
