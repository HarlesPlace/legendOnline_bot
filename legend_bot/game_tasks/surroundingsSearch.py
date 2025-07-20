from core.daily_task import DailyTask

from utils.general_use import go_to_Interface, move_mouse_outside_screen
from utils.screenVision import wait, wait_until_disappear, exists
from utils.actions import wait_time, click
from utils.regions import *


class SurroundingsSearch(DailyTask):
    def __init__(self):
        super().__init__()
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 5

    def _run_task(self):
        """
        Implementa a lógica para coletar nas escavações na redondeza.
        """
        print("Coletando escavações na redondeza...")
        if go_to_Interface("castle"):
            if click(r"legend_bot\images\surroundings_search\surroundsButton.png", region=BOTTOM_RIGHT, confidence=0.8):
                if wait(r"legend_bot\images\surroundings_search\inSurroundIndicator.png", region=TOP_RIGHT, confidence=0.8, timeout=60):
                    if click(r"legend_bot\images\surroundings_search\exploreButton.png", region=BOTTOM_RIGHT, confidence=0.8):
                        if wait(r"legend_bot\images\surroundings_search\bootsButton.png", confidence=0.8, region=BOTTOM_BAR,timeout=15):
                            if click(r"legend_bot\images\surroundings_search\bootsButton.png", confidence=0.8, region=BOTTOM_BAR):
                                count=0
                                while count<30 and self.running:
                                    if exists(r"legend_bot\images\surroundings_search\endColectIndicator.png", confidence=0.8, region=BOTTOM_BAR):
                                        break
                                    if wait(r"legend_bot\images\surroundings_search\colectButton.png",timeout=120, confidence=0.8, region=BOTTOM_BAR):
                                        if click(r"legend_bot\images\surroundings_search\colectButton.png", confidence=0.8, region=BOTTOM_BAR):
                                            wait_time(0.5)
                                            move_mouse_outside_screen()
                                            if wait_until_disappear(r"legend_bot\images\surroundings_search\colectButton.png", confidence=0.6, region=BOTTOM_BAR,timeout=30):
                                                print("[Escavação arredores] Escavação realizada com sucesso")
                                                count+=1
                                            else:
                                                print("[Escavação arredores] Pode ter ocorrido de uma escavação estar muito proxima de outra")
                                                count+=1
                                        else:
                                            print("[Escavação arredores] Botão de coleta não encontrado para pressionar")
                                            return False
                                    else:
                                        print("[Escavação arredores] Escavação demorou além do ideal")
                                        return False
                                if click(r"legend_bot\images\surroundings_search\toCastleButton.png", region=BOTTOM_RIGHT, confidence=0.9):
                                    wait_time(5)
                                    return True
                                else:
                                    print("[Escavação arredores] Botão de retorno para castelo não encontrado")
                                    return False
                            else:
                                print("[Escavação arredores] Botão de exploração automática não detectado")
                                return False
                        else:
                            print("[Escavação arredores] Interface de exploração não detectada")
                            return False
                    else:
                        print("[Escavação arredores] Não foi possível clicar no botão para começar a explorar")
                        return False
                else:
                    print("[Escavação arredores] Esperava entrar nos arredores, mas não ocorreu")
                    return False
            else:
                print("[Escavação arredores] Botão para arredores não encontrado")
                return False
