from core.control import init_control
from core.task_manager import TaskManager
from core.recovery import init_errorMonitor
from utils.OCR import wait_for_text, find_text
from utils.regions import TOP_LEFT
def main():
    init_control()
    #init_errorMonitor()
    try:
        print("[BOT] Iniciando execução...")
        tarefas = []
        manager = TaskManager(tarefas)
        #manager.run_all()
        print("[BOT] Execução finalizada.")
        wait_for_text("80Prefeitura", invert=False, timeout=60, region=TOP_LEFT)
        find_text("80Prefeitura", region=TOP_LEFT, invert=True, debug=False)
    except KeyboardInterrupt:
        print("Bot finalizado com segurança.")

if __name__ == "__main__":
    main()
