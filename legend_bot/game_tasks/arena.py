from core.fixed_time_task import FixedTimeTask

from utils.general_use import go_to_Interface, open_map, by_map_go_to
from utils.screenVision import exists, wait, find, wait_until_disappear
from utils.actions import wait_time, click, type_text
from utils.regions import *
from datetime import time

class Arena(FixedTimeTask):
    def __init__(self):
        super().__init__()
        self.allowed_time_ranges = [
            (time(12, 2), time(13, 40)),
            (time(19, 0), time(19, 40))
        ]
        self.allowed_weekdays = [0,1,2,3,4,5,6]

    def _run_task(self):
        """
        Implementa a lógica para batalhar na arena
        """
        print("Iniciando arena")
        go_to_Interface("sky")
        if open_map():
            if by_map_go_to("CaminhoDaGloria"):
                if wait(r"legend_bot\images\arena\arenaInterfaceIndicator.png", timeout=90, region=FULL_SCREEN, confidence=0.8):
                    arena_region=find(r"legend_bot\images\arena\arenaInterfaceIndicator.png", region=FULL_SCREEN, confidence=0.8)
                    click(r"legend_bot\images\arena\coliseuButton.png", region= arena_region, confidence=0.8)
                    if wait(r"legend_bot\images\arena\arenaEntranceWindow.png", timeout=30, region=FULL_SCREEN,confidence=0.8):
                        entrance=find(r"legend_bot\images\arena\arenaEntranceWindow.png", region=FULL_SCREEN,confidence=0.8)
                        if click(r"legend_bot\images\arena\enterArenaButton.png", region=entrance, confidence=0.8):
                            if wait(r"legend_bot\images\arena\arenaWindowBar.png", region=TOP_BAR, confidence=0.8, timeout=60):
                                windowBar=find(r"legend_bot\images\arena\arenaWindowBar.png", region=TOP_BAR, confidence=0.8)
                                menu=find(r"legend_bot\images\arena\optionMenu.png", confidence=0.8, region=BOTTOM_RIGHT)
                                if click(r"legend_bot\images\arena\createRoomButton.png", region=menu, confidence=0.9):
                                    if wait(r"legend_bot\images\arena\inRoomIndicator.png", confidence=0.75, region=RIGHT_SIDE, timeout=60):
                                        inRoom_region=find(r"legend_bot\images\arena\inRoomIndicator.png", confidence=0.75, region=RIGHT_SIDE)
                                        if click(r"legend_bot\images\arena\lockRoomButton.png", confidence=0.8, region=inRoom_region):
                                            if wait(r"legend_bot\images\arena\passWordInterface.png", region=CENTER, confidence=0.8, timeout=20):
                                                passWord_region=find(r"legend_bot\images\arena\passWordInterface.png", region=CENTER, confidence=0.8)
                                                type_text("135790", 
                                                          BeforeImage_path = r"legend_bot\images\arena\passWordField.png",
                                                          AfterImage_path=r"legend_bot\images\arena\passWordConfirmerButton.png",
                                                          confidence=0.9)
                                                count=0
                                                while count<15 and self.running:
                                                    if click(r"legend_bot\images\arena\battleButton.png", region=inRoom_region, confidence=0.7):
                                                        wait_time(2)
                                                        if exists(r"legend_bot\images\arena\arenaCompletedIndicator.png", region=FULL_SCREEN, confidence=0.8):
                                                            outOfTimes_region=find(r"legend_bot\images\arena\arenaCompletedIndicator.png", region=FULL_SCREEN, confidence=0.8)
                                                            click(r"legend_bot\images\arena\cancelAtemptButton.png", region=outOfTimes_region, confidence=0.8)
                                                            break
                                                        if exists(r"legend_bot\images\arena\warnWindow.png", region=FULL_SCREEN, confidence=0.8):
                                                            warn_region=find(r"legend_bot\images\arena\warnWindow.png", region=FULL_SCREEN, confidence=0.8)
                                                            click(r"legend_bot\images\arena\dontWarnButton.png", region=warn_region, confidence=0.8)
                                                            wait_time(2)
                                                            click(r"legend_bot\images\arena\warnConfirm.png", region=warn_region, confidence=0.8)
                                                            wait_time(2)
                                                        if wait_until_disappear(r"legend_bot\images\arena\inRoomIndicator.png",region=inRoom_region, confidence=0.7, timeout=180):
                                                            if wait(r"legend_bot\images\arena\inBattleIndicator.png", region=TOP_BAR, confidence=0.88,timeout=60):
                                                                if exists(r"legend_bot\images\arena\autoFightButton.png", confidence=0.91, region=BOTTOM_RIGHT):
                                                                    click(r"legend_bot\images\arena\autoFightButton.png", confidence=0.91, region=BOTTOM_RIGHT)
                                                                wait(r"legend_bot\images\arena\inRoomIndicator.png",region=inRoom_region, confidence=0.7, timeout=240)
