from datetime import datetime
from core.base_task import BaseTask

class FixedTimeTask(BaseTask):
    def __init__(self, start_hour: int, end_hour: int):
        self.running = True
        self.start_hour = start_hour
        self.end_hour = end_hour

    def should_run(self) -> bool:
        now = datetime.now().hour
        return self.start_hour <= now < self.end_hour