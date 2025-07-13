from core.repeatable_task import RepeatableTask
from datetime import datetime

from utils.general_use import move_mouse_outside_screen, find_in_eventBar
from utils.screenVision import exists, wait
from utils.actions import wait_time, click
from utils.regions import *

class CollectSummer(RepeatableTask):
    def run(self):
        """
        Implementa a lógica para coletar o evento de verão.
        """
        print("Coletando evento de verão...")
        find_in_eventBar("legend_bot\images\colect_Summer\colectSummerInterfaceButton.png")
        if exists("legend_bot\images\colect_Summer\colectSummerInterfaceButton.png",confidence=0.8, debug=False, region=TOP_BAR) and self.running:
            click("legend_bot\images\colect_Summer\colectSummerInterfaceButton.png",confidence=0.8, region=TOP_BAR)
            if (wait("legend_bot\images\colect_Summer\windowBar.png", timeout=60, confidence=0.8, debug=False, region=TOP_BAR) and self.running):
                if exists("legend_bot\images\colect_Summer\colectButton.png", confidence=0.8, debug=False, region=FULL_SCREEN) and self.running:
                    click("legend_bot\images\colect_Summer\colectButton.png", confidence=0.8, region=FULL_SCREEN)
                    wait_time(5)
                if exists("legend_bot\game_tasks\colectSummer.py", confidence=0.8, debug=False, region=FULL_SCREEN) and self.running:
                    click("legend_bot\game_tasks\colectSummer.py", confidence=0.8, region=FULL_SCREEN)
                    wait_time(5)
                click("legend_bot\images\colect_Summer\chest.png", confidence=0.8, region=TOP_RIGHT)
                wait_time(3)
                move_mouse_outside_screen()
                click("legend_bot\images\colect_Summer\colectSummerExitButton.png", confidence=0.8, region=TOP_RIGHT)
                wait_time(3)
            else:
                print("[ERRO] A janela de coleta de verão não foi encontrada ou a tarefa não está em execução.")
                return False
        else:
            print("[INFO] Botão de entrada na coleta verão não encontrado ou a tarefa não está em execução.")
            return False
        
        self.last_time_executed = datetime.now()
        return True
