from core.control import STOP, ERROR, PAUSED
from utils.general_use import prepare_window
import time

class TaskManager:
    def __init__(self, dailyTasks, fixedTasks, repeatableTasks, max_retries=3):
        self.dailyTasks = dailyTasks
        self.fixedTasks = fixedTasks
        self.repeatableTasks = repeatableTasks
        self.tasks = dailyTasks + fixedTasks + repeatableTasks
        self.currentTask = None
        self.errorTasks = []  # lista de tuplas (task, retries)
        self.lastTaskType = "Daily"
        self.max_retries = max_retries

    def executeTasks(self):
        while not STOP:
            if not ERROR and not PAUSED:
                runTask = self.determine_nextTask()
                if runTask:
                    self.currentTask = runTask
                    prepare_window()
                    print(f"[TAREFA] Executando: {runTask.__class__.__name__}")
                    success = runTask.run()
                    if not success:
                        self._handle_task_error(runTask)
                    self.currentTask = None
                else:
                    print("[TAREFA] Nenhuma tarefa elegível no momento.")
                    time.sleep(2)
            else:
                print("[INFO] Pausado ou em erro. Aguardando...")
                time.sleep(2)

    def _handle_task_error(self, task):
        for i, (t, count) in enumerate(self.errorTasks):
            if t == task:
                self.errorTasks[i] = (t, count + 1)
                return
        self.errorTasks.append((task, 1))

    def determine_nextTask(self):
        # 1. Tarefas de horário fixo têm prioridade
        fixed = self._get_runnable_task(self.fixedTasks)
        if fixed:
            return fixed

        # 2. Verifica se há tarefas elegíveis em cada grupo
        daily_task = self._get_runnable_task(self.dailyTasks)
        repeatable_task = self._get_runnable_task(self.repeatableTasks)

        # 3. Alternância entre tipos, mas prioriza a disponível
        if self.lastTaskType == "Daily":
            if repeatable_task:
                self.lastTaskType = "Repeatable"
                return repeatable_task
            elif daily_task:
                # Continua com Daily, já que Repeatable não está disponível
                return daily_task
        elif self.lastTaskType == "Repeatable":
            if daily_task:
                self.lastTaskType = "Daily"
                return daily_task
            elif repeatable_task:
                return repeatable_task

        # 4. Se nenhuma das anteriores, reexecutar tarefas com erro
        if self.errorTasks:
            task, retry_count = self.errorTasks.pop(0)
            if retry_count < self.max_retries:
                self.errorTasks.append((task, retry_count))
                print(f"[TAREFA] Reexecutando após erro: {task.__class__.__name__} (tentativa {retry_count + 1})")
                return task
            else:
                print(f"[ERRO] {task.__class__.__name__} excedeu número máximo de tentativas.")

        return None
    
    def _get_runnable_task(self, task_list):
        # Ordena as tasks por prioridade crescente
        sorted_tasks = sorted(task_list, key=lambda task: getattr(task, "priority", 5))  # prioridade padrão = 5
        for task in sorted_tasks:
            if task.should_run():
                print(f"[TAREFA] {task.__class__.__name__} deve rodar agora (prioridade {task.priority})")
                return task
        return None
