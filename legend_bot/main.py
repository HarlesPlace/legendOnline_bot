from core.control import init_control
from core.task_manager import TaskManager
from core.recovery import init_errorMonitor

def main():
    init_control()
    #init_errorMonitor()
    try:
        print("[BOT] Iniciando execução...")
        tarefas = []
        manager = TaskManager(tarefas)
        manager.run_all()
        print("[BOT] Execução finalizada.")
    except KeyboardInterrupt:
        print("Bot finalizado com segurança.")

if __name__ == "__main__":
    main()
