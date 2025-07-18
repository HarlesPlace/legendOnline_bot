from core.repeatable_task import RepeatableTask
from datetime import datetime

from utils.general_use import go_to_Interface
from utils.screenVision import exists, wait, find
from utils.actions import wait_time, click, click_all
from utils.regions import *

class XPfarmColector(RepeatableTask):
    def _run_task(self):
        """
        Implementa a lógica para coletar XP farm
        """
        print("Coletando XP farm...")
        go_to_Interface("castle") 
        if exists("legend_bot\images\plant_crops\interfaceButton.png", confidence=0.8, region=FULL_SCREEN) and self.running:
            click("legend_bot\images\plant_crops\interfaceButton.png", confidence=0.8, region=FULL_SCREEN)
            if (wait("legend_bot\images\plant_crops\windowBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running):
                if exists("legend_bot\images\plant_crops\farmButton.png", confidence=0.8, region=BOTTOM_RIGHT) and self.running:
                    click("legend_bot\images\plant_crops\farmButton.png", confidence=0.8, region=BOTTOM_RIGHT)
                    if wait("legend_bot\images\plant_crops\farmWindowBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running:
                        if exists("legend_bot\images\plant_crops\returnHomeButton", confidence=0.8, region=BOTTOM_RIGHT) and self.running:
                            click("legend_bot\images\plant_crops\returnHomeButton", confidence=0.8, region=BOTTOM_RIGHT) 
                            wait_time(3)
                        if exists("legend_bot\images\plant_crops\colectCropIndicator.png", confidence=0.8, region=BOTTOM_RIGHT) and self.running:
                            click("legend_bot\images\plant_crops\colectCropIndicator.png", confidence=0.8, region=BOTTOM_RIGHT)
                            wait_time(5)
                        if exists("legend_bot\images\plant_crops\optionsMenu.png", confidence=0.8, region=BOTTOM_RIGHT) and self.running:
                            option_region=find("legend_bot\images\plant_crops\optionsMenu.png", confidence=0.8, region=BOTTOM_RIGHT)
                            click("legend_bot\images\plant_crops\storeButton.png", confidence=0.9, region=option_region)
                            if wait("legend_bot\images\plant_crops\storeWindowBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running:
                                if exists("legend_bot\images\plant_crops\superMedalSeed.png", confidence=0.8, region=RIGHT_SIDE) and self.running:
                                    click("legend_bot\images\plant_crops\superMedalSeed.png", confidence=0.8, region=RIGHT_SIDE)
                                    wait_time(3)
                                elif exists("legend_bot\images\plant_crops\medalSeed.png", confidence=0.8, region=RIGHT_SIDE) and self.running:
                                    click("legend_bot\images\plant_crops\medalSeed.png", confidence=0.8, region=RIGHT_SIDE)
                                    wait_time(3)
                                    
                                click_all("legend_bot\images\plant_crops\freeSoilIndicator.png", confidence=0.73)
                                wait_time(3)
                                bar=find("legend_bot\images\plant_crops\storeWindowBar.png", confidence=0.8, region=TOP_BAR)
                                click("legend_bot\images\plant_crops\storeExitButton.png", confidence=0.8, region=bar)
                                wait_time(2)
                                bar=find("legend_bot\images\plant_crops\farmWindowBar.png", confidence=0.8, region=TOP_BAR)
                                click("legend_bot\images\plant_crops\farmExitButton.png", confidence=0.8, region=bar)
                                wait_time(2)
                                bar=find("legend_bot\images\plant_crops\windowBar.png", confidence=0.8, region=TOP_BAR)
                                click("legend_bot\images\plant_crops\exitButton.png", confidence=0.8, region=bar)
                                wait_time(2)

                            else:
                                print("Janela de loja não encontrada.")
                                return False                                  
                    else:
                        print("Janela de coleta de XP farm não encontrada.")
                        return False
                else:
                    print("Botão de XP farm não encontrado na região inferior direita.")
                    return False
            else:
                print("Janela de XP farm não encontrada.")
                return False
        else:
            print("Botão de XP farm não encontrado na região do castelo.")
            return False

        self.last_time_executed = datetime.now()
        return True
        