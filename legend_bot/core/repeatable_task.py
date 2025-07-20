from datetime import datetime, timedelta
from core.base_task import BaseTask

class RepeatableTask(BaseTask):
    def __init__(self):
        self.running = True
        self.last_time_executed = None
        self.error = False
        self.timesExecuted = 0
        self.interval = timedelta(minutes=30)
        self.blackout_hours = []
        self.allowed_weekdays = []
        self.priority = 9 # Ex: int de 0 a 9, sendo 0 a maior prioridade

    def _is_in_blackout(self):
        current_hour = datetime.now().hour
        return any(start <= current_hour < end for start, end in self.blackout_hours)

    def _is_weekday_allowed(self):
        if self.allowed_weekdays is None:
            return True
        return datetime.now().weekday() in self.allowed_weekdays

    def should_run(self) -> bool:
        if not self._is_weekday_allowed() or self._is_in_blackout():
            return False
        if self.last_time_executed is None:
            return True
        return (datetime.now() - self.last_time_executed) >= self.interval

    def run(self):
        success = self._run_task()
        self.last_time_executed = datetime.now()
        if success:
            self.timesExecuted += 1
            return True
        else:
            self.error = True
            return False

    def _run_task(self):
        """Sobrescreva esse método com a lógica real da tarefa."""
        raise NotImplementedError