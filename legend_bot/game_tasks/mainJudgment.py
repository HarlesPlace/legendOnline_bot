from core.daily_task import DailyTask
from utils.general_use import open_map, by_map_go_to
from utils.screenVision import exists, wait, find
from utils.actions import wait_time, click
from utils.regions import *

class MainJudgment(DailyTask):
    def __init__(self):
        super().__init__()
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 5

    def _run_task(self):
        if open_map():
            if by_map_go_to("JulgamentoPrincipal"):
                if wait(r"legend_bot\images\main_judgment\interfaceIndicator.png", confidence=0.8, timeout=30, region=FULL_SCREEN):
                    indicator_region = find(r"legend_bot\images\main_judgment\interfaceIndicator.png", confidence=0.8,region=FULL_SCREEN)
                    click(r"legend_bot\images\main_judgment\mainJudgmentButton.png", region=indicator_region, confidence=0.8)
                    if wait(r"legend_bot\images\main_judgment\windowBar.png", confidence=0.8, timeout=30, region=TOP_BAR):
                        windowBarRegion=find(r"legend_bot\images\main_judgment\windowBar.png", confidence=0.8, region=TOP_BAR)
                        engine=True
                        while engine and self.running:
                            if exists(r"legend_bot\images\main_judgment\prayButton.png", confidence=0.8, region=BOTTOM_BAR):
                                click(r"legend_bot\images\main_judgment\prayButton.png", confidence=0.8, region=BOTTOM_BAR)
                            else:
                                print("[JULGAMENTO PRINCIPAL] botão de oração não encontrado")
                                return False
                            if wait(r"legend_bot\images\main_judgment\prayWindowBar.png", timeout=30,region=TOP_BAR, confidence=0.8):
                                if exists(r"legend_bot\images\main_judgment\initPrayButton.png", confidence=0.8, region=BOTTOM_BAR):
                                    if click(r"legend_bot\images\main_judgment\initPrayButton.png", confidence=0.8, region=BOTTOM_BAR):
                                        wait_time(3)
                                        if exists(r"legend_bot\images\main_judgment\optionsBar.png", region=BOTTOM_BAR, confidence=0.8):
                                            menu_bar=find(r"legend_bot\images\main_judgment\optionsBar.png", region=BOTTOM_BAR, confidence=0.8)
                                            click(r"legend_bot\images\main_judgment\begButton.png", region=menu_bar, confidence=0.8)
                                            wait_time(3)
                                            click(r"legend_bot\images\main_judgment\finishPray.png", region=menu_bar, confidence=0.8)
                                            wait_time(3)
                                        else:
                                            engine=False
                                elif exists(r"legend_bot\images\main_judgment\optionsBar.png", confidence=0.8, region=BOTTOM_BAR):
                                    menu_bar=find(r"legend_bot\images\main_judgment\optionsBar.png", region=BOTTOM_BAR, confidence=0.8)
                                    click(r"legend_bot\images\main_judgment\begButton.png", region=menu_bar, confidence=0.8)
                                    wait_time(3)
                                    click(r"legend_bot\images\main_judgment\finishPray.png", region=menu_bar, confidence=0.8)
                                    wait_time(3)
                                if exists(r"legend_bot\images\main_judgment\prayWindowBar.png",region=TOP_BAR, confidence=0.8):
                                    prayBar_region = find(r"legend_bot\images\main_judgment\prayWindowBar.png",region=TOP_BAR, confidence=0.8)
                                    click(r"legend_bot\images\main_judgment\prayExitButton.png", region=prayBar_region, confidence=0.8)
                        click(r"legend_bot\images\main_judgment\exitButton.png", confidence=0.8, region=windowBarRegion)
                        return True
