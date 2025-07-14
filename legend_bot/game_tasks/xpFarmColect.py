from core.repeatable_task import RepeatableTask
from datetime import datetime

from utils.general_use import go_to_Interface
from utils.screenVision import exists, wait, find, list_all
from utils.actions import wait_time, click, click_position
from utils.regions import *

class XPfarmColector(RepeatableTask):
    def _run_task(self):
        """
        Implementa a lógica para coletar XP farm
        """
        print("Coletando XP farm...")
        go_to_Interface("castle") 
        if exists(r"legend_bot\images\xp_farmer_colector\interfaceButton.png", confidence=0.8, region=FULL_SCREEN) and self.running:
            click(r"legend_bot\images\xp_farmer_colector\interfaceButton.png", confidence=0.8, region=FULL_SCREEN)
            if (wait(r"legend_bot\images\xp_farmer_colector\windowBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running):
                if exists(r"legend_bot\images\xp_farmer_colector\farmButton.png", confidence=0.8, region=BOTTOM_RIGHT) and self.running:
                    click(r"legend_bot\images\xp_farmer_colector\farmButton.png", confidence=0.8, region=BOTTOM_RIGHT)
                    if wait(r"legend_bot\images\xp_farmer_colector\farmWindowBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running:
                        click(r"legend_bot\images\xp_farmer_colector\colectButton.png", confidence=0.8, region=BOTTOM_RIGHT)
                        if exists(r"legend_bot\images\xp_farmer_colector\endFriendListIndicator.png",confidence=0.98, region=BOTTOM_RIGHT) and self.running:
                            endListFriendIndicator=find(r"legend_bot\images\xp_farmer_colector\endFriendListIndicator.png", confidence=0.98, region=BOTTOM_RIGHT)
                            click(r"legend_bot\images\xp_farmer_colector\friendListBeginButton.png", confidence=0.98, region=endListFriendIndicator)
                            wait_time(3)
                        else:
                            print("Indicador de fim da lista de amigos não encontrado.")
                        # Coleta de XP farm    
                        while not exists(r"legend_bot\images\xp_farmer_colector\endFriendListIndicator2.png",confidence=0.99,region=BOTTOM_RIGHT) and self.running:     
                            for iten in list_all(r"legend_bot\images\xp_farmer_colector\treeColectorIndicator.png", confidence=0.8):
                                if self.running:
                                    click_position(iten)
                                    wait_time(2)
                                    click(r"legend_bot\images\xp_farmer_colector\colectButton.png", confidence=0.8, region=BOTTOM_RIGHT)
                                else:
                                    break

                            for iten in list_all(r"legend_bot\images\xp_farmer_colector\revivePlantIndicator.png", confidence=0.8):
                                if self.running:
                                    click_position(iten)
                                    wait_time(2)
                                    click(r"legend_bot\images\xp_farmer_colector\colectButton.png", confidence=0.8, region=BOTTOM_RIGHT)
                                else:
                                    break
                            
                            for iten in list_all(r"legend_bot\images\xp_farmer_colector\getFromFriendIndicator.png", confidence=0.9):
                                if self.running:
                                    click_position(iten)
                                    wait_time(2)
                                    click(r"legend_bot\images\xp_farmer_colector\colectButton.png", confidence=0.8, region=BOTTOM_RIGHT)
                                else:
                                    break
                            
                            for iten in list_all(r"legend_bot\images\xp_farmer_colector\bugIndicator.png", confidence=0.9):
                                if self.running:
                                    click_position(iten)
                                    wait_time(2)
                                    click(r"legend_bot\images\xp_farmer_colector\colectButton.png", confidence=0.8, region=BOTTOM_RIGHT)
                                else:
                                    break
                            
                            for iten in list_all(r"legend_bot\images\xp_farmer_colector\grassIndicator.png", confidence=0.9):
                                if self.running:
                                    click_position(iten)
                                    wait_time(2)
                                    click(r"legend_bot\images\xp_farmer_colector\colectButton.png", confidence=0.8, region=BOTTOM_RIGHT)
                                else:
                                    break
                            
                            click(r"legend_bot\images\xp_farmer_colector\nextPageButton.png", confidence=0.9, region=BOTTOM_RIGHT)
                        click(r"legend_bot\images\xp_farmer_colector\farmExitButton.png", confidence=0.9, region=TOP_RIGHT)
                        wait_time(4)
                        click(r"legend_bot\images\xp_farmer_colector\residenceExitButton.png", confidence=0.9, region=TOP_RIGHT)
                        wait_time(4)    
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