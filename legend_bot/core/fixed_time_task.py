from datetime import datetime
from core.base_task import BaseTask

class FixedTimeTask(BaseTask):
    def __init__(self, start_hour: int, end_hour: int, blackout_hours=None, allowed_weekdays=None):
        self.running = True
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.error = False
        self.blackout_hours = blackout_hours or []
        self.allowed_weekdays = allowed_weekdays

    def _is_in_blackout(self):
        current_hour = datetime.now().hour
        return any(start <= current_hour < end for start, end in self.blackout_hours)

    def _is_weekday_allowed(self):
        if self.allowed_weekdays is None:
            return True
        return datetime.now().weekday() in self.allowed_weekdays

    def should_run(self) -> bool:
        now_hour = datetime.now().hour
        in_time_range = self.start_hour <= now_hour < self.end_hour
        return in_time_range and not self._is_in_blackout() and self._is_weekday_allowed()