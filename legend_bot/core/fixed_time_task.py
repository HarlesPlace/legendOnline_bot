from datetime import datetime
from core.base_task import BaseTask

class FixedTimeTask(BaseTask):
    def __init__(self):
        self.running = True
        self.error = False
        self.done = False
        self.allowed_time_ranges = []  # Lista de tuplas (start_time, end_time)
        self.allowed_weekdays = None   # Lista de ints de 0 (segunda) a 6 (domingo)
        self.priority = 9 # Ex: int de 0 a 9, sendo 0 a maior prioridade

    def _is_time_allowed(self):
        now = datetime.now().time()
        return any(start <= now < end for start, end in self.allowed_time_ranges)

    def _is_weekday_allowed(self):
        if self.allowed_weekdays is None:
            return True
        return datetime.now().weekday() in self.allowed_weekdays

    def should_run(self) -> bool:
        return self._is_time_allowed() and self._is_weekday_allowed() and not self.done

    def run(self):
        success = self._run_task()
        if success:
            self.done = True
            return True
        else:
            self.error = True
            return False

    def _run_task(self):
        raise NotImplementedError