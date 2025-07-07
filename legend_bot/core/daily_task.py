from datetime import date
from legend_bot.core.base_task import BaseTask

class DailyTask(BaseTask):
    def __init__(self):
        self.last_run_date = None

    def should_run(self) -> bool:
        today = date.today()
        return self.last_run_date != today

    def run(self):
        self.last_run_date = date.today()
        self._run_task()

    def _run_task(self):
        """Sobrescreva esse método com a lógica real da tarefa."""
        raise NotImplementedError