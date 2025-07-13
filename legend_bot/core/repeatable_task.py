from core.base_task import BaseTask
from datetime import datetime, timedelta

class RepeatableTask(BaseTask):
    def __init__(self):
        self.running = True
        self.last_time_executed = None

    def should_run(self) -> bool:
        if self.last_time_executed is None:
            return True
        now = datetime.now()
        elapsed = now - self.last_time_executed
        return elapsed >= timedelta(minutes=30)

    def run(self):
        """
        Substitua este método nas subclasses com a lógica da tarefa.
        """
        print("Executando tarefa...")
        self.last_time_executed = datetime.now()