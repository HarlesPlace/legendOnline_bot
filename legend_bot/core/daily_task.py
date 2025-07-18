from datetime import date
from core.base_task import BaseTask

class DailyTask(BaseTask):
    def __init__(self):
        self.running = True
        self.last_run_date = None

    def should_run(self) -> bool:
        today = date.today()
        return self.last_run_date != today

    def run(self):
        self._run_task()
        self.last_run_date = date.today()

    def _run_task(self):
        """Sobrescreva esse método com a lógica real da tarefa."""
        raise NotImplementedError