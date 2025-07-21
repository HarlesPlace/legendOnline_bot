from core.repeatable_task import RepeatableTask

from utils.general_use import move_mouse_outside_screen, find_in_eventBar
from utils.screenVision import exists, wait
from utils.actions import wait_time, click
from utils.regions import *
from datetime import timedelta

class CollectSummer(RepeatableTask):
    def __init__(self):
        super().__init__()
        self.interval = timedelta(minutes=30)
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 1 

    def _run_task(self):
        """
        Implementa a lógica para coletar o evento de verão.
        """
        print("Coletando evento de verão...")
        find_in_eventBar(r"legend_bot\images\colect_Summer\colectSummerInterfaceButton.png")
        if exists(r"legend_bot\images\colect_Summer\colectSummerInterfaceButton.png",confidence=0.8, region=TOP_BAR) and self.running:
            click(r"legend_bot\images\colect_Summer\colectSummerInterfaceButton.png",confidence=0.8, region=TOP_BAR)
            if (wait(r"legend_bot\images\colect_Summer\windowBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running):
                if exists(r"legend_bot\images\colect_Summer\colectButton.png", confidence=0.8, region=FULL_SCREEN) and self.running:
                    click(r"legend_bot\images\colect_Summer\colectButton.png", confidence=0.8, region=FULL_SCREEN)
                    wait_time(5)
                if exists(r"legend_bot\images\colect_Summer\selectionButton.png", confidence=0.8, region=FULL_SCREEN) and self.running:
                    click(r"legend_bot\images\colect_Summer\selectionButton.png", confidence=0.8, region=FULL_SCREEN)
                    wait_time(5)
                click(r"legend_bot\images\colect_Summer\chest.png", confidence=0.8, region=TOP_RIGHT)
                wait_time(3)
                move_mouse_outside_screen()
                click(r"legend_bot\images\colect_Summer\colectSummerExitButton.png", confidence=0.8, region=TOP_RIGHT)
                wait_time(3)
            else:
                print("[ERRO] A janela de coleta de verão não foi encontrada ou a tarefa não está em execução.")
                return False
        else:
            print("[INFO] Coleta verão não está presente no momento")
        
        return True
