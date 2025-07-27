from core.fixed_time_task import FixedTimeTask

from utils.general_use import go_to_Interface, open_map, by_map_go_to, by_chest_of_time
from utils.screenVision import exists, wait, find, wait_until_disappear
from utils.actions import wait_time, click, type_text
from utils.regions import *
from datetime import time

class AssassinationOfMidnight(FixedTimeTask):
    def __init__(self):
        super().__init__()
        self.allowed_time_ranges = [(time(15, 2), time(15, 15))]
        self.allowed_weekdays = [0,1,2,3,4,5,6]

    def _run_task(self):
        """
        Implementa a lógica para assassinato da meia noite
        """
        print("Iniciando assassinato da meia noite")
        go_to_Interface("castle")
        if by_chest_of_time(r"legend_bot\images\assassination_midnight\assassinEventButton.png", confidence=0.8):
            if wait(r"legend_bot\images\assassination_midnight\inEventIndicator.png", timeout=120, region=RIGHT_SIDE, confidence=0.8):
                atack_region=find(r"legend_bot\images\assassination_midnight\attackRegion.png", confidence=0.8, region=LEFT_SIDE)
                while (not exists(r"legend_bot\images\assassination_midnight\endAssassinationIndicator.png", confidence=0.8, region=TOP_BAR)) and self.running:
                    if exists(r"legend_bot\images\assassination_midnight\attackButton.png", confidence=0.85, region=atack_region):
                        click(r"legend_bot\images\assassination_midnight\attackButton.png", confidence=0.85, region=atack_region)
                        wait_time(2)
                    elif exists(r"legend_bot\images\assassination_midnight\inBattleIndicator.png", confidence=0.8, region=TOP_RIGHT):
                        if exists(r"legend_bot\images\assassination_midnight\autoFightButton.png", region=BOTTOM_RIGHT, confidence=0.83):
                            click(r"legend_bot\images\assassination_midnight\autoFightButton.png", region=BOTTOM_RIGHT, confidence=0.83)
                            wait_time(1)
                        wait_until_disappear(r"legend_bot\images\assassination_midnight\inBattleIndicator.png", confidence=0.8, region=TOP_RIGHT, timeout=120)
                    wait_time(3)
                try:
                    windowbar_region=find(r"legend_bot\images\assassination_midnight\endAssassinationIndicator.png", confidence=0.8, region=TOP_BAR)
                    click(r"legend_bot\images\assassination_midnight\exitAssassinationButton.png", confidence=0.8, region=windowbar_region)
                except:
                    click(r"legend_bot\images\assassination_midnight\exitAssassinationButton.png", confidence=0.8, region=TOP_RIGHT)
                wait_time(2)
        else:
            return False
        return True