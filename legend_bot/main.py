from core.control import init_control
from core.task_manager import TaskManager
from core.recovery import init_errorMonitor
from utils.OCR import wait_for_text, find_text
from utils.regions import TOP_LEFT, BOTTOM_RIGHT
from utils.general_use import prepare_window
def main():
    init_control()
    #init_errorMonitor()
    try:
        print("[BOT] Iniciando execução...")
        tarefas = []
        manager = TaskManager(tarefas)
        #manager.run_all()
        print("[BOT] Execução finalizada.")
        #wait_for_text("Comunicado", invert=True, timeout=60, region=BOTTOM_RIGHT)
        #find_text("Equipamentos", invert=True, debug=True)
        prepare_window()
    except KeyboardInterrupt:
        print("Bot finalizado com segurança.")

if __name__ == "__main__":
    main()
