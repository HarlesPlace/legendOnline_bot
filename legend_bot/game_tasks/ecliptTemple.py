from core.repeatable_task import RepeatableTask

from utils.general_use import open_map, by_map_go_to
from utils.screenVision import exists, wait, find, wait_until_disappear
from utils.actions import wait_time, click
from utils.regions import *
from datetime import timedelta

class EcliptTemple(RepeatableTask):
    def __init__(self):
        super().__init__()
        self.interval = timedelta(minutes=120)
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 5 

    def _run_task(self):
        """
        Implementa a lógica para coletar templo ecliptico
        """
        print("Coletando templo ecliptico...")
        if open_map():
            if by_map_go_to("TemploEcliptico"):
                if wait(r"legend_bot\images\eclipt_temple\interfaceIndicator.png", timeout=90, region=FULL_SCREEN, confidence=0.8):
                    ecliptTemple_region=find(r"legend_bot\images\eclipt_temple\interfaceIndicator.png", region=FULL_SCREEN, confidence=0.8)
                    click(r"legend_bot\images\eclipt_temple\ecliptTempleButton.png", region=ecliptTemple_region, confidence=0.8)
                    if wait(r"legend_bot\images\eclipt_temple\windowBar.png", timeout=90, region=TOP_BAR,confidence=0.8):
                        windowBar_region=find(r"legend_bot\images\eclipt_temple\windowBar.png", region=TOP_BAR, confidence=0.8)
                        engine=True
                        while engine and self.running:
                            if click(r"legend_bot\images\eclipt_temple\challengeButton.png", region = RIGHT_SIDE, confidence=0.8):
                                wait_time(3)
                                if exists(r"legend_bot\images\eclipt_temple\outOfEnergyWarn.png", region=FULL_SCREEN, confidence=0.8):
                                    outOfEnergyWarn_region = find(r"legend_bot\images\eclipt_temple\outOfEnergyWarn.png", region=FULL_SCREEN, confidence=0.8)
                                    click(r"legend_bot\images\eclipt_temple\cancelButton.png", region=outOfEnergyWarn_region, confidence=0.8)
                                    wait_time(1)
                                    break
                                if wait(r"legend_bot\images\eclipt_temple\inBattleIndicator.png", timeout=60, region=TOP_RIGHT,confidence=0.8):
                                    if exists(r"legend_bot\images\eclipt_temple\autoFightButton.png", region=BOTTOM_RIGHT, confidence=0.9):
                                        click(r"legend_bot\images\eclipt_temple\autoFightButton.png", region=BOTTOM_RIGHT, confidence=0.9)
                                    wait_until_disappear(r"legend_bot\images\eclipt_temple\inBattleIndicator.png", timeout=180, region=TOP_RIGHT, confidence=0.8)
                                wait(r"legend_bot\images\eclipt_temple\windowBar.png", timeout=180, region=TOP_BAR,confidence=0.8)
                                if exists(r"legend_bot\images\eclipt_temple\hiddenEventWarn.png", region=FULL_SCREEN, confidence=0.8):
                                    warn_region = find(r"legend_bot\images\eclipt_temple\hiddenEventWarn.png", region=FULL_SCREEN, confidence=0.8)
                                    if click(r"legend_bot\images\eclipt_temple\confirmeHiddenEvent.png", region=warn_region, confidence=0.8):
                                        wait_time(10)
                                        if exists(r"legend_bot\images\eclipt_temple\inBattleIndicator.png", region=TOP_RIGHT,confidence=0.8):
                                            if exists(r"legend_bot\images\eclipt_temple\autoFightButton.png", region=BOTTOM_RIGHT, confidence=0.9):
                                                click(r"legend_bot\images\eclipt_temple\autoFightButton.png", region=BOTTOM_RIGHT, confidence=0.9)
                                            wait_until_disappear(r"legend_bot\images\eclipt_temple\inBattleIndicator.png", timeout=180, region=TOP_RIGHT, confidence=0.8)
                                        if not exists(r"legend_bot\images\eclipt_temple\windowBar.png", region=TOP_BAR,confidence=0.8):
                                            wait(r"legend_bot\images\eclipt_temple\windowBar.png", timeout=60, region=TOP_BAR, confidence=0.8)
                        click(r"legend_bot\images\eclipt_temple\exitButton.png", region=windowBar_region, confidence=0.8)
                        wait_time(2)
        return True

