from legend_bot.core.base_task import BaseTask

class RepeatableTask(BaseTask):
    def should_run(self) -> bool:
        return True