from core.fixed_time_task import FixedTimeTask

from utils.general_use import go_to_Interface
from utils.screenVision import exists, wait, find
from utils.actions import wait_time, click
from utils.regions import *

class Fishing(FixedTimeTask):
    def _run_task(self):
        """
        Implementa a lógica para coletar XP farm
        """
        print("Coletando Navegação...")
        go_to_Interface("castle") 
        if exists(r"legend_bot\images\navigation\interfaceButton.png", confidence=0.8, region=FULL_SCREEN) and self.running:
            click(r"legend_bot\images\navigation\interfaceButton.png", confidence=0.8, region=FULL_SCREEN)
            if (wait(r"legend_bot\images\navigation\windowBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running):
                residenceWindow_region=find(r"legend_bot\images\navigation\windowBar.png", confidence=0.8, region=TOP_BAR)
                if click(r"legend_bot\images\navigation\navigationButton.png", confidence=0.8, region=TOP_BAR):
                    if wait(r"legend_bot\images\navigation\navigationWindowBar.png",confidence=0.8, timeout=30, region=TOP_BAR):
                        navigation_region=find(r"legend_bot\images\navigation\navigationWindowBar.png",confidence=0.8, region=TOP_BAR)
                        if exists(r"legend_bot\images\fishing\fishButton.png", confidence=0.9, region=FULL_SCREEN):
                            click(r"legend_bot\images\fishing\fishButton.png", confidence=0.9, region=FULL_SCREEN)
                            if wait(r"legend_bot\images\fishing\shipWindowBar.png", timeout=30, confidence=0.8, region=TOP_BAR):
                                if exists(r"legend_bot\images\fishing\ship.png", confidence=0.9,region=FULL_SCREEN):
                                    click(r"legend_bot\images\fishing\ship.png", confidence=0.9,region=FULL_SCREEN)
                                    wait_time(3)
                                    click(r"legend_bot\images\fishing\confirmShipButton.png", confidence=0.8, region=FULL_SCREEN)
                                    wait_time(2)
                                else:
                                    click(r"legend_bot\images\fishing\cancelShipButton.png", confidence=0.8, region=FULL_SCREEN)
                                    wait_time(3)
                            else:
                                print("[Pescaria] Interface de escolha de navio não abriu")
                                return False
                        click(r"legend_bot\images\navigation\residenceExitButton.png",region=navigation_region, confidence=0.9)
                        wait_time(3)
                    else:
                        print("[Pescaria] Janela de navegação não abriu")
                        return False
                click(r"legend_bot\images\navigation\residenceExitButton.png",region=residenceWindow_region, confidence=0.9)
                wait_time(3)
            else:
                print("[Pescaria] Área da residência não abriu")
                return False
        else:
            print("[Pescaria] Botão de entrada na residencia não encontrado na área do castelo")
            return False
        return True
