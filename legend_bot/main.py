from core.control import init_control
from core.task_manager import TaskManager
from core.recovery import init_errorMonitor
from utils.OCR import wait_for_text, find_text, read_text_from_screen
from utils.regions import TOP_LEFT, BOTTOM_RIGHT
from utils.general_use import prepare_window
from game_tasks.surroundingsSearch import SurroundingsSearch
def main():
    init_control()
    #init_errorMonitor()
    try:
        print("[BOT] Iniciando execução...")
        tarefas = []
        #manager = TaskManager(tarefas)
        #manager.run_all()
        print("[BOT] Execução finalizada.")
        #wait_for_text("Comunicado", invert=True, timeout=60, region=BOTTOM_RIGHT)
        #find_text(">> Arena dos Einherjar", invert=True, debug=True)
        prepare_window()
        #print(read_text_from_screen( invert=True))
        arenaPET_task = SurroundingsSearch()
        arenaPET_task.run()
    except KeyboardInterrupt:
        print("Bot finalizado com segurança.")

if __name__ == "__main__":
    main()
