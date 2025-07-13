from core.repeatable_task import RepeatableTask
from datetime import datetime

from utils.general_use import go_to_Interface, move_mouse_outside_screen
from utils.screenVision import exists, wait
from utils.actions import wait_time, click, click_all
from utils.regions import *

class GetTattoo(RepeatableTask):
    def run(self):
        """
        Implementa a lógica para coletar tatuagem
        """
        print("Coletando tatuagem...")
        go_to_Interface("castle")
        if exists("legend_bot\images\get_tattoo\interfaceButton.png", confidence=0.8, region=LEFT_SIDE) and self.running:
            click("legend_bot\images\get_tattoo\interfaceButton.png")
            if (wait("legend_bot\images\get_tattoo\windownBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running):
                move_mouse_outside_screen()
                if exists("legend_bot\images\get_tattoo\colectTattoo.png", confidence=0.8, region=FULL_SCREEN):
                    click_all("legend_bot\images\get_tattoo\colectTattoo.png", confidence=0.8, delay_between=3, debug=False)
                wait_time(5)
                click("legend_bot\images\get_tattoo\getTattooExitButton.png", confidence=0.9, region=TOP_RIGHT)
                wait_time(4)
            else:
                print("Janela de tatuagem não encontrada.")
                return False
        else:
            print("Botão de tatuagem não encontrado na região do castelo.")
            return False   
        self.last_time_executed = datetime.now()
        return True