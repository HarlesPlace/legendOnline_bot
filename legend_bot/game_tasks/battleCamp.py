from core.fixed_time_task import FixedTimeTask

from utils.general_use import go_to_Interface, by_chest_of_time
from utils.screenVision import exists, wait, find, wait_until_disappear
from utils.actions import wait_time, click, drag
from utils.regions import *
from datetime import time, datetime
from typing import override

class BattleCamp(FixedTimeTask):
    def __init__(self):
        super().__init__()
        self.allowed_time_ranges = [
            (time(11, 0), time(11, 8)),
            (time(21, 33), time(21, 41))
        ]
        self.allowed_weekdays = [0,1,2,3,4,5,6]
        self.priority = 0
    
    def _run_task(self):
        """
        Implementa a lógica para o campo de batalha, apenas para cumprir pontos de atividades por enquanto
        """
        print("Iniciando Campo de Batalha")
        go_to_Interface("castle")
        if by_chest_of_time(r"legend_bot\images\battle_camp\battleCampEventButton.png", confidence=0.73):
            if wait(r"legend_bot\images\battle_camp\battleCampEntraceWindowBar.png", timeout=120, region=TOP_BAR, confidence=0.8):
                if not exists(r"legend_bot\images\battle_camp\enterButton.png", region=CENTER, confidence=0.8):
                    drag(from_image = r"legend_bot\images\battle_camp\rollingBar.png", to_image_or_direction="down", confidence=0.8)
                    wait_time(2)
                if exists(r"legend_bot\images\battle_camp\enterButton.png", region=CENTER, confidence=0.8):
                    click(r"legend_bot\images\battle_camp\enterButton.png", region=CENTER, confidence=0.8)
                    wait_time(1)
                    if wait(r"legend_bot\images\battle_camp\inBattleCampIndicator.png", region=RIGHT_SIDE, timeout=150, confidence=0.7):
                        if click(r"legend_bot\images\battle_camp\exitBattleCampButton.png", region=BOTTOM_RIGHT, confidence=0.80):
                            wait_time(2)
                            if exists(r"legend_bot\images\battle_camp\exitWarn.png", region =FULL_SCREEN, cnfidence=0.7):
                                warn_region = find(r"legend_bot\images\battle_camp\exitWarn.png", region=FULL_SCREEN, confidence=0.7)
                                if click(r"legend_bot\images\battle_camp\confirmExitButton.png", region=warn_region, confidence=0.8):
                                    wait_time(2)
                                    if wait_until_disappear(r"legend_bot\images\battle_camp\inBattleCampIndicator.png", region=RIGHT_SIDE, timeout=60, confidence=0.7):
                                        print("Saindo do Campo de Batalha")
                                        wait_time(20)
                                        return True
                else:
                    print("Botão de entrada não encontrado")
                    return False
