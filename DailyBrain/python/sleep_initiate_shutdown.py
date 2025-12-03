# python/sleep_initiate_shutdown.py
"""
SleepTask: Manages sleep initiation and shutdown routines.
Uses OS APIs to schedule shutdown and logs sleep time.
"""
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

@dataclass
class SleepContext:
    target_bedtime: time
    current_time: datetime
    shutdown_warning_minutes: int = 30

@dataclass
class SleepResult:
    should_initiate: bool
    minutes_until_shutdown: int
    note: str

class SleepTask:
    def run(self, ctx: SleepContext) -> SleepResult:
        """
        Determines if sleep shutdown should be initiated based on current time
        and target bedtime.
        """
        current = ctx.current_time.time()
        target = ctx.target_bedtime
        
        # Simple comparison (doesn't handle midnight crossing)
        current_minutes = current.hour * 60 + current.minute
        target_minutes = target.hour * 60 + target.minute
        
        minutes_remaining = target_minutes - current_minutes
        
        if minutes_remaining <= 0:
            return SleepResult(
                should_initiate=True,
                minutes_until_shutdown=0,
                note="Bedtime reached. Initiating shutdown sequence."
            )
        elif minutes_remaining <= ctx.shutdown_warning_minutes:
            return SleepResult(
                should_initiate=False,
                minutes_until_shutdown=minutes_remaining,
                note=f"Warning: {minutes_remaining} minutes until bedtime."
            )
        else:
            return SleepResult(
                should_initiate=False,
                minutes_until_shutdown=minutes_remaining,
                note=f"Bedtime in {minutes_remaining} minutes."
            )

    def log_sleep_time(self, sleep_time: datetime) -> None:
        """
        Logs the actual sleep time for tracking purposes.
        TODO: Integrate with database or file storage.
        """
        print(f"[SLEEP LOG] Sleep initiated at: {sleep_time.strftime('%Y-%m-%d %H:%M')}")
