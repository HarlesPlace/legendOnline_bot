class TaskManager:
    def __init__(self, tasks):
        self.tasks = tasks

    def run_all(self):
        for task in self.tasks:
            task_name = task.__class__.__name__
            try:
                if task.should_run():
                    print(f"[TAREFA] Executando: {task_name}")
                    task.run()
                else:
                    print(f"[TAREFA] Ignorada (não deve rodar agora): {task_name}")
            except Exception as e:
                print(f"[ERRO] Falha ao executar {task_name}: {e}")
