from core.fixed_time_task import FixedTimeTask

from utils.general_use import go_to_Interface, by_chest_of_time
from utils.screenVision import exists, wait, find
from utils.actions import wait_time, click
from utils.regions import *
from datetime import time, datetime
from typing import override

class GlobalBoss(FixedTimeTask):
    def __init__(self):
        super().__init__()
        self.allowed_time_ranges = [
            (time(11, 0), time(11, 8)),
            (time(21, 33), time(21, 41))
        ]
        self.allowed_weekdays = [0,1,2,3,4,5,6]
        self.priority = 0
        self.done_morning = False
        self.done_night = False
    
    def _get_current_slot(self):
        now = datetime.now().time()
        for idx, (start, end) in enumerate(self.allowed_time_ranges):
            if start <= now <= end:
                return idx  # 0 para manhã, 1 para noite
        return None

    @override
    def should_run(self) -> bool:
        slot = self._get_current_slot()
        if not self._is_weekday_allowed() or slot is None:
            return False

        if slot == 0 and not self.done_morning:
            return True
        elif slot == 1 and not self.done_night:
            return True
        return False
    
    @override
    def run(self):
        slot = self._get_current_slot()
        if slot is None:
            return False

        success = self._run_task()
        if success:
            if slot == 0:
                self.done_morning = True
            elif slot == 1:
                self.done_night = True
            return True
        else:
            self.error = True
            return False

    def _run_task(self):
        """
        Implementa a lógica para chefão Global
        """
        print("Iniciando Chefão Global")
        go_to_Interface("castle")
        if by_chest_of_time(r"legend_bot\images\global_boss\globalBossEventButton.png", confidence=0.8):
            if wait(r"legend_bot\images\global_boss\entranceWindowBar.png", timeout=120, region=TOP_BAR, confidence=0.8):
                if click(r"legend_bot\images\global_boss\participateButton.png", region =CENTER, confidence=0.9):
                    wait_time(2)
                    if wait(r"legend_bot\images\global_boss\inGlobalBossNightIndicator.png", timeout=120, region=TOP_BAR, confidence=0.6):
                        inGlobalBoss_region =find(r"legend_bot\images\global_boss\inGlobalBossNightIndicator.png", region=TOP_BAR, confidence=0.6)
                        while not exists(r"legend_bot\images\global_boss\conclusionIndicator.png", region=FULL_SCREEN, confidence=0.6):
                            if exists(r"legend_bot\images\global_boss\notInFightIndicator.png", region=BOTTOM_RIGHT, confidence=0.7):
                                click(r"legend_bot\images\global_boss\clickHereFight.png", region=inGlobalBoss_region, confidence=0.65)
                                wait_time(3)
                            else:
                                if exists(r"legend_bot\images\global_boss\autoFightButton.png", region=BOTTOM_RIGHT, confidence=0.85):
                                    click(r"legend_bot\images\global_boss\autoFightButton.png", region=BOTTOM_RIGHT, confidence=0.85)
                                    wait_time(3)
                                else:
                                    wait_time(5)
                        conclusion_region = find(r"legend_bot\images\global_boss\conclusionIndicator.png", region=FULL_SCREEN, confidence=0.6)
                        if conclusion_region:
                            click(r"legend_bot\images\global_boss\confirmButton.png", region=conclusion_region, confidence=0.8)
                        else:
                            print("Não foi possível encontrar o indicador de conclusão.")
                            click(r"legend_bot\images\global_boss\confirmButton.png", region=FULL_SCREEN, confidence=0.8)
        return True

                            
