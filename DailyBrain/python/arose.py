# python/arose.py
"""
AroseTask: Tracks wake-up time and logs first interaction of the day.
Could integrate with phone/PC first activity detection.
"""
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

@dataclass
class AroseContext:
    target_wakeup: time
    current_time: datetime
    first_interaction_time: Optional[datetime] = None

@dataclass
class AroseResult:
    is_awake: bool
    on_schedule: bool
    deviation_minutes: int
    note: str

class AroseTask:
    def run(self, ctx: AroseContext) -> AroseResult:
        """
        Logs wake time and checks if user is on schedule.
        """
        if ctx.first_interaction_time is None:
            return AroseResult(
                is_awake=False,
                on_schedule=False,
                deviation_minutes=0,
                note="No interaction detected yet. User may still be asleep."
            )
        
        actual_wake = ctx.first_interaction_time.time()
        target = ctx.target_wakeup
        
        actual_minutes = actual_wake.hour * 60 + actual_wake.minute
        target_minutes = target.hour * 60 + target.minute
        
        deviation = actual_minutes - target_minutes
        on_schedule = abs(deviation) <= 15  # 15-minute grace period
        
        if deviation < 0:
            note = f"Woke up {abs(deviation)} minutes EARLY. Good job!"
        elif deviation > 0:
            note = f"Woke up {deviation} minutes LATE."
        else:
            note = "Woke up exactly on time!"
        
        return AroseResult(
            is_awake=True,
            on_schedule=on_schedule,
            deviation_minutes=deviation,
            note=note
        )

    def log_wake_time(self, wake_time: datetime) -> None:
        """
        Logs the actual wake time for tracking purposes.
        TODO: Integrate with database or file storage.
        """
        print(f"[AROSE LOG] Wake detected at: {wake_time.strftime('%Y-%m-%d %H:%M')}")
