from datetime import date, datetime
from core.base_task import BaseTask

class DailyTask(BaseTask):
    def __init__(self, blackout_hours=None, allowed_weekdays=None):
        self.running = True
        self.last_run_date = None
        self.error = False
        self.blackout_hours = blackout_hours or []
        self.allowed_weekdays = allowed_weekdays  # Ex: [0, 1, 2, 3, 4] para dias úteis

    def _is_in_blackout(self):
        current_hour = datetime.now().hour
        return any(start <= current_hour < end for start, end in self.blackout_hours)

    def _is_weekday_allowed(self):
        if self.allowed_weekdays is None:
            return True  # Se não especificado, permite qualquer dia
        return datetime.now().weekday() in self.allowed_weekdays

    def should_run(self) -> bool:
        today = date.today()
        if self.last_run_date == today:
            return False
        return not self._is_in_blackout() and self._is_weekday_allowed()

    def run(self):
        self._run_task()
        self.last_run_date = date.today()

    def _run_task(self):
        """Sobrescreva esse método com a lógica real da tarefa."""
        raise NotImplementedError